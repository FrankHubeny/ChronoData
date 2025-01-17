# chronodata/tuples.py
# Licensed under a 3-clause BSD style license - see LICENSE.md
"""NamedTuples to store, validate and display data
entered by the user for a genealogy.

The NamedTuples are based on the GEDCOM standard with others
added to aid the user in collecting the data.

Each of the NamedTuples have two methods:
    validate: Return True if the data can be used or
        an error message otherwise.
    ged: Display the data in the GEDCOM format.

Examples:


"""

__all__ = [
    'Address',
    'Age',
    'Alias',
    'Association',
    'CallNumber',
    'Checker',
    'Child',
    'Date',
    'DateExact',
    'DateValue',
    'Dater',
    'EventDetail',
    'Exid',
    'Family',
    'Family',
    'FamilyAttribute',
    'FamilyChild',
    'FamilyEvent',
    'FamilyEventDetail',
    'FamilySpouse',
    'FamilyXref',
    'File',
    'FileTranslations',
    'Formatter',
    'Header',
    'Husband',
    'Identifier',
    'Individual',
    'Individual',
    'IndividualAttribute',
    'IndividualEvent',
    'IndividualEventDetail',
    'IndividualXref',
    'LDSIndividualOrdinance',
    'LDSOrdinanceDetail',
    'LDSSpouseSealing',
    'Map',
    'Multimedia',
    'Multimedia',
    'MultimediaLink',
    'MultimediaXref',
    'NameTranslation',
    'NonEvent',
    'Note',
    'NoteTranslation',
    'PersonalName',
    'PersonalNamePieces',
    'Place',
    'PlaceTranslation',
    'Placer',
    'Repository',
    'Repository',
    'RepositoryXref',
    'Schema',
    'SharedNote',
    'SharedNote',
    'SharedNoteXref',
    'Source',
    'Source',
    'SourceCitation',
    'SourceData',
    'SourceEvent',
    'SourceRepositoryCitation',
    'SourceXref',
    'Submitter',
    'Submitter',
    'SubmitterXref',
    'Tagger',
    'Text',
    'Time',
    'Void',
    'Wife',
]

import contextlib
import logging
import math
import re
import urllib.request
from enum import Enum
from textwrap import dedent, indent
from typing import Any, ClassVar, Literal, NamedTuple

import numpy as np
import yaml  # type: ignore[import-untyped]

from chronodata.constants import (
    Adop,
    Cal,
    Default,
    Event,
    FamAttr,
    # FamcStat,
    FamEven,
    GreaterLessThan,
    Id,
    IndiAttr,
    IndiEven,
    MediaType,
    Medium,
    NameType,
    Quay,
    Resn,
    Role,
    Sex,
    Stat,
    String,
    Tag,
    Value,
)
from chronodata.gedcom import Specs
from chronodata.messages import Example, Msg

YNull = Literal['Y'] | None


