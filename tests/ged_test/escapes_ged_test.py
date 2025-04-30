# escapes_ged_test.py
"""Reproduce the `escapes.ged` output.

Reference:
    [GEDCOM Escapes test file](https://gedcom.io/testfiles/gedcom70/escapes.ged)
"""

from genedata.methods import Util


def test_escape_ged() -> None:
    # Test constructing the escapes.ged test data.
    file = Util.read_ged('tests\\data\\ged_examples\\escapes.ged')

    # Import the required packages and classes.
    import genedata.classes70 as gc
    from genedata.build import Genealogy

    # Instantiate a Genealogy class.
    g = Genealogy()

    # Instantiate the cross reference identifiers.
    # There were 8 xref identifiers and 0 void identifiers.
    indi_I1_xref = g.individual_xref('I1')
    snote_N01_xref = g.shared_note_xref('N01', '@ one leading')
    snote_N02_xref = g.shared_note_xref('N02', '@one leading no space')
    snote_N05_xref = g.shared_note_xref('N05', 'doubled @@ internal has two @ characters, not escaped')
    snote_N06_xref = g.shared_note_xref('N06', 'doubled@@internal no space')
    snote_N07_xref = g.shared_note_xref('N07', 'single @ internal')
    snote_N08_xref = g.shared_note_xref('N08', 'single@internal no space')
    snote_N19_xref = g.shared_note_xref('N19', """@ at at front and @ inside line and 
@ at after CONT and @ inside CONT's line too.""")

    # Instantiate the header record.
    header = gc.Head([
        gc.Gedc([
            gc.GedcVers('7.0'),
        ]),
        gc.Note('This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.'),
    ])


    # Instantiate the records holding the GED data.
    indi_I1 = gc.RecordIndi(indi_I1_xref, [
        gc.IndiName('John /Doe/'),
        gc.Note('''me@example.com is an example email address.
@me and @I are example social media handles.
@@@@ has four @ characters where only the first is escaped.'''),
    ])

    snote_N01 = gc.RecordSnote(snote_N01_xref)
    snote_N02 = gc.RecordSnote(snote_N02_xref)
    snote_N05 = gc.RecordSnote(snote_N05_xref)
    snote_N06 = gc.RecordSnote(snote_N06_xref)
    snote_N07 = gc.RecordSnote(snote_N07_xref)
    snote_N08 = gc.RecordSnote(snote_N08_xref)
    snote_N19 = gc.RecordSnote(snote_N19_xref)

    # Stage the GEDCOM records to generate the ged lines.
    g.stage(header)
    g.stage(indi_I1)
    g.stage(snote_N01)
    g.stage(snote_N02)
    g.stage(snote_N05)
    g.stage(snote_N06)
    g.stage(snote_N07)
    g.stage(snote_N08)
    g.stage(snote_N19)

    # Run the following to show the ged file that the above code would produce.
    ged_file = g.show_ged()


    assert file == ged_file
