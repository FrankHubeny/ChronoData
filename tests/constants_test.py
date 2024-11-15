"""------------------------------------------------------------------------------
                            Chronology Constants Tests
------------------------------------------------------------------------------"""

import pytest

from chronodata.constants import (
    Arg,  # noqa: F401
    Calendar,  # noqa: F401
    Column,  # noqa: F401
    Key,  # noqa: F401
    Msg,  # noqa: F401
    String,  # noqa: F401
    Unit,  # noqa: F401
    Value,  # noqa: F401
)

"""------------------------------------------------------------------------------
                                   Constants
------------------------------------------------------------------------------"""

testdata = [
    # arg
    ('Arg.JSON', '.json'),
    ('Arg.INDEX', 'index'),
    ('Arg.INT', 'int'),
    ('Arg.WRITE', 'w'),
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
    ('Key.PRE', 'PRE'),
    ('Key.PERIODS', 'PERIODS'),
    ('Key.POST', 'POST'),
    ('Key.SOURCES', 'SOURCES'),
    ('Key.STRICT', 'STRICT'),
    ('Key.TEXTS', 'TEXTS'),
    ('Key.TIMESTAMP', 'TIMESTAMP'),
    ('Key.ZERO', 'ZERO'),
    # values
    ('Value.AD', ' AD'),
    ('Value.BC', ' BC'),
    ('Value.BCE', ' BCE'),
    ('Value.BEFORE_PRESENT', 'BEFORE PRESENT'),
    ('Value.BP', ' BP'),
    ('Value.CE', ' CE'),
    ('Value.DATETIME_EPOCH', 1970),
    ('Value.EMPTY', ''),
    ('Value.EXPERIMENT', 'EXPERIMENT'),
    ('Value.GREGORIAN', 'GREGORIAN'),
    ('Value.SECULAR', 'SECULAR'),
    # columns
    ('Column.RESERVED', 'Reserved Keys'),
    # calendars
    ('Calendar.GREGORIAN[Key.NAME]', 'GREGORIAN'),
    ('Calendar.GREGORIAN[Key.POST]', ' AD'),
    ('Calendar.GREGORIAN[Key.PRE]', ' BC'),
    ('Calendar.GREGORIAN[Key.STRICT]', True),
    ('Calendar.GREGORIAN[Key.ZERO]', False),
    ('Calendar.SECULAR[Key.NAME]', 'SECULAR'),
    ('Calendar.SECULAR[Key.POST]', ' CE'),
    ('Calendar.SECULAR[Key.PRE]', ' BCE'),
    ('Calendar.SECULAR[Key.STRICT]', True),
    ('Calendar.SECULAR[Key.ZERO]', False),
    ('Calendar.BEFORE_PRESENT[Key.NAME]', 'BEFORE PRESENT'),
    ('Calendar.BEFORE_PRESENT[Key.POST]', ''),
    ('Calendar.BEFORE_PRESENT[Key.PRE]', ' BP'),
    ('Calendar.BEFORE_PRESENT[Key.STRICT]', True),
    ('Calendar.BEFORE_PRESENT[Key.ZERO]', False),
    ('Calendar.EXPERIMENT[Key.NAME]', 'EXPERIMENT'),
    ('Calendar.EXPERIMENT[Key.POST]', ''),
    ('Calendar.EXPERIMENT[Key.PRE]', ''),
    ('Calendar.EXPERIMENT[Key.STRICT]', True),
    ('Calendar.EXPERIMENT[Key.ZERO]', False),
    # strings
    ('String.NEGATIVE', '-'),
    ('String.NEWLINE', '\n'),
    ('String.SPACE', ' '),
    # units
    ('Unit.ATTOSECOND', 'as'),
    ('Unit.DAY', 'D'),
    ('Unit.FEMTOSECOND', 'fs'),
    ('Unit.HOUR', 'h'),
    ('Unit.MICROSECOND', 'us'),
    ('Unit.MILLISECOND', 'ms'),
    ('Unit.MINUTE', 'm'),
    ('Unit.MONTH', 'M'),
    ('Unit.NANOSECOND', 'ns'),
    ('Unit.PICOSECOND', 'ps'),
    ('Unit.SECOND', 's'),
    ('Unit.WEEK', 'W'),
    ('Unit.YEAR', 'Y'),
    # messages
    (
        'Msg.ADDED.format("0","1")',
        'The 0 "1" has been added to the chronology.',
    ),
    ('Msg.ADD_ACTOR.format("0")', 'The actor "0" has been added.'),
    ('Msg.ADD_CHALLENGE.format("0")', 'The challenge "0" has been added.'),
    ('Msg.ADD_COMMENT.format("0")', 'The comment "0" has been added.'),
    ('Msg.ADD_EVENT.format("0")', 'The event "0" has been added.'),
    ('Msg.ADD_MARKER.format("0")', 'The marker "0" has been added.'),
    ('Msg.ADD_PERIOD.format("0")', 'The period "0" has been added.'),
    ('Msg.ADD_SOURCE.format("0")', 'The source "0" has been added.'),
    ('Msg.ADD_TEXT.format("0")', 'The text "0" has been added.'),
    (
        'Msg.BAD_DATE.format("0","1")',
        'The date value "0" does not fit a 1 calendar.',
    ),
    (
        'Msg.BAD_LABEL.format("0","1")',
        'The date "0" contains an inappropriate label "1".',
    ),
    (
        'Msg.CALENDARS_DONT_MATCH.format("0","1")',
        'The calendars "0" and "1" do not match.',
    ),
    (
        'Msg.CHANGED.format("0")',
        'The chronology has been changed to the "0" calendar.',
    ),
    ('Msg.COMMENT_REMOVED.format("0","1")', 'Comment 0 "1" has been removed.'),
    ('Msg.COUNT_RESERVED.format("0")', '0 reserved keys were used.'),
    ('Msg.FILE_SAVED.format("0")', 'The file "0" has been saved.'),
    (
        'Msg.HAS_CALENDAR.format("0")',
        'The chronology already has the "0" calendar.',
    ),
    (
        'Msg.KEY_REMOVED.format("0","1")',
        'The name "0" has been removed from "1".',
    ),
    (
        'Msg.LOADED.format("0","1")',
        'The "0" chronology has been loaded from the "1" file.',
    ),
    ('Msg.NEG_YEAR.format("0")', 'Negative year but a negative label "0".'),
    (
        'Msg.NO_COMMENTS.format("0")',
        'There are no comments for the 0 chronology.',
    ),
    ('Msg.NO_DICT_NAME.format("0","1")', 'The chronology "0" has no 1.'),
    ('Msg.NOT_IN_DICT.format("0","1")', 'The name "0" is not in the "1".'),
    ('Msg.NOT_REMOVABLE.format("0")', 'The name "0" is a reserved key.'),
    ('Msg.ONE', 'One reserved key was used.'),
    ('Msg.OUT_OF_RANGE.format("0")', 'There is no comment at index 0.'),
    ('Msg.POS_YEAR.format("0")', 'Negative year but positive label "0".'),
    ('Msg.REMOVE_ALL_COMMENTS', 'All comments have been removed.'),
    ('Msg.RENAME.format("0")', 'The chronology has been renamed "0".'),
    ('Msg.RESERVED.format("0")', 'The key "0" is a reserved key.'),
    ('Msg.STARTED.format("0")', 'The "0" chronology has been started.'),
    (
        'Msg.STRICT.format("0")',
        'Strict formatting of dates has been set to "0".',
    ),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_constants(test_input: str, expected: str | int | bool) -> None:
    assert eval(test_input) == expected
