# genedata/tuples.py
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
    'WWW',
    'AddrType',
    'Address',
    'Age',
    'Alias',
    'AssoType',
    'Association',
    'CallNumber',
    'CalnType',
    'ChangeDate',
    'ChangeDateType',
    'Checker',
    'ChilType',
    'Child',
    'CreationDate',
    'CreationDateType',
    'Date',
    'DateType',
    'DateValue',
    'DateValueType',
    'Dater',
    'Email',
    'EmailType',
    'EventDetail',
    'Exid',
    'ExidType',
    'ExtTag',
    'FamAttrType',
    'FamEvenDetailType',
    'FamEvenType',
    'FamcType',
    'Family',
    'FamilyAttribute',
    'FamilyChild',
    'FamilyEvent',
    'FamilyEventDetail',
    'FamilySpouse',
    'FamilyXref',
    'FamsType',
    'Fax',
    'FaxType',
    'File',
    'FileTranType',
    'FileTranslation',
    'FileType',
    'Formatter',
    'Header',
    'Identifier',
    'IndiAttrType',
    'IndiEvenType',
    'Individual',
    'IndividualAttribute',
    'IndividualEvent',
    'IndividualEventDetail',
    'IndividualXref',
    'LDSIndividualOrdinance',
    'LDSOrdinanceDetail',
    'LDSSpouseSealing',
    'Lang',
    'LangType',
    'MMLinkType',
    'Map',
    'MapType',
    'Multimedia',
    'MultimediaLink',
    'MultimediaXref',
    'NameTranslation',
    'NoType',
    'NonEvent',
    'Note',
    'NoteTranType',
    'NoteTranslation',
    'PersonalName',
    'PersonalNamePieces',
    'PersonalNamePiecesType',
    'PersonalNameType',
    'Phone',
    'PhoneType',
    'Phrase',
    'PhraseType',
    'PlacTranType',
    'PlacType',
    'Place',
    'PlaceTranslation',
    'Placer',
    'Repository',
    'Repository',
    'RepositoryXref',
    'SharedNote',
    'SharedNoteXref',
    'Source',
    'SourceCitation',
    'SourceData',
    'SourceDataEvent',
    'SourceRepositoryCitation',
    'SourceXref',
    'Submitter',
    'Submitter',
    'SubmitterXref',
    'Tagger',
    'Text',
    'Time',
    'Void',
    'WWWType',
]


import contextlib
import logging
import math
import re
import urllib.request
from enum import Enum
from textwrap import indent
from typing import Any, ClassVar, Literal, NamedTuple

import numpy as np
import yaml  # type: ignore[import-untyped]

from calendars.calendars import CalendarDefinition

# from calendars.french_revolution_calendars import CalendarsFrenchRevolution
from calendars.gregorian_calendars import CalendarsGregorian

# from calendars.hebraic_calendars import CalendarsHebraic
# from calendars.julian_calendars import CalendarsJulian
from genedata.constants import (
    # Adop,
    Cal,
    CalendarName,
    Default,
    GreaterLessThan,
    MediaType,
    String,
)
from genedata.gedcom import (
    Adop,
    Docs,
    Even,
    EvenAttr,
    FamAttr,
    FamEven,
    Id,
    IndiAttr,
    IndiEven,
    Medium,
    NameType,
    Quay,
    Resn,
    Role,
    Sex,
    Specs,
    Stat,
    Tag,
)
from genedata.messages import Example, Msg

