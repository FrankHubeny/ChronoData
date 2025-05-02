# ged_to_code_notes_test.py
"""Tests for the ged_to_code method."""

from genedata.build import Genealogy

notes1_file: str = 'tests/data/ged_examples/notes-1.ged'

def test_ged_to_code_notes1() -> None:
    expected = """# Import the required packages and classes.
import genedata.classes70 as gc
from genedata.build import Genealogy

# Instantiate a Genealogy class.
g = Genealogy()

# Instantiate the cross reference identifiers.
# There were 5 cross reference identifiers.
subm_1_xref = g.submitter_xref('1')
sour_2_xref = g.source_xref('2')
snote_3_xref = g.shared_note_xref('3', 'A single-use note record')
snote_4_xref = g.shared_note_xref('4', 'A dual-use note record')
snote_5_xref = g.shared_note_xref('5', 'A cyclic note record')

# Instantiate the header record.
header = gc.Head([
    gc.HeadSour('conversion test'),
    gc.Subm(subm_1_xref),
    gc.Gedc([
        gc.GedcVers('7.0'),
    ]),
    gc.Note('The header note'),
])

# Instantiate the records holding the GED data.
subm_1 = gc.RecordSubm(subm_1_xref, [
    gc.Name('Luther Tychonievich'),
    gc.Note('An inline submission note'),
    gc.Snote(snote_4_xref),
])
sour_2 = gc.RecordSour(sour_2_xref, [
    gc.Snote(snote_3_xref),
    gc.Snote(snote_4_xref),
    gc.Snote(snote_5_xref),
])
snote_3 = gc.RecordSnote(snote_3_xref, [
    gc.Chan([
        gc.DateExact('25 MAY 2021'),
    ]),
])
snote_4 = gc.RecordSnote(snote_4_xref, [
    gc.Chan([
        gc.DateExact('25 MAY 2021'),
    ]),
])
snote_5 = gc.RecordSnote(snote_5_xref, [
    gc.Sour(sour_2_xref),
])

# Stage the 6 GEDCOM records to generate the ged lines.
g.stage(header)
g.stage(subm_1)
g.stage(sour_2)
g.stage(snote_3)
g.stage(snote_4)
g.stage(snote_5)

# Run the following to show the ged file that the above code would produce.
ged_file = g.show_ged()

# Then print this file to view it.
print(ged_file)
"""
    g = Genealogy(notes1_file)
    code = g.ged_to_code()
    assert code == expected