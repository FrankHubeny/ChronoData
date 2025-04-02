# mypy: disable-error-code="name-defined"
"""Load a version of the GEDCOM specifications into python dictionaries,
generate classes from the loaded specifications and generate test modules for those classes.

"""

__all__ = ['Specs']

from pathlib import Path

from genedata.constants import Default
from genedata.messages import Msg
from genedata.methods import Names, Util


class Specs:
    """Read and store GEDCOM specification."""

    # enumerationset_dict: ClassVar[dict[str, Any]] = {}

    @staticmethod
    def preamble(source: str, version: str) -> str:
        lines: str = f'''"""Store the GEDCOM verson {version} specifications in a dictionary format from yaml files.

This is a generated module. DO NOT MODIFY THIS MODULE MANUALLY.  

Changes should be made to the `{__class__.__name__}` class in the `{__name__}` module.

The specification was obtained from the [GEDCOM-registeries]({source})
made available under the Apache 2.0 license.

The names of the dictionaries are based on the directories in this registry.  Each yaml file
in the directory is read into the appropriate dictionary with the stem of the yaml file acting as the key
and the contents of the yaml file being its value.

The following dictionaries are available.  Each key in the dictionary corresponds to a
single yaml file.
- `Calendar` corresponding to yaml files in the calendar directory.
- `DataType` corresponding to yaml files in the data-type directory.
- `Enumeration` corresponding to yaml files in the enumeration directory.
- `EnumerationSet` corresponding to yaml files in the enumeration-set directory.
- `Month` corresponding to yaml files in the month directory.
- `Structure` corresponding to yaml files in the structure/standard directory.
- `ExtensionStructure` corresponding to yaml files in the structure/extenion directory.
- `Uri` corresponding to yaml files in the uri directory.

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
    def dictionary(
        url: str,
        base: str,
    ) -> str:
        lines: str = Default.BRACE_LEFT
        directory: str = f'{Names.slash(url)}{base}'
        p = Path(directory)
        if p.exists():
            for file in p.iterdir():
                if file.suffix == Default.YAML_FILE_END:
                    yamldict = Util.read_yaml(str(file))
                    # if base in [Default.URL_STRUCTURE, Default.URL_STRUCTURE_EXTENSION]:
                    #     for _key, value in yamldict.items():
                    #         if value[Default.YAML_PAYLOAD] is None:
                    #             value[Default.YAML_PAYLOAD] = 'None'
                    lines = (
                        f"{lines}{Default.EOL}    '{file.stem}': {yamldict},"
                    )
        else:
            raise ValueError(Msg.DIRECTORY_NOT_FOUND.format(directory))
        if lines == Default.BRACE_LEFT:
            return ''.join([lines, Default.BRACE_RIGHT])
        return ''.join([lines, Default.EOL, Default.BRACE_RIGHT])

    @staticmethod
    def calendar_dictionary(url: str) -> str:
        """Retrive the calendar dictionary as a string that can be sent to `eval`."""
        return Specs.dictionary(url, Default.URL_CALENDAR)

    @staticmethod
    def calendar(url: str) -> str:
        """Format the calendar dictionary for use in the specs module."""
        return ''.join(
            [
                'Calendar: dict[str, dict[str, Any]] = ',
                Specs.calendar_dictionary(url),
                Default.EOL,
                Default.EOL,
            ]
        )

    @staticmethod
    def datatype_dictionary(url: str) -> str:
        """Retrive the data type dictionary as a string that can be sent to `eval`."""
        return Specs.dictionary(url, Default.URL_DATATYPE)

    @staticmethod
    def datatype(url: str) -> str:
        """Format the data type dictionary for use in the specs module."""
        return ''.join(
            [
                'DataType: dict[str, dict[str, Any]] = ',
                Specs.datatype_dictionary(url),
                Default.EOL,
                Default.EOL,
            ]
        )

    @staticmethod
    def enumeration_dictionary(url: str) -> str:
        """Retrive the enumeration dictionary as a string that can be sent to `eval`."""
        return Specs.dictionary(url, Default.URL_ENUMERATION)

    @staticmethod
    def enumeration(url: str) -> str:
        """Format the enumeration dictionary for use in the specs module."""
        return ''.join(
            [
                'Enumeration: dict[str, dict[str, Any]] = ',
                Specs.enumeration_dictionary(url),
                Default.EOL,
                Default.EOL,
            ]
        )

    @staticmethod
    def enumerationset_dictionary(url: str) -> str:
        """Retrive the enumeration set dictionary as a string that can be sent to `eval`."""
        return Specs.dictionary(url, Default.URL_ENUMERATION_SET)

    @staticmethod
    def enumerationset(url: str) -> str:
        """Format the enumeration set dictionary for use in the specs module."""
        return ''.join(
            [
                'EnumerationSet: dict[str, dict[str, Any]] = ',
                Specs.enumerationset_dictionary(url),
                Default.EOL,
                Default.EOL,
            ]
        )

    @staticmethod
    def month_dictionary(url: str) -> str:
        """Retrive the month dictionary as a string that can be sent to `eval`."""
        return Specs.dictionary(url, Default.URL_MONTH)

    @staticmethod
    def month(url: str) -> str:
        """Format the month dictionary for use in the specs module."""
        return ''.join(
            [
                'Month: dict[str, dict[str, Any]] = ',
                Specs.month_dictionary(url),
                Default.EOL,
                Default.EOL,
            ]
        )

    @staticmethod
    def structure_dictionary(url: str) -> str:
        """Retrive the structure dictionary as a string that can be sent to `eval`."""
        return Specs.dictionary(url, Default.URL_STRUCTURE)

    @staticmethod
    def structure(url: str) -> str:
        """Format the structure dictionary for use in the specs module."""
        return ''.join(
            [
                'Structure: dict[str, dict[str, Any]] = ',
                Specs.structure_dictionary(url).replace("'payload': None,", "'payload': 'None',"),
                Default.EOL,
                Default.EOL,
            ]
        )

    @staticmethod
    def structure_extension_dictionary(url: str) -> str:
        """Retrive the extension structure dictionary as a string that can be sent to `eval`."""
        return Specs.dictionary(
            url,
            Default.URL_STRUCTURE_EXTENSION,
        )

    @staticmethod
    def structure_extension(url: str) -> str:
        """Format the extension structure dictionary for use in the specs module."""
        return ''.join(
            [
                'ExtensionStructure: dict[str, dict[str, Any]] = ',
                Specs.structure_extension_dictionary(url),
                Default.EOL,
                Default.EOL,
            ]
        )

    @staticmethod
    def uri_dictionary(url: str) -> str:
        """Retrive the uri dictionary as a string that can be sent to `eval`."""
        return Specs.dictionary(url, Default.URL_URI)

    @staticmethod
    def uri(url: str) -> str:
        """Format the uri dictionary for use in the specs module."""
        return ''.join(
            [
                'Uri: dict[str, dict[str, Any]] = ',
                Specs.uri_dictionary(url),
                Default.EOL,
                Default.EOL,
            ]
        )

    @staticmethod
    def build_all(source: str, version: str, url: str) -> str:
        return ''.join(
            [
                Specs.preamble(source, version),
                Specs.calendar(url),
                Specs.datatype(url),
                Specs.enumeration(url),
                Specs.enumerationset(url),
                Specs.month(url),
                Specs.structure(url),
                Specs.structure_extension(url),
                Specs.uri(url),
            ]
        )


# class Tests:
#     """Generate tests for the classes based on the specifications."""

#     @staticmethod
#     def preamble(name: str, version: str = '7') -> str:
#         extra_import: str = Default.EMPTY
#         if name in [
#             Default.TEST_PAYLOAD,
#             Default.TEST_REQUIRED,
#             Default.TEST_PERMITTED,
#             Default.TEST_SINGLE,
#         ]:
#             extra_import = '\n\nimport pytest\n\n'
#         return f"""The {name} tests in this module were generated by {__class__.__name__} in the {__name__} module.

# DO NOT MODIFY THIS FILE MANUALLY.{extra_import}

# import genedata.classes{version} as {Default.CODE_CLASS}
# from genedata.build import Genealogy

# """

#     @staticmethod
#     def build_all(
#         name: str, version: str, structure: dict[str, dict[str, Any]]
#     ) -> str:
#         lines: str = Tests.preamble(name, version)

#         return lines

#     @staticmethod
#     def no_subs_good_test(
#         key: str, value: str | int, xref: str = Default.EMPTY
#     ) -> str:
#         class_name: str = Names.classname(key)
#         xref_code: str = Default.EMPTY
#         input: str | int = f"'{value}'"
#         if value == Default.EMPTY:
#             input = ''
#         if isinstance(value, int):
#             input = value
#         if xref != Default.EMPTY:
#             input = f'{xref}'
#             xref_code = f"""g = Genealogy('test')
#     {xref} = g.{xref}_xref('1')
#     """
#             if xref == 'shared_note':
#                 xref_code = """g = Genealogy('test')
#     shared_note = g.shared_note_xref('1', 'text')
#     """
#         lines: str = f"""

# def test_no_subs_{class_name}() -> None:
#     '''Validate the {class_name} structure with a value, but without substructures.'''
#     {xref_code}m = {Default.CODE_CLASS}.{class_name}({input})
#     assert m.validate()
# """
#         return lines

#     @staticmethod
#     def build_no_subs_good_tests(
#         structure: dict[str, dict[str, Any]],
#         enumerationset: dict[str, dict[str, Any]],
#     ) -> str:
#         lines: str = f"""'''The tests in this file have been generated from the specs module
# to test the classes in the classes module.  None of these have required substructures
# nor exercise the use ob substructures.

