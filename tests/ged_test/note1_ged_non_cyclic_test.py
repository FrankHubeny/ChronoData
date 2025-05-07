# note1_ged_cyclic_test.py
"""This test returns the note1 file without the cyclic error that was
to be caught in the original note1.ged file.

The parts from the notes1_ged_test.py were commented out below.
"""

from genedata.methods import Util


def test_note1_non_cyclic_ged() -> None:
    # Test constructing the note1_ged test data without the circular issue.

    # Test constructing the remarriage2_ged test data.
    file = Util.read('tests/data/ged_examples/notes-1-non-cyclic.ged')

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
    # snote_5_xref = g.shared_note_xref('5', 'A cyclic note record')

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
        # gc.Snote(snote_5_xref),
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
    # snote_5 = gc.RecordSnote(snote_5_xref, [
    #     gc.Sour(sour_2_xref),
    # ])

    # Stage the GEDCOM records to generate the ged lines.
    g.stage(header)
    g.stage(subm_1)
    g.stage(sour_2)
    g.stage(snote_3)
    g.stage(snote_4)
    # g.stage(snote_5)

    # Run the following to show the ged file that the above code would produce.
    ged_file: str = g.show_ged()


    assert file == ged_file
