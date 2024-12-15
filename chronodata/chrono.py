# Licensed under a 3-clause BSD style license - see LICENSE.md
"""Methods to build a chronology based on the GEDCOM standard.

This module implements reading and writing chronology files according to the
[FamilySearch GEDCOM Version 7](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html)
standard.  It also allows reading files in the GEDCOM 5.5.1 standard,
but will write the output in compliance with GEDCOM 7.0.

The underlying datastructure for the chronology is a Python dictionary.
This dictionary can be read and written in JSON.

Rather than introduce extensions to the GEDCOM standards new data items
are placed under `FACT` and `EVEN` tags as
[Tamura Jones](https://www.tamurajones.net/GEDCOMExtensions.xhtml) recommended.
Some extensions are the use of ISO dates as implemented by NumPy's `datetime64`
data type."""

import logging
from typing import Any, NamedTuple

import numpy as np

from chronodata.constants import (
    Cal,
    Value,
)
from chronodata.core import Base
from chronodata.g7 import (
    Enum,
    EnumName,
    Gedcom,
    GEDDateTime,
    GEDSpecial,
    ISOMonths,
    Record,
)
from chronodata.messages import Msg


class Defs:
    """Provide a namespace container for global methods."""

    @staticmethod
    def taginit(xref: str, tag: str, info: str = '') -> str:
        if info == '':
            return f'0 {xref} {tag}\n'
        return f'0 {xref} {tag} {str(info).strip()}\n'

    @staticmethod
    def taginfo(
        level: int,
        tag: str,
        info: str = '',
        extra: str = '',
    ) -> str:
        """Return a GEDCOM formatted line for the information and level.

        This is suitable for most tagged lines to guarantee it is uniformly
        formatted.  Although the user need not worry about calling this line,
        it is provided so the user can see the GEDCOM formatted output
        that would result.

        See Also
        --------

        """

        if extra == '':
            if info == '':
                return f'{level} {tag}\n'
            return f'{level} {tag} {info}\n'
        return f'{level} {tag} {info} {extra}\n'

    @staticmethod
    def verify_type(value: Any, value_type: Any) -> bool:
        """Check if the value has the specified type."""
        if not isinstance(value, value_type):
            raise TypeError(
                Msg.WRONG_TYPE.format(value, type(value), value_type)
            )
        return True

    @staticmethod
    def verify_tuple_type(name: tuple[Any], value_type: Any) -> bool:
        """Check if each member of the tuple has the specified type."""
        for value in name:
            Defs.verify_type(value, value_type)
        return True

    @staticmethod
    def verify_enum(value: str, enum: frozenset[str], name: str) -> bool:
        """Check if the value is in the proper enumation."""
        if value not in enum:
            raise ValueError(Msg.NOT_VALID_ENUM.format(value, name))
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

    # @staticmethod
    # def verify_not_empty(value: str | None, name: str) -> None:
    #     """Check if the value is neither None nor the empty string."""
    #     if value == '' or value is None:
    #         raise ValueError(Msg.EMPTY_ERROR.format(name))


class PersonalName(NamedTuple):
    tag: str
    text: str = ''

    def validate(self) -> bool:
        Defs.verify_type(self.tag, str)
        Defs.verify_type(self.text, str)
        Defs.verify_enum(self.tag, Enum.PERSONAL_NAME, EnumName.PERSONAL_NAME)
        return True

    def ged(self, level=1) -> str:
        personal_name: str = ''
        if self.validate():
            personal_name = Defs.taginfo(level, self.tag, self.text.strip())
        return personal_name


class Name_Translation(NamedTuple):
    text: str
    language: str = ''
    piece: Any = None

    def validate(self) -> bool:
        Defs.verify_type(self.text, str)
        Defs.verify_type(self.language, str)
        Defs.verify_type(self.piece, PersonalName)
        return True


class NoteTranslation(NamedTuple):
    text: str
    mime: str = ''
    language: str = ''

    def validate(self) -> bool:
        Defs.verify_type(self.text, str)
        Defs.verify_type(self.mime, str)
        Defs.verify_type(self.language, str)
        return True


class NoteCitation(NamedTuple):
    text: str
    mime: str = ''
    language: str = ''
    translations: Any = None

    def validate(self) -> bool:
        Defs.verify_type(self.text, str)
        Defs.verify_type(self.mime, str)
        Defs.verify_type(self.language, str)
        Defs.verify_tuple_type(self.translations, NoteTranslation)
        return True


class Citation(NamedTuple):
    xref: str
    page: str = ''
    datetime: str = ''
    text: str = ''
    mime: str = ''
    language: str = ''
    event: str = ''
    phrase: str = ''
    role: str = ''
    role_phrase: str = ''
    quality: str = ''
    multimedia: str = ''
    notes: Any = None

    def validate(self) -> bool:
        Defs.verify_type(self.xref, str)
        Defs.verify_type(self.page, str)
        Defs.verify_type(self.datetime, str)
        Defs.verify_type(self.text, str)
        Defs.verify_type(self.mime, str)
        Defs.verify_type(self.language, str)
        Defs.verify_type(self.event, str)
        Defs.verify_type(self.phrase, str)
        Defs.verify_type(self.role, str)
        Defs.verify_type(self.role_phrase, str)
        Defs.verify_type(self.quality, str)
        Defs.verify_type(self.multimedia, str)
        Defs.verify_tuple_type(self.notes, NoteCitation)
        return True


class Note(NamedTuple):
    text: str
    mime: str = ''
    language: str = ''
    translation: Any = None
    citations: Any = None

    def validate(self) -> bool:
        Defs.verify_type(self.text, str)
        Defs.verify_type(self.mime, str)
        Defs.verify_type(self.language, str)
        Defs.verify_tuple_type(self.translation, NoteTranslation)
        Defs.verify_tuple_type(self.citations, Citation)
        return True


class Association(NamedTuple):
    # xref: str
    role: str
    association_phrase: str = ''
    role_phrase: str = ''
    notes: Any = None
    citations: Any = None

    def validate(self) -> bool:
        # Defs.verify_type(self.xref, str)
        Defs.verify_type(self.role, str)
        Defs.verify_type(self.association_phrase, str)
        Defs.verify_type(self.role_phrase, str)
        Defs.verify_tuple_type(self.notes, Note)
        Defs.verify_tuple_type(self.citations, Citation)
        Defs.verify_enum(self.role, Enum.ROLE, EnumName.ROLE)
        return True

    def ged(self, level: int = 1) -> str:
        lines: str = ''
        if self.validate():
            if self.association_phrase != '':
                lines = ''.join(
                    [
                        lines,
                        Defs.taginfo(
                            level + 1,
                            Gedcom.PHRASE,
                            self.association_phrase,
                        ),
                    ]
                )
            lines = ''.join(
                [
                    lines,
                    Defs.taginfo(level + 2, Gedcom.ROLE, self.role),
                ]
            )
            if self.role_phrase != '':
                lines = ''.join(
                    [
                        lines,
                        Defs.taginfo(
                            level + 2,
                            Gedcom.PHRASE,
                            self.role_phrase,
                        ),
                    ]
                )
            for note in self.notes:
                lines = ''.join([lines, note.ged(1)])
            for citation in self.citations:
                lines = ''.join([lines, citation.ged(1)])
        return lines


class MultimediaLink(NamedTuple):
    crop: str = ''
    top: int = 0
    left: int = 0
    height: int = 0
    width: int = 0
    title: str = ''

    def validate(self) -> bool:
        Defs.verify_type(self.crop, str)
        Defs.verify_type(self.top, int)
        Defs.verify_type(self.left, int)
        Defs.verify_type(self.height, int)
        Defs.verify_type(self.width, int)
        Defs.verify_type(self.title, str)
        return True


class Exid(NamedTuple):
    exid: str
    exid_type: str

    def validate(self) -> bool:
        Defs.verify_type(self.exid, str)
        Defs.verify_type(self.exid_type, str)
        return True

    def ged(self, level: int = 1):
        return ''.join(
            [
                Defs.taginfo(level, Gedcom.EXID, self.exid),
                Defs.taginfo(level + 1, Gedcom.TYPE, self.exid_type),
            ]
        )


class PlaceTranslation(NamedTuple):
    text: str
    language: str = ''

    def validate(self) -> bool:
        Defs.verify_type(self.text, str)
        Defs.verify_type(self.language, str)
        return True


class Map(NamedTuple):
    latitude: float
    longitude: float

    def validate(self) -> bool:
        Defs.verify_type(self.latitude, float)
        Defs.verify_type(self.longitude, float)
        return True


class Place(NamedTuple):
    text: str
    form: str = ''
    language: str = ''
    translations: Any = None
    maps: Any = None
    exids: Any = None
    notes: Any = None

    def validate(self) -> bool:
        Defs.verify_type(self.text, str)
        Defs.verify_type(self.form, str)
        Defs.verify_tuple_type(self.translations, PlaceTranslation)
        Defs.verify_tuple_type(self.maps, Map)
        Defs.verify_tuple_type(self.exids, Exid)
        Defs.verify_tuple_type(self.notes, Note)
        return True


class Address(NamedTuple):
    """Add address information.

    Each address line is a list of five strings:
    - Mailing Address: Each line of the mailing label is separated by `\n`.
    - City: The city or and empty string to leave this blank.
    - State: The state or an empty string to leave this blank.
    - Postal Code: The postal code or an empty string to leave this blank.
    - Country: The country or an empty string to leave this blank.

    One does not have to call this method directly.  The GEDCOM record methods
    call it when creating a chronology.  However, one can use it to
    see what the address information one provides would look like
    in a GEDCOM file.

    Example
    -------
    In the first example note the five strings in the list.  Also note
    that the country was not specified but nonetheless an empty string
    was added as a placeholder for the absent country information.
    Note the `\n` to separate the two address lines.
    [
        '12345 ABC Street\nSouth North City, My State 23456',
        'South North City',
        'My State',
        '23456',
        ''
    ]

    The GEDCOM record would appear as the following:

    1 ADDR 12345 ABC Street
    1 CONT South North City, My State 23456
    2 CITY South North City
    2 STAE My State
    2 POST 23456

    The following is the minimum amount of information for an address.
    [
        '12345 ABC Street\nSouth North City, My State 23456',
    ]

    If one does not want to use the `\n` one can write the following
    provided one imports the GEDSpecial class.  One way to do that is
    by adding the following line at the top of the cell:


    The GEDCOM record would appear as the following:

    1 ADDR 12345 ABC Street
    1 CONT South North City, My State 23456

    If the list is empty the method returns the empty list.

    Reference
    ---------
    The following is from the
    [GEDCOM Specifications](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#substructures)

    >n ADDR <Special>                           {1:1}  g7:ADDR
    >  +1 ADR1 <Special>                        {0:1}  g7:ADR1
    >  +1 ADR2 <Special>                        {0:1}  g7:ADR2
    >  +1 ADR3 <Special>                        {0:1}  g7:ADR3
    >  +1 CITY <Special>                        {0:1}  g7:CITY
    >  +1 STAE <Special>                        {0:1}  g7:STAE
    >  +1 POST <Special>                        {0:1}  g7:POST
    >  +1 CTRY <Special>                        {0:1}  g7:CTRY

    >Duplicating information bloats files and introduces the
    >potential for self-contradiction. ADR1, ADR2, and ADR3
    >should not be added to new files.
    """

    address: str = ''
    city: str = ''
    state: str = ''
    postal: str = ''
    country: str = ''

    def validate(self) -> bool:
        Defs.verify_type(self.address, str)
        Defs.verify_type(self.city, str)
        Defs.verify_type(self.state, str)
        Defs.verify_type(self.postal, str)
        Defs.verify_type(self.country, str)
        return True

    def ged(self, level: int = 1) -> str | None:
        lines: str = ''
        if self.validate() and self.address != '':
            address_lines = self.address.split('\n')
            for line in address_lines:
                if line == '':
                    address_lines.remove(line)
            lines = ''.join(
                [
                    lines,
                    Defs.taginfo(level, Gedcom.ADDR, address_lines[0].strip()),
                ]
            )
            for line in address_lines[1:]:
                lines = ''.join(
                    [lines, Defs.taginfo(level, Gedcom.CONT, line.strip())]
                )
            if self.city != '':
                lines = ''.join(
                    [
                        lines,
                        Defs.taginfo(level + 1, Gedcom.CITY, self.city.strip()),
                    ]
                )
            if self.state != '':
                lines = ''.join(
                    [
                        lines,
                        Defs.taginfo(
                            level + 1, Gedcom.STAE, self.state.strip()
                        ),
                    ]
                )
            if self.postal != '':
                lines = ''.join(
                    [
                        lines,
                        Defs.taginfo(
                            level + 1, Gedcom.POST, self.postal.strip()
                        ),
                    ]
                )
            if self.country != '':
                lines = ''.join(
                    [
                        lines,
                        Defs.taginfo(
                            level + 1, Gedcom.CTRY, self.country.strip()
                        ),
                    ]
                )
        return lines


