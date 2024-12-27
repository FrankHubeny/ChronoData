# chronodata/methods.py
# Copyright: Licensed under a 3-clause BSD style license - see LICENSE.md
"""Global methods to build a chronology based on the GEDCOM standard."""

import contextlib
import logging
import re
from enum import Enum
from typing import Any

import numpy as np

from chronodata.constants import Cal, String
from chronodata.enums import Tag
from chronodata.messages import Msg


class Defs:
    """Provide a namespace container for global methods.

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

    @staticmethod
    def unique_xref(tuples: tuple[Any], xref: Any, name: Any) -> bool:
        values = {getattr(t, str(xref)) for t in tuples}
        values.add(str(name))
        return len(values) == len(tuples)

    @staticmethod
    def taginfo(
        level: int,
        tag: Tag,
        info: str = '',
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
            >>> print(Defs.taginfo(1, Tag.NAME, '  Some Name'))
            1 NAME   Some Name
            <BLANKLINE>

            There can also be an extra parameter.
            >>> from chronodata.enums import Tag
            >>> print(Defs.taginfo(1, Tag.NAME, 'SomeName', 'Other info'))
            1 NAME SomeName Other info
            <BLANKLINE>

        """

        if extra == '':
            if info == '':
                return f'{level} {tag.value}\n'
            return f'{level} {tag.value} {Defs.clean_input(info)}\n'
        return f'{level} {tag.value} {Defs.clean_input(info)} {Defs.clean_input(extra)}\n'

    @staticmethod
    def contact_info(
        level: int = 1,
        phones: Any = None,
        emails: Any = None,
        faxes: Any = None,
        wwws: Any = None
    ) -> str:
        lines: str = ''
        if phones is not None:
            for phone in phones:
                lines = ''.join([lines, Defs.taginfo(level, Tag.PHON, phone)])
        if emails is not None:
            for email in emails:
                lines = ''.join([lines, Defs.taginfo(level, Tag.EMAIL, email)])
        if faxes is not None:
            for fax in faxes:
                lines = ''.join([lines, Defs.taginfo(level, Tag.FAX, fax)])
        if wwws is not None:
            for www in wwws:
                lines = ''.join([lines, Defs.taginfo(level, Tag.WWW, www)])
        return lines

    @staticmethod
    def list_to_str(lines: str, level: int, items: list[Any]) -> str:
        if len(items) > 0:
            for item in items:
                lines = ''.join([lines, item.ged(level)])
        return lines
    
    @staticmethod
    def str_to_str(lines: str, level: int, tag: Tag, info: str = '', extra: str = '') -> str:
        return ''.join([lines, Defs.taginfo(level, tag, info, extra)])

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
                Defs.verify_type(value, value_type)
        return True

    @staticmethod
    def verify_enum(value: str, enumeration: Any) -> bool:
        """Check if the value is in the proper enumation."""
        if value not in enumeration:
            raise ValueError(Msg.NOT_VALID_ENUM.format(value, enumeration))
        return True

    @staticmethod
    def verify_choice(value: str, choice: frozenset[str]) -> bool:
        """Check if the value is one to choose from."""
        if value not in choice:
            raise ValueError(Msg.NOT_VALID_CHOICE.format(value, choice))
        return True

    @staticmethod
    def verify_dict_key(value: str, dictionary: dict[str, str]) -> bool:
        """Check if the value is in the proper dictionary."""
        Defs.verify_type(value, str)
        if value != '' and value not in dictionary:
            raise ValueError(Msg.NOT_VALID_KEY.format(value, dictionary))
        return True

    @staticmethod
    def verify_not_default(value: Any, default: Any) -> bool:
        """Check that the value is not the default value."""
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

    @staticmethod
    def ged_date(
        iso_date: str = String.NOW,
        calendar: str = 'GREGORIAN',
        epoch: bool = True,
    ) -> tuple[str, str]:
        """Obtain the GEDCOM date and time from an ISO date and time or the
        current UTC timestamp in GEDCOM format.

        Parameters
        ----------
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
        >>> from chronodata.methods import Defs  # doctest: +ELLIPSIS
        >>> print(Defs.now())
        2 DATE ...
        3 TIME ...
        <BLANKLINE>

        Changing the level adjusts the level numbers for the two returned strings.

        >>> print(Defs.now(level=5))
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
        date, time = Defs.ged_date()
        return ''.join(
            [
                Defs.taginfo(level, Tag.DATE, date),
                Defs.taginfo(level + 1, Tag.TIME, time),
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
        return ''.join([Defs.taginfo(1, Tag.CREA), Defs.now()])
