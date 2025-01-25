# hebraic_calendars
"""Calendars associated with Israel and the Jewish people, ancient and modern."""

import numpy as np

from calendars.calendars import (
    CalendarDefinition,
    DayDefinition,
    MonthDefinition,
    WeekDayDefinition,
    YearDefinition,
)


class CalendarsHebraic:
    HEBREW = CalendarDefinition(
        name='Hebrew',
        years=YearDefinition(19, 19 * 12, (19 * 365) + 4),
        months=[
            MonthDefinition(0, '', days=0, abbreviation=''), 
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
        holidays=[],
        epoch_year=np.datetime64('-3761-10-07', 'Y'),
        epoch_month=np.datetime64('-3761-10-07', 'M'),
        epoch_day=np.datetime64('-3761-10-07', 'D'),
        negative=False,
        zero=False,
        description='',
    )