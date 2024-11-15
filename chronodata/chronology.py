# Licensed under a 3-clause BSD style license - see LICENSE.md
"""This module provides procedures to create generic chronologies.
It also provides examples of chronologies of actual chronologies
from historical events around the world to processes either
hypothesized or observed in laboratory conditions.

The module also provides means of testing conflicting chronologies
using constraints that could lead one to falsify the
chronology unless the constraints are answered.
"""

import copy
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

import numpy as np
import pandas as pd

from chronodata.constants import (
    Arg,
    Calendar,
    Column,
    Key,
    Msg,
    String,
    Unit,
    Value,
)

__all__ = ['Chronology']
__author__ = 'Frank Hubeny'


class Chronology:
    """Construct a dictionary to represent a chronology.

    The tools provide for storing dates associated with periods and events.
    - One can name an actor with an event.
    - One can add a defense for each date to answer a challenge.
    - One can add a challenge to argue against a competing chronology.
    - One can save the chronology to a human readable file.
    - The file may be modified with a text editor.
    - One can retrieve the dictionary from a file to continue building it.

    Routines
    --------

    See Also
    --------
    `Compare`: After two competing Chronologies have been constructed
        with defenses and challenges they may be compared with the
        visualization tools in this class.

    References
    ----------
    - Introduction to Calendars:
    https://aa.usno.navy.mil/faq/calendars Accessed on Oct 30, 2024

    Examples
    --------
    The first two examples show two competing chronologies for
    biblical history.

    The following would construct a brief chronology based on
    James Ussher's history. It also provides a defense against and
    a challenge for the older Byzantine chronology.

    The following constructs a brief chronology based on the Byzantine
    chronology. It contains a defense against and a challenge
    for the Ussher's history.

    The next two examples show to competing chronologies based on periods
    for the Ancient Near East.

    The following would construct a brief chronology as the basis
    of a genealogy.


    The following would construct a brief chronology of the
    decay of uranian-238.

    The following chronology provides a brief history of China
    using the Chinese calendar.

    The following example converts the above chronology of China to a
    Gregorian calendar.

    The following chronology provides a brief history of Islam
    using the Islamic calendar.

    The following example converts the above chronology of Islam
    to a secular calendar using 'CE' rather than 'AD' labels.
    """

    def __init__(
        self,
        name: str = Value.EMPTY,
        filename: str = Value.EMPTY,
        calendar: dict[str, Any] = Calendar.GREGORIAN,
        log: bool = True,
    ) -> None:
        self.log: bool = log
        logging.basicConfig(
            format='%(levelname)s:%(message)s', level=logging.INFO
        )
        self.chron: dict[str, Any] = {}
        self.chron_name: str = name
        self.strict: bool = calendar[Key.STRICT]
        self.filename: str = filename
        self.post: str = calendar[Key.POST]
        self.postlen: int = len(self.post)
        self.pre: str = calendar[Key.PRE]
        self.prelen: int = len(self.pre)
        if filename == Value.EMPTY:
            self.chron = (
                {Key.NAME: name}
                | {Key.CAL: calendar}
                | {Key.COMMENTS: {}}
                | {Key.ACTORS: {}}
                | {Key.EVENTS: {}}
                | {Key.PERIODS: {}}
                | {Key.SOURCES: {}}
                | {Key.MARKERS: {}}
                | {Key.CHALLENGES: {}}
                | {Key.TEXTS: {}}
            )
            if self.log:
                logging.info(Msg.STARTED.format(self.chron_name))
        else:
            mode: Literal['r'] = 'r'
            with Path.open(Path(filename), mode) as file:
                self.chron = json.load(file)
                file.close()
            self.cal_name = self.chron[Key.CAL][Key.NAME]
            self.chron_name = self.chron[Key.NAME]
            self.post = self.chron[Key.CAL][Key.POST]
            self.postlen = len(self.post)
            self.pre = self.chron[Key.CAL][Key.PRE]
            self.prelen = len(self.pre)
            if self.log:
                logging.info(Msg.LOADED.format(self.chron_name, filename))

    def show(self) -> None:
        """Show the entire chronology."""
        self.dictshow()

    def __str__(self) -> str:
        return json.dumps(self.chron)

    def rename(self, name: str) -> None:
        """Rename the chronology."""
        self.chron.update({Key.NAME: name})
        self.chron_name = self.chron[Key.NAME]
        if self.log:
            logging.info(Msg.RENAME.format(self.chron_name))

    ###### Dictionary Methods

    ###### Calendar Methods

    ###### Astronmical Methods

    ###### ACTORS

    def actors(self) -> pd.DataFrame:
        """Display the actors in a chronology."""
        return self.show_dictionary(Key.ACTORS)

    def actors_pop(self, pops: list[str]) -> pd.DataFrame:
        """Display the actors defined for the chronology if there are any.

        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying
            the actors.

        """
        return self.dictionary_pop(Key.ACTORS, pops)

    def add_actor(
        self,
        name: str,
        father: str = Value.EMPTY,
        mother: str = Value.EMPTY,
        birth: str = Value.EMPTY,
        death: str = Value.EMPTY,
        DESC: str = Value.EMPTY,
        **keyvalues: str,
    ) -> None:
        """Add an actor to the dictionary."""
        if self.check_date(birth) and self.check_date(death):
            self.chron[Key.ACTORS].update(
                {
                    name: {
                        Key.FATHER: father,
                        Key.MOTHER: mother,
                        Key.BIRTH: self.format_date(birth),
                        Key.DEATH: self.format_date(death),
                        Key.DESC: DESC,
                    }
                }
            )
            self.chron[Key.ACTORS][name].update(keyvalues)
            if self.log:
                logging.info(Msg.ADD_ACTOR.format(self.chron[Key.ACTORS][name]))

    def remove_actor(self, name: str) -> None:
        """Remove an actor from the dictionary."""
        self.remove_key(Key.ACTORS, name)

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
        if self.log:
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
        if self.log:
            logging.info(Msg.STRICT.format(str(self.strict)))

    def check_date(self, date: str) -> bool:
        cleandate = date.upper().strip()
        if cleandate[-self.prelen :] == self.pre:
            try:
                np.datetime64(cleandate[0 : -self.prelen :])
            except ValueError:
                if self.log:
                    logging.info(Msg.BAD_DATE.format(date, self.chron[Key.NAME]))
                return False
            else:
                return True
        elif cleandate[-self.postlen :] == self.post:
            try:
                np.datetime64(cleandate[0 : -self.postlen :])
            except ValueError:
                if self.log:
                    logging.info(Msg.BAD_DATE.format(date, self.chron[Key.NAME]))
                return False
            else:
                return True
        elif not self.strict:
            try:
                np.datetime64(cleandate)
            except ValueError:
                if self.log:
                    logging.info(Msg.BAD_DATE.format(date, self.chron[Key.NAME]))
                return False
            else:
                return True
        else:
            if self.log:
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
                return Value.EMPTY.join([formatted_date, self.post])
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
            newdate = Value.EMPTY.join(
                [String.NEGATIVE, newyear, nolabeldate[len(oldyear) :]]
            )
        else:
            newdate = date
        return newdate

    def date_diff(
        self, older: str, younger: str, unit: str = Unit.YEAR
    ) -> float:
        olderdate = np.datetime64(self.to_datetime64(older), unit)
        youngerdate = np.datetime64(self.to_datetime64(younger), unit)
        return float((youngerdate - olderdate) / np.timedelta64(1, unit))

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
            year = np.datetime64(date, Unit.YEAR).astype(Arg.INT) + 1970
        else:
            year = (
                np.datetime_as_string(date, unit=Unit.YEAR).astype(Arg.INT)
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
            if self.log:
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
                if self.log:
                    logging.info(Msg.CHANGED.format(self.chron[Key.CAL][Key.NAME]))

    ###### CHALLENGES

    def challenges(self) -> pd.DataFrame:
        """Display the challenges in a chronology."""
        return self.show_dictionary(Key.CHALLENGES)

    def challenges_pop(self, pops: list[str]) -> pd.DataFrame:
        """Display the challenges defined for the chronology
        if there are any.

        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before
            displaying the periods.

        """
        return self.dictionary_pop(Key.CHALLENGES, pops)

    def add_challenge(
        self, name: str, date: str, desc: str = Value.EMPTY, **keyvalues: str
    ) -> None:
        """Add a challenge to the dictionary."""
        if self.check_date(date):
            self.chron[Key.CHALLENGES].update(
                {
                    name: {
                        Key.DATE: self.format_date(date),
                        Key.DESC: desc,
                    }
                }
            )
            self.chron[Key.CHALLENGES][name].update(keyvalues)
            if self.log:
                logging.info(
                    Msg.ADD_CHALLENGE.format(self.chron[Key.CHALLENGES][name])
                )

    def remove_challenge(self, name: str) -> None:
        """Remove a challenge from the dictionary."""
        self.remove_key(Key.CHALLENGES, name)

    ###### COMMENTS

    def comments(self) -> pd.DataFrame:
        """Display a numbered list of comments."""
        length: int = len(self.chron[Key.COMMENTS])
        if length == 0:
            logging.info(Msg.NO_COMMENTS.format(self.chron_name))
        return pd.DataFrame.from_dict(
            self.chron[Key.COMMENTS], orient=Arg.INDEX
        )

    def add_comment(self, text: str = Value.EMPTY) -> None:
        """Add a comment to a chronology.

        To create a comment with more than one line
        use `\n` to separate the lines.

        Parameters
        ----------
        text: str
            A comment one or more lines long. Each line ended with `\n`.

        See Also
        --------
        `comments`
            Display all comments in the chronology.
        `remove_comment`
            Remove a line from the comment list.
        `remove_all_comments`
            Remove all comments from the chronology.

        Notes
        -----
        Comments are placed at the beginning of the file
        before the dictionaries.

        The file may be opened and edited with a text editor.

        To add a blank line, accept the default value for `text`.

        Exampless
        ---------

        """

        texts: list[str] = text.split(String.NEWLINE)
        stamp: str = str(datetime.now())
        for i in texts:
            how_many: str = str(len(self.chron[Key.COMMENTS]) + 1)
            self.chron[Key.COMMENTS].update(
                {
                    how_many: {
                        Key.MESSAGE: i.strip(),
                        Key.TIMESTAMP: stamp,
                    }
                }
            )
        if self.log:
            logging.info(Msg.ADD_COMMENT.format(text))

    def remove_comment(self, *index: int) -> None:
        """Remove a comment from the chronology by specifying
        its number in the comments list."""
        for idx in index:
            if str(idx) not in dict(self.chron[Key.COMMENTS]):
                if self.log:
                    logging.info(Msg.OUT_OF_RANGE.format(str(idx)))
            else:
                removed = self.chron[Key.COMMENTS][str(idx)][Key.MESSAGE]
                self.chron[Key.COMMENTS].pop(str(idx))
                comments: list[dict[str, str]] = []
                for num in self.chron[Key.COMMENTS]:
                    comments.append(self.chron[Key.COMMENTS][num])
                self.remove_all_comments(show_message=False)
                for i in range(1, len(comments) + 1):
                    self.chron[Key.COMMENTS].update({str(i): comments[i - 1]})
                if self.log:
                    logging.info(Msg.COMMENT_REMOVED.format(str(idx), removed))

    def remove_all_comments(self, show_message: bool = True) -> None:
        """Remove all comments from the chronology."""
        self.chron[Key.COMMENTS] = {}
        if show_message and self.log:
            logging.info(Msg.REMOVE_ALL_COMMENTS.format(self.chron_name))

    ###### DICTIONARIES

    def reserved_keys(self) -> pd.DataFrame:
        """Display the KEYS constants."""
        return pd.DataFrame(data=Key.keys, columns=[Column.RESERVED])

    # def check_keys(
    #     self, keyvalues: dict[str, str] | dict[str, dict[str, Any]]
    # ) -> bool:
    #     count = 0
    #     for i in dict(keyvalues):
    #         if i in Key.keys:
    #             logging.info(Msg.RESERVED.format(i))
    #             count += 1
    #     return not count > 0

    def dictshow(
        self,
        dictname: str = Value.EMPTY,
        as_json: bool = False,
        tab: int = 4,
    ) -> str | pd.DataFrame:
        dict = self.chron if dictname == Value.EMPTY else self.chron[dictname]
        if as_json:
            return json.dumps(dict, indent=tab)
        return pd.DataFrame.from_dict(dict)

    def dictionary_pop(self, dictname: str, pops: list[str]) -> pd.DataFrame:
        """Display the dictionary except for specified keys.

        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying
            the dictionary.
        dictname: str
            The name of the dictionary to display.

        """
        dictionary: dict[str, Any] = copy.deepcopy(dict(self.chron[dictname]))
        for i in pops:
            for j in dictionary:
                try:
                    dictionary[j].pop(i)
                except KeyError:
                    break
        return pd.DataFrame.from_dict(dictionary, orient=Arg.INDEX)

    def show_dictionary(self, dictname: str) -> pd.DataFrame:
        if len(self.chron[dictname]) == 0 and self.log:
            logging.info(
                Msg.NO_DICT_NAME.format(self.chron_name, dictname.lower())
            )
        return pd.DataFrame.from_dict(self.chron[dictname], orient=Arg.INDEX)

    def remove_key(self, dictname: str, key: str) -> None:
        """Revove a key from a dictionary of the chronology.

        Reserved keys cannot be removed, but they can be hiddened
        when displaying the dictionary or entire chronology.

        Parameters
        ----------
        dictname: str
            The name of the dictionary within the chronology
            where the key will be removed
        key: str
            The name of the key to be removed from the dictionary

        """
        # if key in Key.keys:
        #     logging.info(Msg.NOT_REMOVABLE.format(key))
        if key not in dict(self.chron[dictname]) and self.log:
            logging.info(Msg.NOT_IN_DICT.format(key, dictname))
        else:
            self.chron[dictname].pop(key)
            if self.log:
                logging.info(Msg.KEY_REMOVED.format(key, dictname))

    ###### EVENTS

    def events(self) -> pd.DataFrame:
        """Display the EVENTS dictionary."""
        return self.show_dictionary(Key.EVENTS)

    def events_pop(self, pops: list[str]) -> pd.DataFrame:
        """Display the events defined for the chronology
        without some of the keys.

        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed
            before displaying the events.

        """
        return self.dictionary_pop(Key.EVENTS, pops)

    def add_event(
        self, name: str, date: str, DESC: str = Value.EMPTY, **keyvalues: str
    ) -> None:
        """Add an event to the chronology."""
        if self.check_date(date):
            self.chron[Key.EVENTS].update(
                {
                    name: {
                        Key.DATE: self.format_date(date),
                        Key.DESC: DESC,
                    }
                }
            )
            self.chron[Key.EVENTS][name].update(keyvalues)
            if self.log:
                logging.info(Msg.ADD_EVENT.format(self.chron[Key.EVENTS][name]))

    def remove_event(self, name: str) -> None:
        """Remove an event from the dictionary."""
        self.remove_key(Key.EVENTS, name)

    ###### MARKERS

    def markers(self) -> pd.DataFrame:
        """Display the markers in a chronology."""
        return self.show_dictionary(Key.MARKERS)

    def markers_pop(self, pops: list[str]) -> pd.DataFrame:
        """Display the markers defined for the chronology
        if there are any.

        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed
            before displaying the markers.

        """
        return self.dictionary_pop(Key.MARKERS, pops)

    def add_marker(
        self, name: str, date: str, DESC: str = Value.EMPTY, **keyvalues: str
    ) -> None:
        """Add a marker to the chronology."""
        if self.check_date(date): # and self.check_keys(keyvalues):
            self.chron[Key.MARKERS].update(
                {
                    name: {
                        Key.DATE: self.format_date(date),
                        Key.DESC: DESC,
                    }
                }
            )
            self.chron[Key.MARKERS][name].update(keyvalues)
            if self.log:
                logging.info(Msg.ADD_MARKER.format(self.chron[Key.MARKERS][name]))

    def remove_marker(self, name: str) -> None:
        """Remove a marker from the chronology."""
        self.remove_key(Key.MARKERS, name)

    ###### PERIODS

    def periods(self) -> pd.DataFrame:
        """Display the periods defined for the chronology
        if there are any."""
        return self.show_dictionary(Key.PERIODS)

    def periods_pop(self, pops: list[str]) -> pd.DataFrame:
        """Display the periods defined for the chronology
        except for specified keys.

        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before
            displaying the periods.

        """
        return self.dictionary_pop(Key.PERIODS, pops)

    def add_period(
        self, name: str, begin: str, end: str, **keyvalues: str
    ) -> None:
        """Add a period to the chronology."""
        if self.check_date(begin) and self.check_date(end):
            self.chron[Key.PERIODS].update(
                {
                    name: {
                        Key.BEGIN: self.format_date(begin),
                        Key.END: self.format_date(end),
                    }
                }
            )
            self.chron[Key.PERIODS][name].update(keyvalues)
            if self.log:
                logging.info(Msg.ADD_PERIOD.format(self.chron[Key.PERIODS][name]))

    def remove_period(self, name: str) -> None:
        """Remove a period from the chronology."""
        self.remove_key(Key.PERIODS, name)

    ###### SAVE

    def save(self, name: str = Value.EMPTY) -> None:
        file: str = Value.EMPTY
        mode: Literal['w'] = Arg.WRITE
        if name == Value.EMPTY:
            if self.filename == Value.EMPTY:
                file = Value.EMPTY.join([self.chron_name, Arg.JSON])
            else:
                file = self.filename
        else:
            file = name

        with Path.open(Path(file), mode) as f:
            json.dump(self.chron, f)
            f.close()
        if self.log:
            logging.info(Msg.FILE_SAVED.format(file))

    ###### SOURCES

    def sources(self) -> pd.DataFrame:
        """Display the sources referenced to justify a chronology."""
        return self.show_dictionary(Key.SOURCES)

    def sources_pop(self, pops: list[str]) -> pd.DataFrame:
        """Display the sources defined for the chronology
        except for specified keys.

        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before
            displaying the sources.

        """
        return self.dictionary_pop(Key.SOURCES, pops)

    def add_source(
        self, name: str, date: str, DESC: str = Value.EMPTY, **keyvalues: str
    ) -> None:
        """Add a source to the chronology."""
        if self.check_date(date):
            self.chron[Key.SOURCES].update(
                {
                    name: {
                        Key.DATE: self.format_date(date),
                        Key.DESC: DESC,
                    }
                }
            )
            self.chron[Key.SOURCES][name].update(keyvalues)
            if self.log:
                logging.info(Msg.ADD_SOURCE.format(self.chron[Key.SOURCES][name]))

    def remove_source(self, name: str) -> None:
        """Permanently remove a source from the chronology."""
        self.remove_key(Key.SOURCES, name)

    ###### TEXTS

    def texts(self) -> pd.DataFrame:
        """Display the texts referenced to justify a chronology."""
        return self.show_dictionary(Key.TEXTS)

    def texts_pop(self, pops: list[str]) -> pd.DataFrame:
        """Display the texts defined for the chronology
        except for specified keys.

        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before
            displaying the texts.

        """
        return self.dictionary_pop(Key.TEXTS, pops)

    def add_text(
        self, name: str, date: str, DESC: str = Value.EMPTY, **keyvalues: str
    ) -> None:
        """Add an event to the chronology."""
        if self.check_date(date):
            self.chron[Key.TEXTS].update(
                {
                    name: {
                        Key.DATE: self.format_date(date),
                        Key.DESC: DESC,
                    }
                }
            )
            self.chron[Key.TEXTS][name].update(keyvalues)
            if self.log:
                logging.info(Msg.ADD_TEXT.format(self.chron[Key.TEXTS][name]))

    def remove_text(self, name: str) -> None:
        """Permanently remove a text from the chronology."""
        self.remove_key(Key.TEXTS, name)
