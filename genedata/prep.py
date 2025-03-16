# util.py
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
"""

__all__ = [
    'Construct',
    'Convert',
]


from dataclasses import dataclass
from textwrap import wrap
from typing import Any

from ordered_set import OrderedSet  # type: ignore[import-not-found]

from genedata.constants import Default

# from genedata.gedcom7 import Enumeration, Structure
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

The specification was obtained from the [GEDCOM-registeries]({source})
made available under an Apache 2.0 license.

The names of the dictionaries are based on the directories in this registry.  Each yaml file
in the directory is read into a dictionary which is then added to a dictionary named after
the directory.

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
            yamldict = Util.read(f'{path_start}{item}{path_end}')
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
            yamldict = Util.read(f'{path_start}{item}{path_end}')
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
            yamldict = Util.read(f'{path_start}{item}{path_end}')
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
            yamldict = Util.read(f'{path_start}{item}{path_end}')
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
            yamldict = Util.read(f'{path_start}{item}{path_end}')
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
            yamldict = Util.read(f'{path_start}{item}{path_end}')
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
            yamldict = Util.read(f'{path_start}{item}{path_end}')
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
            yamldict = Util.read(f'{path_start}{item}{path_end}')
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
            yamldict = Util.read(f'{path_start}{item}{path_end}')
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
            yamldict = Util.read(f'{path_start}{item}{path_end}')
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
    'LATI': """

    Examples:
        The following example shows how to enter the latitude (Lati))
        coordinates into a Map structure to produce the GEDCOM example
        mentioned in the GEDCOM Specification section.
        >>> from genedata.structure import Lati, Long, Map
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
    'LONG': """

    Examples:
        The following example howss how to enter the longitude (Long)
        coordinates into a map structure to produce the GEDCOM output
        mentioned in the GEDCOM Specification.
        >>> from genedata.structure import Lati, Long, Map
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
    'MAP': """

    Examples:
        The following example illustrates how to enter latitude (Lati) and longitude (Long)
        coordinates into a map structure to produce the GEDCOM output.
        >>> from genedata.structure import Input, Lati, Long, Map
        >>> m = Map([Lati('N18.150944'), Long('E168.150944')])
        >>> print(m.ged())
        1 MAP
        2 LATI N18.150944
        2 LONG E168.150944
        <BLANKLINE>""",
    'MEDI': """

    Examples:
        This example shows a successful run of the Medi structure using
        the enumeration value 'AUDIO'.
        >>> from genedata.structure import Medi
        >>> m = Medi('AUDIO')
        >>> print(m.ged(2))
        2 MEDI AUDIO
        <BLANKLINE>

        This example shows the code that is generated to produce the same result as above.
        >>> print(m.code())
        <BLANKLINE>
        Medi('AUDIO')""",
    'ord-STAT': """

    Examples:
        This example shows a successful run of the OrdStat structure using
        the enumeration value 'BIC'.
        >>> from genedata.structure import OrdStat
        >>> m = OrdStat('BIC')
        >>> print(m.ged(1))
        1 STAT BIC
        <BLANKLINE>

        This example shows the code that is generated to produce the same result as above.
        >>> print(m.code())
        <BLANKLINE>
        OrdStat('BIC')""",
    'PEDI': """

    Examples:
        This example shows a successful run of the Pedi structure using
        the enumeration value 'ADOPTED'.
        >>> from genedata.structure import Pedi
        >>> m = Pedi('ADOPTED')
        >>> print(m.ged(1))
        1 PEDI ADOPTED
        <BLANKLINE>

        This example shows the code that is generated to produce the same result as above.
        >>> print(m.code())
        <BLANKLINE>
        Pedi('ADOPTED')""",
    'QUAY': """

    Examples:
        This example shows a successful run of the Quay structure using
        the enumeration value '0'.
        >>> from genedata.structure import Quay
        >>> m = Quay('0')
        >>> print(m.ged(1))
        1 QUAY 0
        <BLANKLINE>

        This example shows the code that is generated to produce the same result as above.
        >>> print(m.code())
        <BLANKLINE>
        Quay('0')""",
    'RESN': """

    Examples:
        This example shows a successful run of the Resn structure using
        the enumeration value 'CONFIDENTIAL'.
        >>> from genedata.structure import Resn
        >>> m = Resn('CONFIDENTIAL')
        >>> print(m.ged(1))
        1 RESN CONFIDENTIAL
        <BLANKLINE>

        This example shows the code that is generated to produce the same result as above.
        >>> print(m.code())
        <BLANKLINE>
        Resn('CONFIDENTIAL')""",
    'ROLE': """

    Examples:
        This example shows a successful run of the Role structure using
        the enumeration value 'CHIL'.
        >>> from genedata.structure import Role
        >>> m = Role('CHIL')
        >>> print(m.ged(1))
        1 ROLE CHIL
        <BLANKLINE>

        This example shows the code that is generated to produce the same result as above.
        >>> print(m.code())
        <BLANKLINE>
        Role('CHIL')""",
    'SEX': """

    Examples:
        This example shows a successful run of the Sex structure using
        the enumeration value 'F'.
        >>> from genedata.structure import Sex
        >>> m = Sex('F')
        >>> print(m.ged(1))
        1 SEX F
        <BLANKLINE>

        This example shows the code that is generated to produce the same result as above.
        >>> print(m.code())
        <BLANKLINE>
        Sex('F')""",
}


class Construct:
    @staticmethod
    def get_class_name(key: str) -> str:
        return key.title().replace('_', '').replace('-', '')

    @staticmethod
    def preamble(source: str, version: str) -> str:
        return f"""'''The classes were generated by methods in the `Construct` class.  
They should not be manually altered.

The specifications are from the [GEDCOM files]{source} for version {version}.
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
    def generate_specification(key: str, structure: dict[str, Any]) -> str:
        """Construct the Specification section of the documentation."""
        specification: list[str] = structure[key][Default.YAML_SPECIFICATION]
        spec: str = """
    GEDCOM Specification:"""
        for string in specification:
            if '\n' not in string and len(string) > 80:
                wrapped = wrap(string, 75)
                if len(wrapped) > 1:
                    for line in wrapped:
                        spec = ''.join([spec, '\n    > ', line])
            else:
                spec = ''.join(
                    [spec, '\n    > ', string.replace('\n', '\n    > ')]
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
        subs: list[str] = []
        if Default.YAML_SUBSTRUCTURES in structure[key]:
            subs = structure[key][Default.YAML_SUBSTRUCTURES]
        substructures: str = Default.EMPTY
        if len(subs) > 0:
            substructures = """
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |"""
            for value in subs:
                yes: str = 'No'
                one: str = 'Many'
                if Default.YAML_CARDINALITY_REQUIRED in value:
                    yes = 'Yes'
                if Default.YAML_CARDINALITY_SINGULAR in value:
                    one = 'Only One'
                substructures = ''.join(
                    [
                        substructures,
                        '\n    | ',
                        value,
                        ' ' * (42 - len(value)),
                        ' | ',
                        one,
                        ' ' * (8 - len(one)),
                        ' | ',
                        yes,
                        ' ' * (8 - len(yes)),
                        ' |',
                    ]
                )
        return substructures

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
                ': A permitted substructure, an extension or list of permitted substructures or extensions.',
            ]
        )

    @staticmethod
    def generate_references(key: str, structure: dict[str, Any]) -> str:
        """Construct the References section of the documentation."""
        uri = structure[key][Default.YAML_URI]
        tag = structure[key][Default.YAML_STANDARD_TAG]
        return f"""
        
    References:
    - [GEDCOM {tag} Structure]({uri})"""

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
            value_init = 'Default.EMPTY'
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

        Place the output from this in genedata.structure below the commented line
        stating that generaed classes follow.  There are only generated classes
        below this line.

        It may be best to run this in a notebook and then copy the output to the module.

        See Also:
        - `generate_all_classes`

        Args:
            key: The key of the Structure dictionary.
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
        class_name: str = Construct.get_class_name(key)
        parts: str = ''.join(
            [
                Construct.generate_specification(key, structure),
                Construct.generate_examples(key),
                Construct.generate_enumerations(key, structure, enumeration),
                Construct.generate_substructures(key, structure),
                Construct.generate_args(key, structure),
                Construct.generate_references(key, structure),
            ]
        )
        lines: str = f"""

class {class_name}(BaseStructure):
    '''Store, validate and format the {tag} structure. Generated by `Construct.generate_class`.
    {parts}
    '''
    {Construct.generate_init(key, structure)}
    """
        return lines

    @staticmethod
    def generate_all_classes(url: str) -> str:
        """Generate all classes and their documentation defined by the Structure dictionary.

        Place the entire collection in genedata.structure below the commented
        line which reads:

        # Classes below this marker were genered by the genedata.gedcom7 Display class
        # by calling Display.generate_all_classes or Display.generate_class.

        Only generated classes go below this line.

        See Also:
        - `generate_class`
        """

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
        return ''.join(
            [
                Construct.preamble(source, version),
                Construct.generate__all__(),
                Construct.generate_imports(),
                Construct.generate_all_classes(url),
            ]
        )
