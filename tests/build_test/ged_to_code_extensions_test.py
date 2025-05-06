# ged_to_code_extensions_test.py
"""Tests for the ged_to_code method."""

from genedata.build import Genealogy

extensions_file: str = 'tests/data/ged_examples/extensions-modified.ged'

def test_ged_to_code_extensions() -> None:
    expected = """# Import the required packages and classes.
import genedata.classes70 as gc
from genedata.build import Genealogy
from genedata.structure import Void

# Instantiate a Genealogy class.
g = Genealogy()

# Instantiate the cross reference identifiers.
# There were 6 cross reference identifiers.
_user_U1_xref = g.extension_xref('U1')
subm_U2_xref = g.submitter_xref('U2')
indi_I1_xref = g.individual_xref('I1')
_record_R1_xref = g.extension_xref('R1', 'not empty')
_party_P1_xref = g.extension_xref('P1')
_loc_L1_xref = g.extension_xref('L1')

# Add any extensions that were registered in the header record.
_record_record_INDI = g.document_tag('_RECORD', 'tests/data/record-INDI.yaml')
_struct_good_structure = g.document_tag('_STRUCT', 'tests/data/good_structure.yaml')
_enumval_enum_4 = g.document_tag('_ENUMVAL', 'tests/data/enum-4.yaml')
_calendar_good_calendar = g.document_tag('_CALENDAR', 'tests/data/good_calendar.yaml')
_month_good_month = g.document_tag('_MONTH', 'tests/data/good_month.yaml')
_epoch_epoch = g.document_tag('_EPOCH', 'http://example.com/epoch')
_user_record_SUBM = g.document_tag('_USER', 'https://gedcom.io/terms/v7/record-SUBM')
_creator_SUBM = g.document_tag('_CREATOR', 'https://gedcom.io/terms/v7/SUBM')
_calendrier_cal_FRENCH_R = g.document_tag('_CALENDRIER', 'https://gedcom.io/terms/v7/cal-FRENCH_R')
_jour_month_COMP = g.document_tag('_JOUR', 'https://gedcom.io/terms/v7/month-COMP')
_child_enum_CHIL = g.document_tag('_CHILD', 'https://gedcom.io/terms/v7/enum-CHIL')
_phrase_PHRASE = g.document_tag('_PHRASE', 'https://gedcom.io/terms/v7/PHRASE')
_party_party_participation = g.document_tag('_PARTY', 'http://example.com/party-participation')
_party_party = g.document_tag('_PARTY', 'http://example.com/party')

# Instantiate the header record.
header = gc.Head([
    gc.Gedc([
        gc.GedcVers('7.0'),
    ]),
    gc.Schma([
        gc.Tag('_RECORD tests/data/record-INDI.yaml'),
        gc.Tag('_STRUCT tests/data/good_structure.yaml'),
        gc.Tag('_ENUMVAL tests/data/enum-4.yaml'),
        gc.Tag('_CALENDAR tests/data/good_calendar.yaml'),
        gc.Tag('_MONTH tests/data/good_month.yaml'),
        gc.Tag('_EPOCH http://example.com/epoch'),
        gc.Tag('_USER https://gedcom.io/terms/v7/record-SUBM'),
        gc.Tag('_CREATOR https://gedcom.io/terms/v7/SUBM'),
        gc.Tag('_CALENDRIER https://gedcom.io/terms/v7/cal-FRENCH_R'),
        gc.Tag('_JOUR https://gedcom.io/terms/v7/month-COMP'),
        gc.Tag('_CHILD https://gedcom.io/terms/v7/enum-CHIL'),
        gc.Tag('_PHRASE https://gedcom.io/terms/v7/PHRASE'),
        gc.Tag('_PARTY http://example.com/party-participation'),
        gc.Tag('_PARTY http://example.com/party'),
    ]),
    gc.Note('''This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.

This file contains the following extension-related content:
Standard record with an extTag           0 @U1@ _USER
Standard substructure                    1 NAME Aliased record
Standard structure with an extTag        1 _CREATOR @U1@
Standard structure with an extTag        1 _CREATOR @U2@
Relocated standard structure             2 _PHRASE A Family
Documented extension enumeration         2 PEDI _ENUMVAL
Undocumented extension enumeration       2 PEDI _ENUM2
Undocumented structure with a pointer    1 _EXT1 @R1@
Undocumented pointer to relocated record 1 _IN @B1@
Unambiguous extension-defined substruct. 2 ROLE CHIL
Undocumented record                      0 @R1@ _RECORD not empty
Pointer to record with an extTag         1 SUBM @U1@
Standard enumeration with an extTag      2 ROLE _CHILD
Standard month with an extTag            ... FRENCH_R 2 _JOUR 8
Standard calendar with an extTag         ... _CALENDRIER 4 COMP 8
Documented calendar, month, and epoch    ... _CALENDAR 8 _MONTH 190 _EPOCH
Undocumented calendar, month, and epoch  ... _CAL2 23 _MON2 88 _EP2
Undocumented pointer with shared tag     2 _LOC @L1@
Documented pointer with shared tag       1 _PARTY @P1@
Unambiguous extension-defined substruct. 2 ROLE NGHBR
Documented record with shared tag        0 @P1@ _PARTY
Ambiguous extension-defined substructure 1 NAME Spring Fling
Undocumented record with shared tag      0 @L1@ _LOC
Extension-defined substructure           1 SUBM @S2@
Ambiguous extension-defined substructure 1 DATE TO 1880
Unambiguous nested ext.-def. substructu. 2 PHRASE Dissolved in the 1870s
Standard and relocated enumerations      2 EVEN DEAT, _CHILD
Relocated standard structure             3 _CREATOR @U2@'''),
])

# Instantiate the records holding the GED data.
_user_U1 = gc.Ext(_user_U1_xref, [
subm_U2 = gc.RecordSubm(subm_U2_xref, [
    gc.Name('Non-aliased record'),
])
indi_I1 = gc.RecordIndi(indi_I1_xref, [
    gc.IndiFamc(Void.FAM, [
        gc.Pedi('_ENUMVAL'),
    ]),
    gc.IndiFamc(Void.FAM, [
        gc.Pedi('_ENUM2'),
    ]),
_record_R1 = gc.Ext(_record_R1_xref, [
INDI0 = gc.RecordIndi(Void.INDI, [
    gc.Subm(),    gc.Subm(),    gc.Asso(indi_I1_xref, [
        gc.Role('_CHILD'),
    ]),
    gc.Birt('', [
        gc.Date('BET FRENCH_R 2 _JOUR 8 AND _CALENDRIER 4 COMP 8'),
    ]),
    gc.Deat('', [
        gc.Date('_CALENDAR 8 _MONTH 190 _EPOCH'),
    ]),
    gc.Grad('', [
        gc.Date('_CAL2 23 _MON2 88 _EP2'),
_party_P1 = gc.Ext(_party_P1_xref, [
_loc_L1 = gc.Ext(_loc_L1_xref, [
SOUR1 = gc.RecordSour(Void.SOUR, [
    gc.Data([
        gc.DataEven('DEAT, _CHILD', [

# Stage the 9 GEDCOM records to generate the ged lines.
g.stage(header)
g.stage(_user_U1)
g.stage(subm_U2)
g.stage(indi_I1)
g.stage(_record_R1)
g.stage(INDI0)
g.stage(_party_P1)
g.stage(_loc_L1)
g.stage(SOUR1)

# Run the following to show the ged file that the above code would produce.
ged_file = g.show_ged()

# Then print this file to view it.
print(ged_file)
"""

    g = Genealogy(extensions_file)
    code = g.ged_to_code()
    assert code == expected
    