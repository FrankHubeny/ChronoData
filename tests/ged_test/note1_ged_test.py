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

from genedata.messages import Msg
from genedata.methods import Util


def test_note1_ged() -> None:
    # Test constructing the note1_ged test data without the circular issue.

    # Test constructing the remarriage2_ged test data.
    file = Util.read('tests/data/ged_examples/notes-1.ged')

    # Import the required packages and classes.
    import genedata.classes70 as gc
    from genedata.build import Genealogy

    # Instantiate a Genealogy class.
    g = Genealogy()

    # Instantiate the cross reference identifiers.
    # There were 5 cross reference identifiers.
    subm_1_xref = g.submitter_xref('1')
    sour_2_xref = g.source_xref('2')
    snote_3_xref = g.shared_note_xref('3', 'A single-use note record')
    snote_4_xref = g.shared_note_xref('4', 'A dual-use note record')
    snote_5_xref = g.shared_note_xref('5', 'A cyclic note record')

    # Instantiate the header record.
    header = gc.Head([
        gc.HeadSour('conversion test'),
        gc.Subm(subm_1_xref),
        gc.Gedc([
            gc.GedcVers('7.0'),
        ]),
        gc.Note('The header note'),
    ])

    # Instantiate the records holding the GED data.
    subm_1 = gc.RecordSubm(subm_1_xref, [
        gc.Name('Luther Tychonievich'),
        gc.Note('An inline submission note'),
        gc.Snote(snote_4_xref),
    ])
    sour_2 = gc.RecordSour(sour_2_xref, [
        gc.Snote(snote_3_xref),
        gc.Snote(snote_4_xref),
        gc.Snote(snote_5_xref),
    ])
    snote_3 = gc.RecordSnote(snote_3_xref, [
        gc.Chan([
            gc.DateExact('25 MAY 2021'),
        ]),
    ])
    snote_4 = gc.RecordSnote(snote_4_xref, [
        gc.Chan([
            gc.DateExact('25 MAY 2021'),
        ]),
    ])
    snote_5 = gc.RecordSnote(snote_5_xref, [
        gc.Sour(sour_2_xref),
    ])

    # Stage the GEDCOM records to generate the ged lines.
    g.stage(header)
    g.stage(subm_1)
    g.stage(sour_2)
    g.stage(snote_3)
    g.stage(snote_4)
    g.stage(snote_5)

    # Run the following to show the ged file that the above code would produce.

    with pytest.raises(
        ValueError, match=re.escape(Msg.CIRCULAR.format(repr(sour_2_xref), repr(snote_5_xref)))
    ):
        g.show_ged()


    

