# prep.py
"""Utilities to turn GEDCOM specifications into a module of dictionaries and a module of classes
specific to a GEDCOM version.

There are three classes of static methods, `Construct` and `Convert`. A class of keys to the
specific types of specifications and one dictionary, `Examples`.

- Convert: From a version of the GEDCOM specifications convert the yaml files into python dictionaries.
    This is run from a notebook and the output copied to a module called gedcomx.py where x
    is the version number.
- Construct: Obtains a version of the GEDCOM specifications from `Convert` and generates
    a python class from each structure.  This is run from a notebook and the output copied
    to a module called structuresx.py where x is the version number.
- Examples: Code examples that will go into a specific class when `Construct` generates the class.
- Keys: OrderedSets of string which when combined with a beginning url and ".yaml"
    retrieve the specification.

The classes and specs modules are generated from methods in this module.
This is the module to change if one wants to modify the classes or specs modules.
"""

__all__ = [
    'Construct',
    'Convert',
]


from dataclasses import dataclass
from textwrap import wrap
from typing import Any

from ordered_set import OrderedSet  # type: ignore[import-not-found]

from genedata.constants import Config, Default
from genedata.util import Util


@dataclass
class Keys:
    CALENDARS = OrderedSet(
        [
            'FRENCH_R',
            'GREGORIAN',
            'HEBREW',
            'JULIAN',
        ]
    )
    DATATYPES = OrderedSet(
        [
            'Age',
            'Date',
            'Enum',
            'FilePath',
            'List',
            'Name',
            'Time',
        ]
    )
    ENUMERATIONS = OrderedSet(
        [
            '0',
            '1',
            '2',
            '3',
            'ADOP-HUSB',
            'ADOP-WIFE',
            'ADOPTED',
            'AKA',
            'AUDIO',
            'BIC',
            'BIRTH',
            'BOOK',
            'BOTH',
            'CANCELED',
            'CARD',
            'CENS',
            'CHALLENGED',
            'CHIL',
            'CHILD',
            'CLERGY',
            'COMPLETED',
            'CONFIDENTIAL',
            'DISPROVEN',
            'DNS_CAN',
            'DNS',
            'ELECTRONIC',
            'EVEN',
            'EXCLUDED',
            'F',
            'FACT',
            'FATH',
            'FICHE',
            'FILM',
            'FOSTER',
            'FRIEND',
            'GODP',
            'HUSB',
            'IMMIGRANT',
            'INFANT',
            'LOCKED',
            'M',
            'MAGAZINE',
            'MAIDEN',
            'MANUSCRIPT',
            'MAP',
            'MARRIED',
            'MOTH',
            'MULTIPLE',
            'NCHI',
            'NEWSPAPER',
            'NGHBR',
            'OFFICIATOR',
            'OTHER',
            'PARENT',
            'PHOTO',
            'PRE_1970',
            'PRIVACY',
            'PROFESSIONAL',
            'PROVEN',
            'RESI',
            'SEALING',
            'SPOU',
            'STILLBORN',
            'SUBMITTED',
            'TOMBSTONE',
            'U',
            'UNCLEARED',
            'VIDEO',
            'WIFE',
            'WITN',
            'X',
        ]
    )
    ENUMERATION_SETS = OrderedSet(
        [
            'ADOP',
            'EVEN',
            'EVENATTR',
            'FAMC-STAT',
            'MEDI',
            'NAME-TYPE',
            'ord-STAT',
            'PEDI',
            'QUAY',
            'RESN',
            'ROLE',
            'SEX',
        ]
    )
    MONTHS = OrderedSet(
        [
            'AAV',
            'ADR',
            'ADS',
            'APR',
            'AUG',
            'BRUM',
            'COMP',
            'CSH',
            'DEC',
            'ELL',
            'FEB',
            'FLOR',
            'FRIM',
            'FRUC',
            'GERM',
            'IYR',
            'JAN',
            'JUL',
            'JUN',
            'KSL',
            'MAR',
            'MAY',
            'MESS',
            'NIVO',
            'NOV',
            'NSN',
            'OCT',
            'PLUV',
            'PRAI',
            'SEP',
            'SHV',
            'SVN',
            'THER',
            'TMZ',
            'TSH',
            'TVT',
            'VEND',
            'VENT',
        ]
    )
    STRUCTURES = OrderedSet(
        [
            'ABBR',
            'ADDR',
            'ADOP',
            'ADOP-FAMC',
            'ADR1',
            'ADR2',
            'ADR3',
            'AGE',
            'AGNC',
            'ALIA',
            'ANCI',
            'ANUL',
            'ASSO',
            'AUTH',
            'BAPL',
            'BAPM',
            'BARM',
            'BASM',
            'BIRT',
            'BLES',
            'BURI',
            'CALN',
            'CAST',
            'CAUS',
            'CHAN',
            'CHIL',
            'CHR',
            'CHRA',
            'CITY',
            'CONF',
            'CONL',
            'CONT',
            'COPR',
            'CORP',
            'CREA',
            'CREM',
            'CROP',
            'CTRY',
            'DATA',
            'DATA-EVEN',
            'DATA-EVEN-DATE',
            'DATE',
            'DATE-exact',
            'DEAT',
            'DESI',
            'DEST',
            'DIV',
            'DIVF',
            'DSCR',
            'EDUC',
            'EMAIL',
            'EMIG',
            'ENDL',
            'ENGA',
            'EXID',
            'EXID-TYPE',
            'FAM-CENS',
            'FAM-EVEN',
            'FAM-FACT',
            'FAM-HUSB',
            'FAM-NCHI',
            'FAM-RESI',
            'FAM-WIFE',
            'FAMC',
            'FAMC-ADOP',
            'FAMC-STAT',
            'FAMS',
            'FAX',
            'FCOM',
            'FILE',
            'FILE-TRAN',
            'FORM',
            'GEDC',
            'GEDC-VERS',
            'GIVN',
            'GRAD',
            'HEAD',
            'HEAD-DATE',
            'HEAD-LANG',
            'HEAD-PLAC',
            'HEAD-PLAC-FORM',
            'HEAD-SOUR',
            'HEAD-SOUR-DATA',
            'HEIGHT',
            'HUSB',
            'IDNO',
            'IMMI',
            'INDI-CENS',
            'INDI-EVEN',
            'INDI-FACT',
            'INDI-FAMC',
            'INDI-NAME',
            'INDI-NCHI',
            'INDI-RELI',
            'INDI-TITL',
            'INIL',
            'LANG',
            'LATI',
            'LEFT',
            'LONG',
            'MAP',
            'MARB',
            'MARC',
            'MARL',
            'MARR',
            'MARS',
            'MEDI',
            'MIME',
            'NAME',
            'NAME-TRAN',
            'NAME-TYPE',
            'NATI',
            'NATU',
            'NICK',
            'NMR',
            'NO-DATE',
            'NOTE',
            'NOTE-TRAN',
            'NPFX',
            'NSFX',
            'OBJE',
            'OCCU',
            'ord-STAT',
            'ORDN',
            'PAGE',
            'PEDI',
            'PHON',
            'PHRASE',
            'PLAC',
            'PLAC-FORM',
            'PLAC-TRAN',
            'POST',
            'PROB',
            'PUBL',
            'QUAY',
            'record-FAM',
            'record-INDI',
            'record-OBJE',
            'record-REPO',
            'record-SNOTE',
            'record-SOUR',
            'record-SUBM',
            'REFN',
            'RELI',
            'REPO',
            'RESN',
            'RETI',
            'ROLE',
            'SCHMA',
            'SDATE',
            'SEX',
            'SLGC',
            'SLGS',
            'SNOTE',
            'SOUR',
            'SOUR-DATA',
            'SOUR-EVEN',
            'SPFX',
            'SSN',
            'STAE',
            'SUBM',
            'SUBM-LANG',
            'SURN',
            'TAG',
            'TEMP',
            'TEXT',
            'TIME',
            'TITL',
            'TOP',
            'TRLR',
            'TYPE',
            'UID',
            'VERS',
            'WIDTH',
            'WIFE',
            'WILL',
            'WWW',
        ]
    )
    STRUCTURE_EXTENSIONS = OrderedSet(['_DATE', '_SOUR'])
    URIS = OrderedSet(
        [
            'AFN',
            'BillionGraves-CemeteryId',
            'BillionGraves-GraveId',
            'FamilySearch-MemoryId',
            'FamilySearch-PersonId',
            'FamilySearch-PlaceId',
            'FamilySearch-SourceDescriptionId',
            'FamilySearch-UserId',
            'FindAGrave-CemeteryId',
            'FindAGrave-MemorialId',
            'GOV-ID',
            'RFN',
            'RIN',
            'WikiTree-PersonId',
        ]
    )


