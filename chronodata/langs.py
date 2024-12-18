# Licensed under a 3-clause BSD style license - see LICENSE.md
"""Add a dictionary to find the ISO 639-1 language code."""

from typing import ClassVar


class Lang:
    """ISO 639-1 codes for languages.

    The GEDCOM standard requires the use of ISO 639-1 codes for
    languages. These are identified with names and then placed
    in an enumeration list.  There are less than 200 of these
    codes.  A pandas display is provided to view them
    along with the other enumations.

    Reference
    ---------
    - [ISO 639-1 List](https://www.science.co.il/language/Codes.php)
    - [GEDCOM Standard]()
    """

    CODE: ClassVar = {
        'Afar': 'aa',
        'Abkhazian': 'ab',
        'Avestan': 'ae',
        'Afrikaans': 'af',
        'Akan': 'ak',
        'Amharic': 'am',
        'Aragonese': 'an',
        'Arabic': 'ar',
        'Assamese': 'as',
        'Avaric': 'av',
        'Aymara': 'ay',
        'Azerbaijani': 'az',
        'Bashkir': 'ba',
        'Belarusian': 'be',
        'Bulgarian': 'bg',
        'Bihari languages': 'bh',
        'Bislama': 'bi',
        'Bambara': 'bm',
        'Bengali': 'bn',
        'Tibetan': 'bo',
        'Breton': 'br',
        'Bosnian': 'bs',
        'Catalan': 'ca',
        'Valencian': 'ca',
        'Chechen': 'ce',
        'Chamorro': 'ch',
        'Corsican': 'co',
        'Cree': 'cr',
        'Czech': 'cs',
        'Church Slavic': 'cu',
        'Slavonic': 'cu',
        'Old Bulgarian': 'cu',
        'vieux bulgare Chuvash': 'cv',
        'Welsh': 'cy',
        'Danish': 'da',
        'German': 'de',
        'Divehi': 'dv',
        'Dhivehi': 'dv',
        'Maldivian': 'dv',
        'Dzongkha': 'dz',
        'Ewe': 'ee',
        'Greek, Modern (1453-)': 'el',
        'English': 'en',
        'Esperanto': 'eo',
        'Spanish; Castilian': 'es',
        'Estonian': 'et',
        'Basque': 'eu',
        'Persian': 'fa',
        'Fulah': 'ff',
        'Finnish': 'fi',
        'Fijian': 'fj',
        'Faroese': 'fo',
        'French': 'fr',
        'Western Frisian': 'fy',
        'Irish': 'ga',
        'Gaelic': 'gd',
        'Scottish Gaelic': 'gd',
        'Galician': 'gl',
        'Guarani': 'gn',
        'Gujarati': 'gu',
        'Manx': 'gv',
        'Hausa': 'ha',
        'Hebrew': 'he',
        'Hindi': 'hi',
        'Hiri Motu': 'ho',
        'Croatian': 'hr',
        'Haitian': 'ht',
        'Haitian Creole': 'ht',
        'Hungarian': 'hu',
        'Armenian': 'hy',
        'Herero': 'hz',
        'Interlingua': 'ia',
        'Indonesian': 'id',
        'Interlingue; Occidental': 'ie',
        'Igbo': 'ig',
        'Sichuan Yi; Nuosu': 'ii',
        'Inupiaq': 'ik',
        'Ido': 'io',
        'Icelandic': 'is',
        'Italian': 'it',
        'Inuktitut': 'iu',
        'Japanese': 'ja',
        'Javanese': 'jv',
        'Georgian': 'ka',
        'Kongo': 'kg',
        'Kikuyu; Gikuyu': 'ki',
        'Kuanyama; Kwanyama': 'kj',
        'Kazakh': 'kk',
        'Kalaallisut; Greenlandic': 'kl',
        'Central Khmer': 'km',
        'Kannada': 'kn',
        'Korean': 'ko',
        'Kanuri': 'kr',
        'Kashmiri': 'ks',
        'Kurdish': 'ku',
        'Komi': 'kv',
        'Cornish': 'kw',
        'Kirghiz; Kyrgyz': 'ky',
        'Latin': 'la',
        'Luxembourgish; Letzeburgesch': 'lb',
        'Ganda': 'lg',
        'Limburgan; Limburger; Limburgish': 'li',
        'Lingala': 'ln',
        'Lao': 'lo',
        'Lithuanian': 'lt',
        'Luba-Katanga': 'lu',
        'Latvian': 'lv',
        'Malagasy': 'mg',
        'Marshallese': 'mh',
        'Maori': 'mi',
        'Macedonian': 'mk',
        'Malayalam': 'ml',
        'Mongolian': 'mn',
        'Marathi': 'mr',
        'Malay': 'ms',
        'Maltese': 'mt',
        'Burmese': 'my',
        'Nauru': 'na',
        'Norwegian Bokmål': 'nb',
        'Ndebele, North': 'nd',
        'North Ndebele': 'nd',
        'Nepali': 'ne',
        'Ndonga': 'ng',
        'Dutch': 'nl',
        'Flemish': 'nl',
        'Norwegian Nynorsk': 'nn',
        'Norwegian': 'no',
        'Ndebele, South': 'nr',
        'South Ndebele': 'nr',
        'Navajo; Navaho': 'nv',
        'Chichewa': 'ny',
        'Chewa': 'ny',
        'Nyanja': 'ny',
        'Occitan (post 1500)': 'oc',
        'Ojibwa': 'oj',
        'Oromo': 'om',
        'Oriya': 'or',
        'Ossetian; Ossetic': 'os',
        'Panjabi; Punjabi': 'pa',
        'Pali': 'pi',
        'Polish': 'pl',
        'Pushto; Pashto': 'ps',
        'Portuguese': 'pt',
        'Quechua': 'qu',
        'Romansh': 'rm',
        'Rundi': 'rn',
        'Romanian': 'ro',
        'Moldavian': 'ro',
        'Moldovan': 'ro',
        'Russian': 'ru',
        'Kinyarwanda': 'rw',
        'Sanskrit': 'sa',
        'Sardinian': 'sc',
        'Sindhi': 'sd',
        'Northern Sami': 'se',
        'Sango': 'sg',
        'Sinhala': 'si',
        'Sinhalese': 'si',
        'Slovak': 'sk',
        'Slovenian': 'sl',
        'Samoan': 'sm',
        'Shona': 'sn',
        'Somali': 'so',
        'Albanian': 'sq',
        'Serbian': 'sr',
        'Swati': 'ss',
        'Sotho, Southern': 'st',
        'Sundanese': 'su',
        'Swedish': 'sv',
        'Swahili': 'sw',
        'Tamil': 'ta',
        'Telugu': 'te',
        'Tajik': 'tg',
        'Thai': 'th',
        'Tigrinya': 'ti',
        'Turkmen': 'tk',
        'Tagalog': 'tl',
        'Tswana': 'tn',
        'Tonga (Tonga Islands)': 'to',
        'Turkish': 'tr',
        'Tsonga': 'ts',
        'Tatar': 'tt',
        'Twi': 'tw',
        'Tahitian': 'ty',
        'Uighur': 'ug',
        'Uyghur': 'ug',
        'Ukrainian': 'uk',
        'Urdu': 'ur',
        'Uzbek': 'uz',
        'Venda': 've',
        'Vietnamese': 'vi',
        'Volapük': 'vo',
        'Walloon': 'wa',
        'Wolof': 'wo',
        'Xhosa': 'xh',
        'Yiddish': 'yi',
        'Yoruba': 'yo',
        'Zhuang': 'za',
        'Chuang': 'za',
        'Chinese': 'zh',
        'Zulu': 'zu',
    }
