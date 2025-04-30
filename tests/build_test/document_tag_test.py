# document_tag_test.py
"""Tests to cover the document_tag method in the Genealogy class."""

import re

import pytest

import genedata.classes70 as gc
from genedata.build import Genealogy
from genedata.constants import Default
from genedata.messages import Msg
from genedata.methods import Query, Validate
from genedata.specifications70 import Specs
from genedata.structure import Void

# Calendar Extensions

mycalendar: str = 'tests\\data\\extension_tests\\calendars\\cal-_MYGREGORIAN.yaml'
myjan: str = 'tests\\data\\extension_tests\\months\\month-_MYJAN.yaml'
myfeb: str = 'tests\\data\\extension_tests\\months\\month-_MYFEB.yaml'
mymar: str = 'tests\\data\\extension_tests\\months\\month-_MYMAR.yaml'
myapr: str = 'tests\\data\\extension_tests\\months\\month-_MYAPR.yaml'
mymay: str = 'tests\\data\\extension_tests\\months\\month-_MYMAY.yaml'
myjun: str = 'tests\\data\\extension_tests\\months\\month-_MYJUN.yaml'
myjul: str = 'tests\\data\\extension_tests\\months\\month-_MYJUL.yaml'
myaug: str = 'tests\\data\\extension_tests\\months\\month-_MYAUG.yaml'
mysep: str = 'tests\\data\\extension_tests\\months\\month-_MYSEP.yaml'
myoct: str = 'tests\\data\\extension_tests\\months\\month-_MYOCT.yaml'
mynov: str = 'tests\\data\\extension_tests\\months\\month-_MYNOV.yaml'
mydec: str = 'tests\\data\\extension_tests\\months\\month-_MYDEC.yaml'
def test_add_calendar_tag() -> None:
    g = Genealogy()
    g.document_tag('_MYGREGORIAN', mycalendar)
    assert (
        g.specification[Default.YAML_TYPE_CALENDAR]['cal-_MYGREGORIAN'][Default.YAML_TYPE]
        == Default.YAML_TYPE_CALENDAR
    )


def test_add_calendar_tag_underline_upper() -> None:
    g = Genealogy()
    g.document_tag('_MYGREGORIAN', mycalendar)
    assert (
        g.specification[Default.YAML_TYPE_CALENDAR]['cal-_MYGREGORIAN'][
            Default.YAML_EXTENSION_TAGS
        ]
        == '_MYGREGORIAN'
    )

def test_add_calendar_duplicate() -> None:
    h = Genealogy()
    h.document_tag('_MYGREGORIAN', mycalendar)
    with pytest.raises(
        ValueError,
        match=re.escape(Msg.YAML_FILE_HAS_BEEN_USED.format(mycalendar))
    ):
        h.document_tag('_MYGREGORIAN', mycalendar)

def test_add_calendar_with_months() -> None:
    g = Genealogy()
    g.document_tag('_MYGREGORIAN', mycalendar)
    g.document_tag('_MYJAN', myjan)
    g.document_tag('_MYFEB', myfeb)
    g.document_tag('_MYMAR', mymar)
    g.document_tag('_MYAPR', myapr)
    g.document_tag('_MYMAY', mymay)
    g.document_tag('_MYJUN', myjun)
    g.document_tag('_MYJUL', myjul)
    g.document_tag('_MYAUG', myaug)
    g.document_tag('_MYSEP', mysep)
    g.document_tag('_MYOCT', myoct)
    g.document_tag('_MYNOV', mynov)
    g.document_tag('_MYDEC', mydec)
    assert gc.Date('_MYGREGORIAN 1 _MYJAN 2000 BC').validate(specs=g.specification)

# Enumeration Extensions

enum_hide: str = 'tests\\data\\extension_tests\\enumerations\\enum-_HIDE.yaml'
def test_document_tag() -> None:
    g = Genealogy()
    g.document_tag('_HIDE', enum_hide)
    assert len(g.ged_ext_tags) == 1

def test_document_tag_resn() -> None:
    g = Genealogy()
    g.document_tag('_HIDE', enum_hide)
    enums: list[str] = Query.enumerations('enumset-RESN', g.specification)
    assert '_HIDE' in enums

def test_document_tag_no_hide() -> None:
    h = Genealogy()
    enums: list[str] = Query.enumerations('enumset-RESN', h.specification) 
    assert '_HIDE' not in enums

def test_document_tag_resn_without_hide() -> None:
    h = Genealogy()
    m = gc.Resn('LOCKED, CONFIDENTIAL')
    assert m.validate(specs=h.specification)

def test_document_tag_resn_with_hide() -> None:
    h = Genealogy()
    h.document_tag('_HIDE', enum_hide)
    m = gc.Resn('LOCKED, CONFIDENTIAL, _HIDE')
    assert m.validate(specs=h.specification)

def test_document_tag_resn_with_hide_by_itself() -> None:
    h = Genealogy()
    h.document_tag('_HIDE', enum_hide)
    m = gc.Resn('_HIDE')
    assert m.validate(specs=h.specification)

def test_document_tag_resn_with_hide_view_extensions() -> None:
    h = Genealogy()
    h.document_tag('_HIDE', enum_hide)
    values, keys, labels = h.view_extensions()
    assert values[0][0] == '_HIDE'

def test_document_tag_resn_hide_not_there() -> None:
    h = Genealogy()
    m = gc.Resn('LOCKED, CONFIDENTIAL, _HIDE')
    with pytest.raises(
        ValueError,
        match=re.escape(Msg.NOT_VALID_ENUM.format('_HIDE', ['CONFIDENTIAL', 'LOCKED', 'PRIVACY'], m.class_name))
    ):
        m.validate(specs=h.specification)

def test_document_tag_resn_xhide_not_there_but_hide_is() -> None:
    h = Genealogy()
    h.document_tag('_HIDE', enum_hide)
    m = gc.Resn('LOCKED, CONFIDENTIAL, _XHIDE')
    with pytest.raises(
        ValueError,
        match=re.escape(Msg.NOT_VALID_ENUM.format('_XHIDE', ['CONFIDENTIAL', 'LOCKED', 'PRIVACY', '_HIDE'], m.class_name))
    ):
        m.validate(specs=h.specification)

def test_document_tag_resn_duplicate() -> None:
    h = Genealogy()
    h.document_tag('_HIDE', enum_hide)
    with pytest.raises(
        ValueError,
        match=re.escape(Msg.YAML_FILE_HAS_BEEN_USED.format(enum_hide))
    ):
        h.document_tag('_XHIDE', enum_hide)