class Convert:
    @staticmethod
    def preamble(source: str, version: str) -> str:
        lines: str = f'''"""Store the GEDCOM verson {version} specifications in a dictionary format from yaml files.
This is a generated module. DO NOT MODIFY IT MANUALLY.  Changes should be made to the `Convert` class 
in the `prep` module.

The specification was obtained from the [GEDCOM-registeries]({source})
made available under an Apache 2.0 license.

The names of the dictionaries are based on the directories in this registry.  Each yaml file
in the directory is read into a dictionary which is then added to a dictionary named after
the directory.  Other keys besides those in the yaml file have been added
to assist this application to read and write ged files.

The following dictionaries are available.  Each item in the dictionary corresponds to a
single yaml file.
- `Calendar` corresponding to yaml files in the calendar directory.
- `DataType` corresponding to yaml files in the data-type directory.
- `Enumeration` corresponding to yaml files in the enumeration directory.
- `EnumerationSet` corresponding to yaml files in the enumeration-set directory.
- `Month` corresponding to yaml files in the month directory.
- `Structure` corresponding to yaml files in the structure/standard directory.
- `ExtensionStructure` corresponding to yaml files in the structure/extenion directory.
- `Uri` corresponding to yaml files in the uri directory.

Methods from this class read data from the yaml files to construct the
dictionaries mentioned above which are copied to a python file.

Reference:
    [GEDCOM-registeries]({source})
"""

__all__ = [
    'Calendar',
    'DataType',
    'Enumeration',
    'EnumerationSet',
    'ExtensionStructure',
    'Month',
    'Structure',
    'Uri',
]

from typing import Any

'''
        return lines

    @staticmethod
    def calendar(url: str) -> str:
        # path_start = url
        if url[-1] == Default.SLASH:
            path_start: str = f'{url}{Default.URL_CALENDAR}'
        else:
            path_start = f'{url}{Default.SLASH}{Default.URL_CALENDAR}'
        path_end = '.yaml'
        lines: str = 'Calendar: dict[str, dict[str, Any]] = {'
        for item in Keys.CALENDARS:
            yamldict = Util.read_yaml(f'{path_start}{item}{path_end}')
            lines = f"{lines}\n    '{item}': {yamldict},"
        return ''.join([lines, Default.EOL, '}\n\n'])

    @staticmethod
    def datatype(url: str) -> str:
        # path_start = url
        if url[-1] == Default.SLASH:
            path_start: str = f'{url}{Default.URL_DATATYPE}'
        else:
            path_start = f'{url}{Default.SLASH}{Default.URL_DATATYPE}'
        path_end = '.yaml'
        lines: str = 'DataType: dict[str, dict[str, Any]] = {'
        for item in Keys.DATATYPES:
            yamldict = Util.read_yaml(f'{path_start}{item}{path_end}')
            lines = f"{lines}\n    '{item}': {yamldict},"
        return ''.join([lines, Default.EOL, '}\n\n'])

    @staticmethod
    def enumeration_dictionary(url: str) -> str:
        # path_start = url
        if url[-1] == Default.SLASH:
            path_start: str = f'{url}{Default.URL_ENUMERATION}'
        else:
            path_start = f'{url}{Default.SLASH}{Default.URL_ENUMERATION}'
        path_end = '.yaml'
        # lines: str = 'Enumeration: dict[str, dict[str, Any]] = {'
        lines: str = '{'
        for item in Keys.ENUMERATIONS:
            yamldict = Util.read_yaml(f'{path_start}{item}{path_end}')
            lines = f"{lines}'{item}': {yamldict}, "
        return ''.join([lines, Default.EOL, '}\n'])

    @staticmethod
    def enumeration(url: str) -> str:
        # path_start = url
        if url[-1] == Default.SLASH:
            path_start: str = f'{url}{Default.URL_ENUMERATION}'
        else:
            path_start = f'{url}{Default.SLASH}{Default.URL_ENUMERATION}'
        path_end = '.yaml'
        lines: str = 'Enumeration: dict[str, dict[str, Any]] = {'
        for item in Keys.ENUMERATIONS:
            yamldict = Util.read_yaml(f'{path_start}{item}{path_end}')
            lines = f"{lines}\n    '{item}': {yamldict},"
        return ''.join([lines, Default.EOL, '}\n\n'])

    @staticmethod
    def enumerationset(url: str) -> str:
        # path_start = url
        if url[-1] == Default.SLASH:
            path_start: str = f'{url}{Default.URL_ENUMERATION_SET}'
        else:
            path_start = f'{url}{Default.SLASH}{Default.URL_ENUMERATION_SET}'
        path_end = '.yaml'
        lines: str = 'EnumerationSet: dict[str, dict[str, Any]] = {'
        for item in Keys.ENUMERATION_SETS:
            yamldict = Util.read_yaml(f'{path_start}{item}{path_end}')
            lines = f"{lines}\n    '{item}': {yamldict},"
        return ''.join([lines, Default.EOL, '}\n\n'])

    @staticmethod
    def month(url: str) -> str:
        # path_start = url
        if url[-1] == Default.SLASH:
            path_start: str = f'{url}{Default.URL_MONTH}'
        else:
            path_start = f'{url}{Default.SLASH}{Default.URL_MONTH}'
        path_end = '.yaml'
        lines: str = 'Month: dict[str, dict[str, Any]] = {'
        for item in Keys.MONTHS:
            yamldict = Util.read_yaml(f'{path_start}{item}{path_end}')
            lines = f"{lines}\n    '{item}': {yamldict},"
        return ''.join([lines, Default.EOL, '}\n\n'])

    @staticmethod
    def structure_dictionary(url: str) -> str:
        # path_start = url
        if url[-1] == Default.SLASH:
            path_start: str = f'{url}{Default.URL_STRUCTURE}'
        else:
            path_start = f'{url}{Default.SLASH}{Default.URL_STRUCTURE}'
        path_end = '.yaml'
        # lines: str = 'Structure: dict[str, dict[str, Any]] = {'
        enumeration: dict[str, Any] = eval(Convert.enumeration_dictionary(url))
        lines: str = '{'
        for item in Keys.STRUCTURES:
            yamldict = Util.read_yaml(f'{path_start}{item}{path_end}')
            required = []
            single = []
            permitted = []
            enums = []
            if Default.YAML_SUBSTRUCTURES in yamldict:
                for key, value in yamldict[Default.YAML_SUBSTRUCTURES].items():
                    tag = (
                        key[key.rfind(Default.SLASH) + 1 :]
                        .title()
                        .replace('-', '')
                    )
                    permitted.append(tag)
                    if Default.YAML_CARDINALITY_REQUIRED in value:
                        required.append(tag)
                    if Default.YAML_CARDINALITY_SINGULAR in value:
                        single.append(tag)
            yamldict[Default.YAML_PERMITTED] = permitted
            yamldict[Default.YAML_REQUIRED] = required
            yamldict[Default.YAML_SINGULAR] = single
            if Default.YAML_ENUMERATION_SET in yamldict:
                enumset = yamldict[Default.YAML_ENUMERATION_SET]
                for key, value in enumeration.items():  # noqa: B007
                    if enumset in value[Default.YAML_VALUE_OF]:
                        enums.append(value[Default.YAML_STANDARD_TAG])
            yamldict[Default.YAML_ENUMS] = enums
            yamldict[Default.YAML_CLASS_NAME] = (
                item.title().replace('_', '').replace('-', '')
            )
            lines = f"{lines}'{item}': {yamldict}, "
        return ''.join([lines, Default.EOL, '}\n'])

    @staticmethod
    def structure(url: str) -> str:
        if url[-1] == Default.SLASH:
            path_start: str = f'{url}{Default.URL_STRUCTURE}'
        else:
            path_start = f'{url}{Default.SLASH}{Default.URL_STRUCTURE}'
        path_end = '.yaml'
        enumeration: dict[str, Any] = eval(Convert.enumeration_dictionary(url))
        lines: str = 'Structure: dict[str, dict[str, Any]] = {'
        for item in Keys.STRUCTURES:
            yamldict = Util.read_yaml(f'{path_start}{item}{path_end}')
            required = []
            single = []
            permitted = []
            enums = []
            if Default.YAML_SUBSTRUCTURES in yamldict:
                for key, value in yamldict[Default.YAML_SUBSTRUCTURES].items():
                    tag = (
                        key[key.rfind(Default.SLASH) + 1 :]
                        .title()
                        .replace('-', '')
                    )
                    permitted.append(tag)
                    if Default.YAML_CARDINALITY_REQUIRED in value:
                        required.append(tag)
                    if Default.YAML_CARDINALITY_SINGULAR in value:
                        single.append(tag)
            yamldict[Default.YAML_PERMITTED] = permitted
            yamldict[Default.YAML_REQUIRED] = required
            yamldict[Default.YAML_SINGULAR] = single
            if Default.YAML_ENUMERATION_SET in yamldict:
                enumset = yamldict[Default.YAML_ENUMERATION_SET]
                for key, value in enumeration.items():  # noqa: B007
                    if enumset in value[Default.YAML_VALUE_OF]:
                        enums.append(value[Default.YAML_STANDARD_TAG])
            yamldict[Default.YAML_ENUMS] = enums
            yamldict[Default.YAML_CLASS_NAME] = (
                item.title().replace('_', '').replace('-', '')
            )
            lines = f"{lines}\n    '{item}': {yamldict},"
        return ''.join([lines, Default.EOL, '}\n\n'])

    @staticmethod
    def structure_extension(url: str) -> str:
        # path_start = url
        if url[-1] == Default.SLASH:
            path_start: str = f'{url}{Default.URL_STRUCTURE_EXTENSION}'
        else:
            path_start = (
                f'{url}{Default.SLASH}{Default.URL_STRUCTURE_EXTENSION}'
            )
        path_end = '.yaml'
        enumeration: dict[str, Any] = eval(Convert.enumeration_dictionary(url))
        lines: str = 'ExtensionStructure: dict[str, dict[str, Any]] = {'
        for item in Keys.STRUCTURE_EXTENSIONS:
            yamldict = Util.read_yaml(f'{path_start}{item}{path_end}')
            required = []
            single = []
            permitted = []
            enums = []
            if Default.YAML_SUBSTRUCTURES in yamldict:
                for key, value in yamldict[Default.YAML_SUBSTRUCTURES].items():
                    tag = (
                        key[key.rfind(Default.SLASH) + 1 :]
                        .title()
                        .replace('-', '')
                    )
                    permitted.append(tag)
                    if Default.YAML_CARDINALITY_REQUIRED in value:
                        required.append(tag)
                    if Default.YAML_CARDINALITY_SINGULAR in value:
                        single.append(tag)
            yamldict[Default.YAML_PERMITTED] = permitted
            yamldict[Default.YAML_REQUIRED] = required
            yamldict[Default.YAML_SINGULAR] = single
            if Default.YAML_ENUMERATION_SET in yamldict:
                enumset = yamldict[Default.YAML_ENUMERATION_SET]
                for key, value in enumeration.items():  # noqa: B007
                    if enumset in value[Default.YAML_VALUE_OF]:
                        enums.append(value[Default.YAML_STANDARD_TAG])
            yamldict[Default.YAML_ENUMS] = enums
            yamldict[Default.YAML_CLASS_NAME] = (
                item.title().replace('_', '').replace('-', '')
            )
            lines = f"{lines}\n    '{item}': {yamldict},"
        return ''.join([lines, Default.EOL, '}\n\n'])

    @staticmethod
    def uri(url: str) -> str:
        # path_start = url
        if url[-1] == Default.SLASH:
            path_start: str = f'{url}{Default.URL_URI}'
        else:
            path_start = f'{url}{Default.SLASH}{Default.URL_URI}'
        path_end = '.yaml'
        lines: str = 'Uri: dict[str, dict[str, Any]] = {'
        for item in Keys.URIS:
            yamldict = Util.read_yaml(f'{path_start}{item}{path_end}')
            lines = f"{lines}\n    '{item}': {yamldict},"
        return ''.join([lines, Default.EOL, '}\n\n'])

    @staticmethod
    def build_all(source: str, version: str, url: str) -> str:
        return ''.join(
            [
                Convert.preamble(source, version),
                Convert.calendar(url),
                Convert.datatype(url),
                Convert.enumeration(url),
                Convert.enumerationset(url),
                Convert.month(url),
                Convert.structure(url),
                Convert.structure_extension(url),
                Convert.uri(url),
            ]
        )


