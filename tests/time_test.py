"""------------------------------------------------------------------------------
                            Time Tests

    These tests cover the `Time` NamedTuple class.

    Specification: https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#time

------------------------------------------------------------------------------"""

import pytest

from chronodata.chrono import Time
from chronodata.messages import Msg

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


def test_time_not_int_hour():
    with pytest.raises(TypeError):
        Time('10', 10, 10).validate()

def test_time_not_int_minute():
    with pytest.raises(TypeError):
        Time(10, '10', 10).validate()


def test_time_not_int_nor_float_second():
    with pytest.raises(TypeError):
        Time(10, 10, '10').validate()


def test_time_hour_value():
    with pytest.raises(ValueError, match=Msg.RANGE.format(24, 0, 24)):
        Time(24, 0, 0).validate()


def test_time_minute_value():
    with pytest.raises(ValueError, match=Msg.RANGE.format(60, 0, 60)):
        Time(0, 60, 0).validate()


def test_time_second_value():
    with pytest.raises(ValueError, match=Msg.RANGE.format(60, 0, 60)):
        Time(0, 0, 60).validate()


def test_time_second_float_value():
    with pytest.raises(ValueError, match=Msg.RANGE.format(60.0, 0.0, 60.0)):
        Time(0, 0, 60.0).validate()


def test_time_hour_negative_value():
    with pytest.raises(ValueError, match=Msg.RANGE.format(-20, 0, 24)):
        Time(-20, 0, 0).validate()


def test_time_minute_negative_value():
    with pytest.raises(ValueError, match=Msg.RANGE.format(-10, 0, 60)):
        Time(0, -10, 0.0).validate()


def test_time_second_negative_value():
    with pytest.raises(ValueError, match=Msg.RANGE.format(-10.1230, 0.0, 60.0)):
        Time(0, 0, -10.1230).validate()
