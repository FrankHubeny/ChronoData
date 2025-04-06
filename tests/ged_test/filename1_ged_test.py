# filename1_ged_test.py
"""Construct the GEDCOM file """

import genedata.classes70 as gc
from genedata.build import Genealogy
from genedata.constants import Config, Default
from genedata.methods import Util
from genedata.structure import MultimediaXref  # noqa: F401


def test_filename1_ged() -> None:
    # Test constructing the xref_ged test data.

    file = Util.read('tests\\ged_test\\filename-1.ged')
    g = Genealogy('test')
    obje_xref = g.multimedia_xref('1')

    head = gc.Head(
        [
            gc.Gedc(gc.GedcVers(Config.GEDVERSION)), 
            gc.Note('This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.'),
        ]
    )

    obje = gc.RecordObje(
        obje_xref,
        [
            gc.Note('Traditional file URI for a local file with an empty authority, per RFC 8089.'),
            gc.File('file:///unix/absolute', gc.Form('image/bmp')),
            gc.Note('Local file URI with a Windows drive letter, per RFC 8089.'),
            gc.File('file:///c:/windows/absolute', gc.Form('image/bmp')),
            gc.Note('Non-local file URI, per RFC 8089.'),
            gc.File('file://host.example.com/server', gc.Form('image/bmp')),
            gc.Note('URI reference for a local file, per RFC 3986.\nUsing media/ as a directory prefix is recommended but not required.'),
            gc.File('a/relative/path', gc.Form('image/bmp')),
            gc.Note('URI reference with percent escapes in a path segment, per RFC 3986.'),
            gc.File('most/paths%3Fget%23escaped%5Blike%5Dthis', gc.Form('image/bmp')),
            gc.Note('Another URI reference with percent escapes that would be a URI if not escaped, per RFC 3986.'),
            gc.File('https%3a//not.a.url/even-though-similar', gc.Form('image/bmp')),
            gc.Note('Web-accessible file with path and fragment components, per RFC 3986.'),
            gc.File('https://host.example.com?with=args#and-frags', gc.Form('image/bmp')),
            gc.Note("It is recommended that gedcom.ged and MANIFEST.MF and any URL beginning with META-INF/ not be used, but they're not disallowed."),
            gc.File('gedcom.ged', gc.Form('text/vnd.familysearch.gedcom')),
            gc.File('MANIFEST.MF', gc.Form('text/plain')),
            gc.File('META-INF/example', gc.Form('text/plain')),
        ]
    )

    gedcom = ''.join(
        [
            head.ged(), 
            obje.ged(),
            Default.TRAILER,
        ]
    )

    assert file == gedcom

def test_filename1_ged_code() -> None:
    # Test generating code, evaluating it and then finding the ged lines.

    file = Util.read('tests\\ged_test\\filename-1.ged')
    g = Genealogy('test')
    obje_xref = g.multimedia_xref('1')

    head = gc.Head(
        [
            gc.Gedc(gc.GedcVers(Config.GEDVERSION)), 
            gc.Note('This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.'),
        ]
    )

    obje = gc.RecordObje(
        obje_xref,
        [
            gc.Note('Traditional file URI for a local file with an empty authority, per RFC 8089.'),
            gc.File('file:///unix/absolute', gc.Form('image/bmp')),
            gc.Note('Local file URI with a Windows drive letter, per RFC 8089.'),
            gc.File('file:///c:/windows/absolute', gc.Form('image/bmp')),
            gc.Note('Non-local file URI, per RFC 8089.'),
            gc.File('file://host.example.com/server', gc.Form('image/bmp')),
            gc.Note('URI reference for a local file, per RFC 3986.\nUsing media/ as a directory prefix is recommended but not required.'),
            gc.File('a/relative/path', gc.Form('image/bmp')),
            gc.Note('URI reference with percent escapes in a path segment, per RFC 3986.'),
            gc.File('most/paths%3Fget%23escaped%5Blike%5Dthis', gc.Form('image/bmp')),
            gc.Note('Another URI reference with percent escapes that would be a URI if not escaped, per RFC 3986.'),
            gc.File('https%3a//not.a.url/even-though-similar', gc.Form('image/bmp')),
            gc.Note('Web-accessible file with path and fragment components, per RFC 3986.'),
            gc.File('https://host.example.com?with=args#and-frags', gc.Form('image/bmp')),
            gc.Note("It is recommended that gedcom.ged and MANIFEST.MF and any URL beginning with META-INF/ not be used, but they're not disallowed."),
            gc.File('gedcom.ged', gc.Form('text/vnd.familysearch.gedcom')),
            gc.File('MANIFEST.MF', gc.Form('text/plain')),
            gc.File('META-INF/example', gc.Form('text/plain')),
        ]
    )

    gedcom = ''.join(
        [
            eval(head.code(as_name='gc')).ged(), 
            eval(obje.code(as_name='gc')).ged(),
            Default.TRAILER,
        ]
    )

    assert file == gedcom
    