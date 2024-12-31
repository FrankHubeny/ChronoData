"""------------------------------------------------------------------------------
                            Languages Tests

    These tests cover the `langs` module.

------------------------------------------------------------------------------"""

import pytest

from chronodata.langs import Lang
from chronodata.methods import DefCheck, DefTag

testdata = [
    ('english', 'en'),
    ('compare', True),
    ('code', '1 LANG en\n'),
    ('language', '1 LANG en\n'),
    ('english_keyvalues[0]', 'English: en'),
    ('english_keyvalues2[0]', 'English: en'),
    ('len(cu_keyvalues)', 5),
    ('len(none_keyvalues)', 0),
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
    
    # Check dictionary query method.
    english_keyvalues = DefCheck.get_dict_key_values('English', Lang.CODE)  # noqa: F841
    english_keyvalues2 = DefCheck.get_dict_key_values('en', Lang.CODE)  # noqa: F841
    cu_keyvalues = DefCheck.get_dict_key_values('cu', Lang.CODE)  # noqa: F841
    none_keyvalues = DefCheck.get_dict_key_values('cccccc', Lang.CODE)  # noqa: F841


    assert eval(test_input) == expected