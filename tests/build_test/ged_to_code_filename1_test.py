# ged_to_code_filename1_test.py
"""Tests for the ged_to_code method."""

from genedata.build import Genealogy

filename1_file: str = 'tests/data/ged_examples/filename-1.ged'

def test_ged_to_code_filename1() -> None:
    expected = """# Import the required packages and classes.
import genedata.classes70 as gc
from genedata.build import Genealogy

# Instantiate a Genealogy class.
g = Genealogy()

# Instantiate the cross reference identifiers.
# There were 1 cross reference identifiers.
obje_1_xref = g.multimedia_xref('1')

# Instantiate the header record.
header = gc.Head([
    gc.Gedc([
        gc.GedcVers('7.0'),
    ]),
    gc.Note('This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.'),
])

# Instantiate the records holding the GED data.
obje_1 = gc.RecordObje(obje_1_xref, [
    gc.Note('Traditional file URI for a local file with an empty authority, per RFC 8089.'),
    gc.File('file:///unix/absolute', [
        gc.Form('image/bmp'),
    ]),
    gc.Note('Local file URI with a Windows drive letter, per RFC 8089.'),
    gc.File('file:///c:/windows/absolute', [
        gc.Form('image/bmp'),
    ]),
    gc.Note('Non-local file URI, per RFC 8089.'),
    gc.File('file://host.example.com/server', [
        gc.Form('image/bmp'),
    ]),
    gc.Note('''URI reference for a local file, per RFC 3986.
Using media/ as a directory prefix is recommended but not required.'''),
    gc.File('a/relative/path', [
        gc.Form('image/bmp'),
    ]),
    gc.Note('URI reference with percent escapes in a path segment, per RFC 3986.'),
    gc.File('most/paths%3Fget%23escaped%5Blike%5Dthis', [
        gc.Form('image/bmp'),
    ]),
    gc.Note('Another URI reference with percent escapes that would be a URI if not escaped, per RFC 3986.'),
    gc.File('https%3a//not.a.url/even-though-similar', [
        gc.Form('image/bmp'),
    ]),
    gc.Note('Web-accessible file with path and fragment components, per RFC 3986.'),
    gc.File('https://host.example.com?with=args#and-frags', [
        gc.Form('image/bmp'),
    ]),
    gc.Note("It is recommended that gedcom.ged and MANIFEST.MF and any URL beginning with META-INF/ not be used, but they're not disallowed."),
    gc.File('gedcom.ged', [
        gc.Form('text/vnd.familysearch.gedcom'),
    ]),
    gc.File('MANIFEST.MF', [
        gc.Form('text/plain'),
    ]),
    gc.File('META-INF/example', [
        gc.Form('text/plain'),
    ]),
])

# Stage the 2 GEDCOM records to generate the ged lines.
g.stage(header)
g.stage(obje_1)

# Run the following to show the ged file that the above code would produce.
ged_file = g.show_ged()

# Then print this file to view it.
print(ged_file)
"""
    g = Genealogy(filename1_file)
    code = g.ged_to_code()
    assert code == expected
    