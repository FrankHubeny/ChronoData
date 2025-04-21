# ssex_ged_test.py
"""Generate the [Same Sex Marriange GEDCOM Example File](https://gedcom.io/testfiles/gedcom70/same-sex-marriage.ged)."""


from genedata.methods import Util

ged_version: str = '7.0'

def test_ssex_ged() -> None:
    """ Test constructing the same sex marriage_ged test data."""
    file = Util.read('tests\\ged_test\\same-sex-marriage.ged')
    
    # Import the required packages and classes.
    import genedata.classes70 as gc
    from genedata.build import Genealogy

    # Instantiate a Genealogy class.
    g = Genealogy()

    # Instantiate the cross reference identifiers.
    # There were 3 xref identifiers and 0 void identifiers.
    indi_I1_xref = g.individual_xref('I1')
    indi_I2_xref = g.individual_xref('I2')
    fam_F1_xref = g.family_xref('F1')

    # Instantiate the header record.
    header = gc.Head([
        gc.Gedc([
            gc.GedcVers('7.0'),
        ]),
    ])


    # Instantiate the records holding the GED data.
    indi_I1 = gc.RecordIndi(indi_I1_xref, [
        gc.IndiName('John /Doe/'),
        gc.Sex('M'),
        gc.Fams(fam_F1_xref),
    ])

    indi_I2 = gc.RecordIndi(indi_I2_xref, [
        gc.IndiName('Richard /Roe/'),
        gc.Sex('M'),
        gc.Fams(fam_F1_xref),
    ])

    fam_F1 = gc.RecordFam(fam_F1_xref, [
        gc.FamHusb(indi_I1_xref),
        gc.FamWife(indi_I2_xref),
    ])


    # Stage the GEDCOM records to generate the ged lines.
    g.stage(header)
    g.stage(indi_I1)
    g.stage(indi_I2)
    g.stage(fam_F1)

    # Run the following to show the ged file that the above code would produce.
    ged_file = g.show_ged()


    assert file == ged_file

