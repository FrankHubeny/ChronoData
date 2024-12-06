"""------------------------------------------------------------------------------
                            Header Tests
------------------------------------------------------------------------------"""

import pytest

from chronodata.chrono import Chronology
from chronodata.g7 import Gedcom, GEDSpecial

testdata = [
    ('result1[0]', f'0 {Gedcom.HEAD}'),
    ('result1[1]', f'1 {Gedcom.GEDC}'),
    ('result1[2]', f'2 {Gedcom.VERS} {GEDSpecial.VERSION}'),
    ('result1[3][0:6]', f'1 {Gedcom.DATE}'),
    ('result1[4][0:6]', f'2 {Gedcom.TIME}'),
    
]
@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_header(test_input: str, expected: str | int | bool) -> None:
    a = Chronology(name='testing')
    a.header()
    result1 = a.ged_header
    
    assert eval(test_input) == expected