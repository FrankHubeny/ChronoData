# ged_to_code_lang_test.py
"""Tests for the ged_to_code method."""

from genedata.build import Genealogy

lang_file: str = 'tests/data/ged_examples/lang.ged'

def test_ged_to_code_lang() -> None:
    expected = """# Import the required packages and classes.
import genedata.classes70 as gc
from genedata.build import Genealogy

# Instantiate a Genealogy class.
g = Genealogy()

# Instantiate the cross reference identifiers.
# There were 2 cross reference identifiers.
subm_1_xref = g.submitter_xref('1')
subm_2_xref = g.submitter_xref('2')

# Add any extensions that were registered in the header record.
_phrase_PHRASE = g.document_tag('_PHRASE', 'https://gedcom.io/terms/v7/PHRASE')

# Instantiate the header record.
header = gc.Head([
    gc.Gedc([
        gc.GedcVers('7.0'),
    ]),
    gc.Note('This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.'),
    gc.HeadSour('TEST_FILES'),
    gc.Subm(subm_1_xref),
    gc.HeadLang('af'),
    gc.Schma([
        gc.Tag('_PHRASE https://gedcom.io/terms/v7/PHRASE'),
    ]),
])

# Instantiate the records holding the GED data.
subm_1 = gc.RecordSubm(subm_1_xref, [
    gc.Name('Luther'),
    gc.SubmLang('en'),
    gc.SubmLang('ja'),
    gc.SubmLang('es'),
])
subm_2 = gc.RecordSubm(subm_2_xref, [
    gc.Name('GEDCOM 5.5.1'),
    gc.Note('This contains the language tags for every language named in the v5.5.1 spec, namely: Afrikaans, Albanian, Amharic, Anglo-Saxon, Arabic, Armenian, Assamese, Belorusian, Bengali, Braj, Bulgarian, Burmese, Cantonese, Catalan, Catalan_Spn, Church-Slavic, Czech, Danish, Dogri, Dutch, English, Esperanto, Estonian, Faroese, Finnish, French, Georgian, German, Greek, Gujarati, Hawaiian, Hebrew, Hindi, Hungarian, Icelandic, Indonesian, Italian, Japanese, Kannada, Khmer, Konkani, Korean, Lahnda, Lao, Latvian, Lithuanian, Macedonian, Maithili, Malayalam, Mandrin, Manipuri, Marathi, Mewari, Navaho, Nepali, Norwegian, Oriya, Pahari, Pali, Panjabi, Persian, Polish, Portuguese, Prakrit, Pusto, Rajasthani, Romanian, Russian, Sanskrit, Serb, Serbo_Croa, Slovak, Slovene, Spanish, Swedish, Tagalog, Tamil, Telugu, Thai, Tibetan, Turkish, Ukrainian, Urdu, Vietnamese, Wendic, Yiddish'),
    gc.SubmLang('af'),
    gc.SubmLang('sq'),
    gc.SubmLang('am'),
    gc.SubmLang('ang'),
    gc.SubmLang('ar'),
    gc.SubmLang('hy'),
    gc.SubmLang('as'),
    gc.SubmLang('be'),
    gc.SubmLang('bn'),
    gc.SubmLang('bra'),
    gc.SubmLang('bg'),
    gc.SubmLang('my'),
    gc.SubmLang('yue'),
    gc.SubmLang('ca'),
    gc.SubmLang('ca-ES'),
    gc.SubmLang('cu'),
    gc.SubmLang('cs'),
    gc.SubmLang('da'),
    gc.SubmLang('dgr'),
    gc.SubmLang('nl'),
    gc.SubmLang('en'),
    gc.SubmLang('eo'),
    gc.SubmLang('et'),
    gc.SubmLang('fo'),
    gc.SubmLang('fi'),
    gc.SubmLang('fr'),
    gc.SubmLang('ka'),
    gc.SubmLang('de'),
    gc.SubmLang('el'),
    gc.SubmLang('gu'),
    gc.SubmLang('haw'),
    gc.SubmLang('he'),
    gc.SubmLang('hi'),
    gc.SubmLang('hu'),
    gc.SubmLang('is'),
    gc.SubmLang('id'),
    gc.SubmLang('it'),
    gc.SubmLang('ja'),
    gc.SubmLang('kn'),
    gc.SubmLang('km'),
    gc.SubmLang('kok'),
    gc.SubmLang('ko'),
    gc.SubmLang('lah'),
    gc.SubmLang('lo'),
    gc.SubmLang('lv'),
    gc.SubmLang('lt'),
    gc.SubmLang('mk'),
    gc.SubmLang('mai'),
    gc.SubmLang('ml'),
    gc.SubmLang('cmn'),
    gc.SubmLang('mni'),
    gc.SubmLang('mr'),
    gc.SubmLang('mtr'),
    gc.SubmLang('nv'),
    gc.SubmLang('ne'),
    gc.SubmLang('no'),
    gc.SubmLang('or'),
    gc.SubmLang('him'),
    gc.SubmLang('pi'),
    gc.SubmLang('pa'),
    gc.SubmLang('fa'),
    gc.SubmLang('pl'),
    gc.SubmLang('pt'),
    gc.SubmLang('pra'),
    gc.SubmLang('ps'),
    gc.SubmLang('raj'),
    gc.SubmLang('ro'),
    gc.SubmLang('ru'),
    gc.SubmLang('sa'),
    gc.SubmLang('sr'),
    gc.SubmLang('sh'),
    gc.SubmLang('sk'),
    gc.SubmLang('sl'),
    gc.SubmLang('es'),
    gc.SubmLang('sv'),
    gc.SubmLang('tl'),
    gc.SubmLang('ta'),
    gc.SubmLang('te'),
    gc.SubmLang('th'),
    gc.SubmLang('bo'),
    gc.SubmLang('tr'),
    gc.SubmLang('uk'),
    gc.SubmLang('ur'),
    gc.SubmLang('vi'),
    gc.SubmLang('wen'),
    gc.SubmLang('yi'),
])

# Stage the 3 GEDCOM records to generate the ged lines.
g.stage(header)
g.stage(subm_1)
g.stage(subm_2)

# Run the following to show the ged file that the above code would produce.
ged_file = g.show_ged()

# Then print this file to view it.
print(ged_file)
"""
    g = Genealogy(lang_file)
    code = g.ged_to_code()
    assert code == expected
