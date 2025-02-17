"""------------------------------------------------------------------------------
                            Time Tests

    These tests cover the `Time` NamedTuple class.

    Specification: https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#time

------------------------------------------------------------------------------"""

import pytest

from genedata.messages import Msg
from genedata.store import Time

testdata = [
    ('t1.ged(1)', '1 TIME 04:30:10\n'),
    ('t2.ged(1)', '1 TIME 04:30:10Z\n'),
    ('t3.ged(10)', '10 TIME 00:10:10\n'),
    ('t4.ged(1)', '1 TIME 01:10:10.123\n'),
    ('t5.ged(1)', '1 TIME 01:01:01Z\n'),
    ('t6.ged(2)', '2 TIME 11:11:11\n'),
    ('t7.ged(22)', '22 TIME 12:12:12Z\n'),
    ('t8.ged(0)', '0 TIME 00:00:00\n'),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_time(test_input: str, expected: str | int | bool) -> None:
    t1 = Time(4, 30, 10)  # noqa: F841
    t2 = Time(4, 30, 10, UTC=True)  # noqa: F841
    t3 = Time(0, 10, 10)  # noqa: F841
    t4 = Time(1, 10, 10.123)  # noqa: F841
    t5 = Time(1, 1, 1, UTC=True)  # noqa: F841
    t6 = Time(11, 11, 11)  # noqa: F841
    t7 = Time(12, 12, 12, UTC=True)  # noqa: F841
    t8 = Time(0, 0, 0)  # noqa: F841

    assert eval(test_input) == expected


def test_time_not_int_hour() -> None:
    with pytest.raises(TypeError):
        Time('10', 10, 10).validate()  # type: ignore[arg-type]


def test_time_not_int_minute() -> None:
    with pytest.raises(TypeError):
        Time(10, '10', 10).validate()  # type: ignore[arg-type]


def test_time_not_int_nor_float_second() -> None:
    with pytest.raises(TypeError):
        Time(10, 10, '10').validate()  # type: ignore[arg-type]


def test_time_hour_value() -> None:
    with pytest.raises(ValueError, match=Msg.RANGE_ERROR.format(24, 0, 23)):
        Time(24, 0, 0).validate()


def test_time_minute_value() -> None:
    with pytest.raises(ValueError, match=Msg.RANGE_ERROR.format(60, 0, 59)):
        Time(0, 60, 0).validate()


def test_time_second_value() -> None:
    with pytest.raises(ValueError, match=Msg.RANGE_ERROR.format(60, 0, 59.999999999999)):
        Time(0, 0, 60).validate()


def test_time_second_float_value() -> None:
    with pytest.raises(ValueError, match=Msg.RANGE_ERROR.format(60.0, 0, 59.999999999999)):
        Time(0, 0, 60.0).validate()


def test_time_hour_negative_value() -> None:
    with pytest.raises(ValueError, match=Msg.RANGE_ERROR.format(-20, 0, 23)):
        Time(-20, 0, 0).validate()


def test_time_minute_negative_value() -> None:
    with pytest.raises(ValueError, match=Msg.RANGE_ERROR.format(-10, 0, 59)):
        Time(0, -10, 0.0).validate()


def test_time_second_negative_value() -> None:
    with pytest.raises(ValueError, match=Msg.RANGE_ERROR.format(-10.1230, 0, 59.999999999999)):
        Time(0, 0, -10.1230).validate()
