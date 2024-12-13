"""------------------------------------------------------------------------------
                            Genesis 5 Tests

    This builds a chronology of the chronology in Genesis 5.
------------------------------------------------------------------------------"""

import pytest

from chronodata.chrono import Chronology
from chronodata.g7 import Gedcom

testdata = [('adameve', '@ADAM_FAMILY@')]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_address(test_input: str, expected: str | int | bool) -> None:
    a = Chronology(name='genesis5')
    adameve = a.family_xref(' Adam family ')

    assert eval(test_input) == expected
