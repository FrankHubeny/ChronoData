# julian_calendars
"""Calendar definitions sometimes described as Julian calendars.

References:
    [Time and Date](https://www.timeanddate.com/calendar/julian-calendar.html)
"""

import numpy as np

from calendars.calendars import (
    CalendarDefinition,
    DayDefinition,
    MonthDefinition,
    WeekDayDefinition,
    YearDefinition,
)


class CalendarsJulian:
    JULIAN = CalendarDefinition(
        name='Julian',
        years=YearDefinition(4, 4 * 12, (365 * 4) + 1),
        months=[
            MonthDefinition(0, '', days=0, abbreviation=''), 
            MonthDefinition(1,'JANUARY', days=31, abbreviation='JAN'),
            MonthDefinition(2,'FEBRUARY', days=28, abbreviation='FEB'),
            MonthDefinition(3,'MARCH', days=31, abbreviation='MAR'),
            MonthDefinition(4,'APRIL', days=30, abbreviation='APR'),
            MonthDefinition(5,'MAY', days=31, abbreviation='MAY'),
            MonthDefinition(6,'JUNE', days=30, abbreviation='JUN'),
            MonthDefinition(7,'JULY', days=31, abbreviation='JUL'),
            MonthDefinition(8,'AUGUST', days=31, abbreviation='AUG'),
            MonthDefinition(9,'SEPTEMBER', days=30, abbreviation='SEP'),
            MonthDefinition(10,'OCTOBER', days=31, abbreviation='OCT'),
            MonthDefinition(11,'NOVEMBER', days=30, abbreviation='NOV'),
            MonthDefinition(12,'DECEMBER', days=31, abbreviation='DEC'),
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
        holidays=[],
        epoch_year=np.datetime64('-4713-01-01T12:00:00', 'Y'),
        epoch_month=np.datetime64('-4713-01-01T12:00:00', 'M'),
        epoch_day=np.datetime64('-4713-01-01T12:00:00', 'D'),
        zero=False,
        negative=True,
        description='',
    )