# DO NOT MANUALLY MODIFY THIS FILE.
# '''

# import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
# from genedata.build import Genealogy
# """
#         input: str = 'abc'
#         for key, value in structure.items():
#             if len(value[Default.YAML_REQUIRED]) == 0 and key not in [
#                 Default.TRLR,
#                 Default.CONT,
#             ]:
#                 match value[Default.YAML_PAYLOAD]:
#                     case 'http://www.w3.org/2001/XMLSchema#string':
#                         match key:
#                             case 'LATI':
#                                 lines = ''.join(
#                                     [
#                                         lines,
#                                         Tests.no_subs_good_test(key, 'N10.1'),
#                                     ]
#                                 )
#                             case 'LONG':
#                                 lines = ''.join(
#                                     [
#                                         lines,
#                                         Tests.no_subs_good_test(key, 'E10.1'),
#                                     ]
#                                 )
#                             case 'record-SNOTE':
#                                 lines = ''.join(
#                                     [
#                                         lines,
#                                         Tests.no_subs_good_test(
#                                             key, '', 'shared_note'
#                                         ),
#                                     ]
#                                 )
#                             case _:
#                                 lines = ''.join(
#                                     [lines, Tests.no_subs_good_test(key, input)]
#                                 )
#                     case 'Y|<NULL>':
#                         lines = ''.join(
#                             [lines, Tests.no_subs_good_test(key, 'Y')]
#                         )
#                     case None:
#                         match key:
#                             case 'record-INDI':
#                                 lines = ''.join(
#                                     [
#                                         lines,
#                                         Tests.no_subs_good_test(
#                                             key, '', 'individual'
#                                         ),
#                                     ]
#                                 )
#                             case 'record-FAM':
#                                 lines = ''.join(
#                                     [
#                                         lines,
#                                         Tests.no_subs_good_test(
#                                             key, '', 'family'
#                                         ),
#                                     ]
#                                 )
#                             # case 'record-SNOTE':
#                             #     lines = ''.join(
#                             #         [
#                             #             lines,
#                             #             Tests.no_subs_good_test(
#                             #                 key, '', 'shared_note'
#                             #             ),
#                             #         ]
#                             #     )
#                             case 'record-SOUR':
#                                 lines = ''.join(
#                                     [
#                                         lines,
#                                         Tests.no_subs_good_test(
#                                             key, '', 'source'
#                                         ),
#                                     ]
#                                 )
#                             case _:
#                                 lines = ''.join(
#                                     [lines, Tests.no_subs_good_test(key, '')]
#                                 )
#                     case 'https://gedcom.io/terms/v7/type-Enum':
#                         enum = enumerationset[value[Default.YAML_ENUM_KEY]][
#                             Default.YAML_ENUM_TAGS
#                         ][0]
#                         lines = ''.join(
#                             [lines, Tests.no_subs_good_test(key, enum)]
#                         )
#                     case 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger':
#                         lines = ''.join(
#                             [lines, Tests.no_subs_good_test(key, 1)]
#                         )
#                     case '@<https://gedcom.io/terms/v7/record-INDI>@':
#                         lines = ''.join(
#                             [
#                                 lines,
#                                 Tests.no_subs_good_test(key, '', 'individual'),
#                             ]
#                         )
#                     case '@<https://gedcom.io/terms/v7/record-FAM>@':
#                         lines = ''.join(
#                             [lines, Tests.no_subs_good_test(key, '', 'family')]
#                         )
#                     case 'https://gedcom.io/terms/v7/type-List#Text':
#                         lines = ''.join(
#                             [lines, Tests.no_subs_good_test(key, input)]
#                         )
#                     case '@<https://gedcom.io/terms/v7/record-SUBM>@':
#                         lines = ''.join(
#                             [
#                                 lines,
#                                 Tests.no_subs_good_test(key, '', 'submitter'),
#                             ]
#                         )
#                     case 'http://www.w3.org/2001/XMLSchema#Language':
#                         lines = ''.join(
#                             [lines, Tests.no_subs_good_test(key, 'en-US')]
#                         )
#                     case 'https://gedcom.io/terms/v7/type-Date#period':
#                         lines = ''.join(
#                             [
#                                 lines,
#                                 Tests.no_subs_good_test(
#                                     key, 'FROM 1 DEC 2000 TO 5 DEC 2000'
#                                 ),
#                             ]
#                         )
#                     case 'https://gedcom.io/terms/v7/type-List#Enum':
#                         enum = enumerationset[value[Default.YAML_ENUM_KEY]][
#                             Default.YAML_ENUM_TAGS
#                         ][0]
#                         lines = ''.join(
#                             [lines, Tests.no_subs_good_test(key, enum)]
#                         )
#                     case 'https://gedcom.io/terms/v7/type-Date#exact':
#                         lines = ''.join(
#                             [lines, Tests.no_subs_good_test(key, '1 JAN 2026')]
#                         )
#                     case 'https://gedcom.io/terms/v7/type-Date':
#                         lines = ''.join(
#                             [lines, Tests.no_subs_good_test(key, '1 JAN 2026')]
#                         )
#                     # case 'https://gedcom.io/terms/v7/type-FilePath':
#                     #     lines = ''.join(
#                     #         [
#                     #             lines,
#                     #             Tests.no_subs_good_test(
#                     #                 key, 'dir/to/somewhere'
#                     #             ),
#                     #         ]
#                     #     )
#                     case 'http://www.w3.org/ns/dcat#mediaType':
#                         lines = ''.join(
#                             [lines, Tests.no_subs_good_test(key, 'mime/text')]
#                         )
#                     case 'https://gedcom.io/terms/v7/type-Name':
#                         lines = ''.join(
#                             [lines, Tests.no_subs_good_test(key, 'John /Doe/')]
#                         )
#                     case 'https://gedcom.io/terms/v7/type-Age':
#                         lines = ''.join(
#                             [
#                                 lines,
#                                 Tests.no_subs_good_test(key, '> 25y 10m 1d'),
#                             ]
#                         )
#                     case '@<https://gedcom.io/terms/v7/record-OBJE>@':
#                         lines = ''.join(
#                             [
#                                 lines,
#                                 Tests.no_subs_good_test(key, '', 'multimedia'),
#                             ]
#                         )
#                     case '@<https://gedcom.io/terms/v7/record-REPO>@':
#                         lines = ''.join(
#                             [
#                                 lines,
#                                 Tests.no_subs_good_test(key, '', 'repository'),
#                             ]
#                         )
#                     case '@<https://gedcom.io/terms/v7/record-SNOTE>@':
#                         lines = ''.join(
#                             [
#                                 lines,
#                                 Tests.no_subs_good_test(key, '', 'shared_note'),
#                             ]
#                         )
#                     case '@<https://gedcom.io/terms/v7/record-SOUR>@':
#                         lines = ''.join(
#                             [lines, Tests.no_subs_good_test(key, '', 'source')]
#                         )
#                     case 'https://gedcom.io/terms/v7/type-Time':
#                         lines = ''.join(
#                             [lines, Tests.no_subs_good_test(key, '12:12:12')]
#                         )
#         return lines