class Date(NamedTuple):
    """Validate and display date data in various formats.

    Dates are entered based on a Gregorian calendar. This calendar
    does not have a 0 year.  The year 1 BC is entered as `-1`.

    A default value of `0` for any date component means that the component
    will not be displayed.

    The GEDCOM standard allows a week without specifying the other components.

    Parameters
    ----------
    year


    Example
    -------
    """

    year: int = 0
    month: int = 0
    day: int = 0
    week: int = 0
    calendar: str = Value.GREGORIAN

    def validate(self) -> bool:
        """Validate date information provided by the user."""
        Defs.verify_type(self.year, int)
        Defs.verify_type(self.month, int)
        Defs.verify_type(self.day, int)
        Defs.verify_type(self.week, int)
        Defs.verify_range(self.week, 0, 52)
        Defs.verify_range(self.month, 0, 12)
        if self.year == 0:
            raise ValueError(Msg.NO_ZERO_YEAR.format(self.year, self.calendar))
        return True

    def ged(self, level: int = 1, calendar: str = Value.GREGORIAN) -> str:
        """Display the validated date in GEDCOM format.

        Reference
        ---------
        - [GEDCOM Standard V 7.0](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#date)
        """

        if self.validate():
            day_str: str = (
                str(self.day) if self.day > 9 else ''.join(['0', str(self.day)])
            )
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
            output: str = f'{level} {Gedcom.DATE}'
            if self.day != 0:
                output = ''.join([output, f' {day_str}'])
            if self.month != 0:
                output = ''.join(
                    [
                        output,
                        f' {Cal.CALENDARS[calendar][Value.MONTH_NAMES][str(month_str)]}',
                    ]
                )
            if self.year != 0:
                output = ''.join([output, f' {year_str}\n'])
            return output
        return ''

    def iso(self) -> str | None:
        """Return the validated ISO format for the date.

        References
        ----------
        - [ISO 8601 Standard](https://www.iso.org/iso-8601-date-and-time-format.html)
        - [Wikipedia Overview](https://en.wikipedia.org/wiki/ISO_8601)
        """
        if self.validate():
            return f'{self.year}-{self.month}-{self.day}'
        return None


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
        """Validate time information provided by the user."""
        Defs.verify_type(self.hour, int)
        Defs.verify_type(self.minute, int)
        Defs.verify_type(self.second, int | float)
        Defs.verify_type(self.UTC, bool)
        Defs.verify_range(self.hour, 0, 23)
        Defs.verify_range(self.minute, 0, 59)
        Defs.verify_range(self.second, 0, 59.999999999999)
        # if isinstance(self.second, float) and not 0.0 <= self.second < 60.0:
        #     raise ValueError(Msg.RANGE.format(self.second, 0.0, 60.0))
        # if isinstance(self.second, int):
        #     Defs.verify_range(self.second, 0, 59)
        return True

    def ged(self, level: int = 1) -> str:
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
            return Defs.taginfo(
                level, Gedcom.TIME, f'{hour_str}:{minute_str}:{second_str}'
            )
        return ''

    def iso(self) -> str | None:
        """Return the validated ISO format for the time.

        References
        ----------
        - [ISO 8601 Standard](https://www.iso.org/iso-8601-date-and-time-format.html)
        - [Wikipedia Overview](https://en.wikipedia.org/wiki/ISO_8601)
        """
        if self.validate():
            return f'{self.hour}:{self.minute}:{self.second}'
        return None


class Age(NamedTuple):
    """Implement the Age data type in the GEDCOM specification.

    Parameters
    ----------
    - greater_less_than
        The default is ``, which means that the age is exact
        to the day.  The option `>` means that the actual age
        is greater than the one provided.  The option `<` means
        that the actual age is less than the one provided.
    - years
        The number of who years in the age.
    - months
        The number of months in addition to the years.
    = weeks
        The number of weeks in addition to the years and months.
    - days
        The number of days in addition to any years, months, or weeks provided.

    The default values for these parameters is 0.  A 0 value or a value less
    than 0 will be stored.

    Examples
    --------
    >>> Age('>', 10)
    >>> > 10y
    >>> Age(10, 2, 1, 2)
    >>> 10y 2m 1w 2d

    Reference
    ---------
    [GEDCOM Specification](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#age)
    """

    greater_less_than: str = ''
    years: int = 0
    months: int = 0
    weeks: int = 0
    days: int = 0

    def validate(self) -> bool:
        Defs.verify_enum(
            self.greater_less_than,
            Enum.GREATER_LESS_THAN,
            EnumName.GREATER_LESS_THAN,
        )
        Defs.verify_type(self.years, int)
        Defs.verify_type(self.months, int)
        Defs.verify_type(self.weeks, int)
        Defs.verify_type(self.days, int)
        Defs.verify_not_negative(self.years)
        Defs.verify_not_negative(self.months)
        Defs.verify_not_negative(self.weeks)
        Defs.verify_not_negative(self.days)
        return True

    def ged(self) -> str:
        """Format the GEDCOM Age data type."""
        line: str = self.greater_less_than
        if self.years > 0:
            line = ''.join([line, f' {self.years!s}y'])
        if self.months > 0:
            line = ''.join([line, f' {self.months!s}m'])
        if self.weeks > 0:
            line = ''.join([line, f' {self.weeks!s}w'])
        if self.days > 0:
            line = ''.join([line, f' {self.days!s}d'])

        return line.replace('  ', ' ').replace('  ', ' ').strip()


class DateValue(NamedTuple):
    """Construct a DATE_VALUE structure according to the GEDCOM standard.

    Example
    -------


    Reference
    ---------
    >n DATE <DateValue>                         {1:1}  g7:DATE
    >  +1 TIME <Time>                           {0:1}  g7:TIME
    >  +1 PHRASE <Text>                         {0:1}  g7:PHRASE"""

    date: Date = Date(0, 0, 0)
    time: Time = Time(0, 0, 0)
    phrase: str = ''

    def validate(self) -> bool:
        Defs.verify_type(self.phrase, str)
        return self.date.validate() and self.time.validate()

    def ged(self, level: int = 1) -> str:
        lines: str = self.date.ged(level)
        if self.time != Time(0, 0, 0):
            lines = ''.join([lines, self.time.ged(level + 1)])
        if self.phrase != '':
            lines = ''.join(
                [lines, Defs.taginfo(level + 1, Gedcom.PHRASE, self.phrase)]
            )
        return lines


class DateTimeStatus(NamedTuple):
    date: Date = Date(0, 0, 0)
    time: Time = Time(0, 0, 0)
    status: str = ''

    def validate(self) -> bool:
        Defs.verify_type(self.status, str)
        return self.date.validate() and self.time.validate()

    def ged(self, level=1) -> str:
        line: str = ''
        if self.validate():
            pass
        return line


class EventDetail(NamedTuple):
    date_value: DateValue | None = None
    place: Place | None = None
    address: Address | None = None
    phones: tuple[str] | None = None
    emails: tuple[str] | None = None
    faxes: tuple[str] | None = None
    wwws: tuple[str] | None = None
    agency: str = ''
    religion: str = ''
    cause: str = ''
    resn: str = ''
    # sort_date: SortDate = ()
    associations: tuple[Association] | None = None
    notes: tuple[Note] | None = None
    sources: tuple[Citation] | None = None
    multimedia_links: tuple[MultimediaLink] | None = None
    utd: tuple[str] | None = None


class HusbandWife(NamedTuple):
    husband_age: int = 0
    wife_age: int = 0
    husband_phrase: str = ''
    wife_phrase: str = ''
    event_detail: Any = None

    def validate(self) -> bool:
        Defs.verify_type(self.husband_age, int)
        Defs.verify_type(self.wife_age, int)
        Defs.verify_type(self.husband_phrase, str)
        Defs.verify_type(self.wife_phrase, str)
        Defs.verify_type(self.event_detail, EventDetail)
        return True

    def ged(self, level: int = 1) -> str:
        if self.validate():
            pass
        return ''


class FamilyEventDetail(NamedTuple):
    husband_wife_ages: HusbandWife

    def validate(self) -> bool:
        Defs.verify_type(self.husband_wife_ages, HusbandWife)
        return True


class FamilyAttribute(NamedTuple):
    tag: str
    attribute_type: str = ''
    family_event_detail: FamilyEventDetail | None = None

    def validate(self) -> bool:
        Defs.verify_type(self.tag, str)
        Defs.verify_type(self.attribute_type, str)
        Defs.verify_type(self.family_event_detail, FamilyEventDetail | None)
        return True


class FamilyEvent(NamedTuple):
    event: str = ''
    event_type: str = ''
    event_detail: FamilyEventDetail | None = None

    def validate(self) -> bool:
        Defs.verify_type(self.event, str)
        Defs.verify_type(self.event_type, str)
        Defs.verify_type(self.event_detail, FamilyEventDetail | None)
        return True


class Husband(NamedTuple):
    xref: str
    phrase: str = ''

    def validate(self) -> bool:
        Defs.verify_type(self.xref, str)
        Defs.verify_type(self.phrase, str)
        return True


class Wife(NamedTuple):
    xref: str
    phrase: str = ''

    def validate(self) -> bool:
        Defs.verify_type(self.xref, str)
        Defs.verify_type(self.phrase, str)
        return True


class Child(NamedTuple):
    xref: str
    phrase: str = ''

    def validate(self) -> bool:
        Defs.verify_type(self.xref, str)
        Defs.verify_type(self.phrase, str)
        return True


class LDSOrdinanceDetail(NamedTuple):
    date_value: DateValue | None = None
    temp: str = ''
    place: Place | None = None
    status: DateTimeStatus | None = None
    notes: Any = None
    sources: Any = None

    def validate(self) -> bool:
        Defs.verify_type(self.date_value, DateValue | None)
        Defs.verify_type(self.temp, str)
        Defs.verify_type(self.place, Place | None)
        Defs.verify_type(self.status, DateTimeStatus | None)
        Defs.verify_tuple_type(self.notes, Note)
        Defs.verify_tuple_type(self.sources, Citation)
        return True


class LDSSpouseSealing(NamedTuple):
    tag: str = Gedcom.SLGS
    detail: LDSOrdinanceDetail | None = None

    def validate(self) -> bool:
        Defs.verify_type(self.tag, str)
        Defs.verify_type(self.detail, LDSOrdinanceDetail | None)
        return True


class LDSIndividualOrdinances(NamedTuple):
    tag: str
    ordinance_detail: LDSOrdinanceDetail | None = None
    family_xref: str = ''

    def validate(self) -> bool:
        Defs.verify_type(self.tag, str)
        Defs.verify_type(self.ordinance_detail, LDSOrdinanceDetail | None)
        Defs.verify_type(self.family_xref, str)
        return True


