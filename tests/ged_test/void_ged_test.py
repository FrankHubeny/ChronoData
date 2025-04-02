# void_ged_test.py
"""Construct the Void GEDCOM Example file."""

import genedata.classes7 as gc
from genedata.build import Genealogy
from genedata.constants import Config, Default
from genedata.structure import FamilyXref, IndividualXref, Void  # noqa: F401
from genedata.methods import Util


def test_void_ged() -> None:
    # Test constructing the remarriage1_ged test data.
    file = Util.read('tests\\ged_test\\voidptr.ged')
    g = Genealogy('testing')
    indi1_xref = g.individual_xref('I1')
    indi2_xref = g.individual_xref('I2')
    fam_xref = g.family_xref('F1')

    head = gc.Head(gc.Gedc(gc.GedcVers(Config.GEDVERSION)))

    indi1 = gc.RecordIndi(
        indi1_xref,
        [
            gc.IndiName('John /Smith/'),
            gc.Fams(
                Void.FAM,
                gc.Note(
                    'This tests a case where we want to show that Jane Doe was the 2nd wife.'
                ),
            ),
            gc.Fams(fam_xref),
            gc.IndiFamc(Void.FAM, gc.Pedi('ADOPTED')),
        ],
    )

    indi2 = gc.RecordIndi(
        indi2_xref,
        [
            gc.IndiName('Jane /Doe/'),
            gc.Fams(fam_xref),
        ],
    )

    fam = gc.RecordFam(
        fam_xref,
        [
            gc.FamHusb(indi1_xref),
            gc.FamWife(indi2_xref),
            gc.Chil(Void.INDI),
        ],
    )

    gedcom = ''.join(
        [head.ged(), indi1.ged(), indi2.ged(), fam.ged(), Default.TRAILER]
    )

    assert file == gedcom


def test_void_ged_code() -> None:
    # Test generating code, evaluating it and then finding the ged lines.
    file = Util.read('tests\\ged_test\\voidptr.ged')
    g = Genealogy('testing')
    indi1_xref = g.individual_xref('I1')
    indi2_xref = g.individual_xref('I2')
    fam_xref = g.family_xref('F1')

    head = gc.Head(gc.Gedc(gc.GedcVers(Config.GEDVERSION)))

    indi1 = gc.RecordIndi(
        indi1_xref,
        [
            gc.IndiName('John /Smith/'),
            gc.Fams(
                Void.FAM,
                gc.Note(
                    'This tests a case where we want to show that Jane Doe was the 2nd wife.'
                ),
            ),
            gc.Fams(fam_xref),
            gc.IndiFamc(Void.FAM, gc.Pedi('ADOPTED')),
        ],
    )

    indi2 = gc.RecordIndi(
        indi2_xref,
        [
            gc.IndiName('Jane /Doe/'),
            gc.Fams(fam_xref),
        ],
    )

    fam = gc.RecordFam(
        fam_xref,
        [
            gc.FamHusb(indi1_xref),
            gc.FamWife(indi2_xref),
            gc.Chil(Void.INDI),
        ],
    )

    gedcom = ''.join(
        [
            eval(head.code(as_name='gc')).ged(),
            eval(indi1.code(as_name='gc')).ged(),
            eval(indi2.code(as_name='gc')).ged(),
            eval(fam.code(as_name='gc')).ged(),
            Default.TRAILER,
        ]
    )

    assert file == gedcom
