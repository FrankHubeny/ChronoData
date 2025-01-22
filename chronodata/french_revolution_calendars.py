# french_revolution_calendars
"""Definitions for various forms of the French Revolution calendars."""

import numpy as np

from chronodata.calendars import (
    CalendarDefinition,
    DayDefinition,
    MonthDefinition,
    WeekDayDefinition,
    YearDefinition,
)


class CalendarsFrenchRevolution:
    FRENCH_R = CalendarDefinition(
        name='FRENCH_R',
        years=[],
        months=[
            MonthDefinition(0, '', days=0, abbreviation=''), 
            MonthDefinition(1, 'Vendémiaire', symbol='', days=30, abbreviation='VEND'),
            MonthDefinition(2, 'Brumaire', symbol='', days=30, abbreviation='BRUM'),
            MonthDefinition(3, 'Frimaire', symbol='', days=30, abbreviation='FRIM'),
            MonthDefinition(4, 'Nivôse', symbol='', days=30, abbreviation='NIVO'),
            MonthDefinition(5, 'Pluviôse', symbol='', days=30, abbreviation='PLUV'),
            MonthDefinition(6, 'Ventôse', symbol='', days=30, abbreviation='VENT'),
            MonthDefinition(7, 'Germinal', symbol='', days=30, abbreviation='GERM'),
            MonthDefinition(8, 'Floréal', symbol='', days=30, abbreviation='FLOR'),
            MonthDefinition(9, 'Prairial', symbol='', days=30, abbreviation='PRAI'),
            MonthDefinition(10, 'Messidor', symbol='', days=30, abbreviation='MESS'),
            MonthDefinition(11, 'Thermidor', symbol='', days=30, abbreviation='THER'),
            MonthDefinition(12, 'Fructidor', symbol='', days=30, abbreviation='FRUC'),
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
        holidays=[],
        epoch='',
        zero=False,
        negative=False,
        start=np.datetime64('1792-01-01'),
        end=np.datetime64('1806-04-11'),
        description='',
    )