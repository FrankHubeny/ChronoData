"""------------------------------------------------------------------------------
                            Address Tests

    These tests cover the `Address` NamedTuple class.

------------------------------------------------------------------------------"""

import pytest

from chronodata.chrono import Address

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
    ('address5[0]', '1 ADDR 123 Here Street'),
    ('address5[1]', '1 CONT My Town'),
    ('address5[2]', '1 CONT USA'),
    ('address6[0]', '1 ADDR 123 Here Street'),
    ('address6[1]', '1 CONT My Town'),
    ('address6[2]', '1 CONT USA'),
    ('address7[0]', '1 ADDR 123 Here Street'),
    ('address7[1]', '1 CONT My Town'),
    ('address7[2]', '1 CONT USA'),
    ######
    ('ap1.ged()', ''),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_address(test_input: str, expected: str | int | bool) -> None:
    address: list[str] = Address('123 Here Street\nMy Town\nUSA').ged().split('\n')  # noqa: F841
    address2: list[str] = (  # noqa: F841
        Address('someplace', 'My City', 'My State', 'My Postal', 'My Country')
        .ged()
        .split('\n')
    )
    address3: list[str] = (  # noqa: F841
        Address(
            """123 Here Street
My Town
USA""",
            city='My Town',
        )
        .ged()
        .split('\n')
    )
    address4: list[str] = (  # noqa: F841
        Address(
            """123 Here Street
My Town
USA""",
            city='My Town',
            state='My State',
            postal='My Postal',
            country='My Country',
        )
        .ged()
        .split('\n')
    )
    address5: list[str] = (
        Address("""
123 Here Street
My Town
USA
""")
        .ged()
        .split('\n')
    )
    address6: list[str] = (
        Address("""

123 Here Street

My Town

USA

""")
        .ged()
        .split('\n')
    )
    address7: list[str] = (  # noqa: F841
        Address("""

        123 Here Street
        My Town
        USA

""")
        .ged()
        .split('\n')
    )
    ap1: Address = Address('', 'city', 'state', 'postal', 'country')  # noqa: F841

    assert eval(test_input) == expected


def test_address_not_string() -> None:
    with pytest.raises(TypeError):
        Address(3456).validate()  # type: ignore[arg-type]


def test_city_not_string() -> None:
    with pytest.raises(TypeError):
        Address('3456', 1).validate()  # type: ignore[arg-type]


def test_state_not_string() -> None:
    with pytest.raises(TypeError):
        Address('3456', '1', 2).validate()  # type: ignore[arg-type]


def test_postal_not_string() -> None:
    with pytest.raises(TypeError):
        Address('3456', '1', '2', 3).validate()  # type: ignore[arg-type]


def test_country_not_string() -> None:
    with pytest.raises(TypeError):
        Address('3456', '1', '2', '3', 4).validate()  # type: ignore[arg-type]
