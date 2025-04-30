# ged_to_code_test.py
"""Tests for the ged_to_code method."""

import pytest

from genedata.build import Genealogy
from genedata.classes70 import Head
from genedata.messages import Msg
from genedata.methods import Util

minimal_file: str = 'tests\\ged_test\\minimal70.ged'
obje_file: str = 'tests\\ged_test\\obje-1.ged'

def test_ged_to_code_minimal() -> None:
    expected = """# Import the required packages and classes.
import genedata.classes70 as gc
from genedata.build import Genealogy

# Instantiate a Genealogy class.
g = Genealogy()

# Instantiate the cross reference identifiers.
# There were no cross reference identifiers.

# Instantiate the header record.
header = gc.Head([
    gc.Gedc([
        gc.GedcVers('7.0'),
    ]),
])

# Instantiate the records holding the GED data.
# There were no records outside of the header record.

# Stage the 1 GEDCOM records to generate the ged lines.
g.stage(header)

# Run the following to show the ged file that the above code would produce.
ged_file = g.show_ged()

# Then print this file to view it.
print(ged_file)
"""
    g = Genealogy(minimal_file)
    code = g.ged_to_code()
    assert code == expected

