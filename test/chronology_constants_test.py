"""------------------------------------------------------------------------------
                            Chronology Constants Tests
------------------------------------------------------------------------------"""

import pytest

from chronodata.chronology import Chronology, KEYS, CALENDARS, CONSTANTS, DATETIMES

"""------------------------------------------------------------------------------
                                   Constants
------------------------------------------------------------------------------"""

testdata = [
    # keys
    ('KEYS["EVENTS"]', 'EVENTS'),
    ('KEYS["ACTORS"]', 'ACTORS'),
    ('KEYS["BEFOREPRESENT"]', 'Before Present'),
    ('KEYS["BEGIN"]', 'BEGIN'),
    ('KEYS["BIRTH"]', 'BIRTH'),
    ('KEYS["CALENDAR"]', 'CALENDAR'),
    ('KEYS["CHALLENGES"]', 'CHALLENGES'),
    ('KEYS["DATE"]', 'DATE'),
    ('KEYS["DEATH"]', 'DEATH'),
    ('KEYS["DESCRIPTION"]', 'DESCRIPTION'),
    ('KEYS["END"]', 'END'),
    ('KEYS["EVENTS"]', 'EVENTS'),
    ('KEYS["EXPERIMENT"]', 'Experiment'),
    ('KEYS["FATHER"]', 'FATHER'),
    ('KEYS["FEMALE"]', 'FEMALE'),
    ('KEYS["FILE"]', 'FILENAME'),
    ('KEYS["GREGORIAN"]', 'Gregorian'),
    ('KEYS["MALE"]', 'MALE'),
    ('KEYS["MARKERS"]', 'MARKERS'),
    ('KEYS["MOTHER"]', 'MOTHER'),
    ('KEYS["NAME"]', 'NAME'),
    ('KEYS["NEGLABEL"]', 'NEG LABEL'),
    ('KEYS["OVERVIEW"]', 'OVERVIEW'),
    ('KEYS["PERIODS"]', 'PERIODS'),
    ('KEYS["POSLABEL"]', 'POS LABEL'),
    ('KEYS["SECULAR"]', 'Secular'),
    ('KEYS["TEXTS"]', 'TEXTS'),
    ('KEYS["USEZERO"]', 'USE ZERO'),
    ('KEYS["ZEROYEAR"]', 'ZERO YEAR'),
    # calendars
    ('CALENDARS["Gregorian"]["NAME"]', 'Gregorian'),
    ('CALENDARS[KEYS["GREGORIAN"]]["NAME"]', 'Gregorian'),
    ('CALENDARS[KEYS["SECULAR"]]["NAME"]', 'Secular'),
    ('CALENDARS[KEYS["BEFOREPRESENT"]]["NAME"]', 'Before Present'),
    ('CALENDARS[KEYS["EXPERIMENT"]]["NAME"]', 'Experiment'),
    # constants
    ('CONSTANTS["DATETIMEEPOCH"]', 1970),
    ('CONSTANTS["LEFTBRACE"]', '{'),
    ('CONSTANTS["NEGATIVE"]', '-'),
    ('CONSTANTS["NEWLINE"]', '\n'),
    ('CONSTANTS["RIGHTBRACE"]', '}'),
    ('CONSTANTS["SPACE"]', ' '),
    # datetimes
    ('DATETIMES["ATTOSECOND"]', 'as'),
    ('DATETIMES["DAY"]', 'D'),
    ('DATETIMES["FEMTOSECOND"]', 'fs'),
    ('DATETIMES["HOUR"]', 'h'),
    ('DATETIMES["MICROSECOND"]', 'us'),
    ('DATETIMES["MILLISECOND"]', 'ms'),
    ('DATETIMES["MINUTE"]', 'm'),
    ('DATETIMES["MONTH"]', 'M'),
    ('DATETIMES["NANOSECOND"]', 'ns'),
    ('DATETIMES["PICOSECOND"]', 'ps'),
    ('DATETIMES["SECOND"]', 's'),
    ('DATETIMES["WEEK"]', 'W'),
    ('DATETIMES["YEAR"]', 'Y'),
]

@pytest.mark.parametrize("input_n,expected", testdata)
def test_constants(input_n, expected):
    assert eval(input_n) == expected

