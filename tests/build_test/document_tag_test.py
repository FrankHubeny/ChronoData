# document_tag_test.py
"""Tests to cover the document_tag method in the Genealogy class."""

import re

import pytest

import genedata.classes70 as gc
from genedata.build import Genealogy
from genedata.constants import Default
from genedata.messages import Msg
from genedata.methods import Query
from genedata.specifications70 import Specs
from genedata.structure import Ext, Void

# Calendar Extensions

mycalendar: str = (
    'tests\\data\\extension_tests\\calendars\\cal-_MYGREGORIAN.yaml'
)
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
        g.specification[Default.YAML_TYPE_CALENDAR]['cal-_MYGREGORIAN'][
            Default.YAML_TYPE
        ]
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
        match=re.escape(Msg.YAML_FILE_HAS_BEEN_USED.format(mycalendar)),
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
    assert gc.Date('_MYGREGORIAN 1 _MYJAN 2000 BC').validate(
        specs=g.specification
    )


# Data Type Extensions

datatype: str = 'tests/data/extension_tests/datatypes/type-BOOL.yml'


def test_datatype() -> None:
    g = Genealogy()
    g.document_tag('BOOL', datatype)
    values, keys, labels = g.view_extensions()
    assert values[0][2] == 'data type'


# Calendar Extensions


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
        match=re.escape(
            Msg.NOT_VALID_ENUM.format(
                '_HIDE', ['CONFIDENTIAL', 'LOCKED', 'PRIVACY'], m.class_name
            )
        ),
    ):
        m.validate(specs=h.specification)


def test_document_tag_resn_xhide_not_there_but_hide_is() -> None:
    h = Genealogy()
    h.document_tag('_HIDE', enum_hide)
    m = gc.Resn('LOCKED, CONFIDENTIAL, _XHIDE')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_VALID_ENUM.format(
                '_XHIDE',
                ['CONFIDENTIAL', 'LOCKED', 'PRIVACY', '_HIDE'],
                m.class_name,
            )
        ),
    ):
        m.validate(specs=h.specification)


def test_document_tag_resn_duplicate() -> None:
    h = Genealogy()
    h.document_tag('_HIDE', enum_hide)
    with pytest.raises(
        ValueError,
        match=re.escape(Msg.YAML_FILE_HAS_BEEN_USED.format(enum_hide)),
    ):
        h.document_tag('_XHIDE', enum_hide)


# Record Extensions

new = 'tests/data/extension_tests/records/record-_NEW.yml'


def test_record() -> None:
    g = Genealogy()
    g.document_tag('_NEW', new)
    values, keys, labels = g.view_extensions()
    assert values[0][0] == '_NEW'


def test_record_ged() -> None:
    g = Genealogy()
    ext = g.extension_xref('1')
    n = g.document_tag('_NEW', new)
    m = Ext(n, ext, [gc.Name('Jim'), gc.Phon('1234')])
    assert m.ged() == '0 @1@ EXT\n1 NAME Jim\n1 PHON 1234\n'


def test_record_bad_substructure() -> None:
    g = Genealogy()
    ext = g.extension_xref('1')
    n = g.document_tag('_NEW', new)
    m = Ext(n, ext, [gc.Name('Jim'), gc.Phrase('1234')])
    with pytest.raises(
        ValueError,
        match=re.escape(
            "The substructure \"Phrase\" is not in the permitted list ['Email', 'Fax', 'Name', 'Note', 'Phon', 'Refn'] for structure \"Ext\"."
        ),
    ):
        m.ged()


def test_record_missing_required() -> None:
    g = Genealogy()
    ext = g.extension_xref('1')
    n = g.document_tag('_NEW', new)
    m = Ext(n, ext, [gc.Phon('1234')])
    with pytest.raises(
        ValueError,
        match=re.escape(
            'One of the substructures in "[\'Name\']" are missing from the "Ext" structure.'
        ),
    ):
        m.ged()


def test_record_more_than_one_name() -> None:
    g = Genealogy()
    ext = g.extension_xref('1')
    n = g.document_tag('_NEW', new)
    m = Ext(n, ext, [gc.Name('Jim'), gc.Name('John')])
    with pytest.raises(
        ValueError,
        match=re.escape(
            'The substructure "Name" can appear only once in structure "Ext".'
        ),
    ):
        m.ged()


# Structure Extensions

date = 'tests/data/extension_tests/structures/_DATE.yaml'
sour = 'tests/data/extension_tests/structures/_SOUR.yaml'


def test_structure() -> None:
    g = Genealogy()
    g.document_tag('_DATE', date)
    values, keys, labels = g.view_extensions()
    assert values[0][0] == '_DATE'


def test_structure_ged() -> None:
    g = Genealogy()
    d = g.document_tag('_DATE', date)
    m = Ext(d, '1 JAN 2000', [gc.Phrase('test'), gc.Time('01:01:01')])
    assert m.ged() == '1 _DATE 1 JAN 2000\n2 PHRASE test\n2 TIME 01:01:01\n'


def test_structure_sour_ged() -> None:
    g = Genealogy()
    sour_xref = g.source_xref('1')
    sour_tag = g.document_tag('_SOUR', sour)
    m = Ext(sour_tag, sour_xref, [gc.Note('test')])
    assert m.ged() == '1 _SOUR @1@\n2 NOTE test\n'


def test_extension_recognized_by_standard_super() -> None:
    g = Genealogy()
    #repo_xref = g.repository_xref('1')
    sour_xref = g.source_xref('1')
    sour_tag = g.document_tag('_SOUR', sour)
    m = gc.RecordSour(sour_xref, [Ext(sour_tag, sour_xref, [])])
    assert m.ged() == '0 @1@ SOUR\n1 _SOUR @1@\n'


def test_structure_more_than_one_phrase() -> None:
    g = Genealogy()
    n = g.document_tag('_Date', date)
    m = Ext(n, '1 JAN 2000', [gc.Phrase('Jim'), gc.Phrase('John')])
    with pytest.raises(
        ValueError,
        match=re.escape(
            'The substructure "Phrase" can appear only once in structure "Ext".'
        ),
    ):
        m.ged()


def test_structure_date_payload_bad() -> None:
    g = Genealogy()
    n = g.document_tag('_Date', date)
    m = Ext(n, '1 XYZ 2000', [gc.Phrase('John')])
    with pytest.raises(
        ValueError,
        match=re.escape(
            "The value \"1 XYZ 2000\" is not a date period for structure \"Ext\" since the month is not in the list of months ['APR', 'AUG', 'DEC', 'FEB', 'JAN', 'JUL', 'JUN', 'MAR', 'MAY', 'NOV', 'OCT', 'SEP']."
        ),
    ):
        m.ged()
