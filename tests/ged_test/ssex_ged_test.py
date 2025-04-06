# ssex_ged_test.py
"""Generate the [Same Sex Marriange GEDCOM Example File](https://gedcom.io/testfiles/gedcom70/same-sex-marriage.ged)."""

import genedata.classes70 as gc
from genedata.build import Genealogy
from genedata.constants import Config, Default
from genedata.structure import FamilyXref, IndividualXref  # noqa: F401
from genedata.methods import Util


def test_ssex_ged() -> None:
    """ Test constructing the same sex marriage_ged test data."""
    file = Util.read('tests\\ged_test\\same-sex-marriage.ged')
    g = Genealogy('testing')
    indi1_xref = g.individual_xref('I1')
    indi2_xref = g.individual_xref('I2')
    fam_xref = g.family_xref('F1')

    head = gc.Head(gc.Gedc(gc.GedcVers(Config.GEDVERSION)))

    indi1 = gc.RecordIndi(
        indi1_xref,
        [
            gc.IndiName('John /Doe/'),
            gc.Sex('M'),
            gc.Fams(fam_xref),
        ]
    )

    indi2 = gc.RecordIndi(
        indi2_xref,
        [
            gc.IndiName('Richard /Roe/'),
            gc.Sex('M'),
            gc.Fams(fam_xref),
        ],
    )

    fam = gc.RecordFam(
        fam_xref,
        [
            gc.FamHusb(indi1_xref),
            gc.FamWife(indi2_xref),
        ],
    )

    gedcom = ''.join(
        [
            head.ged(), 
            indi1.ged(),
            indi2.ged(),
            fam.ged(),
            Default.TRAILER,
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

    head = gc.Head(gc.Gedc(gc.GedcVers(Config.GEDVERSION)))

    indi1 = gc.RecordIndi(
        indi1_xref,
        [
            gc.IndiName('John /Doe/'),
            gc.Sex('M'),
            gc.Fams(fam_xref),
        ]
    )

    indi2 = gc.RecordIndi(
        indi2_xref,
        [
            gc.IndiName('Richard /Roe/'),
            gc.Sex('M'),
            gc.Fams(fam_xref),
        ],
    )

    fam = gc.RecordFam(
        fam_xref,
        [
            gc.FamHusb(indi1_xref),
            gc.FamWife(indi2_xref),
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