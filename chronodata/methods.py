# chronodata/methods.py
# Copyright: Licensed under a 3-clause BSD style license - see LICENSE.md
"""Provide namespaces global methods.

These functions do various forms of checks and formatting
of output data.

The GEDCOM standard only permits UTF-8 character encodings
with a set of banned characters to explicitely eliminate
from input sources.

Reference
---------
- [GEDCOM UTF-8 Characters](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#characters)
- [Python 3 UTF How To](https://docs.python.org/3/howto/unicode.html)
- [Python 3 string](https://docs.python.org/3/library/string.html)
"""

import contextlib
import logging
import math
import re
from enum import Enum
from typing import Any

import numpy as np
import pandas as pd  # type: ignore[import-untyped]

from chronodata.constants import Cal, String
from chronodata.enums import Tag
from chronodata.messages import Msg

__all__ = [
    'DefCheck',
    'DefDate',
    'DefPlace',
    'DefTag',
]


class DefPlace:
    """Global methods to support place data."""

    @staticmethod
    def to_decimal(
        degrees: int, minutes: int, seconds: float, precision: int = 6
    ) -> float:
        """Convert degrees, minutes and seconds to a decimal.

        Example:
            >>> from chronodata.methods import DefPlace
            >>> DefPlace.to_decimal(49, 17, 50, 10)
            49.2972222222

        See Also:
            - `to_dms`: Convert a decimal to degrees, minutes, seconds to a precision.

        """
        sign: int = -1 if degrees < 0 else 1
        degrees = abs(degrees)
        minutes_per_degree = 60
        seconds_per_degree = 3600
        return round(
            sign * degrees
            + (minutes / minutes_per_degree)
            + (seconds / seconds_per_degree),
            precision,
        )

    @staticmethod
    def to_dms(position: float, precision: int = 6) -> tuple[int, int, float]:
        """Convert a measurment in decimals to one showing degrees, minutes
        and sconds.

        >>> from chronodata.methods import DefPlace
        >>> DefPlace.to_dms(49.29722222222, 10)
        (49, 17, 49.999999992)

        See Also:
            - `to_decimal`: Convert degrees, minutes, seconds with precision to a decimal.

        """
        minutes_per_degree = 60
        seconds_per_degree = 3600
        degrees: int = math.floor(position)
        minutes: int = math.floor((position - degrees) * minutes_per_degree)
        seconds: float = round(
            (position - degrees - (minutes / minutes_per_degree))
            * seconds_per_degree,
            precision,
        )
        return (degrees, minutes, seconds)


