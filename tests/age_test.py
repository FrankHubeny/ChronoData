"""------------------------------------------------------------------------------
                            Age Tests

    These tests cover the `Age` NamedTuple class.

    Specification: https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#age

------------------------------------------------------------------------------"""

import pytest

from chronodata.chrono import Age
from chronodata.g7 import Enum, EnumName
from chronodata.messages import Msg

testdata = [
    ('a1.ged()', '10y'),
    ('a2.ged()', '> 5d'),
    ('a3.ged()', '< 1w'),
    ('a4.ged()', '1y 1m 1w 1d')
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_time(test_input: str, expected: str | int | bool) -> None:
    a1 = Age(years=10)  # noqa: F841
    a2 = Age('>', days=5)  # noqa: F841
    a3 = Age('<', weeks=1)  # noqa: F841
    a4 = Age('', 1, 1, 1, 1)  # noqa: F841

    assert eval(test_input) == expected


def test_years() -> None:
    with pytest.raises(TypeError):
        Age(years='10').validate()  # type: ignore[arg-type]

def test_months() -> None:
    with pytest.raises(TypeError):
        Age(months='10').validate()  # type: ignore[arg-type]

def test_weeks() -> None:
    with pytest.raises(TypeError):
        Age(weeks='10').validate()  # type: ignore[arg-type]

def test_days() -> None:
    with pytest.raises(TypeError):
        Age(days='10').validate()  # type: ignore[arg-type]

def test_greater_less_than() -> None:
    with pytest.raises(ValueError, match=Msg.NOT_VALID_ENUM.format('10', EnumName.GREATER_LESS_THAN)):
        Age('10', 1, 1, 1, 1).validate()  # type: ignore[arg-type]
