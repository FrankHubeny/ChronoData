# Licensed under a 3-clause BSD style license - see LICENSE.md
"""NamedTuples to build a chronology based on the GEDCOM standard."""

from typing import Any, NamedTuple

from chronodata.constants import Cal, Value
from chronodata.enums import (
    Adop,
    ApproxDate,
    EvenAttr,
    FamAttr,
    FamcStat,
    FamEven,
    GreaterLessThan,
    Id,
    IndiAttr,
    IndiEven,
    Medi,
    MediaType,
    NameType,
    Pedi,
    PersonalNamePiece,
    RangeDate,
    Records,
    RestrictDate,
    Role,
    Sex,
    Stat,
)
from chronodata.g7 import Gedcom
from chronodata.methods import Defs


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
        check: bool = (
            Defs.verify_type(self.address, str)
            and Defs.verify_type(self.city, str)
            and Defs.verify_type(self.state, str)
            and Defs.verify_type(self.postal, str)
            and Defs.verify_type(self.country, str)
        )
        return check

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


class Age(NamedTuple):
    """Implement the Age data type in the GEDCOM specification.

    Parameters
    ----------
    - greater_less_than
        The default is '', which means that the age is exact
        to the day.  The option `>` means that the actual age
        is greater than the one provided.  The option `<` means
        that the actual age is less than the one provided.
    - years
        The number of whole years in the age. The specification
        requires this to be rounded down.  Here an error is thrown
        if an integer is not used. One can add information in the
        phrase parameter to clarify the year.
    - months
        The number of months in addition to the years. The specification
        requires this to be rounded down.  Here an error is thrown
        if an integer is not used. One can add information in the
        phrase parameter to clarify the year.
    - weeks
        The number of weeks in addition to the years and months.
        The specification
        requires this to be rounded down.  Here an error is thrown
        if an integer is not used. One can add information in the
        phrase parameter to clarify the year.
    - days
        The number of days in addition to any years, months, or weeks provided.
        The specification requires this to be rounded down.  Here an error is thrown
        if an integer is not used. One can add information in the
        phrase parameter to clarify the year.

    The default values for these parameters is 0 for the integers and '' for the
    strings.

    Exceptions
    ----------
    - If greater_less_than is not one of {'', '<', '>'} a ValueError will be issued.
    - If any value (except `phrase`) is not an integer, a ValueError will be issued.
    - If any value (except `phrase`) is less than 0, a ValueError will be issued.

    Examples
    --------
    >>> Age('>', 10).ged(1)
    >>> 1 AGE > 10y\n
    >>> Age(10, 2, 1, 2).ged(2)
    >>> 2 AGE 10y 2m 1w 2d\n

    Reference
    ---------
    [GEDCOM Specification](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#age)
    """

    greater_less_than: str = ''
    years: int = 0
    months: int = 0
    weeks: int = 0
    days: int = 0
    phrase: str = ''

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_enum(self.greater_less_than, GreaterLessThan)
            and Defs.verify_type(self.years, int)
            and Defs.verify_type(self.months, int)
            and Defs.verify_type(self.weeks, int)
            and Defs.verify_type(self.days, int)
            and Defs.verify_type(self.phrase, str)
            and Defs.verify_not_negative(self.years)
            and Defs.verify_not_negative(self.months)
            and Defs.verify_not_negative(self.weeks)
            and Defs.verify_not_negative(self.days)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format the GEDCOM Age data type."""

        line: str = ''
        info: str = self.greater_less_than
        if self.validate():
            if self.years > 0:
                info = ''.join([info, f' {self.years!s}y'])
            if self.months > 0:
                info = ''.join([info, f' {self.months!s}m'])
            if self.weeks > 0:
                info = ''.join([info, f' {self.weeks!s}w'])
            if self.days > 0:
                info = ''.join([info, f' {self.days!s}d'])
            line = Defs.taginfo(
                level,
                Gedcom.AGE,
                info.replace('  ', ' ').replace('  ', ' ').strip(),
            )
            if self.phrase != '':
                line = ''.join(
                    [line, Defs.taginfo(level + 1, Gedcom.PHRASE, self.phrase)]
                )
        return line


class PersonalName(NamedTuple):
    tag: str
    text: str

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.tag, str)
            and Defs.verify_type(self.text, str)
            and Defs.verify_enum(self.tag, PersonalNamePiece)
        )
        return check

    def ged(self, level: int = 1) -> str:
        personal_name: str = ''
        if self.validate():
            personal_name = Defs.taginfo(level, self.tag, self.text.strip())
        return personal_name


class NameTranslation(NamedTuple):
    text: str
    language: str = ''
    piece: Any = None

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.text, str)
            and Defs.verify_type(self.language, str)
            and Defs.verify_type(self.piece, PersonalName)
        )
        return check

    # def ged(self, level: int = 1) -> str:
    #     name_translation: str = ''
    #     if self.validate():
    #         name_translation = f'{level} {Gedcom.TRAN} {self.text}\n{level+1} {Gedcom.LANG} {self.lang}\n'
    #     return name_translation


class NoteTranslation(NamedTuple):
    text: str
    mime: str = ''
    language: str = ''

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.text, str)
            and Defs.verify_type(self.mime, str)
            and Defs.verify_type(self.language, str)
        )
        return check


class NoteCitation(NamedTuple):
    text: str
    mime: str = ''
    language: str = ''
    translations: Any = None

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.text, str)
            and Defs.verify_type(self.mime, str)
            and Defs.verify_type(self.language, str)
            and Defs.verify_tuple_type(self.translations, NoteTranslation)
        )
        return check


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
        check: bool = (
            Defs.verify_type(self.xref, str)
            and Defs.verify_type(self.page, str)
            and Defs.verify_type(self.datetime, str)
            and Defs.verify_type(self.text, str)
            and Defs.verify_type(self.mime, str)
            and Defs.verify_type(self.language, str)
            and Defs.verify_type(self.event, str)
            and Defs.verify_type(self.phrase, str)
            and Defs.verify_type(self.role, str)
            and Defs.verify_type(self.role_phrase, str)
            and Defs.verify_type(self.quality, str)
            and Defs.verify_type(self.multimedia, str)
            and Defs.verify_tuple_type(self.notes, NoteCitation)
        )
        return check


class Note(NamedTuple):
    text: str
    mime: str = ''
    language: str = ''
    translation: Any = None
    citations: Any = None

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.text, str)
            and Defs.verify_type(self.mime, str)
            and Defs.verify_type(self.language, str)
            and Defs.verify_tuple_type(self.translation, NoteTranslation)
            and Defs.verify_tuple_type(self.citations, Citation)
        )
        return check


class Association(NamedTuple):
    # xref: str
    role: str
    association_phrase: str = ''
    role_phrase: str = ''
    notes: Any = None
    citations: Any = None

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.role, str)
            and Defs.verify_type(self.association_phrase, str)
            and Defs.verify_type(self.role_phrase, str)
            and Defs.verify_tuple_type(self.notes, Note)
            and Defs.verify_tuple_type(self.citations, Citation)
            and Defs.verify_enum(self.role, Role)
        )
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
        check: bool = (
            Defs.verify_type(self.crop, str)
            and Defs.verify_type(self.top, int)
            and Defs.verify_type(self.left, int)
            and Defs.verify_type(self.height, int)
            and Defs.verify_type(self.width, int)
            and Defs.verify_type(self.title, str)
        )
        return check


class Exid(NamedTuple):
    exid: str
    exid_type: str

    def validate(self) -> bool:
        check: bool = Defs.verify_type(self.exid, str) and Defs.verify_type(
            self.exid_type, str
        )
        return check

    def ged(self, level: int = 1) -> str:
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
        check: bool = Defs.verify_type(self.text, str) and Defs.verify_type(
            self.language, str
        )
        return check


class Map(NamedTuple):
    latitude: float
    longitude: float

    def validate(self) -> bool:
        check: bool = Defs.verify_type(
            self.latitude, float
        ) and Defs.verify_type(self.longitude, float)
        return check


class Place(NamedTuple):
    text: str
    form: str = ''
    language: str = ''
    translations: Any = None
    maps: Any = None
    exids: Any = None
    notes: Any = None

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.text, str)
            and Defs.verify_type(self.form, str)
            and Defs.verify_tuple_type(self.translations, PlaceTranslation)
            and Defs.verify_tuple_type(self.maps, Map)
            and Defs.verify_tuple_type(self.exids, Exid)
            and Defs.verify_tuple_type(self.notes, Note)
        )
        return check


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
        check: bool = (
            Defs.verify_type(self.year, int)
            and Defs.verify_type(self.month, int)
            and Defs.verify_type(self.day, int)
            and Defs.verify_type(self.week, int)
            and Defs.verify_range(self.week, 0, 52)
            and Defs.verify_range(self.month, 0, 12)
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
        check: bool = (
            Defs.verify_type(self.hour, int)
            and Defs.verify_type(self.minute, int)
            and Defs.verify_type(self.second, int | float)
            and Defs.verify_type(self.UTC, bool)
            and Defs.verify_range(self.hour, 0, 23)
            and Defs.verify_range(self.minute, 0, 59)
            and Defs.verify_range(self.second, 0, 59.999999999999)
        )
        return check

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

    date: Date = Date(0, 0, 0)
    time: Time = Time(0, 0, 0)
    phrase: str = ''

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.phrase, str)
            and self.date.validate()
            and self.time.validate()
        )
        return check

    def ged(self, level: int = 1) -> str:
        lines: str = self.date.ged(level)
        if self.validate():
            if self.time != Time(0, 0, 0):
                lines = ''.join([lines, self.time.ged(level + 1)])
            if self.phrase != '':
                lines = ''.join(
                    [lines, Defs.taginfo(level + 1, Gedcom.PHRASE, self.phrase)]
                )
        return lines


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

    date: Date = Date(0, 0, 0)
    time: Time = Time(0, 0, 0)
    phrase: str = ''

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.phrase, str)
            and self.date.validate()
            and self.time.validate()
        )
        return check

    def ged(self, level: int = 1) -> str:
        lines: str = ''
        if self.validate():
            lines = self.date.ged(level)
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
        check: bool = (
            Defs.verify_type(self.status, str)
            and self.date.validate() and self.time.validate()
        )
        return check

    def ged(self, level: int = 1) -> str:
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
        check: bool = (
            Defs.verify_type(self.husband_age, int)
            and Defs.verify_type(self.wife_age, int)
            and Defs.verify_type(self.husband_phrase, str)
            and Defs.verify_type(self.wife_phrase, str)
            and Defs.verify_type(self.event_detail, EventDetail)
        )
        return check

    def ged(self, level: int = 1) -> str:
        if self.validate():
            pass
        return ''


class FamilyEventDetail(NamedTuple):
    husband_wife_ages: HusbandWife

    def validate(self) -> bool:
        check: bool = Defs.verify_type(self.husband_wife_ages, HusbandWife)
        return check


class FamilyAttribute(NamedTuple):
    tag: str
    attribute_type: str = ''
    family_event_detail: FamilyEventDetail | None = None

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.tag, str)
            and Defs.verify_type(self.attribute_type, str)
            and Defs.verify_type(self.family_event_detail, FamilyEventDetail | None)
        )
        return check


class FamilyEvent(NamedTuple):
    event: str = ''
    event_type: str = ''
    event_detail: FamilyEventDetail | None = None

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.event, str)
            and Defs.verify_type(self.event_type, str)
            and Defs.verify_type(self.event_detail, FamilyEventDetail | None)
        )
        return check


class Husband(NamedTuple):
    xref: str
    phrase: str = ''

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.xref, str)
            and Defs.verify_type(self.phrase, str)
        )
        return check


class Wife(NamedTuple):
    xref: str
    phrase: str = ''

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.xref, str)
            and Defs.verify_type(self.phrase, str)
        )
        return check


class Child(NamedTuple):
    xref: str
    phrase: str = ''

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.xref, str)
            and Defs.verify_type(self.phrase, str)
        )
        return check


class LDSOrdinanceDetail(NamedTuple):
    date_value: DateValue | None = None
    temp: str = ''
    place: Place | None = None
    status: DateTimeStatus | None = None
    notes: Any = None
    sources: Any = None

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.date_value, DateValue | None)
            and Defs.verify_type(self.temp, str)
            and Defs.verify_type(self.place, Place | None)
            and Defs.verify_type(self.status, DateTimeStatus | None)
            and Defs.verify_tuple_type(self.notes, Note)
            and Defs.verify_tuple_type(self.sources, Citation)
        )
        return check


class LDSSpouseSealing(NamedTuple):
    tag: str = Gedcom.SLGS
    detail: LDSOrdinanceDetail | None = None

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.tag, str)
            and Defs.verify_type(self.detail, LDSOrdinanceDetail | None)
        )
        return check


class LDSIndividualOrdinances(NamedTuple):
    tag: str
    ordinance_detail: LDSOrdinanceDetail | None = None
    family_xref: str = ''

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.tag, str)
            and Defs.verify_type(self.ordinance_detail, LDSOrdinanceDetail | None)
            and Defs.verify_type(self.family_xref, str)
        )
        return check


class Identifier(NamedTuple):
    tag: str
    tag_type: str = ''

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.tag, str)
            and Defs.verify_type(self.tag_type, str)
        )
        return check


class IndividualEventDetail(NamedTuple):
    event_detail: EventDetail
    age: str = ''
    phrase: str = ''

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.event_detail, EventDetail)
            and Defs.verify_type(self.age, str)
            and Defs.verify_type(self.phrase, str)
        )
        return check


class IndividualAttribute(NamedTuple):
    tag: str
    tag_type: str = ''
    event_detail: IndividualEventDetail | None = None

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.tag, str)
            and Defs.verify_type(self.tag_type, str)
            and Defs.verify_type(self.event_detail, IndividualEventDetail | None)
        )
        return check


class IndividualEvent(NamedTuple):
    tag: str
    tag_type: str = ''
    event_detail: IndividualEventDetail | None = None
    family_child: str = ''
    adoption: str = ''
    phrase: str = ''

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.tag, str)
            and Defs.verify_type(self.tag_type, str)
            and Defs.verify_type(self.event_detail, IndividualEventDetail | None)
            and Defs.verify_type(self.family_child, str)
            and Defs.verify_type(self.adoption, str)
            and Defs.verify_type(self.phrase, str)
        )
        return check


class Alias(NamedTuple):
    xref: str
    phrase: str = ''

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.xref, str)
            and Defs.verify_type(self.phrase, str)
        )
        return check


class FamilyChild(NamedTuple):
    family_xref: str
    pedigree: str = ''
    pedigree_phrase: str = ''
    status: str = ''
    status_phrase: str = ''
    notes: Any = None

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.family_xref, str)
            and Defs.verify_type(self.pedigree, str)
            and Defs.verify_type(self.pedigree_phrase, str)
            and Defs.verify_type(self.status, str)
            and Defs.verify_type(self.status_phrase, str)
            and Defs.verify_tuple_type(self.notes, Note)
        )
        return check


class FamilySpouse(NamedTuple):
    family_xref: str = ''
    notes: Any = None

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.family_xref, str)
            and Defs.verify_tuple_type(self.notes, Note)
        )
        return check


class FileTranslations(NamedTuple):
    path: str
    media_type: str = ''

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.path, str)
            and Defs.verify_type(self.media_type, str)
        )
        return check


class Text(NamedTuple):
    text: str
    mime: str = ''
    language: str = ''

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.text, str)
            and Defs.verify_type(self.mime, str)
            and Defs.verify_type(self.language, str)
        )
        return check


class File(NamedTuple):
    path: str
    media_type: str = ''
    media: str = ''
    phrase: str = ''
    title: str = ''
    file_translations: Any = None

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.path, str)
            and Defs.verify_type(self.media_type, str)
            and Defs.verify_type(self.media, str)
            and Defs.verify_type(self.phrase, str)
            and Defs.verify_type(self.title, str)
            and Defs.verify_tuple_type(self.file_translations, FileTranslations)
        )
        return check


class SourceEvent(NamedTuple):
    event: str = ''
    date_period: str = ''
    phrase: str = ''
    place: Place | None = None
    agency: str = ''
    notes: Any = None

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.event, str)
            and Defs.verify_type(self.date_period, str)
            and Defs.verify_type(self.phrase, str)
            and Defs.verify_type(self.place, str)
            and Defs.verify_type(self.agency, str)
            and Defs.verify_tuple_type(self.notes, Note)
        )
        return check


class NonEvent(NamedTuple):
    no: str = ''
    date: Date | None = None
    phrase: str = ''
    notes: Any = None
    sources: Any = None

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.no, str)
            and Defs.verify_type(self.date, Date | None)
            and Defs.verify_type(self.phrase, str)
            and Defs.verify_tuple_type(self.notes, Note)
            and Defs.verify_tuple_type(self.sources, SourceEvent)
        )
        return check


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
        check: bool = (
            Defs.verify_type(self.xref, str)
            and Defs.verify_type(self.resn, str)
            and Defs.verify_tuple_type(self.attributes, FamilyAttribute)
            and Defs.verify_tuple_type(self.events, FamilyEvent)
            and Defs.verify_type(self.husband, Husband | None)
            and Defs.verify_type(self.wife, Wife | None)
            and Defs.verify_type(self.children, tuple | None)
            and Defs.verify_tuple_type(self.associations, Association)
            and Defs.verify_tuple_type(self.submitters, str)
            and Defs.verify_tuple_type(self.lds_spouse_sealings, LDSSpouseSealing)
            and Defs.verify_tuple_type(self.identifiers, Identifier)
            and Defs.verify_tuple_type(self.notes, Note)
            and Defs.verify_tuple_type(self.citations, Citation)
            and Defs.verify_tuple_type(self.multimedia_links, MultimediaLink)
        )
        return check


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
        check: bool = (
            Defs.verify_type(self.name, str)
            and Defs.verify_type(self.address, Address | None)
            and Defs.verify_tuple_type(self.emails, str)
            and Defs.verify_tuple_type(self.faxes, str)
            and Defs.verify_tuple_type(self.wwws, str)
            and Defs.verify_tuple_type(self.notes, Note)
            and Defs.verify_tuple_type(self.identifiers, Identifier)
        )
        return check


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
        check: bool = (
            Defs.verify_type(self.author, str)
            and Defs.verify_type(self.title, str)
            and Defs.verify_type(self.abbreviation, str)
            and Defs.verify_type(self.published, str)
            and Defs.verify_tuple_type(self.events, SourceEvent)
            and Defs.verify_tuple_type(self.text, Text)
            and Defs.verify_tuple_type(self.repositories, Repository)
            and Defs.verify_tuple_type(self.identifiers, Identifier)
            and Defs.verify_tuple_type(self.notes, Note)
            and Defs.verify_tuple_type(self.multimedia_links, MultimediaLink)
        )
        return check


class Individual(NamedTuple):
    xref: str
    personal_names: Any = None
    sex: Sex = Sex.U
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
        check: bool = (
            Defs.verify_type(self.xref, str)
            and Defs.verify_tuple_type(self.personal_names, PersonalName)
            and Defs.verify_type(self.sex, str)
            and Defs.verify_tuple_type(self.attributes, IndividualAttribute)
            and Defs.verify_tuple_type(self.events, IndividualEvent)
            and Defs.verify_tuple_type(
                self.lds_individual_ordinances, LDSIndividualOrdinances
            )
            and Defs.verify_tuple_type(self.families_child, FamilyChild)
            and Defs.verify_tuple_type(self.submitters, str)
            and Defs.verify_tuple_type(self.associations, Association)
            and Defs.verify_tuple_type(self.aliases, Alias)
            and Defs.verify_tuple_type(self.ancestor_interest, str)
            and Defs.verify_tuple_type(self.descendent_interest, str)
            and Defs.verify_tuple_type(self.identifiers, Identifier)
            and Defs.verify_tuple_type(self.notes, Note)
            and Defs.verify_tuple_type(self.sources, Source)
            and Defs.verify_tuple_type(self.multimedia_links, MultimediaLink)
        )
        return check


class Multimedia(NamedTuple):
    files: Any = None
    identifiers: Any = None
    notes: Any = None
    sources: Any = None

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_tuple_type(self.files, File)
            and Defs.verify_tuple_type(self.identifiers, Identifier)
            and Defs.verify_tuple_type(self.notes, Note)
            and Defs.verify_tuple_type(self.sources, Source)
        )
        return check


class SharedNote(NamedTuple):
    text: str = ''
    mime: str = ''
    language: str = ''
    translations: Any = None
    sources: Any = None
    identifiers: Any = None

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.text, str)
            and Defs.verify_type(self.mime, str)
            and Defs.verify_type(self.language, str)
            and Defs.verify_tuple_type(self.translations, NoteTranslation)
            and Defs.verify_tuple_type(self.sources, Source)
            and Defs.verify_tuple_type(self.identifiers, Identifier)
        )
        return check


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
        check: bool = (
            Defs.verify_type(self.name, str)
            and Defs.verify_type(self.address, Address | None)
            and Defs.verify_tuple_type(self.phones, str)
            and Defs.verify_tuple_type(self.emails, str)
            and Defs.verify_tuple_type(self.faxes, str)
            and Defs.verify_tuple_type(self.wwws, str)
            and Defs.verify_tuple_type(self.multimedia_links, MultimediaLink)
            and Defs.verify_tuple_type(self.languages, str)
            and Defs.verify_tuple_type(self.identifiers, Identifier)
            and Defs.verify_tuple_type(self.notes, Note)
        )
        return check
