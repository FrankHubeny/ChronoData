# void_ged_test.py
"""Construct the Void GEDCOM Example file."""

from genedata.build import Genealogy
from genedata.classes7 import (
    Chil,
    FamHusb,
    Fams,
    FamWife,
    Gedc,
    GedcVers,
    Head,
    IndiFamc,
    IndiName,
    Note,
    Pedi,
    RecordFam,
    RecordIndi,
    Trlr,
)
from genedata.constants import Config
from genedata.structure import FamilyXref, IndividualXref, Void  # noqa: F401
from genedata.util import Util


def test_void_ged() -> None:
    # Test constructing the remarriage1_ged test data.
    file = Util.read('tests\\ged_test\\voidptr.ged')
    g = Genealogy('testing')
    indi1_xref = g.individual_xref('I1')
    indi2_xref = g.individual_xref('I2')
    fam_xref = g.family_xref('F1')

    head = Head(Gedc(GedcVers(Config.GEDVERSION)))

    indi1 = RecordIndi(
        indi1_xref,
        [
            IndiName('John /Smith/'),
            Fams(
                Void.FAM,
                Note(
                    'This tests a case where we want to show that Jane Doe was the 2nd wife.'
                ),
            ),
            Fams(fam_xref),
            IndiFamc(Void.FAM, Pedi('ADOPTED')),
        ],
    )

    indi2 = RecordIndi(
        indi2_xref,
        [
            IndiName('Jane /Doe/'),
            Fams(fam_xref),
        ],
    )

    fam = RecordFam(
        fam_xref,
        [
            FamHusb(indi1_xref),
            FamWife(indi2_xref),
            Chil(Void.INDI),
        ],
    )

    gedcom = ''.join(
        [head.ged(), indi1.ged(), indi2.ged(), fam.ged(), Trlr().ged()]
    )

    assert file == gedcom


def test_void_ged_code() -> None:
    # Test generating code, evaluating it and then finding the ged lines.
    file = Util.read('tests\\ged_test\\voidptr.ged')
    g = Genealogy('testing')
    indi1_xref = g.individual_xref('I1')
    indi2_xref = g.individual_xref('I2')
    fam_xref = g.family_xref('F1')

    head = Head(Gedc(GedcVers(Config.GEDVERSION)))

    indi1 = RecordIndi(
        indi1_xref,
        [
            IndiName('John /Smith/'),
            Fams(
                Void.FAM,
                Note(
                    'This tests a case where we want to show that Jane Doe was the 2nd wife.'
                ),
            ),
            Fams(fam_xref),
            IndiFamc(Void.FAM, Pedi('ADOPTED')),
        ],
    )

    indi2 = RecordIndi(
        indi2_xref,
        [
            IndiName('Jane /Doe/'),
            Fams(fam_xref),
        ],
    )

    fam = RecordFam(
        fam_xref,
        [
            FamHusb(indi1_xref),
            FamWife(indi2_xref),
            Chil(Void.INDI),
        ],
    )

    gedcom = ''.join(
        [
            eval(head.code()).ged(),
            eval(indi1.code()).ged(),
            eval(indi2.code()).ged(),
            eval(fam.code()).ged(),
            eval(Trlr().code()).ged(),
        ]
    )

    assert file == gedcom
