# note1_ged_test.py
"""Reproduce the `note-1.ged` output.

This test contains a cyclic cross reference which generates a ValueError.

The test is also run without the cyclic cross reference part.

Reference:
    [GEDCOM Age test file](https://gedcom.io/testfiles/gedcom70/note-1.ged)
"""

import re

import pytest

from genedata.build import Genealogy
from genedata.classes7 import (
    Chan,
    DateExact,
    Gedc,
    GedcVers,
    Head,
    HeadSour,
    Name,
    Note,
    RecordSnote,
    RecordSour,
    RecordSubm,
    Snote,
    Sour,
    Subm,
    Trlr,
)
from genedata.constants import Config
from genedata.messages import Msg


def test_note1_ged() -> None:
    # Test constructing the note1_ged test data without circular issue.

    file = """0 HEAD
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

    g = Genealogy('test')

    subm_xref = g.submitter_xref('1')
    snote3_xref = g.shared_note_xref('3', 'A single-use note record')
    snote4_xref = g.shared_note_xref('4', 'A dual-use note record')
    snote5_xref = g.shared_note_xref('5', 'A cyclic note record')
    sour_xref = g.source_xref('2')

    head = Head(
        [
            HeadSour('conversion test'),
            Subm(subm_xref),
            Gedc(GedcVers(Config.GEDVERSION)),
            Note('the header note'),
        ]
    )
    subm = RecordSubm(
        subm_xref,
        [
            Name('Luther Tychonievich'),
            Note('An inline submission note'),
            Snote(snote4_xref),
        ],
    )
    sour = RecordSour(
        sour_xref,
        [
            Snote(snote3_xref),
            Snote(snote4_xref),
            Snote(snote5_xref),
        ],
    )
    snote3 = RecordSnote(snote3_xref, Chan(DateExact('25 MAY 2021')))
    snote4 = RecordSnote(snote4_xref, Chan(DateExact('25 MAY 2021')))

    gedcom = ''.join(
        [
            head.ged(),
            subm.ged(),
            sour.ged(),
            snote3.ged(),
            snote4.ged(),
            Trlr().ged(),
        ]
    )

    assert gedcom == file


def test_note1_ged_circular() -> None:
    """Test constructing the note1_ged test data with the circular issue."""

    #     file_circular = """0 HEAD
    # 1 SOUR conversion test
    # 1 SUBM @1@
    # 1 GEDC
    # 2 VERS 7.0
    # 1 NOTE the header note
    # 0 @1@ SUBM
    # 1 NAME Luther Tychonievich
    # 1 NOTE An inline submission note
    # 1 SNOTE @4@
    # 0 @2@ SOUR
    # 1 SNOTE @3@
    # 1 SNOTE @4@
    # 1 SNOTE @5@
    # 0 @3@ SNOTE A single-use note record
    # 1 CHAN
    # 2 DATE 25 MAY 2021
    # 0 @4@ SNOTE A dual-use note record
    # 1 CHAN
    # 2 DATE 25 MAY 2021
    # 0 @5@ SNOTE A cyclic note record
    # 1 SOUR @2@
    # 0 TRLR"""

    g = Genealogy('test')

    subm_xref = g.submitter_xref('1')
    snote3_xref = g.shared_note_xref('3', 'A single-use note record')
    snote4_xref = g.shared_note_xref('4', 'A dual-use note record')
    snote5_xref = g.shared_note_xref('5', 'A cyclic note record')
    sour_xref = g.source_xref('2')

    head = Head(
        [
            HeadSour('conversion test'),
            Subm(subm_xref),
            Gedc(GedcVers(Config.GEDVERSION)),
            Note('the header note'),
        ]
    )
    subm = RecordSubm(
        subm_xref,
        [
            Name('Luther Tychonievich'),
            Note('An inline submission note'),
            Snote(snote4_xref),
        ],
    )
    sour = RecordSour(
        sour_xref,
        [
            Snote(snote3_xref),
            Snote(snote4_xref),
            Snote(snote5_xref),
        ],
    )
    snote3 = RecordSnote(snote3_xref, Chan(DateExact('25 MAY 2021')))
    snote4 = RecordSnote(snote4_xref, Chan(DateExact('25 MAY 2021')))
    snote5 = RecordSnote(snote5_xref, Sour(sour_xref))

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
                Trlr().ged(),
            ]
        )
