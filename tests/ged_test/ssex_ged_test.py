# ssex_ged_test.py
"""Generate the [Same Sex Marriange GEDCOM Example File](https://gedcom.io/testfiles/gedcom70/same-sex-marriage.ged)."""

from genedata.build import Genealogy
from genedata.classes7 import (
    FamHusb,
    Fams,
    FamWife,
    Gedc,
    GedcVers,
    Head,
    IndiName,
    RecordFam,
    RecordIndi,
    Sex,
    Trlr,
)
from genedata.constants import Config


def test_xref_ged() -> None:
    """ Test constructing the same sex marriage_ged test data."""
    file = """0 HEAD
1 GEDC
2 VERS 7.0
0 @I1@ INDI
1 NAME John /Doe/
1 SEX M
1 FAMS @F1@
0 @I2@ INDI
1 NAME Richard /Roe/
1 SEX M
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
0 TRLR"""

    g = Genealogy('testing')
    indi1_xref = g.individual_xref('I1')
    indi2_xref = g.individual_xref('I2')
    fam_xref = g.family_xref('F1')

    head = Head(Gedc(GedcVers(Config.GEDVERSION)))

    indi1 = RecordIndi(
        indi1_xref,
        [
            IndiName('John /Doe/'),
            Sex('M'),
            Fams(fam_xref),
        ]
    )

    indi2 = RecordIndi(
        indi2_xref,
        [
            IndiName('Richard /Roe/'),
            Sex('M'),
            Fams(fam_xref),
        ],
    )

    fam = RecordFam(
        fam_xref,
        [
            FamHusb(indi1_xref),
            FamWife(indi2_xref),
        ],
    )

    gedcom = ''.join(
        [
            head.ged(), 
            indi1.ged(),
            indi2.ged(),
            fam.ged(),
            Trlr().ged(),
        ]
    )

    assert file == gedcom