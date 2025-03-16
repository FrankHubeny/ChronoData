# structure.py
"""Store, validate and display GEDCOM files."""

__all__ = [
    'ExtensionXref',
    'FamilyXref',
    'IndividualXref',
    'MultimediaXref',
    'RepositoryXref',
    'SharedNoteXref',
    'SourceXref',
    'SubmitterXref',
    'Tagger',
    'Void',
]
# 'Abbr',
# 'Addr',
# 'Adop',
# 'AdopFamc',
# 'Adr1',
# 'Adr2',
# 'Adr3',
# 'Age',
# 'Agnc',
# 'Alia',
# 'Anci',
# 'Anul',
# 'Asso',
# 'Auth',
# 'Bapl',
# 'Bapm',
# 'Barm',
# 'Basm',
# 'Birt',
# 'Bles',
# 'Buri',
# 'Caln',
# 'Cast',
# 'Caus',
# 'Chan',
# 'Chil',
# 'Chr',
# 'Chra',
# 'City',
# 'Conf',
# 'Conl',
# 'Copr',
# 'Corp',
# 'Crea',
# 'Crem',
# 'Crop',
# 'Ctry',
# 'Data',
# 'DataEven',
# 'DataEvenDate',
# 'Date',
# 'DateExact',
# 'Deat',
# 'Desi',
# 'Dest',
# 'Div',
# 'Divf',
# 'Dscr',
# 'Educ',
# 'Email',
# 'Emig',
# 'Endl',
# 'Enga',
# 'Exid',
# 'ExidType',
# 'FamCens',
# 'FamEven',
# 'FamFact',
# 'FamHusb',
# 'FamNchi',
# 'FamResi',
# 'FamWife',
# 'Famc',
# 'FamcAdop',
# 'FamcStat',
# 'Fams',
# 'Fax',
# 'Fcom',
# 'File',
# 'FileTran',
# 'Form',
# 'Gedc',
# 'GedcVers',
# 'Givn',
# 'Grad',
# 'Head',
# 'HeadDate',
# 'HeadLang',
# 'HeadPlac',
# 'HeadPlacForm',
# 'HeadSourData',
# 'Height',
# 'Husb',
# 'Idno',
# 'Immi',
# 'IndiCens',
# 'IndiEven',
# 'IndiFact',
# 'IndiFamc',
# 'IndiName',
# 'IndiNchi',
# 'IndiReli',
# 'IndiTitl',
# 'Inil',
# 'Lang',
# 'Lati',
# 'Left',
# 'Long',
# 'Map',
# 'Marb',
# 'Marc',
# 'Marl',
# 'Marr',
# 'Mars',
# 'Medi',
# 'Mime',
# 'Name',
# 'NameTran',
# 'NameType',
# 'Nati',
# 'Natu',
# 'Nick',
# 'Nmr',
# 'NoDate',
# 'Note',
# 'NoteTran',
# 'Npfx',
# 'Nsfx',
# 'Obje',
# 'Occu',
# 'OrdStat',
# 'Ordn',
# 'Page',
# 'Pedi',
# 'Phon',
# 'Phrase',
# 'Plac',
# 'PlacForm',
# 'PlacTran',
# 'Post',
# 'Prob',
# 'Publ',
# 'Quay',
# 'RecordFam',
# 'RecordIndi',
# 'RecordObje',
# 'RecordRepo',
# 'RecordSnote',
# 'RecordSour',
# 'RecordSubm',
# 'Refn',
# 'Reli',
# 'Repo',
# 'Resn',
# 'Reti',
# 'Role',
# 'Schma',
# 'Sdate',
# 'Sex',
# 'Slgc',
# 'Slgs',
# 'Snote',
# 'Sour',
# 'SourData',
# 'SourEven',
# 'Spfx',
# 'Ssn',
# 'Stae',
# 'Subm',
# 'SubmLang',
# 'Surn',
# 'Tag',
# 'Temp',
# 'Text',
# 'Time',
# 'Titl',
# 'Top',
# 'Trlr',
# 'Type',
# 'Uid',
# 'Vers',
# 'Width',
# 'Wife',
# 'Will',
# 'Www',
# ]

import collections
import contextlib
import io
import math
import re
import urllib.request
from enum import Enum
from pathlib import Path
from textwrap import indent
from typing import Any, Literal, NamedTuple, Self

import yaml  # type: ignore[import-untyped]
from ordered_set import OrderedSet  # type: ignore[import-not-found]

from genedata.constants import (
    Default,
    XrefTag,
)
from genedata.messages import Msg
from genedata.specs7 import (
    Enumeration,
    ExtensionStructure,
    Structure,
)

AnyList = Any | list[Any] | None
FloatNone = float | None
IntNone = int | None
StrList = str | list[str] | None
SubsType = Any | list[Any] | None
YNull = Literal['Y'] | None


class YamlType(Enum):
    STRUCTURE = 'structure'
    ENUMERATION = 'enumeration'
    ENUMERATION_SET = 'enumeration set'
    CALENDAR = 'calendar'
    MONTH = 'month'
    DATA_TYPE = 'data type'
    URI = 'uri'


class TagTuple(NamedTuple):
    """Store standard and extension tag information."""

    value: str = Default.EMPTY
    kind: str = Default.KIND_STANDARD
    supers: list[str] | None = None
    subs: list[str] | None = None
    required: list[str] | None = None
    single: list[str] | None = None
    enumsets: list[str] | None = None
    enums: list[str] | None = None
    lang: str = Default.EMPTY
    type: str = Default.EMPTY
    uri: str = Default.EMPTY
    fragment: str = Default.EMPTY
    standard_tag: str = Default.EMPTY
    extension_tags: list[str] | None = None
    specification: str = Default.EMPTY
    label: str | None = None
    help_text: str | None = None
    documentation: list[str] | None = None
    payload: str = Default.EMPTY
    substructures: dict[str, str] | None = None
    superstructures: dict[str, str] | None = None
    enumeration_values: list[str] | None = None
    value_of: dict[str, str] = {}  # noqa: RUF012
    calendars: list[str] | None = None
    months: list[str] | None = None
    epochs: list[str] | None = None
    contact: str = Default.EMPTY
    change_controller: str = Default.EMPTY
    yamldict: dict[str, Any] | None = None

    def show(self) -> str:
        return f"    {self.value} = TagTuple(value='{self.value.upper()}', standard_tag='{self.standard_tag}', supers={self.supers}, subs={self.subs}, required={self.required}, single={self.single}, enumsets={self.enumsets}, enums={self.enums})"

    def code(self) -> str:
        return f"""
TagTuple(
  value = {self.value},
  kind = {self.kind},
  supers = {self.supers},
  subs = {self.subs},
  required = {self.required},
  single = {self.single},
  enumsets = {self.enumsets},
  enums = {self.enums},
  lang = '{self.lang}',
  type = '{self.type}',
  uri = '{self.uri}',
  fragment = '{self.fragment}',
  standard_tag = '{self.standard_tag}',
  extension_tags = {self.extension_tags},
  specification = '{self.specification}',
  label = {self.label},
  help_text = {self.help_text},
  documentation = {self.documentation},
  payload = '{self.payload}',
  substructures = {self.substructures},
  superstructures = {self.superstructures},
  enumeration_values = {self.enumeration_values},
  value_of = {self.value_of},
  calendars = {self.calendars},
  months = {self.months},
  epochs = {self.epochs},
  contact = '{self.contact}',
  change_controller = '{self.change_controller}',
  yamldict = {self.yamldict},
)
"""


