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
    ('Key.BEGIN', 'BEGIN'),
    ('Key.BIRTH', 'BIRTH'),
    ('Key.CAL', 'CALENDAR'),
    ('Key.CHALLENGES', 'CHALLENGES'),
    ('Key.COMMENTS', 'COMMENTS'),
    ('Key.DATE', 'DATE'),
    ('Key.DEATH', 'DEATH'),
    ('Key.DESC', 'DESC'),
    ('Key.END', 'END'),
    ('Key.EVENTS', 'EVENTS'),
    ('Key.FATHER', 'FATHER'),
    ('Key.FEMALE', 'FEMALE'),
    ('Key.FILE', 'FILENAME'),
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
    ('Key.SOURCES', 'SOURCES'),
    ('Key.TEXTS', 'TEXTS'),
    ('Key.TIMESTAMP', 'TIMESTAMP'),
    ('Key.USER', 'USER'),
    #('Key.USEZERO', 'USE ZERO'),
    #('Key.ZEROYEAR', 'ZERO YEAR'),
    # calendars
    ('Calendar.GREGORIAN[Key.CAL][Key.NAME]', 'GREGORIAN'),
    ('Calendar.GREGORIAN[Key.CAL][Key.POSLABEL]', ' AD'),
    ('Calendar.GREGORIAN[Key.CAL][Key.NEGLABEL]', ' BC'),
    #('Calendar.GREGORIAN[Key.ZEROYEAR]', -1970),
    #('Calendar.GREGORIAN[Key.USEZERO]', False),
    ('Calendar.SECULAR[Key.CAL][Key.NAME]', 'SECULAR'),
    ('Calendar.SECULAR[Key.CAL][Key.POSLABEL]', ' CE'),
    ('Calendar.SECULAR[Key.CAL][Key.NEGLABEL]', ' BCE'),
    #('Calendar.SECULAR[Key.ZEROYEAR]', -1970),
    #('Calendar.SECULAR[Key.USEZERO]', False),
    ('Calendar.BEFORE_PRESENT[Key.CAL][Key.NAME]', 'BEFORE PRESENT'),
    ('Calendar.BEFORE_PRESENT[Key.CAL][Key.POSLABEL]', ''),
    ('Calendar.BEFORE_PRESENT[Key.CAL][Key.NEGLABEL]', ' BP'),
    #('Calendar.BEFORE_PRESENT[Key.ZEROYEAR]', -1970),
    #('Calendar.BEFORE_PRESENT[Key.USEZERO]', False),
    ('Calendar.EXPERIMENT[Key.CAL][Key.NAME]', 'EXPERIMENT'),
    ('Calendar.EXPERIMENT[Key.CAL][Key.POSLABEL]', ''),
    ('Calendar.EXPERIMENT[Key.CAL][Key.NEGLABEL]', ''),
    #('Calendar.EXPERIMENT[Key.ZEROYEAR]', -1970),
    #('Calendar.EXPERIMENT[Key.USEZERO]', False),
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
    # messages
    ('Msg.ADDED.format("a", "b")', 'The a "b" has been added to the chronology.'),
    ('Msg.ADDED_COMMENT.format("a")', 'The comment "a" has been added.'),
    ('Msg.ALL_COMMENTS_REMOVED', 'All comments have been removed.'),
    ('Msg.BAD_DATE.format("a", "b")', 'The date value "a" does not fit a b calendar.'),
    ('Msg.BAD_LABEL.format("a", "b", "c", "d", "e")', 'The date "a" contains an inappropriate label "b" rather than either "c" or "d" for the e cSalendar.'),
    ('Msg.CALENDARS_DONT_MATCH.format("a", "b")', 'The calendars "a" and "b" do not match.'),
    ('Msg.CHANGED.format("a")', 'The chronology has been changed to the "a" calendar.'),
    ('Msg.CHRONOLOGY_LOADED.format("a", "b")', 'The "a" chronology has been loaded from the "b" file.'),
    ('Msg.CHRONOLOGY_STARTED.format("a")', 'The "a" chronology has been started.'),
    ('Msg.COMMENT_REMOVED.format("a", "b")', 'Comment a "b" has been removed from the chronology.'),
    ('Msg.COUNT_RESERVED.format("a")', 'a reserved keys were used.'),
    ('Msg.FILE_SAVED.format("a")', 'The file "a" has been saved.'),
    ('Msg.HAS_CALENDAR.format("a")', 'The chronology already has the "a" calendar.'),
    ('Msg.KEY_REMOVED.format("a", "b")', 'The name "a" has been removed from "b".'),
    ('Msg.NO_COMMENTS.format("a")', 'There are no comments for the a chronology.'),
    ('Msg.NO_DICT_NAME.format("a", "b")', 'The chronology "a" has no b.'),
    ('Msg.NOT_IN_DICT.format("a", "b")', 'The name "a" is not in the "b".'),
    ('Msg.NOT_REMOVABLE.format("a")', 'The name "a" is a reserved key and cannot be removed.'),
    ('Msg.ONE', 'One reserved key was used.'),
    ('Msg.OUT_OF_RANGE.format("a")', 'There is no comment at index a.'),
    ('Msg.RENAME.format("a")', 'The chronology has been renamed "a".'),
    ('Msg.RESERVED.format("a")', 'The key "a" is a reserved key.'),
]

@pytest.mark.parametrize("input_n,expected", testdata)
def test_constants(input_n, expected):
    assert eval(input_n) == expected

