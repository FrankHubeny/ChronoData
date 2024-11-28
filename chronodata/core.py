# Licensed under a 3-clause BSD style license - see LICENSE.md
"""Read and write methods for chronology files."""

import logging
import json
from pathlib import Path
from typing import Any

from chronodata.constants import (
    Arg,
    Calendar,
    Column,
    Issue,
    Key,
    Line,
    String,
    Tag,
    Unit,
    Value,
)
from chronodata.messages import Msg


class Base:
    """Load a chronology from a file or create an empty chronology."""

    def __init__(
        self,
        name: str = Value.EMPTY,
        filename: str = Value.EMPTY,
        calendar: dict[str, Any] = Calendar.GREGORIAN,
    ) -> None:
        self.chron: dict[str, Any] = {}
        self.chron_name: str = name
        self.strict: bool = calendar[Key.STRICT]
        self.filename: str = filename
        if self.filename[-Arg.JSONLEN :] == Arg.JSON:
            self.filename_type = Arg.JSON
        elif self.filename[-Arg.GEDLEN :] == Arg.GED:
            self.filename_type = Arg.GED
        else:
            self.filename_type = Value.EMPTY
        self.filename_type: str = Value.EMPTY
        self.ged_data: list[str] = []
        self.ged_splitdata: list[list[tuple]] = []
        self.ged_issues: list[list[int, str]] = []
        self.ged_in_version: str = ''
        self.post: str = calendar[Key.POST]
        self.postlen: int = len(self.post)
        self.pre: str = calendar[Key.PRE]
        self.prelen: int = len(self.pre)
        if self.filename == Value.EMPTY:
            logging.info(Msg.STARTED.format(self.chron_name))
        elif self.filename_type == Arg.JSON:
            self.read_json()
            logging.info(Msg.LOADED.format(self.chron_name, filename))
        elif self.filename_type == Arg.GED:
            self.chron = self.read_ged()
            logging.info(Msg.LOADED.format(self.chron_name, filename))
        else:
            logging.warning(Msg.UNRECOGNIZED.format(self.filename))

    def __str__(self) -> str:
        return json.dumps(self.chron)

    def read_json(self) -> list:
        with Path.open(Path(self.filename), Arg.READ) as file:
            self.chron = json.load(file)
            file.close()
        self.cal_name = self.chron[Key.CAL][Key.NAME]
        self.chron_name = self.chron[Key.NAME]
        self.post = self.chron[Key.CAL][Key.POST]
        self.postlen = len(self.post)
        self.pre = self.chron[Key.CAL][Key.PRE]
        self.prelen = len(self.pre)


    def write_json(self, filename: str = Value.EMPTY) -> None:
        mode: str = Arg.WRITE
        if filename == Value.EMPTY:
            filename = self.filename
        with Path.open(Path(filename), mode) as file:
            json.dump(self.chron, file)
            file.close()


    def read_ged(self) -> list:
        """Read and validate the GEDCOM file."""

        with Path.open(Path(self.filename), Arg.READ) as file:
            data = file.readlines()
            file.close()
        # Split each line into components and remove terminator.
        for i in data:
            self.ged_splitdata.append(i.replace('\n', '').split(' ', 2))
        # Check the level for bad increments and starting point.
        level: int = 0
        for index, value in enumerate(self.ged_splitdata, start=1):
            if index == 1 and value[0] != '0':
                self.ged_issues.append([index, Issue.NO_ZERO])
            elif int(value[0]) > level + 1:
                self.ged_issues.append([index, Issue.BAD_INC])
            elif int(value[0]) < 0:
                self.ged_issues.append([index, Issue.LESS_ZERO])
            else:
                level = int(value[0])
        # Report the validation results which exists the function.
        # if len(issues) > 0:
        #     #if self.log:
        #     #logging.info(Msg.LOAD_FAILED.format(filename))
        #     return pd.DataFrame(
        #         data=issues, columns=[Column.LINE, Column.ISSUE]
        #     )
        # Find version.
        for i in self.ged_splitdata:
            if i[1] == 'VERS':
                self.ged_in_version = i[2]
                break
        # add in the base dictionaries.
        count: int = 0
        tags: list[str] = []
        for line in self.ged_splitdata:
            if line[0] == '0' and len(line) == 3:
                count = count + 1
                if line[2] not in self.chron:
                    self.chron.update({line[2]: {}})
                self.chron[line[2]].update({line[1]: {}})
                tags = []
                tags.append(line[2])
                tags.append(line[1])
            elif line[0] == '1' and len(line) == 3 and count > 0:
                # t0 = tags[0]
                # t1 = tags[1]
                self.chron[tags[0]][tags[1]].update({line[1]: line[2]})
                tags.append(line[1])
            # elif line[0] == '2' and len(line) == 3 and count > 0:
            #     self.chron[tags[0]][tags[1]][tags[2]].update({line[1]: line[2]})
            #     tags.append(line[1])
        # logging.info(Msg.LOADED.format(self.chron_name, self.filename))


    def write_ged(self, newfilename: str = Value.EMPTY):
        if newfilename == Value.EMPTY:
            newfilename = self.filename
        with Path.open(Path(newfilename), Arg.WRITE) as file:
            file.write(Line.HEAD)
            file.write(Line.SUBM)
            file.write(Line.TAIL)
            file.close()

    def save(self):
        if self.filename_type == Arg.JSON:
            self.write_json()
            logging(Msg.SAVED.format(self.chron_name, self.filename))
        elif self.filename_type == Arg.GED:
            self.write_ged()
            logging(Msg.SAVED.format(self.chron_name, self.filename))
        else:
            logging(Msg.SAVE_FIRST.format(self.chron_name))