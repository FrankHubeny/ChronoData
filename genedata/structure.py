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
    'Void',
]

import collections
import contextlib
import io
import logging
import re
import urllib.request
from enum import Enum
from pathlib import Path
from textwrap import indent
from typing import Any, Literal, NamedTuple, Self

import yaml  # type: ignore[import-untyped]

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
from genedata.util import Checker, Formatter, Tagger

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
        self.xrefs: list[Xref] = []

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

        # Identify which cross reference identifier started opened the record.
        self.originator: Xref = Void.XREF

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

    def ged(
        self,
        level: int = 1,
        format: bool = True,
        recordkey: Xref = Void.XREF,
        order: bool = False,
    ) -> str:
        """Generate the GEDCOM lines."""
        if self.validate():
            lines: str = Default.EMPTY
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
            
            # Adjust format and recordkey if necessary.
            if isinstance(self.value, Xref):
                format = False
                if self.key[0:6] == 'record':
                    recordkey = self.value
                elif recordkey in self.value.xrefs:
                    logging.info(Msg.CIRCULAR.format(repr(self.value), repr(recordkey)))
                    # raise ValueError(
                    #     Msg.CIRCULAR.format(repr(self.value), repr(recordkey))
                    # )
                if level > 0:
                    recordkey.xrefs.append(self.value)

            # Construct the ged lines for self.value.
            if self.value == Default.EMPTY:
                lines = Tagger.empty(
                    lines, level, self.tag
                )
            elif isinstance(self.value, Xref) and level == 0:
                lines = self.value.ged()
            else:
                lines = Tagger.string(
                    lines,
                    level,
                    self.tag,
                    str(self.value),
                    format=format,
                )

            # Check for circularity of cross reference use.
            # if isinstance(self.value, Xref) and level > 0:
            #     if recordkey in self.value.xrefs:
            #         raise ValueError(Msg.CIRCULAR.format(repr(self.value), repr(recordkey)))
            #     recordkey.xrefs.append(self.value)

            # Construct the ged lines for any substructures.
            if isinstance(self.subs, list):
                if order:
                    lines = Tagger.structure(
                        lines,
                        level + 1,
                        Tagger.order(self.subs),
                        recordkey=recordkey,
                    )
                else:
                    lines = Tagger.structure(
                        lines, level + 1, self.subs, recordkey=recordkey
                    )
            else:
                lines = Tagger.structure(
                    lines, level + 1, self.subs, recordkey=recordkey
                )
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
