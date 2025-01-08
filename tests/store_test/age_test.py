"""------------------------------------------------------------------------------
                            Age Tests

    These tests cover the `Age` NamedTuple class.

    Specification: https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#age

------------------------------------------------------------------------------"""


import pytest

from chronodata.constants import Choice
from chronodata.messages import Msg
from chronodata.store import Age

testdata = [
    ('a1.ged(1)', '1 AGE > 10y\n'),
    ('a2.ged(2)', '2 AGE 5d\n'),
    ('a3.ged(30)', '30 AGE < 1w\n'),
    ('a4.ged(2)', '2 AGE 1y 1m 1w 1d\n'),
    ('a5.ged(1)', '1 AGE < 2m\n'),
    ('a6.ged(3)', '3 AGE < 2m\n4 PHRASE not sure about the age\n'),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_time(test_input: str, expected: str | int | bool) -> None:
    a1 = Age(years=10)  # noqa: F841
    a2 = Age(greater_less_than='', days=5)  # noqa: F841
    a3 = Age(greater_less_than='<', weeks=1)  # noqa: F841
    a4 = Age(1, 1, 1, 1, greater_less_than='')  # noqa: F841
    a5 = Age(greater_less_than='<', months=2)  # noqa: F841
    a6 = Age(greater_less_than='<', months=2, phrase='not sure about the age')  # noqa: F841

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


def test_phrase() -> None:
    with pytest.raises(TypeError):
        Age(days=10, phrase=1).validate()  # type: ignore[arg-type]


# def test_greater_less_than() -> None:
#     with pytest.raises(
#         ValueError,
#         match=Msg.NOT_VALID_CHOICE.format('10', Choice.GREATER_LESS_THAN),
#     ):
#         Age(1, 1, 1, 1, '10').validate()  
