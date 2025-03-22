# remarriage1_ged_test.py
"""Generate the Remarriage 1 example gedcom file."""

from genedata.build import Genealogy
from genedata.classes7 import (
    Date,
    Deat,
    Div,
    FamHusb,
    Fams,
    FamWife,
    Gedc,
    GedcVers,
    Head,
    IndiName,
    Marr,
    RecordFam,
    RecordIndi,
    Sex,
    Trlr,
)
from genedata.constants import Config
from genedata.structure import FamilyXref, IndividualXref  # noqa: F401
from genedata.util import Util


def test_remarriage1_ged() -> None:
    # Test constructing the remarriage1_ged test data.
    file = Util.read('tests\\ged_test\\remarriage1.ged')
    g = Genealogy('test')
    indi_i1_xref = g.individual_xref('I1')
    indi_i2_xref = g.individual_xref('I2')
    indi_i3_xref = g.individual_xref('I3')
    fam_f1_xref = g.family_xref('F1')
    fam_f2_xref = g.family_xref('F2')

    head = Head(Gedc(GedcVers(Config.GEDVERSION)))

    indi1 = RecordIndi(
        indi_i1_xref,
        [
            IndiName('John Q /Public/'),
            Sex('M'),
            Fams(fam_f1_xref),
            Fams(fam_f2_xref),
        ],
    )

    indi2 = RecordIndi(
        indi_i2_xref,
        [
            IndiName('Jane /Doe/'),
            Sex('F'),
            Fams(fam_f1_xref),
        ],
    )

    indi3 = RecordIndi(
        indi_i3_xref,
        [
            IndiName('Mary /Roe/'),
            Deat('', Date('1 MAR 1914')),
            Fams(fam_f2_xref),
        ],
    )

    fam1 = RecordFam(
        fam_f1_xref,
        [
            FamHusb(indi_i1_xref),
            FamWife(indi_i2_xref),
            Marr('', Date('1 APR 1911')),
            Div('', Date('2 MAY 1912')),
            Marr('', Date('4 JUL 1914')),
        ],
    )

    fam2 = RecordFam(
        fam_f2_xref,
        [
            FamHusb(indi_i1_xref),
            FamWife(indi_i3_xref),
            Marr('', Date('3 JUN 1913')),
        ],
    )

    gedcom = ''.join(
        [
            head.ged(),
            indi1.ged(),
            indi2.ged(),
            indi3.ged(),
            fam1.ged(),
            fam2.ged(),
            Trlr().ged(),
        ]
    )

    assert file == gedcom


def test_remarriage1_ged_code() -> None:
    # Test generating code, evaluating it and then finding the ged lines.
    file = Util.read('tests\\ged_test\\remarriage1.ged')
    g = Genealogy('test')
    indi_i1_xref = g.individual_xref('I1')
    indi_i2_xref = g.individual_xref('I2')
    indi_i3_xref = g.individual_xref('I3')
    fam_f1_xref = g.family_xref('F1')
    fam_f2_xref = g.family_xref('F2')

    head = Head(Gedc(GedcVers(Config.GEDVERSION)))

    indi1 = RecordIndi(
        indi_i1_xref,
        [
            IndiName('John Q /Public/'),
            Sex('M'),
            Fams(fam_f1_xref),
            Fams(fam_f2_xref),
        ],
    )

    indi2 = RecordIndi(
        indi_i2_xref,
        [
            IndiName('Jane /Doe/'),
            Sex('F'),
            Fams(fam_f1_xref),
        ],
    )

    indi3 = RecordIndi(
        indi_i3_xref,
        [
            IndiName('Mary /Roe/'),
            Deat('', Date('1 MAR 1914')),
            Fams(fam_f2_xref),
        ],
    )

    fam1 = RecordFam(
        fam_f1_xref,
        [
            FamHusb(indi_i1_xref),
            FamWife(indi_i2_xref),
            Marr('', Date('1 APR 1911')),
            Div('', Date('2 MAY 1912')),
            Marr('', Date('4 JUL 1914')),
        ],
    )

    fam2 = RecordFam(
        fam_f2_xref,
        [
            FamHusb(indi_i1_xref),
            FamWife(indi_i3_xref),
            Marr('', Date('3 JUN 1913')),
        ],
    )

    gedcom = ''.join(
        [
            eval(head.code()).ged(),
            eval(indi1.code()).ged(),
            eval(indi2.code()).ged(),
            eval(indi3.code()).ged(),
            eval(fam1.code()).ged(),
            eval(fam2.code()).ged(),
            eval(Trlr().code()).ged(),
        ]
    )

    assert file == gedcom
