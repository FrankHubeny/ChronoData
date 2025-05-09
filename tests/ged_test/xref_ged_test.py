# xref_ged_test.py
"""Reproduce the `xref.ged` output.

Reference:
    [GEDCOM Age test file](https://gedcom.io/testfiles/gedcom70/xref.ged)
"""

import genedata.classes70 as gc
from genedata.build import Genealogy
from genedata.constants import Default
from genedata.methods import Util
from genedata.structure import IndividualXref, Void  # noqa: F401

ged_version: str = '7.0'

def test_xref_ged() -> None:
    # Test constructing the xref_ged test data.
    file = Util.read('tests/data/ged_examples/xref.ged')

    g = Genealogy(version=ged_version)

    head = gc.Head(
        [
            gc.Gedc(gc.GedcVers('7.0')),
            gc.Note(
                'This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.'
            ),
        ]
    )

    indi4_xref = g.individual_xref('1')
    indi4 = gc.RecordIndi(indi4_xref)
    indi1 = gc.RecordIndi(
        Void.INDI, gc.Note('This individual has no cross-reference identifier.')
    )
    indi2_xref = g.individual_xref('I', True)
    indi2 = gc.RecordIndi(indi2_xref)
    indi3_xref = g.individual_xref('I')
    indi3 = gc.RecordIndi(indi3_xref)
    indi5_xref = g.individual_xref('_')
    indi5 = gc.RecordIndi(indi5_xref)
    indi6_xref = g.individual_xref('0XFFFFFFFF')
    indi6 = gc.RecordIndi(indi6_xref)
    indi7_xref = g.individual_xref(
        'THEXREFPRODUCTIONDOESNOTHAVEAMAXIMUMLENGTHSOTHISISATESTOFALONGCROSSREFERENCEIDENTIFIER'
    )
    indi7 = gc.RecordIndi(indi7_xref)

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
            Default.TRAILER,
        ]
    )

    assert file == gedcom


