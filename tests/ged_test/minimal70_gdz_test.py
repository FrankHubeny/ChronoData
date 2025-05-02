# minimal70_gdz_test

from genedata.methods import Util


def test_minimal_ged() -> None:
    # Test constructing the minimal70.ged test file.
    file = Util.read_gdz_ged_file('gedcom.ged', 'tests/data/ged_examples/minimal70.gdz')
    
    # Import the required packages and classes.
    import genedata.classes70 as gc
    from genedata.build import Genealogy

    # Instantiate a Genealogy class.
    g = Genealogy()

    # Instantiate the cross reference identifiers.
    # There were no cross reference identifiers.

    # Instantiate the header record.
    header = gc.Head([
        gc.Gedc([
            gc.GedcVers('7.0'),
        ]),
    ])

    # Instantiate the records holding the GED data.
    # There were no records outside of the header record.

    # Stage the 1 GEDCOM records to generate the ged lines.
    g.stage(header)

    # Run the following to show the ged file that the above code would produce.
    ged_file = g.show_ged()

    
    assert file == ged_file

