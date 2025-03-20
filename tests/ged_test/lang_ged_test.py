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


def test_lang_ged() -> None:
    # Test constructing the remarriage2_ged test data.

    file = """0 HEAD
1 GEDC
2 VERS 7.0
1 NOTE This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.
1 SOUR TEST_FILES
1 SUBM @1@
1 LANG af
1 SCHMA
2 TAG _PHRASE https://gedcom.io/terms/v7/PHRASE
0 @1@ SUBM
1 NAME Luther
1 LANG en
1 LANG ja
1 LANG es
0 @2@ SUBM
1 NAME GEDCOM 5.5.1
1 NOTE This contains the language tags for every language named in the v5.5.1 spec, namely: Afrikaans, Albanian, Amharic, Anglo-Saxon, Arabic, Armenian, Assamese, Belorusian, Bengali, Braj, Bulgarian, Burmese, Cantonese, Catalan, Catalan_Spn, Church-Slavic, Czech, Danish, Dogri, Dutch, English, Esperanto, Estonian, Faroese, Finnish, French, Georgian, German, Greek, Gujarati, Hawaiian, Hebrew, Hindi, Hungarian, Icelandic, Indonesian, Italian, Japanese, Kannada, Khmer, Konkani, Korean, Lahnda, Lao, Latvian, Lithuanian, Macedonian, Maithili, Malayalam, Mandrin, Manipuri, Marathi, Mewari, Navaho, Nepali, Norwegian, Oriya, Pahari, Pali, Panjabi, Persian, Polish, Portuguese, Prakrit, Pusto, Rajasthani, Romanian, Russian, Sanskrit, Serb, Serbo_Croa, Slovak, Slovene, Spanish, Swedish, Tagalog, Tamil, Telugu, Thai, Tibetan, Turkish, Ukrainian, Urdu, Vietnamese, Wendic, Yiddish
1 LANG af
1 LANG sq
1 LANG am
1 LANG ang
1 LANG ar
1 LANG hy
1 LANG as
1 LANG be
1 LANG bn
1 LANG bra
1 LANG bg
1 LANG my
1 LANG yue
1 LANG ca
1 LANG ca-ES
1 LANG cu
1 LANG cs
1 LANG da
1 LANG dgr
1 LANG nl
1 LANG en
1 LANG eo
1 LANG et
1 LANG fo
1 LANG fi
1 LANG fr
1 LANG ka
1 LANG de
1 LANG el
1 LANG gu
1 LANG haw
1 LANG he
1 LANG hi
1 LANG hu
1 LANG is
1 LANG id
1 LANG it
1 LANG ja
1 LANG kn
1 LANG km
1 LANG kok
1 LANG ko
1 LANG lah
1 LANG lo
1 LANG lv
1 LANG lt
1 LANG mk
1 LANG mai
1 LANG ml
1 LANG cmn
1 LANG mni
1 LANG mr
1 LANG mtr
1 LANG nv
1 LANG ne
1 LANG no
1 LANG or
1 LANG him
1 LANG pi
1 LANG pa
1 LANG fa
1 LANG pl
1 LANG pt
1 LANG pra
1 LANG ps
1 LANG raj
1 LANG ro
1 LANG ru
1 LANG sa
1 LANG sr
1 LANG sh
1 LANG sk
1 LANG sl
1 LANG es
1 LANG sv
1 LANG tl
1 LANG ta
1 LANG te
1 LANG th
1 LANG bo
1 LANG tr
1 LANG uk
1 LANG ur
1 LANG vi
1 LANG wen
1 LANG yi
0 TRLR"""

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