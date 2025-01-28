# calendars
"""Define NamedTuples to store information about a specific calendar system."""

import uuid
from textwrap import indent
from typing import Any, NamedTuple

import numpy as np


class CalendarMessage:
    DAY_RANGE: str = 'The day "{0}" is either less than 1 or greater than the number of days in month {1}: "{2}".'
    END: str = 'The date "{0}" goes beyond the end of the calendar "{1}".'
    BEGIN: str = 'The date "{0}" comes before the start of the calendar "{1}".'
    MONTH_RANGE: str = 'The month "{0}" is either less than 1 or greater than the number of months "{1}".'
    ZERO: str = 'The year is 0, but there is no 0 year in the calendar.'


class Constants:
    BRACKETS: str = '[]'
    COMMA: str = ','
    EMPTY: str = ''
    EOL: str = '\n'
    FLOAT_ZERO: float = 0.0
    HYPHEN: str = '-'
    ICS_BEGIN_CALENDAR: str = """BEGIN:VCALENDAR
PRODID:-//calendars//Year//UND
CALSCALE:GREGORIAN
VERSION:2.0
"""
    ICS_BEGIN_DAY: str = 'BEGIN:VEVENT'
    ICS_DAY_START: str = 'DTSTART;VALUE=DATE:'
    ICS_DAY_END: str = 'DTEND;VALUE=DATE:'
    ICS_DESCRIPTION: str = 'DESCRIPTION:'
    ICS_END_CALENDAR: str = 'END:VCALENDAR'
    ICS_END_DAY: str = 'END:VEVENT'
    ICS_SEPARATOR: str = ':'
    ICS_SUMMARY: str = 'SUMMARY:'
    ICS_UID: str = 'UID:'
    INDENT: str = '    '
    LEFT_BRACKET: str = '['
    NAT: str = 'NaT'
    RIGHT_BRACKET: str = ']'
    ZERO: int = 0


class YearDefinition(NamedTuple):
    """A description of a year in the calendar."""

    years_in_cycle: np.timedelta64
    months_in_cycle: np.timedelta64
    days_in_cycle: np.timedelta64
    years_in_subcycle: np.timedelta64 = np.timedelta64(0, 'Y')
    months_in_subcycle: np.timedelta64 = np.timedelta64(0, 'M')
    days_in_subcycle: np.timedelta64 = np.timedelta64(0, 'D')


class MonthDefinition(NamedTuple):
    """A description of a month in the calendar."""

    number: int
    name: str
    days: int
    abbreviation: str = Constants.EMPTY
    symbol: str = Constants.EMPTY


class WeekDefinition(NamedTuple):
    """A description of a week in the calendar."""

    number: int
    name: str
    symbol: str = Constants.EMPTY


class WeekDayDefinition(NamedTuple):
    """A description of the days of a week."""

    number: int
    name: str
    abbreviation: str = Constants.EMPTY
    symbol: str = Constants.EMPTY


class DayDefinition(NamedTuple):
    """A description of a day in the calendar."""

    number: int
    name: str
    month: int = 0
    symbol: str = Constants.EMPTY
    summary: str = Constants.EMPTY
    description: str = Constants.EMPTY


class HolidayDefinition(NamedTuple):
    """A description of a day in the calendar."""

    number: int
    name: str


class LocationDefinition(NamedTuple):
    """A description of the location where the calendar was used."""

    latitude: float
    longitude: float
    description: str = Constants.EMPTY