class TagYaml:
    """File read and store standard and extension tag specifications.

    The [YAML description format](https://gedcom.io/terms/format) documents a tag.
    An extension tag cannot be used without a yaml file read by the `get`
    static method of this class.

    The standard tags are also obtained by `get` using `generate`.

    Exceptions:
        ValueError NOT_YAML_FILE is raised if the file does not contain '%YAML 1.2'.


    See Also:
        `ExtTag`
        `Extension`
        `StdTag`
        `TagTuple`

    Reference:
        [GEDCOM YAML description format](https://gedcom.io/terms/format)
    """

    @staticmethod
    def read(url: str = Default.EMPTY) -> dict[str, Any]:
        # Read the internet file or a local file.
        if url[0:4] == 'http':
            webUrl = urllib.request.urlopen(url)
            result_code = str(webUrl.getcode())
            if result_code == '404':
                raise ValueError(Msg.PAGE_NOT_FOUND.format(url))
            raw: str = webUrl.read().decode(Default.UTF8)
        else:
            with Path.open(Path(url)) as file:
                raw = file.read()
        # raw = raw.replace('"','')  # To avoid yaml.scanner.ScannerError

        # Check that file has proper yaml directive.
        if Default.YAML_DIRECTIVE not in raw:
            raise ValueError(
                Msg.YAML_NOT_YAML_FILE.format(url, Default.YAML_DIRECTIVE)
            )

        # Put the yaml data into a dictionary.
        raw2: str = raw[raw.find(Default.YAML_DIRECTIVE_END_MARKER) :]
        yaml_data: str = raw2[: raw2.find(Default.YAML_DOCUMENT_END_MARKER)]
        yaml_dict: dict[str, Any] = yaml.safe_load(yaml_data)
        return yaml_dict

    @staticmethod
    def get(
        tag: str = Default.EMPTY,
        url: str = Default.EMPTY,
        alt_name: str = Default.EMPTY,
    ) -> TagTuple:
        """Read a yaml specification file and store the data in a dictionary."""

        yamldict = TagYaml.read(url)

        # Read the internet file or a local file.
        # if url[0:4] == 'http':
        #     webUrl = urllib.request.urlopen(url)
        #     result_code = str(webUrl.getcode())
        #     if result_code == '404':
        #         raise ValueError(Msg.PAGE_NOT_FOUND.format(url))
        #     raw: str = webUrl.read().decode(Default.UTF8)
        # else:
        #     with Path.open(Path(url)) as file:
        #         raw = file.read()
        # # raw = raw.replace('"','')  # To avoid yaml.scanner.ScannerError

        # # Check that file has proper yaml directive.
        # if Default.YAML_DIRECTIVE not in raw:
        #     raise ValueError(
        #         Msg.YAML_NOT_YAML_FILE.format(url, Default.YAML_DIRECTIVE)
        #     )

        # # Put the yaml data into a dictionary.
        # raw2: str = raw[raw.find(Default.YAML_DIRECTIVE_END_MARKER) :]
        # yaml_data: str = raw2[: raw2.find(Default.YAML_DOCUMENT_END_MARKER)]
        # yamldict: dict[str, Any] = yaml.safe_load(yaml_data)

        # Store and check the required `lang` value.
        lang: str = Default.EMPTY
        with contextlib.suppress(Exception):
            lang = yamldict[Default.YAML_LANG]
        if lang == Default.EMPTY or lang is None:
            raise ValueError(Msg.YAML_MISSING_REQUIRED_LANG.format(url))

        # Store and check the required `type` value.
        spectype: YamlType | None = None
        with contextlib.suppress(Exception):
            spectype = yamldict[Default.YAML_TYPE]
        if spectype is None:
            raise ValueError(Msg.YAML_MISSING_REQUIRED_TYPE.format(url))
        if spectype not in YamlType:
            raise ValueError(Msg.YAML_UNRECOGNIZED_TYPE.format(spectype))

        # Store and check the required uri and fragment values.
        uri: str = Default.EMPTY
        with contextlib.suppress(Exception):
            uri = yamldict[Default.YAML_URI]
        if uri == Default.EMPTY or uri is None:
            raise ValueError(Msg.YAML_MISSING_REQUIRED_URI.format(url))
        fragment: str = Default.EMPTY
        with contextlib.suppress(Exception):
            fragment = yamldict[Default.YAML_FRAGMENT]

        # Store and check the standard or extension tags.
        standard_tag: str = Default.EMPTY
        with contextlib.suppress(Exception):
            standard_tag = yamldict[Default.YAML_STANDARD_TAG]
        extension_tags: list[str] | None = None
        with contextlib.suppress(Exception):
            extension_tags = yamldict[Default.YAML_EXTENSION_TAGS]
        if (
            standard_tag == Default.EMPTY
            and spectype == YamlType.STRUCTURE
            and (extension_tags is None or len(extension_tags) == 0)
        ):
            raise ValueError(Msg.YAML_NO_TAG_NAME)

        # Store the documentation sections.
        documentation: list[str] | None = None
        with contextlib.suppress(Exception):
            documentation = yamldict[Default.YAML_DOCUMENTATION]
        help_text: str = Default.EMPTY
        with contextlib.suppress(Exception):
            help_text = yamldict[Default.YAML_HELP_TEXT]
        label: str = Default.EMPTY
        with contextlib.suppress(Exception):
            label = yamldict[Default.YAML_LABEL]
        specification: str = Default.EMPTY
        with contextlib.suppress(Exception):
            specification = yamldict[Default.YAML_SPECIFICATION]

        # Store the payload definition.
        payload: str = Default.EMPTY
        with contextlib.suppress(Exception):
            payload = yamldict[Default.YAML_PAYLOAD]

        # Store the substructures identifying the required structures
        # those which may appear only once.
        substructures: dict[str, str] = {}
        subs: list[str] = []
        required: list[str] = []
        single: list[str] = []
        with contextlib.suppress(Exception):
            substructures = yamldict[Default.YAML_SUBSTRUCTURES]
        if substructures != {} and substructures is not None:
            for key, dictvalue in substructures.items():
                name = (
                    key[key.rfind(Default.SLASH) + 1 :].title().replace('-', '')
                )
                subs.append(name)
                if dictvalue[0:3] == Default.CARDINALITY_REQUIRED:
                    required.append(name)
                if dictvalue[2:5] == Default.CARDINALITY_SINGULAR:
                    single.append(name)

        # Store the superstructures.
        superstructures: dict[str, str] = {}
        supers: list[str] = []
        with contextlib.suppress(Exception):
            superstructures = yamldict[Default.YAML_SUPERSTRUCTURES]
        if superstructures != {} and superstructures is not None:
            supers = [
                super_name[super_name.rfind(Default.SLASH) + 1 :]
                .title()
                .replace('-', '')
                for super_name in superstructures
            ]

        # Check that a structure type contains both superstructures and substructures.
        if (
            spectype is YamlType.STRUCTURE
            and superstructures == {}
            and substructures == {}
        ):
            raise ValueError(Msg.YAML_STRUCTURE_MISSING_VALUES)

        # Store the enumeration definitions.
        value_of: dict[str, str] = {}
        with contextlib.suppress(Exception):
            value_of = yamldict[Default.YAML_VALUE_OF]
        enumsets: list[str] = [
            enum_name[enum_name.rfind('-') + 1 :] for enum_name in value_of
        ]
        enumeration_values: list[str] = []
        with contextlib.suppress(Exception):
            enumeration_values = yamldict[Default.YAML_ENUMERATION_VALUES]
        enums: list[str] = [
            enum_name[enum_name.rfind('/') + 1 :]
            for enum_name in enumeration_values
        ]

        # Store the calendar definitions.
        calendars: list[str] | None = None
        with contextlib.suppress(Exception):
            calendars = yamldict[Default.YAML_CALENDARS]
        months: list[str] | None = None
        with contextlib.suppress(Exception):
            months = yamldict[Default.YAML_MONTHS]
        epochs: list[str] | None = None
        with contextlib.suppress(Exception):
            epochs = yamldict[Default.YAML_EPOCHS]
        # if spectype != YamlType.CALENDAR and (months is not None or epochs is not None):
        #     raise ValueError(Msg.YAML_NO_CALENDAR)

        # Store contact information.
        contact: str = Default.EMPTY
        with contextlib.suppress(Exception):
            contact = yamldict[Default.YAML_CONTACT]
        change_controller: str = Default.EMPTY
        with contextlib.suppress(Exception):
            change_controller = yamldict[Default.YAML_CHANGE_CONTROLLER]

        # Construct the tag name.
        value: str = alt_name.title().replace('-', '')
        if tag != Default.EMPTY:
            if tag[0] != Default.UNDERLINE:
                value = ''.join([Default.UNDERLINE, tag.upper()])
            else:
                value = tag.upper()
        # elif standard_tag != Default.EMPTY:
        #     value = standard_tag
        # elif spectype == YamlType.STRUCTURE:
        #     raise ValueError(Msg.UNKNOWN_TAG.format(url))

        # Identify whether it is a standard or extension definition.
        kind: str = Default.KIND_STANDARD
        if extension_tags is not None:
            kind = Default.KIND_EXTENDED

        # Finished: return the TagTuple.
        return TagTuple(
            value=value,
            kind=kind,
            supers=supers,
            subs=subs,
            required=required,
            single=single,
            enumsets=enumsets,
            enumeration_values=enumeration_values,
            enums=enums,
            lang=lang,
            type=str(spectype),
            uri=uri,
            fragment=fragment,
            standard_tag=standard_tag,
            extension_tags=extension_tags,
            specification=specification,
            label=label,
            help_text=help_text,
            documentation=documentation,
            payload=payload,
            substructures=substructures,
            superstructures=superstructures,
            value_of=value_of,
            calendars=calendars,
            months=months,
            epochs=epochs,
            contact=contact,
            change_controller=change_controller,
            yamldict=yamldict,
        )

    # @staticmethod
    # def generate() -> None:
    #     """This method generates definitions for the `StdTag` class used to check extensions."""
    #     for item in Terms:
    #         print(
    #             TagYaml.get(
    #                 url=f'{Config.TERMS}{item.value}', alt_name=item.value
    #             ).show()
    #         )


class ExtTag:
    """Store, validate and display extension tag information.

    An underline is added to the front of the new tag if one is not there already.
    Also the tag is made upper case.

    This class holds multiple extension tags identified in the header record.  It is not a separate
    GEDCOM structure.

    Examples:


    Args:
        tag: The tag used for the schema information.
        url: A yaml file following the [GEDCOM YAML description format](https://gedcom.io/terms/format)

    See Also:
        `Header`
        `Extension`

    Returns:
        A string representing a GEDCOM line for this tag.

    Reference:
        [GEDCOM YAML description format](https://gedcom.io/terms/format)
        [GENCOM Extensions](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#extensions)

    >  +1 SCHMA                                 {0:1}  [g7:SCHMA](https://gedcom.io/terms/v7/SCHMA)
    >     +2 TAG <Special>                      {0:M}  [g7:TAG](https://gedcom.io/terms/v7/TAG)
    """

    def __init__(self, tag: str, url: str = Default.EMPTY) -> None:
        self.url: str = url
        self.relocated: bool = False
        try:
            # self.stdtag: StdTag = eval(''.join(['StdTag.', tag]))
            self.stdtag: str = Structure[tag][Default.YAML_STANDARD_TAG]
            self.tag: TagTuple
            self.relocated = True
        except AttributeError:
            if url == Default.EMPTY and tag != Default.EMPTY:
                raise ValueError(Msg.UNDOCUMENTED) from None
            self.tag = TagYaml.get(tag, url)
        self.value: str = self.tag.value
        self.supers: list[str] | None = self.tag.supers
        self.subs: list[str] | None = self.tag.subs
        self.enumsets: list[str] | None = self.tag.enumsets
        self.required: list[str] | None = self.tag.required
        self.single: list[str] | None = self.tag.single

    def validate(self) -> bool:
        for char in self.value:
            if not (char.isalnum() or char == Default.UNDERLINE):
                raise ValueError(Msg.SCHEMA_NAME.format(self.value, char))
        check: bool = (
            Checker.verify_type(self.tag, TagTuple, no_list=True)
            and Checker.verify_not_empty(self.tag)
            and Checker.verify_type(self.url, str, no_list=True)
            and Checker.verify_not_empty(self.url)
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = Default.EMPTY
        if self.validate():
            lines = Tagger.string(
                lines, level + 1, 'TAG', self.value, str(self.url)
            )
        return lines

    def show(self) -> dict[str, Any] | None:
        return self.tag.yamldict

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'ExtTag',
                ('    tag = ', self.tag, tabs, full, True),
                ('    url = ', self.url, tabs, full, True),
            ),
            Default.INDENT * tabs,
        )


ExtTagType = ExtTag | list[ExtTag] | None
TagType = XrefTag | ExtTag | None


class Xref:
    """Assign an extension cross-reference type to a string.

    This base class is instantiated through the other cross reference classes.

    Args:
        name: The name of the identifier.
        tag: The tag associated with this identifier.
        value: Any payload associted with this identifier.  Usually empty except for SharedNoteXref.

    See Also:
        `ExtensionXref`
        `FamilyXref`
        `IndividualXref`
        `MultimediaXref`
        `SharedNoteXref`
        `SourceXref`
        `RepositoryXref`
        `SubmitterXref`

    Reference:
        [GEDCOM Extensions](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#extensions)
    """

    def __init__(
        self, name: str, tag: str = Default.EMPTY, text: str = Default.EMPTY
    ):
        self.fullname: str = name.upper()
        self.name: str = name.replace('@', '').replace(Default.UNDERLINE, ' ')
        self.tag: str = tag
        self.code_xref = f'{self.tag.lower()}_{self.name.lower()}_xref'
        self.text: str = text

    def __str__(self) -> str:
        """Return the name used by the GEDCOM standard."""
        return self.fullname

    def __repr__(self) -> str:
        return f"Xref('{self.fullname}')"

    # def ged(self, info: str = Default.EMPTY) -> str:
    def ged(self) -> str:
        """Return the identifier formatted according to the GEDCOM standard."""
        lines: str = Default.EMPTY
        xref_name: str = self.fullname
        if self.fullname == Default.VOID_POINTER:
            xref_name = Default.EMPTY
        if self.text == Default.EMPTY:
            lines = Tagger.empty(lines, level=0, tag=self.tag, xref=xref_name)
        return Tagger.string(
            lines, level=0, tag=self.tag, payload=self.text, xref=xref_name
        )

    def code(self, tabs: int = 0) -> str:  # noqa: ARG002
        return repr(self.fullname)


class ExtensionXref(Xref):
    """Assign an extension cross-reference type to a string.

    This class is not instantiated directly, but only through
    the `genedata.build.extension_xref()` method.

    Args:
        name: The name of the identifier.
        tag: The tag associated with this identifier.

    See Also:
        `genedata.build.extension_xref()`

    Reference:
        [GEDCOM Extensions](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#extensions)
    """

    def __init__(self, name: str, exttag: str = XrefTag.EXT):
        super().__init__(name, exttag)

    def __repr__(self) -> str:
        return f"MultimediaXref('{self.fullname}')"


class FamilyXref(Xref):
    """Assign the FamilyXref type to a string.

    This class is not instantiated directly, but only through
    the `genedata.build.family_xref()` method.

    Args:
        name: The name of the identifier.
        tag: The tag associated with this identifier.

    See Also:
        genedata.build.family_xref()
    """

    def __init__(self, name: str, tag: str = XrefTag.FAM):
        super().__init__(name, tag)

    def __repr__(self) -> str:
        return f"FamilyXref('{self.fullname}')"


class IndividualXref(Xref):
    """Assign the IndividualXref type to a string.

    This class is not instantiated directly, but only through
    the `genedata.build.individual_xref()` method.

    Args:
        name: The name of the identifier.
        tag: The tag associated with this identifier.

    See Also:
        `genedata.build.individual_xref()`

    Reference:
        [GEDCOM INDIVIDUAL Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_RECORD)
    """

    def __init__(self, name: str, tag: str = XrefTag.INDI):
        super().__init__(name, tag)

    def __repr__(self) -> str:
        return f"IndividualXref('{self.fullname}')"