class DefTag:
    """Global methods to construct GEDCOM output."""

    @staticmethod
    def unique_xref(tuples: tuple[Any], xref: Any, name: Any) -> bool:
        values = {getattr(t, str(xref)) for t in tuples}
        values.add(str(name))
        return len(values) == len(tuples)

    @staticmethod
    def taginfo(
        level: int,
        tag: Tag,
        payload: str = '',
        extra: str = '',
    ) -> str:
        """Return a GEDCOM formatted line for the information and level.

        This is suitable for most tagged lines to guarantee it is uniformly
        formatted.  Although the user need not worry about calling this line,
        it is provided so the user can see the GEDCOM formatted output
        that would result.

        Example:
            The main use of this method generates a GEDCOM line.
            Note how the initial and ending spaces have been stripped from
            the input value.
            >>> from chronodata.enums import Tag
            >>> from chronodata.methods import DefTag
            >>> print(DefTag.taginfo(1, Tag.NAME, '  Some Name'))
            1 NAME   Some Name
            <BLANKLINE>

            There can also be an extra parameter.
            >>> from chronodata.enums import Tag
            >>> from chronodata.methods import DefTag
            >>> print(DefTag.taginfo(1, Tag.NAME, 'SomeName', 'Other info'))
            1 NAME SomeName Other info
            <BLANKLINE>

        """

        if extra == '':
            if payload == '':
                return f'{level} {tag.value}\n'
            return f'{level} {tag.value} {DefTag.clean_input(payload)}\n'
        return f'{level} {tag.value} {DefTag.clean_input(payload)} {DefTag.clean_input(extra)}\n'

    # @staticmethod
    # def contact_info(
    #     level: int = 1,
    #     phones: Any = None,
    #     emails: Any = None,
    #     faxes: Any = None,
    #     wwws: Any = None,
    # ) -> str:
    #     lines: str = ''
    #     if phones is not None:
    #         for phone in phones:
    #             lines = ''.join([lines, DefTag.taginfo(level, Tag.PHON, phone)])
    #     if emails is not None:
    #         for email in emails:
    #             lines = ''.join(
    #                 [lines, DefTag.taginfo(level, Tag.EMAIL, email)]
    #             )
    #     if faxes is not None:
    #         for fax in faxes:
    #             lines = ''.join([lines, DefTag.taginfo(level, Tag.FAX, fax)])
    #     if wwws is not None:
    #         for www in wwws:
    #             lines = ''.join([lines, DefTag.taginfo(level, Tag.WWW, www)])
    #     return lines

    @staticmethod
    def list_to_str(
        lines: str, level: int, items: list[Any], flag: str = ''
    ) -> str:
        """Append the GEDCOM lines from a list of NamedTuples to the GEDCOM file.

        Example:
            >>> from chronodata.methods import DefTag
            >>> from chronodata.enums import Tag
            >>> from chronodata.store import Note
            >>> lines = ''
            >>> note1 = Note('This is the first note')
            >>> note2 = Note('This is the second note')
            >>> notes = [note1, note2,]
            >>> lines = DefTag.list_to_str(lines, 1, notes)
            >>> print(lines)
            1 NOTE This is the first note
            1 NOTE This is the second note
            <BLANKLINE>

        Args:
            lines: The already constructed GEDCOM file that will be appended to.
            level: The GEDCOM level of the structure.
            items: The list of NamedTuples to append to `lines`.
            flag: An optional flag that will be passed to the `.ged` method of the
                NamedTuple which will modify its processing.
        """
        if len(items) > 0:
            for item in items:
                if flag != '':
                    lines = ''.join([lines, item.ged(level, flag)])
                else:
                    lines = ''.join([lines, item.ged(level)])
        return lines

    @staticmethod
    def empty_to_str(lines: str, level: int, tag: Tag) -> str:
        """Join a GEDCOM line that has only a level and a tag to a string.

        This method hides the join operation.

        Example:
            >>> from chronodata.methods import DefTag
            >>> from chronodata.enums import Tag
            >>> lines = ''
            >>> line = DefTag.empty_to_str(lines, 1, Tag.MAP)
            >>> print(line)
            1 MAP
            <BLANKLINE>

        Args:
            lines: The prefix of the returned string.
            level: The GEDCOM level of the structure.
            tag: The tag to apply to this line.
        
        """
        return ''.join([lines, DefTag.taginfo(level, tag)])

    @staticmethod
    def str_to_str(
        lines: str, level: int, tag: Tag, payload: str, extra: str = ''
    ) -> str:
        """Join a GEDCOM line to a string.

        This method hides the concatenation of the already constructed
        GEDCOM file with the new line and the check that this should only
        be done if the payload is not empty.
        
        Example:
            >>> from chronodata.enums import Tag
            >>> from chronodata.methods import DefTag
            >>> lines = '1 MAP\\n'
            >>> lines = DefTag.str_to_str(lines, 2, Tag.LATI, 'N30.0')
            >>> lines = DefTag.str_to_str(lines, 2, Tag.LONG, 'W30.0')
            >>> print(lines)
            1 MAP
            2 LATI N30.0
            2 LONG W30.0
            <BLANKLINE>

        Args:
            lines: The prefix string that will be appended to.
            level: The GEDCOM level of the structure.
            tag: The tag to apply to this line.
            info: The payload stored in this tagged line.
            extra: Optional extra payload to be stored on the same line.
        """
        if payload != '':
            return ''.join([lines, DefTag.taginfo(level, tag, payload, extra)])
        return lines

    @staticmethod
    def clean_input(input: str) -> str:
        """Remove banned GEDCOM unicode characters from input strings.

        The control characters U+0000 - U+001F and the delete character U+007F
        are listed in the
        [C0 Controls and Basic Latin](https://www.unicode.org/charts/PDF/U0000.pdf)
        chart.

        The code points U+D800 - U+DFFF are not interpreted.
        They are described in the
        [High Surrogate Area](https://www.unicode.org/charts/PDF/UD800.pdf) and
        [Low Surrogate Area](https://www.unicode.org/charts/PDF/UDC00.pdf)
        standards.

        The code points U+FFFE and U+FFFF are noncharacters as described in the
        [Specials](https://www.unicode.org/charts/PDF/UFFF0.pdf) standard.

        Reference:
            - [GEDCOM Characters](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#characters)
            - [Unicode Specification](https://www.unicode.org/versions/Unicode16.0.0/#Summary)
            - [Python re Module](https://docs.python.org/3/library/re.html)
        """

        return re.sub(String.BANNED, '', input)


