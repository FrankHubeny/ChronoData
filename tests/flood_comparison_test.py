"""------------------------------------------------------------------------------
                        Flood Comparison Tests

    This builds two chronologies based on two different biblical
    accounts of when the flood occurred and puts in a challenge
    based on a living tree to show one chronology is more likely
    than the other.
------------------------------------------------------------------------------"""

import pytest

from chronodata.build import Chronology

testdata = [('ussher_mankind', '@MANKIND@')]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_flood_comparisons(test_input: str, expected: str | int | bool) -> None:
    a = Chronology(name='ussher')
    ussher_mankind = str(a.family_xref(' Mankind '))  # noqa: F841

    b = Chronology(name='smith')
    smith_mankind = str(b.family_xref('Mankind'))  # noqa: F841

    assert eval(test_input) == expected
