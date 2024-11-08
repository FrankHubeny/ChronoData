"""------------------------------------------------------------------------------
                            Chronology General Tests
------------------------------------------------------------------------------"""

import pytest

from chronodata.chronology import Chronology
from chronodata.utils.constants import String, Number, Msg, Datetime, Key, Calendar

"""------------------------------------------------------------------------------
                                   init
------------------------------------------------------------------------------"""

testdata = [
    ('a.name', 'oldname'),
    ('len(a.chronology)', 7),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_init(input_n, expected):
    a = Chronology(user='Frank', chronologyname='oldname')
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                add_comment
------------------------------------------------------------------------------"""

testdata = [
    ('a.chronology[Key.OVERVIEW][Key.COMMENTS][str(1)][Key.MESSAGE]', 'Test'),
    ('a.chronology[Key.OVERVIEW][Key.COMMENTS][str(1)][Key.USER]', 'Frank'),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_add_comment(input_n, expected):
    a = Chronology(user='Frank', chronologyname='oldname')
    a.add_comment('Test')
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  rename
------------------------------------------------------------------------------"""

testdata = [
    ('a.name', 'newname'),
    ('a.chronology[Key.OVERVIEW][Key.NAME]', 'newname'),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_rename(input_n, expected):
    a = Chronology(user='Frank', chronologyname='oldname')
    a.rename('newname')
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                             remove_comment
------------------------------------------------------------------------------"""

testdata = [
    ('a.chronology[Key.OVERVIEW][Key.COMMENTS][str(1)][Key.MESSAGE]', 'Test2'),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_remove_comment(input_n, expected):
    a = Chronology(user='Frank', chronologyname='oldname')
    a.add_comment('Test')
    a.add_comment('Test2')
    a.remove_comment(1)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                            remove_all_comments
------------------------------------------------------------------------------"""

testdata = [
    ('len(a.chronology[Key.OVERVIEW][Key.COMMENTS])', 0),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_remove_all_comments(input_n, expected):
    a = Chronology(user='Frank', chronologyname='oldname')
    a.add_comment('Test')
    a.add_comment('Test2')
    a.remove_all_comments()
    assert eval(input_n) == expected