class DefCheck:
    """Global methods supporting validation of data."""

    @staticmethod
    def verify_type(
        value: Any | None, value_type: Any, validate: bool = True
    ) -> bool:
        """Check if the value has the specified type."""
        check: bool = True
        if value is not None:
            if not isinstance(value, value_type):
                raise TypeError(
                    Msg.WRONG_TYPE.format(value, type(value), value_type)
                )
            if not isinstance(value, int | float | str | Enum) and validate:
                with contextlib.suppress(Exception):
                    check = value.validate()
        return check

    @staticmethod
    def verify_tuple_type(name: list[Any], value_type: Any) -> bool:
        """Check if each member of the tuple has the specified type."""
        if name != [] and name is not None:
            for value in name:
                DefCheck.verify_type(value, value_type)
        return True

    @staticmethod
    def verify_enum(value: str, enumeration: Any) -> bool:
        """Check if the value is in the proper enumation."""
        if value not in enumeration:
            raise ValueError(Msg.NOT_VALID_ENUM.format(value, enumeration))
        return True

    @staticmethod
    def verify_choice(value: str, choice: frozenset[str]) -> bool:
        """Check if the value is available to choose from.

        Some GEDCOM structures involve more than one tag.  The permitted
        tags are in an enumeration set.  This method validates that
        the choice the user made was in the enumeration set.

        Example:
            This test shows that the value of Tag.GIVN which is "GIVN" is in
            the set of accepted values for a Personal Name Piece structure.
            >>> from chronodata.methods import DefCheck
            >>> from chronodata.enums import Tag
            >>> from chronodata.constants import Choice
            >>> DefCheck.verify_choice(Tag.GIVN.value, Choice.PERSONAL_NAME_PIECE)
            True

        Args:
            value: The value of the Tag, not the name of the Tag itself.
            choice: The set the available choices for the value.

        Returns:
            True: If the value of the Tag is in the available choices.
            False: If the value of the Tag is not in the available choices.
        """
        if value not in choice:
            raise ValueError(Msg.NOT_VALID_CHOICE.format(value, choice))
        return True

    # @staticmethod
    # def verify_dict_key(value: str, dictionary: dict[str, str]) -> bool:
    #     """Check if the value is in the proper dictionary."""
    #     DefCheck.verify_type(value, str)
    #     if (
    #         value != ''
    #         and value not in dictionary
    #         and value not in dictionary.values()
    #     ):
    #         raise ValueError(Msg.NOT_VALID_KEY.format(value, dictionary))
    #     return True

    @staticmethod
    def display_dictionary(dictionary: dict[str, str]) -> pd.DataFrame:
        pd.set_option('display.max_rows', None)
        return pd.DataFrame.from_dict(
            dictionary, orient='index', columns=['Value']
        )

    # @staticmethod
    # def get_dict_key_values(
    #     query: str, dictionary: dict[str, str]
    # ) -> list[str]:
    #     """Return all items found in the dictionary matching either key or value."""
    #     found: list[str] = []
    #     if query in dictionary:
    #         found.append(''.join([query, ': ', dictionary[query]]))
    #     for item in dictionary.items():
    #         if query == item[1]:
    #             found.append(''.join([item[0], ': ', item[1]]))
    #     # if query in dictionary.values():
    #     #     for key in dictionary.items():
    #     #         if dictionary[key] == query:
    #     #             found.append(''.join([str(key), ': ', str(query)]))
    #     return found

    @staticmethod
    def verify_not_default(value: Any, default: Any) -> bool:
        """Check that the value is not the default value.

        If the value equals the default value in certain structures,
        the structure is empty.  Further processing on it can stop.
        In particular the output of its `ged` method is the empty string.

        Examples:
            The first example checks that the empty string is recognized
            as the default value of the empty string.
            >>> from chronodata.methods import DefCheck
            >>> DefCheck.verify_not_default('', '')
            Traceback (most recent call last):
            ValueError: The value "" cannot be the default value "".

            The second example checks that a non-empty string
            is not identified as the default.
            >>> DefCheck.verify_not_default('not empty', '')
            True

        Args:
            value: What needs to be checked against the `default` value.
            default: The value to compare with `value`.

        Exception:
            ValueError: An exception is raised if the value is the default value.

        Returns:
            True: If the value does not equal the default value and an exception
                has not been raised.
        """
        if value == default:
            raise ValueError(Msg.NOT_DEFAULT.format(value, default))
        return True

    @staticmethod
    def verify_range(
        value: int | float, low: int | float, high: int | float
    ) -> bool:
        """Check if the value is inclusively between low and high boundaries."""
        if not low <= value <= high:
            raise ValueError(Msg.RANGE_ERROR.format(value, low, high))
        return True

    @staticmethod
    def verify_not_negative(value: int | float) -> bool:
        """Check if the value is a positive number."""
        if value < 0:
            raise ValueError(Msg.NEGATIVE_ERROR.format(value))
        return True