class MultimediaXref(Xref):
    """Assign Assign the MultimediaXref type to a string.

    This class is not instantiated directly, but only through
    the `genedata.build.multimedia_xref()` method.

    Args:
        name: The name of the identifier.
        tag: The tag associated with this identifier.

    See Also:
        `genedata.build.multimedia_xref()`

    Reference:
        [GEDCOM MULTIMEDIA Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#MULTIMEDIA_RECORD)
    """

    def __init__(self, name: str, tag: str = XrefTag.OBJE):
        super().__init__(name, tag)

    def __repr__(self) -> str:
        return f"MultimediaXref('{self.fullname}')"


class RepositoryXref(Xref):
    """Assign the RepositoryXref type to a string.

    This class is not instantiated directly, but only through
    the `genedata.build.repository_xref()` method.

    Args:
        name: The name of the identifier.
        tag: The tag associated with this identifier.

    See Also:
        `genedata.build.repository_xref()`

    Reference:
        https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#REPOSITORY_RECORD
    """

    def __init__(self, name: str, tag: str = XrefTag.REPO):
        super().__init__(name, tag)

    def __repr__(self) -> str:
        return f"RepositoryXref('{self.fullname}')"


class SharedNoteXref(Xref):
    """Assign the SharedNoteXref type to a string.

    This class is not instantiated directly, but only through
    the `genedata.build.shared_note_xref()` method.

    Args:
        name: The name of the identifier.
        tag: The tag associated with this identifier.
        value: The text of the shared note.

    See Also:
        `genedata.build.shared_note_xref()`

    Reference:
        - [GEDCOM SHARED_NOTE Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SHARED_NOTE_RECORD)
    """

    def __init__(
        self, name: str, tag: str = XrefTag.SNOTE, text: str = Default.EMPTY
    ):
        super().__init__(name, tag, text=text)

    def __repr__(self) -> str:
        return f"SharedNoteXref('{self.fullname}', text='{self.text}')"


class SourceXref(Xref):
    """Assign the SourceXref type to a string.

    This class is not instantiated directly, but only through
    the `genedata.build.source_xref()` method.

    Args:
        name: The name of the identifier.

    See Also:
        `genedata.build.source_xref()`

    Reference:
        [GEDCOM SOURCE Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SHARED_NOTE_RECORD)
    """

    def __init__(self, name: str, tag: str = XrefTag.SOUR):
        super().__init__(name, tag)

    def __repr__(self) -> str:
        return f"SourceXref('{self.fullname}')"


class SubmitterXref(Xref):
    """Assign the SubmitterXref type to a string.

    This class is not instantiated directly, but only through
    the `genedata.build.submitter_xref()` method.

    Args:
        name: The name of the identifier.

    See Also:
        genedata.build.submitter_xref()

    Reference:
        [GEDCOM SUBMITTER Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SUBMITTER_RECORD)
    """

    def __init__(self, name: str, tag: str = XrefTag.SUBM):
        super().__init__(name, tag)

    def __repr__(self) -> str:
        return f"SubmitterXref('{self.fullname}')"


class Void:
    NAME: str = Default.VOID_POINTER
    FAM: FamilyXref = FamilyXref(NAME)
    INDI: IndividualXref = IndividualXref(NAME)
    OBJE: MultimediaXref = MultimediaXref(NAME)
    REPO: RepositoryXref = RepositoryXref(NAME)
    SNOTE: SharedNoteXref = SharedNoteXref(NAME)
    SOUR: SourceXref = SourceXref(NAME)
    SUBM: SubmitterXref = SubmitterXref(NAME)
    EXTTAG: ExtensionXref = ExtensionXref(NAME)
    XREF: Xref = Xref(NAME)



class Tagger:
    """Global methods to tag GEDCOM information.

    There are five methods.
    - `clean_input` makes sure that user input does not contain banned utf-8 strings.
    - `taginfo` performs the base tagging process calling clean_input on user input.
    - `empty` constructs a tag where there is no user input.
    - `string` constructs a tag on user input or a list of a similar type of user input.
    - `structure` runs the ged method on an already tagged structure or a list of
        similar structures adding them to the final GEDCOM string.
    """

    @staticmethod
    def clean_input(input: str) -> str:
        """Remove banned GEDCOM unicode characters from input strings.

        The control characters U+0000 - U+001F and the delete character U+007F
        are listed in the
        [C0 Controls and Basic Latin](https://www.unicode.org/charts/PDF/U0000.pdf)
        chart.

        The code points U+D800 - U+DFFF are not interpreted.
        They are described in the
        [High Surrogate Area](https://www.unicode.org/charts/PDF/UD800.pdf) and
        [Low Surrogate Area](https://www.unicode.org/charts/PDF/UDC00.pdf)
        standards.

        The code points U+FFFE and U+FFFF are noncharacters as described in the
        [Specials](https://www.unicode.org/charts/PDF/UFFF0.pdf) standard.

        Examples:


        Reference:
            - [GEDCOM Characters](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#characters)
            - [Unicode Specification](https://www.unicode.org/versions/Unicode16.0.0/#Summary)
            - [Python re Module](https://docs.python.org/3/library/re.html)
        """

        return re.sub(Default.BANNED, Default.EMPTY, input)

    @staticmethod
    def taginfo(
        level: int,
        tag: str,
        payload: str = Default.EMPTY,
        extra: str = Default.EMPTY,
        format: bool = True,
        xref: str = Default.EMPTY,
    ) -> str:
        """Return a GEDCOM formatted line for the information and level.

        This is suitable for most tagged lines to guarantee it is uniformly
        formatted.  Although the user need not worry about calling this line,
        it is provided so the user can see the GEDCOM formatted output
        that would result.

        Example:
            The main use of this method generates a GEDCOM line.
            Note how the initial and ending spaces have been stripped from
            the input value.
            >>> from genedata.structure import Tagger
            >>> print(Tagger.taginfo(1, 'NAME', '  Some Name'))
            1 NAME   Some Name
            <BLANKLINE>

            There can also be an extra parameter.
            >>> print(Tagger.taginfo(1, 'NAME', 'SomeName', 'Other info'))
            1 NAME SomeName Other info
            <BLANKLINE>

            This example comes from the [GEDCOM lines standard](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#lines):
            Note how the `@me` was reformatted as `@@me`.
            > 1 NOTE me@example.com is my email
            > 2 CONT @@me and @I are my social media handles
            >>> from genedata.structure import Note
            >>> mynote = Note(
            ...     '''me@example.com is my email
            ... @me and @I are my social media handles'''
            ... )
            >>> print(mynote.ged(1))
            1 NOTE me@example.com is my email
            2 CONT @@me and @I are my social media handles
            <BLANKLINE>

            However, escaping the '@' should not occur when this is part of a cross-reference identifier.


        Reference:
            [GEDCOM Lines](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#lines)

        """
        lineval: str = payload
        if format and lineval != Default.EMPTY and lineval[0] == Default.ATSIGN:
            lineval = ''.join([Default.ATSIGN, lineval])
        if xref == Default.EMPTY:
            if extra == Default.EMPTY:
                if lineval == Default.EMPTY:
                    return f'{level} {tag}{Default.EOL}'
                return (
                    f'{level} {tag} {Tagger.clean_input(lineval)}{Default.EOL}'
                )
            return f'{level} {tag} {Tagger.clean_input(lineval)} {Tagger.clean_input(extra)}{Default.EOL}'
        if extra == Default.EMPTY:
            if lineval == Default.EMPTY:
                return f'{level} {xref} {tag}{Default.EOL}'
            return f'{level} {xref} {tag} {Tagger.clean_input(lineval)}{Default.EOL}'
        return f'{level} {xref} {tag} {Tagger.clean_input(lineval)} {Tagger.clean_input(extra)}{Default.EOL}'

    @staticmethod
    def empty(
        lines: str, level: int, tag: str, xref: str = Default.EMPTY
    ) -> str:
        """Join a GEDCOM line that has only a level and a tag to a string.

        This method implements the
        [GEDCOM empty LineVal standard](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#lines) which reads:
        > Note that production LineVal does not match the empty string.
        > Because empty payloads and missing payloads are considered equivalent,
        > both a structure with no payload and a structure with the empty string
        > as its payload are encoded with no LineVal and no space after the Tag.

        Example:
            >>> from genedata.structure import Tagger
            >>> lines = ''
            >>> lines = Tagger.empty(lines, 1, 'MAP')
            >>> print(lines)
            1 MAP
            <BLANKLINE>

        Args:
            lines: The prefix of the returned string.
            level: The GEDCOM level of the structure.
            tag: The tag to apply to this line.
            xref: The cross reference identifier.

        """
        if xref == Default.EMPTY:
            return ''.join([lines, Tagger.taginfo(level, tag)])
        return ''.join([lines, Tagger.taginfo(level, tag, xref=xref)])

    @staticmethod
    def string(
        lines: str,
        level: int,
        tag: str,
        payload: list[str] | str | None,
        extra: str = Default.EMPTY,
        format: bool = True,
        xref: str = Default.EMPTY,
    ) -> str:
        """Join a string or a list of string to GEDCOM lines.

        This method hides the concatenation of the already constructed
        GEDCOM file with the new line and the check that this should only
        be done if the payload is not empty.  It also hides checking
        whether the string is part of a list or not.

        Examples:
            Suppose there is only one string that should be tagged.
            >>> from genedata.structure import Tagger
            >>> lines = ''
            >>> lines = Tagger.empty(lines, 1, 'MAP')
            >>> lines = Tagger.string(lines, 2, 'LATI', 'N30.0')
            >>> lines = Tagger.string(lines, 2, 'LONG', 'W30.0')
            >>> print(lines)
            1 MAP
            2 LATI N30.0
            2 LONG W30.0
            <BLANKLINE>

            Suppose there are a list of strings that should be tagged.
            >>> lines = ''
            >>> wwws = [
            ...     'https://here.com',
            ...     'https://there.com',
            ...     'https://everywhere.com',
            ... ]
            >>> lines = Tagger.string(lines, 3, 'WWW', wwws)
            >>> print(lines)
            3 WWW https://here.com
            3 WWW https://there.com
            3 WWW https://everywhere.com
            <BLANKLINE>

        Args:
            lines: The prefix string that will be appended to.
            level: The GEDCOM level of the structure.
            tag: The tag to apply to this line.
            records: The list of strings to tag.
            format: If true and '@' begins the line then escape it with another '@' otherwise not.
            xref: The cross reference identifier.
        """

        if payload is None:
            return lines
        if isinstance(payload, list):
            for item in payload:
                if Default.EOL in item:
                    items: list[str] = item.split(Default.EOL)
                    lines = Tagger.string(
                        lines, level, tag, items[0], format=format, xref=xref
                    )
                    lines = Tagger.string(
                        lines,
                        level + 1,
                        Default.CONT,
                        items[1:],
                        format=format,
                    )
                else:
                    lines = ''.join(
                        [
                            lines,
                            Tagger.taginfo(
                                level, tag, item, format=format, xref=xref
                            ),
                        ]
                    )
            return lines
        if payload != Default.EMPTY and payload is not None:
            if Default.EOL in payload:
                payloads: list[str] = payload.split(Default.EOL)
                lines = Tagger.string(
                    lines, level, tag, payloads[0], format=format, xref=xref
                )
                lines = Tagger.string(
                    lines,
                    level + 1,
                    Default.CONT,
                    payloads[1:],
                    format=format,
                )
            else:
                return ''.join(
                    [
                        lines,
                        Tagger.taginfo(
                            level, tag, payload, extra, format=format, xref=xref
                        ),
                    ]
                )
        return lines

    @staticmethod
    def structure(
        lines: str,
        level: int,
        payload: list[Any] | Any,
        flag: str = Default.EMPTY,
    ) -> str:
        """Join a structure or a list of structure to GEDCOM lines.

        This method hides the concatenation of the already constructed
        GEDCOM file with the new line.  It also hides checking
        whether the string is part of a list or not.

        Examples:
            Suppose there is one structure to write to GEDCOM lines.
            >>> from genedata.structure import Lati, Long, Map, Tagger
            >>> map1 = Map([Lati('N30.000000'), Long('W30.000000')])
            >>> map2 = Map([Lati('S40.000000'), Long('E20.000000')])
            >>> lines = ''
            >>> lines = Tagger.structure(lines, 2, map1)
            >>> print(lines)
            2 MAP
            3 LATI N30.000000
            3 LONG W30.000000
            <BLANKLINE>

            Now include both defined maps into a list.
            >>> lines = ''
            >>> lines = Tagger.structure(lines, 4, [map1, map2])
            >>> print(lines)
            4 MAP
            5 LATI N30.000000
            5 LONG W30.000000
            4 MAP
            5 LATI S40.000000
            5 LONG E20.000000
            <BLANKLINE>

        Args:
            lines: The prefix string that will be appended to.
            level: The GEDCOM level of the structure.
            payload: The structure or list of structures from which the lines will be formed.
            flag: An optional item passed to the structure's ged method to modify its behavior.
        """

        if payload is None or payload == Default.EMPTY:
            return lines
        if isinstance(payload, list):
            # unique_payload = OrderedSet(payload)
            for item in payload:  # unique_payload:
                # for item in payload:
                if flag != Default.EMPTY:
                    lines = ''.join([lines, item.ged(level, flag)])
                else:
                    lines = ''.join([lines, item.ged(level)])
            return lines
        # if payload != default:
        if flag != Default.EMPTY:
            lines = ''.join([lines, payload.ged(level, flag)])
        else:
            lines = ''.join([lines, payload.ged(level)])
        return lines

    @staticmethod
    def order(substructure: list[NamedTuple] | None) -> list[NamedTuple]:
        """Order NamedTuples by collecting similar ones together, but in same order as presented."""
        if substructure is None:
            return []
        ordered: list[NamedTuple] = []
        subs_types: list[str] = [type(sub).__name__ for sub in substructure]
        unique_types: list[str] = OrderedSet(subs_types)
        for index in range(len(unique_types)):
            for sub in substructure:
                if unique_types[index] == type(sub).__name__:
                    ordered.append(sub)
        return ordered

    # @staticmethod
    # def base_ged(
    #     level: int,
    #     tag: str,
    #     value: str,
    #     subs: Any | None = None,
    #     extension: Any = None,
    # ) -> str:
    #     lines: str = ''
    #     lines = Tagger.string(lines, level, tag, value)
    #     lines = Tagger.structure(lines, level + 1, Tagger.order(subs))
    #     return Tagger.structure(lines, level + 1, extension)

    # @staticmethod
    # def ged(
    #     level: int,
    #     tag: TagTuple,
    #     value: str,
    #     subs: Any | None,
    #     ext: Any | None,
    #     format: bool = True,
    # ) -> str:
    #     lines: str = Default.EMPTY
    #     if value == Default.EMPTY:
    #         lines = Tagger.empty(lines, level, tag.standard_tag)
    #     else:
    #         lines = Tagger.string(
    #             lines, level, tag.standard_tag, value, format=format
    #         )
    #     lines = Tagger.structure(lines, level + 1, Tagger.order(subs))
    #     return Tagger.structure(lines, level + 1, ext)

    # @staticmethod
    # def extension(
    #     lines: str,
    #     level: int,
    #     tag: str,
    #     payload: str,
    #     extra: str = Default.EMPTY,
    # ) -> str:
    #     ext_line: str = Default.EMPTY
    #     if extra == Default.EMPTY:
    #         if payload == Default.EMPTY:
    #             ext_line = f'{level} {tag}{Default.EOL}'
    #         else:
    #             ext_line = (
    #                 f'{level} {tag} {Tagger.clean_input(payload)}{Default.EOL}'
    #             )
    #     else:
    #         ext_line = f'{level} {tag} {Tagger.clean_input(payload)} {Tagger.clean_input(extra)}{Default.EOL}'
    #     return ''.join([lines, ext_line])


