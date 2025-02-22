# escapes_ged_test.py
"""Reproduce the `escapes.ged` output.

This does not include the trailer line.  Nor does it write the file.

Reference:
    [GEDCOM Escapes test file](https://gedcom.io/testfiles/gedcom70/escapes.ged)
"""

import pytest

from genedata.build import Genealogy
from genedata.store import (
    Header,
    Individual,
    Note,
    PersonalName,
    SharedNote,
)

escapes_data = [
    ('gedcom[0]', '0 HEAD'),
    ('gedcom[1]', '1 GEDC'),
    ('gedcom[2]', '2 VERS 7.0'),
    (
        'gedcom[3]',
        '1 NOTE This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.',
    ),
    ('gedcom[4]', '0 @I1@ INDI'),
    ('gedcom[5]', '1 NAME John /Doe/'),
    ('gedcom[6]', '1 NOTE me@example.com is an example email address.'),
    ('gedcom[7]', '2 CONT @@me and @I are example social media handles.'),
    (
        'gedcom[8]',
        '2 CONT @@@@@ has four @ characters where only the first is escaped.',
    ),
    ('gedcom[9]', '0 @N01@ SNOTE @@ one leading'),
    ('gedcom[10]', '0 @N02@ SNOTE @@one leading no space'),
    (
        'gedcom[11]',
        '0 @N05@ SNOTE doubled @@ internal has two @ characters, not escaped',
    ),
    ('gedcom[12]', '0 @N06@ SNOTE doubled@@internal no space'),
    ('gedcom[13]', '0 @N07@ SNOTE single @ internal'),
    ('gedcom[14]', '0 @N08@ SNOTE single@internal no space'),
    ('gedcom[15]', '0 @N19@ SNOTE @@ at at front and @ inside line and'),
    ('gedcom[16]', "1 CONT @@ at after CONT and @ inside CONT's line too."),
]


@pytest.mark.parametrize('test_input,expected', escapes_data)  # noqa: PT006
def test_escape_ged(test_input: str, expected: str | int | bool) -> None:  # noqa: ARG001
    # Test constructing the escapes.ged test data.
    g = Genealogy('testing')
    head = Header(
        note=Note(
            'This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.'
        )
    ).ged()
    indi = Individual(
        xref=g.individual_xref('I', True),
        personal_names=PersonalName('John Doe', 'Doe'),
        notes=Note(
            'me@example.com is an example email address.\n@me and @I are example social media handles.\n@@@@ has four @ characters where only the first is escaped.'
        ),
    ).ged()
    sn1 = SharedNote(xref=g.shared_note_xref('N01'), text='@ one leading').ged()
    sn2 = SharedNote(
        xref=g.shared_note_xref('N02'), text='@one leading no space'
    ).ged()
    sn3 = SharedNote(
        xref=g.shared_note_xref('N05'),
        text='doubled @@ internal has two @ characters, not escaped',
    ).ged()
    sn4 = SharedNote(
        xref=g.shared_note_xref('N06'), text='doubled@@internal no space'
    ).ged()
    sn5 = SharedNote(
        xref=g.shared_note_xref('N07'), text='single @ internal'
    ).ged()
    sn6 = SharedNote(
        xref=g.shared_note_xref('N08'), text='single@internal no space'
    ).ged()
    sn7 = SharedNote(
        xref=g.shared_note_xref('N19'),
        text="@ at at front and @ inside line and\n@ at after CONT and @ inside CONT's line too.",
    ).ged()

    gedcom: list[str] = ''.join(  # noqa: F841
        [head, indi, sn1, sn2, sn3, sn4, sn5, sn6, sn7]
    ).split('/n')  
