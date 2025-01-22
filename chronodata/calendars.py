# calendars

from typing import NamedTuple

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
    """A description of a day in the calendar.
    """
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

    def format(self, year: int, month: int = 0, day: int = 0, iso: str = '') -> str:
        if iso != '':
            year, month, day = self.from_iso(iso)
        return f'{year!s}-{self.months[month]}-{day!s}'

    # def to(self) -> str:
    #     return self.format()

    def isleap(self, year: int) -> bool:
        return year % 4 == 0 and year % 400 != 0

    def describe(self, year: int = 0, month: int = 0, day: int = 0, iso: str = '') -> str:
        if iso != '':
            year, month, day = self.from_iso(iso)
        lines: str = f'Date: {self.months[month].abbreviation} {day!s}, {year!s}\n'
        lines = ''.join([lines, f'Calendar: {self.name.title()}\n'])
        lines = ''.join([lines, f'Is leap year? {self.isleap(year)}\n'])
        if day > 0:
            pass
        if month > 0:
            pass
        return lines
    
    def code(self) -> str:
        """Generate the code to define the calendar so it can be modified."""
        years: str = ''.join([''.join([repr(year), ",\n"]) for year in self.years])
        months: str = ''.join([''.join([repr(month), ",\n"]) for month in self.months])
        days: str = ''.join([''.join([repr(day), ",\n"]) for day in self.days])
        lines : str = f"""
CalendarDefinition(
    name = {self.name},
)"""
        return lines


