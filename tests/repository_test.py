"""------------------------------------------------------------------------------
                            Repository Record Tests
------------------------------------------------------------------------------"""

import pytest

from chronodata.chrono import Chronology
from chronodata.g7 import Gedcom, GEDSpecial

testdata = [('xref', '@1@')]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_repository(test_input: str, expected: str | int | bool) -> None:
    a = Chronology(name='testing')
    xref = a.repository_record('some repository')

    assert eval(test_input) == expected
