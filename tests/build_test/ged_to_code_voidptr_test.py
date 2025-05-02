# ged_to_code_voidptr_test.py
"""Tests for the ged_to_code method."""

from genedata.build import Genealogy

voidptr_file: str = 'tests/data/ged_examples/voidptr.ged'

def test_ged_to_code_voidptr() -> None:
    expected = """# Import the required packages and classes.
import genedata.classes70 as gc
from genedata.build import Genealogy
from genedata.structure import Void

# Instantiate a Genealogy class.
g = Genealogy()

# Instantiate the cross reference identifiers.
# There were 3 cross reference identifiers.
indi_I1_xref = g.individual_xref('I1')
indi_I2_xref = g.individual_xref('I2')
fam_F1_xref = g.family_xref('F1')

# Instantiate the header record.
header = gc.Head([
    gc.Gedc([
        gc.GedcVers('7.0'),
    ]),
])

# Instantiate the records holding the GED data.
indi_I1 = gc.RecordIndi(indi_I1_xref, [
    gc.IndiName('John /Smith/'),
    gc.Fams(Void.FAM, [
        gc.Note('This tests a case where we want to show that Jane Doe was the 2nd wife.'),
    ]),
    gc.Fams(fam_F1_xref),
    gc.IndiFamc(Void.FAM, [
        gc.Pedi('ADOPTED'),
    ]),
])
indi_I2 = gc.RecordIndi(indi_I2_xref, [
    gc.IndiName('Jane /Doe/'),
    gc.Fams(fam_F1_xref),
])
fam_F1 = gc.RecordFam(fam_F1_xref, [
    gc.FamHusb(indi_I1_xref),
    gc.FamWife(indi_I2_xref),
    gc.Chil(Void.INDI),
])

# Stage the 4 GEDCOM records to generate the ged lines.
g.stage(header)
g.stage(indi_I1)
g.stage(indi_I2)
g.stage(fam_F1)

# Run the following to show the ged file that the above code would produce.
ged_file = g.show_ged()

# Then print this file to view it.
print(ged_file)
"""
    g = Genealogy(voidptr_file)
    code = g.ged_to_code()
    assert code == expected
    