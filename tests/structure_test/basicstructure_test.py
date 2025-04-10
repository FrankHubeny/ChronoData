# basicstructure_test.py
"""Tests to cover the BasicStructure class."""

import pytest

import genedata.classes70 as gc
from genedata.messages import Msg


def test_y_null_data_type_validation_y() -> None:
    m = gc.Will('Y')
    assert m.validate()

def test_y_null_data_type_validation_null() -> None:
    m = gc.Will('')
    assert m.validate()

def test_y_null_data_type_validation_other() -> None:
    value: str = 'abc'
    m = gc.Will(value)
    with pytest.raises(
        ValueError,
        match=Msg.VALUE_NOT_Y_OR_NULL.format(value, m.class_name),
    ):
        m.validate()

def test_date_period() -> None:
    value: str = 'FROM 1 JAN 2000 TO 1 JAN 2001'
    m = gc.DataEvenDate(value)
    assert m.validate()

def test_date_period_bad() -> None:
    value: str = 'ABT 1 JAN 2000'
    m = gc.DataEvenDate(value)
    with pytest.raises(
        ValueError,
        match=Msg.NOT_DATE_PERIOD.format(value, m.class_name),
    ):
        m.validate()

def test_date_exact() -> None:
    value: str = '1 JAN 2000'
    m = gc.DateExact(value)
    assert m.validate()

def test_date_exact_bad() -> None:
    value: str = '2000'
    m = gc.DateExact(value)
    with pytest.raises(
        ValueError,
        match=Msg.NOT_DATE_EXACT.format(value, m.class_name),
    ):
        m.validate()

def test_date() -> None:
    value: str = '1 JAN 2000'
    m = gc.Date(value)
    assert m.validate()

def test_date_bad() -> None:
    value: str = 'not a date'
    m = gc.Date(value)
    with pytest.raises(
        ValueError,
        match=Msg.NOT_DATE.format(value, m.class_name),
    ):
        m.validate()

def test_time() -> None:
    value: str = '01:10:11'
    m = gc.Time(value)
    assert m.validate()

def test_time_bad() -> None:
    value: str = 'not a time'
    m = gc.Time(value)
    with pytest.raises(
        ValueError,
        match=Msg.NOT_TIME.format(value, m.class_name),
    ):
        m.validate()

def test_lati_integer() -> None:
    value: int = 10
    m = gc.Lati(value)  # type: ignore[arg-type]
    with pytest.raises(
        ValueError,
        match=Msg.NOT_STRING.format(str(value), m.class_name),
    ):
        m.validate()

def test_long_integer() -> None:
    value: int = 10
    m = gc.Long(value)  # type: ignore[arg-type]
    with pytest.raises(
        ValueError,
        match=Msg.NOT_STRING.format(str(value), m.class_name),
    ):
        m.validate()
        