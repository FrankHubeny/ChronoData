# genedata/tuples.py
# Licensed under a 3-clause BSD style license - see LICENSE.md
"""NamedTuples to store, validate and display data
entered by the user for a genealogy.

The NamedTuples are based on the GEDCOM standard with others
added to aid the user in collecting the data.

Each of the NamedTuples have two methods:
    validate: Return True if the data can be used or
        an error message otherwise.
    ged: Display the data in the GEDCOM format.

Examples:


"""

__all__ = [
    'WWW',
    'Address',
    'Age',
    'Alias',
    'Association',
    'CallNumber',
    'ChangeDate',
    'Checker',
    'Child',
    'CreationDate',
    'Date',
    'Dater',
    'Email',
    'EventDetail',
    'ExtTag',
    'Family',
    'FamilyAttribute',
    'FamilyChild',
    'FamilyEvent',
    'FamilyEventDetail',
    'FamilySpouse',
    'FamilyXref',
    'Fax',
    'File',
    'FileTranslation',
    'Formatter',
    'Header',
    'Identifier',
    'Individual',
    'IndividualAttribute',
    'IndividualEvent',
    'IndividualEventDetail',
    'IndividualXref',
    'LDSIndividualOrdinance',
    'LDSOrdinanceDetail',
    'LDSSpouseSealing',
    'Lang',
    'Map',
    'Multimedia',
    'MultimediaLink',
    'MultimediaXref',
    'NameTranslation',
    'NonEvent',
    'Note',
    'NoteTranslation',
    'PersonalName',
    'PersonalNamePieces',
    'Phone',
    'Phrase',
    'Place',
    'PlaceTranslation',
    'Placer',
    'Repository',
    'RepositoryXref',
    'SDate',
    'SharedNote',
    'SharedNoteXref',
    'Source',
    'SourceCitation',
    'SourceData',
    'SourceDataEvent',
    'SourceRepositoryCitation',
    'SourceXref',
    'Submitter',
    'SubmitterXref',
    'Tagger',
    'Text',
    'Time',
    'Void',
]


import contextlib
import logging
import math
import re
import urllib.request
from pathlib import Path
from textwrap import indent
from typing import Any, Literal, NamedTuple

import numpy as np
import yaml  # type: ignore[import-untyped]

# from icecream import ic  # type: ignore[import-not-found]
from ordered_set import OrderedSet  # type: ignore[import-not-found]

from calendars.calendars import CalendarDefinition

# from calendars.french_revolution_calendars import CalendarsFrenchRevolution
from calendars.gregorian_calendars import CalendarsGregorian

# from calendars.hebraic_calendars import CalendarsHebraic
# from calendars.julian_calendars import CalendarsJulian
from genedata.constants import (
    Cal,
    CalendarName,
    String,
)
from genedata.gedcom import (
    Adop,
    Config,
    Default,
    Even,
    EvenAttr,
    FamAttr,
    FamcStat,
    FamEven,
    Id,
    IndiAttr,
    IndiEven,
    Medium,
    NameType,
    OverView,
    Pedi,
    Quay,
    Resn,
    Role,
    Sex,
    Stat,
    StdTag,
    Tag,
    TagTuple,
)
from genedata.messages import Example, Msg

AnyList = Any | list[Any] | None
FloatNone = float | None
StrList = str | list[str] | None
YNull = Literal['Y'] | None


class TagData:
    """File and internet access for tag and extension tag specifications."""

    @staticmethod
    def get(tag: str = Default.EMPTY, url: str = Default.EMPTY) -> TagTuple:
        if url[0:4] == 'http':
            webUrl = urllib.request.urlopen(url)
            result_code = str(webUrl.getcode())
            if result_code == '404':
                raise ValueError(Msg.PAGE_NOT_FOUND.format(url))
            raw: str = webUrl.read().decode('utf-8')
        else:
            with Path.open(Path(url)) as file:
                raw = file.read()
        raw2: str = raw[raw.find('%YAML') :]
        yaml_data: str = raw2[: raw2.find('...')]
        yamldict: dict[str, Any] = yaml.safe_load(yaml_data)
        lang: str = Default.EMPTY
        with contextlib.suppress(Exception):
            lang = yamldict['lang']
        type: str = Default.EMPTY
        with contextlib.suppress(Exception):
            type = yamldict['type']
        uri: str = Default.EMPTY
        with contextlib.suppress(Exception):
            uri = yamldict['uri']
        standard_tag: str = Default.EMPTY
        with contextlib.suppress(Exception):
            standard_tag = yamldict['standard tag']
        specification: str = Default.EMPTY
        with contextlib.suppress(Exception):
            specification = yamldict['specification']
        label: str = Default.EMPTY
        with contextlib.suppress(Exception):
            label = yamldict['label']
        payload: str = Default.EMPTY
        with contextlib.suppress(Exception):
            payload = yamldict['payload']
        substructures: dict[str, str] = {}
        subs: list[str] = []
        required: list[str] = []
        single: list[str] = []
        with contextlib.suppress(Exception):
            substructures = yamldict['substructures']
        if substructures != {} and substructures is not None:
            for key, dictvalue in substructures.items():
                name = key[key.rfind('/') + 1 :]
                subs.append(name)
                if dictvalue[0:3] == '{1:':
                    required.append(name)
                if dictvalue[2:5] == ':1}':
                    single.append(name)
        superstructures: dict[str, str] = {}
        supers: list[str] = []
        with contextlib.suppress(Exception):
            superstructures = yamldict['superstructures']
        if superstructures != {} and superstructures is not None:
            supers = [
                super_name[super_name.rfind('/') + 1 :]
                for super_name in superstructures
            ]
        value_of: dict[str, str] = {}
        with contextlib.suppress(Exception):
            value_of = yamldict['value of']
        enumsets: list[str] = [
            enum_name[enum_name.rfind('-') + 1 :] for enum_name in value_of
        ]
        contact: str = Default.EMPTY
        with contextlib.suppress(Exception):
            contact = yamldict['contact']
        value: str = Default.EMPTY
        if tag != Default.EMPTY:
            if tag[0] != Default.UNDERLINE:
                value = ''.join([Default.UNDERLINE, tag.upper()])
            else:
                value = tag.upper()
        elif standard_tag != Default.EMPTY:
            value = standard_tag
        else:
            raise ValueError(Msg.UNKNOWN_TAG.format(url))
        kind: str = Default.KIND_STANDARD
        if tag != Default.EMPTY:
            kind = Default.KIND_EXTENDED
        return TagTuple(
            value=value,
            kind=kind,
            supers=supers,
            subs=subs,
            required=required,
            single=single,
            enumsets=enumsets,
            lang=lang,
            type=type,
            uri=uri,
            standard_tag=standard_tag,
            specification=specification,
            label=label,
            payload=payload,
            substructures=substructures,
            superstructures=superstructures,
            value_of=value_of,
            contact=contact,
            yamldict=yamldict,
        )

    @staticmethod
    def generate() -> None:
        """This method generates definitions for the `StdTag` class used to check extensions."""
        for tag in Tag:
            with contextlib.suppress(Exception):
                print(  # noqa: T201
                    TagData.get(url=f'{Config.TERMS}{tag.name}').show()
                )