class Calendars:
    FRENCH_R = CalendarDefinition(
        name='FRENCH_R',
        years=[],
        months=[
            MonthDefinition(1, 'Vendémiaire', symbol='', days=30, abbreviation='VEND'),
            MonthDefinition(1, 'Brumaire', symbol='', days=30, abbreviation='BRUM'),
            MonthDefinition(1, 'Frimaire', symbol='', days=30, abbreviation='FRIM'),
            MonthDefinition(1, 'Nivôse', symbol='', days=30, abbreviation='NIVO'),
            MonthDefinition(1, 'Pluviôse', symbol='', days=30, abbreviation='PLUV'),
            MonthDefinition(1, 'Ventôse', symbol='', days=30, abbreviation='VENT'),
            MonthDefinition(1, 'Germinal', symbol='', days=30, abbreviation='GERM'),
            MonthDefinition(1, 'Floréal', symbol='', days=30, abbreviation='FLOR'),
            MonthDefinition(1, 'Prairial', symbol='', days=30, abbreviation='PRAI'),
            MonthDefinition(1, 'Messidor', symbol='', days=30, abbreviation='MESS'),
            MonthDefinition(1, 'Thermidor', symbol='', days=30, abbreviation='THER'),
            MonthDefinition(1, 'Fructidor', symbol='', days=30, abbreviation='FRUC'),
        ],
        weeks=[],
        weekdays=[
            WeekDayDefinition(1, 'primidi', symbol=''),
            WeekDayDefinition(2,'duodi', symbol=''),
            WeekDayDefinition(3,'tridi', symbol=''),
            WeekDayDefinition(4,'quartidi', symbol=''),
            WeekDayDefinition(5,'quintidi', symbol=''),
            WeekDayDefinition(6,'sextidi', symbol=''),
            WeekDayDefinition(7,'septidi', symbol=''),
            WeekDayDefinition(8,'octidi', symbol=''),
            WeekDayDefinition(9,'nonidi', symbol=''),
            WeekDayDefinition(10,'décadi', symbol=''),
        ],
        days=[
            DayDefinition(1, 'Raisin'),
            DayDefinition(2, 'Safran'),
            DayDefinition(3, 'Châtaigne'),
            DayDefinition(4, 'Colchique'),
            DayDefinition(5, 'Cheval'),
            DayDefinition(6, 'Balsamine'),
            DayDefinition(7, 'Carotte'),
            DayDefinition(8, 'Amaranthe'),
            DayDefinition(9, 'Panais'),
            DayDefinition(10, 'Cuve'),
            DayDefinition(11, 'Pomme de terre'),
            DayDefinition(12, 'Immortelle'),
            DayDefinition(13, 'Potiron'),
            DayDefinition(14, 'Réséda'),
            DayDefinition(15, 'Âne'),
            DayDefinition(16, 'Belle de nuit'),
            DayDefinition(17, 'Citrouille'),
            DayDefinition(18, 'Sarrasin'),
            DayDefinition(19, 'Tournesol'),
            DayDefinition(20, 'Pressoir'),
            DayDefinition(21, 'Chanvre'),
            DayDefinition(22, 'Pêche'),
            DayDefinition(23, 'Navet'),
            DayDefinition(24, 'Amaryllis'),
            DayDefinition(25, 'Bœuf'),
            DayDefinition(26, 'Aubergine'),
            DayDefinition(27, 'Piment'),
            DayDefinition(28, 'Tomate'),
            DayDefinition(29, 'Tomate'),
            DayDefinition(30, 'Orge'),
            DayDefinition(31, 'Tonneau'),
            DayDefinition(32, 'Pomme'),
            DayDefinition(33, 'Céleri'),
            DayDefinition(34, 'Poire'),
            DayDefinition(35, 'Betterave'),
            DayDefinition(36, 'Oie'),
            DayDefinition(37, 'Héliotrope'),
            DayDefinition(38, 'Figue'),
            DayDefinition(39, 'Scorsonère'),
            DayDefinition(40, 'Alisier'),
            DayDefinition(41, 'Charrue'),
            DayDefinition(42, 'Salsifis'),
            DayDefinition(43, 'Mâcre'),
            DayDefinition(44, 'Topinambour'),
            DayDefinition(45, 'Endive'),
            DayDefinition(46, 'Dindon'),
            DayDefinition(47, 'Chervis'),
            DayDefinition(48, 'Cresson'),
            DayDefinition(49, 'Dentelaire'),
            DayDefinition(50, 'Grenade'),
            DayDefinition(51, 'Herse'),
            DayDefinition(52, 'Bacchante'),
            DayDefinition(53, 'Azerole'),
            DayDefinition(54, 'Garance'),
            DayDefinition(55, 'Herse'),
            DayDefinition(56, 'Bacchante'),
            DayDefinition(57, 'Azerole'),
            DayDefinition(58, 'Garance'),
            DayDefinition(59, 'Orange'),
            DayDefinition(60, 'Faisan'),
            DayDefinition(61, 'Pistache'),
            DayDefinition(62, 'Macjonc'),
            DayDefinition(63, 'Coing'),
            DayDefinition(64, 'Cormier'),
            DayDefinition(65, 'Rouleau'),
        ],
        epoch='',
        zero=False,
        negative=False,
        start=np.datetime64('1792-01-01'),
        end=np.datetime64('1806-04-11'),
        description='',
    )

    GREGORIAN = CalendarDefinition(
        name='GREGORIAN',
        years=[],
        months=[
            MonthDefinition(1,'JANUARY', days=31, abbreviation='JAN'),
            MonthDefinition(1,'FEBRUARY', days=28, abbreviation='FEB'),
            MonthDefinition(1,'MARCH', days=31, abbreviation='MAR'),
            MonthDefinition(1,'APRIL', days=30, abbreviation='APR'),
            MonthDefinition(1,'MAY', days=31, abbreviation='MAY'),
            MonthDefinition(1,'JUNE', days=30, abbreviation='JUN'),
            MonthDefinition(1,'JULY', days=31, abbreviation='JUL'),
            MonthDefinition(1,'AUGUST', days=31, abbreviation='AUG'),
            MonthDefinition(1,'SEPTEMBER', days=30, abbreviation='SEP'),
            MonthDefinition(1,'OCTOBER', days=31, abbreviation='OCT'),
            MonthDefinition(1,'NOVEMBER', days=30, abbreviation='NOV'),
            MonthDefinition(1,'DECEMBER', days=31, abbreviation='DEC'),
        ],
        weeks=[],
        weekdays=[
            WeekDayDefinition(1,'Sunday'),
            WeekDayDefinition(2,'Monday'),
            WeekDayDefinition(3,'Tuesday'),
            WeekDayDefinition(4,'Wednesday'),
            WeekDayDefinition(5,'Thursday'),
            WeekDayDefinition(6,'Friday'),
            WeekDayDefinition(7,'Saturday'),
        ],
        days=[],
        epoch='BCE',
        zero=False,
        negative=True,
        description='',
    )
    
    HEBREW = CalendarDefinition(
        name='HEBREW',
        years=[],
        months=[
            MonthDefinition(1,'Tishrei', days=0, abbreviation='TSH'),
            MonthDefinition(2,'Kislev', days=0, abbreviation='CSH'),
            MonthDefinition(3,'Shevat', days=0, abbreviation='TSH'),
            MonthDefinition(4,'Iyar', days=0, abbreviation='TSH'),
            MonthDefinition(5,'Tammuz', days=0, abbreviation='TSH'),
            MonthDefinition(6,'Elul', days=0, abbreviation='TSH'),
            MonthDefinition(7,'Marcheshvan', days=0, abbreviation='TSH'),
            MonthDefinition(8,'Tevet', days=0, abbreviation='TSH'),
            MonthDefinition(9,'Adar', days=0, abbreviation='ADR'),
            MonthDefinition(10,'Veadar', days=0, abbreviation='ADS'),
            MonthDefinition(11,'Nisan', days=0, abbreviation='NSN'),
            MonthDefinition(12,'Sivan', days=0, abbreviation='TSH'),
            MonthDefinition(13,'Av', days=0, abbreviation='AAV'),
        ],
        weeks=[],
        weekdays=[
            WeekDayDefinition(1,'Yom Rishon'),
            WeekDayDefinition(1,'Yom Sheni'),
            WeekDayDefinition(1,'Yom Shlishi'),
            WeekDayDefinition(1,'Yom Revii'),
            WeekDayDefinition(1,'Yom Hamishi'),
            WeekDayDefinition(1,'Yom Shishi'),
            WeekDayDefinition(1,'Yom Shabbat'),
        ],
        days=[],
        epoch='',
        negative=False,
        zero=False,
        start=np.datetime64('-3752-01-01'),
        description='',
    )

    JULIAN = CalendarDefinition(
        name='JULIAN',
        years=[],
        months=[
            MonthDefinition(1,'JANUARY', days=31, abbreviation='JAN'),
            MonthDefinition(1,'FEBRUARY', days=28, abbreviation='FEB'),
            MonthDefinition(1,'MARCH', days=31, abbreviation='MAR'),
            MonthDefinition(1,'APRIL', days=30, abbreviation='APR'),
            MonthDefinition(1,'MAY', days=31, abbreviation='MAY'),
            MonthDefinition(1,'JUNE', days=30, abbreviation='JUN'),
            MonthDefinition(1,'JULY', days=31, abbreviation='JUL'),
            MonthDefinition(1,'AUGUST', days=31, abbreviation='AUG'),
            MonthDefinition(1,'SEPTEMBER', days=30, abbreviation='SEP'),
            MonthDefinition(1,'OCTOBER', days=31, abbreviation='OCT'),
            MonthDefinition(1,'NOVEMBER', days=30, abbreviation='NOV'),
            MonthDefinition(1,'DECEMBER', days=31, abbreviation='DEC'),
        ],
        weeks=[],
        weekdays=[
            WeekDayDefinition(1,'Sunday'),
            WeekDayDefinition(2,'Monday'),
            WeekDayDefinition(3,'Tuesday'),
            WeekDayDefinition(4,'Wednesday'),
            WeekDayDefinition(5,'Thursday'),
            WeekDayDefinition(6,'Friday'),
            WeekDayDefinition(7,'Saturday'),
        ],
        days=[],
        epoch='BCE',
        zero=False,
        negative=True,
        description='',
    )
