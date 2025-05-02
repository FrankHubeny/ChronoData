# ged_to_code_remarriage1_test.py
"""Tests for the ged_to_code method."""

from genedata.build import Genealogy

remarriage1_file: str = 'tests/data/ged_examples/remarriage1.ged'

def test_ged_to_code_remarriage1() -> None:
    expected = """# Import the required packages and classes.
import genedata.classes70 as gc
from genedata.build import Genealogy

# Instantiate a Genealogy class.
g = Genealogy()

# Instantiate the cross reference identifiers.
# There were 5 cross reference identifiers.
indi_I1_xref = g.individual_xref('I1')
indi_I2_xref = g.individual_xref('I2')
indi_I3_xref = g.individual_xref('I3')
fam_F1_xref = g.family_xref('F1')
fam_F2_xref = g.family_xref('F2')

# Instantiate the header record.
header = gc.Head([
    gc.Gedc([
        gc.GedcVers('7.0'),
    ]),
])

# Instantiate the records holding the GED data.
indi_I1 = gc.RecordIndi(indi_I1_xref, [
    gc.IndiName('John Q /Public/'),
    gc.Sex('M'),
    gc.Fams(fam_F1_xref),
    gc.Fams(fam_F2_xref),
])
indi_I2 = gc.RecordIndi(indi_I2_xref, [
    gc.IndiName('Jane /Doe/'),
    gc.Sex('F'),
    gc.Fams(fam_F1_xref),
])
indi_I3 = gc.RecordIndi(indi_I3_xref, [
    gc.IndiName('Mary /Roe/'),
    gc.Deat('', [
        gc.Date('1 MAR 1914'),
    ]),
    gc.Fams(fam_F2_xref),
])
fam_F1 = gc.RecordFam(fam_F1_xref, [
    gc.FamHusb(indi_I1_xref),
    gc.FamWife(indi_I2_xref),
    gc.Marr('', [
        gc.Date('1 APR 1911'),
    ]),
    gc.Div('', [
        gc.Date('2 MAY 1912'),
    ]),
    gc.Marr('', [
        gc.Date('4 JUL 1914'),
    ]),
])
fam_F2 = gc.RecordFam(fam_F2_xref, [
    gc.FamHusb(indi_I1_xref),
    gc.FamWife(indi_I3_xref),
    gc.Marr('', [
        gc.Date('3 JUN 1913'),
    ]),
])

# Stage the 6 GEDCOM records to generate the ged lines.
g.stage(header)
g.stage(indi_I1)
g.stage(indi_I2)
g.stage(indi_I3)
g.stage(fam_F1)
g.stage(fam_F2)

# Run the following to show the ged file that the above code would produce.
ged_file = g.show_ged()

# Then print this file to view it.
print(ged_file)
"""
    g = Genealogy(remarriage1_file)
    code = g.ged_to_code()
    assert code == expected