Examples: dict[str, str] = {
    'LATI': f"""

    Examples:
        The following example shows how to enter the latitude (Lati))
        coordinates into a Map structure to produce the GEDCOM example
        mentioned in the GEDCOM Specification section.
        >>> from genedata.classes{Config.VERSION} import Lati, Long, Map
        >>> m = Map([Lati('N18.150944'), Long('E168.150944')])
        >>> print(m.ged())
        1 MAP
        2 LATI N18.150944
        2 LONG E168.150944
        <BLANKLINE>
        
        Since it may be difficult to convert from degrees, minutes
        and seconds to a floating point value, the `Input` class provides
        a utility to do so for Lati.  A similar one exists for Long.
        >>> from genedata.util import Input
        >>> m = Map(
        ...     [
        ...         Lati(Input.lati(18, 9, 3.4)), 
        ...         Long('E168.150944'),
        ...     ]
        ... )
        >>> print(m.ged())
        1 MAP
        2 LATI N18.150944
        2 LONG E168.150944
        <BLANKLINE>""",
    'LONG': f"""

    Examples:
        The following example howss how to enter the longitude (Long)
        coordinates into a map structure to produce the GEDCOM output
        mentioned in the GEDCOM Specification.
        >>> from genedata.classes{Config.VERSION} import Lati, Long, Map
        >>> m = Map([Lati('N18.150944'), Long('E168.150944')])
        >>> print(m.ged())
        1 MAP
        2 LATI N18.150944
        2 LONG E168.150944
        <BLANKLINE>
        
        Since it may be difficult to convert from degrees, minutes
        and seconds to a floating point value, the `Input` class provides
        a utility to do so for Long.  A similar one exists for Lati.
        >>> from genedata.util import Input
        >>> m = Map(
        ...     [
        ...         Lati('N18.150944'), 
        ...         Long(Input.long(168, 9, 3.4)),
        ...     ]
        ... )
        >>> print(m.ged())
        1 MAP
        2 LATI N18.150944
        2 LONG E168.150944
        <BLANKLINE>""",
    'MAP': f"""

    Examples:
        The following example illustrates how to enter latitude (Lati) and longitude (Long)
        coordinates into a map structure to produce the GEDCOM output.
        >>> from genedata.util import Input
        >>> from genedata.classes{Config.VERSION} import Lati, Long, Map
        >>> m = Map([Lati('N18.150944'), Long('E168.150944')])
        >>> print(m.ged())
        1 MAP
        2 LATI N18.150944
        2 LONG E168.150944
        <BLANKLINE>""",
    'MEDI': f"""

    Examples:
        These are the steps to build the example in the specification.
        First import the classes and build a multimedia cross reference identifier.
        >>> from genedata.build import Genealogy
        >>> from genedata.classes{Config.VERSION} import File, Form, Medi, RecordObje
        >>> g = Genealogy('example')
        >>> obje_xref = g.multimedia_xref('M1')

        Next construct the ged lines.  Let `photo.jpg` be the file name of the photo.
        >>> m = RecordObje(obje_xref, File('photo.jpg', Form('image/jpeg', Medi('PHOTO'))))
        >>> print(m.ged())
        0 @M1@ OBJE
        1 FILE photo.jpg
        2 FORM image/jpeg
        3 MEDI PHOTO
        <BLANKLINE>

        This example shows a successful run of the Medi structure using
        the enumeration value 'AUDIO'.
        >>> from genedata.classes{Config.VERSION} import Medi
        >>> m = Medi('AUDIO')
        >>> print(m.ged(2))
        2 MEDI AUDIO
        <BLANKLINE>

        This example shows the code that is generated to produce the same result as above.
        >>> print(m.code())
        <BLANKLINE>
        Medi('AUDIO')""",
    'NAME-TRAN': f"""

    Example:
        These are the steps to build the example in the specification.
        First the classes are imported which construct the ged lines.
        >>> from genedata.classes{Config.VERSION} import Givn, IndiName, Lang, NameTran, Surn
        >>> m = IndiName('/孔/德庸',
        ...         [
        ...             Givn('德庸'),
        ...             Surn('孔'),
        ...             NameTran('/Kǒng/ Déyōng',
        ...                 [
        ...                     Givn('Déyōng'),
        ...                     Surn('Kǒng'),
        ...                     Lang('zh-pinyin'),
        ...                 ]
        ...             )
        ...         ]
        ... )
        >>> print(m.ged(1))
        1 NAME /孔/德庸
        2 GIVN 德庸
        2 SURN 孔
        2 TRAN /Kǒng/ Déyōng
        3 GIVN Déyōng
        3 SURN Kǒng
        3 LANG zh-pinyin
        <BLANKLINE>""",
    'NOTE-TRAN': f"""

    Example:
        These are the steps to build the example in the specification.
        First the classes are imported which construct the ged lines.
        >>> from genedata.classes{Config.VERSION} import Lang, Mime, Name, Note, NoteTran
        >>> m = IndiName('Arete /Hernandez/', 
        ...     Note('Named after Arete from <i>The Odyssey</i>',
        ...         [
        ...             Lang('en'),
        ...             Mime('text/html'),
        ...             NoteTran('Named after Arete from "The Odyssey"', Mime('text/plain')),
        ...             NoteTran('Nombrada en honor a Arete de <i>La Odisea</i>', Lang('es')),
        ...         ]
        ...     )
        ... ) 
        >>> print(m.ged(1))
        1 NAME Arete /Hernandez/
        2 NOTE Named after Arete from <i>The Odyssey</i>
        3 LANG en
        3 MIME text/html
        3 TRAN Named after Arete from "The Odyssey"
        4 MIME text/plain
        3 TRAN Nombrada en honor a Arete de <i>La Odisea</i>
        4 LANG es
        <BLANKLINE>""",
    'ord-STAT': f"""

    Examples:
        This example shows a successful run of the OrdStat structure using
        the enumeration value 'BIC' occurring on January 15, 2020.
        >>> from genedata.classes{Config.VERSION} import DateExact, OrdStat
        >>> m = OrdStat('BIC', DateExact('15 JAN 2020'))
        >>> print(m.ged(1))
        1 STAT BIC
        2 DATE 15 JAN 2020
        <BLANKLINE>

        This example shows the code that is generated to produce the same result as above.
        >>> print(m.code())
        <BLANKLINE>
        OrdStat('BIC', DateExact('15 JAN 2020'))""",
    'PAGE': f"""

    Examples:
        These are the steps to build the examples in the specification.
        First we will import the classes and then create a source cross reference `S1`.
        The void cross reference identifier comes from the Void class.
        >>> from genedata.build import Genealogy
        >>> from genedata.classes{Config.VERSION} import Dscr, Page, Sour 
        >>> from genedata.structure import Void
        >>> g = Genealogy('example')
        >>> sour_xref = g.source_xref('S1')

        These are the steps to build the first example:
        >>> m = Sour(sour_xref, Page('Film: 1234567, Frame: 344, Line: 28'))
        >>> print(m.ged(2))
        2 SOUR @S1@
        3 PAGE Film: 1234567, Frame: 344, Line: 28
        <BLANKLINE>

        These are the steps to build the second example:
        >>> m = Dscr('Tall enough his head touched the ceiling', Sour(Void.SOUR, Page('His grand-daughter Lydia told me this in 1980')))
        >>> print(m.ged(1))
        1 DSCR Tall enough his head touched the ceiling
        2 SOUR @VOID@
        3 PAGE His grand-daughter Lydia told me this in 1980
        <BLANKLINE>""",
    'PEDI': f"""

    Examples:
        This example shows a successful run of the Pedi structure using
        the enumeration value 'ADOPTED'.
        >>> from genedata.classes{Config.VERSION} import Pedi
        >>> m = Pedi('ADOPTED')
        >>> print(m.ged(1))
        1 PEDI ADOPTED
        <BLANKLINE>

        This example shows the code that is generated to produce the same result as above.
        >>> print(m.code())
        <BLANKLINE>
        Pedi('ADOPTED')""",
    'PHRASE': f"""

    Examples:
        The following steps would generate the examples in the specification.
        We will need the following imports for these examples along with one
        individual cross reference identifier `I2` for the fifth example:
        >>> from genedata.classes{Config.VERSION} import Asso, Date, Givn, Marr, Name, Phrase, Role, Type
        >>> from genedata.build import Genealogy
        >>> g = Genealogy('example')
        >>> indi = g.individual_xref('I2')
        
        These are the steps for the first example.
        >>> m = Date('24 JUN 1852', Phrase('During the feast of St John'))
        >>> print(m.ged(2))
        2 DATE 24 JUN 1852
        3 PHRASE During the feast of St John
        <BLANKLINE>

        These are the steps for the second example.
        >>> m = Date('30 JAN 1649', Phrase('30th of January, 1648/9'))
        >>> print(m.ged(2))
        2 DATE 30 JAN 1649
        3 PHRASE 30th of January, 1648/9
        <BLANKLINE>

        These are the steps for the third example.
        >>> m = Date('BET 1648 AND 1649', Phrase('1648/9'))
        >>> print(m.ged(2))
        2 DATE BET 1648 AND 1649
        3 PHRASE 1648/9
        <BLANKLINE>

        These are the steps for the fourth example.
        >>> m = Date('BET 1 JAN 1867 AND 31 MAR 1867', Phrase('Q1 1867'))
        >>> print(m.ged(2))
        2 DATE BET 1 JAN 1867 AND 31 MAR 1867
        3 PHRASE Q1 1867
        <BLANKLINE>

        These are the steps for the fifth example.
        >>> m = Marr('', Asso(indi, Role('OTHER', Phrase('Maid of Honor'))))
        >>> print(m.ged(1))
        1 MARR
        2 ASSO @I2@
        3 ROLE OTHER
        4 PHRASE Maid of Honor
        <BLANKLINE>""",
    'PLAC': f"""

    Example:
        The following steps would generate the example in the specification.  
        First create source cross reference identifier `S1` and then build the ged lines
        in a RecordSour.
        >>> from genedata.classes{Config.VERSION} import Plac, PlacForm, RecordSour, Data, DataEven
        >>> from genedata.build import Genealogy
        >>> g = Genealogy('example')
        >>> sour = g.source_xref('S1')
        >>> m = RecordSour(sour, Data(DataEven('BIRT', Plac(', Oneida, Idaho, USA', PlacForm('City, County, State, Country')))))
        >>> print(m.ged())
        0 @S1@ SOUR
        1 DATA
        2 EVEN BIRT
        3 PLAC , Oneida, Idaho, USA
        4 FORM City, County, State, Country
        <BLANKLINE>""",
    'PLAC-FORM': f"""

    Example:
        The following steps would generate the example in the specifications:
        >>> from genedata.classes{Config.VERSION} import Plac, PlacForm
        >>> m = Plac('Baltimore, , Maryland, USA', PlacForm('City, County, State, Country'))
        >>> print(m.ged(2))
        2 PLAC Baltimore, , Maryland, USA
        3 FORM City, County, State, Country
        <BLANKLINE>""",
    'PLAC-TRAN': f"""

    Example:
        The following steps would generate the example in the specifications.
        >>> from genedata.classes{Config.VERSION} import PlacForm, Lang, PlacTran, Plac, PlacTran
        >>> m = Plac('千代田, 東京, 日本',
        ...     [
        ...         PlacForm('区, 都, 国'),
        ...         Lang('ja'),
        ...         PlacTran('Chiyoda, Tokyo, Nihon', Lang('ja-Latn')),
        ...         PlacTran('Chiyoda, Tokyo, Japan', Lang('en')),
        ...     ]
        ... )
        >>> print(m.ged(2))
        2 PLAC 千代田, 東京, 日本
        3 FORM 区, 都, 国
        3 LANG ja
        3 TRAN Chiyoda, Tokyo, Nihon
        4 LANG ja-Latn
        3 TRAN Chiyoda, Tokyo, Japan
        4 LANG en
        <BLANKLINE>""",
    'QUAY': f"""

    Examples:
        This example shows a successful run of the Quay structure using
        the enumeration value '0'.
        >>> from genedata.classes{Config.VERSION} import Quay
        >>> m = Quay('0')
        >>> print(m.ged(1))
        1 QUAY 0
        <BLANKLINE>

        This example shows the code that is generated to produce the same result as above.
        >>> print(m.code())
        <BLANKLINE>
        Quay('0')""",
    'record-INDI': f"""

    Example:
        Here is the way to construct the ged lines in the example from the specification.
        First create the two individual cross reference identifiers.  Then let a
        RecordIndi class format them into the desired ged lines.
        >>> from genedata.build import Genealogy
        >>> from genedata.classes{Config.VERSION} import Asso, RecordIndi, Role
        >>> g = Genealogy('example')
        >>> indi_i1_xref = g.individual_xref('I1')
        >>> indi_i2_xref = g.individual_xref('I2')
        >>> m = RecordIndi(indi_i1_xref, Asso(indi_i2_xref, Role('GODP')))
        >>> print(m.ged())
        0 @I1@ INDI
        1 ASSO @I2@
        2 ROLE GODP
        <BLANKLINE>""",
    # 'record-SNOTE': f"""
    # Example:
    #     The example in the specification has two records: the source record
    #     `GORDON` and an individual `I1`.  We will create those cross
    #     reference identifiers first.
    #     >>> from genedata.build import Genealogy
    #     >>> g = Genealogy('example')
    #     >>> sour_xref = g.source_xref('GORDON')
    #     >>> indi_xref = g.individual_xref('I1')
    #     Next create the record for the shared note:
    #     >>> from genedata.classes{Config.VERSION} import RecordIndi, RecordSnote, IndiName, Note, Snote
    #     >>> snote = RecordSnote(sour_xref, f'''"Gordon" is a traditional scottish surname.\\nIt became a given name in honor of Charles George Gordon.''')
    #     Next create the individual record.
    #     >>> indi = RecordIndi(
    #     ...     indi_xref,
    #     ...     IndiName('Gordon /Jones/',
    #     ...         [
    #     ...             Note('Named after the astronaut Gordon Cooper'),
    #     ...             Snote(snote_xref),
    #     ...         ]
    #     ...     )
    #     ... )
    #     Now generate the ged lines by calling the ged method on each of the records:
    #     >>> print(''.join([snote.ged(), indi.ged()]))
    #     0 @GORDON@ SNOTE "Gordon" is a traditional Scottish surname.
    #     1 CONT It became a given name in honor of Charles George Gordon.
    #     0 @I1@ INDI
    #     1 NAME Gordon /Jones/
    #     2 NOTE Named after the astronaut Gordon Cooper
    #     2 SNOTE @GORDON@
    #     <BLANKLINE>""",
    'RESN': f"""

    Examples:
        This example shows a successful run of the Resn structure using
        the enumeration value 'CONFIDENTIAL'.
        >>> from genedata.classes{Config.VERSION} import Resn
        >>> m = Resn('CONFIDENTIAL')
        >>> print(m.ged(1))
        1 RESN CONFIDENTIAL
        <BLANKLINE>

        This example shows the code that is generated to produce the same result as above.
        >>> print(m.code())
        <BLANKLINE>
        Resn('CONFIDENTIAL')
        
        More than one enumeration value may be entered for this particular
        enumeration set by separating the values with a comma.  For example,
        >>> n = Resn('CONFIDENTIAL, LOCKED')
        >>> print(n.ged(1))
        1 RESN CONFIDENTIAL, LOCKED
        <BLANKLINE>""",
    'ROLE': f"""

    Examples:
        The first example of the specification could be coded by first creating
        the cross reference identifiers for the individual `I1` and the source `S1`.  
        This would be done as follows:
        >>> from genedata.build import Genealogy
        >>> g = Genealogy('example')
        >>> indi = g.individual_xref('I1')
        >>> sour = g.source_xref('S1')

        With these cross reference identifiers we can create the ged lines:
        >>> from genedata.classes{Config.VERSION} import RecordIndi, IndiName, Sour, SourEven, Role
        >>> m = RecordIndi(indi, IndiName('Mary //', Sour(sour, SourEven('BIRT', Role('MOTH')))))
        >>> print(m.ged(1))
        0 @I1@ INDI
        1 NAME Mary //
        2 SOUR @S1@
        3 EVEN BIRT
        4 ROLE MOTH
        <BLANKLINE>

        The second example from the specification would be created as follows.
        There are two individuals in this example, `I2` and `I3`.  First
        create cross reference identifiers for them.
        >>> indi2 = g.individual_xref('I2')
        >>> indi3 = g.individual_xref('I3')
        With those cross reference identifiers we can complete the ged lines
        after importing the additional classes.
        >>> from genedata.class{Config.VERSION} import Asso, Bapm, Phrase
        Now create the lines:
        >>> m = RecordIndi(
        ...     [
        ...         Asso(indi3, Role('FRIEND', Phrase('best friend'))),
        ...         Bapm('', Asso(indi3, Role('WITN'))),
        ...     ]
        ... )
        >>> print(m.ged())
        0 @I2@ INDI
        1 ASSO @I3@
        2 ROLE FRIEND
        3 PHRASE best friend
        1 BAPM
        2 ASSO @I3@
        3 ROLE WITN
        <BLANKLINE>

        As a simpler example shows a successful run of the Role structure using
        the enumeration value 'CHIL'.  However, ultimately these lines would
        have to be part of a larger record.
        >>> from genedata.classes7 import Role
        >>> m = Role('CHIL')
        >>> print(m.ged(1))
        1 ROLE CHIL
        <BLANKLINE>

        This example shows the code that is generated to produce the same result as above.
        >>> print(m.code())
        <BLANKLINE>
        Role('CHIL')""",
    'SEX': f"""

    Examples:
        This example shows a successful run of the Sex structure using
        the enumeration value 'F'.
        >>> from genedata.classes{Config.VERSION} import Sex
        >>> m = Sex('F')
        >>> print(m.ged(1))
        1 SEX F
        <BLANKLINE>

        This example shows the code that is generated to produce the same result as above.
        >>> print(m.code())
        <BLANKLINE>
        Sex('F')""",
    'TITL': f"""

    Examples:
        Assume that letter.pdf is a scanned copy of a letter from Ann to her husband Henry 
        on April 6, 1920.  Based on the specification one could enter this as follows.
        >>> from genedata.classes{Config.VERSION} import File, Form, Titl
        >>> m = File('letter.pdf', [Form('application/pdf'), Titl('Letter from Ann to Henry April 6, 1920')])
        >>> print(m.ged(1))
        1 FILE letter.pdf
        2 FORM application/pdf
        2 TITL Letter from Ann to Henry April 6, 1920
        <BLANKLINE>""",
    'TYPE': f"""

    Examples:
        To see how the example could be produced from the specification
        first create an individual cross reference identifier then add the
        ordination event as a substructure of the RecordIndi record.
        >>> from genedata.build import Genealogy
        >>> from genedata.classes{Config.VERSION} import Ordn, RecordIndi, Type
        >>> g = Genealogy('test')
        >>> indi_xref = g.individual_xref('I1')
        >>> m = RecordIndi(
        ...     indi_xref,
        ...     [
        ...         Ordn('', Type('Bishop'))
        ...     ]
        ... )
        >>> print(m.ged())
        0 @I1@ INDI
        1 ORDN
        2 TYPE Bishop
        <BLANKLINE>""",
    'WWW': f"""

    Examples:
        The following example would send a logging message warning
        that the site "abc" cannot be reached.
        >>> from genedata.util import Input
        >>> from genedata.classes{Config.VERSION} import Www
        >>> response = Www(Input.www('abc'))
        >>> print(response.ged(1))
        1 WWW abc
        <BLANKLINE>
        
        If one doesn't want the check, one can just enter the url.
        According to the specification the url should be retained even
        it is not available.
        >>> m = Www('abc')
        >>> print(m.ged(1))
        1 WWW abc
        <BLANKLINE>""",
}