class Tagger:
    """Global methods to tag GEDCOM information.

    There are five methods.
    - `clean_input` makes sure that user input does not contain banned utf-8 strings.
    - `taginfo` performs the base tagging process calling clean_input on user input.
    - `empty` constructs a tag where there is no user input.
    - `string` constructs a tag on user input or a list of a similar type of user input.
    - `structure` runs the ged method on an already tagged structure or a list of
        similar structures adding them to the final GEDCOM string.
    """

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

        Examples:


        Reference:
            - [GEDCOM Characters](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#characters)
            - [Unicode Specification](https://www.unicode.org/versions/Unicode16.0.0/#Summary)
            - [Python re Module](https://docs.python.org/3/library/re.html)
        """

        return re.sub(String.BANNED, String.EMPTY, input)

    @staticmethod
    def taginfo(
        level: int,
        tag: Tag,
        payload: str = String.EMPTY,
        extra: str = String.EMPTY,
        format: bool = True,
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
            >>> from chronodata.constants import Tag
            >>> from chronodata.store import Tagger
            >>> print(Tagger.taginfo(1, Tag.NAME, '  Some Name'))
            1 NAME   Some Name
            <BLANKLINE>

            There can also be an extra parameter.
            >>> print(Tagger.taginfo(1, Tag.NAME, 'SomeName', 'Other info'))
            1 NAME SomeName Other info
            <BLANKLINE>

            This example comes from the [GEDCOM lines standard](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#lines):
            Note how the `@me` was reformatted as `@@me`.
            > 1 NOTE me@example.com is my email
            > 2 CONT @@me and @I are my social media handles
            >>> from chronodata.store import Note
            >>> mynote = Note(
            ...     note='''me@example.com is my email
            ... @me and @I are my social media handles'''
            ... )
            >>> print(mynote.ged(1))
            1 NOTE me@example.com is my email
            2 CONT @@me and @I are my social media handles
            <BLANKLINE>

            However, escaping the '@' should not occur when this is part of a cross-reference identifier.


        Reference:
            [GEDCOM Lines](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#lines)

        """
        lineval: str = payload
        if format and lineval != String.EMPTY and lineval[0] == String.ATSIGN:
            lineval = ''.join([String.ATSIGN, lineval])
        if extra == String.EMPTY:
            if lineval == String.EMPTY:
                return f'{level} {tag.value}{String.EOL}'
            return (
                f'{level} {tag.value} {Tagger.clean_input(lineval)}{String.EOL}'
            )
        return f'{level} {tag.value} {Tagger.clean_input(lineval)} {Tagger.clean_input(extra)}{String.EOL}'

    @staticmethod
    def empty(lines: str, level: int, tag: Tag) -> str:
        """Join a GEDCOM line that has only a level and a tag to a string.

        This method implements the
        [GEDCOM empty LineVal standard](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#lines) which reads:
        > Note that production LineVal does not match the empty string.
        > Because empty payloads and missing payloads are considered equivalent,
        > both a structure with no payload and a structure with the empty string
        > as its payload are encoded with no LineVal and no space after the Tag.

        Example:
            >>> from chronodata.store import Tagger
            >>> from chronodata.constants import Tag
            >>> lines = ''
            >>> line = Tagger.empty(lines, 1, Tag.MAP)
            >>> print(line)
            1 MAP
            <BLANKLINE>

        Args:
            lines: The prefix of the returned string.
            level: The GEDCOM level of the structure.
            tag: The tag to apply to this line.

        """
        return ''.join([lines, Tagger.taginfo(level, tag)])

    @staticmethod
    def string(
        lines: str,
        level: int,
        tag: Tag,
        payload: list[str] | str,
        extra: str = String.EMPTY,
        format: bool = True,
    ) -> str:
        """Join a string or a list of string to GEDCOM lines.

        This method hides the concatenation of the already constructed
        GEDCOM file with the new line and the check that this should only
        be done if the payload is not empty.  It also hides checking
        whether the string is part of a list or not.

        Examples:
            Suppose there is only one string that should be tagged.
            >>> from chronodata.store import Tagger
            >>> lines = ''
            >>> lines = Tagger.empty(lines, 1, Tag.MAP)
            >>> lines = Tagger.string(lines, 2, Tag.LATI, 'N30.0')
            >>> lines = Tagger.string(lines, 2, Tag.LONG, 'W30.0')
            >>> print(lines)
            1 MAP
            2 LATI N30.0
            2 LONG W30.0
            <BLANKLINE>

            Suppose there are a list of strings that should be tagged.
            >>> lines = ''
            >>> wwws = [
            ...     'https://here.com',
            ...     'https://there.com',
            ...     'https://everywhere.com',
            ... ]
            >>> lines = Tagger.string(lines, 3, Tag.WWW, wwws)
            >>> print(lines)
            3 WWW https://here.com
            3 WWW https://there.com
            3 WWW https://everywhere.com
            <BLANKLINE>

        Args:
            lines: The prefix string that will be appended to.
            level: The GEDCOM level of the structure.
            tag: The tag to apply to this line.
            records: The list of strings to tag.
        """

        if isinstance(payload, list):
            for item in payload:
                if String.EOL in item:
                    items: list[str] = item.split(String.EOL)
                    lines = Tagger.string(
                        lines, level, tag, items[0], format=format
                    )
                    lines = Tagger.string(
                        lines, level + 1, Tag.CONT, items[1:], format=format
                    )
                else:
                    lines = ''.join(
                        [lines, Tagger.taginfo(level, tag, item, format=format)]
                    )
            return lines
        if payload != String.EMPTY and payload is not None:
            if String.EOL in payload:
                payloads: list[str] = payload.split(String.EOL)
                lines = Tagger.string(
                    lines, level, tag, payloads[0], format=format
                )
                lines = Tagger.string(
                    lines, level + 1, Tag.CONT, payloads[1:], format=format
                )
            else:
                return ''.join(
                    [
                        lines,
                        Tagger.taginfo(
                            level, tag, payload, extra, format=format
                        ),
                    ]
                )
        return lines

    @staticmethod
    def structure(
        lines: str,
        level: int,
        payload: list[Any] | Any,
        default: Any = None,
        flag: str = String.EMPTY,
    ) -> str:
        """Join a structure or a list of structure to GEDCOM lines.

        This method hides the concatenation of the already constructed
        GEDCOM file with the new line.  It also hides checking
        whether the string is part of a list or not.

        Examples:
            Suppose there is one structure to write to GEDCOM lines.
            >>> from chronodata.store import Map, Tagger
            >>> map1 = Map(30.0, -30.0)
            >>> map2 = Map(-40.0, 20.0)
            >>> lines = ''
            >>> lines = Tagger.structure(lines, 2, map1)
            >>> print(lines)
            2 MAP
            3 LATI N30.000000
            3 LONG W30.000000
            <BLANKLINE>

            Now include both defined maps into a list.
            >>> lines = ''
            >>> lines = Tagger.structure(lines, 4, [map1, map2])
            >>> print(lines)
            4 MAP
            5 LATI N30.000000
            5 LONG W30.000000
            4 MAP
            5 LATI S40.000000
            5 LONG E20.000000
            <BLANKLINE>

        Args:
            lines: The prefix string that will be appended to.
            level: The GEDCOM level of the structure.
            payload: The structure or list of structures from which the lines will be formed.
            flag: An optional item passed to the structure's ged method to modify its behavior.
        """

        if isinstance(payload, list):
            for item in payload:
                if flag != String.EMPTY:
                    lines = ''.join([lines, item.ged(level, flag)])
                else:
                    lines = ''.join([lines, item.ged(level)])
            return lines
        if payload is not None and payload != default:
            if flag != String.EMPTY:
                lines = ''.join([lines, payload.ged(level, flag)])
            else:
                lines = ''.join([lines, payload.ged(level)])
        return lines

    @staticmethod
    def extension(
        lines: str,
        level: int,
        tag: str,
        payload: str,
        extra: str = String.EMPTY,
    ) -> str:
        ext_line: str = String.EMPTY
        if extra == String.EMPTY:
            if payload == String.EMPTY:
                ext_line = f'{level} {tag}{String.EOL}'
            else:
                ext_line = (
                    f'{level} {tag} {Tagger.clean_input(payload)}{String.EOL}'
                )
        else:
            ext_line = f'{level} {tag} {Tagger.clean_input(payload)} {Tagger.clean_input(extra)}{String.EOL}'
        return ''.join([lines, ext_line])


class Checker:
    """Global methods supporting validation of data."""

    @staticmethod
    def verify(when: bool, then: bool, message: str) -> bool:
        """Use conditional logic to test whether to raise a ValueError exception.

        The only time this fails is when the `when` is True,
        but the `then` is False.  In that case a ValueError is raised
        with the value in `message`.  In all other cases, True is returned.

        This helps verify that more complicated GEDCOM criteria are met.

        Examples:
            >>> from chronodata.store import Checker
            >>> message = 'Error!'
            >>> Checker.verify(True, 1 == 2, message)
            Traceback (most recent call last):
            ValueError: Error!

            >>> Checker.verify(True, 1 == 1, message)
            True

            When `when` is False, then True is returned no matter what the
            value of `then` happens to be.
            >>> Checker.verify(False, False, message)
            True

            >>> Checker.verify(False, True, message)
            True

        Args:
            when: If this is True then check the `then` condition, otherwise return True.
            then: If `when` is True and this is not, raise the ValueError.
            message: This is the message used by the ValueError.
        """
        if when and not then:
            raise ValueError(message)
        return True

    @staticmethod
    def verify_ext(
        extensions: set[str], structure: str, substructures: set[str]
    ) -> bool:
        all_structures: set[str] = substructures
        all_structures.add(structure)
        check: bool = True
        for extension in extensions:
            if extension not in all_structures:
                check = False
                raise ValueError(
                    Msg.NOT_DEFINED_FOR_STRUCTURE.format(extension)
                )
        return check

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
                Checker.verify_type(value, value_type)
        return True

    @staticmethod
    def verify_enum(value: str, enumeration: Any) -> bool:
        """Check if the value is in the proper enumation."""
        if value not in enumeration:
            raise ValueError(Msg.NOT_VALID_ENUM.format(value, enumeration))
        return True

    @staticmethod
    def verify_not_default(value: Any, default: Any) -> bool:
        """Check that the value is not the default value.

        If the value equals the default value in certain structures,
        the structure is empty.  Further processing on it can stop.
        In particular the output of its `ged` method is the empty string.

        Examples:
            The first example checks that the empty string is recognized
            as the default value of the empty string.
            >>> from chronodata.store import Checker
            >>> Checker.verify_not_default('', '')
            Traceback (most recent call last):
            ValueError: The value "" cannot be the default value "".

            The second example checks that a non-empty string
            is not identified as the default.
            >>> Checker.verify_not_default('not empty', '')
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


class Dater:
    """Global methods supporting date processing."""

    @staticmethod
    def ged_date(
        iso_date: str = String.NOW,
        calendar: str = 'GREGORIAN',
        epoch: bool = True,
    ) -> tuple[str, str]:
        """Obtain the GEDCOM date and time from an ISO 8601 date and time for the
        current UTC timestamp in GEDCOM format.

        Examples:
            The ISO date for January 1, 2000 at 1:15:30 AM would be `20000101 01:15:30`.
            >>> from chronodata.store import Dater
            >>> print(Dater.ged_date(iso_date='2000-01-01T01:15:30'))
            ('01 JAN 2000', '01:15:30Z')

            Viewing this same date in BC context we would have:
            >>> print(Dater.ged_date(iso_date='-2000-01-01T01:15:30'))
            ('01 JAN 2000 BCE', '01:15:30Z')

            There is no zero year in the Gregorian Calendar and neither
            does the ISO 8601 standard have a zero year.
            >>> print(Dater.ged_date(iso_date='0-01-01T01:15:30'))
            Traceback (most recent call last):
            ValueError: The calendar has no zero year.

        Args:
            iso_date: The ISO date or `now` for the current date and time.
            calendar: The GEDCOM calendar to use when returning the date.
            epoch: Return the epoch, `BCE`, for the GEDCOM date if it is before
                the current epoch.  Set this to `False` to not return the epoch.
                This only applies to dates prior to 1 AD starting at 1 BC.

        References:
            [Wikipedia ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)

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
        if int(year) == 0:
            raise ValueError(Msg.ZERO_YEAR)
        ged_time: str = ''.join([time, String.Z])
        good_calendar: str | bool = Cal.CALENDARS.get(String.GREGORIAN, False)
        if not good_calendar:
            raise ValueError(Msg.BAD_CALENDAR.format(calendar))
        month_code: str = Cal.CALENDARS[calendar][String.MONTH_NAMES].get(
            month, False
        )
        if not month_code:
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
        ged_time: str = String.EMPTY,
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
        This method will not likely be needed by the builder of a genealogy
        unless the builder wants to enter the current date and time into
        the genealogy. The current date and time is automatically
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
        >>> from chronodata.store import Dater  # doctest: +ELLIPSIS
        >>> print(Dater.now())
        2 DATE ...
        3 TIME ...
        <BLANKLINE>

        Changing the level adjusts the level numbers for the two returned strings.

        >>> print(Dater.now(level=5))
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
        date, time = Dater.ged_date()
        return ''.join(
            [
                Tagger.taginfo(level, Tag.DATE, date),
                Tagger.taginfo(level + 1, Tag.TIME, time),
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
        return ''.join([Tagger.taginfo(1, Tag.CREA), Dater.now()])


class Placer:
    """Global methods to support place data."""

    @staticmethod
    def to_decimal(
        degrees: int, minutes: int, seconds: float, precision: int = 6
    ) -> float:
        """Convert degrees, minutes and seconds to a decimal.

        Example:
            The specification for the LATI and LONG structures (tags) offer the
            following example.
            >>> from chronodata.store import Placer
            >>> Placer.to_decimal(168, 9, 3.4, 6)
            168.150944

        Args:
            degrees: The degrees in the angle whether latitude or longitude.
            minutes: The minutes in the angle.
            seconds: The seconds in the angle.
            precision: The number of digits to the right of the decimal point.

        See Also:
            - `to_dms`: Convert a decimal to degrees, minutes, seconds to a precision.

        Reference:
            [GEDCOM LONG structure](https://gedcom.io/terms/v7/LONG)
            [GEDCOM LATI structure](https://gedcom.io/terms/v7/LATI)

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

        >>> from chronodata.store import Placer
        >>> Placer.to_dms(49.29722222222, 10)
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

    @staticmethod
    def form(form1: str, form2: str, form3: str, form4: str) -> str:
        return ''.join(
            [
                form1,
                String.LIST_ITEM_SEPARATOR,
                form2,
                String.LIST_ITEM_SEPARATOR,
                form3,
                String.LIST_ITEM_SEPARATOR,
                form4,
            ]
        )

    @staticmethod
    def place(place1: str, place2: str, place3: str, place4: str) -> str:
        return ''.join(
            [
                place1,
                String.LIST_ITEM_SEPARATOR,
                place2,
                String.LIST_ITEM_SEPARATOR,
                place3,
                String.LIST_ITEM_SEPARATOR,
                place4,
            ]
        )


class Formatter:
    """Methods to support formatting strings to meet the GEDCOM standard."""

    @staticmethod
    def phone(data: str) -> str:
        """Format a phone string to meet the GEDCOM standard."""
        return data

    @staticmethod
    def email(data: str) -> str:
        """Format an email string to meet the GEDCOM standard."""
        return data

    @staticmethod
    def fax(data: str) -> str:
        """Format a fax string to meet the GEDCOM standard."""
        return data

    @staticmethod
    def www(data: str) -> str:
        """Format a url string to meet the GEDCOM standard."""
        return data

    @staticmethod
    def listcodes(items: Any, level: int = 1) -> str:
        if isinstance(items, str):
            return ''.join(["'", items, "'"])
        if isinstance(items, list):
            if len(items) == 0:
                return String.LEFT_RIGHT_BRACKET
            lines: str = String.LEFT_BRACKET
            for item in items:
                lines = ''.join([lines, item.code(level), String.COMMA])
            return ''.join(
                [
                    lines,
                    String.EOL,
                    String.INDENT * (level - 1),
                    String.RIGHT_BRACKET,
                ]
            )
        code_lines: str = (
            items.code(level)
            .replace(String.EOL, String.EMPTY, 1)
            .replace(String.INDENT, String.EMPTY, 1)
        )
        return code_lines

    @staticmethod
    def example(
        code_preface: str,
        show_code: str,
        gedcom_preface: str,
        show_ged: str,
        gedcom_docs: str,
        genealogy_docs: str,
    ) -> str:
        return ''.join(
            [
                code_preface,
                String.EOL,
                show_code,
                String.DOUBLE_NEWLINE,
                gedcom_preface,
                String.DOUBLE_NEWLINE,
                show_ged,
                String.EOL,
                gedcom_docs,
                String.EOL,
                genealogy_docs,
            ]
        )


class Xref:
    def __init__(self, name: str, tag: Tag = Tag.NONE):
        """Initialize an instance of the class.

        Args:
        - `name`: The name of the identifier.
        """
        self.fullname: str = name
        self.name: str = name.replace('@', '').replace('_', ' ')
        self.tag: Tag = tag
        self.code_xref = f'{self.tag.value.lower()}_{self.name.lower()}_xref'
        #self.code = f'{self.tag.value.lower()}_{self.name.lower()}'

    def __str__(self) -> str:
        """Return the name used by the GEDCOM standard."""
        return self.fullname

    def ged(self, info: str = String.EMPTY) -> str:
        """Return the identifier formatted according to the GEDCOM standard."""
        if info == String.EMPTY:
            return f'0 {self.fullname} {self.tag.value}{String.EOL}'
        return f'0 {self.fullname} {self.tag.value} {info}{String.EOL}'
    
    def code(self) -> str:
        return self.fullname


class FamilyXref(Xref):
    """Assign the FamilyXref type to a string.

    This class is not instantiated directly, but only through
    the `chronodata.build.family_xref()` method.

    Args:
        name: The name of the identifier.

    See Also:
        chronodata.build.family_xref()
    """

    def __init__(self, name: str, tag: Tag = Tag.FAM):
        super().__init__(name, tag)


class IndividualXref(Xref):
    """Assign the IndividualXref type to a string.

    This class is not instantiated directly, but only through
    the `chronodata.build.individual_xref()` method.

    Args:
        name: The name of the identifier.

    See Also:
        `chronodata.build.individual_xref()`

    Reference:
        [GEDCOM INDIVIDUAL Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_RECORD)
    """

    def __init__(self, name: str, tag: Tag = Tag.INDI):
        super().__init__(name, tag)


class MultimediaXref(Xref):
    """Assign Assign the MultimediaXref type to a string.

    This class is not instantiated directly, but only through
    the `chronodata.build.multimedia_xref()` method.

    Args:
        name: The name of the identifier.

    See Also:
        `chronodata.build.multimedia_xref()`

    Reference:
        [GEDCOM MULTIMEDIA Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#MULTIMEDIA_RECORD)
    """

    def __init__(self, name: str, tag: Tag = Tag.OBJE):
        super().__init__(name, tag)


class RepositoryXref(Xref):
    """Assign the RepositoryXref type to a string.

    This class is not instantiated directly, but only through
    the `chronodata.build.repository_xref()` method.

    Args:
        name: The name of the identifier.

    See Also:
        `chronodata.build.repository_xref()`

    Reference:
        https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#REPOSITORY_RECORD
    """

    def __init__(self, name: str, tag: Tag = Tag.REPO):
        super().__init__(name, tag)


class SharedNoteXref(Xref):
    """Assign the SharedNoteXref type to a string.

    This class is not instantiated directly, but only through
    the `chronodata.build.shared_note_xref()` method.

    Args:
        name: The name of the identifier.

    See Also:
        `chronodata.build.shared_note_xref()`

    Reference:
        - [GEDCOM SHARED_NOTE Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SHARED_NOTE_RECORD)
    """

    def __init__(self, name: str, tag: Tag = Tag.SNOTE):
        super().__init__(name, tag)


class SourceXref(Xref):
    """Assign the SourceXref type to a string.

    This class is not instantiated directly, but only through
    the `chronodata.build.source_xref()` method.

    Args:
        name: The name of the identifier.

    See Also:
        `chronodata.build.source_xref()`

    Reference:
        [GEDCOM SOURCE Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SHARED_NOTE_RECORD)
    """

    def __init__(self, name: str, tag: Tag = Tag.SOUR):
        super().__init__(name, tag)


class SubmitterXref(Xref):
    """Assign the SubmitterXref type to a string.

    This class is not instantiated directly, but only through
    the `chronodata.build.submitter_xref()` method.

    Args:
        name: The name of the identifier.

    See Also:
        chronodata.build.submitter_xref()

    Reference:
        [GEDCOM SUBMITTER Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SUBMITTER_RECORD)
    """

    def __init__(self, name: str, tag: Tag = Tag.SUBM):
        super().__init__(name, tag)


class Void:
    NAME: str = '@VOID@'
    FAM: FamilyXref = FamilyXref(NAME)
    INDI: IndividualXref = IndividualXref(NAME)
    OBJE: MultimediaXref = MultimediaXref(NAME)
    REPO: RepositoryXref = RepositoryXref(NAME)
    SNOTE: SharedNoteXref = SharedNoteXref(NAME)
    SOUR: SourceXref = SourceXref(NAME)
    SUBM: SubmitterXref = SubmitterXref(NAME)


class Schema:
    """Store, validate and display schema information.

    An underline is added to the front of the new tag if one is not there already.
    Also the tag to made upper case.

    This class holds multiple schema tags for the header record.  It is not a separate
    GEDCOM structure.

    Examples:
        Consider making a _DATE extention tag based on the GEDCOM specification for
        the standard DATE tag.
        >>> from chronodata.store import Schema
        >>> date = Schema('date', 'https://gedcom.io/terms/v7/DATE')
        >>> print(date.ged(1))
        2 TAG _DATE https://gedcom.io/terms/v7/DATE
        <BLANKLINE>

        We can put this into the header record as an extension tag as follows.
        >>> from chronodata.store import Header
        >>> header = Header(schema_tags=[date])
        >>> print(header.ged())
        0 HEAD
        1 GEDC
        2 VERS 7.0
        1 SCHMA
        2 TAG _DATE https://gedcom.io/terms/v7/DATE
        <BLANKLINE>




    Args:
        tag: The tag used for the schema information.
        url: The required url defining the payload of the tag.  This url will be accessed
            and its contents stored.  It will be used to check the proper placement
            of the extension tag.

    See Also:
        `header`

    Returns:
        A string representing a GEDCOM line for this tag.

    Reference:
        [GENCOM Extensions](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#extensions)

    >  +1 SCHMA                                 {0:1}  [g7:SCHMA](https://gedcom.io/terms/v7/SCHMA)
    >     +2 TAG <Special>                      {0:M}  [g7:TAG](https://gedcom.io/terms/v7/TAG)
    """

    def __init__(self, tag: str, url: str) -> None:
        self.raw_tag: str = tag
        self.url: str = url
        self.tag: str = ''.join([String.UNDERLINE, self.raw_tag.upper()])
        self.webUrl = urllib.request.urlopen(self.url)
        self.result_code = str(self.webUrl.getcode())
        raw: str = self.webUrl.read().decode('utf-8')
        raw2: str = raw[raw.find('%YAML') :]
        self.yaml: str = raw2[: raw2.find('...')]
        self.yamldict: dict[str, Any] = yaml.safe_load(self.yaml)
        self.substructures: set[str] = self.yamldict['substructures']
        self.superstructures: set[str] = self.yamldict['superstructures']
        self.supers: set[str] = {
            s[s.rfind('/') + 1 :] for s in self.superstructures
        }
        self.specification: str = self.yamldict['specification']
        self.payload_type: Any = self.yamldict['payload']

    def validate(self) -> bool:
        check: bool = Checker.verify_type(
            self.tag, str
        ) and Checker.verify_type(self.url, str)
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            ext_tag: str = self.tag.upper()
            if ext_tag[0] != String.UNDERLINE:
                ext_tag = ''.join([String.UNDERLINE, ext_tag])
            lines = Tagger.string(
                lines, level + 1, Tag.TAG, ext_tag, str(self.url)
            )
        return lines


class Extension(NamedTuple):
    """Store, validate and display extension tags.

    Reference:
        [GedCOM Extensions](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#extensions)
    """

    level: int
    schema: Schema
    payload: str = String.EMPTY
    extra: str = String.EMPTY

    def __str__(self) -> str:
        if self.extra == String.EMPTY:
            return f'Extension({self.schema.tag}, {self.payload})'
        return f'Extension({self.schema.tag}, {self.payload}, {self.extra})'

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.level, int)
            and Checker.verify_type(self.schema, Schema)
            and Checker.verify_type(self.payload, str)
            and Checker.verify_type(self.extra, str)
        )
        return check

    def ged(self, level: int = 1) -> str:
        lines: str = ''
        if self.validate():
            lines = Tagger.extension(
                lines,
                level,
                ''.join([String.UNDERLINE, self.schema.tag.upper()]),
                self.payload,
                self.extra,
            )
        return lines


class Date(NamedTuple):
    """Validate and display date data in various formats.

    Dates are entered based on a Gregorian calendar. This calendar
    does not have a 0 year.  The year 1 BC is entered as `-1`.

    A default value of `0` for any date component means that the component
    will not be displayed.

    The GEDCOM standard allows a week without specifying the other components.

    Parameters:
        year


    Examples:

    Reference:
        [GEDCOM DATE](https://gedcom.io/terms/v7/DATE)
        [GEDCOM DATE type](https://gedcom.io/terms/v7/type-Date)
    """

    year: int = 0
    month: int = 0
    day: int = 0
    week: int = 0
    calendar: str = Value.GREGORIAN

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.year, int)
            and Checker.verify_type(self.month, int)
            and Checker.verify_type(self.day, int)
            and Checker.verify_type(self.week, int)
            and Checker.verify_range(self.week, 0, 52)
            and Checker.verify_range(self.month, 0, 12)
            # and if self.year == 0:
            #     raise ValueError(Msg.NO_ZERO_YEAR.format(self.year, self.calendar))
        )
        return check

    def ged(self, level: int = 1, calendar: str = Value.GREGORIAN) -> str:
        """Display the validated date in GEDCOM format.

        Reference
        ---------
        - [GEDCOM Standard V 7.0](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#date)
        """
        lines: str = ''
        if self.validate():
            # day_str: str = (
            #     str(self.day) if self.day > 9 else ''.join(['0', str(self.day)])
            # )
            month_str: str = (
                str(self.month)
                if self.month > 9
                else ''.join(['0', str(self.month)])
            )
            year_str: str = str(self.year)
            if self.year < 0:
                year_str = ''.join(
                    [str(-self.year), Cal.CALENDARS[calendar][Value.EPOCH]]
                )
            formatted_date: str = ''
            if self.day != 0:
                formatted_date = ''.join([formatted_date, f' {self.day!s}'])
            if self.month != 0:
                formatted_date = ''.join(
                    [
                        formatted_date,
                        f' {Cal.CALENDARS[calendar][Value.MONTH_NAMES][str(month_str)]}',
                    ]
                )
            if self.year != 0:
                formatted_date = ''.join(
                    [formatted_date, f' {year_str}\n']
                ).strip()
            lines = Tagger.string(lines, level, Tag.DATE, formatted_date)
        return lines

    def iso(self) -> str:
        """Return the validated ISO format for the date.

        References
        ----------
        - [ISO 8601 Standard](https://www.iso.org/iso-8601-date-and-time-format.html)
        - [Wikipedia Overview](https://en.wikipedia.org/wiki/ISO_8601)
        """
        if self.validate():
            return f'{self.year}-{self.month}-{self.day}'
        return ''

    def code(self, level: int = 0) -> str:
        spaces: str = String.INDENT * level
        return indent(
            f"""
Date(
    year = {self.year},
    month = '{self.month}',
    day = '{self.day}',
    week = '{self.week}',
    calendar = '{self.calendar}',
)""",
            spaces,
        )

    def example(self, choice: int = Default.CHOICE) -> str:
        """Produce four examples of ChronoData code and GEDCOM output lines and link to
        the GEDCOM documentation.

        The following levels are available:
        - 0 (Default) Produces an empty example with no GEDCOM lines.
        - 1 Produces an example with all arguments containing data.
        - 2 Produces an alternate example with possibly some arguments missing.
        - 3 Produces either another alternate example or an example with non-Latin
            character texts.

        Any other value passed in will produce the same as the default level.

        Args:
            choice: The example one chooses to display.
        """
        show: Date
        gedcom_docs: str = Specs.DATE
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = Date(
                    year=2024,
                    month=10,
                    day=10,
                    week=0,
                    calendar=Value.GREGORIAN,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Date(
                    year=2024,
                    month=10,
                    day=10,
                    week=0,
                    calendar=Value.GREGORIAN,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Date(
                    year=2024,
                    month=10,
                    day=10,
                    week=0,
                    calendar=Value.GREGORIAN,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Date()
                code_preface = Example.EMPTY_CODE
                gedcom_preface = Example.EMPTY_GEDCOM
        return Formatter.example(
            code_preface,
            show.code(),
            gedcom_preface,
            show.ged(),
            gedcom_docs,
            genealogy_docs,
        )


class Time(NamedTuple):
    """Validate and display time data in various formats.

    The standard does not permit leap seconds nor end of day instant (24:00:00).

    Reference
    ---------
    - [GEDCOM Time Data Type](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#time)
    """

    hour: int = 0
    minute: int = 0
    second: int | float = 0.0
    UTC: bool = False

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.hour, int)
            and Checker.verify_type(self.minute, int)
            and Checker.verify_type(self.second, int | float)
            and Checker.verify_type(self.UTC, bool)
            and Checker.verify_range(self.hour, 0, 23)
            and Checker.verify_range(self.minute, 0, 59)
            and Checker.verify_range(self.second, 0, 59.999999999999)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        hour_str: str = str(self.hour)
        minute_str: str = str(self.minute)
        second_str: str = str(self.second)
        if self.validate():
            if 0 <= self.hour < 10:
                hour_str = ''.join(['0', hour_str])
            if 0 <= self.minute < 10:
                minute_str = ''.join(['0', minute_str])
            if 0 <= self.second < 10:
                second_str = ''.join(['0', second_str])
            if self.UTC:
                second_str = ''.join([second_str, 'Z'])
            return Tagger.taginfo(
                level, Tag.TIME, f'{hour_str}:{minute_str}:{second_str}'
            )
        return ''

    def iso(self) -> str:
        """Return the validated ISO format for the time.

        References:
            [ISO 8601 Standard](https://www.iso.org/iso-8601-date-and-time-format.html)
            [Wikipedia Overview](https://en.wikipedia.org/wiki/ISO_8601)
        """
        if self.validate():
            return f'{self.hour}:{self.minute}:{self.second}'
        return ''
    
    def code(self, level: int = 0) -> str:
        spaces: str = String.INDENT * level
        return indent(
            f"""
Time(
    hour = {self.hour},
    minute = {self.minute},
    second = {self.second},
    UTC = '{self.UTC}',
)""",
            spaces,
        )


class DateExact(NamedTuple):
    """Construct a DATEVALUE structure according to the GEDCOM standard.

    Example
    -------


    Reference
    ---------

    >n DATE <DateValue>                         {1:1}  g7:DATE
    >  +1 TIME <Time>                           {0:1}  g7:TIME
    >  +1 PHRASE <Text>                         {0:1}  g7:PHRASE
    """

    date: Date = Date()
    time: Time = Time()
    phrase: str = Default.EMPTY

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.phrase, str)
            and self.date.validate()
            and self.time.validate()
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = String.EMPTY
        if self.validate():
            lines = Tagger.structure(lines, level, self.date, Date())
            lines = Tagger.structure(lines, level + 1, self.time, Time())
            lines = Tagger.string(lines, level + 1, Tag.PHRASE, self.phrase)
        return lines
    
    def code(self, level: int = 0) -> str:
        date: str = Formatter.listcodes(self.date, level + 1)
        time: str = Formatter.listcodes(self.time, level + 1)
        spaces: str = String.INDENT * level
        return indent(
            f"""
DateExact(
    date = {date},
    time = '{time}',
    phrase = '{self.phrase}',
)""",
            spaces,
        )


class DateValue(NamedTuple):
    """Construct a DATEVALUE structure according to the GEDCOM standard.

    Example
    -------


    Reference
    ---------

    >n DATE <DateValue>                         {1:1}  g7:DATE
    >  +1 TIME <Time>                           {0:1}  g7:TIME
    >  +1 PHRASE <Text>                         {0:1}  g7:PHRASE
    """

    date: Date = Date()
    time: Time = Time()
    phrase: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.phrase, str)
            and self.date.validate()
            and self.time.validate()
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.structure(lines, level, self.date, Date())
            lines = Tagger.structure(lines, level + 1, self.time, Time())
            lines = Tagger.string(lines, level + 1, Tag.PHRASE, self.phrase)
        return lines
    
    def code(self, level: int = 0) -> str:
        date: str = Formatter.listcodes(self.date, level + 1)
        time: str = Formatter.listcodes(self.time, level + 1)
        spaces: str = String.INDENT * level
        return indent(
            f"""
DateExact(
    date = {date},
    time = '{time}',
    phrase = '{self.phrase}',
)""",
            spaces,
        )


class Address(NamedTuple):
    """Store, validate and format address information to be saved to a ged file.

    Example:
        The following is the minimum amount of information for an address.
        >>> from chronodata.store import Address
        >>> mailing_address = Address(
        ...     ['12345 ABC Street', 'South North City, My State 22222'],
        ... )
        >>> mailing_address.validate()
        True
        >>> print(mailing_address.ged(1))
        1 ADDR 12345 ABC Street
        1 CONT South North City, My State 22222
        <BLANKLINE>

        There are five named strings stored in this NamedTuple.
        >>> from chronodata.store import Address
        >>> full_address = Address(
        ...     ['12345 ABC Street', 'South North City, My State 23456'],
        ...     'South North City',
        ...     'My State',
        ...     '23456',
        ...     'USA',
        ... )
        >>> print(full_address.ged(1))
        1 ADDR 12345 ABC Street
        1 CONT South North City, My State 23456
        2 CITY South North City
        2 STAE My State
        2 POST 23456
        2 CTRY USA
        <BLANKLINE>

    Args:
        address: The mailing address with each line being one item of a list.
        city: The city or and empty string to leave this blank.
        state: The state or an empty string to leave this blank.
        postal: The postal code or an empty string to leave this blank.
        country: The country or an empty string to leave this blank.

    Returns:
        A string displaying stored Address data formatted to GEDCOM specifications.

    Reference:
        [GEDCOM Specifications](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#ADDRESS_STRUCTURE)

    > n ADDR <Special>                           {1:1}  [g7:ADDR](https://gedcom.io/terms/v7/ADDR)
    >   +1 ADR1 <Special>                        {0:1}  [g7:ADR1](https://gedcom.io/terms/v7/ADR1)
    >   +1 ADR2 <Special>                        {0:1}  [g7:ADR2](https://gedcom.io/terms/v7/ADR2)
    >   +1 ADR3 <Special>                        {0:1}  [g7:ADR3](https://gedcom.io/terms/v7/ADR3)
    >   +1 CITY <Special>                        {0:1}  [g7:CITY](https://gedcom.io/terms/v7/CITY)
    >   +1 STAE <Special>                        {0:1}  [g7:STAE](https://gedcom.io/terms/v7/STAE)
    >   +1 POST <Special>                        {0:1}  [g7:POST](https://gedcom.io/terms/v7/POST)
    >   +1 CTRY <Special>                        {0:1}  [g7:CTRY](https://gedcom.io/terms/v7/CTRY)
    """

    address: list[str] = []  # noqa: RUF012
    city: str = ''
    state: str = ''
    postal: str = ''
    country: str = ''

    def validate(self) -> bool:
        check: bool = (
            Checker.verify_tuple_type(self.address, str)
            and Checker.verify_type(self.city, str)
            and Checker.verify_type(self.state, str)
            and Checker.verify_type(self.postal, str)
            and Checker.verify_type(self.country, str)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            if len(self.address) > 0:
                lines = Tagger.taginfo(level, Tag.ADDR, self.address[0])
                for line in self.address[1:]:
                    lines = Tagger.string(lines, level, Tag.CONT, line)
            lines = Tagger.string(lines, level + 1, Tag.CITY, self.city)
            lines = Tagger.string(lines, level + 1, Tag.STAE, self.state)
            lines = Tagger.string(lines, level + 1, Tag.POST, self.postal)
            lines = Tagger.string(lines, level + 1, Tag.CTRY, self.country)
        return lines

    def code(self, level: int = 0) -> str:
        spaces: str = String.INDENT * level
        return indent(
            f"""address = Address(
    address = {self.address},
    city = '{self.city}',
    state = '{self.state}',
    postal = '{self.postal}',
    country = '{self.country}',
)""",
            spaces,
        )

    def example(self, choice: int = Default.CHOICE) -> str:
        """Produce four examples of ChronoData code and GEDCOM output lines and link to
        the GEDCOM documentation.

        The following levels are available:
        - 0 (Default) Produces an empty example with no GEDCOM lines.
        - 1 Produces an example with all arguments containing data.
        - 2 Produces an alternate example with possibly some arguments missing.
        - 3 Produces either another alternate example or an example with non-Latin
            character texts.

        Any other value passed in will produce the same as the default level.

        Args:
            choice: The example one chooses to display.
        """
        show: Address
        gedcom_docs: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#ADDRESS_STRUCTURE'
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = Address(
                    ['1600 Pennsylvania Avenue NW', 'Washington, DC 20500'],
                    city='Washington',
                    state='DC',
                    postal='20500',
                    country='USA',
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Address(
                    ['北京市东城区景山前街4号'],
                    city='北京',
                    state='',
                    postal='',
                    country='',
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Address(
                    ['McMurdo Station', 'Antarctica'],
                    city='McMurdo Station',
                    state='',
                    postal='',
                    country='Antarctica',
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Address()
                code_preface = Example.EMPTY_CODE
                gedcom_preface = Example.EMPTY_GEDCOM
        return Formatter.example(
            code_preface,
            show.code(),
            gedcom_preface,
            show.ged(),
            gedcom_docs,
            genealogy_docs,
        )


class Age(NamedTuple):
    """Implement the Age data type in the GEDCOM specification.

    The GEDCOM specification requires that these age components be
    rounded down. The `phrase` parameter allows the user to
    add information about the data provided.

    Examples:
        >>> from chronodata.store import Age
        >>> from chronodata.constants import String
        >>> print(
        ...     Age(
        ...         10,
        ...         greater_less_than='>',
        ...         phrase='Estimated',
        ...     ).ged(1)
        ... )
        1 AGE > 10y
        2 PHRASE Estimated
        <BLANKLINE>
        >>> print(Age(10, 2, 1, 2, '').ged(2))
        2 AGE 10y 2m 1w 2d
        <BLANKLINE>

    Args:
        greater_less_than: The default is '', which means that the age is exact
            to the day.  The option `>` means that the actual age
            is greater than the one provided.  The option `<` means
            that the actual age is less than the one provided.
        years: The number of whole years in the age.
        months: The number of months in addition to the years.
        weeks: The number of weeks in addition to the years and months.
        days: The number of days in addition to any years, months, or weeks provided.
        phrase: Addition information to clarify the data added.

    Returns:
        A GEDCOM string storing this data.

    Exceptions:
        ValueError: If greater_less_than is not one of {'', '<', '>'}.
        ValueError: If any value (except `phrase`) is not an integer.
        ValueError: If any value (except `phrase`) is less than 0.

    Reference:
        [GEDCOM Specification](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#age)

    > Age         = [[ageBound D] ageDuration]
    >
    > ageBound    = "<" / ">"
    > ageDuration = years [D months] [D weeks] [D days]
    >             / months [D weeks] [D days]
    >             / weeks [D days]
    >             / days
    >
    > years   = Integer %x79    ; 35y
    > months  = Integer %x6D    ; 11m
    > weeks   = Integer %x77    ; 8w
    > days    = Integer %x64    ; 21d
    """

    years: int = 0
    months: int = 0
    weeks: int = 0
    days: int = 0
    greater_less_than: str = '>'
    phrase: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_enum(self.greater_less_than, GreaterLessThan)
            and Checker.verify_type(self.years, int)
            and Checker.verify_type(self.months, int)
            and Checker.verify_type(self.weeks, int)
            and Checker.verify_type(self.days, int)
            and Checker.verify_type(self.phrase, str)
            and Checker.verify_not_negative(self.years)
            and Checker.verify_not_negative(self.months)
            and Checker.verify_not_negative(self.weeks)
            and Checker.verify_not_negative(self.days)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format the GEDCOM Age data type."""
        line: str = ''
        info: str = self.greater_less_than
        if self.validate() and (
            self.years > 0 or self.months > 0 or self.weeks > 0 or self.days > 0
        ):
            if self.years > 0:
                info = ''.join([info, f' {self.years!s}y'])
            if self.months > 0:
                info = ''.join([info, f' {self.months!s}m'])
            if self.weeks > 0:
                info = ''.join([info, f' {self.weeks!s}w'])
            if self.days > 0:
                info = ''.join([info, f' {self.days!s}d'])
            info = info.replace('  ', ' ').replace('  ', ' ').strip()
            line = Tagger.string(line, level, Tag.AGE, info)
            line = Tagger.string(line, level + 1, Tag.PHRASE, self.phrase)
        return line

    def code(self, level: int = 0) -> str:
        """Generate the ChronoData code that would produce the GEDCOM lines."""
        spaces: str = String.INDENT * level
        return indent(
            f"""
Age(
    years = {self.years},
    months = {self.months},
    weeks = {self.weeks},
    days = {self.days},
    greater_less_than = '{self.greater_less_than}',
    phrase = '{self.phrase}',
)""",
            spaces,
        )

    def example(self, choice: int = Default.CHOICE) -> str:
        """Produce four examples of ChronoData code and GEDCOM output lines and link to
        the GEDCOM documentation.

        The following levels are available:
        - 0 (Default) Produces an empty example with no GEDCOM lines.
        - 1 Produces an example with all arguments containing data.
        - 2 Produces an alternate example with possibly some arguments missing.
        - 3 Produces either another alternate example or an example with non-Latin
            character texts.

        Any other value passed in will produce the same as the default level.

        Args:
            choice: The example one chooses to display.
        """
        show: Age
        gedcom_docs: str = (
            'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#age'
        )
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = Age(
                    years=10,
                    months=2,
                    weeks=1,
                    days=2,
                    greater_less_than='',
                    phrase='Original text read, "Ten years, two months, one week and two days."',
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Age(
                    years=0,
                    months=2,
                    weeks=0,
                    days=2,
                    greater_less_than='<',
                    phrase='Original text read, "Under two months and two days."',
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Age(
                    years=0,
                    months=0,
                    weeks=40,
                    days=2,
                    greater_less_than='>',
                    phrase='Original text read, "Čtyřicet týdnů a dva dny"',
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Age()
                code_preface = Example.EMPTY_CODE
                gedcom_preface = Example.EMPTY_GEDCOM
        return Formatter.example(
            code_preface,
            show.code(),
            gedcom_preface,
            show.ged(),
            gedcom_docs,
            genealogy_docs,
        )


class PersonalNamePieces(NamedTuple):
    """Store, validate and display values for an optional GEDCOM Personal Name Piece.

    Example:
        This example includes all six of the Personal Name Piece tags.
        >>> from chronodata.store import (
        ...     PersonalNamePieces,
        ... )  # doctest: +ELLIPSIS
        >>> from chronodata.constants import Tag

    Args:
        prefix: An option list of NPFX or name prefixes of the name.
        given: An optional list of GIVN or given names of the name.
        nickname: An optional list of NICK or nicknames for the name.
        surname_prefix: An optional list of SPFX or surname prefixes of the name.
        surname: An optional list of SURN or surnames or last names of the name.
        suffix: An optional list NSFX or name suffixes of the name.

    Returns:
        A GEDCOM string storing this data.

    Reference:
        [GEDCOM Personal Name Pieces](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PERSONAL_NAME_PIECES)

    > n NPFX <Text>                              {0:M}  [g7:NPFX](https://gedcom.io/terms/v7/NPFX)
    > n GIVN <Text>                              {0:M}  [g7:GIVN](https://gedcom.io/terms/v7/GIVN)
    > n NICK <Text>                              {0:M}  [g7:NICK](https://gedcom.io/terms/v7/NICK)
    > n SPFX <Text>                              {0:M}  [g7:SPFX](https://gedcom.io/terms/v7/SPFX)
    > n SURN <Text>                              {0:M}  [g7:SURN](https://gedcom.io/terms/v7/SURN)
    > n NSFX <Text>                              {0:M}  [g7:NSFX](https://gedcom.io/terms/v7/NSFX)
    """

    prefix: list[str] = []  # noqa: RUF012
    given: list[str] = []  # noqa: RUF012
    nickname: list[str] = []  # noqa: RUF012
    surname_prefix: list[str] = []  # noqa: RUF012
    surname: list[str] = []  # noqa: RUF012
    suffix: list[str] = []  # noqa: RUF012

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_tuple_type(self.prefix, str)
            and Checker.verify_tuple_type(self.given, str)
            and Checker.verify_tuple_type(self.nickname, str)
            and Checker.verify_tuple_type(self.surname_prefix, str)
            and Checker.verify_tuple_type(self.surname, str)
            and Checker.verify_tuple_type(self.suffix, str)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.NPFX, self.prefix)
            lines = Tagger.string(lines, level, Tag.GIVN, self.given)
            lines = Tagger.string(lines, level, Tag.NICK, self.nickname)
            lines = Tagger.string(lines, level, Tag.SPFX, self.surname_prefix)
            lines = Tagger.string(lines, level, Tag.SURN, self.surname)
            lines = Tagger.string(lines, level, Tag.NSFX, self.suffix)
        return lines

    def code(self, level: int = 0) -> str:
        spaces: str = String.INDENT * level
        return indent(
            f"""
PersonalNamePieces(
    prefix = {self.prefix},
    given = {self.given},
    nickname = {self.nickname},
    surname_prefix = {self.surname_prefix},
    surname = {self.surname},
    suffix = {self.suffix},
)""",
            spaces,
        )

    def example(self, choice: int = Default.CHOICE) -> str:
        """Produce four examples of ChronoData code and GEDCOM output lines and link to
        the GEDCOM documentation.

        The following levels are available:
        - 0 (Default) Produces an empty example with no GEDCOM lines.
        - 1 Produces an example with all arguments containing data.
        - 2 Produces an alternate example with possibly some arguments missing.
        - 3 Produces either another alternate example or an example with non-Latin
            character texts.

        Any other value passed in will produce the same as the default level.

        Args:
            choice: The example one chooses to display.
        """
        show: PersonalNamePieces
        gedcom_docs: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PERSONAL_NAME_PIECES'
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = PersonalNamePieces(
                    prefix=['Mr', 'Sir'],
                    given=['Tom', 'Thomas'],
                    nickname=['Tommy'],
                    surname_prefix=[],
                    surname=['Smith'],
                    suffix=['Jr'],
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = PersonalNamePieces(
                    prefix=['Mr', 'Sir'],
                    given=['Tom', 'Thomas'],
                    nickname=['Tommy'],
                    surname_prefix=[],
                    surname=['Smith'],
                    suffix=['Jr'],
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = PersonalNamePieces(
                    prefix=['Mr', 'Sir'],
                    given=['Tom', 'Thomas'],
                    nickname=['Tommy'],
                    surname_prefix=[],
                    surname=['Smith'],
                    suffix=['Jr'],
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = PersonalNamePieces()
                code_preface = Example.EMPTY_CODE
                gedcom_preface = Example.EMPTY_GEDCOM
        return Formatter.example(
            code_preface,
            show.code(),
            gedcom_preface,
            show.ged(),
            gedcom_docs,
            genealogy_docs,
        )


class NameTranslation(NamedTuple):
    """Store, validate and display name translations.

    The BCP 47 language tag is a hyphenated list of subtags.
    The [W3C Internationalization](https://www.w3.org/International/questions/qa-choosing-language-tags)
    guide will help one make a decision on which tags to use.
    The [Language Subtag Lookup Tool](https://r12a.github.io/app-subtags/)
    can assist with finding and checking the language tag one would like to use.

    Example:
        In this example, the name "Joe" will be translated as "喬" in Chinese.
        Although the `ged` method to display preforms a validation first,
        this example will show that and then display the data using
        the GEDCOM standard.  No personal name pieces will be displayed.
        >>> from chronodata.store import NameTranslation
        >>> joe_in_chinese = '喬'
        >>> language = 'cmn'
        >>> nt = NameTranslation(joe_in_chinese, language)
        >>> nt.validate()
        True
        >>> print(nt.ged(1))
        1 TRAN 喬
        2 LANG cmn
        <BLANKLINE>

    Args:
        translation: the text of the translation.
        language: the BCP 47 language tag.
        name_pieces: an optional tuple of PersonalNamePieces.

    Returns:
        A GEDCOM string storing this data.

    Reference:
        [GEDCOM Pesonal Name Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PERSONAL_NAME_STRUCTURE)

    This is not a specified GEDCOM structure, but implements this portion of `PersonalNamePieces`.
    > +1 TRAN <PersonalName>                   {0:M}  g7:NAME-TRAN
    >    +2 LANG <Language>                    {1:1}  g7:LANG
    >    +2 <<PERSONAL_NAME_PIECES>>           {0:1}
    """

    translation: str = String.EMPTY
    language: str = String.UNDETERMINED
    pieces: PersonalNamePieces = PersonalNamePieces()

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.translation, str)
            and Checker.verify_type(self.language, str)
            and Checker.verify_type(self.pieces, PersonalNamePieces)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.TRAN, self.translation)
            lines = Tagger.string(lines, level + 1, Tag.LANG, self.language)
            lines = Tagger.structure(
                lines, level + 1, self.pieces, PersonalNamePieces()
            )
        return lines

    def code(self, level: int = 0) -> str:
        pieces: str = Formatter.listcodes(self.pieces, level + 1)
        spaces: str = String.INDENT * level
        return indent(
            f"""
NameTranslation(
    translation = '{self.translation}',
    language = '{self.language}',
    pieces = {pieces},
)""",
            spaces,
        )

    def example(self, choice: int = Default.CHOICE) -> str:
        """Produce four examples of ChronoData code and GEDCOM output lines and link to
        the GEDCOM documentation.

        The following levels are available:
        - 0 (Default) Produces an empty example with no GEDCOM lines.
        - 1 Produces an example with all arguments containing data.
        - 2 Produces an alternate example with possibly some arguments missing.
        - 3 Produces either another alternate example or an example with non-Latin
            character texts.

        Any other value passed in will produce the same as the default level.

        Args:
            choice: The example one chooses to display.
        """
        show: NameTranslation
        gedcom_docs: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PERSONAL_NAME_PIECES'
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = NameTranslation(
                    translation="תומס ג'ונס",
                    language='he',
                    pieces=PersonalNamePieces(
                        given=["ג'ונס"],
                        surname=['תומס'],
                    ),
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = NameTranslation(
                    translation='توماس جونز',
                    language='ar',
                    pieces=PersonalNamePieces(
                        given=['توماس '],
                        surname=['جونز'],
                    ),
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = NameTranslation(
                    translation='Τόμας Τζόουνς',
                    language='el',
                    pieces=PersonalNamePieces(
                        given=['Τόμας'],
                        surname=['Τζόουνς'],
                    ),
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = NameTranslation()
                code_preface = Example.EMPTY_CODE
                gedcom_preface = Example.EMPTY_GEDCOM
        return Formatter.example(
            code_preface,
            show.code(),
            gedcom_preface,
            show.ged(),
            gedcom_docs,
            genealogy_docs,
        )


class NoteTranslation(NamedTuple):
    """Store, validate and display the optional note tranlation section of
    the GEDCOM Note Structure.

    The BCP 47 language tag is a hyphenated list of subtags.
    The [W3C Internationalization](https://www.w3.org/International/questions/qa-choosing-language-tags)
    guide will help one make a decision on which tags to use.
    The [Language Subtag Lookup Tool](https://r12a.github.io/app-subtags/)
    can assist with finding and checking the language tag one would like to use.

    Example:
        This example will translation "This is a note." into the Arabic "هذه ملاحظة.".
        >>> from chronodata.store import NoteTranslation
        >>> from chronodata.constants import MediaType
        >>> arabic_text = 'هذه ملاحظة.'
        >>> mime = MediaType.TEXT_HTML
        >>> language = 'afb'
        >>> nt = NoteTranslation(arabic_text, mime, language)
        >>> nt.validate()
        True
        >>> print(nt.ged(1))
        1 TRAN هذه ملاحظة.
        2 MIME TEXT_HTML
        2 LANG afb
        <BLANKLINE>

    Args:
        translation: the text of the translation for the note.
        mime: the mime type of the translation.
        language: the BCP 47 language tag of the translation.

    Returns:
        A GEDCOM string storing this data.

    See Also:
        `Note`

    Reference:
        [GEDCOM Note Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#NOTE_STRUCTURE)]

    This is not a specific GEDCOM structure but implements this part of `Note`
    > +1 TRAN <Text>                           {0:M}  g7:NOTE-TRAN
    >    +2 MIME <MediaType>                   {0:1}  g7:MIME
    >    +2 LANG <Language>                    {0:1}  g7:LANG
    """

    translation: str = Default.EMPTY
    mime: MediaType = MediaType.NONE
    language: str = Default.EMPTY

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.translation, str)
            and Checker.verify_enum(self.mime.value, MediaType)
            and Checker.verify_type(self.language, str)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.translation != String.EMPTY and self.validate():
            lines = Tagger.string(lines, level, Tag.TRAN, self.translation)
            lines = Tagger.string(lines, level + 1, Tag.MIME, self.mime.value)
            lines = Tagger.string(lines, level + 1, Tag.LANG, self.language)
        return lines

    def code(self, level: int = 0) -> str:
        spaces: str = String.INDENT * level
        return indent(
            f"""
NoteTranslation(
    translation = '{self.translation}',
    mime = '{self.mime}',
    language = '{self.language}',
)""",
            spaces,
        )

    def example(self, choice: int = Default.CHOICE) -> str:
        """Produce four examples of ChronoData code and GEDCOM output lines and link to
        the GEDCOM documentation.

        The following levels are available:
        - 0 (Default) Produces an empty example with no GEDCOM lines.
        - 1 Produces an example with all arguments containing data.
        - 2 Produces an alternate example with possibly some arguments missing.
        - 3 Produces either another alternate example or an example with non-Latin
            character texts.

        Any other value passed in will produce the same as the default level.

        Args:
            choice: The example one chooses to display.
        """
        show: NoteTranslation
        gedcom_docs: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#NOTE_STRUCTURE'
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = NoteTranslation(
                    translation='<p>To jest prosta notatka.</p>',
                    mime=MediaType.TEXT_HTML,
                    language='pl',
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = NoteTranslation(
                    translation='Þetta er einföld athugasemd.',
                    mime=MediaType.TEXT_PLAIN,
                    language='is',
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = NoteTranslation(
                    translation='यह एक साधारण नोट है.',
                    mime=MediaType.TEXT_PLAIN,
                    language='hi',
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = NoteTranslation()
                code_preface = Example.EMPTY_CODE
                gedcom_preface = Example.EMPTY_GEDCOM
        return Formatter.example(
            code_preface,
            show.code(),
            gedcom_preface,
            show.ged(),
            gedcom_docs,
            genealogy_docs,
        )


class CallNumber(NamedTuple):
    """Store, validate and display the option call numbers for the
    SourceRepositoryCitation substructure.

    Example:
        This example assumes there is a call number "1111" which is the
        minimal amount of information needed to use this optional feature.
        >>> from chronodata.store import CallNumber
        >>> cn = CallNumber('1111')
        >>> cn.validate()
        True
        >>> print(cn.ged(1))
        1 CALN 1111
        <BLANKLINE>

        This next example uses all of the optional positions.
        >>> from chronodata.constants import Medium
        >>> cn_all = CallNumber('1111', Medium.BOOK, 'New Testament')
        >>> print(cn_all.ged(1))
        1 CALN 1111
        2 MEDI BOOK
        3 PHRASE New Testament
        <BLANKLINE>

    Args:


    Returns:
        A GEDCOM string storing this data.

    See Also:
        `SourceRepositoryCitation`: the superstructure of this NamedTuple.

    Reference:
        [GEDCOM Medium Enumeration Set](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#enumset-MEDI)
        [GEDCOM Source Repository Citation](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_REPOSITORY_CITATION)

    >   +1 CALN <Special>                        {0:M}  [g7:CALN](https://gedcom.io/terms/v7/CALN)
    >      +2 MEDI <Enum>                        {0:1}  [g7:MEDI](https://gedcom.io/terms/v7/MEDI)
    >         +3 PHRASE <Text>                   {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    """

    call_number: str = Default.EMPTY
    medium: Medium = Medium.NONE
    phrase: str = Default.EMPTY

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.call_number, str)
            and Checker.verify_enum(self.medium.value, Medium)
            and Checker.verify_type(self.phrase, str)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.call_number != String.EMPTY and self.validate():
            lines = Tagger.string(lines, level, Tag.CALN, self.call_number)
            lines = Tagger.string(lines, level + 1, Tag.MEDI, self.medium.value)
            lines = Tagger.string(lines, level + 2, Tag.PHRASE, self.phrase)
        return lines

    def code(self, level: int = 0) -> str:
        spaces: str = String.INDENT * level
        return indent(
            f"""
CallNumber(
    call_number = '{self.call_number}',
    medium = '{self.medium}',
    phrase = '{self.phrase}',
)""",
            spaces,
        )

    def example(self, choice: int = Default.CHOICE) -> str:
        """Produce four examples of ChronoData code and GEDCOM output lines and link to
        the GEDCOM documentation.

        The following levels are available:
        - 0 (Default) Produces an empty example with no GEDCOM lines.
        - 1 Produces an example with all arguments containing data.
        - 2 Produces an alternate example with possibly some arguments missing.
        - 3 Produces either another alternate example or an example with non-Latin
            character texts.

        Any other value passed in will produce the same as the default level.

        Args:
            choice: The example one chooses to display.
        """
        show: CallNumber
        gedcom_docs: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_REPOSITORY_CITATION'
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = CallNumber(
                    call_number='1-234-333 ABC',
                    medium=Medium.BOOK,
                    phrase='A special call number',
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = CallNumber(
                    call_number='1-234-333 ABC',
                    medium=Medium.MAGAZINE,
                    phrase='A special article.',
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = CallNumber(
                    call_number='1-234-333 ABC',
                    medium=Medium.NONE,
                    phrase='',
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = CallNumber()
                code_preface = Example.EMPTY_CODE
                gedcom_preface = Example.EMPTY_GEDCOM
        return Formatter.example(
            code_preface,
            show.code(),
            gedcom_preface,
            show.ged(),
            gedcom_docs,
            genealogy_docs,
        )


class Text(NamedTuple):
    """Store, validate and display a text in the GEDCOM standard.

    A Source Citation structure can have multiple texts associated with it.  This NamedTuple describes
    a specific text.

    Examples:

    Args:
        text: the text being added.
        mime: the media type of the text.
        language: the BCP 47 language tag for the text.

    Returns:
        A GEDCOM string storing this data.

    See Also:
        `SourceData`
        `SourceCitation`

    Reference:
        GEDCOM Source Citation](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_CITATION)

    This is part of the GEDCOM Source Citation structure.
    >      +2 TEXT <Text>                        {0:M}  g7:TEXT
    >         +3 MIME <MediaType>                {0:1}  g7:MIME
    >         +3 LANG <Language>                 {0:1}  g7:LANG
    """

    text: str = Default.EMPTY
    mime: MediaType = MediaType.NONE
    language: str = Default.EMPTY

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.text, str)
            and Checker.verify_enum(self.mime.value, MediaType)
            and Checker.verify_type(self.language, str)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.text != String.EMPTY and self.validate():
            lines = Tagger.string(lines, level, Tag.TEXT, str(self.text))
            lines = Tagger.string(lines, level + 1, Tag.MIME, self.mime.value)
            lines = Tagger.string(lines, level + 1, Tag.LANG, self.language)
        return lines

    def code(self, level: int = 0) -> str:
        spaces: str = String.INDENT * level
        return indent(
            f"""
Text(
    text = '{self.text}',
    mime = {self.mime},
    language = '{self.language}',
),""",
            spaces,
        )  # .replace('\n', '', 1)

    def example(self, choice: int = Default.CHOICE) -> str:
        """Produce four examples of ChronoData code and GEDCOM output lines and link to
        the GEDCOM documentation.

        The following levels are available:
        - 0 (Default) Produces an empty example with no GEDCOM lines.
        - 1 Produces an example with all arguments containing data.
        - 2 Produces an alternate example with possibly some arguments missing.
        - 3 Produces either another alternate example or an example with non-Latin
            character texts.

        Any other value passed in will produce the same as the default level.

        Args:
            choice: The example one chooses to display.
        """
        show: Text
        gedcom_docs: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_CITATION'
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = Text(
                    text='This is a text.',
                    mime=MediaType.TEXT_PLAIN,
                    language='en',
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Text(
                    text='ई एकटा पाठ अछि।',
                    mime=MediaType.TEXT_PLAIN,
                    language='mai',
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Text(
                    text='ይህ ጽሑፍ ነው።',
                    mime=MediaType.TEXT_PLAIN,
                    language='am',
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Text()
                code_preface = Example.EMPTY_CODE
                gedcom_preface = Example.EMPTY_GEDCOM
        return Formatter.example(
            code_preface,
            show.code(),
            gedcom_preface,
            show.ged(),
            gedcom_docs,
            genealogy_docs,
        )


class SourceData(NamedTuple):
    """_summary_

    Examples:


    Args:
        date_value:
        texts: a list of texts associated with this source.

    Returns:
        A GEDCOM string storing this data.

    Reference:
        [GEDCOM Source Citation](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_CITATION)

    This is not a GEDCOM structure, but part of the Source Citation structure.
    >   +1 DATA                                  {0:1}  g7:SOUR-DATA
    >      +2 <<DATE_VALUE>>                     {0:1}
    >      +2 TEXT <Text>                        {0:M}  g7:TEXT
    >         +3 MIME <MediaType>                {0:1}  g7:MIME
    >         +3 LANG <Language>                 {0:1}  g7:LANG
    """

    date_value: DateValue = DateValue()
    texts: list[Text] = [Text(), Text()]  # noqa: RUF012

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = Checker.verify_type(
            self.date_value, str
        ) and Checker.verify_tuple_type(self.texts, Text)
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.date_value != DateValue() and self.validate():
            lines = Tagger.string(lines, level, Tag.DATE, str(self.date_value))
            lines = Tagger.structure(lines, level + 1, self.texts, Text())
        return lines

    def code(self, level: int = 0) -> str:
        date_value: str = Formatter.listcodes(self.date_value, level + 1)
        texts: str = Formatter.listcodes(self.texts, level + 1)
        spaces: str = String.INDENT * level
        return indent(
f"""SourceData(
    date_value = '{date_value}',
    texts = {texts},
),""",
            spaces,
        )

    def example(self, choice: int = Default.CHOICE) -> str:
        """Produce four examples of ChronoData code and GEDCOM output lines and link to
        the GEDCOM documentation.

        The following levels are available:
        - 0 (Default) Produces an empty example with no GEDCOM lines.
        - 1 Produces an example with all arguments containing data.
        - 2 Produces an alternate example with possibly some arguments missing.
        - 3 Produces either another alternate example or an example with non-Latin
            character texts.

        Any other value passed in will produce the same as the default level.

        Args:
            choice: The example one chooses to display.
        """
        show: SourceData
        gedcom_docs: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_CITATION'
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = SourceData(
                    date_value=DateValue(),
                    texts=[
                        Text('hello', MediaType.TEXT_PLAIN, language='en'),
                        Text(
                            'hello again', MediaType.TEXT_PLAIN, language='en'
                        ),
                    ],
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = SourceData(
                    date_value=DateValue(),
                    texts=[
                        Text('hello', MediaType.TEXT_PLAIN, language='en'),
                        Text(
                            'hello again', MediaType.TEXT_PLAIN, language='en'
                        ),
                    ],
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = SourceData(
                    date_value=DateValue(),
                    texts=[
                        Text('hello', MediaType.TEXT_PLAIN, language='en'),
                        Text(
                            'hello again', MediaType.TEXT_PLAIN, language='en'
                        ),
                    ],
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = SourceData()
                code_preface = Example.EMPTY_CODE
                gedcom_preface = Example.EMPTY_GEDCOM
        return Formatter.example(
            code_preface,
            show.code(),
            gedcom_preface,
            show.ged(),
            gedcom_docs,
            genealogy_docs,
        )


class SourceCitation(NamedTuple):
    """Store, validate and display the Source Citation
    substructure of the GEDCOM standard.

    Examples:


    Args:
        xref: the source identifier
        page:

    Returns:
        A GEDCOM string storing this data.

    Reference:
        [GEDCOM Source Citation](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_CITATION)

    > n SOUR @<XREF:SOUR>@                       {1:1}  g7:SOUR
    >   +1 PAGE <Text>                           {0:1}  g7:PAGE
    >   +1 DATA                                  {0:1}  g7:SOUR-DATA
    >      +2 <<DATE_VALUE>>                     {0:1}
    >      +2 TEXT <Text>                        {0:M}  g7:TEXT
    >         +3 MIME <MediaType>                {0:1}  g7:MIME
    >         +3 LANG <Language>                 {0:1}  g7:LANG
    >   +1 EVEN <Enum>                           {0:1}  g7:SOUR-EVEN
    >      +2 PHRASE <Text>                      {0:1}  g7:PHRASE
    >      +2 ROLE <Enum>                        {0:1}  g7:ROLE
    >         +3 PHRASE <Text>                   {0:1}  g7:PHRASE
    >   +1 QUAY <Enum>                           {0:1}  g7:QUAY
    >   +1 <<MULTIMEDIA_LINK>>                   {0:M}
    >   +1 <<NOTE_STRUCTURE>>                    {0:M}
    """

    xref: SourceXref = Void.SOUR
    page: str = String.EMPTY
    source_data: SourceData = SourceData()
    event: Event = Event.NONE
    event_phrase: str = String.EMPTY
    role: Role = Role.NONE
    role_phrase: str = String.EMPTY
    quality: Quay = Quay.NONE
    multimedialinks: list[Any] = []  # noqa: RUF012
    notes: list[Any] = []  # noqa: RUF012

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.xref, SourceXref)
            and Checker.verify_type(self.page, str)
            and Checker.verify_type(self.source_data, SourceData)
            and Checker.verify_enum(self.event.value, Event)
            and Checker.verify_type(self.event_phrase, str)
            and Checker.verify_enum(self.role.value, Role)
            and Checker.verify_type(self.role_phrase, str)
            and Checker.verify_enum(self.quality.value, Quay)
            and Checker.verify_tuple_type(self.multimedialinks, MultimediaLink)
            and Checker.verify_tuple_type(self.notes, Note)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(
                lines, level, Tag.SOUR, str(self.xref), format=False
            )
            lines = Tagger.string(lines, level + 1, Tag.PAGE, self.page)
            lines = Tagger.structure(
                lines, level + 1, self.source_data, SourceData()
            )
            if self.event != Event.NONE:
                lines = Tagger.string(
                    lines, level + 1, Tag.EVEN, self.event.value
                )
                lines = Tagger.string(
                    lines, level + 2, Tag.PHRASE, self.event_phrase
                )
                lines = Tagger.string(
                    lines, level + 2, Tag.ROLE, self.role.value
                )
                lines = Tagger.string(
                    lines, level + 2, Tag.PHRASE, self.role_phrase
                )
            lines = Tagger.string(
                lines, level + 1, Tag.QUAY, self.quality.value
            )
            lines = Tagger.structure(lines, level + 1, self.multimedialinks)
            lines = Tagger.structure(lines, level + 1, self.notes)
        return lines

    def code(self, level: int = 0) -> str:
        source_data: str = Formatter.listcodes(self.source_data, level + 1)
        event: str = Formatter.listcodes(self.event, level + 1)
        multimedialinks: str = Formatter.listcodes(self.multimedialinks, level + 1)
        notes: str = Formatter.listcodes(self.notes, level + 1)
        spaces: str = String.INDENT * level
        return indent(
f"""SourceCitation(
    xref = '{self.xref}',
    page = '{self.page}',
    source_data = {source_data},
    event = {event},
    phrase = {self.event_phrase},
    role = {self.role},
    role_phrase = {self.role_phrase},
    quality = {self.quality},
    multimedialinks = {multimedialinks},
    notes = {notes},
),""",
            spaces,
        )

    def example(self, choice: int = Default.CHOICE) -> str:
        """Produce four examples of ChronoData code and GEDCOM output lines and link to
        the GEDCOM documentation.

        The following levels are available:
        - 0 (Default) Produces an empty example with no GEDCOM lines.
        - 1 Produces an example with all arguments containing data.
        - 2 Produces an alternate example with possibly some arguments missing.
        - 3 Produces either another alternate example or an example with non-Latin
            character texts.

        Any other value passed in will produce the same as the default level.

        Args:
            choice: The example one chooses to display.
        """
        show: SourceCitation
        gedcom_docs: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_CITATION'
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = SourceCitation(
                    xref=Void.SOUR,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = SourceCitation(
                    xref=Void.SOUR,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = SourceCitation(
                    xref=Void.SOUR,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = SourceCitation()
                code_preface = Example.EMPTY_CODE
                gedcom_preface = Example.EMPTY_GEDCOM
        return Formatter.example(
            code_preface,
            show.code(),
            gedcom_preface,
            show.ged(),
            gedcom_docs,
            genealogy_docs,
        )


class Note(NamedTuple):
    """Store, validate and display a note substructure of the GEDCOM standard.

    The BCP 47 language tag is a hyphenated list of subtags.
    The [W3C Internationalization](https://www.w3.org/International/questions/qa-choosing-language-tags)
    guide will help one make a decision on which tags to use.
    The [Language Subtag Lookup Tool](https://r12a.github.io/app-subtags/)
    can assist with finding and checking the language tag one would like to use.

    Example:
        This example is a note without other information.
        >>> from chronodata.store import Note
        >>> note = Note(note='This is my note.')
        >>> print(note.ged(1))
        1 NOTE This is my note.
        <BLANKLINE>

        A note line may be continued onto two lines if the "\\n" character
        appears in the note as illustrated in the [GEDCOM Line standard](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#lines).
        >>> multi_line_note = Note(
        ...     note='This is a note field that\\n  spans four lines.\\n\\n(the third line was blank)'
        ... )
        >>> print(multi_line_note.ged(1))
        1 NOTE This is a note field that
        2 CONT   spans four lines.
        2 CONT
        2 CONT (the third line was blank)
        <BLANKLINE>

        This example uses the Hebrew language translating "This is my note." as "זו ההערה שלי."
        The translation comes from [Google Translate](https://translate.google.com/?sl=en&tl=iw&text=This%20is%20my%20note.&op=translate).
        >>> hebrew_note = Note(note='זו ההערה שלי.', language='he')
        >>> print(hebrew_note.ged(1))
        1 NOTE זו ההערה שלי.
        2 LANG he
        <BLANKLINE>

        The next example adds translations of the previous example to the note.
        >>> from chronodata.constants import MediaType
        >>> english_translation = NoteTranslation(
        ...     'This is my note.', MediaType.TEXT_PLAIN, 'en'
        ... )
        >>> urdu_translation = NoteTranslation(
        ...     'یہ میرا نوٹ ہے۔', MediaType.TEXT_PLAIN, 'ur'
        ... )
        >>> hebrew_note_with_translations = Note(
        ...     note='זו ההערה שלי.',
        ...     language='he',
        ...     translations=[
        ...         english_translation,
        ...         urdu_translation,
        ...     ],
        ... )
        >>> print(hebrew_note_with_translations.ged(1))
        1 NOTE זו ההערה שלי.
        2 LANG he
        2 TRAN This is my note.
        3 MIME TEXT_PLAIN
        3 LANG en
        2 TRAN یہ میرا نوٹ ہے۔
        3 MIME TEXT_PLAIN
        3 LANG ur
        <BLANKLINE>


    Args:
        text: the text of the note.
        mime: the optional media type of the note.
        language: the optional BCP 47 language tag for the note.
        translations: an optional tuple of translations of the text.
        citations: an optional tuple of translations of the text.

    Returns:
        A GEDCOM string storing this data.

    Reference:
        [W3C Internationalization](https://www.w3.org/International/questions/qa-choosing-language-tags)
        [Language Subtag Lookup Tool](https://r12a.github.io/app-subtags/)
        [GEDCOM Note Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#NOTE_STRUCTURE)

    [
    n NOTE <Text>                              {1:1}  g7:NOTE
      +1 MIME <MediaType>                      {0:1}  g7:MIME
      +1 LANG <Language>                       {0:1}  g7:LANG
      +1 TRAN <Text>                           {0:M}  g7:NOTE-TRAN
         +2 MIME <MediaType>                   {0:1}  g7:MIME
         +2 LANG <Language>                    {0:1}  g7:LANG
      +1 <<SOURCE_CITATION>>                   {0:M}
    |
    n SNOTE @<XREF:SNOTE>@                     {1:1}  g7:SNOTE
    ]
    """  # noqa: RUF002

    snote: SharedNoteXref = Void.SNOTE
    note: str = String.EMPTY
    mime: MediaType = MediaType.NONE
    language: str = String.EMPTY
    translations: list[NoteTranslation] = []  # noqa: RUF012
    source_citations: list[SourceCitation] = []  # noqa: RUF012

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.snote, SharedNoteXref)
            and Checker.verify_type(self.note, str)
            and Checker.verify_enum(self.mime.value, MediaType)
            and Checker.verify_tuple_type(self.translations, NoteTranslation)
            and Checker.verify_tuple_type(self.source_citations, SourceCitation)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            if self.snote != Void.SNOTE:
                lines = Tagger.string(
                    lines, level, Tag.SNOTE, self.snote.fullname
                )
            else:
                lines = Tagger.string(lines, level, Tag.NOTE, self.note)
                lines = Tagger.string(
                    lines, level + 1, Tag.MIME, self.mime.value
                )
                lines = Tagger.string(lines, level + 1, Tag.LANG, self.language)
                lines = Tagger.structure(
                    lines, level + 1, self.translations, NoteTranslation()
                )
                lines = Tagger.structure(
                    lines, level + 1, self.source_citations, SourceCitation()
                )
        return lines

    def code(self, level: int = 0) -> str:
        spaces: str = String.INDENT * level
        if self.snote != Void.SNOTE:
            return indent(
                f"""
Note(
    snote = {self.snote.fullname},
)""",
                spaces,
            )
        translations = Formatter.listcodes(self.translations, level + 1)
        source_citations = Formatter.listcodes(self.source_citations, level + 1)
        return indent(
            f"""
Note(
    note = '{self.note}',
    mime = '{self.mime}',
    language = '{self.language}',
    translations = {translations},
    source_citations = {source_citations},
)""",
            spaces,
        )


class SourceRepositoryCitation(NamedTuple):
    """Store, validate and display the optional Source Repository Citation
     substructure of the GEDCOM standard.

    Examples:

    Args:
        repo: the reference identifier for the repository.
        notes: a tuple of Notes.
        call_numbers: a tuple of call numbers.

    Returns:
        A GEDCOM string storing this data.

    Reference:
        [GEDCOM Source Repository Citation](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_REPOSITORY_CITATION)

    > n REPO @<XREF:REPO>@                       {1:1}  [g7:REPO](https://gedcom.io/terms/v7/REPO)
    >   +1 <<NOTE_STRUCTURE>>                    {0:M}
    >   +1 CALN <Special>                        {0:M}  [g7:CALN](https://gedcom.io/terms/v7/CALN)
    >      +2 MEDI <Enum>                        {0:1}  [g7:MEDI](https://gedcom.io/terms/v7/MEDI)
    >         +3 PHRASE <Text>                   {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    """

    repo: RepositoryXref = Void.REPO
    notes: list[Note] = []  # noqa: RUF012
    call_numbers: list[CallNumber] = []  # noqa: RUF012

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.repo, RepositoryXref)
            and Checker.verify_tuple_type(self.notes, Note)
            and Checker.verify_tuple_type(self.call_numbers, CallNumber)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.repo.fullname != Void.NAME and self.validate():
            lines = Tagger.taginfo(level, Tag.SOUR, str(self.repo))
            lines = Tagger.structure(lines, level, self.notes, Note())
            lines = Tagger.structure(
                lines, level, self.call_numbers, CallNumber()
            )
        return lines
    
    def code(self, level: int = 0) -> str:
        notes: str = Formatter.listcodes(self.notes, level + 1)
        call_numbers: str = Formatter.listcodes(self.call_numbers, level + 1)
        spaces: str = String.INDENT * level
        return indent(
            f"""
SourceRepositoryCitation(
    repo = {self.repo},
    notes = {notes},
    callnumbers = {call_numbers},
)""",
            spaces,
        )


class PersonalName(NamedTuple):
    """Store, validate and display a personal name.

    Example:
        The first example will not only test ChronoData but also the extend
        the GEDCOM standard can store various kinds of information.  I will want
        to record the first man who was first mentioned in Genesis 1:26, Adam,
        using the Hebrew word "אָדָ֛ם". I obtained the name from
        [Chabad](https://www.chabad.org/library/bible_cdo/aid/8165/jewish/Chapter-1.htm)
        which I could add in as a `SourceCitation`.  In Genesis 2:16 Adam is
        also referred to as "הָֽאָדָ֖ם" which I will use as a nickname and translate
        it into English as "the man".

        I will validate it first to make sure it is correct, but this is not required.
        Note the trailing "," in the `translations` parameter.  Even though there
        is only one translation, this is required to guarantee the tuple
        is not interpreted as a string of letters.
        >>> from chronodata.store import (
        ...     NameTranslation,
        ...     Note,
        ...     PersonalName,
        ...     PersonalNamePieces,
        ...     SourceCitation,
        ... )
        >>> from chronodata.constants import NameType, PersonalNamePieceTag
        >>> adam_note = Note(note='Here is a place to add more information.')
        >>> adam_english = NameTranslation(
        ...     'Adam', 'en', PersonalNamePieces(nickname=['the man'])
        ... )
        >>> adam = PersonalName(
        ...     name='אָדָ֛ם',
        ...     type=NameType.OTHER,
        ...     phrase='The first man',
        ...     pieces=PersonalNamePieces(nickname=['הָֽאָדָ֖ם']),
        ...     translations=[adam_english],
        ...     notes=[adam_note],
        ... )
        >>> print(adam.ged(1))
        1 NAME אָדָ֛ם //
        2 TYPE OTHER
        2 NICK הָֽאָדָ֖ם
        2 TRAN Adam
        3 LANG en
        3 NICK the man
        2 NOTE Here is a place to add more information.
        <BLANKLINE>

    Args:
        name: The full name of the person including the surname.
        surname: Repeat the part of the name that is the surname or last name of the person.
        type: the type of name. There are seven types to choose from:
            - NameType.AKA or also known as.
            - NameType.BIRTH or birth name.
            - NameType.IMMIGRANT or immigrant name.
            - NameType.MAIDEN or maiden name.
            - NameType.MARRIED or married name.
            - NameType.PROFESSIONAL or professional name
            - NameType.OTHER or another type not listed above.
        phrase: a place for uncategorized information about the name.
        pieces: an alternate way to split the name.
        translations: an optional list of translations of the name.
        notes: a list of optional notes regarding the name.
        sources: a list of citations regarding the name.

    Returns:
        A GEDCOM string storing this data.

    Reference:
        [GEDCOM Person Name Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PERSONAL_NAME_STRUCTURE)

    n NAME <PersonalName>                      {1:1}  g7:INDI-NAME
      +1 TYPE <Enum>                           {0:1}  g7:NAME-TYPE
         +2 PHRASE <Text>                      {0:1}  g7:PHRASE
      +1 <<PERSONAL_NAME_PIECES>>              {0:1}
      +1 TRAN <PersonalName>                   {0:M}  g7:NAME-TRAN
         +2 LANG <Language>                    {1:1}  g7:LANG
         +2 <<PERSONAL_NAME_PIECES>>           {0:1}
      +1 <<NOTE_STRUCTURE>>                    {0:M}
      +1 <<SOURCE_CITATION>>                   {0:M}
    """

    name: str = String.EMPTY
    surname: str = String.EMPTY
    type: Tag = Tag.NONE
    phrase: str = String.EMPTY
    pieces: PersonalNamePieces = PersonalNamePieces()
    translations: list[NameTranslation] = []  # noqa: RUF012
    notes: list[Note] = []  # noqa: RUF012
    source_citations: list[SourceCitation] = []  # noqa: RUF012

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_not_default(self.name, '')
            and Checker.verify_type(self.name, str)
            and Checker.verify_type(self.surname, str)
            and Checker.verify_enum(self.type.value, NameType)
            and Checker.verify_type(self.phrase, str)
            and Checker.verify_type(self.pieces, PersonalNamePieces)
            and Checker.verify_tuple_type(self.translations, NameTranslation)
            and Checker.verify_tuple_type(self.notes, Note)
            and Checker.verify_tuple_type(self.source_citations, SourceCitation)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            name_surname: str = self.name
            if name_surname.count(String.SLASH) < 2:
                name_surname = ''.join(
                    [
                        name_surname,
                        ' ',
                        String.SLASH,
                        self.surname,
                        String.SLASH,
                    ]
                )
            lines = Tagger.string(lines, level, Tag.NAME, name_surname)
            lines = Tagger.string(lines, level + 1, Tag.TYPE, self.type.value)
            lines = Tagger.structure(
                lines, level + 1, self.pieces, PersonalNamePieces()
            )
            lines = Tagger.structure(
                lines, level + 1, self.translations, NameTranslation()
            )
            lines = Tagger.structure(lines, level + 1, self.notes, Note())
            lines = Tagger.structure(
                lines, level + 1, self.source_citations, SourceCitation()
            )
        return lines
    
    def code(self, level: int = 0) -> str:
        # pieces: str = Formatter.listcodes(self.pieces, level + 1)
        # translations: str = Formatter.listcodes(self.translations, level + 1)
        # notes: str = Formatter.listcodes(self.notes, level + 1)
        # source_citations: str = Formatter.listcodes(self.source_citations, level + 1)
        #spaces: str = String.INDENT * level
        return indent(
            f"""
PersonalName(
    name = '{self.name}',
    surname = '{self.surname}',
    type = '{self.type}',
    phrase = '{self.phrase}',
    pieces = {Formatter.listcodes(self.pieces, level + 1)},
    translations = {Formatter.listcodes(self.translations, level + 1)},
    notes = {Formatter.listcodes(self.notes, level + 1)},
    source_citations = {Formatter.listcodes(self.source_citations, level + 1)},
)""",
            String.INDENT * level,
        )


class Association(NamedTuple):
    """Store, validate and display a GEDCOM Association structure.



    Examples:
        This example comes from the [GEDCOM specification for the ASSO tag](https://gedcom.io/terms/v7/ASSO).
        The specification displays the GEDCOM lines as follows:

        > 0 @I1@ INDI
        > 1 ASSO @VOID@
        > 2 PHRASE Mr Stockdale
        > 2 ROLE OTHER
        > 3 PHRASE Teacher
        > 1 BAPM
        > 2 DATE 1930
        > 2 ASSO @I2@
        > 3 ROLE CLERGY

        This differs from the outcome produced by `ChronoData` which displays the `BAPM`
        baptismal event association with pointer `@I2@` before the individual association
        with pointer `@VOID@` because
        the event association preceded the individual association in the argument list.
        Both orderings record the same data under the individual with pointer `@I1@`.

        First import the required classes.
        >>> from chronodata.build import Genealogy
        >>> from chronodata.constants import Role
        >>> from chronodata.store import Association, Individual

        Next, create a genealogy and the two individuals references.
        There is no need to create an individual reference for Mr Stockdale
        so we leave his pointer as `@VOID@`.
        >>> gen = Genealogy('test')
        >>> individual = gen.individual_xref('I', initial=True)
        >>> clergy = gen.individual_xref('I', initial=True)

        Finally construct the individual record and display it.
        >>> indi = Individual(
        ...     xref=individual,
        ...     associations=[
        ...         Association(
        ...             association_phrase='Mr Stockdale',
        ...             role=Role.OTHER,
        ...             role_phrase='Teacher',
        ...         ),
        ...     ],
        ...     events=[
        ...         IndividualEvent(
        ...             tag=Tag.BAPM,
        ...             payload='',
        ...             event_detail=IndividualEventDetail(
        ...                 event_detail=EventDetail(
        ...                     date_value=DateValue(
        ...                         Date(year=1930),
        ...                     ),
        ...                     associations=[
        ...                         Association(xref=clergy, role=Role.CLERGY),
        ...                     ],
        ...                 )
        ...             ),
        ...         )
        ...     ],
        ... )
        >>> print(indi.ged())
        0 @I1@ INDI
        1 BAPM
        2 DATE 1930
        2 ASSO @I2@
        3 ROLE CLERGY
        1 ASSO @VOID@
        2 PHRASE Mr Stockdale
        2 ROLE OTHER
        3 PHRASE Teacher
        <BLANKLINE>

        The [GEDCOM Role tag specification](https://gedcom.io/terms/v7/ROLE)
        provides two examples for the use of Tag.ROLE.

        In the first example the child's birth record is the source of the mother's name
        which is only known as "Mary" without a surname.

        > 0 @I1@ INDI
        > 1 NAME Mary //
        > 2 SOUR @S1@
        > 3 EVEN BIRT
        > 4 ROLE MOTH

        To reproduce this we need and individual cross-reference identifier `@I1@` for Mary
        and a source cross-reference identifier `@S1@` for the birth certificate.
        Since we already have an individual referenced as `I1` above, we instantiate
        another Genealogy which illustrates that we can have multiple Genealogies
        instantiated at one time.
        >>> from chronodata.build import Genealogy
        >>> from chronodata.constants import Event, Role
        >>> from chronodata.store import (
        ...     Individual,
        ...     PersonalName,
        ...     SourceCitation,
        ... )
        >>> gen2 = Genealogy('second genealogy')
        >>> ind_i1_xref = gen2.individual_xref('I1')
        >>> sour_s1_xref = gen2.source_xref('S1')
        >>> mary = Individual(
        ...     xref=ind_i1_xref,
        ...     personal_names=[
        ...         PersonalName(
        ...             name='Mary //',
        ...             source_citations=[
        ...                 SourceCitation(
        ...                     xref=sour_s1_xref,
        ...                     event=Event.BIRT,
        ...                     role=Role.MOTH,
        ...                 )
        ...             ],
        ...         ),
        ...     ],
        ... )
        >>> print(mary.ged())
        0 @I1@ INDI
        1 NAME Mary //
        2 SOUR @S1@
        3 EVEN BIRT
        4 ROLE MOTH
        <BLANKLINE>

        The second example describes when a friend who is the witness at a baptism.

        > 0 @I2@ INDI
        > 1 ASSO @I3@
        > 2 ROLE FRIEND
        > 3 PHRASE best friend
        > 1 BAPM
        > 2 ASSO @I3@
        > 3 ROLE WITN

        Then we will create two individuals in the gen3 Genealogy
        with cross-reference identifiers `@I2@` and `@I3@`.
        >>> from chronodata.build import Genealogy
        >>> from chronodata.constants import Event, Role
        >>> from chronodata.store import (
        ...     Association,
        ...     Individual,
        ...     IndividualEvent,
        ... )
        >>> indi_i2_xref = gen2.individual_xref('I2')
        >>> indi_i3_xref = gen2.individual_xref('I3')
        >>> indi_i2 = Individual(
        ...     xref=indi_i2_xref,
        ...     associations=[
        ...         Association(
        ...             xref=indi_i3_xref,
        ...             role=Role.FRIEND,
        ...             role_phrase='best friend',
        ...         ),
        ...     ],
        ...     events=[
        ...         IndividualEvent(
        ...             tag=Tag.BAPM,
        ...             event_detail=IndividualEventDetail(
        ...                 event_detail=EventDetail(
        ...                     associations=[
        ...                         Association(
        ...                             xref=indi_i3_xref,
        ...                             role=Role.WITN,
        ...                         ),
        ...                     ]
        ...                 )
        ...             ),
        ...         )
        ...     ],
        ... )
        >>> print(indi_i2.ged(0))
        0 @I2@ INDI
        1 BAPM
        2 ASSO @I3@
        3 ROLE WITN
        1 ASSO @I3@
        2 ROLE FRIEND
        3 PHRASE best friend
        <BLANKLINE>

    Args:
        xref: the identifier of the individual in this association.
        phrase: a description of the association.
        role: the role of this individual.
        role_phrase: a description of the role.
        notes: a collection of notes related to this association.
        citations: a collection of citations related to this association.

    Returns:
        A GEDCOM string storing this data.

    Reference:
        [GEDCOM Association Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#ASSOCIATION_STRUCTURE)

    n ASSO @<XREF:INDI>@                       {1:1}  [g7:ASSO](https://gedcom.io/terms/v7/ASSO)
      +1 PHRASE <Text>                         {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
      +1 ROLE <Enum>                           {1:1}  [g7:ROLE](https://gedcom.io/terms/v7/ROLE)
         +2 PHRASE <Text>                      {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
      +1 <<NOTE_STRUCTURE>>                    {0:M}
      +1 <<SOURCE_CITATION>>                   {0:M}
    """

    xref: IndividualXref = Void.INDI
    association_phrase: str = String.EMPTY
    role: Role = Role.NONE
    role_phrase: str = String.EMPTY
    notes: list[Note] = []  # noqa: RUF012
    citations: list[SourceCitation] = []  # noqa: RUF012

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.xref, IndividualXref)
            # and Checker.verify_type(self.role, Role)
            and Checker.verify_enum(self.role.value, Role)
            and Checker.verify_type(self.association_phrase, str)
            and Checker.verify_type(self.role_phrase, str)
            and Checker.verify_tuple_type(self.notes, Note)
            and Checker.verify_tuple_type(self.citations, SourceCitation)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = String.EMPTY
        if self.validate():
            lines = Tagger.string(
                lines, level, Tag.ASSO, str(self.xref), format=False
            )
            lines = Tagger.string(
                lines, level + 1, Tag.PHRASE, self.association_phrase
            )
            lines = Tagger.string(lines, level + 1, Tag.ROLE, self.role.value)
            lines = Tagger.string(
                lines, level + 2, Tag.PHRASE, self.role_phrase
            )
            lines = Tagger.structure(lines, level + 1, self.notes, Note())
            lines = Tagger.structure(
                lines, level + 1, self.citations, SourceCitation()
            )
        return lines


class MultimediaLink(NamedTuple):
    """_summary_

    Examples:


    Args:
        NamedTuple (_type_): _description_

    Returns:
        A GEDCOM string storing this data.
    """

    crop: str = ''
    top: int = 0
    left: int = 0
    height: int = 0
    width: int = 0
    title: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.crop, str)
            and Checker.verify_type(self.top, int)
            and Checker.verify_type(self.left, int)
            and Checker.verify_type(self.height, int)
            and Checker.verify_type(self.width, int)
            and Checker.verify_type(self.title, str)
        )
        return check

    def ged(self, level: int = 1) -> str:
        lines: str = f'{level}'
        if self.validate():
            pass
        return lines


class Exid(NamedTuple):
    exid: str
    exid_type: str

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = Checker.verify_type(
            self.exid, str
        ) and Checker.verify_type(self.exid_type, str)
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        return ''.join(
            [
                Tagger.taginfo(level, Tag.EXID, self.exid),
                Tagger.taginfo(level + 1, Tag.TYPE, self.exid_type),
            ]
        )


class Map:
    """Store, validate and save a GEDCOM map structure.

    The latitude and longitude values are formatted to six decimal places
    by adding zeros if necessary or truncating the number of decimals on the
    input.

    The [GEDCOM Map Structure Type](https://gedcom.io/terms/v7/MAP) reads the following
    about the accuracy of this information:

    > Note that `MAP` provides neither a notion of accuracy (for example, the `MAP`
    > for a birth event may be some distance from the point where the birth occurred)
    > nor a notion of region size (for example, the `MAP` for a place "Belarus" may
    > be anywhere within that nation's 200,000 square kilometer area).

    Examples:
    The first example is a basic example using arbitrary latitude and longitude values.
    >>> from chronodata.store import Map
    >>> location = Map(49.297222, -14.470833)
    >>> print(location.ged(1))
    1 MAP
    2 LATI N49.297222
    2 LONG W14.470833
    <BLANKLINE>

    The second example illustrates how to enter the data if we have the angle in
    minutes, degrees or seconds.  Using the same data from the example above,
    we can first convert it into degrees, minutes and seconds to set up the situation
    where the records we are given do not come in a decimal format.
    >>> from chronodata.store import Placer
    >>> Placer.to_dms(49.297222)
    (49, 17, 49.9992)

    >>> Placer.to_dms(-14.470833)
    (-15, 31, 45.0012)

    We can use these values as well as the decimal values to load the Map structure.
    >>> latlon = Map(
    ...     Placer.to_decimal(49, 17, 49.9992),
    ...     Placer.to_decimal(-15, 31, 45.0012),
    ... )
    >>> print(latlon.ged(1))
    1 MAP
    2 LATI N49.297222
    2 LONG W14.470833
    <BLANKLINE>

    Args:
        latitude: The positive decimal value of the angle from the equator.
        longitude: The positive decimal value of the angle from the prime meridian.
        structure: The URL defining the structure used to validate whether an extension can be
            used in this position.
        extension: A list of extensions which have been defined for this structure in the
            SCHMA structure of the header record.  Their definitions would have to permit
            the extension to be used with `Map` as a superstructure.

    Reference:
        - [GEDCOM Map Structure Type](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#MAP)
        - [GEDCOM Latitude Structure Type](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#LATI)
        - [GEDCOM Longitude Structure Type](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#LONG)
    """

    structure: ClassVar[str] = Tag.MAP.value
    substructures: ClassVar[set[str]] = {Tag.LATI.value, Tag.LONG.value}

    def __init__(
        self,
        latitude: float = Default.MAP_LATITUDE,
        longitude: float = Default.MAP_LONGITUDE,
        extensions: list[Extension] | None = None,
    ):
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.extensions: list[Extension] | None = extensions
        self.descriptions: set[str] = set()
        self.map_extensions: list[Extension] = []
        self.lati_extensions: list[Extension] = []
        self.long_extensions: list[Extension] = []
        if self.extensions is not None:
            for ext in self.extensions:
                self.descriptions.union(ext.schema.supers)
                if Tag.MAP.value in ext.schema.supers:
                    self.map_extensions.append(ext)
                elif Tag.LATI.value in ext.schema.supers:
                    self.lati_extensions.append(ext)
                elif Tag.LONG.value in ext.schema.supers:
                    self.long_extensions.append(ext)

    def __str__(self) -> str:
        if self.extensions is None:
            return (
                f'Map(latitude={self.latitude!s}, longitude={self.longitude!s})'
            )
        return f'Map(latitude={self.latitude!s}, longitude={self.longitude!s}, extensions={self.extensions!s})'

    def __repr__(self) -> str:
        return str(self)

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.latitude, float)
            and Checker.verify_type(self.longitude, float)
            and Checker.verify_range(self.latitude, -90.0, 90.0)
            and Checker.verify_range(self.longitude, -180.0, 180.0)
            and Checker.verify_ext(
                self.descriptions, self.structure, self.substructures
            )
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        north_south: str = 'N'
        if self.latitude < 0.0:
            north_south = 'S'
        east_west: str = 'E'
        if self.longitude < 0.0:
            east_west = 'W'
        latitude: str = format(abs(self.latitude), '.6f')
        longitude: str = format(abs(self.longitude), '.6f')
        latitude = ''.join([north_south, latitude])
        longitude = ''.join([east_west, longitude])
        if self.validate():
            lines = Tagger.empty(lines, level, Tag.MAP)
            lines = Tagger.structure(lines, level + 1, self.map_extensions)
            lines = Tagger.string(lines, level + 1, Tag.LATI, latitude)
            lines = Tagger.structure(lines, level + 2, self.lati_extensions)
            lines = Tagger.string(lines, level + 1, Tag.LONG, longitude)
            lines = Tagger.structure(lines, level + 2, self.long_extensions)
        return lines

    def code(self, level: int = 0) -> str:
        spaces: str = String.INDENT * level
        return indent(
            f"""
Map(
    latitude = {self.latitude!s},
    longitude = {self.longitude!s},
)""",
            spaces,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        latitude: float = Default.MAP_LATITUDE,
        longitude: float = Default.MAP_LONGITUDE,
    ) -> str:
        """Produce four examples of ChronoData code and GEDCOM output lines and link to
        the GEDCOM documentation.

        The following levels are available:
        - 0 (Default) Produces an intentional error.  If the Map structure is used
            without specifying values, the default values will trigger an error.
            However, if an acceptable lattitude and longitude are used in this example,
            then the user example will be displayed.
        - 1 Produces an example with all arguments containing data.
        - 2 Produces an alternate example with possibly some arguments missing.
        - 3 Produces either another alternate example or an example with non-Latin
            character texts.

        Any other value passed in will produce the same as the default level.

        Args:
            choice: The example one chooses to display.
            latitude: If a non-zero latitude is entered this will be used in the example.
            longitude: If a non-zero longitude is entered this will be used in the example.
        """
        show: Map
        gedcom_docs: str = Specs.MAP
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = Map(latitude=45.0, longitude=-45.0)
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Map(latitude=-45.123456789000, longitude=45.987654321000)
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Map(latitude=0.0000000001, longitude=0.000000005)
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                if latitude != 91.0 and longitude != 181.0:
                    show = Map(latitude=latitude, longitude=longitude)
                    logging.info(Example.USER_PROVIDED_EXAMPLE)
                    code_preface = Example.USER_PROVIDED
                    gedcom_preface = Example.GEDCOM
                else:
                    logging.info(Example.ERROR_EXPECTED)
                    show = Map()
                    code_preface = Example.EMPTY_CODE
                    gedcom_preface = Example.EMPTY_GEDCOM
        return Formatter.example(
            code_preface,
            show.code(),
            gedcom_preface,
            show.ged(),
            gedcom_docs,
            genealogy_docs,
        )


class PlaceTranslation:
    """Store, validate and return a translation of GEDCOM place names.

    A place is a comma separated string of named locations or regions going from smallest to largest.

    The BCP 47 language tag is a hyphenated list of subtags.
    The [W3C Internationalization](https://www.w3.org/International/questions/qa-choosing-language-tags)
    guide will help one make a decision on which tags to use.
    The [Language Subtag Lookup Tool](https://r12a.github.io/app-subtags/)
    can assist with finding and checking the language tag one would like to use.

    Example:


    Args:
        place1: A part of the place corresponding to the lowest region.
        place2: A part of the place corresponding to the next highest region above `place1`.
        place3: A part of the place corresponding to the next highest region above `place2`.
        place4: A part of the place corresponding to the next highest region above `place3`.
        language: The langue used to report the four places values.

    Reference:
        [GEDCOM Place Form](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PLAC-FORM)
        [GEDCOM Place Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PLACE_STRUCTURE)


    >   +1 TRAN <List:Text>                      {0:M}  [g7:PLAC-TRAN](https://gedcom.io/terms/v7/PLAC-TRAN)
    >      +2 LANG <Language>                    {1:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
    """

    structure: ClassVar[str] = Tag.TRAN.value
    substructures: ClassVar[set[str]] = {Tag.LANG.value}

    def __init__(
        self,
        place1: str = Default.EMPTY,
        place2: str = Default.EMPTY,
        place3: str = Default.EMPTY,
        place4: str = Default.EMPTY,
        language: str = Default.EMPTY,
        extensions: list[Extension] | None = None,
    ) -> None:
        if extensions is None:
            extensions = []

        self.place1: str = place1
        self.place2: str = place2
        self.place3: str = place3
        self.place4: str = place4
        self.place: str = Placer.place(
            self.place1, self.place2, self.place3, self.place4
        )
        self.language: str = language
        self.extensions: list[Extension] = extensions
        self.descriptions: set[str] = set()
        self.tran_extensions: list[Extension] = []
        self.lang_extensions: list[Extension] = []
        if self.extensions is not None:
            for ext in self.extensions:
                self.descriptions.union(ext.schema.supers)
                if Tag.TRAN.value in ext.schema.supers:
                    self.tran_extensions.append(ext)
                elif Tag.LANG.value in ext.schema.supers:
                    self.lang_extensions.append(ext)

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.place1, str)
            and Checker.verify_type(self.place2, str)
            and Checker.verify_type(self.place3, str)
            and Checker.verify_type(self.place4, str)
            and Checker.verify_type(self.language, str)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = String.EMPTY
        if self.validate():
            lines = Tagger.string(lines, level, Tag.TRAN, self.place)
            lines = Tagger.structure(lines, level + 1, self.tran_extensions)
            lines = Tagger.string(lines, level + 1, Tag.LANG, self.language)
            lines = Tagger.structure(lines, level + 1, self.lang_extensions)
        return lines

    def code(self, level: int = 0) -> str:
        spaces: str = String.INDENT * level
        return indent(
            f"""
PlaceTranslation(
    place1 = '{self.place1}',
    place2 = '{self.place2}',
    place3 = '{self.place3}',
    place4 = '{self.place4}',
    language = '{self.language}',
)""",
            spaces,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        place1: str = Default.EMPTY,
        place2: str = Default.EMPTY,
        place3: str = Default.EMPTY,
        place4: str = Default.EMPTY,
        language: str = Default.EMPTY,
    ) -> str:
        """Produce four examples of ChronoData code and GEDCOM output lines and link to
        the GEDCOM documentation.

        The following levels are available:
        - 0 (Default) Produces an intentional error.  If the Map structure is used
            without specifying values, the default values will trigger an error.
            However, if an acceptable lattitude and longitude are used in this example,
            then the user example will be displayed.
        - 1 Produces an example with all arguments containing data.
        - 2 Produces an alternate example with possibly some arguments missing.
        - 3 Produces either another alternate example or an example with non-Latin
            character texts.

        Any other value passed in will produce the same as the default level.

        Args:
            choice: The example one chooses to display.
            latitude: If a non-zero latitude is entered this will be used in the example.
            longitude: If a non-zero longitude is entered this will be used in the example.
        """
        show: PlaceTranslation
        gedcom_docs: str = Specs.PLACE
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = PlaceTranslation(
                    place1='Chicago',
                    place2='Cook County',
                    place3='Illinois',
                    place4='USA',
                    language='en',
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = PlaceTranslation(
                    place1='Chicago',
                    place2='Cook County',
                    place3='Illinois',
                    place4='USA',
                    language='en',
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = PlaceTranslation(
                    place1='Chicago',
                    place2='Cook County',
                    place3='Illinois',
                    place4='USA',
                    language='en-US',
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = PlaceTranslation(
                    place1=place1,
                    place2=place2,
                    place3=place3,
                    place4=place4,
                    language=language,
                )
                logging.info(Example.USER_PROVIDED_EXAMPLE)
                code_preface = Example.USER_PROVIDED
                gedcom_preface = Example.GEDCOM
        return Formatter.example(
            code_preface,
            show.code(),
            gedcom_preface,
            show.ged(),
            gedcom_docs,
            genealogy_docs,
        )


class Place:
    """Store, validate and return a GEDCOM place structure.

    A place is a comma separated string of named locations or regions going from smallest to largest.
    The default is an empty dictionary {'City': '', 'County': '', 'State': '', 'Country': ''}.
    One would fill in the values for city, county, state and country or assign other
    regions with their names if the default is not relevant.

    The BCP 47 language tag is a hyphenated list of subtags.
    The [W3C Internationalization](https://www.w3.org/International/questions/qa-choosing-language-tags)
    guide will help one make a decision on which tags to use.
    The [Language Subtag Lookup Tool](https://r12a.github.io/app-subtags/)
    can assist with finding and checking the language tag one would like to use.

    Example:
        Below are two `PlaceName` tuples for a place.
        The first is in Czech and the second English.
        A `Map` tuple provides latitude and longitude values for the place.
        A couple of simple `Note` tuples are added as well.
        These tuples form the structure of a `Place` tuple.

        Normally one would not call `validate` or `ged` unless one wanted
        to see if the substructure is valid or how it would display
        in the final GEDCOM file.
        >>> from chronodata.store import Map, Place
        >>> place = Place(
        ...     place1='Bechyně',
        ...     place2='okres Tábor',
        ...     place3='Jihočeský kraj',
        ...     place4='Česká republika',
        ...     form1='Město',
        ...     form2='Okres',
        ...     form3='Stát',
        ...     form4='Země',
        ...     language='cs',
        ...     map=Map(49.297222, 14.470833),
        ...     translations=[
        ...         PlaceTranslation(
        ...             place1='Bechyně',
        ...             place2='Tábor District',
        ...             place3='South Bohemian Region',
        ...             place4='Czech Republic',
        ...             language='en',
        ...         )
        ...     ],
        ...     notes=[
        ...         Note(note='A place in the Czech Republic.', language='en'),
        ...         Note(note='Místo v České republice.', language='cs'),
        ...     ],
        ... )
        >>> place.validate()
        True
        >>> print(place.ged(2))
        2 PLAC Bechyně, okres Tábor, Jihočeský kraj, Česká republika
        3 FORM Město, Okres, Stát, Země
        3 LANG cs
        3 TRAN Bechyně, Tábor District, South Bohemian Region, Czech Republic
        4 LANG en
        3 MAP
        4 LATI N49.297222
        4 LONG E14.470833
        3 NOTE A place in the Czech Republic.
        4 LANG en
        3 NOTE Místo v České republice.
        4 LANG cs
        <BLANKLINE>

    Args:
        place1: A part of the place corresponding to the lowest region.
        place2: A part of the place corresponding to the next highest region above `place1`.
        place3: A part of the place corresponding to the next highest region above `place2`.
        place4: A part of the place corresponding to the next highest region above `place3`.
        form1: The name of the region identified by `place1`.
        form2: The name of the region identified by `place2`.
        form3: The name of the region identified by `place3`.
        form4: The name of the region identified by `place4`.
        language: The langue used to report the four places values.
        translation: A list of `Place` tuples used as translations.
        maps: A list of `Map` tuples for the place.
        exid: Identifiers associated with the place.
        notes: Notes associated with the place.


    Reference:
        [GEDCOM Place Form](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PLAC-FORM)
        [GEDCOM Place Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PLACE_STRUCTURE)


    > n PLAC <List:Text>                         {1:1}  [g7:PLAC](https://gedcom.io/terms/v7/PLAC)
    >   +1 FORM <List:Text>                      {0:1}  [g7:PLAC-FORM](https://gedcom.io/terms/v7/PLAC-FORM)
    >   +1 LANG <Language>                       {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
    >   +1 TRAN <List:Text>                      {0:M}  [g7:PLAC-TRAN](https://gedcom.io/terms/v7/PLAC-TRAN)
    >      +2 LANG <Language>                    {1:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
    >   +1 MAP                                   {0:1}  [g7:MAP](https://gedcom.io/terms/v7/MAP)
    >      +2 LATI <Special>                     {1:1}  [g7:LATI](https://gedcom.io/terms/v7/LATI)
    >      +2 LONG <Special>                     {1:1}  [g7:LONG](https://gedcom.io/terms/v7/LONG)
    >   +1 EXID <Special>                        {0:M}  [g7:EXID](https://gedcom.io/terms/v7/EXID)
    >      +2 TYPE <Special>                     {0:1}  [g7:EXID-TYPE](https://gedcom.io/terms/v7/EXID-TYPE)
    >   +1 <<NOTE_STRUCTURE>>                    {0:M}
    """

    structure: ClassVar[str] = Tag.PLAC.value
    substructures: ClassVar[set[str]] = {Tag.FORM.value, Tag.LANG.value}

    def __init__(
        self,
        place1: str = Default.EMPTY,
        place2: str = Default.EMPTY,
        place3: str = Default.EMPTY,
        place4: str = Default.EMPTY,
        form1: str = Default.PLACE_FORM1,
        form2: str = Default.PLACE_FORM2,
        form3: str = Default.PLACE_FORM3,
        form4: str = Default.PLACE_FORM4,
        language: str = Default.EMPTY,
        translations: list[PlaceTranslation] | None = None,
        map: Map | None = None,
        exids: list[Exid] | None = None,
        notes: list[Note] | None = None,
        extensions: list[Extension] | None = None,
    ) -> None:
        if translations is None:
            translations = []
        if map is None:
            map = Map()
        if exids is None:
            exids = []
        if notes is None:
            notes = []
        if extensions is None:
            extensions = []

        self.place1: str = place1
        self.place2: str = place2
        self.place3: str = place3
        self.place4: str = place4
        self.form1: str = form1
        self.form2: str = form2
        self.form3: str = form3
        self.form4: str = form4
        self.language: str = language
        self.translations: list[PlaceTranslation] = translations
        self.map: Map = map
        self.exids: list[Exid] = exids
        self.notes: list[Note] = notes
        self.extensions: list[Extension] = extensions
        self.place: str = Placer.place(
            self.place1, self.place2, self.place3, self.place4
        )
        self.form: str = Placer.form(
            self.form1, self.form2, self.form3, self.form4
        )
        self.descriptions: set[str] = set()
        self.plac_extensions: list[Extension] = []
        self.form_extensions: list[Extension] = []
        self.lang_extensions: list[Extension] = []
        if self.extensions is not None:
            for ext in self.extensions:
                self.descriptions.union(ext.schema.supers)
                if Tag.PLAC.value in ext.schema.supers:
                    self.plac_extensions.append(ext)
                elif Tag.FORM.value in ext.schema.supers:
                    self.form_extensions.append(ext)
                elif Tag.LANG.value in ext.schema.supers:
                    self.lang_extensions.append(ext)

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.place1, str)
            and Checker.verify_type(self.place2, str)
            and Checker.verify_type(self.place3, str)
            and Checker.verify_type(self.place4, str)
            and Checker.verify_type(self.form1, str)
            and Checker.verify_type(self.form2, str)
            and Checker.verify_type(self.form3, str)
            and Checker.verify_type(self.form4, str)
            and Checker.verify_type(self.language, str)
            and Checker.verify_tuple_type(self.translations, PlaceTranslation)
            and Checker.verify_type(self.map, Map)
            and Checker.verify_tuple_type(self.exids, Exid)
            and Checker.verify_tuple_type(self.notes, Note)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = String.EMPTY
        if self.validate():
            lines = Tagger.string(lines, level, Tag.PLAC, self.place)
            lines = Tagger.structure(lines, level + 1, self.plac_extensions)
            lines = Tagger.string(lines, level + 1, Tag.FORM, self.form)
            lines = Tagger.structure(lines, level + 1, self.form_extensions)
            lines = Tagger.string(lines, level + 1, Tag.LANG, self.language)
            lines = Tagger.structure(lines, level + 1, self.lang_extensions)
            lines = Tagger.structure(lines, level + 1, self.translations)
            lines = Tagger.structure(lines, level + 1, self.map, Map())
            lines = Tagger.structure(lines, level + 1, self.exids)
            lines = Tagger.structure(lines, level + 1, self.notes, Note())
        return lines

    def code(self, level: int = 0) -> str:
        return indent(
            f"""
Place(
    place1 = {Formatter.listcodes(self.place1)},
    place2 = {Formatter.listcodes(self.place2)},
    place3 = {Formatter.listcodes(self.place3)},
    place4 = {Formatter.listcodes(self.place4)},
    form1 = {Formatter.listcodes(self.form1)},
    form2 = {Formatter.listcodes(self.form2)},
    form3 = {Formatter.listcodes(self.form3)},
    form4 = {Formatter.listcodes(self.form4)},
    language = {Formatter.listcodes(self.language)},
    translations = {Formatter.listcodes(self.translations, level + 2)},
    map = {Formatter.listcodes(self.map, level + 1)},
    exids = {Formatter.listcodes(self.exids, level + 2)},
    notes = {Formatter.listcodes(self.notes, level + 2)},
    extensions = {Formatter.listcodes(self.extensions, level + 2)},
)""",
            String.INDENT * level,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        place1: str = Default.EMPTY,
        place2: str = Default.EMPTY,
        place3: str = Default.EMPTY,
        place4: str = Default.EMPTY,
        form1: str = Default.PLACE_FORM1,
        form2: str = Default.PLACE_FORM2,
        form3: str = Default.PLACE_FORM3,
        form4: str = Default.PLACE_FORM4,
        language: str = Default.EMPTY,
        translations: list[PlaceTranslation] | None = None,
        map: Map | None = None,
        exids: list[Exid] | None = None,
        notes: list[Note] | None = None,
        extensions: list[Extension] | None = None,
    ) -> str:
        """Produce four examples of ChronoData code and GEDCOM output lines and link to
        the GEDCOM documentation.

        The following levels are available:
        - 0 (Default) Produces an intentional error.  If the Map structure is used
            without specifying values, the default values will trigger an error.
            However, if an acceptable lattitude and longitude are used in this example,
            then the user example will be displayed.
        - 1 Produces an example with all arguments containing data.
        - 2 Produces an alternate example with possibly some arguments missing.
        - 3 Produces either another alternate example or an example with non-Latin
            character texts.

        Any other value passed in will produce the same as the default level.

        Args:
            choice: The example one chooses to display.
            latitude: If a non-zero latitude is entered this will be used in the example.
            longitude: If a non-zero longitude is entered this will be used in the example.
        """
        show: Place
        gedcom_docs: str = Specs.PLACE
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = Place(
                    place1='Chicago',
                    place2='Cook County',
                    place3='Illinois',
                    place4='USA',
                    translations=[
                        PlaceTranslation(
                            place1='Chicago',
                            place2='Cook County',
                            place3='Illinois',
                            place4='USA',
                            language='en-US',
                        ),
                    ],
                    map=Map(latitude=41.881832, longitude=-87.623177),
                    notes=[
                        Note(note='Just a note'),
                        Note(note='Just a second note'),
                    ],
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Place(
                    place1='Chicago',
                    place2='Cook County',
                    place3='Illinois',
                    place4='USA',
                    map=Map(latitude=41.881832, longitude=-87.623177),
                    notes=[Note(note='Just a note')],
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Place(
                    place1='Chicago',
                    place2='Cook County',
                    place3='Illinois',
                    place4='USA',
                    map=Map(latitude=41.881832, longitude=-87.623177),
                    notes=[Note(note='Just a note')],
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Place(
                    place1=place1,
                    place2=place2,
                    place3=place3,
                    place4=place4,
                    form1=form1,
                    form2=form2,
                    form3=form3,
                    form4=form4,
                    language=language,
                    translations=translations,
                    map=map,
                    exids=exids,
                    notes=notes,
                    extensions=extensions,
                )
                logging.info(Example.USER_PROVIDED_EXAMPLE)
                code_preface = Example.USER_PROVIDED
                gedcom_preface = Example.GEDCOM
        return Formatter.example(
            code_preface,
            show.code(),
            gedcom_preface,
            show.ged(),
            gedcom_docs,
            genealogy_docs,
        )


class EventDetail(NamedTuple):
    """Store, validate and display a GEDCOM Event Detail.

    Reference:
        [GEDCOM Event Detail](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#EVENT_DETAIL)

    > n <<DATE_VALUE>>                           {0:1}
    > n <<PLACE_STRUCTURE>>                      {0:1}
    > n <<ADDRESS_STRUCTURE>>                    {0:1}
    > n PHON <Special>                           {0:M}  [g7:PHON](https://gedcom.io/terms/v7/PHON)
    > n EMAIL <Special>                          {0:M}  [g7:EMAIL](https://gedcom.io/terms/v7/EMAIL)
    > n FAX <Special>                            {0:M}  [g7:FAX](https://gedcom.io/terms/v7/FAX)
    > n WWW <Special>                            {0:M}  [g7:WWW](https://gedcom.io/terms/v7/WWW)
    > n AGNC <Text>                              {0:1}  [g7:AGNC](https://gedcom.io/terms/v7/AGNC)
    > n RELI <Text>                              {0:1}  [g7:RELI](https://gedcom.io/terms/v7/RELI)
    > n CAUS <Text>                              {0:1}  [g7:CAUS](https://gedcom.io/terms/v7/CAUS)
    > n RESN <List:Enum>                         {0:1}  [g7:RESN](https://gedcom.io/terms/v7/RESN)
    > n SDATE <DateValue>                        {0:1}  [g7:SDATE](https://gedcom.io/terms/v7/SDATE)
    >   +1 TIME <Time>                           {0:1}  [g7:TIME](https://gedcom.io/terms/v7/TIME)
    >   +1 PHRASE <Text>                         {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    > n <<ASSOCIATION_STRUCTURE>>                {0:M}
    > n <<NOTE_STRUCTURE>>                       {0:M}
    > n <<SOURCE_CITATION>>                      {0:M}
    > n <<MULTIMEDIA_LINK>>                      {0:M}
    > n UID <Special>                            {0:M}  [g7:UID]()
    """

    date_value: DateValue = DateValue()
    place: Place | None = None
    address: Address = Address([], '', '', '', '')
    phones: list[str] = []  # noqa: RUF012
    emails: list[str] = []  # noqa: RUF012
    faxes: list[str] = []  # noqa: RUF012
    wwws: list[str] = []  # noqa: RUF012
    agency: str = ''
    religion: str = ''
    cause: str = ''
    resn: str = ''
    # sort_date: SortDate = ()
    associations: list[Association] = []  # noqa: RUF012
    notes: list[Note] = []  # noqa: RUF012
    sources: list[SourceCitation] = []  # noqa: RUF012
    multimedia_links: list[MultimediaLink] = []  # noqa: RUF012
    uids: list[Id] = []  # noqa: RUF012

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.date_value, DateValue)
            and Checker.verify_type(self.place, Place)
            and Checker.verify_type(self.address, Address)
            and Checker.verify_tuple_type(self.phones, str)
            and Checker.verify_tuple_type(self.emails, str)
            and Checker.verify_tuple_type(self.faxes, str)
            and Checker.verify_tuple_type(self.wwws, str)
            and Checker.verify_type(self.agency, str)
            and Checker.verify_type(self.religion, str)
            and Checker.verify_type(self.cause, str)
            and Checker.verify_type(self.resn, str)
            and Checker.verify_tuple_type(self.associations, Association)
            and Checker.verify_tuple_type(self.notes, Note)
            and Checker.verify_tuple_type(self.sources, Source)
            and Checker.verify_tuple_type(self.multimedia_links, MultimediaLink)
            and Checker.verify_tuple_type(self.uids, Id)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.structure(lines, level, self.date_value, DateValue())
            lines = Tagger.structure(lines, level, self.place, Place())
            lines = Tagger.structure(lines, level, self.address, Address())
            lines = Tagger.string(lines, level, Tag.PHON, self.phones)
            lines = Tagger.string(lines, level, Tag.EMAIL, self.emails)
            lines = Tagger.string(lines, level, Tag.FAX, self.faxes)
            lines = Tagger.string(lines, level, Tag.WWW, self.wwws)
            lines = Tagger.string(lines, level, Tag.AGNC, self.agency)
            lines = Tagger.string(lines, level, Tag.RELI, self.religion)
            lines = Tagger.string(lines, level, Tag.CAUS, self.cause)
            lines = Tagger.string(lines, level, Tag.RESN, self.resn)
            lines = Tagger.structure(lines, level, self.associations)
            lines = Tagger.structure(lines, level, self.notes)
            lines = Tagger.structure(lines, level, self.sources)
            lines = Tagger.structure(lines, level, self.multimedia_links)
            lines = Tagger.structure(lines, level, self.uids)
        return lines

    def code(self, level: int = 0, detail: str = String.MIN) -> str:
        spaces: str = String.INDENT * level
        preface: str = """
            # https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#EVENT_DETAIL
            from chronodata.constants import Choice
            from chronodata.store import Age, FamilyEventDetail

            """
        return indent(
            dedent(f"""
            {preface if detail == String.MAX else ''}
        """),
            spaces,
        )


class FamilyEventDetail(NamedTuple):
    """Store, validate and display GEDCOM family event detail structure.

    Examples:
        >>> from chronodata.store import FamilyEventDetail
        >>> family_detail = FamilyEventDetail(
        ...     husband_age=Age(25, phrase='Happy'),
        ...     wife_age=Age(24, phrase='Very happy'),
        ... )
        >>> print(family_detail.ged(1))
        1 HUSB
        2 AGE > 25y
        3 PHRASE Happy
        1 WIFE
        2 AGE > 24y
        3 PHRASE Very happy
        <BLANKLINE>

    References:
        [GEDCOM Family Event Detail](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_EVENT_DETAIL)

    > n HUSB                                     {0:1}  [g7:HUSB](https://gedcom.io/terms/v7/HUSB)
    >   +1 AGE <Age>                             {1:1}  [g7:AGE](https://gedcom.io/terms/v7/AGE)
    >      +2 PHRASE <Text>                      {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    > n WIFE                                     {0:1}  [g7:WIFE](https://gedcom.io/terms/v7/WIFE)
    >   +1 AGE <Age>                             {1:1}  [g7:AGE](https://gedcom.io/terms/v7/AGE)
    >      +2 PHRASE <Text>                      {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    > n <<EVENT_DETAIL>>                         {0:1}
    """

    husband_age: Age = Age()
    wife_age: Age = Age()
    event_detail: EventDetail = EventDetail()

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.husband_age, Age | None)
            and Checker.verify_type(self.wife_age, Age | None)
            and Checker.verify_type(self.event_detail, EventDetail | None)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            if self.husband_age != Age():
                lines = Tagger.empty(lines, level, Tag.HUSB)
                lines = Tagger.structure(lines, level + 1, self.husband_age)
            if self.wife_age != Age():
                lines = Tagger.empty(lines, level, Tag.WIFE)
                lines = Tagger.structure(lines, level + 1, self.wife_age)
            lines = Tagger.structure(
                lines, level, self.event_detail, EventDetail()
            )
        return lines

    def code(self, level: int = 0, detail: str = String.MIN) -> str:
        spaces: str = String.INDENT * level
        preface: str = """
            # https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_EVENT_DETAIL
            from chronodata.constants import Choice
            from chronodata.store import Age, FamilyEventDetail

            """
        return indent(
            dedent(f"""
            {preface if detail == String.MAX else ''}
        """),
            spaces,
        )


class FamilyAttribute(NamedTuple):
    """Store, validate and display a GEDCOM Family Attribute.

    Reference:
        [GEDCOM Family Attribute](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_ATTRIBUTE_STRUCTURE)

    > [
    > n NCHI <Integer>                           {1:1}  [g7:FAM-NCHI](https://gedcom.io/terms/v7/FAM-NCHI)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > |
    > n RESI <Text>                              {1:1}  [g7:FAM-RESI](https://gedcom.io/terms/v7/FAM-RESI)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > |
    > n FACT <Text>                              {1:1}  [g7:FAM-FACT](https://gedcom.io/terms/v7/FAM-FACT)
    >   +1 TYPE <Text>                           {1:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > ]
    """

    tag: Tag = Tag.NONE
    payload: str = String.EMPTY
    attribute_type: str = String.EMPTY
    family_event_detail: FamilyEventDetail = FamilyEventDetail()

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.tag, Tag)
            and Checker.verify_enum(self.tag.value, FamAttr)
            and Checker.verify_type(self.payload, str)
            and Checker.verify_type(self.attribute_type, str)
            and Checker.verify_type(self.family_event_detail, FamilyEventDetail)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.tag.value != Tag.NONE.value and self.validate():
            lines = Tagger.string(lines, level, self.tag, self.payload)
            lines = Tagger.string(
                lines, level + 1, Tag.TYPE, self.attribute_type
            )
            lines = Tagger.structure(
                lines, level + 1, self.family_event_detail, FamilyEventDetail()
            )
        return lines


class FamilyEvent(NamedTuple):
    """Store, validate and display a GEDCOM Family Event.

    Examples:
        Only the following tags can be used in this structure:
        Tag.ANUL, Tag.CENS, Tag.DIV, Tag.DIVF, Tag.ENGA, Tag.MARB, Tag.MARC, Tag.MARL,
        Tag.MARR, Tag.MARS, Tag.EVEN.  This example shows the error that
        would result if a different tag is used once the NamedTuple is validated.
        First, set up the situation for the error to occur.
        >>> from chronodata.constants import Tag
        >>> from chronodata.store import FamilyEvent
        >>> event = FamilyEvent(Tag.DATE)

        Next, evaluate `event`.
        >>> event.validate()
        Traceback (most recent call last):
        ValueError: The tag DATE is not in the list of valid tags.

        The `validate` method also checks that the Tag.EVEN cannot have an empty payload.
        >>> event2 = FamilyEvent(Tag.EVEN)
        >>> event2.validate()
        Traceback (most recent call last):
        ValueError: The event type for tag EVEN must have some value.

    References:
        [GEDCOM Family Event](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_EVENT_STRUCTURE)

    > [
    > n ANUL [Y|<NULL>]                          {1:1}  [g7:ANUL](https://gedcom.io/terms/v7/ANUL)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > |
    > n CENS [Y|<NULL>]                          {1:1}  [g7:FAM-CENS](https://gedcom.io/terms/v7/FAM-CENS)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > |
    > n DIV [Y|<NULL>]                           {1:1}  [g7:DIV](https://gedcom.io/terms/v7/DIV)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > |
    > n DIVF [Y|<NULL>]                          {1:1}  [g7:DIVF](https://gedcom.io/terms/v7/DIVF)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > |
    > n ENGA [Y|<NULL>]                          {1:1}  [g7:ENGA](https://gedcom.io/terms/v7/ENGA)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > |
    > n MARB [Y|<NULL>]                          {1:1}  [g7:MARB](https://gedcom.io/terms/v7/MARB)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > |
    > n MARC [Y|<NULL>]                          {1:1}  [g7:MARC](https://gedcom.io/terms/v7/MARC)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > |
    > n MARL [Y|<NULL>]                          {1:1}  [g7:MARL](https://gedcom.io/terms/v7/MARL)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > |
    > n MARR [Y|<NULL>]                          {1:1}  [g7:MARR](https://gedcom.io/terms/v7/MARR)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > |
    > n MARS [Y|<NULL>]                          {1:1}  [g7:MARS](https://gedcom.io/terms/v7/MARS)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > |
    > n EVEN <Text>                              {1:1}  [g7:FAM-EVEN](https://gedcom.io/terms/v7/FAM-EVEN)
    >   +1 TYPE <Text>                           {1:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > ]
    """

    tag: Tag = Tag.NONE
    payload: str = String.OCCURRED
    event_type: str = String.EMPTY
    event_detail: FamilyEventDetail | None = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check_payload: bool = self.payload in {
            String.OCCURRED,
            String.EMPTY,
        }
        check_tag: bool = self.tag.value in {
            Tag.ANUL.value,
            Tag.CENS.value,
            Tag.DIV.value,
            Tag.DIVF.value,
            Tag.ENGA.value,
            Tag.MARB.value,
            Tag.MARC.value,
            Tag.MARL.value,
            Tag.MARR.value,
            Tag.MARS.value,
        }
        even: bool = self.event_type != String.EMPTY
        check: bool = (
            Checker.verify_type(self.tag, Tag)
            and Checker.verify_enum(self.tag.value, FamEven)
            and Checker.verify_type(self.payload, str)
            and Checker.verify_type(self.event_type, str)
            and Checker.verify_type(self.event_detail, FamilyEventDetail | None)
            and Checker.verify(
                check_tag,
                check_payload,
                Msg.TAG_PAYLOAD.format(self.tag.value),
            )
            and Checker.verify(
                not check_tag, even, Msg.EMPTY_EVENT_TYPE.format(self.tag.value)
            )
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            if self.payload == String.EMPTY:
                lines = Tagger.empty(lines, level, self.tag)
            else:
                lines = Tagger.string(lines, level, self.tag, self.payload)
            lines = Tagger.string(lines, level + 1, Tag.TYPE, self.event_type)
            lines = Tagger.structure(lines, level + 1, self.event_detail)
        return lines

    def code(self, level: int = 0, detail: str = String.MIN) -> str:
        spaces: str = String.INDENT * level
        preface: str = """
            # https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_EVENT_STRUCTURE
            from chronodata.constants import Choice
            from chronodata.store import FamilyEvent

            """
        return indent(
            dedent(f"""
            {preface if detail == String.MAX else ''}
        """),
            spaces,
        )


class Husband(NamedTuple):
    xref: IndividualXref = Void.INDI
    phrase: str = String.EMPTY

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = Checker.verify_type(
            self.phrase, str
        ) and Checker.verify_type(self.xref, IndividualXref)
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = String.EMPTY
        if str(self.xref) != Void.NAME and self.validate():
            lines = Tagger.string(
                lines, level, Tag.HUSB, str(self.xref), format=False
            )
            lines = Tagger.string(lines, level + 1, Tag.PHRASE, self.phrase)
        return lines


class Wife(NamedTuple):
    xref: IndividualXref = Void.INDI
    phrase: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = Checker.verify_type(
            self.phrase, str
        ) and Checker.verify_type(self.xref, IndividualXref)
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = String.EMPTY
        if str(self.xref) != Void.NAME and self.validate():
            lines = Tagger.string(
                lines, level, Tag.WIFE, str(self.xref), format=False
            )
            lines = Tagger.string(lines, level + 1, Tag.PHRASE, self.phrase)
        return lines


class Child(NamedTuple):
    """Store, validate and display GEDCOM child information.

    Reference:
        [GEDCOM Family Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_RECORD)

    This is a portion of the GEDCOM Family Record.
    >     +1 CHIL @<XREF:INDI>@                    {0:M}  g7:CHIL
    >        +2 PHRASE <Text>                      {0:1}  g7:PHRASE
    """

    xref: IndividualXref = Void.INDI
    phrase: str = String.EMPTY

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = Checker.verify_type(
            self.phrase, str
        ) and Checker.verify_type(self.xref, IndividualXref)
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = String.EMPTY
        if str(self.xref) != Void.NAME and self.validate():
            lines = Tagger.string(
                lines, level, Tag.CHIL, str(self.xref), format=False
            )
            lines = Tagger.string(lines, level + 1, Tag.PHRASE, self.phrase)
        return lines


class LDSOrdinanceDetail(NamedTuple):
    """Store, validate and display the GEDCOM LDS Ordinance Detail structure.

    Reference:
        [GEDCOM LDS Ordinance Detail](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#LDS_ORDINANCE_DETAIL)

    > n <<DATE_VALUE>>                         {0:1}
    > n TEMP <Text>                            {0:1}  [g7:TEMP](https://gedcom.io/terms/v7/TEMP)
    > n <<PLACE_STRUCTURE>>                    {0:1}
    > n STAT <Enum>                            {0:1}  [g7:ord-STAT](https://gedcom.io/terms/v7/ord-STAT)
    >   +1 DATE <DateExact>                    {1:1}  [g7:DATE-exact](https://gedcom.io/terms/v7/DATE-exact)
    >      +2 TIME <Time>                      {0:1}  [g7:TIME](https://gedcom.io/terms/v7/TIME)
    > n <<NOTE_STRUCTURE>>                     {0:M}
    > n <<SOURCE_CITATION>>                    {0:M}
    """

    date_value: DateValue = DateValue()
    temple: str = String.EMPTY
    place: Place = Place()
    status: Stat = Stat.NONE
    status_date: Date = Date()
    status_time: Time = Time()
    notes: list[Note] = [Note(), Note()]  # noqa: RUF012
    source_citations: list[SourceCitation] = [  # noqa: RUF012
        SourceCitation(),
        SourceCitation(),
    ]

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.date_value, DateValue)
            and Checker.verify_type(self.temple, str)
            and Checker.verify_type(self.place, Place)
            and Checker.verify_enum(self.status.value, Stat)
            and Checker.verify_type(self.status_date, Date)
            and Checker.verify_type(self.status_time, Time)
            and Checker.verify_tuple_type(self.notes, Note)
            and Checker.verify_tuple_type(self.source_citations, SourceCitation)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.structure(lines, level, self.date_value, DateValue())
            lines = Tagger.string(lines, level, Tag.TEMP, self.temple)
            lines = Tagger.structure(lines, level, self.place, Place())
            lines = Tagger.string(lines, level, Tag.STAT, self.status.value)
            lines = Tagger.structure(lines, level + 1, self.status_date, Date())
            lines = Tagger.structure(lines, level + 1, self.status_time, Time())
            lines = Tagger.structure(lines, level, self.notes, Note())
            lines = Tagger.structure(
                lines, level, self.source_citations, SourceCitation()
            )
        return lines


class LDSSpouseSealing(NamedTuple):
    """Store, validate and display the LDS Spouse Sealing structure.

    Reference:
        [GEDCOM LDS Spouse Sealing Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#LDS_SPOUSE_SEALING)

    > n SLGS                                     {1:1}  [g7:SLGS](https://gedcom.io/terms/v7/SLGS)
    >   +1 <<LDS_ORDINANCE_DETAIL>>              {0:1}
    """

    tag: Tag = Tag.SLGS
    detail: LDSOrdinanceDetail = LDSOrdinanceDetail()

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = Checker.verify_type(
            self.tag, str
        ) and Checker.verify_type(self.detail, LDSOrdinanceDetail | None)
        return check

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
        return lines


class LDSIndividualOrdinance(NamedTuple):
    """Store, validate and display the GEDCOM LDS Individual Ordinances structure.

    Reference:
        [GEDCOM LDS Individual Ordinances](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#LDS_INDIVIDUAL_ORDINANCE)

    [
    n BAPL                                     {1:1}  [g7:BAPL](https://gedcom.io/terms/v7/BAPL)
      +1 <<LDS_ORDINANCE_DETAIL>>              {0:1}
    |
    n CONL                                     {1:1}  [g7:CONL](https://gedcom.io/terms/v7/CONL)
      +1 <<LDS_ORDINANCE_DETAIL>>              {0:1}
    |
    n ENDL                                     {1:1}  [g7:ENDL](https://gedcom.io/terms/v7/ENDL)
      +1 <<LDS_ORDINANCE_DETAIL>>              {0:1}
    |
    n INIL                                     {1:1}  [g7:INIL](https://gedcom.io/terms/v7/INIL)
      +1 <<LDS_ORDINANCE_DETAIL>>              {0:1}
    |
    n SLGC                                     {1:1}  [g7:SLGC](https://gedcom.io/terms/v7/SLGC)
      +1 <<LDS_ORDINANCE_DETAIL>>              {0:1}
      +1 FAMC @<XREF:FAM>@                     {1:1}  [g7:FAMC](https://gedcom.io/terms/v7/FAMC)
    ]
    """

    tag: Tag = Tag.NONE
    ordinance_detail: LDSOrdinanceDetail = LDSOrdinanceDetail()
    family_xref: FamilyXref = Void.FAM

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.tag, Tag)
            and Checker.verify_type(self.ordinance_detail, LDSOrdinanceDetail)
            and Checker.verify_type(self.family_xref, FamilyXref)
            and Checker.verify(
                self.tag.value == Tag.SLGC.value,
                self.family_xref.fullname != Void.FAM.fullname,
                Msg.SLGC_REQUIRES_FAM,
            )
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.empty(lines, level, self.tag)
            lines = Tagger.structure(lines, level + 1, self.ordinance_detail)
            if self.tag == Tag.SLGC:
                lines = Tagger.string(
                    lines, level + 1, Tag.FAMC, self.family_xref.fullname
                )
        return lines


class Identifier(NamedTuple):
    """Construct GEDCOM data for the Identifier Structure.

    There are three valid identifier structures.  They will be illustrated in
    the examples.

    Examples:



    Reference:

    - [GEDCOM Identifier Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#IDENTIFIER_STRUCTURE)"""

    tag: Id = Id.NONE
    tag_info: str = ''
    tag_type: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_enum(self.tag.value, Id)
            and Checker.verify_type(self.tag_info, str)
            and Checker.verify_type(self.tag_type, str)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            if self.tag != Id.NONE:
                lines = Tagger.taginfo(level, self.tag.value, self.tag_info)
            if self.tag != Id.UID:
                lines = ''.join(
                    [lines, Tagger.taginfo(level + 1, Tag.TYPE, self.tag_type)]
                )
            if self.tag == Id.EXID and self.tag_type == '':
                logging.warning(Msg.EXID_TYPE)
        return lines


class IndividualEventDetail(NamedTuple):
    """Store, validate and display a GEDCOM Individual Event Detail structure.

    Args:
        event_detail: A GEDCOM Event Detail structure.
        age: The age of the individual.
        phrase: Text describing the individual event.

    Reference:
        [GEDCOM Individual Event Detail](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_EVENT_DETAIL)

    > n <<EVENT_DETAIL>>                         {1:1}
    > n AGE <Age>                                {0:1}  [g7:AGE](https://gedcom.io/terms/v7/AGE)
    >   +1 PHRASE <Text>                         {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    """

    event_detail: EventDetail | None = None
    age: Age | None = None  # Age(0, 0, 0, 0, String.EMPTY, String.EMPTY)
    phrase: str = String.EMPTY

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.event_detail, EventDetail)
            and Checker.verify_type(self.age, Age)
            and Checker.verify_type(self.phrase, str)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate() and self.event_detail is not None:
            lines = Tagger.structure(
                lines, level, self.event_detail, EventDetail
            )
            if self.age is not None:
                lines = Tagger.structure(lines, level, self.age, Age())
                lines = Tagger.string(lines, level + 1, Tag.PHRASE, self.phrase)
        return lines


class IndividualAttribute(NamedTuple):
    """Store, validate and display a GEDCOM Individual Attribute structure.

    Reference:
        [GEDCOM Individual Attribute Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_ATTRIBUTE_STRUCTURE)

    > [
    > n CAST <Text>                              {1:1}  [g7:CAST](https://gedcom.io/terms/v7/CAST)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n DSCR <Text>                              {1:1}  [g7:DSCR](https://gedcom.io/terms/v7/DSCR)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n EDUC <Text>                              {1:1}  [g7:EDUC](https://gedcom.io/terms/v7/EDUC)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n IDNO <Special>                           {1:1}  [g7:IDNO](https://gedcom.io/terms/v7/IDNO)
    >   +1 TYPE <Text>                           {1:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n NATI <Text>                              {1:1}  [g7:NATI](https://gedcom.io/terms/v7/NATI)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n NCHI <Integer>                           {1:1}  [g7:INDI-NCHI](https://gedcom.io/terms/v7/INDI-NCHI)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n NMR <Integer>                            {1:1}  [g7:NMR](https://gedcom.io/terms/v7/NMR)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n OCCU <Text>                              {1:1}  [g7:OCCU](https://gedcom.io/terms/v7/OCCU)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n PROP <Text>                              {1:1}  [g7:PROP](https://gedcom.io/terms/v7/PROP)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n RELI <Text>                              {1:1}  [g7:INDI-RELI](https://gedcom.io/terms/v7/INDI-RELI)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n RESI <Text>                              {1:1}  [g7:INDI-RESI](https://gedcom.io/terms/v7/INDI-RESI)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n SSN <Special>                            {1:1}  [g7:SSN](https://gedcom.io/terms/v7/SSN)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n TITL <Text>                              {1:1}  [g7:INDI-TITL](https://gedcom.io/terms/v7/INDI-TITL)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n FACT <Text>                              {1:1}  [g7:INDI-FACT](https://gedcom.io/terms/v7/INDI-FACT)
    >   +1 TYPE <Text>                           {1:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > ]
    """

    tag: IndiAttr
    tag_type: str = ''
    event_detail: IndividualEventDetail = IndividualEventDetail()

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_enum(self.tag.value, IndiAttr)
            and Checker.verify_type(self.tag_type, str)
            and Checker.verify_type(self.event_detail, IndividualEventDetail)
        )
        return check

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
        return lines


class IndividualEvent(NamedTuple):
    """Store, validate and display a GEDCOM Individual Event Structure.

    Examples:
        The GEDCOM specification offers the following example of the use of the `EVEN` event
        tag.  Under the individual `@I1@` there are two events.  The first is a land lease
        with a data of October 2, 1837.  The second is a lease of mining equipment with
        a data of November 4, 1837.

        > 0 @I1@ INDI
        > 1 EVEN
        > 2 TYPE Land Lease
        > 2 DATE 2 OCT 1837
        > 1 EVEN Mining equipment
        > 2 TYPE Equipment Lease
        > 2 DATE 4 NOV 1837

        This example can be implemented as follows.

        First import the needed classes.
        >>> from chronodata.build import Genealogy
        >>> from chronodata.store import Individual, IndividualEvent

        Next, create a Genealogy and an individual with reference `@I1@`.
        >>> genealogy = Genealogy('event example')
        >>> indi_i1_xref = genealogy.individual_xref('I1')

        Finally, create the individual record for `@I1@` with two individual events
        and display the results.
        >>> indi_i1 = Individual(
        ...     xref=indi_i1_xref,
        ...     events=[
        ...         IndividualEvent(
        ...             tag=Tag.EVEN,
        ...             text='Land Lease',
        ...             event_detail=IndividualEventDetail(
        ...                 event_detail=EventDetail(
        ...                     date_value=DateValue(Date(1837, 10, 2))
        ...                 )
        ...             ),
        ...         ),
        ...         IndividualEvent(
        ...             tag=Tag.EVEN,
        ...             payload='Mining equipment',
        ...             text='Equipment Lease',
        ...             event_detail=IndividualEventDetail(
        ...                 EventDetail(date_value=DateValue(Date(1837, 11, 4)))
        ...             ),
        ...         ),
        ...     ],
        ... )
        >>> print(indi_i1.ged(0))
        0 @I1@ INDI
        1 EVEN
        2 TYPE Land Lease
        2 DATE 2 OCT 1837
        1 EVEN Mining equipment
        2 TYPE Equipment Lease
        2 DATE 4 NOV 1837
        <BLANKLINE>

    Args:
        tag: Specifies the kind of event.
        payload: Specifies that the event occurred if the default 'Y' is accepted. Otherwise use ''.
        tag_type: A text describing the event which must not be the empty string.
        event_detail: Information about the event in an IndividualEventDetail substructure.
        family_xref: A family xref will be displayed only for the Tag.ADOP, Tag.BIRT or Tag.CHR events.
        adoption: A tag for the kind of adoption will be displayed only for the Tag.ADOP event.
        phrase: A phrase describing the adoption will be displayed only for the Tag.ADOP event.

    References:
        [GEDCOM INDI-EVEN](https://gedcom.io/terms/v7/INDI-EVEN)
        [GEDCOM Individual Event Tags](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#individual-events)
        [GEDCOM Individual Event Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_EVENT_STRUCTURE)

    [
    > n ADOP [Y|<NULL>]                          {1:1}  [g7:ADOP](https://gedcom.io/terms/v7/ADOP)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    >   +1 FAMC @<XREF:FAM>@                     {0:1}  [g7:ADOP-FAMC](https://gedcom.io/terms/v7/ADOP-FAMC)
    >      +2 ADOP <Enum>                        {0:1}  [g7:FAMC-ADOP](https://gedcom.io/terms/v7/FAMC-ADOP)
    >         +3 PHRASE <Text>                   {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    > |
    > n BAPM [Y|<NULL>]                          {1:1}  [g7:BAPM](https://gedcom.io/terms/v7/BAPM)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n BARM [Y|<NULL>]                          {1:1}  [g7:BARM](https://gedcom.io/terms/v7/BARM)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n BASM [Y|<NULL>]                          {1:1}  [g7:BASM](https://gedcom.io/terms/v7/BASM)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n BIRT [Y|<NULL>]                          {1:1}  [g7:BIRT](https://gedcom.io/terms/v7/BIRT)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    >   +1 FAMC @<XREF:FAM>@                     {0:1}  [g7:FAMC](https://gedcom.io/terms/v7/FAMC)
    > |
    > n BLES [Y|<NULL>]                          {1:1}  [g7:BLES](https://gedcom.io/terms/v7/BLES)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n BURI [Y|<NULL>]                          {1:1}  [g7:BURI](https://gedcom.io/terms/v7/BURI)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n CENS [Y|<NULL>]                          {1:1}  [g7:INDI-CENS](https://gedcom.io/terms/v7/INDI-CENS)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n CHR [Y|<NULL>]                           {1:1}  [g7:CHR](https://gedcom.io/terms/v7/CHR)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    >   +1 FAMC @<XREF:FAM>@                     {0:1}  [g7:FAMC](https://gedcom.io/terms/v7/FAMC)
    > |
    > n CHRA [Y|<NULL>]                          {1:1}  [g7:CHRA](https://gedcom.io/terms/v7/CHRA)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n CONF [Y|<NULL>]                          {1:1}  [g7:CONF](https://gedcom.io/terms/v7/CONF)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n CREM [Y|<NULL>]                          {1:1}  [g7:CREM](https://gedcom.io/terms/v7/CREM)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n DEAT [Y|<NULL>]                          {1:1}  [g7:DEAT](https://gedcom.io/terms/v7/DEAT)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n EMIG [Y|<NULL>]                          {1:1}  [g7:EMIG](https://gedcom.io/terms/v7/EMIG)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n FCOM [Y|<NULL>]                          {1:1}  [g7:FCOM](https://gedcom.io/terms/v7/FCOM)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n GRAD [Y|<NULL>]                          {1:1}  [g7:GRAD](https://gedcom.io/terms/v7/GRAD)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n IMMI [Y|<NULL>]                          {1:1}  [g7:IMMI](https://gedcom.io/terms/v7/IMMI)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n NATU [Y|<NULL>]                          {1:1}  [g7:NATU](https://gedcom.io/terms/v7/NATU)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n ORDN [Y|<NULL>]                          {1:1}  [g7:ORDN](https://gedcom.io/terms/v7/ORDN)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n PROB [Y|<NULL>]                          {1:1}  [g7:PROB](https://gedcom.io/terms/v7/PROB)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n RETI [Y|<NULL>]                          {1:1}  [g7:RETI](https://gedcom.io/terms/v7/RETI)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n WILL [Y|<NULL>]                          {1:1}  [g7:WILL](https://gedcom.io/terms/v7/WILL)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n EVEN <Text>                              {1:1}  [g7:INDI-EVEN](https://gedcom.io/terms/v7/INDI-EVEN)
    >   +1 TYPE <Text>                           {1:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > ]
    """

    tag: Tag = Tag.NONE
    payload: str = String.EMPTY
    text: str = String.EMPTY
    event_detail: IndividualEventDetail = IndividualEventDetail()
    family_xref: FamilyXref = Void.FAM
    adoption: Tag = Tag.NONE
    phrase: str = String.EMPTY

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_enum(self.tag.value, IndiEven)
            and Checker.verify_type(self.text, str)
            and Checker.verify_type(self.event_detail, IndividualEventDetail)
            and Checker.verify_type(self.family_xref, FamilyXref)
            and Checker.verify_enum(self.adoption.value, Adop)
            and Checker.verify_type(self.phrase, str)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            if self.payload == String.EMPTY:
                lines = Tagger.empty(lines, level, self.tag)
            else:
                lines = Tagger.string(lines, level, self.tag, self.payload)
            lines = Tagger.string(lines, level + 1, Tag.TYPE, self.text)
            lines = Tagger.structure(lines, level + 1, self.event_detail)
            if (
                self.tag.value
                in (Tag.BIRT.value, Tag.CHR.value, Tag.ADOP.value)
                and self.family_xref.name != Void.FAM.name
            ):
                lines = Tagger.string(
                    lines, level + 1, Tag.FAMC, self.family_xref.fullname
                )
                if (
                    self.tag.value == Tag.ADOP.value
                    and self.family_xref.name != Void.FAM.name
                ):
                    lines = Tagger.string(
                        lines, level + 2, Tag.ADOP, self.adoption.value
                    )
                    if self.adoption.value != Tag.NONE.value:
                        lines = Tagger.string(
                            lines, level + 3, Tag.PHRASE, self.phrase
                        )
        return lines


class Alias(NamedTuple):
    """Store, validate and display a GEDCOM Alias structure.

    Data about an individual may be contained in the individual records of other individuals.
    This tag references those other individuals.

    This alias information is defined as its own class because multiple aliases could
    be identified for a single individual.

    Args:
        xref: An individual cross-reference identifier containing information about
            the individual referenced in the individual record.
        phrase: Text associated with this other individual.

    Reference:
        [GEDCOM Individual Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_RECORD)

    > +1 ALIA @<XREF:INDI>@                    {0:M}  [g7:ALIA](https://gedcom.io/terms/v7/ALIA)
    >    +2 PHRASE <Text>                      {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    """

    xref: IndividualXref = Void.INDI
    phrase: str = String.EMPTY

    def validate(self, main_individual: IndividualXref = Void.INDI) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.xref, IndividualXref)
            and Checker.verify_type(self.phrase, str)
            and Checker.verify(
                True,
                self.xref != main_individual,
                Msg.SAME_INDIVIDUAL.format(self.xref.fullname),
            )
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.ALIA, self.xref.fullname)
            lines = Tagger.string(lines, level + 1, Tag.PHRASE, self.phrase)
        return lines


class FamilyChild(NamedTuple):
    """Store, validate and display family child data.

    Multiple FAMC records may be defined for a singe Indivdiual Record.  This class
    defines a single FAMC (Family Child) substructure.

    References:
        [GEDCOM Individual Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_RECORD)

    > +1 FAMC @<XREF:FAM>@                     {0:M}  [g7:INDI-FAMC](https://gedcom.io/terms/v7/INDI-FAMC)
    >    +2 PEDI <Enum>                        {0:1}  [g7:PEDI](https://gedcom.io/terms/v7/PEDI)
    >       +3 PHRASE <Text>                   {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    >    +2 STAT <Enum>                        {0:1}  [g7:FAMC-STAT](https://gedcom.io/terms/v7/FAMC-STAT)
    >       +3 PHRASE <Text>                   {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    >    +2 <<NOTE_STRUCTURE>>                 {0:M}
    """

    family_xref: FamilyXref
    pedigree: str = ''
    pedigree_phrase: str = ''
    status: str = ''
    status_phrase: str = ''
    notes: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.family_xref, str)
            and Checker.verify_type(self.pedigree, str)
            and Checker.verify_type(self.pedigree_phrase, str)
            and Checker.verify_type(self.status, str)
            and Checker.verify_type(self.status_phrase, str)
            and Checker.verify_tuple_type(self.notes, Note)
        )
        return check

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
        return lines


class FamilySpouse(NamedTuple):
    family_xref: str = ''
    notes: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = Checker.verify_type(
            self.family_xref, str
        ) and Checker.verify_tuple_type(self.notes, Note)
        return check

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
        return lines


class FileTranslations(NamedTuple):
    path: str = ''
    media_type: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = Checker.verify_type(
            self.path, str
        ) and Checker.verify_type(self.media_type, str)
        return check

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
        return lines


# class Text(NamedTuple):
#     text: str = ''
#     mime: MediaType = MediaType.NONE
#     language: Lang = Lang.CODE['NONE']

#     def validate(self) -> bool:
#         """Validate the stored value."""
#         check: bool = (
#             Checker.verify_type(self.text, str)
#             and Checker.verify_type(self.mime, MediaType)
#             and Checker.verify_type(self.language, Lang)
#         )
#         return check

#     def ged(self, level: int = 1) -> str:
#         """Format to meet GEDCOM standards."""
#         lines: str = ''
#         if self.validate():
#             pass
#         return lines


class File(NamedTuple):
    path: str = ''
    media_type: MediaType = MediaType.NONE
    media: str = ''
    phrase: str = ''
    title: str = ''
    file_translations: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.path, str)
            and Checker.verify_type(self.media_type, str)
            and Checker.verify_type(self.media, str)
            and Checker.verify_type(self.phrase, str)
            and Checker.verify_type(self.title, str)
            and Checker.verify_tuple_type(
                self.file_translations, FileTranslations
            )
        )
        return check

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
        return lines


class SourceEvent(NamedTuple):
    event: str = ''
    date_period: str = ''
    phrase: str = ''
    place: Place | None = None
    agency: str = ''
    notes: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.event, str)
            and Checker.verify_type(self.date_period, str)
            and Checker.verify_type(self.phrase, str)
            and Checker.verify_type(self.place, str)
            and Checker.verify_type(self.agency, str)
            and Checker.verify_tuple_type(self.notes, Note)
        )
        return check

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
        return lines


class NonEvent(NamedTuple):
    no: str = ''
    date: Date | None = None
    phrase: str = ''
    notes: Any = None
    sources: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.no, str)
            and Checker.verify_type(self.date, Date | None)
            and Checker.verify_type(self.phrase, str)
            and Checker.verify_tuple_type(self.notes, Note)
            and Checker.verify_tuple_type(self.sources, SourceEvent)
        )
        return check

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
        return lines


class Family(NamedTuple):
    """Store, validate and display a GEDCOM Family Record.

    Args:
    - `xref`: typed string obtained by running `chrono.family_xref()`.
    - `resn`: restriction codes with the default being no restriction.
    - `attributes`: a tuple of type Attribute.

    Reference:
        [GEDCOM record-FAM](https://gedcom.io/terms/v7/record-FAM)
        [GEDCOM specification](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_RECORD)

    > n @XREF:FAM@ FAM                           {1:1}  [g7:record-FAM](https://gedcom.io/terms/v7/record-FAM)
    >   +1 RESN <List:Enum>                      {0:1}  [g7:RESN](https://gedcom.io/terms/v7/RESN)
    >   +1 <<FAMILY_ATTRIBUTE_STRUCTURE>>        {0:M}
    >   +1 <<FAMILY_EVENT_STRUCTURE>>            {0:M}
    >   +1 <<NON_EVENT_STRUCTURE>>               {0:M}
    >   +1 HUSB @<XREF:INDI>@                    {0:1}  [g7:FAM-HUSB](https://gedcom.io/terms/v7/FAM-HUSB)
    >      +2 PHRASE <Text>                      {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    >   +1 WIFE @<XREF:INDI>@                    {0:1}  [g7:FAM-WIFE](https://gedcom.io/terms/v7/FAM-WIFE)
    >      +2 PHRASE <Text>                      {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    >   +1 CHIL @<XREF:INDI>@                    {0:M}  [g7:CHIL](https://gedcom.io/terms/v7/CHIL)
    >      +2 PHRASE <Text>                      {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    >   +1 <<ASSOCIATION_STRUCTURE>>             {0:M}
    >   +1 SUBM @<XREF:SUBM>@                    {0:M}  [g7:SUBM](https://gedcom.io/terms/v7/SUBM)
    >   +1 <<LDS_SPOUSE_SEALING>>                {0:M}
    >   +1 <<IDENTIFIER_STRUCTURE>>              {0:M}
    >   +1 <<NOTE_STRUCTURE>>                    {0:M}
    >   +1 <<SOURCE_CITATION>>                   {0:M}
    >   +1 <<MULTIMEDIA_LINK>>                   {0:M}
    >   +1 <<CHANGE_DATE>>                       {0:1}
    >   +1 <<CREATION_DATE>>                     {0:1}
    """

    xref: FamilyXref = Void.FAM
    resn: Resn = Resn.NONE
    attributes: Any = None
    events: Any = None
    husband: Husband = Husband(Void.INDI)
    wife: Wife = Wife(Void.INDI)
    children: Any = None
    associations: Any = None
    submitters: Any = None
    lds_spouse_sealings: Any = None
    identifiers: Any = None
    notes: Any = None
    citations: Any = None
    multimedia_links: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.xref, FamilyXref)
            and Checker.verify_enum(self.resn.value, Resn)
            and Checker.verify_tuple_type(self.attributes, FamilyAttribute)
            and Checker.verify_tuple_type(self.events, FamilyEvent)
            and Checker.verify_type(self.husband, Husband)
            and Checker.verify_type(self.wife, Wife)
            and Checker.verify_tuple_type(self.children, Child)
            and Checker.verify_tuple_type(self.associations, Association)
            and Checker.verify_tuple_type(self.submitters, SubmitterXref)
            and Checker.verify_tuple_type(
                self.lds_spouse_sealings, LDSSpouseSealing
            )
            and Checker.verify_tuple_type(self.identifiers, Identifier)
            and Checker.verify_tuple_type(self.notes, Note)
            and Checker.verify_tuple_type(self.citations, SourceCitation)
            and Checker.verify_tuple_type(self.multimedia_links, MultimediaLink)
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged()
        if self.validate():
            if self.resn != Resn.NONE:
                lines = ''.join(
                    [lines, Tagger.taginfo(level, Tag.RESN, self.resn.value)]
                )
            lines = Tagger.structure(lines, level, self.attributes)
            lines = Tagger.structure(lines, level, self.events)
            lines = Tagger.structure(lines, level + 1, self.husband)
            lines = Tagger.structure(lines, level + 1, self.wife)
            lines = Tagger.structure(lines, level + 1, self.children)
            lines = Tagger.structure(lines, level + 1, self.associations)
            lines = Tagger.string(lines, level, Tag.SUBM, self.submitters)
            lines = Tagger.structure(lines, level + 1, self.lds_spouse_sealings)
            lines = Tagger.structure(lines, level + 1, self.identifiers)
            lines = Tagger.structure(lines, level + 1, self.notes)
            lines = Tagger.structure(lines, level + 1, self.citations)
            lines = Tagger.structure(lines, level + 1, self.multimedia_links)
        return lines


class Multimedia(NamedTuple):
    """Store, validate and display a GECDOM Multimedia Record.

    Reference:
        [GEDCOM record-OBJE](https://gedcom.io/terms/v7/record-OBJE)
        [GEDCOM specification](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#MULTIMEDIA_RECORD)

    > n @XREF:OBJE@ OBJE                         {1:1}  [g7:record-OBJE](https://gedcom.io/terms/v7/record-OBJE)
    >   +1 RESN <List:Enum>                      {0:1}  [g7:RESN](https://gedcom.io/terms/v7/RESN)
    >   +1 FILE <FilePath>                       {1:M}  [g7:FILE](https://gedcom.io/terms/v7/FILE)
    >      +2 FORM <MediaType>                   {1:1}  [g7:FORM](https://gedcom.io/terms/v7/FORM)
    >         +3 MEDI <Enum>                     {0:1}  [g7:MEDI](https://gedcom.io/terms/v7/MEDI)
    >            +4 PHRASE <Text>                {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    >      +2 TITL <Text>                        {0:1}  [g7:TITL](https://gedcom.io/terms/v7/TITL)
    >      +2 TRAN <FilePath>                    {0:M}  [g7:FILE-TRAN](https://gedcom.io/terms/v7/FILE-TRAN)
    >         +3 FORM <MediaType>                {1:1}  [g7:FORM](https://gedcom.io/terms/v7/FORM)
    >   +1 <<IDENTIFIER_STRUCTURE>>              {0:M}
    >   +1 <<NOTE_STRUCTURE>>                    {0:M}
    >   +1 <<SOURCE_CITATION>>                   {0:M}
    >   +1 <<CHANGE_DATE>>                       {0:1}
    >   +1 <<CREATION_DATE>>                     {0:1}
    """

    xref: MultimediaXref = Void.OBJE
    resn: Resn = Resn.NONE
    files: Any = None
    identifiers: Any = None
    notes: Any = None
    sources: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.xref, MultimediaXref)
            and Checker.verify_enum(self.resn.value, Resn)
            and Checker.verify_tuple_type(self.files, File)
            and Checker.verify_tuple_type(self.identifiers, Identifier)
            and Checker.verify_tuple_type(self.notes, Note)
            and Checker.verify_tuple_type(self.sources, Source)
        )
        return check

    def ged(self, level: int = 0) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged()
        if self.validate():
            pass
        return lines


class Source(NamedTuple):
    """Store, validate and display a GEDCOM Source Record.

    Reference:
        [GEDCOM record-SOUR](https://gedcom.io/terms/v7/record-SOUR)
        [GEDCOM specification](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_RECORD)

    > n @XREF:SOUR@ SOUR                         {1:1}  [g7:record-SOUR](https://gedcom.io/terms/v7/record-SOUR)
    >   +1 DATA                                  {0:1}  [g7:DATA]()
    >      +2 EVEN <List:Enum>                   {0:M}  [g7:DATA-EVEN]()
    >         +3 DATE <DatePeriod>               {0:1}  [g7:DATA-EVEN-DATE]()
    >            +4 PHRASE <Text>                {0:1}  [g7:PHRASE]()
    >         +3 <<PLACE_STRUCTURE>>             {0:1}
    >      +2 AGNC <Text>                        {0:1}  [g7:AGNC]()
    >      +2 <<NOTE_STRUCTURE>>                 {0:M}
    >   +1 AUTH <Text>                           {0:1}  [g7:AUTH]()
    >   +1 TITL <Text>                           {0:1}  [g7:TITL]()
    >   +1 ABBR <Text>                           {0:1}  [g7:ABBR]()
    >   +1 PUBL <Text>                           {0:1}  [g7:PUBL]()
    >   +1 TEXT <Text>                           {0:1}  [g7:TEXT]()
    >      +2 MIME <MediaType>                   {0:1}  [g7:MIME]()
    >      +2 LANG <Language>                    {0:1}  [g7:LANG]()
    >   +1 <<SOURCE_REPOSITORY_CITATION>>        {0:M}
    >   +1 <<IDENTIFIER_STRUCTURE>>              {0:M}
    >   +1 <<NOTE_STRUCTURE>>                    {0:M}
    >   +1 <<MULTIMEDIA_LINK>>                   {0:M}
    >   +1 <<CHANGE_DATE>>                       {0:1}
    >   +1 <<CREATION_DATE>>                     {0:1}
    """

    xref: SourceXref = Void.SOUR
    author: str = ''
    title: str = ''
    abbreviation: str = ''
    published: str = ''
    events: Any = None
    text: Any = None
    repositories: Any = None
    identifiers: Any = None
    notes: Any = None
    multimedia_links: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.xref, SourceXref)
            and Checker.verify_type(self.author, str)
            and Checker.verify_type(self.title, str)
            and Checker.verify_type(self.abbreviation, str)
            and Checker.verify_type(self.published, str)
            and Checker.verify_tuple_type(self.events, SourceEvent)
            and Checker.verify_tuple_type(self.text, Text)
            and Checker.verify_tuple_type(self.repositories, Repository)
            and Checker.verify_tuple_type(self.identifiers, Identifier)
            and Checker.verify_tuple_type(self.notes, Note)
            and Checker.verify_tuple_type(self.multimedia_links, MultimediaLink)
        )
        return check

    def ged(self, level: int = 0) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged()
        if self.validate():
            pass
        return lines


class Submitter(NamedTuple):
    """Store, validate and disply a GEDCOM Submitter Record.

    Reference:
        [GEDCOM record-SUBM](https://gedcom.io/terms/v7/record-SUBM)
        [GEDCOM specification](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SUBMITTER_RECORD)

    > n @XREF:SUBM@ SUBM                         {1:1}  [g7:record-SUBM](https://gedcom.io/terms/v7/record-SUBM)
    >   +1 NAME <Text>                           {1:1}  [g7:NAME](https://gedcom.io/terms/v7/NAME)
    >   +1 <<ADDRESS_STRUCTURE>>                 {0:1}
    >   +1 PHON <Special>                        {0:M}  [g7:PHON](https://gedcom.io/terms/v7/PHON)
    >   +1 EMAIL <Special>                       {0:M}  [g7:EMAIL](https://gedcom.io/terms/v7/EMAIL)
    >   +1 FAX <Special>                         {0:M}  [g7:FAX](https://gedcom.io/terms/v7/FAX)
    >   +1 WWW <Special>                         {0:M}  [g7:WWW](https://gedcom.io/terms/v7/WWW)
    >   +1 <<MULTIMEDIA_LINK>>                   {0:M}
    >   +1 LANG <Language>                       {0:M}  [g7:SUBM-LANG](https://gedcom.io/terms/v7/SUBM-LANG)
    >   +1 <<IDENTIFIER_STRUCTURE>>              {0:M}
    >   +1 <<NOTE_STRUCTURE>>                    {0:M}
    >   +1 <<CHANGE_DATE>>                       {0:1}
    >   +1 <<CREATION_DATE>>                     {0:1}
    """

    xref: SubmitterXref = Void.SUBM
    name: str = ''
    address: Address = Address([], '', '', '', '')
    phones: list[str] = []  # noqa: RUF012
    emails: list[str] = []  # noqa: RUF012
    faxes: list[str] = []  # noqa: RUF012
    wwws: list[str] = []  # noqa: RUF012
    multimedia_links: Any = None
    languages: Any = None
    identifiers: Any = None
    notes: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.xref, SubmitterXref)
            and Checker.verify_type(self.name, str)
            and Checker.verify_type(self.address, Address | None)
            and Checker.verify_tuple_type(self.phones, str)
            and Checker.verify_tuple_type(self.emails, str)
            and Checker.verify_tuple_type(self.faxes, str)
            and Checker.verify_tuple_type(self.wwws, str)
            and Checker.verify_tuple_type(self.multimedia_links, MultimediaLink)
            and Checker.verify_tuple_type(self.languages, str)
            and Checker.verify_tuple_type(self.identifiers, Identifier)
            and Checker.verify_tuple_type(self.notes, Note)
        )
        return check

    def ged(self, level: int = 0) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged()
        if str(self.xref) != Void.NAME and self.validate():
            pass
        return lines


class Individual(NamedTuple):
    """Store, validate and display the record-INDI GEDCOM structure.

    Examples:
        The GEDCOM specification offers the following example.

        > The following example refers to 2 individuals, `@I1@` and `@I2@`, where `@I2@`
        > is a godparent of `@I1@`:
        >
        > ```gedcom
        > 0 @I1@ INDI
        > 1 ASSO @I2@
        > 2 ROLE GODP
        > ```

        This can be implemented by doing the following.
        First import the packages.
        >>> from chronodata.build import Genealogy
        >>> from chronodata.store import Association, Individual
        >>> from chronodata.constants import Role

        Next instantiate a Genealogy which will store the information.
        This will be named `test`.
        >>> a = Genealogy('test')

        Next instantiate two IndivdiaulXref values called `I1` and `I2`.
        >>> i1 = a.individual_xref('I1')
        >>> i2 = a.individual_xref('I2')

        Add values to the Individual NamedTuple to store this information.
        >>> indi = Individual(
        ...     xref=i1,
        ...     associations=[
        ...         Association(
        ...             xref=i2,
        ...             role=Role.GODP,
        ...         ),
        ...     ],
        ... )

        At this point one could validate the information that is stored
        although this is not necessary since the validation occurs when
        one displays the data.  However, it is available for these
        structure.
        >>> indi.validate()
        True

        Next, we could display the data to verify that it is the same as
        the example shows.  Note that the data is the same although it
        is formatted as a single line with newlines.
        >>> indi.ged(0)
        '0 @I1@ INDI\\n1 ASSO @I2@\\n2 ROLE GODP\\n'

        Using `print` will format the result as in the example.  The additional
        blankline allows the final string to concatenate with additional data.
        >>> print(indi.ged(0))
        0 @I1@ INDI
        1 ASSO @I2@
        2 ROLE GODP
        <BLANKLINE>

        This example shows the kinds of errors that the validate method
        might produce by using a family xref for the individual xref.
        If one has doubts about the data one has loaded into a structure
        one can run its `validate` method to catch an error early on.
        >>> fam = a.family_xref('my family')
        >>> indi_error = Individual(xref=fam)
        >>> indi_error.validate()
        Traceback (most recent call last):
        TypeError: "@MY_FAMILY@" has type <class 'chronodata.store.FamilyXref'> but should have type <class 'chronodata.store.IndividualXref'>.

    Reference:
        [GEDCOM record-INDI](https://gedcom.io/terms/v7/record-INDI)
        [GEDCOM specification](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_RECORD)


    > n @XREF:INDI@ INDI                         {1:1}  [g7:record-INDI](https://gedcom.io/terms/v7/record-INDI)
    >   +1 RESN <List:Enum>                      {0:1}  [g7:RESN](https://gedcom.io/terms/v7/RESN)
    >   +1 <<PERSONAL_NAME_STRUCTURE>>           {0:M}
    >   +1 SEX <Enum>                            {0:1}  [g7:SEX](https://gedcom.io/terms/v7/SEX)
    >   +1 <<INDIVIDUAL_ATTRIBUTE_STRUCTURE>>    {0:M}
    >   +1 <<INDIVIDUAL_EVENT_STRUCTURE>>        {0:M}
    >   +1 <<NON_EVENT_STRUCTURE>>               {0:M}
    >   +1 <<LDS_INDIVIDUAL_ORDINANCE>>          {0:M}
    >   +1 FAMC @<XREF:FAM>@                     {0:M}  [g7:INDI-FAMC](https://gedcom.io/terms/v7/INDI-FAMC)
    >      +2 PEDI <Enum>                        {0:1}  [g7:PEDI](https://gedcom.io/terms/v7/PEDI)
    >         +3 PHRASE <Text>                   {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    >      +2 STAT <Enum>                        {0:1}  [g7:FAMC-STAT](https://gedcom.io/terms/v7/FAMC-STAT)
    >         +3 PHRASE <Text>                   {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    >      +2 <<NOTE_STRUCTURE>>                 {0:M}
    >   +1 FAMS @<XREF:FAM>@                     {0:M}  [g7:FAMS](https://gedcom.io/terms/v7/FAMS)
    >      +2 <<NOTE_STRUCTURE>>                 {0:M}
    >   +1 SUBM @<XREF:SUBM>@                    {0:M}  [g7:SUBM](https://gedcom.io/terms/v7/SUBM)
    >   +1 <<ASSOCIATION_STRUCTURE>>             {0:M}
    >   +1 ALIA @<XREF:INDI>@                    {0:M}  [g7:ALIA](https://gedcom.io/terms/v7/ALIA)
    >      +2 PHRASE <Text>                      {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    >   +1 ANCI @<XREF:SUBM>@                    {0:M}  [g7:ANCI](https://gedcom.io/terms/v7/ANCI)
    >   +1 DESI @<XREF:SUBM>@                    {0:M}  [g7:DESI](https://gedcom.io/terms/v7/DESI)
    >   +1 <<IDENTIFIER_STRUCTURE>>              {0:M}
    >   +1 <<NOTE_STRUCTURE>>                    {0:M}
    >   +1 <<SOURCE_CITATION>>                   {0:M}
    >   +1 <<MULTIMEDIA_LINK>>                   {0:M}
    >   +1 <<CHANGE_DATE>>                       {0:1}
    >   +1 <<CREATION_DATE>>                     {0:1}
    """

    xref: IndividualXref = Void.INDI
    resn: Resn = Resn.NONE
    personal_names: list[PersonalName] = []  # noqa: RUF012
    sex: Sex = Sex.NONE
    attributes: list[IndividualAttribute] = []  # noqa: RUF012
    events: list[IndividualEvent] = []  # noqa: RUF012
    lds_individual_ordinances: list[LDSIndividualOrdinance] = []  # noqa: RUF012
    families_child: list[FamilyChild] = []  # noqa: RUF012
    submitters: list[Submitter] = []  # noqa: RUF012
    associations: list[Association] = []  # noqa: RUF012
    aliases: list[Alias] = []  # noqa: RUF012
    ancestor_interest: list[Submitter] = []  # noqa: RUF012
    descendent_interest: list[Submitter] = []  # noqa: RUF012
    identifiers: list[Identifier] = []  # noqa: RUF012
    notes: list[Note] = []  # noqa: RUF012
    sources: list[Source] = []  # noqa: RUF012
    multimedia_links: list[MultimediaLink] = []  # noqa: RUF012
    extensions: list[Extension] = []  # noqa: RUF012

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.xref, IndividualXref)
            and Checker.verify_enum(self.resn.value, Resn)
            and Checker.verify_tuple_type(self.personal_names, PersonalName)
            and Checker.verify_enum(self.sex.value, Sex)
            and Checker.verify_tuple_type(self.attributes, IndividualAttribute)
            and Checker.verify_tuple_type(self.events, IndividualEvent)
            and Checker.verify_tuple_type(
                self.lds_individual_ordinances, LDSIndividualOrdinance
            )
            and Checker.verify_tuple_type(self.families_child, FamilyChild)
            and Checker.verify_tuple_type(self.submitters, str)
            and Checker.verify_tuple_type(self.associations, Association)
            and Checker.verify_tuple_type(self.aliases, Alias)
            and Checker.verify_tuple_type(self.ancestor_interest, str)
            and Checker.verify_tuple_type(self.descendent_interest, str)
            and Checker.verify_tuple_type(self.identifiers, Identifier)
            and Checker.verify_tuple_type(self.notes, Note)
            and Checker.verify_tuple_type(self.sources, Source)
            and Checker.verify_tuple_type(self.multimedia_links, MultimediaLink)
            and Checker.verify_tuple_type(self.extensions, Extension)
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged()
        if self.validate():
            lines = Tagger.string(lines, level + 1, Tag.RESN, self.resn.value)
            lines = Tagger.structure(lines, level + 1, self.personal_names)
            lines = Tagger.string(lines, level + 1, Tag.SEX, self.sex.value)
            lines = Tagger.structure(lines, level + 1, self.attributes)
            lines = Tagger.structure(lines, level + 1, self.events)
            lines = Tagger.structure(
                lines, level + 1, self.lds_individual_ordinances
            )
            lines = Tagger.structure(lines, level + 1, self.families_child)
            lines = Tagger.structure(lines, level + 1, self.submitters)
            lines = Tagger.structure(lines, level + 1, self.associations)
            lines = Tagger.structure(lines, level + 1, self.aliases)
            lines = Tagger.structure(lines, level + 1, self.ancestor_interest)
            lines = Tagger.structure(lines, level + 1, self.descendent_interest)
            lines = Tagger.structure(lines, level + 1, self.identifiers)
            lines = Tagger.structure(lines, level + 1, self.notes)
            lines = Tagger.structure(lines, level + 1, self.sources)
            lines = Tagger.structure(lines, level + 1, self.multimedia_links)
            lines = Tagger.structure(lines, level + 1, self.extensions)
        return lines

    def code(
        self,
        level: int = 0,
        chronology_name: str = 'chron',
        detail: str = String.MIN,
    ) -> str:
        spaces: str = String.INDENT * level
        preface: str = f"""
            # https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_RECORD
            from chronodata.build import Genealogy
            from chronodata.constants import Resn, Sex
            from chronodata.store import Individual

            {chronology_name} = Genealogy('{chronology_name}')
            {self.xref.code_xref} = {chronology_name}.individual_xref('{self.xref.name}')
            """
        return indent(
            dedent(f"""
            {preface if detail == String.MAX else ''}
            {self.xref.code} = Individual(
                xref = {self.xref.code_xref},
                resn = {self.resn},
                personal_names = {self.personal_names},
                sex = {self.sex},
                attributes = {self.attributes},
                events = {self.events},
                lds_individual_ordinances = {self.lds_individual_ordinances},
                submitters = {self.submitters},
                associations = {self.associations},
                aliases = {self.aliases},
                ancestor_interest = {self.ancestor_interest},
                descendent_interest = {self.descendent_interest},
                identifiers = {self.identifiers},
                notes = {self.notes},
                sources = {self.sources},
                multimedia_links = {self.multimedia_links}
            )
            """),
            spaces,
        )


class Repository(NamedTuple):
    """
    Reference:
        [GEDCOM Repository](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#REPOSITORY_RECORD)

    > n @XREF:REPO@ REPO                         {1:1}  [g7:record-REPO](https://gedcom.io/terms/v7/record-REPO)
    >   +1 NAME <Text>                           {1:1}  [g7:NAME](https://gedcom.io/terms/v7/NAME)
    >   +1 <<ADDRESS_STRUCTURE>>                 {0:1}
    >   +1 PHON <Special>                        {0:M}  [g7:PHON](https://gedcom.io/terms/v7/PHON)
    >   +1 EMAIL <Special>                       {0:M}  [g7:EMAIL](https://gedcom.io/terms/v7/EMAIL)
    >   +1 FAX <Special>                         {0:M}  [g7:FAX](https://gedcom.io/terms/v7/FAX)
    >   +1 WWW <Special>                         {0:M}  [g7:WWW](https://gedcom.io/terms/v7/WWW)
    >   +1 <<NOTE_STRUCTURE>>                    {0:M}
    >   +1 <<IDENTIFIER_STRUCTURE>>              {0:M}
    >   +1 <<CHANGE_DATE>>                       {0:1}
    >   +1 <<CREATION_DATE>>                     {0:1}
    """

    xref: RepositoryXref = Void.REPO
    name: str = ''
    address: Address = Address([], '', '', '', '')
    phones: list[str] = []  # noqa: RUF012
    emails: list[str] = []  # noqa: RUF012
    faxes: list[str] = []  # noqa: RUF012
    wwws: list[str] = []  # noqa: RUF012
    notes: Any = None
    identifiers: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.xref, RepositoryXref)
            and Checker.verify_type(self.name, str)
            and Checker.verify_type(self.address, Address | None)
            and Checker.verify_tuple_type(self.emails, str)
            and Checker.verify_tuple_type(self.faxes, str)
            and Checker.verify_tuple_type(self.wwws, str)
            and Checker.verify_tuple_type(self.notes, Note)
            and Checker.verify_tuple_type(self.identifiers, Identifier)
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged()
        if self.validate():
            lines = Tagger.structure(lines, level, self.address)
            lines = Tagger.string(lines, level, Tag.PHON, self.phones)
            lines = Tagger.string(lines, level, Tag.EMAIL, self.emails)
            lines = Tagger.string(lines, level, Tag.FAX, self.faxes)
            lines = Tagger.string(lines, level, Tag.WWW, self.wwws)
        return lines


class SharedNote(NamedTuple):
    xref: SharedNoteXref = Void.SNOTE
    text: str = ''
    mime: MediaType = MediaType.NONE
    language: str = String.UNDETERMINED
    translations: Any = None
    sources: Any = None
    identifiers: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.xref, SharedNoteXref)
            and Checker.verify_type(self.text, str)
            and Checker.verify_enum(self.mime.value, MediaType)
            and Checker.verify_type(self.language, str)
            and Checker.verify_tuple_type(self.translations, NoteTranslation)
            and Checker.verify_tuple_type(self.sources, Source)
            and Checker.verify_tuple_type(self.identifiers, Identifier)
        )
        return check

    def ged(self, level: int = 0) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged()
        if self.validate():
            pass
        return lines


class Header(NamedTuple):
    """Hold data for the GEDCOM header special record.

    Reference
    ---------
    - [GEDCOM Header](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#HEADER)

    >n HEAD                                     {1:1}  [g7:HEAD](https://gedcom.io/terms/v7/HEAD)
    >  +1 GEDC                                  {1:1}  [g7:GEDC](https://gedcom.io/terms/v7/GEDC)
    >     +2 VERS <Special>                     {1:1}  [g7:GEDC-VERS](https://gedcom.io/terms/v7/GEDC-VERS)
    >  +1 SCHMA                                 {0:1}  [g7:SCHMA](https://gedcom.io/terms/v7/SCHMA)
    >     +2 TAG <Special>                      {0:M}  [g7:TAG](https://gedcom.io/terms/v7/TAG)
    >  +1 SOUR <Special>                        {0:1}  [g7:HEAD-SOUR](https://gedcom.io/terms/v7/HEAD-SOUR)
    >     +2 VERS <Special>                     {0:1}  [g7:VERS](https://gedcom.io/terms/v7/VERS)
    >     +2 NAME <Text>                        {0:1}  [g7:NAME](https://gedcom.io/terms/v7/NAME)
    >     +2 CORP <Text>                        {0:1}  [g7:CORP](https://gedcom.io/terms/v7/CORP)
    >        +3 <<ADDRESS_STRUCTURE>>           {0:1}
    >        +3 PHON <Special>                  {0:M}  [g7:PHON](https://gedcom.io/terms/v7/PHON)
    >        +3 EMAIL <Special>                 {0:M}  [g7:EMAIL](https://gedcom.io/terms/v7/EMAIL)
    >        +3 FAX <Special>                   {0:M}  [g7:FAX](https://gedcom.io/terms/v7/FAX)
    >        +3 WWW <Special>                   {0:M}  [g7:WWW](https://gedcom.io/terms/v7/WWW)
    >     +2 DATA <Text>                        {0:1}  [g7:HEAD-SOUR-DATA](https://gedcom.io/terms/v7/HEAD-SOUR-DATA)
    >        +3 DATE <DateExact>                {0:1}  [g7:DATE-exact](https://gedcom.io/terms/v7/DATE-exact)
    >           +4 TIME <Time>                  {0:1}  [g7:TIME](https://gedcom.io/terms/v7/TIME)
    >        +3 COPR <Text>                     {0:1}  [g7:COPR](https://gedcom.io/terms/v7/COPR)
    >  +1 DEST <Special>                        {0:1}  [g7:DEST](https://gedcom.io/terms/v7/DEST)
    >  +1 DATE <DateExact>                      {0:1}  [g7:HEAD-DATE](https://gedcom.io/terms/v7/HEAD-DATE)
    >     +2 TIME <Time>                        {0:1}  [g7:TIME](https://gedcom.io/terms/v7/TIME)
    >  +1 SUBM @<XREF:SUBM>@                    {0:1}  [g7:SUBM](https://gedcom.io/terms/v7/SUBM)
    >  +1 COPR <Text>                           {0:1}  [g7:COPR](https://gedcom.io/terms/v7/COPR)
    >  +1 LANG <Language>                       {0:1}  [g7:HEAD-LANG](https://gedcom.io/terms/v7/LANG)
    >  +1 PLAC                                  {0:1}  [g7:HEAD-PLAC](https://gedcom.io/terms/v7/PLAC)
    >     +2 FORM <List:Text>                   {1:1}  [g7:HEAD-PLAC-FORM](https://gedcom.io/terms/v7/PLAC-FORM)
    >  +1 <<NOTE_STRUCTURE>>                    {0:1}
    """

    schema_tags: list[Schema] = []  # noqa: RUF012
    source: str = String.EMPTY
    vers: str = String.EMPTY
    name: str = String.EMPTY
    corporation: str = String.EMPTY
    address: Address = Address()
    phones: list[str] = []  # noqa: RUF012
    emails: list[str] = []  # noqa: RUF012
    faxes: list[str] = []  # noqa: RUF012
    wwws: list[str] = []  # noqa: RUF012
    data: str = String.EMPTY
    data_date: Date = Date()
    data_time: Time = Time()
    data_copyright: str = String.EMPTY
    dest: str = String.EMPTY
    header_date: Date = Date()
    header_time: Time = Time()
    submitter: SubmitterXref = Void.SUBM
    subm_copyright: str = String.EMPTY
    language: str = String.EMPTY
    # place: PlaceName = PlaceName()
    note: Note = Note()

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_tuple_type(self.schema_tags, Schema)
            and Checker.verify_type(self.source, str)
            and Checker.verify_type(self.vers, str)
            and Checker.verify_type(self.name, str)
            and Checker.verify_type(self.corporation, str)
            and Checker.verify_type(self.address, Address)
            and Checker.verify_tuple_type(self.phones, str)
            and Checker.verify_tuple_type(self.emails, str)
            and Checker.verify_tuple_type(self.faxes, str)
            and Checker.verify_tuple_type(self.wwws, str)
            and Checker.verify_type(self.data, str)
            and Checker.verify_type(self.data_date, Date)
            and Checker.verify_type(self.data_time, Time)
            and Checker.verify_type(self.data_copyright, str)
            and Checker.verify_type(self.dest, str)
            and Checker.verify_type(self.header_date, Date)
            and Checker.verify_type(self.header_time, Time)
            and Checker.verify_type(self.submitter, SubmitterXref)
            and Checker.verify_type(self.subm_copyright, str)
            and Checker.verify_type(self.language, str)
            # and Checker.verify_type(self.place, PlaceName)
            and Checker.verify_type(self.note, Note)
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.empty(lines, level, Tag.HEAD)
            lines = Tagger.empty(lines, level + 1, Tag.GEDC)
            lines = Tagger.string(lines, level + 2, Tag.VERS, String.VERSION)
            if len(self.schema_tags) > 0:
                lines = Tagger.empty(lines, level + 1, Tag.SCHMA)
                lines = Tagger.structure(lines, level + 1, self.schema_tags)
            lines = Tagger.structure(lines, level, self.address)
            lines = Tagger.string(lines, level, Tag.PHON, self.phones)
            lines = Tagger.string(lines, level, Tag.EMAIL, self.emails)
            lines = Tagger.string(lines, level, Tag.FAX, self.faxes)
            lines = Tagger.string(lines, level, Tag.WWW, self.wwws)
            if self.data != String.EMPTY:
                lines = Tagger.string(lines, level + 2, Tag.DATA, self.data)
                lines = Tagger.structure(
                    lines, level + 3, self.data_date, Date()
                )
                lines = Tagger.structure(
                    lines, level + 4, self.data_time, Time()
                )
                lines = Tagger.string(
                    lines, level + 3, Tag.COPR, self.data_copyright
                )
            lines = Tagger.string(lines, level, Tag.DEST, self.dest)
            lines = Tagger.structure(lines, level, self.header_date, Date())
            lines = Tagger.structure(lines, level + 1, self.header_time, Time())
            if self.submitter != Void.SUBM:
                lines = Tagger.string(
                    lines, level + 1, Tag.SUBM, self.submitter.fullname
                )
            lines = Tagger.string(
                lines, level + 1, Tag.COPR, self.subm_copyright
            )
            lines = Tagger.string(lines, level, Tag.LANG, self.language)
            # lines = Tagger.structure(lines, level, self.place, PlaceName())
            lines = Tagger.structure(lines, level, self.note)
        return lines
