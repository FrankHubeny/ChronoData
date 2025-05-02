# ged_to_code_obje1_test.py
"""Tests for the ged_to_code method."""

from genedata.build import Genealogy

obje_file: str = 'tests/data/ged_examples/obje-1.ged'

def test_ged_to_code_obje1() -> None:
    expected = """# Import the required packages and classes.
import genedata.classes70 as gc
from genedata.build import Genealogy

# Instantiate a Genealogy class.
g = Genealogy()

# Instantiate the cross reference identifiers.
# There were 3 cross reference identifiers.
obje_1_xref = g.multimedia_xref('1')
obje_X1_xref = g.multimedia_xref('X1')
indi_2_xref = g.individual_xref('2')

# Instantiate the header record.
header = gc.Head([
    gc.Gedc([
        gc.GedcVers('7.0'),
    ]),
])

# Instantiate the records holding the GED data.
obje_1 = gc.RecordObje(obje_1_xref, [
    gc.File('example.jpg', [
        gc.Form('image/jpeg', [
            gc.Medi('PHOTO'),
        ]),
        gc.Titl('Example Image File'),
    ]),
    gc.File('example.mp3', [
        gc.Form('application/x-mp3'),
        gc.Titl('Sound Clip'),
    ]),
    gc.Note('note in OBJE record'),
])
obje_X1 = gc.RecordObje(obje_X1_xref, [
    gc.File('gifts.webm', [
        gc.Form('application/x-other', [
            gc.Medi('VIDEO'),
        ]),
    ]),
    gc.File('cake.webm', [
        gc.Form('application/x-other', [
            gc.Medi('VIDEO'),
        ]),
    ]),
    gc.Note('note in OBJE link'),
])
indi_2 = gc.RecordIndi(indi_2_xref, [
    gc.Obje(obje_1_xref),
    gc.Obje(obje_X1_xref, [
        gc.Titl('fifth birthday party'),
    ]),
])

# Stage the 4 GEDCOM records to generate the ged lines.
g.stage(header)
g.stage(obje_1)
g.stage(obje_X1)
g.stage(indi_2)

# Run the following to show the ged file that the above code would produce.
ged_file = g.show_ged()

# Then print this file to view it.
print(ged_file)
"""
    g = Genealogy(obje_file)
    code = g.ged_to_code()
    assert code == expected