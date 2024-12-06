"""------------------------------------------------------------------------------
                            Family Record Tests
------------------------------------------------------------------------------"""

import pytest

from chronodata.chrono import Chronology
from chronodata.g7 import Gedcom, GEDSpecial

testdata = [
    ('a.xref_family[0]', '@1@'),
    ('result1[0]', f'0 @1@ {Gedcom.FAM}'),
    ('result1[1]', f'1 {Gedcom.CREA}'),
    ('result1[2][0:6]', f'1 {Gedcom.DATE}'),
    ('result1[3][0:6]', f'2 {Gedcom.TIME}'),
    
]
@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_family(test_input: str, expected: str | int | bool) -> None:
    a = Chronology(name='testing')
    a.family_record()
    result1 = a.ged_family
    
    assert eval(test_input) == expected