#     @staticmethod
#     def one_sub_good_test(
#         key: str,
#         value: str | int,
#         sub_class_name: str,
#         xref: str = Default.EMPTY,
#     ) -> str:
#         class_name: str = Names.classname(key)
#         xref_code: str = Default.EMPTY
#         sub_input: str | int = "'abc'"
#         match sub_class_name:
#             case 'DateExact':
#                 sub_input = "'1 JAN 2000'"
#             case 'Form':
#                 sub_input = "'text/html'"
#             case 'Role':
#                 sub_input = "'WITN'"
#             case 'Type':
#                 sub_input = "'Bishop'"
#             case 'Age':
#                 sub_input = "'> 25y'"
#         # if isinstance(value, int):
#         #     sub_input = sub_value
#         input: str | int = f"'{value}'"
#         if isinstance(value, int):
#             input = value
#         if xref != Default.EMPTY:
#             input = f'{xref}'
#             xref_code = f"""g = Genealogy('test')
#     {xref} = g.{xref}_xref('1')
#     """
#         #         if xref == 'shared_note':
#         #             xref_code = """g = Genealogy('test')
#         # shared_note = g.shared_note_xref('1', 'text')
#         # """
#         lines: str = f"""

# def test_one_sub_{class_name}() -> None:
#     '''Validate the {class_name} structure with a value and one substructure.'''
#     {xref_code}m = {Default.CODE_CLASS}.{class_name}({input}, {Default.CODE_CLASS}.{sub_class_name}({sub_input}))
#     assert m.validate()
# """
#         return lines