class DefDate:
    """Global methods supporting date processing."""

    @staticmethod
    def ged_date(
        iso_date: str = String.NOW,
        calendar: str = 'GREGORIAN',
        epoch: bool = True,
    ) -> tuple[str, str]:
        """Obtain the GEDCOM date and time from an ISO date and time or the
        current UTC timestamp in GEDCOM format.

        Args:
            iso_date: The ISO date or `now` for the current date and time.
            calendar: The GEDCOM calendar to use when returning the date.
            epoch: Return the epoch, `BCE`, for the GEDCOM date if it is before
                the current epoch.  Set this to `False` to not return the epoch.
                This only applies to dates prior to 1 AD.

        References
        ----------

        Exceptions:

        """
        datetime: str = str(np.datetime64(iso_date))
        date, time = datetime.split(String.T)
        date_pieces = date.split(String.HYPHEN)
        if len(date_pieces) == 3:
            year: str = date_pieces[0]
            month: str = date_pieces[1]
            day: str = date_pieces[2]
        else:
            year = date_pieces[1]
            month = date_pieces[2]
            day = date_pieces[3]
        ged_time: str = ''.join([time, String.Z])
        good_calendar: str | bool = Cal.CALENDARS.get(String.GREGORIAN, False)
        if not good_calendar:
            logging.critical(Msg.BAD_CALENDAR.format(calendar))
            raise ValueError(Msg.BAD_CALENDAR.format(calendar))
        month_code: str = Cal.CALENDARS[calendar][String.MONTH_NAMES].get(
            month, False
        )
        if not month_code:
            logging.critical(Msg.BAD_MONTH.format(calendar, month))
            raise ValueError(Msg.BAD_MONTH.format(calendar, month))
        ged_date: str = ''
        if epoch and len(date_pieces) == 4:
            ged_date = ''.join(
                [
                    day,
                    String.SPACE,
                    month_code,
                    String.SPACE,
                    year,
                    String.SPACE,
                    String.BC,
                ]
            )
        else:
            ged_date = ''.join(
                [day, String.SPACE, month_code, String.SPACE, year]
            )
        return ged_date, ged_time

    @staticmethod
    def iso_date(
        ged_date: str,
        ged_time: str = '',
        calendar: str = String.GREGORIAN,
    ) -> str:
        """Return an ISO date and time given a GEDCOM date and time."""
        day: str
        month: str
        year: str
        day, month, year = ged_date.split(String.SPACE)
        time: str = ged_time.split(String.Z)[0]
        good_calendar: str | bool = Cal.CALENDARS[calendar].get(
            String.GREGORIAN, False
        )
        if not good_calendar:
            logging.critical(Msg.BAD_CALENDAR.format(calendar))
            raise ValueError(Msg.BAD_CALENDAR.format(calendar))
        month_code: str = Cal.CALENDARS[calendar].get(month, False)
        if not month_code:
            logging.critical(Msg.BAD_MONTH.format(calendar, month))
            raise ValueError(Msg.BAD_MONTH.format(calendar, month))
        iso_datetime: str = ''.join(
            [
                year,
                String.HYPHEN,
                month_code,
                String.HYPHEN,
                day,
                String.T,
                time,
            ]
        )
        return iso_datetime

    @staticmethod
    def now(level: int = 2) -> str:
        """Return the current UTC date and time rather than an entered value.

        This will be returned as a list of two lines for a GEDCOM file.
        This method will not likely be needed by the builder of a chronology
        unless the builder wants to enter the current date and time into
        the chronology. The current date and time is automatically
        entered for each record as its creation date and time
        as well as its change date and time.

        Return
        ------
        A list containing two strings is returned. The first member of
        the list is the date formatted to be used in a GEDCOM file.
        The second member of the list is the time formatted to
        be used in a GEDCOM file.

        Example
        -------
        >>> from chronodata.methods import DefDate  # doctest: +ELLIPSIS
        >>> print(DefDate.now())
        2 DATE ...
        3 TIME ...
        <BLANKLINE>

        Changing the level adjusts the level numbers for the two returned strings.

        >>> print(DefDate.now(level=5))
        5 DATE ...
        6 TIME ...
        <BLANKLINE>

        See Also
        --------
        - `creation_date`
        - `change_date`
        - `header`
        """
        date: str
        time: str
        date, time = DefDate.ged_date()
        return ''.join(
            [
                DefTag.taginfo(level, Tag.DATE, date),
                DefTag.taginfo(level + 1, Tag.TIME, time),
            ]
        )

    @staticmethod
    def creation_date() -> str:
        """Return three GEDCOM lines showing a line with a creation tag (CREA)
        and then two automatically generated
        UTC date and time lines.  These are used to
        show when a record has been created.

        See Also
        --------
        - `now`: the method that generates the current UTC date and time
        - `family`: the method creating the family record (FAM)
        - `individual`: the method creating the individual record (INDI)
        - `multimedia`: the method creating the multimedia record (OBJE)
        - `repository`: the method creating the repository record (REPO)
        - `shared_note`: the method creating the shared note record (SNOTE)
        - `source`: the method creating the source record (SOUR)
        - `submitter`: the method creating the submitter record (SUBM)
        """
        return ''.join([DefTag.taginfo(1, Tag.CREA), DefDate.now()])
