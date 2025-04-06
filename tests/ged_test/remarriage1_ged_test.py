# remarriage1_ged_test.py
"""Generate the Remarriage 1 example gedcom file."""

import genedata.classes70 as gc
from genedata.build import Genealogy
from genedata.constants import Config, Default
from genedata.structure import FamilyXref, IndividualXref  # noqa: F401
from genedata.methods import Util


def test_remarriage1_ged() -> None:
    # Test constructing the remarriage1_ged test data.
    file = Util.read('tests\\ged_test\\remarriage1.ged')
    g = Genealogy('test')
    indi_i1_xref = g.individual_xref('I1')
    indi_i2_xref = g.individual_xref('I2')
    indi_i3_xref = g.individual_xref('I3')
    fam_f1_xref = g.family_xref('F1')
    fam_f2_xref = g.family_xref('F2')

    head = gc.Head(gc.Gedc(gc.GedcVers(Config.GEDVERSION)))

    indi1 = gc.RecordIndi(
        indi_i1_xref,
        [
            gc.IndiName('John Q /Public/'),
            gc.Sex('M'),
            gc.Fams(fam_f1_xref),
            gc.Fams(fam_f2_xref),
        ],
    )

    indi2 = gc.RecordIndi(
        indi_i2_xref,
        [
            gc.IndiName('Jane /Doe/'),
            gc.Sex('F'),
            gc.Fams(fam_f1_xref),
        ],
    )

    indi3 = gc.RecordIndi(
        indi_i3_xref,
        [
            gc.IndiName('Mary /Roe/'),
            gc.Deat('', gc.Date('1 MAR 1914')),
            gc.Fams(fam_f2_xref),
        ],
    )

    fam1 = gc.RecordFam(
        fam_f1_xref,
        [
            gc.FamHusb(indi_i1_xref),
            gc.FamWife(indi_i2_xref),
            gc.Marr('', gc.Date('1 APR 1911')),
            gc.Div('', gc.Date('2 MAY 1912')),
            gc.Marr('', gc.Date('4 JUL 1914')),
        ],
    )

    fam2 = gc.RecordFam(
        fam_f2_xref,
        [
            gc.FamHusb(indi_i1_xref),
            gc.FamWife(indi_i3_xref),
            gc.Marr('', gc.Date('3 JUN 1913')),
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
            Default.TRAILER,
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

    head = gc.Head(gc.Gedc(gc.GedcVers(Config.GEDVERSION)))

    indi1 = gc.RecordIndi(
        indi_i1_xref,
        [
            gc.IndiName('John Q /Public/'),
            gc.Sex('M'),
            gc.Fams(fam_f1_xref),
            gc.Fams(fam_f2_xref),
        ],
    )

    indi2 = gc.RecordIndi(
        indi_i2_xref,
        [
            gc.IndiName('Jane /Doe/'),
            gc.Sex('F'),
            gc.Fams(fam_f1_xref),
        ],
    )

    indi3 = gc.RecordIndi(
        indi_i3_xref,
        [
            gc.IndiName('Mary /Roe/'),
            gc.Deat('', gc.Date('1 MAR 1914')),
            gc.Fams(fam_f2_xref),
        ],
    )

    fam1 = gc.RecordFam(
        fam_f1_xref,
        [
            gc.FamHusb(indi_i1_xref),
            gc.FamWife(indi_i2_xref),
            gc.Marr('', gc.Date('1 APR 1911')),
            gc.Div('', gc.Date('2 MAY 1912')),
            gc.Marr('', gc.Date('4 JUL 1914')),
        ],
    )

    fam2 = gc.RecordFam(
        fam_f2_xref,
        [
            gc.FamHusb(indi_i1_xref),
            gc.FamWife(indi_i3_xref),
            gc.Marr('', gc.Date('3 JUN 1913')),
        ],
    )

    gedcom = ''.join(
        [
            eval(head.code(as_name='gc')).ged(),
            eval(indi1.code(as_name='gc')).ged(),
            eval(indi2.code(as_name='gc')).ged(),
            eval(indi3.code(as_name='gc')).ged(),
            eval(fam1.code(as_name='gc')).ged(),
            eval(fam2.code(as_name='gc')).ged(),
            Default.TRAILER,
        ]
    )

    assert file == gedcom
