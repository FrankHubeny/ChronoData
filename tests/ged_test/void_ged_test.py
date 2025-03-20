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
from genedata.structure import Void


def test_void_ged() -> None:
    # Test constructing the remarriage1_ged test data.

    file = """0 HEAD
1 GEDC
2 VERS 7.0
0 @I1@ INDI
1 NAME John /Smith/
1 FAMS @VOID@
2 NOTE This tests a case where we want to show that Jane Doe was the 2nd wife.
1 FAMS @F1@
1 FAMC @VOID@
2 PEDI ADOPTED
0 @I2@ INDI
1 NAME Jane /Doe/
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 CHIL @VOID@
0 TRLR"""

    g = Genealogy('testing')
    indi1_xref = g.individual_xref('I1')
    indi2_xref = g.individual_xref('I2')
    fam_xref = g.family_xref('F1')

    head = Head(Gedc(GedcVers(Config.GEDVERSION)))

    indi1 = RecordIndi(
        indi1_xref,
        [
            IndiName('John /Smith/'),
            Fams(Void.FAM,Note('This tests a case where we want to show that Jane Doe was the 2nd wife.')),
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
        ]
    )

    gedcom = ''.join([head.ged(), indi1.ged(), indi2.ged(), fam.ged(), Trlr().ged()])

    assert file == gedcom