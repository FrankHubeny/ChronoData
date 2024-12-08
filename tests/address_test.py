"""------------------------------------------------------------------------------
                            Address Tests

    These tests cover the `address_structure` procedure.

------------------------------------------------------------------------------"""

import pytest

from chronodata.chrono import Chronology

testdata = [
    ('address[0]', '1 ADDR 123 Here Street'),
    ('address[1]', '1 CONT My Town'),
    ('address[2]', '1 CONT USA'),
    ('address2[0]', '1 ADDR someplace'),
    ('address2[1]', '2 CITY My City'),
    ('address2[2]', '2 STAE My State'),
    ('address2[3]', '2 POST My Postal'),
    ('address2[4]', '2 CTRY My Country'),
    ('address3[0]', '1 ADDR 123 Here Street'),
    ('address3[1]', '1 CONT My Town'),
    ('address3[2]', '1 CONT USA'),
    ('address3[3]', '2 CITY My Town'),
    ('address4[0]', '1 ADDR 123 Here Street'),
    ('address4[1]', '1 CONT My Town'),
    ('address4[2]', '1 CONT USA'),
    ('address4[3]', '2 CITY My Town'),
    ('address4[4]', '2 STAE My State'),
    ('address4[5]', '2 POST My Postal'),
    ('address4[6]', '2 CTRY My Country'),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_address(test_input: str, expected: str | int | bool) -> None:
    a = Chronology(name='testing')
    address = a.address_structure('123 Here Street\nMy Town\nUSA').split('\n')  # noqa: F841
    address2 = a.address_structure(
        'someplace', 'My City', 'My State', 'My Postal', 'My Country'
    ).split('\n')  # noqa: F841
    address3 = a.address_structure("""123 Here Street
My Town
USA""", city='My Town').split('\n')
    address4 = a.address_structure("""123 Here Street
My Town
USA""", city='My Town', state='My State', postal='My Postal', country='My Country').split('\n')

    assert eval(test_input) == expected
