# ged_read_write.py
"""Test reading and writing ged and gdz files."""

from genedata.constants import Default
from genedata.methods import Util


def test_read_ged() -> None:
    # Test reading a ged file comparing it to the its expected contents.
    ged = """0 HEAD
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
    assert file_read == ged


def test_list_gdz() -> None:
    # Test listing the contents of a gdz archive file.
    file_read: str = Default.EMPTY
    gdz_path: str = 'tests\\ged_test\\minimal70.gdz'
    file_read = Util.list_gdz(gdz_path)
    assert file_read == 'gedcom.ged\n'


def test_read_gdz_ged() -> None:
    # Test reading a ged file from a gdz archive file and comparing it to a string.
    ged = """0 HEAD
1 GEDC
2 VERS 7.0
0 TRLR
"""

    gdz_path: str = 'tests\\ged_test\\minimal70.gdz'
    file_name = 'gedcom.ged'
    file_read = Util.read_gdz_ged_file(file_name, gdz_path)
    assert file_read == ged


def test_write_ged() -> None:
    # Test writing a ged string as a file and then reading the file and comparing it to the string.
    ged = """0 HEAD
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

    file_name: str = 'tests\\ged_test\\ged_written.ged'
    Util.write_ged(ged, file_name)
    file_read = Util.read(file_name)
    assert file_read == ged
