# ged_to_code_xref_test.py
"""Tests for the ged_to_code method."""

from genedata.build import Genealogy

xref_file: str = 'tests/data/ged_examples/xref.ged'

def test_ged_to_code_xref() -> None:
    expected = """# Import the required packages and classes.
import genedata.classes70 as gc
from genedata.build import Genealogy

# Instantiate a Genealogy class.
g = Genealogy()

# Instantiate the cross reference identifiers.
# There were 6 cross reference identifiers.
indi_I1_xref = g.individual_xref('I1')
indi_I_xref = g.individual_xref('I')
indi_1_xref = g.individual_xref('1')
indi___xref = g.individual_xref('_')
indi_0XFFFFFFFF_xref = g.individual_xref('0XFFFFFFFF')
indi_THEXREFPRODUCTIONDOESNOTHAVEAMAXIMUMLENGTHSOTHISISATESTOFALONGCROSSREFERENCEIDENTIFIER_xref = g.individual_xref('THEXREFPRODUCTIONDOESNOTHAVEAMAXIMUMLENGTHSOTHISISATESTOFALONGCROSSREFERENCEIDENTIFIER')

# Instantiate the header record.
header = gc.Head([
    gc.Gedc([
        gc.GedcVers('7.0'),
    ]),
    gc.Note('This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.'),
])

# Instantiate the records holding the GED data.
INDI0 = gc.RecordIndi(Void.INDI, [
    gc.Note('This individual has no cross-reference identifier.'),
])
indi_I1 = gc.RecordIndi(indi_I1_xref)
indi_I = gc.RecordIndi(indi_I_xref)
indi_1 = gc.RecordIndi(indi_1_xref)
indi__ = gc.RecordIndi(indi___xref)
indi_0XFFFFFFFF = gc.RecordIndi(indi_0XFFFFFFFF_xref)
indi_THEXREFPRODUCTIONDOESNOTHAVEAMAXIMUMLENGTHSOTHISISATESTOFALONGCROSSREFERENCEIDENTIFIER = gc.RecordIndi(indi_THEXREFPRODUCTIONDOESNOTHAVEAMAXIMUMLENGTHSOTHISISATESTOFALONGCROSSREFERENCEIDENTIFIER_xref)

# Stage the 8 GEDCOM records to generate the ged lines.
g.stage(header)
g.stage(INDI0)
g.stage(indi_I1)
g.stage(indi_I)
g.stage(indi_1)
g.stage(indi__)
g.stage(indi_0XFFFFFFFF)
g.stage(indi_THEXREFPRODUCTIONDOESNOTHAVEAMAXIMUMLENGTHSOTHISISATESTOFALONGCROSSREFERENCEIDENTIFIER)

# Run the following to show the ged file that the above code would produce.
ged_file = g.show_ged()

# Then print this file to view it.
print(ged_file)
"""
    g = Genealogy(xref_file)
    code = g.ged_to_code()
    assert code == expected