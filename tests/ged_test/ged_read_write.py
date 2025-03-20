# ged_read_write.py
"""Test reading and writing ged and gdz files."""

from genedata.util import Util


def test_read_ged() -> None:
    # Test constructing the xref_ged test data.
    file = """0 HEAD
1 GEDC
2 VERS 7.0
1 NOTE This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.
0 INDI
1 NOTE This individual has no cross-reference identifier.
0 @I1@ INDI
0 @I@ INDI
0 @1@ INDI
0 @_@ INDI
0 @0XFFFFFFFF@ INDI
0 @THEXREFPRODUCTIONDOESNOTHAVEAMAXIMUMLENGTHSOTHISISATESTOFALONGCROSSREFERENCEIDENTIFIER@ INDI
0 TRLR"""

    file_name: str = 'tests\\ged_test\\xref.ged'
    file_read = Util.read(file_name)
    assert file_read == file