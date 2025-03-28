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
- Keys: OrderedSets of strings which when combined with a beginning url and ".yaml"
    retrieve the specification.

The classes and specs modules are generated from methods in this module.
This is the module to change if one wants to modify them.
"""

__all__ = [
    'Construct',
    'Convert',
    'Examples',
]

from pathlib import Path
from textwrap import wrap
from typing import Any, ClassVar

from genedata.constants import Config, Default
from genedata.messages import Msg
from genedata.util import Util


class Convert:
    """Read and store GEDCOM specification."""

    #enumerationset_dict: ClassVar[dict[str, Any]] = {}

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
    def get_enum_tag(value: str) -> str:
        """Extract the tag from the file name specifying an enumeration tag.
        
        This can also be obtained from the `standard tag` key within that file.
        
        Example:
            Suppose the file name is "https://gedcom.io/terms/v7/enum-ADOP-HUSB".
            This method returns only HUSB as the tag.
            >>> from genedata.prep import Convert
            >>> print(Convert.get_enum_tag('"https://gedcom.io/terms/v7/enum-ADOP-HUSB"'))
            HUSB

            """
        tag: str = (
            value[value.rfind(Default.SLASH) + 1 :]
            .replace(Default.URL_ENUMERATION_PREFIX, Default.EMPTY)
            .replace(Default.QUOTE_DOUBLE, Default.EMPTY)
        )
        if Default.HYPHEN in tag:
            tag = tag[tag.rfind(Default.HYPHEN) + 1 :]
        return tag
    
    @staticmethod
    def get_slash(url: str) -> str:
        """Add a '/' at the end of a string if one is not there already.
        
        This makes sure that a directory string ends with a /.
        
        Example:
            Let `abcdefghi` be the name of the directory.
            >>> from genedata.prep import Convert
            >>> print(Convert.get_slash('abcdefghi'))
            abcdefghi/

        """
        if url[-1] == Default.SLASH:
            return url
        return f'{url}{Default.SLASH}'

    @staticmethod
    def dictionary(
        url: str,
        base: str,
        prefix: str,
    ) -> str:
        lines: str = Default.BRACE_LEFT
        directory: str = f'{Convert.get_slash(url)}{base}'
        p = Path(directory)
        if p.exists():
            for file in p.iterdir():
                if file.suffix == Default.YAML_FILE_END:
                    key = file.stem.replace(prefix, Default.EMPTY)
                    yamldict = Util.read_yaml(str(file))
                    match base:
                        case (
                            Default.URL_STRUCTURE
                            | Default.URL_STRUCTURE_EXTENSION
                        ):
                            required: list[str] = []
                            single: list[str] = []
                            permitted: list[str] = []
                            enumset: str = Default.EMPTY
                            if Default.YAML_SUBSTRUCTURES in yamldict:
                                for keyname, value in yamldict[
                                    Default.YAML_SUBSTRUCTURES
                                ].items():
                                    tag = (
                                        keyname[
                                            keyname.rfind(Default.SLASH) + 1 :
                                        ]
                                        .title()
                                        .replace(Default.HYPHEN, Default.EMPTY)
                                    )
                                    permitted.append(tag)
                                    if (
                                        Default.YAML_CARDINALITY_REQUIRED
                                        in value
                                    ):
                                        required.append(tag)
                                    if (
                                        Default.YAML_CARDINALITY_SINGULAR
                                        in value
                                    ):
                                        single.append(tag)
                            if Default.YAML_PAYLOAD in yamldict and yamldict[
                                Default.YAML_PAYLOAD
                            ] in [
                                'https://gedcom.io/terms/v7/type-List#Enum',
                                'https://gedcom.io/terms/v7/type-Enum',
                            ]:
                                enumset = yamldict[Default.YAML_ENUMERATION_SET]

                            yamldict[Default.YAML_PERMITTED] = permitted
                            yamldict[Default.YAML_REQUIRED] = required
                            yamldict[Default.YAML_SINGULAR] = single
                            yamldict[Default.YAML_ENUMERATION_SET] = enumset
                            yamldict[Default.YAML_ENUM_KEY] = enumset[
                                enumset.rfind(Default.SLASH) + 1 :
                            ].replace(
                                Default.URL_ENUMERATION_SET_PREFIX,
                                Default.EMPTY,
                            )
                            yamldict[Default.YAML_CLASS_NAME] = (
                                file.stem.title()
                                .replace(Default.UNDERLINE, Default.EMPTY)
                                .replace(Default.HYPHEN, Default.EMPTY)
                            )
                            yamldict[Default.YAML_KEY] = file.stem
                        case Default.URL_ENUMERATION_SET:
                            enum_tags: list[str] = []
                            for tag in yamldict[
                                Default.YAML_ENUMERATION_VALUES
                            ]:
                                enum_tags.append(Convert.get_enum_tag(tag))
                            yamldict[Default.YAML_ENUM_TAGS] = enum_tags
                    lines = f"{lines}{Default.EOL}    '{key}': {yamldict},"
        else:
            raise ValueError(Msg.DIRECTORY_NOT_FOUND.format(directory))
        if lines == Default.BRACE_LEFT:
            return ''.join([lines, Default.BRACE_RIGHT])
        return ''.join([lines, Default.EOL, Default.BRACE_RIGHT])

    @staticmethod
    def calendar_dictionary(url: str) -> str:
        """Retrive the calendar dictionary as a string that can be sent to `eval`."""
        return Convert.dictionary(
            url, Default.URL_CALENDAR, Default.URL_CALENDAR_PREFIX
        )

    @staticmethod
    def calendar(url: str) -> str:
        """Format the calendar dictionary for use in the specs module."""
        return ''.join(
            [
                'Calendar: dict[str, dict[str, Any]] = ',
                Convert.calendar_dictionary(url),
                Default.EOL,
                Default.EOL,
            ]
        )

    @staticmethod
    def datatype_dictionary(url: str) -> str:
        """Retrive the data type dictionary as a string that can be sent to `eval`."""
        return Convert.dictionary(
            url, Default.URL_DATATYPE, Default.URL_DATATYPE_PREFIX
        )

    @staticmethod
    def datatype(url: str) -> str:
        """Format the data type dictionary for use in the specs module."""
        return ''.join(
            [
                'DataType: dict[str, dict[str, Any]] = ',
                Convert.datatype_dictionary(url),
                Default.EOL,
                Default.EOL,
            ]
        )

    @staticmethod
    def enumeration_dictionary(url: str) -> str:
        """Retrive the enumeration dictionary as a string that can be sent to `eval`."""
        return Convert.dictionary(
            url, Default.URL_ENUMERATION_SET, Default.URL_ENUMERATION_SET_PREFIX
        )

    @staticmethod
    def enumeration(url: str) -> str:
        """Format the enumeration dictionary for use in the specs module."""
        return ''.join(
            [
                'Enumeration: dict[str, dict[str, Any]] = ',
                Convert.enumeration_dictionary(url),
                Default.EOL,
                Default.EOL,
            ]
        )

    @staticmethod
    def enumerationset_dictionary(url: str) -> str:
        """Retrive the enumeration set dictionary as a string that can be sent to `eval`."""
        return Convert.dictionary(
            url, Default.URL_ENUMERATION_SET, Default.URL_ENUMERATION_SET_PREFIX
        )

    @staticmethod
    def enumerationset(url: str) -> str:
        """Format the enumeration set dictionary for use in the specs module."""
        return ''.join(
            [
                'EnumerationSet: dict[str, dict[str, Any]] = ',
                Convert.enumerationset_dictionary(url),
                Default.EOL,
                Default.EOL,
            ]
        )

    @staticmethod
    def month_dictionary(url: str) -> str:
        """Retrive the month dictionary as a string that can be sent to `eval`."""
        return Convert.dictionary(
            url, Default.URL_MONTH, Default.URL_MONTH_PREFIX
        )

    @staticmethod
    def month(url: str) -> str:
        """Format the month dictionary for use in the specs module."""
        return ''.join(
            [
                'Month: dict[str, dict[str, Any]] = ',
                Convert.month_dictionary(url),
                Default.EOL,
                Default.EOL,
            ]
        )

    @staticmethod
    def structure_dictionary(url: str) -> str:
        """Retrive the structure dictionary as a string that can be sent to `eval`."""
        return Convert.dictionary(
            url, Default.URL_STRUCTURE, Default.URL_STRUCTURE_PREFIX
        )

    @staticmethod
    def structure(url: str) -> str:
        """Format the structure dictionary for use in the specs module."""
        return ''.join(
            [
                'Structure: dict[str, dict[str, Any]] = ',
                Convert.structure_dictionary(url),
                Default.EOL,
                Default.EOL,
            ]
        )

    @staticmethod
    def structure_extension_dictionary(url: str) -> str:
        """Retrive the extension structure dictionary as a string that can be sent to `eval`."""
        return Convert.dictionary(
            url,
            Default.URL_STRUCTURE_EXTENSION,
            Default.URL_STRUCTURE_EXTENSION_PREFIX,
        )

    @staticmethod
    def structure_extension(url: str) -> str:
        """Format the extension structure dictionary for use in the specs module."""
        return ''.join(
            [
                'ExtensionStructure: dict[str, dict[str, Any]] = ',
                Convert.structure_extension_dictionary(url),
                Default.EOL,
                Default.EOL,
            ]
        )

    @staticmethod
    def uri_dictionary(url: str) -> str:
        """Retrive the uri dictionary as a string that can be sent to `eval`."""
        return Convert.dictionary(url, Default.URL_URI, Default.URL_URI_PREFIX)

    @staticmethod
    def uri(url: str) -> str:
        """Format the uri dictionary for use in the specs module."""
        return ''.join(
            [
                'Uri: dict[str, dict[str, Any]] = ',
                Convert.uri_dictionary(url),
                Default.EOL,
                Default.EOL,
            ]
        )

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
    'ASSO': f"""

    Examples:
        This example illustrates how one may construct the example in the
        specification. First create two individual cross reference identifiers.
        The add the data to a RecordIndi class for the first individual.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> from genedata.build import Genealogy
        >>> from genedata.structure import Void
        >>> {Default.CODE_GENEALOGY} = Genealogy('example')
        >>> indi1 = {Default.CODE_GENEALOGY}.individual_xref('I1')
        >>> indi2 = {Default.CODE_GENEALOGY}.individual_xref('I2')
        >>> indi = {Default.CODE_CLASS}.RecordIndi(indi1,
        ...     [
        ...         {Default.CODE_CLASS}.Asso(Void.INDI, 
        ...             [
        ...                 {Default.CODE_CLASS}.Phrase('Mr Stockdale'),
        ...                 {Default.CODE_CLASS}.Role('OTHER', {Default.CODE_CLASS}.Phrase('Teacher')),
        ...             ]
        ...         ),
        ...         {Default.CODE_CLASS}.Bapm('',
        ...             [
        ...                 {Default.CODE_CLASS}.Date('1930'),
        ...                 {Default.CODE_CLASS}.Asso(indi2, {Default.CODE_CLASS}.Role('CLERGY')),
        ...             ]
        ...         ),
        ...     ]
        ... )
        >>> print(indi.ged())
        0 @I1@ INDI
        1 ASSO @VOID@
        2 PHRASE Mr Stockdale
        2 ROLE OTHER
        3 PHRASE Teacher
        1 BAPM
        2 DATE 1930
        2 ASSO @I2@
        3 ROLE CLERGY
        <BLANKLINE>""",
    'FILE-TRAN': f"""

    Examples:
        The following example shows how to construct the example in the specification.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> from genedata.build import Genealogy
        >>> {Default.CODE_GENEALOGY} = Genealogy('example')
        >>> obje_xref = {Default.CODE_GENEALOGY}.multimedia_xref('EX')
        >>> obje = {Default.CODE_CLASS}.RecordObje(obje_xref,
        ...     [
        ...         {Default.CODE_CLASS}.File('media/original.mp3',
        ...             [
        ...                 {Default.CODE_CLASS}.Form('audio/mp3'),
        ...                 {Default.CODE_CLASS}.FileTran('media/derived.oga', {Default.CODE_CLASS}.Form('audio/ogg')),
        ...                 {Default.CODE_CLASS}.FileTran('media/transcript.vtt', {Default.CODE_CLASS}.Form('text/vtt')),
        ...             ]
        ...         ),
        ...     ]
        ... )
        >>> print(obje.ged())
        0 @EX@ OBJE
        1 FILE media/original.mp3
        2 FORM audio/mp3
        2 TRAN media/derived.oga
        3 FORM audio/ogg
        2 TRAN media/transcript.vtt
        3 FORM text/vtt
        <BLANKLINE>""",
    'HEIGHT': f"""

    Examples:
        The following example shows how to construct the example in the specification.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> from genedata.build import Genealogy
        >>> {Default.CODE_GENEALOGY} = Genealogy('example')
        >>> indi_xref = {Default.CODE_GENEALOGY}.individual_xref('I45')
        >>> indi = {Default.CODE_CLASS}.RecordIndi(indi_xref, 
        ...     [
        ...         {Default.CODE_CLASS}.Dscr('brown eyes, 5ft 10in, 198 pounds'),
        ...     ]
        ... )
        >>> print(indi.ged())
        0 @I45@ INDI
        1 DSCR brown eyes, 5ft 10in, 198 pounds
        <BLANKLINE>""",
    'INDI-EVEN': f"""

    Example:
        The following example shows how to construct the example in the specification.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> from genedata.build import Genealogy
        >>> {Default.CODE_GENEALOGY} = Genealogy('example')
        >>> indi_xref = {Default.CODE_GENEALOGY}.individual_xref('I1')
        >>> indi = {Default.CODE_CLASS}.RecordIndi(indi_xref, 
        ...     [
        ...         {Default.CODE_CLASS}.IndiEven('',
        ...             [
        ...                 {Default.CODE_CLASS}.Type('Land Lease'),
        ...                 {Default.CODE_CLASS}.Date('2 OCT 1837'),
        ...             ]
        ...         ),
        ...         {Default.CODE_CLASS}.IndiEven('Mining equipment',
        ...             [
        ...                 {Default.CODE_CLASS}.Type('Equipment Lease'),
        ...                 {Default.CODE_CLASS}.Date('4 NOV 1837'),
        ...             ]
        ...         ),
        ...     ]
        ... )
        >>> print(indi.ged())
        0 @I1@ INDI
        1 EVEN
        2 TYPE Land Lease
        2 DATE 2 OCT 1837
        1 EVEN Mining equipment
        2 TYPE Equipment Lease
        2 DATE 4 NOV 1837
        <BLANKLINE>""",
    'INDI-FACT': f"""
    
    Examples:
        The following example shows how to construct the example in the specification.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> from genedata.build import Genealogy
        >>> {Default.CODE_GENEALOGY} = Genealogy('example')
        >>> indi_xref = {Default.CODE_GENEALOGY}.individual_xref('I1')
        >>> indi = {Default.CODE_CLASS}.RecordIndi(indi_xref, 
        ...     {Default.CODE_CLASS}.IndiFact('Woodworking', {Default.CODE_CLASS}.Type('Skills'))
        ... )
        >>> print(indi.ged())
        0 @I1@ INDI
        1 FACT Woodworking
        2 TYPE Skills
        <BLANKLINE>""",
    'INDI-RESI': f"""

    Examples:
        The following examples show how to construct the examples in the specification.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> resi = {Default.CODE_CLASS}.IndiResi('living with an aunt', {Default.CODE_CLASS}.Date('ABT MAR 1894'))
        >>> print(resi.ged())
        1 RESI living with an aunt
        2 DATE ABT MAR 1894
        <BLANKLINE>

        >>> resi2 = {Default.CODE_CLASS}.IndiResi('in a mobile caravan', 
        ...     {Default.CODE_CLASS}.Plac(', , Austro-Hungarian Empire',
        ...         {Default.CODE_CLASS}.PlacForm('City, County, Country'))
        ... )
        >>> print(resi2.ged())
        1 RESI in a mobile caravan
        2 PLAC , , Austro-Hungarian Empire
        3 FORM City, County, Country
        <BLANKLINE>""",
    'LATI': f"""

    Examples:
        The following example shows how to enter the latitude (Lati))
        coordinates into a Map structure to produce the GEDCOM example
        mentioned in the GEDCOM Specification section.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.Map(
        ...     [
        ...         {Default.CODE_CLASS}.Lati('N18.150944'), 
        ...         {Default.CODE_CLASS}.Long('E168.150944')
        ...     ]
        ... )
        >>> print(m.ged())
        1 MAP
        2 LATI N18.150944
        2 LONG E168.150944
        <BLANKLINE>
        
        Since it may be difficult to convert from degrees, minutes
        and seconds to a floating point value, the `Input` class provides
        a utility to do so for Lati.  A similar one exists for Long.
        >>> from genedata.util import Input
        >>> m = {Default.CODE_CLASS}.Map(
        ...     [
        ...         {Default.CODE_CLASS}.Lati(Input.lati(18, 9, 3.4)), 
        ...         {Default.CODE_CLASS}.Long('E168.150944'),
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
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.Map(
        ...     [
        ...         {Default.CODE_CLASS}.Lati('N18.150944'), 
        ...         {Default.CODE_CLASS}.Long('E168.150944')
        ...     ]
        ... )
        >>> print(m.ged())
        1 MAP
        2 LATI N18.150944
        2 LONG E168.150944
        <BLANKLINE>
        
        Since it may be difficult to convert from degrees, minutes
        and seconds to a floating point value, the `Input` class provides
        a utility to do so for Long.  A similar one exists for Lati.
        >>> from genedata.util import Input
        >>> m = {Default.CODE_CLASS}.Map(
        ...     [
        ...         {Default.CODE_CLASS}.Lati('N18.150944'), 
        ...         {Default.CODE_CLASS}.Long(Input.long(168, 9, 3.4)),
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
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.Map(
        ...     [
        ...         {Default.CODE_CLASS}.Lati('N18.150944'), 
        ...         {Default.CODE_CLASS}.Long('E168.150944'),
        ...     ]
        ... )
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
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> {Default.CODE_GENEALOGY} = Genealogy('example')
        >>> obje_xref = {Default.CODE_GENEALOGY}.multimedia_xref('M1')

        Next construct the ged lines.  Let `photo.jpg` be the file name of the photo.
        >>> m = {Default.CODE_CLASS}.RecordObje(obje_xref, 
        ...     {Default.CODE_CLASS}.File('photo.jpg', 
        ...         {Default.CODE_CLASS}.Form('image/jpeg', 
        ...             {Default.CODE_CLASS}.Medi('PHOTO')
        ...         )
        ...     )
        ... )
        >>> print(m.ged())
        0 @M1@ OBJE
        1 FILE photo.jpg
        2 FORM image/jpeg
        3 MEDI PHOTO
        <BLANKLINE>

        This example shows a successful run of the Medi structure using
        the enumeration value 'AUDIO'.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.Medi('AUDIO')
        >>> print(m.ged(2))
        2 MEDI AUDIO
        <BLANKLINE>""",
    'NAME-TRAN': f"""

    Example:
        These are the steps to build the example in the specification.
        First the classes are imported which construct the ged lines.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.IndiName('/孔/德庸',
        ...         [
        ...             {Default.CODE_CLASS}.Givn('德庸'),
        ...             {Default.CODE_CLASS}.Surn('孔'),
        ...             {Default.CODE_CLASS}.NameTran('/Kǒng/ Déyōng',
        ...                 [
        ...                     {Default.CODE_CLASS}.Givn('Déyōng'),
        ...                     {Default.CODE_CLASS}.Surn('Kǒng'),
        ...                     {Default.CODE_CLASS}.Lang('zh-pinyin'),
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
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.IndiName('Arete /Hernandez/', 
        ...     {Default.CODE_CLASS}.Note('Named after Arete from <i>The Odyssey</i>',
        ...         [
        ...             {Default.CODE_CLASS}.Lang('en'),
        ...             {Default.CODE_CLASS}.Mime('text/html'),
        ...             {Default.CODE_CLASS}.NoteTran('Named after Arete from "The Odyssey"', 
        ...                 {Default.CODE_CLASS}.Mime('text/plain')
        ...             ),
        ...             {Default.CODE_CLASS}.NoteTran('Nombrada en honor a Arete de <i>La Odisea</i>', 
        ...                 {Default.CODE_CLASS}.Lang('es')
        ...             ),
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
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.OrdStat('BIC', 
        ...     {Default.CODE_CLASS}.DateExact('15 JAN 2020')
        ... )
        >>> print(m.ged(1))
        1 STAT BIC
        2 DATE 15 JAN 2020
        <BLANKLINE>""",
    'PAGE': f"""

    Examples:
        These are the steps to build the examples in the specification.
        First we will import the classes and then create a source cross reference `S1`.
        The void cross reference identifier comes from the Void class.
        >>> from genedata.build import Genealogy
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS} 
        >>> from genedata.structure import Void
        >>> {Default.CODE_GENEALOGY} = Genealogy('example')
        >>> sour_xref = {Default.CODE_GENEALOGY}.source_xref('S1')

        These are the steps to build the first example:
        >>> m = {Default.CODE_CLASS}.Sour(sour_xref, 
        ...     {Default.CODE_CLASS}.Page('Film: 1234567, Frame: 344, Line: 28')
        ... )
        >>> print(m.ged(2))
        2 SOUR @S1@
        3 PAGE Film: 1234567, Frame: 344, Line: 28
        <BLANKLINE>

        These are the steps to build the second example:
        >>> m = {Default.CODE_CLASS}.Dscr('Tall enough his head touched the ceiling', 
        ...     {Default.CODE_CLASS}.Sour(Void.SOUR, 
        ...         {Default.CODE_CLASS}.Page('His grand-daughter Lydia told me this in 1980')
        ...     )
        ... )
        >>> print(m.ged(1))
        1 DSCR Tall enough his head touched the ceiling
        2 SOUR @VOID@
        3 PAGE His grand-daughter Lydia told me this in 1980
        <BLANKLINE>""",
    'PEDI': f"""

    Examples:
        This example shows a successful run of the Pedi structure using
        the enumeration value 'ADOPTED'.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.Pedi('ADOPTED')
        >>> print(m.ged(1))
        1 PEDI ADOPTED
        <BLANKLINE>""",
    'PHRASE': f"""

    Examples:
        The following steps would generate the examples in the specification.
        We will need the following imports for these examples along with one
        individual cross reference identifier `I2` for the fifth example:
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> from genedata.build import Genealogy
        >>> {Default.CODE_GENEALOGY} = Genealogy('example')
        >>> indi = {Default.CODE_GENEALOGY}.individual_xref('I2')
        
        These are the steps for the first example.
        >>> m = {Default.CODE_CLASS}.Date('24 JUN 1852', 
        ...     {Default.CODE_CLASS}.Phrase('During the feast of St John')
        ... )
        >>> print(m.ged(2))
        2 DATE 24 JUN 1852
        3 PHRASE During the feast of St John
        <BLANKLINE>

        These are the steps for the second example.
        >>> m = {Default.CODE_CLASS}.Date('30 JAN 1649', 
        ...     {Default.CODE_CLASS}.Phrase('30th of January, 1648/9')
        ... )
        >>> print(m.ged(2))
        2 DATE 30 JAN 1649
        3 PHRASE 30th of January, 1648/9
        <BLANKLINE>

        These are the steps for the third example.
        >>> m = {Default.CODE_CLASS}.Date('BET 1648 AND 1649', 
        ...     {Default.CODE_CLASS}.Phrase('1648/9')
        ... )
        >>> print(m.ged(2))
        2 DATE BET 1648 AND 1649
        3 PHRASE 1648/9
        <BLANKLINE>

        These are the steps for the fourth example.
        >>> m = {Default.CODE_CLASS}.Date('BET 1 JAN 1867 AND 31 MAR 1867', 
        ...     {Default.CODE_CLASS}.Phrase('Q1 1867')
        ... )
        >>> print(m.ged(2))
        2 DATE BET 1 JAN 1867 AND 31 MAR 1867
        3 PHRASE Q1 1867
        <BLANKLINE>

        These are the steps for the fifth example.
        >>> m = {Default.CODE_CLASS}.Marr('', 
        ...     {Default.CODE_CLASS}.Asso(indi, 
        ...         {Default.CODE_CLASS}.Role('OTHER', 
        ...             {Default.CODE_CLASS}.Phrase('Maid of Honor')
        ...         )
        ...     )
        ... )
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
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> from genedata.build import Genealogy
        >>> {Default.CODE_GENEALOGY} = Genealogy('example')
        >>> sour = {Default.CODE_GENEALOGY}.source_xref('S1')
        >>> m = {Default.CODE_CLASS}.RecordSour(sour, 
        ...     {Default.CODE_CLASS}.Data(
        ...         {Default.CODE_CLASS}.DataEven('BIRT', 
        ...             {Default.CODE_CLASS}.Plac(', Oneida, Idaho, USA', 
        ...                 {Default.CODE_CLASS}.PlacForm('City, County, State, Country')
        ...             )
        ...         )
        ...     )
        ... )
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
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.Plac('Baltimore, , Maryland, USA', 
        ...     {Default.CODE_CLASS}.PlacForm('City, County, State, Country')
        ... )
        >>> print(m.ged(2))
        2 PLAC Baltimore, , Maryland, USA
        3 FORM City, County, State, Country
        <BLANKLINE>""",
    'PLAC-TRAN': f"""

    Example:
        The following steps would generate the example in the specifications.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.Plac('千代田, 東京, 日本',
        ...     [
        ...         {Default.CODE_CLASS}.PlacForm('区, 都, 国'),
        ...         {Default.CODE_CLASS}.Lang('ja'),
        ...         {Default.CODE_CLASS}.PlacTran('Chiyoda, Tokyo, Nihon', 
        ...             {Default.CODE_CLASS}.Lang('ja-Latn')
        ...         ),
        ...         {Default.CODE_CLASS}.PlacTran('Chiyoda, Tokyo, Japan', 
        ...             {Default.CODE_CLASS}.Lang('en')
        ...         ),
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
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.Quay('0')
        >>> print(m.ged(1))
        1 QUAY 0
        <BLANKLINE>""",
    'record-INDI': f"""

    Example:
        Here is the way to construct the ged lines in the example from the specification.
        First create the two individual cross reference identifiers.  Then let a
        RecordIndi class format them into the desired ged lines.
        >>> from genedata.build import Genealogy
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> {Default.CODE_GENEALOGY} = Genealogy('example')
        >>> indi_i1_xref = {Default.CODE_GENEALOGY}.individual_xref('I1')
        >>> indi_i2_xref = {Default.CODE_GENEALOGY}.individual_xref('I2')
        >>> m = {Default.CODE_CLASS}.RecordIndi(indi_i1_xref, 
        ...     {Default.CODE_CLASS}.Asso(indi_i2_xref, {Default.CODE_CLASS}.Role('GODP'))
        ... )
        >>> print(m.ged())
        0 @I1@ INDI
        1 ASSO @I2@
        2 ROLE GODP
        <BLANKLINE>""",
    'record-SNOTE': f"""

    Example:
        The example in the specification has two records: the source record
        `GORDON` and an individual `I1`.  We will create those cross
        reference identifiers first.
        >>> from genedata.build import Genealogy
        >>> {Default.CODE_GENEALOGY} = Genealogy('example')
        >>> snote_xref = {Default.CODE_GENEALOGY}.shared_note_xref('GORDON', '"Gordon" is a traditional Scottish surname.\\\\nIt became a given name in honor of Charles George Gordon.')
        >>> indi_xref = {Default.CODE_GENEALOGY}.individual_xref('I1')

        Next create the record for the shared note:
        >>> import genedata.classes7 as {Default.CODE_CLASS}
        >>> snote = {Default.CODE_CLASS}.RecordSnote(snote_xref)

        Next create the individual record.
        >>> indi = {Default.CODE_CLASS}.RecordIndi(
        ...     indi_xref,
        ...     {Default.CODE_CLASS}.IndiName('Gordon /Jones/',
        ...         [
        ...             {Default.CODE_CLASS}.Note('Named after the astronaut Gordon Cooper'),
        ...             {Default.CODE_CLASS}.Snote(snote_xref),
        ...         ]
        ...     )
        ... )
        
        Now generate the ged lines for each record separately:
        >>> print(''.join([snote.ged(), indi.ged()]))
        0 @GORDON@ SNOTE "Gordon" is a traditional Scottish surname.
        1 CONT It became a given name in honor of Charles George Gordon.
        0 @I1@ INDI
        1 NAME Gordon /Jones/
        2 NOTE Named after the astronaut Gordon Cooper
        2 SNOTE @GORDON@
        <BLANKLINE>""",
    'RESN': f"""

    Examples:
        This example shows a successful run of the Resn structure using
        the enumeration value 'CONFIDENTIAL'.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.Resn('CONFIDENTIAL')
        >>> print(m.ged(1))
        1 RESN CONFIDENTIAL
        <BLANKLINE>

        More than one enumeration value may be entered for this particular
        enumeration set by separating the values with a comma.  For example,
        >>> n = {Default.CODE_CLASS}.Resn('CONFIDENTIAL, LOCKED')
        >>> print(n.ged(1))
        1 RESN CONFIDENTIAL, LOCKED
        <BLANKLINE>""",
    'ROLE': f"""

    Examples:
        The first example of the specification could be coded by first creating
        the cross reference identifiers for the individual `I1` and the source `S1`.  
        This would be done as follows:
        >>> from genedata.build import Genealogy
        >>> {Default.CODE_GENEALOGY} = Genealogy('example')
        >>> indi = {Default.CODE_GENEALOGY}.individual_xref('I1')
        >>> sour = {Default.CODE_GENEALOGY}.source_xref('S1')

        With these cross reference identifiers we can create the ged lines:
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.RecordIndi(indi, 
        ...     {Default.CODE_CLASS}.IndiName('Mary //', 
        ...         {Default.CODE_CLASS}.Sour(sour, 
        ...             {Default.CODE_CLASS}.SourEven('BIRT', 
        ...                 {Default.CODE_CLASS}.Role('MOTH')
        ...             )
        ...         )
        ...     )
        ... )
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
        >>> indi2 = {Default.CODE_GENEALOGY}.individual_xref('I2')
        >>> indi3 = {Default.CODE_GENEALOGY}.individual_xref('I3')

        With those cross reference identifiers we can complete the ged lines
        after importing the additional classes.
        Now create the lines:
        >>> m = {Default.CODE_CLASS}.RecordIndi(indi2,
        ...     [
        ...         {Default.CODE_CLASS}.Asso(indi3, 
        ...             {Default.CODE_CLASS}.Role('FRIEND', 
        ...                 {Default.CODE_CLASS}.Phrase('best friend')
        ...             )
        ...         ),
        ...         {Default.CODE_CLASS}.Bapm('', 
        ...             {Default.CODE_CLASS}.Asso(indi3, 
        ...                 {Default.CODE_CLASS}.Role('WITN')
        ...             )
        ...         ),
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
        >>> import genedata.classes7 as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.Role('CHIL')
        >>> print(m.ged(1))
        1 ROLE CHIL
        <BLANKLINE>""",
    'SEX': f"""

    Examples:
        This example shows a successful run of the Sex structure using
        the enumeration value 'F'.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.Sex('F')
        >>> print(m.ged(1))
        1 SEX F
        <BLANKLINE>""",
    'TITL': f"""

    Examples:
        Assume that letter.pdf is a scanned copy of a letter from Ann to her husband Henry 
        on April 6, 1920.  Based on the specification one could enter this as follows.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.File('letter.pdf', 
        ...     [
        ...         {Default.CODE_CLASS}.Form('application/pdf'), 
        ...         {Default.CODE_CLASS}.Titl('Letter from Ann to Henry April 6, 1920'),
        ...     ]
        ... )
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
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> {Default.CODE_GENEALOGY} = Genealogy('test')
        >>> indi_xref = {Default.CODE_GENEALOGY}.individual_xref('I1')
        >>> m = {Default.CODE_CLASS}.RecordIndi(indi_xref, 
        ...     {Default.CODE_CLASS}.Ordn('', 
        ...         {Default.CODE_CLASS}.Type('Bishop')
        ...     )
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
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
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
    """Methods to construct classes from the GEDCOM specification."""

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
    def classname(name: str) -> str:
        return (
            name.title()
            .replace(Default.UNDERLINE, Default.EMPTY)
            .replace(Default.HYPHEN, Default.EMPTY)
        )

    @staticmethod
    def tableheader() -> str:
        return """
    |               Specification                | Quantity | Required |  Class Name  |
    | ------------------------------------------ | -------- | -------- | ------------ |"""

    @staticmethod
    def generate__all__(url: str) -> str:
        """Generate the __all__ = [] by filling in the list with the modified keys from Structure."""
        count: int = 0
        lines: str = '__all__ = [    # noqa: RUF022'
        directory: str = f'{Convert.get_slash(url)}{Default.URL_STRUCTURE}'
        p = Path(directory)
        if p.exists():
            for file in p.iterdir():
                if file.suffix == Default.YAML_FILE_END:
                    key = file.stem.replace(
                        Default.URL_STRUCTURE_PREFIX, Default.EMPTY
                    )
                    if key not in [Default.CONT, Default.TRLR]:
                        edited_key: str = Construct.classname(key)
                        lines = f"{lines}{Default.EOL}{Default.INDENT}'{edited_key}'{Default.COMMA}"
                        count += 1
        else:
            raise ValueError(Msg.DIRECTORY_NOT_FOUND.format(directory))
        if count == 0:
            return Default.EMPTY
        return f'{lines}{Default.EOL}]{Default.EOL}'

    @staticmethod
    def generate_imports() -> str:
        return f"""
import logging
from typing import Any

from genedata.messages import Msg
from genedata.structure import (
    BaseStructure,
    {Default.XREF_FAMILY},
    {Default.XREF_INDIVIDUAL},
    {Default.XREF_MULTIMEDIA},
    {Default.XREF_REPOSITORY},
    {Default.XREF_SHARED_NOTE},
    {Default.XREF_SOURCE},
    {Default.XREF_SUBMITTER},
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
                f'{Default.EOL}[BCP 47](https://en.wikipedia.org/wiki/IETF_language_tag)',
            )
            .replace(
                '[documented extension tag]',
                f'[documented extension tag]({site}#extension-tags)',
            )
            .replace('[E.123]', '[E.123](https://en.wikipedia.org/wiki/E.123)')
            .replace(
                '[E.164]',
                f'{Default.EOL}[E.164](https://en.wikipedia.org/wiki/E.164)',
            )
            .replace(
                '[exid-types registry]',
                f'{Default.EOL}[exid-types registry]({site}#EXID)',
            )
            .replace(
                '[Extensions]', f'{Default.EOL}[Extensions]({site}#extensions)'
            )
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
            .replace('[List]', f'[List]({site}#list){Default.EOL}')
            .replace(
                '[media type]',
                f'[media type]({site}#media-type){Default.EOL}',
            )
            .replace(
                '[Removing data]',
                f'{Default.EOL}[Removing data]({site}#removing-data)',
            )
            .replace(
                '[registry of component subtags] ',
                '[registry of component subtags](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry)\n',
            )
            .replace('[RFC 3696]', f'[RFC 3696]({datatracker}3696)')
            .replace(
                f'[RFC{Default.EOL}3696]',
                f'{Default.EOL}[RFC 3696]({datatracker}3696)',
            )
            .replace(
                f'[RFC{Default.EOL}3986]',
                f'{Default.EOL}[RFC 3986]({datatracker}3986)',
            )
            .replace(
                '[RFC 3987]', f'{Default.EOL}[RFC 3987]({datatracker}3987)'
            )
            .replace('[RFC 4122]', f'[RFC 4122]({datatracker}4122)')
            .replace(
                '[RFC 5321]', f'{Default.EOL}[RFC 5321]({datatracker}5321)'
            )
            .replace(
                '[RFC 5322]', f'{Default.EOL}[RFC 5322]({datatracker}5322)'
            )
            .replace('. See also ', f'.{Default.EOL}See also ')
            .replace(
                '[The Header and Trailer]',
                f'{Default.EOL}[The Header and Trailer]({site}#the-header)',
            )
            .replace(
                '[whatwg/url]',
                f'{Default.EOL}[whatwg/url](https://url.spec.whatwg.org/)',
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
            if (
                Default.EOL not in string_linked
                and len(string_linked) > Default.LINE_LENGTH
            ):
                wrapped = wrap(
                    string_linked,
                    Default.LINE_LENGTH,
                    break_long_words=False,
                    break_on_hyphens=False,
                )
                if len(wrapped) > 1:
                    for index, line in enumerate(wrapped):
                        if index == 0:
                            spec = ''.join(
                                [spec, Default.YAML_WITH_HYPHEN, line]
                            )
                        else:
                            spec = ''.join(
                                [spec, Default.YAML_WITHOUT_HYPHEN, line]
                            )
            elif Default.EOL in string_linked:
                string_linked_split: list[str] = string_linked.split('\n')
                for line in string_linked_split:
                    if len(line) > 80:
                        line_wrapped: list[str] = wrap(
                            line,
                            75,
                            break_long_words=False,
                            break_on_hyphens=False,
                        )
                        if len(line_wrapped) > 1:
                            for index, item in enumerate(line_wrapped):
                                if index == 0:
                                    spec = ''.join(
                                        [spec, Default.YAML_WITH_HYPHEN, item]
                                    )
                                else:
                                    spec = ''.join(
                                        [
                                            spec,
                                            Default.YAML_WITHOUT_HYPHEN,
                                            item,
                                        ]
                                    )
                    else:
                        spec = ''.join(
                            [spec, Default.YAML_WITHOUT_HYPHEN, line]
                        )
            else:
                spec = ''.join([spec, Default.YAML_WITH_HYPHEN, string_linked])
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
        key: str, structure: dict[str, Any], enumerationset: dict[str, Any]
    ) -> str:
        """Construct the Enumerations section of the documentation."""
        enumeration_values: str = Default.EMPTY
        if (
            Default.YAML_ENUMERATION_SET in structure[key]
            and structure[key][Default.YAML_ENUM_KEY] != Default.EMPTY
        ):
            enum_key: str = structure[key][Default.YAML_ENUM_KEY]
            enumeration_values = """

    Enumeration Values:"""
            for value in enumerationset[enum_key][
                Default.YAML_ENUMERATION_VALUES
            ]:
                enumeration_values = ''.join(
                    [
                        enumeration_values,
                        Default.EOL,
                        Default.INDENT,
                        Default.HYPHEN,
                        Default.SPACE,
                        Default.BRACKET_LEFT,
                        Convert.get_enum_tag(value),
                        Default.BRACKET_RIGHT,
                        Default.PARENS_LEFT,
                        value,
                        Default.PARENS_RIGHT,
                    ]
                )
        return enumeration_values

    @staticmethod
    def generate_substructures(key: str, structure: dict[str, Any]) -> str:
        """Construct the Substructures section of the documentation."""
        class_name: str = Default.EMPTY
        subs: dict[str, str] = {}
        if Default.YAML_SUBSTRUCTURES in structure[key]:
            subs = structure[key][Default.YAML_SUBSTRUCTURES]
        substructures: str = Default.EMPTY
        if len(subs) > 0:
            substructures = f"""

    Substructures:{Construct.tableheader()}"""

            for subskey, value in subs.items():
                yes: str = Default.NO
                one: str = Default.MANY
                if Default.YAML_CARDINALITY_REQUIRED in value:
                    yes = Default.YES
                if Default.YAML_CARDINALITY_SINGULAR in value:
                    one = Default.ONLY_ONE
                class_name = Construct.classname(
                    subskey[subskey.rfind(Default.SLASH) + 1 :]
                )
                substructures = ''.join(
                    [
                        substructures,
                        Default.EOL,
                        Default.INDENT,
                        Default.BAR,
                        Default.SPACE,
                        subskey,
                        Default.SPACE * (42 - len(subskey) + 1),
                        Default.BAR,
                        Default.SPACE,
                        one,
                        Default.SPACE * (8 - len(one) + 1),
                        Default.BAR,
                        Default.SPACE,
                        yes,
                        Default.SPACE * (8 - len(yes) + 1),
                        Default.BAR,
                        Default.SPACE,
                        class_name,
                        Default.SPACE * (12 - len(class_name) + 1),
                        Default.BAR,
                        Default.SPACE,
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
            superstructures = f"""

    Superstructures:{Construct.tableheader()}"""
            for superskey, value in supers.items():
                yes: str = Default.NO
                one: str = Default.MANY
                if Default.YAML_CARDINALITY_REQUIRED in value:
                    yes = Default.YES
                if Default.YAML_CARDINALITY_SINGULAR in value:
                    one = Default.ONLY_ONE
                class_name = Construct.classname(
                    superskey[superskey.rfind(Default.SLASH) + 1 :]
                )
                superstructures = ''.join(
                    [
                        superstructures,
                        Default.EOL,
                        Default.INDENT,
                        Default.BAR,
                        Default.SPACE,
                        superskey,
                        Default.SPACE * (42 - len(superskey) + 1),
                        Default.BAR,
                        Default.SPACE,
                        one,
                        Default.SPACE * (8 - len(one) + 1),
                        Default.BAR,
                        Default.SPACE,
                        yes,
                        Default.SPACE * (8 - len(yes) + 1),
                        Default.BAR,
                        Default.SPACE,
                        class_name,
                        Default.SPACE * (12 - len(class_name) + 1),
                        Default.BAR,
                    ]
                )
        return superstructures

    @staticmethod
    def generate_value_of(key: str, structure: dict[str, Any]) -> str:
        """Construct the Enumerations section of the documentation."""
        value_of: str = Default.EMPTY
        if Default.YAML_VALUE_OF in structure[key]:
            value_of = """

    Enumeration Value Of:"""
            for value in structure[key][Default.YAML_VALUE_OF]:
                value_of = f'{value_of}{Default.EOL}{Default.INDENT}{Default.HYPHEN} {value}'
        return value_of

    @staticmethod
    def generate_args(key: str, structure: dict[str, Any]) -> str:
        """Construct the Args section of the documentation."""
        args = """
        
    Args:"""
        if (
            Default.YAML_PAYLOAD in structure[key]
            and structure[key][Default.YAML_PAYLOAD] is not None
            and key[0:6] != Default.RECORD
        ):
            args = ''.join(
                [
                    args,
                    Default.EOL,
                    Default.INDENT * 2,
                    Default.CODE_VALUE,
                    ': A value of data type ',
                    structure[key][Default.YAML_PAYLOAD],
                ]
            )
        if key[0:6] == Default.RECORD:
            args = ''.join(
                [
                    args,
                    Default.EOL,
                    Default.INDENT * 2,
                    Default.CODE_VALUE,
                    ': A value of data type ',
                    Construct.get_record_datatype(key),
                ]
            )
        return ''.join(
            [
                args,
                Default.EOL,
                Default.INDENT * 2,
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
                return Default.XREF_INDIVIDUAL
            case '@<https://gedcom.io/terms/v7/record-FAM>@':
                return Default.XREF_FAMILY
            case '@<https://gedcom.io/terms/v7/record-SUBM>@':
                return Default.XREF_SUBMITTER
            case '@<https://gedcom.io/terms/v7/record-OBJE>@':
                return Default.XREF_MULTIMEDIA
            case '@<https://gedcom.io/terms/v7/record-REPO>@':
                return Default.XREF_REPOSITORY
            case '@<https://gedcom.io/terms/v7/record-SNOTE>@':
                return Default.XREF_SHARED_NOTE
            case '@<https://gedcom.io/terms/v7/record-SOUR>@':
                return Default.XREF_SOURCE
            case _:
                return 'str'

    @staticmethod
    def get_record_datatype(key: str) -> str:
        """Assign a cross reference datatype to specific records."""
        datatype: str = key[7:]
        result: str = Default.EMPTY
        match datatype:
            case Default.TAG_FAM:
                result = Default.XREF_FAMILY
            case Default.TAG_INDI:
                result = Default.XREF_INDIVIDUAL
            case Default.TAG_OBJE:
                result = Default.XREF_MULTIMEDIA
            case Default.TAG_REPO:
                result = Default.XREF_REPOSITORY
            case Default.TAG_SNOTE:
                result = Default.XREF_SHARED_NOTE
            case Default.TAG_SOUR:
                result = Default.XREF_SOURCE
            case Default.TAG_SUBM:
                result = Default.XREF_SUBMITTER
        return result

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
        init: str = f"{Default.EOL}    key: str = '{key}'"
        if payload == Default.EMPTY or key == 'record-SNOTE':
            value_arg = Default.EMPTY
            value_init = 'None'
            if 'record-' in key:
                init = f"{Default.EOL}    key: str = '{key}'"
                value_arg = f', {Default.CODE_VALUE}: {Construct.get_record_datatype(key)}'
                value_init = Default.CODE_VALUE
        deprecation_line: str = Default.EMPTY
        if key in ['ADR1', 'ADR2', 'ADR3']:
            deprecation_line = f'{Default.EOL}        logging.info(Msg.DEPRECATION_WARNING.format(self.class_name))'
        init_line: str = f"""
        
    def __init__(self{value_arg}{subs_arg}) -> None:
        super().__init__({value_init}, {subs_init}, self.key){deprecation_line}"""
        return ''.join([init, init_line])

    @staticmethod
    def generate_class(
        key: str,
        url: str,
        structure_dictionary: dict[str, Any] | None = None,
        enumerationset_dictionary: dict[str, Any] | None = None,
    ) -> str:
        """Generate a single class and its documentation defined by its Structure definition.

        Args:
            key: The key of the Structure dictionary.
            url: The source of the yaml files where one can read the structure and enumeration dictionaries.
            structure_dictionary: The structure dictionary as an alternative to using the url to get this.
            enumeration_dictionary: The enumeration dictionary as an alternative to using the url to get this.
        """
        base_url: str = Convert.get_slash(url)
        if structure_dictionary is None:
            structure_dictionary = {}
        if enumerationset_dictionary is None:
            enumerationset_dictionary = {}
        structure: dict[str, Any] = structure_dictionary
        if len(structure) == 0:
            structure = eval(Convert.structure_dictionary(base_url))
        enumerationset: dict[str, Any] = enumerationset_dictionary
        if len(enumerationset) == 0:
            enumerationset = eval(Convert.enumeration_dictionary(base_url))
        tag: str = structure[key][Default.YAML_STANDARD_TAG]
        class_name: str = structure[key][Default.YAML_CLASS_NAME]
        parts: str = ''.join(
            [
                Construct.generate_specification(key, structure),
                Construct.generate_examples(key),
                Construct.generate_substructures(key, structure),
                Construct.generate_superstructures(key, structure),
                Construct.generate_enumerations(key, structure, enumerationset),
                Construct.generate_value_of(key, structure),
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

        base_url: str = Convert.get_slash(url)
        structure: dict[str, Any] = eval(Convert.structure_dictionary(base_url))
        enumerationset: dict[str, Any] = eval(
            Convert.enumerationset_dictionary(base_url)
        )
        lines: str = Default.EMPTY
        for key in structure:
            if key not in [Default.CONT, Default.TRLR]:
                lines = ''.join(
                    [
                        lines,
                        Construct.generate_class(
                            key, url, structure, enumerationset
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
                Construct.generate__all__(url),
                Construct.generate_imports(),
                Construct.generate_all_classes(url),
            ]
        )
