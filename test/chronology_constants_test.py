"""------------------------------------------------------------------------------
                            Chronology Constants Tests
------------------------------------------------------------------------------"""

import pytest

from chronodata.utils.constants import String, Number, Msg, Datetime, Key, Calendar

"""------------------------------------------------------------------------------
                                   Constants
------------------------------------------------------------------------------"""

testdata = [
    # keys
    ('Key.value["EVENTS"]', 'EVENTS'),
    ('Key.value["ACTORS"]', 'ACTORS'),
    ('Key.value["BEFOREPRESENT"]', 'Before Present'),
    ('Key.value["BEGIN"]', 'BEGIN'),
    ('Key.value["BIRTH"]', 'BIRTH'),
    ('Key.value["CALENDAR"]', 'CALENDAR'),
    ('Key.value["CHALLENGES"]', 'CHALLENGES'),
    ('Key.value["DATE"]', 'DATE'),
    ('Key.value["DEATH"]', 'DEATH'),
    ('Key.value["DESCRIPTION"]', 'DESCRIPTION'),
    ('Key.value["END"]', 'END'),
    ('Key.value["EVENTS"]', 'EVENTS'),
    ('Key.value["EXPERIMENT"]', 'Experiment'),
    ('Key.value["FATHER"]', 'FATHER'),
    ('Key.value["FEMALE"]', 'FEMALE'),
    ('Key.value["FILE"]', 'FILENAME'),
    ('Key.value["GREGORIAN"]', 'Gregorian'),
    ('Key.value["MALE"]', 'MALE'),
    ('Key.value["MARKERS"]', 'MARKERS'),
    ('Key.value["MOTHER"]', 'MOTHER'),
    ('Key.value["NAME"]', 'NAME'),
    ('Key.value["NEGLABEL"]', 'NEG LABEL'),
    ('Key.value["OVERVIEW"]', 'OVERVIEW'),
    ('Key.value["PERIODS"]', 'PERIODS'),
    ('Key.value["POSLABEL"]', 'POS LABEL'),
    ('Key.value["SECULAR"]', 'Secular'),
    ('Key.value["TEXTS"]', 'TEXTS'),
    ('Key.value["USEZERO"]', 'USE ZERO'),
    ('Key.value["ZEROYEAR"]', 'ZERO YEAR'),
    # calendars
    ('Calendar.system["Gregorian"]["NAME"]', 'Gregorian'),
    ('Calendar.system[Key.value["GREGORIAN"]]["NAME"]', 'Gregorian'),
    ('Calendar.system[Key.value["SECULAR"]]["NAME"]', 'Secular'),
    ('Calendar.system[Key.value["BEFOREPRESENT"]]["NAME"]', 'Before Present'),
    ('Calendar.system[Key.value["EXPERIMENT"]]["NAME"]', 'Experiment'),
    # numbers
    ('Number.DATETIME_EPOCH', 1970),
    # strings
    ('String.LEFT_BRACE', '{'),
    ('String.NEGATIVE', '-'),
    ('String.NEWLINE', '\n'),
    ('String.RIGHT_BRACE', '}'),
    ('String.SPACE', ' '),
    # datetimes
    ('Datetime.unit["ATTOSECOND"]', 'as'),
    ('Datetime.unit["DAY"]', 'D'),
    ('Datetime.unit["FEMTOSECOND"]', 'fs'),
    ('Datetime.unit["HOUR"]', 'h'),
    ('Datetime.unit["MICROSECOND"]', 'us'),
    ('Datetime.unit["MILLISECOND"]', 'ms'),
    ('Datetime.unit["MINUTE"]', 'm'),
    ('Datetime.unit["MONTH"]', 'M'),
    ('Datetime.unit["NANOSECOND"]', 'ns'),
    ('Datetime.unit["PICOSECOND"]', 'ps'),
    ('Datetime.unit["SECOND"]', 's'),
    ('Datetime.unit["WEEK"]', 'W'),
    ('Datetime.unit["YEAR"]', 'Y'),
]

@pytest.mark.parametrize("input_n,expected", testdata)
def test_constants(input_n, expected):
    assert eval(input_n) == expected

