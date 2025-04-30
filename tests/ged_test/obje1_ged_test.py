# obje1_ged_test.py
"""Reproduce the `obje-1.ged` output.

Reference:
    [GEDCOM Age test file](https://gedcom.io/testfiles/gedcom70/obje-1.ged)
"""


from genedata.methods import Util


def test_obje1_ged() -> None:
    """Construct the obje1_ged example file."""
    file = Util.read('tests\\data\\ged_examples\\obje-1.ged')

    # Import the required packages and classes.
    import genedata.classes70 as gc
    from genedata.build import Genealogy

    # Instantiate a Genealogy class.
    g = Genealogy()

    # Instantiate the cross reference identifiers.
    # There were 3 xref identifiers and 0 void identifiers.
    obje_1_xref = g.multimedia_xref('1')
    obje_X1_xref = g.multimedia_xref('X1')
    indi_2_xref = g.individual_xref('2')

    # Instantiate the header record.
    header = gc.Head([
        gc.Gedc([
            gc.GedcVers('7.0'),
        ]),
    ])


    # Instantiate the records holding the GED data.
    obje_1 = gc.RecordObje(obje_1_xref, [
        gc.File('example.jpg', [
            gc.Form('image/jpeg', [
                gc.Medi('PHOTO'),
            ]),
            gc.Titl('Example Image File'),
        ]),
        gc.File('example.mp3', [
            gc.Form('application/x-mp3'),
            gc.Titl('Sound Clip'),
        ]),
        gc.Note('note in OBJE record'),
    ])

    obje_X1 = gc.RecordObje(obje_X1_xref, [
        gc.File('gifts.webm', [
            gc.Form('application/x-other', [
                gc.Medi('VIDEO'),
            ]),
        ]),
        gc.File('cake.webm', [
            gc.Form('application/x-other', [
                gc.Medi('VIDEO'),
            ]),
        ]),
        gc.Note('note in OBJE link'),
    ])

    indi_2 = gc.RecordIndi(indi_2_xref, [
        gc.Obje(obje_1_xref),
        gc.Obje(obje_X1_xref, [
            gc.Titl('fifth birthday party'),
        ]),
    ])


    # Stage the GEDCOM records to generate the ged lines.
    g.stage(header)
    g.stage(obje_1)
    g.stage(obje_X1)
    g.stage(indi_2)

    # Run the following to show the ged file that the above code would produce.
    ged_file = g.show_ged()

    assert file == ged_file


