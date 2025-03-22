# xref_ged_test.py
"""Reproduce the `xref.ged` output.

Reference:
    [GEDCOM Age test file](https://gedcom.io/testfiles/gedcom70/xref.ged)
"""

from genedata.build import Genealogy
from genedata.classes7 import (
    Gedc,
    GedcVers,
    Head,
    Note,
    RecordIndi,
    Trlr,
)
from genedata.constants import Config
from genedata.structure import IndividualXref, Void  # noqa: F401
from genedata.util import Util


def test_xref_ged() -> None:
    # Test constructing the xref_ged test data.
    file = Util.read('tests\\ged_test\\xref.ged')

    g = Genealogy('test')

    head = Head(
        [
            Gedc(GedcVers(Config.GEDVERSION)),
            Note(
                'This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.'
            ),
        ]
    )

    indi4_xref = g.individual_xref('1')
    indi4 = RecordIndi(indi4_xref)
    indi1 = RecordIndi(
        Void.INDI, Note('This individual has no cross-reference identifier.')
    )
    indi2_xref = g.individual_xref('I', True)
    indi2 = RecordIndi(indi2_xref)
    indi3_xref = g.individual_xref('I')
    indi3 = RecordIndi(indi3_xref)
    indi5_xref = g.individual_xref('_')
    indi5 = RecordIndi(indi5_xref)
    indi6_xref = g.individual_xref('0XFFFFFFFF')
    indi6 = RecordIndi(indi6_xref)
    indi7_xref = g.individual_xref(
        'THEXREFPRODUCTIONDOESNOTHAVEAMAXIMUMLENGTHSOTHISISATESTOFALONGCROSSREFERENCEIDENTIFIER'
    )
    indi7 = RecordIndi(indi7_xref)

    gedcom = ''.join(
        [
            head.ged(),
            indi1.ged(),
            indi2.ged(),
            indi3.ged(),
            indi4.ged(),
            indi5.ged(),
            indi6.ged(),
            indi7.ged(),
            Trlr().ged(),
        ]
    )

    assert file == gedcom


def test_xref_ged_code() -> None:
    # Test generating code, evaluating it and then finding the ged lines.
    file = Util.read('tests\\ged_test\\xref.ged')

    g = Genealogy('test')

    head = Head(
        [
            Gedc(GedcVers(Config.GEDVERSION)),
            Note(
                'This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.'
            ),
        ]
    )

    indi4_xref = g.individual_xref('1')
    indi4 = RecordIndi(indi4_xref)
    indi1 = RecordIndi(
        Void.INDI, Note('This individual has no cross-reference identifier.')
    )
    indi2_xref = g.individual_xref('I', True)
    indi2 = RecordIndi(indi2_xref)
    indi3_xref = g.individual_xref('I')
    indi3 = RecordIndi(indi3_xref)
    indi5_xref = g.individual_xref('_')
    indi5 = RecordIndi(indi5_xref)
    indi6_xref = g.individual_xref('0XFFFFFFFF')
    indi6 = RecordIndi(indi6_xref)
    indi7_xref = g.individual_xref(
        'THEXREFPRODUCTIONDOESNOTHAVEAMAXIMUMLENGTHSOTHISISATESTOFALONGCROSSREFERENCEIDENTIFIER'
    )
    indi7 = RecordIndi(indi7_xref)

    gedcom = ''.join(
        [
            eval(head.code()).ged(),
            eval(indi1.code()).ged(),
            eval(indi2.code()).ged(),
            eval(indi3.code()).ged(),
            eval(indi4.code()).ged(),
            eval(indi5.code()).ged(),
            eval(indi6.code()).ged(),
            eval(indi7.code()).ged(),
            eval(Trlr().code()).ged(),
        ]
    )

    assert file == gedcom
