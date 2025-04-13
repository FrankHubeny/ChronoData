"""------------------------------------------------------------------------------
                            Genesis 5 Tests

    This builds a genealogy of the genealogy in Genesis 5.
------------------------------------------------------------------------------"""

import pytest

from genedata.build import Genealogy

testdata = [('adameve', '@ADAM_FAMILY@')]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_address(test_input: str, expected: str | int | bool) -> None:
    a = Genealogy()
    adameve = str(a.family_xref(' Adam family '))  # noqa: F841

    assert eval(test_input) == expected