class Identifier(NamedTuple):
    tag: str
    tag_type: str = ''

    def validate(self) -> bool:
        Defs.verify_type(self.tag, str)
        Defs.verify_type(self.tag_type, str)
        return True


class IndividualEventDetail(NamedTuple):
    event_detail: EventDetail
    age: str = ''
    phrase: str = ''

    def validate(self) -> bool:
        Defs.verify_type(self.event_detail, EventDetail)
        Defs.verify_type(self.age, str)
        Defs.verify_type(self.phrase, str)
        return True


class IndividualAttribute(NamedTuple):
    tag: str
    tag_type: str = ''
    event_detail: IndividualEventDetail | None = None

    def validate(self) -> bool:
        Defs.verify_type(self.tag, str)
        Defs.verify_type(self.tag_type, str)
        Defs.verify_type(self.event_detail, IndividualEventDetail | None)
        return True


class IndividualEvent(NamedTuple):
    tag: str
    tag_type: str = ''
    event_detail: IndividualEventDetail | None = None
    family_child: str = ''
    adoption: str = ''
    phrase: str = ''

    def validate(self) -> bool:
        Defs.verify_type(self.tag, str)
        Defs.verify_type(self.tag_type, str)
        Defs.verify_type(self.event_detail, IndividualEventDetail | None)
        Defs.verify_type(self.family_child, str)
        Defs.verify_type(self.adoption, str)
        Defs.verify_type(self.phrase, str)
        return True


class Alias(NamedTuple):
    xref: str
    phrase: str = ''

    def validate(self) -> bool:
        Defs.verify_type(self.xref, str)
        Defs.verify_type(self.phrase, str)
        return True


class FamilyChild(NamedTuple):
    family_xref: str
    pedigree: str = ''
    pedigree_phrase: str = ''
    status: str = ''
    status_phrase: str = ''
    notes: Any = None

    def validate(self) -> bool:
        Defs.verify_type(self.family_xref, str)
        Defs.verify_type(self.pedigree, str)
        Defs.verify_type(self.pedigree_phrase, str)
        Defs.verify_type(self.status, str)
        Defs.verify_type(self.status_phrase, str)
        Defs.verify_tuple_type(self.notes, Note)
        return True


class FamilySpouse(NamedTuple):
    family_xref: str = ''
    notes: Any = None

    def validate(self) -> bool:
        Defs.verify_type(self.family_xref, str)
        Defs.verify_tuple_type(self.notes, Note)
        return True


class FileTranslations(NamedTuple):
    path: str
    media_type: str = ''

    def validate(self) -> bool:
        Defs.verify_type(self.path, str)
        Defs.verify_type(self.media_type, str)
        return True


class Text(NamedTuple):
    text: str
    mime: str = ''
    language: str = ''

    def validate(self) -> bool:
        Defs.verify_type(self.text, str)
        Defs.verify_type(self.mime, str)
        Defs.verify_type(self.language, str)
        return True


class File(NamedTuple):
    path: str
    media_type: str = ''
    media: str = ''
    phrase: str = ''
    title: str = ''
    file_translations: Any = None

    def validate(self) -> bool:
        Defs.verify_type(self.path, str)
        Defs.verify_type(self.media_type, str)
        Defs.verify_type(self.media, str)
        Defs.verify_type(self.phrase, str)
        Defs.verify_type(self.title, str)
        Defs.verify_tuple_type(self.file_translations, FileTranslations)
        return True


class SourceEvent(NamedTuple):
    event: str = ''
    date_period: str = ''
    phrase: str = ''
    place: Place | None = None
    agency: str = ''
    notes: Any = None

    def validate(self) -> bool:
        Defs.verify_type(self.event, str)
        Defs.verify_type(self.date_period, str)
        Defs.verify_type(self.phrase, str)
        Defs.verify_type(self.place, str)
        Defs.verify_type(self.agency, str)
        Defs.verify_tuple_type(self.notes, Note)
        return True


class NonEvent(NamedTuple):
    no: str = ''
    date: Date | None = None
    phrase: str = ''
    notes: Any = None
    sources: Any = None

    def validate(self) -> bool:
        Defs.verify_type(self.no, str)
        Defs.verify_type(self.date, Date | None)
        Defs.verify_type(self.phrase, str)
        Defs.verify_tuple_type(self.notes, Note)
        Defs.verify_tuple_type(self.sources, SourceEvent)
        return True


class Family(NamedTuple):
    xref: str = ''
    resn: str = ''
    attributes: Any = None
    events: Any = None
    husband: Husband | None = None
    wife: Wife | None = None
    children: tuple[Child] | None = None
    associations: Any = None
    submitters: Any = None
    lds_spouse_sealings: Any = None
    identifiers: Any = None
    notes: Any = None
    citations: Any = None
    multimedia_links: Any = None

    def validate(self) -> bool:
        Defs.verify_type(self.xref, str)
        Defs.verify_type(self.resn, str)
        Defs.verify_tuple_type(self.attributes, FamilyAttribute)
        Defs.verify_tuple_type(self.events, FamilyEvent)
        Defs.verify_type(self.husband, Husband | None)
        Defs.verify_type(self.wife, Wife | None)
        Defs.verify_type(self.children, tuple | None)
        Defs.verify_tuple_type(self.associations, Association)
        Defs.verify_tuple_type(self.submitters, str)
        Defs.verify_tuple_type(self.lds_spouse_sealings, LDSSpouseSealing)
        Defs.verify_tuple_type(self.identifiers, Identifier)
        Defs.verify_tuple_type(self.notes, Note)
        Defs.verify_tuple_type(self.citations, Citation)
        Defs.verify_tuple_type(self.multimedia_links, MultimediaLink)
        return True


class Repository(NamedTuple):
    name: str = ''
    address: Address | None = None
    phones: Any = None
    emails: Any = None
    faxes: Any = None
    wwws: Any = None
    notes: Any = None
    identifiers: Any = None

    def validate(self) -> bool:
        Defs.verify_type(self.name, str)
        Defs.verify_type(self.address, Address | None)
        Defs.verify_tuple_type(self.emails, str)
        Defs.verify_tuple_type(self.faxes, str)
        Defs.verify_tuple_type(self.wwws, str)
        Defs.verify_tuple_type(self.notes, Note)
        Defs.verify_tuple_type(self.identifiers, Identifier)
        return True


class Source(NamedTuple):
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
        Defs.verify_type(self.author, str)
        Defs.verify_type(self.title, str)
        Defs.verify_type(self.abbreviation, str)
        Defs.verify_type(self.published, str)
        Defs.verify_tuple_type(self.events, SourceEvent)
        Defs.verify_tuple_type(self.text, Text)
        Defs.verify_tuple_type(self.repositories, Repository)
        Defs.verify_tuple_type(self.identifiers, Identifier)
        Defs.verify_tuple_type(self.notes, Note)
        Defs.verify_tuple_type(self.multimedia_links, MultimediaLink)
        return True


class Individual(NamedTuple):
    xref: str
    personal_names: Any = None
    sex: str = Gedcom.U
    attributes: Any = None
    events: Any = None
    lds_individual_ordinances: Any = None
    families_child: Any = None
    submitters: Any = None
    associations: Any = None
    aliases: Any = None
    ancestor_interest: Any = None
    descendent_interest: Any = None
    identifiers: Any = None
    notes: Any = None
    sources: Any = None
    multimedia_links: Any = None

    def validate(self) -> bool:
        Defs.verify_type(self.xref, str)
        Defs.verify_tuple_type(self.personal_names, PersonalName)
        Defs.verify_type(self.sex, str)
        Defs.verify_tuple_type(self.attributes, IndividualAttribute)
        Defs.verify_tuple_type(self.events, IndividualEvent)
        Defs.verify_tuple_type(
            self.lds_individual_ordinances, LDSIndividualOrdinances
        )
        Defs.verify_tuple_type(self.families_child, FamilyChild)
        Defs.verify_tuple_type(self.submitters, str)
        Defs.verify_tuple_type(self.associations, Association)
        Defs.verify_tuple_type(self.aliases, Alias)
        Defs.verify_tuple_type(self.ancestor_interest, str)
        Defs.verify_tuple_type(self.descendent_interest, str)
        Defs.verify_tuple_type(self.identifiers, Identifier)
        Defs.verify_tuple_type(self.notes, Note)
        Defs.verify_tuple_type(self.sources, Source)
        Defs.verify_tuple_type(self.multimedia_links, MultimediaLink)
        return True


class Multimedia(NamedTuple):
    files: Any = None
    identifiers: Any = None
    notes: Any = None
    sources: Any = None

    def validate(self) -> bool:
        Defs.verify_tuple_type(self.files, File)
        Defs.verify_tuple_type(self.identifiers, Identifier)
        Defs.verify_tuple_type(self.notes, Note)
        Defs.verify_tuple_type(self.sources, Source)
        return True


class SharedNote(NamedTuple):
    text: str = ''
    mime: str = ''
    language: str = ''
    translations: Any = None
    sources: Any = None
    identifiers: Any = None

    def validate(self) -> bool:
        Defs.verify_type(self.text, str)
        Defs.verify_type(self.mime, str)
        Defs.verify_type(self.language, str)
        Defs.verify_tuple_type(self.translations, NoteTranslation)
        Defs.verify_tuple_type(self.sources, Source)
        Defs.verify_tuple_type(self.identifiers, Identifier)
        return True


class Submitter(NamedTuple):
    name: str = ''
    address: Address | None = None
    phones: Any = None
    emails: Any = None
    faxes: Any = None
    wwws: Any = None
    multimedia_links: Any = None
    languages: Any = None
    identifiers: Any = None
    notes: Any = None

    def validate(self) -> bool:
        Defs.verify_type(self.name, str)
        Defs.verify_type(self.address, Address | None)
        Defs.verify_tuple_type(self.phones, str)
        Defs.verify_tuple_type(self.emails, str)
        Defs.verify_tuple_type(self.faxes, str)
        Defs.verify_tuple_type(self.wwws, str)
        Defs.verify_tuple_type(self.multimedia_links, MultimediaLink)
        Defs.verify_tuple_type(self.languages, str)
        Defs.verify_tuple_type(self.identifiers, Identifier)
        Defs.verify_tuple_type(self.notes, Note)
        return True


