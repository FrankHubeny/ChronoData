"""------------------------------------------------------------------------------
                            Languages Tests

    These tests cover the `langs` module.

------------------------------------------------------------------------------"""

import pytest

from chronodata.langs import Lang
from chronodata.methods import DefTag

testdata = [
    ('english', 'en'),
    ('compare', True),
    ('code', '1 LANG en\n'),
    ('language', '1 LANG en\n'),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_langs(test_input: str, expected: str | int | bool) -> None:
    # Retrieve the code for English.
    english = Lang.CODE['English']  # noqa: F841

    # Some keys have the same value.
    compare: bool = Lang.CODE['Church Slavic'] == Lang.CODE['Old Slavonic']  # noqa: F841

    # Check that tags work for both language name and code.
    code: str = DefTag.taglanguage(1, 'en', Lang.CODE)  # noqa: F841
    language: str = DefTag.taglanguage(1, 'English', Lang.CODE)  # noqa: F841
    


    assert eval(test_input) == expected