class Checker:
    """Global methods supporting validation of data."""

    # @staticmethod
    # def count_named_tuples(named_tuples: Any | None) -> dict[str, int]:
    #     """Return the count of the number of named tuples by name in the list of named tuples."""
    #     if named_tuples is None:
    #         return {}
    #     if isinstance(named_tuples, list):
    #         named_tuple_counted = [
    #             type(named_tuple).__name__ for named_tuple in named_tuples
    #         ]
    #     else:
    #         named_tuple_counted = [type(named_tuples).__name__]
    #     return collections.Counter(named_tuple_counted)

    # @staticmethod
    # def only_one(names: list[str] | None, counted: dict[str, int]) -> bool:
    #     if names is None:
    #         return True
    #     for name in names:
    #         if name in counted and counted[name] > 1:
    #             raise ValueError(Msg.ONLY_ONE_PERMITTED.format(name))
    #     return True

    # @staticmethod
    # def only_permitted(
    #     permitted: list[str] | None, counted: dict[str, int]
    # ) -> bool:
    #     if permitted is None and len(counted) > 0:
    #         raise ValueError(Msg.NO_SUBS)
    #     if permitted is not None:
    #         for key in counted:
    #             if key not in permitted:
    #                 raise ValueError(Msg.NOT_PERMITTED.format(key, permitted))
    #     return True

    # @staticmethod
    # def required(names: list[str] | None, counted: dict[str, int]) -> bool:
    #     if names is None:
    #         return True
    #     for name in names:
    #         if name not in counted:
    #             raise ValueError(Msg.MISSING_REQUIRED.format(name))
    #     return True

    # @staticmethod
    # def permitted_enum(value: str | int | Xref, enums: list[str]) -> bool:
    #     """Check if the value is in the proper enumeration."""
    #     if len(enums) == 0:
    #         return True
    #     if value not in enums:
    #         raise ValueError(Msg.NOT_VALID_ENUM.format(value, enums))
    #     return True

    # @staticmethod
    # def payload(
    #     value: str | int | Xref | None = None, payload: str | None = None
    # ) -> bool:
    #     """Check that the data types of the payloads are as expected.

    #     Enumerations are handled separately by `Checker.permitted_enum`.

    #     Empty, or None, payloads do not have a value input argument.  So there is
    #     nothing to check.

    #     Reference:
    #     - [GEDCOM Data Types](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#datatypes)
    #     """
    #     if payload is None or payload in [
    #         'https://gedcom.io/terms/v7/type-Enum',
    #         'https://gedcom.io/terms/v7/type-List#Enum',
    #     ]:
    #         return True
    #     match payload:
    #         case 'Y|<NULL>':
    #             if not isinstance(value, str) or str(value) not in ['Y', '']:
    #                 raise ValueError(Msg.VALUE_NOT_Y_OR_NULL.format(str(value)))
    #             return True
    #         case 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger':
    #             if not isinstance(value, int) or int(value) < 0:
    #                 raise ValueError(Msg.NEGATIVE_ERROR.format(str(value)))
    #             return True
    #         case '@<https://gedcom.io/terms/v7/record-INDI>@':
    #             if not isinstance(value, IndividualXref):
    #                 raise ValueError(Msg.NOT_INDIVIDUAL_XREF.format(str(value)))
    #         case '@<https://gedcom.io/terms/v7/record-FAM>@':
    #             if not isinstance(value, FamilyXref):
    #                 raise ValueError(Msg.NOT_FAMILY_XREF.format(str(value)))
    #         case 'https://gedcom.io/terms/v7/type-List#Text':
    #             if not isinstance(value, str) or not re.match(',', str(value)):
    #                 raise ValueError(Msg.NOT_LIST.format(str(value)))
    #         case '@<https://gedcom.io/terms/v7/record-SUBM>@':
    #             if not isinstance(value, SubmitterXref):
    #                 raise ValueError(Msg.NOT_SUBMITTER_XREF.format(str(value)))
    #         case 'http://www.w3.org/2001/XMLSchema#Language':
    #             if not isinstance(value, str) or not re.match('', str(value)):
    #                 raise ValueError(Msg.NOT_LANGUAGE.format(str(value)))
    #         case 'https://gedcom.io/terms/v7/type-Date#period':
    #             if not isinstance(value, str) or not re.match('', str(value)):
    #                 raise ValueError(Msg.NOT_DATE_PERIOD.format(str(value)))
    #         case 'https://gedcom.io/terms/v7/type-Date#exact':
    #             if not isinstance(value, str) or not re.match('', str(value)):
    #                 raise ValueError(Msg.NOT_DATE_EXACT.format(str(value)))
    #         case 'https://gedcom.io/terms/v7/type-Date':
    #             if not isinstance(value, str) or not re.match('', str(value)):
    #                 raise ValueError(Msg.NOT_DATE.format(str(value)))
    #         case 'https://gedcom.io/terms/v7/type-FilePath':
    #             if not isinstance(value, str) or not re.match('', str(value)):
    #                 raise ValueError(Msg.NOT_FILE_PATH.format(str(value)))
    #         case 'https://gedcom.io/terms/v7/type-Name':
    #             if not isinstance(value, str) or not re.match('', (str(value))):
    #                 raise ValueError(Msg.NOT_NAME.format(str(value)))
    #         case 'https://gedcom.io/terms/v7/type-Age':
    #             if not re.match('', str(value)):
    #                 raise ValueError(Msg.NOT_AGE.format(str(value)))
    #         case 'http://www.w3.org/ns/dcat#mediaType':
    #             if not isinstance(value, str) or not re.match('', str(value)):
    #                 raise ValueError(Msg.NOT_MEDIA_TYPE.format(str(value)))
    #         case '@<https://gedcom.io/terms/v7/record-OBJE>@':
    #             if not isinstance(value, MultimediaXref):
    #                 raise ValueError(Msg.NOT_MULTIMEDIA_XREF.format(str(value)))
    #         case '@<https://gedcom.io/terms/v7/record-REPO>@':
    #             if not isinstance(value, RepositoryXref):
    #                 raise ValueError(Msg.NOT_REPOSITORY_XREF.format(str(value)))
    #         case '@<https://gedcom.io/terms/v7/record-SNOTE>@':
    #             if not isinstance(value, SharedNoteXref):
    #                 raise ValueError(
    #                     Msg.NOT_SHARED_NOTE_XREF.format(str(value))
    #                 )
    #         case '@<https://gedcom.io/terms/v7/record-SOUR>@':
    #             if not isinstance(value, SourceXref):
    #                 raise ValueError(Msg.NOT_SOURCE_XREF.format(str(value)))
    #         case 'https://gedcom.io/terms/v7/type-Time':
    #             if not isinstance(value, str) or not re.match('', str(value)):
    #                 raise ValueError(Msg.NOT_TIME.format(str(value)))
    #         case _:
    #             return True
    #     return True

    # @staticmethod
    # def verify(when: bool, then: bool, message: str) -> bool:
    #     """Use conditional logic to test whether to raise a ValueError exception.

    #     The only time this fails is when the `when` is True,
    #     but the `then` is False.  In that case a ValueError is raised
    #     with the value in `message`.  In all other cases, True is returned.

    #     This helps verify that more complicated GEDCOM criteria are met.

    #     Examples:
    #         >>> from genedata.structure import Checker
    #         >>> message = 'Error!'
    #         >>> Checker.verify(True, 1 == 2, message)
    #         Traceback (most recent call last):
    #         ValueError: Error!

    #         >>> Checker.verify(True, 1 == 1, message)
    #         True

    #         When `when` is False, then True is returned no matter what the
    #         value of `then` happens to be.
    #         >>> Checker.verify(False, False, message)
    #         True

    #         >>> Checker.verify(False, True, message)
    #         True

    #     Args:
    #         when: If this is True then check the `then` condition, otherwise return True.
    #         then: If `when` is True and this is not, raise the ValueError.
    #         message: This is the message used by the ValueError.
    #     """
    #     if when and not then:
    #         raise ValueError(message)
    #     return True

    @staticmethod
    def verify_type(value: Any, value_type: Any, no_list: bool = False) -> bool:
        """Check if the value has the specified type."""
        check: bool = True
        if value is None:
            return check
        if isinstance(value, list):
            if no_list and isinstance(value, list):
                raise TypeError(Msg.NO_LIST)
            for item in value:
                if not isinstance(item, value_type):
                    raise TypeError(
                        Msg.WRONG_TYPE.format(item, type(item), value_type)
                    )
            return check
        if not isinstance(value, value_type):
            raise TypeError(
                Msg.WRONG_TYPE.format(value, type(value), value_type)
            )
        return check

    @staticmethod
    def verify_tuple_type(name: Any, value_type: Any) -> bool:
        """Check if each member of the tuple has the specified type."""
        if name != [] and name is not None:
            for value in name:
                Checker.verify_type(value, value_type)
        return True

    @staticmethod
    def verify_not_empty(value: Any) -> bool:
        if value is None:
            raise ValueError(Msg.NO_NONE)
        if isinstance(value, str) and value == Default.EMPTY:
            raise ValueError(Msg.NO_EMPTY_STRING)
        if isinstance(value, list) and len(value) == 0:
            raise ValueError(Msg.NO_EMPTY_LIST)
        if isinstance(value, Xref) and value.fullname == Default.VOID_POINTER:
            raise ValueError(Msg.NO_EMPTY_POINTER)
        return True

    # @staticmethod
    # def verify_not_all_none(*values: Any) -> bool:
    #     check: bool = False
    #     for item in values:
    #         if item is not None:
    #             check = True
    #     return check

    # @staticmethod
    # def verify_range(
    #     value: int | float, low: int | float, high: int | float
    # ) -> bool:
    #     """Check if the value is inclusively between low and high boundaries."""
    #     if not low <= value <= high:
    #         raise ValueError(Msg.RANGE_ERROR.format(value, low, high))
    #     return True

    # @staticmethod
    # def verify_not_negative(value: int | float | None) -> bool:
    #     """Check if the value is a positive number."""
    #     if value is not None and value < 0:
    #         raise ValueError(Msg.NEGATIVE_ERROR.format(value))
    #     return True