YNull = Literal['Y'] | None
StrList = str | list[str] | None


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
            >>> from genedata.gedcom import Tag
            >>> from genedata.store import Tagger
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
            >>> from genedata.store import Note
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
            >>> from genedata.store import Tagger
            >>> from genedata.gedcom import Tag
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
        payload: list[str] | str | None,
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
            >>> from genedata.store import Tagger
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

        if payload is None:
            return lines
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
            >>> from genedata.store import Map, Tagger
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

        if payload is None:
            return lines
        if isinstance(payload, list):
            for item in payload:
                if flag != String.EMPTY:
                    lines = ''.join([lines, item.ged(level, flag)])
                else:
                    lines = ''.join([lines, item.ged(level)])
            return lines
        if payload != default:
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
            >>> from genedata.store import Checker
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
    def verify_ext(tag: Tag, extensions: Any) -> bool:
        check: bool = True
        if extensions is None:
            return check
        if isinstance(extensions, list):
            for extension in extensions:
                if (
                    len(extension.schema.supers) > 0
                    and tag.value not in extension.schema.supers
                ):
                    check = False
                    raise ValueError(
                        Msg.NOT_DEFINED_FOR_STRUCTURE.format(extension)
                    )
            return check
        if (
            len(extension.schema.supers) > 0
            and tag.value not in extension.schema.supers
        ):
            check = False
            raise ValueError(Msg.NOT_DEFINED_FOR_STRUCTURE.format(extension))
        return check

    @staticmethod
    def verify_type(value: Any, value_type: Any, validate: bool = True) -> bool:
        """Check if the value has the specified type."""
        check: bool = True
        if value is None:
            return check
        if isinstance(value, list):
            for item in value:
                if not isinstance(item, value_type):
                    raise TypeError(
                        Msg.WRONG_TYPE.format(item, type(item), value_type)
                    )
                if not isinstance(item, int | float | str | Enum) and validate:
                    with contextlib.suppress(Exception):
                        check = item.validate()
            return check
        if not isinstance(value, value_type):
            raise TypeError(
                Msg.WRONG_TYPE.format(value, type(value), value_type)
            )
        if not isinstance(value, int | float | str | Enum) and validate:
            with contextlib.suppress(Exception):
                check = value.validate()
        return check

    @staticmethod
    def verify_tuple_type(name: Any, value_type: Any) -> bool:
        """Check if each member of the tuple has the specified type."""
        if name != [] and name is not None:
            for value in name:
                Checker.verify_type(value, value_type)
        return True

    @staticmethod
    def verify_enum(tag: Any, enumeration: Any) -> bool:
        """Check if the value is in the proper enumation."""
        if not isinstance(tag, Tag) and not isinstance(tag, ExtTag):
            raise ValueError(Msg.NEITHER_TAG_NOR_EXTTAG.format(str(tag)))
        if isinstance(tag, Tag) and tag.value not in enumeration:
            raise ValueError(Msg.NOT_VALID_ENUM.format(tag.value, enumeration))
        if isinstance(tag, ExtTag):
            return True
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
            >>> from genedata.store import Checker
            >>> Checker.verify_not_default('', '')
            Traceback (most recent call last):
            ValueError: GEDCOM requires a specific value different from the default "".

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
            raise ValueError(Msg.NOT_DEFAULT.format(default))
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
    def format(
        year: int,
        month: int = 0,
        day: int = 0,
        calendar: CalendarDefinition = CalendarsGregorian.GREGORIAN,
    ) -> str:
        formatted: str = str(year)
        if year < 0:
            formatted = ''.join([str(-year), String.SPACE, calendar.epoch_name])
        if month > 0:
            formatted = ''.join(
                [calendar.months[month].abbreviation, String.SPACE, formatted]
            )
        if day > 0:
            formatted = ''.join([str(day), String.SPACE, formatted])
        return formatted

    @staticmethod
    def ged_date(
        iso_date: str = String.NOW,
        calendar: CalendarName = CalendarName.GREGORIAN,
        epoch: bool = True,
    ) -> tuple[str, str]:
        """Obtain the GEDCOM date and time from an ISO 8601 date and time for the
        current UTC timestamp in GEDCOM format.

        Examples:
            The ISO date for January 1, 2000 at 1:15:30 AM would be `20000101 01:15:30`.
            >>> from genedata.store import Dater
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
        good_calendar: str | bool = Cal.CALENDARS.get(calendar, False)
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
        >>> from genedata.store import Dater  # doctest: +ELLIPSIS
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
            >>> from genedata.store import Placer
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

        >>> from genedata.store import Placer
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
    def phone(area: int, prefix: int, line: int, country: int = 1) -> str:
        """Format a phone string to meet the GEDCOM standard.

        The International Notation from the ITU-T E.123 standard
        are followed.  Spaces are used between the country, area_code and local numbers.
        A `+` precedes the country code.

        The GEDCOM standard does not require this international notation, but recommends it.
        This method formats for the optional international notation should the user
        choose have a method format the number in a uniform manner.

        One may use this for fax numbers as well.

        Examples:
            The first example shows the use of the default, US, international number.
            >>> from genedata.store import Formatter
            >>> Formatter.phone(123, 456, 7890)
            '+1 123 456 7890'

            The second example provides a non-US country number.
            >>> Formatter.phone(123, 456, 7890, 44)
            '+44 123 456 7890'

        Args:
            area: The area code for the phone number.
            prefix: The prefix portion of the phone number.
            line: The local number for the phone number.
            country: The country code with default 1 for United States.

        Reference:
            [GEDCOM Standard](https://gedcom.io/terms/v7/PHON)
            [ITU-T E.123 Standard](https://www.itu.int/rec/T-REC-E.123-200102-I/en)
        """
        return f'+{country!s} {area!s} {prefix!s} {line!s}'

    @staticmethod
    def codes(items: Any, tabs: int = 1) -> str:
        if items is None:
            return 'None'
        if isinstance(items, list):
            if len(items) == 0:
                return String.LEFT_RIGHT_BRACKET
            lines: str = String.LEFT_BRACKET
            for item in items:
                lines = ''.join([lines, item.code(tabs), String.COMMA])
            return ''.join(
                [
                    lines,
                    String.EOL,
                    String.INDENT * (tabs - 1),
                    String.RIGHT_BRACKET,
                ]
            )
        if isinstance(items, str | int | float | Enum | Xref):
            return f'{items!r}'
        code_lines: str = (
            items.code(tabs)
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
    ) -> None:
        print(  # noqa: T201
            ''.join(
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
        )

    @staticmethod
    def schema_example(
        code_preface: str,
        show_code: str,
        gedcom_preface: str,
        show_ged: str,
        superstructures: dict[str, str],
        substructures: dict[str, str],
        gedcom_docs: str,
        genealogy_docs: str,
    ) -> None:
        superstructs: str = String.EMPTY
        substructs: str = String.EMPTY
        key: str
        value: str
        for key, value in superstructures.items():
            superstructs = ''.join(
                [
                    superstructs,
                    String.EOL,
                    f'{String.INDENT}{key:<40} {value:<6}',
                ]
            )
        for key, value in substructures.items():
            substructs = ''.join(
                [substructs, String.EOL, f'{String.INDENT}{key:<40} {value:<6}']
            )
        print(  # noqa: T201
            ''.join(
                [
                    code_preface,
                    String.EOL,
                    show_code,
                    String.DOUBLE_NEWLINE,
                    gedcom_preface,
                    String.DOUBLE_NEWLINE,
                    show_ged,
                    String.EOL,
                    Example.SUPERSTRUCTURES,
                    superstructs,
                    Example.SUBSTRUCTURES,
                    substructs,
                    Example.GEDCOM_SPECIFICATION,
                    gedcom_docs,
                    String.EOL,
                    genealogy_docs,
                ]
            )
        )


class Xref:
    def __init__(self, name: str, tag: Tag = Tag.NONE):
        """Initialize an instance of the class.

        Args:
        - `name`: The name of the identifier.
        """
        self.fullname: str = name.upper()
        self.name: str = name.replace('@', '').replace('_', ' ')
        self.tag: Tag = tag
        self.code_xref = f'{self.tag.value.lower()}_{self.name.lower()}_xref'

    def __str__(self) -> str:
        """Return the name used by the GEDCOM standard."""
        return self.fullname

    def __repr__(self) -> str:
        return f"Xref('{self.fullname}')"

    def ged(self, info: str = String.EMPTY) -> str:
        """Return the identifier formatted according to the GEDCOM standard."""
        if info == String.EMPTY:
            return f'0 {self.fullname} {self.tag.value}{String.EOL}'
        return f'0 {self.fullname} {self.tag.value} {info}{String.EOL}'

    def code(self, tabs: int = 0) -> str:  # noqa: ARG002
        return self.fullname


class FamilyXref(Xref):
    """Assign the FamilyXref type to a string.

    This class is not instantiated directly, but only through
    the `genedata.build.family_xref()` method.

    Args:
        name: The name of the identifier.

    See Also:
        genedata.build.family_xref()
    """

    def __init__(self, name: str, tag: Tag = Tag.FAM):
        super().__init__(name, tag)

    def __repr__(self) -> str:
        return f"FamilyXref('{self.fullname}')"


class IndividualXref(Xref):
    """Assign the IndividualXref type to a string.

    This class is not instantiated directly, but only through
    the `genedata.build.individual_xref()` method.

    Args:
        name: The name of the identifier.

    See Also:
        `genedata.build.individual_xref()`

    Reference:
        [GEDCOM INDIVIDUAL Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_RECORD)
    """

    def __init__(self, name: str, tag: Tag = Tag.INDI):
        super().__init__(name, tag)

    def __repr__(self) -> str:
        return f"IndividualXref('{self.fullname}')"


class MultimediaXref(Xref):
    """Assign Assign the MultimediaXref type to a string.

    This class is not instantiated directly, but only through
    the `genedata.build.multimedia_xref()` method.

    Args:
        name: The name of the identifier.

    See Also:
        `genedata.build.multimedia_xref()`

    Reference:
        [GEDCOM MULTIMEDIA Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#MULTIMEDIA_RECORD)
    """

    def __init__(self, name: str, tag: Tag = Tag.OBJE):
        super().__init__(name, tag)

    def __repr__(self) -> str:
        return f"MultimediaXref('{self.fullname}')"


class RepositoryXref(Xref):
    """Assign the RepositoryXref type to a string.

    This class is not instantiated directly, but only through
    the `genedata.build.repository_xref()` method.

    Args:
        name: The name of the identifier.

    See Also:
        `genedata.build.repository_xref()`

    Reference:
        https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#REPOSITORY_RECORD
    """

    def __init__(self, name: str, tag: Tag = Tag.REPO):
        super().__init__(name, tag)

    def __repr__(self) -> str:
        return f"RepositoryXref('{self.fullname}')"


class SharedNoteXref(Xref):
    """Assign the SharedNoteXref type to a string.

    This class is not instantiated directly, but only through
    the `genedata.build.shared_note_xref()` method.

    Args:
        name: The name of the identifier.

    See Also:
        `genedata.build.shared_note_xref()`

    Reference:
        - [GEDCOM SHARED_NOTE Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SHARED_NOTE_RECORD)
    """

    def __init__(self, name: str, tag: Tag = Tag.SNOTE):
        super().__init__(name, tag)

    def __repr__(self) -> str:
        return f"SharedNoteXref('{self.fullname}')"


class SourceXref(Xref):
    """Assign the SourceXref type to a string.

    This class is not instantiated directly, but only through
    the `genedata.build.source_xref()` method.

    Args:
        name: The name of the identifier.

    See Also:
        `genedata.build.source_xref()`

    Reference:
        [GEDCOM SOURCE Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SHARED_NOTE_RECORD)
    """

    def __init__(self, name: str, tag: Tag = Tag.SOUR):
        super().__init__(name, tag)

    def __repr__(self) -> str:
        return f"SourceXref('{self.fullname}')"


class SubmitterXref(Xref):
    """Assign the SubmitterXref type to a string.

    This class is not instantiated directly, but only through
    the `genedata.build.submitter_xref()` method.

    Args:
        name: The name of the identifier.

    See Also:
        genedata.build.submitter_xref()

    Reference:
        [GEDCOM SUBMITTER Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SUBMITTER_RECORD)
    """

    def __init__(self, name: str, tag: Tag = Tag.SUBM):
        super().__init__(name, tag)

    def __repr__(self) -> str:
        return f"SubmitterXref('{self.fullname}')"


class Void:
    NAME: str = '@VOID@'
    FAM: FamilyXref = FamilyXref(NAME)
    INDI: IndividualXref = IndividualXref(NAME)
    OBJE: MultimediaXref = MultimediaXref(NAME)
    REPO: RepositoryXref = RepositoryXref(NAME)
    SNOTE: SharedNoteXref = SharedNoteXref(NAME)
    SOUR: SourceXref = SourceXref(NAME)
    SUBM: SubmitterXref = SubmitterXref(NAME)


class Structure:
    """A base class for the GEDCOM structure classes to define dunder methods."""

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return self.ged()

    def __repr__(self) -> str:
        return (
            self.code()
            .replace(String.EOL, String.EMPTY)
            .replace(String.INDENT, String.SPACE)
            .replace('( ', '(')
            .replace(',)', ')')
        )

    def __eq__(self, other: Any) -> bool:
        check: bool = isinstance(other, Structure) and self.ged() == other.ged()
        return check

    def ged(self) -> str:
        return String.EMPTY

    def code(self) -> str:
        return String.EMPTY

    def example(self) -> None:
        print(String.EMPTY)  # noqa: T201


class ExtTag(Structure):
    """Store, validate and display extension tag information.

    An underline is added to the front of the new tag if one is not there already.
    Also the tag to made upper case.

    This class holds multiple extension tags for the header record.  It is not a separate
    GEDCOM structure.

    Examples:
        Consider making a _DATE extention tag based on the GEDCOM specification for
        the standard DATE tag.
        >>> from genedata.store import ExtTag
        >>> date = ExtTag('date', 'https://gedcom.io/terms/v7/DATE')
        >>> print(date.ged(1))
        2 TAG _DATE https://gedcom.io/terms/v7/DATE
        <BLANKLINE>

        We can put this into the header record as an extension tag as follows.
        >>> from genedata.store import Header
        >>> header = Header(exttags=[date])
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

    structure: ClassVar[str] = Tag.SCHMA.value

    def __init__(self, tag: str, url: str) -> None:
        self.raw_tag: str = tag
        self.url: str = url
        self.tag: str = self.raw_tag.upper()
        if self.tag[0] != String.UNDERLINE:
            self.tag = ''.join([String.UNDERLINE, self.raw_tag.upper()])
        self.webUrl = urllib.request.urlopen(self.url)
        self.result_code = str(self.webUrl.getcode())
        raw: str = self.webUrl.read().decode('utf-8')
        raw2: str = raw[raw.find('%YAML') :]
        self.yaml: str = raw2[: raw2.find('...')]
        self.yamldict: dict[str, Any] = yaml.safe_load(self.yaml)
        self.lang: str = self.yamldict['lang']
        self.type: str = self.yamldict['type']
        self.uri: str = self.yamldict['uri']
        self.label: str = self.yamldict['label']
        self.payload: str = self.yamldict['payload']
        self.specification: str = self.yamldict['specification']
        self.contact: str = self.yamldict['contact']
        self.value_of: list[str] = []
        with contextlib.suppress(Exception):
            self.value_of = self.yamldict['value of']
        self.substructures: dict[str, str] = self.yamldict['substructures']
        self.superstructures: dict[str, str] = self.yamldict['superstructures']
        self.supers: set[str] = {
            s[s.rfind('/') + 1 :] for s in self.superstructures
        }

    def validate(self) -> bool:
        check: bool = True
        for char in self.tag:
            if not (char.isalnum() or char == '_'):
                raise ValueError(Msg.SCHEMA_NAME.format(self.tag, char))
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = String.EMPTY
        if self.validate():
            ext_tag: str = self.tag.upper()
            if ext_tag[0] != String.UNDERLINE:
                ext_tag = ''.join([String.UNDERLINE, ext_tag])
            lines = Tagger.string(
                lines, level + 1, Tag.TAG, ext_tag, str(self.url)
            )
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
ExtTag(
    tag = {Formatter.codes(self.tag, tabs)},
    url = {Formatter.codes(self.url, tabs)},
)""",
            String.INDENT * tabs,
        )

    def show(self) -> None:
        print(self.yamldict)  # noqa: T201

    def example(
        self,
        choice: int = Default.CHOICE,
        tag: str = Default.EMPTY,
        url: str = Default.EMPTY,
    ) -> None:
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
        show: ExtTag
        gedcom_docs: str = Specs.SCHEMA
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = ExtTag(
                    tag='_DATE',
                    url='https://gedcom.io/terms/v7/DATE',
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = ExtTag(
                    tag='_DATE',
                    url='',
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = ExtTag(
                    tag='_DATE',
                    url='',
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = ExtTag(tag=tag, url=url)
                code_preface = Example.EMPTY_CODE
                gedcom_preface = Example.EMPTY_GEDCOM
        return Formatter.schema_example(
            code_preface,
            show.code(),
            gedcom_preface,
            show.ged(),
            self.superstructures,
            self.substructures,
            gedcom_docs,
            genealogy_docs,
        )


ExtTagType = ExtTag | list[ExtTag] | None


class Extension(NamedTuple):
    """Store, validate and display extension tags.

    Reference:
        [GedCOM Extensions](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#extensions)
    """

    level: int
    exttag: ExtTag
    payload: str = String.EMPTY
    extra: str = String.EMPTY
    substructures: list[Any] | None = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.level, int)
            and Checker.verify_type(self.exttag, ExtTag)
            and Checker.verify_type(self.payload, str)
            and Checker.verify_type(self.extra, str)
            and Checker.verify_type(self.substructures, Any)
        )
        return check

    def ged(self, level: int = 1) -> str:
        lines: str = ''
        if self.validate():
            lines = Tagger.extension(
                lines,
                level,
                ''.join([String.UNDERLINE, self.exttag.tag.upper()]),
                self.payload,
                self.extra,
            )
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
Extension(
    level = {Formatter.codes(self.level, tabs)},
    exttag = {Formatter.codes(self.exttag, tabs)},
    payload = {Formatter.codes(self.payload, tabs)},
    extra = {Formatter.codes(self.extra, tabs)},
    substructures = {Formatter.codes(self.substructures, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        level: int = 1,
        exttag: ExtTag | None = None,
        payload: str = Default.EMPTY,
        extra: str = Default.EMPTY,
        substructures: list[Any] | None = None,
    ) -> None:
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
        show: Extension
        gedcom_docs: str = Specs.EXTENSION
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = Extension(
                    level=1,
                    exttag=ExtTag(tag='_DATE', url=''),
                    payload='',
                    extra='',
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Extension(
                    level=1,
                    exttag=ExtTag(tag='_DATE', url=''),
                    payload='',
                    extra='',
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Extension(
                    level=1,
                    exttag=ExtTag(tag='_DATE', url=''),
                    payload='',
                    extra='',
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                if exttag is None:
                    exttag = ExtTag(Default.EMPTY, Default.EMPTY)
                show = Extension(
                    level=level,
                    exttag=exttag,
                    payload=payload,
                    extra=extra,
                    substructures=substructures,
                )
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


ExtType = Extension | list[Extension] | None


class Date(NamedTuple):
    """Validate and display date data in various formats.

    Dates are entered based on a Gregorian calendar. This calendar
    does not have a 0 year.  The year 1 BC is entered as `-1`.

    A default value of `0` for any date component means that the component
    will not be displayed.

    The GEDCOM standard allows a week without specifying the other components.

    Arg:
        year: A numerical value representing the year.  It is the only required parameter.
        month: An optional numerical value representing the month.  It will be converted to a string
            value for the month.
        day: An optional numerical value representing the day.
        calendar: An optional tag representing the calendar system. There are four standard calendars:
            Tag.GREGORIAN, Tag.JULIAN, Tag.FRENCH_R (French Revolution) and Tag.HEBREW.  If no calendar
            is listed the default for calculating the month will be the Gregorian calendar.  If a
            calendar is present, it will be displayed as part of the date.


    Examples:

    Reference:
        [GEDCOM DATE](https://gedcom.io/terms/v7/DATE)
        [GEDCOM DATE type](https://gedcom.io/terms/v7/type-Date)
    """

    year: int = Default.DATE_YEAR
    month: int = Default.DATE_MONTH
    day: int = Default.DATE_DAY
    calendar: CalendarDefinition = CalendarsGregorian.GREGORIAN
    iso: str = Default.EMPTY
    display_calendar: bool = False
    date_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.year, int)
            and Checker.verify_type(self.month, int)
            and Checker.verify_type(self.day, int)
            and Checker.verify_range(self.month, 0, 13)
            and Checker.verify_type(self.calendar, CalendarDefinition)
            and Checker.verify_type(self.display_calendar, bool)
            and Checker.verify_type(self.iso, str)
            and self.calendar.validate(
                self.year, self.month, self.day, self.iso
            )
            and Checker.verify_ext(Tag.DATE, self.date_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        lines: str = String.EMPTY
        formatted_date: str = Dater.format(
            self.year, self.month, self.day, self.calendar
        )
        formatted_calendar_date: str = formatted_date
        if self.display_calendar:
            formatted_calendar_date = ''.join(
                [self.calendar.name, String.EMPTY, formatted_date]
            )
        lines = Tagger.string(lines, level, Tag.DATE, formatted_calendar_date)
        return Tagger.structure(lines, level + 1, self.date_ext)

    def from_iso(self) -> str:
        """Return the validated ISO format for the date.

        References
        ----------
        - [ISO 8601 Standard](https://www.iso.org/iso-8601-date-and-time-format.html)
        - [Wikipedia Overview](https://en.wikipedia.org/wiki/ISO_8601)
        """
        if self.validate():
            return f'{self.year}-{self.month}-{self.day}'
        return ''

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
Date(
    year = {Formatter.codes(self.year, tabs)},
    month = {Formatter.codes(self.month, tabs)},
    day = {Formatter.codes(self.day, tabs)},
    calendar = {Formatter.codes(self.calendar, tabs)},
    date_ext = {Formatter.codes(self.date_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        year: int = 0,
        month: int = 0,
        day: int = 0,
        calendar: CalendarDefinition = CalendarsGregorian.GREGORIAN,
        iso: str = Default.EMPTY,
        display_calendar: bool = False,
        date_ext: ExtType = None,
    ) -> None:
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
                    calendar=CalendarsGregorian.GREGORIAN,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Date(
                    year=2024,
                    month=10,
                    day=10,
                    calendar=CalendarsGregorian.GREGORIAN,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Date(
                    year=2024,
                    month=10,
                    day=10,
                    calendar=CalendarsGregorian.GREGORIAN,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Date(
                    year=year,
                    month=month,
                    day=day,
                    calendar=calendar,
                    iso=iso,
                    display_calendar=display_calendar,
                    date_ext=date_ext,
                )
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


DateType = Date | None


class Time(NamedTuple):
    """Validate and display time data in various formats.

    The standard does not permit leap seconds nor end of day instant (24:00:00).

    Reference
    ---------
    - [GEDCOM Time Data Type](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#time)
    """

    hour: int = Default.TIME_HOUR
    minute: int = Default.TIME_MINUTE
    second: int | float = Default.TIME_SECOND
    UTC: bool = False
    time_ext: ExtType = None

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
            and Checker.verify_ext(Tag.TIME, self.time_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        hour_str: str = str(self.hour)
        minute_str: str = str(self.minute)
        second_str: str = str(self.second)
        lines: str = String.EMPTY
        if self.validate():
            if 0 <= self.hour < 10:
                hour_str = ''.join(['0', hour_str])
            if 0 <= self.minute < 10:
                minute_str = ''.join(['0', minute_str])
            if 0 <= self.second < 10:
                second_str = ''.join(['0', second_str])
            if self.UTC:
                second_str = ''.join([second_str, 'Z'])
            lines = Tagger.string(
                lines, level, Tag.TIME, f'{hour_str}:{minute_str}:{second_str}'
            )
            lines = Tagger.structure(lines, level + 1, self.time_ext)
        return lines

    def iso(self) -> str:
        """Return the validated ISO format for the time.

        References:
            [ISO 8601 Standard](https://www.iso.org/iso-8601-date-and-time-format.html)
            [Wikipedia Overview](https://en.wikipedia.org/wiki/ISO_8601)
        """
        if self.validate():
            return f'{self.hour}:{self.minute}:{self.second}'
        return ''

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
Time(
    hour = {Formatter.codes(self.hour, tabs)},
    minute = {Formatter.codes(self.minute, tabs)},
    second = {Formatter.codes(self.second, tabs)},
    UTC = {Formatter.codes(self.UTC, tabs)},
    time_ext = {Formatter.codes(self.time_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        hour: int = Default.TIME_HOUR,
        minute: int = Default.TIME_MINUTE,
        second: int | float = Default.TIME_SECOND,
        UTC: bool = False,
        time_ext: ExtType = None,
    ) -> None:
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
        show: Time
        gedcom_docs: str = Specs.TIME
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = Time(
                    hour=22,
                    minute=1,
                    second=50,
                    UTC=True,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Time(
                    hour=22,
                    minute=1,
                    second=50,
                    UTC=True,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Time(
                    hour=22,
                    minute=1,
                    second=50,
                    UTC=True,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Time(
                    hour=hour,
                    minute=minute,
                    second=second,
                    UTC=UTC,
                    time_ext=time_ext,
                )
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


TimeType = Time | None


# class DateExact(Structure):
#     """Construct a DATEVALUE structure according to the GEDCOM standard.

#     Example
#     -------


#     Reference
#     ---------

#     >n DATE <DateValue>                         {1:1}  g7:DATE
#     >  +1 TIME <Time>                           {0:1}  g7:TIME
#     >  +1 PHRASE <Text>                         {0:1}  g7:PHRASE
#     """
#     structure: ClassVar[str] = Tag.DATE.value
#     substructures: ClassVar[set[str]] = {Tag.TIME.value, Tag.PHRASE.value}

#     def __init__(
#         self,
#         date: Date = Date(),
#         time: Time = Time(),
#         phrase: str = Default.EMPTY,
#     ):
#         self.date = date
#         self.time = time
#         self.phrase = phrase

#     def validate(self) -> bool:
#         """Validate the stored value."""
#         check: bool = (
#             Checker.verify_type(self.phrase, str)
#             and self.date.validate()
#             and self.time.validate()
#         )
#         return check

#     def ged(self, level: int = 1) -> str:
#         """Format to meet GEDCOM standards."""
#         lines: str = String.EMPTY
#         if self.validate():
#             lines = Tagger.structure(lines, level, self.date, Date())
#             lines = Tagger.structure(lines, level + 1, self.time, Time())
#             lines = Tagger.string(lines, level + 1, Tag.PHRASE, self.phrase)
#         return lines

#     def code(self, tabs: int = 0) -> str:
#         return indent(
#             f"""
# DateExact(
#     date = {Formatter.codes(self.date, tabs)},
#     time = {Formatter.codes(self.time, tabs)},
#     phrase = {Formatter.codes(self.phrase, tabs)},
# )""",
#             String.INDENT * tabs,
#         )


class DateValue(NamedTuple):
    """Construct a DATEVALUE structure according to the GEDCOM standard.

    Example
    -------


    Reference:
        [GEDCOM Date Value](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#DATE_VALUE)

    >n DATE <DateValue>                         {1:1}  g7:DATE
    >  +1 TIME <Time>                           {0:1}  g7:TIME
    >  +1 PHRASE <Text>                         {0:1}  g7:PHRASE
    """

    date: DateType = None
    time: TimeType = None
    phrase: str = Default.EMPTY
    phrase_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.phrase, str)
            and (self.date is not None and self.date.validate())
            and (self.time is not None and self.time.validate())
            and Checker.verify_ext(Tag.PHRASE, self.phrase_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.structure(lines, level, self.date, Date())
            lines = Tagger.structure(lines, level + 1, self.time, Time())
            lines = Tagger.string(lines, level + 1, Tag.PHRASE, self.phrase)
            lines = Tagger.structure(lines, level + 2, self.phrase_ext)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
DateValue(
    date = {Formatter.codes(self.date, tabs)},
    time = {Formatter.codes(self.time, tabs)},
    phrase = {Formatter.codes(self.phrase, tabs)},
    phrase_ext = {Formatter.codes(self.phrase_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        date: Date = Date(),  # noqa: B008
        time: Time = Time(),  # noqa: B008
        phrase: str = Default.EMPTY,
        phrase_ext: ExtType = None,
    ) -> None:
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
        show: DateValue
        gedcom_docs: str = Specs.DATE_VALUE
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = DateValue(
                    Date(2024, 1, 10),
                    Time(12, 30, 5),
                    phrase='Test Date and Time',
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = DateValue(
                    Date(2024, 1, 10),
                    Time(12, 30, 5),
                    phrase='Test Date and Time',
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = DateValue(
                    Date(2024, 1, 10),
                    Time(12, 30, 5),
                    phrase='Test Date and Time',
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = DateValue(
                    date=date,
                    time=time,
                    phrase=phrase,
                    phrase_ext=phrase_ext,
                )
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


DateValueType = DateValue | None


class ChangeDate(NamedTuple):
    """Store, validate and format change date information.

    Example:

    Args:

    Reference:
        [GEDCOM Change Date](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#CHANGE_DATE)
    > n CHAN                                     {1:1}  g7:CHAN
    >   +1 DATE <DateExact>                      {1:1}  g7:DATE-exact
    >      +2 TIME <Time>                        {0:1}  g7:TIME
    >   +1 <<NOTE_STRUCTURE>>                    {0:M}
    """

    date: Date = Date()
    time: Time = Time()
    notes: list[Any] | None = None
    chan_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.notes, Note)
            and self.date.validate()
            and self.time.validate()
            and Checker.verify_ext(Tag.CHAN, self.chan_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.empty(lines, level, Tag.CHAN)
            lines = Tagger.structure(lines, level + 1, self.date, Date())
            lines = Tagger.structure(lines, level + 2, self.time, Time())
            lines = Tagger.structure(lines, level + 1, self.notes, Note())
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
ChangeDate(
    date = {Formatter.codes(self.date, tabs)},
    time = {Formatter.codes(self.time, tabs)},
    notes = {Formatter.codes(self.notes, tabs)},
    chan_ext = {Formatter.codes(self.chan_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        date: Date = Date(),  # noqa: B008
        time: Time = Time(),  # noqa: B008
        notes: list[Any] | None = None,
        chan_ext: ExtType = None,
    ) -> None:
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
        show: ChangeDate
        gedcom_docs: str = Specs.DATE_VALUE
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = ChangeDate(
                    Date(2024, 1, 10),
                    Time(12, 30, 5),
                    notes=None,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = ChangeDate(
                    Date(2024, 1, 10),
                    Time(12, 30, 5),
                    notes=[Note(note='Test Date and Time')],
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = ChangeDate(
                    Date(2024, 1, 10),
                    Time(12, 30, 5),
                    notes=[Note(note='Test Date and Time')],
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = ChangeDate(
                    date=date,
                    time=time,
                    notes=notes,
                    chan_ext=chan_ext,
                )
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


ChangeDateType = ChangeDate | None


class CreationDate(NamedTuple):
    """Store, validate and format create date information.

    Example:

    Args:

    Reference:
        [GEDCOM Creation Date](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#CREATION_DATE)
    > n CREA                                     {1:1}  g7:CREA
    >   +1 DATE <DateExact>                      {1:1}  g7:DATE-exact
    >      +2 TIME <Time>                        {0:1}  g7:TIME
    """

    date: Date = Date()
    time: Time = Time()
    crea_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            self.date.validate()
            and self.time.validate()
            and Checker.verify_ext(Tag.CREA, self.crea_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.empty(lines, level, Tag.CREA)
            lines = Tagger.structure(lines, level + 1, self.crea_ext)
            lines = Tagger.structure(lines, level + 1, self.date, Date())
            lines = Tagger.structure(lines, level + 2, self.time, Time())
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
CreationDate(
    date = {Formatter.codes(self.date, tabs)},
    time = {Formatter.codes(self.time, tabs)},
    crea_ext = {Formatter.codes(self.crea_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        date: Date = Date(),  # noqa: B008
        time: Time = Time(),  # noqa: B008
        crea_ext: ExtType = None,
    ) -> None:
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
        show: CreationDate
        gedcom_docs: str = Specs.DATE_VALUE
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = CreationDate(
                    Date(2024, 1, 10),
                    Time(12, 30, 5),
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = CreationDate(
                    Date(2024, 1, 10),
                    Time(12, 30, 5),
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = CreationDate(
                    Date(2024, 1, 10),
                    Time(12, 30, 5),
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = CreationDate(
                    date=date,
                    time=time,
                    crea_ext=crea_ext,
                )
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


CreationDateType = CreationDate | None


class Identifier(NamedTuple):
    """Construct GEDCOM data for the Identifier Structure.

    There are three valid identifier structures.  They will be illustrated in
    the examples.

    Examples:



    Reference:

    - [GEDCOM Identifier Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#IDENTIFIER_STRUCTURE)

    [
    n REFN <Special>                           {1:1}  g7:REFN
    +1 TYPE <Text>                           {0:1}  g7:TYPE
    |
    n UID <Special>                            {1:1}  g7:UID
    |
    n EXID <Special>                           {1:1}  g7:EXID
    +1 TYPE <Special>                        {0:1}  g7:EXID-TYPE
    ]
    """

    tag: Tag = Tag.NONE
    tag_info: str = Default.EMPTY
    tag_type: str = Default.EMPTY
    tag_ext: ExtType = None
    type_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_enum(self.tag, Id)
            and Checker.verify_type(self.tag_info, str)
            and Checker.verify_type(self.tag_type, str)
            and Checker.verify_ext(self.tag, self.tag_ext)
            and Checker.verify_ext(Tag.TYPE, self.type_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, self.tag, self.tag_info)
            lines = Tagger.structure(lines, level + 1, self.tag_ext)
            lines = Tagger.string(lines, level + 1, Tag.TYPE, self.tag_type)
            lines = Tagger.structure(lines, level + 2, self.type_ext)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
Identifier(
    tag = {Formatter.codes(self.tag, tabs)},
    tag_info = {Formatter.codes(self.tag_info, tabs)},
    tag_type = {Formatter.codes(self.tag_type, tabs)},
    tag_ext = {Formatter.codes(self.tag_ext, tabs)}
    type_ext = {Formatter.codes(self.type_ext, tabs)}
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        tag: Tag = Tag.NONE,
        tag_info: str = Default.EMPTY,
        tag_type: str = Default.EMPTY,
        tag_ext: ExtType = None,
        type_ext: ExtType = None,
    ) -> None:
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
        show: Identifier
        gedcom_docs: str = Specs.IDENTIFIER
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = Identifier(
                    tag=Tag.NONE,
                    tag_info='',
                    tag_type='',
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Identifier(
                    tag=Tag.NONE,
                    tag_info='',
                    tag_type='',
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Identifier(
                    tag=Tag.NONE,
                    tag_info='',
                    tag_type='',
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Identifier(
                    tag=tag,
                    tag_info=tag_info,
                    tag_type=tag_type,
                    tag_ext=tag_ext,
                    type_ext=type_ext,
                )
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


IdenType = Identifier | list[Identifier] | None


class Phone(NamedTuple):
    """Store, validate and format phone information.

    Example:

    Args:

    Reference:
        [GEDCOM Phone](https://gedcom.io/terms/v7/PHON)

    """

    phone: str = Default.EMPTY
    phon_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = Checker.verify_type(
            self.phone, str
        ) and Checker.verify_ext(Tag.PHON, self.phon_ext)
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.PHON, self.phone)
            lines = Tagger.structure(lines, level + 1, self.phon_ext)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
Phone(
    phone = {Formatter.codes(self.phone, tabs)},
    phon_ext = {Formatter.codes(self.phon_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        phone: str = Default.EMPTY,
        phon_ext: ExtType = None,
    ) -> None:
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
        show: Phone
        gedcom_docs: str = Docs.PHON
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = Phone(
                    phone='234 456 789',
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Phone(phone='12345667')
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Phone(phone='23456')
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Phone(
                    phone=phone,
                    phon_ext=phon_ext,
                )
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


PhoneType = Phone | list[Phone] | None


class Email(NamedTuple):
    """Store, validate and format email information.

    Example:

    Args:

    Reference:
        [GEDCOM Phone](https://gedcom.io/terms/v7/EMAIL)

    """

    email: str = Default.EMPTY
    email_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = Checker.verify_type(
            self.email, str
        ) and Checker.verify_ext(Tag.EMAIL, self.email_ext)
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.EMAIL, self.email)
            lines = Tagger.structure(lines, level + 1, self.email_ext)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
Email(
    email = {Formatter.codes(self.email, tabs)},
    email_ext = {Formatter.codes(self.email_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        email: str = Default.EMPTY,
        email_ext: ExtType = None,
    ) -> None:
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
        show: Email
        gedcom_docs: str = Docs.EMAIL
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = Email(
                    email='abe@a.mail',
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Email(email='r@c.com')
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Email(email='two@three.com')
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Email(
                    email=email,
                    email_ext=email_ext,
                )
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


EmailType = Email | list[Email] | None


class Fax(NamedTuple):
    """Store, validate and format fax information.

    Example:

    Args:

    Reference:
        [GEDCOM Phone](https://gedcom.io/terms/v7/FAX)

    """

    fax: str = Default.EMPTY
    fax_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = Checker.verify_type(self.fax, str) and Checker.verify_ext(
            Tag.FAX, self.fax_ext
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.FAX, self.fax)
            lines = Tagger.structure(lines, level + 1, self.fax_ext)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
Fax(
    fax = {Formatter.codes(self.fax, tabs)},
    fax_ext = {Formatter.codes(self.fax_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        fax: str = Default.EMPTY,
        fax_ext: ExtType = None,
    ) -> None:
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
        show: Fax
        gedcom_docs: str = Docs.FAX
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = Fax(
                    fax='234567',
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Fax(fax='3333333')
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Fax(fax='two@three.com')
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Fax(
                    fax=fax,
                    fax_ext=fax_ext,
                )
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


FaxType = Fax | list[Fax] | None


class WWW(NamedTuple):
    """Store, validate and format fax information.

    Example:

    Args:

    Reference:
        [GEDCOM Phone](https://gedcom.io/terms/v7/FAX)

    """

    www: str = Default.EMPTY
    www_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = Checker.verify_type(self.www, str) and Checker.verify_ext(
            Tag.WWW, self.www_ext
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.WWW, self.www)
            lines = Tagger.structure(lines, level + 1, self.www_ext)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
WWW(
    www = {Formatter.codes(self.www, tabs)},
    www_ext = {Formatter.codes(self.www_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        www: str = Default.EMPTY,
        www_ext: ExtType = None,
    ) -> None:
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
        show: WWW
        gedcom_docs: str = Docs.WWW
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = WWW(
                    www='234567',
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = WWW(www='3333333')
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = WWW(www='two@three.com')
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = WWW(
                    www=www,
                    www_ext=www_ext,
                )
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


WWWType = WWW | list[WWW] | None


class Lang(NamedTuple):
    """Store, validate and format fax information.

    Example:

    Args:

    Reference:
        [GEDCOM Phone](https://gedcom.io/terms/v7/FAX)

    """

    lang: str = Default.EMPTY
    lang_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = Checker.verify_type(
            self.lang, str
        ) and Checker.verify_ext(Tag.LANG, self.lang_ext)
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.LANG, self.lang)
            lines = Tagger.structure(lines, level + 1, self.lang_ext)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
Lang(
    lang = {Formatter.codes(self.lang, tabs)},
    lang_ext = {Formatter.codes(self.lang_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        lang: str = Default.EMPTY,
        lang_ext: ExtType = None,
    ) -> None:
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
        show: Lang
        gedcom_docs: str = Docs.LANG
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = Lang(
                    lang='en-US',
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Lang(lang='en')
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Lang(lang='two@three.com')
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Lang(
                    lang=lang,
                    lang_ext=lang_ext,
                )
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


LangType = Lang | list[Lang] | None


class Phrase(NamedTuple):
    """Store, validate and format fax information.

    Example:

    Args:

    Reference:
        [GEDCOM Phone](https://gedcom.io/terms/v7/FAX)

    """

    phrase: str = Default.EMPTY
    phrase_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = Checker.verify_type(
            self.phrase, str
        ) and Checker.verify_ext(Tag.LANG, self.phrase_ext)
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.PHRASE, self.phrase)
            lines = Tagger.structure(lines, level + 1, self.phrase_ext)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
Phrase(
    phrase = {Formatter.codes(self.phrase, tabs)},
    phrase_ext = {Formatter.codes(self.phrase_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        phrase: str = Default.EMPTY,
        phrase_ext: ExtType = None,
    ) -> None:
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
        show: Phrase
        gedcom_docs: str = Docs.LANG
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = Phrase('something')
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Phrase('else')
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Phrase('now')
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Phrase(
                    phrase=phrase,
                    phrase_ext=phrase_ext,
                )
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


PhraseType = Phrase | None


class Address(NamedTuple):
    """Store, validate and format address information to be saved to a ged file.

    Example:
        The following is the minimum amount of information for an address.
        >>> from genedata.store import Address
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
        >>> from genedata.store import Address
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

    address: list[str] | None = None
    city: str = Default.EMPTY
    state: str = Default.EMPTY
    postal: str = Default.EMPTY
    country: str = Default.EMPTY
    addr_ext: ExtType = None
    city_ext: ExtType = None
    stae_ext: ExtType = None
    post_ext: ExtType = None
    ctry_ext: ExtType = None

    def validate(self) -> bool:
        check: bool = (
            Checker.verify_type(self.address, str | list | None)
            and Checker.verify_type(self.city, str)
            and Checker.verify_type(self.state, str)
            and Checker.verify_type(self.postal, str)
            and Checker.verify_type(self.country, str)
            and Checker.verify_ext(Tag.ADDR, self.addr_ext)
            and Checker.verify_ext(Tag.CITY, self.city_ext)
            and Checker.verify_ext(Tag.STAE, self.stae_ext)
            and Checker.verify_ext(Tag.POST, self.post_ext)
            and Checker.verify_ext(Tag.CTRY, self.ctry_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = String.EMPTY
        if self.validate():
            if self.address is not None and len(self.address) > 0:
                lines = Tagger.taginfo(level, Tag.ADDR, self.address[0])
                for line in self.address[1:]:
                    lines = Tagger.string(lines, level, Tag.CONT, line)
                lines = Tagger.structure(lines, level + 1, self.addr_ext)
            lines = Tagger.string(lines, level + 1, Tag.CITY, self.city)
            lines = Tagger.structure(lines, level + 1, self.city_ext)
            lines = Tagger.string(lines, level + 1, Tag.STAE, self.state)
            lines = Tagger.structure(lines, level + 1, self.stae_ext)
            lines = Tagger.string(lines, level + 1, Tag.POST, self.postal)
            lines = Tagger.structure(lines, level + 1, self.post_ext)
            lines = Tagger.string(lines, level + 1, Tag.CTRY, self.country)
            lines = Tagger.structure(lines, level + 1, self.ctry_ext)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
Address(
    address = {Formatter.codes(self.address, tabs)},
    city = {Formatter.codes(self.city, tabs + 1)},
    state = {Formatter.codes(self.state, tabs + 1)},
    postal = {Formatter.codes(self.postal, tabs + 1)},
    country = {Formatter.codes(self.country, tabs + 1)},
    addr_ext = {Formatter.codes(self.addr_ext, tabs + 1)},
    city_ext = {Formatter.codes(self.city_ext, tabs + 1)},
    stae_ext = {Formatter.codes(self.stae_ext, tabs + 1)},
    post_ext = {Formatter.codes(self.post_ext, tabs + 1)},
    ctry_ext = {Formatter.codes(self.ctry_ext, tabs + 1)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        address: list[str] = [],  # noqa: B006
        city: str = Default.EMPTY,
        state: str = Default.EMPTY,
        postal: str = Default.EMPTY,
        country: str = Default.EMPTY,
        addr_ext: ExtType = None,
        city_ext: ExtType = None,
        stae_ext: ExtType = None,
        post_ext: ExtType = None,
        ctry_ext: ExtType = None,
    ) -> None:
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
                show = Address(
                    address=address,
                    city=city,
                    state=state,
                    postal=postal,
                    country=country,
                    addr_ext=addr_ext,
                    city_ext=city_ext,
                    stae_ext=stae_ext,
                    post_ext=post_ext,
                    ctry_ext=ctry_ext,
                )
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


AddrType = Address | None


class Age(NamedTuple):
    """Implement the Age data type in the GEDCOM specification.

    The GEDCOM specification requires that these age components be
    rounded down. The `phrase` parameter allows the user to
    add information about the data provided.

    Examples:
        >>> from genedata.store import Age, Phrase
        >>> from genedata.constants import String
        >>> print(
        ...     Age(
        ...         10,
        ...         greater_less_than='>',
        ...         phrase=Phrase('Estimated'),
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

    years: int = Default.YEARS
    months: int = Default.MONTHS
    weeks: int = Default.WEEKS
    days: int = Default.DAYS
    greater_less_than: str = Default.GREATER_LESS_THAN
    phrase: PhraseType = None
    age_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.years, int)
            and Checker.verify_type(self.months, int)
            and Checker.verify_type(self.weeks, int)
            and Checker.verify_type(self.days, int)
            and Checker.verify_type(self.phrase, Phrase)
            and Checker.verify_not_negative(self.years)
            and Checker.verify_not_negative(self.months)
            and Checker.verify_not_negative(self.weeks)
            and Checker.verify_not_negative(self.days)
            and Checker.verify_ext(Tag.AGE, self.age_ext)
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
            line = Tagger.structure(line, level + 1, self.age_ext)
            line = Tagger.structure(line, level + 1, self.phrase)
        return line

    def code(self, tabs: int = 0) -> str:
        """Generate the ChronoData code that would produce the GEDCOM lines."""
        return indent(
            f"""
Age(
    years = {Formatter.codes(self.years, tabs)},
    months = {Formatter.codes(self.months, tabs)},
    weeks = {Formatter.codes(self.weeks, tabs)},
    days = {Formatter.codes(self.days, tabs)},
    greater_less_than = {Formatter.codes(self.greater_less_than, tabs)},
    phrase = {Formatter.codes(self.phrase)},
    age_ext = {Formatter.codes(self.age_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        years: int = Default.YEARS,
        months: int = Default.MONTHS,
        weeks: int = Default.WEEKS,
        days: int = Default.DAYS,
        greater_less_than: str = Default.GREATER_LESS_THAN,
        phrase: PhraseType = None,
        age_ext: ExtType = None,
    ) -> None:
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
                    phrase=Phrase(
                        'Original text read, "Ten years, two months, one week and two days."'
                    ),
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
                    phrase=Phrase(
                        'Original text read, "Under two months and two days."'
                    ),
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
                    phrase=Phrase(
                        'Original text read, "Čtyřicet týdnů a dva dny"'
                    ),
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Age(
                    years=years,
                    months=months,
                    weeks=weeks,
                    days=days,
                    greater_less_than=greater_less_than,
                    phrase=phrase,
                    age_ext=age_ext,
                )
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


AgeType = Age | None


class PersonalNamePieces(NamedTuple):
    """Store, validate and display values for an optional GEDCOM Personal Name Piece.

    Example:
        This example includes all six of the Personal Name Piece tags.
        >>> from genedata.store import (
        ...     PersonalNamePieces,
        ... )  # doctest: +ELLIPSIS
        >>> from genedata.gedcom import Tag

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

    prefix: list[str] | None = None
    given: list[str] | None = None
    nickname: list[str] | None = None
    surname_prefix: list[str] | None = None
    surname: list[str] | None = None
    suffix: list[str] | None = None
    npfx_ext: ExtType = None
    givn_ext: ExtType = None
    nick_ext: ExtType = None
    spfx_ext: ExtType = None
    surn_ext: ExtType = None
    nsfx_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.prefix, str | list | None)
            and Checker.verify_type(self.given, str | list | None)
            and Checker.verify_type(self.nickname, str | list | None)
            and Checker.verify_type(self.surname_prefix, str | list | None)
            and Checker.verify_type(self.surname, str | list | None)
            and Checker.verify_type(self.suffix, str | list | None)
            and Checker.verify_ext(Tag.NPFX, self.npfx_ext)
            and Checker.verify_ext(Tag.GIVN, self.givn_ext)
            and Checker.verify_ext(Tag.NICK, self.nick_ext)
            and Checker.verify_ext(Tag.SPFX, self.spfx_ext)
            and Checker.verify_ext(Tag.SURN, self.surn_ext)
            and Checker.verify_ext(Tag.NSFX, self.nsfx_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.NPFX, self.prefix)
            lines = Tagger.structure(lines, level + 1, self.npfx_ext)
            lines = Tagger.string(lines, level, Tag.GIVN, self.given)
            lines = Tagger.structure(lines, level + 1, self.givn_ext)
            lines = Tagger.string(lines, level, Tag.NICK, self.nickname)
            lines = Tagger.structure(lines, level + 1, self.nick_ext)
            lines = Tagger.string(lines, level, Tag.SPFX, self.surname_prefix)
            lines = Tagger.structure(lines, level + 1, self.spfx_ext)
            lines = Tagger.string(lines, level, Tag.SURN, self.surname)
            lines = Tagger.structure(lines, level + 1, self.surn_ext)
            lines = Tagger.string(lines, level, Tag.NSFX, self.suffix)
            lines = Tagger.structure(lines, level + 1, self.nsfx_ext)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
PersonalNamePieces(
    prefix = {Formatter.codes(self.prefix, tabs)},
    given = {Formatter.codes(self.given, tabs)},
    nickname = {Formatter.codes(self.nickname, tabs)},
    surname_prefix = {Formatter.codes(self.surname_prefix, tabs)},
    surname = {Formatter.codes(self.surname, tabs)},
    suffix = {Formatter.codes(self.suffix, tabs)},
    npfx_ext = {Formatter.codes(self.npfx_ext, tabs)},
    givn_ext = {Formatter.codes(self.givn_ext, tabs)},
    nick_ext = {Formatter.codes(self.nick_ext, tabs)},
    spfx_ext = {Formatter.codes(self.spfx_ext, tabs)},
    surn_ext = {Formatter.codes(self.surn_ext, tabs)},
    nsfx_ext = {Formatter.codes(self.nsfx_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        prefix: list[str] | None = None,
        given: list[str] | None = None,
        nickname: list[str] | None = None,
        surname_prefix: list[str] | None = None,
        surname: list[str] | None = None,
        suffix: list[str] | None = None,
        npfx_ext: ExtType = None,
        givn_ext: ExtType = None,
        nick_ext: ExtType = None,
        spfx_ext: ExtType = None,
        surn_ext: ExtType = None,
        nsfx_ext: ExtType = None,
    ) -> None:
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
                show = PersonalNamePieces(
                    prefix=prefix,
                    given=given,
                    nickname=nickname,
                    surname_prefix=surname_prefix,
                    surname=surname,
                    suffix=suffix,
                    npfx_ext=npfx_ext,
                    givn_ext=givn_ext,
                    nick_ext=nick_ext,
                    spfx_ext=spfx_ext,
                    surn_ext=surn_ext,
                    nsfx_ext=nsfx_ext,
                )
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


PersonalNamePiecesType = PersonalNamePieces | None


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
        >>> from genedata.store import Lang, NameTranslation
        >>> joe_in_chinese = '喬'
        >>> language = Lang('cmn')
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
    language: LangType = None
    pieces: PersonalNamePieces | None = None
    tran_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.translation, str)
            and Checker.verify_type(self.language, Lang)
            and Checker.verify_not_default(self.language, None)
            and Checker.verify_type(self.pieces, PersonalNamePieces)
            and Checker.verify_ext(Tag.TRAN, self.tran_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.TRAN, self.translation)
            lines = Tagger.structure(lines, level + 1, self.tran_ext)
            lines = Tagger.structure(lines, level + 1, self.language)
            lines = Tagger.structure(
                lines, level + 1, self.pieces, PersonalNamePieces()
            )
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
NameTranslation(
    translation = {Formatter.codes(self.translation, tabs)},
    language = {Formatter.codes(self.language, tabs + 1)},
    pieces = {Formatter.codes(self.pieces, tabs + 1)},
    tran_ext = {Formatter.codes(self.tran_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        translation: str = String.EMPTY,
        language: LangType = None,
        pieces: PersonalNamePieces | None = None,
        tran_ext: ExtType = None,
    ) -> None:
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
                    language=Lang('he'),
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
                    language=Lang('ar'),
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
                    language=Lang('el'),
                    pieces=PersonalNamePieces(
                        given=['Τόμας'],
                        surname=['Τζόουνς'],
                    ),
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = NameTranslation(
                    translation=translation,
                    language=language,
                    pieces=pieces,
                    tran_ext=tran_ext,
                )
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


NameTranType = NameTranslation | list[NameTranslation] | None


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
        >>> from genedata.store import Lang, NoteTranslation
        >>> from genedata.constants import MediaType
        >>> arabic_text = 'هذه ملاحظة.'
        >>> mime = MediaType.TEXT_HTML
        >>> language = Lang('afb')
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
    language: LangType = None
    tran_ext: ExtType = None
    mime_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.translation, str)
            and Checker.verify_type(self.mime, MediaType)
            and Checker.verify_type(self.language, Lang)
            and Checker.verify_ext(Tag.TRAN, self.tran_ext)
            and Checker.verify_ext(Tag.MIME, self.mime_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.translation != String.EMPTY and self.validate():
            lines = Tagger.string(lines, level, Tag.TRAN, self.translation)
            lines = Tagger.structure(lines, level + 1, self.tran_ext)
            lines = Tagger.string(lines, level + 1, Tag.MIME, self.mime.value)
            lines = Tagger.structure(lines, level + 2, self.mime_ext)
            lines = Tagger.structure(lines, level + 1, self.language)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
NoteTranslation(
    translation = {Formatter.codes(self.translation, tabs)},
    mime = {Formatter.codes(self.mime, tabs)},
    language = {Formatter.codes(self.language, tabs)},
    tran_ext = {Formatter.codes(self.tran_ext, tabs)},
    mime_ext = {Formatter.codes(self.mime_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        translation: str = Default.EMPTY,
        mime: MediaType = MediaType.NONE,
        language: LangType = None,
        tran_ext: ExtType = None,
        mime_ext: ExtType = None,
    ) -> None:
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
                    language=Lang('pl'),
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = NoteTranslation(
                    translation='Þetta er einföld athugasemd.',
                    mime=MediaType.TEXT_PLAIN,
                    language=Lang('is'),
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = NoteTranslation(
                    translation='यह एक साधारण नोट है.',
                    mime=MediaType.TEXT_PLAIN,
                    language=Lang('hi'),
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = NoteTranslation(
                    translation=translation,
                    mime=mime,
                    language=language,
                    tran_ext=tran_ext,
                    mime_ext=mime_ext,
                )
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


NoteTranType = NoteTranslation | list[NoteTranslation] | None


class CallNumber(NamedTuple):
    """Store, validate and display the option call numbers for the
    SourceRepositoryCitation substructure.

    Example:
        This example assumes there is a call number "1111" which is the
        minimal amount of information needed to use this optional feature.
        >>> from genedata.store import CallNumber
        >>> cn = CallNumber('1111')
        >>> cn.validate()
        True
        >>> print(cn.ged(1))
        1 CALN 1111
        <BLANKLINE>

        This next example uses all of the optional positions.
        >>> from genedata.gedcom import Tag
        >>> cn_all = CallNumber('1111', Tag.BOOK, Phrase('New Testament'))
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
    medium: Tag = Tag.NONE
    phrase: PhraseType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.call_number, str)
            and Checker.verify_enum(self.medium, Medium)
            and Checker.verify_type(self.phrase, Phrase)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.call_number != String.EMPTY and self.validate():
            lines = Tagger.string(lines, level, Tag.CALN, self.call_number)
            lines = Tagger.string(lines, level + 1, Tag.MEDI, self.medium.value)
            lines = Tagger.structure(lines, level + 2, self.phrase)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
CallNumber(
    call_number = {Formatter.codes(self.call_number, tabs)},
    medium = {Formatter.codes(self.medium, tabs)},
    phrase = {Formatter.codes(self.phrase, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        call_number: str = Default.EMPTY,
        medium: Tag = Tag.NONE,
        phrase: PhraseType = None,
    ) -> None:
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
                    medium=Tag.BOOK,
                    phrase=Phrase('A special call number'),
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = CallNumber(
                    call_number='1-234-333 ABC',
                    medium=Tag.MAGAZINE,
                    phrase=Phrase('A special article.'),
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = CallNumber(
                    call_number='1-234-333 ABC',
                    medium=Tag.NONE,
                    phrase=Phrase(''),
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = CallNumber(
                    call_number=call_number,
                    medium=medium,
                    phrase=phrase,
                )
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


CalnType = CallNumber | list[CallNumber] | None


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
    language: LangType = None
    text_ext: ExtType = None
    mime_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.text, str)
            and Checker.verify_type(self.mime, MediaType)
            and Checker.verify_type(self.language, Lang)
            and Checker.verify_ext(Tag.TEXT, self.text_ext)
            and Checker.verify_ext(Tag.MIME, self.mime_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.text != String.EMPTY and self.validate():
            lines = Tagger.string(lines, level, Tag.TEXT, str(self.text))
            lines = Tagger.structure(lines, level + 1, self.text_ext)
            lines = Tagger.string(lines, level + 1, Tag.MIME, self.mime.value)
            lines = Tagger.structure(lines, level + 1, self.mime_ext)
            lines = Tagger.structure(lines, level + 1, self.language)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
Text(
    text = {Formatter.codes(self.text, tabs)},
    mime = {Formatter.codes(self.mime, tabs)},
    language = {Formatter.codes(self.language, tabs)},
    text_ext = {Formatter.codes(self.text_ext, tabs)},
    mime_ext = {Formatter.codes(self.mime_ext, tabs)},
),""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        text: str = Default.EMPTY,
        mime: MediaType = MediaType.NONE,
        language: LangType = None,
        text_ext: ExtType = None,
        mime_ext: ExtType = None,
    ) -> None:
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
                    language=Lang('en'),
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Text(
                    text='ई एकटा पाठ अछि।',
                    mime=MediaType.TEXT_PLAIN,
                    language=Lang('mai'),
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Text(
                    text='ይህ ጽሑፍ ነው።',
                    mime=MediaType.TEXT_PLAIN,
                    language=Lang('am'),
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Text(
                    text=text,
                    mime=mime,
                    language=language,
                    text_ext=text_ext,
                    mime_ext=mime_ext,
                )
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


TextType = Text | list[Text] | None


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

    date_value: DateValue | None = None
    texts: list[Text] | None = None
    data_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.date_value, str)
            and Checker.verify_type(self.texts, Text)
            and Checker.verify_ext(Tag.DATA, self.data_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.date_value != DateValue() and self.validate():
            lines = Tagger.empty(lines, level, Tag.DATA)
            lines = Tagger.structure(lines, level + 1, self.data_ext)
            lines = Tagger.structure(lines, level, self.date_value)
            lines = Tagger.structure(lines, level + 1, self.texts, Text())
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""SourceData(
    date_value = {Formatter.codes(self.date_value, tabs + 1)},
    texts = {Formatter.codes(self.texts, tabs + 1)},
    data_ext = {Formatter.codes(self.data_ext, tabs)},
),""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        date_value: DateValue | None = None,
        texts: list[Text] | None = None,
        data_ext: ExtType = None,
    ) -> None:
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
                        Text(
                            'hello', MediaType.TEXT_PLAIN, language=Lang('en')
                        ),
                        Text(
                            'hello again',
                            MediaType.TEXT_PLAIN,
                            language=Lang('en'),
                        ),
                    ],
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = SourceData(
                    date_value=DateValue(),
                    texts=[
                        Text(
                            'hello', MediaType.TEXT_PLAIN, language=Lang('en')
                        ),
                        Text(
                            'hello again',
                            MediaType.TEXT_PLAIN,
                            language=Lang('en'),
                        ),
                    ],
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = SourceData(
                    date_value=DateValue(),
                    texts=[
                        Text(
                            'hello', MediaType.TEXT_PLAIN, language=Lang('en')
                        ),
                        Text(
                            'hello again',
                            MediaType.TEXT_PLAIN,
                            language=Lang('en'),
                        ),
                    ],
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = SourceData(
                    date_value=date_value,
                    texts=texts,
                    data_ext=data_ext,
                )
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


SourDataType = SourceData | None


class SourceCitation(NamedTuple):
    """Store, validate and display the Source Citation
    substructure of the GEDCOM standard.

    Examples:


    Args:
        source_xref: the source identifier
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

    source_xref: SourceXref = Void.SOUR
    page: str = String.EMPTY
    source_data: SourceData | None = None
    event: Tag = Tag.NONE
    event_phrase: PhraseType = None
    role: Tag = Tag.NONE
    role_phrase: PhraseType = None
    quality: Tag = Tag.NONE
    multimedialinks: list[Any] | None = None
    notes: list[Any] | None = None
    sour_ext: ExtType = None
    page_ext: ExtType = None
    even_ext: ExtType = None
    role_ext: ExtType = None
    quay_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.source_xref, SourceXref)
            and Checker.verify_type(self.page, str)
            and Checker.verify_type(self.source_data, SourceData)
            and Checker.verify_enum(self.event, Even)
            and Checker.verify_type(self.event_phrase, Phrase)
            and Checker.verify_enum(self.role, Role)
            and Checker.verify_type(self.role_phrase, Phrase)
            and Checker.verify_enum(self.quality, Quay)
            and Checker.verify_type(self.multimedialinks, MultimediaLink)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_ext(Tag.SOUR, self.sour_ext)
            and Checker.verify_ext(Tag.PAGE, self.page_ext)
            and Checker.verify_ext(Tag.EVEN, self.even_ext)
            and Checker.verify_ext(Tag.ROLE, self.role_ext)
            and Checker.verify_ext(Tag.QUAY, self.quay_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(
                lines, level, Tag.SOUR, str(self.source_xref), format=False
            )
            lines = Tagger.structure(lines, level + 1, self.sour_ext)
            lines = Tagger.string(lines, level + 1, Tag.PAGE, self.page)
            lines = Tagger.structure(lines, level + 2, self.page_ext)
            lines = Tagger.structure(
                lines, level + 1, self.source_data, SourceData()
            )
            if self.event != Tag.NONE:
                lines = Tagger.string(
                    lines, level + 1, Tag.EVEN, self.event.value
                )
                lines = Tagger.structure(lines, level + 1, self.even_ext)
                lines = Tagger.structure(lines, level + 2, self.event_phrase)
                lines = Tagger.string(
                    lines, level + 2, Tag.ROLE, self.role.value
                )
                lines = Tagger.structure(lines, level + 1, self.role_ext)
                lines = Tagger.structure(lines, level + 2, self.role_phrase)
            lines = Tagger.string(
                lines, level + 1, Tag.QUAY, self.quality.value
            )
            lines = Tagger.structure(lines, level + 1, self.quay_ext)
            lines = Tagger.structure(lines, level + 1, self.multimedialinks)
            lines = Tagger.structure(lines, level + 1, self.notes)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
SourceCitation(
    source_xref = {Formatter.codes(self.source_xref, tabs)},
    page = {Formatter.codes(self.page, tabs)},
    source_data = {Formatter.codes(self.source_data, tabs + 1)},
    event = {Formatter.codes(self.event, tabs + 1)},
    event_phrase = {Formatter.codes(self.event_phrase, tabs)},
    role = {Formatter.codes(self.role, tabs)},
    role_phrase = {Formatter.codes(self.role_phrase, tabs)},
    quality = {Formatter.codes(self.quality, tabs)},
    multimedialinks = {Formatter.codes(self.multimedialinks, tabs + 1)},
    notes = {Formatter.codes(self.notes, tabs + 1)},
    sour_ext = {Formatter.codes(self.sour_ext, tabs + 1)},
    page_ext = {Formatter.codes(self.page_ext, tabs + 1)},
    even_ext = {Formatter.codes(self.even_ext, tabs + 1)},
    role_ext = {Formatter.codes(self.role_ext, tabs + 1)},
    quay_ext = {Formatter.codes(self.quay_ext, tabs + 1)},
),""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        source_xref: SourceXref = Void.SOUR,
        page: str = String.EMPTY,
        source_data: SourceData | None = None,
        event: Tag = Tag.NONE,
        event_phrase: PhraseType = None,
        role: Tag = Tag.NONE,
        role_phrase: PhraseType = None,
        quality: Tag = Tag.NONE,
        multimedialinks: list[Any] | None = None,
        notes: list[Any] | None = None,
        sour_ext: ExtType = None,
        page_ext: ExtType = None,
        even_ext: ExtType = None,
        role_ext: ExtType = None,
        quay_ext: ExtType = None,
    ) -> None:
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
                    source_xref=Void.SOUR,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = SourceCitation(
                    source_xref=Void.SOUR,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = SourceCitation(
                    source_xref=Void.SOUR,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = SourceCitation(
                    source_xref=source_xref,
                    page=page,
                    source_data=source_data,
                    event=event,
                    event_phrase=event_phrase,
                    role=role,
                    role_phrase=role_phrase,
                    quality=quality,
                    multimedialinks=multimedialinks,
                    notes=notes,
                    sour_ext=sour_ext,
                    page_ext=page_ext,
                    even_ext=even_ext,
                    role_ext=role_ext,
                    quay_ext=quay_ext,
                )
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


SourCiteType = SourceCitation | list[SourceCitation] | None


class Note(NamedTuple):
    """Store, validate and display a note substructure of the GEDCOM standard.

    The BCP 47 language tag is a hyphenated list of subtags.
    The [W3C Internationalization](https://www.w3.org/International/questions/qa-choosing-language-tags)
    guide will help one make a decision on which tags to use.
    The [Language Subtag Lookup Tool](https://r12a.github.io/app-subtags/)
    can assist with finding and checking the language tag one would like to use.

    Example:
        This example is a note without other information.
        >>> from genedata.store import Lang, Note
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
        >>> hebrew_note = Note(note='זו ההערה שלי.', language=Lang('he'))
        >>> print(hebrew_note.ged(1))
        1 NOTE זו ההערה שלי.
        2 LANG he
        <BLANKLINE>

        The next example adds translations of the previous example to the note.
        >>> from genedata.constants import MediaType
        >>> english_translation = NoteTranslation(
        ...     'This is my note.', MediaType.TEXT_PLAIN, Lang('en')
        ... )
        >>> urdu_translation = NoteTranslation(
        ...     'یہ میرا نوٹ ہے۔', MediaType.TEXT_PLAIN, Lang('ur')
        ... )
        >>> hebrew_note_with_translations = Note(
        ...     note='זו ההערה שלי.',
        ...     language=Lang('he'),
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

    shared_note_xref: SharedNoteXref = Void.SNOTE
    note: str = Default.EMPTY
    mime: MediaType = MediaType.NONE
    language: LangType = None
    translations: NoteTranType = None
    source_citations: SourCiteType = None
    snote_ext: ExtType = None
    note_ext: ExtType = None
    mime_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.shared_note_xref, SharedNoteXref)
            and Checker.verify_type(self.note, str)
            and Checker.verify_type(self.mime, MediaType)
            and Checker.verify_type(self.translations, NoteTranslation)
            and Checker.verify_type(self.source_citations, SourceCitation)
            and Checker.verify_ext(Tag.SNOTE, self.snote_ext)
            and Checker.verify_ext(Tag.NOTE, self.note_ext)
            and Checker.verify_ext(Tag.MIME, self.mime_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            if self.shared_note_xref != Void.SNOTE:
                lines = Tagger.string(
                    lines, level, Tag.SNOTE, self.shared_note_xref.fullname
                )
                lines = Tagger.structure(lines, level + 1, self.snote_ext)
            else:
                lines = Tagger.string(lines, level, Tag.NOTE, self.note)
                lines = Tagger.structure(lines, level + 1, self.note_ext)
                lines = Tagger.string(
                    lines, level + 1, Tag.MIME, self.mime.value
                )
                lines = Tagger.structure(lines, level + 2, self.mime_ext)
                lines = Tagger.structure(lines, level + 1, self.language)
                lines = Tagger.structure(
                    lines, level + 1, self.translations, NoteTranslation()
                )
                lines = Tagger.structure(
                    lines, level + 1, self.source_citations, SourceCitation()
                )
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
Note(
    snote = {Formatter.codes(self.shared_note_xref, tabs)},
    note = {Formatter.codes(self.note, tabs)},
    mime = {Formatter.codes(self.mime, tabs)},
    language = {Formatter.codes(self.language, tabs)},
    translations = {Formatter.codes(self.translations, tabs + 1)},
    source_citations = {Formatter.codes(self.source_citations, tabs + 1)},
    snote_ext = {Formatter.codes(self.snote_ext, tabs + 1)},
    note_ext = {Formatter.codes(self.note_ext, tabs + 1)},
    mime_ext = {Formatter.codes(self.mime_ext, tabs + 1)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        shared_note_xref: SharedNoteXref = Void.SNOTE,
        note: str = Default.EMPTY,
        mime: MediaType = MediaType.NONE,
        language: LangType = None,
        translations: NoteTranType = None,
        source_citations: SourCiteType = None,
        snote_ext: ExtType = None,
        note_ext: ExtType = None,
        mime_ext: ExtType = None,
    ) -> None:
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
        show: Note
        gedcom_docs: str = Specs.NOTE
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = Note(
                    note='A note',
                    mime=MediaType.NONE,
                    language=Lang('en-US'),
                    translations=None,
                    source_citations=None,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Note(
                    note='A note',
                    mime=MediaType.NONE,
                    language=Lang('en-US'),
                    translations=None,
                    source_citations=None,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Note(
                    note='A note',
                    mime=MediaType.NONE,
                    language=Lang('en-US'),
                    translations=None,
                    source_citations=None,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Note(
                    shared_note_xref=shared_note_xref,
                    note=note,
                    mime=mime,
                    language=language,
                    translations=translations,
                    source_citations=source_citations,
                    snote_ext=snote_ext,
                    note_ext=note_ext,
                    mime_ext=mime_ext,
                )
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


NoteType = Note | list[Note] | None


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

    repository_xref: RepositoryXref = Void.REPO
    notes: NoteType = None
    call_numbers: CalnType = None
    repo_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.repository_xref, RepositoryXref)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_type(self.call_numbers, CallNumber)
            and Checker.verify_ext(Tag.REPO, self.repo_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.repository_xref.fullname != Void.NAME and self.validate():
            lines = Tagger.string(
                lines, level, Tag.SOUR, str(self.repository_xref)
            )
            lines = Tagger.structure(lines, level + 1, self.repo_ext)
            lines = Tagger.structure(lines, level, self.notes, Note())
            lines = Tagger.structure(
                lines, level, self.call_numbers, CallNumber()
            )
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
SourceRepositoryCitation(
    repository_xref = {Formatter.codes(self.repository_xref, tabs)},
    notes = {Formatter.codes(self.notes, tabs + 1)},
    callnumbers = {Formatter.codes(self.call_numbers, tabs + 1)},
    repo_ext = {Formatter.codes(self.repo_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        repository_xref: RepositoryXref = Void.REPO,
        notes: NoteType = None,
        call_numbers: CalnType = None,
        repo_ext: ExtType = None,
    ) -> None:
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
        show: SourceRepositoryCitation
        gedcom_docs: str = Specs.SOURCE_REPOSITORY_CITATION
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = SourceRepositoryCitation(
                    repository_xref=Void.REPO,
                    notes=None,
                    call_numbers=None,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = SourceRepositoryCitation(
                    repository_xref=Void.REPO,
                    notes=None,
                    call_numbers=None,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = SourceRepositoryCitation(
                    repository_xref=Void.REPO,
                    notes=None,
                    call_numbers=None,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = SourceRepositoryCitation(
                    repository_xref=repository_xref,
                    notes=notes,
                    call_numbers=call_numbers,
                    repo_ext=repo_ext,
                )
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


SourRepoCiteType = (
    SourceRepositoryCitation | list[SourceRepositoryCitation] | None
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
        >>> from genedata.store import (
        ...     Lang,
        ...     NameTranslation,
        ...     Note,
        ...     PersonalName,
        ...     PersonalNamePieces,
        ...     Phrase,
        ...     SourceCitation,
        ... )
        >>> from genedata.gedcom import NameType, PersonalNamePieceTag
        >>> adam_note = Note(note='Here is a place to add more information.')
        >>> adam_english = NameTranslation(
        ...     'Adam', Lang('en'), PersonalNamePieces(nickname=['the man'])
        ... )
        >>> adam = PersonalName(
        ...     name='אָדָ֛ם',
        ...     type=Tag.OTHER,
        ...     phrase=Phrase('The first man'),
        ...     pieces=PersonalNamePieces(nickname=['הָֽאָדָ֖ם']),
        ...     translations=[adam_english],
        ...     notes=[adam_note],
        ... )
        >>> print(adam.ged(1))
        1 NAME אָדָ֛ם //
        2 TYPE OTHER
        3 PHRASE The first man
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

    name: str = Default.EMPTY
    surname: str = Default.EMPTY
    type: Tag = Tag.NONE
    phrase: PhraseType = None
    pieces: PersonalNamePiecesType = None
    translations: NameTranType = None
    notes: NoteType = None
    source_citations: SourCiteType = None
    name_ext: ExtType = None
    type_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_not_default(self.name, '')
            and Checker.verify_type(self.name, str)
            and Checker.verify_type(self.surname, str)
            and Checker.verify_enum(self.type, NameType)
            and Checker.verify_type(self.phrase, Phrase)
            and Checker.verify_type(self.pieces, PersonalNamePieces)
            and Checker.verify_type(self.translations, NameTranslation)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_type(self.source_citations, SourceCitation)
            and Checker.verify_ext(Tag.NAME, self.name_ext)
            and Checker.verify_ext(Tag.TYPE, self.type_ext)
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
            lines = Tagger.structure(lines, level + 1, self.name_ext)
            lines = Tagger.string(lines, level + 1, Tag.TYPE, self.type.value)
            lines = Tagger.structure(lines, level + 2, self.type_ext)
            lines = Tagger.structure(lines, level + 2, self.phrase)
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

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
PersonalName(
    name = {Formatter.codes(self.name, tabs)},
    surname = {Formatter.codes(self.surname, tabs)},
    type = {Formatter.codes(self.type, tabs)},
    phrase = {Formatter.codes(self.phrase, tabs)},
    pieces = {Formatter.codes(self.pieces, tabs + 1)},
    translations = {Formatter.codes(self.translations, tabs + 1)},
    notes = {Formatter.codes(self.notes, tabs + 1)},
    source_citations = {Formatter.codes(self.source_citations, tabs + 1)},
    name_ext = {Formatter.codes(self.name_ext, tabs + 1)},
    type_ext = {Formatter.codes(self.type_ext, tabs + 1)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        name: str = Default.EMPTY,
        surname: str = Default.EMPTY,
        type: Tag = Tag.NONE,
        phrase: PhraseType = None,
        pieces: PersonalNamePiecesType = None,
        translations: NameTranType = None,
        notes: NoteType = None,
        source_citations: SourCiteType = None,
        name_ext: ExtType = None,
        type_ext: ExtType = None,
    ) -> None:
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
        show: PersonalName
        gedcom_docs: str = Specs.PERSONAL_NAME
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = PersonalName(
                    name='First Name Last Name',
                    surname='Last Name',
                    type=Tag.NONE,
                    phrase=None,
                    pieces=None,
                    translations=None,
                    notes=None,
                    source_citations=None,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = PersonalName(
                    name='First Name Last Name',
                    surname='Last Name',
                    type=Tag.NONE,
                    phrase=None,
                    pieces=None,
                    translations=None,
                    notes=None,
                    source_citations=None,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = PersonalName(
                    name='First Name Last Name',
                    surname='Last Name',
                    type=Tag.NONE,
                    phrase=None,
                    pieces=None,
                    translations=None,
                    notes=None,
                    source_citations=None,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = PersonalName(
                    name=name,
                    surname=surname,
                    type=type,
                    phrase=phrase,
                    pieces=pieces,
                    translations=translations,
                    notes=notes,
                    source_citations=source_citations,
                    name_ext=name_ext,
                    type_ext=type_ext,
                )
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


PersonalNameType = PersonalName | list[PersonalName] | None


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
        >>> from genedata.build import Genealogy
        >>> from genedata.gedcom import Tag
        >>> from genedata.store import Association, Individual, Phrase

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
        ...             association_phrase=Phrase('Mr Stockdale'),
        ...             role=Tag.OTHER,
        ...             role_phrase=Phrase('Teacher'),
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
        ...                         Association(
        ...                             individual_xref=clergy, role=Tag.CLERGY
        ...                         ),
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
        >>> from genedata.build import Genealogy
        >>> from genedata.gedcom import Tag
        >>> from genedata.store import (
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
        ...                     source_xref=sour_s1_xref,
        ...                     event=Tag.BIRT,
        ...                     role=Tag.MOTH,
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
        >>> from genedata.build import Genealogy
        >>> from genedata.gedcom import Tag
        >>> from genedata.store import (
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
        ...             individual_xref=indi_i3_xref,
        ...             role=Tag.FRIEND,
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
        ...                             individual_xref=indi_i3_xref,
        ...                             role=Tag.WITN,
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
        individual_xref: the identifier of the individual in this association.
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

    individual_xref: IndividualXref = Void.INDI
    association_phrase: PhraseType = None
    role: Tag = Tag.NONE
    role_phrase: PhraseType = None
    notes: NoteType = None
    citations: SourCiteType = None
    asso_ext: ExtType = None
    role_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.individual_xref, IndividualXref)
            and Checker.verify_enum(self.role, Role)
            and Checker.verify_type(self.association_phrase, Phrase)
            and Checker.verify_type(self.role_phrase, Phrase)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_type(self.citations, SourceCitation)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = String.EMPTY
        if self.validate():
            lines = Tagger.string(
                lines, level, Tag.ASSO, str(self.individual_xref), format=False
            )
            lines = Tagger.structure(lines, level + 1, self.asso_ext)
            lines = Tagger.structure(lines, level + 1, self.association_phrase)
            lines = Tagger.string(lines, level + 1, Tag.ROLE, self.role.value)
            lines = Tagger.structure(lines, level + 2, self.role_ext)
            lines = Tagger.structure(lines, level + 2, self.role_phrase)
            lines = Tagger.structure(lines, level + 1, self.notes, Note())
            lines = Tagger.structure(
                lines, level + 1, self.citations, SourceCitation()
            )
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
Association(
    individual_xref = {Formatter.codes(self.individual_xref, tabs)},
    association_phrase = {Formatter.codes(self.association_phrase, tabs)},
    role = {Formatter.codes(self.role, tabs)},
    role_phrase = {Formatter.codes(self.role_phrase, tabs)},
    notes = {Formatter.codes(self.notes, tabs)},
    citations = {Formatter.codes(self.citations, tabs)},
    asso_ext = {Formatter.codes(self.asso_ext, tabs)},
    role_ext = {Formatter.codes(self.role_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        individual_xref: IndividualXref = Void.INDI,
        association_phrase: PhraseType = None,
        role: Tag = Tag.NONE,
        role_phrase: PhraseType = None,
        notes: NoteType = None,
        citations: SourCiteType = None,
        asso_ext: ExtType = None,
        role_ext: ExtType = None,
    ) -> None:
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
        show: Association
        gedcom_docs: str = Specs.ASSOCIATION
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = Association(
                    individual_xref=Void.INDI,
                    association_phrase=Phrase('A phrase'),
                    role=Tag.NONE,
                    role_phrase=Phrase('Role Phrase'),
                    notes=None,
                    citations=None,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Association(
                    individual_xref=Void.INDI,
                    association_phrase=Phrase('A phrase'),
                    role=Tag.NONE,
                    role_phrase=Phrase('Role Phrase'),
                    notes=None,
                    citations=None,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Association(
                    individual_xref=Void.INDI,
                    association_phrase=Phrase('A phrase'),
                    role=Tag.NONE,
                    role_phrase=Phrase('Role Phrase'),
                    notes=None,
                    citations=None,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Association(
                    individual_xref=individual_xref,
                    association_phrase=association_phrase,
                    role=role,
                    role_phrase=role_phrase,
                    notes=notes,
                    citations=citations,
                    asso_ext=asso_ext,
                    role_ext=role_ext,
                )
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


AssoType = Association | None


class MultimediaLink(NamedTuple):
    """_summary_

    Examples:


    Args:


    Returns:
        A GEDCOM string storing this data.

    n OBJE @<XREF:OBJE>@                       {1:1}  [g7:OBJE](https://gedcom.io/terms/v7/OBJE)
      +1 CROP                                  {0:1}  [g7:CROP](https://gedcom.io/terms/v7/CROP)
         +2 TOP <Integer>                      {0:1}  [g7:TOP](https://gedcom.io/terms/v7/TOP)
         +2 LEFT <Integer>                     {0:1}  [g7:LEFT](https://gedcom.io/terms/v7/LEFT)
         +2 HEIGHT <Integer>                   {0:1}  [g7:HEIGHT](https://gedcom.io/terms/v7/HEIGHT)
         +2 WIDTH <Integer>                    {0:1}  [g7:WIDTH](https://gedcom.io/terms/v7/WIDTH)
      +1 TITL <Text>                           {0:1}  [g7:TITL](https://gedcom.io/terms/v7/TITL)
    """

    multimedia_xref: MultimediaXref = Void.OBJE
    top: int = Default.TOP
    left: int = Default.LEFT
    height: int = Default.HEIGHT
    width: int = Default.WIDTH
    title: str = Default.EMPTY
    obje_ext: ExtType = None
    top_ext: ExtType = None
    left_ext: ExtType = None
    height_ext: ExtType = None
    width_ext: ExtType = None
    title_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.multimedia_xref, MultimediaXref)
            and Checker.verify_type(self.top, int)
            and Checker.verify_type(self.left, int)
            and Checker.verify_type(self.height, int)
            and Checker.verify_type(self.width, int)
            and Checker.verify_type(self.title, str)
            and Checker.verify_type(Tag.OBJE, self.obje_ext)
            and Checker.verify_ext(Tag.TOP, self.top_ext)
            and Checker.verify_ext(Tag.LEFT, self.left_ext)
            and Checker.verify_ext(Tag.HEIGHT, self.height_ext)
            and Checker.verify_ext(Tag.WIDTH, self.width_ext)
            and Checker.verify_ext(Tag.TITL, self.title_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        lines: str = String.EMPTY
        if self.validate():
            # display only if there is an image file under the multimedia xref
            # need to find out how to identify this and the pixels in that file
            lines = Tagger.string(
                lines, level, Tag.OBJE, self.multimedia_xref.fullname
            )
            lines = Tagger.structure(lines, level + 1, self.obje_ext)
            lines = Tagger.empty(lines, level + 1, Tag.CROP)
            lines = Tagger.structure(lines, level + 2, self.top_ext)
            lines = Tagger.string(lines, level + 2, Tag.TOP, str(self.top))
            lines = Tagger.structure(lines, level + 3, self.top_ext)
            lines = Tagger.string(lines, level + 2, Tag.LEFT, str(self.left))
            lines = Tagger.structure(lines, level + 3, self.left_ext)
            lines = Tagger.string(
                lines, level + 2, Tag.HEIGHT, str(self.height)
            )
            lines = Tagger.structure(lines, level + 3, self.height_ext)
            lines = Tagger.string(lines, level + 2, Tag.WIDTH, str(self.width))
            lines = Tagger.structure(lines, level + 3, self.width_ext)
            lines = Tagger.string(lines, level + 1, Tag.TITL, self.title)
            lines = Tagger.structure(lines, level + 2, self.title_ext)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
MultimediaLink(
    obje = {Formatter.codes(self.multimedia_xref, tabs)},
    top = {Formatter.codes(self.top, tabs)},
    left = {Formatter.codes(self.left, tabs)},
    height = {Formatter.codes(self.height, tabs)},
    width = {Formatter.codes(self.width, tabs)},
    title = {Formatter.codes(self.title, tabs)},
    obje_ext = {Formatter.codes(self.obje_ext, tabs)},
    top_ext = {Formatter.codes(self.top_ext, tabs)},
    left_ext = {Formatter.codes(self.left_ext, tabs)},
    height_ext = {Formatter.codes(self.height_ext, tabs)},
    width_ext = {Formatter.codes(self.width_ext, tabs)},
    title_ext = {Formatter.codes(self.title_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = 1,
        multimedia_xref: MultimediaXref = Void.OBJE,
        top: int = Default.TOP,
        left: int = Default.LEFT,
        height: int = Default.HEIGHT,
        width: int = Default.WIDTH,
        title: str = Default.EMPTY,
        obje_ext: ExtType = None,
        top_ext: ExtType = None,
        left_ext: ExtType = None,
        height_ext: ExtType = None,
        width_ext: ExtType = None,
        title_ext: ExtType = None,
    ) -> None:
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
        show: MultimediaLink
        gedcom_docs: str = Specs.MULTIMEDIA_LINK
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = MultimediaLink(
                    multimedia_xref=Void.OBJE,
                    top=0,
                    left=0,
                    height=0,
                    width=0,
                    title='My title',
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = MultimediaLink(
                    multimedia_xref=Void.OBJE,
                    top=0,
                    left=0,
                    height=0,
                    width=0,
                    title='My title',
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = MultimediaLink(
                    multimedia_xref=Void.OBJE,
                    top=0,
                    left=0,
                    height=0,
                    width=0,
                    title='My title',
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = MultimediaLink(
                    multimedia_xref=multimedia_xref,
                    top=top,
                    left=left,
                    height=height,
                    width=width,
                    title=title,
                    obje_ext=obje_ext,
                    top_ext=top_ext,
                    left_ext=left_ext,
                    width_ext=width_ext,
                    height_ext=height_ext,
                    title_ext=title_ext,
                )
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


MMLinkType = MultimediaLink | None


class Exid(NamedTuple):
    """Store, validate and display an EXID structure."""

    exid: str
    exid_type: str
    exid_ext: ExtType = None
    exid_type_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.exid, str)
            and Checker.verify_type(self.exid_type, str)
            and Checker.verify_ext(Tag.EXID, self.exid_ext)
            and Checker.verify_ext(Tag.TYPE, self.exid_type_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = String.EMPTY
        lines = Tagger.string(lines, level, Tag.EXID, self.exid)
        lines = Tagger.structure(lines, level + 1, self.exid_ext)
        lines = Tagger.string(lines, level + 1, Tag.TYPE, self.exid_type)
        return Tagger.structure(lines, level + 2, self.exid_type_ext)

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
Exid(
    exid = {Formatter.codes(self.exid, tabs)},
    exid_type = {Formatter.codes(self.exid_type, tabs)},
    exid_ext = {Formatter.codes(self.exid_ext, tabs)},
    exid_type_ext = {Formatter.codes(self.exid_type_ext, tabs)}
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        exid: str = Default.EMPTY,
        exid_type: str = Default.EMPTY,
        exid_ext: ExtType = None,
        exid_type_ext: ExtType = None,
    ) -> None:
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
        show: Exid
        gedcom_docs: str = Specs.EXID
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = Exid(
                    exid='22222',
                    exid_type='type',
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Exid(
                    exid='22222',
                    exid_type='type',
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Exid(
                    exid='22222',
                    exid_type='type',
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Exid(
                    exid=exid,
                    exid_type=exid_type,
                    exid_ext=exid_ext,
                    exid_type_ext=exid_type_ext,
                )
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


ExidType = Exid | list[Exid] | None


class Map(NamedTuple):
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
    >>> from genedata.store import Map
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
    >>> from genedata.store import Placer
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

    latitude: float = Default.MAP_LATITUDE
    longitude: float = Default.MAP_LONGITUDE
    map_ext: ExtType = None
    latitude_ext: ExtType = None
    longitude_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.latitude, float)
            and Checker.verify_type(self.longitude, float)
            and Checker.verify_range(self.latitude, -90.0, 90.0)
            and Checker.verify_range(self.longitude, -180.0, 180.0)
            and Checker.verify_ext(Tag.MAP, self.map_ext)
            and Checker.verify_ext(Tag.LATI, self.latitude_ext)
            and Checker.verify_ext(Tag.LONG, self.longitude_ext)
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
            lines = Tagger.structure(lines, level + 1, self.map_ext)
            lines = Tagger.string(lines, level + 1, Tag.LATI, latitude)
            lines = Tagger.structure(lines, level + 2, self.latitude_ext)
            lines = Tagger.string(lines, level + 1, Tag.LONG, longitude)
            lines = Tagger.structure(lines, level + 2, self.longitude_ext)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
Map(
    latitude = {Formatter.codes(self.latitude, tabs)},
    longitude = {Formatter.codes(self.longitude, tabs)},
    map_ext = {Formatter.codes(self.map_ext, tabs)},
    latitude_ext = {Formatter.codes(self.latitude_ext, tabs)},
    longitude_ext = {Formatter.codes(self.longitude_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        latitude: float = Default.MAP_LATITUDE,
        longitude: float = Default.MAP_LONGITUDE,
        map_ext: ExtType = None,
        latitude_ext: ExtType = None,
        longitude_ext: ExtType = None,
    ) -> None:
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
                    show = Map(
                        latitude=latitude,
                        longitude=longitude,
                        map_ext=map_ext,
                        latitude_ext=latitude_ext,
                        longitude_ext=longitude_ext,
                    )
                    logging.info(Example.USER_PROVIDED_EXAMPLE)
                    code_preface = Example.USER_PROVIDED
                    gedcom_preface = Example.GEDCOM
                else:
                    logging.info(Example.ERROR_EXPECTED)
                    show = Map(
                        latitude=latitude,
                        longitude=longitude,
                        map_ext=map_ext,
                        latitude_ext=latitude_ext,
                        longitude_ext=longitude_ext,
                    )
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


MapType = Map | None


class PlaceTranslation(NamedTuple):
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

    place1: str = Default.EMPTY
    place2: str = Default.EMPTY
    place3: str = Default.EMPTY
    place4: str = Default.EMPTY
    language: LangType = None
    tran_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.place1, str)
            and Checker.verify_type(self.place2, str)
            and Checker.verify_type(self.place3, str)
            and Checker.verify_type(self.place4, str)
            and Checker.verify_type(self.language, Lang)
            and Checker.verify_ext(Tag.PLAC, self.tran_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = String.EMPTY
        if self.validate():
            lines = Tagger.string(
                lines,
                level,
                Tag.TRAN,
                Placer.place(
                    self.place1, self.place2, self.place3, self.place4
                ),
            )
            lines = Tagger.structure(lines, level + 1, self.tran_ext)
            lines = Tagger.structure(lines, level + 1, self.language)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
PlaceTranslation(
    place1 = {Formatter.codes(self.place1, tabs)},
    place2 = {Formatter.codes(self.place2, tabs)},
    place3 = {Formatter.codes(self.place3, tabs)},
    place4 = {Formatter.codes(self.place4, tabs)},
    language = {Formatter.codes(self.language, tabs)},
    tran_ext = {Formatter.codes(self.tran_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        place1: str = Default.EMPTY,
        place2: str = Default.EMPTY,
        place3: str = Default.EMPTY,
        place4: str = Default.EMPTY,
        language: LangType = None,
        tran_ext: ExtType = None,
    ) -> None:
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
                    language=Lang('en'),
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = PlaceTranslation(
                    place1='Chicago',
                    place2='Cook County',
                    place3='Illinois',
                    place4='USA',
                    language=Lang('en'),
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = PlaceTranslation(
                    place1='Chicago',
                    place2='Cook County',
                    place3='Illinois',
                    place4='USA',
                    language=Lang('en-US'),
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
                    tran_ext=tran_ext,
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


PlacTranType = PlaceTranslation | list[PlaceTranslation] | None


class Place(NamedTuple):
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
        >>> from genedata.store import Lang, Map, Place
        >>> place = Place(
        ...     place1='Bechyně',
        ...     place2='okres Tábor',
        ...     place3='Jihočeský kraj',
        ...     place4='Česká republika',
        ...     form1='Město',
        ...     form2='Okres',
        ...     form3='Stát',
        ...     form4='Země',
        ...     language=Lang('cs'),
        ...     map=Map(49.297222, 14.470833),
        ...     translations=[
        ...         PlaceTranslation(
        ...             place1='Bechyně',
        ...             place2='Tábor District',
        ...             place3='South Bohemian Region',
        ...             place4='Czech Republic',
        ...             language=Lang('en'),
        ...         )
        ...     ],
        ...     notes=[
        ...         Note(
        ...             note='A place in the Czech Republic.',
        ...             language=Lang('en'),
        ...         ),
        ...         Note(note='Místo v České republice.', language=Lang('cs')),
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

    place1: str = Default.EMPTY
    place2: str = Default.EMPTY
    place3: str = Default.EMPTY
    place4: str = Default.EMPTY
    form1: str = Default.PLACE_FORM1
    form2: str = Default.PLACE_FORM2
    form3: str = Default.PLACE_FORM3
    form4: str = Default.PLACE_FORM4
    language: LangType = None
    translations: PlacTranType = None
    map: MapType = None
    exids: ExidType = None
    notes: NoteType = None
    plac_ext: ExtType = None
    form_ext: ExtType = None

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
            and Checker.verify_type(self.language, Lang)
            and Checker.verify_type(self.translations, PlaceTranslation)
            and Checker.verify_type(self.map, Map)
            and Checker.verify_type(self.exids, Exid)
            and Checker.verify_type(self.notes, Note)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = String.EMPTY
        if self.validate():
            lines = Tagger.string(
                lines,
                level,
                Tag.PLAC,
                Placer.place(
                    self.place1, self.place2, self.place3, self.place4
                ),
            )
            lines = Tagger.structure(lines, level + 1, self.plac_ext)
            lines = Tagger.string(
                lines,
                level + 1,
                Tag.FORM,
                Placer.form(self.form1, self.form2, self.form3, self.form4),
            )
            lines = Tagger.structure(lines, level + 1, self.form_ext)
            lines = Tagger.structure(lines, level + 1, self.language)
            lines = Tagger.structure(lines, level + 1, self.translations)
            lines = Tagger.structure(lines, level + 1, self.map, Map())
            lines = Tagger.structure(lines, level + 1, self.exids)
            lines = Tagger.structure(lines, level + 1, self.notes, Note())
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
Place(
    place1 = {Formatter.codes(self.place1, tabs)},
    place2 = {Formatter.codes(self.place2, tabs)},
    place3 = {Formatter.codes(self.place3, tabs)},
    place4 = {Formatter.codes(self.place4, tabs)},
    form1 = {Formatter.codes(self.form1, tabs)},
    form2 = {Formatter.codes(self.form2, tabs)},
    form3 = {Formatter.codes(self.form3, tabs)},
    form4 = {Formatter.codes(self.form4, tabs)},
    language = {Formatter.codes(self.language, tabs)},
    translations = {Formatter.codes(self.translations, tabs + 2)},
    map = {Formatter.codes(self.map, tabs + 1)},
    exids = {Formatter.codes(self.exids, tabs + 2)},
    notes = {Formatter.codes(self.notes, tabs + 2)},
    plac_ext = {Formatter.codes(self.plac_ext, tabs + 2)},
    form_ext = {Formatter.codes(self.form_ext, tabs)}
)""",
            String.INDENT * tabs,
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
        language: LangType = None,
        translations: PlacTranType = None,
        map: MapType = None,
        exids: ExidType = None,
        notes: NoteType = None,
        plac_ext: ExtType = None,
        form_ext: ExtType = None,
    ) -> None:
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
                            language=Lang('en-US'),
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
                    plac_ext=plac_ext,
                    form_ext=form_ext,
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


PlacType = Place | None


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

    date_value: DateValueType = None
    place: PlacType = None
    address: AddrType = None
    phones: PhoneType = None
    emails: EmailType = None
    faxes: FaxType = None
    wwws: WWWType = None
    agency: str = Default.EMPTY
    religion: str = Default.EMPTY
    cause: str = Default.EMPTY
    resn: Resn = Resn.NONE
    associations: AssoType = None
    notes: NoteType = None
    sources: SourCiteType = None
    multimedia_links: MMLinkType = None
    uids: list[Id] | None = None
    agnc_ext: ExtType = None
    reli_ext: ExtType = None
    caus_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.date_value, DateValue)
            and Checker.verify_type(self.place, Place)
            and Checker.verify_type(self.address, Address)
            and Checker.verify_type(self.phones, Phone)
            and Checker.verify_type(self.emails, Email)
            and Checker.verify_type(self.faxes, Fax)
            and Checker.verify_type(self.wwws, WWW)
            and Checker.verify_type(self.agency, str)
            and Checker.verify_type(self.religion, str)
            and Checker.verify_type(self.cause, str)
            and Checker.verify_type(self.resn, Resn)
            and Checker.verify_type(self.associations, Association)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_type(self.sources, Source)
            and Checker.verify_type(self.multimedia_links, MultimediaLink)
            and Checker.verify_type(self.uids, Id)
            and Checker.verify_ext(Tag.AGNC, self.agnc_ext)
            and Checker.verify_ext(Tag.RELI, self.reli_ext)
            and Checker.verify_ext(Tag.CAUS, self.caus_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = String.EMPTY
        if self.validate():
            lines = Tagger.structure(lines, level, self.date_value, DateValue())
            lines = Tagger.structure(lines, level, self.place, Place())
            lines = Tagger.structure(lines, level, self.address, Address())
            lines = Tagger.structure(lines, level, self.phones)
            lines = Tagger.structure(lines, level, self.emails)
            lines = Tagger.structure(lines, level, self.faxes)
            lines = Tagger.structure(lines, level, self.wwws)
            lines = Tagger.string(lines, level, Tag.AGNC, self.agency)
            lines = Tagger.structure(lines, level + 1, self.agnc_ext)
            lines = Tagger.string(lines, level, Tag.RELI, self.religion)
            lines = Tagger.structure(lines, level + 1, self.reli_ext)
            lines = Tagger.string(lines, level, Tag.CAUS, self.cause)
            lines = Tagger.structure(lines, level + 1, self.caus_ext)
            lines = Tagger.string(lines, level, Tag.RESN, self.resn.value)
            lines = Tagger.structure(lines, level, self.associations)
            lines = Tagger.structure(lines, level, self.notes)
            lines = Tagger.structure(lines, level, self.sources)
            lines = Tagger.structure(lines, level, self.multimedia_links)
            lines = Tagger.structure(lines, level, self.uids)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
EventDetail(
    date_value = {Formatter.codes(self.date_value, tabs)},
    place = {Formatter.codes(self.place, tabs)},
    address = {Formatter.codes(self.address, tabs)},
    phones = {Formatter.codes(self.phones, tabs)},
    emails = {Formatter.codes(self.emails, tabs)},
    faxes = {Formatter.codes(self.faxes, tabs)},
    wwws = {Formatter.codes(self.wwws, tabs)},
    agency = {Formatter.codes(self.agency, tabs)},
    religion = {Formatter.codes(self.religion, tabs)},
    cause = {Formatter.codes(self.cause, tabs)},
    resn = {Formatter.codes(self.resn, tabs)},
    associations = {Formatter.codes(self.associations, tabs)},
    notes = {Formatter.codes(self.notes, tabs)},
    sources = {Formatter.codes(self.sources, tabs)},
    multimedia_links = {Formatter.codes(self.multimedia_links, tabs)}
    uids = {Formatter.codes(self.uids, tabs)},
    agnc_ext = {Formatter.codes(self.agnc_ext, tabs)},
    reli_ext = {Formatter.codes(self.reli_ext, tabs)}
    caus_ext = {Formatter.codes(self.caus_ext, tabs)}
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        date_value: DateValueType = None,
        place: PlacType = None,
        address: AddrType = None,
        phones: PhoneType = None,
        emails: EmailType = None,
        faxes: FaxType = None,
        wwws: WWWType = None,
        agency: str = '',
        religion: str = '',
        cause: str = '',
        resn: Resn = Resn.NONE,
        associations: AssoType = None,
        notes: NoteType = None,
        sources: SourCiteType = None,
        multimedia_links: MMLinkType = None,
        uids: list[Id] | None = None,
        agnc_ext: ExtType = None,
        reli_ext: ExtType = None,
        caus_ext: ExtType = None,
    ) -> None:
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
        show: EventDetail
        gedcom_docs: str = Specs.EVENT_DETAIL
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = EventDetail(
                    date_value=DateValue(),
                    place=Place(),
                    address=Address(),
                    phones=Phone('123-122-1223'),
                    emails=Email('abc@xyz.com'),
                    faxes=Fax('345-234-2345'),
                    wwws=WWW('https:here.com'),
                    agency='',
                    religion='',
                    cause='',
                    resn=Resn.NONE,
                    associations=None,
                    notes=None,
                    sources=None,
                    multimedia_links=None,
                    uids=None,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = EventDetail(
                    date_value=DateValue(),
                    place=Place(),
                    address=Address(),
                    phones=Phone('123-122-1223'),
                    emails=Email('abc@xyz.com'),
                    faxes=Fax('345-234-2345'),
                    wwws=WWW('https:here.com'),
                    agency='',
                    religion='',
                    cause='',
                    resn=Resn.NONE,
                    associations=None,
                    notes=None,
                    sources=None,
                    multimedia_links=None,
                    uids=None,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = EventDetail(
                    date_value=DateValue(),
                    place=Place(),
                    address=Address(),
                    phones=Phone('123-122-1223'),
                    emails=Email('abc@xyz.com'),
                    faxes=Fax('345-234-2345'),
                    wwws=WWW('https:here.com'),
                    agency='',
                    religion='',
                    cause='',
                    resn=Resn.NONE,
                    associations=None,
                    notes=None,
                    sources=None,
                    multimedia_links=None,
                    uids=None,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = EventDetail(
                    date_value=date_value,
                    place=place,
                    address=address,
                    phones=phones,
                    emails=emails,
                    faxes=faxes,
                    wwws=wwws,
                    agency=agency,
                    religion=religion,
                    cause=cause,
                    resn=resn,
                    associations=associations,
                    notes=notes,
                    sources=sources,
                    multimedia_links=multimedia_links,
                    uids=uids,
                    agnc_ext=agnc_ext,
                    reli_ext=reli_ext,
                    caus_ext=caus_ext,
                )
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


EvenDetailType = EventDetail | list[EventDetail] | None


class FamilyEventDetail(NamedTuple):
    """Store, validate and display GEDCOM family event detail structure.

    Examples:
        >>> from genedata.store import Phrase, FamilyEventDetail
        >>> family_detail = FamilyEventDetail(
        ...     husband_age=Age(25, phrase=Phrase('Happy')),
        ...     wife_age=Age(24, phrase=Phrase('Very happy')),
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

    husband_age: AgeType = None
    wife_age: AgeType = None
    event_detail: EvenDetailType = None
    husb_ext: ExtType = None
    wife_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.husband_age, Age | None)
            and Checker.verify_type(self.wife_age, Age | None)
            and Checker.verify_type(self.event_detail, EventDetail | None)
            and Checker.verify_ext(Tag.HUSB, self.husb_ext)
            and Checker.verify_ext(Tag.WIFE, self.wife_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = String.EMPTY
        if self.validate():
            if self.husband_age != Age():
                lines = Tagger.empty(lines, level, Tag.HUSB)
                lines = Tagger.structure(lines, level + 1, self.husb_ext)
                lines = Tagger.structure(lines, level + 1, self.husband_age)
            if self.wife_age != Age():
                lines = Tagger.empty(lines, level, Tag.WIFE)
                lines = Tagger.structure(lines, level + 1, self.wife_ext)
                lines = Tagger.structure(lines, level + 1, self.wife_age)
            lines = Tagger.structure(
                lines, level, self.event_detail, EventDetail()
            )
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
FamilyEventDetail(
    husband_age = {Formatter.codes(self.husband_age, tabs)},
    wife_age = {Formatter.codes(self.wife_age, tabs)},
    event_detail = {Formatter.codes(self.event_detail, tabs)},
    husb_ext = {Formatter.codes(self.husb_ext, tabs)},
    wife_ext = {Formatter.codes(self.wife_ext, tabs)}
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        husband_age: AgeType = None,
        wife_age: AgeType = None,
        event_detail: EvenDetailType = None,
        husb_ext: ExtType = None,
        wife_ext: ExtType = None,
    ) -> None:
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
        show: FamilyEventDetail
        gedcom_docs: str = Specs.FAMILY_EVENT_DETAIL
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = FamilyEventDetail(
                    husband_age=Age(30),
                    wife_age=Age(30),
                    event_detail=None,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = FamilyEventDetail(
                    husband_age=Age(30),
                    wife_age=Age(30),
                    event_detail=None,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = FamilyEventDetail(
                    husband_age=Age(30),
                    wife_age=Age(30),
                    event_detail=None,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = FamilyEventDetail(
                    husband_age=husband_age,
                    wife_age=wife_age,
                    event_detail=event_detail,
                    husb_ext=husb_ext,
                    wife_ext=wife_ext,
                )
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


FamEvenDetailType = FamilyEventDetail | None


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
    payload: str = Default.EMPTY
    attribute_type: str = Default.EMPTY
    family_event_detail: FamEvenDetailType = None
    tag_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.tag, Tag)
            and Checker.verify_enum(self.tag, FamAttr)
            and Checker.verify_type(self.payload, str)
            and Checker.verify_type(self.attribute_type, str)
            and Checker.verify_type(self.family_event_detail, FamilyEventDetail)
            and Checker.verify_ext(self.tag, self.tag_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.tag.value != Tag.NONE.value and self.validate():
            lines = Tagger.string(lines, level, self.tag, self.payload)
            lines = Tagger.structure(lines, level + 1, self.tag_ext)
            lines = Tagger.string(
                lines, level + 1, Tag.TYPE, self.attribute_type
            )
            lines = Tagger.structure(
                lines, level + 1, self.family_event_detail, FamilyEventDetail()
            )
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
FamilyAttribute(
    tag = {Formatter.codes(self.tag, tabs)},
    payload = {Formatter.codes(self.payload, tabs)},
    attribute_type = {Formatter.codes(self.attribute_type, tabs)},
    family_event_detail = {Formatter.codes(self.family_event_detail, tabs)},
    tag_ext = {Formatter.codes(self.tag_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        tag: Tag = Tag.NONE,
        payload: str = Default.EMPTY,
        attribute_type: str = Default.EMPTY,
        family_event_detail: FamEvenDetailType = None,
        tag_ext: ExtType = None,
    ) -> None:
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
        show: FamilyAttribute
        gedcom_docs: str = Specs.FAMILY_ATTRIBUTE
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = FamilyAttribute(
                    tag=Tag.NONE,
                    payload='',
                    attribute_type='',
                    family_event_detail=None,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = FamilyAttribute(
                    tag=Tag.NONE,
                    payload='',
                    attribute_type='',
                    family_event_detail=None,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = FamilyAttribute(
                    tag=Tag.NONE,
                    payload='',
                    attribute_type='',
                    family_event_detail=None,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = FamilyAttribute(
                    tag=tag,
                    payload=payload,
                    attribute_type=attribute_type,
                    family_event_detail=family_event_detail,
                    tag_ext=tag_ext,
                )
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


FamAttrType = FamilyAttribute | list[FamilyAttribute] | None


class FamilyEvent(NamedTuple):
    """Store, validate and display a GEDCOM Family Event.

    Examples:
        Only the following tags can be used in this structure:
        Tag.ANUL, Tag.CENS, Tag.DIV, Tag.DIVF, Tag.ENGA, Tag.MARB, Tag.MARC, Tag.MARL,
        Tag.MARR, Tag.MARS, Tag.EVEN.  This example shows the error that
        would result if a different tag is used once the NamedTuple is validated.
        First, set up the situation for the error to occur.
        >>> from genedata.gedcom import Tag
        >>> from genedata.store import FamilyEvent
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
    occurred: bool = True
    event_type: str = String.EMPTY
    event_detail: FamEvenDetailType = None
    tag_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.tag, Tag)
            and Checker.verify_enum(self.tag, FamEven)
            and Checker.verify_type(self.event_type, str)
            and Checker.verify_type(self.event_detail, FamilyEventDetail)
            and Checker.verify_ext(self.tag, self.tag_ext)
            and Checker.verify(
                self.tag == Tag.EVEN,
                self.event_type != String.EMPTY,
                Msg.EMPTY_EVENT_TYPE.format(self.tag.value),
            )
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            if not self.occurred:
                lines = Tagger.empty(lines, level, self.tag)
            else:
                lines = Tagger.string(lines, level, self.tag, String.OCCURRED)
            lines = Tagger.structure(lines, level + 1, self.tag_ext)
            lines = Tagger.string(lines, level + 1, Tag.TYPE, self.event_type)
            lines = Tagger.structure(lines, level + 1, self.event_detail)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
FamilyEvent(
    tag = {Formatter.codes(self.tag, tabs)},
    occurred = {Formatter.codes(self.occurred, tabs)},
    event_type = {Formatter.codes(self.event_type, tabs)},
    event_detail = {Formatter.codes(self.event_detail, tabs)},
    tag_ext = {Formatter.codes(self.tag_ext, tabs)}
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        tag: Tag = Tag.NONE,
        occurred: bool = True,
        event_type: str = String.EMPTY,
        event_detail: FamEvenDetailType = None,
        tag_ext: ExtType = None,
    ) -> None:
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
        show: FamilyEvent
        gedcom_docs: str = Specs.FAMILY_EVENT
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = FamilyEvent(
                    tag=Tag.NONE,
                    occurred=True,
                    event_type='',
                    event_detail=None,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = FamilyEvent(
                    tag=Tag.NONE,
                    occurred=True,
                    event_type='',
                    event_detail=None,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = FamilyEvent(
                    tag=Tag.NONE,
                    occurred=True,
                    event_type='',
                    event_detail=None,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = FamilyEvent(
                    tag=tag,
                    occurred=occurred,
                    event_type=event_type,
                    event_detail=event_detail,
                    tag_ext=tag_ext,
                )
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


FamEvenType = FamilyEvent | list[FamilyEvent] | None


class Child(NamedTuple):
    """Store, validate and display GEDCOM child information.

    Reference:
        [GEDCOM Family Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_RECORD)

    This is a portion of the GEDCOM Family Record.
    >     +1 CHIL @<XREF:INDI>@                    {0:M}  g7:CHIL
    >        +2 PHRASE <Text>                      {0:1}  g7:PHRASE
    """

    individual_xref: IndividualXref = Void.INDI
    phrase: PhraseType = None
    chil_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.phrase, Phrase)
            and Checker.verify_type(self.individual_xref, IndividualXref)
            and Checker.verify_ext(Tag.CHIL, self.chil_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = String.EMPTY
        if str(self.individual_xref) != Void.NAME and self.validate():
            lines = Tagger.string(
                lines, level, Tag.CHIL, str(self.individual_xref), format=False
            )
            lines = Tagger.structure(lines, level + 1, self.chil_ext)
            lines = Tagger.structure(lines, level + 1, self.phrase)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
Child(
    individual_xref = {Formatter.codes(self.individual_xref, tabs)},
    phrase = {Formatter.codes(self.phrase, tabs)},
    chil_ext = {Formatter.codes(self.chil_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        individual_xref: IndividualXref = Void.INDI,
        phrase: PhraseType = None,
        chil_ext: ExtType = None,
    ) -> None:
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
        show: Child
        gedcom_docs: str = Specs.CHILD
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = Child(
                    individual_xref=Void.INDI,
                    phrase=Phrase('Child'),
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Child(
                    individual_xref=Void.INDI,
                    phrase=Phrase('Child'),
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Child(
                    individual_xref=Void.INDI,
                    phrase=None,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Child(
                    individual_xref=individual_xref,
                    phrase=phrase,
                    chil_ext=chil_ext,
                )
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


ChilType = Child | list[Child] | None


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

    date_value: DateValueType = None
    temple: str = String.EMPTY
    place: PlacType = None
    status: Tag = Tag.NONE
    status_date: DateType = None
    status_time: TimeType = None
    notes: NoteType = None
    source_citations: SourCiteType = None
    temple_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.date_value, DateValue)
            and Checker.verify_type(self.temple, str)
            and Checker.verify_type(self.place, Place)
            and Checker.verify_enum(self.status, Stat)
            and Checker.verify_type(self.status_date, Date)
            and Checker.verify_type(self.status_time, Time)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_type(self.source_citations, SourceCitation)
            and Checker.verify_ext(Tag.TEMP, self.temple_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.structure(lines, level, self.date_value, DateValue())
            lines = Tagger.string(lines, level, Tag.TEMP, self.temple)
            lines = Tagger.structure(lines, level + 1, self.temple_ext)
            lines = Tagger.structure(lines, level, self.place, Place())
            lines = Tagger.string(lines, level, Tag.STAT, self.status.value)
            lines = Tagger.structure(lines, level + 1, self.status_date, Date())
            lines = Tagger.structure(lines, level + 1, self.status_time, Time())
            lines = Tagger.structure(lines, level, self.notes, Note())
            lines = Tagger.structure(
                lines, level, self.source_citations, SourceCitation()
            )
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
LDSOrdinanceDetail(
    date_value = {Formatter.codes(self.date_value, tabs)},
    temple = {Formatter.codes(self.temple, tabs)},
    place = {Formatter.codes(self.place, tabs)},
    status = {Formatter.codes(self.status, tabs)},
    status_date = {Formatter.codes(self.status_date, tabs)},
    status_time = {Formatter.codes(self.status_time, tabs)},
    notes = {Formatter.codes(self.notes, tabs)},
    source_citations = {Formatter.codes(self.source_citations, tabs)},
    temple_ext = {Formatter.codes(self.temple_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        date_value: DateValueType = None,
        temple: str = String.EMPTY,
        place: PlacType = None,
        status: Tag = Tag.NONE,
        status_date: DateType = None,
        status_time: TimeType = None,
        notes: NoteType = None,
        source_citations: SourCiteType = None,
        temple_ext: ExtType = None,
    ) -> None:
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
        show: LDSOrdinanceDetail
        gedcom_docs: str = Specs.LDS_ORDINANCE_DETAIL
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = LDSOrdinanceDetail(
                    date_value=DateValue(),
                    temple='',
                    place=Place(),
                    status=Tag.NONE,
                    status_date=Date(),
                    status_time=Time(),
                    notes=None,
                    source_citations=None,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = LDSOrdinanceDetail(
                    date_value=DateValue(),
                    temple=Default.EMPTY,
                    place=Place(),
                    status=Tag.NONE,
                    status_date=Date(),
                    status_time=Time(),
                    notes=None,
                    source_citations=None,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = LDSOrdinanceDetail(
                    date_value=DateValue(),
                    temple=Default.EMPTY,
                    place=Place(),
                    status=Tag.NONE,
                    status_date=Date(),
                    status_time=Time(),
                    notes=None,
                    source_citations=None,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = LDSOrdinanceDetail(
                    date_value=date_value,
                    temple=temple,
                    place=place,
                    status=status,
                    status_date=status_date,
                    status_time=status_time,
                    notes=notes,
                    source_citations=source_citations,
                    temple_ext=temple_ext,
                )
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


LDSOrdDetailType = LDSOrdinanceDetail | None


class LDSSpouseSealing(NamedTuple):
    """Store, validate and display the LDS Spouse Sealing structure.

    Reference:
        [GEDCOM LDS Spouse Sealing Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#LDS_SPOUSE_SEALING)

    > n SLGS                                     {1:1}  [g7:SLGS](https://gedcom.io/terms/v7/SLGS)
    >   +1 <<LDS_ORDINANCE_DETAIL>>              {0:1}
    """

    tag: Tag = Tag.SLGS
    detail: LDSOrdDetailType = None
    slgs_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.tag, str)
            and Checker.verify_type(self.detail, LDSOrdinanceDetail | None)
            and Checker.verify_ext(Tag.SLGS, self.slgs_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.empty(lines, level, Tag.SLGS)
            lines = Tagger.structure(lines, level + 1, self.slgs_ext)
            lines = Tagger.structure(lines, level + 1, self.detail)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
LDSSpouseSealing(
    tag = {Formatter.codes(self.tag, tabs)},
    detail = {Formatter.codes(self.detail, tabs)},
    slgs_ext = {Formatter.codes(self.slgs_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        tag: Tag = Tag.SLGS,
        detail: LDSOrdDetailType = None,
        slgs_ext: ExtType = None,
    ) -> None:
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
        show: LDSSpouseSealing
        gedcom_docs: str = Specs.LDS_SPOUSE_SEALING
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = LDSSpouseSealing(
                    tag=Tag.SLGS,
                    detail=None,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = LDSSpouseSealing(
                    tag=Tag.SLGS,
                    detail=None,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = LDSSpouseSealing(
                    tag=Tag.SLGS,
                    detail=None,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = LDSSpouseSealing(
                    tag=tag,
                    detail=detail,
                    slgs_ext=slgs_ext,
                )
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


LDSSpouSealingType = LDSSpouseSealing | None


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
    ordinance_detail: LDSOrdDetailType = None
    family_xref: FamilyXref = Void.FAM
    tag_ext: ExtType = None

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
            and Checker.verify_ext(self.tag, self.tag_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.empty(lines, level, self.tag)
            lines = Tagger.structure(lines, level + 1, self.tag_ext)
            lines = Tagger.structure(lines, level + 1, self.ordinance_detail)
            if self.tag == Tag.SLGC:
                lines = Tagger.string(
                    lines, level + 1, Tag.FAMC, self.family_xref.fullname
                )
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
LDSIndividualOrdinance(
    tag = {Formatter.codes(self.tag, tabs)},
    ordinance_detail = {Formatter.codes(self.ordinance_detail, tabs)},
    family_xref = {Formatter.codes(self.family_xref, tabs)},
    tag_ext = {Formatter.codes(self.tag_ext, tabs)}
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        tag: Tag = Tag.NONE,
        ordinance_detail: LDSOrdDetailType = None,
        family_xref: FamilyXref = Void.FAM,
        tag_ext: ExtType = None,
    ) -> None:
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
        show: LDSIndividualOrdinance
        gedcom_docs: str = Specs.LDS_INDIVIDUAL_ORDINANCE
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = LDSIndividualOrdinance(
                    tag=Tag.NONE,
                    ordinance_detail=None,
                    family_xref=Void.FAM,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = LDSIndividualOrdinance(
                    tag=Tag.NONE,
                    ordinance_detail=None,
                    family_xref=Void.FAM,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = LDSIndividualOrdinance(
                    tag=Tag.NONE,
                    ordinance_detail=None,
                    family_xref=Void.FAM,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = LDSIndividualOrdinance(
                    tag=tag,
                    ordinance_detail=ordinance_detail,
                    family_xref=family_xref,
                    tag_ext=tag_ext,
                )
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


LDSIndiOrd = LDSIndividualOrdinance | None


class IndividualEventDetail(NamedTuple):
    """Store, validate and display a GEDCOM Individual Event Detail structure.

    Args:l
        event_detail: A GEDCOM Event Detail structure.
        age: The age of the individual.
        phrase: Text describing the individual event.

    Reference:
        [GEDCOM Individual Event Detail](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_EVENT_DETAIL)

    > n <<EVENT_DETAIL>>                         {1:1}
    > n AGE <Age>                                {0:1}  [g7:AGE](https://gedcom.io/terms/v7/AGE)
    >   +1 PHRASE <Text>                         {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    """

    event_detail: EvenDetailType = None
    age: AgeType = None  # Age(0, 0, 0, 0, String.EMPTY, String.EMPTY)
    phrase: PhraseType = None

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
                lines = Tagger.structure(lines, level + 1, self.phrase)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
IndividualEventDetail(
    event_detail = {Formatter.codes(self.event_detail, tabs)},
    age = {Formatter.codes(self.age, tabs)},
    phrase = {Formatter.codes(self.phrase, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        event_detail: EvenDetailType = None,
        age: AgeType = None,  # Age(0, 0, 0, 0, String.EMPTY, String.EMPTY)
        phrase: PhraseType = None,
    ) -> None:
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
        show: IndividualEventDetail
        gedcom_docs: str = Specs.INDIVIDUAL_EVENT_DETAIL
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = IndividualEventDetail(
                    event_detail=None,
                    age=Age(10),
                    phrase=Phrase('Birthday'),
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = IndividualEventDetail(
                    event_detail=None,
                    age=Age(10),
                    phrase=Phrase('Birthday'),
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = IndividualEventDetail(
                    event_detail=None,
                    age=Age(10),
                    phrase=Phrase('Birthday'),
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = IndividualEventDetail(
                    event_detail=event_detail,
                    age=age,
                    phrase=phrase,
                )
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


IndiEvenDetailType = IndividualEventDetail | list[IndividualEventDetail] | None


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

    tag: Tag
    payload: str
    tag_type: str = Default.EMPTY
    event_detail: IndiEvenDetailType = None
    type_ext: ExtType = None
    tag_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_enum(self.tag, IndiAttr)
            and Checker.verify_type(self.payload, str)
            and Checker.verify_type(self.tag_type, str)
            and Checker.verify_type(self.event_detail, IndividualEventDetail)
            and Checker.verify_ext(Tag.TYPE, self.type_ext)
            and Checker.verify_ext(self.tag, self.tag_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, self.tag, self.payload)
            lines = Tagger.structure(lines, level + 1, self.tag_ext)
            lines = Tagger.string(lines, level + 1, Tag.TYPE, self.tag_type)
            lines = Tagger.structure(lines, level + 1, self.type_ext)
            lines = Tagger.structure(lines, level + 1, self.event_detail)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
IndividualAttribute(
    tag = {Formatter.codes(self.tag, tabs)},
    payload = {Formatter.codes(self.payload, tabs)}
    tag_type = {Formatter.codes(self.tag_type, tabs)},
    event_detail = {Formatter.codes(self.event_detail, tabs)},
    type_ext = {Formatter.codes(self.type_ext, tabs)},
    tag_ext = {Formatter.codes(self.tag_ext, tabs)}
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        tag: Tag = Tag.NONE,
        payload: str = Default.EMPTY,
        tag_type: str = Default.EMPTY,
        event_detail: IndiEvenDetailType = None,
        type_ext: ExtType = None,
        tag_ext: ExtType = None,
    ) -> None:
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
        show: IndividualAttribute
        gedcom_docs: str = Specs.INDIVIDUAL_ATTRIBUTE
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = IndividualAttribute(
                    tag=Tag.NONE,
                    payload='',
                    tag_type='',
                    event_detail=None,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = IndividualAttribute(
                    tag=Tag.NONE,
                    payload='',
                    tag_type='',
                    event_detail=None,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = IndividualAttribute(
                    tag=Tag.NONE,
                    payload='',
                    tag_type='',
                    event_detail=None,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = IndividualAttribute(
                    tag=tag,
                    payload=payload,
                    tag_type=tag_type,
                    event_detail=event_detail,
                    type_ext=type_ext,
                    tag_ext=tag_ext,
                )
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


IndiAttrType = IndividualAttribute | list[IndividualAttribute] | None


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
        >>> from genedata.build import Genealogy
        >>> from genedata.store import Date, DateValue, EventDetail, Individual, IndividualEvent, IndividualEventDetail
        >>> from genedata.gedcom import Tag

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
    payload: str = Default.EMPTY
    text: str = Default.EMPTY
    event_detail: IndiEvenDetailType = None
    family_xref: FamilyXref = Void.FAM
    adoption: Tag = Tag.NONE
    phrase: PhraseType = None
    tag_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_enum(self.tag, IndiEven)
            and Checker.verify_type(self.text, str)
            and Checker.verify_type(self.event_detail, IndividualEventDetail)
            and Checker.verify_type(self.family_xref, FamilyXref)
            and Checker.verify_enum(self.adoption, Adop)
            and Checker.verify_type(self.phrase, Phrase)
            and Checker.verify_ext(self.tag, self.tag_ext)
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
            lines = Tagger.structure(lines, level + 1, self.tag_ext)
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
                        lines = Tagger.structure(lines, level + 3, self.phrase)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
IndividualEvent(
    tag = {Formatter.codes(self.tag, tabs)},
    payload = {Formatter.codes(self.payload, tabs)},
    text = {Formatter.codes(self.text, tabs)},
    event_detail = {Formatter.codes(self.event_detail, tabs)},
    family_xref = {Formatter.codes(self.family_xref, tabs)},
    adoption = {Formatter.codes(self.adoption, tabs)},
    phrase = {Formatter.codes(self.phrase, tabs)},
    tag_ext = {Formatter.codes(self.tag_ext, tabs)}
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        tag: Tag = Tag.NONE,
        payload: str = Default.EMPTY,
        text: str = Default.EMPTY,
        event_detail: IndiEvenDetailType = None,
        family_xref: FamilyXref = Void.FAM,
        adoption: Tag = Tag.NONE,
        phrase: PhraseType = None,
        tag_ext: ExtType = None,
    ) -> None:
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
        show: IndividualEvent
        gedcom_docs: str = Specs.INDIVIDUAL_EVENT
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = IndividualEvent(
                    tag=Tag.NONE,
                    payload='',
                    text='',
                    event_detail=None,
                    family_xref=Void.FAM,
                    adoption=Tag.NONE,
                    phrase=None,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = IndividualEvent(
                    tag=Tag.NONE,
                    payload='',
                    text='',
                    event_detail=None,
                    family_xref=Void.FAM,
                    adoption=Tag.NONE,
                    phrase=None,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = IndividualEvent(
                    tag=Tag.NONE,
                    payload='',
                    text='',
                    event_detail=None,
                    family_xref=Void.FAM,
                    adoption=Tag.NONE,
                    phrase=None,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = IndividualEvent(
                    tag=tag,
                    payload=payload,
                    text=text,
                    event_detail=event_detail,
                    family_xref=family_xref,
                    adoption=adoption,
                    phrase=phrase,
                    tag_ext=tag_ext,
                )
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


IndiEvenType = IndividualEvent | list[IndividualEvent] | None


class Alias(NamedTuple):
    """Store, validate and display a GEDCOM Alias structure.

    Data about an individual may be contained in the individual records of other individuals.
    This tag references those other individuals.

    This alias information is defined as its own class because multiple aliases could
    be identified for a single individual.

    Args:
        individual_xref: An individual cross-reference identifier containing information about
            the individual referenced in the individual record.
        phrase: Text associated with this other individual.

    Reference:
        [GEDCOM Individual Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_RECORD)

    > +1 ALIA @<XREF:INDI>@                    {0:M}  [g7:ALIA](https://gedcom.io/terms/v7/ALIA)
    >    +2 PHRASE <Text>                      {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    """

    individual_xref: IndividualXref = Void.INDI
    phrase: PhraseType = None
    alia_ext: ExtType = None

    def validate(self, main_individual: IndividualXref = Void.INDI) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.individual_xref, IndividualXref)
            and Checker.verify_type(self.phrase, Phrase)
            and Checker.verify(
                True,
                self.individual_xref != main_individual,
                Msg.SAME_INDIVIDUAL.format(self.individual_xref.fullname),
            )
            and Checker.verify_ext(Tag.ALIA, self.alia_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(
                lines, level, Tag.ALIA, self.individual_xref.fullname
            )
            lines = Tagger.structure(lines, level + 1, self.alia_ext)
            lines = Tagger.structure(lines, level + 1, self.phrase)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
Alias(
    individual_xref = {Formatter.codes(self.individual_xref, tabs)},
    phrase = {Formatter.codes(self.phrase, tabs)},
    alia_ext = {Formatter.codes(self.alia_ext, tabs)}
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        individual_xref: IndividualXref = Void.INDI,
        phrase: PhraseType = None,
        alia_ext: ExtType = None,
    ) -> None:
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
        show: Alias
        gedcom_docs: str = Specs.ALIAS
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = Alias(
                    individual_xref=Void.INDI,
                    phrase=None,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Alias(
                    individual_xref=Void.INDI,
                    phrase=None,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Alias(
                    individual_xref=Void.INDI,
                    phrase=None,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Alias(
                    individual_xref=individual_xref,
                    phrase=phrase,
                    alia_ext=alia_ext,
                )
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


AliaType = Alias | list[Alias] | None


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

    family_xref: FamilyXref = Void.FAM
    pedigree: str = Default.EMPTY
    pedigree_phrase: PhraseType = None
    status: str = Default.EMPTY
    status_phrase: PhraseType = None
    notes: list[Note] | None = None
    famc_ext: ExtType = None
    pedi_ext: ExtType = None
    stat_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.family_xref, str)
            and Checker.verify_type(self.pedigree, str)
            and Checker.verify_type(self.pedigree_phrase, Phrase)
            and Checker.verify_type(self.status, str)
            and Checker.verify_type(self.status_phrase, Phrase)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_ext(Tag.FAMC, self.famc_ext)
            and Checker.verify_ext(Tag.PEDI, self.pedi_ext)
            and Checker.verify_ext(Tag.STAT, self.stat_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(
                lines, level, Tag.FAMC, str(self.family_xref), format=False
            )
            lines = Tagger.structure(lines, level + 1, self.famc_ext)
            lines = Tagger.string(lines, level + 1, Tag.PEDI, self.pedigree)
            lines = Tagger.structure(lines, level + 1, self.pedi_ext)
            lines = Tagger.structure(lines, level + 2, self.pedigree_phrase)
            lines = Tagger.string(lines, level + 1, Tag.STAT, self.status)
            lines = Tagger.structure(lines, level + 2, self.stat_ext)
            lines = Tagger.structure(lines, level + 2, self.status_phrase)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
FamilyChild(
    family_xref = {Formatter.codes(self.family_xref, tabs)},
    pedigree = {Formatter.codes(self.pedigree, tabs)},
    pedigree_phrase = {Formatter.codes(self.pedigree_phrase, tabs)},
    status = {Formatter.codes(self.status, tabs)},
    status_phrase = {Formatter.codes(self.status_phrase, tabs)},
    notes = {Formatter.codes(self.notes, tabs)},
    famc_ext = {Formatter.codes(self.famc_ext, tabs)},
    pedi_ext = {Formatter.codes(self.pedi_ext, tabs)},
    stat_ext = {Formatter.codes(self.stat_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        family_xref: FamilyXref = Void.FAM,
        pedigree: str = Default.EMPTY,
        pedigree_phrase: PhraseType = None,
        status: str = Default.EMPTY,
        status_phrase: PhraseType = None,
        notes: list[Note] | None = None,
        famc_ext: ExtType = None,
        pedi_ext: ExtType = None,
        stat_ext: ExtType = None,
    ) -> None:
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
        show: FamilyChild
        gedcom_docs: str = Specs.FAMILY_CHILD
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = FamilyChild(
                    family_xref=Void.FAM,
                    pedigree='',
                    pedigree_phrase=None,
                    status='',
                    status_phrase=None,
                    notes=None,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = FamilyChild(
                    family_xref=Void.FAM,
                    pedigree='',
                    pedigree_phrase=None,
                    status='',
                    status_phrase=None,
                    notes=None,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = FamilyChild(
                    family_xref=Void.FAM,
                    pedigree='',
                    pedigree_phrase=None,
                    status='',
                    status_phrase=None,
                    notes=None,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = FamilyChild(
                    family_xref=family_xref,
                    pedigree=pedigree,
                    pedigree_phrase=pedigree_phrase,
                    status=status,
                    status_phrase=status_phrase,
                    notes=notes,
                    famc_ext=famc_ext,
                    pedi_ext=pedi_ext,
                    stat_ext=stat_ext,
                )
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


FamcType = FamilyChild | list[FamilyChild] | None


class FamilySpouse(NamedTuple):
    """Store, validate and display the GEDCOM Family Spouse structure.

    > +1 FAMS @<XREF:FAM>@                     {0:M}  g7:FAMS
    >    +2 <<NOTE_STRUCTURE>>                 {0:M}
    """

    family_xref: FamilyXref = Void.FAM
    notes: list[Note] | None = None
    fams_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.family_xref, FamilyXref)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_ext(Tag.FAMS, self.fams_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(
                lines, level, Tag.FAMS, str(self.family_xref), format=False
            )
            lines = Tagger.structure(lines, level + 1, self.fams_ext)
            lines = Tagger.structure(lines, level + 1, self.notes)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
FamilySpouse(
    family_xref = {Formatter.codes(self.family_xref, tabs)},
    notes = {Formatter.codes(self.notes, tabs)},
    fams_ext = {Formatter.codes(self.fams_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        family_xref: FamilyXref = Void.FAM,
        notes: list[Note] | None = None,
        fams_ext: ExtType = None,
    ) -> None:
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
        show: FamilySpouse
        gedcom_docs: str = Specs.FAMILY_SPOUSE
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = FamilySpouse(
                    family_xref=Void.FAM,
                    notes=None,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = FamilySpouse(
                    family_xref=Void.FAM,
                    notes=None,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = FamilySpouse(
                    family_xref=Void.FAM,
                    notes=None,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = FamilySpouse(
                    family_xref=family_xref,
                    notes=notes,
                    fams_ext=fams_ext,
                )
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


FamsType = FamilySpouse | list[FamilySpouse] | None


class FileTranslation(NamedTuple):
    """Store, validate and display the GEDCOM File structure.

    Reference:
        [GEDCOM Multimedia Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#MULTIMEDIA_RECORD)
    > +1 FILE <FilePath>                       {1:M}  g7:FILE
    >    +2 FORM <MediaType>                   {1:1}  g7:FORM
    >       +3 MEDI <Enum>                     {0:1}  g7:MEDI
    >          +4 PHRASE <Text>                {0:1}  g7:PHRASE
    >    +2 TITL <Text>                        {0:1}  g7:TITL
    >    +2 TRAN <FilePath>                    {0:M}  g7:FILE-TRAN
    >       +3 FORM <MediaType>                {1:1}  g7:FORM
    """

    tran: str = Default.EMPTY
    form: Tag = Tag.NONE
    tran_ext: ExtType = None
    form_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.tran, str)
            and Checker.verify_enum(self.form, MediaType)
            and Checker.verify_ext(Tag.TRAN, self.tran_ext)
            and Checker.verify_ext(Tag.FORM, self.form_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.TRAN, self.tran)
            lines = Tagger.structure(lines, level + 1, self.tran_ext)
            lines = Tagger.string(lines, level + 1, Tag.FORM, self.form.value)
            lines = Tagger.structure(lines, level + 2, self.form_ext)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
FileTranslation(
    tran = {Formatter.codes(self.tran, tabs)},
    form = {Formatter.codes(self.form, tabs)},
    tran_ext = {Formatter.codes(self.tran_ext, tabs)},
    form_ext = {Formatter.codes(self.form_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        tran: str = Default.EMPTY,
        form: Tag = Tag.NONE,
        tran_ext: ExtType = None,
        form_ext: ExtType = None,
    ) -> None:
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
        show: FileTranslation
        gedcom_docs: str = Specs.FILE_TRANSLATION
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = FileTranslation(
                    tran='',
                    form=Tag.NONE,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = FileTranslation(
                    tran='',
                    form=Tag.NONE,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = FileTranslation(
                    tran='',
                    form=Tag.NONE,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = FileTranslation(
                    tran=tran,
                    form=form,
                    tran_ext=tran_ext,
                    form_ext=form_ext,
                )
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


FileTranType = FileTranslation | list[FileTranslation] | None


class File(NamedTuple):
    """Store, validate and display the GEDCOM File structure.

    Multiple files may be used in a Multimedia Record, but at least one exists.

    Reference:
        [GEDCOM Multimedia Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#MULTIMEDIA_RECORD)
    > +1 FILE <FilePath>                       {1:M}  g7:FILE
    >    +2 FORM <MediaType>                   {1:1}  g7:FORM
    >       +3 MEDI <Enum>                     {0:1}  g7:MEDI
    >          +4 PHRASE <Text>                {0:1}  g7:PHRASE
    >    +2 TITL <Text>                        {0:1}  g7:TITL
    >    +2 TRAN <FilePath>                    {0:M}  g7:FILE-TRAN
    >       +3 FORM <MediaType>                {1:1}  g7:FORM
    """

    file: str = Default.EMPTY
    form: Tag = Tag.NONE
    medi: Tag = Tag.NONE
    phrase: PhraseType = None
    titl: str = Default.EMPTY
    file_translations: FileTranType = None
    file_ext: ExtType = None
    form_ext: ExtType = None
    medi_ext: ExtType = None
    titl_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.file, str)
            and Checker.verify_enum(self.form, MediaType)
            and Checker.verify_enum(self.medi, Medium)
            and Checker.verify_type(self.phrase, Phrase)
            and Checker.verify_type(self.titl, str)
            and Checker.verify_type(self.file_translations, FileTranslation)
            and Checker.verify_ext(Tag.FILE, self.file_ext)
            and Checker.verify_ext(Tag.FORM, self.form_ext)
            and Checker.verify_ext(Tag.MEDI, self.medi_ext)
            and Checker.verify_ext(Tag.TITL, self.titl_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.FILE, self.file)
            lines = Tagger.structure(lines, level + 1, self.file_ext)
            lines = Tagger.string(lines, level + 1, Tag.FORM, self.form.value)
            lines = Tagger.structure(lines, level + 2, self.form_ext)
            lines = Tagger.string(lines, level + 3, Tag.MEDI, self.medi.value)
            lines = Tagger.structure(lines, level + 4, self.medi_ext)
            lines = Tagger.structure(lines, level + 4, self.phrase)
            lines = Tagger.string(lines, level + 1, Tag.TITL, self.titl)
            lines = Tagger.structure(lines, level + 2, self.titl_ext)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
File(
    file = {Formatter.codes(self.file, tabs)},
    form = {Formatter.codes(self.form, tabs)},
    medi = {Formatter.codes(self.medi, tabs)},
    phrase = {Formatter.codes(self.phrase, tabs)},
    titl = {Formatter.codes(self.titl, tabs)},
    file_translations = {Formatter.codes(self.file_translations, tabs)},
    file_ext = {Formatter.codes(self.file_ext, tabs)},
    form_ext = {Formatter.codes(self.form_ext, tabs)},
    medi_ext = {Formatter.codes(self.medi_ext, tabs)},
    titl_ext = {Formatter.codes(self.titl_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        file: str = Default.EMPTY,
        form: Tag = Tag.NONE,
        medi: Tag = Tag.NONE,
        phrase: PhraseType = None,
        titl: str = Default.EMPTY,
        file_translations: FileTranType = None,
        file_ext: ExtType = None,
        form_ext: ExtType = None,
        medi_ext: ExtType = None,
        titl_ext: ExtType = None,
    ) -> None:
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
        show: File
        gedcom_docs: str = Specs.FILE
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = File(
                    file='',
                    form=Tag.NONE,
                    medi=Tag.NONE,
                    phrase=None,
                    titl='',
                    file_translations=None,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = File(
                    file='',
                    form=Tag.NONE,
                    medi=Tag.NONE,
                    phrase=None,
                    titl='',
                    file_translations=None,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = File(
                    file='',
                    form=Tag.NONE,
                    medi=Tag.NONE,
                    phrase=None,
                    titl='',
                    file_translations=None,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = File(
                    file=file,
                    form=form,
                    medi=medi,
                    phrase=phrase,
                    titl=titl,
                    file_translations=file_translations,
                    file_ext=file_ext,
                    form_ext=form_ext,
                    medi_ext=medi_ext,
                    titl_ext=titl_ext,
                )
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


FileType = File | list[File] | None


class SourceDataEvent(NamedTuple):
    """Store, validate and display the GEDCOM Source Event structure.

    This is an optional part of the Source.Data Record placed as a separate class
    because there may be many of these events.

    Reference:
        [GEDCOM Source Event](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_RECORD)

    >   +1 DATA                                  {0:1}  [g7:DATA]()
    >      +2 EVEN <List:Enum>                   {0:M}  [g7:DATA-EVEN]()
    >         +3 DATE <DatePeriod>               {0:1}  [g7:DATA-EVEN-DATE]()
    >            +4 PHRASE <Text>                {0:1}  [g7:PHRASE]()
    >         +3 <<PLACE_STRUCTURE>>             {0:1}
    >      +2 AGNC <Text>                        {0:1}  [g7:AGNC]()
    >      +2 <<NOTE_STRUCTURE>>                 {0:M}
    """

    event: Tag = Tag.NONE
    date_period: str = Default.EMPTY
    phrase: PhraseType = None
    place: PlacType = None
    even_ext: ExtType = None
    date_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_enum(self.event, EvenAttr)
            and Checker.verify_type(self.date_period, str)
            and Checker.verify_type(self.phrase, Phrase)
            and Checker.verify_type(self.place, str)
            and Checker.verify_ext(Tag.EVEN, self.even_ext)
            and Checker.verify_ext(Tag.DATE, self.date_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.EVEN, self.event.value)
            lines = Tagger.structure(lines, level + 1, self.even_ext)
            lines = Tagger.string(lines, level + 1, Tag.DATE, self.date_period)
            lines = Tagger.structure(lines, level + 2, self.date_ext)
            lines = Tagger.structure(lines, level + 2, self.phrase)
            lines = Tagger.structure(lines, level + 2, self.place)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
SourceDataEvent(
    event = {Formatter.codes(self.event, tabs)},
    date_period = {Formatter.codes(self.date_period, tabs)},
    phrase = {Formatter.codes(self.phrase, tabs)},
    place = {Formatter.codes(self.place, tabs)},
    even_ext = {Formatter.codes(self.even_ext, tabs)},
    date_ext = {Formatter.codes(self.date_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        event: Tag = Tag.NONE,
        date_period: str = Default.EMPTY,
        phrase: PhraseType = None,
        place: PlacType = None,
        even_ext: ExtType = None,
        date_ext: ExtType = None,
    ) -> None:
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
        show: SourceDataEvent
        gedcom_docs: str = Specs.SOURCE_EVENT
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = SourceDataEvent(
                    event=Tag.NONE,
                    date_period='',
                    phrase=None,
                    place=Place(),
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = SourceDataEvent(
                    event=Tag.NONE,
                    date_period='',
                    phrase=None,
                    place=Place(),
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = SourceDataEvent(
                    event=Tag.NONE,
                    date_period='',
                    phrase=None,
                    place=Place(),
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = SourceDataEvent(
                    event=event,
                    date_period=date_period,
                    phrase=phrase,
                    place=place,
                    even_ext=even_ext,
                    date_ext=date_ext,
                )
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


SourDataEvenType = SourceDataEvent | list[SourceDataEvent] | None


class NonEvent(NamedTuple):
    """Store, validate and display a GEDCOM Non Event structure.

    > n NO <Enum>                                {1:1}  [g7:NO](https://gedcom.io/terms/v7/NO)
    >   +1 DATE <DatePeriod>                     {0:1}  [g7:NO-DATE](https://gedcom.io/terms/v7/NO-DATE)
    >      +2 PHRASE <Text>                      {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    >   +1 <<NOTE_STRUCTURE>>                    {0:M}
    >   +1 <<SOURCE_CITATION>>                   {0:M}
    """

    no: Tag = Tag.NONE
    date: DateType = None
    phrase: PhraseType = None
    notes: NoteType = None
    sources: SourCiteType = None
    no_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_enum(self.no, Even)
            and Checker.verify_type(self.date, Date | None)
            and Checker.verify_type(self.phrase, Phrase)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_type(self.sources, SourceCitation)
            and Checker.verify_ext(Tag.NO, self.no_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.NO, self.no.value)
            lines = Tagger.structure(lines, level + 1, self.no_ext)
            lines = Tagger.structure(lines, level + 1, self.date)
            lines = Tagger.structure(lines, level + 2, self.phrase)
            lines = Tagger.structure(lines, level + 2, self.notes)
            lines = Tagger.structure(lines, level + 2, self.sources)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
NonEvent(
    no = {Formatter.codes(self.no, tabs)},
    date = {Formatter.codes(self.date, tabs)},
    phrase = {Formatter.codes(self.phrase, tabs)},
    notes = {Formatter.codes(self.notes, tabs)},
    sources = {Formatter.codes(self.sources, tabs)},
    no_ext = {Formatter.codes(self.no_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        no: Tag = Tag.NONE,
        date: DateType = None,
        phrase: PhraseType = None,
        notes: NoteType = None,
        sources: SourCiteType = None,
        no_ext: ExtType = None,
    ) -> None:
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
        show: NonEvent
        gedcom_docs: str = Specs.NON_EVENT
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = NonEvent(
                    no=Tag.NONE,
                    date=Date(),
                    phrase=None,
                    notes=None,
                    sources=None,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = NonEvent(
                    no=Tag.NONE,
                    date=Date(),
                    phrase=None,
                    notes=None,
                    sources=None,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = NonEvent(
                    no=Tag.NONE,
                    date=Date(),
                    phrase=None,
                    notes=None,
                    sources=None,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = NonEvent(
                    no=no,
                    date=date,
                    phrase=phrase,
                    notes=notes,
                    sources=sources,
                    no_ext=no_ext,
                )
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


NoType = NonEvent | list[NonEvent] | None


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
    name: str = Default.EMPTY
    address: AddrType = None
    phones: PhoneType = None
    emails: EmailType = None
    faxes: FaxType = None
    wwws: WWWType = None
    multimedia_links: MMLinkType = None
    languages: LangType = None
    identifiers: IdenType = None
    notes: NoteType = None
    change: ChangeDateType = None
    creation: CreationDateType = None
    name_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.xref, SubmitterXref)
            and Checker.verify_type(self.name, str)
            and Checker.verify_type(self.address, Address)
            and Checker.verify_type(self.phones, Phone)
            and Checker.verify_type(self.emails, Email)
            and Checker.verify_type(self.faxes, Fax)
            and Checker.verify_type(self.wwws, WWW)
            and Checker.verify_type(self.multimedia_links, MultimediaLink)
            and Checker.verify_type(self.languages, Lang)
            and Checker.verify_type(self.identifiers, Identifier)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_type(self.change, ChangeDate | None)
            and Checker.verify_type(self.creation, CreationDate | None)
            and Checker.verify_ext(Tag.NAME, self.name_ext)
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged()
        if str(self.xref) != Void.NAME and self.validate():
            lines = Tagger.string(lines, level + 1, Tag.NAME, self.name)
            lines = Tagger.structure(lines, level + 2, self.name_ext)
            lines = Tagger.structure(lines, level + 1, self.address)
            lines = Tagger.structure(lines, level + 1, self.phones)
            lines = Tagger.structure(lines, level + 1, self.emails)
            lines = Tagger.structure(lines, level + 1, self.faxes)
            lines = Tagger.structure(lines, level + 1, self.wwws)
            lines = Tagger.structure(lines, level + 1, self.multimedia_links)
            lines = Tagger.structure(lines, level + 1, self.languages)
            lines = Tagger.structure(lines, level + 1, self.identifiers)
            lines = Tagger.structure(lines, level + 1, self.notes)
            lines = Tagger.structure(lines, level + 1, self.change)
            lines = Tagger.structure(lines, level + 1, self.creation)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
Submitter(
    xref = {Formatter.codes(self.xref, tabs)},
    name = {Formatter.codes(self.name, tabs)},
    address = {Formatter.codes(self.address, tabs)},
    phones = {Formatter.codes(self.phones, tabs)},
    emails = {Formatter.codes(self.emails, tabs)},
    faxes = {Formatter.codes(self.faxes, tabs)},
    wwws = {Formatter.codes(self.wwws, tabs)},
    multimedia_links = {Formatter.codes(self.multimedia_links, tabs)},
    languages = {Formatter.codes(self.languages, tabs)},
    identifiers = {Formatter.codes(self.identifiers, tabs)},
    notes = {Formatter.codes(self.notes, tabs)},
    change = {Formatter.codes(self.change, tabs)},
    creation = {Formatter.codes(self.creation, tabs)},
    name_ext = {Formatter.codes(self.name_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        xref: SubmitterXref = Void.SUBM,
        name: str = Default.EMPTY,
        address: AddrType = None,
        phones: PhoneType = None,
        emails: EmailType = None,
        faxes: FaxType = None,
        wwws: WWWType = None,
        multimedia_links: MMLinkType = None,
        languages: LangType = None,
        identifiers: IdenType = None,
        notes: NoteType = None,
        change: ChangeDateType = None,
        creation: CreationDateType = None,
        name_ext: ExtType = None,
    ) -> None:
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
        show: Submitter
        gedcom_docs: str = Specs.SUBMITTER
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = Submitter(
                    xref=Void.SUBM,
                    name='',
                    address=Address(),
                    phones=None,
                    emails=None,
                    faxes=None,
                    wwws=None,
                    multimedia_links=None,
                    languages=None,
                    identifiers=None,
                    notes=None,
                    change=None,
                    creation=None,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Submitter(
                    xref=Void.SUBM,
                    name='',
                    address=Address(),
                    phones=None,
                    emails=None,
                    faxes=None,
                    wwws=None,
                    multimedia_links=None,
                    languages=None,
                    identifiers=None,
                    notes=None,
                    change=None,
                    creation=None,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Submitter(
                    xref=Void.SUBM,
                    name='',
                    address=Address(),
                    phones=None,
                    emails=None,
                    faxes=None,
                    wwws=None,
                    multimedia_links=None,
                    languages=None,
                    identifiers=None,
                    notes=None,
                    change=None,
                    creation=None,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Submitter(
                    xref=xref,
                    name=name,
                    address=address,
                    phones=phones,
                    emails=emails,
                    faxes=faxes,
                    wwws=wwws,
                    multimedia_links=multimedia_links,
                    languages=languages,
                    identifiers=identifiers,
                    notes=notes,
                    change=change,
                    creation=creation,
                    name_ext=name_ext,
                )
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
    resn: Tag = Tag.NONE
    attributes: FamAttrType = None
    events: FamEvenType = None
    husband: IndividualXref = Void.INDI
    husband_phrase: PhraseType = None
    wife: IndividualXref = Void.INDI
    wife_phrase: PhraseType = None
    children: ChilType = None
    associations: AssoType = None
    submitters: StrList = None
    lds_spouse_sealings: LDSSpouSealingType = None
    identifiers: IdenType = None
    notes: NoteType = None
    citations: SourCiteType = None
    multimedia_links: MMLinkType = None
    change: ChangeDateType = None
    creation: CreationDateType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.xref, FamilyXref)
            and Checker.verify_enum(self.resn, Resn)
            and Checker.verify_type(self.attributes, FamilyAttribute)
            and Checker.verify_type(self.events, FamilyEvent)
            and Checker.verify_type(self.husband, IndividualXref)
            and Checker.verify_type(self.husband_phrase, Phrase)
            and Checker.verify_type(self.wife, IndividualXref)
            and Checker.verify_type(self.wife_phrase, Phrase)
            and Checker.verify_type(self.children, Child)
            and Checker.verify_type(self.associations, Association)
            and Checker.verify_type(self.submitters, SubmitterXref)
            and Checker.verify_type(self.lds_spouse_sealings, LDSSpouseSealing)
            and Checker.verify_type(self.identifiers, Identifier)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_type(self.citations, SourceCitation)
            and Checker.verify_type(self.multimedia_links, MultimediaLink)
            and Checker.verify_type(self.change, ChangeDate)
            and Checker.verify_type(self.creation, CreationDate)
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged()
        if self.validate():
            if self.resn != Tag.NONE:
                lines = ''.join(
                    [lines, Tagger.taginfo(level, Tag.RESN, self.resn.value)]
                )
            lines = Tagger.structure(lines, level, self.attributes)
            lines = Tagger.structure(lines, level, self.events)
            if str(self.husband) != str(Void.INDI):
                lines = Tagger.string(
                    lines, level + 1, Tag.HUSB, str(self.husband), format=False
                )
                lines = Tagger.structure(lines, level + 2, self.husband_phrase)
            if str(self.wife) != str(Void.INDI):
                lines = Tagger.string(
                    lines, level + 1, Tag.WIFE, str(self.wife), format=False
                )
                lines = Tagger.structure(lines, level + 2, self.wife_phrase)
            lines = Tagger.structure(lines, level + 1, self.children)
            lines = Tagger.structure(lines, level + 1, self.associations)
            lines = Tagger.string(
                lines, level, Tag.SUBM, self.submitters, format=False
            )
            lines = Tagger.structure(lines, level + 1, self.lds_spouse_sealings)
            lines = Tagger.structure(lines, level + 1, self.identifiers)
            lines = Tagger.structure(lines, level + 1, self.notes)
            lines = Tagger.structure(lines, level + 1, self.citations)
            lines = Tagger.structure(lines, level + 1, self.multimedia_links)
            lines = Tagger.structure(lines, level + 1, self.change)
            lines = Tagger.structure(lines, level + 1, self.creation)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
Family(
    xref = {Formatter.codes(self.xref, tabs)},
    resn = {Formatter.codes(self.resn, tabs)},
    attributes = {Formatter.codes(self.attributes, tabs)},
    events = {Formatter.codes(self.events, tabs)},
    husband = {Formatter.codes(self.husband, tabs)},
    husband_phrase = {Formatter.codes(self.husband_phrase, tabs)},
    wife = {Formatter.codes(self.wife, tabs)},
    wife_phrase = {Formatter.codes(self.wife_phrase, tabs)},
    children = {Formatter.codes(self.children, tabs)},
    associations = {Formatter.codes(self.associations, tabs)},
    submitters = {Formatter.codes(self.submitters, tabs)},
    lds_spouse_sealings = {Formatter.codes(self.lds_spouse_sealings, tabs)},
    identifiers = {Formatter.codes(self.identifiers, tabs)},
    notes = {Formatter.codes(self.notes, tabs)},
    citations = {Formatter.codes(self.citations, tabs)},
    multimedia_links = {Formatter.codes(self.multimedia_links, tabs)},
    change = {Formatter.codes(self.change, tabs)}
    creation = {Formatter.codes(self.creation, tabs)}
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        xref: FamilyXref = Void.FAM,
        resn: Tag = Tag.NONE,
        attributes: FamAttrType = None,
        events: FamEvenType = None,
        husband: IndividualXref = Void.INDI,
        husband_phrase: PhraseType = None,
        wife: IndividualXref = Void.INDI,
        wife_phrase: PhraseType = None,
        children: ChilType = None,
        associations: AssoType = None,
        submitters: StrList = None,
        lds_spouse_sealings: LDSSpouSealingType = None,
        identifiers: IdenType = None,
        notes: NoteType = None,
        citations: SourCiteType = None,
        multimedia_links: MMLinkType = None,
        change: ChangeDateType = None,
        creation: CreationDateType = None,
    ) -> None:
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
        show: Family
        gedcom_docs: str = Specs.FAMILY
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = Family(
                    xref=Void.FAM,
                    resn=Tag.NONE,
                    attributes=None,
                    husband=Void.INDI,
                    husband_phrase=None,
                    wife=Void.INDI,
                    wife_phrase=None,
                    children=None,
                    associations=None,
                    submitters=None,
                    lds_spouse_sealings=None,
                    identifiers=None,
                    notes=None,
                    citations=None,
                    multimedia_links=None,
                    change=None,
                    creation=None,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Family(
                    xref=Void.FAM,
                    resn=Tag.NONE,
                    attributes=None,
                    husband=Void.INDI,
                    husband_phrase=None,
                    wife=Void.INDI,
                    wife_phrase=None,
                    children=None,
                    associations=None,
                    submitters=None,
                    lds_spouse_sealings=None,
                    identifiers=None,
                    notes=None,
                    citations=None,
                    multimedia_links=None,
                    change=None,
                    creation=None,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Family(
                    xref=Void.FAM,
                    resn=Tag.NONE,
                    attributes=None,
                    husband=Void.INDI,
                    husband_phrase=None,
                    wife=Void.INDI,
                    wife_phrase=None,
                    children=None,
                    associations=None,
                    submitters=None,
                    lds_spouse_sealings=None,
                    identifiers=None,
                    notes=None,
                    citations=None,
                    multimedia_links=None,
                    change=None,
                    creation=None,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Family(
                    xref=xref,
                    resn=resn,
                    attributes=attributes,
                    events=events,
                    husband=husband,
                    husband_phrase=husband_phrase,
                    wife=wife,
                    wife_phrase=wife_phrase,
                    children=children,
                    associations=associations,
                    submitters=submitters,
                    lds_spouse_sealings=lds_spouse_sealings,
                    identifiers=identifiers,
                    notes=notes,
                    citations=citations,
                    multimedia_links=multimedia_links,
                    change=change,
                    creation=creation,
                )
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
    resn: Tag = Tag.NONE
    files: FileType = None
    identifiers: IdenType = None
    notes: NoteType = None
    sources: SourCiteType = None
    change: ChangeDateType = None
    creation: CreationDateType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.xref, MultimediaXref)
            and Checker.verify_enum(self.resn, Resn)
            and Checker.verify_type(self.files, File)
            and Checker.verify_type(self.identifiers, Identifier)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_type(self.sources, Source)
            and Checker.verify_type(self.change, ChangeDate | None)
            and Checker.verify_type(self.creation, CreationDate | None)
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged()
        if self.validate():
            lines = Tagger.string(lines, level + 1, Tag.RESN, self.resn.value)
            lines = Tagger.structure(lines, level + 1, self.files)
            lines = Tagger.structure(lines, level + 1, self.identifiers)
            lines = Tagger.structure(lines, level + 1, self.notes)
            lines = Tagger.structure(lines, level + 1, self.sources)
            lines = Tagger.structure(lines, level + 1, self.change)
            lines = Tagger.structure(lines, level + 1, self.creation)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
Multimedia(
    xref = {Formatter.codes(self.xref, tabs)},
    resn = {Formatter.codes(self.resn, tabs)},
    files = {Formatter.codes(self.files, tabs)},
    identifiers = {Formatter.codes(self.identifiers, tabs)},
    notes = {Formatter.codes(self.notes, tabs)},
    sources = {Formatter.codes(self.sources, tabs)},
    change = {Formatter.codes(self.change, tabs)}
    creation = {Formatter.codes(self.creation, tabs)}
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        xref: MultimediaXref = Void.OBJE,
        resn: Tag = Tag.NONE,
        files: FileType = None,
        identifiers: IdenType = None,
        notes: NoteType = None,
        sources: SourCiteType = None,
        change: ChangeDateType = None,
        creation: CreationDateType = None,
    ) -> None:
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
        show: Multimedia
        gedcom_docs: str = Specs.MULTIMEDIA
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = Multimedia(
                    xref=Void.OBJE,
                    resn=Tag.NONE,
                    files=None,
                    identifiers=None,
                    notes=None,
                    sources=None,
                    change=None,
                    creation=None,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Multimedia(
                    xref=Void.OBJE,
                    resn=Tag.NONE,
                    files=None,
                    identifiers=None,
                    notes=None,
                    sources=None,
                    change=None,
                    creation=None,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Multimedia(
                    xref=Void.OBJE,
                    resn=Tag.NONE,
                    files=None,
                    identifiers=None,
                    notes=None,
                    sources=None,
                    change=None,
                    creation=None,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Multimedia(
                    xref=xref,
                    resn=resn,
                    files=files,
                    identifiers=identifiers,
                    notes=notes,
                    sources=sources,
                    change=change,
                    creation=creation,
                )
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
    source_data_events: list[SourceDataEvent] | None = None
    agency: str = Default.EMPTY
    data_notes: NoteType = None
    author: str = Default.EMPTY
    title: str = Default.EMPTY
    abbreviation: str = Default.EMPTY
    published: str = Default.EMPTY
    text: str = Default.EMPTY
    mime: MediaType = MediaType.NONE
    language: LangType = None
    repositories: list[Any] | None = None
    identifiers: IdenType = None
    notes: NoteType = None
    multimedia_links: MMLinkType = None
    change: ChangeDateType = None
    creation: CreationDateType = None
    data_ext: ExtType = None
    agnc_ext: ExtType = None
    auth_ext: ExtType = None
    titl_ext: ExtType = None
    abbr_ext: ExtType = None
    publ_ext: ExtType = None
    text_ext: ExtType = None
    mime_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.xref, SourceXref)
            and Checker.verify_type(self.author, str)
            and Checker.verify_type(self.title, str)
            and Checker.verify_type(self.abbreviation, str)
            and Checker.verify_type(self.published, str)
            and Checker.verify_type(self.text, str)
            and Checker.verify_type(self.mime, MediaType)
            and Checker.verify_type(self.language, str)
            and Checker.verify_type(self.repositories, Repository)
            and Checker.verify_type(self.identifiers, Identifier)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_type(self.multimedia_links, MultimediaLink)
            and Checker.verify_type(self.change, ChangeDate | None)
            and Checker.verify_type(self.creation, CreationDate | None)
            and Checker.verify_ext(Tag.DATA, self.data_ext)
            and Checker.verify_ext(Tag.AGNC, self.agnc_ext)
            and Checker.verify_ext(Tag.AUTH, self.auth_ext)
            and Checker.verify_ext(Tag.TITL, self.titl_ext)
            and Checker.verify_ext(Tag.ABBR, self.abbr_ext)
            and Checker.verify_ext(Tag.PUBL, self.publ_ext)
            and Checker.verify_ext(Tag.TEXT, self.text_ext)
            and Checker.verify_ext(Tag.MIME, self.mime_ext)
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged()
        if self.validate():
            if (
                self.source_data_events is not None
                or self.agency != Default.EMPTY
                or self.notes is not None
            ):
                lines = Tagger.empty(lines, level + 1, Tag.DATA)
                lines = Tagger.structure(lines, level + 2, self.data_ext)
                lines = Tagger.structure(
                    lines, level + 2, self.source_data_events
                )
                lines = Tagger.string(lines, level + 2, Tag.AGNC, self.agency)
                lines = Tagger.structure(lines, level + 3, self.agnc_ext)
                lines = Tagger.structure(lines, level + 1, self.notes)
            lines = Tagger.string(lines, level + 1, Tag.AUTH, self.author)
            lines = Tagger.structure(lines, level + 2, self.auth_ext)
            lines = Tagger.string(lines, level + 1, Tag.TITL, self.title)
            lines = Tagger.structure(lines, level + 2, self.titl_ext)
            lines = Tagger.string(lines, level + 1, Tag.ABBR, self.abbreviation)
            lines = Tagger.structure(lines, level + 2, self.abbr_ext)
            lines = Tagger.string(lines, level + 1, Tag.PUBL, self.published)
            lines = Tagger.structure(lines, level + 2, self.publ_ext)
            lines = Tagger.string(lines, level + 1, Tag.TEXT, self.text)
            lines = Tagger.structure(lines, level + 2, self.text_ext)
            lines = Tagger.string(lines, level + 2, Tag.MIME, self.mime.value)
            lines = Tagger.structure(lines, level + 3, self.mime_ext)
            lines = Tagger.structure(lines, level + 2, self.language)
            lines = Tagger.structure(lines, level + 1, self.repositories)
            lines = Tagger.structure(lines, level + 1, self.identifiers)
            lines = Tagger.structure(lines, level + 1, self.notes)
            lines = Tagger.structure(lines, level + 1, self.multimedia_links)
            lines = Tagger.structure(lines, level + 1, self.change)
            lines = Tagger.structure(lines, level + 1, self.creation)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
Source(
    xref = {Formatter.codes(self.xref, tabs)},
    source_data_events = {Formatter.codes(self.source_data_events, tabs)}
    agency = {Formatter.codes(self.agency, tabs)}
    data_notes = {Formatter.codes(self.data_notes, tabs)}
    author = {Formatter.codes(self.author, tabs)},
    title = {Formatter.codes(self.title, tabs)},
    abbreviation = {Formatter.codes(self.abbreviation, tabs)},
    published = {Formatter.codes(self.published, tabs)},
    text = {Formatter.codes(self.text, tabs)},
    repositories = {Formatter.codes(self.repositories, tabs)},
    identifiers = {Formatter.codes(self.identifiers, tabs)},
    notes = {Formatter.codes(self.notes, tabs)},
    multimedia_links = {Formatter.codes(self.multimedia_links, tabs)},
    change = {Formatter.codes(self.change, tabs)}
    creation = {Formatter.codes(self.creation, tabs)}
    data_ext = {Formatter.codes(self.data_ext, tabs)}
    agnc_ext = {Formatter.codes(self.agnc_ext, tabs)}
    auth_ext = {Formatter.codes(self.auth_ext, tabs)}
    titl_ext = {Formatter.codes(self.titl_ext, tabs)}
    abbr_ext = {Formatter.codes(self.abbr_ext, tabs)}
    publ_ext = {Formatter.codes(self.publ_ext, tabs)}
    text_ext = {Formatter.codes(self.text_ext, tabs)}
    mime_ext = {Formatter.codes(self.mime_ext, tabs)}
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        xref: SourceXref = Void.SOUR,
        source_data_events: list[SourceDataEvent] | None = None,
        agency: str = Default.EMPTY,
        data_notes: NoteType = None,
        author: str = Default.EMPTY,
        title: str = Default.EMPTY,
        abbreviation: str = Default.EMPTY,
        published: str = Default.EMPTY,
        text: str = Default.EMPTY,
        mime: MediaType = MediaType.NONE,
        language: LangType = None,
        repositories: list[Any] | None = None,
        identifiers: IdenType = None,
        notes: NoteType = None,
        multimedia_links: MMLinkType = None,
        change: ChangeDateType = None,
        creation: CreationDateType = None,
        data_ext: ExtType = None,
        agnc_ext: ExtType = None,
        auth_ext: ExtType = None,
        titl_ext: ExtType = None,
        abbr_ext: ExtType = None,
        publ_ext: ExtType = None,
        text_ext: ExtType = None,
        mime_ext: ExtType = None,
    ) -> None:
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
        show: Source
        gedcom_docs: str = Specs.SOURCE
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = Source(
                    xref=Void.SOUR,
                    source_data_events=None,
                    agency=Default.EMPTY,
                    data_notes=None,
                    author='',
                    title='',
                    abbreviation='',
                    published='',
                    text='',
                    repositories=None,
                    identifiers=None,
                    notes=None,
                    multimedia_links=None,
                    change=None,
                    creation=None,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Source(
                    xref=Void.SOUR,
                    source_data_events=None,
                    agency=Default.EMPTY,
                    data_notes=None,
                    author='',
                    title='',
                    abbreviation='',
                    published='',
                    text='',
                    repositories=None,
                    identifiers=None,
                    notes=None,
                    multimedia_links=None,
                    change=None,
                    creation=None,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Source(
                    xref=Void.SOUR,
                    source_data_events=None,
                    agency=Default.EMPTY,
                    data_notes=None,
                    author='',
                    title='',
                    abbreviation='',
                    published='',
                    text='',
                    repositories=None,
                    identifiers=None,
                    notes=None,
                    multimedia_links=None,
                    change=None,
                    creation=None,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Source(
                    xref=xref,
                    source_data_events=source_data_events,
                    agency=agency,
                    data_notes=data_notes,
                    author=author,
                    title=title,
                    abbreviation=abbreviation,
                    published=published,
                    text=text,
                    mime=mime,
                    language=language,
                    repositories=repositories,
                    identifiers=identifiers,
                    notes=notes,
                    multimedia_links=multimedia_links,
                    change=change,
                    creation=creation,
                    data_ext=data_ext,
                    agnc_ext=agnc_ext,
                    auth_ext=auth_ext,
                    titl_ext=titl_ext,
                    abbr_ext=abbr_ext,
                    publ_ext=publ_ext,
                    text_ext=text_ext,
                    mime_ext=mime_ext,
                )
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
        >>> from genedata.build import Genealogy
        >>> from genedata.store import Association, Individual
        >>> from genedata.gedcom import Role

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
        ...             individual_xref=i2,
        ...             role=Tag.GODP,
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
        TypeError: "@MY_FAMILY@" has type <class 'genedata.store.FamilyXref'> but should have type <class 'genedata.store.IndividualXref'>.

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
    resn: Tag = Tag.NONE
    personal_names: PersonalNameType = None
    sex: Tag = Tag.NONE
    attributes: IndiAttrType = None
    events: IndiEvenType = None
    lds_individual_ordinances: list[LDSIndividualOrdinance] | None = None
    families_child: FamcType = None
    submitters: StrList = None
    associations: AssoType = None
    aliases: AliaType = None
    ancestor_interest: StrList = None
    descendent_interest: StrList = None
    identifiers: IdenType = None
    notes: NoteType = None
    sources: StrList = None
    multimedia_links: MMLinkType = None
    change: ChangeDateType = None
    creation: CreationDateType = None
    resn_ext: ExtType = None
    sex_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.xref, IndividualXref)
            and Checker.verify_enum(self.resn, Resn)
            and Checker.verify_type(self.personal_names, PersonalName)
            and Checker.verify_enum(self.sex, Sex)
            and Checker.verify_type(self.attributes, IndividualAttribute)
            and Checker.verify_type(self.events, IndividualEvent)
            and Checker.verify_type(
                self.lds_individual_ordinances, LDSIndividualOrdinance
            )
            and Checker.verify_type(self.families_child, FamilyChild)
            and Checker.verify_type(self.submitters, str)
            and Checker.verify_type(self.associations, Association)
            and Checker.verify_type(self.aliases, Alias)
            and Checker.verify_type(self.ancestor_interest, str)
            and Checker.verify_type(self.descendent_interest, str)
            and Checker.verify_type(self.identifiers, Identifier)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_type(self.sources, Source)
            and Checker.verify_type(self.multimedia_links, MultimediaLink)
            and Checker.verify_type(self.change, ChangeDate | None)
            and Checker.verify_type(self.creation, CreationDate | None)
            and Checker.verify_ext(Tag.RESN, self.resn_ext)
            and Checker.verify_ext(Tag.SEX, self.sex_ext)
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged()
        if self.validate():
            lines = Tagger.string(lines, level + 1, Tag.RESN, self.resn.value)
            lines = Tagger.structure(lines, level + 2, self.resn_ext)
            lines = Tagger.structure(lines, level + 1, self.personal_names)
            lines = Tagger.string(lines, level + 1, Tag.SEX, self.sex.value)
            lines = Tagger.structure(lines, level + 2, self.sex_ext)
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
            lines = Tagger.structure(lines, level + 1, self.change)
            lines = Tagger.structure(lines, level + 1, self.creation)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
Individual(
    xref = {Formatter.codes(self.xref, tabs)},
    resn = {Formatter.codes(self.resn, tabs)},
    personal_names = {Formatter.codes(self.personal_names, tabs)},
    sex = {Formatter.codes(self.sex, tabs)},
    attributes = {Formatter.codes(self.attributes, tabs)},
    events = {Formatter.codes(self.events, tabs)},
    lds_individual_ordinances = {Formatter.codes(self.lds_individual_ordinances, tabs)},
    submitters = {Formatter.codes(self.submitters, tabs)},
    associations = {Formatter.codes(self.associations, tabs)},
    aliases = {Formatter.codes(self.aliases, tabs)},
    ancestor_interest = {Formatter.codes(self.ancestor_interest, tabs)},
    descendent_interest = {Formatter.codes(self.descendent_interest, tabs)},
    identifiers = {Formatter.codes(self.identifiers, tabs)},
    notes = {Formatter.codes(self.notes, tabs)},
    sources = {Formatter.codes(self.sources, tabs)},
    multimedia_links = {Formatter.codes(self.multimedia_links, tabs)},
    change = {Formatter.codes(self.change, tabs)}
    creation = {Formatter.codes(self.creation, tabs)}
    resn_ext = {Formatter.codes(self.resn_ext, tabs)},
    sex_ext = {Formatter.codes(self.sex_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        xref: IndividualXref = Void.INDI,
        resn: Tag = Tag.NONE,
        personal_names: PersonalNameType = None,
        sex: Tag = Tag.NONE,
        attributes: IndiAttrType = None,
        events: IndiEvenType = None,
        lds_individual_ordinances: list[LDSIndividualOrdinance] | None = None,
        families_child: FamcType = None,
        submitters: StrList = None,
        associations: AssoType = None,
        aliases: AliaType = None,
        ancestor_interest: StrList = None,
        descendent_interest: StrList = None,
        identifiers: IdenType = None,
        notes: NoteType = None,
        sources: StrList = None,
        multimedia_links: MMLinkType = None,
        change: ChangeDateType = None,
        creation: CreationDateType = None,
        resn_ext: ExtType = None,
        sex_ext: ExtType = None,
    ) -> None:
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
        show: Individual
        gedcom_docs: str = Specs.INDIVIDUAL
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = Individual(
                    xref=Void.INDI,
                    resn=Tag.NONE,
                    personal_names=None,
                    sex=Tag.NONE,
                    attributes=None,
                    events=None,
                    lds_individual_ordinances=None,
                    submitters=None,
                    associations=None,
                    aliases=None,
                    ancestor_interest=None,
                    descendent_interest=None,
                    identifiers=None,
                    notes=None,
                    sources=None,
                    multimedia_links=None,
                    change=None,
                    creation=None,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Individual(
                    xref=Void.INDI,
                    resn=Tag.NONE,
                    personal_names=None,
                    sex=Tag.NONE,
                    attributes=None,
                    events=None,
                    lds_individual_ordinances=None,
                    submitters=None,
                    associations=None,
                    aliases=None,
                    ancestor_interest=None,
                    descendent_interest=None,
                    identifiers=None,
                    notes=None,
                    sources=None,
                    multimedia_links=None,
                    change=None,
                    creation=None,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Individual(
                    xref=Void.INDI,
                    resn=Tag.NONE,
                    personal_names=None,
                    sex=Tag.NONE,
                    attributes=None,
                    events=None,
                    lds_individual_ordinances=None,
                    submitters=None,
                    associations=None,
                    aliases=None,
                    ancestor_interest=None,
                    descendent_interest=None,
                    identifiers=None,
                    notes=None,
                    sources=None,
                    multimedia_links=None,
                    change=None,
                    creation=None,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Individual(
                    xref=xref,
                    resn=resn,
                    personal_names=personal_names,
                    sex=sex,
                    attributes=attributes,
                    events=events,
                    lds_individual_ordinances=lds_individual_ordinances,
                    families_child=families_child,
                    submitters=submitters,
                    associations=associations,
                    aliases=aliases,
                    ancestor_interest=ancestor_interest,
                    descendent_interest=descendent_interest,
                    identifiers=identifiers,
                    notes=notes,
                    sources=sources,
                    multimedia_links=multimedia_links,
                    change=change,
                    creation=creation,
                    resn_ext=resn_ext,
                    sex_ext=sex_ext,
                )
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
    name: str = Default.EMPTY
    address: AddrType = None
    phones: PhoneType = None
    emails: EmailType = None
    faxes: FaxType = None
    wwws: WWWType = None
    notes: NoteType = None
    identifiers: IdenType = None
    change: ChangeDateType = None
    creation: CreationDateType = None
    name_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.xref, RepositoryXref)
            and Checker.verify_type(self.name, str)
            and Checker.verify_type(self.address, Address)
            and Checker.verify_type(self.phones, Phone)
            and Checker.verify_type(self.emails, Email)
            and Checker.verify_type(self.faxes, Fax)
            and Checker.verify_type(self.wwws, WWW)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_type(self.identifiers, Identifier)
            and Checker.verify_type(self.change, ChangeDate | None)
            and Checker.verify_type(self.creation, CreationDate | None)
            and Checker.verify_ext(Tag.RESN, self.name_ext)
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged()
        if self.validate():
            lines = Tagger.string(lines, level, Tag.NAME, self.name)
            lines = Tagger.structure(lines, level + 1, self.name_ext)
            lines = Tagger.structure(lines, level, self.address)
            lines = Tagger.structure(lines, level, self.phones)
            lines = Tagger.structure(lines, level, self.emails)
            lines = Tagger.structure(lines, level, self.faxes)
            lines = Tagger.structure(lines, level, self.wwws)
            lines = Tagger.structure(lines, level, self.change)
            lines = Tagger.structure(lines, level, self.creation)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
Repository(
    xref = {Formatter.codes(self.xref, tabs)},
    name = {Formatter.codes(self.name, tabs)},
    address = {Formatter.codes(self.address, tabs)},
    phones = {Formatter.codes(self.phones, tabs)},
    emails = {Formatter.codes(self.emails, tabs)},
    faxes = {Formatter.codes(self.faxes, tabs)},
    wwws = {Formatter.codes(self.wwws, tabs)},
    notes = {Formatter.codes(self.notes, tabs)},
    identifiers = {Formatter.codes(self.identifiers, tabs)},
    change = {Formatter.codes(self.change, tabs)},
    creation = {Formatter.codes(self.creation, tabs)},
    name_ext = {Formatter.codes(self.name_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        xref: RepositoryXref = Void.REPO,
        name: str = Default.EMPTY,
        address: AddrType = None,
        phones: PhoneType = None,
        emails: EmailType = None,
        faxes: FaxType = None,
        wwws: WWWType = None,
        notes: NoteType = None,
        identifiers: IdenType = None,
        change: ChangeDateType = None,
        creation: CreationDateType = None,
        name_ext: ExtType = None,
    ) -> None:
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
        show: Repository
        gedcom_docs: str = Specs.REPOSITORY
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = Repository(
                    xref=Void.REPO,
                    name='',
                    address=Address(),
                    phones=None,
                    emails=None,
                    faxes=None,
                    wwws=None,
                    notes=None,
                    identifiers=None,
                    change=None,
                    creation=None,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Repository(
                    xref=Void.REPO,
                    name='',
                    address=Address(),
                    phones=None,
                    emails=None,
                    faxes=None,
                    wwws=None,
                    notes=None,
                    identifiers=None,
                    change=None,
                    creation=None,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Repository(
                    xref=Void.REPO,
                    name='',
                    address=Address(),
                    phones=None,
                    emails=None,
                    faxes=None,
                    wwws=None,
                    notes=None,
                    identifiers=None,
                    change=None,
                    creation=None,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Repository(
                    xref=xref,
                    name=name,
                    address=address,
                    phones=phones,
                    emails=emails,
                    faxes=faxes,
                    wwws=wwws,
                    notes=notes,
                    identifiers=identifiers,
                    change=change,
                    creation=creation,
                    name_ext=name_ext,
                )
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


class SharedNote(NamedTuple):
    """Store, validate and display a GEDCOM Shared Note Record.

    Reference:
        [GEDCOM Shared Note Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SHARED_NOTE_RECORD)

    > n @XREF:SNOTE@ SNOTE <Text>                {1:1}  g7:record-SNOTE
    >   +1 MIME <MediaType>                      {0:1}  g7:MIME
    >   +1 LANG <Language>                       {0:1}  g7:LANG
    >   +1 TRAN <Text>                           {0:M}  g7:NOTE-TRAN
    >      +2 MIME <MediaType>                   {0:1}  g7:MIME
    >      +2 LANG <Language>                    {0:1}  g7:LANG
    >   +1 <<SOURCE_CITATION>>                   {0:M}
    >   +1 <<IDENTIFIER_STRUCTURE>>              {0:M}
    >   +1 <<CHANGE_DATE>>                       {0:1}
    >   +1 <<CREATION_DATE>>                     {0:1}
    """

    xref: SharedNoteXref = Void.SNOTE
    text: str = Default.EMPTY
    mime: MediaType = MediaType.NONE
    language: LangType = None
    translations: NoteTranType = None
    sources: SourCiteType = None
    identifiers: IdenType = None
    change: ChangeDateType = None
    creation: CreationDateType = None
    snote_ext: ExtType = None
    mime_ext: ExtType = None
    lang_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.xref, SharedNoteXref)
            and Checker.verify_type(self.text, str)
            and Checker.verify_type(self.mime, MediaType)
            and Checker.verify_type(self.language, Lang)
            and Checker.verify_type(self.translations, NoteTranslation)
            and Checker.verify_type(self.sources, Source)
            and Checker.verify_type(self.identifiers, Identifier)
            and Checker.verify_type(self.change, ChangeDate | None)
            and Checker.verify_type(self.creation, CreationDate | None)
            and Checker.verify_ext(Tag.SNOTE, self.snote_ext)
            and Checker.verify_ext(Tag.MIME, self.mime_ext)
            and Checker.verify_ext(Tag.LANG, self.lang_ext)
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged()
        if self.validate():
            lines = Tagger.string(lines, level + 1, Tag.MIME, self.mime.value)
            lines = Tagger.structure(lines, level + 2, self.mime_ext)
            lines = Tagger.structure(lines, level + 1, self.language)
            lines = Tagger.structure(lines, level + 2, self.lang_ext)
            lines = Tagger.structure(lines, level + 1, self.translations)
            lines = Tagger.structure(lines, level + 1, self.sources)
            lines = Tagger.structure(lines, level + 1, self.identifiers)
            lines = Tagger.structure(lines, level + 1, self.change)
            lines = Tagger.structure(lines, level + 1, self.creation)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
SharedNote(
    xref = {Formatter.codes(self.xref, tabs)},
    text = {Formatter.codes(self.text, tabs)},
    mime = {Formatter.codes(self.mime, tabs)},
    language = {Formatter.codes(self.language, tabs)},
    translations = {Formatter.codes(self.translations, tabs)},
    sources = {Formatter.codes(self.sources, tabs)},
    identifiers = {Formatter.codes(self.identifiers, tabs)},
    change = {Formatter.codes(self.change, tabs)}
    creation = {Formatter.codes(self.creation, tabs)}
    snote_ext = {Formatter.codes(self.snote_ext, tabs)},
    mime_ext = {Formatter.codes(self.mime_ext, tabs)},
    lang_ext = {Formatter.codes(self.lang_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        xref: SharedNoteXref = Void.SNOTE,
        text: str = Default.EMPTY,
        mime: MediaType = MediaType.NONE,
        language: LangType = None,
        translations: NoteTranType = None,
        sources: SourCiteType = None,
        identifiers: IdenType = None,
        change: ChangeDateType = None,
        creation: CreationDateType = None,
        snote_ext: ExtType = None,
        mime_ext: ExtType = None,
        lang_ext: ExtType = None,
    ) -> None:
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
        show: SharedNote
        gedcom_docs: str = Specs.SHARED_NOTE
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = SharedNote(
                    xref=Void.SNOTE,
                    text='',
                    mime=MediaType.NONE,
                    language=Lang('en-US'),
                    translations=None,
                    sources=None,
                    identifiers=None,
                    change=None,
                    creation=None,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = SharedNote(
                    xref=Void.SNOTE,
                    text='',
                    mime=MediaType.NONE,
                    language=Lang('en-US'),
                    translations=None,
                    sources=None,
                    identifiers=None,
                    change=None,
                    creation=None,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = SharedNote(
                    xref=Void.SNOTE,
                    text='',
                    mime=MediaType.NONE,
                    language=Lang('en-US'),
                    translations=None,
                    sources=None,
                    identifiers=None,
                    change=None,
                    creation=None,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = SharedNote(
                    xref=xref,
                    text=text,
                    mime=mime,
                    language=language,
                    translations=translations,
                    sources=sources,
                    identifiers=identifiers,
                    change=change,
                    creation=creation,
                    snote_ext=snote_ext,
                    mime_ext=mime_ext,
                    lang_ext=lang_ext,
                )
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

    exttags: ExtTagType = None
    source: str = String.EMPTY
    vers: str = String.EMPTY
    name: str = String.EMPTY
    corporation: str = String.EMPTY
    address: AddrType = None
    phones: PhoneType = None
    emails: EmailType = None
    faxes: FaxType = None
    wwws: WWWType = None
    data: str = String.EMPTY
    data_date: DateType = None
    data_time: TimeType = None
    data_copyright: str = String.EMPTY
    dest: str = String.EMPTY
    header_date: DateType = None
    header_time: TimeType = None
    submitter: SubmitterXref = Void.SUBM
    subm_copyright: str = String.EMPTY
    language: LangType = None
    note: NoteType = None
    head_ext: ExtType = None
    gedc_ext: ExtType = None
    vers_ext: ExtType = None
    dest_ext: ExtType = None
    subm_ext: ExtType = None
    copr_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.exttags, ExtTag)
            and Checker.verify_type(self.source, str)
            and Checker.verify_type(self.vers, str)
            and Checker.verify_type(self.name, str)
            and Checker.verify_type(self.corporation, str)
            and Checker.verify_type(self.address, Address)
            and Checker.verify_type(self.phones, Phone)
            and Checker.verify_type(self.emails, Email)
            and Checker.verify_type(self.faxes, Fax)
            and Checker.verify_type(self.wwws, WWW)
            and Checker.verify_type(self.data, str)
            and Checker.verify_type(self.data_date, Date)
            and Checker.verify_type(self.data_time, Time)
            and Checker.verify_type(self.data_copyright, str)
            and Checker.verify_type(self.dest, str)
            and Checker.verify_type(self.header_date, Date)
            and Checker.verify_type(self.header_time, Time)
            and Checker.verify_type(self.submitter, SubmitterXref)
            and Checker.verify_type(self.subm_copyright, str)
            and Checker.verify_type(self.language, Lang)
            and Checker.verify_type(self.note, Note)
            and Checker.verify_ext(Tag.HEAD, self.head_ext)
            and Checker.verify_ext(Tag.GEDC, self.gedc_ext)
            and Checker.verify_ext(Tag.VERS, self.vers_ext)
            and Checker.verify_ext(Tag.DEST, self.dest_ext)
            and Checker.verify_ext(Tag.SUBM, self.subm_ext)
            and Checker.verify_ext(Tag.COPR, self.copr_ext)
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.empty(lines, level, Tag.HEAD)
            lines = Tagger.structure(lines, level + 1, self.head_ext)
            lines = Tagger.empty(lines, level + 1, Tag.GEDC)
            lines = Tagger.structure(lines, level + 2, self.gedc_ext)
            lines = Tagger.string(lines, level + 2, Tag.VERS, String.VERSION)
            lines = Tagger.structure(lines, level + 3, self.vers_ext)
            if self.exttags is not None and (
                (isinstance(self.exttags, list) and len(self.exttags) > 0)
                or isinstance(self.exttags, ExtTag)
            ):
                lines = Tagger.empty(lines, level + 1, Tag.SCHMA)
                lines = Tagger.structure(lines, level + 1, self.exttags)
            lines = Tagger.structure(lines, level, self.address)
            lines = Tagger.structure(lines, level, self.phones)
            lines = Tagger.structure(lines, level, self.emails)
            lines = Tagger.structure(lines, level, self.faxes)
            lines = Tagger.structure(lines, level, self.wwws)
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
            lines = Tagger.structure(lines, level + 1, self.dest_ext)
            lines = Tagger.structure(lines, level, self.header_date, Date())
            lines = Tagger.structure(lines, level + 1, self.header_time, Time())
            if self.submitter != Void.SUBM:
                lines = Tagger.string(
                    lines, level + 1, Tag.SUBM, self.submitter.fullname
                )
                lines = Tagger.structure(lines, level + 2, self.subm_ext)
            lines = Tagger.string(
                lines, level + 1, Tag.COPR, self.subm_copyright
            )
            lines = Tagger.structure(lines, level + 2, self.copr_ext)
            lines = Tagger.structure(lines, level, self.language)
            lines = Tagger.structure(lines, level, self.note)
        return lines

    def code(self, tabs: int = 0) -> str:
        return indent(
            f"""
Header(
    exttags = {Formatter.codes(self.exttags, tabs)},
    source = {Formatter.codes(self.source, tabs)},
    vers = {Formatter.codes(self.vers, tabs)},
    name = {Formatter.codes(self.name, tabs)},
    corporation = {Formatter.codes(self.corporation, tabs)},
    address = {Formatter.codes(self.address, tabs)},
    phones = {Formatter.codes(self.phones, tabs)},
    emails = {Formatter.codes(self.emails, tabs)},
    faxes = {Formatter.codes(self.faxes, tabs)},
    wwws = {Formatter.codes(self.wwws, tabs)},
    data = {Formatter.codes(self.data, tabs)},
    data_date = {Formatter.codes(self.data_date, tabs)},
    data_time = {Formatter.codes(self.data_time, tabs)},
    data_copyright = {Formatter.codes(self.data_copyright, tabs)},
    dest = {Formatter.codes(self.dest, tabs)},
    header_date = {Formatter.codes(self.header_date, tabs)},
    header_time = {Formatter.codes(self.header_time, tabs)},
    submitter = {Formatter.codes(self.submitter, tabs)},
    subm_copyright = {Formatter.codes(self.subm_copyright, tabs)},
    language = {Formatter.codes(self.language, tabs)},
    note = {Formatter.codes(self.note, tabs)},
    head_ext = {Formatter.codes(self.head_ext, tabs)},
    gedc_ext = {Formatter.codes(self.gedc_ext, tabs)},
    vers_ext = {Formatter.codes(self.vers_ext, tabs)},
    dest_ext = {Formatter.codes(self.dest_ext, tabs)},
    subm_ext = {Formatter.codes(self.subm_ext, tabs)},
    copr_ext = {Formatter.codes(self.copr_ext, tabs)},
)""",
            String.INDENT * tabs,
        )

    def example(
        self,
        choice: int = Default.CHOICE,
        exttags: ExtTagType = None,
        source: str = String.EMPTY,
        vers: str = String.EMPTY,
        name: str = String.EMPTY,
        corporation: str = String.EMPTY,
        address: AddrType = None,
        phones: PhoneType = None,
        emails: EmailType = None,
        faxes: FaxType = None,
        wwws: WWWType = None,
        data: str = String.EMPTY,
        data_date: DateType = None,
        data_time: TimeType = None,
        data_copyright: str = String.EMPTY,
        dest: str = String.EMPTY,
        header_date: DateType = None,
        header_time: TimeType = None,
        submitter: SubmitterXref = Void.SUBM,
        subm_copyright: str = String.EMPTY,
        language: LangType = None,
        note: NoteType = None,
        head_ext: ExtType = None,
        gedc_ext: ExtType = None,
        vers_ext: ExtType = None,
        dest_ext: ExtType = None,
        subm_ext: ExtType = None,
        copr_ext: ExtType = None,
    ) -> None:
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
        show: Header
        gedcom_docs: str = Specs.HEADER
        genealogy_docs: str = 'To be constructed'
        code_preface: str = String.EMPTY
        gedcom_preface: str = String.EMPTY
        match choice:
            case 1:
                show = Header(
                    exttags=None,
                    source='',
                    vers='v7.0',
                    name='',
                    corporation='',
                    address=Address(),
                    phones=None,
                    emails=None,
                    faxes=None,
                    wwws=None,
                    data='',
                    data_date=Date(),
                    data_time=Time(),
                    data_copyright='',
                    dest='',
                    header_date=Date(),
                    header_time=Time(),
                    submitter=Void.SUBM,
                    subm_copyright='',
                    language=Lang('en-US'),
                    note=None,
                )
                code_preface = Example.FULL
                gedcom_preface = Example.GEDCOM
            case 2:
                show = Header(
                    exttags=None,
                    source='',
                    vers='v7.0',
                    name='',
                    corporation='',
                    address=Address(),
                    phones=None,
                    emails=None,
                    faxes=None,
                    wwws=None,
                    data='',
                    data_date=Date(),
                    data_time=Time(),
                    data_copyright='',
                    dest='',
                    header_date=Date(),
                    header_time=Time(),
                    submitter=Void.SUBM,
                    subm_copyright='',
                    language=Lang('en-US'),
                    note=None,
                )
                code_preface = Example.SECOND
                gedcom_preface = Example.GEDCOM
            case 3:
                show = Header(
                    exttags=None,
                    source='',
                    vers='v7.0',
                    name='',
                    corporation='',
                    address=Address(),
                    phones=None,
                    emails=None,
                    faxes=None,
                    wwws=None,
                    data='',
                    data_date=Date(),
                    data_time=Time(),
                    data_copyright='',
                    dest='',
                    header_date=Date(),
                    header_time=Time(),
                    submitter=Void.SUBM,
                    subm_copyright='',
                    language=Lang('en-US'),
                    note=None,
                )
                code_preface = Example.THIRD
                gedcom_preface = Example.GEDCOM
            case _:
                show = Header(
                    exttags=exttags,
                    source=source,
                    vers=vers,
                    name=name,
                    corporation=corporation,
                    address=address,
                    phones=phones,
                    emails=emails,
                    faxes=faxes,
                    wwws=wwws,
                    data=data,
                    data_date=data_date,
                    data_time=data_time,
                    data_copyright=data_copyright,
                    dest=dest,
                    header_date=header_date,
                    header_time=header_time,
                    submitter=submitter,
                    subm_copyright=subm_copyright,
                    language=language,
                    note=note,
                    head_ext=head_ext,
                    gedc_ext=gedc_ext,
                    vers_ext=vers_ext,
                    dest_ext=dest_ext,
                    subm_ext=subm_ext,
                    copr_ext=copr_ext,
                )
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
