"""------------------------------------------------------------------------------
                            Uranium Tests

    This builds a chronology of the uranium transition to lead testing
    results along the way.
------------------------------------------------------------------------------"""

import pytest

from chronodata.chrono import Chronology
from chronodata.g7 import Gedcom

testdata = [('uraniumfamily', '@URANIUM_FAMILY@')]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_address(test_input: str, expected: str | int | bool) -> None:
    a = Chronology(name='uranium')
    uraniumfamily = a.family_xref('uranium family ')

    assert eval(test_input) == expected
