"""------------------------------------------------------------------------------
                            DNA Tests

    This builds a chronology based on DNA mutation changes between
    generations.
------------------------------------------------------------------------------"""

import pytest

from chronodata.build import Chronology
from chronodata.g7 import Gedcom

testdata = [('first', '@DNA@')]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_address(test_input: str, expected: str | int | bool) -> None:
    a = Chronology(name='dna')
    first = a.family_xref('DNA')

    assert eval(test_input) == expected
