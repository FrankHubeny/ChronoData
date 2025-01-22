# calendars

from textwrap import indent
from typing import Any, NamedTuple

import numpy as np


class CalendarMessage:
    DAY_RANGE: str = 'The day "{0}" is either less than 1 or greater than the number of days in month {1}: "{2}".'
    END: str = 'The date "{0}" goes beyond the end of the calendar "{1}".'
    BEGIN: str = 'The date "{0}" comes before the start of the calendar "{1}".'
    MONTH_RANGE: str = 'The month "{0}" is either less than 1 or greater than the number of months "{1}".'
    ZERO: str = 'The year is 0, but there is no 0 year in the calendar.'


class YearDefinition(NamedTuple):
    """A description of a year in the calendar."""

    number: int
    name: str
    symbol: str


class MonthDefinition(NamedTuple):
    """A description of a month in the calendar."""

    number: int
    name: str
    days: int
    abbreviation: str = ''
    symbol: str = ''


class WeekDefinition(NamedTuple):
    """A description of a week in the calendar."""

    number: int
    name: str
    symbol: str = ''


class WeekDayDefinition(NamedTuple):
    """A description of the days of a week."""

    number: int
    name: str
    symbol: str = ''


class DayDefinition(NamedTuple):
    """A description of a day in the calendar."""

    number: int
    name: str


class HolidayDefinition(NamedTuple):
    """A description of a day in the calendar."""

    number: int
    name: str


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
    years: list[YearDefinition]
    months: list[MonthDefinition]
    weeks: list[WeekDefinition]
    weekdays: list[WeekDayDefinition]
    days: list[DayDefinition]
    holidays: list[HolidayDefinition]

    epoch: str = ''
    zero: bool = True
    negative: bool = True
    start: np.datetime64 = np.datetime64('nat')
    end: np.datetime64 = np.datetime64('nat')
    location: tuple[float, float] = (0.0, 0.0)
    description: str = ''

    def validate(self, year: int, month: int, day: int, iso: str = '') -> bool:
        date: tuple[int, int, int] = (year, month, day)
        if iso != '':
            year, month, day = self.from_iso(iso)
        if year == 0 and not self.zero:
            raise ValueError(CalendarMessage.ZERO)
        if month < 0 or month > len(self.months) - 1:
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
        if self.end != (0, 0, 0) and date > self.end:
            raise ValueError(CalendarMessage.END.format(date, self.end))
        if self.start != (0, 0, 0) and date < self.start:
            raise ValueError(CalendarMessage.BEGIN.format(date, self.start))
        return True

    def days_in_month(self, days: int) -> int:
        return days

    def days_in_year(self, days: int) -> int:
        return days

    def from_iso(self, iso: str) -> tuple[int, int, int]:
        year_month_day: list[str] = iso.split('-')
        year: int = int(year_month_day[0])
        month: int = int(year_month_day[1])
        day: int = int(year_month_day[2])
        return year, month, day

    def format(
        self, year: int, month: int = 0, day: int = 0, iso: str = ''
    ) -> str:
        if iso != '':
            year, month, day = self.from_iso(iso)
        return f'{year!s}-{self.months[month]}-{day!s}'

    # def to(self) -> str:
    #     return self.format()

    def isleap(self, year: int) -> bool:
        return year % 4 == 0 and year % 400 != 0

    def describe(
        self, year: int = 0, month: int = 0, day: int = 0, iso: str = ''
    ) -> str:
        if iso != '':
            year, month, day = self.from_iso(iso)
        lines: str = (
            f'Date: {self.months[month].abbreviation} {day!s}, {year!s}\n'
        )
        lines = ''.join([lines, f'Calendar: {self.name.title()}\n'])
        lines = ''.join([lines, f'Is leap year? {self.isleap(year)}\n'])
        if day > 0:
            pass
        if month > 0:
            pass
        return lines

    def codelist(self, items: list[Any], tabs: int = 1) -> str:
        if len(items) == 0:
            return '[]'
        lines: str = '[\n'
        for item in items:
            lines = ''.join([lines, '    ' * tabs, repr(item), ',\n'])
        return ''.join(
            [
                lines[:-1],
                '\n',
                '    ' * (tabs - 1),
                ']',
            ]
        )

    def code(self, tabs: int = 0) -> str:
        """Generate the code to define the calendar so it can be modified."""

        return indent(
            f"""
CalendarDefinition(
    name = '{self.name}',
    years = {self.codelist(self.years, 2)},
    months = {self.codelist(self.months, 2)},
    weeks = {self.codelist(self.weeks, 2)},
    weekdays = {self.codelist(self.weekdays, 2)},
    days = {self.codelist(self.days, 2)},
    holidays = {self.codelist(self.holidays, 2)},
    epoch = '{self.epoch}',
    zero = {self.zero},
    negative = {self.negative},
    start = np.datetime64('{self.start}'),
    end = np.datetime64('{self.end}'),
    location = {self.location},
    description = '{self.description}',
)""",
            '    ' * tabs,
        )
