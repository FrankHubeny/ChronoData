"""------------------------------------------------------------------------------
                            Multimedia Record Tests
------------------------------------------------------------------------------"""

import pytest

from chronodata.build import Chronology
from chronodata.g7 import Gedcom, GEDSpecial

testdata = [
    ('xref', '@1@'),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_family(test_input: str, expected: str | int | bool) -> None:
    a = Chronology(name='testing')
    xref = a.multimedia_record(files=[['hello world', 'text/html']])

    assert eval(test_input) == expected
