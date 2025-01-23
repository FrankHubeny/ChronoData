# gregorian_calendars
"""This is a set of one or more calendars that represent the Gregorian calendar."""

from calendars.calendars import (
    CalendarDefinition,
    DayDefinition,
    HolidayDefinition,
    MonthDefinition,
    WeekDayDefinition,
    YearDefinition,
)


class CalendarsGregorian:
    GREGORIAN: CalendarDefinition = CalendarDefinition(
        name='GREGORIAN',
        years=[],
        months=[
            MonthDefinition(0, '', days=0, abbreviation=''), 
            MonthDefinition(1, 'JANUARY', days=31, abbreviation='JAN'),
            MonthDefinition(2, 'FEBRUARY', days=28, abbreviation='FEB'),
            MonthDefinition(3, 'MARCH', days=31, abbreviation='MAR'),
            MonthDefinition(4, 'APRIL', days=30, abbreviation='APR'),
            MonthDefinition(5, 'MAY', days=31, abbreviation='MAY'),
            MonthDefinition(6, 'JUNE', days=30, abbreviation='JUN'),
            MonthDefinition(7, 'JULY', days=31, abbreviation='JUL'),
            MonthDefinition(8, 'AUGUST', days=31, abbreviation='AUG'),
            MonthDefinition(9, 'SEPTEMBER', days=30, abbreviation='SEP'),
            MonthDefinition(10, 'OCTOBER', days=31, abbreviation='OCT'),
            MonthDefinition(11, 'NOVEMBER', days=30, abbreviation='NOV'),
            MonthDefinition(12, 'DECEMBER', days=31, abbreviation='DEC'),
        ],
        weeks=[],
        weekdays=[
            WeekDayDefinition(1, 'Sunday', abbreviation='SUN'),
            WeekDayDefinition(2, 'Monday', abbreviation='MON'),
            WeekDayDefinition(3, 'Tuesday', abbreviation='TUE'),
            WeekDayDefinition(4, 'Wednesday', abbreviation='WED'),
            WeekDayDefinition(5, 'Thursday', abbreviation='THU'),
            WeekDayDefinition(6, 'Friday', abbreviation='FRI'),
            WeekDayDefinition(7, 'Saturday', abbreviation='SAT'),
        ],
        days=[],
        holidays=[],
        epoch='BCE',
        zero=False,
        negative=True,
        description='',
    )
