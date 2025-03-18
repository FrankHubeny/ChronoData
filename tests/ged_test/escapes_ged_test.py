# escapes_ged_test.py
"""Reproduce the `escapes.ged` output.

Reference:
    [GEDCOM Escapes test file](https://gedcom.io/testfiles/gedcom70/escapes.ged)
"""

from genedata.build import Genealogy
from genedata.classes7 import (
    Gedc,
    GedcVers,
    Head,
    IndiName,
    Note,
    RecordIndi,
    RecordSnote,
    Trlr,
)
from genedata.constants import Config


def test_escape_ged() -> None:
    # Test constructing the escapes.ged test data.
    g = Genealogy('test')
    indi_xref = g.individual_xref('I1')
    sn1_xref = g.shared_note_xref('N01', '@ one leading')
    sn2_xref = g.shared_note_xref('N02', '@one leading no space')
    sn5_xref = g.shared_note_xref(
        'N05', 'doubled @@ internal has two @ characters, not escaped'
    )
    sn6_xref = g.shared_note_xref('N06', 'doubled@@internal no space')
    sn7_xref = g.shared_note_xref('N07', 'single @ internal')
    sn8_xref = g.shared_note_xref('N08', 'single@internal no space')
    sn19_xref = g.shared_note_xref(
        'N19',
        """@ at at front and @ inside line and
@ at after CONT and @ inside CONT's line too.""",
    )

    head = Head(
        [
            Gedc(GedcVers(Config.GEDVERSION)),
            Note(
                'This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.'
            ),
        ]
    )

    indi = RecordIndi(
        indi_xref,
        [
            IndiName('John /Doe/'),
            Note("""me@example.com is an example email address.
@me and @I are example social media handles.
@@@@ has four @ characters where only the first is escaped."""),
        ],
    )

    gedcom = ''.join(
        [
            head.ged(),
            indi.ged(),
            RecordSnote(sn1_xref).ged(),
            RecordSnote(sn2_xref).ged(),
            RecordSnote(sn5_xref).ged(),
            RecordSnote(sn6_xref).ged(),
            RecordSnote(sn7_xref).ged(),
            RecordSnote(sn8_xref).ged(),
            RecordSnote(sn19_xref).ged(),
            Trlr().ged(),
        ]
    )

    assert (
        gedcom
        == """0 HEAD
1 GEDC
2 VERS 7.0
1 NOTE This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.
0 @I1@ INDI
1 NAME John /Doe/
1 NOTE me@example.com is an example email address.
2 CONT @@me and @I are example social media handles.
2 CONT @@@@@ has four @ characters where only the first is escaped.
0 @N01@ SNOTE @@ one leading
0 @N02@ SNOTE @@one leading no space
0 @N05@ SNOTE doubled @@ internal has two @ characters, not escaped
0 @N06@ SNOTE doubled@@internal no space
0 @N07@ SNOTE single @ internal
0 @N08@ SNOTE single@internal no space
0 @N19@ SNOTE @@ at at front and @ inside line and
1 CONT @@ at after CONT and @ inside CONT's line too.
0 TRLR"""
    )
