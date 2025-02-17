"""------------------------------------------------------------------------------
                            DNA Tests

    This builds a genealogy based on DNA mutation changes between
    generations.
------------------------------------------------------------------------------"""

import pytest

from genedata.build import Genealogy

testdata = [('first', '@DNA@')]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_address(test_input: str, expected: str | int | bool) -> None:
    a = Genealogy(name='dna')
    first = str(a.family_xref('DNA'))  # noqa: F841

    assert eval(test_input) == expected
