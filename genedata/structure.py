# structure.py
"""Store, validate and display GEDCOM files."""

__all__ = [
    'ExtensionAttributes',
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
from typing import Any, Literal, NamedTuple, Self

from genedata.constants import Default
from genedata.messages import Msg
from genedata.methods import Names, Tagger, Validate
from genedata.specifications70 import Specs

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
        return f"ExtensionXref('{self.fullname}')"


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
        tag: str = Default.EMPTY,
        supers: int = 0,
        permitted: list[str] | None = None,
        required: list[str] | None = None,
        single: list[str] | None = None,
        enumset_key: str = Default.EMPTY,
        enum_tags: list[str] | None = None,
        payload: str = Default.EMPTY,
        class_name: str = Default.EMPTY,
    ):
        # Process value argument
        self.value: str | int | Xref | None = value
        self.payload: str = payload
        if isinstance(self.value, str):
            self.value = Validate.clean_value(self.value, self.payload)
        self.code_value: str = Default.EMPTY
        if isinstance(self.value, str):
            self.code_value = Names.quote_text(self.value)
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
        self.tag: str = tag
        if permitted is None:
            permitted = []
        if required is None:
            required = []
        if single is None:
            single = []
        if enum_tags is None:
            enum_tags = []
        self.supers: int = supers
        self.permitted: list[str] = permitted
        self.required: list[str] = required
        self.single: list[str] = single
        self.enumset_key: str = enumset_key
        self.enum_tags: list[str] = enum_tags
        self.class_name: str = class_name
        if len(self.enum_tags) > 0 and isinstance(self.value, str):
            self.value = self.value.upper()
            self.code_value = f"'{self.value}'"

        # Identify which cross reference identifier opened the record.
        self.originator: Xref = Void.XREF

    def validate(self, specs: dict[str, dict[str, Any]] = Specs) -> bool:
        """Validate the stored value."""

        # Does it have all required substructures?
        for name in self.required:
            if name not in self.counted:
                raise ValueError(
                    Msg.MISSING_REQUIRED.format(self.required, self.class_name)
                )

        # Does a single substructure appear only once?
        for name in self.single:
            if name in self.counted and self.counted[name] > 1:
                raise ValueError(
                    Msg.ONLY_ONE_PERMITTED.format(name, self.class_name)
                )

        # Are there substructures not in the permitted list of substructures?
        for name in self.counted:
            if name not in self.permitted:
                raise ValueError(
                    Msg.NOT_PERMITTED.format(
                        name, self.permitted, self.class_name
                    )
                )

        # Does the value have the required data type?
        match self.payload:
            # Verify the value is a string.
            case 'http://www.w3.org/2001/XMLSchema#string':
                # A shared note has its text incorporated in the SharedNoteXref,
                # so just verify that the value is a SharedNoteXref.
                if self.key == 'record-SNOTE':
                    if not isinstance(self.value, SharedNoteXref):
                        raise ValueError(
                            Msg.NOT_SHARED_NOTE_XREF.format(
                                repr(self.value), self.class_name
                            )
                        )

                # If the value is not an instance of SharedNoteXref, check that it is a string.
                else:
                    return Validate.string(self.value, self.class_name)

            # Verify that the value is either `Y` or `''`, but not ``.
            case 'Y|<NULL>':
                return Validate.y_or_null(self.value, self.class_name)

            # Verify that the value is a non-negative integer.
            case 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger':
                return Validate.non_negative_integer(
                    self.value, self.class_name
                )

            # Verify a value is in the enumeration set.
            # Do this also for a list of enumberation values.
            case (
                'https://gedcom.io/terms/v7/type-Enum'
                | 'https://gedcom.io/terms/v7/type-List#Enum'
            ):
                return Validate.enum(
                    self.value,
                    self.class_name,
                    self.enum_tags,
                    self.enumset_key,
                    specs,
                )
                # if Validate.string(self.value, self.class_name) and isinstance(
                #     self.value, str
                # ):
                #     for value in self.value.split(Default.LIST_ITEM_SEPARATOR):
                #         if not Validate.enum(value, self.class_name, self.enum_tags, self.enumset_key, specs):
                #             return False
                #     return True

            # Verify a value is in the enumeration set.
            # case 'https://gedcom.io/terms/v7/type-Enum':
            #     return Validate.enum(
            #         self.value,
            #         self.class_name,
            #         self.enum_tags,
            #         self.enumset_key,
            #         specs,
            #     )

            # Verify that the value is an instance of IndividualXref.
            case '@<https://gedcom.io/terms/v7/record-INDI>@':
                if not isinstance(self.value, IndividualXref):
                    raise ValueError(
                        Msg.NOT_INDIVIDUAL_XREF.format(
                            str(self.value), self.class_name
                        )
                    )

            # Verify that the value is an instance of FamilyXref.
            case '@<https://gedcom.io/terms/v7/record-FAM>@':
                if not isinstance(self.value, FamilyXref):
                    raise ValueError(
                        Msg.NOT_FAMILY_XREF.format(
                            str(self.value), self.class_name
                        )
                    )

            # Verify the value is a listing with items separated by `, `.
            case 'https://gedcom.io/terms/v7/type-List#Text':
                return Validate.listing(self.value, self.class_name)

            # Verify that the value is an instance of SubmitterXref.
            case '@<https://gedcom.io/terms/v7/record-SUBM>@':
                if not isinstance(self.value, SubmitterXref):
                    raise ValueError(
                        Msg.NOT_SUBMITTER_XREF.format(
                            str(self.value), self.class_name
                        )
                    )

            # Verify the value meets the language specification.
            case 'http://www.w3.org/2001/XMLSchema#Language':
                return Validate.language(self.value, self.class_name)

            # Verify the value meets the date period specifications
            case 'https://gedcom.io/terms/v7/type-Date#period':
                return Validate.date_period(self.value, self.class_name, specs)

            # Verify the value meets the date exact specifications.
            case 'https://gedcom.io/terms/v7/type-Date#exact':
                return Validate.date_exact(self.value, self.class_name)

            # Verify the value meets the general date specifications.
            case 'https://gedcom.io/terms/v7/type-Date':
                return Validate.date(self.value, self.class_name, specs)

            # Verify the value meets the file path specifications.
            case 'https://gedcom.io/terms/v7/type-FilePath':
                return Validate.filepath(self.value, self.class_name)

            # Verify the value meets the personal name specifications.
            case 'https://gedcom.io/terms/v7/type-Name':
                return Validate.name(self.value, self.class_name)

            # Verify that the value meets the age specifications.
            case 'https://gedcom.io/terms/v7/type-Age':
                return Validate.age(self.value, self.class_name)

            # Verify the media type meets the specifications.
            case 'http://www.w3.org/ns/dcat#mediaType':
                return Validate.mediatype(self.value, self.class_name)

            # Verify that the value is an instance of MultimediaXref.
            case '@<https://gedcom.io/terms/v7/record-OBJE>@':
                if not isinstance(self.value, MultimediaXref):
                    raise ValueError(
                        Msg.NOT_MULTIMEDIA_XREF.format(
                            repr(self.value), self.class_name
                        )
                    )

            # Verify that the value is an instance of RepositoryXref.
            case '@<https://gedcom.io/terms/v7/record-REPO>@':
                if not isinstance(self.value, RepositoryXref):
                    raise ValueError(
                        Msg.NOT_REPOSITORY_XREF.format(
                            repr(self.value), self.class_name
                        )
                    )

            # Verify that the value is an instance of SharedNoteXref.
            case '@<https://gedcom.io/terms/v7/record-SNOTE>@':
                if not isinstance(self.value, SharedNoteXref):
                    raise ValueError(
                        Msg.NOT_SHARED_NOTE_XREF.format(
                            repr(self.value), self.class_name
                        )
                    )

            # Verify that the value is an instance of SourceXref.
            case '@<https://gedcom.io/terms/v7/record-SOUR>@':
                if not isinstance(self.value, SourceXref):
                    raise ValueError(
                        Msg.NOT_SOURCE_XREF.format(
                            repr(self.value), self.class_name
                        )
                    )

            # Verify that the data type meets the time specifications.
            case 'https://gedcom.io/terms/v7/type-Time':
                return Validate.time(self.value, self.class_name)

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
                if isinstance(self.value, str) and self.value[0] not in [
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
                if isinstance(self.value, str) and (
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
                if isinstance(self.value, str) and self.value[0] not in [
                    Default.LONG_EAST,
                    Default.LONG_WEST,
                ]:
                    raise ValueError(
                        Msg.LONG_EAST_WEST.format(
                            self.value[0],
                            self.value,
                            Default.LONG_EAST,
                            Default.LONG_WEST,
                            self.class_name,
                        )
                    )
                if isinstance(self.value, str) and (
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
            case 'Tag':
                if isinstance(self.value, str):
                    tag_list: list[str] = self.value.split(Default.SPACE)
                    if len(tag_list) != 2:
                        raise ValueError(
                            Msg.TAG_SPACES.format(
                                self.value, str(len(tag_list))
                            )
                        )

        # Check if all subs validate.
        if self.subs is not None:
            if isinstance(self.subs, list):
                for sub in self.subs:
                    sub.validate(specs=specs)
            else:
                self.subs.validate(specs=specs)
        return True

    def ged(
        self,
        level: int = 1,
        format: bool = True,
        recordkey: Xref = Void.XREF,
        specs: dict[str, dict[str, Any]] = Specs,
    ) -> str:
        """Generate the GEDCOM lines."""
        if self.validate(specs=specs):
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
                # if order:
                #     lines = Tagger.structure(
                #         lines,
                #         level + 1,
                #         Tagger.order(self.subs),
                #         recordkey=recordkey,
                #     )
                # else:
                lines = Tagger.structure(
                    lines, level + 1, self.subs, recordkey=recordkey
                )
            else:
                lines = Tagger.structure(
                    lines, level + 1, self.subs, recordkey=recordkey
                )
        # if self.tag == 'HEAD':
        #     lines = lines.replace('0 HEAD\n', '0 HEAD\n1 GEDC\n2 VERS 7.0\n')
        return lines  # .replace('0 TRLR\n', '0 TRLR')

    def code(
        self,
        tabs: int = 0,
        no_indent: bool = False,
        as_name: str = Default.EMPTY,
    ) -> str:
        """Generate a formatted code that can be evaluated of the class."""
        class_name: str = self.class_name
        if as_name != Default.EMPTY:
            class_name = f'{as_name}.{self.class_name}'
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
                    class_name,
                    Default.PARENS_LEFT,
                ]
            )
        else:
            code_lines = ''.join(
                [
                    initial,
                    class_name,
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
                    self.subs.code(no_indent=True, as_name=as_name),
                    Default.PARENS_RIGHT,
                ]
            )
        if not isinstance(self.subs, list):
            return ''.join(
                [
                    code_lines,
                    Default.COMMA,
                    Default.SPACE,
                    self.subs.code(no_indent=True, as_name=as_name),
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
                        sub.code(tabs + 2, as_name=as_name),
                        # Default.EOL,
                    ]
                )
            else:
                code_lines = ''.join(
                    [
                        code_lines,
                        sub.code(tabs + 2, as_name=as_name),
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


class ExtensionAttributes(NamedTuple):
    id: int = 0
    key: str = Default.EMPTY
    tag: str = Default.EMPTY
    yaml_file: str = Default.EMPTY
    yaml_type: str = Default.EMPTY
    supers: int = 0
    payload: str = Default.EMPTY
    required: list[str] | None = None
    single: list[str] | None = None
    permitted: list[str] | None = None
    enumset_key: str = Default.EMPTY
    enum_tags: list[str] | None = None


class Ext(BaseStructure):
    """Store, validate and format an extension structure."""

    def __init__(
        self, attributes: ExtensionAttributes, value: str, subs: SubsType
    ):
        super().__init__(
            value=value,
            subs=subs,
            key=attributes.key,
            tag=attributes.tag,
            supers=attributes.supers,
            permitted=attributes.permitted,
            required=attributes.required,
            single=attributes.single,
            enumset_key=attributes.enumset_key,
            enum_tags=attributes.enum_tags,
            payload=attributes.payload,
            class_name='Ext',
        )