class Chronology(Base):
    """Methods to add, update and remove a specific loaded chronology."""

    def __init__(
        self,
        name: str = '',
        filename: str = '',
        calendar: str = GEDSpecial.GREGORIAN,
        log: bool = True,
    ) -> None:
        super().__init__(name, filename, calendar, log)
        self.xref_counter: int = 1
        self.family_xreflist: list[str] = []
        self.individual_xreflist: list[str] = []
        self.multimedia_xreflist: list[str] = []
        self.repository_xreflist: list[str] = []
        self.shared_note_xreflist: list[str] = []
        self.source_xreflist: list[str] = []
        self.submitter_xreflist: list[str] = []

    def _check_tag(
        self, tag: str, dictionary: dict[str, Any] | None = None
    ) -> None:
        if dictionary is None:
            dictionary = self.chron
        if tag not in dictionary:
            dictionary.update({tag: {}})

    def add_event(self, name: str, when: str) -> None:
        self._check_tag(Gedcom.EVEN)
        self.chron[Gedcom.EVEN].update({name: {Gedcom.DATE: when}})
        logging.info(Msg.ADD_EVENT.format(name, self.chron_name))

    ###### GEDCOM Substructures

    # def taginit(self, xref: str, tag: str, info: str = '') -> str:
    #     if info == '':
    #         return f'0 {xref} {tag}\n'
    #     return f'0 {xref} {tag} {str(info).strip()}\n'

    # def taginfo(
    #     self,
    #     level: int,
    #     tag: str,
    #     info: str = '',
    #     extra: str = '',
    # ) -> str:
    #     """Return a GEDCOM formatted line for the information and level.

    #     This is suitable for most tagged lines to guarantee it is uniformly
    #     formatted.  Although the user need not worry about calling this line,
    #     it is provided so the user can see the GEDCOM formatted output
    #     that would result.

    #     See Also
    #     --------

    #     """

    #     if extra == '':
    #         if info == '':
    #             return f'{level} {tag}\n'
    #         return f'{level} {tag} {info}\n'
    #     return f'{level} {tag} {info} {extra}\n'

    def verify_xref(self, xref: str, xreflist: list[str], name: str) -> bool:
        """Check if an xref value in in the proper xreflist."""
        if xref not in xreflist:
            raise ValueError(Msg.NOT_RECORD.format(xref, name))
        return True

    def ged_date(
        self,
        iso_date: str = GEDSpecial.NOW,
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
        date, time = datetime.split(GEDSpecial.T)
        date_pieces = date.split(GEDSpecial.HYPHEN)
        if len(date_pieces) == 3:
            year: str = date_pieces[0]
            month: str = date_pieces[1]
            day: str = date_pieces[2]
        else:
            year = date_pieces[1]
            month = date_pieces[2]
            day = date_pieces[3]
        ged_time: str = ''.join([time, GEDSpecial.Z])
        good_calendar: str | bool = GEDDateTime.CALENDARS.get(
            GEDSpecial.GREGORIAN, False
        )
        if not good_calendar:
            logging.critical(Msg.BAD_CALENDAR.format(self.calendar))
            raise ValueError(Msg.BAD_CALENDAR.format(self.calendar))
        month_code: str = GEDDateTime.CALENDARS[self.calendar][
            GEDSpecial.MONTH_NAMES
        ].get(month, False)
        if not month_code:
            logging.critical(Msg.BAD_MONTH.format(self.calendar, month))
            raise ValueError(Msg.BAD_MONTH.format(self.calendar, month))
        ged_date: str = ''
        if epoch and len(date_pieces) == 4:
            ged_date = ''.join(
                [
                    day,
                    GEDSpecial.SPACE,
                    month_code,
                    GEDSpecial.SPACE,
                    year,
                    GEDSpecial.SPACE,
                    GEDSpecial.BC,
                ]
            )
        else:
            ged_date = ''.join(
                [day, GEDSpecial.SPACE, month_code, GEDSpecial.SPACE, year]
            )
        return ged_date, ged_time

    def iso_date(
        self,
        ged_date: str,
        ged_time: str = '',
        # calendar: str = GEDSpecial.GREGORIAN,
    ) -> str:
        """Return an ISO date and time given a GEDCOM date and time."""
        day: str
        month: str
        year: str
        day, month, year = ged_date.split(GEDSpecial.SPACE)
        time: str = ged_time.split(GEDSpecial.Z)[0]
        good_calendar: str | bool = ISOMonths.CALENDARS.get(
            GEDSpecial.GREGORIAN, False
        )
        if not good_calendar:
            logging.critical(Msg.BAD_CALENDAR.format(self.calendar))
            raise ValueError(Msg.BAD_CALENDAR.format(self.calendar))
        month_code: str = ISOMonths.CALENDARS[self.calendar].get(month, False)
        if not month_code:
            logging.critical(Msg.BAD_MONTH.format(self.calendar, month))
            raise ValueError(Msg.BAD_MONTH.format(self.calendar, month))
        iso_datetime: str = ''.join(
            [
                year,
                GEDSpecial.HYPHEN,
                month_code,
                GEDSpecial.HYPHEN,
                day,
                GEDSpecial.T,
                time,
            ]
        )
        return iso_datetime

    def now(self, level: int = 2) -> str:
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
        >>> a = Chronology(name='testing')
        >>> a.now()
        ['2 DATE 05 DEC 2024', '3 TIME 02:58:19Z']

        Changing the level adjusts the level numbers for the two returned strings.

        >>> a = Chronology(name='testing')
        >>> a.now(level=5)
        ['5 DATE 05 DEC 2024', '6 TIME 02:58:19Z']

        See Also
        --------
        - `creation_date`
        - `change_date`
        - `header`
        """
        date: str
        time: str
        date, time = self.ged_date()
        return ''.join(
            [
                Defs.taginfo(level, Gedcom.DATE, date),
                Defs.taginfo(level + 1, Gedcom.TIME, time),
            ]
        )

    def change_date(self, note: Note | None = None) -> str:
        """Return three GEDCOM lines showing a line with a change tag
        and then two automatically generated
        UTC date and time lines.  These are used to
        show when a record has been modified.

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
        if note is None:
            # note = Note('', '', '', [], [])
            return ''.join(
                [
                    Defs.taginfo(1, Gedcom.CHAN),
                    self.now(),
                ]
            )
        return ''.join(
            [
                Defs.taginfo(1, Gedcom.CHAN),
                self.now(),
                self.note_structure(note),
            ]
        )

    def creation_date(self) -> str:
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
        return ''.join([Defs.taginfo(1, Gedcom.CREA), self.now()])

    def date_value(
        self,
        date: Date,
        time: Time | None = None,
        phrase: str = '',
        level: int = 1,
        epoch: str = '',
    ) -> str:
        if time is None:
            time = Time(0, 0, 0)
        # Do checks on numeric input.
        if date.day < 1 or not isinstance(date.day, int):
            raise ValueError(Msg.NOT_POSITIVE.format(str(date.day)))
        if date.month < 1 or not isinstance(date.month, int):
            raise ValueError(Msg.NOT_POSITIVE.format(str(date.month)))
        if not isinstance(date.year, int):
            raise ValueError(Msg.NOT_POSITIVE.format(str(date.year)))
        if time.hour < 0 or not isinstance(time.hour, int):
            raise ValueError(Msg.NOT_POSITIVE.format(str(time.hour)))
        if time.minute < 0:
            raise ValueError(Msg.NOT_POSITIVE.format(str(time.minute)))
        if time.second < 0:
            raise ValueError(Msg.NOT_POSITIVE.format(str(time.second)))

        # Format for insertion.
        day_str: str = str(date.day)
        month_str: str = str(date.month)
        if len(month_str) == 1:
            month_str = ''.join(['0', month_str])
        max_months: int = GEDDateTime.CALENDARS[self.calendar][
            GEDSpecial.MAX_MONTHS
        ]
        if date.month > max_months:
            raise ValueError(Msg.TOO_MANY_MONTHS.format(str(date.month)))
        max_days: int = GEDDateTime.CALENDARS[self.calendar][
            GEDSpecial.MONTH_MAX_DAYS
        ][month_str]
        month_str = GEDDateTime.CALENDARS[self.calendar][
            GEDSpecial.MONTH_NAMES
        ][month_str]
        if date.day > max_days:
            raise ValueError(Msg.TOO_MANY_DAYS.format(str(date.day), month_str))
        year_str: str = str(date.year)
        hour_str: str = str(time.hour)
        minute_str: str = str(time.minute)
        second_str: str = str(time.second)
        if len(day_str) == 1:
            day_str = ''.join(['0', day_str])

        if len(hour_str) == 1:
            hour_str = ''.join(['0', hour_str])
        if len(minute_str) == 1:
            minute_str = ''.join(['0', minute_str])
        if len(second_str) == 1:
            second_str = ''.join(['0', second_str])

        if date.year < 0 and epoch != '':
            year_str = ''.join([str(-date.year), ' ', epoch])
        time_str = ''.join([hour_str, ':', minute_str, ':', second_str])
        date_str = ''.join([day_str, ' ', month_str, ' ', year_str])
        # if len(date) == 0:
        #     logging.error(Msg.NO_VALUE)
        #     raise ValueError(Msg.NO_VALUE)
        if time == Time(0, 0, 0) and phrase == '':
            return Defs.taginfo(level, Gedcom.DATE, date_str)
        if time != Time(0, 0, 0) and phrase == '':
            return ''.join(
                [
                    Defs.taginfo(level, Gedcom.DATE, date_str),
                    Defs.taginfo(level + 1, Gedcom.TIME, time_str),
                ]
            )
        if time == Time(0, 0, 0) and phrase != '':
            return ''.join(
                [
                    Defs.taginfo(level, Gedcom.DATE, date_str),
                    Defs.taginfo(level + 1, Gedcom.PHRASE, phrase),
                ]
            )
        return ''.join(
            [
                Defs.taginfo(level, Gedcom.DATE, date_str),
                Defs.taginfo(level + 1, Gedcom.TIME, time_str),
                Defs.taginfo(level + 1, Gedcom.PHRASE, phrase),
            ]
        )

    ###### Methods to Assisting Building GEDCOM Records

    # def address_structure(
    #     self,
    #     address: str = '',
    #     city: str = '',
    #     state: str = '',
    #     postal: str = '',
    #     country: str = '',
    #     level: int = 1,
    # ) -> str:
    # """Add address information.

    # Each address line is a list of five strings:
    # - Mailing Address: Each line of the mailing label is separated by `\n`.
    # - City: The city or and empty string to leave this blank.
    # - State: The state or an empty string to leave this blank.
    # - Postal Code: The postal code or an empty string to leave this blank.
    # - Country: The country or an empty string to leave this blank.

    # One does not have to call this method directly.  The GEDCOM record methods
    # call it when creating a chronology.  However, one can use it to
    # see what the address information one provides would look like
    # in a GEDCOM file.

    # Example
    # -------
    # In the first example note the five strings in the list.  Also note
    # that the country was not specified but nonetheless an empty string
    # was added as a placeholder for the absent country information.
    # Note the `\n` to separate the two address lines.
    # [
    #     '12345 ABC Street\nSouth North City, My State 23456',
    #     'South North City',
    #     'My State',
    #     '23456',
    #     ''
    # ]

    # The GEDCOM record would appear as the following:

    # 1 ADDR 12345 ABC Street
    # 1 CONT South North City, My State 23456
    # 2 CITY South North City
    # 2 STAE My State
    # 2 POST 23456

    # The following is the minimum amount of information for an address.
    # [
    #     '12345 ABC Street\nSouth North City, My State 23456',
    # ]

    # If one does not want to use the `\n` one can write the following
    # provided one imports the GEDSpecial class.  One way to do that is
    # by adding the following line at the top of the cell:

    # The GEDCOM record would appear as the following:

    # 1 ADDR 12345 ABC Street
    # 1 CONT South North City, My State 23456

    # If the list is empty the method returns the empty list.

    # """
    # lines: str = ''
    # if address != '':
    #     address_lines = address.split('\n')
    #     for line in address_lines:
    #         if line == '':
    #             address_lines.remove(line)
    #     lines = ''.join(
    #         [
    #             lines,
    #             Defs.taginfo(level, Gedcom.ADDR, address_lines[0].strip()),
    #         ]
    #     )
    #     for line in address_lines[1:]:
    #         lines = ''.join(
    #             [lines, Defs.taginfo(level, Gedcom.CONT, line.strip())]
    #         )
    #     if city != '':
    #         lines = ''.join(
    #             [lines, Defs.taginfo(level + 1, Gedcom.CITY, city.strip())]
    #         )
    #     if state != '':
    #         lines = ''.join(
    #             [lines, Defs.taginfo(level + 1, Gedcom.STAE, state.strip())]
    #         )
    #     if postal != '':
    #         lines = ''.join(
    #             [
    #                 lines,
    #                 Defs.taginfo(
    #                     level + 1, Gedcom.POST, str(postal).strip()
    #                 ),
    #             ]
    #         )
    #     if country != '':
    #         lines = ''.join(
    #             [
    #                 lines,
    #                 Defs.taginfo(level + 1, Gedcom.CTRY, country.strip()),
    #             ]
    #         )
    # return lines

    def association_structure(
        self, xref: str, association: Association, level: int = 1
    ) -> str:
        """Add association information."""
        lines: str = ''
        if self.verify_xref(xref, self.individual_xreflist, Record.INDIVIDUAL):
            lines = ''.join([lines, Defs.taginfo(level, Gedcom.ASSO, xref)])
            association.ged(1)
        #     if association.association_phrase != '':
        #         lines = ''.join(
        #             [
        #                 lines,
        #                 Defs.taginfo(
        #                     level + 1,
        #                     Gedcom.PHRASE,
        #                     association.association_phrase,
        #                 ),
        #             ]
        #         )
        #     if association.role in Enum.ROLE:
        #         lines = ''.join(
        #             [
        #                 lines,
        #                 Defs.taginfo(level + 2, Gedcom.ROLE, association.role),
        #             ]
        #         )
        #         if association.role_phrase != '':
        #             lines = ''.join(
        #                 [
        #                     lines,
        #                     Defs.taginfo(
        #                         level + 2,
        #                         Gedcom.PHRASE,
        #                         association.role_phrase,
        #                     ),
        #                 ]
        #             )
        #     else:
        #         raise ValueError(
        #             Msg.NOT_VALID_ENUM.format(association.role, EnumName.ROLE)
        #         )
        #     for note in association.notes:
        #         lines = ''.join([lines, self.note_structure(note)])
        #     for citation in association.citations:
        #         lines = ''.join([lines, self.source_citation(citation)])
        # else:
        #     raise ValueError(
        #         Msg.NOT_RECORD.format(association.xref, Record.INDIVIDUAL)
        #     )
        return lines

    def event_detail(self, event: list[Any], level: int = 1) -> str:
        """Add event detail information."""
        lines: str = ''
        return lines

    def family_attribute_structure(
        self, attribute: list[Any], level: int = 1
    ) -> str:
        """Add attribute information."""
        lines: str = ''
        return lines

    def family_event_detail(self, detail: list[Any], level: int = 1) -> str:
        """Add family event detail information."""
        lines: str = ''
        return lines

    def family_event_structure(self, event: list[Any], level: int = 1) -> str:
        """Add family event information."""
        lines: str = ''
        return lines

    def identifier_structure(
        self, identifier: list[str], level: int = 1
    ) -> str:
        """Add an identifier to a record.

        Each identifier is a list contain at least two strings and at most three.
        The first string is the kind of identifier.
        The second string is the identifier itself.
        The optional third is the type of identifier.
        """
        lines: str = ''
        if (
            identifier[0] in Enum.ID
            and len(identifier) > 1
            and len(identifier) < 4
        ):
            if len(identifier) > 1:
                lines = ''.join(
                    [lines, Defs.taginfo(level, identifier[0], identifier[1])]
                )
            if len(identifier) > 2:
                lines = ''.join(
                    [lines, Defs.taginfo(level + 1, Gedcom.TYPE, identifier[2])]
                )
        return lines

    def individual_attribute_structure(
        self, attribute: list[Any], level: int = 1
    ) -> str:
        """Add individual attribute information."""
        lines: str = ''
        return lines

    def individual_event_detail(self, detail: list[Any], level: int = 1) -> str:
        """Add individual event detail information."""
        lines: str = ''
        return lines

    def individual_event_structure(
        self, event: list[Any], level: int = 1
    ) -> str:
        """Add individual event information."""
        lines: str = ''
        return lines

    def lds_individual_ordinance(
        self, ordinance: list[Any], level: int = 1
    ) -> str:
        """Add LDS individual ordinance information."""
        lines: str = ''
        return lines

    def lds_ordinance_detail(self, detail: list[Any], level: int = 1) -> str:
        """Add LDS ordinance detail information."""
        lines: str = ''
        return lines

    def lds_spouse_sealing(self, spouse: list[Any], level: int = 1) -> str:
        """Add LDS spouse sealing information."""
        lines: str = ''
        return lines

    def multimedia_link(self, media: list[Any], level: int = 1) -> str:
        """Add multimedia information."""
        lines: str = ''
        if len(media) > 0:
            lines = ''.join([lines, Defs.taginfo(level, Gedcom.OBJE, media[0])])
            if len(media) == 6:
                lines = ''.join(
                    [
                        lines,
                        Defs.taginfo(level + 1, Gedcom.CROP),
                        Defs.taginfo(level + 2, Gedcom.TOP, media[1]),
                        Defs.taginfo(level + 2, Gedcom.LEFT, media[2]),
                        Defs.taginfo(level + 2, Gedcom.HEIGHT, media[3]),
                        Defs.taginfo(level + 2, Gedcom.WIDTH, media[4]),
                        Defs.taginfo(level + 1, Gedcom.TITL, media[5]),
                    ]
                )
            if len(media) == 2:
                lines = ''.join(
                    [lines, Defs.taginfo(level + 1, Gedcom.TITL, media[1])]
                )
        return lines

    def non_event_structure(self, event: list[Any], level: int = 1) -> str:
        """Add non event information."""
        lines: str = ''
        return lines

    def note_structure(self, note: Note, level: int = 1) -> str:
        """Add note information."""
        # if note is None:
        #     note = ()
        lines: str = ''
        # if note != ():
        if note.mime != '' and note.mime not in Enum.MEDIA_TYPE:
            raise ValueError(
                Msg.NOT_VALID_ENUM.format(note.mime, EnumName.MEDIA_TYPE)
            )
        if note.text != '':
            lines = ''.join(
                [lines, Defs.taginfo(level, Gedcom.NOTE, note.text)]
            )
            if note.mime != '':
                lines = ''.join(
                    [lines, Defs.taginfo(level + 1, Gedcom.MIME, note.mime)]
                )
            if note.language != '':
                lines = ''.join(
                    [lines, Defs.taginfo(level + 1, Gedcom.LANG, note.language)]
                )
            for trans in note.translation:
                lines = ''.join(
                    [lines, Defs.taginfo(level, Gedcom.TRAN, trans.text)]
                )

                if trans.mime not in Enum.MEDIA_TYPE:
                    raise ValueError(
                        Msg.NOT_VALID_ENUM.format(
                            trans.mime, EnumName.MEDIA_TYPE
                        )
                    )
                lines = ''.join(
                    [lines, Defs.taginfo(level + 1, Gedcom.MIME, trans.mime)]
                )
                lines = ''.join(
                    [
                        lines,
                        Defs.taginfo(level + 1, Gedcom.LANG, trans.language),
                    ]
                )
        for cite in note.citations:
            lines = ''.join([lines, self.source_citation(cite)])
        return lines

    # def personal_name_pieces(self, name: PersonalName, level: int = 1) -> str:
    #     """Add pieces of personal name information."""
    #     if name.tag in Enum.PERSONAL_NAME:
    #         personal_name = Defs.taginfo(level, name.tag, name.text.strip())
    #     return personal_name

    def personal_name_structure(
        self,
        name: str,
        type_name: str,
        phrase: str,
        pieces: Any = None,
        translations: Any = None,
        notes: Any = None,
        sources: Any = None,
        level: int = 1,
    ) -> str:
        """Add note information."""
        Defs.verify_enum(type_name, Enum.NAME_TYPE, EnumName.NAME_TYPE)
        lines: str = ''.join(
            [
                Defs.taginfo(level, Gedcom.NAME, name),
                Defs.taginfo(level + 1, Gedcom.TYPE, type_name),
            ]
        )
        if phrase != '':
            lines = ''.join(
                [lines, Defs.taginfo(level + 2, Gedcom.PHRASE, phrase)]
            )
        if pieces is not None and len(pieces) > 0:
            for piece in pieces:
                lines = ''.join(
                    # [lines, self.personal_name_pieces(piece, level + 1)]
                    [lines, piece.ged(level + 1)]
                )
        if translations is not None and len(translations) > 0:
            for translation in translations:
                lines = ''.join(
                    [lines, self.translation(translation, level=level + 1)]
                )
        return lines

    def place_structure(self, place: list[Any], level: int = 1) -> str:
        """Add note information."""

        lines: str = ''
        return lines

    def source_citation(self, source: Citation, level: int = 1) -> str:
        """Add source citation information."""
        lines: str = ''
        return lines

    def source_repository_citation(
        self, repository: Any, level: int = 1
    ) -> str:
        """Add source repository information."""
        lines: str = ''
        return lines

    def translation(self, trans: Name_Translation, level: int = 1) -> str:
        lines: str = ''.join(
            [
                Defs.taginfo(level, Gedcom.TRAN, trans.text),
                Defs.taginfo(level + 1, Gedcom.LANG, trans.language),
                Defs.taginfo(level + 1, trans.piece.tag, trans.piece.text),
            ]
        )
        return lines

    ###### GEDCOM Records

    def contact(
        self,
        phones: list[str] | None = None,
        emails: list[str] | None = None,
        faxes: list[str] | None = None,
        wwws: list[str] | None = None,
        level: int = 1,
    ) -> str:
        """Return a string of contact options.

        Although this method is not expected to be used directly by the user,
        the user may find it useful to how how the specific contact information
        would be represented in a GEDCOM file.

        See Also
        --------
        """
        if phones is None:
            phones = []
        if emails is None:
            emails = []
        if faxes is None:
            faxes = []
        if wwws is None:
            wwws = []
        lines: str = ''
        for phone in phones:
            lines = ''.join([lines, Defs.taginfo(level, Gedcom.PHON, phone)])
        for email in emails:
            lines = ''.join([lines, Defs.taginfo(level, Gedcom.EMAIL, email)])
        for fax in faxes:
            lines = ''.join([lines, Defs.taginfo(level, Gedcom.FAX, fax)])
        for www in wwws:
            lines = ''.join([lines, Defs.taginfo(level, Gedcom.WWW, www)])
        return lines

    def next_counter(
        self, xref_list: list[str], xref_type: str, xref_name: str = ''
    ) -> str:
        """Allows one to override a numeric counter for a name as identifier for a record.

        This overriding works for family and individual records.

        The identifier name can be composed of upper case letters, digits or the underscore
        based on the
        [GEDCOM Standard](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#cb3-5).

        The value of naming individuals and families is for comparison purposes
        between two different chronologies that reference the same individuals or
        familys.  With the same identifiers they can more easily be searched.

        See Also
        --------
        - `family_xref`
        - `individual_xref`
        - `named_family_xref`
        - `named_individual_xref`
        """
        xref: str = ''
        if xref_name != '':
            modified_name = str(xref_name).strip().upper().replace(' ', '_')
            xref = ''.join(
                [
                    GEDSpecial.ATSIGN,
                    modified_name,
                    GEDSpecial.ATSIGN,
                ]
            )
            self.named_xreflist.append([xref_type, modified_name])
            xref_list.append(xref)
            return xref
        counter: int = self.xref_counter
        xref = ''.join([GEDSpecial.ATSIGN, str(counter), GEDSpecial.ATSIGN])
        xref_list.append(xref)
        self.xref_counter += 1
        return xref

    def family_xref(self, xref_name: str = '') -> str:
        """Create a cross reference identifier for a family.

        A family may reference many individuals.  An individual
        may reference many families.  This method creates
        the reference identifier for a family without specifying
        reference identifiers for its members.

        See Also
        --------
        - `individual_xref`: create a cross reference identifier for an individual.

        Examples
        --------
        Examples of both `individual_xref` and `family_xref` are provided
        with the `individual_xref` documentation.

        The following chronology has only two events in it both under a family record.

        >>> from chronodata.chrono import Chronology
        >>>
        >>> c = Chronology('mankind')
        >>> c.family_record(
        >>>    xref_family=c.family_xref(),
        >>>    family_events=[]
        >>> )

        The GEDCOM file for this chronology would look like the following.

        For an example of how ChronoData was used to compare various such
        chronologies, see
        """
        return self.next_counter(
            xref_list=self.family_xreflist,
            xref_type=Gedcom.FAM,
            xref_name=xref_name,
        )

    # def named_xref(self, search_for: str = '', pandas: bool = True) -> pd.DataFrame | list[list[str]]:
    #     """Report on the family and individuals with named identifiers."""
    #     names_index = list(range(1, len(self.named_xreflist) + 1))
    #     if pandas:
    #         return pd.DataFrame(
    #             data=self.named_xreflist,
    #             columns=['Group', 'Name'],
    #             index=names_index,
    #         )
    #     return self.named_

    def individual_xref(self, xref_name: str = '') -> str:
        """Create a cross reference identifier for an individual.

        A individual may reference different families one where
        the individual is a parent in one marriage and another where the individual
        is a child or has been adopted or may be a distant descendent.  This method creates
        the reference identifier for an individual without associating
        it with reference identifiers for its families.

        The other five record types (`multimedia`, `repository`, `shared_note`,
        `source` and `submitter`) return a cross reference identifier
        which should be saved since they will be needed in individual and family
        records.

        See Also
        --------
        - `family_xref`: create a cross reference identifier for a family.

        Example
        -------
        One could start a chronology by getting reference identifiers
        for the individuals and the families in any order.  Once one has
        the identifiers one can build out the individual and family records.

        >>> from chronodata.chrono import Chronology
        >>>
        >>> c = Chronology('adam to seth')
        >>> adam = c.individual_xref()
        >>> adameve = c.family_xref()
        >>> eve = c.individual_xref()
        >>> cain = c.individual_xref()
        >>> abel = c.individual_xref()
        >>> seth = c.individual_xref()
        >>> c.family_record(
        >>>     xref_family=adameve,
        >>>     husband=adam,
        >>>     wife=eve,
        >>>     children=[cain,abel,seth]
        >>> )
        >>> c.individual_record(
        >>>     xref_individual=adam,
        >>>     families_spouse=[adameve]
        >>> )
        >>> c.individual_record(
        >>>    xref_individual=eve,
        >>>    families_spouse=[adameve]
        >>> )
        >>> c.individual_record(
        >>>    xref_individual=cain,
        >>>    families_child=[adameve]
        >>> )
        >>> c.individual_record(
        >>>    xref_individual=abel,
        >>>    families_child=[adameve]
        >>> )
        >>> c.individual_record(
        >>>    xref_individual=seth,
        >>>    families_child=[adameve]
        >>> )

        One would get the following GEDCOM record:


        Various chronologies for the Ancient Near East have been constructed.
        They do not all agree with each other, but one can compare them
        to identifiy specifically where they disagree and decide which
        represents the best view of ancient history.


        Something similar could be even for non-biological transitions
        such as the decay of uranium-238 to lead-206.

        >>> from chronodata.chrono import Chronology
        >>>
        >>> c = Chronology('uranium to lead')
        >>> uranium = c.individual_xref()
        >>> lead = c.individual_xref()
        >>> uranium_lead = c.family_xref()
        >>> c.individual_record(
        >>>     xref_individual=uranium,
        >>>     families_spouse=[uranium_lead],
        >>> )
        >>> c.individual_record(
        >>>     xref_individual=lead,
        >>>     families_child=[uranium_lead]
        >>> )
        >>> c.family_record(
        >>>     xref_family=uranium_lead,
        >>>     wife=uranium,
        >>>     child=[lead]
        >>> )

        A complete example of the state transitions from uranium-238 to
        lead is provided in the example section.


        """
        return self.next_counter(
            xref_list=self.individual_xreflist,
            xref_type=Gedcom.INDI,
            xref_name=xref_name,
        )

    def family_record(
        self,
        xref: str,
        resn: str = '',
        family_attributes: list[Any] | None = None,
        family_events: list[Any] | None = None,
        family_non_events: list[Any] | None = None,
        husband: str = GEDSpecial.VOID,
        husband_phrase: str = '',
        wife: str = GEDSpecial.VOID,
        wife_phrase: str = '',
        children: list[Any] | None = None,
        associations: list[Association] | None = None,
        submitters: list[Any] | None = None,
        lds_spouse_sealing: list[Any] | None = None,
        identifiers: list[Any] | None = None,
        notes: list[Any] | None = None,
        sources: list[Any] | None = None,
        multimedia: list[Any] | None = None,
    ) -> None:
        """Create a detailed record for a family.

        Prior to calling this one will need a family cross reference
        identifier.  This can be obtained by running the `family_xref`
        method which will return the needed identifier.

        Parameter
        ---------
        - xref_family: The cross reference identifier obtained from the
            `family_xref` method.
        - resn: A flag specifying if access to the record must be restricted.
        - family_attributes: list[Any] | None = None,
        - family_events: list[Any] | None = None,
        - family_non_events: list[Any] | None = None,
        - husband: str = GEDSpecial.VOID,
        - husband_phrase: str = '',
        - wife: str = GEDSpecial.VOID,
        - wife_phrase: str = '',
        - children: list[Any] | None = None,
        - associations: list[Any] | None = None,
        - submitters: list[Any] | None = None,
        - lds_spouse_sealing: list[Any] | None = None,
        - identifiers: list[Any] | None = None,
        - notes: list[Any] | None = None,
        - sources: list[Any] | None = None,
        - multimedia: list[Any] | None = None,

        Exceptions
        ----------
        - A value error is raised if the family cross reference identifier
        has not been created in advance and used for the `xref_family` parameter.
        ` A value error is raised if the `husband` cross reference identifier
        has not been created in advance using the `individual_xref` method.
        ` A value error is raised if the `wife` cross reference identifier
        has not been created in advance using the `individual_xref` method.
        ` A value error is raised if any of the `children`
        do not have a cross reference identifier that was
        created in advance using the `individual_xref` method.
        - A value error is raised if the
        [reason code](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#enumset-RESN)
        for restricting
        the record is not in the set of valid reason codes.

        Reference
        ---------
        - [GEDCOM Specification](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html)

        See Also
        --------
        - family_xref: Create a family cross reference identifier.
        - individual_xref: Create an individual cross reference identifier.
        """

        if associations is None:
            associations = []
        if children is None:
            children = []
        if family_attributes is None:
            family_attributes = []
        if family_events is None:
            family_events = []
        if family_non_events is None:
            family_non_events = []
        if identifiers is None:
            identifiers = []
        if lds_spouse_sealing is None:
            lds_spouse_sealing = []
        if multimedia is None:
            multimedia = []
        if notes is None:
            notes = []
        if sources is None:
            sources = []
        if submitters is None:
            submitters = []
        if xref not in self.family_xreflist:
            raise ValueError(Msg.NOT_RECORD.format(xref, Record.FAMILY))
        if resn != '' and resn not in Enum.RESN:
            raise ValueError(Msg.NOT_VALID_ENUM.format(resn, EnumName.RESN))
        if (
            husband != GEDSpecial.VOID
            and husband not in self.individual_xreflist
        ):
            raise ValueError(Msg.NOT_RECORD.format(husband, Record.INDIVIDUAL))
        if wife != GEDSpecial.VOID and wife not in self.individual_xreflist:
            raise ValueError(Msg.NOT_RECORD.format(wife, Record.INDIVIDUAL))
        for child in children:
            if (
                child != GEDSpecial.VOID
                and child not in self.individual_xreflist
            ):
                raise ValueError(
                    Msg.NOT_RECORD.format(child, Record.INDIVIDUAL)
                )
        ged_family: str = Defs.taginit(xref, Gedcom.FAM)
        if resn != '' and resn in Enum.RESN:
            ged_family = ''.join(
                [ged_family, Defs.taginfo(1, Gedcom.RESN, resn)]
            )
        for attribute in family_attributes:
            ged_family = ''.join(
                [ged_family, self.family_attribute_structure(attribute)]
            )
        for event in family_events:
            ged_family = ''.join(
                [ged_family, self.family_event_structure(event)]
            )
        for non_event in family_non_events:
            ged_family = ''.join(
                [ged_family, self.non_event_structure(non_event)]
            )
        ged_family = ''.join(
            [ged_family, Defs.taginfo(1, Gedcom.HUSB, husband)]
        )
        if husband_phrase != '':
            ged_family = ''.join(
                [ged_family, Defs.taginfo(2, Gedcom.PHRASE, husband_phrase)]
            )
        ged_family = ''.join([ged_family, Defs.taginfo(1, Gedcom.WIFE, wife)])
        if wife_phrase != '':
            ged_family = ''.join(
                [ged_family, Defs.taginfo(2, Gedcom.PHRASE, wife_phrase)]
            )
        for child, phrase in children:
            ged_family = ''.join(
                [ged_family, Defs.taginfo(1, Gedcom.CHIL, child)]
            )
            if phrase != '':
                ged_family = ''.join(
                    [ged_family, Defs.taginfo(2, Gedcom.PHRASE, phrase)]
                )
        for association in associations:
            ged_family = ''.join(
                [ged_family, self.association_structure(association)]
            )
        for submitter in submitters:
            ged_family = ''.join(
                [ged_family, Defs.taginfo(1, Gedcom.SUBM, submitter)]
            )
        for spouse in lds_spouse_sealing:
            ged_family = ''.join([ged_family, self.lds_spouse_sealing(spouse)])
        for identifier in identifiers:
            ged_family = ''.join(
                [ged_family, self.identifier_structure(identifier)]
            )
        for note in notes:
            ged_family = ''.join([ged_family, self.note_structure(note)])
        for source in sources:
            ged_family = ''.join([ged_family, self.source_citation(source)])
        for media in multimedia:
            ged_family = ''.join([ged_family, self.multimedia_link(media)])
        ged_family = ''.join([ged_family, self.creation_date()])
        self.ged_family = ''.join([self.ged_family, ged_family])
        logging.info(Msg.ADDED_RECORD.format(Record.FAMILY, xref))

    def individual_record(
        self,
        xref: str,
        resn: str = '',
        personal_names: list[Any] | None = None,
        sex: str = '',
        attributes: list[Any] | None = None,
        events: list[Any] | None = None,
        non_events: list[Any] | None = None,
        lds_individual_ordinances: list[Any] | None = None,
        families_child: list[Any] | None = None,
        families_spouse: list[Any] | None = None,
        submitters: list[Any] | None = None,
        associations: list[Any] | None = None,
        aliases: list[str] | None = None,
        ancestor_interest: list[str] | None = None,
        descendent_interest: list[str] | None = None,
        identifiers: list[Any] | None = None,
        notes: list[Any] | None = None,
        sources: list[Any] | None = None,
        multimedia: list[Any] | None = None,
    ) -> None:
        if aliases is None:
            aliases = []
        if ancestor_interest is None:
            ancestor_interest = []
        if associations is None:
            associations = []
        if attributes is None:
            attributes = []
        if descendent_interest is None:
            descendent_interest = []
        if events is None:
            events = []
        if families_child is None:
            families_child = []
        if families_spouse is None:
            families_spouse = []
        if identifiers is None:
            identifiers = []
        if lds_individual_ordinances is None:
            lds_individual_ordinances = []
        if multimedia is None:
            multimedia = []
        if non_events is None:
            non_events = []
        if notes is None:
            notes = []
        if personal_names is None:
            personal_names = []
        if sources is None:
            sources = []
        if submitters is None:
            submitters = []
        if xref not in self.individual_xreflist:
            raise ValueError(Msg.NOT_RECORD.format(xref, Record.INDIVIDUAL))
        if resn != '' and resn not in Enum.RESN:
            raise ValueError(Msg.NOT_VALID_ENUM.format(resn, EnumName.RESN))
        if sex != '' and sex not in Enum.SEX:
            raise ValueError(Msg.NOT_VALID_ENUM.format(sex, EnumName.SEX))
        for family in families_child:
            if len(family) > 1 and family[1] not in Enum.PEDI:
                raise ValueError(
                    Msg.NOT_VALID_ENUM.format(family[3], EnumName.PEDI)
                )
            if len(family) > 3 and family[3] not in Enum.STAT:
                raise ValueError(
                    Msg.NOT_VALID_ENUM.format(family[3], EnumName.STAT)
                )
        for alias in aliases:
            if alias[0] not in self.individual_xreflist:
                raise ValueError(
                    Msg.NOT_RECORD.format(alias[0], Record.INDIVIDUAL)
                )
        for interest in ancestor_interest:
            if interest not in self.submitter_xreflist:
                raise ValueError(
                    Msg.NOT_RECORD.format(interest, Record.SUBMITTER)
                )
        for interest in descendent_interest:
            if interest not in self.submitter_xreflist:
                raise ValueError(
                    Msg.NOT_RECORD.format(interest, Record.SUBMITTER)
                )
        for submitter in submitters:
            if submitter not in self.submitter_xreflist:
                raise ValueError(
                    Msg.NOT_RECORD.format(submitter, Record.SUBMITTER)
                )
        ged_individual: str = Defs.taginit(xref, Gedcom.INDI)
        if resn != '' and resn in Enum.RESN:
            ged_individual = ''.join(
                [ged_individual, Defs.taginfo(1, Gedcom.RESN, resn)]
            )
        for name in personal_names:
            ged_individual = ''.join(
                [ged_individual, self.personal_name_structure(name)]
            )
        if sex != '' and sex in Enum.SEX:
            ged_individual = ''.join(
                [ged_individual, Defs.taginfo(1, Gedcom.SEX, sex)]
            )
        for attribute in attributes:
            ged_individual = ''.join(
                [ged_individual, self.individual_attribute_structure(attribute)]
            )
        for event in events:
            ged_individual = ''.join(
                [ged_individual, self.individual_event_structure(event)]
            )
        for non_event in non_events:
            ged_individual = ''.join(
                [ged_individual, self.non_event_structure(non_event)]
            )
        for ordinance in lds_individual_ordinances:
            ged_individual = ''.join(
                [ged_individual, self.lds_individual_ordinance(ordinance)]
            )
        for family in families_child:
            if family[0] in self.family_xreflist:
                ged_individual = ''.join(
                    [ged_individual, Defs.taginfo(1, Gedcom.FAMC, family[0])]
                )
                if len(family) > 1:
                    ged_individual = ''.join(
                        [
                            ged_individual,
                            Defs.taginfo(2, Gedcom.PEDI, family[1]),
                        ]
                    )
                    if len(family) > 2:
                        ged_individual = ''.join(
                            [
                                ged_individual,
                                Defs.taginfo(3, Gedcom.PHRASE, family[2]),
                            ]
                        )
                if len(family) > 3:
                    ged_individual = ''.join(
                        [
                            ged_individual,
                            Defs.taginfo(2, Gedcom.STAT, family[2]),
                        ]
                    )
                    if len(family) > 4:
                        ged_individual = ''.join(
                            [
                                ged_individual,
                                Defs.taginfo(3, Gedcom.PHRASE, family[3]),
                            ]
                        )
        for family in families_spouse:
            if family[0] in self.family_xreflist:
                ged_individual = ''.join(
                    [ged_individual, Defs.taginfo(1, Gedcom.FAMS, family[0])]
                )
                if len(family) > 1:
                    ged_individual = ''.join(
                        [ged_individual, self.note_structure(family[1])]
                    )
        for submitter in submitters:
            if submitter in self.submitter_xreflist:
                ged_individual = ''.join(
                    [ged_individual, Defs.taginfo(1, Gedcom.SUBM, submitter)]
                )
        for association in associations:
            ged_individual = ''.join(
                [ged_individual, self.association_structure(association)]
            )
        for alias in aliases:
            if alias[0] in self.individual_xreflist:
                ged_individual = ''.join(
                    [ged_individual, Defs.taginfo(1, Gedcom.ALIA, alias[0])]
                )
                if len(alias) > 1 and alias[1] != '':
                    ged_individual = ''.join(
                        [
                            ged_individual,
                            Defs.taginfo(2, Gedcom.PHRASE, alias[1]),
                        ]
                    )
        for interest in ancestor_interest:
            if interest in self.submitter_xreflist:
                ged_individual = ''.join(
                    [ged_individual, Defs.taginfo(1, Gedcom.ANCI, interest)]
                )
        for interest in descendent_interest:
            if interest in self.submitter_xreflist:
                ged_individual = ''.join(
                    [ged_individual, Defs.taginfo(1, Gedcom.DESI, interest)]
                )
        for identifier in identifiers:
            ged_individual = ''.join(
                [ged_individual, self.identifier_structure(identifier)]
            )
        for note in notes:
            ged_individual = ''.join(
                [ged_individual, self.note_structure(note)]
            )
        for source in sources:
            ged_individual = ''.join(
                [ged_individual, self.source_citation(source)]
            )
        for media in multimedia:
            ged_individual = ''.join(
                [ged_individual, self.multimedia_link(media)]
            )
        ged_individual = ''.join([ged_individual, self.creation_date()])
        self.ged_individual = ''.join([self.ged_individual, ged_individual])
        logging.info(Msg.ADDED_RECORD.format(Record.INDIVIDUAL, xref))

    def multimedia_record(
        self,
        files: list[Any],
        resn: str = '',
        identifiers: list[Any] | None = None,
        notes: list[Any] | None = None,
        sources: list[Any] | None = None,
        xref_name: str = '',
    ) -> str:
        if identifiers is None:
            identifiers = []
        if notes is None:
            notes = []
        if sources is None:
            sources = []
        if resn != '' and resn not in Enum.RESN:
            raise ValueError(Msg.NOT_VALID_ENUM.format(resn, EnumName.RESN))
        for file in files:
            if file[1] not in Enum.MEDIA_TYPE:
                raise ValueError(
                    Msg.NOT_VALID_ENUM.format(file[1], EnumName.MEDIA_TYPE)
                )
        if len(file) > 5 and len(file[5]) > 0:
            for translation in file[5]:
                if translation[1] not in Enum.MEDIA_TYPE:
                    raise ValueError(
                        Msg.NOT_VALID_ENUM.format(file[1], EnumName.MEDIA_TYPE)
                    )
        if len(file) > 3 and file[3] != '' and file[3] not in Enum.MEDI:
            raise ValueError(Msg.NOT_VALID_ENUM.format(file[3], EnumName.MEDI))
        xref: str = self.next_counter(
            self.multimedia_xreflist, Gedcom.OBJE, xref_name
        )
        ged_multimedia: str = Defs.taginit(xref, Gedcom.OBJE)
        if resn != '':
            ged_multimedia = ''.join(
                [ged_multimedia, Defs.taginfo(1, Gedcom.RESN, resn)]
            )
        for file in files:
            ged_multimedia = ''.join(
                [
                    ged_multimedia,
                    Defs.taginfo(1, Gedcom.FILE, file[0]),
                    Defs.taginfo(2, Gedcom.FORM, file[1]),
                ]
            )
            if len(file) > 2 and file[2] != '':
                ged_multimedia = ''.join(
                    [ged_multimedia, Defs.taginfo(3, Gedcom.MEDI, file[2])]
                )
            if len(file) > 3 and file[3] != '':
                ged_multimedia = ''.join(
                    [ged_multimedia, Defs.taginfo(4, Gedcom.PHRASE, file[3])]
                )
            if len(file) > 4 and file[4] != '':
                ged_multimedia = ''.join(
                    [ged_multimedia, Defs.taginfo(2, Gedcom.TITL, file[4])]
                )
            if len(file) > 5 and len(file[5]) > 0:
                for translation in file[5]:
                    ged_multimedia = ''.join(
                        [
                            ged_multimedia,
                            Defs.taginfo(2, Gedcom.TRAN, translation[0]),
                            Defs.taginfo(3, Gedcom.FORM, translation[1]),
                        ]
                    )
        for identifier in identifiers:
            ged_multimedia = ''.join(
                [ged_multimedia, self.identifier_structure(identifier)]
            )
        for note in notes:
            ged_multimedia = ''.join(
                [ged_multimedia, self.note_structure(note)]
            )
        for source in sources:
            ged_multimedia = ''.join(
                [ged_multimedia, self.source_citation(source)]
            )
        ged_multimedia = ''.join([ged_multimedia, self.creation_date()])
        self.ged_multimedia = ''.join([self.ged_multimedia, ged_multimedia])
        logging.info(Msg.ADDED_RECORD.format(Record.MULTIMEDIA, xref))
        return xref

    def repository_record(
        self,
        name: str,
        address: str = '',
        city: str = '',
        state: str = '',
        postal: str = '',
        country: str = '',
        phones: list[Any] | None = None,
        emails: list[Any] | None = None,
        faxes: list[Any] | None = None,
        wwws: list[Any] | None = None,
        notes: list[Any] | None = None,
        identifiers: list[Any] | None = None,
        xref_name: str = '',
    ) -> str:
        if phones is None:
            phones = []
        if emails is None:
            emails = []
        if faxes is None:
            faxes = []
        if wwws is None:
            wwws = []
        if identifiers is None:
            identifiers = []
        if notes is None:
            notes = []
        for id in identifiers:
            if id[0] not in Enum.ID:
                raise ValueError(Msg.NOT_VALID_ENUM.format(id[0], EnumName.ID))
        xref: str = self.next_counter(
            self.repository_xreflist, Gedcom.REPO, xref_name
        )
        ged_repository: str = Defs.taginit(xref, Gedcom.REPO)
        ged_repository = ''.join(
            [ged_repository, Defs.taginfo(1, Gedcom.NAME, name)]
        )
        ged_repository = ''.join(
            [
                ged_repository,
                Address(address, city, state, postal, country),
            ]
        )
        ged_repository = ''.join(
            [ged_repository, self.contact(phones, emails, faxes, wwws)]
        )
        for note in notes:
            ged_repository = ''.join(
                [ged_repository, self.note_structure(note)]
            )
        for identifier in identifiers:
            ged_repository = ''.join(
                [ged_repository, self.identifier_structure(identifier)]
            )
        ged_repository = ''.join([self.ged_repository, self.creation_date()])
        logging.info(Msg.ADDED_RECORD.format(Record.REPOSITORY, xref))
        return xref

    def shared_note_record(
        self,
        note: str,
        mime: str = '',
        language: str = '',
        translations: list[Any] | None = None,
        sources: list[Any] | None = None,
        identifiers: list[Any] | None = None,
        xref_name: str = '',
    ) -> str:
        if translations is None:
            translations = []
        if sources is None:
            sources = []
        if identifiers is None:
            identifiers = []
        if mime != '' and mime not in Enum.MEDIA_TYPE:
            raise ValueError(
                Msg.NOT_VALID_ENUM.format(mime, EnumName.MEDIA_TYPE)
            )
        for translation in translations:
            if len(translation) > 1 and translation[1] not in Enum.MEDIA_TYPE:
                raise ValueError(
                    Msg.NOT_VALID_ENUM.format(
                        translation[1], EnumName.MEDIA_TYPE
                    )
                )
        for id in identifiers:
            if id[0] not in Enum.ID:
                raise ValueError(Msg.NOT_VALID_ENUM.format(id[0], EnumName.ID))
        xref: str = self.next_counter(
            self.shared_note_xreflist, Gedcom.SNOTE, xref_name
        )
        ged_shared_note: str = Defs.taginit(xref, Gedcom.SNOTE, note)
        if mime != '' and mime in Enum.MEDIA_TYPE:
            ged_shared_note = ''.join(
                [ged_shared_note, Defs.taginfo(1, Gedcom.MIME, mime)]
            )
        if language != '':
            ged_shared_note = ''.join(
                [ged_shared_note, Defs.taginfo(1, Gedcom.LANG, language)]
            )
        for translation in translations:
            ged_shared_note = ''.join(
                [ged_shared_note, Defs.taginfo(1, Gedcom.TRAN, translation[0])]
            )
            if len(translation) > 1:
                ged_shared_note = ''.join(
                    [
                        ged_shared_note,
                        Defs.taginfo(2, Gedcom.MIME, translation[1]),
                    ]
                )
            if len(translation) > 2:
                ged_shared_note = ''.join(
                    [
                        ged_shared_note,
                        Defs.taginfo(2, Gedcom.LANG, translation[2]),
                    ]
                )
        for source in sources:
            ged_shared_note = ''.join(
                [ged_shared_note, self.source_citation(source)]
            )
        for identifier in identifiers:
            ged_shared_note = ''.join(
                [ged_shared_note, self.identifier_structure(identifier)]
            )
        ged_shared_note = ''.join([ged_shared_note, self.creation_date()])
        self.ged_shared_note = ''.join([self.ged_shared_note, ged_shared_note])
        logging.info(Msg.ADDED_RECORD.format(Record.SHARED_NOTE, xref))
        return xref

    def source_record(
        self,
        events: list[Any] | None = None,
        author: str = '',
        title: str = '',
        abbreviation: str = '',
        publisher: str = '',
        text: str = '',
        mime: str = '',
        language: str = '',
        sources: list[Any] | None = None,
        identifiers: list[Any] | None = None,
        notes: list[Any] | None = None,
        multimedia: list[Any] | None = None,
        xref_name: str = '',
    ) -> str:
        if events is None:
            events = []
        if identifiers is None:
            identifiers = []
        if multimedia is None:
            multimedia = []
        if notes is None:
            notes = []
        if sources is None:
            sources = []
        if mime != '' and mime not in Enum.MEDIA_TYPE:
            raise ValueError(
                Msg.NOT_VALID_ENUM.format(mime, EnumName.MEDIA_TYPE)
            )
        for media in multimedia:
            if media[0] not in self.multimedia_xreflist:
                raise ValueError(
                    Msg.NOT_RECORD.format(media[0], Record.MULTIMEDIA)
                )
        for id in identifiers:
            if id[0] not in Enum.ID:
                raise ValueError(Msg.NOT_VALID_ENUM.format(mime, EnumName.ID))
        xref: str = self.next_counter(
            self.source_xreflist, Gedcom.SOUR, xref_name
        )
        ged_source: str = Defs.taginit(xref, Gedcom.SOUR)
        if len(events) > 0:
            ged_source = ''.join([ged_source, Defs.taginfo(1, Gedcom.DATA)])
            for event in events:
                ged_source = ''.join(
                    [ged_source, Defs.taginfo(2, Gedcom.EVEN, event[0])]
                )
                if len(event) > 1:
                    ged_source = ''.join(
                        [ged_source, Defs.taginfo(3, Gedcom.DATE, event[1])]
                    )
                if len(event) > 2:
                    ged_source = ''.join(
                        [ged_source, Defs.taginfo(4, Gedcom.PHRASE, event[2])]
                    )
                if len(event) > 3:
                    ged_source = ''.join(
                        [ged_source, Defs.taginfo(2, Gedcom.AGNC, event[3])]
                    )
                if len(event) > 4:
                    ged_source = ''.join(
                        [ged_source, self.note_structure(event[4])]
                    )
        if author != '':
            ged_source = ''.join(
                [ged_source, Defs.taginfo(1, Gedcom.AUTH, author)]
            )
        if title != '':
            ged_source = ''.join(
                [ged_source, Defs.taginfo(1, Gedcom.TITL, title)]
            )
        if abbreviation != '':
            ged_source = ''.join(
                [ged_source, Defs.taginfo(1, Gedcom.ABBR, abbreviation)]
            )
        if publisher != '':
            ged_source = ''.join(
                [ged_source, Defs.taginfo(1, Gedcom.PUBL, publisher)]
            )
        if text != '':
            ged_source = ''.join(
                [ged_source, Defs.taginfo(1, Gedcom.TEXT, text)]
            )
        if mime != '' and mime in Enum.MEDIA_TYPE:
            ged_source = ''.join(
                [ged_source, Defs.taginfo(2, Gedcom.MIME, mime)]
            )
        if language != '':
            ged_source = ''.join(
                [ged_source, Defs.taginfo(2, Gedcom.LANG, language)]
            )
        for source in sources:
            ged_source = ''.join(
                [ged_source, self.source_repository_citation(source)]
            )
        for identifier in identifiers:
            ged_source = ''.join(
                [ged_source, self.identifier_structure(identifier)]
            )
        for note in notes:
            ged_source = ''.join([ged_source, self.note_structure(note)])
        for media in multimedia:
            ged_source = ''.join([ged_source, self.multimedia_link(media)])
        ged_source = ''.join([ged_source, self.creation_date()])
        self.ged_source = ''.join([self.ged_source, ged_source])
        logging.info(Msg.ADDED_RECORD.format(Record.SOURCE, xref))
        return xref

    def submitter_record(
        self,
        name: str,
        address: str = '',
        city: str = '',
        state: str = '',
        postal: str = '',
        country: str = '',
        phones: list[str] | None = None,
        emails: list[str] | None = None,
        faxes: list[str] | None = None,
        wwws: list[str] | None = None,
        multimedia: list[Any] | None = None,
        languages: list[str] | None = None,
        identifiers: list[list[str]] | None = None,
        notes: list[Any] | None = None,
        shared_note: str = '',
        xref_name: str = '',
    ) -> str:
        if phones is None:
            phones = []
        if emails is None:
            emails = []
        if faxes is None:
            faxes = []
        if wwws is None:
            wwws = []
        if multimedia is None:
            multimedia = []
        if languages is None:
            languages = []
        if identifiers is None:
            identifiers = []
        if notes is None:
            notes = []
        for id in identifiers:
            if id[0] not in Enum.ID:
                raise ValueError(Msg.NOT_VALID_ENUM.format(id[0], EnumName.ID))
        for media in multimedia:
            if media[0] not in self.multimedia_xreflist:
                raise ValueError(
                    Msg.NOT_RECORD.format(media[0], Record.MULTIMEDIA)
                )
        xref: str = self.next_counter(
            self.submitter_xreflist, Gedcom.SUBM, xref_name
        )
        ged_submitter: str = Defs.taginit(xref, Gedcom.SUBM)
        ged_submitter = ''.join(
            [ged_submitter, Defs.taginfo(1, Gedcom.NAME, name)]
        )
        ged_submitter = ''.join(
            [
                ged_submitter,
                self.address_structure(address, city, state, postal, country),
            ]
        )
        ged_submitter = ''.join(
            [ged_submitter, self.contact(phones, emails, faxes, wwws)]
        )
        for media in multimedia:
            ged_submitter = ''.join(
                [ged_submitter, self.multimedia_link(media)]
            )
        for language in languages:
            ged_submitter = ''.join(
                [ged_submitter, Defs.taginfo(1, Gedcom.LANG, language)]
            )
        for identifier in identifiers:
            ged_submitter = ''.join(
                [ged_submitter, self.identifier_structure(identifier)]
            )
        for note in notes:
            ged_submitter = ''.join([ged_submitter, self.note_structure(note)])
        if shared_note != '':
            ged_submitter = ''.join(
                [ged_submitter, Defs.taginfo(1, Gedcom.SNOTE, shared_note)]
            )
        ged_submitter = ''.join([ged_submitter, self.creation_date()])
        self.ged_submitter = ''.join([self.ged_submitter, ged_submitter])
        logging.info(Msg.ADDED_RECORD.format(Record.SUBMITTER, xref))
        return xref

    ###### GEDCOM Special Records

    def header(
        self,
        schemas: list[Any] | None = None,
        source: str = '',
        vers: str = '',
        name: str = '',
        corp: str = '',
        address: str = '',
        city: str = '',
        state: str = '',
        postal: str = '',
        country: str = '',
        phones: list[str] | None = None,
        emails: list[str] | None = None,
        faxes: list[str] | None = None,
        wwws: list[str] | None = None,
        data: str = '',
        data_date: str = '',
        data_time: str = '',
        data_copr: str = '',
        date: str = '',
        time: str = '',
        dest: str = '',
        submitter: str = '',
        copr: str = '',
        language: str = '',
        place: list[Any] | None = None,
        note: Note | None = None,
        shared_note: str = '',
    ) -> None:
        if submitter != '' and submitter not in self.submitter_xreflist:
            raise ValueError(Msg.NOT_RECORD.format(submitter, Record.SUBMITTER))
        if schemas is None:
            schemas = []
        if phones is None:
            phones = []
        if emails is None:
            emails = []
        if faxes is None:
            faxes = []
        if wwws is None:
            wwws = []
        if place is None:
            place = []
        if note is None:
            note = Note('', '', '', [], [])
        ged_header: str = ''.join(
            [
                Defs.taginfo(0, Gedcom.HEAD),
                Defs.taginfo(1, Gedcom.GEDC),
                Defs.taginfo(2, Gedcom.VERS, GEDSpecial.VERSION),
            ]
        )
        if len(schemas) > 0:
            ged_header = ''.join([ged_header, Defs.taginfo(1, Gedcom.SCHMA)])
            for schema in schemas:
                tag, ref = schema
                ged_header = ''.join(
                    [ged_header, Defs.taginfo(2, Gedcom.TAG, tag, ref)]
                )
        if source != '':
            ged_header = ''.join(
                [ged_header, Defs.taginfo(1, Gedcom.SOUR, source)]
            )
            if vers != '':
                ged_header = ''.join(
                    [ged_header, Defs.taginfo(2, Gedcom.VERS, vers)]
                )
            if name != '':
                ged_header = ''.join(
                    [ged_header, Defs.taginfo(2, Gedcom.NAME, name)]
                )
            if corp != '':
                ged_header = ''.join(
                    [ged_header, Defs.taginfo(2, Gedcom.CORP, corp)]
                )
            ged_header = ''.join(
                [
                    ged_header,
                    Address(address, city, state, postal, country, level=3),
                ]
            )
            ged_header = ''.join(
                [ged_header, self.contact(phones, emails, faxes, wwws, level=3)]
            )
            if data != '':
                ged_header = ''.join(
                    [ged_header, Defs.taginfo(2, Gedcom.DATA, data)]
                )
                if data_date != '':
                    ged_header = ''.join(
                        [ged_header, Defs.taginfo(3, Gedcom.DATE, data_date)]
                    )
                if data_time != '':
                    ged_header = ''.join(
                        [ged_header, Defs.taginfo(4, Gedcom.TIME, data_time)]
                    )
                if data_copr != '':
                    ged_header = ''.join(
                        [ged_header, Defs.taginfo(2, Gedcom.COPR, data_copr)]
                    )
        if dest != '':
            ged_header = ''.join(
                [ged_header, Defs.taginfo(1, Gedcom.DEST, dest)]
            )
        if date != '':
            ged_header = ''.join(
                [ged_header, Defs.taginfo(1, Gedcom.DATE, date)]
            )
        if time != '':
            ged_header = ''.join(
                [ged_header, Defs.taginfo(2, Gedcom.TIME, time)]
            )
        if submitter != '':
            ged_header = ''.join(
                [ged_header, Defs.taginfo(1, Gedcom.SUBM, submitter)]
            )
        if copr != '':
            ged_header = ''.join(
                [ged_header, Defs.taginfo(1, Gedcom.COPR, copr)]
            )
        if language != '':
            ged_header = ''.join(
                [ged_header, Defs.taginfo(1, Gedcom.LANG, language)]
            )
        if len(place) > 0:
            ged_header = ''.join(
                [
                    ged_header,
                    Defs.taginfo(1, Gedcom.PLAC, place[0]),
                    Defs.taginfo(2, Gedcom.FORM, place[1]),
                ]
            )
        if shared_note != '':
            ged_header = ''.join(
                [ged_header, Defs.taginfo(1, Gedcom.SNOTE, shared_note)]
            )
        ged_header = ''.join([ged_header, self.note_structure(note)])
        self.ged_header = ged_header
