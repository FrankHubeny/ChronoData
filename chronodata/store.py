# chronodata/tuples.py
# Licensed under a 3-clause BSD style license - see LICENSE.md
"""NamedTuples to store, validate and display data
entered by the user for a chronology.

The NamedTuples are based on the GEDCOM standard with others
added to aid the user in collecting the data.

Each of the NamedTuples have two methods:
    validate: Return True if the data can be used or
        an error message otherwise.
    ged: Display the data in the GEDCOM format.

Examples:


"""

__all__ = [
    'Family',
    'Individual',
    'Multimedia',
    'Repository',
    'SharedNote',
    'Source',
    'Submitter',
]

import logging
from textwrap import dedent, indent
from typing import Any, Literal, NamedTuple

from chronodata.constants import Cal, String, Value
from chronodata.enums import (
    Adop,
    Event,
    FamAttr,
    # FamcStat,
    FamEven,
    GreaterLessThan,
    Id,
    IndiAttr,
    IndiEven,
    Latitude,
    Longitude,
    Media,
    MediaType,
    NameType,
    Quay,
    Resn,
    Role,
    Sex,
    Stat,
    Tag,
)
from chronodata.messages import Msg
from chronodata.methods import DefCheck, DefTag
from chronodata.records import (
    FamilyXref,
    IndividualXref,
    MultimediaXref,
    RepositoryXref,
    SharedNoteXref,
    SourceXref,
    SubmitterXref,
    Void,
)