# class Dater:
#     """Global methods supporting date processing."""

#     @staticmethod
#     def format(
#         year: int,
#         month: int = 0,
#         day: int = 0,
#         calendar: CalendarDefinition = CalendarsGregorian.GREGORIAN,
#     ) -> str:
#         formatted: str = str(year)
#         if year < 0:
#             formatted = ''.join(
#                 [str(-year), Default.SPACE, calendar.epoch_name]
#             )
#         if month > 0:
#             formatted = ''.join(
#                 [calendar.months[month].abbreviation, Default.SPACE, formatted]
#             )
#         if day > 0:
#             formatted = ''.join([str(day), Default.SPACE, formatted])
#         return formatted

#     @staticmethod
#     def ged_date(
#         iso_date: str = String.NOW,
#         calendar: CalendarName = CalendarName.GREGORIAN,
#         epoch: bool = True,
#     ) -> tuple[str, str]:
#         """Obtain the GEDCOM date and time from an ISO 8601 date and time for the
#         current UTC timestamp in GEDCOM format.

#         Examples:
#             The ISO date for January 1, 2000 at 1:15:30 AM would be `20000101 01:15:30`.
#             >>> from genedata.store import Dater
#             >>> print(Dater.ged_date(iso_date='2000-01-01T01:15:30'))
#             ('01 JAN 2000', '01:15:30Z')

#             Viewing this same date in BC context we would have:
#             >>> print(Dater.ged_date(iso_date='-2000-01-01T01:15:30'))
#             ('01 JAN 2000 BCE', '01:15:30Z')

#             There is no zero year in the Gregorian Calendar and neither
#             does the ISO 8601 standard have a zero year.
#             >>> print(Dater.ged_date(iso_date='0-01-01T01:15:30'))
#             Traceback (most recent call last):
#             ValueError: The calendar has no zero year.

#         Args:
#             iso_date: The ISO date or `now` for the current date and time.
#             calendar: The GEDCOM calendar to use when returning the date.
#             epoch: Return the epoch, `BCE`, for the GEDCOM date if it is before
#                 the current epoch.  Set this to `False` to not return the epoch.
#                 This only applies to dates prior to 1 AD starting at 1 BC.

#         References:
#             [Wikipedia ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)

#         Exceptions:

#         """
#         datetime: str = str(np.datetime64(iso_date))
#         date, time = datetime.split(Default.T)
#         date_pieces = date.split(Default.HYPHEN)
#         if len(date_pieces) == 3:
#             year: str = date_pieces[0]
#             month: str = date_pieces[1]
#             day: str = date_pieces[2]
#         else:
#             year = date_pieces[1]
#             month = date_pieces[2]
#             day = date_pieces[3]
#         if int(year) == 0:
#             raise ValueError(Msg.ZERO_YEAR)
#         ged_time: str = ''.join([time, Default.Z])
#         good_calendar: str | bool = Cal.CALENDARS.get(calendar, False)
#         if not good_calendar:
#             raise ValueError(Msg.BAD_CALENDAR.format(calendar))
#         month_code: str = Cal.CALENDARS[calendar][String.MONTH_NAMES].get(
#             month, False
#         )
#         if not month_code:
#             raise ValueError(Msg.BAD_MONTH.format(calendar, month))
#         ged_date: str = ''
#         if epoch and len(date_pieces) == 4:
#             ged_date = ''.join(
#                 [
#                     day,
#                     Default.SPACE,
#                     month_code,
#                     Default.SPACE,
#                     year,
#                     Default.SPACE,
#                     String.BC,
#                 ]
#             )
#         else:
#             ged_date = ''.join(
#                 [day, Default.SPACE, month_code, Default.SPACE, year]
#             )
#         return ged_date, ged_time

#     @staticmethod
#     def iso_date(
#         ged_date: str,
#         ged_time: str = Default.EMPTY,
#         calendar: str = String.GREGORIAN,
#     ) -> str:
#         """Return an ISO date and time given a GEDCOM date and time."""
#         day: str
#         month: str
#         year: str
#         day, month, year = ged_date.split(Default.SPACE)
#         time: str = ged_time.split(Default.Z)[0]
#         good_calendar: str | bool = Cal.CALENDARS[calendar].get(
#             String.GREGORIAN, False
#         )
#         if not good_calendar:
#             logging.critical(Msg.BAD_CALENDAR.format(calendar))
#             raise ValueError(Msg.BAD_CALENDAR.format(calendar))
#         month_code: str = Cal.CALENDARS[calendar].get(month, False)
#         if not month_code:
#             logging.critical(Msg.BAD_MONTH.format(calendar, month))
#             raise ValueError(Msg.BAD_MONTH.format(calendar, month))
#         iso_datetime: str = ''.join(
#             [
#                 year,
#                 Default.HYPHEN,
#                 month_code,
#                 Default.HYPHEN,
#                 day,
#                 Default.T,
#                 time,
#             ]
#         )
#         return iso_datetime

#     # @staticmethod
#     # def now(level: int = 2) -> str:
#     #     """Return the current UTC date and time rather than an entered value.

#     #     This will be returned as a list of two lines for a GEDCOM file.
#     #     This method will not likely be needed by the builder of a genealogy
#     #     unless the builder wants to enter the current date and time into
#     #     the genealogy. The current date and time is automatically
#     #     entered for each record as its creation date and time
#     #     as well as its change date and time.

#     #     Return
#     #     ------
#     #     A list containing two strings is returned. The first member of
#     #     the list is the date formatted to be used in a GEDCOM file.
#     #     The second member of the list is the time formatted to
#     #     be used in a GEDCOM file.

#     #     Example
#     #     -------
#     #     >>> from genedata.store import Dater  # doctest: +ELLIPSIS
#     #     >>> print(Dater.now())
#     #     2 DATE ...
#     #     3 TIME ...
#     #     <BLANKLINE>

#     #     Changing the level adjusts the level numbers for the two returned strings.

#     #     >>> print(Dater.now(level=5))
#     #     5 DATE ...
#     #     6 TIME ...
#     #     <BLANKLINE>

#     #     See Also
#     #     --------
#     #     - `creation_date`
#     #     - `change_date`
#     #     - `header`
#     #     """
#     #     date: str
#     #     time: str
#     #     date, time = Dater.ged_date()
#     #     return ''.join(
#     #         [
#     #             Tagger.taginfo(level, Tag.DATE.value, date),
#     #             Tagger.taginfo(level + 1, Tag.TIME.value, time),
#     #         ]
#     #     )

#     # @staticmethod
#     # def creation_date() -> str:
#     #     """Return three GEDCOM lines showing a line with a creation tag (CREA)
#     #     and then two automatically generated
#     #     UTC date and time lines.  These are used to
#     #     show when a record has been created.

#     #     See Also
#     #     --------
#     #     - `now`: the method that generates the current UTC date and time
#     #     - `family`: the method creating the family record (FAM)
#     #     - `individual`: the method creating the individual record (INDI)
#     #     - `multimedia`: the method creating the multimedia record (OBJE)
#     #     - `repository`: the method creating the repository record (REPO)
#     #     - `shared_note`: the method creating the shared note record (SNOTE)
#     #     - `source`: the method creating the source record (SOUR)
#     #     - `submitter`: the method creating the submitter record (SUBM)
#     #     """
#     #     return ''.join([Tagger.taginfo(1, Tag.CREA.value), Dater.now()])


class Placer:
    """Global methods to support place data."""

    @staticmethod
    def to_decimal(
        degrees: int, minutes: int, seconds: float, precision: int = 6
    ) -> float:
        """Convert degrees, minutes and seconds to a decimal.

        Example:
            The specification for the LATI and LONG structures (tags) offer the
            following example.
            >>> from genedata.structure import Placer
            >>> Placer.to_decimal(168, 9, 3.4, 6)
            168.150944

        Args:
            degrees: The degrees in the angle whether latitude or longitude.
            minutes: The minutes in the angle.
            seconds: The seconds in the angle.
            precision: The number of digits to the right of the decimal point.

        See Also:
            - `to_dms`: Convert a decimal to degrees, minutes, seconds to a precision.

        Reference:
            [GEDCOM LONG structure](https://gedcom.io/terms/v7/LONG)
            [GEDCOM LATI structure](https://gedcom.io/terms/v7/LATI)

        """
        sign: int = -1 if degrees < 0 else 1
        degrees = abs(degrees)
        minutes_per_degree = 60
        seconds_per_degree = 3600
        return round(
            sign * degrees
            + (minutes / minutes_per_degree)
            + (seconds / seconds_per_degree),
            precision,
        )

    @staticmethod
    def to_dms(position: float, precision: int = 6) -> tuple[int, int, float]:
        """Convert a measurment in decimals to one showing degrees, minutes
        and sconds.

        >>> from genedata.structure import Placer
        >>> Placer.to_dms(49.29722222222, 10)
        (49, 17, 49.999999992)

        See Also:
            - `to_decimal`: Convert degrees, minutes, seconds with precision to a decimal.

        """
        minutes_per_degree = 60
        seconds_per_degree = 3600
        degrees: int = math.floor(position)
        minutes: int = math.floor((position - degrees) * minutes_per_degree)
        seconds: float = round(
            (position - degrees - (minutes / minutes_per_degree))
            * seconds_per_degree,
            precision,
        )
        return (degrees, minutes, seconds)

    @staticmethod
    def form(form1: str, form2: str, form3: str, form4: str) -> str:
        return ''.join(
            [
                form1,
                Default.LIST_ITEM_SEPARATOR,
                form2,
                Default.LIST_ITEM_SEPARATOR,
                form3,
                Default.LIST_ITEM_SEPARATOR,
                form4,
            ]
        )

    @staticmethod
    def place(place1: str, place2: str, place3: str, place4: str) -> str:
        return ''.join(
            [
                place1,
                Default.LIST_ITEM_SEPARATOR,
                place2,
                Default.LIST_ITEM_SEPARATOR,
                place3,
                Default.LIST_ITEM_SEPARATOR,
                place4,
            ]
        )


