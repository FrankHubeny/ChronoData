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
import io
import re
import urllib.request
from typing import Any, Literal, Self

import yaml  # type: ignore[import-untyped]

from genedata.constants import Default
from genedata.messages import Msg
from genedata.specs7 import (
    Enumeration,
    EnumerationSet,
    ExtensionStructure,
    Structure,
)
from genedata.methods import Tagger

AnyList = Any | list[Any] | None
FloatNone = float | None
IntNone = int | None
StrList = str | list[str] | None
SubsType = Any | list[Any] | None
YNull = Literal['Y'] | None


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

    def __init__(self, name: str, exttag: str = Default.TAG_EXT):
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

    def __init__(self, name: str, tag: str = Default.TAG_FAM):
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

    def __init__(self, name: str, tag: str = Default.TAG_INDI):
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

    def __init__(self, name: str, tag: str = Default.TAG_OBJE):
        super().__init__(name, tag)
        self.records: list[Any] = []

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

    def __init__(self, name: str, tag: str = Default.TAG_REPO):
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
        self, name: str, text: str = Default.EMPTY, tag: str = Default.TAG_SNOTE
    ):
        super().__init__(name, tag, text=text)

    def code(self, tabs: int = 0) -> str:  # noqa: ARG002
        text: str = f"'{self.text}'"
        if Default.QUOTE_SINGLE in self.text:
            text = f'"{self.text}"'
        if Default.EOL in self.text:
            if Default.QUOTE_SINGLE in self.text:
                text = f'"""{self.text}"""'
            else:
                text = f"'''{self.text}'''"
        return f"SharedNoteXref('{self.fullname}', {text})"

    def __repr__(self) -> str:
        return self.code()


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

    def __init__(self, name: str, tag: str = Default.TAG_SOUR):
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

    def __init__(self, name: str, tag: str = Default.TAG_SUBM):
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
        value: str | int | Xref | None = None,
        subs: Self | list[Self] | None = None,
        key: str = Default.EMPTY,
    ):
        # Process value argument
        self.value: str | int | Xref | None = value
        self.code_value: str = Default.EMPTY
        if isinstance(self.value, str):
            if Default.EOL in self.value:
                if Default.QUOTE_SINGLE in self.value:
                    self.code_value = f'"""{self.value}"""'
                else:
                    self.code_value = f"'''{self.value}'''"
            elif Default.QUOTE_SINGLE in self.value:
                self.code_value = f'"{self.value}"'
            else:
                self.code_value = f"'{self.value}'"
        elif isinstance(self.value, int):
            self.code_value = str(self.value)
        elif isinstance(self.value, Xref):
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
        self.enum_key: str = Default.EMPTY
        self.enum_tags: list[str] = []
        if (
            Default.YAML_ENUM_KEY in Structure[self.key]
            and Structure[self.key][Default.YAML_ENUM_KEY] != Default.EMPTY
        ):
            self.enum_key = Structure[self.key][Default.YAML_ENUM_KEY]
            self.enum_tags = EnumerationSet[self.enum_key][
                Default.YAML_ENUM_TAGS
            ]
        if len(self.enum_tags) > 0 and isinstance(self.value, str):
            self.value = self.value.upper()
            self.code_value = f"'{self.value}'"
        self.payload: str | None = Structure[self.key][Default.YAML_PAYLOAD]
        self.class_name: str = (
            self.key.title().replace('_', '').replace('-', '')
        )
        self.class_name = f'{Default.CODE_CLASS}.{self.class_name}'

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
            case 'https://gedcom.io/terms/v7/type-List#Enum':
                if not isinstance(self.value, str):
                    raise ValueError(
                        Msg.NOT_STRING.format(repr(self.value), self.class_name)
                    )
                for value in self.value.split(','):
                    if value.strip() not in self.enum_tags:
                        raise ValueError(
                            Msg.NOT_VALID_ENUM.format(
                                self.value, self.enum_tags, self.class_name
                            )
                        )
            case 'https://gedcom.io/terms/v7/type-Enum':
                if not isinstance(self.value, str):
                    raise ValueError(
                        Msg.NOT_STRING.format(repr(self.value), self.class_name)
                    )
                if self.value not in self.enum_tags:
                    raise ValueError(
                        Msg.NOT_VALID_ENUM.format(
                            self.value, self.enum_tags, self.class_name
                        )
                    )
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
                        Msg.NOT_LIST.format(str(self.value), self.class_name)
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
                        Msg.NOT_LANGUAGE.format(self.value, self.class_name)
                    )
            case 'https://gedcom.io/terms/v7/type-Date#period':
                if not isinstance(self.value, str):
                    raise ValueError(
                        Msg.NOT_STRING.format(repr(self.value), self.class_name)
                    )
                if not re.match('^TO|^FROM', self.value) or re.match(
                    '[a-z]', self.value
                ):
                    raise ValueError(
                        Msg.NOT_DATE_PERIOD.format(self.value, self.class_name)
                    )
            case 'https://gedcom.io/terms/v7/type-Date#exact':
                if not isinstance(self.value, str):
                    raise ValueError(
                        Msg.NOT_STRING.format(repr(self.value), self.class_name)
                    )
                if (
                    re.search('[a-z]', self.value) is not None
                    or re.search('[0-9]', self.value) is None
                    or len(re.findall(' ', self.value)) != 2
                ):
                    raise ValueError(
                        Msg.NOT_DATE_EXACT.format(self.value, self.class_name)
                    )
            case 'https://gedcom.io/terms/v7/type-Date':
                if not isinstance(self.value, str):
                    raise ValueError(
                        Msg.NOT_STRING.format(repr(self.value), self.class_name)
                    )
                if (
                    re.search('[a-z]', self.value) is not None
                    or re.search('[0-9]', self.value) is None
                ):
                    raise ValueError(Msg.NOT_DATE.format(self.value))
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
                if not len(re.findall('/', self.value)) == 2:
                    raise ValueError(
                        Msg.NOT_NAME.format(self.value, self.class_name)
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
                        Msg.NOT_MEDIA_TYPE.format(self.value, self.class_name)
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
            case 'gc.Lati':
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
            case 'gc.Long':
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
                f'{Default.CODE_CLASS}.Head',
                f'{Default.CODE_CLASS}.RecordFam',
                f'{Default.CODE_CLASS}.RecordIndi',
                f'{Default.CODE_CLASS}.RecordObje',
                f'{Default.CODE_CLASS}.RecordRepo',
                f'{Default.CODE_CLASS}.RecordSnote',
                f'{Default.CODE_CLASS}.RecordSour',
                f'{Default.CODE_CLASS}.RecordSubm',
            ]:
                level = 0

            # Adjust format and recordkey if necessary.
            if isinstance(self.value, Xref):
                format = False
                if self.key[0:6] == 'record':
                    recordkey = self.value
                elif (
                    (
                        isinstance(recordkey, SourceXref)
                        and isinstance(self.value, SharedNoteXref)
                    )
                    or (
                        isinstance(recordkey, SharedNoteXref)
                        and isinstance(self.value, SourceXref)
                    )
                ) and recordkey in self.value.xrefs:
                    raise ValueError(
                        Msg.CIRCULAR.format(repr(self.value), repr(recordkey))
                    )
                if level > 0:
                    recordkey.xrefs.append(self.value)

            # Construct the ged lines for self.value.
            if self.value == Default.EMPTY or self.value is None:
                lines = Tagger.empty(lines, level, self.tag)
            elif isinstance(self.value, Xref) and level == 0:
                lines = self.value.ged()
            # elif isinstance(self.value, Xref):
            #     lines = self.value.fullname
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

    def code(self, tabs: int = 0, no_indent: bool = False) -> str:
        """Generate a formatted code that can be evaluated of the class."""
        indent: str = Default.INDENT * tabs
        indent_plus_one: str = Default.INDENT * (tabs + 1)
        initial: str = indent
        if initial == Default.EMPTY:
            initial = Default.EOL
        if no_indent:
            initial = Default.EMPTY
        code_lines: str = Default.EMPTY
        if self.value is None:
            code_lines = ''.join(
                [
                    initial,
                    self.class_name,
                    Default.PARENS_LEFT,
                ]
            )
        else:
            code_lines = ''.join(
                [
                    initial,
                    self.class_name,
                    Default.PARENS_LEFT,
                    self.code_value,
                ]
            )
        if self.subs is None:
            return ''.join([code_lines, Default.PARENS_RIGHT])
        if not isinstance(self.subs, list) and self.value is None:
            return ''.join(
                [
                    code_lines,
                    self.subs.code(no_indent=True),
                    Default.PARENS_RIGHT,
                ]
            )
        if not isinstance(self.subs, list):
            return ''.join(
                [
                    code_lines,
                    Default.COMMA,
                    Default.SPACE,
                    self.subs.code(no_indent=True),
                    Default.PARENS_RIGHT,
                    # Default.COMMA,
                ]
            )
        if self.value is not None:
            code_lines = ''.join([code_lines, Default.COMMA])
        code_lines = ''.join(
            [
                code_lines,
                Default.EOL,
                indent_plus_one,
                Default.BRACKET_LEFT,
                Default.EOL,
            ]
        )
        for index, sub in enumerate(self.subs):
            if index > 0:
                code_lines = ''.join(
                    [
                        code_lines,
                        Default.COMMA,
                        Default.EOL,
                        sub.code(tabs + 2),
                        # Default.EOL,
                    ]
                )
            else:
                code_lines = ''.join(
                    [
                        code_lines,
                        sub.code(tabs + 2),
                        # Default.EOL,
                    ]
                )
        code_lines = ''.join(
            [
                code_lines,
                Default.COMMA,
                Default.EOL,
            ]
        )
        return ''.join(
            [
                code_lines,
                indent_plus_one,
                Default.BRACKET_RIGHT,
                Default.EOL,
                Default.PARENS_RIGHT,
            ]
        )


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
            yamldict[Default.YAML_ENUM_TAGS] = enums
            self.tag = yamldict[Default.YAML_EXTENSION_TAGS][0]
            self.permitted = yamldict[Default.YAML_PERMITTED]
            self.required = yamldict[Default.YAML_REQUIRED]
            self.single = yamldict[Default.YAML_SINGULAR]
            self.enums = yamldict[Default.YAML_ENUM_TAGS]
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
            self.enums = ExtensionStructure[self.key][Default.YAML_ENUM_TAGS]
            self.payload = ExtensionStructure[self.key][Default.YAML_PAYLOAD]
            # self.class_name: str = (
            #     self.key.title().replace('_', '').replace('-', '')
            # )
