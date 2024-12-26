"""------------------------------------------------------------------------------
                            Languages Tests

    These tests cover the `langs` module.

------------------------------------------------------------------------------"""

import pytest

from chronodata.langs import Lang

testdata = [
    ('english', 'en'),
    ('compare', True),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_langs(test_input: str, expected: str | int | bool) -> None:
    # Retrieve the code for English.
    english = Lang.CODE['English']  # noqa: F841

    # Some keys have the same value.
    compare: bool = Lang.CODE['Church Slavic'] == Lang.CODE['Slavonic']  # noqa: F841
    


    assert eval(test_input) == expected