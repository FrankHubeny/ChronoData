"""------------------------------------------------------------------------------
                            Uranium Tests

    This builds a genealogy of the uranium transition to lead testing
    results along the way.
------------------------------------------------------------------------------"""

import pytest

from chronodata.build import Genealogy

testdata = [('uraniumfamily', '@URANIUM_FAMILY@')]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_address(test_input: str, expected: str | int | bool) -> None:
    a = Genealogy(name='uranium')
    uraniumfamily = str(a.family_xref('uranium family '))  # noqa: F841

    assert eval(test_input) == expected
