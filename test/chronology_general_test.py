"""------------------------------------------------------------------------------
                            Chronology General Tests
------------------------------------------------------------------------------"""

import pytest

from chronodata.chronology import Chronology, KEYS, CALENDARS, CONSTANTS, DATETIMES

"""------------------------------------------------------------------------------
                                   init
------------------------------------------------------------------------------"""

testdata = [
    ('a.name', 'oldname'),
    ('len(a.chronology)', 7),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_init(input_n, expected):
    a = Chronology('oldname')
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                add_comment
------------------------------------------------------------------------------"""

testdata = [
    ('a.commentlist[0]', 'Test'),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_add_comment(input_n, expected):
    a = Chronology('oldname')
    a.add_comment('Test')
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                                  rename
------------------------------------------------------------------------------"""

testdata = [
    ('a.name', 'newname'),
    ('a.chronology[KEYS["OVERVIEW"]][KEYS["NAME"]]', 'newname'),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_rename(input_n, expected):
    a = Chronology('oldname')
    a.rename('newname')
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                             remove_comment
------------------------------------------------------------------------------"""

testdata = [
    ('a.commentlist[0]', 'Test2'),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_remove_comment(input_n, expected):
    a = Chronology('oldname')
    a.add_comment('Test')
    a.add_comment('Test2')
    a.remove_comment(0)
    assert eval(input_n) == expected

"""------------------------------------------------------------------------------
                            remove_all_comments
------------------------------------------------------------------------------"""

testdata = [
    ('len(a.commentlist)', 0),
]
@pytest.mark.parametrize("input_n,expected", testdata)
def test_remove_all_comments(input_n, expected):
    a = Chronology('oldname')
    a.add_comment('Test')
    a.add_comment('Test2')
    a.remove_all_comments()
    assert eval(input_n) == expected
