# Licensed under a 3-clause BSD style license - see LICENSE.md
"""Read and write files for chronology files."""

import csv
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

import numpy as np
import pandas as pd  # type: ignore[import-untyped]

from chronodata.constants import (
    Number,
    String,
    Tag,
    Unit,
)
from chronodata.messages import Issue, Msg


@dataclass(frozen=True)
class Value:
    """The following constants are dictionary values."""

    AD: str = ' AD'
    BC: str = ' BC'
    BCE: str = ' BCE'
    BEFORE_PRESENT: str = 'BEFORE PRESENT'
    BP: str = ' BP'
    CE: str = ' CE'
    DATETIME_EPOCH: int = 1970
    EMPTY: str = ''
    EPOCH: str = 'Epoch'
    EXPERIMENT: str = 'EXPERIMENT'
    GREGORIAN: str = 'GREGORIAN'
    ISO: str = 'ISO'
    MAX_MONTHS: str = 'Max Months'
    MONTH_NAMES: str = 'Month Names'
    MONTH_MAX_DAYS: str = 'Month Max Days'
    SECULAR: str = 'SECULAR'


@dataclass(frozen=True)
class Key:
    """The following constants define the keys that are used
    for dictionaries."""

    ACTORS: str = 'ACTORS'
    BEGIN: str = 'BEGIN'
    BIRTH: str = 'BIRTH'
    CAL: str = 'CALENDAR'
    CHALLENGES: str = 'CHALLENGES'
    COMMENTS: str = 'COMMENTS'
    DATE: str = 'DATE'
    DEATH: str = 'DEATH'
    DESC: str = 'DESC'
    END: str = 'END'
    EVENTS: str = 'EVENTS'
    FATHER: str = 'FATHER'
    FEMALE: str = 'FEMALE'
    FILE: str = 'FILENAME'
    LABELS: str = 'LABELS'
    MALE: str = 'MALE'
    MARKERS: str = 'MARKERS'
    MESSAGE: str = 'MSG'
    MOTHER: str = 'MOTHER'
    NAME: str = 'NAME'
    PRE: str = 'PRE'
    PERIODS: str = 'PERIODS'
    POST: str = 'POST'
    SOURCES: str = 'SOURCES'
    STRICT: str = 'STRICT'
    TEXTS: str = 'TEXTS'
    TIMESTAMP: str = 'TIMESTAMP'
    ZERO: str = 'ZERO'
    keys: ClassVar = [
        ACTORS,
        BEGIN,
        BIRTH,
        CAL,
        CHALLENGES,
        COMMENTS,
        DATE,
        DEATH,
        DESC,
        END,
        EVENTS,
        FATHER,
        FEMALE,
        FILE,
        LABELS,
        MALE,
        MARKERS,
        MOTHER,
        NAME,
        PERIODS,
        POST,
        PRE,
        SOURCES,
        STRICT,
        TEXTS,
        ZERO,
    ]


@dataclass(frozen=True)
class Calendar:
    """The following dictionaries define the constants for
    particular calendars using previously defined constants.
    """

    BEFORE_PRESENT: ClassVar = {
        Key.NAME: Value.BEFORE_PRESENT,
        Key.POST: '',
        Key.PRE: Value.BP,
        Key.STRICT: True,
        Key.ZERO: False,
    }
    EXPERIMENT: ClassVar = {
        Key.NAME: Value.EXPERIMENT,
        Key.POST: '',
        Key.PRE: '',
        Key.STRICT: True,
        Key.ZERO: False,
    }
    GREGORIAN: ClassVar = {
        Key.NAME: Value.GREGORIAN,
        Key.POST: Value.AD,
        Key.PRE: Value.BC,
        Key.STRICT: True,
        Key.ZERO: False,
    }
    SECULAR: ClassVar = {
        Key.NAME: Value.SECULAR,
        Key.POST: Value.CE,
        Key.PRE: Value.BCE,
        Key.STRICT: True,
        Key.ZERO: False,
    }
    calendars: ClassVar = [
        BEFORE_PRESENT,
        EXPERIMENT,
        GREGORIAN,
        SECULAR,
    ]


