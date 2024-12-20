"""------------------------------------------------------------------------------
                        Flood Comparison Tests

    This builds two chronologies based on two different biblical
    accounts of when the flood occurred and puts in a challenge
    based on a living tree to show one chronology is more likely
    than the other.
------------------------------------------------------------------------------"""

import pytest

from chronodata.build import Chronology
from chronodata.g7 import Gedcom

testdata = [('ussher_mankind', '@MANKIND@')]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_address(test_input: str, expected: str | int | bool) -> None:
    a = Chronology(name='ussher')
    ussher_mankind = a.family_xref(' Mankind ')

    b = Chronology(name='smith')
    smith_mankind = a.family_xref('Mankind')

    assert eval(test_input) == expected
