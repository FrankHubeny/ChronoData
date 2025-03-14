# structure.py
"""Store, validate and display GEDCOM files."""

__all__ = [
    'Abbr',
    'Addr',
    'Adop',
    'AdopFamc',
    'Adr1',
    'Adr2',
    'Adr3',
    'Age',
    'Agnc',
    'Alia',
    'Anci',
    'Anul',
    'Asso',
    'Auth',
    'Bapl',
    'Bapm',
    'Barm',
    'Basm',
    'Birt',
    'Bles',
    'Buri',
    'Caln',
    'Cast',
    'Caus',
    'Chan',
    'Chil',
    'Chr',
    'Chra',
    'City',
    'Conf',
    'Conl',
    'Copr',
    'Corp',
    'Crea',
    'Crem',
    'Crop',
    'Ctry',
    'Data',
    'DataEven',
    'DataEvenDate',
    'Date',
    'DateExact',
    'Deat',
    'Desi',
    'Dest',
    'Div',
    'Divf',
    'Dscr',
    'Educ',
    'Email',
    'Emig',
    'Endl',
    'Enga',
    'Exid',
    'ExidType',
    'FamCens',
    'FamEven',
    'FamFact',
    'FamHusb',
    'FamNchi',
    'FamResi',
    'FamWife',
    'Famc',
    'FamcAdop',
    'FamcStat',
    'Fams',
    'Fax',
    'Fcom',
    'File',
    'FileTran',
    'Form',
    'Gedc',
    'GedcVers',
    'Givn',
    'Grad',
    'Head',
    'HeadDate',
    'HeadLang',
    'HeadPlac',
    'HeadPlacForm',
    'HeadSourData',
    'Height',
    'Husb',
    'Idno',
    'Immi',
    'IndiCens',
    'IndiEven',
    'IndiFact',
    'IndiFamc',
    'IndiName',
    'IndiNchi',
    'IndiReli',
    'IndiTitl',
    'Inil',
    'Lang',
    'Lati',
    'Left',
    'Long',
    'Map',
    'Marb',
    'Marc',
    'Marl',
    'Marr',
    'Mars',
    'Medi',
    'Mime',
    'Name',
    'NameTran',
    'NameType',
    'Nati',
    'Natu',
    'Nick',
    'Nmr',
    'NoDate',
    'Note',
    'NoteTran',
    'Npfx',
    'Nsfx',
    'Obje',
    'Occu',
    'OrdStat',
    'Ordn',
    'Page',
    'Pedi',
    'Phon',
    'Phrase',
    'Plac',
    'PlacForm',
    'PlacTran',
    'Post',
    'Prob',
    'Publ',
    'Quay',
    'RecordFam',
    'RecordIndi',
    'RecordObje',
    'RecordRepo',
    'RecordSnote',
    'RecordSour',
    'RecordSubm',
    'Refn',
    'Reli',
    'Repo',
    'Resn',
    'Reti',
    'Role',
    'Schma',
    'Sdate',
    'Sex',
    'Slgc',
    'Slgs',
    'Snote',
    'Sour',
    'SourData',
    'SourEven',
    'Spfx',
    'Ssn',
    'Stae',
    'Subm',
    'SubmLang',
    'Surn',
    'Tag',
    'Temp',
    'Text',
    'Time',
    'Titl',
    'Top',
    'Trlr',
    'Type',
    'Uid',
    'Vers',
    'Width',
    'Wife',
    'Will',
    'Www',
]

import collections
import contextlib
import io
import logging
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
from genedata.gedcom7 import (
    Calendar,
    Enumeration,
    ExtensionStructure,
    Month,
    Structure,
)
from genedata.messages import Msg

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

    def __init__(self, name: str, tag: str = Default.EMPTY, text: str = Default.EMPTY):
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

    #def ged(self, info: str = Default.EMPTY) -> str:
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

    def __init__(self, name: str, tag: str = XrefTag.SNOTE, text: str = Default.EMPTY):
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


