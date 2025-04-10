# note1_ged_test.py
"""Reproduce the `note-1.ged` output.

This test contains a cyclic cross reference which generates a ValueError.

The test is also run without the cyclic cross reference part.

The original file has the "1 GEDC 2 VERS 7.0" start after the source and
submitter references.  These have been modified so those lines come
immediately after "0 HEAD".

Reference:
    [GEDCOM Age test file](https://gedcom.io/testfiles/gedcom70/note-1.ged)
"""

import re

import pytest

import genedata.classes70 as gc
from genedata.build import Genealogy
from genedata.constants import Default
from genedata.messages import Msg
from genedata.structure import (  # noqa: F401
    SharedNoteXref,
    SourceXref,
    SubmitterXref,
    Xref,
)

ged_version: str = '7.0'

def test_note1_ged() -> None:
    # Test constructing the note1_ged test data without the circular issue.

    file_not_circular = """0 HEAD
1 SOUR conversion test
1 SUBM @1@
1 GEDC
2 VERS 7.0
1 NOTE the header note
0 @1@ SUBM
1 NAME Luther Tychonievich
1 NOTE An inline submission note
1 SNOTE @4@
0 @2@ SOUR
1 SNOTE @3@
1 SNOTE @4@
1 SNOTE @5@
0 @3@ SNOTE A single-use note record
1 CHAN
2 DATE 25 MAY 2021
0 @4@ SNOTE A dual-use note record
1 CHAN
2 DATE 25 MAY 2021
0 TRLR"""

    g = Genealogy('test', version=ged_version)

    subm_xref = g.submitter_xref('1')
    snote3_xref = g.shared_note_xref('3', 'A single-use note record')
    snote4_xref = g.shared_note_xref('4', 'A dual-use note record')
    snote5_xref = g.shared_note_xref('5', 'A cyclic note record')
    sour_xref = g.source_xref('2')

    head = gc.Head(
        [
            gc.HeadSour('conversion test'),
            gc.Subm(subm_xref),
            gc.Gedc(gc.GedcVers('7.0')),
            gc.Note('the header note'),
        ]
    )
    subm = gc.RecordSubm(
        subm_xref,
        [
            gc.Name('Luther Tychonievich'),
            gc.Note('An inline submission note'),
            gc.Snote(snote4_xref),
        ],
    )
    sour = gc.RecordSour(
        sour_xref,
        [
            gc.Snote(snote3_xref),
            gc.Snote(snote4_xref),
            gc.Snote(snote5_xref),
        ],
    )
    snote3 = gc.RecordSnote(snote3_xref, gc.Chan(gc.DateExact('25 MAY 2021')))
    snote4 = gc.RecordSnote(snote4_xref, gc.Chan(gc.DateExact('25 MAY 2021')))

    gedcom = ''.join(
        [
            head.ged(),
            subm.ged(),
            sour.ged(),
            snote3.ged(),
            snote4.ged(),
            Default.TRAILER,
        ]
    )

    assert gedcom == file_not_circular

def test_note1_ged_code() -> None:
    # Test generating code, evaluating it and then finding the ged lines.

    file_not_circular = """0 HEAD
1 SOUR conversion test
1 SUBM @1@
1 GEDC
2 VERS 7.0
1 NOTE the header note
0 @1@ SUBM
1 NAME Luther Tychonievich
1 NOTE An inline submission note
1 SNOTE @4@
0 @2@ SOUR
1 SNOTE @3@
1 SNOTE @4@
1 SNOTE @5@
0 @3@ SNOTE A single-use note record
1 CHAN
2 DATE 25 MAY 2021
0 @4@ SNOTE A dual-use note record
1 CHAN
2 DATE 25 MAY 2021
0 TRLR"""

    g = Genealogy('test', version=ged_version)

    subm_xref = g.submitter_xref('1')
    snote3_xref = g.shared_note_xref('3', 'A single-use note record')
    snote4_xref = g.shared_note_xref('4', 'A dual-use note record')
    snote5_xref = g.shared_note_xref('5', 'A cyclic note record')
    sour_xref = g.source_xref('2')

    head = gc.Head(
        [
            gc.HeadSour('conversion test'),
            gc.Subm(subm_xref),
            gc.Gedc(gc.GedcVers('7.0')),
            gc.Note('the header note'),
        ]
    )
    subm = gc.RecordSubm(
        subm_xref,
        [
            gc.Name('Luther Tychonievich'),
            gc.Note('An inline submission note'),
            gc.Snote(snote4_xref),
        ],
    )
    sour = gc.RecordSour(
        sour_xref,
        [
            gc.Snote(snote3_xref),
            gc.Snote(snote4_xref),
            gc.Snote(snote5_xref),
        ],
    )
    snote3 = gc.RecordSnote(snote3_xref, gc.Chan(gc.DateExact('25 MAY 2021')))
    snote4 = gc.RecordSnote(snote4_xref, gc.Chan(gc.DateExact('25 MAY 2021')))

    gedcom = ''.join(
        [
            eval(head.code(as_name='gc')).ged(),
            eval(subm.code(as_name='gc')).ged(),
            eval(sour.code(as_name='gc')).ged(),
            eval(snote3.code(as_name='gc')).ged(),
            eval(snote4.code(as_name='gc')).ged(),
            Default.TRAILER,
        ]
    )

    assert gedcom == file_not_circular


def test_note1_ged_circular() -> None:
    """Test constructing the note1_ged test data with the circular issue."""

    g = Genealogy('test', version=ged_version)

    subm_xref = g.submitter_xref('1')
    snote3_xref = g.shared_note_xref('3', 'A single-use note record')
    snote4_xref = g.shared_note_xref('4', 'A dual-use note record')
    snote5_xref = g.shared_note_xref('5', 'A cyclic note record')
    sour_xref = g.source_xref('2')

    head = gc.Head(
        [
            gc.Gedc(gc.GedcVers('7.0')),
            gc.HeadSour('conversion test'),
            gc.Subm(subm_xref),
            gc.Note('the header note'),
        ]
    )
    subm = gc.RecordSubm(
        subm_xref,
        [
            gc.Name('Luther Tychonievich'),
            gc.Note('An inline submission note'),
            gc.Snote(snote4_xref),
        ],
    )
    sour = gc.RecordSour(
        sour_xref,
        [
            gc.Snote(snote3_xref),
            gc.Snote(snote4_xref),
            gc.Snote(snote5_xref),
        ],
    )
    snote3 = gc.RecordSnote(snote3_xref, gc.Chan(gc.DateExact('25 MAY 2021')))
    snote4 = gc.RecordSnote(snote4_xref, gc.Chan(gc.DateExact('25 MAY 2021')))
    snote5 = gc.RecordSnote(snote5_xref, gc.Sour(sour_xref))

    with pytest.raises(
        ValueError,
        match=re.escape(Msg.CIRCULAR.format(repr(sour_xref), repr(snote5_xref))),
    ):
        gedcom: str = ''.join(  # noqa: F841
            [
                head.ged(),
                subm.ged(),
                sour.ged(),
                snote3.ged(),
                snote4.ged(),
                snote5.ged(),
                Default.TRAILER,
            ]
        )
