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
    ('Key.ACTORS', 'ACTORS'),
    ('Key.BEFOREPRESENT', 'Before Present'),
    ('Key.BEGIN', 'BEGIN'),
    ('Key.BIRTH', 'BIRTH'),
    ('Key.CALENDAR', 'CALENDAR'),
    ('Key.CHALLENGES', 'CHALLENGES'),
    ('Key.COMMENTS', 'COMMENTS'),
    ('Key.DATE', 'DATE'),
    ('Key.DEATH', 'DEATH'),
    ('Key.DESCRIPTION', 'DESCRIPTION'),
    ('Key.END', 'END'),
    ('Key.EVENTS', 'EVENTS'),
    ('Key.EXPERIMENT', 'Experiment'),
    ('Key.FATHER', 'FATHER'),
    ('Key.FEMALE', 'FEMALE'),
    ('Key.FILE', 'FILENAME'),
    ('Key.GREGORIAN', 'Gregorian'),
    ('Key.LABELS', 'LABELS'),
    ('Key.MALE', 'MALE'),
    ('Key.MARKERS', 'MARKERS'),
    ('Key.MESSAGE', 'MSG'),
    ('Key.MOTHER', 'MOTHER'),
    ('Key.NAME', 'NAME'),
    ('Key.NEGLABEL', 'NEG LABEL'),
    ('Key.OVERVIEW', 'OVERVIEW'),
    ('Key.PERIODS', 'PERIODS'),
    ('Key.POSLABEL', 'POS LABEL'),
    ('Key.SECULAR', 'Secular'),
    ('Key.TEXTS', 'TEXTS'),
    ('Key.TIMESTAMP', 'TIMESTAMP'),
    ('Key.USER', 'USER'),
    ('Key.USEZERO', 'USE ZERO'),
    ('Key.ZEROYEAR', 'ZERO YEAR'),
    # calendars
    ('Calendar.system[Key.GREGORIAN][Key.NAME]', 'Gregorian'),
    ('Calendar.system[Key.SECULAR][Key.NAME]', 'Secular'),
    ('Calendar.system[Key.BEFOREPRESENT][Key.NAME]', 'Before Present'),
    ('Calendar.system[Key.EXPERIMENT][Key.NAME]', 'Experiment'),
    # numbers
    ('Number.DATETIME_EPOCH', 1970),
    # strings
    ('String.ACTOR', 'actor'),
    ('String.CHALLENGE', 'challenge'),
    ('String.EVENT', 'event'),
    ('String.LEFT_BRACE', '{'),
    ('String.LEFT_BRACKET', '['),
    ('String.MARKER', 'marker'),
    ('String.NEGATIVE', '-'),
    ('String.NEWLINE', '\n'),
    ('String.PERIOD', 'period'),
    ('String.RIGHT_BRACE', '}'),
    ('String.RIGHT_BRACKET', ']'),
    ('String.SPACE', ' '),
    ('String.TEXT', 'text'),
    # datetimes
    ('Datetime.ATTOSECOND', 'as'),
    ('Datetime.DAY', 'D'),
    ('Datetime.FEMTOSECOND', 'fs'),
    ('Datetime.HOUR', 'h'),
    ('Datetime.MICROSECOND', 'us'),
    ('Datetime.MILLISECOND', 'ms'),
    ('Datetime.MINUTE', 'm'),
    ('Datetime.MONTH', 'M'),
    ('Datetime.NANOSECOND', 'ns'),
    ('Datetime.PICOSECOND', 'ps'),
    ('Datetime.SECOND', 's'),
    ('Datetime.WEEK', 'W'),
    ('Datetime.YEAR', 'Y'),
]

@pytest.mark.parametrize("input_n,expected", testdata)
def test_constants(input_n, expected):
    assert eval(input_n) == expected

