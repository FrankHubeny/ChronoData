# extensions_ged_test.py
"""Construct the GEDCOM file """

from genedata.methods import Util

file = Util.read('tests\\data\\ged_examples\\extension-modified.ged')

# def test_extension_ged() -> None:
#     # Import the required packages and classes.
#     import genedata.classes70 as gc
#     from genedata.build import Genealogy

#     # Instantiate a Genealogy class.
#     g = Genealogy()

#     # Instantiate the cross reference identifiers.
#     # There were 3 cross reference identifiers.
#     indi_I1_xref = g.individual_xref('I1')
#     _loc_LOC1_xref = g.extension_xref('LOC1')
#     _loc_LOC2_xref = g.extension_xref('LOC2')

#     # Instantiate the header record.
#     header = gc.Head([
#         gc.Gedc([
#             gc.GedcVers('7.0'),
#         ]),
#         gc.Note('This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.'),
#         gc.HeadSour('Test'),
#     ])

#     # Instantiate the records holding the GED data.
#     indi_I1 = gc.RecordIndi(indi_I1_xref, [
#         gc.IndiName('John /Doe/'),
#         gc.Birt('', [
#             gc.Plac('Town, Country', [
#     _loc_LOC1 = gc.Ext(_loc_LOC1_xref, [
#     _loc_LOC2 = gc.Ext(_loc_LOC2_xref, [

#     # Stage the 4 GEDCOM records to generate the ged lines.
#     g.stage(header)
#     g.stage(indi_I1)
#     g.stage(_loc_LOC1)
#     g.stage(_loc_LOC2)

#     # Run the following to show the ged file that the above code would produce.
#     ged_file = g.show_ged()

    