class Construct:
    # @staticmethod
    # def get_class_name(key: str) -> str:
    #     return key.title().replace('_', '').replace('-', '')

    @staticmethod
    def preamble(source: str, version: str) -> str:
        return f"""'''This module of classes was generated by methods in the `Construct` class
of the `util` module from GEDCOM yaml specification files.  

They should not be manually altered, but the `Construct` class should be changed
if needed and the classes modules from each GEDCOM version regenerated.

The specifications for this module are from the 
[GEDCOM files]({source}) for version {version}.
'''

"""

    @staticmethod
    def generate__all__() -> str:
        """Generate the __all__ = [] by filling in the list with the modified keys from Structure."""
        lines: str = '__all__ = ['
        for key in Keys.STRUCTURES:
            if key not in ['CONT']:
                edited_key: str = key.title().replace('_', '').replace('-', '')
                lines = f"{lines}\n    '{edited_key}',"
        return f'{lines}\n]\n'

    @staticmethod
    def generate_imports() -> str:
        return """
import logging
from typing import Any

from genedata.constants import Default
from genedata.messages import Msg
from genedata.structure import (
    BaseStructure,
    ExtensionXref,
    FamilyXref,
    IndividualXref,
    MultimediaXref,
    RepositoryXref,
    SharedNoteXref,
    SourceXref,
    SubmitterXref,
)
"""

    @staticmethod
    def add_links(text: str) -> str:
        """Add links missing in the specifications to text with brackets around it."""
        site: str = f'https://gedcom.io/specifications/FamilySearchGEDCOMv{Config.VERSION}.html'
        datatracker: str = 'https://datatracker.ietf.org/doc/html/rfc'
        return (
            text.replace(
                '[BCP 47]',
                '\n[BCP 47](https://en.wikipedia.org/wiki/IETF_language_tag)',
            )
            .replace(
                '[documented extension tag]',
                f'[documented extension tag]({site}#extension-tags)',
            )
            .replace('[E.123]', '[E.123](https://en.wikipedia.org/wiki/E.123)')
            .replace(
                '[E.164]', '\n[E.164](https://en.wikipedia.org/wiki/E.164)'
            )
            .replace(
                '[exid-types registry]', f'\n[exid-types registry]({site}#EXID)'
            )
            .replace('[Extensions]', f'\n[Extensions]({site}#extensions)')
            .replace(
                '[Family Attribute]',
                f'[Family Attribute]({site}#family-attributes)',
            )
            .replace('[Family Event]', f'[Family Event]({site}#family-events)')
            .replace(
                '[File Path datatype]',
                f'[File Path datatype]({site}#file-path)',
            )
            .replace(
                '[Individual Attribute]',
                f'[Individual Attribute]({site}#individual-attributes)',
            )
            .replace(
                '[Individual Event]',
                f'[Individual Event]({site}#INDIVIDUAL_EVENT_STRUCTURE)',
            )
            .replace(
                '[Latter-Day Saint Ordinance]',
                f'[Latter-Day Saint Ordinance]({site}#latter-day-saint-ordinances)',
            )
            .replace('[List]', f'[List]({site}#list)\n')
            .replace(
                '[media type]',
                f'[media type]({site}#media-type)\n',
            )
            .replace(
                '[Removing data]', f'\n[Removing data]({site}#removing-data)'
            )
            .replace('[RFC 3696]', f'[RFC 3696]({datatracker}3696)')
            .replace('[RFC\n3696]', f'\n[RFC 3696]({datatracker}3696)')
            .replace('[RFC\n3986]', f'\n[RFC 3986]({datatracker}3986)')
            .replace('[RFC 3987]', f'\n[RFC 3987]({datatracker}3987)')
            .replace('[RFC 4122]', f'[RFC 4122]({datatracker}4122)')
            .replace('[RFC 5321]', f'\n[RFC 5321]({datatracker}5321)')
            .replace('[RFC 5322]', f'\n[RFC 5322]({datatracker}5322)')
            .replace('. See also ', '.\nSee also ')
            .replace(
                '[The Header and Trailer]',
                f'\n[The Header and Trailer]({site}#the-header)',
            )
            .replace(
                '[whatwg/url]', '\n[whatwg/url](https://url.spec.whatwg.org/)'
            )
            .replace('[YAML file format]', f'[YAML file format]({site})')
        )

    @staticmethod
    def generate_specification(key: str, structure: dict[str, Any]) -> str:
        """Construct the Specification section of the documentation."""
        specification: list[str] = structure[key][Default.YAML_SPECIFICATION]
        string_linked: str = Default.EMPTY
        spec: str = """
    GEDCOM Specification:"""
        for string in specification:
            string_linked = Construct.add_links(string)
            if '\n' not in string_linked and len(string_linked) > 80:
                wrapped = wrap(
                    string_linked,
                    75,
                    break_long_words=False,
                    break_on_hyphens=False,
                )
                if len(wrapped) > 1:
                    for line in wrapped:
                        spec = ''.join([spec, '\n    > ', line])
            else:
                spec = ''.join(
                    [spec, '\n    > ', string_linked.replace('\n', '\n    > ')]
                )
        return spec

    @staticmethod
    def generate_examples(key: str) -> str:
        """Construct the Example section from the Examples dictionary in gedcom7."""
        example: str = Default.EMPTY
        if key in Examples:
            example = Examples[key]
        return example

    @staticmethod
    def generate_enumerations(
        key: str, structure: dict[str, Any], enumeration: dict[str, Any]
    ) -> str:
        """Construct the Enumerations section of the documentation."""
        enumeration_set: str = Default.EMPTY
        if Default.YAML_ENUMERATION_SET in structure[key]:
            enumeration_set = """
        
    Enumerations:"""
            for _keyname, value in enumeration.items():
                if (
                    Default.YAML_VALUE_OF in value
                    and structure[key][Default.YAML_ENUMERATION_SET]
                    in value[Default.YAML_VALUE_OF]
                ):
                    wrapped = wrap(value[Default.YAML_SPECIFICATION][0], 75)
                    enumvalue: str = Default.EMPTY
                    if len(wrapped) > 1:
                        for line in wrapped:
                            enumvalue = ''.join(
                                [enumvalue, '\n        > ', line]
                            )
                    else:
                        enumvalue = ''.join(
                            [
                                enumvalue,
                                '\n        > ',
                                wrapped[0].replace('\n', '\n    '),
                            ]
                        )
                    enumeration_set = ''.join(
                        [
                            enumeration_set,
                            "\n    - '",
                            value[Default.YAML_STANDARD_TAG],
                            "': ",
                            value[Default.YAML_URI],
                            enumvalue,
                        ]
                    )
        return enumeration_set

    @staticmethod
    def generate_substructures(key: str, structure: dict[str, Any]) -> str:
        """Construct the Substructures section of the documentation."""
        class_name: str = Default.EMPTY
        subs: dict[str, str] = {}
        if Default.YAML_SUBSTRUCTURES in structure[key]:
            subs = structure[key][Default.YAML_SUBSTRUCTURES]
        substructures: str = Default.EMPTY
        if len(subs) > 0:
            substructures = """
        
    Substructures:
    |               Specification                | Quantity | Required |  Class Name  |
    | ------------------------------------------ | -------- | -------- | ------------ |"""
            for subskey, value in subs.items():
                yes: str = 'No'
                one: str = 'Many'
                if Default.YAML_CARDINALITY_REQUIRED in value:
                    yes = 'Yes'
                if Default.YAML_CARDINALITY_SINGULAR in value:
                    one = 'Only One'
                class_name = (
                    subskey[subskey.rfind('/') + 1 :]
                    .title()
                    .replace('_', '')
                    .replace('-', '')
                )
                substructures = ''.join(
                    [
                        substructures,
                        '\n    | ',
                        subskey,
                        ' ' * (42 - len(subskey)),
                        ' | ',
                        one,
                        ' ' * (8 - len(one)),
                        ' | ',
                        yes,
                        ' ' * (8 - len(yes)),
                        ' | ',
                        class_name,
                        ' ' * (12 - len(class_name)),
                        ' |',
                    ]
                )
        return substructures

    @staticmethod
    def generate_superstructures(key: str, structure: dict[str, Any]) -> str:
        """Construct the Substructures section of the documentation."""
        class_name: str = Default.EMPTY
        supers: dict[str, str] = {}
        if Default.YAML_SUPERSTRUCTURES in structure[key]:
            supers = structure[key][Default.YAML_SUPERSTRUCTURES]
        superstructures: str = Default.EMPTY
        if len(supers) > 0:
            superstructures = """
        
    Superstructures:
    |               Specification                | Quantity | Required |  Class Name  |
    | ------------------------------------------ | -------- | -------- | ------------ |"""
            for superskey, value in supers.items():
                yes: str = 'No'
                one: str = 'Many'
                if Default.YAML_CARDINALITY_REQUIRED in value:
                    yes = 'Yes'
                if Default.YAML_CARDINALITY_SINGULAR in value:
                    one = 'Only One'
                class_name = (
                    superskey[superskey.rfind('/') + 1 :]
                    .title()
                    .replace('_', '')
                    .replace('-', '')
                )
                superstructures = ''.join(
                    [
                        superstructures,
                        '\n    | ',
                        superskey,
                        ' ' * (42 - len(superskey)),
                        ' | ',
                        one,
                        ' ' * (8 - len(one)),
                        ' | ',
                        yes,
                        ' ' * (8 - len(yes)),
                        ' | ',
                        class_name,
                        ' ' * (12 - len(class_name)),
                        ' |',
                    ]
                )
        return superstructures

    @staticmethod
    def generate_args(key: str, structure: dict[str, Any]) -> str:
        """Construct the Args section of the documentation."""
        args = """
        
    Args:"""
        if (
            Default.YAML_PAYLOAD in structure[key]
            and structure[key][Default.YAML_PAYLOAD] is not None
            and key[0:6] != 'record'
        ):
            args = ''.join(
                [
                    args,
                    '\n        ',
                    Default.CODE_VALUE,
                    ': A value of data type ',
                    structure[key][Default.YAML_PAYLOAD],
                ]
            )
        if key[0:6] == 'record':
            args = ''.join(
                [
                    args,
                    '\n        ',
                    Default.CODE_VALUE,
                    ': A value of data type ',
                    Construct.get_record_datatype(key),
                ]
            )
        return ''.join(
            [
                args,
                '\n        ',
                Default.CODE_SUBS,
                ': A permitted substructure or list of permitted substructures.',
            ]
        )

    @staticmethod
    def generate_references(key: str, structure: dict[str, Any]) -> str:
        """Construct the References section of the documentation."""
        uri = structure[key][Default.YAML_URI]
        tag = structure[key][Default.YAML_STANDARD_TAG]
        return f"""
        
    References:
    - [GEDCOM {tag} Structure]({uri})
    - [GEDCOM Specifications](https://gedcom.io/specifications/FamilySearchGEDCOMv{Config.VERSION}.html)"""

    @staticmethod
    def get_datatype(key: str, structure: dict[str, Any]) -> str:
        """Convert the GEDCOM datatype into python datatype."""
        datatype: str = Default.EMPTY
        if (
            Default.YAML_PAYLOAD in structure[key]
            and structure[key] is not None
        ):
            datatype = structure[key][Default.YAML_PAYLOAD]
        match datatype:
            case 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger':
                return 'int'
            case '@<https://gedcom.io/terms/v7/record-INDI>@':
                return 'IndividualXref'
            case '@<https://gedcom.io/terms/v7/record-FAM>@':
                return 'FamilyXref'
            case '@<https://gedcom.io/terms/v7/record-SUBM>@':
                return 'SubmitterXref'
            case '@<https://gedcom.io/terms/v7/record-OBJE>@':
                return 'MultimediaXref'
            case '@<https://gedcom.io/terms/v7/record-REPO>@':
                return 'RepositoryXref'
            case '@<https://gedcom.io/terms/v7/record-SNOTE>@':
                return 'SharedNoteXref'
            case '@<https://gedcom.io/terms/v7/record-SOUR>@':
                return 'SourceXref'
            case _:
                return 'str'

    @staticmethod
    def get_record_datatype(key: str) -> str:
        """Assign a cross reference datatype to specific records."""
        datatype: str = key[7:]
        match datatype:
            case 'FAM':
                return 'FamilyXref'
            case 'INDI':
                return 'IndividualXref'
            case 'OBJE':
                return 'MultimediaXref'
            case 'REPO':
                return 'RepositoryXref'
            case 'SNOTE':
                return 'SharedNoteXref'
            case 'SOUR':
                return 'SourceXref'
            case 'SUBM':
                return 'SubmitterXref'
            case _:
                return 'Xref'

    @staticmethod
    def generate_init(key: str, structure: dict[str, Any]) -> str:
        """Construct the global constants and init section of the class."""
        required: list[str] = structure[key][Default.YAML_REQUIRED]
        value_arg: str = (
            f', {Default.CODE_VALUE}: {Construct.get_datatype(key, structure)}'
        )
        value_init: str = Default.CODE_VALUE
        subs_arg: str = f', {Default.CODE_SUBS}: Any'
        if len(required) == 0:
            subs_arg = f', {Default.CODE_SUBS}: Any = None'
        subs_init: str = Default.CODE_SUBS
        payload: str = Default.EMPTY
        if (
            Default.YAML_PAYLOAD in structure[key]
            and structure[key][Default.YAML_PAYLOAD] is not None
        ):
            payload = structure[key][Default.YAML_PAYLOAD]
        init: str = f"\n    key: str = '{key}'"
        if payload == Default.EMPTY or key == 'record-SNOTE':
            value_arg = Default.EMPTY
            #value_init = 'Default.EMPTY'
            value_init = 'None'
            if 'record-' in key:
                init = f"\n    key: str = '{key}'"
                value_arg = f', {Default.CODE_VALUE}: {Construct.get_record_datatype(key)}'
                value_init = Default.CODE_VALUE
        deprecation_line: str = Default.EMPTY
        if key in ['ADR1', 'ADR2', 'ADR3']:
            deprecation_line = '\n        logging.info(Msg.DEPRECATION_WARNING.format(self.class_name))'
        init_line: str = f"""
        
    def __init__(self{value_arg}{subs_arg}) -> None:
        super().__init__({value_init}, {subs_init}, self.key){deprecation_line}"""
        return ''.join([init, init_line])

    @staticmethod
    def generate_class(
        key: str,
        url: str,
        structure_dictionary: dict[str, Any] | None = None,
        enumeration_dictionary: dict[str, Any] | None = None,
    ) -> str:
        """Generate a single class and its documentation defined by its Structure definition.

        Args:
            key: The key of the Structure dictionary.
            url: The source of the yaml files where one can read the structure and enumeration dictionaries.
            structure_dictionary: The structure dictionary as an alternative to using the url to get this.
            enumeration_dictionary: The enumeration dictionary as an alternative to using the url to get this.
        """
        if url[-1] == Default.SLASH:
            base_url: str = url
        else:
            base_url = f'{url}{Default.SLASH}'
        if structure_dictionary is None:
            structure_dictionary = {}
        if enumeration_dictionary is None:
            enumeration_dictionary = {}
        structure: dict[str, Any] = structure_dictionary
        if len(structure) == 0:
            structure = eval(Convert.structure_dictionary(base_url))
        enumeration: dict[str, Any] = enumeration_dictionary
        if len(enumeration) == 0:
            enumeration = eval(Convert.enumeration_dictionary(base_url))
        tag: str = structure[key][Default.YAML_STANDARD_TAG]
        class_name: str = structure[key][Default.YAML_CLASS_NAME]
        parts: str = ''.join(
            [
                Construct.generate_specification(key, structure),
                Construct.generate_examples(key),
                Construct.generate_enumerations(key, structure, enumeration),
                Construct.generate_substructures(key, structure),
                Construct.generate_superstructures(key, structure),
                Construct.generate_args(key, structure),
                Construct.generate_references(key, structure),
            ]
        )
        lines: str = f"""

class {class_name}(BaseStructure):
    '''Store, validate and format the {tag} structure. 
    
    This class was generated by `Construct.generate_class` in the prep module
    using GEDCOM yaml specification files.  Links were added to the specification 
    and tables constructed from the yaml files to aid the user of these classes.  
    DO NOT CHANGE THIS CLASS MANUALLY.  

    {parts}
    '''
    {Construct.generate_init(key, structure)}
    """
        return lines

    @staticmethod
    def generate_all_classes(url: str) -> str:
        """Generate all classes and their documentation defined by the Structure dictionary."""

        if url[-1] == Default.SLASH:
            base_url: str = url
        else:
            base_url = f'{url}{Default.SLASH}'
        structure: dict[str, Any] = eval(Convert.structure_dictionary(base_url))
        enumeration: dict[str, Any] = eval(
            Convert.enumeration_dictionary(base_url)
        )
        lines: str = Default.EMPTY
        for key in Keys.STRUCTURES:
            if key not in ['CONT']:
                lines = ''.join(
                    [
                        lines,
                        Construct.generate_class(
                            key, url, structure, enumeration
                        ),
                    ]
                )
        return lines

    @staticmethod
    def build_all(source: str, version: str, url: str) -> str:
        """Construct the entire module containing GEDCOM structures converted to classes."""
        return ''.join(
            [
                Construct.preamble(source, version),
                Construct.generate__all__(),
                Construct.generate_imports(),
                Construct.generate_all_classes(url),
            ]
        )