class Base:
    """Load a chronology from a file or create an empty chronology."""

    def __init__(
        self,
        name: str = '',
        filename: str = '',
        calendar: str = String.GREGORIAN,
        log: bool = True,
    ) -> None:
        self.chron: dict[Any, Any] = {
            Tag.FAM: {},
            Tag.INDI: {},
            Tag.OBJE: {},
            Tag.REPO: {},
            Tag.SNOTE: {},
            Tag.SOUR: {},
            Tag.SUBM: {},
            Tag.SUBM: {},
        }
        self.chron_name: str = name
        self.calendar: str = calendar
        self.ged_data: list[str] = []
        self.ged_splitdata: list[Any] = []
        self.ged_issues: list[Any] = []
        self.ged_in_version: str = ''
        self.ged_header: str = ''
        self.ged_trailer: str = f'0 {Tag.TRLR}\n'
        self.ged_family: str = ''
        self.ged_individual: str = ''
        self.ged_multimedia: str = ''
        self.ged_repository: str = ''
        self.ged_shared_note: str = ''
        self.ged_source: str = ''
        self.ged_submitter: str = ''
        self.csv_data: str = ''
        self.filename: str = filename
        self.filename_type: str = self._get_filename_type(self.filename)
        match self.filename_type:
            case '':
                self.chron = {
                    Tag.NAME: name,
                    Key.CAL: calendar,
                }
                if log:
                    logging.info(Msg.STARTED.format(self.chron_name))
            case String.JSON:
                self.read_json()
                if log:
                    logging.info(Msg.LOADED.format(self.chron_name, filename))
            case String.GED:
                self.read_ged()
                if log:
                    logging.info(Msg.LOADED.format(self.chron_name, filename))
            case String.CSV:
                self.read_csv()
                if log:
                    logging.info(Msg.LOADED.format(self.chron_name, filename))
            case _:
                logging.warning(Msg.UNRECOGNIZED.format(self.filename))

    def __str__(self) -> str:
        return json.dumps(self.chron)

    def _get_filename_type(self, filename: str) -> str:
        filename_type: str = ''
        if filename[-Number.JSONLEN :] == String.JSON:
            filename_type = String.JSON
        if filename[-Number.GEDLEN :] == String.GED:
            filename_type = String.GED
        return filename_type

    def read_csv(self) -> None:
        try:
            with Path.open(
                Path(self.filename), encoding='utf-8', mode=String.READ
            ) as infile:
                data: Any = infile.readlines()
                self.csv_data = ''.join([self.csv_data, data])
                infile.close()
        except UnicodeDecodeError:
            logging.error(Msg.NOT_UNICODE.format(self.filename))
            raise
        self.cal_name = self.chron[Key.CAL][Key.NAME]
        self.chron_name = self.chron[Key.NAME]

    def read_json(self) -> None:
        try:
            with Path.open(
                Path(self.filename), encoding='utf-8', mode=String.READ
            ) as infile:
                self.chron = json.load(infile)
                infile.close()
        except UnicodeDecodeError:
            logging.error(Msg.NOT_UNICODE.format(self.filename))
            raise
        self.cal_name = self.chron[Key.CAL][Key.NAME]
        self.chron_name = self.chron[Key.NAME]

    def read_ged(self) -> None:
        """Read and validate the GEDCOM file."""
        try:
            with Path.open(
                Path(self.filename), encoding='utf-8', mode=String.READ
            ) as infile:
                data: Any = infile.readlines()
                self.ged_data.append(data)
                infile.close()
        except UnicodeDecodeError:
            logging.error(Msg.NOT_UNICODE.format(self.filename))
            raise
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

    def save(self, filename: str = '', overwrite: bool = False) -> None:
        """Save the current chronology.

        Parameters
        ----------
        filename:
            The name of the file. If empty it will use the name
        """

        if filename == '':
            filename = self.filename
        else:
            self.filename = filename
            self.filename_type = self._get_filename_type(filename)
        if Path.exists(Path(filename)) and not overwrite:
            logging.info(Msg.FILE_EXISTS.format(filename))
        else:
            match self.filename_type:
                # https://stackoverflow.com/questions/10373247/how-do-i-write-a-python-dictionary-to-a-csv-file
                case String.CSV:
                    with Path.open(
                        Path(self.filename), encoding='utf-8', mode=String.WRITE
                    ) as file:
                        w = csv.DictWriter(file, self.chron.keys())
                        w.writerows(self.chron)
                    logging.info(
                        Msg.SAVED.format(self.chron_name, self.filename)
                    )
                case String.JSON:
                    with Path.open(
                        Path(self.filename), encoding='utf-8', mode=String.WRITE
                    ) as file:
                        json.dump(self.chron, file)
                        file.close()
                    logging.info(
                        Msg.SAVED.format(self.chron_name, self.filename)
                    )
                case String.GED:
                    output: str = ''.join(
                        [
                            self.ged_header,
                            self.ged_family,
                            self.ged_individual,
                            self.ged_multimedia,
                            self.ged_shared_note,
                            self.ged_source,
                            self.ged_submitter,
                            self.ged_trailer,
                        ]
                    )
                    with Path.open(
                        Path(filename), encoding='utf-8', mode=String.WRITE
                    ) as file:
                        file.write(output)
                        file.close()
                    logging.info(
                        Msg.SAVED.format(self.chron_name, self.filename)
                    )
                case _:
                    logging.info(Msg.SAVE_FIRST.format(self.chron_name))

    def rename(self, name: str) -> None:
        """Rename the chronology."""
        self.chron.update({Key.NAME: name})
        self.chron_name = self.chron[Key.NAME]
        logging.info(Msg.RENAME.format(self.chron_name))

    ###### CALENDARS

    def calendars(self) -> pd.DataFrame:
        """Display all of the available CALENDARS.

        This is a list of calendars that one can move to from
        the one defined by the current chronology.

        See Also
        --------

        Example
        -------
        """
        return pd.DataFrame(data=Calendar.calendars)

    # def datetimes(self) -> pd.DataFrame:
    #     """Display the datetime units NumPy permits.

    #     Reference
    #     ---------
    #     For more information on the units available in NumPy's `datetime64` see
    #     [NumPy Units](https://numpy.org/doc/stable/reference/arrays.datetime.html#datetime-units)
    #     """
    #     return pd.DataFrame(
    #         data=Unit.units, columns=[Column.DATETIME, Column.CODE]
    #     )

    def strict_labels(self) -> None:
        """Set strict formatting for dates.

        Each date will have a label for before or after
        the epoch of the calendar.  This may become
        unnecessary if all dates are after or before
        the epoch.  This is the default behavior.

        See Also
        --------
        - `relaxed_labels` does not add epoch labels
        to all dates.

        Example
        -------
            The date "2024" will be formatted and displayed
            as "2024 AD" in the Gregorian calendar because
            the post label after the epoch is " AD".
        """
        self.strict = True
        self.chron.update({Key.LABELS: self.strict})
        logging.info(Msg.STRICT.format(str(self.strict)))

    def relaxed_labels(self) -> None:
        """Set relaxed formatting for dates.

        Each day after the epoch of the calendar will
        not have a label displayed.  This is not the default
        behavior.  The default behavior always adds a
        label showing whether the date is before or after
        the epoch for the calendar.

        See Also
        --------
        - `strict_labels` adds epoch labels to all dates.

        Example
        -------
            The date "2024" will be formatted and displayed
            as "2024" rather than "2024 AD" in the
            Gregorian calendar or "2024 CE" in the Secular
            calendar.
        """
        self.strict = False
        self.chron.update({Key.LABELS: self.strict})
        logging.info(Msg.STRICT.format(str(self.strict)))

    def check_date(self, date: str) -> bool:
        cleandate = date.upper().strip()
        if cleandate[-self.prelen :] == self.pre:
            try:
                np.datetime64(cleandate[0 : -self.prelen :])
            except ValueError:
                logging.info(Msg.BAD_DATE.format(date, self.chron[Key.NAME]))
                return False
            else:
                return True
        elif cleandate[-self.postlen :] == self.post:
            try:
                np.datetime64(cleandate[0 : -self.postlen :])
            except ValueError:
                logging.info(Msg.BAD_DATE.format(date, self.chron[Key.NAME]))
                return False
            else:
                return True
        elif not self.strict:
            try:
                np.datetime64(cleandate)
            except ValueError:
                logging.info(Msg.BAD_DATE.format(date, self.chron[Key.NAME]))
                return False
            else:
                return True
        else:
            logging.info(
                Msg.BAD_LABEL.format(
                    date,
                    date[-self.postlen :],
                    self.post,
                    self.pre,
                    self.chron[Key.NAME],
                )
            )
            return False

    def format_date(self, date: str) -> str:
        formatted_date: str = date.upper().strip()
        if self.strict:
            try:
                np.datetime64(formatted_date)
            except ValueError:
                return formatted_date
            else:
                return ''.join([formatted_date, self.post])
        else:
            return formatted_date

    def to_datetime64(self, date: str) -> str:
        """Convert a calendar date to an ISO 8601 date and time string.

        The calendar date may contain labels.  These are removed.
        If the label signals a negative value for the NumPy string,
        then a negative sign is added to the front of the string.

        Parameters
        ----------
        date: str
            The calendar date to be converted to a NumPy datetime64
            data type extending the ISO 8601 functionality.

        See Also
        --------
        `date_diff`
            This method uses `to_datetime64` to convert a calendar
            date to a NumPy datetime64 data type.

        References
        ----------
        [The ISO 8601 Standard](https://en.wikipedia.org/wiki/ISO_8601)
        [NumPy Datetime64 Documentation](https://numpy.org/doc/stable/reference/arrays.datetime.html)

        """
        if date[-self.postlen :] == self.post:
            newdate = date[0 : -self.postlen]
        elif date[-self.prelen :] == self.pre:
            nolabeldate = date[0 : -self.prelen]
            try:
                end = nolabeldate.index(String.NEGATIVE)
            except ValueError:
                end = len(nolabeldate)
            oldyear = nolabeldate[0:end]
            newyear = str(int(oldyear) - 1)
            newdate = ''.join(
                [String.NEGATIVE, newyear, nolabeldate[len(oldyear) :]]
            )
        else:
            newdate = date
        return newdate

    # def date_diff(
    #     self, older: str, younger: str, unit: str = Unit.YEAR
    # ) -> float:
    #     olderdate = np.datetime64(self.to_datetime64(older), unit)
    #     youngerdate = np.datetime64(self.to_datetime64(younger), unit)
    #     return int((youngerdate - olderdate) / np.timedelta64(1, unit))

    def daysinyear(self, date: Any) -> int:
        """A procedure to count number of days in a Gregorian year
        given the year.

        Parameters
        ----------
        date: np.datetime64
            The date to find the number of days in the year

        Examples
        --------

        """
        if isinstance(date, str):
            year = np.datetime64(date, Unit.YEAR).astype(String.INT) + 1970
        else:
            year = (
                np.datetime_as_string(date, unit=Unit.YEAR).astype(String.INT)
                + 1970
            )
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            days = 366
        else:
            days = 365
        return days

    def numericdate(self, date: str) -> np.datetime64:
        """A procedure to convert an ISO string with KEYS to astronomical
        year numbering. This numeric value contains a Year Zero as 0.
        Dates labelled as `BC` or `BCE` will be converted to a
        negative value one year larger than the string date with
        the label.

        Parameters
        ----------
        date: string
            The date that will be converted to a numeric value.

        Returns
        -------
        np.datetime64
            The numeric value of the date in astronomical time with
            Year Zero being 0.

        Examples
        --------

        """
        # Look for errors
        if date[0] == String.NEGATIVE:
            if date[-self.prelen :] == self.pre:
                logging.warning(Msg.NEG_YEAR.format(date[-self.prelen :]))
            elif date[-self.postlen :] == self.post:
                logging.warning(Msg.POS_YEAR.format(date[-self.postlen :]))

        # If no errors, proceed
        if date[-self.prelen :] == self.pre:
            days = self.daysinyear(date[0 : -self.prelen])
            numericdate = np.datetime64(
                String.NEGATIVE + date[0 : -self.prelen]
            ) + np.timedelta64(days, Unit.DAY)
        elif date[-self.postlen :] == self.post:
            numericdate = np.datetime64(date[0 : -self.postlen])
        else:
            numericdate = np.datetime64(date)
        return numericdate

    # def stringdate(
    #     self, date: np.ndarray[Any, Any], unit: str = Unit.YEAR
    # ) -> np.ndarray[Any, np.dtype[Any]]:
    #     """A procedure to convert a numeric date to a date labelled
    #     with an epoch label.

    #     Parameters
    #     ----------
    #     date: np.datetime64
    #         The numeric date to be converted to a string

    #     """

    #     return np.datetime_as_string(date, unit=unit)

    # def add_calendar(
    #     self, name: str, begin: str, end: str, **keyvalues: str
    # ) -> None:
    #     """Add a calendar to the dictionary."""

    def to(self, calendar: dict[str, Any]) -> None:
        """Convert the calendar of the chronology to anther calendar.

        Parameter
        ---------
        calendar: str
            The key of the calendar to convert the current calendar to.
        """

        if calendar[Key.NAME] == self.chron[Key.CAL][Key.NAME]:
            logging.info(Msg.HAS_CALENDAR.format(self.chron[Key.CAL][Key.NAME]))
        else:
            cals: list[dict[str, Any]] = [Calendar.GREGORIAN, Calendar.SECULAR]
            oldcal: dict[str, Any] = self.chron[Key.CAL]
            post: str = oldcal[Key.POST]
            postlen: int = -len(post)
            newcal = calendar
            if calendar in cals and self.chron[Key.CAL] in cals:
                self.chron[Key.CAL].update(newcal)
                for i in self.chron[Key.PERIODS]:
                    for k in [Key.BEGIN, Key.END]:
                        if self.chron[Key.PERIODS][i][k][-postlen:] == post:
                            new = self.chron[Key.PERIODS][i][k].replace(
                                oldcal[post], newcal[post]
                            )
                        else:
                            new = self.chron[Key.PERIODS][i][k].replace(
                                oldcal[Key.PRE], newcal[Key.PRE]
                            )
                        self.chron[Key.PERIODS][i].update({k: new})
                for i in self.chron[Key.EVENTS]:
                    for k in [Key.DATE]:
                        if self.chron[Key.EVENTS][i][k][postlen:] == post:
                            new = self.chron[Key.EVENTS][i][k].replace(
                                oldcal[Key.POST], newcal[Key.POST]
                            )
                        else:
                            new = self.chron[Key.EVENTS][i][k].replace(
                                oldcal[Key.PRE], newcal[Key.PRE]
                            )
                        self.chron[Key.EVENTS][i].update({k: new})
                self.post = self.chron[Key.CAL][Key.POST]
                self.postlen = len(self.post)
                self.pre = self.chron[Key.CAL][Key.PRE]
                self.prelen = len(self.pre)
                logging.info(Msg.CHANGED.format(self.chron[Key.CAL][Key.NAME]))
