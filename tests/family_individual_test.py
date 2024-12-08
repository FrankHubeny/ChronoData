"""------------------------------------------------------------------------------
                            Family Individual Record Tests
------------------------------------------------------------------------------"""

import pytest

from chronodata.chrono import Chronology
from chronodata.g7 import Gedcom, GEDSpecial

testdata = [
    ('a.individual_xreflist[0]', '@1@'),
    ('man', '@1@'),
    ('a.family_xreflist[0]', '@2@'),
    ('adam_eve', '@2@'),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_family_individual(test_input: str, expected: str | int | bool) -> None:
    a = Chronology(name='testing')
    man = a.individual_xref()
    a.individual_record(xref=man)
    adam_eve = a.family_xref()

    assert eval(test_input) == expected
