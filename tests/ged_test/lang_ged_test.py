# lang_ged_test.py
"""Generate the Lang GEDCOM example file."""
from genedata.build import Genealogy
from genedata.classes7 import (
    Gedc,
    GedcVers,
    Head,
    HeadLang,
    HeadSour,
    Name,
    Note,
    RecordSubm,
    Schma,
    Subm,
    SubmLang,
    Tag,
    Trlr,
)
from genedata.constants import Config
from genedata.structure import SubmitterXref  # noqa: F401
from genedata.util import Util


def test_lang_ged() -> None:
    # Test constructing the remarriage2_ged test data.
    file = Util.read('tests\\ged_test\\lang.ged')
    g = Genealogy('test')
    subm1_xref = g.submitter_xref('1')
    subm2_xref = g.submitter_xref('2')

    head = Head(
        [
            Gedc(GedcVers(Config.GEDVERSION)), 
            Note('This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.'),
            HeadSour('TEST_FILES'),
            Subm(subm1_xref),
            HeadLang('af'),
            Schma(Tag('_PHRASE https://gedcom.io/terms/v7/PHRASE')),
        ]
    )

    subm1 = RecordSubm(
        subm1_xref,
        [
            Name('Luther'),
            SubmLang('en'),
            SubmLang('ja'),
            SubmLang('es'),
        ],
    )

    subm2 = RecordSubm(
        subm2_xref,
        [
            Name('GEDCOM 5.5.1'),
            Note('This contains the language tags for every language named in the v5.5.1 spec, namely: Afrikaans, Albanian, Amharic, Anglo-Saxon, Arabic, Armenian, Assamese, Belorusian, Bengali, Braj, Bulgarian, Burmese, Cantonese, Catalan, Catalan_Spn, Church-Slavic, Czech, Danish, Dogri, Dutch, English, Esperanto, Estonian, Faroese, Finnish, French, Georgian, German, Greek, Gujarati, Hawaiian, Hebrew, Hindi, Hungarian, Icelandic, Indonesian, Italian, Japanese, Kannada, Khmer, Konkani, Korean, Lahnda, Lao, Latvian, Lithuanian, Macedonian, Maithili, Malayalam, Mandrin, Manipuri, Marathi, Mewari, Navaho, Nepali, Norwegian, Oriya, Pahari, Pali, Panjabi, Persian, Polish, Portuguese, Prakrit, Pusto, Rajasthani, Romanian, Russian, Sanskrit, Serb, Serbo_Croa, Slovak, Slovene, Spanish, Swedish, Tagalog, Tamil, Telugu, Thai, Tibetan, Turkish, Ukrainian, Urdu, Vietnamese, Wendic, Yiddish'),
            SubmLang('af'),
            SubmLang('sq'),
            SubmLang('am'),
            SubmLang('ang'),
            SubmLang('ar'),
            SubmLang('hy'),
            SubmLang('as'),
            SubmLang('be'),
            SubmLang('bn'),
            SubmLang('bra'),
            SubmLang('bg'),
            SubmLang('my'),
            SubmLang('yue'),
            SubmLang('ca'),
            SubmLang('ca-ES'),
            SubmLang('cu'),
            SubmLang('cs'),
            SubmLang('da'),
            SubmLang('dgr'),
            SubmLang('nl'),
            SubmLang('en'),
            SubmLang('eo'),
            SubmLang('et'),
            SubmLang('fo'),
            SubmLang('fi'),
            SubmLang('fr'),
            SubmLang('ka'),
            SubmLang('de'),
            SubmLang('el'),
            SubmLang('gu'),
            SubmLang('haw'),
            SubmLang('he'),
            SubmLang('hi'),
            SubmLang('hu'),
            SubmLang('is'),
            SubmLang('id'),
            SubmLang('it'),
            SubmLang('ja'),
            SubmLang('kn'),
            SubmLang('km'),
            SubmLang('kok'),
            SubmLang('ko'),
            SubmLang('lah'),
            SubmLang('lo'),
            SubmLang('lv'),
            SubmLang('lt'),
            SubmLang('mk'),
            SubmLang('mai'),
            SubmLang('ml'),
            SubmLang('cmn'),
            SubmLang('mni'),
            SubmLang('mr'),
            SubmLang('mtr'),
            SubmLang('nv'),
            SubmLang('ne'),
            SubmLang('no'),
            SubmLang('or'),
            SubmLang('him'),
            SubmLang('pi'),
            SubmLang('pa'),
            SubmLang('fa'),
            SubmLang('pl'),
            SubmLang('pt'),
            SubmLang('pra'),
            SubmLang('ps'),
            SubmLang('raj'),
            SubmLang('ro'),
            SubmLang('ru'),
            SubmLang('sa'),
            SubmLang('sr'),
            SubmLang('sh'),
            SubmLang('sk'),
            SubmLang('sl'),
            SubmLang('es'),
            SubmLang('sv'),
            SubmLang('tl'),
            SubmLang('ta'),
            SubmLang('te'),
            SubmLang('th'),
            SubmLang('bo'),
            SubmLang('tr'),
            SubmLang('uk'),
            SubmLang('ur'),
            SubmLang('vi'),
            SubmLang('wen'),
            SubmLang('yi'),
        ],
    )

    gedcom = ''.join(
        [
            head.ged(), 
            subm1.ged(),
            subm2.ged(),
            Trlr().ged()
        ]
    )

    assert file == gedcom

