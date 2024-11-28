# Licensed under a 3-clause BSD style license - see LICENSE.md
"""Read and write methods for GEDCOM genealogy files."""

from pathlib import Path

import pandas as pd

from chronodata.constants import (
    Arg,
    Column,
    Issue,
    Line,
    Tag,
)
from chronodata.messages import Msg


def read(filename: str) -> list:
    """Read and validate the GEDCOM file."""
    # filename = Path(filename)
    # chron_name = str(filename.stem)
    data: list = []
    splitdata: list = []
    issues: list = []
    chron: dict = {}
    with Path.open(Path(filename), Arg.READ) as file:
        data = file.readlines()
        file.close()
    # Split each line into components and remove terminator.
    for i in data:
        splitdata.append(i.replace('\n', '').split(' ', 2))
    # Check the level for bad increments and starting point.
    level: int = 0
    for index, value in enumerate(splitdata, start=1):
        if index == 1 and value[0] != '0':
            issues.append([index, Issue.NO_ZERO])
        elif int(value[0]) > level + 1:
            issues.append([index, Issue.BAD_INC])
        elif int(value[0]) < 0:
            issues.append([index, Issue.LESS_ZERO])
        else:
            level = int(value[0])
    # Report the validation results which exists the function.
    if len(issues) > 0:
        #if self.log:
        #logging.info(Msg.LOAD_FAILED.format(filename))
        return pd.DataFrame(
            data=issues, columns=[Column.LINE, Column.ISSUE]
        )
    # Find version.
    version: str = ''
    for i in splitdata:
        if i[1] == 'VERS':
            version = i[2]
            break
    # add in the base dictionaries.
    count: int = 0
    tags: list[str] = []
    for line in splitdata:
        if line[0] == '0' and len(line) == 3:
            count = count + 1
            if line[2] not in chron:
                chron.update({line[2]: {}})
            chron[line[2]].update({line[1]: {}})
            tags = []
            tags.append(line[2])
            tags.append(line[1])
        elif line[0] == '1' and len(line) == 3 and count > 0:
            # t0 = tags[0]
            # t1 = tags[1]
            chron[tags[0]][tags[1]].update({line[1]: line[2]})
            tags.append(line[1])
        # elif line[0] == '2' and len(line) == 3 and count > 0:
        #     self.chron[tags[0]][tags[1]][tags[2]].update({line[1]: line[2]})
        #     tags.append(line[1])
    # logging.info(Msg.LOADED.format(self.chron_name, self.filename))
    return chron

def write(filename: str, chron: dict):
    mode: str = Arg.WRITE
    with Path.open(Path(filename), mode) as file:
        file.write(Line.HEAD)
        file.write(Line.SUBM)
        file.write(Line.TAIL)
        file.close()
    # if self.log:
    #     logging.info(Msg.FILE_SAVED.format(name))