class Input:
    @staticmethod
    def age(
        years: int | float = -1,
        months: int | float = -1,
        weeks: int | float = -1,
        days: int | float = -1,
        greater_less_than: str = Default.GREATER_LESS_THAN,
    ) -> str:
        """The formatted age based on the GEDCOM specification.

        Example:
            The following example has 1.1 years, 2.2 weeks and 1 day.  Since the values
            are rounded down it is best to include non-negative integers for the years, months,
            weeks and days.
            >>> from genedata.structure import Input
            >>> Input.age(1.1, 0, 2.2, 1)
            > 1y 2w 1d
            <BLANKLINE>

            Negative values will not display that unit.
            >>> Input.age(-2, -14.2, -1, 1)
            > 1d
            <BLANKLINE>

        args:
            years: The number of years rounded down to an integer value.
            months: The number of months in addition to the years rounded down to an integer value.
            weeks: The number of weeks in addition to the years and months rounded down to an integer value.
            days: The number of days in addition to the years, months and weeks rounded down to an integer value.
            greater_less_than: A choice between ">", greater than, "<", less than, or "" equal.

        Reference:
        - [GEDCOM Age type](https://gedcom.io/terms/v7/type-Age)
        """
        info: str = Default.EMPTY
        if years >= 0:
            info = ''.join([info, f' {int(years)!s}{Default.AGE_YEAR}'])
        if months >= 0:
            info = ''.join([info, f' {int(months)!s}{Default.AGE_MONTH}'])
        if weeks >= 0:
            info = ''.join([info, f' {int(weeks)!s}{Default.AGE_WEEK}'])
        if days >= 0:
            info = ''.join([info, f' {int(days)!s}{Default.AGE_DAY}'])
        info.replace(Default.SPACE_DOUBLE, Default.SPACE).replace(
            Default.SPACE_DOUBLE, Default.SPACE
        ).strip()
        if info == Default.EMPTY:
            greater_less_than = Default.EMPTY
        return f'{greater_less_than}{info}'.strip()

    @staticmethod
    def date(
        year: int,
        month: int = 0,
        day: int = 0,
        calendar: str = 'GREGORIAN',
        show: bool = False,
    ) -> str:
        """Format a date based on GEDCOM specifications.

        Args:
            year: The integer value of the year.
            month: The integer value of the month in the year.
            day: The integer value of the day in the year.
            calendar: The calendar to use.
            show: If True then the calendar name will be displayed in front of the date.

        Reference:
        - [GEDCOM Date Type](https://gedcom.io/terms/v7/type-Date)"""
        calendar_tag: str = Default.EMPTY
        if show:
            calendar_tag = Calendar[calendar]['standard tag']
        epoch_list: list[str] = Calendar[calendar]['epochs']
        epoch: str = Default.EMPTY
        if year < 0 and len(epoch_list) > 0:
            epoch = epoch_list[0]
            year = abs(year)
        if calendar in ['GREGORIAN', 'JULIAN'] and year == 0:
            raise ValueError(Msg.ZERO_YEAR.format(calendar))
        month_tag: str = Default.EMPTY
        if month > 0:
            month_spec: str = Calendar[calendar]['months'][month - 1]
            month_tag = Month[month_spec[month_spec.rfind('month-') + 6 :]][
                'standard tag'
            ]
        day_tag: str = Default.EMPTY
        if day > 0:
            day_tag = str(day)
        return (
            f'{calendar_tag} {day_tag} {month_tag} {year!s} {epoch}'.replace(
                '  ', ' '
            )
            .replace('  ', ' ')
            .replace('  ', ' ')
            .strip()
        )

    @staticmethod
    def date_period(
        from_date: str = Default.EMPTY, to_date: str = Default.EMPTY
    ) -> str:
        """Display a date period according to GEDCOM specifications.

        The date_period may be empty.

        Examples:
            This example constructs a date period using the Input.date method to construct the from and to dates.
            >>> from genedata.structure import Input
            >>> Input.date_period(
            ...     Input.date(2024, 1, 1), Input.date(2025, 1, 1)
            ... )
            FROM 1 JAN 2024 TO 1 JAN 2025

            This example displays the calendar name on the from date:
            >>> Input.date_period(
            ...     Input.date(2024, 1, 1), Input.date(2025, 1, 1, use_tag=True)
            ... )
            FROM GREGORIAN 1 JAN 2024 TO 1 JAN 2025

        Args:
            from_date: The earliest date of the period.
            to_date: The latest date of the period which may be the only date entered of the period.


        References:
        - [GEDCOM Date Type](https://gedcom.io/terms/v7/type-Date)
        """
        to_value: str = Default.EMPTY
        from_value: str = Default.EMPTY
        if to_date != Default.EMPTY:
            to_value = f'TO {to_date}'
        if from_date != Default.EMPTY:
            from_value = f'FROM {from_date} '
        return f'{from_value}{to_value}'.strip()

    @staticmethod
    def date_between_and(
        between_date: str = Default.EMPTY, and_date: str = Default.EMPTY
    ) -> str:
        """Display a date period according to GEDCOM specifications.

        The date_period may be empty.

        Examples:
            This example constructs a date period using the Input.date method to construct each date.
            The default calendar is the Gregorian calendar.
            >>> from genedata.structure import Input
            >>> Input.date_between_and(
            ...     Input.date(2024, 1, 1), Input.date(2025, 1, 1)
            ... )
            BET 1 JAN 2024 AND 1 JAN 2025

            This example displays the calendar name on the from date:
            >>> Input.date_period(
            ...     Input.date(2024, 1, 1), Input.date(2025, 1, 1, show=True)
            ... )
            BET GREGORIAN 1 JAN 2024 AND 1 JAN 2025

        Args:
            between_date: The date following the BET tag.
            and_date: The date following the AND tag.

        References:
        - [GEDCOM Date Type](https://gedcom.io/terms/v7/type-Date)
        """
        between_value: str = Default.EMPTY
        and_value: str = Default.EMPTY
        if between_date != Default.EMPTY:
            between_value = f'BET {between_date}'
        if and_date != Default.EMPTY:
            and_value = f' AND {and_date} '
        return f'{between_value}{and_value}'.strip()

    @staticmethod
    def date_after(date: str = Default.EMPTY) -> str:
        """Format a date with the AFT tag in front of it.

        Examples:
            This example constructs a date after using the Input.date method to construct date.
            >>> from genedata.structure import Input
            >>> Input.date_after(Input.date(2024, 1, 1))
            AFT 1 JAN 2024

            This example displays the calendar name on the date:
            >>> Input.date_after(Input.date(2025, 1, 1, show=True))
            AFT GREGORIAN 1 JAN 2024

        Args:
            date: The date following the AFT tag.

        References:
        - [GEDCOM Date Type](https://gedcom.io/terms/v7/type-Date)
        """
        value: str = Default.EMPTY
        if date != Default.EMPTY:
            value = f'AFT {date}'
        return value

    @staticmethod
    def date_before(date: str = Default.EMPTY) -> str:
        """Display a date with the BEF tag according to GEDCOM specifications.

        Examples:
            This example constructs a date from the Input.date method.
            This method attached the BEF tag in front of that date.
            >>> from genedata.structure import Input
            >>> Input.date_before(Input.date(2024, 1, 1))
            BEF 1 JAN 2024

            This example displays the calendar name on the date:
            >>> Input.date_before(Input.date(2025, 1, 1, show=True))
            BEF GREGORIAN 1 JAN 2025

        Args:
            date: The date following the BEF tag.

        References:
        - [GEDCOM Date Type](https://gedcom.io/terms/v7/type-Date)
        """
        value: str = Default.EMPTY
        if date != Default.EMPTY:
            value = f'BEF {date}'
        return value

    @staticmethod
    def date_about(date: str = Default.EMPTY) -> str:
        """Display a date with the ABT tag according to GEDCOM specifications.

        Examples:
            This example constructs a date from the Input.date method.
            This method attaches the ABT tag in front of that date.
            >>> from genedata.structure import Input
            >>> Input.date_about(Input.date(2024, 1, 1))
            ABT 1 JAN 2024

            This example displays the calendar name on the date:
            >>> Input.date_before(Input.date(2025, 1, 1, show=True))
            AFT GREGORIAN 1 JAN 2025

        Args:
            date: The date following the AFT tag.

        References:
        - [GEDCOM Date Type](https://gedcom.io/terms/v7/type-Date)
        """
        value: str = Default.EMPTY
        if date != Default.EMPTY:
            value = f'ABT {date}'
        return value

    @staticmethod
    def date_calculated(date: str = Default.EMPTY) -> str:
        """Display a date with the CAL tag according to GEDCOM specifications.

        Examples:
            This example constructs a date from the Input.date method.
            This method attaches the CAL tag in front of that date.
            >>> from genedata.structure import Input
            >>> Input.date_calculated(Input.date(2024, 1, 1))
            CAL 1 JAN 2024

            This example displays the calendar name on the date:
            >>> Input.date_calculated(Input.date(2025, 1, 1, show=True))
            CAL GREGORIAN 1 JAN 2025

        Args:
            date: The date following the AFT tag.

        References:
        - [GEDCOM Date Type](https://gedcom.io/terms/v7/type-Date)
        """
        value: str = Default.EMPTY
        if date != Default.EMPTY:
            value = f'CAL {date}'
        return value

    @staticmethod
    def date_estimated(date: str = Default.EMPTY) -> str:
        """Display a date with the EST tag according to GEDCOM specifications.

        Examples:
            This example constructs a date from the Input.date method.
            This method attaches the EST tag in front of that date.
            >>> from genedata.structure import Input
            >>> Input.date_estimated(Input.date(2024, 1, 1))
            EST 1 JAN 2024

            This example displays the calendar name on the date:
            >>> Input.date_estimatedd(Input.date(2025, 1, 1, show=True))
            EST GREGORIAN 1 JAN 2025

        Args:
            date: The date following the AFT tag.

        References:
        - [GEDCOM Date Type](https://gedcom.io/terms/v7/type-Date)
        """
        value: str = Default.EMPTY
        if date != Default.EMPTY:
            value = f'EST {date}'
        return value

    @staticmethod
    def name(full: str, surname: str) -> str:
        """Format a personal name to meet GEDCOM name type specifications.

        Example:
            >>> from genedata.structure import Input
            >>> Input.name('Jim Smith', 'Smith')
            Jim /Smith/

            If more than one space separates parts of the name they are removed along with
            spaces at the beginning or end of the name.
            >>> Input.name(' Jim      Smith ', '   Smith ')
            Jim /Smith/

            Line breaks are also removed from both name and surname.
            >>> Input.name(' Jim\n\n\nSmith\n', '\n\nSmith\n')
            Jim /Smith/

            This methods assists formatting a personal name using IndiName.
            >>> from genedata.structure import IndiName
            >>> m = IndiName(Input.name('Jim Smith', 'Smith'))
            >>> print(m.ged())
            1 NAME Jim /Smith/
            <BLANKLINE>

        Args:
            full: The full name of the person.
            surname: The surname of the person. This will be used to put a "/" around the surname
                in the full name.

        Reference:
        - [GEDCOM type Name](https://gedcom.io/terms/v7/type-Name)
        """

        # Remove extraneous characters from full.
        edited_name: str = full
        edited_name = re.sub(Default.EOL, Default.SPACE, edited_name)
        while Default.SPACE_DOUBLE in edited_name:
            edited_name = re.sub(Default.SPACE_DOUBLE, Default.SPACE, edited_name)
        edited_name = edited_name.strip()

        # Remove extraneous characters from surname.
        edited_surname: str = surname
        edited_surname = re.sub(Default.EOL, Default.SPACE, edited_surname)
        while Default.SPACE_DOUBLE in edited_surname:
            edited_surname = re.sub(Default.SPACE_DOUBLE, Default.SPACE, edited_surname)
        edited_surname = edited_surname.strip()

        # Replace surname in full with slashed surname.
        if edited_surname in edited_name:
            surname_slash = f'{Default.SLASH}{edited_surname}{Default.SLASH}'
            edited_name = re.sub(edited_surname, surname_slash, edited_name)
        return edited_name

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
    def lati(
        degrees: int, minutes: int, seconds: float, precision: int = 6
    ) -> str:
        latitude = Input.to_decimal(degrees, minutes, seconds, precision)
        if latitude > Default.LATI_HIGH or latitude < Default.LATI_LOW:
            raise ValueError(
                Msg.LATI_RANGE_METHOD.format(
                    latitude, Default.LATI_LOW, Default.LATI_HIGH
                )
            )
        if degrees >= 0:
            return f'{Default.LATI_NORTH}{latitude!s}'
        return f'{Default.LATI_SOUTH}{abs(latitude)!s}'

    @staticmethod
    def long(
        degrees: int, minutes: int, seconds: float, precision: int = 6
    ) -> str:
        longitude = Input.to_decimal(degrees, minutes, seconds, precision)
        if longitude > Default.LONG_HIGH or longitude < Default.LONG_LOW:
            raise ValueError(
                Msg.LONG_RANGE_METHOD.format(
                    longitude, Default.LONG_LOW, Default.LONG_HIGH
                )
            )
        if degrees >= 0:
            return f'{Default.LONG_EAST}{longitude!s}'
        return f'{Default.LONG_WEST}{abs(longitude)!s}'

    @staticmethod
    def from_ged(lines: str | list[list[str]]) -> str:
        if isinstance(lines, str):
            strlist: list[list[str]] = [
                a.split(' ') for a in lines.split('\n') if a != ''
            ]
            return Input.from_ged(strlist)
        level: int = int(lines[0][0])
        tag: str = lines[0][1]
        payload: str = Default.EMPTY
        output: str = Default.EMPTY
        number_of_lines: int = len(lines)
        if len(lines[0]) == 3:
            payload = lines[0][2]
        output = f'{tag}({payload}'
        intermediate_lines: list[list[str]] = []
        number_of_lines = len(lines[1:])
        for i in range(number_of_lines):
            if int(lines[i][0]) == level and len(intermediate_lines) > 0:
                output = ''.join(
                    [output, '[', Input.from_ged(intermediate_lines), '])']
                )
                intermediate_lines = []
            elif int(lines[i][0]) == level:
                output = ''.join([output, ')'])
                if i < number_of_lines:
                    return ''.join(
                        [',', output, Input.from_ged(lines[i:]), ')']
                    )
                return output
            else:
                intermediate_lines.append(lines[i])
        return output


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
                            Msg.NOT_STRING.format(repr(self.value), self.class_name)
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
                            Msg.NOT_STRING.format(repr(self.value), self.class_name)
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
                            Msg.NOT_STRING.format(repr(self.value), self.class_name)
                        )
                    if not re.match('', str(self.value)):
                        raise ValueError(
                            Msg.NOT_LANGUAGE.format(
                                self.value, self.class_name
                            )
                        )
                case 'https://gedcom.io/terms/v7/type-Date#period':
                    if not isinstance(self.value, str):
                        raise ValueError(
                            Msg.NOT_STRING.format(repr(self.value), self.class_name)
                        )
                    if not re.match('^TO|^FROM', self.value) or re.match('[a-z]', self.value):
                        raise ValueError(
                            Msg.NOT_DATE_PERIOD.format(
                                self.value, self.class_name
                            )
                        )
                case 'https://gedcom.io/terms/v7/type-Date#exact':
                    if not isinstance(self.value, str):
                        raise ValueError(
                            Msg.NOT_STRING.format(repr(self.value), self.class_name)
                        )
                    if not re.match('\\d$', self.value) or re.match('[a-z]', self.value) or not re.search('[0-9]', self.value):
                        raise ValueError(
                            Msg.NOT_DATE_EXACT.format(
                                self.value, self.class_name
                            )
                        )
                case 'https://gedcom.io/terms/v7/type-Date':
                    if not isinstance(self.value, str):
                        raise ValueError(
                            Msg.NOT_STRING.format(repr(self.value), self.class_name)
                        )
                    if re.match('[a-z]', self.value) or not re.search('[0-9]', self.value):
                        raise ValueError(Msg.NOT_DATE.format(str(self.value)))
                case 'https://gedcom.io/terms/v7/type-FilePath':
                    if not isinstance(self.value, str):
                        raise ValueError(
                            Msg.NOT_STRING.format(repr(self.value), self.class_name)
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
                            Msg.NOT_STRING.format(repr(self.value), self.class_name)
                        )
                    if not re.match('[/][/]', (self.value)):
                        raise ValueError(
                            Msg.NOT_NAME.format(
                                self.value, self.class_name
                            )
                        )
                case 'https://gedcom.io/terms/v7/type-Age':
                    if not isinstance(self.value, str):
                        raise ValueError(
                            Msg.NOT_STRING.format(repr(self.value), self.class_name)
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
                            Msg.NOT_STRING.format(repr(self.value), self.class_name)
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
                            Msg.NOT_STRING.format(repr(self.value), self.class_name)
                        )
                    if not re.match('', str(self.value)):
                        raise ValueError(
                            Msg.NOT_TIME.format(
                                self.value, self.class_name
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
                'FamHusb',
                'FamWife',
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
        return lines  

    def code(self, tabs: int = 0, full: bool = True) -> str:
        if self.payload is None and (
            self.subs is None
            or (isinstance(self.subs, list) and len(self.subs) == 0)
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
        if (self.payload is not None or isinstance(self.value, Xref)) and isinstance(self.subs, BaseStructure):
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


# Classes below this marker were genered by the genedata.gedcom7 Display class
# by calling Display.generate_all_classes or Display.generate_class.



class Abbr(BaseStructure):
    '''Store, validate and format the ABBR structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Abbreviation
    > A short name of a title, description, or name used for sorting, filing, and
    > retrieving records.
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM ABBR Structure](https://gedcom.io/terms/v7/ABBR)
    '''
    
    key: str = 'ABBR'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Addr(BaseStructure):
    '''Store, validate and format the ADDR structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Address
    > The location of, or most relevant to, the subject of the superstructure.
    > See `ADDRESS_STRUCTURE` for more details.
    > A specific building, plot, or location. The payload is the full formatted
    > address as it would appear on a mailing label, including appropriate line
    > breaks (encoded using `CONT` tags). The expected order of address components
    > varies by region; the address should be organized as expected by the addressed
    > region.
    > 
    > Optionally, additional substructures such as `STAE` and `CTRY` are provided to
    > be used by systems that have structured their addresses for indexing and
    > sorting. If the substructures and `ADDR` payload disagree, the `ADDR` payload
    > shall be taken as correct. Because the regionally-correct order and formatting
    > of address components cannot be determined from the substructures alone, the
    > `ADDR` payload is required, even if its content appears to be redundant with
    > the substructures.
    > 
    > <div class="deprecation">
    > 
    > `ADR1` and `ADR2` were introduced in version 5.5 (1996) and `ADR3` in version
    > 5.5.1 (1999), defined as "The first/second/third line of an address." Some
    > applications interpreted ADR1 as "the first line of the *street* address", but
    > most took the spec as-written and treated it as a straight copy of a line of
    > text already available in the `ADDR` payload.
    > 
    > Duplicating information bloats files and introduces the potential for
    > self-contradiction. `ADR1`, `ADR2`, and `ADR3` should not be added to new
    > files.
    > 
    > </div>
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADR1            | Many     | No       |
    | https://gedcom.io/terms/v7/ADR2            | Many     | No       |
    | https://gedcom.io/terms/v7/ADR3            | Many     | No       |
    | https://gedcom.io/terms/v7/CITY            | Many     | No       |
    | https://gedcom.io/terms/v7/CTRY            | Many     | No       |
    | https://gedcom.io/terms/v7/POST            | Many     | No       |
    | https://gedcom.io/terms/v7/STAE            | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM ADDR Structure](https://gedcom.io/terms/v7/ADDR)
    '''
    
    key: str = 'ADDR'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class AdopFamc(BaseStructure):
    '''Store, validate and format the FAMC structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Family child
    > The individual or couple that adopted this individual.
    > 
    > Adoption by an individual, rather than a couple, may be represented either by
    > pointing to a `FAM` where that individual is a `HUSB` or `WIFE` and using a
    > `https://gedcom.io/terms/v7/FAMC-ADOP` substructure to indicate which 1
    > performed the adoption; or by using a `FAM` where the adopting individual is
    > the only `HUSB`/`WIFE`.
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/FAMC-ADOP       | Many     | No       |
        
    Args:
        value: A value of data type @<https://gedcom.io/terms/v7/record-FAM>@
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM FAMC Structure](https://gedcom.io/terms/v7/ADOP-FAMC)
    '''
    
    key: str = 'ADOP-FAMC'
        
    def __init__(self, value: FamilyXref, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Adop(BaseStructure):
    '''Store, validate and format the ADOP structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Adoption
    > An [Individual Event]. See also `INDIVIDUAL_EVENT_STRUCTURE`.
    > adoption
    > Creation of a legally approved child-parent relationship that does not
    > exist biologically.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/ADOP-FAMC       | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM ADOP Structure](https://gedcom.io/terms/v7/ADOP)
    '''
    
    key: str = 'ADOP'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Adr1(BaseStructure):
    '''Store, validate and format the ADR1 structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Address Line 1
    > The first line of the address, used for indexing. This structure's payload
    > should be a single line of text equal to the first line of the corresponding
    > `ADDR`. See `ADDRESS_STRUCTURE` for more details.
    > 
    > <div class="deprecation">
    > 
    > `ADR1` should not be added to new files; see `ADDRESS_STRUCTURE` for more
    > details.
    > 
    > </div>
    > 
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM ADR1 Structure](https://gedcom.io/terms/v7/ADR1)
    '''
    
    key: str = 'ADR1'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
        logging.info(Msg.DEPRECATION_WARNING.format(self.class_name))
    

class Adr2(BaseStructure):
    '''Store, validate and format the ADR2 structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Address Line 2
    > The second line of the address, used for indexing. This structure's payload
    > should be a single line of text equal to the second line of the corresponding
    > `ADDR`. See `ADDRESS_STRUCTURE` for more details.
    > 
    > <div class="deprecation">
    > 
    > `ADR2` should not be added to new files; see `ADDRESS_STRUCTURE` for more
    > details.
    > 
    > </div>
    > 
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM ADR2 Structure](https://gedcom.io/terms/v7/ADR2)
    '''
    
    key: str = 'ADR2'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
        logging.info(Msg.DEPRECATION_WARNING.format(self.class_name))
    

class Adr3(BaseStructure):
    '''Store, validate and format the ADR3 structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Address Line 3
    > The third line of the address, used for indexing. This structure's payload
    > should be a single line of text equal to the third line of the corresponding
    > `ADDR`. See `ADDRESS_STRUCTURE` for more details.
    > 
    > <div class="deprecation">
    > 
    > `ADR3` should not be added to new files; see `ADDRESS_STRUCTURE` for more
    > details.
    > 
    > </div>
    > 
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM ADR3 Structure](https://gedcom.io/terms/v7/ADR3)
    '''
    
    key: str = 'ADR3'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
        logging.info(Msg.DEPRECATION_WARNING.format(self.class_name))
    

class Age(BaseStructure):
    '''Store, validate and format the AGE structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Age at event
    > The age of the individual at the time an event occurred, or the age listed
    > in the document.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/PHRASE          | Many     | No       |
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-Age
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM AGE Structure](https://gedcom.io/terms/v7/AGE)
    '''
    
    key: str = 'AGE'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Agnc(BaseStructure):
    '''Store, validate and format the AGNC structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Responsible agency
    > The organization, institution, corporation, person, or other entity that
    > has responsibility for the associated context. Examples are an employer of
    > a person of an associated occupation, or a church that administered rites
    > or events, or an organization responsible for creating or archiving
    > records.
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM AGNC Structure](https://gedcom.io/terms/v7/AGNC)
    '''
    
    key: str = 'AGNC'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Alia(BaseStructure):
    '''Store, validate and format the ALIA structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Alias
    > A single individual may have facts distributed across multiple individual
    > records, connected by `ALIA` pointers (named after "alias" in the computing
    > sense, not the pseudonym sense).
    > 
    > <div class="note">
    > 
    > This specification does not define how to connect `INDI` records with `ALIA`.
    > Some systems organize `ALIA` pointers to create a tree structure, with the root
    > `INDI` record containing the composite view of all facts in the leaf `INDI`
    > records. Others distribute events and attributes between `INDI` records
    > mutually linked by symmetric pairs of `ALIA` pointers. A future version of this
    > specification may adjust the definition of `ALIA`.
    > 
    > </div>
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/PHRASE          | Many     | No       |
        
    Args:
        value: A value of data type @<https://gedcom.io/terms/v7/record-INDI>@
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM ALIA Structure](https://gedcom.io/terms/v7/ALIA)
    '''
    
    key: str = 'ALIA'
        
    def __init__(self, value: IndividualXref, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Anci(BaseStructure):
    '''Store, validate and format the ANCI structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Ancestor interest
    > Indicates an interest in additional research for ancestors of this
    > individual. (See also `DESI`).
        
    Args:
        value: A value of data type @<https://gedcom.io/terms/v7/record-SUBM>@
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM ANCI Structure](https://gedcom.io/terms/v7/ANCI)
    '''
    
    key: str = 'ANCI'
        
    def __init__(self, value: SubmitterXref, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Anul(BaseStructure):
    '''Store, validate and format the ANUL structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Annulment
    > A [Family Event]. See also `FAMILY_EVENT_STRUCTURE`.
    > annulment
    > Declaring a marriage void from the beginning (never existed).
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/HUSB            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WIFE            | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM ANUL Structure](https://gedcom.io/terms/v7/ANUL)
    '''
    
    key: str = 'ANUL'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Asso(BaseStructure):
    '''Store, validate and format the ASSO structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Associates
    > A pointer to an associated individual. See `ASSOCIATION_STRUCTURE` for more
    > details.
    > An individual associated with the subject of the superstructure. The nature of
    > the association is indicated in the `ROLE` substructure.
    > 
    > A `voidPtr` and `PHRASE` can be used to describe associations to people not
    > referenced by any `INDI` record.
    > 
    > <div class="example">
    > 
    > The following indicates that "Mr Stockdale" was the individual's teacher and
    > that individual `@I2@` was the clergy officiating at their baptism.
    > 
    > ```gedcom
    > 0 @I1@ INDI
    > 1 ASSO @VOID@
    > 2 PHRASE Mr Stockdale
    > 2 ROLE OTHER
    > 3 PHRASE Teacher
    > 1 BAPM
    > 2 DATE 1930
    > 2 ASSO @I2@
    > 3 ROLE CLERGY
    > ```
    > 
    > </div>
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHRASE          | Many     | No       |
    | https://gedcom.io/terms/v7/ROLE            | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
        
    Args:
        value: A value of data type @<https://gedcom.io/terms/v7/record-INDI>@
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM ASSO Structure](https://gedcom.io/terms/v7/ASSO)
    '''
    
    key: str = 'ASSO'
        
    def __init__(self, value: IndividualXref, subs: Any) -> None:
        super().__init__(value, subs, self.key)
    

class Auth(BaseStructure):
    '''Store, validate and format the AUTH structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Author
    > The person, agency, or entity who created the record. For a published work,
    > this could be the author, compiler, transcriber, abstractor, or editor. For
    > an unpublished source, this may be an individual, a government agency,
    > church organization, or private organization.
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM AUTH Structure](https://gedcom.io/terms/v7/AUTH)
    '''
    
    key: str = 'AUTH'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Bapl(BaseStructure):
    '''Store, validate and format the BAPL structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Baptism, Latter-Day Saint
    > A [Latter-Day Saint Ordinance]. See also `LDS_INDIVIDUAL_ORDINANCE`.
    > baptism
    > The event of baptism performed at age 8 or later by priesthood authority of
    > The Church of Jesus Christ of Latter-day Saints. (See also [`BAPM`])
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TEMP            | Many     | No       |
    | https://gedcom.io/terms/v7/ord-STAT        | Many     | No       |
        
    Args:
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM BAPL Structure](https://gedcom.io/terms/v7/BAPL)
    '''
    
    key: str = 'BAPL'
        
    def __init__(self, subs: Any = None) -> None:
        super().__init__(Default.EMPTY, subs, self.key)
    

class Bapm(BaseStructure):
    '''Store, validate and format the BAPM structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Baptism
    > An [Individual Event]. See also `INDIVIDUAL_EVENT_STRUCTURE`.
    > baptism
    > Baptism, performed in infancy or later. (See also [`BAPL`] and `CHR`.)
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM BAPM Structure](https://gedcom.io/terms/v7/BAPM)
    '''
    
    key: str = 'BAPM'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Barm(BaseStructure):
    '''Store, validate and format the BARM structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Bar Mitzvah
    > An [Individual Event]. See also `INDIVIDUAL_EVENT_STRUCTURE`.
    > Bar Mitzvah
    > The ceremonial event held when a Jewish boy reaches age 13.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM BARM Structure](https://gedcom.io/terms/v7/BARM)
    '''
    
    key: str = 'BARM'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Basm(BaseStructure):
    '''Store, validate and format the BASM structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Bas Mitzvah
    > An [Individual Event]. See also `INDIVIDUAL_EVENT_STRUCTURE`.
    > Bas Mitzvah
    > The ceremonial event held when a Jewish girl reaches age 13, also known as
    > "Bat Mitzvah."
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM BASM Structure](https://gedcom.io/terms/v7/BASM)
    '''
    
    key: str = 'BASM'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Birt(BaseStructure):
    '''Store, validate and format the BIRT structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Birth
    > An [Individual Event]. See also `INDIVIDUAL_EVENT_STRUCTURE`.
    > birth
    > Entering into life.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAMC            | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM BIRT Structure](https://gedcom.io/terms/v7/BIRT)
    '''
    
    key: str = 'BIRT'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Bles(BaseStructure):
    '''Store, validate and format the BLES structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Blessing
    > An [Individual Event]. See also `INDIVIDUAL_EVENT_STRUCTURE`.
    > blessing
    > Bestowing divine care or intercession. Sometimes given in connection with a
    > naming ceremony.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM BLES Structure](https://gedcom.io/terms/v7/BLES)
    '''
    
    key: str = 'BLES'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Buri(BaseStructure):
    '''Store, validate and format the BURI structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Depositing remains
    > An [Individual Event]. See also `INDIVIDUAL_EVENT_STRUCTURE`.
    > 
    > Although defined as any depositing of remains since it was introduced in the
    > first version of GEDCOM, this tag is a shortened form of the English word
    > "burial" and has been interpreted to mean "depositing of remains by burial" by
    > some applications and users. In the absence of a clarifying `TYPE` substructure
    > it is likely, but not guaranteed, that a `BURI` structure refers to a burial
    > rather than another form of depositing remains.
    > 
    > depositing remains
    > Depositing the mortal remains of a deceased person.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM BURI Structure](https://gedcom.io/terms/v7/BURI)
    '''
    
    key: str = 'BURI'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Caln(BaseStructure):
    '''Store, validate and format the CALN structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Call number
    > An identification or reference description used to file and retrieve items
    > from the holdings of a repository. Despite the word "number" in the name,
    > may contain any character, not just digits.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/MEDI            | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM CALN Structure](https://gedcom.io/terms/v7/CALN)
    '''
    
    key: str = 'CALN'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Cast(BaseStructure):
    '''Store, validate and format the CAST structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Caste
    > An [Individual Attribute]. See also `INDIVIDUAL_ATTRIBUTE_STRUCTURE`.
    > caste
    > The name of an individual's rank or status in society which is sometimes
    > based on racial or religious differences, or differences in wealth,
    > inherited rank, profession, or occupation.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM CAST Structure](https://gedcom.io/terms/v7/CAST)
    '''
    
    key: str = 'CAST'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Caus(BaseStructure):
    '''Store, validate and format the CAUS structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Cause
    > The reasons which precipitated an event. It is often used subordinate to a
    > death event to show cause of death, such as might be listed on a death
    > certificate.
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM CAUS Structure](https://gedcom.io/terms/v7/CAUS)
    '''
    
    key: str = 'CAUS'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Chan(BaseStructure):
    '''Store, validate and format the CHAN structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Change
    > The most recent change to the superstructure. This is metadata about the
    > structure itself, not data about its subject. See `CHANGE_DATE` for more
    > details.
    > The date of the most recent modification of the superstructure, optionally with
    > notes about that modification.
    > 
    > The `NOTE` substructure may describe previous changes as well as the most
    > recent, although only the most recent change is described by the `DATE`
    > substructure.
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/DATE-exact      | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
        
    Args:
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM CHAN Structure](https://gedcom.io/terms/v7/CHAN)
    '''
    
    key: str = 'CHAN'
        
    def __init__(self, subs: Any) -> None:
        super().__init__(Default.EMPTY, subs, self.key)
    

class Chil(BaseStructure):
    '''Store, validate and format the CHIL structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Child
    > The child in a family, whether biological, adopted, foster, sealed, or
    > other relationship.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/PHRASE          | Many     | No       |
        
    Args:
        value: A value of data type @<https://gedcom.io/terms/v7/record-INDI>@
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM CHIL Structure](https://gedcom.io/terms/v7/CHIL)
    '''
    
    key: str = 'CHIL'
        
    def __init__(self, value: IndividualXref, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Chr(BaseStructure):
    '''Store, validate and format the CHR structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Christening
    > An [Individual Event]. See also `INDIVIDUAL_EVENT_STRUCTURE`.
    > christening
    > Baptism or naming events for a child.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAMC            | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM CHR Structure](https://gedcom.io/terms/v7/CHR)
    '''
    
    key: str = 'CHR'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Chra(BaseStructure):
    '''Store, validate and format the CHRA structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Christening, adult
    > An [Individual Event]. See also `INDIVIDUAL_EVENT_STRUCTURE`.
    > adult christening
    > Baptism or naming events for an adult person.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM CHRA Structure](https://gedcom.io/terms/v7/CHRA)
    '''
    
    key: str = 'CHRA'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class City(BaseStructure):
    '''Store, validate and format the CITY structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > City
    > The name of the city used in the address. See `ADDRESS_STRUCTURE` for more
    > details.
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM CITY Structure](https://gedcom.io/terms/v7/CITY)
    '''
    
    key: str = 'CITY'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Conf(BaseStructure):
    '''Store, validate and format the CONF structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Confirmation
    > An [Individual Event]. See also `INDIVIDUAL_EVENT_STRUCTURE`.
    > confirmation
    > Conferring full church membership.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM CONF Structure](https://gedcom.io/terms/v7/CONF)
    '''
    
    key: str = 'CONF'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Conl(BaseStructure):
    '''Store, validate and format the CONL structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Confirmation, Latter-Day Saint
    > A [Latter-Day Saint Ordinance]. See also `LDS_INDIVIDUAL_ORDINANCE`.
    > confirmation
    > The religious event by which a person receives membership in The Church of
    > Jesus Christ of Latter-day Saints. (See also [`CONF`])
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TEMP            | Many     | No       |
    | https://gedcom.io/terms/v7/ord-STAT        | Many     | No       |
        
    Args:
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM CONL Structure](https://gedcom.io/terms/v7/CONL)
    '''
    
    key: str = 'CONL'
        
    def __init__(self, subs: Any = None) -> None:
        super().__init__(Default.EMPTY, subs, self.key)
    

class Copr(BaseStructure):
    '''Store, validate and format the COPR structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Copyright
    > A copyright statement, as appropriate for the copyright laws applicable to
    > this data.
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM COPR Structure](https://gedcom.io/terms/v7/COPR)
    '''
    
    key: str = 'COPR'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Corp(BaseStructure):
    '''Store, validate and format the CORP structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Corporate name
    > The name of the business, corporation, or person that produced or
    > commissioned the product.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM CORP Structure](https://gedcom.io/terms/v7/CORP)
    '''
    
    key: str = 'CORP'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Crea(BaseStructure):
    '''Store, validate and format the CREA structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Creation
    > The initial creation of the superstructure. This is metadata about the
    > structure itself, not data about its subject. See `CREATION_DATE` for more
    > details.
    > The date of the initial creation of the superstructure. Because this refers
    > to the initial creation, it should not be modified after the structure is
    > created.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/DATE-exact      | Many     | No       |
        
    Args:
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM CREA Structure](https://gedcom.io/terms/v7/CREA)
    '''
    
    key: str = 'CREA'
        
    def __init__(self, subs: Any) -> None:
        super().__init__(Default.EMPTY, subs, self.key)
    

class Crem(BaseStructure):
    '''Store, validate and format the CREM structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Cremation
    > An [Individual Event]. See also `INDIVIDUAL_EVENT_STRUCTURE`.
    > cremation
    > The act of reducing a dead body to ashes by fire.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM CREM Structure](https://gedcom.io/terms/v7/CREM)
    '''
    
    key: str = 'CREM'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Crop(BaseStructure):
    '''Store, validate and format the CROP structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Crop
    > A subregion of an image to display. It is only valid when the superstructure
    > links to a `MULTIMEDIA_RECORD` with at least 1 `FILE` substructure that refers
    > to an external file with a defined pixel unit.
    > 
    > `LEFT` and `TOP` indicate the top-left corner of the region to display. `WIDTH`
    > and `HEIGHT` indicate how many pixels wide and tall the region to display is.
    > If omitted, `LEFT` and `TOP` each default to 0; `WIDTH` defaults to the image
    > width minus `LEFT`; and `HEIGHT` defaults to the image height minus `TOP`.
    > 
    > If the superstructure links to a `MULTIMEDIA_RECORD` that includes multiple
    > `FILE` substructures, the `CROP` applies to the first `FILE` to which it can
    > apply, namely the first external file with a defined pixel unit.
    > 
    > It is recommended that `CROP` be used only with a single-FILE
    > `MULTIMEDIA_RECORD`.
    > 
    > The following are errors:
    > 
    > - `LEFT` or `LEFT` + `WIDTH` exceed the image width.
    > - `TOP` or `TOP` + `HEIGHT` exceed the image height.
    > - `CROP` applied to a non-image or image without a defined pixel unit.
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/HEIGHT          | Many     | No       |
    | https://gedcom.io/terms/v7/LEFT            | Many     | No       |
    | https://gedcom.io/terms/v7/TOP             | Many     | No       |
    | https://gedcom.io/terms/v7/WIDTH           | Many     | No       |
        
    Args:
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM CROP Structure](https://gedcom.io/terms/v7/CROP)
    '''
    
    key: str = 'CROP'
        
    def __init__(self, subs: Any = None) -> None:
        super().__init__(Default.EMPTY, subs, self.key)
    

class Ctry(BaseStructure):
    '''Store, validate and format the CTRY structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Country
    > The name of the country that pertains to the associated address. See
    > `ADDRESS_STRUCTURE` for more details.
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM CTRY Structure](https://gedcom.io/terms/v7/CTRY)
    '''
    
    key: str = 'CTRY'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class DataEvenDate(BaseStructure):
    '''Store, validate and format the DATE structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Date
    > The `DatePeriod` covered by the entire source; the period during which this
    > source recorded events.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/PHRASE          | Many     | No       |
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-Date#period
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM DATE Structure](https://gedcom.io/terms/v7/DATA-EVEN-DATE)
    '''
    
    key: str = 'DATA-EVEN-DATE'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class DataEven(BaseStructure):
    '''Store, validate and format the EVEN structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Event
    > A list of enumerated values from set `https://gedcom.io/terms/v7/enumset-
    > EVENATTR` indicating the types of events that were recorded in a particular
    > source. Each event type is separated by a comma and space. For example, a
    > parish register of births, deaths, and marriages would be `BIRT, DEAT,
    > MARR`.
        
    Enumerations:
    - 'CENS': https://gedcom.io/terms/v7/enum-CENS
        > A census event; either `https://gedcom.io/terms/v7/INDI-CENS` or
        > `https://gedcom.io/terms/v7/FAM-CENS`
    - 'EVEN': https://gedcom.io/terms/v7/enum-EVEN
        > A generic event; either `https://gedcom.io/terms/v7/INDI-EVEN` or
        > `https://gedcom.io/terms/v7/FAM-EVEN`
    - 'FACT': https://gedcom.io/terms/v7/enum-FACT
        > A generic attribute; either `https://gedcom.io/terms/v7/INDI-FACT` or
        > `https://gedcom.io/terms/v7/FAM-FACT`
    - 'NCHI': https://gedcom.io/terms/v7/enum-NCHI
        > A count of children; either `https://gedcom.io/terms/v7/INDI-NCHI` or
        > `https://gedcom.io/terms/v7/FAM-NCHI`
    - 'RESI': https://gedcom.io/terms/v7/enum-RESI
        > A residence attribute; either `https://gedcom.io/terms/v7/INDI-RESI` or
        > `https://gedcom.io/terms/v7/FAM-RESI`
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/DATA-EVEN-DATE  | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-List#Enum
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM EVEN Structure](https://gedcom.io/terms/v7/DATA-EVEN)
    '''
    
    key: str = 'DATA-EVEN'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Data(BaseStructure):
    '''Store, validate and format the DATA structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Data
    > A structure with no payload used to distinguish a description of something
    > from metadata about it. For example, `SOUR` and its other substructures
    > describe a source itself, while `SOUR`.`DATA` describes the content of the
    > source.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/DATA-EVEN       | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
        
    Args:
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM DATA Structure](https://gedcom.io/terms/v7/DATA)
    '''
    
    key: str = 'DATA'
        
    def __init__(self, subs: Any = None) -> None:
        super().__init__(Default.EMPTY, subs, self.key)
    

class DateExact(BaseStructure):
    '''Store, validate and format the DATE structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Date
    > The principal date of the subject of the superstructure. The payload is a
    > `DateExact`.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/TIME            | Many     | No       |
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-Date#exact
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM DATE Structure](https://gedcom.io/terms/v7/DATE-exact)
    '''
    
    key: str = 'DATE-exact'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Date(BaseStructure):
    '''Store, validate and format the DATE structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Date
    > The principal date of the subject of the superstructure. The payload is a
    > `DateValue`.
    > 
    > When the superstructure is an event, the principal date indicates when the
    > event took place.
    > 
    > When the superstructure is an attribute, the principal date indicates when the
    > attribute was observed, asserted, or applied. A date period might put bounds on
    > the attributes applicability, but other date forms assume that the attribute
    > may have also applied on other dates too.
    > 
    > When the superstructure is a `https://gedcom.io/terms/v7/SOUR-DATA`, the
    > principal date indicates when the data was entered into the source; or, for a
    > source like a website that changes over time, a date on which the source
    > contained the data.
    > 
    > See `DATE_VALUE` for more details.
    > 
    > A date, optionally with a time and/or a phrase. If there is a `TIME`, it
    > asserts that the event happened at a specific time on a single day. `TIME`
    > should not be used with `DatePeriod` but may be used with other date types.
    > 
    > <div class="note">
    > 
    > There is currently no provision for approximate times or time phrases. Time
    > phrases are expected to be added in version 7.1.
    > 
    > </div>
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/PHRASE          | Many     | No       |
    | https://gedcom.io/terms/v7/TIME            | Many     | No       |
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-Date
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM DATE Structure](https://gedcom.io/terms/v7/DATE)
    '''
    
    key: str = 'DATE'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Deat(BaseStructure):
    '''Store, validate and format the DEAT structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Death
    > An [Individual Event]. See also `INDIVIDUAL_EVENT_STRUCTURE`.
    > death
    > Mortal life terminates.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM DEAT Structure](https://gedcom.io/terms/v7/DEAT)
    '''
    
    key: str = 'DEAT'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Desi(BaseStructure):
    '''Store, validate and format the DESI structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Descendant Interest
    > Indicates an interest in research to identify additional descendants of
    > this individual. See also `ANCI`.
        
    Args:
        value: A value of data type @<https://gedcom.io/terms/v7/record-SUBM>@
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM DESI Structure](https://gedcom.io/terms/v7/DESI)
    '''
    
    key: str = 'DESI'
        
    def __init__(self, value: SubmitterXref, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Dest(BaseStructure):
    '''Store, validate and format the DEST structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Destination
    > An identifier for the system expected to receive this document. See
    > `HEAD`.`SOUR` for guidance on choosing identifiers.
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM DEST Structure](https://gedcom.io/terms/v7/DEST)
    '''
    
    key: str = 'DEST'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Div(BaseStructure):
    '''Store, validate and format the DIV structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Divorce
    > A [Family Event]. See also `FAMILY_EVENT_STRUCTURE`.
    > divorce
    > Dissolving a marriage through civil action.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/HUSB            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WIFE            | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM DIV Structure](https://gedcom.io/terms/v7/DIV)
    '''
    
    key: str = 'DIV'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Divf(BaseStructure):
    '''Store, validate and format the DIVF structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Divorce filing
    > A [Family Event]. See also `FAMILY_EVENT_STRUCTURE`.
    > divorce filed
    > Filing for a divorce by a spouse.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/HUSB            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WIFE            | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM DIVF Structure](https://gedcom.io/terms/v7/DIVF)
    '''
    
    key: str = 'DIVF'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Dscr(BaseStructure):
    '''Store, validate and format the DSCR structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Description
    > An [Individual Attribute]. See also `INDIVIDUAL_ATTRIBUTE_STRUCTURE`.
    > physical description
    > The physical characteristics of a person.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM DSCR Structure](https://gedcom.io/terms/v7/DSCR)
    '''
    
    key: str = 'DSCR'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Educ(BaseStructure):
    '''Store, validate and format the EDUC structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Education
    > An [Individual Attribute]. See also `INDIVIDUAL_ATTRIBUTE_STRUCTURE`.
    > education
    > Indicator of a level of education attained.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM EDUC Structure](https://gedcom.io/terms/v7/EDUC)
    '''
    
    key: str = 'EDUC'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Email(BaseStructure):
    '''Store, validate and format the EMAIL structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Email
    > An electronic mail address, as defined by any relevant standard such as [RFC
    > 3696], [RFC 5321], or [RFC 5322].
    > 
    > If an invalid email address is present upon import, it should be preserved
    > as-is on export.
    > 
    > <div class="note">
    > 
    > The version 5.5.1 specification contained a typo where this tag was sometimes
    > written `EMAI` and sometimes written `EMAIL`. `EMAIL` should be used in version
    > 7.0 and later.
    > 
    > </div>
    > 
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM EMAIL Structure](https://gedcom.io/terms/v7/EMAIL)
    '''
    
    key: str = 'EMAIL'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Emig(BaseStructure):
    '''Store, validate and format the EMIG structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Emigration
    > An [Individual Event]. See also `INDIVIDUAL_EVENT_STRUCTURE`.
    > emigration
    > Leaving one's homeland with the intent of residing elsewhere.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM EMIG Structure](https://gedcom.io/terms/v7/EMIG)
    '''
    
    key: str = 'EMIG'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Endl(BaseStructure):
    '''Store, validate and format the ENDL structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Endowment, Latter-Day Saint
    > A [Latter-Day Saint Ordinance]. See also `LDS_INDIVIDUAL_ORDINANCE`.
    > endowment
    > A religious event where an endowment ordinance for an individual was
    > performed by priesthood authority in a temple of The Church of Jesus Christ
    > of Latter-day Saints.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TEMP            | Many     | No       |
    | https://gedcom.io/terms/v7/ord-STAT        | Many     | No       |
        
    Args:
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM ENDL Structure](https://gedcom.io/terms/v7/ENDL)
    '''
    
    key: str = 'ENDL'
        
    def __init__(self, subs: Any = None) -> None:
        super().__init__(Default.EMPTY, subs, self.key)
    

class Enga(BaseStructure):
    '''Store, validate and format the ENGA structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Engagement
    > A [Family Event]. See also `FAMILY_EVENT_STRUCTURE`.
    > engagement
    > Recording or announcing an agreement between 2 people to become married.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/HUSB            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WIFE            | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM ENGA Structure](https://gedcom.io/terms/v7/ENGA)
    '''
    
    key: str = 'ENGA'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class ExidType(BaseStructure):
    '''Store, validate and format the TYPE structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Type
    > The authority issuing the `EXID`, represented as a URI. It is recommended that
    > this be a URL.
    > 
    > If the authority maintains stable URLs for each identifier it issues, it is
    > recommended that the `TYPE` payload be selected such that appending the `EXID`
    > payload to it yields that URL. However, this is not required and a different
    > URI for the set of issued identifiers may be used instead.
    > 
    > Registered URIs are listed in the [exid-types registry], where fields are
    > defined using the [YAML file format].
    > 
    > Additional type URIs can be registered by filing a [GitHub pull request].
    > 
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM TYPE Structure](https://gedcom.io/terms/v7/EXID-TYPE)
    '''
    
    key: str = 'EXID-TYPE'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Exid(BaseStructure):
    '''Store, validate and format the EXID structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > External Identifier
    > An identifier for the subject of the superstructure. The identifier is
    > maintained by some external authority; the authority owning the identifier is
    > provided in the TYPE substructure; see `EXID`.`TYPE` for more details.
    > 
    > Depending on the maintaining authority, an `EXID` may be a unique identifier
    > for the subject, an identifier for 1 of several views of the subject, or an
    > identifier for the externally-maintained copy of the same information as is
    > contained in this structure. However, unlike `UID` and `REFN`, `EXID` does not
    > identify a structure; structures with the same `EXID` may have originated
    > independently rather than by edits from the same starting point.
    > 
    > `EXID` identifiers are expected to be unique. Once assigned, an `EXID`
    > identifier should never be re-used for any other purpose.
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/EXID-TYPE       | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM EXID Structure](https://gedcom.io/terms/v7/EXID)
    '''
    
    key: str = 'EXID'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class FamCens(BaseStructure):
    '''Store, validate and format the CENS structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Census
    > An [Family Event].
    > census
    > Periodic count of the population for a designated locality, such as a
    > national or state census.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/HUSB            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WIFE            | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM CENS Structure](https://gedcom.io/terms/v7/FAM-CENS)
    '''
    
    key: str = 'FAM-CENS'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class FamEven(BaseStructure):
    '''Store, validate and format the EVEN structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Event
    > See `https://gedcom.io/terms/v7/INDI-EVEN`.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/HUSB            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WIFE            | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM EVEN Structure](https://gedcom.io/terms/v7/FAM-EVEN)
    '''
    
    key: str = 'FAM-EVEN'
        
    def __init__(self, value: str, subs: Any) -> None:
        super().__init__(value, subs, self.key)
    

class FamFact(BaseStructure):
    '''Store, validate and format the FACT structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Fact
    > See `https://gedcom.io/terms/v7/INDI-FACT`.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/HUSB            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WIFE            | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM FACT Structure](https://gedcom.io/terms/v7/FAM-FACT)
    '''
    
    key: str = 'FAM-FACT'
        
    def __init__(self, value: str, subs: Any) -> None:
        super().__init__(value, subs, self.key)
    

class FamHusb(BaseStructure):
    '''Store, validate and format the HUSB structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Husband
    > This is a partner in a `FAM` record. See `FAMILY_RECORD` for more details.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/PHRASE          | Many     | No       |
        
    Args:
        value: A value of data type @<https://gedcom.io/terms/v7/record-INDI>@
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM HUSB Structure](https://gedcom.io/terms/v7/FAM-HUSB)
    '''
    
    key: str = 'FAM-HUSB'
        
    def __init__(self, value: IndividualXref, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class FamNchi(BaseStructure):
    '''Store, validate and format the NCHI structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Number of children
    > A [Family Attribute]. See also `FAMILY_ATTRIBUTE_STRUCTURE`.
    > number of children
    > The number of children that belong to this family.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/HUSB            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WIFE            | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#nonNegativeInteger
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM NCHI Structure](https://gedcom.io/terms/v7/FAM-NCHI)
    '''
    
    key: str = 'FAM-NCHI'
        
    def __init__(self, value: int, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class FamResi(BaseStructure):
    '''Store, validate and format the RESI structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Residence
    > A [Family Attribute]. See also `FAMILY_ATTRIBUTE_STRUCTURE`.
    > 
    > See `https://gedcom.io/terms/v7/INDI-RESI` for comments on the use of payload
    > strings in `RESI` structures.
    > 
    > residence
    > An address or place of residence where a family resided.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/HUSB            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WIFE            | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM RESI Structure](https://gedcom.io/terms/v7/FAM-RESI)
    '''
    
    key: str = 'FAM-RESI'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class FamWife(BaseStructure):
    '''Store, validate and format the WIFE structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Wife
    > A partner in a `FAM` record. See `FAMILY_RECORD` for more details.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/PHRASE          | Many     | No       |
        
    Args:
        value: A value of data type @<https://gedcom.io/terms/v7/record-INDI>@
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM WIFE Structure](https://gedcom.io/terms/v7/FAM-WIFE)
    '''
    
    key: str = 'FAM-WIFE'
        
    def __init__(self, value: IndividualXref, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class FamcAdop(BaseStructure):
    '''Store, validate and format the ADOP structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Adoption
    > An enumerated value from set `https://gedcom.io/terms/v7/enumset-ADOP`
    > indicating which parent(s) in the family adopted this individual.
        
    Enumerations:
    - 'HUSB': https://gedcom.io/terms/v7/enum-ADOP-HUSB
        > Adopted by the `HUSB` of the `FAM` pointed to by `FAMC`.
    - 'WIFE': https://gedcom.io/terms/v7/enum-ADOP-WIFE
        > Adopted by the `WIFE` of the `FAM` pointed to by `FAMC`.
    - 'BOTH': https://gedcom.io/terms/v7/enum-BOTH
        > Adopted by both `HUSB` and `WIFE` of the `FAM` pointed to by `FAMC`
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/PHRASE          | Many     | No       |
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-Enum
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM ADOP Structure](https://gedcom.io/terms/v7/FAMC-ADOP)
    '''
    
    key: str = 'FAMC-ADOP'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class FamcStat(BaseStructure):
    '''Store, validate and format the STAT structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Status
    > An enumerated value from set `https://gedcom.io/terms/v7/enumset-FAMC-STAT`
    > assessing of the state or condition of a researcher's belief in a family
    > connection.
        
    Enumerations:
    - 'CHALLENGED': https://gedcom.io/terms/v7/enum-CHALLENGED
        > Linking this child to this family is suspect, but the linkage has been
        > neither proven nor disproven.
    - 'DISPROVEN': https://gedcom.io/terms/v7/enum-DISPROVEN
        > There has been a claim by some that this child belongs to this family, but
        > the linkage has been disproven.
    - 'PROVEN': https://gedcom.io/terms/v7/enum-PROVEN
        > Linking this child to this family has been proven.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/PHRASE          | Many     | No       |
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-Enum
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM STAT Structure](https://gedcom.io/terms/v7/FAMC-STAT)
    '''
    
    key: str = 'FAMC-STAT'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Famc(BaseStructure):
    '''Store, validate and format the FAMC structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Family child
    > The family with which this individual event is associated.
        
    Args:
        value: A value of data type @<https://gedcom.io/terms/v7/record-FAM>@
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM FAMC Structure](https://gedcom.io/terms/v7/FAMC)
    '''
    
    key: str = 'FAMC'
        
    def __init__(self, value: FamilyXref, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Fams(BaseStructure):
    '''Store, validate and format the FAMS structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Family spouse
    > The family in which an individual appears as a partner. See `FAMILY_RECORD`
    > for more details.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
        
    Args:
        value: A value of data type @<https://gedcom.io/terms/v7/record-FAM>@
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM FAMS Structure](https://gedcom.io/terms/v7/FAMS)
    '''
    
    key: str = 'FAMS'
        
    def __init__(self, value: FamilyXref, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Fax(BaseStructure):
    '''Store, validate and format the FAX structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Facsimile
    > A fax telephone number appropriate for sending data facsimiles. See `PHON`
    > for additional comments on telephone numbers.
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM FAX Structure](https://gedcom.io/terms/v7/FAX)
    '''
    
    key: str = 'FAX'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Fcom(BaseStructure):
    '''Store, validate and format the FCOM structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > First communion
    > An [Individual Event]. See also `INDIVIDUAL_EVENT_STRUCTURE`.
    > first communion
    > The first act of sharing in the Lord's supper as part of church worship.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM FCOM Structure](https://gedcom.io/terms/v7/FCOM)
    '''
    
    key: str = 'FCOM'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class FileTran(BaseStructure):
    '''Store, validate and format the TRAN structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Translation
    > A type of `TRAN` for external media files. Each
    > `https://gedcom.io/terms/v7/NOTE-TRAN` must have a `FORM` substructure. See
    > also `FILE` and the [File Path datatype].
    > 
    > <div class="example">
    > 
    > If an mp3 audio file has been transcoded as an ogg file and a timestamped
    > transcript has been extracted as a WebVTT file, the resulting set of files
    > might be presented as follows:
    > 
    > ```gedcom
    > 0 @EX@ OBJE
    > 1 FILE media/original.mp3
    > 2 FORM audio/mp3
    > 2 TRAN media/derived.oga
    > 3 FORM audio/ogg
    > 2 TRAN media/transcript.vtt
    > 3 FORM text/vtt
    > ```
    > 
    > </div>
    > 
    > Note that `FILE`.`TRAN` refers to translation to a different digital format,
    > not to translation to a different human language. Files that differ in the
    > human language of their content should each be given their own `FILE`
    > structure.
    > 
    > A representation of the superstructure's data in a different format.
    > 
    > In some situations it is desirable to provide the same semantic content in
    > multiple formats. Where this is desirable, a `TRAN` substructure is used, where
    > the specific format is given in its language tag substructure, media type
    > substructure, or both.
    > 
    > Different `TRAN` structures are used in different contexts to fully capture the
    > structure of the information being presented in multiple formats. In all cases,
    > a `TRAN` structure's payload and substructures should provide only information
    > also contained in the `TRAN` structures' superstructure, but provide it in a
    > new language, script, or media type.
    > 
    > Each `TRAN` substructure must have either a language tag or a media type or
    > both. Each `TRAN` structure must differ from its superstructure and from every
    > other `TRAN` substructure of its superstructure in either its language tag or
    > its media type or both.
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/FORM            | Many     | No       |
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-FilePath
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM TRAN Structure](https://gedcom.io/terms/v7/FILE-TRAN)
    '''
    
    key: str = 'FILE-TRAN'
        
    def __init__(self, value: str, subs: Any) -> None:
        super().__init__(value, subs, self.key)
    

class File(BaseStructure):
    '''Store, validate and format the FILE structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > File reference
    > A reference to an external file. See the [File Path datatype] for more details.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/FILE-TRAN       | Many     | No       |
    | https://gedcom.io/terms/v7/FORM            | Many     | No       |
    | https://gedcom.io/terms/v7/TITL            | Many     | No       |
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-FilePath
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM FILE Structure](https://gedcom.io/terms/v7/FILE)
    '''
    
    key: str = 'FILE'
        
    def __init__(self, value: str, subs: Any) -> None:
        super().__init__(value, subs, self.key)
    

class Form(BaseStructure):
    '''Store, validate and format the FORM structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Format
    > The [media type] of the file referenced by the superstructure.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/MEDI            | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/ns/dcat#mediaType
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM FORM Structure](https://gedcom.io/terms/v7/FORM)
    '''
    
    key: str = 'FORM'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class GedcVers(BaseStructure):
    '''Store, validate and format the VERS structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Version
    > The version number of the official specification that this document's data
    > conforms to. This must include the major and minor version (for example,
    > "`7.0`"); it may include the patch as well (for example, "`7.0.1`"), but
    > doing so is not required. See [A Guide to Version Numbers] for more details
    > about version numbers.
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM VERS Structure](https://gedcom.io/terms/v7/GEDC-VERS)
    '''
    
    key: str = 'GEDC-VERS'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Gedc(BaseStructure):
    '''Store, validate and format the GEDC structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > GEDCOM
    > A container for information about the entire document.
    > 
    > It is recommended that applications write `GEDC` with its required substructure
    > `https://gedcom.io/terms/v7/GEDC-VERS` as the first substructure of `HEAD`.
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/GEDC-VERS       | Many     | No       |
        
    Args:
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM GEDC Structure](https://gedcom.io/terms/v7/GEDC)
    '''
    
    key: str = 'GEDC'
        
    def __init__(self, subs: Any) -> None:
        super().__init__(Default.EMPTY, subs, self.key)
    

class Givn(BaseStructure):
    '''Store, validate and format the GIVN structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Given name
    > A given or earned name used for official identification of a person.
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM GIVN Structure](https://gedcom.io/terms/v7/GIVN)
    '''
    
    key: str = 'GIVN'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Grad(BaseStructure):
    '''Store, validate and format the GRAD structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Graduation
    > An [Individual Event]. See also `INDIVIDUAL_EVENT_STRUCTURE`.
    > graduation
    > Awarding educational diplomas or degrees to individuals.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM GRAD Structure](https://gedcom.io/terms/v7/GRAD)
    '''
    
    key: str = 'GRAD'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class HeadDate(BaseStructure):
    '''Store, validate and format the DATE structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Date
    > The `DateExact` that this document was created.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/TIME            | Many     | No       |
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-Date#exact
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM DATE Structure](https://gedcom.io/terms/v7/HEAD-DATE)
    '''
    
    key: str = 'HEAD-DATE'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class HeadLang(BaseStructure):
    '''Store, validate and format the LANG structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Language
    > A default language which may be used to interpret any `Text`-typed payloads
    > that lack a specific language tag from a `https://gedcom.io/terms/v7/LANG`
    > structure. An application may choose to use a different default based on its
    > knowledge of the language preferences of the user.
    > 
    > The payload of the `LANG` structure is a language tag, as defined by [BCP 47].
    > 
    > <div class="note">
    > 
    > Some algorithms on text are language-specific. Examples include sorting
    > sequences, name comparison and phonetic name matching algorithms,
    > spell-checking, computer-synthesized speech, Braille transcription, and
    > language translation. When the language of the text is given through a
    > `https://gedcom.io/terms/v7/LANG`, that should be used. When
    > `https://gedcom.io/terms/v7/LANG` is not available,
    > `https://gedcom.io/terms/v7/HEAD-LANG` provides the file creator's suggested
    > default language. For some language-specific algorithms, the user's preferred
    > language may be a more appropriate default than the file's default language.
    > User language preferences can be found in a variety of platform-specific
    > places, such as the default language from operating system settings, user
    > locales, Input Method Editors (IMEs), etc.
    > 
    > </div>
    > 
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#Language
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM LANG Structure](https://gedcom.io/terms/v7/HEAD-LANG)
    '''
    
    key: str = 'HEAD-LANG'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class HeadPlacForm(BaseStructure):
    '''Store, validate and format the FORM structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Format
    > Any `PLAC` with no [`FORM`] shall be treated as if it has this [`FORM`].
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-List#Text
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM FORM Structure](https://gedcom.io/terms/v7/HEAD-PLAC-FORM)
    '''
    
    key: str = 'HEAD-PLAC-FORM'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class HeadPlac(BaseStructure):
    '''Store, validate and format the PLAC structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Place
    > This is a placeholder for providing a default `PLAC`.`FORM`, and must not
    > have a payload.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/HEAD-PLAC-FORM  | Many     | No       |
        
    Args:
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM PLAC Structure](https://gedcom.io/terms/v7/HEAD-PLAC)
    '''
    
    key: str = 'HEAD-PLAC'
        
    def __init__(self, subs: Any) -> None:
        super().__init__(Default.EMPTY, subs, self.key)
    

class HeadSourData(BaseStructure):
    '''Store, validate and format the DATA structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Data
    > The database, electronic data source, or digital repository from which this
    > dataset was exported. The payload is the name of the database, electronic
    > data source, or digital repository, with substructures providing additional
    > details about it (not about the export).
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/COPR            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE-exact      | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM DATA Structure](https://gedcom.io/terms/v7/HEAD-SOUR-DATA)
    '''
    
    key: str = 'HEAD-SOUR-DATA'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Head(BaseStructure):
    '''Store, validate and format the HEAD structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Header
    > A pseudo-structure for storing metadata about the document. See [The Header
    > and Trailer] for more details.
    > The header pseudo-structure provides metadata about the entire dataset. A few
    > substructures of note:
    > 
    > - `GEDC` identifies the specification that this document conforms to. It is
    >   recommended that `GEDC` be the first substructure of the header.
    > - `SCHMA` gives the meaning of extension tags; see [Extensions] for more
    >   details.
    > - `SOUR` describes the originating software.
    >   - `CORP` describes the corporation creating the software.
    >   - `HEAD`.`SOUR`.`DATA` describes a larger database, electronic data source,
    >     or digital repository this data is extracted from.
    > - `LANG` and `PLAC` give a default value for the rest of the document.
    > 
    > <div class="deprecation">
    > 
    > `HEAD`.`SOUR`.`DATA` is now deprecated and applications should use
    > `HEAD`.`SOUR`.`NAME` instead.
    > 
    > </div>
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/COPR            | Many     | No       |
    | https://gedcom.io/terms/v7/DEST            | Many     | No       |
    | https://gedcom.io/terms/v7/GEDC            | Many     | No       |
    | https://gedcom.io/terms/v7/HEAD-DATE       | Many     | No       |
    | https://gedcom.io/terms/v7/HEAD-LANG       | Many     | No       |
    | https://gedcom.io/terms/v7/HEAD-PLAC       | Many     | No       |
    | https://gedcom.io/terms/v7/HEAD-SOUR       | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/SCHMA           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SUBM            | Many     | No       |
        
    Args:
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM HEAD Structure](https://gedcom.io/terms/v7/HEAD)
    '''
    
    key: str = 'HEAD'
        
    def __init__(self, subs: Any) -> None:
        super().__init__(Default.EMPTY, subs, self.key)
    

class Height(BaseStructure):
    '''Store, validate and format the HEIGHT structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Height in pixels
    > How many pixels to display vertically for the image. See `CROP` for more
    > details.
    > 
    > <div class="note">
    > 
    > `HEIGHT` is a number of pixels. The correct tag for the height of an individual
    > is the `DSCR` attribute.
    > 
    > <div class="example">
    > 
    > ```gedcom
    > 0 @I45@ INDI
    > 1 DSCR brown eyes, 5ft 10in, 198 pounds
    > ```
    > 
    > </div>
    > 
    > </div>
    > 
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#nonNegativeInteger
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM HEIGHT Structure](https://gedcom.io/terms/v7/HEIGHT)
    '''
    
    key: str = 'HEIGHT'
        
    def __init__(self, value: int, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Husb(BaseStructure):
    '''Store, validate and format the HUSB structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Husband
    > A container for information relevant to the subject of the superstructure
    > specific to the individual described by the associated `FAM`'s `HUSB`
    > substructure.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
        
    Args:
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM HUSB Structure](https://gedcom.io/terms/v7/HUSB)
    '''
    
    key: str = 'HUSB'
        
    def __init__(self, subs: Any) -> None:
        super().__init__(Default.EMPTY, subs, self.key)
    

class Idno(BaseStructure):
    '''Store, validate and format the IDNO structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Identification number
    > An [Individual Attribute]. See also `INDIVIDUAL_ATTRIBUTE_STRUCTURE`.
    > identifying number
    > A number or other string assigned to identify a person within some
    > significant external system. It must have a `TYPE` substructure to define
    > what kind of identification number is being provided.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM IDNO Structure](https://gedcom.io/terms/v7/IDNO)
    '''
    
    key: str = 'IDNO'
        
    def __init__(self, value: str, subs: Any) -> None:
        super().__init__(value, subs, self.key)
    

class Immi(BaseStructure):
    '''Store, validate and format the IMMI structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Immigration
    > An [Individual Event]. See also `INDIVIDUAL_EVENT_STRUCTURE`.
    > immigration
    > Entering into a new locality with the intent of residing there.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM IMMI Structure](https://gedcom.io/terms/v7/IMMI)
    '''
    
    key: str = 'IMMI'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class IndiCens(BaseStructure):
    '''Store, validate and format the CENS structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Census
    > An [Individual Event]. See also `INDIVIDUAL_EVENT_STRUCTURE`.
    > census
    > Periodic count of the population for a designated locality, such as a
    > national or state census.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM CENS Structure](https://gedcom.io/terms/v7/INDI-CENS)
    '''
    
    key: str = 'INDI-CENS'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class IndiEven(BaseStructure):
    '''Store, validate and format the EVEN structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Event
    > An event: a noteworthy happening related to an individual or family. If a
    > specific event type exists, it should be used instead of a generic `EVEN`
    > structure. Each `EVEN` must be classified by a subordinate use of the `TYPE`
    > tag and may be further described in the structure's payload.
    > 
    > <div class="example">
    > 
    > A person that signed a lease for land dated October 2, 1837 and a lease for
    > mining equipment dated November 4, 1837 would be written as:
    > 
    > ```gedcom
    > 0 @I1@ INDI
    > 1 EVEN
    > 2 TYPE Land Lease
    > 2 DATE 2 OCT 1837
    > 1 EVEN Mining equipment
    > 2 TYPE Equipment Lease
    > 2 DATE 4 NOV 1837
    > ```
    > 
    > </div>
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM EVEN Structure](https://gedcom.io/terms/v7/INDI-EVEN)
    '''
    
    key: str = 'INDI-EVEN'
        
    def __init__(self, value: str, subs: Any) -> None:
        super().__init__(value, subs, self.key)
    

class IndiFact(BaseStructure):
    '''Store, validate and format the FACT structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Fact
    > A noteworthy attribute or fact concerning an individual or family. If a
    > specific attribute type exists, it should be used instead of a generic `FACT`
    > structure. Each `FACT` must be classified by a subordinate use of the `TYPE`
    > tag and may be further described in the structure's payload.
    > 
    > <div class="example">
    > 
    > If the attribute being defined was 1 of the person's skills, such as
    > woodworking, the `FACT` tag would have the value of "Woodworking", followed by
    > a subordinate `TYPE` tag with the value "Skills".
    > 
    > ```gedcom
    > 0 @I1@ INDI
    > 1 FACT Woodworking
    > 2 TYPE Skills
    > ```
    > 
    > </div>
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM FACT Structure](https://gedcom.io/terms/v7/INDI-FACT)
    '''
    
    key: str = 'INDI-FACT'
        
    def __init__(self, value: str, subs: Any) -> None:
        super().__init__(value, subs, self.key)
    

class IndiFamc(BaseStructure):
    '''Store, validate and format the FAMC structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Family child
    > The family in which an individual appears as a child. It is also used with
    > a `https://gedcom.io/terms/v7/FAMC-STAT` substructure to show individuals
    > who are not children of the family. See `FAMILY_RECORD` for more details.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/FAMC-STAT       | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/PEDI            | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
        
    Args:
        value: A value of data type @<https://gedcom.io/terms/v7/record-FAM>@
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM FAMC Structure](https://gedcom.io/terms/v7/INDI-FAMC)
    '''
    
    key: str = 'INDI-FAMC'
        
    def __init__(self, value: FamilyXref, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class IndiName(BaseStructure):
    '''Store, validate and format the NAME structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Name
    > A `PERSONAL_NAME_STRUCTURE` with parts, translations, sources, and so forth.
    > Names of individuals are represented in the manner the name is normally spoken,
    > with the family name, surname, or nearest cultural parallel thereunto separated
    > by slashes (U+002F `/`). Based on the dynamic nature or unknown compositions of
    > naming conventions, it is difficult to provide a more detailed name piece
    > structure to handle every case. The `PERSONAL_NAME_PIECES` are provided
    > optionally for systems that cannot operate effectively with less structured
    > information. The Personal Name payload shall be seen as the primary name
    > representation, with name pieces as optional auxiliary information; in
    > particular it is recommended that all name parts in `PERSONAL_NAME_PIECES`
    > appear within the `PersonalName` payload in some form, possibly adjusted for
    > gender-specific suffixes or the like. It is permitted for the payload to
    > contain information not present in any name piece substructure.
    > 
    > The name may be translated or transliterated into different languages or
    > scripts using the `TRAN` substructure. It is recommended, but not required,
    > that if the name pieces are used, the same pieces are used in each translation
    > and transliteration.
    > 
    > A `TYPE` is used to specify the particular variation that this name is. For
    > example; it could indicate that this name is a name taken at immigration or
    > that it could be an ‘also known as’ name. See
    > `https://gedcom.io/terms/v7/enumset-NAME-TYPE` for more details.
    > 
    > <div class="note">
    > 
    > Alternative approaches to representing names are being considered for future
    > versions of this specification.
    > 
    > </div>
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/GIVN            | Many     | No       |
    | https://gedcom.io/terms/v7/NAME-TRAN       | Many     | No       |
    | https://gedcom.io/terms/v7/NAME-TYPE       | Many     | No       |
    | https://gedcom.io/terms/v7/NICK            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/NPFX            | Many     | No       |
    | https://gedcom.io/terms/v7/NSFX            | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/SPFX            | Many     | No       |
    | https://gedcom.io/terms/v7/SURN            | Many     | No       |
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-Name
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM NAME Structure](https://gedcom.io/terms/v7/INDI-NAME)
    '''
    
    key: str = 'INDI-NAME'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class IndiNchi(BaseStructure):
    '''Store, validate and format the NCHI structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Number of children
    > An [Individual Attribute]. See also `INDIVIDUAL_ATTRIBUTE_STRUCTURE`.
    > number of children
    > The number of children that this person is known to be the parent of (all
    > marriages).
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#nonNegativeInteger
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM NCHI Structure](https://gedcom.io/terms/v7/INDI-NCHI)
    '''
    
    key: str = 'INDI-NCHI'
        
    def __init__(self, value: int, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class IndiReli(BaseStructure):
    '''Store, validate and format the RELI structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Religion
    > An [Individual Attribute]. See also `INDIVIDUAL_ATTRIBUTE_STRUCTURE`.
    > religion
    > A religious denomination to which a person is affiliated or for which a
    > record applies.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM RELI Structure](https://gedcom.io/terms/v7/INDI-RELI)
    '''
    
    key: str = 'INDI-RELI'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class IndiTitl(BaseStructure):
    '''Store, validate and format the TITL structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Title
    > An [Individual Attribute]. See also `INDIVIDUAL_ATTRIBUTE_STRUCTURE`.
    > title
    > A formal designation used by an individual in connection with positions of
    > royalty or other social status, such as Grand Duke.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM TITL Structure](https://gedcom.io/terms/v7/INDI-TITL)
    '''
    
    key: str = 'INDI-TITL'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Inil(BaseStructure):
    '''Store, validate and format the INIL structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Initiatory, Latter-Day Saint
    > A [Latter-Day Saint Ordinance]. See also `LDS_INDIVIDUAL_ORDINANCE`.
    > Previously, GEDCOM versions 3.0 through 5.3 called this `WAC`; it was not
    > part of 5.4 through 5.5.1. FamilySearch GEDCOM 7.0 reintroduced it with the
    > name `INIL` for consistency with `BAPL`, `CONL`, and `ENDL`.
    > initiatory
    > A religious event where an initiatory ordinance for an individual was
    > performed by priesthood authority in a temple of The Church of Jesus Christ
    > of Latter-day Saints.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TEMP            | Many     | No       |
    | https://gedcom.io/terms/v7/ord-STAT        | Many     | No       |
        
    Args:
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM INIL Structure](https://gedcom.io/terms/v7/INIL)
    '''
    
    key: str = 'INIL'
        
    def __init__(self, subs: Any = None) -> None:
        super().__init__(Default.EMPTY, subs, self.key)
    

class Lang(BaseStructure):
    '''Store, validate and format the LANG structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Language
    > The primary human language of the superstructure. The primary language in which
    > the `Text`-typed payloads of the superstructure and its substructures appear.
    > 
    > The payload of the `LANG` structure is a language tag, as defined by [BCP 47].
    > A [registry of component subtags] is maintained publicly by the IANA.
    > 
    > In the absence of a `LANG` structure, the language is assumed to be
    > unspecified; that may also be recorded explicitly with language tag `und`
    > (meaning "undetermined"). See `https://gedcom.io/terms/v7/HEAD-LANG` for
    > information about applying language-specific algorithms to text in an
    > unspecified language.
    > 
    > If the text is primarily in one language with a few parts in a different
    > language, it is recommended that a language tag identifying the primary
    > language be used. If no one language is primary, the language tag `mul`
    > (meaning "multiple") may be used, but most language-specific algorithms will
    > treat `mul` the same way they do `und`.
    > 
    > <div class="note">
    > 
    > Conversations are ongoing about adding part-of-payload language tagging in a
    > future version of the specification to provide more fidelity for multilingual
    > text.
    > 
    > </div>
    > 
    > If the text is not in any human language and should not be treated as lingual
    > content, the language tag `zxx` (meaning "no linguistic content" or "not
    > applicable") may be used. An example of `zxx` text might be a diagram
    > approximated using characters for their shape, not their meaning.
    > 
    > <div class="note">
    > 
    > This specification does not permit `LANG` in every place where human language
    > text might appear. Conversations are ongoing about adding it in more places in
    > a future version of the specification. Using the current specification,
    > additional language tagging can be accomplished using a [documented extension
    > tag] by including the following in the header:
    > 
    > ```gedcom
    > 1 SCHEMA
    > 2 TAG _LANG https://gedcom.io/terms/v7/LANG
    > ```
    > 
    > and using the extension tag like so:
    > 
    > ```gedcom
    > 2 DATE 31 AUG 2018
    > 3 PHRASE 2018年8月31日
    > 4 _LANG cmn
    > ```
    > 
    > </div>
    > 
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#Language
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM LANG Structure](https://gedcom.io/terms/v7/LANG)
    '''
    
    key: str = 'LANG'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Lati(BaseStructure):
    '''Store, validate and format the LATI structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Latitude
    > A latitudinal coordinate. The payload is either `N` (for a coordinate north of
    > the equator) or `S` (for a coordinate south of the equator) followed by a
    > decimal number of degrees. Minutes and seconds are not used and should be
    > converted to fractional degrees prior to encoding.
    > 
    > <div class="example">
    > 
    > 18 degrees, 9 minutes, and 3.4 seconds North would be formatted as
    > `N18.150944`.
    > 
    > </div>
    > 

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
        >>> from genedata.structure import Input
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
        <BLANKLINE>
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM LATI Structure](https://gedcom.io/terms/v7/LATI)
    '''
    
    key: str = 'LATI'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Left(BaseStructure):
    '''Store, validate and format the LEFT structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Left crop width
    > Left is a number of pixels to not display from the left side of the image.
    > See `CROP` for more details.
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#nonNegativeInteger
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM LEFT Structure](https://gedcom.io/terms/v7/LEFT)
    '''
    
    key: str = 'LEFT'
        
    def __init__(self, value: int, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Long(BaseStructure):
    '''Store, validate and format the LONG structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Longitude
    > A longitudinal coordinate. The payload is either `E` (for a coordinate east of
    > the prime meridian) or `W` (for a coordinate west of the prime meridian)
    > followed by a decimal number of degrees. Minutes and seconds are not used and
    > should be converted to fractional degrees prior to encoding.
    > 
    > <div class="example">
    > 
    > 168 degrees, 9 minutes, and 3.4 seconds East would be formatted as
    > `E168.150944`.
    > 
    > </div>
    > 

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
        >>> from genedata.structure import Input
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
        <BLANKLINE>
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM LONG Structure](https://gedcom.io/terms/v7/LONG)
    '''
    
    key: str = 'LONG'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Map(BaseStructure):
    '''Store, validate and format the MAP structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Map
    > A representative point for a location, as defined by `LATI` and `LONG`
    > substructures.
    > 
    > Note that `MAP` provides neither a notion of accuracy (for example, the `MAP`
    > for a birth event may be some distance from the point where the birth occurred)
    > nor a notion of region size (for example, the `MAP` for a place "Belarus" may
    > be anywhere within that nation's 200,000 square kilometer area).
    > 

    Examples:
        The following example illustrates how to enter latitude (Lati) and longitude (Long)
        coordinates into a map structure to produce the GEDCOM output.
        >>> from genedata.structure import Input, Lati, Long, Map
        >>> m = Map([Lati('N18.150944'), Long('E168.150944')])
        >>> print(m.ged())
        1 MAP
        2 LATI N18.150944
        2 LONG E168.150944
        <BLANKLINE>
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/LATI            | Many     | No       |
    | https://gedcom.io/terms/v7/LONG            | Many     | No       |
        
    Args:
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM MAP Structure](https://gedcom.io/terms/v7/MAP)
    '''
    
    key: str = 'MAP'
        
    def __init__(self, subs: Any) -> None:
        super().__init__(Default.EMPTY, subs, self.key)
    

class Marb(BaseStructure):
    '''Store, validate and format the MARB structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Marriage banns
    > A [Family Event]. See also `FAMILY_EVENT_STRUCTURE`.
    > marriage bann
    > Official public notice given that 2 people intend to marry.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/HUSB            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WIFE            | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM MARB Structure](https://gedcom.io/terms/v7/MARB)
    '''
    
    key: str = 'MARB'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Marc(BaseStructure):
    '''Store, validate and format the MARC structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Marriage contract
    > A [Family Event]. See also `FAMILY_EVENT_STRUCTURE`.
    > marriage contract
    > Recording a formal agreement of marriage, including the prenuptial
    > agreement in which marriage partners reach agreement about the property
    > rights of 1 or both, securing property to their children.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/HUSB            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WIFE            | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM MARC Structure](https://gedcom.io/terms/v7/MARC)
    '''
    
    key: str = 'MARC'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Marl(BaseStructure):
    '''Store, validate and format the MARL structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Marriage license
    > A [Family Event]. See also `FAMILY_EVENT_STRUCTURE`.
    > marriage license
    > Obtaining a legal license to marry.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/HUSB            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WIFE            | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM MARL Structure](https://gedcom.io/terms/v7/MARL)
    '''
    
    key: str = 'MARL'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Marr(BaseStructure):
    '''Store, validate and format the MARR structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Marriage
    > A [Family Event]. See also `FAMILY_EVENT_STRUCTURE`.
    > marriage
    > A legal, common-law, or customary event such as a wedding or marriage
    > ceremony that joins 2 partners to create or extend a family unit.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/HUSB            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WIFE            | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM MARR Structure](https://gedcom.io/terms/v7/MARR)
    '''
    
    key: str = 'MARR'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Mars(BaseStructure):
    '''Store, validate and format the MARS structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Marriage settlement
    > A [Family Event]. See also `FAMILY_EVENT_STRUCTURE`.
    > marriage settlement
    > Creating an agreement between 2 people contemplating marriage, at which
    > time they agree to release or modify property rights that would otherwise
    > arise from the marriage.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/HUSB            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WIFE            | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM MARS Structure](https://gedcom.io/terms/v7/MARS)
    '''
    
    key: str = 'MARS'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Medi(BaseStructure):
    '''Store, validate and format the MEDI structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Medium
    > An enumerated value from set `https://gedcom.io/terms/v7/enumset-MEDI`
    > providing information about the media or the medium in which information is
    > stored.
    > 
    > When `MEDI` is a substructure of a `https://gedcom.io/terms/v7/CALN`, it is
    > recommended that its payload describes the medium directly found at that call
    > number rather than a medium from which it was derived.
    > 
    > <div class="example">
    > 
    > Consider an asset in a repository that is a digital scan of a book of compiled
    > newspapers; for this asset, the `CALN`.`MEDI` is recommended to be `ELECTRONIC`
    > rather than `BOOK` or `NEWSPAPER`.
    > 
    > </div>
    > 
    > When `MEDI` is a substructure of a `https://gedcom.io/terms/v7/FORM`, it is
    > recommended that its payload describes the medium from which it was derived.
    > 
    > <div class="example">
    > 
    > Consider a digital photo in a multimedia record; for this asset, the
    > `FORM`.`MEDI` is recommended to be `PHOTO` rather than `ELECTRONIC`.
    > 
    > </div>
    > 

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
        Medi('AUDIO')
        
    Enumerations:
    - 'AUDIO': https://gedcom.io/terms/v7/enum-AUDIO
        > An audio recording
    - 'BOOK': https://gedcom.io/terms/v7/enum-BOOK
        > A bound book
    - 'CARD': https://gedcom.io/terms/v7/enum-CARD
        > A card or file entry
    - 'ELECTRONIC': https://gedcom.io/terms/v7/enum-ELECTRONIC
        > A digital artifact
    - 'FICHE': https://gedcom.io/terms/v7/enum-FICHE
        > Microfiche
    - 'FILM': https://gedcom.io/terms/v7/enum-FILM
        > Microfilm
    - 'MAGAZINE': https://gedcom.io/terms/v7/enum-MAGAZINE
        > Printed periodical
    - 'MANUSCRIPT': https://gedcom.io/terms/v7/enum-MANUSCRIPT
        > Written pages
    - 'MAP': https://gedcom.io/terms/v7/enum-MAP
        > Cartographic map
    - 'NEWSPAPER': https://gedcom.io/terms/v7/enum-NEWSPAPER
        > Printed newspaper
    - 'OTHER': https://gedcom.io/terms/v7/enum-OTHER
        > A value not listed here; should have a `PHRASE` substructure
    - 'PHOTO': https://gedcom.io/terms/v7/enum-PHOTO
        > Photograph
    - 'TOMBSTONE': https://gedcom.io/terms/v7/enum-TOMBSTONE
        > Burial marker or related memorial
    - 'VIDEO': https://gedcom.io/terms/v7/enum-VIDEO
        > Motion picture recording
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/PHRASE          | Many     | No       |
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-Enum
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM MEDI Structure](https://gedcom.io/terms/v7/MEDI)
    '''
    
    key: str = 'MEDI'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Mime(BaseStructure):
    '''Store, validate and format the MIME structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Media type
    > Indicates the [media type] of the payload of the superstructure.
    > 
    > As of version 7.0, only 2 media types are supported by this structure:
    > 
    > - `text/plain` shall be presented to the user as-is, preserving all spacing,
    >   line breaks, and so forth.
    > 
    > - `text/html` uses HTML tags to provide presentation information. Applications
    >   should support at least the following:
    > 
    >   - `p` and `br` elements for paragraphing and line breaks.
    >   - `b`, `i`, `u`, and `s` elements for bold, italic, underlined, and
    >     strike-through text (or corresponding display in other locales; see [HTML
    >     §4.5] for more).
    >   - `sup` and `sub` elements for super- and sub-script.
    >   - The 3 XML entities that appear in text: `&amp;`, `&lt;` `&gt;`. Note that
    >     `&quote;` and `&apos;` are only needed in attributes. Other entities should
    >     be represented as their respective Unicode characters instead.
    > 
    >   Supporting more of HTML is encouraged. Unsupported tags should be ignored
    >   during display.
    > 
    > <div class="note">
    > 
    > Applications are welcome to support more XML entities or HTML character
    > references in their user interface. However, exporting must only use the core
    > XML entities, translating any other entities into their corresponding Unicode
    > characters.
    > 
    > </div>
    > 
    > <div class="note">
    > 
    > Applications are welcome to support additional HTML elements, but they should
    > ensure that content is meaningful if those extra elements are ignored and only
    > their content text is displayed.
    > 
    > </div>
    > 
    > <div class="note">
    > 
    > Media types are also used by external files, as described under `FORM`.
    > External file media types are not limited to `text/plain` and `text/html`.
    > 
    > </div>
    > 
    > If needed, `text/html` can be converted to `text/plain` using the following
    > steps:
    > 
    > 1. Replace any sequence of 1 or more spaces, tabs, and line breaks with a
    >    single space
    > 2. Case-insensitively replace each `<p`...`>`, `</p`...`>`, and `<br`...`>`
    >    with a line break
    > 3. Remove all other `<`...`>` tags
    > 4. Replace each `&lt;` with `<` and `&gt;` with `>`
    > 5. Replace each `&amp;` with `&`
    > 
        
    Args:
        value: A value of data type http://www.w3.org/ns/dcat#mediaType
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM MIME Structure](https://gedcom.io/terms/v7/MIME)
    '''
    
    key: str = 'MIME'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class NameTran(BaseStructure):
    '''Store, validate and format the TRAN structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Translation
    > A type of `TRAN` substructure specific to [Personal Names]. Each `NAME`.`TRAN`
    > must have a `LANG` substructure. See also `INDI`.`NAME`.
    > 
    > <div class="example">
    > 
    > The following presents a name in Mandarin, transliterated using Pinyin
    > 
    > ```gedcom
    > 1 NAME /孔/德庸
    > 2 GIVN 德庸
    > 2 SURN 孔
    > 2 TRAN /Kǒng/ Déyōng
    > 3 GIVN Déyōng
    > 3 SURN Kǒng
    > 3 LANG zh-pinyin
    > ```
    > 
    > </div>
    > 
    > A representation of the superstructure's data in a different format.
    > 
    > In some situations it is desirable to provide the same semantic content in
    > multiple formats. Where this is desirable, a `TRAN` substructure is used, where
    > the specific format is given in its language tag substructure, media type
    > substructure, or both.
    > 
    > Different `TRAN` structures are used in different contexts to fully capture the
    > structure of the information being presented in multiple formats. In all cases,
    > a `TRAN` structure's payload and substructures should provide only information
    > also contained in the `TRAN` structures' superstructure, but provide it in a
    > new language, script, or media type.
    > 
    > Each `TRAN` substructure must have either a language tag or a media type or
    > both. Each `TRAN` structure must differ from its superstructure and from every
    > other `TRAN` substructure of its superstructure in either its language tag or
    > its media type or both.
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/GIVN            | Many     | No       |
    | https://gedcom.io/terms/v7/LANG            | Many     | No       |
    | https://gedcom.io/terms/v7/NICK            | Many     | No       |
    | https://gedcom.io/terms/v7/NPFX            | Many     | No       |
    | https://gedcom.io/terms/v7/NSFX            | Many     | No       |
    | https://gedcom.io/terms/v7/SPFX            | Many     | No       |
    | https://gedcom.io/terms/v7/SURN            | Many     | No       |
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-Name
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM TRAN Structure](https://gedcom.io/terms/v7/NAME-TRAN)
    '''
    
    key: str = 'NAME-TRAN'
        
    def __init__(self, value: str, subs: Any) -> None:
        super().__init__(value, subs, self.key)
    

class NameType(BaseStructure):
    '''Store, validate and format the TYPE structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Type
    > An enumerated value from set `https://gedcom.io/terms/v7/enumset-NAME-TYPE`
    > indicating the type of the name.
        
    Enumerations:
    - 'AKA': https://gedcom.io/terms/v7/enum-AKA
        > Also known as, alias, etc.
    - 'BIRTH': https://gedcom.io/terms/v7/enum-BIRTH
        > Associated with birth, such as a birth name or birth parents.
    - 'IMMIGRANT': https://gedcom.io/terms/v7/enum-IMMIGRANT
        > Name assumed at the time of immigration.
    - 'MAIDEN': https://gedcom.io/terms/v7/enum-MAIDEN
        > Maiden name, name before first marriage.
    - 'MARRIED': https://gedcom.io/terms/v7/enum-MARRIED
        > Married name, assumed as part of marriage.
    - 'OTHER': https://gedcom.io/terms/v7/enum-OTHER
        > A value not listed here; should have a `PHRASE` substructure
    - 'PROFESSIONAL': https://gedcom.io/terms/v7/enum-PROFESSIONAL
        > Name used professionally (pen, screen, stage name).
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/PHRASE          | Many     | No       |
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-Enum
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM TYPE Structure](https://gedcom.io/terms/v7/NAME-TYPE)
    '''
    
    key: str = 'NAME-TYPE'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Name(BaseStructure):
    '''Store, validate and format the NAME structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Name
    > The name of the superstructure's subject, represented as a simple string.
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM NAME Structure](https://gedcom.io/terms/v7/NAME)
    '''
    
    key: str = 'NAME'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Nati(BaseStructure):
    '''Store, validate and format the NATI structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Nationality
    > An [Individual Attribute]. See also `INDIVIDUAL_ATTRIBUTE_STRUCTURE`.
    > nationality
    > An individual's national heritage or origin, or other folk, house, kindred,
    > lineage, or tribal interest.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM NATI Structure](https://gedcom.io/terms/v7/NATI)
    '''
    
    key: str = 'NATI'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Natu(BaseStructure):
    '''Store, validate and format the NATU structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Naturalization
    > An [Individual Event]. See also `INDIVIDUAL_EVENT_STRUCTURE`.
    > naturalization
    > Obtaining citizenship.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM NATU Structure](https://gedcom.io/terms/v7/NATU)
    '''
    
    key: str = 'NATU'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Nick(BaseStructure):
    '''Store, validate and format the NICK structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Nickname
    > A descriptive or familiar name that is used instead of, or in addition to,
    > one’s official or legal name.
    > 
    > <div class="note">
    > 
    > The label "nickname" and description text of this structure were introduced
    > with version 5.5 in 1996, but are understood differently by different users.
    > Some use `NICK` only for names that would be inappropriate in formal settings.
    > Some use it for pseudonyms regardless of where they are used. Some use it for
    > any variant of a name that is not the one used on legal documents. Because all
    > of these uses, and likely others as well, are common in existing data, no
    > further clarification of the meaning of the `NICK` structure is possible
    > without contradicting some existing data.
    > 
    > </div>
    > 
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM NICK Structure](https://gedcom.io/terms/v7/NICK)
    '''
    
    key: str = 'NICK'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Nmr(BaseStructure):
    '''Store, validate and format the NMR structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Number of marriages
    > An [Individual Attribute]. See also `INDIVIDUAL_ATTRIBUTE_STRUCTURE`.
    > number of marriages
    > The number of times this person has participated in a family as a spouse or
    > parent.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#nonNegativeInteger
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM NMR Structure](https://gedcom.io/terms/v7/NMR)
    '''
    
    key: str = 'NMR'
        
    def __init__(self, value: int, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class NoDate(BaseStructure):
    '''Store, validate and format the DATE structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Date
    > The `DatePeriod` during which the event did not occur or the attribute did
    > not apply.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/PHRASE          | Many     | No       |
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-Date#period
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM DATE Structure](https://gedcom.io/terms/v7/NO-DATE)
    '''
    
    key: str = 'NO-DATE'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class NoteTran(BaseStructure):
    '''Store, validate and format the TRAN structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Translation
    > A type of `TRAN` for unstructured human-readable text, such as is found in
    > `NOTE` and `SNOTE` payloads. Each `https://gedcom.io/terms/v7/NOTE-TRAN` must
    > have either a `LANG` substructure or a `MIME` substructure or both. If either
    > is missing, it is assumed to have the same value as the superstructure. See
    > also `NOTE` and `SNOTE`.
    > 
    > <div class="example">
    > 
    > The following presents the same note in HTML-format English; in plain-text with
    > the same language as the superstructure (English); and in Spanish with the same
    > media type as the superstructure (HTML).
    > 
    > ```gedcom
    > 1 NAME Arete /Hernandez/
    > 2 NOTE Named after Arete from <i>The Odyssey</i>
    > 3 LANG en
    > 3 MIME text/html
    > 3 TRAN Named after Arete from "The Odyssey"
    > 4 MIME text/plain
    > 3 TRAN Nombrada en honor a Arete de <i>La Odisea</i>
    > 4 LANG es
    > ```
    > 
    > </div>
    > 
    > It is recommended that text given in `text/html` should only be translated into
    > `text/plain` if the resulting text is different from the text created by the
    > HTML-to-text conversion process defined in `https://gedcom.io/terms/v7/MIME`.
    > 
    > A representation of the superstructure's data in a different format.
    > 
    > In some situations it is desirable to provide the same semantic content in
    > multiple formats. Where this is desirable, a `TRAN` substructure is used, where
    > the specific format is given in its language tag substructure, media type
    > substructure, or both.
    > 
    > Different `TRAN` structures are used in different contexts to fully capture the
    > structure of the information being presented in multiple formats. In all cases,
    > a `TRAN` structure's payload and substructures should provide only information
    > also contained in the `TRAN` structures' superstructure, but provide it in a
    > new language, script, or media type.
    > 
    > Each `TRAN` substructure must have either a language tag or a media type or
    > both. Each `TRAN` structure must differ from its superstructure and from every
    > other `TRAN` substructure of its superstructure in either its language tag or
    > its media type or both.
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/LANG            | Many     | No       |
    | https://gedcom.io/terms/v7/MIME            | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM TRAN Structure](https://gedcom.io/terms/v7/NOTE-TRAN)
    '''
    
    key: str = 'NOTE-TRAN'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Note(BaseStructure):
    '''Store, validate and format the NOTE structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Note
    > A `NOTE_STRUCTURE`, containing additional information provided by the submitter
    > for understanding the enclosing data.
    > 
    > When a substructure of `HEAD`, it should describe the contents of the document
    > in terms of "ancestors or descendants of" so that the person receiving the data
    > knows what genealogical information the document contains.
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/LANG            | Many     | No       |
    | https://gedcom.io/terms/v7/MIME            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE-TRAN       | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM NOTE Structure](https://gedcom.io/terms/v7/NOTE)
    '''
    
    key: str = 'NOTE'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Npfx(BaseStructure):
    '''Store, validate and format the NPFX structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Name prefix
    > Text that appears on a name line before the given and surname parts of a name.
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM NPFX Structure](https://gedcom.io/terms/v7/NPFX)
    '''
    
    key: str = 'NPFX'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Nsfx(BaseStructure):
    '''Store, validate and format the NSFX structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Name suffix
    > Text which appears on a name line after or behind the given and surname
    > parts of a name.
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM NSFX Structure](https://gedcom.io/terms/v7/NSFX)
    '''
    
    key: str = 'NSFX'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Obje(BaseStructure):
    '''Store, validate and format the OBJE structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Object
    > See `MULTIMEDIA_LINK`.
    > Links the superstructure to the `MULTIMEDIA_RECORD` with the given pointer.
    > 
    > The optional `CROP` substructure indicates that a subregion of an image
    > represents or applies to the superstructure.
    > 
    > The optional `TITL` substructure supersedes any `OBJE.FILE.TITL` substructures
    > included in the `MULTIMEDIA_RECORD`.
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/CROP            | Many     | No       |
    | https://gedcom.io/terms/v7/TITL            | Many     | No       |
        
    Args:
        value: A value of data type @<https://gedcom.io/terms/v7/record-OBJE>@
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM OBJE Structure](https://gedcom.io/terms/v7/OBJE)
    '''
    
    key: str = 'OBJE'
        
    def __init__(self, value: MultimediaXref, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Occu(BaseStructure):
    '''Store, validate and format the OCCU structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Occupation
    > An [Individual Attribute]. See also `INDIVIDUAL_ATTRIBUTE_STRUCTURE`.
    > occupation
    > The type of work or profession of an individual.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM OCCU Structure](https://gedcom.io/terms/v7/OCCU)
    '''
    
    key: str = 'OCCU'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class OrdStat(BaseStructure):
    '''Store, validate and format the STAT structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Status
    > An enumerated value from set `https://gedcom.io/terms/v7/enumset-ord-STAT`
    > assessing of the state or condition of an ordinance.

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
        OrdStat('BIC')
        
    Enumerations:
    - 'BIC': https://gedcom.io/terms/v7/enum-BIC
        > Applies to: `SLGC`
    - 'CANCELED': https://gedcom.io/terms/v7/enum-CANCELED
        > Applies to: `SLGS`
    - 'CHILD': https://gedcom.io/terms/v7/enum-CHILD
        > Applies to: All but `SLGC`
    - 'COMPLETED': https://gedcom.io/terms/v7/enum-COMPLETED
        > Applies to: All
    - 'DNS_CAN': https://gedcom.io/terms/v7/enum-DNS_CAN
        > Applies to: `SLGS`
    - 'DNS': https://gedcom.io/terms/v7/enum-DNS
        > Applies to: `SLGC`, `SLGS`
    - 'EXCLUDED': https://gedcom.io/terms/v7/enum-EXCLUDED
        > Applies to: All
    - 'INFANT': https://gedcom.io/terms/v7/enum-INFANT
        > Applies to: All but `SLGC`
    - 'PRE_1970': https://gedcom.io/terms/v7/enum-PRE_1970
        > Applies to: All
    - 'STILLBORN': https://gedcom.io/terms/v7/enum-STILLBORN
        > Applies to: All
    - 'SUBMITTED': https://gedcom.io/terms/v7/enum-SUBMITTED
        > Applies to: All
    - 'UNCLEARED': https://gedcom.io/terms/v7/enum-UNCLEARED
        > Applies to: All
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/DATE-exact      | Many     | No       |
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-Enum
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM STAT Structure](https://gedcom.io/terms/v7/ord-STAT)
    '''
    
    key: str = 'ord-STAT'
        
    def __init__(self, value: str, subs: Any) -> None:
        super().__init__(value, subs, self.key)
    

class Ordn(BaseStructure):
    '''Store, validate and format the ORDN structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Ordination
    > An [Individual Event]. See also `INDIVIDUAL_EVENT_STRUCTURE`.
    > ordination
    > Receiving authority to act in religious matters.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM ORDN Structure](https://gedcom.io/terms/v7/ORDN)
    '''
    
    key: str = 'ORDN'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Page(BaseStructure):
    '''Store, validate and format the PAGE structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Page
    > A specific location within the information referenced. For a published work,
    > this could include the volume of a multi-volume work and the page number or
    > numbers. For a periodical, it could include volume, issue, and page numbers.
    > For a newspaper, it could include a date, page number, and column number. For
    > an unpublished source or microfilmed works, this could be a film or sheet
    > number, page number, or frame number. A census record might have an enumerating
    > district, page number, line number, dwelling number, and family number.
    > 
    > It is recommended that the data in this field be formatted comma-separated with
    > label: value pairs
    > 
    > <div class="example">
    > 
    > ```gedcom
    > 2 SOUR @S1@
    > 3 PAGE Film: 1234567, Frame: 344, Line: 28
    > ```
    > 
    > </div>
    > 
    > If the superstructure's pointer is `@VOID@` then there is no information
    > referenced and the `PAGE` may describe the entire source.
    > 
    > <div class="example">
    > 
    > ```gedcom
    > 1 DSCR Tall enough his head touched the ceiling
    > 2 SOUR @VOID@
    > 3 PAGE His grand-daughter Lydia told me this in 1980
    > ```
    > 
    > </div>
    > 
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM PAGE Structure](https://gedcom.io/terms/v7/PAGE)
    '''
    
    key: str = 'PAGE'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Pedi(BaseStructure):
    '''Store, validate and format the PEDI structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Pedigree
    > An enumerated value from set `https://gedcom.io/terms/v7/enumset-PEDI`
    > indicating the type of child-to-family relationship represented by the
    > superstructure.

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
        Pedi('ADOPTED')
        
    Enumerations:
    - 'ADOPTED': https://gedcom.io/terms/v7/enum-ADOPTED
        > Adoptive parents
    - 'BIRTH': https://gedcom.io/terms/v7/enum-BIRTH
        > Associated with birth, such as a birth name or birth parents.
    - 'FOSTER': https://gedcom.io/terms/v7/enum-FOSTER
        > The child was included in a foster or guardian family
    - 'OTHER': https://gedcom.io/terms/v7/enum-OTHER
        > A value not listed here; should have a `PHRASE` substructure
    - 'SEALING': https://gedcom.io/terms/v7/enum-SEALING
        > The child was sealed to parents other than birth parents
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/PHRASE          | Many     | No       |
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-Enum
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM PEDI Structure](https://gedcom.io/terms/v7/PEDI)
    '''
    
    key: str = 'PEDI'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Phon(BaseStructure):
    '''Store, validate and format the PHON structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Phone
    > A telephone number. Telephone numbers have many regional variations and can
    > contain non-digit characters. Users should be encouraged to use
    > internationalized telephone numbers rather than local versions. As a starting
    > point for this recommendation, there are international standards that use a
    > "'+'" shorthand for the international prefix (for example, in place of "011" in
    > the US or "00" in the UK). Examples are `+1 (555) 555-1234` (US) or
    > `+44 20 1234 1234` (UK).
    > 
    > See ITU standards [E.123] and [E.164] for more information.
    > 
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM PHON Structure](https://gedcom.io/terms/v7/PHON)
    '''
    
    key: str = 'PHON'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Phrase(BaseStructure):
    '''Store, validate and format the PHRASE structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Phrase
    > Textual information that cannot be expressed in the superstructure due to the
    > limitations of its data type. A `PHRASE` may restate information contained in
    > the superstructure, but doing so is not recommended unless it is needed for
    > clarity.
    > 
    > <div class="example">
    > 
    > A date interpreted from the phrase "The Feast of St John" might be
    > 
    > ```gedcom
    > 2 DATE 24 JUN 1852
    > 3 PHRASE During the feast of St John
    > ```
    > 
    > </div>
    > 
    > <div class="example">
    > 
    > A record using `1648/9` to indicate a change in new year might become
    > 
    > ```gedcom
    > 2 DATE 30 JAN 1649
    > 3 PHRASE 30th of January, 1648/9
    > ```
    > 
    > </div>
    > 
    > <div class="example">
    > 
    > A record using `1648/9` to indicate uncertainty in the year might become
    > 
    > ```gedcom
    > 2 DATE BET 1648 AND 1649
    > 3 PHRASE 1648/9
    > ```
    > 
    > </div>
    > 
    > <div class="example">
    > 
    > A record using `Q1 1867` to indicate an event occurred sometime within the
    > first quarter of 1867 might become
    > 
    > ```gedcom
    > 2 DATE BET 1 JAN 1867 AND 31 MAR 1867
    > 3 PHRASE Q1 1867
    > ```
    > 
    > </div>
    > 
    > <div class="example">
    > 
    > A record defining the Maid of Honor in a marriage might become
    > 
    > ```gedcom
    > 1 MARR
    > 2 ASSO @I2@
    > 3 ROLE OTHER
    > 4 PHRASE Maid of Honor
    > ```
    > 
    > </div>
    > 
    > <div class="example">
    > 
    > A name given to a foundling orphan might be
    > 
    > ```gedcom
    > 1 NAME Mary //
    > 2 GIVN Mary
    > 2 TYPE OTHER
    > 3 PHRASE given by orphanage
    > ```
    > 
    > </div>
    > 
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM PHRASE Structure](https://gedcom.io/terms/v7/PHRASE)
    '''
    
    key: str = 'PHRASE'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class PlacForm(BaseStructure):
    '''Store, validate and format the FORM structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Format
    > A comma-separated list of jurisdictional titles, which has the same number of
    > elements and in the same order as the `PLAC` structure. As with `PLAC`, this
    > shall be ordered from lowest to highest jurisdiction.
    > 
    > <div class="example">
    > 
    > The following represents Baltimore, a city that is not within a county.
    > 
    > ```gedcom
    > 2 PLAC Baltimore, , Maryland, USA
    > 3 FORM City, County, State, Country
    > ```
    > 
    > </div>
    > 
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-List#Text
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM FORM Structure](https://gedcom.io/terms/v7/PLAC-FORM)
    '''
    
    key: str = 'PLAC-FORM'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class PlacTran(BaseStructure):
    '''Store, validate and format the TRAN structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Translation
    > A type of `TRAN` substructure specific to places. Each `PLAC`.`TRAN` must have
    > a `LANG` substructure. See also `PLAC`.
    > 
    > <div class="example">
    > 
    > The following presents a place in Japanese with a romaji transliteration and
    > English translation
    > 
    > ```gedcom
    > 2 PLAC 千代田, 東京, 日本
    > 3 FORM 区, 都, 国
    > 3 LANG ja
    > 3 TRAN Chiyoda, Tokyo, Nihon
    > 4 LANG ja-Latn
    > 3 TRAN Chiyoda, Tokyo, Japan
    > 4 LANG en
    > ```
    > 
    > </div>
    > 
    > A representation of the superstructure's data in a different format.
    > 
    > In some situations it is desirable to provide the same semantic content in
    > multiple formats. Where this is desirable, a `TRAN` substructure is used, where
    > the specific format is given in its language tag substructure, media type
    > substructure, or both.
    > 
    > Different `TRAN` structures are used in different contexts to fully capture the
    > structure of the information being presented in multiple formats. In all cases,
    > a `TRAN` structure's payload and substructures should provide only information
    > also contained in the `TRAN` structures' superstructure, but provide it in a
    > new language, script, or media type.
    > 
    > Each `TRAN` substructure must have either a language tag or a media type or
    > both. Each `TRAN` structure must differ from its superstructure and from every
    > other `TRAN` substructure of its superstructure in either its language tag or
    > its media type or both.
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/LANG            | Many     | No       |
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-List#Text
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM TRAN Structure](https://gedcom.io/terms/v7/PLAC-TRAN)
    '''
    
    key: str = 'PLAC-TRAN'
        
    def __init__(self, value: str, subs: Any) -> None:
        super().__init__(value, subs, self.key)
    

class Plac(BaseStructure):
    '''Store, validate and format the PLAC structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Place
    > The principal place in which the superstructure's subject occurred, represented
    > as a [List] of jurisdictional entities in a sequence from the lowest to the
    > highest jurisdiction, where "jurisdiction" includes units in a political,
    > ecclesiastical, and geographical hierarchies and may include units of any size,
    > such as a continent, "at sea", or a specific building, farm, or cemetery. As
    > with other lists, the jurisdictions are separated by commas. Any jurisdiction's
    > name that is missing is still accounted for by an empty string in the list.
    > 
    > The type of each jurisdiction is given in the `PLAC`.`FORM` substructure, if
    > present, or in the `HEAD`.`PLAC`.`FORM` structure. If neither is present, the
    > jurisdictional types are unspecified beyond the lowest-to-highest order noted
    > above.
    > 
    > <div class="deprecation">
    > 
    > Having an `EXID` without an `EXID`.`TYPE` substructure is deprecated. The
    > meaning of an `EXID` depends on its `EXID`.`TYPE`. The cardinality of
    > `EXID`.`TYPE` will be changed to `{1:1}` in version 8.0.
    > 
    > </div>
    > 
    > A place, which can be represented in several ways:
    > 
    > - The payload contains a comma-separated list of region names, ordered from
    >   smallest to largest. The specific meaning of each element is given by the
    >   `FORM` substructure, or in the `HEAD`.`PLAC`.`FORM` if there is no `FORM`
    >   substructure. If neither `FORM` exists, the meaning of the elements are not
    >   defined in this specification beyond being names of jurisdictions of some
    >   kind, ordered from smallest to largest.
    > 
    >   <div class="note">
    >     Some applications and users have defaulted to assuming a `FORM` of "City, County, State, Country",
    >     and some applications even ignore any `FORM` substructures and treat payloads with a smaller number of
    >     elements as if they had additional blank elements at the end.
    >     </div>
    > 
    >   Elements should be left blank if they are unknown, do not apply to the
    >   location, or are too specific for the region in question.
    > 
    >   <div class="example">
    >     A record describing births throughout Oneida county could be recorded as
    > 
    >   ```gedcom
    >   0 @S1@ SOUR
    >   1 DATA
    >   2 EVEN BIRT
    >   3 PLAC , Oneida, Idaho, USA
    >   4 FORM City, County, State, Country
    >   ```
    > 
    >   </div>
    > 
    > - The payload may be translated or transliterated into different languages or
    >   scripts using the `TRAN` substructure. It should use the same `FORM` as the
    >   payload.
    > 
    > - Global coordinates may be presented in the `MAP` substructure
    > 
    > <div class="note">
    > 
    > This specification does not support places where a region name contains a
    > comma. An alternative system for representing locations is likely to be added
    > in a later version.
    > 
    > </div>
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/EXID            | Many     | No       |
    | https://gedcom.io/terms/v7/LANG            | Many     | No       |
    | https://gedcom.io/terms/v7/MAP             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC-FORM       | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC-TRAN       | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-List#Text
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM PLAC Structure](https://gedcom.io/terms/v7/PLAC)
    '''
    
    key: str = 'PLAC'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Post(BaseStructure):
    '''Store, validate and format the POST structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Postal code
    > A code used by a postal service to identify an area to facilitate mail
    > handling. See `ADDRESS_STRUCTURE` for more details.
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM POST Structure](https://gedcom.io/terms/v7/POST)
    '''
    
    key: str = 'POST'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Prob(BaseStructure):
    '''Store, validate and format the PROB structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Probate
    > An [Individual Event]. See also `INDIVIDUAL_EVENT_STRUCTURE`.
    > probate
    > Judicial determination of the validity of a will. It may indicate several
    > related court activities over several dates.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM PROB Structure](https://gedcom.io/terms/v7/PROB)
    '''
    
    key: str = 'PROB'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Publ(BaseStructure):
    '''Store, validate and format the PUBL structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Publication
    > When and where the record was created. For published works, this includes
    > information such as the city of publication, name of the publisher, and year of
    > publication.
    > 
    > For an unpublished work, it includes the date the record was created and the
    > place where it was created, such as the county and state of residence of a
    > person making a declaration for a pension or the city and state of residence of
    > the writer of a letter.
    > 
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM PUBL Structure](https://gedcom.io/terms/v7/PUBL)
    '''
    
    key: str = 'PUBL'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Quay(BaseStructure):
    '''Store, validate and format the QUAY structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Quality of data
    > An enumerated value from set `https://gedcom.io/terms/v7/enumset-QUAY`
    > indicating the credibility of a piece of information, based on its
    > supporting evidence. Some systems use this feature to rank multiple
    > conflicting opinions for display of most likely information first. It is
    > not intended to eliminate the receivers' need to evaluate the evidence for
    > themselves.

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
        Quay('0')
        
    Enumerations:
    - '0': https://gedcom.io/terms/v7/enum-0
        > Unreliable evidence or estimated data
    - '1': https://gedcom.io/terms/v7/enum-1
        > Questionable reliability of evidence (interviews, census, oral genealogies,
        > or potential for bias, such as an autobiography)
    - '2': https://gedcom.io/terms/v7/enum-2
        > Secondary evidence, data officially recorded sometime after the event
    - '3': https://gedcom.io/terms/v7/enum-3
        > Direct and primary evidence used, or by dominance of the evidence
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-Enum
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM QUAY Structure](https://gedcom.io/terms/v7/QUAY)
    '''
    
    key: str = 'QUAY'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class RecordFam(BaseStructure):
    '''Store, validate and format the FAM structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Family record
    > See `FAMILY_RECORD`
    > 
    > <div class="note">
    > 
    > The common case is that each couple has one `FAM` record, but that is not
    > always the case.
    > 
    > A couple that separates and then gets together again can be represented either
    > as a single `FAM` with multiple events (`MARR`, `DIV`, etc.) or as a separate
    > `FAM` for each time together. Some user interfaces may display these two in
    > different ways and the two admit different semantics in sourcing. A single
    > `FAM` with two `MARR` with distinct dates might also represent uncertainty
    > about dates and a pair of `FAM` with same spouses might also be the result of
    > merging multiple files.
    > 
    > Implementers should support both representations, and should choose between
    > them based on user input or other context beyond that provided in the datasets
    > themselves.
    > 
    > </div>
    > 
    > The `FAM` record was originally structured to represent families where a male
    > `HUSB` (husband or father) and female `WIFE` (wife or mother) produce `CHIL`
    > (children). The `FAM` record may also be used for cultural parallels to this,
    > including nuclear families, marriage, cohabitation, fostering, adoption, and so
    > on, regardless of the gender of the partners. Sex, gender, titles, and roles of
    > partners should not be inferred based on the partner that the `HUSB` or `WIFE`
    > structure points to.
    > 
    > The individuals pointed to by the `HUSB` and `WIFE` are collectively referred
    > to as "partners", "parents" or "spouses".
    > 
    > Some displays may be unable to display more than 2 partners. Displays may use
    > `HUSB` and `WIFE` as layout hints, for example, by consistently displaying the
    > `HUSB` on the same side of the `WIFE` in a tree view. Family structures with
    > more than 2 partners may either use several `FAM` records or use
    > `ASSOCIATION_STRUCTURE`s to indicate additional partners. `ASSO` should not be
    > used for relationships that can be expressed using `HUSB`, `WIFE`, or `CHIL`
    > instead.
    > 
    > <div class="note">
    > 
    > The `FAM` record will be revised in a future version to more fully express the
    > diversity of human family relationships.
    > 
    > </div>
    > 
    > The order of the `CHIL` (children) pointers within a `FAM` (family) structure
    > should be chronological by birth; this is an exception to the usual "most
    > preferred value first" rule. A `CHIL` with a `voidPtr` indicates a placeholder
    > for an unknown child in this birth order.
    > 
    > If a `FAM` record uses `HUSB` or `WIFE` to point to an `INDI` record, the
    > `INDI` record must use `FAMS` to point to the `FAM` record. If a `FAM` record
    > uses `CHIL` to point to an `INDI` record, the `INDI` record must use a `FAMC`
    > to point to the `FAM` record.
    > 
    > An `INDI` record should not have multiple `FAMS` substructures pointing to the
    > same `FAM`.
    > 
    > A `FAM` record should not have multiple `CHIL` substructures pointing to the
    > same `INDI`; doing so implies a nonsensical birth order. An `INDI` record may
    > have multiple `FAMC` substructures pointing to the same `FAM`, but doing so is
    > not recommended.
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ANUL            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CHAN            | Many     | No       |
    | https://gedcom.io/terms/v7/CHIL            | Many     | No       |
    | https://gedcom.io/terms/v7/CREA            | Many     | No       |
    | https://gedcom.io/terms/v7/DIV             | Many     | No       |
    | https://gedcom.io/terms/v7/DIVF            | Many     | No       |
    | https://gedcom.io/terms/v7/ENGA            | Many     | No       |
    | https://gedcom.io/terms/v7/EXID            | Many     | No       |
    | https://gedcom.io/terms/v7/FAM-CENS        | Many     | No       |
    | https://gedcom.io/terms/v7/FAM-EVEN        | Many     | No       |
    | https://gedcom.io/terms/v7/FAM-FACT        | Many     | No       |
    | https://gedcom.io/terms/v7/FAM-HUSB        | Many     | No       |
    | https://gedcom.io/terms/v7/FAM-NCHI        | Many     | No       |
    | https://gedcom.io/terms/v7/FAM-RESI        | Many     | No       |
    | https://gedcom.io/terms/v7/FAM-WIFE        | Many     | No       |
    | https://gedcom.io/terms/v7/MARB            | Many     | No       |
    | https://gedcom.io/terms/v7/MARC            | Many     | No       |
    | https://gedcom.io/terms/v7/MARL            | Many     | No       |
    | https://gedcom.io/terms/v7/MARR            | Many     | No       |
    | https://gedcom.io/terms/v7/MARS            | Many     | No       |
    | https://gedcom.io/terms/v7/NO              | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/REFN            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SLGS            | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/SUBM            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
        
    Args:
        value: A value of data type FamilyXref
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM FAM Structure](https://gedcom.io/terms/v7/record-FAM)
    '''
    
    key: str = 'record-FAM'
        
    def __init__(self, value: FamilyXref, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class RecordIndi(BaseStructure):
    '''Store, validate and format the INDI structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Individual
    > See `INDIVIDUAL_RECORD`.
    > The individual record is a compilation of facts or hypothesized facts about an
    > individual. These facts may come from multiple sources. Source citations and
    > notes allow documentation of the source where each of the facts were
    > discovered.
    > 
    > A single individual may have facts distributed across multiple individual
    > records, connected by `ALIA` (alias, in the computing sense not the pseudonym
    > sense) pointers. See `ALIA` for more details.
    > 
    > Individual records are linked to Family records by use of bi-directional
    > pointers. Details about those links are stored as substructures of the pointers
    > in the individual record.
    > 
    > Other associations or relationships are represented by the `ASSO` (association)
    > tag. The person's relation or associate is the person being pointed to. The
    > association or relationship is stated by the value on the subordinate `ROLE`
    > line. `ASSO` should not be used for relationships that can be expressed using
    > `FAMS` or `FAMC` instead.
    > 
    > <div class="example">
    > 
    > The following example refers to 2 individuals, `@I1@` and `@I2@`, where `@I2@`
    > is a godparent of `@I1@`:
    > 
    > ```gedcom
    > 0 @I1@ INDI
    > 1 ASSO @I2@
    > 2 ROLE GODP
    > ```
    > 
    > </div>
    > 
    > Events stored as facts within an `INDI` record may also have `FAMC` or `ASSO`
    > tags to indicate families and individuals that participated in those events.
    > For example, a `FAMC` pointer subordinate to an adoption event indicates a
    > relationship to family by adoption; biological parents can be shown by a `FAMC`
    > pointer subordinate to the birth event; the eulogist at a funeral can be shown
    > by an `ASSO` pointer subordinate to the burial event; and so on. A subordinate
    > `FAMC` pointer is allowed to refer to a family where the individual does not
    > appear as a child.
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADOP            | Many     | No       |
    | https://gedcom.io/terms/v7/ALIA            | Many     | No       |
    | https://gedcom.io/terms/v7/ANCI            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/BAPL            | Many     | No       |
    | https://gedcom.io/terms/v7/BAPM            | Many     | No       |
    | https://gedcom.io/terms/v7/BARM            | Many     | No       |
    | https://gedcom.io/terms/v7/BASM            | Many     | No       |
    | https://gedcom.io/terms/v7/BIRT            | Many     | No       |
    | https://gedcom.io/terms/v7/BLES            | Many     | No       |
    | https://gedcom.io/terms/v7/BURI            | Many     | No       |
    | https://gedcom.io/terms/v7/CAST            | Many     | No       |
    | https://gedcom.io/terms/v7/CHAN            | Many     | No       |
    | https://gedcom.io/terms/v7/CHR             | Many     | No       |
    | https://gedcom.io/terms/v7/CHRA            | Many     | No       |
    | https://gedcom.io/terms/v7/CONF            | Many     | No       |
    | https://gedcom.io/terms/v7/CONL            | Many     | No       |
    | https://gedcom.io/terms/v7/CREA            | Many     | No       |
    | https://gedcom.io/terms/v7/CREM            | Many     | No       |
    | https://gedcom.io/terms/v7/DEAT            | Many     | No       |
    | https://gedcom.io/terms/v7/DESI            | Many     | No       |
    | https://gedcom.io/terms/v7/DSCR            | Many     | No       |
    | https://gedcom.io/terms/v7/EDUC            | Many     | No       |
    | https://gedcom.io/terms/v7/EMIG            | Many     | No       |
    | https://gedcom.io/terms/v7/ENDL            | Many     | No       |
    | https://gedcom.io/terms/v7/EXID            | Many     | No       |
    | https://gedcom.io/terms/v7/FAMS            | Many     | No       |
    | https://gedcom.io/terms/v7/FCOM            | Many     | No       |
    | https://gedcom.io/terms/v7/GRAD            | Many     | No       |
    | https://gedcom.io/terms/v7/IDNO            | Many     | No       |
    | https://gedcom.io/terms/v7/IMMI            | Many     | No       |
    | https://gedcom.io/terms/v7/INDI-CENS       | Many     | No       |
    | https://gedcom.io/terms/v7/INDI-EVEN       | Many     | No       |
    | https://gedcom.io/terms/v7/INDI-FACT       | Many     | No       |
    | https://gedcom.io/terms/v7/INDI-FAMC       | Many     | No       |
    | https://gedcom.io/terms/v7/INDI-NAME       | Many     | No       |
    | https://gedcom.io/terms/v7/INDI-NCHI       | Many     | No       |
    | https://gedcom.io/terms/v7/INDI-RELI       | Many     | No       |
    | https://gedcom.io/terms/v7/INDI-RESI       | Many     | No       |
    | https://gedcom.io/terms/v7/INDI-TITL       | Many     | No       |
    | https://gedcom.io/terms/v7/INIL            | Many     | No       |
    | https://gedcom.io/terms/v7/NATI            | Many     | No       |
    | https://gedcom.io/terms/v7/NATU            | Many     | No       |
    | https://gedcom.io/terms/v7/NMR             | Many     | No       |
    | https://gedcom.io/terms/v7/NO              | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/OCCU            | Many     | No       |
    | https://gedcom.io/terms/v7/ORDN            | Many     | No       |
    | https://gedcom.io/terms/v7/PROB            | Many     | No       |
    | https://gedcom.io/terms/v7/PROP            | Many     | No       |
    | https://gedcom.io/terms/v7/REFN            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/RETI            | Many     | No       |
    | https://gedcom.io/terms/v7/SEX             | Many     | No       |
    | https://gedcom.io/terms/v7/SLGC            | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/SSN             | Many     | No       |
    | https://gedcom.io/terms/v7/SUBM            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WILL            | Many     | No       |
        
    Args:
        value: A value of data type IndividualXref
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM INDI Structure](https://gedcom.io/terms/v7/record-INDI)
    '''
    
    key: str = 'record-INDI'
        
    def __init__(self, value: IndividualXref, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class RecordObje(BaseStructure):
    '''Store, validate and format the OBJE structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Object
    > See `MULTIMEDIA_RECORD`.
    > The multimedia record refers to 1 or more external digital files, and may
    > provide some additional information about the files and the media they encode.
    > 
    > The file reference can occur more than once to group multiple files together.
    > Grouped files should each pertain to the same context. For example, a sound
    > clip and a photo both of the same event might be grouped in a single `OBJE`.
    > 
    > The change and creation dates should be for the `OBJE` record itself, not the
    > underlying files.
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/CHAN            | Many     | No       |
    | https://gedcom.io/terms/v7/CREA            | Many     | No       |
    | https://gedcom.io/terms/v7/EXID            | Many     | No       |
    | https://gedcom.io/terms/v7/FILE            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/REFN            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
        
    Args:
        value: A value of data type MultimediaXref
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM OBJE Structure](https://gedcom.io/terms/v7/record-OBJE)
    '''
    
    key: str = 'record-OBJE'
        
    def __init__(self, value: MultimediaXref, subs: Any) -> None:
        super().__init__(value, subs, self.key)
    

class RecordRepo(BaseStructure):
    '''Store, validate and format the REPO structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Repository
    > See `REPOSITORY_RECORD`.
    > The repository record provides information about an institution or person that
    > has a collection of sources. Informal repositories include the owner of an
    > unpublished work or of a rare published source, or a keeper of personal
    > collections. An example would be the owner of a family Bible containing
    > unpublished family genealogical entries.
    > 
    > Layered repositories, such as an archive containing copies of a subset of
    > records from another archive or archives that have moved or been bought by
    > other archives, are not modeled in this version of the specification. It is
    > expected they will be added in a later version. Until such time, it is
    > recommended that the repository record store current contact information, if
    > known.
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/CHAN            | Many     | No       |
    | https://gedcom.io/terms/v7/CREA            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/EXID            | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NAME            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/REFN            | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type RepositoryXref
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM REPO Structure](https://gedcom.io/terms/v7/record-REPO)
    '''
    
    key: str = 'record-REPO'
        
    def __init__(self, value: RepositoryXref, subs: Any) -> None:
        super().__init__(value, subs, self.key)
    

class RecordSnote(BaseStructure):
    '''Store, validate and format the SNOTE structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Shared note
    > A note that is shared by multiple structures. See `SHARED_NOTE_RECORD` for
    > more details.
    > A catch-all location for information that does not fully fit within other
    > structures. It may include research notes, additional context, alternative
    > interpretations, reasoning, and so forth.
    > 
    > A shared note record may be pointed to by multiple other structures. Shared
    > notes should only be used if editing the note in one place should edit it in
    > all other places or if the note itself requires an `IDENTIFIER_STRUCTURE`. If
    > each instance of the note may be edited separately and no identifier is needed,
    > a `NOTE` should be used instead.
    > 
    > Each [`SNOTE`.`TRAN`] must have either a `MIME` or `LANG` substructure or
    > both.
    > 
    > <div class="example">
    > 
    > The origin of a name might be a reasonable shared note, while the reason a
    > particular person was given that name may make more sense as a non-shared note.
    > 
    > ```gedcom
    > 0 @GORDON@ SNOTE "Gordon" is a traditional Scottish surname.
    > 1 CONT It became a given name in honor of Charles George Gordon.
    > 0 @I1@ INDI
    > 1 NAME Gordon /Jones/
    > 2 NOTE Named after the astronaut Gordon Cooper
    > 2 SNOTE @GORDON@
    > ```
    > 
    > </div>
    > 
    > <div class="note">
    > 
    > The ability to have multiple structures share a single note using pointers was
    > introduced in version 5.0 in 1991. However, as of 2021 relatively few
    > applications have a user interface that presents shared notes as such to users.
    > It is recommended that `SNOTE` be avoided when `NOTE` will suffice.
    > 
    > </div>
    > 
    > A `SHARED_NOTE_RECORD` may contain a pointer to a `SOURCE_RECORD` and vice
    > versa. Applications must not create datasets where these mutual pointers form a
    > cycle. Applications should also ensure they can handle invalid files with such
    > cycles in a safe manner.
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/CHAN            | Many     | No       |
    | https://gedcom.io/terms/v7/CREA            | Many     | No       |
    | https://gedcom.io/terms/v7/EXID            | Many     | No       |
    | https://gedcom.io/terms/v7/LANG            | Many     | No       |
    | https://gedcom.io/terms/v7/MIME            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE-TRAN       | Many     | No       |
    | https://gedcom.io/terms/v7/REFN            | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
        
    Args:
        value: A value of data type SharedNoteXref
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM SNOTE Structure](https://gedcom.io/terms/v7/record-SNOTE)
    '''
    
    key: str = 'record-SNOTE'
        
    def __init__(self, value: SharedNoteXref, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class RecordSour(BaseStructure):
    '''Store, validate and format the SOUR structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Source
    > A description of an entire source. See `SOURCE_RECORD` for more details.
    > A source record describes an entire source. A source may also point to `REPO`s
    > to describe repositories or archives where the source document may be found.
    > The part of a source relevant to a specific fact, such as a specific page or
    > entry, is indicated in a `SOURCE_CITATION` that points to the source record.
    > 
    > <div class="note">
    > 
    > This sourcing model is known to be insufficient for some use cases and may be
    > refined in a future version of this specification.
    > 
    > </div>
    > 
    > A `SOURCE_RECORD` may contain a pointer to a `SHARED_NOTE_RECORD` and vice
    > versa. Applications must not create datasets where these mutual pointers form a
    > cycle. Applications should also ensure they can handle invalid files with such
    > cycles in a safe manner.
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ABBR            | Many     | No       |
    | https://gedcom.io/terms/v7/AUTH            | Many     | No       |
    | https://gedcom.io/terms/v7/CHAN            | Many     | No       |
    | https://gedcom.io/terms/v7/CREA            | Many     | No       |
    | https://gedcom.io/terms/v7/DATA            | Many     | No       |
    | https://gedcom.io/terms/v7/EXID            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PUBL            | Many     | No       |
    | https://gedcom.io/terms/v7/REFN            | Many     | No       |
    | https://gedcom.io/terms/v7/REPO            | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/TEXT            | Many     | No       |
    | https://gedcom.io/terms/v7/TITL            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
        
    Args:
        value: A value of data type SourceXref
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM SOUR Structure](https://gedcom.io/terms/v7/record-SOUR)
    '''
    
    key: str = 'record-SOUR'
        
    def __init__(self, value: SourceXref, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class RecordSubm(BaseStructure):
    '''Store, validate and format the SUBM structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Submitter
    > A description of a contributor of information to the document. See
    > `SUBMITTER_RECORD` for more details.
    > The submitter record identifies an individual or organization that
    > contributed information contained in the dataset. All records in the
    > document are assumed to be contributed by the submitter referenced in the
    > `HEAD`, unless a `SUBM` structure inside a specific record points at a
    > different submitter record.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/CHAN            | Many     | No       |
    | https://gedcom.io/terms/v7/CREA            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/EXID            | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NAME            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/REFN            | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SUBM-LANG       | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type SubmitterXref
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM SUBM Structure](https://gedcom.io/terms/v7/record-SUBM)
    '''
    
    key: str = 'record-SUBM'
        
    def __init__(self, value: SubmitterXref, subs: Any) -> None:
        super().__init__(value, subs, self.key)
    

class Refn(BaseStructure):
    '''Store, validate and format the REFN structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Reference
    > A user-defined number or text that the submitter uses to identify the
    > superstructure. For instance, it may be a record number within the submitter's
    > automated or manual system, or it may be a page and position number on a
    > pedigree chart.
    > 
    > This is metadata about the structure itself, not data about its subject.
    > Multiple structures describing different aspects of the same subject must not
    > have the same `REFN` value.
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM REFN Structure](https://gedcom.io/terms/v7/REFN)
    '''
    
    key: str = 'REFN'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Reli(BaseStructure):
    '''Store, validate and format the RELI structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Religion
    > A religious denomination associated with the event or attribute described
    > by the superstructure.
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM RELI Structure](https://gedcom.io/terms/v7/RELI)
    '''
    
    key: str = 'RELI'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Repo(BaseStructure):
    '''Store, validate and format the REPO structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Repository
    > See `SOURCE_REPOSITORY_CITATION`.
    > This structure is used within a source record to point to a name and
    > address record of the holder of the source document. Formal and informal
    > repository name and addresses are stored in the `REPOSITORY_RECORD`. More
    > formal repositories, such as the Family History Library, should show a call
    > number of the source at that repository. The call number of that source
    > should be recorded using a `CALN` substructure.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/CALN            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
        
    Args:
        value: A value of data type @<https://gedcom.io/terms/v7/record-REPO>@
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM REPO Structure](https://gedcom.io/terms/v7/REPO)
    '''
    
    key: str = 'REPO'
        
    def __init__(self, value: RepositoryXref, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Resn(BaseStructure):
    '''Store, validate and format the RESN structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Restriction
    > A [List] of enumerated values from set
    > `https://gedcom.io/terms/v7/enumset-RESN` signifying access to information may
    > be denied or otherwise restricted.
    > 
    > The `RESN` structure is provided to assist software in filtering data that
    > should not be exported or otherwise used in a particular context. It is
    > recommended that tools provide an interface to allow users to filter data on
    > export such that certain `RESN` structure payload entries result in the `RESN`
    > structure and its superstructure being removed from the export. Such removal
    > must abide by some constraints: see [Removing data] for more details.
    > 
    > This is metadata about the structure itself, not data about its subject.
    > 

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
        Resn('CONFIDENTIAL')
        
    Enumerations:
    - 'CONFIDENTIAL': https://gedcom.io/terms/v7/enum-CONFIDENTIAL
        > This data was marked as confidential by the user.
    - 'LOCKED': https://gedcom.io/terms/v7/enum-LOCKED
        > Some systems may ignore changes to this data.
    - 'PRIVACY': https://gedcom.io/terms/v7/enum-PRIVACY
        > This data is not to be shared outside of a trusted circle, generally
        > because it contains information about living individuals. This definition
        > is known to admit multiple interpretations, so use of the `PRIVACY`
        > restriction notice is not recommended.
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-List#Enum
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM RESN Structure](https://gedcom.io/terms/v7/RESN)
    '''
    
    key: str = 'RESN'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Reti(BaseStructure):
    '''Store, validate and format the RETI structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Retirement
    > An [Individual Event]. See also `INDIVIDUAL_EVENT_STRUCTURE`.
    > retirement
    > Exiting an occupational relationship with an employer after a qualifying
    > time period.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM RETI Structure](https://gedcom.io/terms/v7/RETI)
    '''
    
    key: str = 'RETI'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Role(BaseStructure):
    '''Store, validate and format the ROLE structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Role
    > An enumerated value from set `https://gedcom.io/terms/v7/enumset-ROLE`
    > indicating what role this person played in an event or person's life.
    > 
    > <div class="example">
    > 
    > The following indicates a child's birth record as the source of the mother's
    > name:
    > 
    > ```gedcom
    > 0 @I1@ INDI
    > 1 NAME Mary //
    > 2 SOUR @S1@
    > 3 EVEN BIRT
    > 4 ROLE MOTH
    > ```
    > 
    > </div>
    > 
    > <div class="example">
    > 
    > The following indicates that a person's best friend was a witness at their
    > baptism:
    > 
    > ```gedcom
    > 0 @I2@ INDI
    > 1 ASSO @I3@
    > 2 ROLE FRIEND
    > 3 PHRASE best friend
    > 1 BAPM
    > 2 ASSO @I3@
    > 3 ROLE WITN
    > ```
    > 
    > </div>
    > 

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
        Role('CHIL')
        
    Enumerations:
    - 'CHIL': https://gedcom.io/terms/v7/enum-CHIL
        > Child
    - 'CLERGY': https://gedcom.io/terms/v7/enum-CLERGY
        > Religious official in event; implies `OFFICIATOR`
    - 'FATH': https://gedcom.io/terms/v7/enum-FATH
        > Father; implies `PARENT`
    - 'FRIEND': https://gedcom.io/terms/v7/enum-FRIEND
        > Friend
    - 'GODP': https://gedcom.io/terms/v7/enum-GODP
        > Godparent or related role in other religions
    - 'HUSB': https://gedcom.io/terms/v7/enum-HUSB
        > Husband; implies `SPOU`
    - 'MOTH': https://gedcom.io/terms/v7/enum-MOTH
        > Mother; implies `PARENT`
    - 'MULTIPLE': https://gedcom.io/terms/v7/enum-MULTIPLE
        > A sibling from the same pregnancy (twin, triplet, quadruplet, and so on). A
        > `PHRASE` can be used to specify the kind of multiple birth.
    - 'NGHBR': https://gedcom.io/terms/v7/enum-NGHBR
        > Neighbor
    - 'OFFICIATOR': https://gedcom.io/terms/v7/enum-OFFICIATOR
        > Officiator of the event
    - 'OTHER': https://gedcom.io/terms/v7/enum-OTHER
        > A value not listed here; should have a `PHRASE` substructure
    - 'PARENT': https://gedcom.io/terms/v7/enum-PARENT
        > Parent
    - 'SPOU': https://gedcom.io/terms/v7/enum-SPOU
        > Spouse
    - 'WIFE': https://gedcom.io/terms/v7/enum-WIFE
        > Wife; implies `SPOU`
    - 'WITN': https://gedcom.io/terms/v7/enum-WITN
        > Witness
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/PHRASE          | Many     | No       |
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-Enum
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM ROLE Structure](https://gedcom.io/terms/v7/ROLE)
    '''
    
    key: str = 'ROLE'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Schma(BaseStructure):
    '''Store, validate and format the SCHMA structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Extension schema
    > A container for storing meta-information about the extension tags used in
    > this document. See [Extensions] for more details.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/TAG             | Many     | No       |
        
    Args:
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM SCHMA Structure](https://gedcom.io/terms/v7/SCHMA)
    '''
    
    key: str = 'SCHMA'
        
    def __init__(self, subs: Any = None) -> None:
        super().__init__(Default.EMPTY, subs, self.key)
    

class Sdate(BaseStructure):
    '''Store, validate and format the SDATE structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Sort date
    > A date to be used as a sorting hint. It is intended for use when the actual
    > date is unknown, but the display order may be dependent on date.
    > 
    > If both a `DATE` and `SDATE` are present in the same structure, the `SDATE`
    > should be used for sorting and positioning while the `DATE` should be displayed
    > as the date of the structure.
    > 
    > `SDATE` and its substructures (including `PHRASE`, `TIME`, and any extension
    > structures) should be used only as sorting hints, not to convey historical
    > meaning.
    > 
    > It is recommended to use a payload that matches
    > `[[day D] month D] year [D epoch]`. Other DateValue forms may have unreliable
    > effects on sorting. Including a month and day is encouraged to help different
    > applications sort dates the same way, as the relative ordering of dates with
    > different levels of precision is not well defined.
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/PHRASE          | Many     | No       |
    | https://gedcom.io/terms/v7/TIME            | Many     | No       |
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-Date
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM SDATE Structure](https://gedcom.io/terms/v7/SDATE)
    '''
    
    key: str = 'SDATE'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Sex(BaseStructure):
    '''Store, validate and format the SEX structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Sex
    > An enumerated value from set `https://gedcom.io/terms/v7/enumset-SEX` that
    > indicates the sex of the individual at birth.

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
        Sex('F')
        
    Enumerations:
    - 'F': https://gedcom.io/terms/v7/enum-F
        > Female
    - 'M': https://gedcom.io/terms/v7/enum-M
        > Male
    - 'U': https://gedcom.io/terms/v7/enum-U
        > Cannot be determined from available sources
    - 'X': https://gedcom.io/terms/v7/enum-X
        > Does not fit the typical definition of only Male or only Female
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-Enum
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM SEX Structure](https://gedcom.io/terms/v7/SEX)
    '''
    
    key: str = 'SEX'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Slgc(BaseStructure):
    '''Store, validate and format the SLGC structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Sealing, child
    > A [Latter-Day Saint Ordinance]. See also `LDS_INDIVIDUAL_ORDINANCE`.
    > sealing child
    > A religious event pertaining to the sealing of a child to his or her
    > parents in a temple ceremony of The Church of Jesus Christ of Latter-day
    > Saints.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/FAMC            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TEMP            | Many     | No       |
    | https://gedcom.io/terms/v7/ord-STAT        | Many     | No       |
        
    Args:
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM SLGC Structure](https://gedcom.io/terms/v7/SLGC)
    '''
    
    key: str = 'SLGC'
        
    def __init__(self, subs: Any) -> None:
        super().__init__(Default.EMPTY, subs, self.key)
    

class Slgs(BaseStructure):
    '''Store, validate and format the SLGS structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Sealing, spouse
    > A [Latter-Day Saint Ordinance]. See also `LDS_SPOUSE_SEALING`.
    > Ordinances performed by members of The Church of Jesus Christ of Latter-day
    > Saints; see [Latter-day Saint Ordinances] for descriptions of each
    > ordinance type.
    > sealing spouse
    > A religious event pertaining to the sealing of a husband and wife in a
    > temple ceremony of The Church of Jesus Christ of Latter-day Saints. (See
    > also [`MARR`])
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TEMP            | Many     | No       |
    | https://gedcom.io/terms/v7/ord-STAT        | Many     | No       |
        
    Args:
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM SLGS Structure](https://gedcom.io/terms/v7/SLGS)
    '''
    
    key: str = 'SLGS'
        
    def __init__(self, subs: Any = None) -> None:
        super().__init__(Default.EMPTY, subs, self.key)
    

class Snote(BaseStructure):
    '''Store, validate and format the SNOTE structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Shared note
    > A pointer to a note that is shared by multiple structures. See
    > `NOTE_STRUCTURE` for more details.
        
    Args:
        value: A value of data type @<https://gedcom.io/terms/v7/record-SNOTE>@
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM SNOTE Structure](https://gedcom.io/terms/v7/SNOTE)
    '''
    
    key: str = 'SNOTE'
        
    def __init__(self, value: SharedNoteXref, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class SourData(BaseStructure):
    '''Store, validate and format the DATA structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Data
    > See `https://gedcom.io/terms/v7/DATA`.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/TEXT            | Many     | No       |
        
    Args:
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM DATA Structure](https://gedcom.io/terms/v7/SOUR-DATA)
    '''
    
    key: str = 'SOUR-DATA'
        
    def __init__(self, subs: Any = None) -> None:
        super().__init__(Default.EMPTY, subs, self.key)
    

class SourEven(BaseStructure):
    '''Store, validate and format the EVEN structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Event
    > An enumerated value from set `https://gedcom.io/terms/v7/enumset-EVENATTR`
    > indicating the type of event or attribute which was responsible for the
    > source entry being recorded. For example, if the entry was created to
    > record a birth of a child, then the type would be `BIRT` regardless of the
    > assertions made from that record, such as the mother's name or mother's
    > birth date.
        
    Enumerations:
    - 'CENS': https://gedcom.io/terms/v7/enum-CENS
        > A census event; either `https://gedcom.io/terms/v7/INDI-CENS` or
        > `https://gedcom.io/terms/v7/FAM-CENS`
    - 'EVEN': https://gedcom.io/terms/v7/enum-EVEN
        > A generic event; either `https://gedcom.io/terms/v7/INDI-EVEN` or
        > `https://gedcom.io/terms/v7/FAM-EVEN`
    - 'FACT': https://gedcom.io/terms/v7/enum-FACT
        > A generic attribute; either `https://gedcom.io/terms/v7/INDI-FACT` or
        > `https://gedcom.io/terms/v7/FAM-FACT`
    - 'NCHI': https://gedcom.io/terms/v7/enum-NCHI
        > A count of children; either `https://gedcom.io/terms/v7/INDI-NCHI` or
        > `https://gedcom.io/terms/v7/FAM-NCHI`
    - 'RESI': https://gedcom.io/terms/v7/enum-RESI
        > A residence attribute; either `https://gedcom.io/terms/v7/INDI-RESI` or
        > `https://gedcom.io/terms/v7/FAM-RESI`
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/PHRASE          | Many     | No       |
    | https://gedcom.io/terms/v7/ROLE            | Many     | No       |
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-Enum
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM EVEN Structure](https://gedcom.io/terms/v7/SOUR-EVEN)
    '''
    
    key: str = 'SOUR-EVEN'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Sour(BaseStructure):
    '''Store, validate and format the SOUR structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Source
    > A description of the relevant part of a source to support the
    > superstructure's data. See `SOURCE_CITATION` for more details.
    > A citation indicating that the pointed-to source record supports the claims
    > made in the superstructure. Substructures provide additional information about
    > how that source applies to the subject of the citation's superstructure:
    > 
    > - `PAGE`: where in the source the relevant material can be found.
    > - `DATA`: the relevant data from the source.
    > - `EVEN`: what event the relevant material was recording.
    > - `QUAY`: an estimation of the reliability of the source in regard to these
    >   claims.
    > - `MULTIMEDIA_LINK`: digital copies of the cited part of the source
    > 
    > It is recommended that every `SOURCE_CITATION` point to a `SOURCE_RECORD`.
    > However, a `voidPtr` can be used with the citation text in a `PAGE`
    > substructure. The `PAGE` is defined to express a "specific location within the
    > information referenced;" with a `voidPtr` there is no information referenced,
    > so the `PAGE` may describe the entire source.
    > 
    > A `SOURCE_CITATION` can contain a `NOTE_STRUCTURE`, which in turn can contain a
    > `SOURCE_CITATION`, allowing potentially unbounded nesting of structures.
    > Because each dataset is finite, this nesting is also guaranteed to be finite.
    > 
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PAGE            | Many     | No       |
    | https://gedcom.io/terms/v7/QUAY            | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR-DATA       | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR-EVEN       | Many     | No       |
        
    Args:
        value: A value of data type @<https://gedcom.io/terms/v7/record-SOUR>@
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM SOUR Structure](https://gedcom.io/terms/v7/SOUR)
    '''
    
    key: str = 'SOUR'
        
    def __init__(self, value: SourceXref, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Spfx(BaseStructure):
    '''Store, validate and format the SPFX structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Surname prefix
    > A name piece used as a non-indexing pre-part of a surname.
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM SPFX Structure](https://gedcom.io/terms/v7/SPFX)
    '''
    
    key: str = 'SPFX'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Ssn(BaseStructure):
    '''Store, validate and format the SSN structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Social security number
    > An [Individual Attribute]. See also `INDIVIDUAL_ATTRIBUTE_STRUCTURE`.
    > social security number
    > A number assigned by the United States Social Security Administration, used
    > for tax identification purposes. It is a type of `IDNO`.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM SSN Structure](https://gedcom.io/terms/v7/SSN)
    '''
    
    key: str = 'SSN'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Stae(BaseStructure):
    '''Store, validate and format the STAE structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > State
    > A geographical division of a larger jurisdictional area, such as a state
    > within the United States of America. See `ADDRESS_STRUCTURE` for more
    > details.
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM STAE Structure](https://gedcom.io/terms/v7/STAE)
    '''
    
    key: str = 'STAE'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class SubmLang(BaseStructure):
    '''Store, validate and format the LANG structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Language
    > A language the subject of that record understands.
    > 
    > The payload of the `LANG` structure is a language tag, as defined by [BCP 47].
    > 
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#Language
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM LANG Structure](https://gedcom.io/terms/v7/SUBM-LANG)
    '''
    
    key: str = 'SUBM-LANG'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Subm(BaseStructure):
    '''Store, validate and format the SUBM structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Submitter
    > A contributor of information in the substructure. This is metadata about
    > the structure itself, not data about its subject.
        
    Args:
        value: A value of data type @<https://gedcom.io/terms/v7/record-SUBM>@
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM SUBM Structure](https://gedcom.io/terms/v7/SUBM)
    '''
    
    key: str = 'SUBM'
        
    def __init__(self, value: SubmitterXref, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Surn(BaseStructure):
    '''Store, validate and format the SURN structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Surname
    > A family name passed on or used by members of a family.
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM SURN Structure](https://gedcom.io/terms/v7/SURN)
    '''
    
    key: str = 'SURN'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Tag(BaseStructure):
    '''Store, validate and format the TAG structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Extension tag
    > Information relating to a single extension tag as used in this document.
    > See [Extensions] for more details.
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM TAG Structure](https://gedcom.io/terms/v7/TAG)
    '''
    
    key: str = 'TAG'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Temp(BaseStructure):
    '''Store, validate and format the TEMP structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Temple
    > The name of a temple of The Church of Jesus Christ of Latter-day Saints.
    > Previous versions recommended using a set of abbreviations for temple
    > names, but the list of abbreviations is no longer published by the Church
    > and using abbreviations is no longer recommended.
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM TEMP Structure](https://gedcom.io/terms/v7/TEMP)
    '''
    
    key: str = 'TEMP'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Text(BaseStructure):
    '''Store, validate and format the TEXT structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Text from Source
    > A verbatim copy of any description contained within the source. This
    > indicates notes or text that are actually contained in the source document,
    > not the submitter's opinion about the source. This should be, from the
    > evidence point of view, "what the original record keeper said" as opposed
    > to the researcher's interpretation.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/LANG            | Many     | No       |
    | https://gedcom.io/terms/v7/MIME            | Many     | No       |
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM TEXT Structure](https://gedcom.io/terms/v7/TEXT)
    '''
    
    key: str = 'TEXT'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Time(BaseStructure):
    '''Store, validate and format the TIME structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Time
    > A `Time` value in a 24-hour clock format.
        
    Args:
        value: A value of data type https://gedcom.io/terms/v7/type-Time
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM TIME Structure](https://gedcom.io/terms/v7/TIME)
    '''
    
    key: str = 'TIME'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Titl(BaseStructure):
    '''Store, validate and format the TITL structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Title
    > The title, formal or informal, of the superstructure.
    > 
    > A published work, such as a book, might have a title plus the title of the
    > series of which the book is a part. A magazine article would have a title plus
    > the title of the magazine that published the article.
    > 
    > For an unpublished work, including most digital files, titles should be
    > descriptive and appropriate to the work.
    > 
    > <div class="example">
    > 
    > <p></p>
    > 
    > - The `TITL` of a letter might include the date, the sender, and the receiver.
    > - The `TITL` of a transaction between a buyer and seller might have their names
    >   and the transaction date.
    > - The `TITL` of a family Bible containing genealogical information might have
    >   past and present owners and a physical description of the book.
    > - The `TITL` of a personal interview would cite the informant and interviewer.
    > 
    > </div>
    > 
    > Some sources may have a citation text that cannot readily be represented using
    > the `SOURCE_RECORD` substructures `AUTH`, `PUBL`, `REPO`, and so on. In such
    > cases, the entire citation text may be presented as the payload of the
    > `SOUR`.`TITL`.
    > 
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM TITL Structure](https://gedcom.io/terms/v7/TITL)
    '''
    
    key: str = 'TITL'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Top(BaseStructure):
    '''Store, validate and format the TOP structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Top crop width
    > A number of pixels to not display from the top side of the image. See
    > `CROP` for more details.
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#nonNegativeInteger
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM TOP Structure](https://gedcom.io/terms/v7/TOP)
    '''
    
    key: str = 'TOP'
        
    def __init__(self, value: int, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Trlr(BaseStructure):
    '''Store, validate and format the TRLR structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Trailer
    > A pseudo-structure marking the end of a dataset. See [The Header and
    > Trailer] for more details.
        
    Args:
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM TRLR Structure](https://gedcom.io/terms/v7/TRLR)
    '''
    
    key: str = 'TRLR'
        
    def __init__(self, subs: Any = None) -> None:
        super().__init__(Default.EMPTY, subs, self.key)
    

class Type(BaseStructure):
    '''Store, validate and format the TYPE structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Type
    > A descriptive word or phrase used to further classify the superstructure.
    > 
    > When both a `NOTE` and free-text `TYPE` are permitted as substructures of the
    > same structure, the displaying systems should always display the `TYPE` value
    > when they display the data from the associated structure; `NOTE` will typically
    > be visible only in a detailed view.
    > 
    > `TYPE` must be used whenever the generic `EVEN`, `FACT` and `IDNO` tags are
    > used. It may also be used for any other event or attribute.
    > 
    > Using the subordinate `TYPE` classification method provides a further
    > classification of the superstructure but does not change its basic meaning.
    > 
    > <div class="example">
    > 
    > A `ORDN` with a `TYPE` could clarify what kind of ordination was performed:
    > 
    > ```gedcom
    > 0 @I1@ INDI
    > 1 ORDN
    > 2 TYPE Bishop
    > ```
    > 
    > This classifies the entry as an ordination as a bishop, which is still a
    > ordination event. The event could be further clarified with `RELI`, `DATE`, and
    > other substructures.
    > 
    > Other descriptor values might include, for example,
    > 
    > - "Stillborn" as a qualifier to `BIRT` (birth)
    > - "Civil" as a qualifier to `MARR` (marriage)
    > - "College" as a qualifier to `GRAD` (graduation)
    > - "Oral" as a qualifier to `WILL`
    > 
    > See also `FACT` and `EVEN` for additional examples.
    > 
    > </div>
    > 
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM TYPE Structure](https://gedcom.io/terms/v7/TYPE)
    '''
    
    key: str = 'TYPE'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Uid(BaseStructure):
    '''Store, validate and format the UID structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Unique Identifier
    > A globally-unique identifier of the superstructure, to be preserved across
    > edits. If a globally-unique identifier for the record already exists, it should
    > be used without modification, not even whitespace or letter case normalization.
    > New globally unique identifiers should be created and formatted as described in
    > [RFC 4122].
    > 
    > This is metadata about the structure itself, not data about its subject.
    > Multiple structures describing different aspects of the same subject would have
    > different `UID` values.
    > 
    > Because the `UID` identifies a structure, it can facilitate inter-tool
    > collaboration by distinguishing between a structure being edited and a new
    > structure being created. If an application allows structures to be edited in a
    > way that completely changes their meaning (e.g., changing all the contents of
    > an `INDI` record to have it describe a completely different person) then any
    > `UID`s should also be changed.
    > 
    > <div class="note">
    > 
    > Some systems used a 16-byte UUID with a custom 2-byte checksum for a total of
    > 18 bytes:
    > 
    > - checksum byte 1 = (sum of (byte~*i*~) for *i* 1 through 16) mod 256
    > - checksum byte 2 = (sum of ((16 − *i*) × (byte~*i*~)) for *i* 1 through 16)
    >   mod 256
    > 
    > Use of checksums for UIDs is discouraged except in cases where error-prone
    > input is expected and an appropriate action to take in case of an error is
    > known.
    > 
    > </div>
    > 
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM UID Structure](https://gedcom.io/terms/v7/UID)
    '''
    
    key: str = 'UID'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Vers(BaseStructure):
    '''Store, validate and format the VERS structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Version
    > An identifier that represents the version level assigned to the associated
    > product. It is defined and changed by the creators of the product.
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM VERS Structure](https://gedcom.io/terms/v7/VERS)
    '''
    
    key: str = 'VERS'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Width(BaseStructure):
    '''Store, validate and format the WIDTH structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Width in pixels
    > How many pixels to display horizontally for the image. See `CROP` for more
    > details.
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#nonNegativeInteger
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM WIDTH Structure](https://gedcom.io/terms/v7/WIDTH)
    '''
    
    key: str = 'WIDTH'
        
    def __init__(self, value: int, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Wife(BaseStructure):
    '''Store, validate and format the WIFE structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Wife
    > A container for information relevant to the subject of the superstructure
    > specific to the individual described by the associated `FAM`'s `WIFE`
    > substructure.
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
        
    Args:
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM WIFE Structure](https://gedcom.io/terms/v7/WIFE)
    '''
    
    key: str = 'WIFE'
        
    def __init__(self, subs: Any) -> None:
        super().__init__(Default.EMPTY, subs, self.key)
    

class Will(BaseStructure):
    '''Store, validate and format the WILL structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Will
    > An [Individual Event]. See also `INDIVIDUAL_EVENT_STRUCTURE`.
    > will
    > A legal document treated as an event, by which a person disposes of his or
    > her estate. It takes effect after death. The event date is the date the
    > will was signed while the person was alive. (See also `PROB`)
        
    Substructures:
    |               Specification                | Quantity | Required |
    | ------------------------------------------ | -------- | -------- |
    | https://gedcom.io/terms/v7/ADDR            | Many     | No       |
    | https://gedcom.io/terms/v7/AGE             | Many     | No       |
    | https://gedcom.io/terms/v7/AGNC            | Many     | No       |
    | https://gedcom.io/terms/v7/ASSO            | Many     | No       |
    | https://gedcom.io/terms/v7/CAUS            | Many     | No       |
    | https://gedcom.io/terms/v7/DATE            | Many     | No       |
    | https://gedcom.io/terms/v7/EMAIL           | Many     | No       |
    | https://gedcom.io/terms/v7/FAX             | Many     | No       |
    | https://gedcom.io/terms/v7/NOTE            | Many     | No       |
    | https://gedcom.io/terms/v7/OBJE            | Many     | No       |
    | https://gedcom.io/terms/v7/PHON            | Many     | No       |
    | https://gedcom.io/terms/v7/PLAC            | Many     | No       |
    | https://gedcom.io/terms/v7/RELI            | Many     | No       |
    | https://gedcom.io/terms/v7/RESN            | Many     | No       |
    | https://gedcom.io/terms/v7/SDATE           | Many     | No       |
    | https://gedcom.io/terms/v7/SNOTE           | Many     | No       |
    | https://gedcom.io/terms/v7/SOUR            | Many     | No       |
    | https://gedcom.io/terms/v7/TYPE            | Many     | No       |
    | https://gedcom.io/terms/v7/UID             | Many     | No       |
    | https://gedcom.io/terms/v7/WWW             | Many     | No       |
        
    Args:
        value: A value of data type Y|<NULL>
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM WILL Structure](https://gedcom.io/terms/v7/WILL)
    '''
    
    key: str = 'WILL'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    

class Www(BaseStructure):
    '''Store, validate and format the WWW structure. Generated by `Display.generate_class`.
    
    GEDCOM Specification:
    > Web address
    > A URL or other locator for a World Wide Web page of the subject of the
    > superstructure, as defined by any relevant standard such as [whatwg/url], [RFC
    > 3986], [RFC 3987], and so forth.
    > 
    > Like other substructures, the `WWW` structure provides details about the
    > subject of its superstructure. For example, a `MARR`.`WWW` is a world wide web
    > page of the marriage event, not the personal website of the couple or an entry
    > in an online database serving as a source documenting the marriage. However,
    > the meaning of `WWW` was only implicit when it was introduced in version 5.5.1
    > and many files were created that use `WWW` to store a more tangentially-related
    > web address, so applications are recommended to interpret the `WWW` structure's
    > meaning cautiously.
    > 
    > If an invalid or no longer existing web address is present upon import, it
    > should be preserved as-is on export.
    > 
        
    Args:
        value: A value of data type http://www.w3.org/2001/XMLSchema#string
        subs: A permitted substructure, an extension or list of permitted substructures or extensions.
        
    References:
    - [GEDCOM WWW Structure](https://gedcom.io/terms/v7/WWW)
    '''
    
    key: str = 'WWW'
        
    def __init__(self, value: str, subs: Any = None) -> None:
        super().__init__(value, subs, self.key)
    