def test_lang_ged_code() -> None:
    # Test generating code, evaluating it and then finding the ged lines.
    file = Util.read('tests\\ged_test\\lang.ged')
    g = Genealogy('test')
    subm1_xref = g.submitter_xref('1')
    subm2_xref = g.submitter_xref('2')

    head = Head(
        [
            Gedc(GedcVers(Config.GEDVERSION)), 
            Note('This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.'),
            HeadSour('TEST_FILES'),
            Subm(subm1_xref),
            HeadLang('af'),
            Schma(Tag('_PHRASE https://gedcom.io/terms/v7/PHRASE')),
        ]
    )

    subm1 = RecordSubm(
        subm1_xref,
        [
            Name('Luther'),
            SubmLang('en'),
            SubmLang('ja'),
            SubmLang('es'),
        ],
    )

    subm2 = RecordSubm(
        subm2_xref,
        [
            Name('GEDCOM 5.5.1'),
            Note('This contains the language tags for every language named in the v5.5.1 spec, namely: Afrikaans, Albanian, Amharic, Anglo-Saxon, Arabic, Armenian, Assamese, Belorusian, Bengali, Braj, Bulgarian, Burmese, Cantonese, Catalan, Catalan_Spn, Church-Slavic, Czech, Danish, Dogri, Dutch, English, Esperanto, Estonian, Faroese, Finnish, French, Georgian, German, Greek, Gujarati, Hawaiian, Hebrew, Hindi, Hungarian, Icelandic, Indonesian, Italian, Japanese, Kannada, Khmer, Konkani, Korean, Lahnda, Lao, Latvian, Lithuanian, Macedonian, Maithili, Malayalam, Mandrin, Manipuri, Marathi, Mewari, Navaho, Nepali, Norwegian, Oriya, Pahari, Pali, Panjabi, Persian, Polish, Portuguese, Prakrit, Pusto, Rajasthani, Romanian, Russian, Sanskrit, Serb, Serbo_Croa, Slovak, Slovene, Spanish, Swedish, Tagalog, Tamil, Telugu, Thai, Tibetan, Turkish, Ukrainian, Urdu, Vietnamese, Wendic, Yiddish'),
            SubmLang('af'),
            SubmLang('sq'),
            SubmLang('am'),
            SubmLang('ang'),
            SubmLang('ar'),
            SubmLang('hy'),
            SubmLang('as'),
            SubmLang('be'),
            SubmLang('bn'),
            SubmLang('bra'),
            SubmLang('bg'),
            SubmLang('my'),
            SubmLang('yue'),
            SubmLang('ca'),
            SubmLang('ca-ES'),
            SubmLang('cu'),
            SubmLang('cs'),
            SubmLang('da'),
            SubmLang('dgr'),
            SubmLang('nl'),
            SubmLang('en'),
            SubmLang('eo'),
            SubmLang('et'),
            SubmLang('fo'),
            SubmLang('fi'),
            SubmLang('fr'),
            SubmLang('ka'),
            SubmLang('de'),
            SubmLang('el'),
            SubmLang('gu'),
            SubmLang('haw'),
            SubmLang('he'),
            SubmLang('hi'),
            SubmLang('hu'),
            SubmLang('is'),
            SubmLang('id'),
            SubmLang('it'),
            SubmLang('ja'),
            SubmLang('kn'),
            SubmLang('km'),
            SubmLang('kok'),
            SubmLang('ko'),
            SubmLang('lah'),
            SubmLang('lo'),
            SubmLang('lv'),
            SubmLang('lt'),
            SubmLang('mk'),
            SubmLang('mai'),
            SubmLang('ml'),
            SubmLang('cmn'),
            SubmLang('mni'),
            SubmLang('mr'),
            SubmLang('mtr'),
            SubmLang('nv'),
            SubmLang('ne'),
            SubmLang('no'),
            SubmLang('or'),
            SubmLang('him'),
            SubmLang('pi'),
            SubmLang('pa'),
            SubmLang('fa'),
            SubmLang('pl'),
            SubmLang('pt'),
            SubmLang('pra'),
            SubmLang('ps'),
            SubmLang('raj'),
            SubmLang('ro'),
            SubmLang('ru'),
            SubmLang('sa'),
            SubmLang('sr'),
            SubmLang('sh'),
            SubmLang('sk'),
            SubmLang('sl'),
            SubmLang('es'),
            SubmLang('sv'),
            SubmLang('tl'),
            SubmLang('ta'),
            SubmLang('te'),
            SubmLang('th'),
            SubmLang('bo'),
            SubmLang('tr'),
            SubmLang('uk'),
            SubmLang('ur'),
            SubmLang('vi'),
            SubmLang('wen'),
            SubmLang('yi'),
        ],
    )

    gedcom = ''.join(
        [
            eval(head.code()).ged(), 
            eval(subm1.code()).ged(),
            eval(subm2.code()).ged(),
            eval(Trlr().code()).ged()
        ]
    )

    assert file == gedcom