class Address(NamedTuple):
    """Store, validate and format address information to be saved to a ged file.

    Example:
        The following is the minimum amount of information for an address.
        >>> from chronodata.store import Address
        >>> mailing_address = Address(
        ...     ['12345 ABC Street', 'South North City, My State 22222'],
        ... )
        >>> mailing_address.validate()
        True
        >>> print(mailing_address.ged(1))
        1 ADDR 12345 ABC Street
        1 CONT South North City, My State 22222
        <BLANKLINE>

        There are five named strings stored in this NamedTuple.
        >>> from chronodata.store import Address
        >>> full_address = Address(
        ...     ['12345 ABC Street', 'South North City, My State 23456'],
        ...     'South North City',
        ...     'My State',
        ...     '23456',
        ...     'USA',
        ... )
        >>> print(full_address.ged(1))
        1 ADDR 12345 ABC Street
        1 CONT South North City, My State 23456
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

    Returns:
        A string displaying stored Address data formatted to GEDCOM specifications.

    Reference:
        [GEDCOM Specifications](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#substructures)

    > n ADDR <Special>                           {1:1}  [g7:ADDR](https://gedcom.io/terms/v7/ADDR)
    >   +1 ADR1 <Special>                        {0:1}  [g7:ADR1](https://gedcom.io/terms/v7/ADR1)
    >   +1 ADR2 <Special>                        {0:1}  [g7:ADR2](https://gedcom.io/terms/v7/ADR2)
    >   +1 ADR3 <Special>                        {0:1}  [g7:ADR3](https://gedcom.io/terms/v7/ADR3)
    >   +1 CITY <Special>                        {0:1}  [g7:CITY](https://gedcom.io/terms/v7/CITY)
    >   +1 STAE <Special>                        {0:1}  [g7:STAE](https://gedcom.io/terms/v7/STAE)
    >   +1 POST <Special>                        {0:1}  [g7:POST](https://gedcom.io/terms/v7/POST)
    >   +1 CTRY <Special>                        {0:1}  [g7:CTRY](https://gedcom.io/terms/v7/CTRY)
    """

    address: list[str] = []  # noqa: RUF012
    city: str = ''
    state: str = ''
    postal: str = ''
    country: str = ''

    def validate(self) -> bool:
        check: bool = (
            DefCheck.verify_tuple_type(self.address, str)
            and DefCheck.verify_type(self.city, str)
            and DefCheck.verify_type(self.state, str)
            and DefCheck.verify_type(self.postal, str)
            and DefCheck.verify_type(self.country, str)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            if len(self.address) > 0:
                lines = DefTag.taginfo(level, Tag.ADDR, self.address[0])
                for line in self.address[1:]:
                    lines = DefTag.str_to_str(lines, level, Tag.CONT, line)
            lines = DefTag.str_to_str(lines, level + 1, Tag.CITY, self.city)
            lines = DefTag.str_to_str(lines, level + 1, Tag.STAE, self.state)
            lines = DefTag.str_to_str(lines, level + 1, Tag.POST, self.postal)
            lines = DefTag.str_to_str(lines, level + 1, Tag.CTRY, self.country)
        return lines


class Age(NamedTuple):
    """Implement the Age data type in the GEDCOM specification.

    The GEDCOM specification requires that these age components be
    rounded down. The `phrase` parameter allows the user to
    add information about the data provided.

    Examples:
        >>> from chronodata.store import Age
        >>> from chronodata.constants import String
        >>> print(
        ...     Age(
        ...         10,
        ...         greater_less_than='>',
        ...         phrase='Estimated',
        ...     ).ged(1)
        ... )
        1 AGE > 10y
        2 PHRASE Estimated
        <BLANKLINE>
        >>> print(Age(10, 2, 1, 2, '').ged(2))
        2 AGE 10y 2m 1w 2d
        <BLANKLINE>

    Args:
        greater_less_than: The default is '', which means that the age is exact
            to the day.  The option `>` means that the actual age
            is greater than the one provided.  The option `<` means
            that the actual age is less than the one provided.
        years: The number of whole years in the age.
        months: The number of months in addition to the years.
        weeks: The number of weeks in addition to the years and months.
        days: The number of days in addition to any years, months, or weeks provided.
        phrase: Addition information to clarify the data added.

    Returns:
        A GEDCOM string storing this data.

    Exceptions:
        ValueError: If greater_less_than is not one of {'', '<', '>'}.
        ValueError: If any value (except `phrase`) is not an integer.
        ValueError: If any value (except `phrase`) is less than 0.

    Reference:
        [GEDCOM Specification](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#age)
    """

    years: int = 0
    months: int = 0
    weeks: int = 0
    days: int = 0
    greater_less_than: str = '>'
    phrase: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_enum(self.greater_less_than, GreaterLessThan)
            and DefCheck.verify_type(self.years, int)
            and DefCheck.verify_type(self.months, int)
            and DefCheck.verify_type(self.weeks, int)
            and DefCheck.verify_type(self.days, int)
            and DefCheck.verify_type(self.phrase, str)
            and DefCheck.verify_not_negative(self.years)
            and DefCheck.verify_not_negative(self.months)
            and DefCheck.verify_not_negative(self.weeks)
            and DefCheck.verify_not_negative(self.days)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format the GEDCOM Age data type."""
        line: str = ''
        info: str = self.greater_less_than
        if self.validate():
            if self.years > 0:
                info = ''.join([info, f' {self.years!s}y'])
            if self.months > 0:
                info = ''.join([info, f' {self.months!s}m'])
            if self.weeks > 0:
                info = ''.join([info, f' {self.weeks!s}w'])
            if self.days > 0:
                info = ''.join([info, f' {self.days!s}d'])
            line = DefTag.taginfo(
                level,
                Tag.AGE,
                info.replace('  ', ' ').replace('  ', ' ').strip(),
            )
            if self.phrase != '':
                line = ''.join(
                    [line, DefTag.taginfo(level + 1, Tag.PHRASE, self.phrase)]
                )
        return line


class PersonalNamePieces(NamedTuple):
    """Store, validate and display values for an optional GEDCOM Personal Name Piece.

    Example:
        This example includes all six of the Personal Name Piece tags.
        >>> from chronodata.store import PersonalNamePieces  # doctest: +ELLIPSIS
        >>> from chronodata.enums import Tag

    Args:
        prefix: An option list of NPFX or name prefixes of the name.
        given: An optional list of GIVN or given names of the name.
        nickname: An optional list of NICK or nicknames for the name.
        surname_prefix: An optional list of SPFX or surname prefixes of the name.
        surname: An optional list of SURN or surnames or last names of the name.
        suffix: An optional list NSFX or name suffixes of the name.

    Returns:
        A GEDCOM string storing this data.

    Reference:
        [GEDCOM Personal Name Pieces](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PERSONAL_NAME_PIECES)

    > n NPFX <Text>                              {0:M}  [g7:NPFX](https://gedcom.io/terms/v7/NPFX)
    > n GIVN <Text>                              {0:M}  [g7:GIVN](https://gedcom.io/terms/v7/GIVN)
    > n NICK <Text>                              {0:M}  [g7:NICK](https://gedcom.io/terms/v7/NICK)
    > n SPFX <Text>                              {0:M}  [g7:SPFX](https://gedcom.io/terms/v7/SPFX)
    > n SURN <Text>                              {0:M}  [g7:SURN](https://gedcom.io/terms/v7/SURN)
    > n NSFX <Text>                              {0:M}  [g7:NSFX](https://gedcom.io/terms/v7/NSFX)
    """

    prefix: list[str] = []  # noqa: RUF012
    given: list[str] = []  # noqa: RUF012
    nickname: list[str] = []  # noqa: RUF012
    surname_prefix: list[str] = []  # noqa: RUF012
    surname: list[str] = []  # noqa: RUF012
    suffix: list[str] = []  # noqa: RUF012

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_tuple_type(self.prefix, str)
            and DefCheck.verify_tuple_type(self.given, str)
            and DefCheck.verify_tuple_type(self.nickname, str)
            and DefCheck.verify_tuple_type(self.surname_prefix, str)
            and DefCheck.verify_tuple_type(self.surname, str)
            and DefCheck.verify_tuple_type(self.suffix, str)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = DefTag.strlist_to_str(lines, level, Tag.NPFX, self.prefix)
            lines = DefTag.strlist_to_str(lines, level, Tag.GIVN, self.given)
            lines = DefTag.strlist_to_str(lines, level, Tag.NICK, self.nickname)
            lines = DefTag.strlist_to_str(
                lines, level, Tag.SPFX, self.surname_prefix
            )
            lines = DefTag.strlist_to_str(lines, level, Tag.SURN, self.surname)
            lines = DefTag.strlist_to_str(lines, level, Tag.NSFX, self.suffix)
        return lines


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
        >>> from chronodata.store import NameTranslation
        >>> joe_in_chinese = '喬'
        >>> language = 'cmn'
        >>> nt = NameTranslation(joe_in_chinese, language)
        >>> nt.validate()
        True
        >>> print(nt.ged(1))
        1 TRAN 喬
        2 LANG cmn
        <BLANKLINE>

    Args:
        translation: the text of the translation.
        language: the BCP 47 language tag.
        name_pieces: an optional tuple of PersonalNamePieces.

    Returns:
        A GEDCOM string storing this data.

    Reference:
        [GEDCOM Pesonal Name Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PERSONAL_NAME_STRUCTURE)
    """

    translation: str = String.EMPTY
    language: str = String.UNDETERMINED
    pieces: PersonalNamePieces | None = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.translation, str)
            and DefCheck.verify_not_default(self.translation, '')
            and DefCheck.verify_type(self.pieces, PersonalNamePieces)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = DefTag.str_to_str(lines, level, Tag.TRAN, self.translation)
            lines = DefTag.str_to_str(lines, level + 1, Tag.LANG, self.language)
            if self.pieces is not None:
                lines = ''.join([lines, self.pieces.ged(level + 1)])
        return lines


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
        >>> from chronodata.store import NoteTranslation
        >>> from chronodata.enums import MediaType
        >>> arabic_text = 'هذه ملاحظة.'
        >>> mime = MediaType.TEXT_HTML
        >>> language = 'afb'
        >>> nt = NoteTranslation(arabic_text, mime, language)
        >>> nt.validate()
        True
        >>> print(nt.ged(1))
        1 TRAN هذه ملاحظة.
        2 MIME TEXT_HTML
        2 LANG afb
        <BLANKLINE>

    Args:
        translation: the text of the translation for the note.
        mime: the mime type of the translation.
        language: the BCP 47 language tag of the translation.

    Returns:
        A GEDCOM string storing this data.

    Reference:
        [W3C Internationalization](https://www.w3.org/International/questions/qa-choosing-language-tags)
        [Language Subtag Lookup Tool](https://r12a.github.io/app-subtags/)
        [GEDCOM Note Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#NOTE_STRUCTURE)]


    """

    translation: str = ''
    mime: MediaType = MediaType.NONE
    language: str = String.UNDETERMINED

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.translation, str)
            and DefCheck.verify_not_default(self.translation, '')
            and DefCheck.verify_enum(self.mime.value, MediaType)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = ''.join(
                [
                    lines,
                    DefTag.taginfo(level, Tag.TRAN, self.translation),
                    DefTag.taginfo(level + 1, Tag.MIME, self.mime.value),
                    DefTag.taginfo(level + 1, Tag.LANG, self.language),
                ]
            )
        return lines


class CallNumber(NamedTuple):
    """Store, validate and display the option call numbers for the
    SourceRepositoryCitation substructure.

    Example:
        This example assumes there is a call number "1111" which is the
        minimal amount of information needed to use this optional feature.
        >>> from chronodata.store import CallNumber
        >>> cn = CallNumber('1111')
        >>> cn.validate()
        True
        >>> print(cn.ged(1))
        1 CALN 1111
        <BLANKLINE>

        This next example uses all of the optional positions.
        >>> from chronodata.enums import Media
        >>> cn_all = CallNumber('1111', Media.BOOK, 'New Testament')
        >>> print(cn_all.ged(1))
        1 CALN 1111
        2 MEDI BOOK
        3 PHRASE New Testament
        <BLANKLINE>

    Args:


    Returns:
        A GEDCOM string storing this data.

    See Also:
        `SourceRepositoryCitation`: the superstructure of this NamedTuple.

    """

    call_number: str = ''
    media: Media = Media.NONE
    phrase: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.call_number, str)
            and DefCheck.verify_not_default(self.call_number, '')
            and DefCheck.verify_enum(self.media.value, Media)
            and DefCheck.verify_type(self.phrase, str)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = DefTag.taginfo(level, Tag.CALN, self.call_number)
            if self.media != Media.NONE:
                lines = ''.join(
                    [
                        lines,
                        DefTag.taginfo(level + 1, Tag.MEDI, self.media.value),
                    ]
                )
            if self.phrase != '':
                lines = ''.join(
                    [
                        lines,
                        DefTag.taginfo(level + 2, Tag.PHRASE, self.phrase),
                    ]
                )
        return lines


class SourceRepositoryCitation(NamedTuple):
    """Store, validate and display the optional Source Repository Citation
     substructure of the GEDCOM standard.

    Examples:

    Args:
        repo: the reference identifier for the repository.
        notes: a tuple of Notes.
        call_numbers: a tuple of call numbers.

    Returns:
        A GEDCOM string storing this data.

    Reference:
        [GEDCOM Source Repository Citation](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_REPOSITORY_CITATION)

    > n REPO @<XREF:REPO>@                       {1:1}  [g7:REPO](https://gedcom.io/terms/v7/REPO)
    >   +1 <<NOTE_STRUCTURE>>                    {0:M}
    >   +1 CALN <Special>                        {0:M}  [g7:CALN](https://gedcom.io/terms/v7/CALN)
    >      +2 MEDI <Enum>                        {0:1}  [g7:MEDI](https://gedcom.io/terms/v7/MEDI)
    >         +3 PHRASE <Text>                   {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    """

    repo: RepositoryXref
    notes: list[Any] = []  # noqa: RUF012
    call_numbers: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.repo, RepositoryXref)
            and DefCheck.verify_not_default(self.repo, Void.REPO)
            and DefCheck.verify_tuple_type(self.notes, Note)
            and DefCheck.verify_type(self.call_numbers, CallNumber)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = DefTag.taginfo(level, Tag.SOUR, str(self.repo))
            lines = DefTag.list_to_str(lines, level, self.notes)
            lines = DefTag.list_to_str(lines, level, self.call_numbers)
            # if self.notes is not None:
            #     for note in self.notes:
            #         lines = ''.join([lines, note.ged(level + 1)])
            # if self.call_numbers is not None:
            #     for call_number in self.call_numbers:
            #         lines = ''.join([lines, call_number.ged(level + 1)])
        return lines


class Text(NamedTuple):
    """_summary_

    The BCP 47 language tag is a hyphenated list of subtags.
    The [W3C Internationalization](https://www.w3.org/International/questions/qa-choosing-language-tags)
    guide will help one make a decision on which tags to use.
    The [Language Subtag Lookup Tool](https://r12a.github.io/app-subtags/)
    can assist with finding and checking the language tag one would like to use.

    Examples:

    Args:
        text: the text being added.
        mime: the media type of the text.
        language: the BCP 47 language tag for the text.

    Returns:
        A GEDCOM string storing this data.

    Reference:
        [W3C Internationalization](https://www.w3.org/International/questions/qa-choosing-language-tags)
        [Language Subtag Lookup Tool](https://r12a.github.io/app-subtags/)
    """

    text: str = ''
    mime: MediaType = MediaType.NONE
    language: str = String.UNDETERMINED


class SourceData(NamedTuple):
    """_summary_

    Examples:


    Args:
        date_value:
        texts: a list of texts associated with this source.

    Returns:
        A GEDCOM string storing this data.

    Reference:
        []()
    """

    date_value: str = ''
    texts: Any = None


class SourceCitation(NamedTuple):
    """Store, validate and display the Source Citation
    substructure of the GEDCOM standard.

    Examples:


    Args:
        xref: the source identifier
        page:

    Returns:
        A GEDCOM string storing this data.

    Reference:
        [GEDCOM Source Citation](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_CITATION)
    """

    xref: SourceXref = Void.SOUR
    page: str = ''
    texts: Any = None
    event: Event = Event.NONE
    phrase: str = ''
    role: Role = Role.NONE
    role_phrase: str = ''
    quality: Quay = Quay.NONE
    multimedia: Any = None
    notes: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_not_default(str(self.xref), Void.SOUR)
            and DefCheck.verify_type(self.xref, SourceXref)
            and DefCheck.verify_type(self.page, str)
            and DefCheck.verify_tuple_type(self.texts, Text)
            and DefCheck.verify_enum(self.event.value, Event)
            and DefCheck.verify_type(self.phrase, str)
            and DefCheck.verify_enum(self.role.value, Role)
            and DefCheck.verify_type(self.role_phrase, str)
            and DefCheck.verify_enum(self.quality.value, Quay)
            and DefCheck.verify_tuple_type(self.multimedia, MultimediaLink)
            and DefCheck.verify_tuple_type(self.notes, Note)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = DefTag.taginfo(level, Tag.SOUR, str(self.xref))
            if self.page != '':
                lines = DefTag.taginfo(level + 1, Tag.PAGE, self.page)

        return lines


class Note(NamedTuple):
    """Store, validate and display a note substructure of the GEDCOM standard.

    The BCP 47 language tag is a hyphenated list of subtags.
    The [W3C Internationalization](https://www.w3.org/International/questions/qa-choosing-language-tags)
    guide will help one make a decision on which tags to use.
    The [Language Subtag Lookup Tool](https://r12a.github.io/app-subtags/)
    can assist with finding and checking the language tag one would like to use.

    Example:
        This example is a note without other information.
        >>> from chronodata.store import Note
        >>> note = Note(note='This is my note.')
        >>> print(note.ged(1))
        1 NOTE This is my note.
        2 LANG und
        <BLANKLINE>

        This example uses the Hebrew language translating "This is my note." as "זו ההערה שלי."
        The translation comes from [Google Translate](https://translate.google.com/?sl=en&tl=iw&text=This%20is%20my%20note.&op=translate).
        >>> hebrew_note = Note(note='זו ההערה שלי.', language='he')
        >>> print(hebrew_note.ged(1))
        1 NOTE זו ההערה שלי.
        2 LANG he
        <BLANKLINE>

        The next example adds translations of the previous example to the note.
        >>> from chronodata.enums import MediaType
        >>> english_translation = NoteTranslation(
        ...     'This is my note.', MediaType.TEXT_PLAIN, 'en'
        ... )
        >>> urdu_translation = NoteTranslation(
        ...     'یہ میرا نوٹ ہے۔', MediaType.TEXT_PLAIN, 'ur'
        ... )
        >>> hebrew_note_with_translations = Note(
        ...     note='זו ההערה שלי.',
        ...     language='he',
        ...     translations=(
        ...         english_translation,
        ...         urdu_translation,
        ...     ),
        ... )
        >>> print(hebrew_note_with_translations.ged(1))
        1 NOTE זו ההערה שלי.
        2 LANG he
        2 TRAN This is my note.
        3 MIME TEXT_PLAIN
        3 LANG en
        2 TRAN یہ میرا نوٹ ہے۔
        3 MIME TEXT_PLAIN
        3 LANG ur
        <BLANKLINE>

    Args:
        text: the text of the note.
        mime: the optional media type of the note.
        language: the optional BCP 47 language tag for the note.
        translations: an optional tuple of translations of the text.
        citations: an optional tuple of translations of the text.

    Returns:
        A GEDCOM string storing this data.

    Reference:
        [W3C Internationalization](https://www.w3.org/International/questions/qa-choosing-language-tags)
        [Language Subtag Lookup Tool](https://r12a.github.io/app-subtags/)
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

    snote: SharedNoteXref | None = None
    note: str = String.EMPTY
    mime: MediaType = MediaType.NONE
    language: str = String.UNDETERMINED
    translations: list[NoteTranslation] = []  # noqa: RUF012
    source_citations: list[SourceCitation] = []  # noqa: RUF012

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.snote, SharedNoteXref | None)
            and DefCheck.verify_type(self.note, str)
            and DefCheck.verify_enum(self.mime.value, MediaType)
            and DefCheck.verify_tuple_type(self.translations, NoteTranslation)
            and DefCheck.verify_tuple_type(
                self.source_citations, SourceCitation
            )
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            if self.snote is not None:
                lines = DefTag.str_to_str(
                    lines, level, Tag.SNOTE, self.snote.fullname
                )
            else:
                lines = DefTag.str_to_str(lines, level, Tag.NOTE, self.note)
                lines = DefTag.str_to_str(
                    lines, level + 1, Tag.MIME, self.mime.value
                )
                lines = DefTag.str_to_str(
                    lines, level + 1, Tag.LANG, self.language
                )
                lines = DefTag.list_to_str(lines, level + 1, self.translations)
                lines = DefTag.list_to_str(
                    lines, level + 1, self.source_citations
                )
        return lines


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
        >>> from chronodata.store import (
        ...     NameTranslation,
        ...     Note,
        ...     PersonalName,
        ...     PersonalNamePieces,
        ...     SourceCitation,
        ... )
        >>> from chronodata.enums import NameType, PersonalNamePieceTag
        >>> adam_note = Note(note='Here is a place to add more information.')
        >>> adam_english = NameTranslation(
        ...     'Adam', 'en', PersonalNamePieces(nickname=['the man'])
        ... )
        >>> adam = PersonalName(
        ...     name='אָדָ֛ם',
        ...     type=NameType.OTHER,
        ...     phrase='The first man',
        ...     pieces=PersonalNamePieces(nickname=['הָֽאָדָ֖ם']),
        ...     translations=[adam_english],
        ...     notes=[adam_note],
        ... )
        >>> print(adam.ged(1))
        1 NAME אָדָ֛ם
        2 TYPE OTHER
        2 NICK הָֽאָדָ֖ם
        2 TRAN Adam
        3 LANG en
        3 NICK the man
        2 NOTE Here is a place to add more information.
        3 LANG und
        <BLANKLINE>

    Args:
        name: The full name of the person including the surname.
        surname: Repeat the part of the name that is the surname or last name of the person.
        type: the type of name. There are seven types to choose from:
            - NameType.AKA or also known as.
            - NameType.BIRTH or birth name.
            - NameType.IMMIGRANT or immigrant name.
            - NameType.MAIDEN or maiden name.
            - NameType.MARRIED or married name.
            - NameType.PROFESSIONAL or professional name
            - NameType.OTHER or another type not listed above.
        phrase: a place for uncategorized information about the name.
        pieces: an alternate way to split the name.
        translations: an optional tuple of translations of the name.
        notes: a tuple of optional notes regarding the name.
        sources: a tuple of citations regarding the name.

    Returns:
        A GEDCOM string storing this data.

    Reference:
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

    name: str = String.EMPTY
    surname: str = String.EMPTY
    type: Tag = Tag.NONE
    phrase: str = String.EMPTY
    pieces: PersonalNamePieces | None = None
    translations: list[NameTranslation] = []  # noqa: RUF012
    notes: list[Note] = []  # noqa: RUF012
    source_citations: list[SourceCitation] = []  # noqa: RUF012

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_not_default(self.name, '')
            and DefCheck.verify_type(self.name, str)
            and DefCheck.verify_type(self.surname, str)
            and DefCheck.verify_enum(self.type.value, NameType)
            and DefCheck.verify_type(self.phrase, str)
            and DefCheck.verify_type(self.pieces, PersonalNamePieces)
            and DefCheck.verify_tuple_type(self.translations, NameTranslation)
            and DefCheck.verify_tuple_type(self.notes, Note)
            and DefCheck.verify_tuple_type(
                self.source_citations, SourceCitation
            )
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = DefTag.str_to_str(lines, level, Tag.NAME, self.name)
            lines = DefTag.str_to_str(
                lines, level + 1, Tag.TYPE, self.type.value
            )
            # lines = ''.join(
            #     [
            #         DefTag.taginfo(level, Tag.NAME, self.name),
            #         DefTag.taginfo(level + 1, Tag.TYPE, self.type.value),
            #     ]
            # )
            if self.pieces is not None:
                lines = ''.join([lines, self.pieces.ged(level + 1)])
            # if self.translations is not None:
            #     for translation in self.translations:
            lines = DefTag.list_to_str(lines, level + 1, self.translations)
            lines = DefTag.list_to_str(lines, level + 1, self.notes)
            lines = DefTag.list_to_str(lines, level + 1, self.source_citations)
            # if self.notes is not None:
            #     for note in self.notes:
            #         lines = ''.join([lines, note.ged(level + 1)])
            # if self.source_citations is not None:
            #     for source in self.source_citations:
            #         lines = ''.join([lines, source.ged(level + 1)])
        return lines


class Association(NamedTuple):
    """Store, validate and display a GEDCOM Association structure.



    Examples:
        This example comes from the GEDCOM specification referenced below.
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
        >>> from chronodata.build import Chronology
        >>> from chronodata.enums import Role
        >>> from chronodata.store import Association, Individual

        Next, create a chronology and the two individuals references.
        There is no need to create an individual reference for Mr Stockdale
        so we leave his pointer as `@VOID@`.
        >>> chron = Chronology('test')
        >>> individual = chron.individual_xref('I', initial=True)
        >>> clergy = chron.individual_xref('I', initial=True)

        Next, create two associations, one for the individual and one for a baptism
        event.
        >>> individual_association = Association(
        ...     phrase='Mr Stockdale',
        ...     role=Role.OTHER,
        ...     role_phrase='Teacher',
        ... )
        >>> event_association = Association(xref=clergy, role=Role.CLERGY)

        Finally construct the individual record and display it.
        >>> indi = Individual(
        ...     xref=individual,
        ...     associations=[individual_association],
        ...     events=[
        ...         IndividualEvent(
        ...             tag=Tag.BAPM,
        ...             payload='',
        ...             event_detail=IndividualEventDetail(
        ...                 event_detail=EventDetail(
        ...                     date_value=DateValue(
        ...                         Date(year=1930),
        ...                     ),
        ...                     associations=[event_association],
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

    Args:
        xref: the identifier of the individual in this association.
        phrase: a description of the association.
        role: the role of this individual.
        role_phrase: a description of the role.
        notes: a collection of notes related to this association.
        citations: a collection of citations related to this association.

    Returns:
        A GEDCOM string storing this data.

    Reference:
        [GEDCOM Association Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#ASSOCIATION_STRUCTURE)
    """

    xref: IndividualXref = Void.INDI
    phrase: str = String.EMPTY
    role: Role = Role.NONE
    role_phrase: str = String.EMPTY
    notes: list[Note] = []  # noqa: RUF012
    citations: list[SourceCitation] = []  # noqa: RUF012

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.xref, IndividualXref)
            and DefCheck.verify_type(self.role, Role)
            # and DefCheck.verify_enum(self.role.value, Role)
            and DefCheck.verify_type(self.phrase, str)
            and DefCheck.verify_type(self.role_phrase, str)
            and DefCheck.verify_tuple_type(self.notes, Note)
            and DefCheck.verify_tuple_type(self.citations, SourceCitation)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            # if self.xref == '':
            #     lines = DefTag.str_to_str(lines, level, Tag.ASSO, Void.NAME)
            # else:
            lines = DefTag.str_to_str(lines, level, Tag.ASSO, str(self.xref))
            lines = DefTag.str_to_str(lines, level + 1, Tag.PHRASE, self.phrase)
            lines = DefTag.str_to_str(
                lines, level + 1, Tag.ROLE, self.role.value
            )
            lines = DefTag.str_to_str(
                lines, level + 2, Tag.PHRASE, self.role_phrase
            )
            lines = DefTag.list_to_str(lines, level + 1, self.notes)
            lines = DefTag.list_to_str(lines, level + 1, self.citations)
        return lines


class MultimediaLink(NamedTuple):
    """_summary_

    Examples:


    Args:
        NamedTuple (_type_): _description_

    Returns:
        A GEDCOM string storing this data.
    """

    crop: str = ''
    top: int = 0
    left: int = 0
    height: int = 0
    width: int = 0
    title: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.crop, str)
            and DefCheck.verify_type(self.top, int)
            and DefCheck.verify_type(self.left, int)
            and DefCheck.verify_type(self.height, int)
            and DefCheck.verify_type(self.width, int)
            and DefCheck.verify_type(self.title, str)
        )
        return check

    def ged(self, level: int = 1) -> str:
        lines: str = f'{level}'
        if self.validate():
            pass
        return lines


class Exid(NamedTuple):
    exid: str
    exid_type: str

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = DefCheck.verify_type(
            self.exid, str
        ) and DefCheck.verify_type(self.exid_type, str)
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        return ''.join(
            [
                DefTag.taginfo(level, Tag.EXID, self.exid),
                DefTag.taginfo(level + 1, Tag.TYPE, self.exid_type),
            ]
        )


class PlaceName(NamedTuple):
    """Store, validate and display a place translation.

    A place is a series of named jurisdictions associated with political,
    ecclesiastical or geographic regions.  They are listed in increasing order of size.
    These jurisdictions are assigned a name in the form arguments.
    By default, the jusisdictions are 'City', 'County', 'State' and
    'Country'.  Only four are available, but not all four need be used.

    For the translations the forms are the same as for the original language, but
    the names of the jurisdictions are translated into a different language.

    Examples:
    The first example takes advantage of the four form defaults.
    >>> chicago = PlaceName(
    ...     place1='Chicago',
    ...     place2='Cook County',
    ...     place3='Illinois',
    ...     place4='USA',
    ...     language='en',
    ... )
    >>> print(chicago.ged(1))
    1 PLAC Chicago, Cook County, Illinois, USA
    2 FORM City, County, State, Country
    2 LANG en
    <BLANKLINE>

    The second example adds in specific form values.
    >>> chicago = PlaceName(
    ...     place1='Chicago',
    ...     place2='Cook County',
    ...     place3='Illinois',
    ...     place4='USA',
    ...     form1='City2',
    ...     form2='County2',
    ...     form3='State2',
    ...     form4='Country2',
    ...     language='en',
    ... )
    >>> print(chicago.ged(1))
    1 PLAC Chicago, Cook County, Illinois, USA
    2 FORM City2, County2, State2, Country2
    2 LANG en
    <BLANKLINE>

    The third example uses only three of the four jurisdictions accepting
    the defaults for the unspecified values.
    >>> chicago = PlaceName(
    ...     place1='Chicago', place3='Illinois', place4='USA', language='en'
    ... )
    >>> print(chicago.ged(1))
    1 PLAC Chicago, , Illinois, USA
    2 FORM City, County, State, Country
    2 LANG en
    <BLANKLINE>

    Args:
        place1: The smallest region associated with a place, such as, the city.
        place2: The next region larger than `place1` associated with a place, such as, county.
        place3: The next region larger than `place2` associated with a place, such as, state.
        place4: The next region larger than `place3` associated with a place, such as, country.
        form1: The name of the `place1` region. (Default 'City')
        form2: The name of the `place2` region. (Default 'County')
        form3: The name of the `place3` region. (Default 'State')
        form4: The name of the `place4` region. (Default 'Country')
        language: The BCP 47 language tag for the langues of this information.

    Reference:
        [GEDCOM Place Translation](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PLAC-TRAN)
    """

    place1: str = String.EMPTY
    place2: str = String.EMPTY
    place3: str = String.EMPTY
    place4: str = String.EMPTY
    form1: str = String.FORM_DEFAULT1
    form2: str = String.FORM_DEFAULT2
    form3: str = String.FORM_DEFAULT3
    form4: str = String.FORM_DEFAULT4
    language: str = String.UNDETERMINED

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.place1, str)
            and DefCheck.verify_type(self.place2, str)
            and DefCheck.verify_type(self.place3, str)
            and DefCheck.verify_type(self.place4, str)
            and DefCheck.verify_type(self.form1, str)
            and DefCheck.verify_type(self.form2, str)
            and DefCheck.verify_type(self.form3, str)
            and DefCheck.verify_type(self.form4, str)
            and DefCheck.verify_type(self.language, str)
        )
        return check

    def ged(self, level: int = 1, style: str = String.PLACE_FULL) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            place: str = ''.join(
                [
                    self.place1,
                    ', ',
                    self.place2,
                    ', ',
                    self.place3,
                    ', ',
                    self.place4,
                ]
            )
            form: str = ''.join(
                [
                    self.form1,
                    ', ',
                    self.form2,
                    ', ',
                    self.form3,
                    ', ',
                    self.form4,
                ]
            )
            match style:
                case String.PLACE_FULL:
                    lines = DefTag.str_to_str(lines, level, Tag.PLAC, place)
                    lines = DefTag.str_to_str(lines, level + 1, Tag.FORM, form)
                    lines = DefTag.str_to_str(
                        lines, level + 1, Tag.LANG, self.language
                    )
                case String.PLACE_SHORT:
                    lines = DefTag.str_to_str(lines, level, Tag.PLAC, place)
                    lines = DefTag.str_to_str(lines, level + 1, Tag.FORM, form)
                case String.PLACE_TRANSLATION:
                    lines = DefTag.str_to_str(lines, level, Tag.TRAN, place)
                    lines = DefTag.str_to_str(
                        lines, level + 1, Tag.LANG, self.language
                    )
        return lines


class Map(NamedTuple):
    """Store, validate and save a GEDCOM map structure.

    Examples:
    >>> from chronodata.store import Map
    >>> location = Map('N', 49.297222, 'E', 14.470833)
    >>> print(location.ged(1))
    1 MAP
    2 LATI N49.297222
    2 LONG E14.470833
    <BLANKLINE>

    Reference:
        - [GEDCOM Map Standard](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#MAP)
        - [GEDCOM Latitude Standard](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#LATI)
        - [GEDCOM Longitude Standard](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#LONG)
    """

    north_south: Literal['N', 'S'] = 'N'
    latitude: float = 90.0
    east_west: Literal['E', 'W'] = 'W'
    longitude: float = 0.0

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.latitude, float)
            and DefCheck.verify_enum(self.north_south, Latitude)
            and DefCheck.verify_type(self.longitude, float)
            and DefCheck.verify_enum(self.east_west, Longitude)
            and DefCheck.verify_range(self.latitude, 0.0, 360.0)
            and DefCheck.verify_range(self.longitude, -90.0, 90.0)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        latitude: str = ''.join([self.north_south, str(self.latitude)])
        longitude: str = ''.join([self.east_west, str(self.longitude)])
        if self.validate():
            lines = DefTag.empty_to_str(lines, level, Tag.MAP)
            lines = DefTag.str_to_str(lines, level + 1, Tag.LATI, latitude)
            lines = DefTag.str_to_str(lines, level + 1, Tag.LONG, longitude)
        return lines


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
        >>> from chronodata.store import Map, Place, PlaceName
        >>> bechyne_cs = PlaceName(
        ...     place1='Bechyně',
        ...     place2='okres Tábor',
        ...     place3='Jihočeský kraj',
        ...     place4='Česká republika',
        ...     form1='Město',
        ...     form2='Okres',
        ...     form3='Stát',
        ...     form4='Země',
        ...     language='cs',
        ... )
        >>> bechyne_en = PlaceName(
        ...     place1='Bechyně',
        ...     place2='Tábor District',
        ...     place3='South Bohemian Region',
        ...     place4='Czech Republic',
        ...     language='en',
        ... )
        >>> place = Place(
        ...     place=bechyne_cs,
        ...     translations=[
        ...         bechyne_en,
        ...     ],
        ...     map=Map('N', 49.297222, 'E', 14.470833),
        ...     notes=[
        ...         Note(note='A place in the Czech Republic.', language='en'),
        ...         Note(note='Místo v České republice.', language='cs'),
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
        place: A `PlaceName` tuple containing four place names, four forms and language tag.
        translation: A list of `PlaceName` tuples used as translations.
        maps: A list of `Map` tuples for the place.
        exid: Identifiers associated with the place.
        notes: Notes associated with the place.


    Reference:
        [W3C Internationalization](https://www.w3.org/International/questions/qa-choosing-language-tags)
        [Language Subtag Lookup Tool](https://r12a.github.io/app-subtags/)
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

    place: PlaceName = PlaceName(String.EMPTY)
    translations: list[PlaceName] = []  # noqa: RUF012
    map: Map = Map('N', 0, 'W', 0)
    exids: list[Exid] = []  # noqa: RUF012
    notes: list[Note] = []  # noqa: RUF012

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.place, PlaceName)
            and DefCheck.verify_tuple_type(self.translations, PlaceName)
            and DefCheck.verify_type(self.map, Map)
            and DefCheck.verify_tuple_type(self.exids, Exid)
            and DefCheck.verify_tuple_type(self.notes, Note)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = ''.join([lines, self.place.ged(level)])
            lines = DefTag.list_to_str(
                lines,
                level + 1,
                self.translations,
                flag=String.PLACE_TRANSLATION,
            )
            lines = ''.join([lines, self.map.ged(level + 1)])
            lines = DefTag.list_to_str(lines, level + 1, self.exids)
            lines = DefTag.list_to_str(lines, level + 1, self.notes)
        return lines


class Date(NamedTuple):
    """Validate and display date data in various formats.

    Dates are entered based on a Gregorian calendar. This calendar
    does not have a 0 year.  The year 1 BC is entered as `-1`.

    A default value of `0` for any date component means that the component
    will not be displayed.

    The GEDCOM standard allows a week without specifying the other components.

    Parameters:
        year


    Examples:

    Reference:
        [GEDCOM DATE](https://gedcom.io/terms/v7/DATE)
        [GEDCOM DATE type](https://gedcom.io/terms/v7/type-Date)
    """

    year: int = 0
    month: int = 0
    day: int = 0
    week: int = 0
    calendar: str = Value.GREGORIAN

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.year, int)
            and DefCheck.verify_type(self.month, int)
            and DefCheck.verify_type(self.day, int)
            and DefCheck.verify_type(self.week, int)
            and DefCheck.verify_range(self.week, 0, 52)
            and DefCheck.verify_range(self.month, 0, 12)
            # and if self.year == 0:
            #     raise ValueError(Msg.NO_ZERO_YEAR.format(self.year, self.calendar))
        )
        return check

    def ged(self, level: int = 1, calendar: str = Value.GREGORIAN) -> str:
        """Display the validated date in GEDCOM format.

        Reference
        ---------
        - [GEDCOM Standard V 7.0](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#date)
        """
        lines: str = ''
        if self.validate():
            # day_str: str = (
            #     str(self.day) if self.day > 9 else ''.join(['0', str(self.day)])
            # )
            month_str: str = (
                str(self.month)
                if self.month > 9
                else ''.join(['0', str(self.month)])
            )
            year_str: str = str(self.year)
            if self.year < 0:
                year_str = ''.join(
                    [str(-self.year), Cal.CALENDARS[calendar][Value.EPOCH]]
                )
            formatted_date: str = ''
            if self.day != 0:
                formatted_date = ''.join([formatted_date, f' {self.day!s}'])
            if self.month != 0:
                formatted_date = ''.join(
                    [
                        formatted_date,
                        f' {Cal.CALENDARS[calendar][Value.MONTH_NAMES][str(month_str)]}',
                    ]
                )
            if self.year != 0:
                formatted_date = ''.join(
                    [formatted_date, f' {year_str}\n']
                ).strip()
            lines = DefTag.str_to_str(lines, level, Tag.DATE, formatted_date)
        return lines

    def iso(self) -> str:
        """Return the validated ISO format for the date.

        References
        ----------
        - [ISO 8601 Standard](https://www.iso.org/iso-8601-date-and-time-format.html)
        - [Wikipedia Overview](https://en.wikipedia.org/wiki/ISO_8601)
        """
        if self.validate():
            return f'{self.year}-{self.month}-{self.day}'
        return ''


class Time(NamedTuple):
    """Validate and display time data in various formats.

    The standard does not permit leap seconds nor end of day instant (24:00:00).

    Reference
    ---------
    - [GEDCOM Time Data Type](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#time)
    """

    hour: int = 0
    minute: int = 0
    second: int | float = 0.0
    UTC: bool = False

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.hour, int)
            and DefCheck.verify_type(self.minute, int)
            and DefCheck.verify_type(self.second, int | float)
            and DefCheck.verify_type(self.UTC, bool)
            and DefCheck.verify_range(self.hour, 0, 23)
            and DefCheck.verify_range(self.minute, 0, 59)
            and DefCheck.verify_range(self.second, 0, 59.999999999999)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        hour_str: str = str(self.hour)
        minute_str: str = str(self.minute)
        second_str: str = str(self.second)
        if self.validate():
            if 0 <= self.hour < 10:
                hour_str = ''.join(['0', hour_str])
            if 0 <= self.minute < 10:
                minute_str = ''.join(['0', minute_str])
            if 0 <= self.second < 10:
                second_str = ''.join(['0', second_str])
            if self.UTC:
                second_str = ''.join([second_str, 'Z'])
            return DefTag.taginfo(
                level, Tag.TIME, f'{hour_str}:{minute_str}:{second_str}'
            )
        return ''

    def iso(self) -> str:
        """Return the validated ISO format for the time.

        References:
            [ISO 8601 Standard](https://www.iso.org/iso-8601-date-and-time-format.html)
            [Wikipedia Overview](https://en.wikipedia.org/wiki/ISO_8601)
        """
        if self.validate():
            return f'{self.hour}:{self.minute}:{self.second}'
        return ''


class DateExact(NamedTuple):
    """Construct a DATEVALUE structure according to the GEDCOM standard.

    Example
    -------


    Reference
    ---------

    >n DATE <DateValue>                         {1:1}  g7:DATE
    >  +1 TIME <Time>                           {0:1}  g7:TIME
    >  +1 PHRASE <Text>                         {0:1}  g7:PHRASE
    """

    date: Date = Date(0, 0, 0)
    time: Time = Time(0, 0, 0)
    phrase: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.phrase, str)
            and self.date.validate()
            and self.time.validate()
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = self.date.ged(level)
        if self.validate():
            if self.time != Time(0, 0, 0):
                lines = ''.join([lines, self.time.ged(level + 1)])
            if self.phrase != '':
                lines = ''.join(
                    [lines, DefTag.taginfo(level + 1, Tag.PHRASE, self.phrase)]
                )
        return lines


class DateValue(NamedTuple):
    """Construct a DATEVALUE structure according to the GEDCOM standard.

    Example
    -------


    Reference
    ---------

    >n DATE <DateValue>                         {1:1}  g7:DATE
    >  +1 TIME <Time>                           {0:1}  g7:TIME
    >  +1 PHRASE <Text>                         {0:1}  g7:PHRASE
    """

    date: Date = Date(0, 0, 0)
    time: Time = Time(0, 0, 0)
    phrase: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.phrase, str)
            and self.date.validate()
            and self.time.validate()
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = self.date.ged(level)
            if self.time != Time(0, 0, 0):
                lines = ''.join([lines, self.time.ged(level + 1)])
            if self.phrase != '':
                lines = ''.join(
                    [lines, DefTag.taginfo(level + 1, Tag.PHRASE, self.phrase)]
                )
        return lines


class EventDetail(NamedTuple):
    """Store, validate and display a GEDCOM Event Detail.

    Reference:
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

    date_value: DateValue | None = None
    place: Place | None = None
    address: Address = Address([], '', '', '', '')
    phones: list[str] = []  # noqa: RUF012
    emails: list[str] = []  # noqa: RUF012
    faxes: list[str] = []  # noqa: RUF012
    wwws: list[str] = []  # noqa: RUF012
    agency: str = ''
    religion: str = ''
    cause: str = ''
    resn: str = ''
    # sort_date: SortDate = ()
    associations: list[Association] = []  # noqa: RUF012
    notes: list[Note] = []  # noqa: RUF012
    sources: list[SourceCitation] = []  # noqa: RUF012
    multimedia_links: list[MultimediaLink] = []  # noqa: RUF012
    uids: list[Id] = []  # noqa: RUF012

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.date_value, DateValue)
            and DefCheck.verify_type(self.place, Place)
            and DefCheck.verify_type(self.address, Address)
            and DefCheck.verify_tuple_type(self.phones, str)
            and DefCheck.verify_tuple_type(self.emails, str)
            and DefCheck.verify_tuple_type(self.faxes, str)
            and DefCheck.verify_tuple_type(self.wwws, str)
            and DefCheck.verify_type(self.agency, str)
            and DefCheck.verify_type(self.religion, str)
            and DefCheck.verify_type(self.cause, str)
            and DefCheck.verify_type(self.resn, str)
            and DefCheck.verify_tuple_type(self.associations, Association)
            and DefCheck.verify_tuple_type(self.notes, Note)
            and DefCheck.verify_tuple_type(self.sources, Source)
            and DefCheck.verify_tuple_type(
                self.multimedia_links, MultimediaLink
            )
            and DefCheck.verify_tuple_type(self.uids, Id)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            if self.date_value is not None:
                lines = ''.join([lines, self.date_value.ged(level)])
            if self.place is not None:
                lines = ''.join([lines, self.place.ged(level)])
            # if self.address != Address([], '', '', '', ''):
            lines = ''.join([lines, self.address.ged(level)])
            lines = DefTag.strlist_to_str(lines, level, Tag.PHON, self.phones)
            lines = DefTag.strlist_to_str(lines, level, Tag.EMAIL, self.emails)
            lines = DefTag.strlist_to_str(lines, level, Tag.FAX, self.faxes)
            lines = DefTag.strlist_to_str(lines, level, Tag.WWW, self.wwws)
            lines = DefTag.str_to_str(lines, level, Tag.AGNC, self.agency)
            lines = DefTag.str_to_str(lines, level, Tag.RELI, self.religion)
            lines = DefTag.str_to_str(lines, level, Tag.CAUS, self.cause)
            lines = DefTag.str_to_str(lines, level, Tag.RESN, self.resn)
            lines = DefTag.list_to_str(lines, level, self.associations)
            lines = DefTag.list_to_str(lines, level, self.notes)
            lines = DefTag.list_to_str(lines, level, self.sources)
            lines = DefTag.list_to_str(lines, level, self.multimedia_links)
            lines = DefTag.list_to_str(lines, level, self.uids)
        return lines

    def code(self, level: int = 0, detail: str = String.MIN) -> str:
        spaces: str = String.INDENT * level
        preface: str = """
            # https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#EVENT_DETAIL
            from chronodata.constants import Choice
            from chronodata.store import Age, FamilyEventDetail

            """
        return indent(
            dedent(f"""
            {preface if detail == String.MAX else ''}
        """),
            spaces,
        )


class FamilyEventDetail(NamedTuple):
    """Store, validate and display GEDCOM family event detail structure.

    Examples:
        >>> from chronodata.store import FamilyEventDetail
        >>> family_detail = FamilyEventDetail(
        ...     husband_age=Age(25, phrase='Happy'),
        ...     wife_age=Age(24, phrase='Very happy'),
        ... )
        >>> print(family_detail.ged(1))
        1 HUSB
        2 AGE > 25y
        3 PHRASE Happy
        1 WIFE
        2 AGE > 24y
        3 PHRASE Very happy
        <BLANKLINE>

    References:
        [GEDCOM Family Event Detail](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_EVENT_DETAIL)

    > n HUSB                                     {0:1}  [g7:HUSB](https://gedcom.io/terms/v7/HUSB)
    >   +1 AGE <Age>                             {1:1}  [g7:AGE](https://gedcom.io/terms/v7/AGE)
    >      +2 PHRASE <Text>                      {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    > n WIFE                                     {0:1}  [g7:WIFE](https://gedcom.io/terms/v7/WIFE)
    >   +1 AGE <Age>                             {1:1}  [g7:AGE](https://gedcom.io/terms/v7/AGE)
    >      +2 PHRASE <Text>                      {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    > n <<EVENT_DETAIL>>                         {0:1}
    """

    husband_age: Age | None = None
    wife_age: Age | None = None
    event_detail: EventDetail | None = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.husband_age, Age | None)
            and DefCheck.verify_type(self.wife_age, Age | None)
            and DefCheck.verify_type(self.event_detail, EventDetail | None)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            if self.husband_age is not None:
                lines = DefTag.empty_to_str(lines, level, Tag.HUSB)
                lines = ''.join([lines, self.husband_age.ged(level + 1)])
            if self.wife_age is not None:
                lines = DefTag.empty_to_str(lines, level, Tag.WIFE)
                lines = ''.join([lines, self.wife_age.ged(level + 1)])
            if self.event_detail is not None:
                lines = ''.join([lines, self.event_detail.ged(level)])
        return lines

    def code(self, level: int = 0, detail: str = String.MIN) -> str:
        spaces: str = String.INDENT * level
        preface: str = """
            # https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_EVENT_DETAIL
            from chronodata.constants import Choice
            from chronodata.store import Age, FamilyEventDetail

            """
        return indent(
            dedent(f"""
            {preface if detail == String.MAX else ''}
        """),
            spaces,
        )


class FamilyAttribute(NamedTuple):
    """Store, validate and display a GEDCOM Family Attribute.

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
    payload: str = String.EMPTY
    attribute_type: str = String.EMPTY
    family_event_detail: FamilyEventDetail | None = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.tag, Tag)
            and DefCheck.verify_enum(self.tag.value, FamAttr)
            and DefCheck.verify_type(self.payload, str)
            and DefCheck.verify_type(self.attribute_type, str)
            and DefCheck.verify_type(
                self.family_event_detail, FamilyEventDetail | None
            )
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.tag.value != Tag.NONE.value and self.validate():
            lines = DefTag.str_to_str(lines, level, self.tag, self.payload)
            lines = DefTag.str_to_str(
                lines, level + 1, Tag.TYPE, self.attribute_type
            )
            if self.family_event_detail is not None:
                lines = ''.join(
                    [lines, self.family_event_detail.ged(level + 1)]
                )
        return lines


class FamilyEvent(NamedTuple):
    """Store, validate and display a GEDCOM Family Event.

    Examples:
        Only the following tags can be used in this structure:
        Tag.ANUL, Tag.CENS, Tag.DIV, Tag.DIVF, Tag.ENGA, Tag.MARB, Tag.MARC, Tag.MARL,
        Tag.MARR, Tag.MARS, Tag.EVEN.  This example shows the error that
        would result if a different tag is used once the NamedTuple is validated.
        First, set up the situation for the error to occur.
        >>> from chronodata.enums import Tag
        >>> from chronodata.store import FamilyEvent
        >>> event = FamilyEvent(Tag.DATE)

        Next, evaluate `event`.
        >>> event.validate()
        Traceback (most recent call last):
        ValueError: The tag DATE is not in the list of valid tags.

        The `validate` method also checks that the Tag.EVEN cannot have an empty payload.
        >>> event2 = FamilyEvent(Tag.EVEN)
        >>> event2.validate()
        Traceback (most recent call last):
        ValueError: The event type for tag EVEN must have some value.

    References:
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
    payload: str = String.OCCURRED
    event_type: str = String.EMPTY
    event_detail: FamilyEventDetail | None = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check_payload: bool = self.payload in {
            String.OCCURRED,
            String.EMPTY,
        }
        check_tag: bool = self.tag.value in {
            Tag.ANUL.value,
            Tag.CENS.value,
            Tag.DIV.value,
            Tag.DIVF.value,
            Tag.ENGA.value,
            Tag.MARB.value,
            Tag.MARC.value,
            Tag.MARL.value,
            Tag.MARR.value,
            Tag.MARS.value,
        }
        even: bool = self.event_type != String.EMPTY
        check: bool = (
            DefCheck.verify_type(self.tag, Tag)
            and DefCheck.verify_enum(self.tag.value, FamEven)
            and DefCheck.verify_type(self.payload, str)
            and DefCheck.verify_type(self.event_type, str)
            and DefCheck.verify_type(
                self.event_detail, FamilyEventDetail | None
            )
            and DefCheck.verify(
                check_tag,
                check_payload,
                Msg.TAG_PAYLOAD.format(self.tag.value),
            )
            and DefCheck.verify(
                not check_tag, even, Msg.EMPTY_EVENT_TYPE.format(self.tag.value)
            )
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            if self.payload == String.EMPTY:
                lines = DefTag.empty_to_str(lines, level, self.tag)
            else:
                lines = DefTag.str_to_str(lines, level, self.tag, self.payload)
            lines = DefTag.str_to_str(
                lines, level + 1, Tag.TYPE, self.event_type
            )
            if self.event_detail is not None:
                lines = ''.join([lines, self.event_detail.ged(level + 1)])
        return lines

    def code(self, level: int = 0, detail: str = String.MIN) -> str:
        spaces: str = String.INDENT * level
        preface: str = """
            # https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_EVENT_STRUCTURE
            from chronodata.constants import Choice
            from chronodata.store import FamilyEvent

            """
        return indent(
            dedent(f"""
            {preface if detail == String.MAX else ''}
        """),
            spaces,
        )


class Husband(NamedTuple):
    xref: IndividualXref = Void.INDI
    phrase: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = DefCheck.verify_type(
            self.phrase, str
        ) and DefCheck.verify_type(self.xref, IndividualXref)
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if str(self.xref) != Void.NAME and self.validate():
            lines = DefTag.str_to_str(lines, level, Tag.HUSB, str(self.xref))
            lines = DefTag.str_to_str(lines, level + 1, Tag.PHRASE, self.phrase)
        return lines


class Wife(NamedTuple):
    xref: IndividualXref = Void.INDI
    phrase: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = DefCheck.verify_type(
            self.phrase, str
        ) and DefCheck.verify_type(self.xref, IndividualXref)
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if str(self.xref) != Void.NAME and self.validate():
            lines = DefTag.str_to_str(lines, level, Tag.WIFE, str(self.xref))
            lines = DefTag.str_to_str(lines, level + 1, Tag.PHRASE, self.phrase)
        return lines


class Child(NamedTuple):
    xref: IndividualXref = Void.INDI
    phrase: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = DefCheck.verify_type(
            self.phrase, str
        ) and DefCheck.verify_type(self.xref, IndividualXref)
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if str(self.xref) != Void.NAME and self.validate():
            lines = DefTag.str_to_str(lines, level, Tag.CHIL, str(self.xref))
            lines = DefTag.str_to_str(lines, level + 1, Tag.PHRASE, self.phrase)
        return lines


class LDSOrdinanceDetail(NamedTuple):
    date_value: DateValue | None = None
    temp: str = ''
    place: Place | None = None
    status: Stat = Stat.NONE
    notes: Any = None
    sources: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.date_value, DateValue | None)
            and DefCheck.verify_type(self.temp, str)
            and DefCheck.verify_type(self.place, Place | None)
            and DefCheck.verify_enum(self.status.value, Stat)
            and DefCheck.verify_tuple_type(self.notes, Note)
            and DefCheck.verify_tuple_type(self.sources, SourceCitation)
        )
        return check

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
        return lines


class LDSSpouseSealing(NamedTuple):
    tag: Tag = Tag.SLGS
    detail: LDSOrdinanceDetail | None = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = DefCheck.verify_type(
            self.tag, str
        ) and DefCheck.verify_type(self.detail, LDSOrdinanceDetail | None)
        return check

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
        return lines


class LDSIndividualOrdinances(NamedTuple):
    tag: str
    ordinance_detail: LDSOrdinanceDetail | None = None
    family_xref: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.tag, str)
            and DefCheck.verify_type(
                self.ordinance_detail, LDSOrdinanceDetail | None
            )
            and DefCheck.verify_type(self.family_xref, str)
        )
        return check

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
        return lines


class Identifier(NamedTuple):
    """Construct GEDCOM data for the Identifier Structure.

    There are three valid identifier structures.  They will be illustrated in
    the examples.

    Examples:



    Reference:

    - [GEDCOM Identifier Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#IDENTIFIER_STRUCTURE)"""

    tag: Id = Id.NONE
    tag_info: str = ''
    tag_type: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_enum(self.tag.value, Id)
            and DefCheck.verify_type(self.tag_info, str)
            and DefCheck.verify_type(self.tag_type, str)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            if self.tag != Id.NONE:
                lines = DefTag.taginfo(level, self.tag.value, self.tag_info)
            if self.tag != Id.UID:
                lines = ''.join(
                    [lines, DefTag.taginfo(level + 1, Tag.TYPE, self.tag_type)]
                )
            if self.tag == Id.EXID and self.tag_type == '':
                logging.warning(Msg.EXID_TYPE)
        return lines


class IndividualEventDetail(NamedTuple):
    """Store, validate and display a GEDCOM Individual Event Detail structure.

    Args:
        event_detail: A GEDCOM Event Detail structure.
        age: The age of the individual.
        phrase: Text describing the individual event.

    Reference:
        [GEDCOM Individual Event Detail](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_EVENT_DETAIL)

    > n <<EVENT_DETAIL>>                         {1:1}
    > n AGE <Age>                                {0:1}  [g7:AGE](https://gedcom.io/terms/v7/AGE)
    >   +1 PHRASE <Text>                         {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    """

    event_detail: EventDetail | None = None
    age: Age | None = None  # Age(0, 0, 0, 0, String.EMPTY, String.EMPTY)
    phrase: str = String.EMPTY

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.event_detail, EventDetail)
            and DefCheck.verify_type(self.age, Age)
            and DefCheck.verify_type(self.phrase, str)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate() and self.event_detail is not None:
            lines = ''.join([lines, self.event_detail.ged(level)])
            if self.age is not None:
                lines = ''.join([lines, self.age.ged(level)])
                lines = DefTag.str_to_str(
                    lines, level + 1, Tag.PHRASE, self.phrase
                )
        return lines


class IndividualAttribute(NamedTuple):
    """Store, validate and display a GEDCOM Individual Attribute structure.

    Reference:
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

    tag: IndiAttr
    tag_type: str = ''
    event_detail: IndividualEventDetail | None = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_enum(self.tag.value, IndiAttr)
            and DefCheck.verify_type(self.tag_type, str)
            and DefCheck.verify_type(
                self.event_detail, IndividualEventDetail | None
            )
        )
        return check

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
        return lines


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
        >>> from chronodata.build import Chronology
        >>> from chronodata.store import Individual, IndividualEvent

        Next, create a Chronology and an individual with reference `@I1@`.
        >>> chron = Chronology('event example')
        >>> indi_i1_xref = chron.individual_xref('I1')

        Finally, create the individual record for `@I1@` with two individual events
        and display the results.
        >>> indi_i1 = Individual(
        ...     xref=indi_i1_xref,
        ...     events=[
        ...         IndividualEvent(
        ...             tag=Tag.EVEN,
        ...             text='Land Lease',
        ...             event_detail=IndividualEventDetail(
        ...                 event_detail=EventDetail(
        ...                     date_value=DateValue(Date(1837, 10, 2))
        ...                 )
        ...             ),
        ...         ),
        ...         IndividualEvent(
        ...             tag=Tag.EVEN,
        ...             payload='Mining equipment',
        ...             text='Equipment Lease',
        ...             event_detail=IndividualEventDetail(
        ...                 EventDetail(date_value=DateValue(Date(1837, 11, 4)))
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
        tag: Specifies the kind of event.
        payload: Specifies that the event occurred if the default 'Y' is accepted. Otherwise use ''.
        tag_type: A text describing the event which must not be the empty string.
        event_detail: Information about the event in an IndividualEventDetail substructure.
        family_xref: A family xref will be displayed only for the Tag.ADOP, Tag.BIRT or Tag.CHR events.
        adoption: A tag for the kind of adoption will be displayed only for the Tag.ADOP event.
        phrase: A phrase describing the adoption will be displayed only for the Tag.ADOP event.

    References:
        [GEDCOM INDI-EVEN](https://gedcom.io/terms/v7/INDI-EVEN)
        [GEDCOM Individual Event Tags](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#individual-events)
        [GEDCOM Individual Event Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_EVENT_STRUCTURE)

    [
    > n ADOP [Y|<NULL>]                          {1:1}  [g7:ADOP](https://gedcom.io/terms/v7/ADOP)
    >   +1 TYPE <Text>                           {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
    >   +1 <<INDIVIDUAL_EVENT_DETAIL>>           {0:1}
    >   +1 FAMC @<XREF:FAM>@                     {0:1}  [g7:ADOP-FAMC](https://gedcom.io/terms/v7/ADOP-FAMC)
    >      +2 ADOP <Enum>                        {0:1}  [g7:FAMC-ADOP](https://gedcom.io/terms/v7/FAMC-ADOP)
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
    payload: str = String.EMPTY
    text: str = String.EMPTY
    event_detail: IndividualEventDetail | None = None
    family_xref: FamilyXref = Void.FAM
    adoption: Tag = Tag.NONE
    phrase: str = String.EMPTY

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_enum(self.tag.value, IndiEven)
            and DefCheck.verify_type(self.text, str)
            # and DefCheck.verify_not_default(self.text, String.EMPTY)
            and DefCheck.verify_type(
                self.event_detail, IndividualEventDetail | None
            )
            and DefCheck.verify_type(self.family_xref, FamilyXref)
            and DefCheck.verify_enum(self.adoption.value, Adop)
            and DefCheck.verify_type(self.phrase, str)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            if self.payload == String.EMPTY:
                lines = DefTag.empty_to_str(lines, level, self.tag)
            else:
                lines = DefTag.str_to_str(lines, level, self.tag, self.payload)
            lines = DefTag.str_to_str(lines, level + 1, Tag.TYPE, self.text)
            if self.event_detail is not None:
                lines = ''.join([lines, self.event_detail.ged(level + 1)])
            if (
                self.tag.value
                in (Tag.BIRT.value, Tag.CHR.value, Tag.ADOP.value)
                and self.family_xref.name != Void.FAM.name
            ):
                lines = DefTag.str_to_str(
                    lines, level + 1, Tag.FAMC, self.family_xref.fullname
                )
                if (
                    self.tag.value == Tag.ADOP.value
                    and self.family_xref.name != Void.FAM.name
                ):
                    lines = DefTag.str_to_str(
                        lines, level + 2, Tag.ADOP, self.adoption.value
                    )
                    if self.adoption.value != Tag.NONE.value:
                        lines = DefTag.str_to_str(
                            lines, level + 3, Tag.PHRASE, self.phrase
                        )
        return lines


class Alias(NamedTuple):
    """Store, validate and display a GEDCOM Alias structure."""

    xref: str
    phrase: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = DefCheck.verify_type(
            self.xref, str
        ) and DefCheck.verify_type(self.phrase, str)
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = DefTag.str_to_str(lines, level, Tag.ALIA, self.xref)
            lines = DefTag.str_to_str(lines, level + 1, Tag.PHRASE, self.phrase)
        return lines


class FamilyChild(NamedTuple):
    family_xref: FamilyXref
    pedigree: str = ''
    pedigree_phrase: str = ''
    status: str = ''
    status_phrase: str = ''
    notes: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.family_xref, str)
            and DefCheck.verify_type(self.pedigree, str)
            and DefCheck.verify_type(self.pedigree_phrase, str)
            and DefCheck.verify_type(self.status, str)
            and DefCheck.verify_type(self.status_phrase, str)
            and DefCheck.verify_tuple_type(self.notes, Note)
        )
        return check

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
        return lines


class FamilySpouse(NamedTuple):
    family_xref: str = ''
    notes: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = DefCheck.verify_type(
            self.family_xref, str
        ) and DefCheck.verify_tuple_type(self.notes, Note)
        return check

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
        return lines


class FileTranslations(NamedTuple):
    path: str = ''
    media_type: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = DefCheck.verify_type(
            self.path, str
        ) and DefCheck.verify_type(self.media_type, str)
        return check

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
        return lines


# class Text(NamedTuple):
#     text: str = ''
#     mime: MediaType = MediaType.NONE
#     language: Lang = Lang.CODE['NONE']

#     def validate(self) -> bool:
#         """Validate the stored value."""
#         check: bool = (
#             DefCheck.verify_type(self.text, str)
#             and DefCheck.verify_type(self.mime, MediaType)
#             and DefCheck.verify_type(self.language, Lang)
#         )
#         return check

#     def ged(self, level: int = 1) -> str:
#         """Format to meet GEDCOM standards."""
#         lines: str = ''
#         if self.validate():
#             pass
#         return lines


class File(NamedTuple):
    path: str = ''
    media_type: MediaType = MediaType.NONE
    media: str = ''
    phrase: str = ''
    title: str = ''
    file_translations: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.path, str)
            and DefCheck.verify_type(self.media_type, str)
            and DefCheck.verify_type(self.media, str)
            and DefCheck.verify_type(self.phrase, str)
            and DefCheck.verify_type(self.title, str)
            and DefCheck.verify_tuple_type(
                self.file_translations, FileTranslations
            )
        )
        return check

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
        return lines


class SourceEvent(NamedTuple):
    event: str = ''
    date_period: str = ''
    phrase: str = ''
    place: Place | None = None
    agency: str = ''
    notes: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.event, str)
            and DefCheck.verify_type(self.date_period, str)
            and DefCheck.verify_type(self.phrase, str)
            and DefCheck.verify_type(self.place, str)
            and DefCheck.verify_type(self.agency, str)
            and DefCheck.verify_tuple_type(self.notes, Note)
        )
        return check

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
        return lines


class NonEvent(NamedTuple):
    no: str = ''
    date: Date | None = None
    phrase: str = ''
    notes: Any = None
    sources: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.no, str)
            and DefCheck.verify_type(self.date, Date | None)
            and DefCheck.verify_type(self.phrase, str)
            and DefCheck.verify_tuple_type(self.notes, Note)
            and DefCheck.verify_tuple_type(self.sources, SourceEvent)
        )
        return check

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
        return lines


class Family(NamedTuple):
    """Store, validate and display a GEDCOM Family Record.

    Args:
    - `xref`: typed string obtained by running `chrono.family_xref()`.
    - `resn`: restriction codes with the default being no restriction.
    - `attributes`: a tuple of type Attribute.

    Reference:
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
    resn: Resn = Resn.NONE
    attributes: Any = None
    events: Any = None
    husband: Husband = Husband(Void.INDI)
    wife: Wife = Wife(Void.INDI)
    children: Any = None
    associations: Any = None
    submitters: Any = None
    lds_spouse_sealings: Any = None
    identifiers: Any = None
    notes: Any = None
    citations: Any = None
    multimedia_links: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.xref, FamilyXref)
            and DefCheck.verify_enum(self.resn.value, Resn)
            and DefCheck.verify_tuple_type(self.attributes, FamilyAttribute)
            and DefCheck.verify_tuple_type(self.events, FamilyEvent)
            and DefCheck.verify_type(self.husband, Husband)
            and DefCheck.verify_type(self.wife, Wife)
            and DefCheck.verify_tuple_type(self.children, Child)
            and DefCheck.verify_tuple_type(self.associations, Association)
            and DefCheck.verify_tuple_type(self.submitters, SubmitterXref)
            and DefCheck.verify_tuple_type(
                self.lds_spouse_sealings, LDSSpouseSealing
            )
            and DefCheck.verify_tuple_type(self.identifiers, Identifier)
            and DefCheck.verify_tuple_type(self.notes, Note)
            and DefCheck.verify_tuple_type(self.citations, SourceCitation)
            and DefCheck.verify_tuple_type(
                self.multimedia_links, MultimediaLink
            )
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged(level)
        if self.validate():
            if self.resn != Resn.NONE:
                lines = ''.join(
                    [lines, DefTag.taginfo(level, Tag.RESN, self.resn.value)]
                )
            if self.attributes is not None:
                for attribute in self.attributes:
                    lines = ''.join([lines, attribute.ged(level)])
            if self.events is not None:
                for event in self.events:
                    lines = ''.join([lines, event.ged(level)])
            if self.husband != Husband(Void.INDI):
                lines = ''.join([lines, self.husband.ged(level + 1)])
            if self.wife != Wife(Void.INDI):
                lines = ''.join([lines, self.wife.ged(level + 1)])
            if self.children is not None:
                for child in self.children:
                    lines = ''.join([lines, child.ged(level + 1)])
            if self.associations is not None:
                for association in self.associations:
                    lines = ''.join([lines, association.ged(level + 1)])
            if self.submitters is not None:
                for submitter in self.submitters:
                    lines = ''.join(
                        [lines, DefTag.taginfo(level, Tag.SUBM, submitter)]
                    )
            if self.lds_spouse_sealings is not None:
                for sealing in self.lds_spouse_sealings:
                    lines = ''.join([lines, sealing.ged(level + 1)])
            if self.identifiers is not None:
                for identifier in self.identifiers:
                    lines = ''.join([lines, identifier.ged(level + 1)])
            if self.notes is not None:
                for note in self.notes:
                    lines = ''.join([lines, note.ged(level + 1)])
            if self.citations is not None:
                for citation in self.citations:
                    lines = ''.join([lines, citation.ged(level + 1)])
            if self.multimedia_links is not None:
                for multimedia_link in self.multimedia_links:
                    lines = ''.join([lines, multimedia_link.ged(level + 1)])
        return lines


class Multimedia(NamedTuple):
    """Store, validate and display a GECDOM Multimedia Record.

    Reference:
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
    resn: Resn = Resn.NONE
    files: Any = None
    identifiers: Any = None
    notes: Any = None
    sources: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.xref, MultimediaXref)
            and DefCheck.verify_enum(self.resn.value, Resn)
            and DefCheck.verify_tuple_type(self.files, File)
            and DefCheck.verify_tuple_type(self.identifiers, Identifier)
            and DefCheck.verify_tuple_type(self.notes, Note)
            and DefCheck.verify_tuple_type(self.sources, Source)
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged(level)
        if self.validate():
            pass
        return lines


class Source(NamedTuple):
    """Store, validate and display a GEDCOM Source Record.

    Reference:
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
    author: str = ''
    title: str = ''
    abbreviation: str = ''
    published: str = ''
    events: Any = None
    text: Any = None
    repositories: Any = None
    identifiers: Any = None
    notes: Any = None
    multimedia_links: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.xref, SourceXref)
            and DefCheck.verify_type(self.author, str)
            and DefCheck.verify_type(self.title, str)
            and DefCheck.verify_type(self.abbreviation, str)
            and DefCheck.verify_type(self.published, str)
            and DefCheck.verify_tuple_type(self.events, SourceEvent)
            and DefCheck.verify_tuple_type(self.text, Text)
            and DefCheck.verify_tuple_type(self.repositories, Repository)
            and DefCheck.verify_tuple_type(self.identifiers, Identifier)
            and DefCheck.verify_tuple_type(self.notes, Note)
            and DefCheck.verify_tuple_type(
                self.multimedia_links, MultimediaLink
            )
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged(level)
        if self.validate():
            pass
        return lines


class Submitter(NamedTuple):
    """Store, validate and disply a GEDCOM Submitter Record.

    Reference:
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
    name: str = ''
    address: Address = Address([], '', '', '', '')
    phones: list[str] = []  # noqa: RUF012
    emails: list[str] = []  # noqa: RUF012
    faxes: list[str] = []  # noqa: RUF012
    wwws: list[str] = []  # noqa: RUF012
    multimedia_links: Any = None
    languages: Any = None
    identifiers: Any = None
    notes: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.xref, SubmitterXref)
            and DefCheck.verify_type(self.name, str)
            and DefCheck.verify_type(self.address, Address | None)
            and DefCheck.verify_tuple_type(self.phones, str)
            and DefCheck.verify_tuple_type(self.emails, str)
            and DefCheck.verify_tuple_type(self.faxes, str)
            and DefCheck.verify_tuple_type(self.wwws, str)
            and DefCheck.verify_tuple_type(
                self.multimedia_links, MultimediaLink
            )
            and DefCheck.verify_tuple_type(self.languages, str)
            and DefCheck.verify_tuple_type(self.identifiers, Identifier)
            and DefCheck.verify_tuple_type(self.notes, Note)
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged(level)
        if str(self.xref) != Void.NAME and self.validate():
            pass
        return lines


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
        >>> from chronodata.build import Chronology
        >>> from chronodata.store import Association, Individual
        >>> from chronodata.enums import Role

        Next instantiate a Chronology which will store the information.
        This will be named `test`.
        >>> a = Chronology('test')

        Next instantiate two IndivdiaulXref values called `I1` and `I2`.
        >>> i1 = a.individual_xref('I1')
        >>> i2 = a.individual_xref('I2')

        Add values to the Individual NamedTuple to store this information.
        >>> indi = Individual(
        ...     xref=i1,
        ...     associations=[
        ...         Association(
        ...             xref=i2,
        ...             role=Role.GODP,
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
        TypeError: "@MY_FAMILY@" has type <class 'chronodata.records.FamilyXref'> but should have type <class 'chronodata.records.IndividualXref'>.

    Reference:
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
    resn: Resn = Resn.NONE
    personal_names: list[PersonalNamePieces] = []  # noqa: RUF012
    sex: Sex = Sex.NONE
    attributes: list[IndividualAttribute] = []  # noqa: RUF012
    events: list[IndividualEvent] = []  # noqa: RUF012
    lds_individual_ordinances: list[LDSIndividualOrdinances] = []  # noqa: RUF012
    submitters: list[Submitter] = []  # noqa: RUF012
    associations: list[Association] = []  # noqa: RUF012
    aliases: list[Alias] = []  # noqa: RUF012
    ancestor_interest: list[Submitter] = []  # noqa: RUF012
    descendent_interest: list[Submitter] = []  # noqa: RUF012
    identifiers: list[Identifier] = []  # noqa: RUF012
    notes: list[Note] = []  # noqa: RUF012
    sources: list[Source] = []  # noqa: RUF012
    multimedia_links: list[Multimedia] = []  # noqa: RUF012

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.xref, IndividualXref)
            and DefCheck.verify_enum(self.resn.value, Resn)
            and DefCheck.verify_tuple_type(
                self.personal_names, PersonalNamePieces
            )
            and DefCheck.verify_enum(self.sex.value, Sex)
            and DefCheck.verify_tuple_type(self.attributes, IndividualAttribute)
            and DefCheck.verify_tuple_type(self.events, IndividualEvent)
            and DefCheck.verify_tuple_type(
                self.lds_individual_ordinances, LDSIndividualOrdinances
            )
            and DefCheck.verify_tuple_type(self.submitters, str)
            and DefCheck.verify_tuple_type(self.associations, Association)
            and DefCheck.verify_tuple_type(self.aliases, Alias)
            and DefCheck.verify_tuple_type(self.ancestor_interest, str)
            and DefCheck.verify_tuple_type(self.descendent_interest, str)
            and DefCheck.verify_tuple_type(self.identifiers, Identifier)
            and DefCheck.verify_tuple_type(self.notes, Note)
            and DefCheck.verify_tuple_type(self.sources, Source)
            and DefCheck.verify_tuple_type(
                self.multimedia_links, MultimediaLink
            )
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged(level)
        if self.validate():
            lines = DefTag.str_to_str(
                lines, level + 1, Tag.RESN, self.resn.value
            )
            lines = DefTag.list_to_str(lines, level + 1, self.personal_names)
            lines = DefTag.str_to_str(lines, level + 1, Tag.SEX, self.sex.value)
            lines = DefTag.list_to_str(lines, level + 1, self.attributes)
            lines = DefTag.list_to_str(lines, level + 1, self.events)
            lines = DefTag.list_to_str(
                lines, level + 1, self.lds_individual_ordinances
            )
            lines = DefTag.list_to_str(lines, level + 1, self.submitters)
            lines = DefTag.list_to_str(lines, level + 1, self.associations)
            lines = DefTag.list_to_str(lines, level + 1, self.aliases)
            lines = DefTag.list_to_str(lines, level + 1, self.ancestor_interest)
            lines = DefTag.list_to_str(
                lines, level + 1, self.descendent_interest
            )
            lines = DefTag.list_to_str(lines, level + 1, self.identifiers)
            lines = DefTag.list_to_str(lines, level + 1, self.notes)
            lines = DefTag.list_to_str(lines, level + 1, self.sources)
            lines = DefTag.list_to_str(lines, level + 1, self.multimedia_links)
        return lines

    def code(
        self,
        level: int = 0,
        chronology_name: str = 'chron',
        detail: str = String.MIN,
    ) -> str:
        spaces: str = String.INDENT * level
        preface: str = f"""
            # https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_RECORD
            from chronodata.build import Chronology
            from chronodata.enums import Resn, Sex
            from chronodata.store import Individual

            {chronology_name} = Chronology('{chronology_name}')
            {self.xref.code_xref} = {chronology_name}.individual_xref('{self.xref.name}')
            """
        return indent(
            dedent(f"""
            {preface if detail == String.MAX else ''}
            {self.xref.code} = Individual(
                xref = {self.xref.code_xref},
                resn = {self.resn},
                personal_names = {self.personal_names},
                sex = {self.sex},
                attributes = {self.attributes},
                events = {self.events},
                lds_individual_ordinances = {self.lds_individual_ordinances},
                submitters = {self.submitters},
                associations = {self.associations},
                aliases = {self.aliases},
                ancestor_interest = {self.ancestor_interest},
                descendent_interest = {self.descendent_interest},
                identifiers = {self.identifiers},
                notes = {self.notes},
                sources = {self.sources},
                multimedia_links = {self.multimedia_links}
            )
            """),
            spaces,
        )


class Repository(NamedTuple):
    """
    Reference:
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
    name: str = ''
    address: Address = Address([], '', '', '', '')
    phones: list[str] = []  # noqa: RUF012
    emails: list[str] = []  # noqa: RUF012
    faxes: list[str] = []  # noqa: RUF012
    wwws: list[str] = []  # noqa: RUF012
    notes: Any = None
    identifiers: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.xref, RepositoryXref)
            and DefCheck.verify_type(self.name, str)
            and DefCheck.verify_type(self.address, Address | None)
            and DefCheck.verify_tuple_type(self.emails, str)
            and DefCheck.verify_tuple_type(self.faxes, str)
            and DefCheck.verify_tuple_type(self.wwws, str)
            and DefCheck.verify_tuple_type(self.notes, Note)
            and DefCheck.verify_tuple_type(self.identifiers, Identifier)
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged(level)
        if self.validate():
            lines = ''.join([lines, self.address.ged(level)])
            lines = DefTag.strlist_to_str(lines, level, Tag.PHON, self.phones)
            lines = DefTag.strlist_to_str(lines, level, Tag.EMAIL, self.emails)
            lines = DefTag.strlist_to_str(lines, level, Tag.FAX, self.faxes)
            lines = DefTag.strlist_to_str(lines, level, Tag.WWW, self.wwws)
        return lines


class SharedNote(NamedTuple):
    xref: SharedNoteXref = Void.SNOTE
    text: str = ''
    mime: MediaType = MediaType.NONE
    language: str = String.UNDETERMINED
    translations: Any = None
    sources: Any = None
    identifiers: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.xref, SharedNoteXref)
            and DefCheck.verify_type(self.text, str)
            and DefCheck.verify_enum(self.mime.value, MediaType)
            and DefCheck.verify_type(self.language, str)
            and DefCheck.verify_tuple_type(self.translations, NoteTranslation)
            and DefCheck.verify_tuple_type(self.sources, Source)
            and DefCheck.verify_tuple_type(self.identifiers, Identifier)
        )
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged(level)
        if self.validate():
            pass
        return lines


class Schema(NamedTuple):
    """Store, validate and display schema information.

    Examples:


    Args:
        tag: The tag used for the schema information.
        url: The url defining the payload of the tag.

    Returns:
        A string representing a GEDCOM line for this tag.

    """

    tag: Tag = Tag.NONE
    url: str = ''

    def validate(self) -> bool:
        check: bool = (
            DefCheck.verify_type(self.tag, Tag)
            # and DefCheck.verify_enum(self.tag.value, Choice.EXTENSION_TAG)
            and DefCheck.verify_type(self.url, str)
        )
        return check


class Header(NamedTuple):
    """Hold data for the GEDCOM header special record.

    Reference
    ---------
    - [GEDCOM Header](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#HEADER)

    >n HEAD                                     {1:1}  g7:HEAD
    >  +1 GEDC                                  {1:1}  g7:GEDC
    >     +2 VERS <Special>                     {1:1}  g7:GEDC-VERS
    >  +1 SCHMA                                 {0:1}  g7:SCHMA
    >     +2 TAG <Special>                      {0:M}  g7:TAG
    >  +1 SOUR <Special>                        {0:1}  g7:HEAD-SOUR
    >     +2 VERS <Special>                     {0:1}  g7:VERS
    >     +2 NAME <Text>                        {0:1}  g7:NAME
    >     +2 CORP <Text>                        {0:1}  g7:CORP
    >        +3 <<ADDRESS_STRUCTURE>>           {0:1}
    >        +3 PHON <Special>                  {0:M}  g7:PHON
    >        +3 EMAIL <Special>                 {0:M}  g7:EMAIL
    >        +3 FAX <Special>                   {0:M}  g7:FAX
    >        +3 WWW <Special>                   {0:M}  g7:WWW
    >     +2 DATA <Text>                        {0:1}  g7:HEAD-SOUR-DATA
    >        +3 DATE <DateExact>                {0:1}  g7:DATE-exact
    >           +4 TIME <Time>                  {0:1}  g7:TIME
    >        +3 COPR <Text>                     {0:1}  g7:COPR
    >  +1 DEST <Special>                        {0:1}  g7:DEST
    >  +1 DATE <DateExact>                      {0:1}  g7:HEAD-DATE
    >     +2 TIME <Time>                        {0:1}  g7:TIME
    >  +1 SUBM @<XREF:SUBM>@                    {0:1}  g7:SUBM
    >  +1 COPR <Text>                           {0:1}  g7:COPR
    >  +1 LANG <Language>                       {0:1}  g7:HEAD-LANG
    >  +1 PLAC                                  {0:1}  g7:HEAD-PLAC
    >     +2 FORM <List:Text>                   {1:1}  g7:HEAD-PLAC-FORM
    >  +1 <<NOTE_STRUCTURE>>                    {0:1}
    """

    schemas: Any = None
    source: str = ''
    vers: str = ''
    name: str = ''
    corp: str = ''
    address: Address = Address([], '', '', '', '')
    phones: list[str] = []  # noqa: RUF012
    emails: list[str] = []  # noqa: RUF012
    faxes: list[str] = []  # noqa: RUF012
    wwws: list[str] = []  # noqa: RUF012
    data: str = ''
    dest: str = ''
    date: Date = Date(0, 0, 0)
    time: Time = Time(0, 0, 0)
    copr: str = ''
    language: str = String.UNDETERMINED
    place: PlaceName | None = None
    note: Note | None = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = True
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = DefTag.empty_to_str(lines, level, Tag.HEAD)
            lines = DefTag.empty_to_str(lines, level + 1, Tag.GEDC)
            lines = DefTag.str_to_str(
                lines, level + 2, Tag.VERS, String.VERSION
            )
            if self.schemas is not None:
                lines = DefTag.empty_to_str(lines, level + 1, Tag.SCHMA)
            lines = ''.join([lines, self.address.ged(level)])
            lines = DefTag.strlist_to_str(lines, level, Tag.PHON, self.phones)
            lines = DefTag.strlist_to_str(lines, level, Tag.EMAIL, self.emails)
            lines = DefTag.strlist_to_str(lines, level, Tag.FAX, self.faxes)
            lines = DefTag.strlist_to_str(lines, level, Tag.WWW, self.wwws)
            # lines = DefTag.list_to_str(lines, level + 1, Tag.TAG, self.schemas)
        return lines
