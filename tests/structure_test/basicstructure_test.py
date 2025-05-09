# basicstructure_test.py
"""Tests to cover the BasicStructure class."""


import pytest

import genedata.classes70 as gc
from genedata.build import Genealogy
from genedata.messages import Msg
from genedata.structure import Ext


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
        match=Msg.VALUE_NOT_Y_OR_NULL.format(value.upper(), m.class_name),
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


def test_time() -> None:
    value: str = '01:10:11'
    m = gc.Time(value)
    assert m.validate()


def test_time_bad() -> None:
    value: str = 'not a time'
    m = gc.Time(value)
    with pytest.raises(
        ValueError,
        match=Msg.NOT_TIME.format(value.upper(), m.class_name),
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


def test_tag_spaces() -> None:
    value: str = 'T A G'
    m = gc.Tag(value)
    with pytest.raises(ValueError, match=Msg.TAG_SPACES.format(value)):
        m.validate()


def test_not_shared_note() -> None:
    value: int = 1
    m = gc.RecordSnote(value)  # type: ignore[arg-type]
    with pytest.raises(
        ValueError,
        match=Msg.NOT_SHARED_NOTE_XREF.format(value, m.class_name),
    ):
        m.validate()


def test_superstructure_check_sub_list() -> None:
    g = Genealogy()
    d = g.document_tag('_DATE', 'tests/data/extension_tests/structures/_DATE.yaml')
    m = gc.Map([gc.Lati('N10.1'), gc.Long('E10.1'), Ext(d, '1 JAN 2000', []), ])
    with pytest.raises(
        ValueError,
        match=Msg.NOT_SUPERSTRUCTURE.format(m.class_name, '_DATE')
    ):
        m.validate()

def test_superstructure_check_sub_not_list() -> None:
    g = Genealogy()
    d = g.document_tag('_DATE', 'tests/data/extension_tests/structures/_DATE.yaml')
    m = gc.Date('1 JAN 2000', Ext(d, '1 JAN 2000', []))
    with pytest.raises(
        ValueError,
        match=Msg.NOT_SUPERSTRUCTURE.format(m.class_name, '_DATE')
    ):
        m.validate()
