"""------------------------------------------------------------------------------
                            Submitter Record Tests
------------------------------------------------------------------------------"""

import pytest

from chronodata.chrono import Chronology
from chronodata.g7 import Gedcom, GEDSpecial

testdata = [
    ('xref', '@1@'),
    ('minimal_result[0]', f'0 @1@ {Gedcom.SUBM}'),
    ('minimal_result[1]', f'1 {Gedcom.NAME} frank'),
    ('len(minimal_result)', 3),
    ('address_result[2]', f'1 {Gedcom.ADDR} 1234 Here Street'), 
    ('address_result[3]', f'1 {Gedcom.CONT} There, CA 22222'), 
    ('address_result[4]', f'1 {Gedcom.CONT} usa'),
    ('len(address_result)', 6),
    
    
]
@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_submitter(test_input: str, expected: str | int | bool) -> None:
    # Run submitter with only the required name.
    a = Chronology(name='minimal')
    xref = a.submitter_record(name='frank')
    minimal_result = a.ged_submitter.split('\n')

    # Run submitter with name and address.
    b = Chronology(name='address')
    address_xref = b.submitter_record(name='frank',address='1234 Here Street\nThere, CA 22222\nusa')
    address_result = b.ged_submitter.split('\n')
    
    
    
    
    assert eval(test_input) == expected