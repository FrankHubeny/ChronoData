"""------------------------------------------------------------------------------
                            Age Tests

    These tests cover the `Age` NamedTuple class.

    Specification: https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#age

------------------------------------------------------------------------------"""

import pytest

from chronodata.chrono import Age
from chronodata.messages import Msg

testdata = [
    ('a1.ged()', '10y'),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_time(test_input: str, expected: str | int | bool) -> None:
    a1 = Age(10)  # noqa: F841

    assert eval(test_input) == expected


# def test_time_not_int_hour() -> None:
#     with pytest.raises(TypeError):
#         Time('10', 10, 10).validate()  # type: ignore[arg-type]
