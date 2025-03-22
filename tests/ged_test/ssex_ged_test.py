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
from genedata.structure import FamilyXref, IndividualXref  # noqa: F401
from genedata.util import Util


def test_ssex_ged() -> None:
    """ Test constructing the same sex marriage_ged test data."""
    file = Util.read('tests\\ged_test\\same-sex-marriage.ged')
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

def test_ssex_ged_code() -> None:
    # Test generating code, evaluating it and then finding the ged lines.
    file = Util.read('tests\\ged_test\\same-sex-marriage.ged')
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
            eval(head.code()).ged(), 
            eval(indi1.code()).ged(),
            eval(indi2.code()).ged(),
            eval(fam.code()).ged(),
            eval(Trlr().code()).ged(),
        ]
    )

    assert file == gedcom