class CalendarDefinition(NamedTuple):
    """Frameword for definitions for specific calendars with methods to work with those calendars.

    Args:
        name: The name of the calendar provding a way to display it as a string.
        months: A list of abbreviations for the names of the months. The 0 month is ''.
        days_in_monts: A lit of the number of days for each month.  The 0 day is 0.
        epoch: If the calendar has and epoch splitting the years into positive and negative, this is the name
            of the negative years.
        zero: If the calendar has a zero year (unlike the Gregorian calendar) then this is True.
            Otherwise, it is false.
        negative: Even if the calendar has a beginning, it may not permit negative years.  This flag
            signal that negative dates before the beginning are not permitted.

    Reference:

    """

    name: str
    years: YearDefinition
    months: list[MonthDefinition]
    weeks: list[WeekDefinition]
    weekdays: list[WeekDayDefinition]
    days: list[DayDefinition]
    holidays: list[HolidayDefinition]
    epoch_year: np.datetime64 = np.datetime64(Constants.NAT)
    epoch_month: np.datetime64 = np.datetime64(Constants.NAT)
    epoch_day: np.datetime64 = np.datetime64(Constants.NAT)
    epoch_name: str = Constants.EMPTY
    zero: bool = True
    negative: bool = True
    end: np.datetime64 = np.datetime64(Constants.NAT)
    location: LocationDefinition = LocationDefinition(
        Constants.FLOAT_ZERO, Constants.FLOAT_ZERO, Constants.EMPTY
    )
    description: str = Constants.EMPTY

    def validate(
        self, year: int, month: int, day: int, iso: str = Constants.EMPTY
    ) -> bool:
        date: tuple[int, int, int] = (year, month, day)
        if iso != Constants.EMPTY:
            year, month, day = self.from_iso(iso)
        if year == Constants.ZERO and not self.zero:
            raise ValueError(CalendarMessage.ZERO)
        if month < Constants.ZERO or month > len(self.months) - 1:
            raise ValueError(
                CalendarMessage.MONTH_RANGE.format(
                    str(month), str(len(self.months) - 1)
                )
            )
        if day < 0 or day > self.months[month].days:
            raise ValueError(
                CalendarMessage.DAY_RANGE.format(
                    str(day), str(month), str(self.months[month].days)
                )
            )
        if (
            self.end != (Constants.ZERO, Constants.ZERO, Constants.ZERO)
            and date > self.end
        ):
            raise ValueError(CalendarMessage.END.format(date, self.end))
        if (
            self.epoch_year != np.datetime64(Constants.NAT)
            and date < self.epoch_year
            and not self.negative
        ):
            raise ValueError(CalendarMessage.BEGIN.format(date, self.epoch_year))
        return True

    def days_in_month(self, month: int) -> int:
        """Return the number of days in a month."""
        return self.months[month].days

    def days_in_year(self, days: int) -> int:
        return days

    def from_iso(self, iso: str) -> tuple[int, int, int]:
        """Convert a Gregorian ISO 8601 date to this calendar's year, month and day."""
        year_month_day: list[str] = iso.split(Constants.HYPHEN)
        year: int = int(year_month_day[0])
        month: int = int(year_month_day[1])
        day: int = int(year_month_day[2])
        return year, month, day

    def format(
        self,
        year: int,
        month: int = Constants.ZERO,
        day: int = Constants.ZERO,
        iso: str = Constants.EMPTY,
    ) -> str:
        if iso != Constants.EMPTY:
            year, month, day = self.from_iso(iso)
        return f'{year!s}-{self.months[month]}-{day!s}'

    def ics(self, start: str, end: str) -> str:
        """Construct an ICS list of events from the days defined in the calendar.

        The days are represented as day-long events.  This allows one to
        see the calendar as aligned with the more common
        universal calendar of the program.

        Args:
            start: The first day for the ICS list of events.
            end: The last day for the ICS list of events.
        
        Reference:
            [RFC 5545](https://datatracker.ietf.org/doc/html/rfc5545)
            [icalendar](https://icalendar.readthedocs.io/en/latest/)
        """
        lines: str = Constants.ICS_BEGIN_CALENDAR
        index: int = 1
        day: str = start
        end_day: str = end
        for day_item in self.days:
            summary: str = self.months[self.days[day_item.number].month].name
            day_summary: str = self.days[index].summary
            if day_summary != Constants.EMPTY:
                summary = ''.join(
                    [summary, Constants.ICS_SEPARATOR, day_summary]
                )
            lines = ''.join(
                [
                    lines,
                    Constants.ICS_BEGIN_DAY,
                    Constants.EOL,
                    Constants.ICS_UID,
                    str(uuid.uuid4()),
                    Constants.EOL,
                    Constants.ICS_DAY_START,
                    day,
                    Constants.EOL,
                    Constants.ICS_DAY_END,
                    end_day,
                    Constants.EOL,
                    Constants.ICS_SUMMARY,
                    summary,
                    Constants.EOL,
                    Constants.ICS_DESCRIPTION,
                    self.days[index].description,
                    Constants.EOL,
                    Constants.ICS_END_DAY,
                    Constants.EOL,
                ]
            )
            index += 1
        return ''.join([lines, Constants.ICS_END_CALENDAR])

    def isleap(self, year: int) -> bool:  
        """Test if a year is a leap year with the default test for the Gregorian calendar."""
        return year % 4 == 0 and year % 400 != 0

    

    def describe(
        self,
        year: int = Constants.ZERO,
        month: int = Constants.ZERO,
        day: int = Constants.ZERO,
        iso: str = Constants.EMPTY,
    ) -> str:
        if iso != Constants.EMPTY:
            year, month, day = self.from_iso(iso)
        lines: str = f'Date: {self.months[month].abbreviation} {day!s}, {year!s}{Constants.EOL}'
        lines = ''.join(
            [lines, f'Calendar: {self.name.title()}{Constants.EOL}']
        )
        lines = ''.join(
            [lines, f'Is leap year? {self.isleap(year)},{Constants.EOL}']
        )
        if day > Constants.ZERO:
            pass
        if month > Constants.ZERO:
            pass
        return lines

    def codelist(self, items: list[Any], tabs: int = 2) -> str:
        if len(items) == Constants.ZERO:
            return Constants.BRACKETS
        lines: str = ''.join([Constants.LEFT_BRACKET, Constants.EOL])
        for item in items:
            lines = ''.join(
                [
                    lines,
                    Constants.INDENT * tabs,
                    repr(item),
                    Constants.COMMA,
                    Constants.EOL,
                ]
            )
        return ''.join(
            [
                lines[:-1],
                Constants.EOL,
                Constants.INDENT * (tabs - 1),
                Constants.RIGHT_BRACKET,
            ]
        )

    def code(self, tabs: int = Constants.ZERO) -> None:
        """Generate the code to define the calendar so it can be modified.

        This method is based on the __repr__ method for NamedTuples.  One can
        get similar, but unformatted results by running `repr` on an already
        existing CalendarDefinition, say CalendarsGregorian.GREGORIAN.  If one
        ran `repr(CalendarsGregorian.GREGORIAN) one would get a string that would
        get a string one could run and get another NamedTuple like it.

        What this method adds is formatting for the repr result and the imports
        that would be needed for the repr to run.

        Examples:
            There is an empty Gregorian CalendarsGregorian for testing and starting
            a new calendar system from scratch called `CalendarsGregorian.GREGORIAN_EMPTY`.
            One could get the code for that calendar by using `repr` as in the first
            example.
            >>> import calendars.gregorian_calendars 
        
        """

        print(indent(  # noqa: T201
            f"""
import numpy as np
from calendars.calendars import (
    CalendarDefinition,
    DayDefinition,
    HolidayDefinition,
    LocationDefinition,
    MonthDefinition,
    WeekDefinition,
    WeekDayDefinition,
    YearDefinition, 
)  
new_calendar = CalendarDefinition(
    name = {self.name!r},
    years = YearDefinition(
        years_in_cycle = {self.years.years_in_cycle!r},           # Gregorian example: Although years divisible by 4 are leap years, years divisible by 400 are not.
        months_in_cycle = {self.years.months_in_cycle!r},         # 12 months/year * 400 years/cycle = 4800 years/cycle.
        days_in_cycle = {self.years.days_in_cycle!r},         # 365 days/year * 400 years/cycle + 100 leap years - 1 year divisible by 400 per cycle.
        years_in_subcycle = {self.years.years_in_subcycle!r},          # The subcycle has only 4 years.
        months_in_subcycle = {self.years.months_in_subcycle!r},        # 12 months/year * 4 years/subcycle = 48 months/cycle
        days_in_subcycle = {self.years.days_in_subcycle!r},        # 365 days/year * 4 years/subcycle + 1 leap year/cycle
    ),
    months = {self.codelist(self.months)},
    weeks = {self.codelist(self.weeks)},
    weekdays = {self.codelist(self.weekdays)},
    days = {self.codelist(self.days)},
    holidays = {self.codelist(self.holidays)},
    epoch_year = {self.epoch_year!r},
    epoch_month = {self.epoch_month!r},
    epoch_day = {self.epoch_day!r},
    epoch_name = {self.epoch_name!r},
    zero = {self.zero!r},
    negative = {self.negative!r},
    end = {self.end!r},
    location = {self.location!r},
    description = {self.description!r},
)""",
            Constants.INDENT * tabs,
        ))
