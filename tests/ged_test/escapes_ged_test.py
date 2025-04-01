# escapes_ged_test.py
"""Reproduce the `escapes.ged` output.

Reference:
    [GEDCOM Escapes test file](https://gedcom.io/testfiles/gedcom70/escapes.ged)
"""

import genedata.classes7 as gc
from genedata.build import Genealogy
from genedata.constants import Config, Default
from genedata.methods import Util


def test_escape_ged() -> None:
    # Test constructing the escapes.ged test data.
    file = Util.read('tests\\ged_test\\escapes.ged')
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

    head = gc.Head(
        [
            gc.Gedc(gc.GedcVers(Config.GEDVERSION)),
            gc.Note(
                'This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.'
            ),
        ]
    )

    indi = gc.RecordIndi(
        indi_xref,
        [
            gc.IndiName('John /Doe/'),
            gc.Note("""me@example.com is an example email address.
@me and @I are example social media handles.
@@@@ has four @ characters where only the first is escaped."""),
        ],
    )

    gedcom = ''.join(
        [
            head.ged(),
            indi.ged(),
            gc.RecordSnote(sn1_xref).ged(),
            gc.RecordSnote(sn2_xref).ged(),
            gc.RecordSnote(sn5_xref).ged(),
            gc.RecordSnote(sn6_xref).ged(),
            gc.RecordSnote(sn7_xref).ged(),
            gc.RecordSnote(sn8_xref).ged(),
            gc.RecordSnote(sn19_xref).ged(),
            Default.TRAILER,
        ]
    )

    assert gedcom == file
