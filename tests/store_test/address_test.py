"""------------------------------------------------------------------------------
                            Address Tests

    These tests cover the `Address` NamedTuple class.

------------------------------------------------------------------------------"""


import pytest

from chronodata.store import Address

testdata = [
    ('address[0]', '1 ADDR 123 Here Street'),
    ('address[1]', '1 CONT My Town'),
    ('address[2]', '1 CONT USA'),
    ('address2[0]', '1 ADDR someplace'),
    ('address2[1]', '2 CITY My City'),
    ('address2[2]', '2 STAE My State'),
    ('address2[3]', '2 POST My Postal'),
    ('address2[4]', '2 CTRY My Country'),
    ######
    #('ap1.ged()', ''),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_address(test_input: str, expected: str | int | bool) -> None:
    address: list[str] = Address('123 Here Street\nMy Town\nUSA').ged().split('\n')  # noqa: F841
    address2: list[str] = (  # noqa: F841
        Address('someplace', 'My City', 'My State', 'My Postal', 'My Country')
        .ged().split('\n')
    )
    ap1: Address = Address('', 'city', 'state', 'postal', 'country')  # noqa: F841

    assert eval(test_input) == expected


# def test_address_not_list() -> None:
#     with pytest.raises(TypeError):
#         Address('').validate()  


# def test_city_not_string() -> None:
#     with pytest.raises(TypeError):
#         Address('3456', 1).validate()  # type: ignore[arg-type]


# def test_state_not_string() -> None:
#     with pytest.raises(TypeError):
#         Address('3456', '1', 2).validate()  # type: ignore[arg-type]


# def test_postal_not_string() -> None:
#     with pytest.raises(TypeError):
#         Address('3456', '1', '2', 3).validate()  # type: ignore[arg-type]


# def test_country_not_string() -> None:
#     with pytest.raises(TypeError):
#         Address('3456', '1', '2', '3', 4).validate()  # type: ignore[arg-type]
