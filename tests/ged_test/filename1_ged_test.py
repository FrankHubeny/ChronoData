# filename1_ged_test.py
"""Construct the GEDCOM file """

from genedata.build import Genealogy
from genedata.classes7 import (
    File,
    Form,
    Gedc,
    GedcVers,
    Head,
    Note,
    RecordObje,
    Trlr,
)
from genedata.constants import Config
from genedata.structure import MultimediaXref  # noqa: F401
from genedata.util import Util


def test_filename1_ged() -> None:
    # Test constructing the xref_ged test data.

    file = Util.read('tests\\ged_test\\filename-1.ged')
    g = Genealogy('test')
    obje_xref = g.multimedia_xref('1')

    head = Head(
        [
            Gedc(GedcVers(Config.GEDVERSION)), 
            Note('This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.'),
        ]
    )

    obje = RecordObje(
        obje_xref,
        [
            Note('Traditional file URI for a local file with an empty authority, per RFC 8089.'),
            File('file:///unix/absolute', Form('image/bmp')),
            Note('Local file URI with a Windows drive letter, per RFC 8089.'),
            File('file:///c:/windows/absolute', Form('image/bmp')),
            Note('Non-local file URI, per RFC 8089.'),
            File('file://host.example.com/server', Form('image/bmp')),
            Note('URI reference for a local file, per RFC 3986.\nUsing media/ as a directory prefix is recommended but not required.'),
            File('a/relative/path', Form('image/bmp')),
            Note('URI reference with percent escapes in a path segment, per RFC 3986.'),
            File('most/paths%3Fget%23escaped%5Blike%5Dthis', Form('image/bmp')),
            Note('Another URI reference with percent escapes that would be a URI if not escaped, per RFC 3986.'),
            File('https%3a//not.a.url/even-though-similar', Form('image/bmp')),
            Note('Web-accessible file with path and fragment components, per RFC 3986.'),
            File('https://host.example.com?with=args#and-frags', Form('image/bmp')),
            Note("It is recommended that gedcom.ged and MANIFEST.MF and any URL beginning with META-INF/ not be used, but they're not disallowed."),
            File('gedcom.ged', Form('text/vnd.familysearch.gedcom')),
            File('MANIFEST.MF', Form('text/plain')),
            File('META-INF/example', Form('text/plain')),
        ]
    )

    gedcom = ''.join(
        [
            head.ged(), 
            obje.ged(),
            Trlr().ged()
        ]
    )

    assert file == gedcom

def test_filename1_ged_code() -> None:
    # Test generating code, evaluating it and then finding the ged lines.

    file = Util.read('tests\\ged_test\\filename-1.ged')
    g = Genealogy('test')
    obje_xref = g.multimedia_xref('1')

    head = Head(
        [
            Gedc(GedcVers(Config.GEDVERSION)), 
            Note('This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.'),
        ]
    )

    obje = RecordObje(
        obje_xref,
        [
            Note('Traditional file URI for a local file with an empty authority, per RFC 8089.'),
            File('file:///unix/absolute', Form('image/bmp')),
            Note('Local file URI with a Windows drive letter, per RFC 8089.'),
            File('file:///c:/windows/absolute', Form('image/bmp')),
            Note('Non-local file URI, per RFC 8089.'),
            File('file://host.example.com/server', Form('image/bmp')),
            Note('URI reference for a local file, per RFC 3986.\nUsing media/ as a directory prefix is recommended but not required.'),
            File('a/relative/path', Form('image/bmp')),
            Note('URI reference with percent escapes in a path segment, per RFC 3986.'),
            File('most/paths%3Fget%23escaped%5Blike%5Dthis', Form('image/bmp')),
            Note('Another URI reference with percent escapes that would be a URI if not escaped, per RFC 3986.'),
            File('https%3a//not.a.url/even-though-similar', Form('image/bmp')),
            Note('Web-accessible file with path and fragment components, per RFC 3986.'),
            File('https://host.example.com?with=args#and-frags', Form('image/bmp')),
            Note("It is recommended that gedcom.ged and MANIFEST.MF and any URL beginning with META-INF/ not be used, but they're not disallowed."),
            File('gedcom.ged', Form('text/vnd.familysearch.gedcom')),
            File('MANIFEST.MF', Form('text/plain')),
            File('META-INF/example', Form('text/plain')),
        ]
    )

    gedcom = ''.join(
        [
            eval(head.code()).ged(), 
            eval(obje.code()).ged(),
            eval(Trlr().code()).ged()
        ]
    )

    assert file == gedcom
    