class Formatter:
    """Methods to support formatting strings to meet the GEDCOM standard."""

    @staticmethod
    def phone(country: int, area: int, prefix: int, line: int) -> str:
        """Format a phone string to meet the GEDCOM standard.

        The International Notation from the ITU-T E.123 standard
        are followed.  Spaces are used between the country, area_code, prefix and line numbers.
        A `+` precedes the country code.

        The GEDCOM standard does not require this international notation, but recommends it.
        This method formats for the optional international notation should the user
        choose to have a method format the number in a uniform manner.

        If the number cannot be formatted correctly with this method any string is accepted
        as a phone number.

        One may use this for fax numbers as well.

        Examples:
            The first example shows the use of the default, US, international number.
            >>> from genedata.structure import Formatter
            >>> Formatter.phone(1, 123, 456, 7890)
            '+1 123 456 7890'

            The second example provides a non-US country number.
            >>> Formatter.phone(44, 123, 456, 7890)
            '+44 123 456 7890'

        Args:
            country: The country code greater than 0 and and less than 1000.
            area: The area code for the phone number greater than 0 and less than 1000.
            prefix: The prefix portion of the phone number greater than 0 and less than 1000.
            line: The line portion of the phone number greater than 0 and less than 10000.

        Reference:
            [GEDCOM Standard](https://gedcom.io/terms/v7/PHON)
            [ITU-T E.123 Standard](https://www.itu.int/rec/T-REC-E.123-200102-I/en)
        """
        if not Default.PHONE_COUNTRY_MIN < country < Default.PHONE_COUNTRY_MAX:
            raise ValueError(
                Msg.PHONE_COUNTRY_CODE.format(
                    country,
                    Default.PHONE_COUNTRY_MIN,
                    Default.PHONE_COUNTRY_MAX,
                )
            )
        if not Default.PHONE_AREA_MIN < area < Default.PHONE_AREA_MAX:
            raise ValueError(
                Msg.PHONE_AREA_CODE.format(
                    area, Default.PHONE_AREA_MIN, Default.PHONE_AREA_MAX
                )
            )
        if not Default.PHONE_PREFIX_MIN < prefix < Default.PHONE_PREFIX_MAX:
            raise ValueError(
                Msg.PHONE_PREFIX_CODE.format(
                    prefix, Default.PHONE_PREFIX_MIN, Default.PHONE_PREFIX_MAX
                )
            )
        if not Default.PHONE_LINE_MIN < line < Default.PHONE_LINE_MAX:
            raise ValueError(
                Msg.PHONE_LINE_CODE.format(
                    line, Default.PHONE_LINE_MIN, Default.PHONE_LINE_MAX
                )
            )
        return f'+{country!s} {area!s} {prefix!s} {line!s}'

    @staticmethod
    def codes_single(item: Any, tabs: int, full: bool) -> str:
        if isinstance(item, str):
            return f'{item!r}'
        if isinstance(item, int | float):
            return f'{item!r}'
        if isinstance(item, Xref):
            return f'{item!r}'
        # if isinstance(item, Tag):
        #     return f'Tag.{item.name}'
        # if isinstance(item, AdopEnum):
        #     return f'Adop.{item.name}'
        # if isinstance(item, EvenEnum):
        #     return f'Even.{item.name}'
        # # elif isinstance(self.tag, EvenAttr):
        # #     enum_name = Tag.EVEN
        # if isinstance(item, MediumEnum):
        #     return f'Medi.{item.name}'
        # if isinstance(item, PediEnum):
        #     return f'Pedi.{item.name}'
        # if isinstance(item, QuayEnum):
        #     return f'Quay.{item.name}'
        # if isinstance(item, ResnEnum):
        #     return f'Resn.{item.name}'
        # if isinstance(item, RoleEnum):
        #     return f'Role.{item.name}'
        # if isinstance(item, SexEnum):
        #     return f'Sex.{item.name}'
        # if isinstance(item, FamcStatEnum):
        #     return f'FamcStat.{item.name}'
        # if isinstance(item, StatEnum):
        #     return f'Stat.{item.name}'
        # if isinstance(item, NameTypeEnum):
        #     return f'NameType.{item.name}'
        code_lines: str = (
            item.code(tabs - 1, full=full)
            .replace(Default.EOL, Default.EMPTY, 1)
            .replace(Default.INDENT, Default.EMPTY, 1)
        )
        return code_lines

    @staticmethod
    def codes(
        items: Any, tabs: int = 1, full: bool = False, required: bool = False
    ) -> str:
        if items is None:
            return Default.NONE
        if isinstance(items, list):
            if len(items) == 0:
                return Default.BRACKET_LEFT_RIGHT
            if len(items) == 1:
                return Formatter.codes_single(items[0], tabs, full)
            lines: str = Default.BRACKET_LEFT
            for item in items:
                line_end = Default.COMMA
                if required:
                    line_end = Default.COMMA_REQUIRED
                if isinstance(item, int | float | Xref):
                    lines = ''.join(
                        [
                            lines,
                            Default.EOL,
                            Default.INDENT * (tabs),
                            str(item),
                            line_end,
                        ]
                    )
                elif isinstance(item, str):
                    quote_mark: str = Default.QUOTE_SINGLE
                    if quote_mark in str(item):
                        quote_mark = Default.QUOTE_DOUBLE
                    lines = ''.join(
                        [
                            lines,
                            Default.EOL,
                            Default.INDENT * (tabs),
                            quote_mark,
                            str(item),
                            quote_mark,
                            line_end,
                        ]
                    )
                else:
                    lines = ''.join(
                        [lines, item.code(tabs, full=full), Default.COMMA]
                    )
            return ''.join(
                [
                    lines,
                    Default.EOL,
                    Default.INDENT * (tabs - 1),
                    Default.BRACKET_RIGHT,
                ]
            )
        return Formatter.codes_single(items, tabs, full)

    @staticmethod
    def codes_line(initial: str, items: Any, tabs: int, full: bool) -> str:
        line_end: str = Default.COMMA
        result: str = Formatter.codes(items, tabs, full)
        keep: bool = full or result not in ['None']
        if keep:
            return ''.join([initial, result, line_end])
        return Default.EMPTY

    @staticmethod
    def display_code(
        name: str, *code_lines: tuple[str, Any, int, bool, bool]
    ) -> str:
        if len(code_lines) > 0:
            lines: str = ''.join([Default.EOL, name, '('])
            for line in code_lines:
                returned_line = Formatter.codes_line(
                    line[0], line[1], line[2], line[3]
                )
                if returned_line != Default.EMPTY:
                    lines = ''.join([lines, Default.EOL, returned_line])
            return ''.join([lines, Default.EOL, ')'])
        return ''.join([Default.EOL, name])

    # @staticmethod
    # def display_two(
    #     name: str, subs: SubsType, ext: Any, tabs: int = 1, full: bool = True
    # ) -> str:
    #     return indent(
    #         Formatter.display_code(
    #             f'{name}',
    #             ('    subs = ', subs, tabs + 1, full, False),
    #             ('    ext = ', ext, tabs + 1, full, True),
    #         ),
    #         Default.INDENT * tabs,
    #     )

    # @staticmethod
    # def display_three(
    #     name: str,
    #     value: str,
    #     subs: SubsType,
    #     ext: Any,
    #     tabs: int = 1,
    #     full: bool = True,
    # ) -> str:
    #     return indent(
    #         Formatter.display_code(
    #             f'{name}',
    #             ('    value = ', value, tabs, full, True),
    #             ('    subs = ', subs, tabs + 1, full, False),
    #             ('    ext = ', ext, tabs + 1, full, True),
    #         ),
    #         Default.INDENT * tabs,
    #     )

    @staticmethod
    def display_no_subs(
        name: str,
        value: str,
        ext: Any,
        tabs: int = 1,
        full: bool = True,
    ) -> str:
        if ext is None and not full:
            return indent(
                Formatter.display_code(f"{name}('{value}')"),
                Default.INDENT * tabs,
            )
        return indent(
            Formatter.display_code(
                f'{name}',
                ('    value = ', value, tabs, full, True),
                ('    ext = ', ext, tabs + 1, full, True),
            ),
            Default.INDENT * tabs,
        )

    @staticmethod
    def base_string(
        value: str,
        sub_name: str,
        ext: Any = None,
        tabs: int = 1,
        full: bool = False,
    ) -> str:
        if ext is None:
            return indent(
                Formatter.display_code(f"{sub_name}('{value}')"),
                Default.INDENT * tabs,
            )
        return indent(
            Formatter.display_code(
                f'{sub_name}',
                ('    value = ', value, tabs, full, True),
                ('    ext = ', ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )

    @staticmethod
    def base_enum(
        value: str,
        sub_name: str,
        extension: Any,
        tabs: int = 1,
        full: bool = False,
    ) -> str:
        if extension is None:
            return indent(
                Formatter.display_code(f'{sub_name}(Tag.{value})'),
                Default.INDENT * tabs,
            )
        return indent(
            Formatter.display_code(
                f'{sub_name}',
                ('    tag = Tag.', value, tabs, full, True),
                ('    extension = ', extension, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )

    # @staticmethod
    # def schema_example(
    #     code_preface: str,
    #     show_code: str,
    #     gedcom_preface: str,
    #     show_ged: str,
    #     superstructures: dict[str, str],
    #     substructures: dict[str, str],
    #     gedcom_docs: str,
    #     genealogy_docs: str,
    # ) -> None:
    #     superstructs: str = Default.EMPTY
    #     substructs: str = Default.EMPTY
    #     key: str
    #     value: str
    #     for key, value in superstructures.items():
    #         superstructs = ''.join(
    #             [
    #                 superstructs,
    #                 Default.EOL,
    #                 f'{Default.INDENT}{key:<40} {value:<6}',
    #             ]
    #         )
    #     for key, value in substructures.items():
    #         substructs = ''.join(
    #             [
    #                 substructs,
    #                 Default.EOL,
    #                 f'{Default.INDENT}{key:<40} {value:<6}',
    #             ]
    #         )
    #     print(
    #         ''.join(
    #             [
    #                 code_preface,
    #                 Default.EOL,
    #                 show_code,
    #                 Default.EOL_DOUBLE,
    #                 gedcom_preface,
    #                 Default.EOL_DOUBLE,
    #                 show_ged,
    #                 Default.EOL,
    #                 Example.SUPERSTRUCTURES,
    #                 superstructs,
    #                 Example.SUBSTRUCTURES,
    #                 substructs,
    #                 Example.GEDCOM_SPECIFICATION,
    #                 gedcom_docs,
    #                 Default.EOL,
    #                 genealogy_docs,
    #             ]
    #         )
    #     )

    # @staticmethod
    # def display_tuple(named_tuple: Any) -> None:
    #     print(
    #         str(named_tuple)
    #         .replace('(', '(\n     ', 1)
    #         .replace(',', ',\n    ')
    #         .replace(')', ',\n)')
    #     )

    # @staticmethod
    # def display(named_tuple: Any, full: bool = False) -> None:
    #     """Display the results of the ged and code methods for a named tuple.

    #     Args:
    #         named_tuple: This is the NamedTuple to display.

    #     There are two methods to run:
    #     1. `ged` runs validate() capturing any error message.
    #     2. `code` which runs even if the ged method fails.
    #     """
    #     # print('DISPLAY:')
    #     # print(f'{Formatter.display_tuple(named_tuple)}\n')
    #     try:
    #         print(f'GED:\n{named_tuple.ged()}')
    #     except Exception as e:
    #         print('ERROR MESSAGE:\n')
    #         print(str(e))
    #         print()
    #     print(f'CODE:{named_tuple.code(full=full)}')


# class Extension(NamedTuple):
#     """Store, validate and display extension tags.

#     The GEDCOM specification recommends the following:

#     > The recommended way to go beyond the set of standard structure types in this specification
#     > or to expand their usage is to submit a feature request on the FamilySearch GEDCOM development page
#     > so that the ramifications of the proposed addition and its interplay with other proposals
#     > may be discussed and the addition may be included in a subsequent version of this specification.
#     >
#     > This specification also provides multiple ways for extension authors to go beyond the specification
#     > without submitting a feature request, which are described in the remainder of this section.

#     This NamedTuple implements going beyond the specification without submitting
#     a feature request.

#     Example:

#     Args:
#         exttag: The tag used entered through ExtTag()
#         payload: The value on the same line as the tag.
#         extra: Extra values on the same line as the tag.
#         substructures: Substructures having this extension as a superstructure.  They are
#             placed in the ged file with a level one higher than this extension has.
#             They are also Extension tuples and may have substructures of their own.

#     See Also:
#         `ExtTag`

#     Reference:
#         [GedCOM Extensions](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#extensions)
#     """

#     exttag: str
#     payload: str = Default.EMPTY
#     extra: str = Default.EMPTY
#     substructures: Any = None

#     def validate(self) -> bool:
#         """Validate the stored value."""
#         check: bool = (
#             Checker.verify_type(self.exttag, ExtTag | Tag, no_list=True)
#             and Checker.verify_type(self.payload, str, no_list=True)
#             and Checker.verify_type(self.extra, str, no_list=True)
#         )
#         if self.substructures is not None:
#             for sub in self.substructures:
#                 if check:
#                     check = sub.validate()
#         return check

#     def ged(self, level: int = 1) -> str:
#         lines: str = ''
#         if self.validate():
#             lines = Tagger.string(
#                 lines, level, self.exttag, self.payload, self.extra
#             )
#             lines = Tagger.structure(lines, level + 1, self.substructures)
#         return lines

#     def code(self, tabs: int = 1, full: bool = False) -> str:
#         return indent(
#             Formatter.display_code(
#                 'Extension(',
#                 ('    exttag = ', self.exttag, tabs, full, True),
#                 ('    payload = ', self.payload, tabs, full, False),
#                 ('    extra = ', self.extra, tabs, full, False),
#                 ('    substructures = ', self.substructures, tabs, full, False),
#             ),
#             Default.INDENT * tabs,
#         )


# ExtType = Extension | list[Extension] | None
ExtType = Any | list[Any] | None


class BaseStructure:
    """The base class for structures with only substructures and extensions.

    Args:
        value: The value associated with the tag.
        subs: One or more substructures permitted by the structure.
    """

    def __init__(
        self,
        value: str | int | Xref,
        subs: Self | list[Self] | None,
        key: str,
    ):
        # Process value argument
        self.value: str | int | Xref = value
        if isinstance(self.value, str):
            self.code_value: str = f"'{self.value}'"
        elif isinstance(self.value, int):
            self.code_value = str(self.value)
        else:
            self.code_value = repr(self.value)

        # Process subs argument
        self.subs: Any = subs
        self.counted: dict[str, int] = {}
        if isinstance(self.subs, list):
            self.counted = collections.Counter(
                [type(sub).__name__ for sub in self.subs]
            )
        elif self.subs is not None:
            self.counted = collections.Counter([type(self.subs).__name__])

        # Process key argument
        self.key = key
        self.tag: str = Structure[self.key][Default.YAML_STANDARD_TAG]
        self.permitted: list[str] = Structure[self.key][Default.YAML_PERMITTED]
        self.required: list[str] = Structure[self.key][Default.YAML_REQUIRED]
        self.single: list[str] = Structure[self.key][Default.YAML_SINGULAR]
        self.enums: list[str] = Structure[self.key][Default.YAML_ENUMS]
        if len(self.enums) > 0 and isinstance(self.value, str):
            self.value = self.value.upper()
            self.code_value = f"'{self.value}'"
        self.payload: str | None = Structure[self.key][Default.YAML_PAYLOAD]
        self.class_name: str = (
            self.key.title().replace('_', '').replace('-', '')
        )

    def validate(self) -> bool:
        """Validate the stored value."""

        # Does it have all required substructures?
        for name in self.required:
            if name not in self.counted:
                raise ValueError(
                    Msg.MISSING_REQUIRED.format(name, self.class_name)
                )

        # Does a single substructure appear only once?
        for name in self.single:
            if name in self.counted and self.counted[name] > 1:
                raise ValueError(
                    Msg.ONLY_ONE_PERMITTED.format(name, self.class_name)
                )

        # Are there substructures when none are permitted?
        if len(self.permitted) == 0 and len(self.counted) > 0:
            raise ValueError(Msg.NO_SUBS.format(self.class_name))

        # Are there substructures not in the permitted list of substructures?
        for name in self.counted:
            if name not in self.permitted:
                raise ValueError(
                    Msg.NOT_PERMITTED.format(
                        name, self.permitted, self.class_name
                    )
                )

        # Is the value of an enumeration substructure in its list of enumerated values?
        if len(self.enums) > 0 and self.value not in self.enums:
            raise ValueError(
                Msg.NOT_VALID_ENUM.format(
                    self.value, self.enums, self.class_name
                )
            )

        # Check that extenions meet requirements.
        # if self.ext is not None:
        #     # Is an extension tag the same as a standard tag?
        #     if isinstance(self.ext, list):
        #         for extension in self.ext:
        #             for yamlkey, yamlvalue in Structure:
        #                 if extension.tag == yamlvalue[Default.YAML_STANDARD_TAG]:
        #                     raise ValueError(Msg.EXTENSION_DUPLICATES_TAG.format(extension.tag, yamlvalue[Default.YAML_STANDARD_TAG]))
        #     else:
        #         for key, value in Structure:
        #             if self.ext.tag == value[Default.YAML_STANDARD_TAG]:
        #                 raise ValueError(Msg.EXTENSION_DUPLICATES_TAG.format(self.ext.tag, value[Default.YAML_STANDARD_TAG]))

        # Does value have the required data type?
        if self.payload not in [
            'https://gedcom.io/terms/v7/type-Enum',
            'https://gedcom.io/terms/v7/type-List#Enum',
        ]:
            match self.payload:
                case 'Y|<NULL>':
                    if not isinstance(self.value, str):
                        raise ValueError(
                            Msg.NOT_STRING.format(
                                repr(self.value), self.class_name
                            )
                        )
                    if str(self.value) not in ['Y', '']:
                        raise ValueError(
                            Msg.VALUE_NOT_Y_OR_NULL.format(
                                self.value, self.class_name
                            )
                        )
                    return True
                case 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger':
                    if not isinstance(self.value, int):
                        raise ValueError(
                            Msg.NOT_INTEGER.format(self.value, self.class_name)
                        )
                    if int(self.value) < 0:
                        raise ValueError(
                            Msg.NEGATIVE_ERROR.format(
                                str(self.value), self.class_name
                            )
                        )
                    return True
                case '@<https://gedcom.io/terms/v7/record-INDI>@':
                    if not isinstance(self.value, IndividualXref):
                        raise ValueError(
                            Msg.NOT_INDIVIDUAL_XREF.format(
                                str(self.value), self.class_name
                            )
                        )
                case '@<https://gedcom.io/terms/v7/record-FAM>@':
                    if not isinstance(self.value, FamilyXref):
                        raise ValueError(
                            Msg.NOT_FAMILY_XREF.format(
                                str(self.value), self.class_name
                            )
                        )
                case 'https://gedcom.io/terms/v7/type-List#Text':
                    if not isinstance(self.value, str):
                        raise ValueError(
                            Msg.NOT_STRING.format(
                                repr(self.value), self.class_name
                            )
                        )
                    if not re.match('', str(self.value)):
                        raise ValueError(
                            Msg.NOT_LIST.format(
                                str(self.value), self.class_name
                            )
                        )
                case '@<https://gedcom.io/terms/v7/record-SUBM>@':
                    if not isinstance(self.value, SubmitterXref):
                        raise ValueError(
                            Msg.NOT_SUBMITTER_XREF.format(
                                str(self.value), self.class_name
                            )
                        )
                case 'http://www.w3.org/2001/XMLSchema#Language':
                    if not isinstance(self.value, str):
                        raise ValueError(
                            Msg.NOT_STRING.format(
                                repr(self.value), self.class_name
                            )
                        )
                    if not re.match('', str(self.value)):
                        raise ValueError(
                            Msg.NOT_LANGUAGE.format(self.value, self.class_name)
                        )
                case 'https://gedcom.io/terms/v7/type-Date#period':
                    if not isinstance(self.value, str):
                        raise ValueError(
                            Msg.NOT_STRING.format(
                                repr(self.value), self.class_name
                            )
                        )
                    if not re.match('^TO|^FROM', self.value) or re.match(
                        '[a-z]', self.value
                    ):
                        raise ValueError(
                            Msg.NOT_DATE_PERIOD.format(
                                self.value, self.class_name
                            )
                        )
                case 'https://gedcom.io/terms/v7/type-Date#exact':
                    if not isinstance(self.value, str):
                        raise ValueError(
                            Msg.NOT_STRING.format(
                                repr(self.value), self.class_name
                            )
                        )
                    if (
                        re.search('[a-z]', self.value) is not None
                        or re.search('[0-9]', self.value) is None
                        or len(re.findall(' ', self.value)) != 2
                    ):
                        raise ValueError(
                            Msg.NOT_DATE_EXACT.format(
                                self.value, self.class_name
                            )
                        )
                case 'https://gedcom.io/terms/v7/type-Date':
                    if not isinstance(self.value, str):
                        raise ValueError(
                            Msg.NOT_STRING.format(
                                repr(self.value), self.class_name
                            )
                        )
                    if (
                        re.search('[a-z]', self.value) is not None
                        or re.search('[0-9]', self.value) is None
                    ):
                        raise ValueError(Msg.NOT_DATE.format(self.value))
                case 'https://gedcom.io/terms/v7/type-FilePath':
                    if not isinstance(self.value, str):
                        raise ValueError(
                            Msg.NOT_STRING.format(
                                repr(self.value), self.class_name
                            )
                        )
                    if not re.match('', self.value):
                        raise ValueError(
                            Msg.NOT_FILE_PATH.format(
                                str(self.value), self.class_name
                            )
                        )
                case 'https://gedcom.io/terms/v7/type-Name':
                    if not isinstance(self.value, str):
                        raise ValueError(
                            Msg.NOT_STRING.format(
                                repr(self.value), self.class_name
                            )
                        )
                    if not len(re.findall('/', self.value)) == 2:
                        raise ValueError(
                            Msg.NOT_NAME.format(self.value, self.class_name)
                        )
                case 'https://gedcom.io/terms/v7/type-Age':
                    if not isinstance(self.value, str):
                        raise ValueError(
                            Msg.NOT_STRING.format(
                                repr(self.value), self.class_name
                            )
                        )
                    if (
                        re.search('[abcefghijklnopqrstuxz]|[A-Z]', self.value)
                        or not re.search('[ymwd]', self.value)
                        or not re.search('[0-9]', self.value)
                        or not re.search('^[<|>|\\d]', self.value)
                        or re.search('[ymwd][ymwd]', self.value)
                    ) and self.value != Default.EMPTY:
                        raise ValueError(
                            Msg.NOT_AGE.format(str(self.value), self.class_name)
                        )
                case 'http://www.w3.org/ns/dcat#mediaType':
                    if not isinstance(self.value, str):
                        raise ValueError(
                            Msg.NOT_STRING.format(
                                repr(self.value), self.class_name
                            )
                        )
                    if not re.match('', str(self.value)):
                        raise ValueError(
                            Msg.NOT_MEDIA_TYPE.format(
                                self.value, self.class_name
                            )
                        )
                case '@<https://gedcom.io/terms/v7/record-OBJE>@':
                    if not isinstance(self.value, MultimediaXref):
                        raise ValueError(
                            Msg.NOT_MULTIMEDIA_XREF.format(
                                repr(self.value), self.class_name
                            )
                        )
                case '@<https://gedcom.io/terms/v7/record-REPO>@':
                    if not isinstance(self.value, RepositoryXref):
                        raise ValueError(
                            Msg.NOT_REPOSITORY_XREF.format(
                                repr(self.value), self.class_name
                            )
                        )
                case '@<https://gedcom.io/terms/v7/record-SNOTE>@':
                    if not isinstance(self.value, SharedNoteXref):
                        raise ValueError(
                            Msg.NOT_SHARED_NOTE_XREF.format(
                                repr(self.value), self.class_name
                            )
                        )
                case '@<https://gedcom.io/terms/v7/record-SOUR>@':
                    if not isinstance(self.value, SourceXref):
                        raise ValueError(
                            Msg.NOT_SOURCE_XREF.format(
                                repr(self.value), self.class_name
                            )
                        )
                case 'https://gedcom.io/terms/v7/type-Time':
                    if not isinstance(self.value, str):
                        raise ValueError(
                            Msg.NOT_STRING.format(
                                repr(self.value), self.class_name
                            )
                        )
                    if not re.match('', str(self.value)):
                        raise ValueError(
                            Msg.NOT_TIME.format(self.value, self.class_name)
                        )
        # Do records have the correct class?
        match self.key:
            case 'record-FAM':
                if not isinstance(self.value, FamilyXref):
                    raise ValueError(
                        Msg.NOT_FAMILY_XREF.format(
                            str(self.value), self.class_name
                        )
                    )
            case 'record-INDI':
                if not isinstance(self.value, IndividualXref):
                    raise ValueError(
                        Msg.NOT_INDIVIDUAL_XREF.format(
                            str(self.value), self.class_name
                        )
                    )
            case 'record-OBJE':
                if not isinstance(self.value, MultimediaXref):
                    raise ValueError(
                        Msg.NOT_MULTIMEDIA_XREF.format(
                            str(self.value), self.class_name
                        )
                    )
            case 'record-REPO':
                if not isinstance(self.value, RepositoryXref):
                    raise ValueError(
                        Msg.NOT_REPOSITORY_XREF.format(
                            str(self.value), self.class_name
                        )
                    )
            case 'record-SNOTE':
                if not isinstance(self.value, SharedNoteXref):
                    raise ValueError(
                        Msg.NOT_SHARED_NOTE_XREF.format(
                            str(self.value), self.class_name
                        )
                    )
            case 'record-SOUR':
                if not isinstance(self.value, SourceXref):
                    raise ValueError(
                        Msg.NOT_SOURCE_XREF.format(
                            str(self.value), self.class_name
                        )
                    )
            case 'record-SUBM':
                if not isinstance(self.value, SubmitterXref):
                    raise ValueError(
                        Msg.NOT_SUBMITTER_XREF.format(
                            str(self.value), self.class_name
                        )
                    )

        # Is value formatted correctly for its structure specification?
        match self.class_name:
            case 'Lati':
                if not isinstance(self.value, str):
                    raise ValueError(Msg.NOT_STRING.format(str(self.value)))
                if self.value[0] not in [
                    Default.LATI_NORTH,
                    Default.LATI_SOUTH,
                ]:
                    raise ValueError(
                        Msg.LATI_NORTH_SOUTH.format(
                            self.value[0],
                            self.value,
                            Default.LATI_NORTH,
                            Default.LATI_SOUTH,
                            self.class_name,
                        )
                    )
                if (
                    float(self.value[1:]) > Default.LATI_HIGH
                    or float(self.value[1:]) < Default.LATI_LOW
                ):
                    raise ValueError(
                        Msg.LATI_RANGE.format(
                            self.value,
                            Default.LATI_LOW,
                            Default.LATI_HIGH,
                            self.class_name,
                        )
                    )
            case 'Long':
                if not isinstance(self.value, str):
                    raise ValueError(Msg.NOT_STRING.format(str(self.value)))
                if self.value[0] not in [Default.LONG_EAST, Default.LONG_WEST]:
                    raise ValueError(
                        Msg.LONG_EAST_WEST.format(
                            self.value[0],
                            self.value,
                            Default.LONG_EAST,
                            Default.LONG_WEST,
                            self.class_name,
                        )
                    )
                if (
                    float(self.value[1:]) > Default.LONG_HIGH
                    or float(self.value[1:]) < Default.LONG_LOW
                ):
                    raise ValueError(
                        Msg.LONG_RANGE.format(
                            self.value,
                            Default.LONG_LOW,
                            Default.LONG_HIGH,
                            self.class_name,
                        )
                    )

        # Check if all subs validate.
        if self.subs is not None:
            if isinstance(self.subs, list):
                for sub in self.subs:
                    sub.validate()
            else:
                self.subs.validate()
        return True

    def ged(self, level: int = 1, format: bool = True) -> str:
        """Generate the GEDCOM lines."""
        if self.validate():
            if self.class_name in [
                'Head',
                'RecordFam',
                'RecordIndi',
                'RecordObje',
                'RecordRepo',
                'RecordSnote',
                'RecordSour',
                'RecordSubm',
                'Trlr',
            ]:
                level = 0
            # Modify self.value if data type is IndividualXref
            if self.class_name in [
                'Alia',
                'Fam',
                'FamHusb',
                'FamWife',
                'Indi',
                'Obje',
                'Repo',
                'Snote',
                'Sour',
                'Subm',
            ]:
                format = False
            lines: str = Default.EMPTY
            if self.key[0:6] == 'record' and isinstance(self.value, Xref):
                lines = self.value.ged()
            elif self.value == Default.EMPTY:
                lines = Tagger.empty(lines, level, self.tag)
            else:
                lines = Tagger.string(
                    lines, level, self.tag, str(self.value), format=format
                )
            if isinstance(self.subs, list):
                lines = Tagger.structure(
                    lines, level + 1, Tagger.order(self.subs)
                )
            else:
                lines = Tagger.structure(lines, level + 1, self.subs)
        return lines.replace('0 TRLR\n', '0 TRLR')

    def code(self, tabs: int = 0, full: bool = True) -> str:
        if (
            self.payload is None
            and not isinstance(self.value, Xref)
            and (
                self.subs is None
                or (isinstance(self.subs, list) and len(self.subs) == 0)
            )
        ):
            return indent(
                Formatter.display_code(f'{self.class_name}()'),
                Default.INDENT * tabs,
            )
        if (self.payload is not None or isinstance(self.value, Xref)) and (
            self.subs is None
            or (isinstance(self.subs, list) and len(self.subs) == 0)
        ):
            return indent(
                Formatter.display_code(f'{self.class_name}({self.code_value})'),
                Default.INDENT * tabs,
            )
        if (
            self.payload is not None or isinstance(self.value, Xref)
        ) and isinstance(self.subs, BaseStructure):
            return indent(
                Formatter.display_code(
                    f'{self.class_name}({self.code_value}, {self.subs.code().replace("\n", "")})'
                ),
                Default.INDENT * tabs,
            )
        if (self.payload is not None or isinstance(self.value, Xref)) and (
            isinstance(self.subs, list) and len(self.subs) == 1
        ):
            return indent(
                Formatter.display_code(
                    f'{self.class_name}({self.code_value}, {self.subs[0].code().replace("\n", "")})'
                ),
                Default.INDENT * tabs,
            )
        if (self.payload is not None or isinstance(self.value, Xref)) and (
            isinstance(self.subs, list) and len(self.subs) > 0
        ):
            return indent(
                Formatter.display_code(
                    f'{self.class_name}',
                    (
                        f'    {Default.CODE_VALUE} = ',
                        self.code_value,
                        tabs + 1,
                        full,
                        False,
                    ),
                    (
                        f'    {Default.CODE_SUBS} = ',
                        self.subs,
                        tabs + 2,
                        full,
                        True,
                    ),
                ),
                Default.INDENT * tabs,
            )
        if (
            self.payload is None
            and isinstance(self.subs, list)
            and len(self.subs) > 0
        ):
            return indent(
                Formatter.display_code(
                    f'{self.class_name}',
                    (
                        f'    {Default.CODE_SUBS} = ',
                        self.subs,
                        tabs + 2,
                        full,
                        True,
                    ),
                ),
                Default.INDENT * tabs,
            )
        return Default.EMPTY


class Ext(BaseStructure):
    """Store, validate and format an extension structure."""

    def __init__(self, key: str, value: str, subs: SubsType):
        super().__init__(value, subs, Default.EMPTY)

        self.tag: str = Default.EMPTY
        self.permitted: list[str] = []
        self.required: list[str] = []
        self.single: list[str] = []
        self.enums: list[str] = []
        self.payload: str | None = Default.EMPTY
        self.yamldict: dict[str, Any] = {}
        if '.yaml' in key:
            if key[0:4] == 'http':
                webUrl = urllib.request.urlopen(key)
                result_code = str(webUrl.getcode())
                if result_code == '404':
                    raise ValueError(Msg.PAGE_NOT_FOUND.format(key))
                raw: str = webUrl.read().decode(Default.UTF8)
            else:
                with io.open(key, 'r', encoding='utf8') as file:  # noqa: UP020
                    raw = file.read()

            # Check that file has proper yaml directive.
            if Default.YAML_DIRECTIVE not in raw:
                raise ValueError(
                    Msg.YAML_NOT_YAML_FILE.format(key, Default.YAML_DIRECTIVE)
                )

            # Put the yaml data into a dictionary.
            raw2: str = raw[raw.find(Default.YAML_DIRECTIVE_END_MARKER) :]
            yaml_data: str = raw2[: raw2.find(Default.YAML_DOCUMENT_END_MARKER)]
            yamldict = yaml.safe_load(yaml_data)
            required = []
            single = []
            permitted = []
            enums = []
            if Default.YAML_SUBSTRUCTURES in yamldict:
                for yamlkey, yamlvalue in yamldict[
                    Default.YAML_SUBSTRUCTURES
                ].items():
                    tag = (
                        yamlkey[yamlkey.rfind(Default.SLASH) + 1 :]
                        .title()
                        .replace('-', '')
                    )
                    permitted.append(tag)
                    if Default.YAML_CARDINALITY_REQUIRED in yamlvalue:
                        required.append(tag)
                    if Default.YAML_CARDINALITY_SINGULAR in yamlvalue:
                        single.append(tag)
            yamldict[Default.YAML_PERMITTED] = permitted
            yamldict[Default.YAML_REQUIRED] = required
            yamldict[Default.YAML_SINGULAR] = single
            if Default.YAML_ENUMERATION_SET in yamldict:
                enumset = yamldict[Default.YAML_ENUMERATION_SET]
                for yamlkey, yamlvalue in Enumeration.items():  # noqa: B007
                    if enumset in yamlvalue[Default.YAML_VALUE_OF]:
                        enums.append(yamlvalue[Default.YAML_STANDARD_TAG])
            yamldict[Default.YAML_ENUMS] = enums
            self.tag = yamldict[Default.YAML_EXTENSION_TAGS][0]
            self.permitted = yamldict[Default.YAML_PERMITTED]
            self.required = yamldict[Default.YAML_REQUIRED]
            self.single = yamldict[Default.YAML_SINGULAR]
            self.enums = yamldict[Default.YAML_ENUMS]
            self.payload = yamldict[Default.YAML_PAYLOAD]
        else:
            self.tag = ExtensionStructure[self.key][
                Default.YAML_EXTENSION_TAGS
            ][0]
            self.permitted = ExtensionStructure[self.key][
                Default.YAML_PERMITTED
            ]
            self.required = ExtensionStructure[self.key][Default.YAML_REQUIRED]
            self.single = ExtensionStructure[self.key][Default.YAML_SINGULAR]
            self.enums = ExtensionStructure[self.key][Default.YAML_ENUMS]
            self.payload = ExtensionStructure[self.key][Default.YAML_PAYLOAD]
            # self.class_name: str = (
            #     self.key.title().replace('_', '').replace('-', '')
            # )