#     @staticmethod
#     def build_one_sub_good_tests(
#         structure: dict[str, dict[str, Any]],
#         enumerationset: dict[str, dict[str, Any]],
#     ) -> str:
#         lines: str = f"""'''The {Default.TEST_BASE} tests in this file have been generated 
# from the `{__class__.__name__}` class of the `{__name__}` module.

# DO NOT MANUALLY MODIFY THIS FILE.
# '''

# import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
# from genedata.build import Genealogy
# """
#         input: str = 'abc'
#         for key, value in structure.items():
#             if (
#                 key not in [Default.TRLR, Default.CONT]
#                 and len(value[Default.YAML_REQUIRED]) < 2
#                 and len(value[Default.YAML_PERMITTED]) > 0
#             ):
#                 sub_permitted: list[str] = value[Default.YAML_PERMITTED]
#                 sub_class_name: str = Default.EMPTY
#                 for item in [
#                     'Age',
#                     'DateExact',
#                     'Form',
#                     'Gedc',
#                     'GedcVers',
#                     'HeadPlacForm',
#                     'Mime',
#                     'Name',
#                     'Note',
#                     'Phrase',
#                     'Phon',
#                     'Role',
#                     'Time',
#                     'Titl',
#                     'Type',
#                 ]:
#                     if item in sub_permitted:
#                         sub_class_name = item
#                         break
#                 if len(value[Default.YAML_REQUIRED]) == 1:
#                     sub_class_name = value[Default.YAML_REQUIRED][0]
#                 if sub_class_name != Default.EMPTY:
#                     match value[Default.YAML_PAYLOAD]:
#                         case 'http://www.w3.org/2001/XMLSchema#string':
#                             # match key:
#                             #     case 'LATI':
#                             #         lines = ''.join(
#                             #             [
#                             #                 lines,
#                             #                 Tests.one_sub_good_test(
#                             #                     key, 'N10.1', sub_class_name
#                             #                 ),
#                             #             ]
#                             #         )
#                             #     case 'LONG':
#                             #         lines = ''.join(
#                             #             [
#                             #                 lines,
#                             #                 Tests.one_sub_good_test(
#                             #                     key, 'E10.1', sub_class_name
#                             #                 ),
#                             #             ]
#                             #         )
#                             #     case 'record-SNOTE':
#                             #         lines = ''.join(
#                             #             [
#                             #                 lines,
#                             #                 Tests.one_sub_good_test(
#                             #                     key,
#                             #                     '',
#                             #                     sub_class_name,
#                             #                     'shared_note',
#                             #                 ),
#                             #             ]
#                             #         )
#                             #     case _:
#                             lines = ''.join(
#                                 [
#                                     lines,
#                                     Tests.one_sub_good_test(
#                                         key, input, sub_class_name
#                                     ),
#                                 ]
#                             )
#                         case 'Y|<NULL>':
#                             lines = ''.join(
#                                 [
#                                     lines,
#                                     Tests.one_sub_good_test(
#                                         key, 'Y', sub_class_name
#                                     ),
#                                 ]
#                             )
#                         case None:
#                             match key:
#                                 case 'record-INDI':
#                                     lines = ''.join(
#                                         [
#                                             lines,
#                                             Tests.one_sub_good_test(
#                                                 key,
#                                                 '',
#                                                 sub_class_name,
#                                                 'individual',
#                                             ),
#                                         ]
#                                     )
#                                 case 'record-FAM':
#                                     lines = ''.join(
#                                         [
#                                             lines,
#                                             Tests.one_sub_good_test(
#                                                 key,
#                                                 '',
#                                                 sub_class_name,
#                                                 'family',
#                                             ),
#                                         ]
#                                     )
#                                 # case 'record-SNOTE':
#                                 #     lines = ''.join(
#                                 #         [
#                                 #             lines,
#                                 #             Tests.one_sub_good_test(
#                                 #                 key,
#                                 #                 '',
#                                 #                 sub_class_name,
#                                 #                 'shared_note',
#                                 #             ),
#                                 #         ]
#                                 #     )
#                         case 'https://gedcom.io/terms/v7/type-Enum':
#                             enum = enumerationset[value[Default.YAML_ENUM_KEY]][
#                                 Default.YAML_ENUM_TAGS
#                             ][0]
#                             lines = ''.join(
#                                 [
#                                     lines,
#                                     Tests.one_sub_good_test(
#                                         key, enum, sub_class_name
#                                     ),
#                                 ]
#                             )
#                         case 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger':
#                             lines = ''.join(
#                                 [
#                                     lines,
#                                     Tests.one_sub_good_test(
#                                         key, 1, sub_class_name
#                                     ),
#                                 ]
#                             )
#                         case '@<https://gedcom.io/terms/v7/record-INDI>@':
#                             lines = ''.join(
#                                 [
#                                     lines,
#                                     Tests.one_sub_good_test(
#                                         key, '', sub_class_name, 'individual'
#                                     ),
#                                 ]
#                             )
#                         case '@<https://gedcom.io/terms/v7/record-FAM>@':
#                             lines = ''.join(
#                                 [
#                                     lines,
#                                     Tests.one_sub_good_test(
#                                         key, '', sub_class_name, 'family'
#                                     ),
#                                 ]
#                             )
#                         case 'https://gedcom.io/terms/v7/type-List#Text':
#                             lines = ''.join(
#                                 [
#                                     lines,
#                                     Tests.one_sub_good_test(
#                                         key, input, sub_class_name
#                                     ),
#                                 ]
#                             )
#                         # case '@<https://gedcom.io/terms/v7/record-SUBM>@':
#                         #     lines = ''.join(
#                         #         [
#                         #             lines,
#                         #             Tests.one_sub_good_test(
#                         #                 key, '', sub_class_name, 'submitter'
#                         #             ),
#                         #         ]
#                         #     )
#                         # case 'http://www.w3.org/2001/XMLSchema#Language':
#                         #     lines = ''.join(
#                         #         [
#                         #             lines,
#                         #             Tests.one_sub_good_test(
#                         #                 key, 'en-US', sub_class_name
#                         #             ),
#                         #         ]
#                         #     )
#                         case 'https://gedcom.io/terms/v7/type-Date#period':
#                             lines = ''.join(
#                                 [
#                                     lines,
#                                     Tests.one_sub_good_test(
#                                         key,
#                                         'FROM 1 DEC 2000 TO 5 DEC 2000',
#                                         sub_class_name,
#                                     ),
#                                 ]
#                             )
#                         # case 'https://gedcom.io/terms/v7/type-List#Enum':
#                         #     enum = enumerationset[value[Default.YAML_ENUM_KEY]][
#                         #         Default.YAML_ENUM_TAGS
#                         #     ][0]
#                         #     lines = ''.join(
#                         #         [
#                         #             lines,
#                         #             Tests.one_sub_good_test(
#                         #                 key, enum, sub_class_name
#                         #             ),
#                         #         ]
#                         #     )
#                         case 'https://gedcom.io/terms/v7/type-Date#exact':
#                             lines = ''.join(
#                                 [
#                                     lines,
#                                     Tests.one_sub_good_test(
#                                         key, '1 JAN 2026', sub_class_name
#                                     ),
#                                 ]
#                             )
#                         case 'https://gedcom.io/terms/v7/type-Date':
#                             lines = ''.join(
#                                 [
#                                     lines,
#                                     Tests.one_sub_good_test(
#                                         key, '1 JAN 2026', sub_class_name
#                                     ),
#                                 ]
#                             )
#                         case 'https://gedcom.io/terms/v7/type-FilePath':
#                             lines = ''.join(
#                                 [
#                                     lines,
#                                     Tests.one_sub_good_test(
#                                         key, 'dir/to/somewhere', sub_class_name
#                                     ),
#                                 ]
#                             )
#                         # case 'http://www.w3.org/ns/dcat#mediaType':
#                         #     lines = ''.join(
#                         #         [
#                         #             lines,
#                         #             Tests.one_sub_good_test(
#                         #                 key, 'mime/text', sub_class_name
#                         #             ),
#                         #         ]
#                         #     )
#                         case 'https://gedcom.io/terms/v7/type-Name':
#                             lines = ''.join(
#                                 [
#                                     lines,
#                                     Tests.one_sub_good_test(
#                                         key, 'John /Doe/', sub_class_name
#                                     ),
#                                 ]
#                             )
#                         case 'https://gedcom.io/terms/v7/type-Age':
#                             lines = ''.join(
#                                 [
#                                     lines,
#                                     Tests.one_sub_good_test(
#                                         key, '> 25y 10m 1d', sub_class_name
#                                     ),
#                                 ]
#                             )
#                         case '@<https://gedcom.io/terms/v7/record-OBJE>@':
#                             lines = ''.join(
#                                 [
#                                     lines,
#                                     Tests.one_sub_good_test(
#                                         key, '', sub_class_name, 'multimedia'
#                                     ),
#                                 ]
#                             )
#                         case '@<https://gedcom.io/terms/v7/record-REPO>@':
#                             lines = ''.join(
#                                 [
#                                     lines,
#                                     Tests.one_sub_good_test(
#                                         key, '', sub_class_name, 'repository'
#                                     ),
#                                 ]
#                             )
#                         # case '@<https://gedcom.io/terms/v7/record-SNOTE>@':
#                         #     lines = ''.join(
#                         #         [
#                         #             lines,
#                         #             Tests.one_sub_good_test(
#                         #                 key, '', sub_class_name, 'shared_note'
#                         #             ),
#                         #         ]
#                         #     )
#                         case '@<https://gedcom.io/terms/v7/record-SOUR>@':
#                             lines = ''.join(
#                                 [
#                                     lines,
#                                     Tests.one_sub_good_test(
#                                         key, '', sub_class_name, 'source'
#                                     ),
#                                 ]
#                             )
#                         # case 'https://gedcom.io/terms/v7/type-Time':
#                         #     lines = ''.join(
#                         #         [
#                         #             lines,
#                         #             Tests.one_sub_good_test(
#                         #                 key, '12:12:12', sub_class_name
#                         #             ),
#                         #         ]
#                         #     )
#         return lines

#     ####################################

    
#     #########################

#     @staticmethod
#     def no_subs_no_value(structures: dict[str, dict[str, Any]]) -> str:
#         lines: str = Default.EMPTY

#         return lines

#     @staticmethod
#     def one_sub(Structure: dict[str, dict[str, Any]]) -> str:
#         lines: str = Default.EMPTY
#         return lines

#     @staticmethod
#     def required(Structure: dict[str, dict[str, Any]]) -> str:
#         lines: str = Default.EMPTY
#         return lines

#     @staticmethod
#     def permitted(Structure: dict[str, dict[str, Any]]) -> str:
#         lines: str = Default.EMPTY
#         return lines

#     @staticmethod
#     def single(Structure: dict[str, dict[str, Any]]) -> str:
#         lines: str = Default.EMPTY
#         return lines

#     @staticmethod
#     def payload(Structure: dict[str, dict[str, Any]]) -> str:
#         lines: str = Default.EMPTY
#         return lines