class ExtTag:
    """Store, validate and display extension tag information.

    An underline is added to the front of the new tag if one is not there already.
    Also the tag is made upper case.

    This class holds multiple extension tags identified in the header record.  It is not a separate
    GEDCOM structure.

    Examples:
        Consider making a _DATE extention tag based on the GEDCOM specification for
        the standard DATE tag.
        >>> from genedata.store import ExtTag
        >>> date = ExtTag('date', 'https://gedcom.io/terms/v7/DATE')
        >>> print(date.ged(1))
        2 TAG _DATE https://gedcom.io/terms/v7/DATE
        <BLANKLINE>

        We can put this into the header record as an extension tag as follows.
        >>> from genedata.store import Header
        >>> header = Header(exttags=[date])
        >>> print(header.ged())
        0 HEAD
        1 GEDC
        2 VERS 7.0
        1 SCHMA
        2 TAG _DATE https://gedcom.io/terms/v7/DATE
        <BLANKLINE>

    Args:
        tag: The tag used for the schema information.
        url: The required url defining the payload of the tag.  This url will be accessed
            and its contents stored.  It will be used to check the proper placement
            of the extension tag.

    See Also:
        `Header`
        `Extension`

    Returns:
        A string representing a GEDCOM line for this tag.

    Reference:
        [GENCOM Extensions](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#extensions)

    >  +1 SCHMA                                 {0:1}  [g7:SCHMA](https://gedcom.io/terms/v7/SCHMA)
    >     +2 TAG <Special>                      {0:M}  [g7:TAG](https://gedcom.io/terms/v7/TAG)
    """

    def __init__(self, tag: str, url: str = Default.EMPTY) -> None:
        self.url: str = url
        self.stdtag: StdTag
        try:
            self.stdtag = eval(''.join(['StdTag.', tag]))
            self.tag: TagTuple = self.stdtag.value
        except AttributeError:
            if url == Default.EMPTY and tag != Default.EMPTY:
                raise ValueError(Msg.UNDOCUMENTED) from None
            self.tag = TagData.get(tag, url)
        self.value: str = self.tag.value
        self.supers: list[str] | None = self.tag.supers
        self.subs: list[str] | None = self.tag.subs
        self.enumsets: list[str] | None = self.tag.enumsets

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
                lines, level + 1, Tag.TAG, self.value, str(self.url)
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
        tag: Tag | ExtTag,
        payload: str = Default.EMPTY,
        extra: str = Default.EMPTY,
        format: bool = True,
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
            >>> from genedata.gedcom import Tag
            >>> from genedata.store import Tagger
            >>> print(Tagger.taginfo(1, Tag.NAME, '  Some Name'))
            1 NAME   Some Name
            <BLANKLINE>

            There can also be an extra parameter.
            >>> print(Tagger.taginfo(1, Tag.NAME, 'SomeName', 'Other info'))
            1 NAME SomeName Other info
            <BLANKLINE>

            This example comes from the [GEDCOM lines standard](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#lines):
            Note how the `@me` was reformatted as `@@me`.
            > 1 NOTE me@example.com is my email
            > 2 CONT @@me and @I are my social media handles
            >>> from genedata.store import Note
            >>> mynote = Note(
            ...     note='''me@example.com is my email
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
        if extra == Default.EMPTY:
            if lineval == Default.EMPTY:
                return f'{level} {tag.value}{Default.EOL}'
            return f'{level} {tag.value} {Tagger.clean_input(lineval)}{Default.EOL}'
        return f'{level} {tag.value} {Tagger.clean_input(lineval)} {Tagger.clean_input(extra)}{Default.EOL}'

    @staticmethod
    def empty(lines: str, level: int, tag: Tag) -> str:
        """Join a GEDCOM line that has only a level and a tag to a string.

        This method implements the
        [GEDCOM empty LineVal standard](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#lines) which reads:
        > Note that production LineVal does not match the empty string.
        > Because empty payloads and missing payloads are considered equivalent,
        > both a structure with no payload and a structure with the empty string
        > as its payload are encoded with no LineVal and no space after the Tag.

        Example:
            >>> from genedata.store import Tagger
            >>> from genedata.gedcom import Tag
            >>> lines = ''
            >>> line = Tagger.empty(lines, 1, Tag.MAP)
            >>> print(line)
            1 MAP
            <BLANKLINE>

        Args:
            lines: The prefix of the returned string.
            level: The GEDCOM level of the structure.
            tag: The tag to apply to this line.

        """
        return ''.join([lines, Tagger.taginfo(level, tag)])

    @staticmethod
    def string(
        lines: str,
        level: int,
        tag: Tag | ExtTag,
        payload: list[str] | str | None,
        extra: str = Default.EMPTY,
        format: bool = True,
    ) -> str:
        """Join a string or a list of string to GEDCOM lines.

        This method hides the concatenation of the already constructed
        GEDCOM file with the new line and the check that this should only
        be done if the payload is not empty.  It also hides checking
        whether the string is part of a list or not.

        Examples:
            Suppose there is only one string that should be tagged.
            >>> from genedata.store import Tagger
            >>> lines = ''
            >>> lines = Tagger.empty(lines, 1, Tag.MAP)
            >>> lines = Tagger.string(lines, 2, Tag.LATI, 'N30.0')
            >>> lines = Tagger.string(lines, 2, Tag.LONG, 'W30.0')
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
            >>> lines = Tagger.string(lines, 3, Tag.WWW, wwws)
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
        """

        if payload is None:
            return lines
        if isinstance(payload, list):
            for item in payload:
                if Default.EOL in item:
                    items: list[str] = item.split(Default.EOL)
                    lines = Tagger.string(
                        lines, level, tag, items[0], format=format
                    )
                    lines = Tagger.string(
                        lines, level + 1, Tag.CONT, items[1:], format=format
                    )
                else:
                    lines = ''.join(
                        [lines, Tagger.taginfo(level, tag, item, format=format)]
                    )
            return lines
        if payload != Default.EMPTY and payload is not None:
            if Default.EOL in payload:
                payloads: list[str] = payload.split(Default.EOL)
                lines = Tagger.string(
                    lines, level, tag, payloads[0], format=format
                )
                lines = Tagger.string(
                    lines, level + 1, Tag.CONT, payloads[1:], format=format
                )
            else:
                return ''.join(
                    [
                        lines,
                        Tagger.taginfo(
                            level, tag, payload, extra, format=format
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
            >>> from genedata.store import Map, Tagger
            >>> map1 = Map(30.0, -30.0)
            >>> map2 = Map(-40.0, 20.0)
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
            unique_payload = OrderedSet(payload)
            for item in unique_payload:
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
    def extension(
        lines: str,
        level: int,
        tag: str,
        payload: str,
        extra: str = Default.EMPTY,
    ) -> str:
        ext_line: str = Default.EMPTY
        if extra == Default.EMPTY:
            if payload == Default.EMPTY:
                ext_line = f'{level} {tag}{Default.EOL}'
            else:
                ext_line = (
                    f'{level} {tag} {Tagger.clean_input(payload)}{Default.EOL}'
                )
        else:
            ext_line = f'{level} {tag} {Tagger.clean_input(payload)} {Tagger.clean_input(extra)}{Default.EOL}'
        return ''.join([lines, ext_line])


class Checker:
    """Global methods supporting validation of data."""

    @staticmethod
    def verify(when: bool, then: bool, message: str) -> bool:
        """Use conditional logic to test whether to raise a ValueError exception.

        The only time this fails is when the `when` is True,
        but the `then` is False.  In that case a ValueError is raised
        with the value in `message`.  In all other cases, True is returned.

        This helps verify that more complicated GEDCOM criteria are met.

        Examples:
            >>> from genedata.store import Checker
            >>> message = 'Error!'
            >>> Checker.verify(True, 1 == 2, message)
            Traceback (most recent call last):
            ValueError: Error!

            >>> Checker.verify(True, 1 == 1, message)
            True

            When `when` is False, then True is returned no matter what the
            value of `then` happens to be.
            >>> Checker.verify(False, False, message)
            True

            >>> Checker.verify(False, True, message)
            True

        Args:
            when: If this is True then check the `then` condition, otherwise return True.
            then: If `when` is True and this is not, raise the ValueError.
            message: This is the message used by the ValueError.
        """
        if when and not then:
            raise ValueError(message)
        return True

    @staticmethod
    def verify_ext(tag: Tag, extensions: Any) -> bool:
        check: bool = True
        if extensions is None or (
            isinstance(extensions, list) and len(extensions) == 0
        ):
            return check
        if isinstance(extensions, list):
            for ext in extensions:
                # if isinstance(ext.exttag, ExtTag):
                if (
                    len(ext.exttag.supers) > 0
                    and tag.value not in ext.exttag.supers
                ):
                    check = False
                    raise ValueError(
                        Msg.NOT_DEFINED_FOR_STRUCTURE.format(tag.value)
                    )
                check = Checker.verify_ext(ext.exttag, ext.substructures)
                # if isinstance(ext.exttag, Tag):
                #     if (
                #         len(ext.exttag.supers) > 0
                #         and tag.value not in ext.exttag.supers
                #     ):
                #         check = False
                #         raise ValueError(
                #             Msg.NOT_DEFINED_FOR_STRUCTURE.format(tag.value)
                #         )
                #     check = Checker.verify_ext(ext.exttag, ext.substructures)
            return check
        if tag.value not in extensions.exttag.supers:
            check = False
            raise ValueError(Msg.NOT_DEFINED_FOR_STRUCTURE.format(tag.value))
        return check

    @staticmethod
    def verify_string_set(string: str, string_set: str) -> bool:
        """Check that each character of a string isin the set of permitted characters."""
        check: bool = True
        for char in string:
            if char not in string_set:
                raise ValueError(Msg.BAD_CHAR.format(char, string_set))
        return check

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
    def verify_enum(tag: Any, enumeration: Any) -> bool:
        """Check if the value is in the proper enumation."""
        if not isinstance(tag, Tag) and not isinstance(tag, ExtTag):
            raise ValueError(Msg.NEITHER_TAG_NOR_EXTTAG.format(str(tag)))
        if isinstance(tag, Tag) and tag.value not in enumeration:
            raise ValueError(Msg.NOT_VALID_ENUM.format(tag.name, enumeration))
        if isinstance(tag, ExtTag):
            enum_name: str = (
                str(enumeration)
                .replace("<enum '", '')
                .replace("'>", '')
                .upper()
            )
            if (
                tag.tag.enumsets is not None
                and enum_name not in tag.tag.enumsets
            ):
                raise ValueError(
                    Msg.EXTENSION_ENUM_TAG.format(tag.value, enum_name)
                )
        return True

    @staticmethod
    def verify_not_default(value: Any, default: Any) -> bool:
        """Check that the value is not the default value.

        If the value equals the default value in certain structures,
        the structure is empty.  Further processing on it can stop.
        In particular the output of its `ged` method is the empty string.

        Examples:
            The first example checks that the empty string is recognized
            as the default value of the empty string.
            >>> from genedata.store import Checker
            >>> Checker.verify_not_default('', '')
            Traceback (most recent call last):
            ValueError: GEDCOM requires a specific value different from the default "".

            The second example checks that a non-empty string
            is not identified as the default.
            >>> Checker.verify_not_default('not empty', '')
            True

        Args:
            value: What needs to be checked against the `default` value.
            default: The value to compare with `value`.

        Exception:
            ValueError: An exception is raised if the value is the default value.

        Returns:
            True: If the value does not equal the default value and an exception
                has not been raised.
        """
        if value == default:
            raise ValueError(Msg.NOT_DEFAULT.format(default))
        return True

    @staticmethod
    def verify_not_empty(value: Any) -> bool:
        if value is None:
            raise ValueError(Msg.NO_NONE)
        if isinstance(value, str) and value == Default.EMPTY:
            raise ValueError(Msg.NO_EMPTY_STRING)
        if isinstance(value, list) and len(value) == 0:
            raise ValueError(Msg.NO_EMPTY_LIST)
        if isinstance(value, Tag) and value == Tag.NONE:
            raise ValueError(Msg.NO_EMPTY_TAG)
        if isinstance(value, Xref) and value.fullname == Default.POINTER:
            raise ValueError(Msg.NO_EMPTY_POINTER)
        return True

    @staticmethod
    def verify_range(
        value: int | float, low: int | float, high: int | float
    ) -> bool:
        """Check if the value is inclusively between low and high boundaries."""
        if not low <= value <= high:
            raise ValueError(Msg.RANGE_ERROR.format(value, low, high))
        return True

    @staticmethod
    def verify_not_negative(value: int | float) -> bool:
        """Check if the value is a positive number."""
        if value < 0:
            raise ValueError(Msg.NEGATIVE_ERROR.format(value))
        return True


class Dater:
    """Global methods supporting date processing."""

    @staticmethod
    def format(
        year: int,
        month: int = 0,
        day: int = 0,
        calendar: CalendarDefinition = CalendarsGregorian.GREGORIAN,
    ) -> str:
        formatted: str = str(year)
        if year < 0:
            formatted = ''.join(
                [str(-year), Default.SPACE, calendar.epoch_name]
            )
        if month > 0:
            formatted = ''.join(
                [calendar.months[month].abbreviation, Default.SPACE, formatted]
            )
        if day > 0:
            formatted = ''.join([str(day), Default.SPACE, formatted])
        return formatted

    @staticmethod
    def ged_date(
        iso_date: str = String.NOW,
        calendar: CalendarName = CalendarName.GREGORIAN,
        epoch: bool = True,
    ) -> tuple[str, str]:
        """Obtain the GEDCOM date and time from an ISO 8601 date and time for the
        current UTC timestamp in GEDCOM format.

        Examples:
            The ISO date for January 1, 2000 at 1:15:30 AM would be `20000101 01:15:30`.
            >>> from genedata.store import Dater
            >>> print(Dater.ged_date(iso_date='2000-01-01T01:15:30'))
            ('01 JAN 2000', '01:15:30Z')

            Viewing this same date in BC context we would have:
            >>> print(Dater.ged_date(iso_date='-2000-01-01T01:15:30'))
            ('01 JAN 2000 BCE', '01:15:30Z')

            There is no zero year in the Gregorian Calendar and neither
            does the ISO 8601 standard have a zero year.
            >>> print(Dater.ged_date(iso_date='0-01-01T01:15:30'))
            Traceback (most recent call last):
            ValueError: The calendar has no zero year.

        Args:
            iso_date: The ISO date or `now` for the current date and time.
            calendar: The GEDCOM calendar to use when returning the date.
            epoch: Return the epoch, `BCE`, for the GEDCOM date if it is before
                the current epoch.  Set this to `False` to not return the epoch.
                This only applies to dates prior to 1 AD starting at 1 BC.

        References:
            [Wikipedia ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)

        Exceptions:

        """
        datetime: str = str(np.datetime64(iso_date))
        date, time = datetime.split(Default.T)
        date_pieces = date.split(Default.HYPHEN)
        if len(date_pieces) == 3:
            year: str = date_pieces[0]
            month: str = date_pieces[1]
            day: str = date_pieces[2]
        else:
            year = date_pieces[1]
            month = date_pieces[2]
            day = date_pieces[3]
        if int(year) == 0:
            raise ValueError(Msg.ZERO_YEAR)
        ged_time: str = ''.join([time, Default.Z])
        good_calendar: str | bool = Cal.CALENDARS.get(calendar, False)
        if not good_calendar:
            raise ValueError(Msg.BAD_CALENDAR.format(calendar))
        month_code: str = Cal.CALENDARS[calendar][String.MONTH_NAMES].get(
            month, False
        )
        if not month_code:
            raise ValueError(Msg.BAD_MONTH.format(calendar, month))
        ged_date: str = ''
        if epoch and len(date_pieces) == 4:
            ged_date = ''.join(
                [
                    day,
                    Default.SPACE,
                    month_code,
                    Default.SPACE,
                    year,
                    Default.SPACE,
                    String.BC,
                ]
            )
        else:
            ged_date = ''.join(
                [day, Default.SPACE, month_code, Default.SPACE, year]
            )
        return ged_date, ged_time

    @staticmethod
    def iso_date(
        ged_date: str,
        ged_time: str = Default.EMPTY,
        calendar: str = String.GREGORIAN,
    ) -> str:
        """Return an ISO date and time given a GEDCOM date and time."""
        day: str
        month: str
        year: str
        day, month, year = ged_date.split(Default.SPACE)
        time: str = ged_time.split(Default.Z)[0]
        good_calendar: str | bool = Cal.CALENDARS[calendar].get(
            String.GREGORIAN, False
        )
        if not good_calendar:
            logging.critical(Msg.BAD_CALENDAR.format(calendar))
            raise ValueError(Msg.BAD_CALENDAR.format(calendar))
        month_code: str = Cal.CALENDARS[calendar].get(month, False)
        if not month_code:
            logging.critical(Msg.BAD_MONTH.format(calendar, month))
            raise ValueError(Msg.BAD_MONTH.format(calendar, month))
        iso_datetime: str = ''.join(
            [
                year,
                Default.HYPHEN,
                month_code,
                Default.HYPHEN,
                day,
                Default.T,
                time,
            ]
        )
        return iso_datetime

    @staticmethod
    def now(level: int = 2) -> str:
        """Return the current UTC date and time rather than an entered value.

        This will be returned as a list of two lines for a GEDCOM file.
        This method will not likely be needed by the builder of a genealogy
        unless the builder wants to enter the current date and time into
        the genealogy. The current date and time is automatically
        entered for each record as its creation date and time
        as well as its change date and time.

        Return
        ------
        A list containing two strings is returned. The first member of
        the list is the date formatted to be used in a GEDCOM file.
        The second member of the list is the time formatted to
        be used in a GEDCOM file.

        Example
        -------
        >>> from genedata.store import Dater  # doctest: +ELLIPSIS
        >>> print(Dater.now())
        2 DATE ...
        3 TIME ...
        <BLANKLINE>

        Changing the level adjusts the level numbers for the two returned strings.

        >>> print(Dater.now(level=5))
        5 DATE ...
        6 TIME ...
        <BLANKLINE>

        See Also
        --------
        - `creation_date`
        - `change_date`
        - `header`
        """
        date: str
        time: str
        date, time = Dater.ged_date()
        return ''.join(
            [
                Tagger.taginfo(level, Tag.DATE, date),
                Tagger.taginfo(level + 1, Tag.TIME, time),
            ]
        )

    @staticmethod
    def creation_date() -> str:
        """Return three GEDCOM lines showing a line with a creation tag (CREA)
        and then two automatically generated
        UTC date and time lines.  These are used to
        show when a record has been created.

        See Also
        --------
        - `now`: the method that generates the current UTC date and time
        - `family`: the method creating the family record (FAM)
        - `individual`: the method creating the individual record (INDI)
        - `multimedia`: the method creating the multimedia record (OBJE)
        - `repository`: the method creating the repository record (REPO)
        - `shared_note`: the method creating the shared note record (SNOTE)
        - `source`: the method creating the source record (SOUR)
        - `submitter`: the method creating the submitter record (SUBM)
        """
        return ''.join([Tagger.taginfo(1, Tag.CREA), Dater.now()])


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
            >>> from genedata.store import Placer
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

        >>> from genedata.store import Placer
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
            >>> from genedata.store import Formatter
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
        if isinstance(item, Tag):
            return f'Tag.{item.name}'
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
                elif isinstance(item, Tag):
                    lines = ''.join(
                        [
                            lines,
                            Default.EOL,
                            Default.INDENT * (tabs),
                            'Tag.',
                            item.value,
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
    def codes_line(
        initial: str, items: Any, tabs: int, full: bool, required: bool = False
    ) -> str:
        line_end: str = Default.COMMA
        if required:
            line_end = Default.COMMA_REQUIRED
        result: str = Formatter.codes(items, tabs, full, required)
        keep: bool = required or full or result not in ['None', 'Tag.NONE']
        if keep:
            return ''.join([initial, result, line_end])
        return Default.EMPTY

    @staticmethod
    def display_code(
        name: str, *code_lines: tuple[str, Any, int, bool, bool]
    ) -> str:
        lines: str = ''.join([Default.EOL, name, '('])
        for line in code_lines:
            returned_line = Formatter.codes_line(
                line[0], line[1], line[2], line[3], line[4]
            )
            if returned_line != Default.EMPTY:
                lines = ''.join([lines, Default.EOL, returned_line])
        return ''.join([lines, Default.EOL, ')'])

    @staticmethod
    def schema_example(
        code_preface: str,
        show_code: str,
        gedcom_preface: str,
        show_ged: str,
        superstructures: dict[str, str],
        substructures: dict[str, str],
        gedcom_docs: str,
        genealogy_docs: str,
    ) -> None:
        superstructs: str = Default.EMPTY
        substructs: str = Default.EMPTY
        key: str
        value: str
        for key, value in superstructures.items():
            superstructs = ''.join(
                [
                    superstructs,
                    Default.EOL,
                    f'{Default.INDENT}{key:<40} {value:<6}',
                ]
            )
        for key, value in substructures.items():
            substructs = ''.join(
                [
                    substructs,
                    Default.EOL,
                    f'{Default.INDENT}{key:<40} {value:<6}',
                ]
            )
        print(  # noqa: T201
            ''.join(
                [
                    code_preface,
                    Default.EOL,
                    show_code,
                    Default.EOL_DOUBLE,
                    gedcom_preface,
                    Default.EOL_DOUBLE,
                    show_ged,
                    Default.EOL,
                    Example.SUPERSTRUCTURES,
                    superstructs,
                    Example.SUBSTRUCTURES,
                    substructs,
                    Example.GEDCOM_SPECIFICATION,
                    gedcom_docs,
                    Default.EOL,
                    genealogy_docs,
                ]
            )
        )

    @staticmethod
    def display_tuple(named_tuple: Any) -> None:
        print(  # noqa: T201
            str(named_tuple)
            .replace('(', '(\n     ', 1)
            .replace(',', ',\n    ')
            .replace(')', ',\n)')
        )

    @staticmethod
    def display(named_tuple: Any, full: bool = False) -> None:
        """Display the results of the ged and code methods for a named tuple.

        Args:
            named_tuple: This is the NamedTuple to display.

        There are two methods to run:
        1. `ged` runs validate() capturing any error message.
        2. `code` which runs even if the ged method fails.
        """
        # print('DISPLAY:')
        # print(f'{Formatter.display_tuple(named_tuple)}\n')
        try:
            print(f'GED:\n{named_tuple.ged()}')  # noqa: T201
        except Exception as e:
            print('ERROR MESSAGE:\n')  # noqa: T201
            print(str(e))  # noqa: T201
            print()  # noqa: T201
        print(f'CODE:{named_tuple.code(full=full)}')  # noqa: T201
        type_string: str = str(type(named_tuple))
        match type_string:
            case "<class 'genedata.store.Address'>":
                print(OverView.ADDRESS_STRUCTURE)  # noqa: T201
            case "<class 'genedata.store.Age'>":
                print(OverView.FAMILY_EVENT_DETAIL)  # noqa: T201
            case "<class 'genedata.store.Alias'>":
                print(OverView.INDIVIDUAL)  # noqa: T201
            case "<class 'genedata.store.Association'>":
                print(OverView.ASSOCIATION_STRUCTURE)  # noqa: T201
            case "<class 'genedata.store.CallNumber'>":
                print(OverView.SOURCE_REPOSITORY_CITATION)  # noqa: T201
            case "<class 'genedata.store.ChangeDate'>":
                print(OverView.CHANGE_DATE)  # noqa: T201
            case "<class 'genedata.store.Child'>":
                print(OverView.FAMILY)  # noqa: T201
            case "<class 'genedata.store.CreationDate'>":
                print(OverView.CREATION_DATE)  # noqa: T201
            case "<class 'genedata.store.Date'>":
                print(OverView.DATE_VALUE)  # noqa: T201
            case "<class 'genedata.store.Email'>":
                print(OverView.SUBMITTER)  # noqa: T201
            case "<class 'genedata.store.EventDetail'>":
                print(OverView.EVENT_DETAIL)  # noqa: T201
            case "<class 'genedata.store.ExtTag'>":
                print(OverView.HEADER)  # noqa: T201
            case "<class 'genedata.store.Family'>":
                print(OverView.FAMILY)  # noqa: T201
            case "<class 'genedata.store.FamilyAttribute'>":
                print(OverView.FAMILY_ATTRIBUTE_STRUCTURE)  # noqa: T201
            case "<class 'genedata.store.FamilyEventDetail'>":
                print(OverView.FAMILY_EVENT_DETAIL)  # noqa: T201
            case "<class 'genedata.store.FamilyEvent'>":
                print(OverView.FAMILY_EVENT_STRUCTURE)  # noqa: T201
            case "<class 'genedata.store.FamilyChild'>":
                print(OverView.INDIVIDUAL)  # noqa: T201
            case "<class 'genedata.store.FamilySpouse'>":
                print(OverView.INDIVIDUAL)  # noqa: T201
            case "<class 'genedata.store.Fax'>":
                print(OverView.SUBMITTER)  # noqa: T201
            case "<class 'genedata.store.File'>":
                print(OverView.MULTIMEDIA)  # noqa: T201
            case "<class 'genedata.store.FileTranslation'>":
                print(OverView.MULTIMEDIA)  # noqa: T201
            case "<class 'genedata.store.Header'>":
                print(OverView.HEADER)  # noqa: T201
            case "<class 'genedata.store.Identifier'>":
                print(OverView.IDENTIFIER_STRUCTURE)  # noqa: T201
            case "<class 'genedata.store.Individual'>":
                print(OverView.INDIVIDUAL)  # noqa: T201
            case "<class 'genedata.store.IndividualAttribute'>":
                print(OverView.INDIVIDUAL_ATTRIBUTE_STRUCTURE)  # noqa: T201
            case "<class 'genedata.store.IndividualEventDetail'>":
                print(OverView.INDIVIDUAL_EVENT_DETAIL)  # noqa: T201
            case "<class 'genedata.store.IndividualEvent'>":
                print(OverView.INDIVIDUAL_EVENT_STRUCTURE)  # noqa: T201
            case "<class 'genedata.store.Lang'>":
                print(OverView.SUBMITTER)  # noqa: T201
            case "<class 'genedata.store.LDSOrdinanceDetail'>":
                print(OverView.LDS_ORDINANCE_DETAIL)  # noqa: T201
            case "<class 'genedata.store.LDSIndividualOrdinance'>":
                print(OverView.LDS_INDIVIDUAL_ORDINANCE)  # noqa: T201
            case "<class 'genedata.store.LDSSpouseSealing'>":
                print(OverView.LDS_SPOUSE_SEALING)  # noqa: T201
            case "<class 'genedata.store.Map'>":
                print(OverView.PLACE_STRUCTURE)  # noqa: T201
            case "<class 'genedata.store.Multimedia'>":
                print(OverView.MULTIMEDIA)  # noqa: T201
            case "<class 'genedata.store.MultimediaLink'>":
                print(OverView.MULTIMEDIA_LINK)  # noqa: T201
            case "<class 'genedata.store.NameTranslation'>":
                print(OverView.PERSONAL_NAME_STRUCTURE)  # noqa: T201
            case "<class 'genedata.store.NonEvent'>":
                print(OverView.NON_EVENT_STRUCTURE)  # noqa: T201
            case "<class 'genedata.store.Note'>":
                print(OverView.NOTE_STRUCTURE)  # noqa: T201
            case "<class 'genedata.store.NoteTranslation'>":
                print(OverView.NOTE_STRUCTURE)  # noqa: T201
            case "<class 'genedata.store.PersonalNamePieces'>":
                print(OverView.PERSONAL_NAME_PIECES)  # noqa: T201
            case "<class 'genedata.store.PersonalName'>":
                print(OverView.PERSONAL_NAME_STRUCTURE)  # noqa: T201
            case "<class 'genedata.store.Phone'>":
                print(OverView.SUBMITTER)  # noqa: T201
            case "<class 'genedata.store.Phrase'>":
                print(OverView.INDIVIDUAL)  # noqa: T201
            case "<class 'genedata.store.Place'>":
                print(OverView.PLACE_STRUCTURE)  # noqa: T201
            case "<class 'genedata.store.PlaceTranslation'>":
                print(OverView.PLACE_STRUCTURE)  # noqa: T201
            case "<class 'genedata.store.Repository'>":
                print(OverView.REPOSITORY)  # noqa: T201
            case "<class 'genedata.store.SDate'>":
                print(OverView.EVENT_DETAIL)  # noqa: T201
            case "<class 'genedata.store.SharedNote'>":
                print(OverView.SHARED_NOTE)  # noqa: T201
            case "<class 'genedata.store.Source'>":
                print(OverView.SOURCE)  # noqa: T201
            case "<class 'genedata.store.SourceCitation'>":
                print(OverView.SOURCE_CITATION)  # noqa: T201
            case "<class 'genedata.store.SourceData'>":
                print(OverView.SOURCE)  # noqa: T201
            case "<class 'genedata.store.SourceDataEvent'>":
                print(OverView.SOURCE)  # noqa: T201
            case "<class 'genedata.store.SourceRepositoryCitation'>":
                print(OverView.SOURCE_REPOSITORY_CITATION)  # noqa: T201
            case "<class 'genedata.store.Submitter'>":
                print(OverView.SUBMITTER)  # noqa: T201
            case "<class 'genedata.store.Text'>":
                print(OverView.SOURCE)  # noqa: T201
            case "<class 'genedata.store.Time'>":
                print(OverView.DATE_VALUE)  # noqa: T201
            case "<class 'genedata.store.WWW'>":
                print(OverView.SUBMITTER)  # noqa: T201
            case _:
                pass


class Xref:
    """Assign an extension cross-reference type to a string.

    This base class is instantiated through the other cross reference classes.

    Args:
        name: The name of the identifier.
        tag: The tag associated with this identifier.

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

    def __init__(self, name: str, tag: Tag | ExtTag = Tag.NONE):
        self.fullname: str = name.upper()
        self.name: str = name.replace('@', '').replace(Default.UNDERLINE, ' ')
        self.tag: Tag | ExtTag = tag
        self.code_xref = f'{self.tag.value.lower()}_{self.name.lower()}_xref'

    def __str__(self) -> str:
        """Return the name used by the GEDCOM standard."""
        return self.fullname

    def __repr__(self) -> str:
        return f"Xref('{self.fullname}')"

    def ged(self, info: str = Default.EMPTY) -> str:
        """Return the identifier formatted according to the GEDCOM standard."""
        if info == Default.EMPTY:
            return f'0 {self.fullname} {self.tag.value}{Default.EOL}'
        return f'0 {self.fullname} {self.tag.value} {info}{Default.EOL}'

    def code(self, tabs: int = 0) -> str:  # noqa: ARG002
        return self.fullname


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

    def __init__(self, name: str, exttag: ExtTag | Tag = Tag.NONE):
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

    def __init__(self, name: str, tag: Tag = Tag.FAM):
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

    def __init__(self, name: str, tag: Tag = Tag.INDI):
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

    def __init__(self, name: str, tag: Tag = Tag.OBJE):
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

    def __init__(self, name: str, tag: Tag = Tag.REPO):
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

    See Also:
        `genedata.build.shared_note_xref()`

    Reference:
        - [GEDCOM SHARED_NOTE Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SHARED_NOTE_RECORD)
    """

    def __init__(self, name: str, tag: Tag = Tag.SNOTE):
        super().__init__(name, tag)

    def __repr__(self) -> str:
        return f"SharedNoteXref('{self.fullname}')"


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

    def __init__(self, name: str, tag: Tag = Tag.SOUR):
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

    def __init__(self, name: str, tag: Tag = Tag.SUBM):
        super().__init__(name, tag)

    def __repr__(self) -> str:
        return f"SubmitterXref('{self.fullname}')"


class Void:
    NAME: str = Default.POINTER
    FAM: FamilyXref = FamilyXref(NAME)
    INDI: IndividualXref = IndividualXref(NAME)
    OBJE: MultimediaXref = MultimediaXref(NAME)
    REPO: RepositoryXref = RepositoryXref(NAME)
    SNOTE: SharedNoteXref = SharedNoteXref(NAME)
    SOUR: SourceXref = SourceXref(NAME)
    SUBM: SubmitterXref = SubmitterXref(NAME)
    EXTTAG: ExtensionXref = ExtensionXref(NAME)


class Extension(NamedTuple):
    """Store, validate and display extension tags.

    The GEDCOM specification recommends the following:

    > The recommended way to go beyond the set of standard structure types in this specification
    > or to expand their usage is to submit a feature request on the FamilySearch GEDCOM development page
    > so that the ramifications of the proposed addition and its interplay with other proposals
    > may be discussed and the addition may be included in a subsequent version of this specification.
    >
    > This specification also provides multiple ways for extension authors to go beyond the specification
    > without submitting a feature request, which are described in the remainder of this section.

    This NamedTuple implements going beyond the specification without submitting
    a feature request.

    Example:

    Args:
        exttag: The tag used entered through ExtTag()
        payload: The value on the same line as the tag.
        extra: Extra values on the same line as the tag.
        substructures: Substructures having this extension as a superstructure.  They are
            placed in the ged file with a level one higher than this extension has.
            They are also Extension tuples and may have substructures of their own.

    See Also:
        `ExtTag`

    Reference:
        [GedCOM Extensions](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#extensions)
    """

    exttag: ExtTag | Tag
    payload: str = Default.EMPTY
    extra: str = Default.EMPTY
    substructures: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.exttag, ExtTag | Tag, no_list=True)
            and Checker.verify_type(self.payload, str, no_list=True)
            and Checker.verify_type(self.extra, str, no_list=True)
        )
        return check

    def ged(self, level: int = 1) -> str:
        lines: str = ''
        if self.validate():
            lines = Tagger.string(
                lines, level, self.exttag, self.payload, self.extra
            )
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'Extension(',
                ('    exttag = ', self.exttag, tabs, full, True),
                ('    payload = ', self.payload, tabs, full, False),
                ('    extra = ', self.extra, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


ExtType = Extension | list[Extension] | None


class Date(NamedTuple):
    """Validate and display date data in various formats.

    Dates are entered based on a Gregorian calendar. This calendar
    does not have a 0 year.  The year 1 BC is entered as `-1`.

    A default value of `0` for any date component means that the component
    will not be displayed.

    Examples:

    Arg:
        year: A numerical value representing the year.  It is the only required parameter.
        month: An optional numerical value representing the month.  It will be converted to a string
            value for the month.
        day: An optional numerical value representing the day.
        calendar: An optional tag representing the calendar system. There are four standard calendars:
            Tag.GREGORIAN, Tag.JULIAN, Tag.FRENCH_R (French Revolution) and Tag.HEBREW.  If no calendar
            is listed the default for calculating the month will be the Gregorian calendar.  If a
            calendar is present, it will be displayed as part of the date.
        iso: A representation of the date in ISO 8601 standard used instead of `year`, `month` and `day`.
        display_calendar: Flag to determine if the calendar name should be displayed in the GEDCOM output.
        date_ext: Optional substructures extending [DATE tag](https://gedcom.io/terms/v7/DATE) entered through `Extension`.

    See Also:
        `Extension`

    Reference:
        [GEDCOM DATE](https://gedcom.io/terms/v7/DATE)
        [GEDCOM DATE type](https://gedcom.io/terms/v7/type-Date)
    """

    year: int = Default.DATE_YEAR
    month: int = Default.DATE_MONTH
    day: int = Default.DATE_DAY
    calendar: CalendarDefinition = CalendarsGregorian.GREGORIAN
    iso: str | None = None
    display_calendar: bool = False
    date_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.year, int, no_list=True)
            and Checker.verify_type(self.month, int, no_list=True)
            and Checker.verify_type(self.day, int, no_list=True)
            and Checker.verify_range(self.month, 0, 13)
            # and Checker.verify_type(self.calendar, CalendarDefinition)
            and Checker.verify_type(self.display_calendar, bool)
            and Checker.verify_type(self.iso, str | None, no_list=True)
            # and self.calendar.validate(
            #     self.year, self.month, self.day, self.iso
            # )
            and Checker.verify_ext(Tag.DATE, self.date_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        lines: str = Default.EMPTY
        formatted_date: str = Dater.format(
            self.year, self.month, self.day, self.calendar
        )
        formatted_calendar_date: str = formatted_date
        if self.display_calendar:
            formatted_calendar_date = ''.join(
                [self.calendar.name, Default.EMPTY, formatted_date]
            )
        lines = Tagger.string(lines, level, Tag.DATE, formatted_calendar_date)
        return Tagger.structure(lines, level + 1, self.date_ext)

    def from_iso(self) -> str:
        """Return the validated ISO format for the date.

        References:
            - [ISO 8601 Standard](https://www.iso.org/iso-8601-date-and-time-format.html)
            - [Wikipedia Overview](https://en.wikipedia.org/wiki/ISO_8601)
        """
        if self.validate():
            return f'{self.year}-{self.month}-{self.day}'
        return ''

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'Date',
                ('    year = ', self.year, tabs, full, False),
                ('    month = ', self.month, tabs, full, False),
                ('    day = ', self.day, tabs, full, False),
                ('    iso = ', self.iso, tabs, full, False),
                (
                    '    display_calendar = ',
                    self.display_calendar,
                    tabs,
                    full,
                    False,
                ),
                ('    date_ext = ', self.date_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


DateType = Date | None


class SDate(NamedTuple):
    """Validate and display date data in various formats.

    Dates are entered based on a Gregorian calendar. This calendar
    does not have a 0 year.  The year 1 BC is entered as `-1`.

    A default value of `0` for any date component means that the component
    will not be displayed.

    Examples:

    Arg:
        year: A numerical value representing the year.  It is the only required parameter.
        month: An optional numerical value representing the month.  It will be converted to a string
            value for the month.
        day: An optional numerical value representing the day.
        calendar: An optional tag representing the calendar system. There are four standard calendars:
            Tag.GREGORIAN, Tag.JULIAN, Tag.FRENCH_R (French Revolution) and Tag.HEBREW.  If no calendar
            is listed the default for calculating the month will be the Gregorian calendar.  If a
            calendar is present, it will be displayed as part of the date.
        iso: A representation of the date in ISO 8601 standard used instead of `year`, `month` and `day`.
        display_calendar: Flag to determine if the calendar name should be displayed in the GEDCOM output.
        date_ext: Optional substructures extending [SDATE tag](https://gedcom.io/terms/v7/SDATE) entered through Extension().

    See Also:
        `Extension`

    Reference:
        [GEDCOM DATE](https://gedcom.io/terms/v7/SDATE)
        [GEDCOM DATE type](https://gedcom.io/terms/v7/type-Date)
    """

    year: int = Default.DATE_YEAR
    month: int = Default.DATE_MONTH
    day: int = Default.DATE_DAY
    calendar: CalendarDefinition = CalendarsGregorian.GREGORIAN
    iso: str | None = None
    display_calendar: bool = False
    date_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.year, int)
            and Checker.verify_type(self.month, int)
            and Checker.verify_type(self.day, int)
            and Checker.verify_range(self.month, 0, 13)
            # and Checker.verify_type(self.calendar, CalendarDefinition)
            and Checker.verify_type(self.display_calendar, bool)
            and Checker.verify_type(self.iso, str | None, no_list=True)
            # and self.calendar.validate(
            #     self.year, self.month, self.day, self.iso
            # )
            and Checker.verify_ext(Tag.SDATE, self.date_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        lines: str = Default.EMPTY
        formatted_date: str = Dater.format(
            self.year, self.month, self.day, self.calendar
        )
        formatted_calendar_date: str = formatted_date
        if self.display_calendar:
            formatted_calendar_date = ''.join(
                [self.calendar.name, Default.EMPTY, formatted_date]
            )
        lines = Tagger.string(lines, level, Tag.SDATE, formatted_calendar_date)
        return Tagger.structure(lines, level + 1, self.date_ext)

    def from_iso(self) -> str:
        """Return the validated ISO format for the date.

        References
        ----------
        - [ISO 8601 Standard](https://www.iso.org/iso-8601-date-and-time-format.html)
        - [Wikipedia Overview](https://en.wikipedia.org/wiki/ISO_8601)
        """
        if self.validate():
            return f'{self.year}-{self.month}-{self.day}'
        return ''

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'SDate',
                ('    year = ', self.year, tabs, full, False),
                ('    month = ', self.month, tabs, full, False),
                ('    day = ', self.day, tabs, full, False),
                ('    iso = ', self.iso, tabs, full, False),
                (
                    '    display_calendar = ',
                    self.display_calendar,
                    tabs,
                    full,
                    False,
                ),
                ('    date_ext = ', self.date_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


SDateType = SDate | None


class Time(NamedTuple):
    """Validate and display time data in various formats.

    The standard does not permit leap seconds nor end of day instant (24:00:00).

    Examples:

    Args:
        hour: The hour of the time.
        minute: The minute of the time.
        second: The second of the time including fractional seconds.
        UTC: A boolean declaring whether the date is in UTC time or in some time zone.
        time_ext: Optional substructures extending [TIME tag](https://gedcom.io/terms/v7/TIME) entered through `Extension`.

    See Also:
        `Extension`

    Reference:
        [GEDCOM Time Data Type](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#time)
    """

    hour: int = Default.TIME_HOUR
    minute: int = Default.TIME_MINUTE
    second: int | float = Default.TIME_SECOND
    UTC: bool = False
    time_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.hour, int)
            and Checker.verify_type(self.minute, int)
            and Checker.verify_type(self.second, int | float)
            and Checker.verify_type(self.UTC, bool)
            and Checker.verify_range(self.hour, 0, 23)
            and Checker.verify_range(self.minute, 0, 59)
            and Checker.verify_range(self.second, 0, 59.999999999999)
            and Checker.verify_ext(Tag.TIME, self.time_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        hour_str: str = str(self.hour)
        minute_str: str = str(self.minute)
        second_str: str = str(self.second)
        lines: str = Default.EMPTY
        if self.validate():
            if 0 <= self.hour < 10:
                hour_str = ''.join(['0', hour_str])
            if 0 <= self.minute < 10:
                minute_str = ''.join(['0', minute_str])
            if 0 <= self.second < 10:
                second_str = ''.join(['0', second_str])
            if self.UTC:
                second_str = ''.join([second_str, 'Z'])
            lines = Tagger.string(
                lines, level, Tag.TIME, f'{hour_str}:{minute_str}:{second_str}'
            )
            lines = Tagger.structure(lines, level + 1, self.time_ext)
        return lines

    def iso(self) -> str:
        """Return the validated ISO format for the time.

        References:
            [ISO 8601 Standard](https://www.iso.org/iso-8601-date-and-time-format.html)
            [Wikipedia Overview](https://en.wikipedia.org/wiki/ISO_8601)
        """
        if self.validate():
            return f'{self.hour}:{self.minute}:{self.second}'
        return ''

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'Time',
                ('    hour = ', self.hour, tabs, full, False),
                ('    minute = ', self.minute, tabs, full, False),
                ('    second = ', self.second, tabs, full, False),
                ('    UTC = ', self.UTC, tabs, full, False),
                ('    time_ext = ', self.time_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


TimeType = Time | None


class CreationDate(NamedTuple):
    """Store, validate and format create date information.

    Example:

    Args:
        date: The value of the date entered using Date().
        time: The value of the time entered using Time().
        crea_ext: Optional substructures extending [CREA tag](https://gedcom.io/terms/v7/CREA) entered through Extension().

    See Also:
        `Date`
        `Time`
        `Extension`

    Reference:
        [GEDCOM CREA tag](https://gedcom.io/terms/v7/CREA)
        [GEDCOM Creation Date](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#CREATION_DATE)

    > n CREA                                     {1:1}  g7:CREA
    >   +1 DATE <DateExact>                      {1:1}  g7:DATE-exact
    >      +2 TIME <Time>                        {0:1}  g7:TIME
    """

    date: Date = Date()
    time: Time = Time()
    crea_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            self.date.validate()
            and self.time.validate()
            and Checker.verify_ext(Tag.CREA, self.crea_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.empty(lines, level, Tag.CREA)
            lines = Tagger.structure(lines, level + 1, self.crea_ext)
            lines = Tagger.structure(lines, level + 1, self.date)
            lines = Tagger.structure(lines, level + 2, self.time)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'CreationDate',
                ('    date = ', self.date, tabs + 1, full, True),
                ('    time = ', self.time, tabs + 1, full, True),
                ('    crea_ext = ', self.crea_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


CreationDateType = CreationDate | None


class Identifier(NamedTuple):
    """Construct GEDCOM data for the Identifier Structure.

    There are three valid identifier structures.  They will be illustrated in
    the examples.

    Examples:

    Args:
        tag: One of the three tags for identifiers.
        payload: Information associated with the tag displayed on the same GEDCOM line.
        tag_type: Information about the type of the tag.
        tag_ext: Optional substructures extending [TAG tag](https://gedcom.io/terms/v7/TAG) entered through `Extension`.
        type_ext: Optional substructures extending [TYPE tag](https://gedcom.io/terms/v7/TYPE) entered through 'Extension'.

    See Also:
        `Extension`

    Reference:
        [GEDCOM TAG tag](https://gedcom.io/terms/v7/TAG)
        [GEDCOM TYPE tag](https://gedcom.io/terms/v7/TYPE)
        [GEDCOM Identifier Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#IDENTIFIER_STRUCTURE)

    > [
    > n REFN <Special>                           {1:1}  g7:REFN
    >   +1 TYPE <Text>                           {0:1}  g7:TYPE
    > |
    > n UID <Special>                            {1:1}  g7:UID
    > |
    > n EXID <Special>                           {1:1}  g7:EXID
    >   +1 TYPE <Special>                        {0:1}  g7:EXID-TYPE
    > ]
    """

    tag: Tag = Tag.NONE
    payload: str = Default.EMPTY
    tag_type: str = Default.EMPTY
    tag_ext: ExtType = None
    type_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_enum(self.tag, Id)
            and Checker.verify_not_empty(self.tag)
            and Checker.verify_type(self.payload, str, no_list=True)
            and Checker.verify_not_empty(self.payload)
            and Checker.verify_type(self.tag_type, str, no_list=True)
            and Checker.verify(
                self.tag == Tag.EXID,
                self.tag_type != Default.EMPTY,
                Msg.EXID_TYPE,
            )
            and Checker.verify_ext(self.tag, self.tag_ext)
            and Checker.verify_ext(Tag.TYPE, self.type_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, self.tag, self.payload)
            lines = Tagger.structure(lines, level + 1, self.tag_ext)
            lines = Tagger.string(lines, level + 1, Tag.TYPE, self.tag_type)
            lines = Tagger.structure(lines, level + 2, self.type_ext)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'Identifier',
                ('    tag = ', self.tag, tabs, full, True),
                ('    payload = ', self.payload, tabs, full, True),
                (
                    '    tag_type = ',
                    self.tag_type,
                    tabs,
                    full,
                    (self.tag == Tag.EXID),
                ),
                ('    tag_ext = ', self.tag_ext, tabs, full, False),
                ('    type_ext = ', self.type_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


IdenType = Identifier | list[Identifier] | None


class Phone(NamedTuple):
    """Store, validate and format phone information.

    Example:
        One can enter a phone number as a string of characters.
        >>> from genedata.store import Phone
        >>> p = Phone('(123) 456-7890')
        >>> print(p.ged(1))
        1 PHON (123) 456-7890
        <BLANKLINE>

        One can also use `Formatter.phone` to make sure the number is formatted
        according to the GEDCOM recommended International Standard.
        >>> q = Phone(Formatter.phone(1, 123, 456, 7890))
        >>> print(q.ged(2))
        2 PHON +1 123 456 7890
        <BLANKLINE>

    Args:
        phone: The string containing the phone number optionally formatted through `Formatter.phone`.
        phon_ext: Optional substructures extending [PHON tag](https://gedcom.io/terms/v7/PHON) entered through `Extension`.

    See Also:
        `Extension`
        `Formatter.phone`

    Reference:
        [GEDCOM PHON tag](https://gedcom.io/terms/v7/PHON)
        [ITU E-123 Standard](https://www.itu.int/rec/T-REC-E.123-200102-I/en)

    """

    phone: str = Default.EMPTY
    phon_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.phone, str, no_list=True)
            and Checker.verify_not_empty(self.phone)
            and Checker.verify_ext(Tag.PHON, self.phon_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.PHON, self.phone)
            lines = Tagger.structure(lines, level + 1, self.phon_ext)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'Phone',
                ('    phone = ', self.phone, tabs, full, True),
                ('    phon_ext = ', self.phon_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


PhoneType = Phone | list[Phone] | None


class Email(NamedTuple):
    """Store, validate and format email information.

    Example:

    Args:
        email: The string containing the email.
        email_ext: Optional substructures extending [EMAIL tag](https://gedcom.io/terms/v7/EMAIL) entered through `Extension`.

    See Also:
        `Extension`

    Reference:
        [GEDCOM EMAIL tag](https://gedcom.io/terms/v7/EMAIL)

    """

    email: str = Default.EMPTY
    email_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.email, str, no_list=True)
            and Checker.verify_not_empty(self.email)
            and Checker.verify_ext(Tag.EMAIL, self.email_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = Default.EMPTY
        if self.validate():
            lines = Tagger.string(lines, level, Tag.EMAIL, self.email)
            lines = Tagger.structure(lines, level + 1, self.email_ext)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'Email',
                ('    email = ', self.email, tabs, full, True),
                ('    email_ext = ', self.email_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


EmailType = Email | list[Email] | None


class Fax(NamedTuple):
    """Store, validate and format fax information.

    Example:

    Args:
        fax: The string containing the fax optionally entered through `Formatter.phone`.
        fax_ext: Optional substructures extending [FAX tag](https://gedcom.io/terms/v7/FAX) entered through `Extension`.

    See Also:
        `Extension`
        `Formatter.phone`

    Reference:
        [GEDCOM FAX tag](https://gedcom.io/terms/v7/FAX)

    """

    fax: str = Default.EMPTY
    fax_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.fax, str, no_list=True)
            and Checker.verify_not_empty(self.fax)
            and Checker.verify_ext(Tag.FAX, self.fax_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.FAX, self.fax)
            lines = Tagger.structure(lines, level + 1, self.fax_ext)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'Fax',
                ('    fax = ', self.fax, tabs, full, True),
                ('    fax_ext = ', self.fax_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


FaxType = Fax | list[Fax] | None


class WWW(NamedTuple):
    """Store, validate and format fax information.

    Example:

    Args:
        www: The string containing the internet url.
        www_ext: Optional substructures extending [WWW tag](https://gedcom.io/terms/v7/WWW) entered through `Extension`.

    See Also:
        `Extension`

    Reference:
        [GEDCOM WWW tag](https://gedcom.io/terms/v7/WWW)

    """

    www: str = Default.EMPTY
    www_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.www, str, no_list=True)
            and Checker.verify_not_empty(self.www)
            and Checker.verify_ext(Tag.WWW, self.www_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.WWW, self.www)
            lines = Tagger.structure(lines, level + 1, self.www_ext)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'WWW',
                ('    www = ', self.www, tabs, full, True),
                ('    www_ext = ', self.www_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


WWWType = WWW | list[WWW] | None


class Lang(NamedTuple):
    """Store, validate and format fax information.

    Example:

    Args:
        lang: The string containing the language.
        lang_ext: Optional substructures extending [LANG tag](https://gedcom.io/terms/v7/LANG) entered through `Extension`.

    See Also:
        `Extension`

    Reference:
        [GEDCOM LANG tag](https://gedcom.io/terms/v7/LANG)

    """

    lang: str = Default.EMPTY
    lang_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.lang, str, no_list=True)
            and Checker.verify_not_empty(self.lang)
            and Checker.verify_ext(Tag.LANG, self.lang_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.LANG, self.lang)
            lines = Tagger.structure(lines, level + 1, self.lang_ext)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'Lang',
                ('    lang = ', self.lang, tabs, full, True),
                ('    lang_ext = ', self.lang_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


LangType = Lang | list[Lang] | None


class Phrase(NamedTuple):
    """Store, validate and format fax information.

    Example:
        A phrase is a string which will be broken into separate GEDCOM lines if
        any line break is present.  A line break is present either by putting
        on in explicitly with "\n" or by using a multiline string.  Here is an
        example of using "\n".
        >>> from genedata.store import Phrase
        >>> print(Phrase('This is a\\ntest phrase with two lines.').ged(1))
        1 PHRASE This is a
        2 CONT test phrase with two lines.
        <BLANKLINE>

        One may also use a multiline string.
        >>> from genedata.store import Phrase
        >>> print(
        ...     Phrase('''This is a
        ... test phrase with two lines.''').ged(1)
        ... )
        1 PHRASE This is a
        2 CONT test phrase with two lines.
        <BLANKLINE>

    Args:
        phrase: The text of the phrase.
        phrase_ext: Optional substructures extending [PHRASE tag](https://gedcom.io/terms/v7/PHRASE)
            entered through `Extension`.

    Reference:
        [GEDCOM PHRASE tag](https://gedcom.io/terms/v7/PHRASE)

    """

    phrase: str = Default.EMPTY
    phrase_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.phrase, str, no_list=True)
            and Checker.verify_not_empty(self.phrase)
            and Checker.verify_ext(Tag.LANG, self.phrase_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.PHRASE, self.phrase)
            lines = Tagger.structure(lines, level + 1, self.phrase_ext)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'Phrase',
                ('    phrase = ', self.phrase, tabs, full, True),
                ('    phrase_ext = ', self.phrase_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


PhraseType = Phrase | None


class Address(NamedTuple):
    """Store, validate and format address information to be saved to a ged file.

    Example:
        The following is the minimum amount of information for an address.
        >>> from genedata.store import Address
        >>> mailing_address = Address(
        ...     '12345 ABC Street\\nSouth North City, My State 22222',
        ... )
        >>> mailing_address.validate()
        True
        >>> print(mailing_address.ged(1))
        1 ADDR 12345 ABC Street
        2 CONT South North City, My State 22222
        <BLANKLINE>

        There are five named strings stored in this NamedTuple.
        >>> from genedata.store import Address
        >>> full_address = Address(
        ...     '12345 ABC Street\\nSouth North City, My State 23456',
        ...     'South North City',
        ...     'My State',
        ...     '23456',
        ...     'USA',
        ... )
        >>> print(full_address.ged(1))
        1 ADDR 12345 ABC Street
        2 CONT South North City, My State 23456
        2 CITY South North City
        2 STAE My State
        2 POST 23456
        2 CTRY USA
        <BLANKLINE>

    Args:
        address: The mailing address with each line being one item of a list.
        city: The city or and empty string to leave this blank.
        state: The state or an empty string to leave this blank.
        postal: The postal code or an empty string to leave this blank.
        country: The country or an empty string to leave this blank.
        addr_ext: Optional substructures extending [ADDR tag](https://gedcom.io/terms/v7/ADDR)
            entered through `Extension`.
        city_ext: Optional substructures extending [CITY tag](https://gedcom.io/terms/v7/CITY)
            entered through `Extension`.
        stae_ext: Optional substructures extending [STAE tag](https://gedcom.io/terms/v7/STAE)
            entered through `Extension`.
        post_ext: Optional substructures extending [POST tag](https://gedcom.io/terms/v7/POST)
            entered through `Extension`.
        ctry_ext: Optional substructures extending [CITY tag](https://gedcom.io/terms/v7/CITY)
            entered through `Extension`.

    See Also:
        `Extension`

    Reference:
        [GEDCOM Specifications](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#ADDRESS_STRUCTURE)

    > n ADDR <Special>                           {1:1}  [g7:ADDR](https://gedcom.io/terms/v7/ADDR)
    >   +1 ADR1 <Special>                        {0:1}  [g7:ADR1](https://gedcom.io/terms/v7/ADR1)
    >   +1 ADR2 <Special>                        {0:1}  [g7:ADR2](https://gedcom.io/terms/v7/ADR2)
    >   +1 ADR3 <Special>                        {0:1}  [g7:ADR3](https://gedcom.io/terms/v7/ADR3)
    >   +1 CITY <Special>                        {0:1}  [g7:CITY](https://gedcom.io/terms/v7/CITY)
    >   +1 STAE <Special>                        {0:1}  [g7:STAE](https://gedcom.io/terms/v7/STAE)
    >   +1 POST <Special>                        {0:1}  [g7:POST](https://gedcom.io/terms/v7/POST)
    >   +1 CTRY <Special>                        {0:1}  [g7:CTRY](https://gedcom.io/terms/v7/CTRY)
    """

    address: str = Default.EMPTY
    city: str = Default.EMPTY
    state: str = Default.EMPTY
    postal: str = Default.EMPTY
    country: str = Default.EMPTY
    addr_ext: ExtType = None
    city_ext: ExtType = None
    stae_ext: ExtType = None
    post_ext: ExtType = None
    ctry_ext: ExtType = None

    def validate(self) -> bool:
        check: bool = (
            Checker.verify_type(self.address, str, no_list=True)
            and Checker.verify_not_empty(self.address)
            and Checker.verify_type(self.city, str, no_list=True)
            and Checker.verify_type(self.state, str, no_list=True)
            and Checker.verify_type(self.postal, str, no_list=True)
            and Checker.verify_type(self.country, str, no_list=True)
            and Checker.verify_ext(Tag.ADDR, self.addr_ext)
            and Checker.verify_ext(Tag.CITY, self.city_ext)
            and Checker.verify_ext(Tag.STAE, self.stae_ext)
            and Checker.verify_ext(Tag.POST, self.post_ext)
            and Checker.verify_ext(Tag.CTRY, self.ctry_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = Default.EMPTY
        if self.validate():
            lines = Tagger.string(lines, level, Tag.ADDR, self.address)
            lines = Tagger.structure(lines, level + 1, self.addr_ext)
            lines = Tagger.string(lines, level + 1, Tag.CITY, self.city)
            lines = Tagger.structure(lines, level + 1, self.city_ext)
            lines = Tagger.string(lines, level + 1, Tag.STAE, self.state)
            lines = Tagger.structure(lines, level + 1, self.stae_ext)
            lines = Tagger.string(lines, level + 1, Tag.POST, self.postal)
            lines = Tagger.structure(lines, level + 1, self.post_ext)
            lines = Tagger.string(lines, level + 1, Tag.CTRY, self.country)
            lines = Tagger.structure(lines, level + 1, self.ctry_ext)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'Address',
                ('    address = ', self.address, tabs, full, True),
                ('    city = ', self.city, tabs, full, False),
                ('    state = ', self.state, tabs, full, False),
                ('    postal = ', self.postal, tabs, full, False),
                ('    country = ', self.country, tabs, full, False),
                ('    addr_ext = ', self.addr_ext, tabs, full, False),
                ('    city_ext = ', self.city_ext, tabs, full, False),
                ('    stae_ext = ', self.stae_ext, tabs, full, False),
                ('    post_ext = ', self.post_ext, tabs, full, False),
                ('    ctry_ext = ', self.ctry_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


AddrType = Address | None


class Age(NamedTuple):
    """Implement the Age data type in the GEDCOM specification.

    The GEDCOM specification requires that these age components be
    rounded down. The `phrase` parameter allows the user to
    add information about the data provided.

    Examples:
        >>> from genedata.store import Age, Phrase
        >>> from genedata.constants import String
        >>> print(
        ...     Age(
        ...         10,
        ...         greater_less_than='>',
        ...         phrase=Phrase('Estimated'),
        ...     ).ged(1)
        ... )
        1 AGE > 10y
        2 PHRASE Estimated
        <BLANKLINE>
        >>> print(Age(10, 2, 1, 2, '').ged(2))
        2 AGE 10y 2m 1w 2d
        <BLANKLINE>

    Args:
        years: The number of whole years in the age.
        months: The number of months in addition to the years.
        weeks: The number of weeks in addition to the years and months.
        days: The number of days in addition to any years, months, or weeks provided.
        greater_less_than: The default is '', which means that the age is exact
            to the day.  The option `>` means that the actual age
            is greater than the one provided.  The option `<` means
            that the actual age is less than the one provided.
        phrase: Addition information to clarify the data added.
        age_ext: Optional substructures extending [AGE tag](https://gedcom.io/terms/v7/AGE)
            entered through `Extension`.

    See Also:
        `Extension`

    Exceptions:
        ValueError: If greater_less_than is not one of {'', '<', '>'}.
        ValueError: If any value (except `phrase`) is not an integer.
        ValueError: If any value (except `phrase`) is less than 0.

    Reference:
        [GEDCOM AGE tag](https://gedcom.io/terms/v7/AGE)
        [GEDCOM Specification](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#age)

    > Age         = [[ageBound D] ageDuration]
    >
    > ageBound    = "<" / ">"
    > ageDuration = years [D months] [D weeks] [D days]
    >             / months [D weeks] [D days]
    >             / weeks [D days]
    >             / days
    >
    > years   = Integer %x79    ; 35y
    > months  = Integer %x6D    ; 11m
    > weeks   = Integer %x77    ; 8w
    > days    = Integer %x64    ; 21d
    """

    years: int = Default.YEARS
    months: int = Default.MONTHS
    weeks: int = Default.WEEKS
    days: int = Default.DAYS
    greater_less_than: str = Default.GREATER_LESS_THAN
    phrase: PhraseType = None
    age_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.years, int, no_list=True)
            and Checker.verify_type(self.months, int, no_list=True)
            and Checker.verify_type(self.weeks, int, no_list=True)
            and Checker.verify_type(self.days, int, no_list=True)
            and Checker.verify_type(self.phrase, Phrase, no_list=True)
            and Checker.verify_not_negative(self.years)
            and Checker.verify_not_negative(self.months)
            and Checker.verify_not_negative(self.weeks)
            and Checker.verify_not_negative(self.days)
            and Checker.verify_ext(Tag.AGE, self.age_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format the GEDCOM Age data type."""
        line: str = ''
        info: str = self.greater_less_than
        if self.validate() and (
            self.years > 0 or self.months > 0 or self.weeks > 0 or self.days > 0
        ):
            if self.years > 0:
                info = ''.join([info, f' {self.years!s}{Default.AGE_YEAR}'])
            if self.months > 0:
                info = ''.join([info, f' {self.months!s}{Default.AGE_MONTH}'])
            if self.weeks > 0:
                info = ''.join([info, f' {self.weeks!s}{Default.AGE_WEEK}'])
            if self.days > 0:
                info = ''.join([info, f' {self.days!s}{Default.AGE_DAY}'])
            info = (
                info.replace(Default.SPACE_DOUBLE, Default.SPACE)
                .replace(Default.SPACE_DOUBLE, Default.SPACE)
                .strip()
            )
            line = Tagger.string(line, level, Tag.AGE, info)
            line = Tagger.structure(line, level + 1, self.age_ext)
            line = Tagger.structure(line, level + 1, self.phrase)
        return line

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'Age',
                ('    years = ', self.years, tabs, full, False),
                ('    months = ', self.months, tabs, full, False),
                ('    weeks = ', self.weeks, tabs, full, False),
                ('    days = ', self.days, tabs, full, False),
                (
                    '    greater_less_than = ',
                    self.greater_less_than,
                    tabs,
                    full,
                    False,
                ),
                ('    phrase = ', self.phrase, tabs + 1, full, False),
                ('    age_ext = ', self.age_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


AgeType = Age | None


class PersonalNamePieces(NamedTuple):
    """Store, validate and display values for an optional GEDCOM Personal Name Piece.

    Example:
        This example includes all six of the Personal Name Piece tags.
        >>> from genedata.store import (
        ...     PersonalNamePieces,
        ... )  # doctest: +ELLIPSIS
        >>> from genedata.gedcom import Tag

    Args:
        prefix: An option list of NPFX or name prefixes of the name.
        given: An optional list of GIVN or given names of the name.
        nickname: An optional list of NICK or nicknames for the name.
        surname_prefix: An optional list of SPFX or surname prefixes of the name.
        surname: An optional list of SURN or surnames or last names of the name.
        suffix: An optional list NSFX or name suffixes of the name.
        npfx_ext: Optional substructures extending [NPFX tag](https://gedcom.io/terms/v7/NPFX)
            entered through `Extension`.
        givn_ext: Optional substructures extending [GIVN tag](https://gedcom.io/terms/v7/GIVN)
            entered through `Extension`.
        nick_ext: Optional substructures extending [NICK tag](https://gedcom.io/terms/v7/NICK)
            entered through `Extension`.
        spfx_ext: Optional substructures extending [SPFX tag](https://gedcom.io/terms/v7/SPFX)
            entered through `Extension`.
        surn_ext: Optional substructures extending [SURN tag](https://gedcom.io/terms/v7/SURN)
            entered through `Extension`.
        nsfx_ext: Optional substructures extending [NSFX tag](https://gedcom.io/terms/v7/NSFX)
            entered through `Extension`.

    See Also:
        `Extension`

    Reference:
        [GEDCOM GIVN tag](https://gedcom.io/terms/v7/GIVN)
        [GEDCOM NICK tag](https://gedcom.io/terms/v7/NICK)
        [GEDCOM NPFX tag](https://gedcom.io/terms/v7/NPFX)
        [GEDCOM NSFX tag](https://gedcom.io/terms/v7/NSFX)
        [GEDCOM SPFX tag](https://gedcom.io/terms/v7/SPFX)
        [GEDCOM SURN tag](https://gedcom.io/terms/v7/SURN)
        [GEDCOM Personal Name Pieces](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PERSONAL_NAME_PIECES)

    > n NPFX <Text>                              {0:M}  [g7:NPFX](https://gedcom.io/terms/v7/NPFX)
    > n GIVN <Text>                              {0:M}  [g7:GIVN](https://gedcom.io/terms/v7/GIVN)
    > n NICK <Text>                              {0:M}  [g7:NICK](https://gedcom.io/terms/v7/NICK)
    > n SPFX <Text>                              {0:M}  [g7:SPFX](https://gedcom.io/terms/v7/SPFX)
    > n SURN <Text>                              {0:M}  [g7:SURN](https://gedcom.io/terms/v7/SURN)
    > n NSFX <Text>                              {0:M}  [g7:NSFX](https://gedcom.io/terms/v7/NSFX)
    """

    prefix: str | list[str] = Default.EMPTY
    given: str | list[str] = Default.EMPTY
    nickname: str | list[str] = Default.EMPTY
    surname_prefix: str | list[str] = Default.EMPTY
    surname: str | list[str] = Default.EMPTY
    suffix: str | list[str] = Default.EMPTY
    npfx_ext: ExtType = None
    givn_ext: ExtType = None
    nick_ext: ExtType = None
    spfx_ext: ExtType = None
    surn_ext: ExtType = None
    nsfx_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        length: int = (
            len(self.prefix)
            + len(self.given)
            + len(self.nickname)
            + len(self.surname_prefix)
            + len(self.surname)
            + len(self.suffix)
        )
        if length == 0:
            raise ValueError(Msg.PIECES_EMPTY)
        check: bool = (
            Checker.verify_type(self.prefix, str)
            and Checker.verify_type(self.given, str)
            and Checker.verify_type(self.nickname, str)
            and Checker.verify_type(self.surname_prefix, str)
            and Checker.verify_type(self.surname, str)
            and Checker.verify_type(self.suffix, str)
            and Checker.verify_ext(Tag.NPFX, self.npfx_ext)
            and Checker.verify_ext(Tag.GIVN, self.givn_ext)
            and Checker.verify_ext(Tag.NICK, self.nick_ext)
            and Checker.verify_ext(Tag.SPFX, self.spfx_ext)
            and Checker.verify_ext(Tag.SURN, self.surn_ext)
            and Checker.verify_ext(Tag.NSFX, self.nsfx_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.NPFX, self.prefix)
            lines = Tagger.structure(lines, level + 1, self.npfx_ext)
            lines = Tagger.string(lines, level, Tag.GIVN, self.given)
            lines = Tagger.structure(lines, level + 1, self.givn_ext)
            lines = Tagger.string(lines, level, Tag.NICK, self.nickname)
            lines = Tagger.structure(lines, level + 1, self.nick_ext)
            lines = Tagger.string(lines, level, Tag.SPFX, self.surname_prefix)
            lines = Tagger.structure(lines, level + 1, self.spfx_ext)
            lines = Tagger.string(lines, level, Tag.SURN, self.surname)
            lines = Tagger.structure(lines, level + 1, self.surn_ext)
            lines = Tagger.string(lines, level, Tag.NSFX, self.suffix)
            lines = Tagger.structure(lines, level + 1, self.nsfx_ext)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'PersonalNamePieces',
                ('    prefix = ', self.prefix, tabs + 1, full, False),
                ('    given = ', self.given, tabs + 1, full, False),
                ('    nickname = ', self.nickname, tabs + 1, full, False),
                (
                    '    surname_prefix = ',
                    self.surname_prefix,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    surname = ', self.surname, tabs + 1, full, False),
                ('    suffix = ', self.suffix, tabs + 1, full, False),
                ('    npfx_ext = ', self.npfx_ext, tabs, full, False),
                ('    givn_ext = ', self.givn_ext, tabs, full, False),
                ('    nick_ext = ', self.nick_ext, tabs, full, False),
                ('    spfx_ext = ', self.spfx_ext, tabs, full, False),
                ('    surn_ext = ', self.surn_ext, tabs, full, False),
                ('    nsfx_ext = ', self.nsfx_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


PersonalNamePiecesType = PersonalNamePieces | None


class NameTranslation(NamedTuple):
    """Store, validate and display name translations.

    The BCP 47 language tag is a hyphenated list of subtags.
    The [W3C Internationalization](https://www.w3.org/International/questions/qa-choosing-language-tags)
    guide will help one make a decision on which tags to use.
    The [Language Subtag Lookup Tool](https://r12a.github.io/app-subtags/)
    can assist with finding and checking the language tag one would like to use.

    Example:
        In this example, the name "Joe" will be translated as "喬" in Chinese.
        Although the `ged` method to display preforms a validation first,
        this example will show that and then display the data using
        the GEDCOM standard.  No personal name pieces will be displayed.
        >>> from genedata.store import Lang, NameTranslation
        >>> joe_in_chinese = '喬'
        >>> language = Lang('cmn')
        >>> nt = NameTranslation(joe_in_chinese, language)
        >>> nt.validate()
        True
        >>> print(nt.ged(1))
        1 TRAN 喬
        2 LANG cmn
        <BLANKLINE>

    Args:
        translation: The text of the translation.
        language: The BCP 47 language tag entered through `Lang`.
        name_pieces: an optional tuple of PersonalNamePieces entered through `PersonalNamePieces`.
        tran_ext: Optional substructures extending [TRAN tag](https://gedcom.io/terms/v7/TRAN)
            entered through `Extension`.

    See Also:
        `Extension`
        `Lang`
        `PersonalNamePieces`

    Reference:
        [GEDCOM TRAN tag](https://gedcom.io/terms/v7/TRAN)
        [GEDCOM Pesonal Name Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PERSONAL_NAME_STRUCTURE)

    This is not a specified GEDCOM structure, but implements this portion of `PersonalNamePieces`.
    > +1 TRAN <PersonalName>                   {0:M}  g7:NAME-TRAN
    >    +2 LANG <Language>                    {1:1}  g7:LANG
    >    +2 <<PERSONAL_NAME_PIECES>>           {0:1}
    """

    translation: str = Default.EMPTY
    language: LangType = None
    pieces: PersonalNamePiecesType = None
    tran_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.translation, str)
            and Checker.verify_not_empty(self.translation)
            and Checker.verify_type(self.language, Lang)
            and Checker.verify_not_empty(self.language)
            and Checker.verify_type(self.pieces, PersonalNamePieces)
            and Checker.verify_ext(Tag.TRAN, self.tran_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.TRAN, self.translation)
            lines = Tagger.structure(lines, level + 1, self.tran_ext)
            lines = Tagger.structure(lines, level + 1, self.language)
            lines = Tagger.structure(lines, level + 1, self.pieces)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'NameTranslation',
                ('    translation = ', self.translation, tabs, full, True),
                ('    language = ', self.language, tabs + 1, full, True),
                ('    pieces = ', self.pieces, tabs + 1, full, False),
                ('    tran_ext = ', self.tran_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


NameTranType = NameTranslation | list[NameTranslation] | None


class NoteTranslation(NamedTuple):
    """Store, validate and display the optional note tranlation section of
    the GEDCOM Note Structure.

    The BCP 47 language tag is a hyphenated list of subtags.
    The [W3C Internationalization](https://www.w3.org/International/questions/qa-choosing-language-tags)
    guide will help one make a decision on which tags to use.
    The [Language Subtag Lookup Tool](https://r12a.github.io/app-subtags/)
    can assist with finding and checking the language tag one would like to use.

    Example:
        This example will translation "This is a note." into the Arabic "هذه ملاحظة.".
        >>> from genedata.store import Lang, NoteTranslation
        >>> from genedata.gedcom import Default
        >>> arabic_text = 'هذه ملاحظة.'
        >>> mime = Default.MIME
        >>> language = Lang('afb')
        >>> nt = NoteTranslation(arabic_text, mime, language)
        >>> nt.validate()
        True
        >>> print(nt.ged(1))
        1 TRAN هذه ملاحظة.
        2 LANG afb
        <BLANKLINE>

    Args:
        translation: The text of the translation for the note.
        mime: The mime type of the translation.
        language: The BCP 47 language tag of the translation entered through `Lang`.
        tran_ext: Optional substructures extending [TRAN tag](https://gedcom.io/terms/v7/TRAN)
            entered through `Extension`.
        mime_ext: Optional substructures extending [MIME tag](https://gedcom.io/terms/v7/MIME)
            entered through `Extension`.

    See Also:
        `Lang`
        `Extension`


    Reference:
        [GEDCOM MIME tag](https://gedcom.io/terms/v7/MIME)
        [GEDCOM TRAN tag](https://gedcom.io/terms/v7/TRAN)
        [GEDCOM Note Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#NOTE_STRUCTURE)]

    This is not a specific GEDCOM structure but implements this part of `Note`
    > +1 TRAN <Text>                           {0:M}  g7:NOTE-TRAN
    >    +2 MIME <MediaType>                   {0:1}  g7:MIME
    >    +2 LANG <Language>                    {0:1}  g7:LANG
    """

    translation: str = Default.EMPTY
    mime: str = Default.MIME
    language: LangType = None
    tran_ext: ExtType = None
    mime_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.translation, str, no_list=True)
            and Checker.verify_not_empty(self.translation)
            and Checker.verify_type(self.mime, str, no_list=True)
            and Checker.verify_type(self.language, Lang, no_list=True)
            and Checker.verify_ext(Tag.TRAN, self.tran_ext)
            and Checker.verify_ext(Tag.MIME, self.mime_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.translation != Default.EMPTY and self.validate():
            lines = Tagger.string(lines, level, Tag.TRAN, self.translation)
            lines = Tagger.structure(lines, level + 1, self.tran_ext)
            lines = Tagger.string(lines, level + 1, Tag.MIME, self.mime)
            lines = Tagger.structure(lines, level + 2, self.mime_ext)
            lines = Tagger.structure(lines, level + 1, self.language)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'NoteTranslation',
                ('    translation = ', self.translation, tabs, full, True),
                ('    mime = ', self.mime, tabs, full, False),
                ('    language = ', self.language, tabs + 1, full, False),
                ('    tran_ext = ', self.tran_ext, tabs, full, False),
                ('    mime_ext = ', self.mime_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


NoteTranType = NoteTranslation | list[NoteTranslation] | None


class CallNumber(NamedTuple):
    """Store, validate and display the option call numbers for the
    SourceRepositoryCitation substructure.

    Example:
        This example assumes there is a call number "1111" which is the
        minimal amount of information needed to use this optional feature.
        >>> from genedata.store import CallNumber
        >>> cn = CallNumber('1111')
        >>> cn.validate()
        True
        >>> print(cn.ged(1))
        1 CALN 1111
        <BLANKLINE>

        This next example uses all of the optional positions.
        >>> from genedata.gedcom import Tag
        >>> cn_all = CallNumber('1111', Tag.BOOK, Phrase('New Testament'))
        >>> print(cn_all.ged(1))
        1 CALN 1111
        2 MEDI BOOK
        3 PHRASE New Testament
        <BLANKLINE>

    Args:
        call_number: A required value to use this structure containing the call number.
        medium: A tag from the
            [MEDI enumeration set](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#enumset-MEDI)
            entered by placing `Tag.` in front of the capitalized name from the set.
        phrase: PhraseType = None
        caln_ext: Optional substructures extending [CALN tag](https://gedcom.io/terms/v7/CALN)
            entered through `Extension`.
        medi_ext: Optional substructures extending [MEDI tag](https://gedcom.io/terms/v7/MEDI)
            entered through `Extension`.


    See Also:
        `SourceRepositoryCitation`: the superstructure of this NamedTuple.
        `Extension`

    Reference:
        [GEDCOM MEDI enumeration set](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#enumset-MEDI)
        [GEDCOM CALN tag](https://gedcom.io/terms/v7/CALN)
        [GEDCOM MEDI tag](https://gedcom.io/terms/v7/MEDI)
        [GEDCOM Source Repository Citation](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_REPOSITORY_CITATION)

    >   +1 CALN <Special>                        {0:M}  [g7:CALN](https://gedcom.io/terms/v7/CALN)
    >      +2 MEDI <Enum>                        {0:1}  [g7:MEDI](https://gedcom.io/terms/v7/MEDI)
    >         +3 PHRASE <Text>                   {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    """

    call_number: str = Default.EMPTY
    medium: Tag = Tag.NONE
    phrase: PhraseType = None
    caln_ext: ExtType = None
    medi_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.call_number, str)
            and Checker.verify_not_empty(self.call_number)
            and Checker.verify_enum(self.medium, Medium)
            and Checker.verify_type(self.phrase, Phrase)
            and Checker.verify_ext(Tag.CALN, self.caln_ext)
            and Checker.verify_ext(Tag.MEDI, self.medi_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.CALN, self.call_number)
            lines = Tagger.structure(lines, level + 1, self.caln_ext)
            lines = Tagger.string(lines, level + 1, Tag.MEDI, self.medium.value)
            lines = Tagger.structure(lines, level + 2, self.medi_ext)
            lines = Tagger.structure(lines, level + 2, self.phrase)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'CallNumber',
                ('    call_number = ', self.call_number, tabs, full, True),
                ('    medium = ', self.medium, tabs, full, False),
                ('    phrase = ', self.phrase, tabs + 1, full, False),
                ('    caln_ext = ', self.caln_ext, tabs + 1, full, False),
                ('    medi_ext = ', self.medi_ext, tabs + 1, full, False),
            ),
            Default.INDENT * tabs,
        )


CalnType = CallNumber | list[CallNumber] | None


class Text(NamedTuple):
    """Store, validate and display a text in the GEDCOM standard.

    A Source Citation structure can have multiple texts associated with it.  This NamedTuple describes
    a specific text.

    Examples:

    Args:
        text: The text being added.
        mime: The media type of the text.
        language: The BCP 47 language tag for the text entered through `Lang`.
        text_ext: Optional substructures extending [TEXT tag](https://gedcom.io/terms/v7/TEXT)
            entered through `Extension`.
        mime_ext: Optional substructures extending [MIME tag](https://gedcom.io/terms/v7/MIME)
            entered through `Extension`.

    See Also:
        `Extension`
        `Lang`

    Reference:
        [GEDCOM MIME tag](https://gedcom.io/terms/v7/MIME)
        [GEDCOM TEXT tag](https://gedcom.io/terms/v7/TEXT)
        [GEDCOM Source Citation](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_CITATION)

    This is part of the GEDCOM Source Citation structure.
    >      +2 TEXT <Text>                        {0:M}  g7:TEXT
    >         +3 MIME <MediaType>                {0:1}  g7:MIME
    >         +3 LANG <Language>                 {0:1}  g7:LANG
    """

    text: str = Default.EMPTY
    mime: str = Default.MIME
    language: LangType = None
    text_ext: ExtType = None
    mime_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.text, str)
            and Checker.verify_not_empty(self.text)
            and Checker.verify_type(self.mime, str)
            and Checker.verify_type(self.language, Lang)
            and Checker.verify_ext(Tag.TEXT, self.text_ext)
            and Checker.verify_ext(Tag.MIME, self.mime_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.TEXT, str(self.text))
            lines = Tagger.structure(lines, level + 1, self.text_ext)
            lines = Tagger.string(lines, level + 1, Tag.MIME, self.mime)
            lines = Tagger.structure(lines, level + 1, self.mime_ext)
            lines = Tagger.structure(lines, level + 1, self.language)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'Text',
                ('    text = ', self.text, tabs, full, True),
                ('    mime = ', self.mime, tabs, full, False),
                ('    language = ', self.language, tabs + 1, full, False),
                ('    text_ext = ', self.text_ext, tabs, full, False),
                ('    mime_ext = ', self.mime_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


TextType = Text | list[Text] | None


class SourceData(NamedTuple):
    """_summary_

    Examples:


    Args:
        date_value: The date entered through `Date`.
        texts: a list of texts associated with this source entered through `Text`.
        data_ext: Optional substructures extending [DATA tag](https://gedcom.io/terms/v7/DATA)
            entered through `Extension`.

    See Also:
        `Date`
        `Extension`
        `Text`

    Reference:
        [GEDCOM DATA tag](https://gedcom.io/terms/v7/DATA)
        [GEDCOM Source Citation](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_CITATION)

    This is not a GEDCOM structure, but part of the Source Citation structure.
    >   +1 DATA                                  {0:1}  g7:SOUR-DATA
    >      +2 <<DATE_VALUE>>                     {0:1}
    >      +2 TEXT <Text>                        {0:M}  g7:TEXT
    >         +3 MIME <MediaType>                {0:1}  g7:MIME
    >         +3 LANG <Language>                 {0:1}  g7:LANG
    """

    date: DateType = None
    texts: TextType = None
    data_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.date, Date)
            and Checker.verify_type(self.texts, Text)
            and Checker.verify_ext(Tag.DATA, self.data_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.empty(lines, level, Tag.DATA)
            lines = Tagger.structure(lines, level + 1, self.data_ext)
            lines = Tagger.structure(lines, level, self.date)
            lines = Tagger.structure(lines, level + 1, self.texts)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'SourceData',
                ('    date = ', self.date, tabs + 1, full, False),
                ('    texts = ', self.texts, tabs + 1, full, False),
                ('    data_ext = ', self.data_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


SourDataType = SourceData | None


class SourceCitation(NamedTuple):
    """Store, validate and display the Source Citation
    substructure of the GEDCOM standard.

    Examples:


    Args:
        source_xref: The source cross reference identifier constructed using `genedata.build.source_xref`.
        page: The page number of the citation.
        source_data: A reference to the source data entered through `SourceData`.
        event: A tag from the [EVEN enumeration set](https://gedcom.io/terms/v7/enumset-EVEN).
            entered by placing `Tag.` in front of the capitalized name from the set.
        event_phrase: A phrase describing the event entered through `Phrase`.
        role: A tag from the [ROLE enumeration set](https://gedcom.io/terms/v7/enumset-ROLE)
            entered by placing `Tag.` in front of the capitalized name from the set.
        role_phrase: A phrase describing the role entered through `Phrase`.
        quality: A tag from the [QUAY enumeration set](https://gedcom.io/terms/v7/enumset-QUAY)
            entered by placing `Tag.QUAY` in front of the number (0, 1, 2, 3) from the set.
        multimedialinks: Multimedia links entered through `MultimediaLink`.
        notes: Notes entered through `Note`.
        sour_ext: Optional substructures extending [SOUR tag](https://gedcom.io/terms/v7/SOUR)
            entered through `Extension`.
        page_ext: Optional substructures extending [PAGE tag](https://gedcom.io/terms/v7/PAGE)
            entered through `Extension`.
        even_ext: Optional substructures extending [EVEN tag](https://gedcom.io/terms/v7/EVEN)
            entered through `Extension`.
        role_ext: Optional substructures extending [ROLE tag](https://gedcom.io/terms/v7/ROLE)
            entered through `Extension`.
        quay_ext: Optional substructures extending [QUAY tag](https://gedcom.io/terms/v7/QUAY)
            entered through `Extension`.

    See Also:
        `genedata.build.source_xref`
        `Extension`
        `MultimediaLink`
        `Note`
        `Phrase`
        `SourceData`

    Reference:
        [GEDCOM EVEN enumeration set](https://gedcom.io/terms/v7/enumset-EVEN)
        [GEDCOM QUAY enumeration set](https://gedcom.io/terms/v7/enumset-QUAY)
        [GEDCOM ROLE enumeration set](https://gedcom.io/terms/v7/enumset-ROLE)
        [GEDCOM EVEN tag](https://gedcom.io/terms/v7/EVEN)
        [GEDCOM PAGE tag](https://gedcom.io/terms/v7/PAGE)
        [GEDCOM QUAY tag](https://gedcom.io/terms/v7/QUAY)
        [GEDCOM ROLE tag](https://gedcom.io/terms/v7/ROLE)
        [GEDCOM SOUR tag](https://gedcom.io/terms/v7/SOUR)
        [GEDCOM Source Citation](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_CITATION)

    > n SOUR @<XREF:SOUR>@                       {1:1}  g7:SOUR
    >   +1 PAGE <Text>                           {0:1}  g7:PAGE
    >   +1 DATA                                  {0:1}  g7:SOUR-DATA
    >      +2 <<DATE_VALUE>>                     {0:1}
    >      +2 TEXT <Text>                        {0:M}  g7:TEXT
    >         +3 MIME <MediaType>                {0:1}  g7:MIME
    >         +3 LANG <Language>                 {0:1}  g7:LANG
    >   +1 EVEN <Enum>                           {0:1}  g7:SOUR-EVEN
    >      +2 PHRASE <Text>                      {0:1}  g7:PHRASE
    >      +2 ROLE <Enum>                        {0:1}  g7:ROLE
    >         +3 PHRASE <Text>                   {0:1}  g7:PHRASE
    >   +1 QUAY <Enum>                           {0:1}  g7:QUAY
    >   +1 <<MULTIMEDIA_LINK>>                   {0:M}
    >   +1 <<NOTE_STRUCTURE>>                    {0:M}
    """

    source_xref: SourceXref = Void.SOUR
    page: str = Default.EMPTY
    source_data: SourDataType = None
    event: Tag = Tag.NONE
    event_phrase: PhraseType = None
    role: Tag = Tag.NONE
    role_phrase: PhraseType = None
    quality: Tag = Tag.NONE
    multimedialinks: AnyList = None
    notes: AnyList = None
    sour_ext: ExtType = None
    page_ext: ExtType = None
    even_ext: ExtType = None
    role_ext: ExtType = None
    quay_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.source_xref, SourceXref)
            and Checker.verify_not_empty(self.source_xref)
            and Checker.verify_type(self.page, str, no_list=True)
            and Checker.verify_type(self.source_data, SourceData, no_list=True)
            and Checker.verify_enum(self.event, Even)
            and Checker.verify_type(self.event_phrase, Phrase, no_list=True)
            and Checker.verify_enum(self.role, Role)
            and Checker.verify_type(self.role_phrase, Phrase, no_list=True)
            and Checker.verify_enum(self.quality, Quay)
            and Checker.verify_type(self.multimedialinks, MultimediaLink)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_ext(Tag.SOUR, self.sour_ext)
            and Checker.verify_ext(Tag.PAGE, self.page_ext)
            and Checker.verify_ext(Tag.EVEN, self.even_ext)
            and Checker.verify_ext(Tag.ROLE, self.role_ext)
            and Checker.verify_ext(Tag.QUAY, self.quay_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(
                lines, level, Tag.SOUR, str(self.source_xref), format=False
            )
            lines = Tagger.structure(lines, level + 1, self.sour_ext)
            lines = Tagger.string(lines, level + 1, Tag.PAGE, self.page)
            lines = Tagger.structure(lines, level + 2, self.page_ext)
            lines = Tagger.structure(lines, level + 1, self.source_data)
            if self.event != Tag.NONE:
                lines = Tagger.string(
                    lines, level + 1, Tag.EVEN, self.event.value
                )
                lines = Tagger.structure(lines, level + 1, self.even_ext)
                lines = Tagger.structure(lines, level + 2, self.event_phrase)
                lines = Tagger.string(
                    lines, level + 2, Tag.ROLE, self.role.value
                )
                lines = Tagger.structure(lines, level + 1, self.role_ext)
                lines = Tagger.structure(lines, level + 2, self.role_phrase)
            lines = Tagger.string(
                lines, level + 1, Tag.QUAY, self.quality.value
            )
            lines = Tagger.structure(lines, level + 1, self.quay_ext)
            lines = Tagger.structure(lines, level + 1, self.multimedialinks)
            lines = Tagger.structure(lines, level + 1, self.notes)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'SourceCitation',
                ('    source_xref = ', self.source_xref, tabs, full, True),
                ('    page = ', self.page, tabs, full, False),
                ('    source_data = ', self.source_data, tabs + 1, full, False),
                ('    event = ', self.event, tabs + 1, full, False),
                (
                    '    event_phrase = ',
                    self.event_phrase,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    role = ', self.role, tabs, full, False),
                ('    role_phrase = ', self.role_phrase, tabs + 1, full, False),
                ('    quality = ', self.quality, tabs, full, False),
                (
                    '    multimedialinks = ',
                    self.multimedialinks,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    notes = ', self.notes, tabs + 1, full, False),
                ('    sour_ext = ', self.sour_ext, tabs, full, False),
                ('    page_ext = ', self.page_ext, tabs, full, False),
                ('    even_ext = ', self.even_ext, tabs, full, False),
                ('    role_ext = ', self.role_ext, tabs, full, False),
                ('    quay_ext = ', self.quay_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


SourCiteType = SourceCitation | list[SourceCitation] | None


class Note(NamedTuple):
    """Store, validate and display a note substructure of the GEDCOM standard.

    The BCP 47 language tag is a hyphenated list of subtags.
    The [W3C Internationalization](https://www.w3.org/International/questions/qa-choosing-language-tags)
    guide will help one make a decision on which tags to use.
    The [Language Subtag Lookup Tool](https://r12a.github.io/app-subtags/)
    can assist with finding and checking the language tag one would like to use.

    Example:
        This example is a note without other information.
        >>> from genedata.store import Lang, Note
        >>> note = Note(note='This is my note.')
        >>> print(note.ged(1))
        1 NOTE This is my note.
        <BLANKLINE>

        A note line may be continued onto two lines if the "\\n" character
        appears in the note as illustrated in the [GEDCOM Line standard](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#lines).
        >>> multi_line_note = Note(
        ...     note='This is a note field that\\n  spans four lines.\\n\\n(the third line was blank)'
        ... )
        >>> print(multi_line_note.ged(1))
        1 NOTE This is a note field that
        2 CONT   spans four lines.
        2 CONT
        2 CONT (the third line was blank)
        <BLANKLINE>

        This example uses the Hebrew language translating "This is my note." as "זו ההערה שלי."
        The translation comes from [Google Translate](https://translate.google.com/?sl=en&tl=iw&text=This%20is%20my%20note.&op=translate).
        >>> hebrew_note = Note(note='זו ההערה שלי.', language=Lang('he'))
        >>> print(hebrew_note.ged(1))
        1 NOTE זו ההערה שלי.
        2 LANG he
        <BLANKLINE>

        The next example adds translations of the previous example to the note.
        >>> from genedata.gedcom import Default
        >>> english_translation = NoteTranslation(
        ...     'This is my note.', Default.MIME, Lang('en')
        ... )
        >>> urdu_translation = NoteTranslation(
        ...     'یہ میرا نوٹ ہے۔', Default.MIME, Lang('ur')
        ... )
        >>> hebrew_note_with_translations = Note(
        ...     note='זו ההערה שלי.',
        ...     language=Lang('he'),
        ...     translations=[
        ...         english_translation,
        ...         urdu_translation,
        ...     ],
        ... )
        >>> print(hebrew_note_with_translations.ged(1))
        1 NOTE זו ההערה שלי.
        2 LANG he
        2 TRAN This is my note.
        3 LANG en
        2 TRAN یہ میرا نوٹ ہے۔
        3 LANG ur
        <BLANKLINE>


    Args:
        text: The text of the note.
        mime: The optional media type of the note.
        language: The optional BCP 47 language tag for the note entered through `Lang`.
        translations: Translations entered through `NoteTranslation`.
        citations: Citations entered through `SourceCitation`.
        note_ext: Optional substructures extending [NOTE tag](https://gedcom.io/terms/v7/NOTE)
            entered through `Extension`.
        mime_ext: Optional substructures extending [MIME tag](https://gedcom.io/terms/v7/MIME)
            entered through `Extension`.

    See Also:
        `Extension`
        `Lang`
        `NoteTranslation`
        `SourceCitation`

    Reference:
        [W3C Internationalization](https://www.w3.org/International/questions/qa-choosing-language-tags)
        [Language Subtag Lookup Tool](https://r12a.github.io/app-subtags/)
        [GEDCOM MIME tag](https://gedcom.io/terms/v7/MIME)
        [GEDCOM NOTE tag](https://gedcom.io/terms/v7/NOTE)
        [GEDCOM Note Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#NOTE_STRUCTURE)

    [
    n NOTE <Text>                              {1:1}  g7:NOTE
      +1 MIME <MediaType>                      {0:1}  g7:MIME
      +1 LANG <Language>                       {0:1}  g7:LANG
      +1 TRAN <Text>                           {0:M}  g7:NOTE-TRAN
         +2 MIME <MediaType>                   {0:1}  g7:MIME
         +2 LANG <Language>                    {0:1}  g7:LANG
      +1 <<SOURCE_CITATION>>                   {0:M}
    |
    n SNOTE @<XREF:SNOTE>@                     {1:1}  g7:SNOTE
    ]
    """  # noqa: RUF002

    note: str = Default.EMPTY
    mime: str = Default.MIME
    language: LangType = None
    translations: NoteTranType = None
    source_citations: SourCiteType = None
    note_ext: ExtType = None
    mime_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.note, str, no_list=True)
            and Checker.verify_not_empty(self.note)
            and Checker.verify_type(self.mime, str)
            and Checker.verify_type(self.language, Lang, no_list=True)
            and Checker.verify_type(self.translations, NoteTranslation)
            and Checker.verify_type(self.source_citations, SourceCitation)
            and Checker.verify_ext(Tag.NOTE, self.note_ext)
            and Checker.verify_ext(Tag.MIME, self.mime_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.NOTE, self.note)
            lines = Tagger.structure(lines, level + 1, self.note_ext)
            lines = Tagger.string(lines, level + 1, Tag.MIME, self.mime)
            lines = Tagger.structure(lines, level + 2, self.mime_ext)
            lines = Tagger.structure(lines, level + 1, self.language)
            lines = Tagger.structure(lines, level + 1, self.translations)
            lines = Tagger.structure(lines, level + 1, self.source_citations)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'Note',
                ('    note = ', self.note, tabs, full, True),
                ('    mime = ', self.mime, tabs, full, False),
                ('    language = ', self.language, tabs + 1, full, False),
                (
                    '    translations = ',
                    self.translations,
                    tabs + 1,
                    full,
                    False,
                ),
                (
                    '    soource_citations = ',
                    self.source_citations,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    note_ext = ', self.note_ext, tabs, full, False),
                ('    mime_ext = ', self.mime_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


NoteType = Note | list[Note] | None


class SNote(NamedTuple):
    """Store, validate and display a shared note substructure of the GEDCOM standard.

    The BCP 47 language tag is a hyphenated list of subtags.
    The [W3C Internationalization](https://www.w3.org/International/questions/qa-choosing-language-tags)
    guide will help one make a decision on which tags to use.
    The [Language Subtag Lookup Tool](https://r12a.github.io/app-subtags/)
    can assist with finding and checking the language tag one would like to use.

    Example:

    Args:
        snote_xref: The shared note cross reference identifier constructed from `genedata.build.shared_note_xref`.
        snote_ext: Optional substructures extending [SNOTE tag](https://gedcom.io/terms/v7/SNOTE)
            entered through `Extension`.

    See Also:
        `Extension`
        `genedata.build.shared_note_xref`

    Reference:
        [W3C Internationalization](https://www.w3.org/International/questions/qa-choosing-language-tags)
        [Language Subtag Lookup Tool](https://r12a.github.io/app-subtags/)
        [GEDCOM SNOTE tag](https://gedcom.io/terms/v7/SNOTE)
        [GEDCOM Note Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#NOTE_STRUCTURE)

    n SNOTE @<XREF:SNOTE>@                     {1:1}  g7:SNOTE
    """

    snote_xref: SharedNoteXref = Void.SNOTE
    snote_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.snote_xref, SharedNoteXref, no_list=True)
            and Checker.verify_not_empty(self.snote_xref)
            and Checker.verify_ext(Tag.SNOTE, self.snote_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(
                lines, level, Tag.SNOTE, self.snote_xref.fullname
            )
            lines = Tagger.structure(lines, level + 1, self.snote_ext)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'SNote',
                ('    snote_xref = ', self.snote_xref, tabs, full, True),
                ('    snote_ext = ', self.snote_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


SNoteType = SNote | list[SNote] | None


class ChangeDate(NamedTuple):
    """Store, validate and format change date information.

    Example:

    Args:
        date: The date entered through `Date`.
        time: The time entered through `Time`.
        notes: Notes entered through `Note`.
        chan_ext: Optional substructures extending [CHAN tag](https://gedcom.io/terms/v7/CHAN)
            entered through `Extension`.

    See Also:
        `Date`
        `Extension`
        `Note`
        `Time`

    Reference:
        [GEDCOM CHAN tag](https://gedcom.io/terms/v7/CHAN)
        [GEDCOM Change Date](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#CHANGE_DATE)

    > n CHAN                                     {1:1}  g7:CHAN
    >   +1 DATE <DateExact>                      {1:1}  g7:DATE-exact
    >      +2 TIME <Time>                        {0:1}  g7:TIME
    >   +1 <<NOTE_STRUCTURE>>                    {0:M}
    """

    date: DateType = None
    time: TimeType = None
    notes: NoteType = None
    chan_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.date, Date, no_list=True)
            and Checker.verify_not_empty(self.date)
            and Checker.verify_type(self.time, Time, no_list=True)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_ext(Tag.CHAN, self.chan_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.empty(lines, level, Tag.CHAN)
            lines = Tagger.structure(lines, level + 1, self.date)
            lines = Tagger.structure(lines, level + 2, self.time)
            lines = Tagger.structure(lines, level + 1, self.notes)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'ChangeDate',
                ('    date = ', self.date, tabs + 1, full, True),
                ('    time = ', self.time, tabs + 1, full, False),
                ('    notes = ', self.notes, tabs + 1, full, False),
                ('    chan_ext = ', self.chan_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


ChangeDateType = ChangeDate | None


class SourceRepositoryCitation(NamedTuple):
    """Store, validate and display the optional Source Repository Citation
     substructure of the GEDCOM standard.

    Examples:

    Args:
        repo: The cross reference repository identifier constructed from `genedata.build.repository_xref`.
        notes: Notes entered through `Note`.
        call_numbers: Call numbers entered through `CallNumber`.
        repo_ext: Optional substructures extending [REPO tag](https://gedcom.io/terms/v7/REPO)
            entered through `Extension`.

    See Also:
        `CallNumber`
        `Extension`
        `genedata.build.repository_xref`

    Reference:
        [GEDCOM REPO tag](https://gedcom.io/terms/v7/REPO)
        [GEDCOM Source Repository Citation](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_REPOSITORY_CITATION)

    > n REPO @<XREF:REPO>@                       {1:1}  [g7:REPO](https://gedcom.io/terms/v7/REPO)
    >   +1 <<NOTE_STRUCTURE>>                    {0:M}
    >   +1 CALN <Special>                        {0:M}  [g7:CALN](https://gedcom.io/terms/v7/CALN)
    >      +2 MEDI <Enum>                        {0:1}  [g7:MEDI](https://gedcom.io/terms/v7/MEDI)
    >         +3 PHRASE <Text>                   {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    """

    repository_xref: RepositoryXref = Void.REPO
    notes: NoteType = None
    call_numbers: CalnType = None
    repo_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(
                self.repository_xref, RepositoryXref, no_list=True
            )
            and Checker.verify_not_empty(self.repository_xref)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_type(self.call_numbers, CallNumber)
            and Checker.verify_ext(Tag.REPO, self.repo_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.repository_xref.fullname != Void.NAME and self.validate():
            lines = Tagger.string(
                lines, level, Tag.SOUR, str(self.repository_xref)
            )
            lines = Tagger.structure(lines, level + 1, self.repo_ext)
            lines = Tagger.structure(lines, level, self.notes)
            lines = Tagger.structure(lines, level, self.call_numbers)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'SourceRepositoryCitation',
                (
                    '    repository_xref = ',
                    self.repository_xref,
                    tabs,
                    full,
                    True,
                ),
                ('    notes = ', self.notes, tabs + 1, full, False),
                (
                    '    call_numbers = ',
                    self.call_numbers,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    repo_ext = ', self.repo_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


SourRepoCiteType = (
    SourceRepositoryCitation | list[SourceRepositoryCitation] | None
)


class PersonalName(NamedTuple):
    """Store, validate and display a personal name.

    Example:
        The first example will not only test ChronoData but also the extend
        the GEDCOM standard can store various kinds of information.  I will want
        to record the first man who was first mentioned in Genesis 1:26, Adam,
        using the Hebrew word "אָדָ֛ם". I obtained the name from
        [Chabad](https://www.chabad.org/library/bible_cdo/aid/8165/jewish/Chapter-1.htm)
        which I could add in as a `SourceCitation`.  In Genesis 2:16 Adam is
        also referred to as "הָֽאָדָ֖ם" which I will use as a nickname and translate
        it into English as "the man".

        I will validate it first to make sure it is correct, but this is not required.
        Note the trailing "," in the `translations` parameter.  Even though there
        is only one translation, this is required to guarantee the tuple
        is not interpreted as a string of letters.
        >>> from genedata.store import (
        ...     Lang,
        ...     NameTranslation,
        ...     Note,
        ...     PersonalName,
        ...     PersonalNamePieces,
        ...     Phrase,
        ...     SourceCitation,
        ... )
        >>> from genedata.gedcom import NameType, PersonalNamePieceTag
        >>> adam_note = Note(note='Here is a place to add more information.')
        >>> adam_english = NameTranslation(
        ...     'Adam', Lang('en'), PersonalNamePieces(nickname='the man')
        ... )
        >>> adam = PersonalName(
        ...     name='אָדָ֛ם',
        ...     surname=' ',
        ...     type=Tag.OTHER,
        ...     phrase=Phrase('The first man'),
        ...     pieces=PersonalNamePieces(nickname='הָֽאָדָ֖ם'),
        ...     translations=adam_english,
        ...     notes=adam_note,
        ... )
        >>> print(adam.ged(1))
        1 NAME אָדָ֛ם / /
        2 TYPE OTHER
        3 PHRASE The first man
        2 NICK הָֽאָדָ֖ם
        2 TRAN Adam
        3 LANG en
        3 NICK the man
        2 NOTE Here is a place to add more information.
        <BLANKLINE>

    Args:
        name: The full name of the person including the surname required to use this structure.
        surname: The part of the name representing the surname or the last name of the person required to use
            this structure.  If no surname is known enter a space as ' '.
        type: A tag from the [NameType enumeration set](https://gedcom.io/terms/v7/enumset-NAME-TYPE)
            entered by placing `Tag.` in front of the capitalized name of the tag.
        phrase: A phrase describing the name entered through `Phrase`.
        pieces: Personal name pieces entered through `PersonalNamePieces`.
        translations: Translations entered through `NameTranslation`.
        notes: Notes entered through `Note`.
        sources: Citations entered through `SourceCitation`.
        name_ext: Optional substructures extending [NAME tag](https://gedcom.io/terms/v7/NAME)
            entered through `Extension`.
        type_ext: Optional substructures extending [TYPE tag](https://gedcom.io/terms/v7/TYPE)
            entered through `Extension`.

    See Also:
        `Extension`
        `NameTranslation`
        `Note`
        `PersonalNamePieces`
        `SourceCitation`

    Reference:
        [GEDCOM NameType enumeration set](https://gedcom.io/terms/v7/enumset-NAME-TYPE)
        [GEDCOM NAME tag](https://gedcom.io/terms/v7/NAME)
        [GEDCOM TYPE tag](https://gedcom.io/terms/v7/TYPE)
        [GEDCOM Person Name Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PERSONAL_NAME_STRUCTURE)

    n NAME <PersonalName>                      {1:1}  g7:INDI-NAME
      +1 TYPE <Enum>                           {0:1}  g7:NAME-TYPE
         +2 PHRASE <Text>                      {0:1}  g7:PHRASE
      +1 <<PERSONAL_NAME_PIECES>>              {0:1}
      +1 TRAN <PersonalName>                   {0:M}  g7:NAME-TRAN
         +2 LANG <Language>                    {1:1}  g7:LANG
         +2 <<PERSONAL_NAME_PIECES>>           {0:1}
      +1 <<NOTE_STRUCTURE>>                    {0:M}
      +1 <<SOURCE_CITATION>>                   {0:M}
    """

    name: str = Default.EMPTY
    surname: str = Default.EMPTY
    type: Tag = Tag.NONE
    phrase: PhraseType = None
    pieces: PersonalNamePiecesType = None
    translations: NameTranType = None
    notes: NoteType = None
    source_citations: SourCiteType = None
    name_ext: ExtType = None
    type_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.name, str, no_list=True)
            and Checker.verify_not_empty(self.name)
            and Checker.verify_type(self.surname, str, no_list=True)
            and Checker.verify_not_empty(self.surname)
            and Checker.verify_enum(self.type, NameType)
            and Checker.verify_type(self.phrase, Phrase, no_list=True)
            and Checker.verify_type(
                self.pieces, PersonalNamePieces, no_list=True
            )
            and Checker.verify_type(self.translations, NameTranslation)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_type(self.source_citations, SourceCitation)
            and Checker.verify_ext(Tag.NAME, self.name_ext)
            and Checker.verify_ext(Tag.TYPE, self.type_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            name_surname: str = ''.join(
                [
                    Default.SLASH,
                    self.surname,
                    Default.SLASH,
                ]
            )
            new_name: str = self.name.replace(self.surname, name_surname)
            if self.surname not in self.name:
                new_name = ''.join([self.name, Default.SPACE, name_surname])
            lines = Tagger.string(lines, level, Tag.NAME, new_name)
            lines = Tagger.structure(lines, level + 1, self.name_ext)
            lines = Tagger.string(lines, level + 1, Tag.TYPE, self.type.value)
            lines = Tagger.structure(lines, level + 2, self.type_ext)
            lines = Tagger.structure(lines, level + 2, self.phrase)
            lines = Tagger.structure(lines, level + 1, self.pieces)
            lines = Tagger.structure(lines, level + 1, self.translations)
            lines = Tagger.structure(lines, level + 1, self.notes)
            lines = Tagger.structure(lines, level + 1, self.source_citations)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'PersonalName',
                ('    name = ', self.name, tabs, full, True),
                ('    surname = ', self.surname, tabs, full, True),
                ('    type = ', self.type, tabs, full, False),
                ('    phrase = ', self.phrase, tabs + 1, full, False),
                ('    pieces = ', self.pieces, tabs + 1, full, False),
                (
                    '    translations = ',
                    self.translations,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    notes = ', self.notes, tabs + 1, full, False),
                (
                    '    source_citations = ',
                    self.source_citations,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    name_ext = ', self.name_ext, tabs, full, False),
                ('    type_ext = ', self.type_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


PersonalNameType = PersonalName | list[PersonalName] | None


class Association(NamedTuple):
    """Store, validate and display a GEDCOM Association structure.

    Examples:
        This example comes from the [GEDCOM specification for the ASSO tag](https://gedcom.io/terms/v7/ASSO).
        The specification displays the GEDCOM lines as follows:

        > 0 @I1@ INDI
        > 1 ASSO @VOID@
        > 2 PHRASE Mr Stockdale
        > 2 ROLE OTHER
        > 3 PHRASE Teacher
        > 1 BAPM
        > 2 DATE 1930
        > 2 ASSO @I2@
        > 3 ROLE CLERGY

        This differs from the outcome produced by `ChronoData` which displays the `BAPM`
        baptismal event association with pointer `@I2@` before the individual association
        with pointer `@VOID@` because
        the event association preceded the individual association in the argument list.
        Both orderings record the same data under the individual with pointer `@I1@`.

        First import the required classes.
        >>> from genedata.build import Genealogy
        >>> from genedata.gedcom import Tag
        >>> from genedata.store import Association, Individual, Phrase

        Next, create a genealogy and the two individuals references.
        There is no need to create an individual reference for Mr Stockdale
        so we leave his pointer as `@VOID@`.
        >>> gen = Genealogy('test')
        >>> individual = gen.individual_xref('I', initial=True)
        >>> clergy = gen.individual_xref('I', initial=True)

        Finally construct the individual record and display it.
        >>> indi = Individual(
        ...     xref=individual,
        ...     associations=[
        ...         Association(
        ...             association_phrase=Phrase('Mr Stockdale'),
        ...             role=Tag.OTHER,
        ...             role_phrase=Phrase('Teacher'),
        ...         ),
        ...     ],
        ...     events=[
        ...         IndividualEvent(
        ...             tag=Tag.BAPM,
        ...             payload='',
        ...             event_detail=IndividualEventDetail(
        ...                 event_detail=EventDetail(
        ...                     date=Date(year=1930),
        ...                     associations=[
        ...                         Association(
        ...                             individual_xref=clergy, role=Tag.CLERGY
        ...                         ),
        ...                     ],
        ...                 )
        ...             ),
        ...         )
        ...     ],
        ... )
        >>> print(indi.ged())
        0 @I1@ INDI
        1 BAPM
        2 DATE 1930
        2 ASSO @I2@
        3 ROLE CLERGY
        1 ASSO @VOID@
        2 PHRASE Mr Stockdale
        2 ROLE OTHER
        3 PHRASE Teacher
        <BLANKLINE>

        The [GEDCOM Role tag specification](https://gedcom.io/terms/v7/ROLE)
        provides two examples for the use of Tag.ROLE.

        In the first example the child's birth record is the source of the mother's name
        which is only known as "Mary" without a surname.

        > 0 @I1@ INDI
        > 1 NAME Mary //
        > 2 SOUR @S1@
        > 3 EVEN BIRT
        > 4 ROLE MOTH

        To reproduce this we need and individual cross-reference identifier `@I1@` for Mary
        and a source cross-reference identifier `@S1@` for the birth certificate.
        Since we already have an individual referenced as `I1` above, we instantiate
        another Genealogy which illustrates that we can have multiple Genealogies
        instantiated at one time.
        >>> from genedata.build import Genealogy
        >>> from genedata.gedcom import Tag
        >>> from genedata.store import (
        ...     Individual,
        ...     PersonalName,
        ...     SourceCitation,
        ... )
        >>> gen2 = Genealogy('second genealogy')
        >>> ind_i1_xref = gen2.individual_xref('I1')
        >>> sour_s1_xref = gen2.source_xref('S1')
        >>> mary = Individual(
        ...     xref=ind_i1_xref,
        ...     personal_names=[
        ...         PersonalName(
        ...             name='Mary //',
        ...             source_citations=[
        ...                 SourceCitation(
        ...                     source_xref=sour_s1_xref,
        ...                     event=Tag.BIRT,
        ...                     role=Tag.MOTH,
        ...                 )
        ...             ],
        ...         ),
        ...     ],
        ... )
        >>> print(mary.ged())
        0 @I1@ INDI
        1 NAME Mary //
        2 SOUR @S1@
        3 EVEN BIRT
        4 ROLE MOTH
        <BLANKLINE>

        The second example describes when a friend who is the witness at a baptism.

        > 0 @I2@ INDI
        > 1 ASSO @I3@
        > 2 ROLE FRIEND
        > 3 PHRASE best friend
        > 1 BAPM
        > 2 ASSO @I3@
        > 3 ROLE WITN

        Then we will create two individuals in the gen3 Genealogy
        with cross-reference identifiers `@I2@` and `@I3@`.
        >>> from genedata.build import Genealogy
        >>> from genedata.gedcom import Tag
        >>> from genedata.store import (
        ...     Association,
        ...     Individual,
        ...     IndividualEvent,
        ... )
        >>> indi_i2_xref = gen2.individual_xref('I2')
        >>> indi_i3_xref = gen2.individual_xref('I3')
        >>> indi_i2 = Individual(
        ...     xref=indi_i2_xref,
        ...     associations=[
        ...         Association(
        ...             individual_xref=indi_i3_xref,
        ...             role=Tag.FRIEND,
        ...             role_phrase=Phrase('best friend'),
        ...         ),
        ...     ],
        ...     events=[
        ...         IndividualEvent(
        ...             tag=Tag.BAPM,
        ...             event_detail=IndividualEventDetail(
        ...                 event_detail=EventDetail(
        ...                     associations=[
        ...                         Association(
        ...                             individual_xref=indi_i3_xref,
        ...                             role=Tag.WITN,
        ...                         ),
        ...                     ]
        ...                 )
        ...             ),
        ...         )
        ...     ],
        ... )
        >>> print(indi_i2.ged(0))
        0 @I2@ INDI
        1 BAPM
        2 ASSO @I3@
        3 ROLE WITN
        1 ASSO @I3@
        2 ROLE FRIEND
        3 PHRASE best friend
        <BLANKLINE>

    Args:
        individual_xref: The individual cross-reference identified constructed through `genedata.build.individual_xref`.
        association_phrase: A phrase describing the association entered through `Phrase`.
        role: A tag from the [Role enumeration set](https://gedcom.io/terms/v7/enumset-ROLE).
        role_phrase: A phrase describing the role entered through `Phrase`.
        notes: Notes entered through `Note`.
        citations: Citations entered through `SourceCitation`.
        asso_ext: Optional substructures extending [ASSO tag](https://gedcom.io/terms/v7/ASSO)
            entered through `Extension`.
        role_ext: Optional substructures extending [ROLE tag](https://gedcom.io/terms/v7/ROLE)
            entered through `Extension`.

    See Also:
        `Extension`
        `genedata.build.individual_xref`
        `Phrase`

    Reference:
        [GEDCOM ASSO tag](https://gedcom.io/terms/v7/ASSO)
        [GEDCOM ROLE tag](https://gedcom.io/terms/v7/ROLE)
        [GEDCOM Role enumeration set](https://gedcom.io/terms/v7/enumset-ROLE)
        [GEDCOM Association Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#ASSOCIATION_STRUCTURE)

    n ASSO @<XREF:INDI>@                       {1:1}  [g7:ASSO](https://gedcom.io/terms/v7/ASSO)
      +1 PHRASE <Text>                         {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
      +1 ROLE <Enum>                           {1:1}  [g7:ROLE](https://gedcom.io/terms/v7/ROLE)
         +2 PHRASE <Text>                      {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
      +1 <<NOTE_STRUCTURE>>                    {0:M}
      +1 <<SOURCE_CITATION>>                   {0:M}
    """

    individual_xref: IndividualXref = Void.INDI
    association_phrase: PhraseType = None
    role: Tag = Tag.NONE
    role_phrase: PhraseType = None
    notes: NoteType = None
    citations: SourCiteType = None
    asso_ext: ExtType = None
    role_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(
                self.individual_xref, IndividualXref, no_list=True
            )
            and Checker.verify_not_empty(self.individual_xref)
            and Checker.verify_type(
                self.association_phrase, Phrase, no_list=True
            )
            and Checker.verify_enum(self.role, Role)
            and Checker.verify_not_empty(self.role)
            and Checker.verify_type(self.role_phrase, Phrase, no_list=True)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_type(self.citations, SourceCitation)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = Default.EMPTY
        if self.validate():
            lines = Tagger.string(
                lines, level, Tag.ASSO, str(self.individual_xref), format=False
            )
            lines = Tagger.structure(lines, level + 1, self.asso_ext)
            lines = Tagger.structure(lines, level + 1, self.association_phrase)
            lines = Tagger.string(lines, level + 1, Tag.ROLE, self.role.value)
            lines = Tagger.structure(lines, level + 2, self.role_ext)
            lines = Tagger.structure(lines, level + 2, self.role_phrase)
            lines = Tagger.structure(lines, level + 1, self.notes)
            lines = Tagger.structure(lines, level + 1, self.citations)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'Association',
                (
                    '    individual_xref = ',
                    self.individual_xref,
                    tabs,
                    full,
                    True,
                ),
                (
                    '    association_phrase = ',
                    self.association_phrase,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    role = ', self.role, tabs, full, True),
                ('    role_phrase = ', self.role_phrase, tabs + 1, full, False),
                ('    notes = ', self.notes, tabs + 2, full, False),
                ('    citations = ', self.citations, tabs + 1, full, False),
                ('    asso_ext = ', self.asso_ext, tabs, full, False),
                ('    role_ext = ', self.role_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


AssoType = Association | None


class MultimediaLink(NamedTuple):
    """_summary_

    Examples:


    Args:
        multimedia_xref: A multimedia cross-reference identifier constructed using `genedata.build.multimedia_xref`
        top: int = Default.TOP
        left: int = Default.LEFT
        height: int = Default.HEIGHT
        width: int = Default.WIDTH
        title: str = Default.EMPTY
        obje_ext: Optional substructures extending [OBJE tag](https://gedcom.io/terms/v7/OBJE)
            entered through `Extension`.
        top_ext: Optional substructures extending [TOP tag](https://gedcom.io/terms/v7/TOP)
            entered through `Extension`.
        left_ext: Optional substructures extending [LEFT tag](https://gedcom.io/terms/v7/LEFT)
            entered through `Extension`.
        height_ext: Optional substructures extending [HEIGHT tag](https://gedcom.io/terms/v7/HEIGHT)
            entered through `Extension`.
        width_ext: Optional substructures extending [WIDTH tag](https://gedcom.io/terms/v7/WIDTH)
            entered through `Extension`.
        titl_ext: Optional substructures extending [TITL tag](https://gedcom.io/terms/v7/TITL)
            entered through `Extension`.


    See Also:
        `Extension`
        `genedata.build.multimedia_xref`

    References:
        [GEDCOM HEIGHT tag](https://gedcom.io/terms/v7/HEIGHT)
        [GEDCOM LEFT tag](https://gedcom.io/terms/v7/LEFT)
        [GEDCOM OBJE tag](https://gedcom.io/terms/v7/OBJE)
        [GEDCOM TITL tag](https://gedcom.io/terms/v7/TITL)
        [GEDCOM TOP tag](https://gedcom.io/terms/v7/TOP)
        [GEDCOM WIDTH tag](https://gedcom.io/terms/v7/WIDTH)

    n OBJE @<XREF:OBJE>@                       {1:1}  [g7:OBJE](https://gedcom.io/terms/v7/OBJE)
      +1 CROP                                  {0:1}  [g7:CROP](https://gedcom.io/terms/v7/CROP)
         +2 TOP <Integer>                      {0:1}  [g7:TOP](https://gedcom.io/terms/v7/TOP)
         +2 LEFT <Integer>                     {0:1}  [g7:LEFT](https://gedcom.io/terms/v7/LEFT)
         +2 HEIGHT <Integer>                   {0:1}  [g7:HEIGHT](https://gedcom.io/terms/v7/HEIGHT)
         +2 WIDTH <Integer>                    {0:1}  [g7:WIDTH](https://gedcom.io/terms/v7/WIDTH)
      +1 TITL <Text>                           {0:1}  [g7:TITL](https://gedcom.io/terms/v7/TITL)
    """

    multimedia_xref: MultimediaXref = Void.OBJE
    top: int = Default.TOP
    left: int = Default.LEFT
    height: int = Default.HEIGHT
    width: int = Default.WIDTH
    title: str = Default.EMPTY
    obje_ext: ExtType = None
    top_ext: ExtType = None
    left_ext: ExtType = None
    height_ext: ExtType = None
    width_ext: ExtType = None
    titl_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(
                self.multimedia_xref, MultimediaXref, no_list=True
            )
            and Checker.verify_not_empty(self.multimedia_xref)
            and Checker.verify_type(self.top, int, no_list=True)
            and Checker.verify_type(self.left, int, no_list=True)
            and Checker.verify_type(self.height, int, no_list=True)
            and Checker.verify_type(self.width, int, no_list=True)
            and Checker.verify_type(self.title, str, no_list=True)
            and Checker.verify_ext(Tag.OBJE, self.obje_ext)
            and Checker.verify_ext(Tag.TOP, self.top_ext)
            and Checker.verify_ext(Tag.LEFT, self.left_ext)
            and Checker.verify_ext(Tag.HEIGHT, self.height_ext)
            and Checker.verify_ext(Tag.WIDTH, self.width_ext)
            and Checker.verify_ext(Tag.TITL, self.titl_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        lines: str = Default.EMPTY
        if self.validate():
            # display only if there is an image file under the multimedia xref
            # need to find out how to identify this and the pixels in that file
            lines = Tagger.string(
                lines,
                level,
                Tag.OBJE,
                self.multimedia_xref.fullname,
                format=False,
            )
            lines = Tagger.structure(lines, level + 1, self.obje_ext)
            lines = Tagger.empty(lines, level + 1, Tag.CROP)
            lines = Tagger.structure(lines, level + 2, self.top_ext)
            lines = Tagger.string(lines, level + 2, Tag.TOP, str(self.top))
            lines = Tagger.structure(lines, level + 3, self.top_ext)
            lines = Tagger.string(lines, level + 2, Tag.LEFT, str(self.left))
            lines = Tagger.structure(lines, level + 3, self.left_ext)
            lines = Tagger.string(
                lines, level + 2, Tag.HEIGHT, str(self.height)
            )
            lines = Tagger.structure(lines, level + 3, self.height_ext)
            lines = Tagger.string(lines, level + 2, Tag.WIDTH, str(self.width))
            lines = Tagger.structure(lines, level + 3, self.width_ext)
            lines = Tagger.string(lines, level + 1, Tag.TITL, self.title)
            lines = Tagger.structure(lines, level + 2, self.titl_ext)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'MultimediaLink',
                (
                    '    multimedia_xref = ',
                    self.multimedia_xref,
                    tabs,
                    full,
                    True,
                ),
                ('    top = ', self.top, tabs, full, False),
                ('    left = ', self.left, tabs, full, False),
                ('    height = ', self.height, tabs, full, False),
                ('    width = ', self.width, tabs, full, False),
                ('    title = ', self.title, tabs, full, False),
                ('    obje_ext = ', self.obje_ext, tabs, full, False),
                ('    top_ext = ', self.top_ext, tabs, full, False),
                ('    left_ext = ', self.left_ext, tabs, full, False),
                ('    height_ext = ', self.height_ext, tabs, full, False),
                ('    width_ext = ', self.width_ext, tabs, full, False),
                ('    titl_ext = ', self.titl_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


MMLinkType = MultimediaLink | list[MultimediaLink] | None


class Map(NamedTuple):
    """Store, validate and save a GEDCOM map structure.

    The latitude and longitude values are formatted to six decimal places
    by adding zeros if necessary or truncating the number of decimals on the
    input.

    The [GEDCOM Map Structure Type](https://gedcom.io/terms/v7/MAP) reads the following
    about the accuracy of this information:

    > Note that `MAP` provides neither a notion of accuracy (for example, the `MAP`
    > for a birth event may be some distance from the point where the birth occurred)
    > nor a notion of region size (for example, the `MAP` for a place "Belarus" may
    > be anywhere within that nation's 200,000 square kilometer area).

    Examples:
    The first example is a basic example using arbitrary latitude and longitude values.
    >>> from genedata.store import Map
    >>> location = Map(49.297222, -14.470833)
    >>> print(location.ged(1))
    1 MAP
    2 LATI N49.297222
    2 LONG W14.470833
    <BLANKLINE>

    The second example illustrates how to enter the data if we have the angle in
    minutes, degrees or seconds.  Using the same data from the example above,
    we can first convert it into degrees, minutes and seconds to set up the situation
    where the records we are given do not come in a decimal format.
    >>> from genedata.store import Placer
    >>> Placer.to_dms(49.297222)
    (49, 17, 49.9992)

    >>> Placer.to_dms(-14.470833)
    (-15, 31, 45.0012)

    We can use these values as well as the decimal values to load the Map structure.
    >>> latlon = Map(
    ...     Placer.to_decimal(49, 17, 49.9992),
    ...     Placer.to_decimal(-15, 31, 45.0012),
    ... )
    >>> print(latlon.ged(1))
    1 MAP
    2 LATI N49.297222
    2 LONG W14.470833
    <BLANKLINE>

    Args:
        latitude: The positive decimal value of the angle from the equator.
        longitude: The positive decimal value of the angle from the prime meridian.
        map_ext: Optional substructures extending [MAP tag](https://gedcom.io/terms/v7/MAP)
            entered through `Extension`.
        lati_ext: Optional substructures extending [LATI tag](https://gedcom.io/terms/v7/LATI)
            entered through `Extension`.
        long_ext: Optional substructures extending [LONG tag](https://gedcom.io/terms/v7/LONG)
            entered through `Extension`.

    Reference:
        [GEDCOM LATI tag](https://gedcom.io/terms/v7/LATI)
        [GEDCOM LONG tag](https://gedcom.io/terms/v7/LONG)
        [GEDCOM MAP tag](https://gedcom.io/terms/v7/MAP)
        [GEDCOM Map Structure Type](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#MAP)
        [GEDCOM Latitude Structure Type](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#LATI)
        [GEDCOM Longitude Structure Type](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#LONG)
    """

    latitude: float = Default.MAP_LATITUDE
    longitude: float = Default.MAP_LONGITUDE
    map_ext: ExtType = None
    lati_ext: ExtType = None
    long_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.latitude, float, no_list=True)
            and Checker.verify_type(self.longitude, float, no_list=True)
            and Checker.verify_range(self.latitude, -90.0, 90.0)
            and Checker.verify_range(self.longitude, -180.0, 180.0)
            and Checker.verify_ext(Tag.MAP, self.map_ext)
            and Checker.verify_ext(Tag.LATI, self.lati_ext)
            and Checker.verify_ext(Tag.LONG, self.long_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        north_south: str = 'N'
        if self.latitude < 0.0:
            north_south = 'S'
        east_west: str = 'E'
        if self.longitude < 0.0:
            east_west = 'W'
        latitude: str = format(abs(self.latitude), '.6f')
        longitude: str = format(abs(self.longitude), '.6f')
        latitude = ''.join([north_south, latitude])
        longitude = ''.join([east_west, longitude])
        if self.validate():
            lines = Tagger.empty(lines, level, Tag.MAP)
            lines = Tagger.structure(lines, level + 1, self.map_ext)
            lines = Tagger.string(lines, level + 1, Tag.LATI, latitude)
            lines = Tagger.structure(lines, level + 2, self.lati_ext)
            lines = Tagger.string(lines, level + 1, Tag.LONG, longitude)
            lines = Tagger.structure(lines, level + 2, self.long_ext)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'Map',
                ('    latitude = ', self.latitude, tabs, full, True),
                ('    longitude = ', self.longitude, tabs, full, True),
                ('    map_ext = ', self.map_ext, tabs, full, False),
                ('    lati_ext = ', self.lati_ext, tabs, full, False),
                ('    long_ext = ', self.long_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


MapType = Map | None


class PlaceTranslation(NamedTuple):
    """Store, validate and return a translation of GEDCOM place names.

    A place is a comma separated string of named locations or regions going from smallest to largest.

    The BCP 47 language tag is a hyphenated list of subtags.
    The [W3C Internationalization](https://www.w3.org/International/questions/qa-choosing-language-tags)
    guide will help one make a decision on which tags to use.
    The [Language Subtag Lookup Tool](https://r12a.github.io/app-subtags/)
    can assist with finding and checking the language tag one would like to use.

    Example:


    Args:
        place1: A part of the place corresponding to the lowest region.
        place2: A part of the place corresponding to the next highest region above `place1`.
        place3: A part of the place corresponding to the next highest region above `place2`.
        place4: A part of the place corresponding to the next highest region above `place3`.
        language: The language used to report the four places values entered through `Lang`.
        tran_ext: Optional substructures extending [TRAN tag](https://gedcom.io/terms/v7/TRAN)
            entered through `Extension`.

    See Also:
        `Extension`
        `Lang`

    Reference:
        [GEDCOM TRAN tag](https://gedcom.io/terms/v7/TRAN)
        [GEDCOM Place Form](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PLAC-FORM)
        [GEDCOM Place Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PLACE_STRUCTURE)


    >   +1 TRAN <List:Text>                      {0:M}  [g7:PLAC-TRAN](https://gedcom.io/terms/v7/PLAC-TRAN)
    >      +2 LANG <Language>                    {1:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
    """

    place1: str = Default.EMPTY
    place2: str = Default.EMPTY
    place3: str = Default.EMPTY
    place4: str = Default.EMPTY
    language: LangType = None
    tran_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.place1, str, no_list=True)
            and Checker.verify_type(self.place2, str, no_list=True)
            and Checker.verify_type(self.place3, str, no_list=True)
            and Checker.verify_type(self.place4, str, no_list=True)
            and Checker.verify_not_empty(
                ''.join([self.place1, self.place2, self.place3, self.place4])
            )
            and Checker.verify_type(self.language, Lang, no_list=True)
            and Checker.verify_not_empty(self.language)
            and Checker.verify_ext(Tag.PLAC, self.tran_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = Default.EMPTY
        if self.validate():
            lines = Tagger.string(
                lines,
                level,
                Tag.TRAN,
                Placer.place(
                    self.place1, self.place2, self.place3, self.place4
                ),
            )
            lines = Tagger.structure(lines, level + 1, self.tran_ext)
            lines = Tagger.structure(lines, level + 1, self.language)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'PlaceTranslation',
                ('    place1 = ', self.place1, tabs, full, False),
                ('    place2 = ', self.place2, tabs, full, False),
                ('    place3 = ', self.place3, tabs, full, False),
                ('    place4 = ', self.place4, tabs, full, False),
                ('    language = ', self.language, tabs + 1, full, False),
                ('    tran_ext = ', self.tran_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


PlacTranType = PlaceTranslation | list[PlaceTranslation] | None


class Place(NamedTuple):
    """Store, validate and return a GEDCOM place structure.

    A place is a comma separated string of named locations or regions going from smallest to largest.
    The default is an empty dictionary {'City': '', 'County': '', 'State': '', 'Country': ''}.
    One would fill in the values for city, county, state and country or assign other
    regions with their names if the default is not relevant.

    The BCP 47 language tag is a hyphenated list of subtags.
    The [W3C Internationalization](https://www.w3.org/International/questions/qa-choosing-language-tags)
    guide will help one make a decision on which tags to use.
    The [Language Subtag Lookup Tool](https://r12a.github.io/app-subtags/)
    can assist with finding and checking the language tag one would like to use.

    Example:
        Below are two `PlaceName` tuples for a place.
        The first is in Czech and the second English.
        A `Map` tuple provides latitude and longitude values for the place.
        A couple of simple `Note` tuples are added as well.
        These tuples form the structure of a `Place` tuple.

        Normally one would not call `validate` or `ged` unless one wanted
        to see if the substructure is valid or how it would display
        in the final GEDCOM file.
        >>> from genedata.store import Lang, Map, Place
        >>> place = Place(
        ...     place1='Bechyně',
        ...     place2='okres Tábor',
        ...     place3='Jihočeský kraj',
        ...     place4='Česká republika',
        ...     form1='Město',
        ...     form2='Okres',
        ...     form3='Stát',
        ...     form4='Země',
        ...     language=Lang('cs'),
        ...     map=Map(49.297222, 14.470833),
        ...     translations=[
        ...         PlaceTranslation(
        ...             place1='Bechyně',
        ...             place2='Tábor District',
        ...             place3='South Bohemian Region',
        ...             place4='Czech Republic',
        ...             language=Lang('en'),
        ...         )
        ...     ],
        ...     notes=[
        ...         Note(
        ...             note='A place in the Czech Republic.',
        ...             language=Lang('en'),
        ...         ),
        ...         Note(note='Místo v České republice.', language=Lang('cs')),
        ...     ],
        ... )
        >>> place.validate()
        True
        >>> print(place.ged(2))
        2 PLAC Bechyně, okres Tábor, Jihočeský kraj, Česká republika
        3 FORM Město, Okres, Stát, Země
        3 LANG cs
        3 TRAN Bechyně, Tábor District, South Bohemian Region, Czech Republic
        4 LANG en
        3 MAP
        4 LATI N49.297222
        4 LONG E14.470833
        3 NOTE A place in the Czech Republic.
        4 LANG en
        3 NOTE Místo v České republice.
        4 LANG cs
        <BLANKLINE>

    Args:
        place1: A part of the place corresponding to the lowest region.
        place2: A part of the place corresponding to the next highest region above `place1`.
        place3: A part of the place corresponding to the next highest region above `place2`.
        place4: A part of the place corresponding to the next highest region above `place3`.
        form1: The name of the region identified by `place1`.
        form2: The name of the region identified by `place2`.
        form3: The name of the region identified by `place3`.
        form4: The name of the region identified by `place4`.
        language: The langue used to report the four places values entered through `Lang`.
        translation: Place translations entered though `PlaceTranslation`.
        maps: Maps entered through `Map`.
        exid: Identifiers associated with the place entered through `Identifier`.
        notes: Notes entered through `Note`.
        plac_ext: Optional substructures extending [PLAC tag](https://gedcom.io/terms/v7/PLAC)
            entered through `Extension`.
        form_ext: Optional substructures extending [FORM tag](https://gedcom.io/terms/v7/FORM)
            entered through `Extension`.

    See Also:
        `Extension`
        `Identifier`
        `Lang`
        `Map`
        `Note`
        `PlaceTranslation`


    Reference:
        [GEDCOM FORM tag](https://gedcom.io/terms/v7/FORM)
        [GEDCOM PLAC tag](https://gedcom.io/terms/v7/PLAC)
        [GEDCOM Place Form](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PLAC-FORM)
        [GEDCOM Place Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PLACE_STRUCTURE)


    > n PLAC <List:Text>                         {1:1}  [g7:PLAC](https://gedcom.io/terms/v7/PLAC)
    >   +1 FORM <List:Text>                      {0:1}  [g7:PLAC-FORM](https://gedcom.io/terms/v7/PLAC-FORM)
    >   +1 LANG <Language>                       {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
    >   +1 TRAN <List:Text>                      {0:M}  [g7:PLAC-TRAN](https://gedcom.io/terms/v7/PLAC-TRAN)
    >      +2 LANG <Language>                    {1:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
    >   +1 MAP                                   {0:1}  [g7:MAP](https://gedcom.io/terms/v7/MAP)
    >      +2 LATI <Special>                     {1:1}  [g7:LATI](https://gedcom.io/terms/v7/LATI)
    >      +2 LONG <Special>                     {1:1}  [g7:LONG](https://gedcom.io/terms/v7/LONG)
    >   +1 EXID <Special>                        {0:M}  [g7:EXID](https://gedcom.io/terms/v7/EXID)
    >      +2 TYPE <Special>                     {0:1}  [g7:EXID-TYPE](https://gedcom.io/terms/v7/EXID-TYPE)
    >   +1 <<NOTE_STRUCTURE>>                    {0:M}
    """

    place1: str = Default.EMPTY
    place2: str = Default.EMPTY
    place3: str = Default.EMPTY
    place4: str = Default.EMPTY
    form1: str = Default.PLACE_FORM1
    form2: str = Default.PLACE_FORM2
    form3: str = Default.PLACE_FORM3
    form4: str = Default.PLACE_FORM4
    language: LangType = None
    translations: PlacTranType = None
    map: MapType = None
    exids: IdenType = None
    notes: NoteType = None
    plac_ext: ExtType = None
    form_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.place1, str, no_list=True)
            and Checker.verify_type(self.place2, str, no_list=True)
            and Checker.verify_type(self.place3, str, no_list=True)
            and Checker.verify_type(self.place4, str, no_list=True)
            and Checker.verify_not_empty(
                ''.join([self.place1, self.place2, self.place3, self.place4])
            )
            and Checker.verify_type(self.form1, str, no_list=True)
            and Checker.verify_type(self.form2, str, no_list=True)
            and Checker.verify_type(self.form3, str, no_list=True)
            and Checker.verify_type(self.form4, str, no_list=True)
            and Checker.verify_type(self.language, Lang, no_list=True)
            and Checker.verify_type(self.translations, PlaceTranslation)
            and Checker.verify_type(self.map, Map, no_list=True)
            and Checker.verify_type(self.exids, Identifier)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_ext(Tag.PLAC, self.plac_ext)
            and Checker.verify_ext(Tag.FORM, self.form_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = Default.EMPTY
        if self.validate():
            lines = Tagger.string(
                lines,
                level,
                Tag.PLAC,
                Placer.place(
                    self.place1, self.place2, self.place3, self.place4
                ),
            )
            lines = Tagger.structure(lines, level + 1, self.plac_ext)
            lines = Tagger.string(
                lines,
                level + 1,
                Tag.FORM,
                Placer.form(self.form1, self.form2, self.form3, self.form4),
            )
            lines = Tagger.structure(lines, level + 1, self.form_ext)
            lines = Tagger.structure(lines, level + 1, self.language)
            lines = Tagger.structure(lines, level + 1, self.translations)
            lines = Tagger.structure(lines, level + 1, self.map)
            lines = Tagger.structure(lines, level + 1, self.exids)
            lines = Tagger.structure(lines, level + 1, self.notes)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'Place',
                ('    place1 = ', self.place1, tabs, full, False),
                ('    place2 = ', self.place2, tabs, full, False),
                ('    place3 = ', self.place3, tabs, full, False),
                ('    place4 = ', self.place4, tabs, full, False),
                ('    form1 = ', self.form1, tabs, full, False),
                ('    form2 = ', self.form2, tabs, full, False),
                ('    form3 = ', self.form3, tabs, full, False),
                ('    form4 = ', self.form4, tabs, full, False),
                ('    language = ', self.language, tabs + 1, full, False),
                (
                    '    translations = ',
                    self.translations,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    map = ', self.map, tabs + 1, full, False),
                ('    exids = ', self.exids, tabs + 1, full, False),
                ('    notes = ', self.notes, tabs + 1, full, False),
                ('    plac_ext = ', self.plac_ext, tabs, full, False),
                ('    form_ext = ', self.form_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


PlacType = Place | None


class EventDetail(NamedTuple):
    """Store, validate and display a GEDCOM Event Detail.

    Examples:

    Args:
        date: The date entered through `Date`.
        time: The time entered thorugh `Time`.`
        phrase: A phrase entered through `Phrase`.
        place: A place entered through `Place`.
        address: An addressed entered through `Address`.
        phones: Phones entered through `Phone`.
        emails: Emails entered through `Email`.
        faxes: Faxes entered through `Fax`.
        wwws: Internet addressed entered through `WWW`
        agency: The name of the agency associated with the event.
        religion: The name of a religion associated with the event.
        cause: The name of a cause associated with the event.
        resn: A tag from the [RESN enumeration set](https://gedcom.io/terms/v7/enumset-RESN)
            entered by placing `Tag.` in front of the capitalized name from the set.
        sdate: A sort date entered through `SDate`.
        stime: A sort time entered through `Time`.
        sphrase: A sort phrase entered through `Phrase`.
        associations: Associations entered through `Association`.
        notes: Notes entered through `Note`.
        sources: Citations entered through `SourceCitation`.
        multimedia_links: Multimedia links entered through `MultimediaLink`.
        uids: Identifiers entered through `Identifier`.
        agnc_ext: Optional substructures extending [AGNC tag](https://gedcom.io/terms/v7/AGNC)
            entered through `Extension`.
        reli_ext: Optional substructures extending [RELI tag](https://gedcom.io/terms/v7/RELI)
            entered through `Extension`.
        caus_ext: Optional substructures extending [CAUS tag](https://gedcom.io/terms/v7/CAUS)
            entered through `Extension`.

    See Also:
        `Address`
        `Association`
        `Date`
        `Email`
        `Extension`
        `Fax`
        `Identifier`
        `MutlimediaLink`
        `Note`
        `Phrase`
        `Phone`
        `Place`
        `SDate`
        `SourceCitation`
        `Time`
        `WWW`

    Reference:
        [GEDCOM RESN enumeration set](https://gedcom.io/terms/v7/enumset-RESN)
        [GEDCOM AGNC tag](https://gedcom.io/terms/v7/AGNC)
        [GEDCOM CAUS tag](https://gedcom.io/terms/v7/CAUS)
        [GEDCOM RELI tag](https://gedcom.io/terms/v7/RELI)
        [GEDCOM Resn enumeration set](https://gedcom.io/terms/v7/enumset-RESN)
        [GEDCOM Event Detail](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#EVENT_DETAIL)

    > n <<DATE_VALUE>>                           {0:1}
    > n <<PLACE_STRUCTURE>>                      {0:1}
    > n <<ADDRESS_STRUCTURE>>                    {0:1}
    > n PHON <Special>                           {0:M}  [g7:PHON](https://gedcom.io/terms/v7/PHON)
    > n EMAIL <Special>                          {0:M}  [g7:EMAIL](https://gedcom.io/terms/v7/EMAIL)
    > n FAX <Special>                            {0:M}  [g7:FAX](https://gedcom.io/terms/v7/FAX)
    > n WWW <Special>                            {0:M}  [g7:WWW](https://gedcom.io/terms/v7/WWW)
    > n AGNC <Text>                              {0:1}  [g7:AGNC](https://gedcom.io/terms/v7/AGNC)
    > n RELI <Text>                              {0:1}  [g7:RELI](https://gedcom.io/terms/v7/RELI)
    > n CAUS <Text>                              {0:1}  [g7:CAUS](https://gedcom.io/terms/v7/CAUS)
    > n RESN <List:Enum>                         {0:1}  [g7:RESN](https://gedcom.io/terms/v7/RESN)
    > n SDATE <DateValue>                        {0:1}  [g7:SDATE](https://gedcom.io/terms/v7/SDATE)
    >   +1 TIME <Time>                           {0:1}  [g7:TIME](https://gedcom.io/terms/v7/TIME)
    >   +1 PHRASE <Text>                         {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    > n <<ASSOCIATION_STRUCTURE>>                {0:M}
    > n <<NOTE_STRUCTURE>>                       {0:M}
    > n <<SOURCE_CITATION>>                      {0:M}
    > n <<MULTIMEDIA_LINK>>                      {0:M}
    > n UID <Special>                            {0:M}  [g7:UID]()
    """

    date: DateType = None
    time: TimeType = None
    phrase: PhraseType = None
    place: PlacType = None
    address: AddrType = None
    phones: PhoneType = None
    emails: EmailType = None
    faxes: FaxType = None
    wwws: WWWType = None
    agency: str = Default.EMPTY
    religion: str = Default.EMPTY
    cause: str = Default.EMPTY
    resn: Tag = Tag.NONE
    sdate: SDateType = None
    stime: TimeType = None
    sphrase: PhraseType = None
    associations: AssoType = None
    notes: NoteType = None
    sources: SourCiteType = None
    multimedia_links: MMLinkType = None
    uids: IdenType = None
    agnc_ext: ExtType = None
    reli_ext: ExtType = None
    caus_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.date, Date, no_list=True)
            and Checker.verify_type(self.time, Time, no_list=True)
            and Checker.verify_type(self.phrase, Phrase, no_list=True)
            and Checker.verify_type(self.place, Place, no_list=True)
            and Checker.verify_type(self.address, Address, no_list=True)
            and Checker.verify_type(self.phones, Phone)
            and Checker.verify_type(self.emails, Email)
            and Checker.verify_type(self.faxes, Fax)
            and Checker.verify_type(self.wwws, WWW)
            and Checker.verify_type(self.agency, str, no_list=True)
            and Checker.verify_type(self.religion, str, no_list=True)
            and Checker.verify_type(self.cause, str, no_list=True)
            and Checker.verify_enum(self.resn, Resn)
            and Checker.verify_type(self.sdate, SDate, no_list=True)
            and Checker.verify_type(self.stime, Time, no_list=True)
            and Checker.verify_type(self.sphrase, Phrase, no_list=True)
            and Checker.verify_type(self.associations, Association)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_type(self.sources, Source)
            and Checker.verify_type(self.multimedia_links, MultimediaLink)
            and Checker.verify_type(self.uids, Identifier)
            and Checker.verify_ext(Tag.AGNC, self.agnc_ext)
            and Checker.verify_ext(Tag.RELI, self.reli_ext)
            and Checker.verify_ext(Tag.CAUS, self.caus_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = Default.EMPTY
        if self.validate():
            lines = Tagger.structure(lines, level, self.date)
            lines = Tagger.structure(lines, level, self.time)
            lines = Tagger.structure(lines, level, self.phrase)
            lines = Tagger.structure(lines, level, self.place)
            lines = Tagger.structure(lines, level, self.address)
            lines = Tagger.structure(lines, level, self.phones)
            lines = Tagger.structure(lines, level, self.emails)
            lines = Tagger.structure(lines, level, self.faxes)
            lines = Tagger.structure(lines, level, self.wwws)
            lines = Tagger.string(lines, level, Tag.AGNC, self.agency)
            lines = Tagger.structure(lines, level + 1, self.agnc_ext)
            lines = Tagger.string(lines, level, Tag.RELI, self.religion)
            lines = Tagger.structure(lines, level + 1, self.reli_ext)
            lines = Tagger.string(lines, level, Tag.CAUS, self.cause)
            lines = Tagger.structure(lines, level + 1, self.caus_ext)
            lines = Tagger.string(lines, level, Tag.RESN, self.resn.value)
            lines = Tagger.structure(lines, level, self.sdate)
            lines = Tagger.structure(lines, level, self.stime)
            lines = Tagger.structure(lines, level, self.sphrase)
            lines = Tagger.structure(lines, level, self.associations)
            lines = Tagger.structure(lines, level, self.notes)
            lines = Tagger.structure(lines, level, self.sources)
            lines = Tagger.structure(lines, level, self.multimedia_links)
            lines = Tagger.structure(lines, level, self.uids)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'EventDetail',
                ('    date = ', self.date, tabs + 1, full, False),
                ('    time = ', self.time, tabs + 1, full, False),
                ('    phrase = ', self.phrase, tabs + 1, full, False),
                ('    place = ', self.place, tabs + 1, full, False),
                ('    address = ', self.address, tabs + 1, full, False),
                ('    phones = ', self.phones, tabs + 1, full, False),
                ('    emails = ', self.emails, tabs + 1, full, False),
                ('    faxes = ', self.faxes, tabs + 1, full, False),
                ('    wwws = ', self.wwws, tabs + 1, full, False),
                ('    agency = ', self.agency, tabs, full, False),
                ('    religion = ', self.religion, tabs, full, False),
                ('    cause = ', self.cause, tabs, full, False),
                ('    resn = ', self.resn, tabs, full, False),
                ('    sdate = ', self.sdate, tabs + 1, full, False),
                ('    stime = ', self.stime, tabs + 1, full, False),
                ('    sphrase = ', self.sphrase, tabs + 1, full, False),
                (
                    '    associations = ',
                    self.associations,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    notes = ', self.notes, tabs + 1, full, False),
                ('    sources = ', self.sources, tabs + 1, full, False),
                (
                    '    multimedia_links = ',
                    self.multimedia_links,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    uids = ', self.uids, tabs + 1, full, False),
                ('    agnc_ext = ', self.agnc_ext, tabs, full, False),
                ('    reli_ext = ', self.reli_ext, tabs, full, False),
                ('    caus_ext = ', self.caus_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


EvenDetailType = EventDetail | list[EventDetail] | None


class FamilyEventDetail(NamedTuple):
    """Store, validate and display GEDCOM family event detail structure.

    Examples:
        >>> from genedata.store import Phrase, FamilyEventDetail
        >>> family_detail = FamilyEventDetail(
        ...     husband_age=Age(25, phrase=Phrase('Happy')),
        ...     wife_age=Age(24, phrase=Phrase('Very happy')),
        ... )
        >>> print(family_detail.ged(1))
        1 HUSB
        2 AGE > 25y
        3 PHRASE Happy
        1 WIFE
        2 AGE > 24y
        3 PHRASE Very happy
        <BLANKLINE>

    Args:
        husband_age: The husband's age entered through `Age`.
        wife_age: The wife's age entered through `Age`.
        event_detail: The details of the event entered through `EventDetail`.
        husb_ext: Optional substructures extending [HUSB tag](https://gedcom.io/terms/v7/HUSB)
            entered through `Extension`.
        wife_ext: Optional substructures extending [WIFE tag](https://gedcom.io/terms/v7/WIFe)
            entered through `Extension`.

    See Also:
        `Age`
        `EventDetail`
        `Extension`

    References:
        [GEDCOM HUSB tag](https://gedcom.io/terms/v7/HUSB)
        [GEDCOM WIFE tag](https://gedcom.io/terms/v7/WIFe)
        [GEDCOM Family Event Detail](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_EVENT_DETAIL)

    > n HUSB                                     {0:1}  [g7:HUSB](https://gedcom.io/terms/v7/HUSB)
    >   +1 AGE <Age>                             {1:1}  [g7:AGE](https://gedcom.io/terms/v7/AGE)
    >      +2 PHRASE <Text>                      {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    > n WIFE                                     {0:1}  [g7:WIFE](https://gedcom.io/terms/v7/WIFE)
    >   +1 AGE <Age>                             {1:1}  [g7:AGE](https://gedcom.io/terms/v7/AGE)
    >      +2 PHRASE <Text>                      {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    > n <<EVENT_DETAIL>>                         {0:1}
    """

    husband_age: AgeType = None
    wife_age: AgeType = None
    event_detail: EvenDetailType = None
    husb_ext: ExtType = None
    wife_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.husband_age, Age, no_list=True)
            and Checker.verify_not_empty(self.husband_age)
            and Checker.verify_type(self.wife_age, Age, no_list=True)
            and Checker.verify_not_empty(self.wife_age)
            and Checker.verify_type(
                self.event_detail, EventDetail, no_list=True
            )
            and Checker.verify_ext(Tag.HUSB, self.husb_ext)
            and Checker.verify_ext(Tag.WIFE, self.wife_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = Default.EMPTY
        if self.validate():
            if self.husband_age != Age():
                lines = Tagger.empty(lines, level, Tag.HUSB)
                lines = Tagger.structure(lines, level + 1, self.husb_ext)
                lines = Tagger.structure(lines, level + 1, self.husband_age)
            if self.wife_age != Age():
                lines = Tagger.empty(lines, level, Tag.WIFE)
                lines = Tagger.structure(lines, level + 1, self.wife_ext)
                lines = Tagger.structure(lines, level + 1, self.wife_age)
            lines = Tagger.structure(lines, level, self.event_detail)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'FamilyEventDetail',
                ('    husband_age = ', self.husband_age, tabs + 1, full, True),
                ('    wife_age = ', self.wife_age, tabs + 1, full, True),
                (
                    '    event_detail = ',
                    self.event_detail,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    husb_ext = ', self.husb_ext, tabs, full, False),
                ('    wife_ext = ', self.wife_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


FamEvenDetailType = FamilyEventDetail | None


class FamilyAttribute(NamedTuple):
    """Store, validate and display a GEDCOM Family Attribute.

    Examples:


    Args:
        tag: A tag from the [Family Attribute enumeration set]()
            entered by placing `Tag.` in front of the capitalized name from the set.
        payload: A value to be displayed on the same line as the tag.
        attribute_type: The type of the attribute.
        family_event_detail: Family event detail entered through `FamilyEventDetail`.
        tag_ext: Optional substructures extending whichever tag was used and entered through `Extension`.


    See Also:
        `Extension`

    Reference:
        [GEDCOM Family Attribute](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_ATTRIBUTE_STRUCTURE)

    > [
    > n NCHI <Integer>                           {1:1}  [g7:FAM-NCHI](https://gedcom.io/terms/v7/FAM-NCHI)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > |
    > n RESI <Text>                              {1:1}  [g7:FAM-RESI](https://gedcom.io/terms/v7/FAM-RESI)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > |
    > n FACT <Text>                              {1:1}  [g7:FAM-FACT](https://gedcom.io/terms/v7/FAM-FACT)
    >   +1 TYPE <Text>                           {1:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > ]
    """

    tag: Tag = Tag.NONE
    payload: str = Default.EMPTY
    attribute_type: str = Default.EMPTY
    family_event_detail: FamEvenDetailType = None
    tag_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.tag, Tag)
            and Checker.verify_enum(self.tag, FamAttr)
            and Checker.verify_not_empty(self.tag)
            and Checker.verify(
                self.tag == Tag.FACT,
                self.attribute_type != Default.EMPTY,
                Msg.FACT_REQUIRES_TYPE,
            )
            and Checker.verify_type(self.payload, str, no_list=True)
            and Checker.verify_type(self.attribute_type, str, no_list=True)
            and Checker.verify_type(
                self.family_event_detail, FamilyEventDetail, no_list=True
            )
            and Checker.verify_ext(self.tag, self.tag_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.tag.value != Tag.NONE.value and self.validate():
            lines = Tagger.string(lines, level, self.tag, self.payload)
            lines = Tagger.structure(lines, level + 1, self.tag_ext)
            lines = Tagger.string(
                lines, level + 1, Tag.TYPE, self.attribute_type
            )
            lines = Tagger.structure(lines, level + 1, self.family_event_detail)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'FamilyAttribute',
                ('    tag = ', self.tag, tabs, full, True),
                ('    payload = ', self.payload, tabs, full, True),
                (
                    '    attribute_type = ',
                    self.attribute_type,
                    tabs,
                    full,
                    False,
                ),
                (
                    '    family_event_detail = ',
                    self.family_event_detail,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    tag_ext = ', self.tag_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


FamAttrType = FamilyAttribute | list[FamilyAttribute] | None


class FamilyEvent(NamedTuple):
    """Store, validate and display a GEDCOM Family Event.

    Examples:
        Only the following tags can be used in this structure:
        Tag.ANUL, Tag.CENS, Tag.DIV, Tag.DIVF, Tag.ENGA, Tag.MARB, Tag.MARC, Tag.MARL,
        Tag.MARR, Tag.MARS, Tag.EVEN.  This example shows the error that
        would result if a different tag is used once the NamedTuple is validated.
        First, set up the situation for the error to occur.
        >>> from genedata.gedcom import Tag
        >>> from genedata.store import FamilyEvent
        >>> event = FamilyEvent(Tag.DATE)

        Next, evaluate `event`.
        >>> event.validate()
        Traceback (most recent call last):
        ValueError: The tag DATE is not in the list of valid tags.

        The `validate` method also checks that the Tag.EVEN cannot have an empty payload.
        >>> event2 = FamilyEvent(Tag.EVEN)
        >>> event2.validate()
        Traceback (most recent call last):
        ValueError: The EVEN tag requires a non-empty TYPE.

    Args:
        tag: A tag from the [EVEN enumeration set](https://gedcom.io/terms/v7/enumset-EVEN).
        occurred: A rule value means the event occurred.  A false value that it did not.  This information
            is displayed on the line with the tag.
        event_type: The type of event.
        event_detail: Details of the event entered through `FamilyEventDetail`.
        tag_ext: Optional substructures extending whichever tag was used and entered through `Extension`.


    See Also:
        `Extension`
        `FamilyEventDetail`

    References:
        [GEDCOM EVEN enumeration set](https://gedcom.io/terms/v7/enumset-EVEN)
        [GEDCOM Family Event](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_EVENT_STRUCTURE)

    > [
    > n ANUL [Y|<NULL>]                          {1:1}  [g7:ANUL](https://gedcom.io/terms/v7/ANUL)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > |
    > n CENS [Y|<NULL>]                          {1:1}  [g7:FAM-CENS](https://gedcom.io/terms/v7/FAM-CENS)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > |
    > n DIV [Y|<NULL>]                           {1:1}  [g7:DIV](https://gedcom.io/terms/v7/DIV)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > |
    > n DIVF [Y|<NULL>]                          {1:1}  [g7:DIVF](https://gedcom.io/terms/v7/DIVF)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > |
    > n ENGA [Y|<NULL>]                          {1:1}  [g7:ENGA](https://gedcom.io/terms/v7/ENGA)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > |
    > n MARB [Y|<NULL>]                          {1:1}  [g7:MARB](https://gedcom.io/terms/v7/MARB)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > |
    > n MARC [Y|<NULL>]                          {1:1}  [g7:MARC](https://gedcom.io/terms/v7/MARC)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > |
    > n MARL [Y|<NULL>]                          {1:1}  [g7:MARL](https://gedcom.io/terms/v7/MARL)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > |
    > n MARR [Y|<NULL>]                          {1:1}  [g7:MARR](https://gedcom.io/terms/v7/MARR)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > |
    > n MARS [Y|<NULL>]                          {1:1}  [g7:MARS](https://gedcom.io/terms/v7/MARS)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > |
    > n EVEN <Text>                              {1:1}  [g7:FAM-EVEN](https://gedcom.io/terms/v7/FAM-EVEN)
    >   +1 TYPE <Text>                           {1:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<FAMILY_EVENT_DETAIL>>               {0:1}
    > ]
    """

    tag: Tag = Tag.NONE
    occurred: bool = True
    event_type: str = Default.EMPTY
    event_detail: FamEvenDetailType = None
    tag_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.tag, Tag, no_list=True)
            and Checker.verify_not_empty(self.tag)
            and Checker.verify_enum(self.tag, FamEven)
            and Checker.verify_type(self.event_type, str, no_list=True)
            and Checker.verify(
                self.tag == Tag.EVEN,
                self.event_type != Default.EMPTY,
                Msg.EVEN_REQUIRES_TYPE,
            )
            and Checker.verify_type(
                self.event_detail, FamilyEventDetail, no_list=True
            )
            and Checker.verify_ext(self.tag, self.tag_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            if not self.occurred:
                lines = Tagger.empty(lines, level, self.tag)
            else:
                lines = Tagger.string(lines, level, self.tag, Default.OCCURRED)
            lines = Tagger.structure(lines, level + 1, self.tag_ext)
            lines = Tagger.string(lines, level + 1, Tag.TYPE, self.event_type)
            lines = Tagger.structure(lines, level + 1, self.event_detail)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'FamilyEvent',
                ('    tag = ', self.tag, tabs + 1, full, True),
                ('    occurred = ', self.occurred, tabs, full, False),
                (
                    '    event_type = ',
                    self.event_type,
                    tabs,
                    full,
                    self.tag == Tag.EVEN,
                ),
                (
                    '    event_detail = ',
                    self.event_detail,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    tag_ext = ', self.tag_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


FamEvenType = FamilyEvent | list[FamilyEvent] | None


class Child(NamedTuple):
    """Store, validate and display GEDCOM child information.

    Examples:

    Args:
        individual_xref: An individual cross-reference identified constructed using `genedata.build.individual_xref`.
        phrase: A phrase entered through `Phrase`.
        chil_ext: Optional substructures extending [CHIL tag](https://gedcom.io/terms/v7/CHIL)
            entered through `Extension`.

    See Also:
        `Extension`
        `genedata.build.individual_xref`
        `Phrase`

    Reference:
        [GEDCOM CHIL tag](https://gedcom.io/terms/v7/CHIL)
        [GEDCOM Family Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_RECORD)

    This is a portion of the GEDCOM Family Record.
    >     +1 CHIL @<XREF:INDI>@                    {0:M}  g7:CHIL
    >        +2 PHRASE <Text>                      {0:1}  g7:PHRASE
    """

    individual_xref: IndividualXref = Void.INDI
    phrase: PhraseType = None
    chil_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(
                self.individual_xref, IndividualXref, no_list=True
            )
            and Checker.verify_not_empty(self.individual_xref)
            and Checker.verify_type(self.phrase, Phrase, no_list=True)
            and Checker.verify_ext(Tag.CHIL, self.chil_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = Default.EMPTY
        if str(self.individual_xref) != Void.NAME and self.validate():
            lines = Tagger.string(
                lines, level, Tag.CHIL, str(self.individual_xref), format=False
            )
            lines = Tagger.structure(lines, level + 1, self.chil_ext)
            lines = Tagger.structure(lines, level + 1, self.phrase)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'Child',
                (
                    '    individual_xref = ',
                    self.individual_xref,
                    tabs + 1,
                    full,
                    True,
                ),
                ('    phrase = ', self.phrase, tabs + 1, full, False),
                ('    chil_ext = ', self.chil_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


ChilType = Child | list[Child] | None


class LDSOrdinanceDetail(NamedTuple):
    """Store, validate and display the GEDCOM LDS Ordinance Detail structure.

    Examples:

    Args:
        date: A date entered through `Date`.
        time: A time entered through `Time`.
        phrase: A phrase entered through `Phrase`.
        temple: The name of the tmeple where the ordinance occurred.
        place: The place where the ordinance occurred entered through `Place`.
        status: A tag from the [ord-STAT enumeration set](https://gedcom.io/terms/v7/enumset-ord-STAT)
            entered by placing `Tag.` in front of the capitalized name of the tag.
        status_date: The status date entered through `Date`.
        status_time: The status time entered through `Time`.
        notes: Notes entered through `Note`.
        source_citations: Citations entered through `SourceCitation`.
        temple_ext: Optional substructures extending [TEMP tag](https://gedcom.io/terms/v7/TEMP)
            entered through `Extension`.

    See Also:
        `Date`
        `Extension`
        `Note`
        `Phrase`
        `Place`
        `SourceCitation`
        `Time`

    Reference:
        [GEEDCOM ord-STAT enumeration set](https://gedcom.io/terms/v7/enumset-ord-STAT)
        [GEDCOM TEMP tag](https://gedcom.io/terms/v7/TEMP)
        [GEDCOM LDS Ordinance Detail](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#LDS_ORDINANCE_DETAIL)

    > n <<DATE_VALUE>>                         {0:1}
    > n TEMP <Text>                            {0:1}  [g7:TEMP](https://gedcom.io/terms/v7/TEMP)
    > n <<PLACE_STRUCTURE>>                    {0:1}
    > n STAT <Enum>                            {0:1}  [g7:ord-STAT](https://gedcom.io/terms/v7/ord-STAT)
    >   +1 DATE <DateExact>                    {1:1}  [g7:DATE-exact](https://gedcom.io/terms/v7/DATE-exact)
    >      +2 TIME <Time>                      {0:1}  [g7:TIME](https://gedcom.io/terms/v7/TIME)
    > n <<NOTE_STRUCTURE>>                     {0:M}
    > n <<SOURCE_CITATION>>                    {0:M}
    """

    date: DateType = None
    time: TimeType = None
    phrase: PhraseType = None
    temple: str = Default.EMPTY
    place: PlacType = None
    status: Tag = Tag.NONE
    status_date: DateType = None
    status_time: TimeType = None
    notes: NoteType = None
    source_citations: SourCiteType = None
    temple_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.date, Date, no_list=True)
            and Checker.verify_type(self.time, Time, no_list=True)
            and Checker.verify_type(self.phrase, Phrase, no_list=True)
            and Checker.verify_type(self.temple, str, no_list=True)
            and Checker.verify_type(self.place, Place, no_list=True)
            and Checker.verify_enum(self.status, Stat)
            and Checker.verify_type(self.status_date, Date, no_list=True)
            and Checker.verify_type(self.status_time, Time, no_list=True)
            and Checker.verify(
                self.status != Tag.NONE,
                self.date is not None,
                Msg.STAT_REQUIRES_DATE,
            )
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_type(self.source_citations, SourceCitation)
            and Checker.verify_ext(Tag.TEMP, self.temple_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.structure(lines, level, self.date)
            lines = Tagger.structure(lines, level + 1, self.time)
            lines = Tagger.structure(lines, level + 1, self.phrase)
            lines = Tagger.string(lines, level, Tag.TEMP, self.temple)
            lines = Tagger.structure(lines, level + 1, self.temple_ext)
            lines = Tagger.structure(lines, level, self.place)
            lines = Tagger.string(lines, level, Tag.STAT, self.status.value)
            lines = Tagger.structure(lines, level + 1, self.status_date)
            lines = Tagger.structure(lines, level + 1, self.status_time)
            lines = Tagger.structure(lines, level, self.notes)
            lines = Tagger.structure(lines, level, self.source_citations)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'LDSOrdinanceDetail',
                ('    date = ', self.date, tabs + 1, full, False),
                ('    time = ', self.time, tabs + 1, full, False),
                ('    phrase = ', self.phrase, tabs + 1, full, False),
                ('    temple = ', self.temple, tabs, full, False),
                ('    place = ', self.place, tabs + 1, full, False),
                ('    status = ', self.status, tabs, full, False),
                ('    status_date = ', self.status_date, tabs + 1, full, False),
                ('    status_time = ', self.status_time, tabs + 1, full, False),
                ('    notes = ', self.notes, tabs + 1, full, False),
                (
                    '    source_citations = ',
                    self.source_citations,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    temple_ext = ', self.temple_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


LDSOrdDetailType = LDSOrdinanceDetail | None


class LDSSpouseSealing(NamedTuple):
    """Store, validate and display the LDS Spouse Sealing structure.

    Examples:

    Args:
        detail: The ordinance details enetered through `LDSOrdinanceDetail`.
        slgs_ext: Optional substructures extending [SLGS tag](https://gedcom.io/terms/v7/SLGS)
            entered through `Extension`.

    See Also:
        `Extension`
        `LDSOrdinanceDetail`

    Reference:
        [GEDCOM SLGS tag](https://gedcom.io/terms/v7/SLGS)
        [GEDCOM LDS Spouse Sealing Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#LDS_SPOUSE_SEALING)

    > n SLGS                                     {1:1}  [g7:SLGS](https://gedcom.io/terms/v7/SLGS)
    >   +1 <<LDS_ORDINANCE_DETAIL>>              {0:1}
    """

    detail: LDSOrdDetailType = None
    slgs_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = Checker.verify_type(
            self.detail, LDSOrdinanceDetail, no_list=True
        ) and Checker.verify_ext(Tag.SLGS, self.slgs_ext)
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.empty(lines, level, Tag.SLGS)
            lines = Tagger.structure(lines, level + 1, self.slgs_ext)
            lines = Tagger.structure(lines, level + 1, self.detail)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'LDSSpouseSealing',
                ('    detail = ', self.detail, tabs + 1, full, False),
                ('    slgs_ext = ', self.slgs_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


LDSSpouSealingType = LDSSpouseSealing | None


class LDSIndividualOrdinance(NamedTuple):
    """Store, validate and display the GEDCOM LDS Individual Ordinances structure.

    Examples:

    Args:
        tag: A tag from the enumeration set.
        ordinance_detail: The ordination details entered through `LDSOrdinanceDetail`.
        family_xref: A family cross-reference identifier constructed from `genedata.build.family_xref`.
        tag_ext: Optional substructures extending whichever tag was used and entered through `Extension`.

    See Also:
        `Extension`
        `genedata.build.family_xref`
        `LDSOrdinanceDetail`

    Reference:
        [GEDCOM LDS Individual Ordinances](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#LDS_INDIVIDUAL_ORDINANCE)

    [
    n BAPL                                     {1:1}  [g7:BAPL](https://gedcom.io/terms/v7/BAPL)
      +1 <<LDS_ORDINANCE_DETAIL>>              {0:1}
    |
    n CONL                                     {1:1}  [g7:CONL](https://gedcom.io/terms/v7/CONL)
      +1 <<LDS_ORDINANCE_DETAIL>>              {0:1}
    |
    n ENDL                                     {1:1}  [g7:ENDL](https://gedcom.io/terms/v7/ENDL)
      +1 <<LDS_ORDINANCE_DETAIL>>              {0:1}
    |
    n INIL                                     {1:1}  [g7:INIL](https://gedcom.io/terms/v7/INIL)
      +1 <<LDS_ORDINANCE_DETAIL>>              {0:1}
    |
    n SLGC                                     {1:1}  [g7:SLGC](https://gedcom.io/terms/v7/SLGC)
      +1 <<LDS_ORDINANCE_DETAIL>>              {0:1}
      +1 FAMC @<XREF:FAM>@                     {1:1}  [g7:FAMC](https://gedcom.io/terms/v7/FAMC)
    ]
    """

    tag: Tag = Tag.NONE
    ordinance_detail: LDSOrdDetailType = None
    family_xref: FamilyXref = Void.FAM
    tag_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.tag, Tag, no_list=True)
            and Checker.verify_not_empty(self.tag)
            and Checker.verify_type(
                self.ordinance_detail, LDSOrdinanceDetail, no_list=True
            )
            and Checker.verify_type(self.family_xref, FamilyXref, no_list=True)
            and Checker.verify(
                self.tag.value == Tag.SLGC.value,
                self.family_xref.fullname != Void.FAM.fullname,
                Msg.SLGC_REQUIRES_FAM,
            )
            and Checker.verify_ext(self.tag, self.tag_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.empty(lines, level, self.tag)
            lines = Tagger.structure(lines, level + 1, self.tag_ext)
            lines = Tagger.structure(lines, level + 1, self.ordinance_detail)
            if self.tag == Tag.SLGC:
                lines = Tagger.string(
                    lines,
                    level + 1,
                    Tag.FAMC,
                    self.family_xref.fullname,
                    format=False,
                )
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'LDSIndividualOrdinance',
                ('    tag = ', self.tag, tabs + 1, full, True),
                (
                    '    ordinance_detail = ',
                    self.ordinance_detail,
                    tabs + 1,
                    full,
                    False,
                ),
                (
                    '    family_xref = ',
                    self.family_xref,
                    tabs,
                    full,
                    self.tag == Tag.SLGC,
                ),
                ('    tag_ext = ', self.tag_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


LDSIndiOrd = LDSIndividualOrdinance | None


class IndividualEventDetail(NamedTuple):
    """Store, validate and display a GEDCOM Individual Event Detail structure.

    Args:
        event_detail: Event details entered through `IndividualEventDetail`.
        age: The individual's age entered through `Age`.
        phrase: A phrase entered through `Phrase`.

    See Also:
        `Age`
        `IndividualEventDetail`
        `Phrase`

    Reference:
        [GEDCOM Individual Event Detail](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_EVENT_DETAIL)

    > n <<EVENT_DETAIL>>                         {1:1}
    > n AGE <Age>                                {0:1}  [g7:AGE](https://gedcom.io/terms/v7/AGE)
    >   +1 PHRASE <Text>                         {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    """

    event_detail: EvenDetailType = None
    age: AgeType = None
    phrase: PhraseType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.event_detail, EventDetail, no_list=True)
            and Checker.verify_not_empty(self.event_detail)
            and Checker.verify_type(self.age, Age, no_list=True)
            and Checker.verify_type(self.phrase, Phrase, no_list=True)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.structure(lines, level, self.event_detail)
            if self.age is not None:
                lines = Tagger.structure(lines, level, self.age)
                lines = Tagger.structure(lines, level + 1, self.phrase)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'IndividualEventDetail',
                (
                    '    event_detail = ',
                    self.event_detail,
                    tabs + 1,
                    full,
                    True,
                ),
                ('    age = ', self.age, tabs + 1, full, False),
                ('    phrase = ', self.phrase, tabs + 1, full, False),
            ),
            Default.INDENT * tabs,
        )


IndiEvenDetailType = IndividualEventDetail | list[IndividualEventDetail] | None


class IndividualAttribute(NamedTuple):
    """Store, validate and display a GEDCOM Individual Attribute structure.

    Examples:

    Args:
        tag: A tag from the enumeration set
        payload: The value on the same GEDCOM output line as the tag.
        tag_type: The type or additional information about the tag.
        event_detail: Individual event details entered through `IndividualEventDetail`.
        tag_ext: Optional substructures extending whichever tag was used and entered through `Extension`.
        type_ext: Optional substructures extending [TYPE tag](https://gedcom.io/terms/v7/TYPE)
            entered through `Extension`.

    See Also:
        `Extension`
        `IndividualEventDetail`

    Reference:
        [GEDCOM SLGS tag](https://gedcom.io/terms/v7/SLGS)
        [GEDCOM TYPE tag](https://gedcom.io/terms/v7/TYPE)
        [GEDCOM Individual Attribute Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_ATTRIBUTE_STRUCTURE)

    > [
    > n CAST <Text>                              {1:1}  [g7:CAST](https://gedcom.io/terms/v7/CAST)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n DSCR <Text>                              {1:1}  [g7:DSCR](https://gedcom.io/terms/v7/DSCR)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n EDUC <Text>                              {1:1}  [g7:EDUC](https://gedcom.io/terms/v7/EDUC)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n IDNO <Special>                           {1:1}  [g7:IDNO](https://gedcom.io/terms/v7/IDNO)
    >   +1 TYPE <Text>                           {1:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n NATI <Text>                              {1:1}  [g7:NATI](https://gedcom.io/terms/v7/NATI)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n NCHI <Integer>                           {1:1}  [g7:INDI-NCHI](https://gedcom.io/terms/v7/INDI-NCHI)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n NMR <Integer>                            {1:1}  [g7:NMR](https://gedcom.io/terms/v7/NMR)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n OCCU <Text>                              {1:1}  [g7:OCCU](https://gedcom.io/terms/v7/OCCU)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n PROP <Text>                              {1:1}  [g7:PROP](https://gedcom.io/terms/v7/PROP)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n RELI <Text>                              {1:1}  [g7:INDI-RELI](https://gedcom.io/terms/v7/INDI-RELI)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n RESI <Text>                              {1:1}  [g7:INDI-RESI](https://gedcom.io/terms/v7/INDI-RESI)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n SSN <Special>                            {1:1}  [g7:SSN](https://gedcom.io/terms/v7/SSN)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n TITL <Text>                              {1:1}  [g7:INDI-TITL](https://gedcom.io/terms/v7/INDI-TITL)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n FACT <Text>                              {1:1}  [g7:INDI-FACT](https://gedcom.io/terms/v7/INDI-FACT)
    >   +1 TYPE <Text>                           {1:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > ]
    """

    tag: Tag = Tag.NONE
    payload: str = Default.EMPTY
    tag_type: str = Default.EMPTY
    event_detail: IndiEvenDetailType = None
    tag_ext: ExtType = None
    type_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_enum(self.tag, IndiAttr)
            and Checker.verify_not_empty(self.tag)
            and Checker.verify_type(self.payload, str, no_list=True)
            and Checker.verify_not_empty(self.payload)
            and Checker.verify_type(self.tag_type, str, no_list=True)
            and Checker.verify(
                self.tag == Tag.FACT,
                self.tag_type == Default.EMPTY,
                Msg.FACT_REQUIRES_TYPE,
            )
            and Checker.verify(
                self.tag == Tag.IDNO,
                self.tag_type == Default.EMPTY,
                Msg.IDNO_REQUIRES_TYPE,
            )
            and Checker.verify_type(
                self.event_detail, IndividualEventDetail, no_list=True
            )
            and Checker.verify_ext(Tag.TYPE, self.type_ext)
            and Checker.verify_ext(self.tag, self.tag_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, self.tag, self.payload)
            lines = Tagger.structure(lines, level + 1, self.tag_ext)
            lines = Tagger.string(lines, level + 1, Tag.TYPE, self.tag_type)
            lines = Tagger.structure(lines, level + 1, self.type_ext)
            lines = Tagger.structure(lines, level + 1, self.event_detail)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'IndividualAttribute',
                ('    tag = ', self.tag, tabs, full, True),
                ('    payload = ', self.payload, tabs, full, True),
                (
                    '    tag_type = ',
                    self.tag_type,
                    tabs,
                    full,
                    self.tag in [Tag.FACT, Tag.IDNO],
                ),
                (
                    '    event_detail = ',
                    self.event_detail,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    tag_ext = ', self.tag_ext, tabs, full, False),
                ('    type_ext = ', self.type_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


IndiAttrType = IndividualAttribute | list[IndividualAttribute] | None


class IndividualEvent(NamedTuple):
    """Store, validate and display a GEDCOM Individual Event Structure.

    Examples:
        The GEDCOM specification offers the following example of the use of the `EVEN` event
        tag.  Under the individual `@I1@` there are two events.  The first is a land lease
        with a data of October 2, 1837.  The second is a lease of mining equipment with
        a data of November 4, 1837.

        > 0 @I1@ INDI
        > 1 EVEN
        > 2 TYPE Land Lease
        > 2 DATE 2 OCT 1837
        > 1 EVEN Mining equipment
        > 2 TYPE Equipment Lease
        > 2 DATE 4 NOV 1837

        This example can be implemented as follows.

        First import the needed classes.
        >>> from genedata.build import Genealogy
        >>> from genedata.store import (
        ...     Date,
        ...     Time,
        ...     EventDetail,
        ...     Individual,
        ...     IndividualEvent,
        ...     IndividualEventDetail,
        ... )
        >>> from genedata.gedcom import Tag

        Next, create a Genealogy and an individual with reference `@I1@`.
        >>> genealogy = Genealogy('event example')
        >>> indi_i1_xref = genealogy.individual_xref('I1')

        Finally, create the individual record for `@I1@` with two individual events
        and display the results.
        >>> indi_i1 = Individual(
        ...     xref=indi_i1_xref,
        ...     events=[
        ...         IndividualEvent(
        ...             tag=Tag.EVEN,
        ...             tag_type='Land Lease',
        ...             event_detail=IndividualEventDetail(
        ...                 event_detail=EventDetail(date=Date(1837, 10, 2))
        ...             ),
        ...         ),
        ...         IndividualEvent(
        ...             tag=Tag.EVEN,
        ...             payload='Mining equipment',
        ...             tag_type='Equipment Lease',
        ...             event_detail=IndividualEventDetail(
        ...                 EventDetail(date=Date(1837, 11, 4))
        ...             ),
        ...         ),
        ...     ],
        ... )
        >>> print(indi_i1.ged(0))
        0 @I1@ INDI
        1 EVEN
        2 TYPE Land Lease
        2 DATE 2 OCT 1837
        1 EVEN Mining equipment
        2 TYPE Equipment Lease
        2 DATE 4 NOV 1837
        <BLANKLINE>

    Args:
        tag: A tag from the [EVEN enumeration set](https://gedcom.io/terms/v7/enumset-EVEN)
            entered by placing `Tag.` in front of the capitalized name from the set.
        payload: A value appearing on the same GEDCOM line as the tag.
        tag_type: Information associated with the tag.
        event_detail: Individual event details entered through `IndividualEventDetail`.
        family_xref: A cross-reference identifier constructed from `genedata.build.family_xref` displayed only for the ADOP, BIRT or CHR tags.
        adoption: A tag from the [ADOP enumeration set](https://gedcom.io/terms/v7/enumset-ADOP) displayed only for the ADOP tag
            entered by placing `Tag.` in front of the capitalized name from the set.
        phrase: A phrase describing the adoption and displayed only for the ADOP event entered through `Phrase`.
        tag_ext: Optional substructures extending whichever tag was used and entered through `Extension`.

    See Also:
        `Extension`
        `genedata.build.family_xref`
        `IndividualEventDetail`
        `Phrase`

    References:
        [GEDCOM ADOP enumeration set](https://gedcom.io/terms/v7/enumset-ADOP)
        [GEDCOM EVEN enumeration set](https://gedcom.io/terms/v7/enumset-EVEN)
        [GEDCOM INDI-EVEN](https://gedcom.io/terms/v7/INDI-EVEN)
        [GEDCOM Individual Event Tags](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#individual-events)
        [GEDCOM Individual Event Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_EVENT_STRUCTURE)

    [
    > n ADOP [Y|<NULL>]                          {1:1}  [g7:ADOP](https://gedcom.io/terms/v7/ADOP)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    >   +1 FAMC @<XREF:FAM>@                     {0:1}  [g7:ADOP-FAMC](https://gedcom.io/terms/v7/ADOP-FAMC)
    >      +2 ADOP <Enum>                        {0:1}  [g7:FAMC-ADOP](https://gedcom.io/terms/v7/enumset-ADOP)
    >         +3 PHRASE <Text>                   {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    > |
    > n BAPM [Y|<NULL>]                          {1:1}  [g7:BAPM](https://gedcom.io/terms/v7/BAPM)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n BARM [Y|<NULL>]                          {1:1}  [g7:BARM](https://gedcom.io/terms/v7/BARM)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n BASM [Y|<NULL>]                          {1:1}  [g7:BASM](https://gedcom.io/terms/v7/BASM)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n BIRT [Y|<NULL>]                          {1:1}  [g7:BIRT](https://gedcom.io/terms/v7/BIRT)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    >   +1 FAMC @<XREF:FAM>@                     {0:1}  [g7:FAMC](https://gedcom.io/terms/v7/FAMC)
    > |
    > n BLES [Y|<NULL>]                          {1:1}  [g7:BLES](https://gedcom.io/terms/v7/BLES)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n BURI [Y|<NULL>]                          {1:1}  [g7:BURI](https://gedcom.io/terms/v7/BURI)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n CENS [Y|<NULL>]                          {1:1}  [g7:INDI-CENS](https://gedcom.io/terms/v7/INDI-CENS)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n CHR [Y|<NULL>]                           {1:1}  [g7:CHR](https://gedcom.io/terms/v7/CHR)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    >   +1 FAMC @<XREF:FAM>@                     {0:1}  [g7:FAMC](https://gedcom.io/terms/v7/FAMC)
    > |
    > n CHRA [Y|<NULL>]                          {1:1}  [g7:CHRA](https://gedcom.io/terms/v7/CHRA)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n CONF [Y|<NULL>]                          {1:1}  [g7:CONF](https://gedcom.io/terms/v7/CONF)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n CREM [Y|<NULL>]                          {1:1}  [g7:CREM](https://gedcom.io/terms/v7/CREM)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n DEAT [Y|<NULL>]                          {1:1}  [g7:DEAT](https://gedcom.io/terms/v7/DEAT)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n EMIG [Y|<NULL>]                          {1:1}  [g7:EMIG](https://gedcom.io/terms/v7/EMIG)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n FCOM [Y|<NULL>]                          {1:1}  [g7:FCOM](https://gedcom.io/terms/v7/FCOM)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n GRAD [Y|<NULL>]                          {1:1}  [g7:GRAD](https://gedcom.io/terms/v7/GRAD)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n IMMI [Y|<NULL>]                          {1:1}  [g7:IMMI](https://gedcom.io/terms/v7/IMMI)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n NATU [Y|<NULL>]                          {1:1}  [g7:NATU](https://gedcom.io/terms/v7/NATU)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n ORDN [Y|<NULL>]                          {1:1}  [g7:ORDN](https://gedcom.io/terms/v7/ORDN)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n PROB [Y|<NULL>]                          {1:1}  [g7:PROB](https://gedcom.io/terms/v7/PROB)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n RETI [Y|<NULL>]                          {1:1}  [g7:RETI](https://gedcom.io/terms/v7/RETI)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n WILL [Y|<NULL>]                          {1:1}  [g7:WILL](https://gedcom.io/terms/v7/WILL)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > |
    > n EVEN <Text>                              {1:1}  [g7:INDI-EVEN](https://gedcom.io/terms/v7/INDI-EVEN)
    >   +1 TYPE <Text>                           {1:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    > ]
    """

    tag: Tag = Tag.NONE
    payload: str = Default.EMPTY
    tag_type: str = Default.EMPTY
    event_detail: IndiEvenDetailType = None
    family_xref: FamilyXref = Void.FAM
    adoption: Tag = Tag.NONE
    phrase: PhraseType = None
    tag_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_enum(self.tag, IndiEven)
            and Checker.verify_not_empty(self.tag)
            and Checker.verify_type(self.tag_type, str, no_list=True)
            and Checker.verify(
                self.tag != Tag.EVEN,
                self.payload in ['Y', ''],
                Msg.PAYLOAD_IS_Y,
            )
            and Checker.verify(
                self.tag == Tag.EVEN,
                self.tag_type != Default.EMPTY,
                Msg.EVEN_REQUIRES_TYPE,
            )
            and Checker.verify_type(
                self.event_detail, IndividualEventDetail, no_list=True
            )
            and Checker.verify_type(self.family_xref, FamilyXref, no_list=True)
            and Checker.verify_enum(self.adoption, Adop)
            and Checker.verify_type(self.phrase, Phrase, no_list=True)
            and Checker.verify_ext(self.tag, self.tag_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            if self.payload == Default.EMPTY:
                lines = Tagger.empty(lines, level, self.tag)
            else:
                lines = Tagger.string(lines, level, self.tag, self.payload)
            lines = Tagger.structure(lines, level + 1, self.tag_ext)
            lines = Tagger.string(lines, level + 1, Tag.TYPE, self.tag_type)
            lines = Tagger.structure(lines, level + 1, self.event_detail)
            if (
                self.tag.value
                in (Tag.BIRT.value, Tag.CHR.value, Tag.ADOP.value)
                and self.family_xref.name != Void.FAM.name
            ):
                lines = Tagger.string(
                    lines,
                    level + 1,
                    Tag.FAMC,
                    self.family_xref.fullname,
                    format=False,
                )
                if (
                    self.tag.value == Tag.ADOP.value
                    and self.family_xref.name != Void.FAM.name
                ):
                    lines = Tagger.string(
                        lines, level + 2, Tag.ADOP, self.adoption.value
                    )
                    if self.adoption.value != Tag.NONE.value:
                        lines = Tagger.structure(lines, level + 3, self.phrase)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'IndividualEvent',
                ('    tag = ', self.tag, tabs, full, True),
                ('    payload = ', self.payload, tabs, full, False),
                (
                    '    tag_type = ',
                    self.tag_type,
                    tabs,
                    full,
                    self.tag == Tag.EVEN,
                ),
                (
                    '    event_detail = ',
                    self.event_detail,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    family_xref = ', self.family_xref, tabs, full, False),
                ('    adoption = ', self.adoption, tabs, full, False),
                ('    phrase = ', self.phrase, tabs + 1, full, False),
                ('    tag_ext = ', self.tag_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


IndiEvenType = IndividualEvent | list[IndividualEvent] | None


class Alias(NamedTuple):
    """Store, validate and display a GEDCOM Alias structure.

    Data about an individual may be contained in the individual records of other individuals.
    This tag references those other individuals.

    This alias information is defined as its own class because multiple aliases could
    be identified for a single individual.

    Args:
        individual_xref: An individual cross-reference identifier constructed by `genedata.build.individual_xref`.
        phrase: A phrase associated with this alias entered through `Phrase`.
        alia_ext: Optional substructures extending [ALIA tag](https://gedcom.io/terms/v7/ALIA)
            entered through `Extension`.

    See Also:
        `Extension`
        `genedata.build.individual_xref`
        `Phrase`

    Reference:
        [GEDCOM ALIA tag](https://gedcom.io/terms/v7/ALIA)
        [GEDCOM Individual Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_RECORD)

    > +1 ALIA @<XREF:INDI>@                    {0:M}  [g7:ALIA](https://gedcom.io/terms/v7/ALIA)
    >    +2 PHRASE <Text>                      {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    """

    individual_xref: IndividualXref = Void.INDI
    phrase: PhraseType = None
    alia_ext: ExtType = None

    def validate(self, main_individual: IndividualXref = Void.INDI) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(
                self.individual_xref, IndividualXref, no_list=True
            )
            and Checker.verify_not_empty(self.individual_xref)
            and Checker.verify_type(self.phrase, Phrase, no_list=True)
            and Checker.verify(
                True,
                self.individual_xref != main_individual,
                Msg.SAME_INDIVIDUAL.format(self.individual_xref.fullname),
            )
            and Checker.verify_ext(Tag.ALIA, self.alia_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(
                lines,
                level,
                Tag.ALIA,
                self.individual_xref.fullname,
                format=False,
            )
            lines = Tagger.structure(lines, level + 1, self.alia_ext)
            lines = Tagger.structure(lines, level + 1, self.phrase)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'Alias',
                (
                    '    individual_xref = ',
                    self.individual_xref,
                    tabs,
                    full,
                    True,
                ),
                ('    phrase = ', self.phrase, tabs + 1, full, False),
                ('    alia_ext = ', self.alia_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


AliaType = Alias | list[Alias] | None


class FamilyChild(NamedTuple):
    """Store, validate and display family child data.

    Multiple FAMC records may be defined for a singe Indivdiual Record.  This class
    defines a single FAMC (Family Child) substructure.

    Examples:

    Args:
        family_xref: A cross-reference identifier constructed with `genedata.build.family_xref`.
        pedigree: A tag from the [PEDI enumeration set](https://gedcom.io/terms/v7/enumset-PEDI)
            entered by placing `Tag.` in front of the capitalized name from the set.
        pedigree_phrase: A phrase related to the pedigree entered through `Phrase`.
        status: A tag from the [FAMC-STAT enumeration set](https://gedcom.io/terms/v7/enumset-FAMC-STAT)
            entered by placing `Tag.` in front of the capitalized name of the tag.
        status_phrase: A phrase related to the status entered through `Phrase`.
        notes: Notes entered through `Note`.
        famc_ext: Optional substructures extending [FAMC tag](https://gedcom.io/terms/v7/FAMC)
            entered through `Extension`.
        pedi_ext: Optional substructures extending [PEDI tag](https://gedcom.io/terms/v7/PEDI)
            entered through `Extension`.
        stat_ext: Optional substructures extending [STAT tag](https://gedcom.io/terms/v7/STAT)
            entered through `Extension`.

    See Also:
        `Extension`
        `genedata.build.family_xref`
        `Note`
        `Phrase`

    References:
        [GEDCOM PEDI enumeration set](https://gedcom.io/terms/v7/enumset-PEDI)
        [GEDCOM FAMC tag](https://gedcom.io/terms/v7/FAMC)
        [GEDCOM PEDI tag](https://gedcom.io/terms/v7/PEDI)
        [GEDCOM STAT tag](https://gedcom.io/terms/v7/STAT)
        [GEDCOM Individual Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_RECORD)

    > +1 FAMC @<XREF:FAM>@                     {0:M}  [g7:INDI-FAMC](https://gedcom.io/terms/v7/INDI-FAMC)
    >    +2 PEDI <Enum>                        {0:1}  [g7:PEDI](https://gedcom.io/terms/v7/PEDI)
    >       +3 PHRASE <Text>                   {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    >    +2 STAT <Enum>                        {0:1}  [g7:FAMC-STAT](https://gedcom.io/terms/v7/FAMC-STAT)
    >       +3 PHRASE <Text>                   {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    >    +2 <<NOTE_STRUCTURE>>                 {0:M}
    """

    family_xref: FamilyXref = Void.FAM
    pedigree: Tag = Tag.NONE
    pedigree_phrase: PhraseType = None
    status: Tag = Tag.NONE
    status_phrase: PhraseType = None
    notes: list[Note] | None = None
    famc_ext: ExtType = None
    pedi_ext: ExtType = None
    stat_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.family_xref, FamilyXref, no_list=True)
            and Checker.verify_not_empty(self.family_xref)
            and Checker.verify_enum(self.pedigree, Pedi)
            and Checker.verify_type(self.pedigree_phrase, Phrase, no_list=True)
            and Checker.verify_enum(self.status, FamcStat)
            and Checker.verify_type(self.status_phrase, Phrase, no_list=True)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_ext(Tag.FAMC, self.famc_ext)
            and Checker.verify_ext(Tag.PEDI, self.pedi_ext)
            and Checker.verify_ext(Tag.STAT, self.stat_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(
                lines, level, Tag.FAMC, self.family_xref.fullname, format=False
            )
            lines = Tagger.structure(lines, level + 1, self.famc_ext)
            lines = Tagger.string(
                lines, level + 1, Tag.PEDI, self.pedigree.value
            )
            lines = Tagger.structure(lines, level + 1, self.pedi_ext)
            lines = Tagger.structure(lines, level + 2, self.pedigree_phrase)
            lines = Tagger.string(lines, level + 1, Tag.STAT, self.status.value)
            lines = Tagger.structure(lines, level + 2, self.stat_ext)
            lines = Tagger.structure(lines, level + 2, self.status_phrase)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'FamilyChild',
                ('    family_xref = ', self.family_xref, tabs, full, True),
                ('    pedigree = ', self.pedigree, tabs, full, False),
                (
                    '    pedigree_phrase = ',
                    self.pedigree_phrase,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    status = ', self.status, tabs, full, False),
                (
                    '    status_phrase = ',
                    self.status_phrase,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    notes = ', self.notes, tabs + 1, full, False),
                ('    famc_ext = ', self.famc_ext, tabs, full, False),
                ('    pedi_ext = ', self.pedi_ext, tabs, full, False),
                ('    stat_ext = ', self.stat_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


FamcType = FamilyChild | list[FamilyChild] | None


class FamilySpouse(NamedTuple):
    """Store, validate and display the GEDCOM Family Spouse structure.

    Examples:

    Args:
        family_xref: A cross-reference identifier constructed by `genedata.build.family_xref`.
        notes: Notes entered through `Note`.
        fams_ext: Optional substructures extending [FAMS tag](https://gedcom.io/terms/v7/FAMS)
            entered through `Extension`.

    See Also:
        `Extension`
        `genedata.build.family_xref`
        `Note`

    Reference:
        [GEDCOM FAMS tag](https://gedcom.io/terms/v7/FAMS)

    > +1 FAMS @<XREF:FAM>@                     {0:M}  g7:FAMS
    >    +2 <<NOTE_STRUCTURE>>                 {0:M}
    """

    family_xref: FamilyXref = Void.FAM
    notes: NoteType = None
    fams_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.family_xref, FamilyXref, no_list=True)
            and Checker.verify_not_empty(self.family_xref)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_ext(Tag.FAMS, self.fams_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(
                lines, level, Tag.FAMS, str(self.family_xref), format=False
            )
            lines = Tagger.structure(lines, level + 1, self.fams_ext)
            lines = Tagger.structure(lines, level + 1, self.notes)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'FamilySpouse',
                ('    family_xref = ', self.family_xref, tabs, full, True),
                ('    notes = ', self.notes, tabs + 1, full, False),
                ('    fams_ext = ', self.fams_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


FamsType = FamilySpouse | list[FamilySpouse] | None


class FileTranslation(NamedTuple):
    """Store, validate and display the GEDCOM File structure.

    Examples:

    Args:
        tran: A file reference to the translation.
        form: The mime type of the file.
        tran_ext: Optional substructures extending [TRAN tag](https://gedcom.io/terms/v7/TRAN)
            entered through `Extension`.
        form_ext: Optional substructures extending [FORM tag](https://gedcom.io/terms/v7/FORM)
            entered through `Extension`.


    See Also:
        `Exception`

    Reference:
        [GEDCOM FORM tag](https://gedcom.io/terms/v7/FORM)
        [GEDCOM TRAN tag](https://gedcom.io/terms/v7/TRAN)
        [GEDCOM Multimedia Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#MULTIMEDIA_RECORD)

    > +1 FILE <FilePath>                       {1:M}  g7:FILE
    >    +2 FORM <MediaType>                   {1:1}  g7:FORM
    >       +3 MEDI <Enum>                     {0:1}  g7:MEDI
    >          +4 PHRASE <Text>                {0:1}  g7:PHRASE
    >    +2 TITL <Text>                        {0:1}  g7:TITL
    >    +2 TRAN <FilePath>                    {0:M}  g7:FILE-TRAN
    >       +3 FORM <MediaType>                {1:1}  g7:FORM
    """

    tran: str = Default.EMPTY
    form: str = Default.MIME
    tran_ext: ExtType = None
    form_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.tran, str, no_list=True)
            and Checker.verify_not_empty(self.tran)
            and Checker.verify_type(self.form, str, no_list=True)
            and Checker.verify_not_empty(self.form)
            and Checker.verify_ext(Tag.TRAN, self.tran_ext)
            and Checker.verify_ext(Tag.FORM, self.form_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.TRAN, self.tran)
            lines = Tagger.structure(lines, level + 1, self.tran_ext)
            lines = Tagger.string(lines, level + 1, Tag.FORM, self.form)
            lines = Tagger.structure(lines, level + 2, self.form_ext)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'FileTranslation',
                ('    tran = ', self.tran, tabs, full, True),
                ('    form = ', self.form, tabs, full, False),
                ('    tran_ext = ', self.tran_ext, tabs, full, False),
                ('    form_ext = ', self.form_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


FileTranType = FileTranslation | list[FileTranslation] | None


class File(NamedTuple):
    """Store, validate and display the GEDCOM File structure.

    Multiple files may be used in a Multimedia Record, but at least one exists.

    Examples:

    Args:
        file: The location of the file.
        form: The mime type of the file.
        medi: A tag from the [MEDI enumeration set](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#enumset-MEDI)
            entered by placing `Tag.` in front of the capitalized name from the set.
        phrase: A phrase associated with the file entered through `Phrase`.
        titl: The title of the file.
        file_translations: Translations entered through `FileTranslation`.
        file_ext: Optional substructures extending [FILE tag](https://gedcom.io/terms/v7/FILE)
            entered through `Extension`.
        form_ext: Optional substructures extending [FORM tag](https://gedcom.io/terms/v7/FORM)
            entered through `Extension`.
        medi_ext: Optional substructures extending [MEDI tag](https://gedcom.io/terms/v7/MEDI)
            entered through `Extension`.
        titl_ext: Optional substructures extending [TITL tag](https://gedcom.io/terms/v7/TITL)
            entered through `Extension`.

    See Also:
        `Extension`
        `FileTranslation`
        `Phrase`

    Reference:
        [GEDCOM MEDI enumeration set](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#enumset-MEDI)
        [GEDCOM FILE tag](https://gedcom.io/terms/v7/FILE)
        [GEDCOM FORM tag](https://gedcom.io/terms/v7/FORM)
        [GEDCOM MEDI tag](https://gedcom.io/terms/v7/MEDI)
        [GEDCOM TITL tag](https://gedcom.io/terms/v7/TITL)
        [GEDCOM Multimedia Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#MULTIMEDIA_RECORD)

    > +1 FILE <FilePath>                       {1:M}  g7:FILE
    >    +2 FORM <MediaType>                   {1:1}  g7:FORM
    >       +3 MEDI <Enum>                     {0:1}  g7:MEDI
    >          +4 PHRASE <Text>                {0:1}  g7:PHRASE
    >    +2 TITL <Text>                        {0:1}  g7:TITL
    >    +2 TRAN <FilePath>                    {0:M}  g7:FILE-TRAN
    >       +3 FORM <MediaType>                {1:1}  g7:FORM
    """

    file: str = Default.EMPTY
    form: str = Default.MIME
    medi: Tag = Tag.NONE
    phrase: PhraseType = None
    titl: str = Default.EMPTY
    file_translations: FileTranType = None
    file_ext: ExtType = None
    form_ext: ExtType = None
    medi_ext: ExtType = None
    medi_tag_ext: ExtType = None
    titl_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.file, str, no_list=True)
            and Checker.verify_not_empty(self.file)
            and Checker.verify_type(self.form, str, no_list=True)
            and Checker.verify_not_empty(self.form)
            and Checker.verify_enum(self.medi, Medium)
            and Checker.verify_type(self.phrase, Phrase, no_list=True)
            and Checker.verify_type(self.titl, str, no_list=True)
            and Checker.verify_type(self.file_translations, FileTranslation)
            and Checker.verify_ext(Tag.FILE, self.file_ext)
            and Checker.verify_ext(Tag.FORM, self.form_ext)
            and Checker.verify_ext(Tag.MEDI, self.medi_ext)
            and Checker.verify_ext(Tag.TITL, self.titl_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.FILE, self.file)
            lines = Tagger.structure(lines, level + 1, self.file_ext)
            lines = Tagger.string(lines, level + 1, Tag.FORM, self.form)
            lines = Tagger.structure(lines, level + 2, self.form_ext)
            lines = Tagger.string(lines, level + 3, Tag.MEDI, self.medi.value)
            lines = Tagger.structure(lines, level + 4, self.phrase)
            lines = Tagger.string(lines, level + 1, Tag.TITL, self.titl)
            lines = Tagger.structure(lines, level + 2, self.titl_ext)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'File',
                ('    file = ', self.file, tabs, full, True),
                ('    form = ', self.form, tabs, full, True),
                ('    medi = ', self.medi, tabs, full, False),
                ('    phrase = ', self.phrase, tabs + 1, full, False),
                ('    titl = ', self.titl, tabs, full, False),
                (
                    '    file_translations = ',
                    self.file_translations,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    file_ext = ', self.file_ext, tabs, full, False),
                ('    form_ext = ', self.form_ext, tabs, full, False),
                ('    medi_ext = ', self.medi_ext, tabs, full, False),
                ('    titl_ext = ', self.titl_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


FileType = File | list[File] | None


class SourceDataEvent(NamedTuple):
    """Store, validate and display the GEDCOM Source Event structure.

    This is an optional part of the Source.Data Record placed as a separate class
    because there may be many of these events.

    Examples:

    Args:
        event: A tag from the [EVENATTR enumeration set](https://gedcom.io/terms/v7/enumset-EVENATTR)
            entered by placing `Tag.` in front of the capitalized name from the set.
        date_period: A date period entered through `Date`.
        phrase: A phrase entered through `Phrase`.
        place: A place entered through `Place`.
        even_ext: Optional substructures extending [EVEN tag](https://gedcom.io/terms/v7/EVEN)
            entered through `Extension`.
        data_ext: Optional substructures extending [DATA tag](https://gedcom.io/terms/v7/DATA)
            entered through `Extension`.

    See Also:
        `Date`
        `Extension`
        `Phrase`
        `Place`

    Reference:
        [GEDCOM EVENATTR enumeration set](https://gedcom.io/terms/v7/enumset-EVENATTR)
        [GEDCOM DATA tag](https://gedcom.io/terms/v7/DATA)
        [GEDCOM EVEN tag](https://gedcom.io/terms/v7/EVEN)
        [GEDCOM Source Event](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_RECORD)

    >   +1 DATA                                  {0:1}  [g7:DATA]()
    >      +2 EVEN <List:Enum>                   {0:M}  [g7:DATA-EVEN]()
    >         +3 DATE <DatePeriod>               {0:1}  [g7:DATA-EVEN-DATE]()
    >            +4 PHRASE <Text>                {0:1}  [g7:PHRASE]()
    >         +3 <<PLACE_STRUCTURE>>             {0:1}
    >      +2 AGNC <Text>                        {0:1}  [g7:AGNC]()
    >      +2 <<NOTE_STRUCTURE>>                 {0:M}
    """

    event: Tag = Tag.NONE
    date_period: str = Default.EMPTY
    phrase: PhraseType = None
    place: PlacType = None
    even_ext: ExtType = None
    data_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_enum(self.event, EvenAttr)
            and Checker.verify_not_empty(self.event)
            and Checker.verify_type(self.date_period, str, no_list=True)
            and Checker.verify_type(self.phrase, Phrase, no_list=True)
            and Checker.verify_type(self.place, Place, no_list=True)
            and Checker.verify_ext(Tag.EVEN, self.even_ext)
            and Checker.verify_ext(Tag.DATE, self.data_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.EVEN, self.event.value)
            lines = Tagger.structure(lines, level + 1, self.even_ext)
            lines = Tagger.string(lines, level + 1, Tag.DATE, self.date_period)
            lines = Tagger.structure(lines, level + 2, self.data_ext)
            lines = Tagger.structure(lines, level + 2, self.phrase)
            lines = Tagger.structure(lines, level + 2, self.place)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'SourceDataEvent',
                ('    event = ', self.event, tabs + 1, full, True),
                ('    date_period = ', self.date_period, tabs + 1, full, False),
                ('    phrase = ', self.phrase, tabs + 1, full, False),
                ('    place = ', self.place, tabs + 1, full, False),
                ('    even_ext = ', self.even_ext, tabs, full, False),
                ('    data_ext = ', self.data_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


SourDataEvenType = SourceDataEvent | list[SourceDataEvent] | None


class NonEvent(NamedTuple):
    """Store, validate and display a GEDCOM Non Event structure.

    Examples:

    Args:
        no: A tag from the [EVEN enumeration set](https://gedcom.io/terms/v7/enumset-EVEN)
            entered by placing `Tag.` in front of the capitalized name from the set.
        date: A date entered through `Date`.
        phrase: A phrase entered through `Phrase`.
        notes: Notes entered through `Note`.
        sources: Citations entered through `SourceCitation`.
        no_ext: Optional substructures extending [NO tag](https://gedcom.io/terms/v7/NO)
            entered through `Extension`.

    See Also:
        `Date`
        `Extension`
        `Note`
        `Phrase`
        `SourceCitation`

    References:
        [GEDCOM EVEN enumeration set](https://gedcom.io/terms/v7/enumset-EVEN)
        [GEDCOM NO tag](https://gedcom.io/terms/v7/NO)

    > n NO <Enum>                                {1:1}  [g7:NO](https://gedcom.io/terms/v7/NO)
    >   +1 DATE <DatePeriod>                     {0:1}  [g7:NO-DATE](https://gedcom.io/terms/v7/NO-DATE)
    >      +2 PHRASE <Text>                      {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    >   +1 <<NOTE_STRUCTURE>>                    {0:M}
    >   +1 <<SOURCE_CITATION>>                   {0:M}
    """

    no: Tag = Tag.NONE
    date: DateType = None
    phrase: PhraseType = None
    notes: NoteType = None
    sources: SourCiteType = None
    no_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_enum(self.no, Even)
            and Checker.verify_not_empty(self.no)
            and Checker.verify_type(self.date, Date, no_list=True)
            and Checker.verify_type(self.phrase, Phrase, no_list=True)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_type(self.sources, SourceCitation)
            and Checker.verify_ext(Tag.NO, self.no_ext)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.string(lines, level, Tag.NO, self.no.value)
            lines = Tagger.structure(lines, level + 1, self.no_ext)
            lines = Tagger.structure(lines, level + 1, self.date)
            lines = Tagger.structure(lines, level + 2, self.phrase)
            lines = Tagger.structure(lines, level + 2, self.notes)
            lines = Tagger.structure(lines, level + 2, self.sources)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'NonEvent',
                ('    no = ', self.no, tabs, full, True),
                ('    date = ', self.date, tabs + 1, full, False),
                ('    phrase = ', self.phrase, tabs + 1, full, False),
                ('    notes = ', self.notes, tabs + 1, full, False),
                ('    sources = ', self.sources, tabs + 1, full, False),
                ('    no_ext = ', self.no_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


NoType = NonEvent | list[NonEvent] | None


class Submitter(NamedTuple):
    """Store, validate and disply a GEDCOM Submitter Record.

    Examples:

    Args:
        xref: A cross-reference identifier constructed with `genedata.build.submitter_xref`.
        name: A name associated with the record.
        address: An address entered through `Address`.
        phones: Phones entered through `Phone`.
        emails: Emails entered through `Email`.
        faxes: Fax numbers entered through `Fax`.
        wwws: Internet sites entered through `WWW`.
        multimedia_links: Multimedia links entered through `MultimediaLink`.
        languages: Languages entered through `Lang`.
        identifiers: Identifiers entered through `Identifier`.
        notes: Notes entered through `Note`.
        change: A change date entered through `ChangeDate`.
        creation: A creation date entered through `CreationDate`.
        name_ext: Optional substructures extending [NAME tag](https://gedcom.io/terms/v7/NAME)
            entered through `Extension`.


    See Also:
        `Address`
        `ChangeDate`
        `CreationDate`
        `Email`
        `Extension`
        `Fax`
        `genedata.build.submitter_xref`
        `Identifier`
        `Lang`
        `MultimediaLink`
        `Note`
        `Phone`
        `WWW`

    Reference:
        [GEDCOM NAME tag](https://gedcom.io/terms/v7/NAME)
        [GEDCOM record-SUBM](https://gedcom.io/terms/v7/record-SUBM)
        [GEDCOM specification](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SUBMITTER_RECORD)

    > n @XREF:SUBM@ SUBM                         {1:1}  [g7:record-SUBM](https://gedcom.io/terms/v7/record-SUBM)
    >   +1 NAME <Text>                           {1:1}  [g7:NAME](https://gedcom.io/terms/v7/NAME)
    >   +1 <<ADDRESS_STRUCTURE>>                 {0:1}
    >   +1 PHON <Special>                        {0:M}  [g7:PHON](https://gedcom.io/terms/v7/PHON)
    >   +1 EMAIL <Special>                       {0:M}  [g7:EMAIL](https://gedcom.io/terms/v7/EMAIL)
    >   +1 FAX <Special>                         {0:M}  [g7:FAX](https://gedcom.io/terms/v7/FAX)
    >   +1 WWW <Special>                         {0:M}  [g7:WWW](https://gedcom.io/terms/v7/WWW)
    >   +1 <<MULTIMEDIA_LINK>>                   {0:M}
    >   +1 LANG <Language>                       {0:M}  [g7:SUBM-LANG](https://gedcom.io/terms/v7/SUBM-LANG)
    >   +1 <<IDENTIFIER_STRUCTURE>>              {0:M}
    >   +1 <<NOTE_STRUCTURE>>                    {0:M}
    >   +1 <<CHANGE_DATE>>                       {0:1}
    >   +1 <<CREATION_DATE>>                     {0:1}
    """

    xref: SubmitterXref = Void.SUBM
    name: str = Default.EMPTY
    address: AddrType = None
    phones: PhoneType = None
    emails: EmailType = None
    faxes: FaxType = None
    wwws: WWWType = None
    multimedia_links: MMLinkType = None
    languages: LangType = None
    identifiers: IdenType = None
    notes: NoteType = None
    change: ChangeDateType = None
    creation: CreationDateType = None
    name_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.xref, SubmitterXref, no_list=True)
            and Checker.verify_not_empty(self.xref)
            and Checker.verify_type(self.name, str, no_list=True)
            and Checker.verify_not_empty(self.name)
            and Checker.verify_type(self.address, Address, no_list=True)
            and Checker.verify_type(self.phones, Phone)
            and Checker.verify_type(self.emails, Email)
            and Checker.verify_type(self.faxes, Fax)
            and Checker.verify_type(self.wwws, WWW)
            and Checker.verify_type(self.multimedia_links, MultimediaLink)
            and Checker.verify_type(self.languages, Lang)
            and Checker.verify_type(self.identifiers, Identifier)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_type(self.change, ChangeDate, no_list=True)
            and Checker.verify_type(self.creation, CreationDate, no_list=True)
            and Checker.verify_ext(Tag.NAME, self.name_ext)
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        if self.validate():
            lines: str = self.xref.ged()
            lines = Tagger.string(lines, level + 1, Tag.NAME, self.name)
            lines = Tagger.structure(lines, level + 2, self.name_ext)
            lines = Tagger.structure(lines, level + 1, self.address)
            lines = Tagger.structure(lines, level + 1, self.phones)
            lines = Tagger.structure(lines, level + 1, self.emails)
            lines = Tagger.structure(lines, level + 1, self.faxes)
            lines = Tagger.structure(lines, level + 1, self.wwws)
            lines = Tagger.structure(lines, level + 1, self.multimedia_links)
            lines = Tagger.structure(lines, level + 1, self.languages)
            lines = Tagger.structure(lines, level + 1, self.identifiers)
            lines = Tagger.structure(lines, level + 1, self.notes)
            lines = Tagger.structure(lines, level + 1, self.change)
            lines = Tagger.structure(lines, level + 1, self.creation)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'Submitter',
                ('    xref = ', self.xref, tabs, full, True),
                ('    name = ', self.name, tabs, full, True),
                ('    address = ', self.address, tabs + 1, full, False),
                ('    phones = ', self.phones, tabs + 1, full, False),
                ('    emails = ', self.emails, tabs + 1, full, False),
                ('    faxes = ', self.faxes, tabs + 1, full, False),
                ('    wwws = ', self.wwws, tabs + 1, full, False),
                (
                    '    multimedia_links = ',
                    self.multimedia_links,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    languages = ', self.languages, tabs + 1, full, False),
                ('    identifiers = ', self.identifiers, tabs + 1, full, False),
                ('    notes = ', self.notes, tabs + 1, full, False),
                ('    change = ', self.change, tabs + 1, full, False),
                ('    creation = ', self.creation, tabs + 1, full, False),
                ('    name_ext = ', self.name_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


SubmType = Submitter | list[Submitter] | None


class Family(NamedTuple):
    """Store, validate and display a GEDCOM Family Record.

    Examples:

    Args:
        xref: A cross-reference identifier constructed by `genedata.build.family_xref`.
        resn: A tag from the [RESN enumeration set](https://gedcom.io/terms/v7/enumset-RESN)
            entered by placing `Tag.` in front of the capitalized name from the set.
        attributes: Family attributes enterd through `FamilyAttribute`.
        events: Events entered through `FamilyEvents`.
        husband: A cross-reference identifier for the husband constructed by `genedata.build.individual_xref`.
        husband_phrase: A phrase associated with the husband entered through `Phrase`.
        wife: A cross-reference identifier for the wife constructed by `genedata.build.individual_xref`.
        wife_phrase: A phrase associated with the wife entered through `Phrase`.
        children: Children entered through `ChildFamily`.
        associations: Associations entered through `Association`.
        submitters: Submitters entered through `Submitter`.
        lds_spouse_sealings: LDS spouse sealings entered through `LDSSpouseSealing`.
        identifiers: Indentifiers entered through `Identifier`.
        citations: Citations entered through `SourceCitation`.
        multimedia_links: Multimedia links entered through `MultimediaLink`.
        change: A change date entered through `ChangeDate`.
        creation: A creation date entered through `CreationDate`.
        resn_ext: Optional substructures extending [RESN tag](https://gedcom.io/terms/v7/RESN)
            entered through `Extension`.
        husb_ext: Optional substructures extending [HUSB tag](https://gedcom.io/terms/v7/HUSB)
            entered through `Extension`.
        wife_ext: Optional substructures extending [WIFE tag](https://gedcom.io/terms/v7/WIFE)
            entered through `Extension`.

    See Also:
        `Association`
        `ChangeDate`
        `ChildFamily`
        `CreationDate`
        `Extension`
        `FamilyAttribute`
        `genedata.build.family_xref`
        `Identifier`
        `LDSSpouseSealing`
        `MultimediaLink`
        `Phrase`
        `SourceCitation`
        `Submitter`


    Reference:
        [GEDCOM RESN enumeration set](https://gedcom.io/terms/v7/enumset-RESN)
        [GEDCOM HUSB tag](https://gedcom.io/terms/v7/HUSB)
        [GEDCOM WIFE tag](https://gedcom.io/terms/v7/WIFE)
        [GEDCOM record-FAM](https://gedcom.io/terms/v7/record-FAM)
        [GEDCOM specification](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_RECORD)

    > n @XREF:FAM@ FAM                           {1:1}  [g7:record-FAM](https://gedcom.io/terms/v7/record-FAM)
    >   +1 RESN <List:Enum>                      {0:1}  [g7:RESN](https://gedcom.io/terms/v7/RESN)
    >   +1 <<FAMILY_ATTRIBUTE_STRUCTURE>>        {0:M}
    >   +1 <<FAMILY_EVENT_STRUCTURE>>            {0:M}
    >   +1 <<NON_EVENT_STRUCTURE>>               {0:M}
    >   +1 HUSB @<XREF:INDI>@                    {0:1}  [g7:FAM-HUSB](https://gedcom.io/terms/v7/FAM-HUSB)
    >      +2 PHRASE <Text>                      {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    >   +1 WIFE @<XREF:INDI>@                    {0:1}  [g7:FAM-WIFE](https://gedcom.io/terms/v7/FAM-WIFE)
    >      +2 PHRASE <Text>                      {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    >   +1 CHIL @<XREF:INDI>@                    {0:M}  [g7:CHIL](https://gedcom.io/terms/v7/CHIL)
    >      +2 PHRASE <Text>                      {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    >   +1 <<ASSOCIATION_STRUCTURE>>             {0:M}
    >   +1 SUBM @<XREF:SUBM>@                    {0:M}  [g7:SUBM](https://gedcom.io/terms/v7/SUBM)
    >   +1 <<LDS_SPOUSE_SEALING>>                {0:M}
    >   +1 <<IDENTIFIER_STRUCTURE>>              {0:M}
    >   +1 <<NOTE_STRUCTURE>>                    {0:M}
    >   +1 <<SOURCE_CITATION>>                   {0:M}
    >   +1 <<MULTIMEDIA_LINK>>                   {0:M}
    >   +1 <<CHANGE_DATE>>                       {0:1}
    >   +1 <<CREATION_DATE>>                     {0:1}
    """

    xref: FamilyXref = Void.FAM
    resn: Tag = Tag.NONE
    attributes: FamAttrType = None
    events: FamEvenType = None
    husband: IndividualXref = Void.INDI
    husband_phrase: PhraseType = None
    wife: IndividualXref = Void.INDI
    wife_phrase: PhraseType = None
    children: ChilType = None
    associations: AssoType = None
    submitters: StrList = None
    lds_spouse_sealings: LDSSpouSealingType = None
    identifiers: IdenType = None
    notes: NoteType = None
    citations: SourCiteType = None
    multimedia_links: MMLinkType = None
    change: ChangeDateType = None
    creation: CreationDateType = None
    resn_ext: ExtType = None
    husb_ext: ExtType = None
    wife_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.xref, FamilyXref, no_list=True)
            and Checker.verify_not_empty(self.xref)
            and Checker.verify_enum(self.resn, Resn)
            and Checker.verify_type(self.attributes, FamilyAttribute)
            and Checker.verify_type(self.events, FamilyEvent)
            and Checker.verify_type(self.husband, IndividualXref, no_list=True)
            and Checker.verify_type(self.husband_phrase, Phrase, no_list=True)
            and Checker.verify_type(self.wife, IndividualXref, no_list=True)
            and Checker.verify_type(self.wife_phrase, Phrase, no_list=True)
            and Checker.verify_type(self.children, Child)
            and Checker.verify_type(self.associations, Association)
            and Checker.verify_type(self.submitters, SubmitterXref)
            and Checker.verify_type(self.lds_spouse_sealings, LDSSpouseSealing)
            and Checker.verify_type(self.identifiers, Identifier)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_type(self.citations, SourceCitation)
            and Checker.verify_type(self.multimedia_links, MultimediaLink)
            and Checker.verify_type(self.change, ChangeDate, no_list=True)
            and Checker.verify_type(self.creation, CreationDate, no_list=True)
            and Checker.verify_ext(Tag.RESN, self.resn_ext)
            and Checker.verify_ext(Tag.HUSB, self.husb_ext)
            and Checker.verify_ext(Tag.WIFE, self.wife_ext)
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged()
        if self.validate():
            if self.resn != Tag.NONE:
                lines = Tagger.string(lines, level, Tag.RESN, self.resn.value)
                lines = Tagger.structure(lines, level + 1, self.resn_ext)
            lines = Tagger.structure(lines, level, self.attributes)
            lines = Tagger.structure(lines, level, self.events)
            if str(self.husband) != str(Void.INDI):
                lines = Tagger.string(
                    lines, level + 1, Tag.HUSB, str(self.husband), format=False
                )
                lines = Tagger.structure(lines, level + 2, self.husb_ext)
                lines = Tagger.structure(lines, level + 2, self.husband_phrase)
            if str(self.wife) != str(Void.INDI):
                lines = Tagger.string(
                    lines, level + 1, Tag.WIFE, str(self.wife), format=False
                )
                lines = Tagger.structure(lines, level + 2, self.wife_ext)
                lines = Tagger.structure(lines, level + 2, self.wife_phrase)
            lines = Tagger.structure(lines, level + 1, self.children)
            lines = Tagger.structure(lines, level + 1, self.associations)
            lines = Tagger.string(
                lines, level, Tag.SUBM, self.submitters, format=False
            )
            lines = Tagger.structure(lines, level + 1, self.lds_spouse_sealings)
            lines = Tagger.structure(lines, level + 1, self.identifiers)
            lines = Tagger.structure(lines, level + 1, self.notes)
            lines = Tagger.structure(lines, level + 1, self.citations)
            lines = Tagger.structure(lines, level + 1, self.multimedia_links)
            lines = Tagger.structure(lines, level + 1, self.change)
            lines = Tagger.structure(lines, level + 1, self.creation)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'Family',
                ('    xref = ', self.xref, tabs, full, True),
                ('    resn = ', self.resn, tabs, full, False),
                ('    attributes = ', self.attributes, tabs + 1, full, False),
                ('    events = ', self.events, tabs + 1, full, False),
                ('    husband = ', self.husband, tabs, full, False),
                (
                    '    husband_phrase = ',
                    self.husband_phrase,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    wife = ', self.wife, tabs, full, False),
                ('    wife_phrase = ', self.wife_phrase, tabs + 1, full, False),
                ('    children = ', self.children, tabs + 1, full, False),
                (
                    '    associations = ',
                    self.associations,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    submitters = ', self.submitters, tabs + 1, full, False),
                (
                    '    lds_spouse_sealings = ',
                    self.lds_spouse_sealings,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    identifiers = ', self.identifiers, tabs + 1, full, False),
                ('    notes = ', self.notes, tabs + 1, full, False),
                ('    citations = ', self.citations, tabs + 1, full, False),
                (
                    '    multimedia_links = ',
                    self.multimedia_links,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    change = ', self.change, tabs + 1, full, False),
                ('    creation = ', self.creation, tabs + 1, full, False),
                ('    resn_ext = ', self.husb_ext, tabs, full, False),
                ('    husb_ext = ', self.husb_ext, tabs, full, False),
                ('    wife_ext = ', self.wife_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


FamType = Family | list[Family] | None


class Multimedia(NamedTuple):
    """Store, validate and display a GECDOM Multimedia Record.

    Examples:

    Args:
        xref: A multimedia cross-reference identifier constructed by `genedata.build.multimedia_xref`.
        resn: A tag from the [RESN enumeration set](https://gedcom.io/terms/v7/enumset-RESN)
            entered by placing `Tag.` in front of the capitalized name from the set.
        files: Files entered through `File`.
        identifiers: Identifiers entered through `Identifier`.
        notes: Notes entered through `Note`.
        sources: Citations entered through `SourceCitation`.
        change: A change date entered through `ChangeDate`.
        creation: A creation date entered through `CreationDate`.
        resn_ext: Optional substructures extending [RESN tag](https://gedcom.io/terms/v7/RESN)
            entered through `Extension`.


    See Also:
        `ChangeDate`
        `CreationDate`
        `Extension`
        `File`
        `Identifier`
        `genedata.build.multimedia_xref`
        `Note`
        `SourceCitation`

    Reference:
        [GEDCOM RESN enumeration set](https://gedcom.io/terms/v7/enumset-RESN)
        [GEDCOM RESN tag](https://gedcom.io/terms/v7/RESN)
        [GEDCOM record-OBJE](https://gedcom.io/terms/v7/record-OBJE)
        [GEDCOM specification](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#MULTIMEDIA_RECORD)

    > n @XREF:OBJE@ OBJE                         {1:1}  [g7:record-OBJE](https://gedcom.io/terms/v7/record-OBJE)
    >   +1 RESN <List:Enum>                      {0:1}  [g7:RESN](https://gedcom.io/terms/v7/RESN)
    >   +1 FILE <FilePath>                       {1:M}  [g7:FILE](https://gedcom.io/terms/v7/FILE)
    >      +2 FORM <MediaType>                   {1:1}  [g7:FORM](https://gedcom.io/terms/v7/FORM)
    >         +3 MEDI <Enum>                     {0:1}  [g7:MEDI](https://gedcom.io/terms/v7/MEDI)
    >            +4 PHRASE <Text>                {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    >      +2 TITL <Text>                        {0:1}  [g7:TITL](https://gedcom.io/terms/v7/TITL)
    >      +2 TRAN <FilePath>                    {0:M}  [g7:FILE-TRAN](https://gedcom.io/terms/v7/FILE-TRAN)
    >         +3 FORM <MediaType>                {1:1}  [g7:FORM](https://gedcom.io/terms/v7/FORM)
    >   +1 <<IDENTIFIER_STRUCTURE>>              {0:M}
    >   +1 <<NOTE_STRUCTURE>>                    {0:M}
    >   +1 <<SOURCE_CITATION>>                   {0:M}
    >   +1 <<CHANGE_DATE>>                       {0:1}
    >   +1 <<CREATION_DATE>>                     {0:1}
    """

    xref: MultimediaXref = Void.OBJE
    resn: Tag = Tag.NONE
    files: FileType = None
    identifiers: IdenType = None
    notes: NoteType = None
    sources: SourCiteType = None
    change: ChangeDateType = None
    creation: CreationDateType = None
    resn_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.xref, MultimediaXref, no_list=True)
            and Checker.verify_not_empty(self.xref)
            and Checker.verify_enum(self.resn, Resn)
            and Checker.verify_type(self.files, File)
            and Checker.verify_not_empty(self.files)
            and Checker.verify_type(self.identifiers, Identifier)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_type(self.sources, Source)
            and Checker.verify_type(self.change, ChangeDate, no_list=True)
            and Checker.verify_type(self.creation, CreationDate, no_list=True)
            and Checker.verify_ext(Tag.RESN, self.resn_ext)
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged()
        if self.validate():
            if self.resn != Tag.NONE:
                lines = Tagger.string(
                    lines, level + 1, Tag.RESN, self.resn.value
                )
                lines = Tagger.structure(lines, level + 1, self.resn_ext)
            lines = Tagger.structure(lines, level + 1, self.files)
            lines = Tagger.structure(lines, level + 1, self.identifiers)
            lines = Tagger.structure(lines, level + 1, self.notes)
            lines = Tagger.structure(lines, level + 1, self.sources)
            lines = Tagger.structure(lines, level + 1, self.change)
            lines = Tagger.structure(lines, level + 1, self.creation)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'Multimedia',
                ('    xref = ', self.xref, tabs, full, True),
                ('    resn = ', self.resn, tabs, full, False),
                ('    files = ', self.files, tabs + 1, full, True),
                ('    identifiers = ', self.identifiers, tabs + 1, full, False),
                ('    notes = ', self.notes, tabs + 1, full, False),
                ('    sources = ', self.sources, tabs + 1, full, False),
                ('    change = ', self.change, tabs + 1, full, False),
                ('    creation = ', self.creation, tabs + 1, full, False),
                ('    resn_ext = ', self.resn_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


ObjeType = Multimedia | list[Multimedia] | None


class Source(NamedTuple):
    """Store, validate and display a GEDCOM Source Record.

    Examples:

    Args:
        xref: A source cross-reference identifier constructed by `genedata.build.source_xref`.
        source_data_events: Source data events entered through `SourceDataEvent`.
        agency: The name of the agency associated with the source.
        data_notes: Notes entered through `Note`.
        author: The name of the author of the source.
        title: The title of the source.
        abbreviation: An abbreviation for the source.
        published: Publication information for the source.
        text: Text of the source entered through `Text`.
        repositories: Repository citations entered thrugh `SourceRepositoryCitation`.
        identifiers: Identifiers entered through `Identifier`.
        notes: Notes entered through `Note`.
        multimedia_links: Multimedia links entered through `MultimediaLink`.
        change: A change date entered through `ChangeDate`.
        creation: A creation date entered through `CreationDate`.
        data_ext: Optional substructures extending [DATA tag](https://gedcom.io/terms/v7/DATA)
            entered through `Extension`.
        agnc_ext: Optional substructures extending [AGNC tag](https://gedcom.io/terms/v7/AGNC)
            entered through `Extension`.
        auth_ext: Optional substructures extending [AUTH tag](https://gedcom.io/terms/v7/AUTH)
            entered through `Extension`.
        titl_ext: Optional substructures extending [TITL tag](https://gedcom.io/terms/v7/TITL)
            entered through `Extension`.
        abbr_ext: Optional substructures extending [ABBR tag](https://gedcom.io/terms/v7/ABBR)
            entered through `Extension`.
        publ_ext: Optional substructures extending [PUBL tag](https://gedcom.io/terms/v7/PUBL)
            entered through `Extension`.

    See Also:
        `ChangeDate`
        `CreationDate`
        `Extension`
        `Identifier`
        `MultimediaLink`
        `Note`
        `SourceDataEvent`
        `SourceRepositoryCitation`
        `Text`

    Reference:
        [GEDCOM ABBR tag](https://gedcom.io/terms/v7/ABBR)
        [GEDCOM AGNC tag](https://gedcom.io/terms/v7/AGNC)
        [GEDCOM AUTH tag](https://gedcom.io/terms/v7/AUTH)
        [GEDCOM DATA tag](https://gedcom.io/terms/v7/DATA)
        [GEDCOM PUBL tag](https://gedcom.io/terms/v7/PUBL)
        [GEDCOM TITL tag](https://gedcom.io/terms/v7/TITL)
        [GEDCOM record-SOUR](https://gedcom.io/terms/v7/record-SOUR)
        [GEDCOM specification](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_RECORD)

    > n @XREF:SOUR@ SOUR                         {1:1}  [g7:record-SOUR](https://gedcom.io/terms/v7/record-SOUR)
    >   +1 DATA                                  {0:1}  [g7:DATA]()
    >      +2 EVEN <List:Enum>                   {0:M}  [g7:DATA-EVEN]()
    >         +3 DATE <DatePeriod>               {0:1}  [g7:DATA-EVEN-DATE]()
    >            +4 PHRASE <Text>                {0:1}  [g7:PHRASE]()
    >         +3 <<PLACE_STRUCTURE>>             {0:1}
    >      +2 AGNC <Text>                        {0:1}  [g7:AGNC]()
    >      +2 <<NOTE_STRUCTURE>>                 {0:M}
    >   +1 AUTH <Text>                           {0:1}  [g7:AUTH]()
    >   +1 TITL <Text>                           {0:1}  [g7:TITL]()
    >   +1 ABBR <Text>                           {0:1}  [g7:ABBR]()
    >   +1 PUBL <Text>                           {0:1}  [g7:PUBL]()
    >   +1 TEXT <Text>                           {0:1}  [g7:TEXT]()
    >      +2 MIME <MediaType>                   {0:1}  [g7:MIME]()
    >      +2 LANG <Language>                    {0:1}  [g7:LANG]()
    >   +1 <<SOURCE_REPOSITORY_CITATION>>        {0:M}
    >   +1 <<IDENTIFIER_STRUCTURE>>              {0:M}
    >   +1 <<NOTE_STRUCTURE>>                    {0:M}
    >   +1 <<MULTIMEDIA_LINK>>                   {0:M}
    >   +1 <<CHANGE_DATE>>                       {0:1}
    >   +1 <<CREATION_DATE>>                     {0:1}
    """

    xref: SourceXref = Void.SOUR
    source_data_events: SourDataEvenType = None
    agency: str = Default.EMPTY
    data_notes: NoteType = None
    author: str = Default.EMPTY
    title: str = Default.EMPTY
    abbreviation: str = Default.EMPTY
    published: str = Default.EMPTY
    text: TextType = None
    repositories: SourRepoCiteType = None
    identifiers: IdenType = None
    notes: NoteType = None
    multimedia_links: MMLinkType = None
    change: ChangeDateType = None
    creation: CreationDateType = None
    data_ext: ExtType = None
    agnc_ext: ExtType = None
    auth_ext: ExtType = None
    titl_ext: ExtType = None
    abbr_ext: ExtType = None
    publ_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.xref, SourceXref)
            and Checker.verify_not_empty(self.xref)
            and Checker.verify_type(self.author, str, no_list=True)
            and Checker.verify_type(self.title, str, no_list=True)
            and Checker.verify_type(self.abbreviation, str, no_list=True)
            and Checker.verify_type(self.published, str, no_list=True)
            and Checker.verify_type(self.text, Text, no_list=True)
            and Checker.verify_type(self.repositories, Repository)
            and Checker.verify_type(self.identifiers, Identifier)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_type(self.multimedia_links, MultimediaLink)
            and Checker.verify_type(self.change, ChangeDate, no_list=True)
            and Checker.verify_type(self.creation, CreationDate, no_list=True)
            and Checker.verify_ext(Tag.DATA, self.data_ext)
            and Checker.verify_ext(Tag.AGNC, self.agnc_ext)
            and Checker.verify_ext(Tag.AUTH, self.auth_ext)
            and Checker.verify_ext(Tag.TITL, self.titl_ext)
            and Checker.verify_ext(Tag.ABBR, self.abbr_ext)
            and Checker.verify_ext(Tag.PUBL, self.publ_ext)
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged()
        if self.validate():
            if (
                self.source_data_events is not None
                or self.agency != Default.EMPTY
                or self.notes is not None
            ):
                lines = Tagger.empty(lines, level + 1, Tag.DATA)
                lines = Tagger.structure(lines, level + 2, self.data_ext)
                lines = Tagger.structure(
                    lines, level + 2, self.source_data_events
                )
                lines = Tagger.string(lines, level + 2, Tag.AGNC, self.agency)
                lines = Tagger.structure(lines, level + 3, self.agnc_ext)
                lines = Tagger.structure(lines, level + 1, self.notes)
            lines = Tagger.string(lines, level + 1, Tag.AUTH, self.author)
            lines = Tagger.structure(lines, level + 2, self.auth_ext)
            lines = Tagger.string(lines, level + 1, Tag.TITL, self.title)
            lines = Tagger.structure(lines, level + 2, self.titl_ext)
            lines = Tagger.string(lines, level + 1, Tag.ABBR, self.abbreviation)
            lines = Tagger.structure(lines, level + 2, self.abbr_ext)
            lines = Tagger.string(lines, level + 1, Tag.PUBL, self.published)
            lines = Tagger.structure(lines, level + 2, self.publ_ext)
            lines = Tagger.structure(lines, level + 1, self.text)
            lines = Tagger.structure(lines, level + 1, self.repositories)
            lines = Tagger.structure(lines, level + 1, self.identifiers)
            lines = Tagger.structure(lines, level + 1, self.notes)
            lines = Tagger.structure(lines, level + 1, self.multimedia_links)
            lines = Tagger.structure(lines, level + 1, self.change)
            lines = Tagger.structure(lines, level + 1, self.creation)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'Source',
                ('    xref = ', self.xref, tabs, full, True),
                (
                    '    source_data_events = ',
                    self.source_data_events,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    agency = ', self.agency, tabs, full, False),
                ('    data_notes = ', self.data_notes, tabs + 1, full, False),
                ('    author = ', self.author, tabs, full, False),
                ('    title = ', self.title, tabs, full, False),
                ('    abbreviation = ', self.abbreviation, tabs, full, False),
                ('    published = ', self.published, tabs, full, False),
                ('    text = ', self.text, tabs + 1, full, False),
                (
                    '    repositories = ',
                    self.repositories,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    identifiers = ', self.identifiers, tabs + 1, full, False),
                ('    notes = ', self.notes, tabs + 1, full, False),
                (
                    '    multimedia_links = ',
                    self.multimedia_links,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    change = ', self.change, tabs + 1, full, False),
                ('    creation = ', self.creation, tabs + 1, full, False),
                ('    data_ext = ', self.data_ext, tabs, full, False),
                ('    agnc_ext = ', self.agnc_ext, tabs, full, False),
                ('    auth_ext = ', self.auth_ext, tabs, full, False),
                ('    titl_ext = ', self.titl_ext, tabs, full, False),
                ('    abbr_ext = ', self.abbr_ext, tabs, full, False),
                ('    publ_ext = ', self.publ_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


SourType = Source | list[Source] | None


class Individual(NamedTuple):
    """Store, validate and display the record-INDI GEDCOM structure.

    Examples:
        The GEDCOM specification offers the following example.

        > The following example refers to 2 individuals, `@I1@` and `@I2@`, where `@I2@`
        > is a godparent of `@I1@`:
        >
        > ```gedcom
        > 0 @I1@ INDI
        > 1 ASSO @I2@
        > 2 ROLE GODP
        > ```

        This can be implemented by doing the following.
        First import the packages.
        >>> from genedata.build import Genealogy
        >>> from genedata.store import Association, Individual
        >>> from genedata.gedcom import Role

        Next instantiate a Genealogy which will store the information.
        This will be named `test`.
        >>> a = Genealogy('test')

        Next instantiate two IndivdiaulXref values called `I1` and `I2`.
        >>> i1 = a.individual_xref('I1')
        >>> i2 = a.individual_xref('I2')

        Add values to the Individual NamedTuple to store this information.
        >>> indi = Individual(
        ...     xref=i1,
        ...     associations=[
        ...         Association(
        ...             individual_xref=i2,
        ...             role=Tag.GODP,
        ...         ),
        ...     ],
        ... )

        At this point one could validate the information that is stored
        although this is not necessary since the validation occurs when
        one displays the data.  However, it is available for these
        structure.
        >>> indi.validate()
        True

        Next, we could display the data to verify that it is the same as
        the example shows.  Note that the data is the same although it
        is formatted as a single line with newlines.
        >>> indi.ged(0)
        '0 @I1@ INDI\\n1 ASSO @I2@\\n2 ROLE GODP\\n'

        Using `print` will format the result as in the example.  The additional
        blankline allows the final string to concatenate with additional data.
        >>> print(indi.ged(0))
        0 @I1@ INDI
        1 ASSO @I2@
        2 ROLE GODP
        <BLANKLINE>

        This example shows the kinds of errors that the validate method
        might produce by using a family xref for the individual xref.
        If one has doubts about the data one has loaded into a structure
        one can run its `validate` method to catch an error early on.
        >>> fam = a.family_xref('my family')
        >>> indi_error = Individual(xref=fam)
        >>> indi_error.validate()
        Traceback (most recent call last):
        TypeError: "@MY_FAMILY@" has type <class 'genedata.store.FamilyXref'> but should have type <class 'genedata.store.IndividualXref'>.

    Args:
        xref: An individual cross-reference identifier constructed by `genedata.build.individual_xref`.
        resn: A tag from the [RESN enumeration set](https://gedcom.io/terms/v7/enumset-RESN)
            entered by placing `Tag.` in front of the capitalized name from the set.
        personal_names: Personal names entered through `PersonalName`.
        sex: A tag from the [SEX enumeration set](https://gedcom.io/terms/v7/enumset-SEX)
            entered by placing `Tag.` in front of the capitalized name from the set.
        attributes: Individual attributes entered through `IndividualAttribute`.
        events: Individual events entered through `IndividualEvent`.
        lds_individual_ordinances: LDS individual ordinances entered through `LDSIndividualOrdinance`.
        families_child: Families in the individual is a child entered through `FamilyChild`.
        submitters: Submitters entered through `Submitter`.
        associations: Associations entered through `Association`.
        aliases: Aliases entered through `Alias`.
        ancestor_interest: Submitters interested in ancestors of the individual entered through `Submitter`.
        descendent_interest: Submitters interested in the descendents of the individual entered through `Submitter`.
        identifiers: Identifiers entered through `Identifier`.
        notes: Notes entered through `Note`.
        sources: Citations entered through `SourceCitations`.
        multimedia_links: Multimedia links entered through `MultimediaLink`.
        change: A change date entered through `ChangeDate`.
        creation: A creation date entered through `CreationDate`.
        resn_ext: Optional substructures extending [RESN tag](https://gedcom.io/terms/v7/RESN)
            entered through `Extension`.
        sex_ext: Optional substructures extending [SEX tag](https://gedcom.io/terms/v7/SEX)
            entered through `Extension`.

    See Also:
        `Alias`
        `Association`
        `ChangeDate`
        `CreationDate`
        `Extension`
        `FamilyChild`
        `genedata.build.individual_xref`
        `Identifier`
        `IndividualAttribute`
        `IndividualEvent`
        `LDSIndividualOrdinances`
        `MultimediaLink`
        `Note`
        `PersonalName`
        `SourceCitation`
        `Submitter`

    Reference:
        [GEDCOM RESN enumeration set](https://gedcom.io/terms/v7/enumset-RESN)
        [GEDCOM SEX enumeration set](https://gedcom.io/terms/v7/enumset-SEX)
        [GEDCOM RESN tag](https://gedcom.io/terms/v7/RESN)
        [GEDCOM SEX tag](https://gedcom.io/terms/v7/SEX)
        [GEDCOM record-INDI](https://gedcom.io/terms/v7/record-INDI)
        [GEDCOM specification](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_RECORD)


    > n @XREF:INDI@ INDI                         {1:1}  [g7:record-INDI](https://gedcom.io/terms/v7/record-INDI)
    >   +1 RESN <List:Enum>                      {0:1}  [g7:RESN](https://gedcom.io/terms/v7/RESN)
    >   +1 <<PERSONAL_NAME_STRUCTURE>>           {0:M}
    >   +1 SEX <Enum>                            {0:1}  [g7:SEX](https://gedcom.io/terms/v7/SEX)
    >   +1 <<INDIVIDUAL_ATTRIBUTE_STRUCTURE>>    {0:M}
    >   +1 <<INDIVIDUAL_EVENT_STRUCTURE>>        {0:M}
    >   +1 <<NON_EVENT_STRUCTURE>>               {0:M}
    >   +1 <<LDS_INDIVIDUAL_ORDINANCE>>          {0:M}
    >   +1 FAMC @<XREF:FAM>@                     {0:M}  [g7:INDI-FAMC](https://gedcom.io/terms/v7/INDI-FAMC)
    >      +2 PEDI <Enum>                        {0:1}  [g7:PEDI](https://gedcom.io/terms/v7/PEDI)
    >         +3 PHRASE <Text>                   {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    >      +2 STAT <Enum>                        {0:1}  [g7:FAMC-STAT](https://gedcom.io/terms/v7/FAMC-STAT)
    >         +3 PHRASE <Text>                   {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    >      +2 <<NOTE_STRUCTURE>>                 {0:M}
    >   +1 FAMS @<XREF:FAM>@                     {0:M}  [g7:FAMS](https://gedcom.io/terms/v7/FAMS)
    >      +2 <<NOTE_STRUCTURE>>                 {0:M}
    >   +1 SUBM @<XREF:SUBM>@                    {0:M}  [g7:SUBM](https://gedcom.io/terms/v7/SUBM)
    >   +1 <<ASSOCIATION_STRUCTURE>>             {0:M}
    >   +1 ALIA @<XREF:INDI>@                    {0:M}  [g7:ALIA](https://gedcom.io/terms/v7/ALIA)
    >      +2 PHRASE <Text>                      {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    >   +1 ANCI @<XREF:SUBM>@                    {0:M}  [g7:ANCI](https://gedcom.io/terms/v7/ANCI)
    >   +1 DESI @<XREF:SUBM>@                    {0:M}  [g7:DESI](https://gedcom.io/terms/v7/DESI)
    >   +1 <<IDENTIFIER_STRUCTURE>>              {0:M}
    >   +1 <<NOTE_STRUCTURE>>                    {0:M}
    >   +1 <<SOURCE_CITATION>>                   {0:M}
    >   +1 <<MULTIMEDIA_LINK>>                   {0:M}
    >   +1 <<CHANGE_DATE>>                       {0:1}
    >   +1 <<CREATION_DATE>>                     {0:1}
    """

    xref: IndividualXref = Void.INDI
    resn: Tag = Tag.NONE
    personal_names: PersonalNameType = None
    sex: Tag = Tag.NONE
    attributes: IndiAttrType = None
    events: IndiEvenType = None
    lds_individual_ordinances: list[LDSIndividualOrdinance] | None = None
    families_child: FamcType = None
    submitters: SubmType = None
    associations: AssoType = None
    aliases: AliaType = None
    ancestor_interest: SubmType = None
    descendent_interest: SubmType = None
    identifiers: IdenType = None
    notes: NoteType = None
    sources: StrList = None
    multimedia_links: MMLinkType = None
    change: ChangeDateType = None
    creation: CreationDateType = None
    resn_ext: ExtType = None
    sex_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.xref, IndividualXref, no_list=True)
            and Checker.verify_not_empty(self.xref)
            and Checker.verify_enum(self.resn, Resn)
            and Checker.verify_type(self.personal_names, PersonalName)
            and Checker.verify_enum(self.sex, Sex)
            and Checker.verify_type(self.attributes, IndividualAttribute)
            and Checker.verify_type(self.events, IndividualEvent)
            and Checker.verify_type(
                self.lds_individual_ordinances, LDSIndividualOrdinance
            )
            and Checker.verify_type(self.families_child, FamilyChild)
            and Checker.verify_type(self.submitters, Submitter)
            and Checker.verify_type(self.associations, Association)
            and Checker.verify_type(self.aliases, Alias)
            and Checker.verify_type(self.ancestor_interest, Submitter)
            and Checker.verify_type(self.descendent_interest, Submitter)
            and Checker.verify_type(self.identifiers, Identifier)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_type(self.sources, Source)
            and Checker.verify_type(self.multimedia_links, MultimediaLink)
            and Checker.verify_type(self.change, ChangeDate, no_list=True)
            and Checker.verify_type(self.creation, CreationDate, no_list=True)
            and Checker.verify_ext(Tag.RESN, self.resn_ext)
            and Checker.verify_ext(Tag.SEX, self.sex_ext)
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged()
        if self.validate():
            lines = Tagger.string(lines, level + 1, Tag.RESN, self.resn.value)
            lines = Tagger.structure(lines, level + 2, self.resn_ext)
            lines = Tagger.structure(lines, level + 1, self.personal_names)
            lines = Tagger.string(lines, level + 1, Tag.SEX, self.sex.value)
            lines = Tagger.structure(lines, level + 2, self.sex_ext)
            lines = Tagger.structure(lines, level + 1, self.attributes)
            lines = Tagger.structure(lines, level + 1, self.events)
            lines = Tagger.structure(
                lines, level + 1, self.lds_individual_ordinances
            )
            lines = Tagger.structure(lines, level + 1, self.families_child)
            lines = Tagger.structure(lines, level + 1, self.submitters)
            lines = Tagger.structure(lines, level + 1, self.associations)
            lines = Tagger.structure(lines, level + 1, self.aliases)
            lines = Tagger.structure(lines, level + 1, self.ancestor_interest)
            lines = Tagger.structure(lines, level + 1, self.descendent_interest)
            lines = Tagger.structure(lines, level + 1, self.identifiers)
            lines = Tagger.structure(lines, level + 1, self.notes)
            lines = Tagger.structure(lines, level + 1, self.sources)
            lines = Tagger.structure(lines, level + 1, self.multimedia_links)
            lines = Tagger.structure(lines, level + 1, self.change)
            lines = Tagger.structure(lines, level + 1, self.creation)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'Individual',
                ('    xref = ', self.xref, tabs, full, True),
                ('    resn = ', self.resn, tabs, full, False),
                (
                    '    personal_names = ',
                    self.personal_names,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    sex = ', self.sex, tabs, full, False),
                ('    attributes = ', self.attributes, tabs + 1, full, False),
                ('    events = ', self.events, tabs + 1, full, False),
                (
                    '    lds_individual_ordinances = ',
                    self.lds_individual_ordinances,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    submitters = ', self.submitters, tabs + 1, full, False),
                (
                    '    associations = ',
                    self.associations,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    aliases = ', self.aliases, tabs + 1, full, False),
                (
                    '    ancestor_interest = ',
                    self.ancestor_interest,
                    tabs + 1,
                    full,
                    False,
                ),
                (
                    '    descendent_interest = ',
                    self.descendent_interest,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    identifiers = ', self.identifiers, tabs + 1, full, False),
                ('    notes = ', self.notes, tabs + 1, full, False),
                ('    sources = ', self.sources, tabs + 1, full, False),
                (
                    '    multimedia_links = ',
                    self.multimedia_links,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    change = ', self.change, tabs + 1, full, False),
                ('    creation = ', self.creation, tabs + 1, full, False),
                ('    resn_ext = ', self.resn_ext, tabs, full, False),
                ('    sex_ext = ', self.sex_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


class Repository(NamedTuple):
    """Store, validate and display the record-INDI GEDCOM structure.

    Examples:

    Args:
        xref: A repository cross-reference identifier constructed by `genedata.build.repository_xref`.
        name: The name of the repository.
        address: The address of the repository entered through `Address`.
        phones: Phones entered through `Phone`.
        emails: Emails entered through `Email`.
        faxes: Fax numbers entered through `Fax`.
        wwws: Internet addresses entered through `WWW`.
        notes: Notes entered through `Note`.
        identifiers: Identifiers entered through `Identifier`.
        change: A change date entered through `ChangeDate`.
        creation: A creation date entered through `CreationDate`.
        name_ext: Optional substructures extending [NAME tag](https://gedcom.io/terms/v7/NAME)
            entered through `Extension`.


    See Also:
        `Extension`

    Reference:
        [GEDCOM NAME tag](https://gedcom.io/terms/v7/NAME)
        [GEDCOM Repository](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#REPOSITORY_RECORD)

    > n @XREF:REPO@ REPO                         {1:1}  [g7:record-REPO](https://gedcom.io/terms/v7/record-REPO)
    >   +1 NAME <Text>                           {1:1}  [g7:NAME](https://gedcom.io/terms/v7/NAME)
    >   +1 <<ADDRESS_STRUCTURE>>                 {0:1}
    >   +1 PHON <Special>                        {0:M}  [g7:PHON](https://gedcom.io/terms/v7/PHON)
    >   +1 EMAIL <Special>                       {0:M}  [g7:EMAIL](https://gedcom.io/terms/v7/EMAIL)
    >   +1 FAX <Special>                         {0:M}  [g7:FAX](https://gedcom.io/terms/v7/FAX)
    >   +1 WWW <Special>                         {0:M}  [g7:WWW](https://gedcom.io/terms/v7/WWW)
    >   +1 <<NOTE_STRUCTURE>>                    {0:M}
    >   +1 <<IDENTIFIER_STRUCTURE>>              {0:M}
    >   +1 <<CHANGE_DATE>>                       {0:1}
    >   +1 <<CREATION_DATE>>                     {0:1}
    """

    xref: RepositoryXref = Void.REPO
    name: str = Default.EMPTY
    address: AddrType = None
    phones: PhoneType = None
    emails: EmailType = None
    faxes: FaxType = None
    wwws: WWWType = None
    notes: NoteType = None
    identifiers: IdenType = None
    change: ChangeDateType = None
    creation: CreationDateType = None
    name_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.xref, RepositoryXref, no_list=True)
            and Checker.verify_not_empty(self.xref)
            and Checker.verify_type(self.name, str, no_list=True)
            and Checker.verify_not_empty(self.name)
            and Checker.verify_type(self.address, Address, no_list=True)
            and Checker.verify_type(self.phones, Phone)
            and Checker.verify_type(self.emails, Email)
            and Checker.verify_type(self.faxes, Fax)
            and Checker.verify_type(self.wwws, WWW)
            and Checker.verify_type(self.notes, Note)
            and Checker.verify_type(self.identifiers, Identifier)
            and Checker.verify_type(self.change, ChangeDate, no_list=True)
            and Checker.verify_type(self.creation, CreationDate, no_list=True)
            and Checker.verify_ext(Tag.RESN, self.name_ext)
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged()
        if self.validate():
            lines = Tagger.string(lines, level + 1, Tag.NAME, self.name)
            lines = Tagger.structure(lines, level + 1, self.name_ext)
            lines = Tagger.structure(lines, level + 1, self.address)
            lines = Tagger.structure(lines, level + 1, self.phones)
            lines = Tagger.structure(lines, level + 1, self.emails)
            lines = Tagger.structure(lines, level + 1, self.faxes)
            lines = Tagger.structure(lines, level + 1, self.wwws)
            lines = Tagger.structure(lines, level + 1, self.change)
            lines = Tagger.structure(lines, level + 1, self.creation)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'Repository',
                ('    xref = ', self.xref, tabs, full, True),
                ('    name = ', self.name, tabs, full, True),
                ('    address = ', self.address, tabs + 1, full, False),
                ('    phones = ', self.phones, tabs + 1, full, False),
                ('    emails = ', self.emails, tabs + 1, full, False),
                ('    faxes = ', self.faxes, tabs + 1, full, False),
                ('    wwws = ', self.wwws, tabs + 1, full, False),
                ('    notes = ', self.notes, tabs + 1, full, False),
                ('    identifiers = ', self.identifiers, tabs + 1, full, False),
                ('    change = ', self.change, tabs + 1, full, False),
                ('    creation = ', self.creation, tabs + 1, full, False),
                ('    name_ext = ', self.name_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


class SharedNote(NamedTuple):
    """Store, validate and display a GEDCOM Shared Note Record.

    Examples:

    Args:
        xref: A shared note cross-reference identifier constructed with `genedata.build.shared_note_xref`.
        text: The text of the shared note.
        mime: The mime type of the shared note.
        language: The language of the shared note entered through `Lang`.
        translations: Translations of the shared note entered through `NoteTranslation`.
        sources: Citations of the shared note entered through `SourceCitation`.
        identifiers: Identifiers of the shared note entered through `Identifier`.
        change: A change date entered through `ChangeDate`.
        creation: A creation date entered through `CreationDate`.
        snote_ext: Optional substructures extending [SNOTE tag](https://gedcom.io/terms/v7/SNOTE)
            entered through `Extension`.
        mime_ext: Optional substructures extending [MIME tag](https://gedcom.io/terms/v7/MIME)
            entered through `Extension`.


    See Also:
        `ChangeDate`
        `CreationDate`
        `Extension`
        `genedata.build.shared_note_xref`
        `Identifier`
        `Lang`
        `NoteTranslation`
        `SourceCitation`

    Reference:
        [GEDCOM MIME tag](https://gedcom.io/terms/v7/MIME)
        [GEDCOM SNOTE tag](https://gedcom.io/terms/v7/SNOTE)
        [GEDCOM Shared Note Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SHARED_NOTE_RECORD)

    > n @XREF:SNOTE@ SNOTE <Text>                {1:1}  g7:record-SNOTE
    >   +1 MIME <MediaType>                      {0:1}  g7:MIME
    >   +1 LANG <Language>                       {0:1}  g7:LANG
    >   +1 TRAN <Text>                           {0:M}  g7:NOTE-TRAN
    >      +2 MIME <MediaType>                   {0:1}  g7:MIME
    >      +2 LANG <Language>                    {0:1}  g7:LANG
    >   +1 <<SOURCE_CITATION>>                   {0:M}
    >   +1 <<IDENTIFIER_STRUCTURE>>              {0:M}
    >   +1 <<CHANGE_DATE>>                       {0:1}
    >   +1 <<CREATION_DATE>>                     {0:1}
    """

    xref: SharedNoteXref
    text: str = Default.EMPTY
    mime: str = Default.MIME
    language: LangType = None
    translations: NoteTranType = None
    sources: SourCiteType = None
    identifiers: IdenType = None
    change: ChangeDateType = None
    creation: CreationDateType = None
    snote_ext: ExtType = None
    mime_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.xref, SharedNoteXref, no_list=True)
            and Checker.verify_not_empty(self.xref)
            and Checker.verify_type(self.text, str, no_list=True)
            and Checker.verify_not_empty(self.text)
            and Checker.verify_type(self.mime, str, no_list=True)
            and Checker.verify_type(self.language, Lang, no_list=True)
            and Checker.verify_type(self.translations, NoteTranslation)
            and Checker.verify_type(self.sources, Source)
            and Checker.verify_type(self.identifiers, Identifier)
            and Checker.verify_type(self.change, ChangeDate, no_list=True)
            and Checker.verify_type(self.creation, CreationDate, no_list=True)
            and Checker.verify_ext(Tag.SNOTE, self.snote_ext)
            and Checker.verify_ext(Tag.MIME, self.mime_ext)
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged(self.text)
        if self.validate():
            lines = Tagger.string(lines, level + 1, Tag.MIME, self.mime)
            lines = Tagger.structure(lines, level + 2, self.mime_ext)
            lines = Tagger.structure(lines, level + 1, self.language)
            lines = Tagger.structure(lines, level + 1, self.translations)
            lines = Tagger.structure(lines, level + 1, self.sources)
            lines = Tagger.structure(lines, level + 1, self.identifiers)
            lines = Tagger.structure(lines, level + 1, self.change)
            lines = Tagger.structure(lines, level + 1, self.creation)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'SharedNote',
                ('    xref = ', self.xref, tabs, full, True),
                ('    text = ', self.text, tabs, full, True),
                ('    mime = ', self.mime, tabs, full, False),
                ('    language = ', self.language, tabs + 1, full, False),
                (
                    '    translations = ',
                    self.translations,
                    tabs + 1,
                    full,
                    False,
                ),
                ('    sources = ', self.sources, tabs + 1, full, False),
                ('    identifiers = ', self.identifiers, tabs + 1, full, False),
                ('    change = ', self.change, tabs + 1, full, False),
                ('    creation = ', self.creation, tabs + 1, full, False),
                ('    snote_ext = ', self.snote_ext, tabs, full, False),
                ('    mime_ext = ', self.mime_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )


class Header(NamedTuple):
    """Hold data for the GEDCOM header special record.

    Examples:

    Args:
        exttags: Extension tag definitions entered through `ExtTag`.
        source: The source name for the genealogy.
        vers: The version of the genealogy.
        name: The name of the genealogy.
        corporation: The corporation associated with the genealogy.
        address: The address entered by `Address`.
        phones: Phones entered by `Phone`.
        emails: Emails entered by `Email`.
        faxes: Fax numbers entered by `Fax`.
        wwws: Internet addresses entered by `WWW`
        data: Data entry.
        data_date: Date of the data entered by `Date`.
        data_time: Time of the data entered by `Time`.
        data_copyright: Copyright information of the data.
        dest: Destination of the genealogy.
        header_date: The date of the header entered by `Date`.
        header_time: The time of the header entered by `Time`.
        submitter: The submitter of the genealogy entered by `Submitter`.
        subm_copyright: The submitter copyright of the genealogy.
        language: The language of the genalogy entered by `Lang`.
        note: Notes entered by `Note`.
        head_ext: Optional substructures extending [HEAD tag](https://gedcom.io/terms/v7/HEAD)
            entered through `Extension`.
        gedc_ext: Optional substructures extending [GEDC tag](https://gedcom.io/terms/v7/GEDC)
            entered through `Extension`.
        vers_ext: Optional substructures extending [VERS tag](https://gedcom.io/terms/v7/VERS)
            entered through `Extension`.
        dest_ext: Optional substructures extending [DEST tag](https://gedcom.io/terms/v7/DEST)
            entered through `Extension`.
        subm_ext: Optional substructures extending [SUBM tag](https://gedcom.io/terms/v7/SUBM)
            entered through `Extension`.
        copr_ext: Optional substructures extending [COPR tag](https://gedcom.io/terms/v7/COPR)
            entered through `Extension`.

    See Also:
        `Address`
        `Date`
        `Email`
        `Extension`
        `ExtTag`
        `Fax`
        `Lang`
        `Note`
        `Phone`
        `Submitter`
        `Time`
        `WWW`

    Reference:
        [GEDCOM COPR tag](https://gedcom.io/terms/v7/COPR)
        [GEDCOM DEST tag](https://gedcom.io/terms/v7/DEST)
        [GEDCOM GEDC tag](https://gedcom.io/terms/v7/GEDC)
        [GEDCOM HEAD tag](https://gedcom.io/terms/v7/HEAD)
        [GEDCOM VERS tag](https://gedcom.io/terms/v7/VERS)
        [GEDCOM SUBM tag](https://gedcom.io/terms/v7/SUBM)
        [GEDCOM Header](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#HEADER)

    >n HEAD                                     {1:1}  [g7:HEAD](https://gedcom.io/terms/v7/HEAD)
    >  +1 GEDC                                  {1:1}  [g7:GEDC](https://gedcom.io/terms/v7/GEDC)
    >     +2 VERS <Special>                     {1:1}  [g7:GEDC-VERS](https://gedcom.io/terms/v7/GEDC-VERS)
    >  +1 SCHMA                                 {0:1}  [g7:SCHMA](https://gedcom.io/terms/v7/SCHMA)
    >     +2 TAG <Special>                      {0:M}  [g7:TAG](https://gedcom.io/terms/v7/TAG)
    >  +1 SOUR <Special>                        {0:1}  [g7:HEAD-SOUR](https://gedcom.io/terms/v7/HEAD-SOUR)
    >     +2 VERS <Special>                     {0:1}  [g7:VERS](https://gedcom.io/terms/v7/VERS)
    >     +2 NAME <Text>                        {0:1}  [g7:NAME](https://gedcom.io/terms/v7/NAME)
    >     +2 CORP <Text>                        {0:1}  [g7:CORP](https://gedcom.io/terms/v7/CORP)
    >        +3 <<ADDRESS_STRUCTURE>>           {0:1}
    >        +3 PHON <Special>                  {0:M}  [g7:PHON](https://gedcom.io/terms/v7/PHON)
    >        +3 EMAIL <Special>                 {0:M}  [g7:EMAIL](https://gedcom.io/terms/v7/EMAIL)
    >        +3 FAX <Special>                   {0:M}  [g7:FAX](https://gedcom.io/terms/v7/FAX)
    >        +3 WWW <Special>                   {0:M}  [g7:WWW](https://gedcom.io/terms/v7/WWW)
    >     +2 DATA <Text>                        {0:1}  [g7:HEAD-SOUR-DATA](https://gedcom.io/terms/v7/HEAD-SOUR-DATA)
    >        +3 DATE <DateExact>                {0:1}  [g7:DATE-exact](https://gedcom.io/terms/v7/DATE-exact)
    >           +4 TIME <Time>                  {0:1}  [g7:TIME](https://gedcom.io/terms/v7/TIME)
    >        +3 COPR <Text>                     {0:1}  [g7:COPR](https://gedcom.io/terms/v7/COPR)
    >  +1 DEST <Special>                        {0:1}  [g7:DEST](https://gedcom.io/terms/v7/DEST)
    >  +1 DATE <DateExact>                      {0:1}  [g7:HEAD-DATE](https://gedcom.io/terms/v7/HEAD-DATE)
    >     +2 TIME <Time>                        {0:1}  [g7:TIME](https://gedcom.io/terms/v7/TIME)
    >  +1 SUBM @<XREF:SUBM>@                    {0:1}  [g7:SUBM](https://gedcom.io/terms/v7/SUBM)
    >  +1 COPR <Text>                           {0:1}  [g7:COPR](https://gedcom.io/terms/v7/COPR)
    >  +1 LANG <Language>                       {0:1}  [g7:HEAD-LANG](https://gedcom.io/terms/v7/LANG)
    >  +1 PLAC                                  {0:1}  [g7:HEAD-PLAC](https://gedcom.io/terms/v7/PLAC)
    >     +2 FORM <List:Text>                   {1:1}  [g7:HEAD-PLAC-FORM](https://gedcom.io/terms/v7/PLAC-FORM)
    >  +1 <<NOTE_STRUCTURE>>                    {0:1}
    """

    exttags: ExtTagType = None
    source: str = Default.EMPTY
    vers: str = Default.EMPTY
    name: str = Default.EMPTY
    corporation: str = Default.EMPTY
    address: AddrType = None
    phones: PhoneType = None
    emails: EmailType = None
    faxes: FaxType = None
    wwws: WWWType = None
    data: str = Default.EMPTY
    data_date: DateType = None
    data_time: TimeType = None
    data_copyright: str = Default.EMPTY
    dest: str = Default.EMPTY
    header_date: DateType = None
    header_time: TimeType = None
    submitter: SubmitterXref = Void.SUBM
    subm_copyright: str = Default.EMPTY
    language: LangType = None
    note: NoteType = None
    head_ext: ExtType = None
    gedc_ext: ExtType = None
    vers_ext: ExtType = None
    dest_ext: ExtType = None
    subm_ext: ExtType = None
    copr_ext: ExtType = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Checker.verify_type(self.exttags, ExtTag)
            and Checker.verify_type(self.source, str, no_list=True)
            and Checker.verify_type(self.vers, str, no_list=True)
            and Checker.verify_type(self.name, str, no_list=True)
            and Checker.verify_type(self.corporation, str, no_list=True)
            and Checker.verify_type(self.address, Address, no_list=True)
            and Checker.verify_type(self.phones, Phone)
            and Checker.verify_type(self.emails, Email)
            and Checker.verify_type(self.faxes, Fax)
            and Checker.verify_type(self.wwws, WWW)
            and Checker.verify_type(self.data, str, no_list=True)
            and Checker.verify_type(self.data_date, Date, no_list=True)
            and Checker.verify_type(self.data_time, Time, no_list=True)
            and Checker.verify_type(self.data_copyright, str, no_list=True)
            and Checker.verify_type(self.dest, str, no_list=True)
            and Checker.verify_type(self.header_date, Date, no_list=True)
            and Checker.verify_type(self.header_time, Time, no_list=True)
            and Checker.verify_type(self.submitter, SubmitterXref, no_list=True)
            and Checker.verify_type(self.subm_copyright, str, no_list=True)
            and Checker.verify_type(self.language, Lang, no_list=True)
            and Checker.verify_type(self.note, Note, no_list=True)
            and Checker.verify_ext(Tag.HEAD, self.head_ext)
            and Checker.verify_ext(Tag.GEDC, self.gedc_ext)
            and Checker.verify_ext(Tag.VERS, self.vers_ext)
            and Checker.verify_ext(Tag.DEST, self.dest_ext)
            and Checker.verify_ext(Tag.SUBM, self.subm_ext)
            and Checker.verify_ext(Tag.COPR, self.copr_ext)
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Tagger.empty(lines, level, Tag.HEAD)
            lines = Tagger.structure(lines, level + 1, self.head_ext)
            lines = Tagger.empty(lines, level + 1, Tag.GEDC)
            lines = Tagger.structure(lines, level + 2, self.gedc_ext)
            lines = Tagger.string(lines, level + 2, Tag.VERS, Config.GEDVERSION)
            lines = Tagger.structure(lines, level + 3, self.vers_ext)
            if self.exttags is not None and (
                (isinstance(self.exttags, list) and len(self.exttags) > 0)
                or isinstance(self.exttags, ExtTag)
            ):
                lines = Tagger.empty(lines, level + 1, Tag.SCHMA)
                lines = Tagger.structure(lines, level + 1, self.exttags)
            lines = Tagger.structure(lines, level + 2, self.address)
            lines = Tagger.structure(lines, level + 3, self.phones)
            lines = Tagger.structure(lines, level + 3, self.emails)
            lines = Tagger.structure(lines, level + 3, self.faxes)
            lines = Tagger.structure(lines, level + 3, self.wwws)
            if self.data != Default.EMPTY:
                lines = Tagger.string(lines, level + 2, Tag.DATA, self.data)
                lines = Tagger.structure(lines, level + 3, self.data_date)
                lines = Tagger.structure(lines, level + 4, self.data_time)
                lines = Tagger.string(
                    lines, level + 3, Tag.COPR, self.data_copyright
                )
            lines = Tagger.string(lines, level, Tag.DEST, self.dest)
            lines = Tagger.structure(lines, level + 1, self.dest_ext)
            lines = Tagger.structure(lines, level + 1, self.header_date)
            lines = Tagger.structure(lines, level + 2, self.header_time)
            if self.submitter != Void.SUBM:
                lines = Tagger.string(
                    lines,
                    level + 1,
                    Tag.SUBM,
                    self.submitter.fullname,
                    format=False,
                )
                lines = Tagger.structure(lines, level + 2, self.subm_ext)
            lines = Tagger.string(
                lines, level + 1, Tag.COPR, self.subm_copyright
            )
            lines = Tagger.structure(lines, level + 2, self.copr_ext)
            lines = Tagger.structure(lines, level + 1, self.language)
            lines = Tagger.structure(lines, level + 1, self.note)
        return lines

    def code(self, tabs: int = 1, full: bool = False) -> str:
        return indent(
            Formatter.display_code(
                'Header',
                ('    exttags = ', self.exttags, tabs + 1, full, False),
                ('    source = ', self.source, tabs, full, False),
                ('    vers = ', self.vers, tabs, full, False),
                ('    name = ', self.name, tabs, full, False),
                ('    corporation = ', self.corporation, tabs, full, False),
                ('    address = ', self.address, tabs + 1, full, False),
                ('    phones = ', self.phones, tabs + 1, full, False),
                ('    emails = ', self.emails, tabs + 1, full, False),
                ('    faxes = ', self.faxes, tabs + 1, full, False),
                ('    wwws = ', self.wwws, tabs + 1, full, False),
                ('    data = ', self.data, tabs, full, False),
                ('    data_date = ', self.data_date, tabs + 1, full, False),
                ('    data_time = ', self.data_time, tabs + 1, full, False),
                ('    submitter = ', self.submitter, tabs, full, False),
                (
                    '    subm_copyright = ',
                    self.subm_copyright,
                    tabs,
                    full,
                    False,
                ),
                ('    language = ', self.language, tabs + 1, full, False),
                ('    note = ', self.note, tabs + 1, full, False),
                ('    head_ext = ', self.head_ext, tabs, full, False),
                ('    gedc_ext = ', self.gedc_ext, tabs, full, False),
                ('    vers_ext = ', self.vers_ext, tabs, full, False),
                ('    dest_ext = ', self.dest_ext, tabs, full, False),
                ('    subm_ext = ', self.subm_ext, tabs, full, False),
                ('    copr_ext = ', self.copr_ext, tabs, full, False),
            ),
            Default.INDENT * tabs,
        )
