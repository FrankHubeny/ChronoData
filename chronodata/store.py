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

import logging
from typing import Any, Literal, NamedTuple

from chronodata.constants import Cal, Choice, String, Value
from chronodata.enums import (
    Event,
    Id,
    IndiAttr,
    Media,
    MediaType,
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
)


class Address(NamedTuple):
    """Store, validate and format address information to be saved to a ged file.

    Example:
        The following is the minimum amount of information for an address.
        >> from chronodata.store import Address
        >> mailing_address = Address(
        ..     '12345 ABC Street\nSouth North City, My State 22222'
        .. )
        >> print(mailing_address.ged(1))
        1 ADDR 12345 ABC Street
        1 CONT South North City, My State 22222
        <BLANKLINE>

        There are five named strings stored in this NamedTuple.
        >> from chronodata.store import Address
        >> full_address = Address(
        .. '12345 ABC Street\nSouth North City, My State 23456',
        .. 'South North City',
        .. 'My State',
        .. '23456',
        .. 'USA',
        .. )
        >> print(full_address.ged(1))
        1 ADDR 12345 ABC Street
        1 CONT South North City, My State 23456
        2 CITY South North City
        2 STAE My State
        2 POST 23456
        2 CTRY USA
        <BLANKLINE>

    Args:
        address: The mailing address with each line separated by '\n'.
        city: The city or and empty string to leave this blank.
        state: The state or an empty string to leave this blank.
        postal: The postal code or an empty string to leave this blank.
        country: The country or an empty string to leave this blank.

    Returns:
        A string displaying stored Address data formatted to GEDCOM specifications.

    Reference:
        [GEDCOM Specifications](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#substructures)
    """

    address: str = ''
    city: str = ''
    state: str = ''
    postal: str = ''
    country: str = ''

    def validate(self) -> bool:
        check: bool = (
            DefCheck.verify_type(self.address, str)
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
            if self.address != '':
                split_address: list[str] = self.address.split('\n')
                lines = DefTag.str_to_str(
                    lines, level, Tag.ADDR, split_address[0]
                )
                for line in split_address[1:]:
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
        >>> print(Age(10, 2, 1, 2).ged(2))
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
    greater_less_than: str = ''
    phrase: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_choice(
                self.greater_less_than, Choice.GREATER_LESS_THAN
            )
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


class PersonalNamePiece(NamedTuple):
    """Store, validate and display values for an optional GEDCOM Personal Name Piece.

    This is one of the 24 substructures in the GEDCOM standard.

    There are six GEDCOM tags which are formatted through this class.
    - [NPFX]():
        a prefix for the person, such as, "Dr" or "Mrs".
    - [GIVN]():
        the given, or first, name of the person, such as, "Thomas" or "Mary".
    - [NICK]():
        a nickname for the person, such as, "Joey".
    - [SPFX]():
        a surname prefix for the person.
    - [SURN]():
        the surname, or last name, of the person, such as, "Smith".
    - [NSFX]():
        a surname suffix for the person.

    Example:
        This example includes all six of the Personal Name Piece tags.
        >>> from chronodata.store import PersonalNamePiece  # doctest: +ELLIPSIS
        >>> from chronodata.enums import Tag
        >>> prefix = PersonalNamePiece(Tag.NPFX, 'Mr.')
        >>> given = PersonalNamePiece(Tag.GIVN, 'Joseph')
        >>> nickname = PersonalNamePiece(Tag.NICK, 'Joey')
        >>> surname = PersonalNamePiece(Tag.SURN, 'Hall')
        >>> suffix = PersonalNamePiece(Tag.NSFX, 'Jr.')
        >>> surname_prefix = PersonalNamePiece(Tag.SPFX, 'Wall')
        >>> print(prefix.ged(2))
        2 NPFX Mr.
        <BLANKLINE>
        >>> print(given.ged(2))
        2 GIVN Joseph
        <BLANKLINE>
        >>> print(nickname.ged(2))
        2 NICK Joey
        <BLANKLINE>
        >>> print(surname.ged(2))
        2 SURN Hall
        <BLANKLINE>
        >>> print(suffix.ged(2))
        2 NSFX Jr.
        <BLANKLINE>
        >>> print(surname_prefix.ged(2))
        2 SPFX Wall
        <BLANKLINE>

        If one of these tags is not used, an ValueError would display.
        >>> bad_piece = PersonalNamePiece(Tag.NAME, 'Tom')
        >>> bad_piece.ged(1)
        Traceback (most recent call last):
        ValueError: The value "NAME" is not in the ...

        The error in the above example did not occur immediately, but one had to
        attempt to use the NamedTuple by displaying it as a GEDCOM line.  One could
        also run the `validate` method on `bad piece` to trigger the error.  This
        method is called by `ged` prior to displaying the GEDCOM line.
        >>> bad_piece.validate()
        Traceback (most recent call last):
        ValueError: The value "NAME" is not in the ...

    Args:
        tag: One of six tags used for a personal name pieces.
        text: The string value associated with that tag.

    Returns:
        A GEDCOM string storing this data.

    Reference:
        [GEDCOM Personal Name Pieces](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PERSONAL_NAME_PIECES)
    """

    tag: Tag = Tag.NONE
    text: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.tag, Tag)
            and DefCheck.verify_choice(
                self.tag.value, Choice.PERSONAL_NAME_PIECE
            )
            and DefCheck.verify_type(self.text, str)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        name_piece: str = ''
        if self.validate():
            name_piece = DefTag.taginfo(level, self.tag, self.text)
        return name_piece


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
        ...     PersonalNamePiece,
        ...     SourceCitation,
        ... )
        >>> from chronodata.enums import NameType
        >>> adam_note = Note('Here is a place to add more information.')
        >>> adam_nickname = PersonalNamePiece(Tag.NICK, 'הָֽאָדָ֖ם')
        >>> adam_english = NameTranslation('Adam', 'en')
        >>> adam_english_nickname = NameTranslation('the man', 'en')
        >>> adam = PersonalName(
        ...     name='אָדָ֛ם',
        ...     type=NameType.OTHER,
        ...     phrase='The first man',
        ...     pieces=(adam_nickname,),
        ...     translations=(
        ...         adam_english,
        ...         adam_english_nickname,
        ...     ),
        ...     notes=(adam_note,),
        ... )
        >>> print(adam.ged(1))
        1 NAME אָדָ֛ם
        2 TYPE OTHER
        2 NICK הָֽאָדָ֖ם
        2 TRAN Adam
        3 LANG en
        2 TRAN the man
        3 LANG en
        2 NOTE Here is a place to add more information.
        <BLANKLINE>

    Args:
        name: the person's name.
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
    """

    name: str = ''
    type: Tag = Tag.NONE
    phrase: str = ''
    pieces: Any = None
    translations: Any = None
    notes: Any = None
    sources: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_not_default(self.name, '')
            and DefCheck.verify_choice(self.type.value, Choice.NAME_TYPE)
            and DefCheck.verify_type(self.phrase, str)
            and DefCheck.verify_tuple_type(self.pieces, PersonalNamePiece)
            and DefCheck.verify_tuple_type(self.translations, NameTranslation)
            and DefCheck.verify_tuple_type(self.notes, Note)
            and DefCheck.verify_tuple_type(self.sources, SourceCitation)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = ''.join(
                [
                    DefTag.taginfo(level, Tag.NAME, self.name),
                    DefTag.taginfo(level + 1, Tag.TYPE, self.type.value),
                ]
            )
            if self.pieces is not None:
                for piece in self.pieces:
                    lines = ''.join([lines, piece.ged(level + 1)])
            if self.translations is not None:
                for translation in self.translations:
                    lines = ''.join([lines, translation.ged(level + 1)])
            if self.notes is not None:
                for note in self.notes:
                    lines = ''.join([lines, note.ged(level + 1)])
            if self.sources is not None:
                for source in self.sources:
                    lines = ''.join([lines, source.ged(level + 1)])
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
        [W3C Internationalization](https://www.w3.org/International/questions/qa-choosing-language-tags)
        [Language Subtag Lookup Tool](https://r12a.github.io/app-subtags/)
        [GEDCOM Pesonal Name Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PERSONAL_NAME_STRUCTURE)
    """

    translation: str = ''
    language: str = String.UNDETERMINED
    name_pieces: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.translation, str)
            and DefCheck.verify_not_default(self.translation, '')
            # and DefCheck.verify_dict_key(self.language, Lang.CODE)
            # and DefCheck.verify_not_default(self.language, '')
            and DefCheck.verify_tuple_type(self.name_pieces, PersonalNamePiece)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = ''.join(
                [
                    DefTag.taginfo(level, Tag.TRAN, self.translation),
                    DefTag.taginfo(level + 1, Tag.LANG, self.language),
                ]
            )
            if self.name_pieces is not None:
                for piece in self.name_pieces:
                    lines = ''.join([lines, piece.ged(level + 1)])
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
            # and DefCheck.verify_dict_key(self.language, Lang.CODE)
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
                    DefTag.taginfo(level + 1, Tag.LANG, self.language)
                    # DefTag.taglanguage(level + 1, self.language, Lang.CODE),
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
    """

    repo: RepositoryXref
    notes: Any = None
    call_numbers: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.repo, RepositoryXref)
            and DefCheck.verify_not_default(
                self.repo, RepositoryXref(String.RECORD)
            )
            and DefCheck.verify_tuple_type(self.notes, Note)
            and DefCheck.verify_type(self.call_numbers, CallNumber)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = DefTag.taginfo(level, Tag.SOUR, str(self.repo))
            if self.notes is not None:
                for note in self.notes:
                    lines = ''.join([lines, note.ged(level + 1)])
            if self.call_numbers is not None:
                for call_number in self.call_numbers:
                    lines = ''.join([lines, call_number.ged(level + 1)])
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

    xref: SourceXref = SourceXref(String.RECORD)
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
            DefCheck.verify_not_default(str(self.xref), String.RECORD)
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


class SNote(NamedTuple):
    """Use an already defined shared note in a GEDCOM structure.

    Example:
        If one has already defined a shared note record then one can reference it
        in a note substructure of a GEDCOM structure.  Here is an example of
        how that is done.  First, we will create a chronology to get a shared note
        reference id.  Then we will use it in a note.  The details of the note
        will not be included in the example.
        >>> from chronodata.build import Chronology
        >>> from chronodata.store import SNote
        >>> a = Chronology('illustrating shared notes usage')
        >>> sn = a.shared_note_xref()
        >>> referenced_sn = SNote(sn)
        >>> print(referenced_sn.ged(1))
        1 SNOTE @1@
        <BLANKLINE>

    Args:
        shared_note: the identifier of the shared note record.

    Returns:
        A GEDCOM string storing this data.

    Reference:
        [GEDCOM Note Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#NOTE_STRUCTURE)
    """

    shared_note: SharedNoteXref

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = DefCheck.verify_type(self.shared_note, SharedNoteXref)
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = DefTag.taginfo(level, Tag.SNOTE, str(self.shared_note))
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
        >>> note = Note('This is my note.')
        >>> print(note.ged(1))
        1 NOTE This is my note.
        <BLANKLINE>

        This example uses the Hebrew language translating "This is my note." as "זו ההערה שלי."
        The translation comes from [Google Translate](https://translate.google.com/?sl=en&tl=iw&text=This%20is%20my%20note.&op=translate).
        >>> hebrew_note = Note('זו ההערה שלי.', language='he')
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
        ...     'זו ההערה שלי.',
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
    """  # noqa: RUF002

    text: str = ''
    mime: MediaType = MediaType.NONE
    language: str = String.UNDETERMINED
    translations: Any = None
    citations: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_not_default(self.text, '')
            and DefCheck.verify_enum(self.mime.value, MediaType)
            # and DefCheck.verify_dict_key(self.language, Lang.CODE)
            and DefCheck.verify_tuple_type(self.translations, NoteTranslation)
            and DefCheck.verify_tuple_type(self.citations, SourceCitation)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = DefTag.taginfo(level, Tag.NOTE, self.text)
            if self.mime != MediaType.NONE:
                lines = ''.join(
                    [
                        lines,
                        DefTag.taginfo(level + 1, Tag.MIME, self.mime.value),
                    ]
                )
            if self.language != String.UNDETERMINED:
                lines = DefTag.str_to_str(lines, level + 1, Tag.LANG, self.language)
            if self.translations is not None:
                for translation in self.translations:
                    lines = ''.join([lines, translation.ged(level + 1)])
            if self.citations is not None:
                for citation in self.citations:
                    lines = ''.join([lines, citation.ged(level + 1)])
        return lines


class Association(NamedTuple):
    """_summary_

    Examples:


    Args:
        xref: the identifier of the individual in this association.
        role: the role of this individual.
        association_phrase: a description of the association.
        role_phrase: a description of the role.
        notes: a collection of notes related to this association.
        citations: a collection of citations related to this association.

    Returns:
        A GEDCOM string storing this data.
    """

    xref: IndividualXref
    role: Role = Role.NONE
    association_phrase: str = ''
    role_phrase: str = ''
    notes: Any = None
    citations: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_enum(self.role.value, Role)
            and DefCheck.verify_type(self.association_phrase, str)
            and DefCheck.verify_type(self.role_phrase, str)
            and DefCheck.verify_tuple_type(self.notes, Note)
            and DefCheck.verify_tuple_type(self.citations, SourceCitation)
            and DefCheck.verify_enum(self.role.value, Role)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            if self.association_phrase != '':
                lines = ''.join(
                    [
                        lines,
                        DefTag.taginfo(
                            level + 1,
                            Tag.PHRASE,
                            self.association_phrase,
                        ),
                    ]
                )
            lines = ''.join(
                [
                    lines,
                    DefTag.taginfo(level + 2, Tag.ROLE, self.role.value),
                ]
            )
            if self.role_phrase != '':
                lines = ''.join(
                    [
                        lines,
                        DefTag.taginfo(
                            level + 2,
                            Tag.PHRASE,
                            self.role_phrase,
                        ),
                    ]
                )
            for note in self.notes:
                lines = ''.join([lines, note.ged(1)])
            for citation in self.citations:
                lines = ''.join([lines, citation.ged(1)])
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


class PlaceTranslation(NamedTuple):
    """Store, validate and display a place translation.

    A place is a series of named regions in increasing order of size.  These regions
    are assigned a name.  By default, the regions are 'City', 'County', 'State' and
    'Country'.

    For the translations the forms are the same as for the original language, but
    the names of the regions are translated into a different language.

    Examples:


    Reference:
        [GEDCOM Place Translation](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PLAC-TRAN)
    """

    translation: str = ''
    language: str = String.UNDETERMINED

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = DefCheck.verify_type(
            self.translation, str
        ) and DefCheck.verify_type(self.language, str)
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = DefTag.str_to_str(lines, level, Tag.TRAN, self.translation)
            lines = DefTag.str_to_str(lines, level + 1, Tag.LANG, self.language)
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
            and DefCheck.verify_choice(self.north_south, Choice.NORTH_SOUTH)
            and DefCheck.verify_type(self.longitude, float)
            and DefCheck.verify_choice(self.east_west, Choice.EAST_WEST)
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

    A place is a dictionary of locations or regions going from smallest to largest.
    The default is an empty dictionary {'City': '', 'County': '', 'State': '', 'Country': ''}.
    One would fill in the values for city, county, state and country or assign other
    regions with their names if the default is not relevant.

    The BCP 47 language tag is a hyphenated list of subtags.  
    The [W3C Internationalization](https://www.w3.org/International/questions/qa-choosing-language-tags)
    guide will help one make a decision on which tags to use. 
    The [Language Subtag Lookup Tool](https://r12a.github.io/app-subtags/)
    can assist with finding and checking the language tag one would like to use.

    Example:
        Below are a couple of place names.  The first uses the default form names.
        The second alters some of the form names to fit the place and provides a translation
        from Czech to English.
        >>> from chronodata.store import Map, Place, PlaceTranslation
        >>> from chronodata.langs import Lang
        >>> bechyne_cs = 'Bechyně, okres Tábor, Jihočeský kraj, Česká republika'
        >>> bechyne_en = (
        ...     'Bechyně, Tábor District, South Bohemian Region, Czech Republic'
        ... )
        >>> place = Place(
        ...     place=bechyne_cs,
        ...     language='cs',
        ...     translations=[
        ...         PlaceTranslation(bechyne_en, 'en'),
        ...     ],
        ...     map=Map('N', 49.297222, 'E', 14.470833),
        ... )
        >>> place.validate()
        True
        >>> print(place.ged(2))
        2 PLAC Bechyně, okres Tábor, Jihočeský kraj, Česká republika
        3 FORM City, Country, State, Country
        3 LANG cs
        3 TRAN Bechyně, Tábor District, South Bohemian Region, Czech Republic
        4 LANG en
        3 MAP
        4 LATI N49.297222
        4 LONG E14.470833
        <BLANKLINE>


    Args:
        place_form: A dictionary representing the place from smallest to largest area.
        language: The BCP 47 langauage tag of the place names.
        translation: A list of translations of the place names.
        maps: A list of references to maps of the place.
        exid: Identifiers associated with the place.
        notes: Notes associated with the place.


    Reference:
        [W3C Internationalization](https://www.w3.org/International/questions/qa-choosing-language-tags)
        [Language Subtag Lookup Tool](https://r12a.github.io/app-subtags/)
        [GEDCOM Place Form](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PLAC-FORM)
        [GEDCOM Place Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PLACE_STRUCTURE)
    """

    place: str = ''
    form: str = 'City, Country, State, Country'
    language: str = String.UNDETERMINED
    translations: list[str] = []  # noqa: RUF012
    map: Map = Map('N', 90, 'E', 0)
    exids: list[Exid] = []  # noqa: RUF012
    notes: list[Note] = []  # noqa: RUF012

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.place, str)
            and DefCheck.verify_type(self.form, str)
            # and DefCheck.verify_dict_key(self.language, Lang.CODE)
            and DefCheck.verify_tuple_type(self.translations, PlaceTranslation)
            and DefCheck.verify_type(self.map, Map)
            and DefCheck.verify_tuple_type(self.exids, Exid)
            and DefCheck.verify_tuple_type(self.notes, Note)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = DefTag.str_to_str(lines, level, Tag.PLAC, self.place)
            lines = DefTag.str_to_str(lines, level + 1, Tag.FORM, self.form)
            lines = DefTag.str_to_str(lines, level + 1, Tag.LANG, self.language)
            lines = DefTag.list_to_str(lines, level + 1, self.translations)
            lines = ''.join([lines, self.map.ged(3)])
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

    Parameters
    ----------
    year


    Example
    -------
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

        if self.validate():
            day_str: str = (
                str(self.day) if self.day > 9 else ''.join(['0', str(self.day)])
            )
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
            output: str = f'{level} {Tag.DATE}'
            if self.day != 0:
                output = ''.join([output, f' {day_str}'])
            if self.month != 0:
                output = ''.join(
                    [
                        output,
                        f' {Cal.CALENDARS[calendar][Value.MONTH_NAMES][str(month_str)]}',
                    ]
                )
            if self.year != 0:
                output = ''.join([output, f' {year_str}\n'])
            return output
        return ''

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

        References
        ----------
        - [ISO 8601 Standard](https://www.iso.org/iso-8601-date-and-time-format.html)
        - [Wikipedia Overview](https://en.wikipedia.org/wiki/ISO_8601)
        """
        if self.validate():
            return f'{self.hour}:{self.minute}:{self.second}'
        return ''

        # def ged(self, level: int = 1) -> str:
        #     lines: str = ''
        #     if self.validate():
        #         pass
        #     return lines


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


# class DateTimeStatus(NamedTuple):
#     date: Date = Date(0, 0, 0)
#     time: Time = Time(0, 0, 0)
#     status: str = ''

#     def validate(self) -> bool:
#         check: bool = (
#             DefCheck.verify_type(self.status, str)
#             and self.date.validate()
#             and self.time.validate()
#         )
#         return check

# def ged(self, level: int = 1) -> str:
#     line: str = ''
#     if self.validate():
#         pass
#     return line


class EventDetail(NamedTuple):
    """

    Reference:
        [GEDCOM Event Detail](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#EVENT_DETAIL)"""

    date_value: DateValue | None = None
    place: Place | None = None
    address: Address = Address('', '', '', '', '')
    phones: Any = None
    emails: Any = None
    faxes: Any = None
    wwws: Any = None
    agency: str = ''
    religion: str = ''
    cause: str = ''
    resn: str = ''
    # sort_date: SortDate = ()
    associations: Any = None
    notes: Any = None
    sources: Any = None
    multimedia_links: Any = None
    uids: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = True
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            if self.date_value is not None:
                lines = ''.join([lines, self.date_value.ged(level)])
            if self.place is not None:
                lines = ''.join([lines, self.place.ged(level)])
            if self.address != Address('', '', '', '', ''):
                lines = ''.join([lines, self.address.ged(level)])
            contacts: str = DefTag.contact_info(
                level, self.phones, self.emails, self.faxes, self.wwws
            )
            lines = ''.join([lines, contacts])
            lines = DefTag.str_to_str(lines, level, Tag.AGNC, self.agency)
            lines = DefTag.str_to_str(lines, level, Tag.RELI, self.religion)
            lines = DefTag.str_to_str(lines, level, Tag.CAUS, self.cause)
            lines = DefTag.str_to_str(lines, level, Tag.RESN, self.resn)
            # if self.agency != '':
            #     lines = ''.join(
            #         [lines, DefTag.taginfo(level, Tag.AGNC, self.agency)]
            #     )
            # if self.religion != '':
            #     lines = ''.join(
            #         [lines, DefTag.taginfo(level, Tag.RELI, self.religion)]
            #     )
            # if self.cause != '':
            #     lines = ''.join(
            #         [lines, DefTag.taginfo(level, Tag.CAUS, self.cause)]
            #     )
            # if self.resn != '':
            #     lines = ''.join(
            #         [lines, DefTag.taginfo(level, Tag.RESN, self.resn)]
            #     )
            lines = DefTag.list_to_str(lines, level, self.associations)
            lines = DefTag.list_to_str(lines, level, self.notes)
            lines = DefTag.list_to_str(lines, level, self.sources)
            lines = DefTag.list_to_str(lines, level, self.multimedia_links)
            lines = DefTag.list_to_str(lines, level, self.uids)
            # if self.associations is not None:
            #     for association in self.associations:
            #         lines = ''.join([lines, association.ged(level)])
            # if self.notes is not None:
            #     for note in self.notes:
            #         lines = ''.join([lines, note.ged(level)])
            # if self.sources is not None:
            #     for source in self.sources:
            #         lines = ''.join([lines, source.ged(level)])
            # if self.multimedia_links is not None:
            #     for link in self.multimedia_links:
            #         lines = ''.join([lines, link.ged(level)])
            # if self.uids is not None:
            #     for uid in self.uids:
            #         lines = ''.join([lines, uid.ged(level)])

        return lines


class HusbandWife(NamedTuple):
    husband_age: int = 0
    wife_age: int = 0
    husband_phrase: str = ''
    wife_phrase: str = ''
    event_detail: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.husband_age, int)
            and DefCheck.verify_type(self.wife_age, int)
            and DefCheck.verify_type(self.husband_phrase, str)
            and DefCheck.verify_type(self.wife_phrase, str)
            and DefCheck.verify_type(self.event_detail, EventDetail)
        )
        return check

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        if self.validate():
            pass
        return ''


class FamilyEventDetail(NamedTuple):
    husband_wife_ages: HusbandWife

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = DefCheck.verify_type(self.husband_wife_ages, HusbandWife)
        return check

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
        return lines


class FamilyAttribute(NamedTuple):
    tag: str
    attribute_type: str = ''
    family_event_detail: FamilyEventDetail | None = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.tag, str)
            and DefCheck.verify_type(self.attribute_type, str)
            and DefCheck.verify_type(
                self.family_event_detail, FamilyEventDetail | None
            )
        )
        return check

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
        return lines


class FamilyEvent(NamedTuple):
    event: str = ''
    event_type: str = ''
    event_detail: FamilyEventDetail | None = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.event, str)
            and DefCheck.verify_type(self.event_type, str)
            and DefCheck.verify_type(
                self.event_detail, FamilyEventDetail | None
            )
        )
        return check

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
        return lines


class Husband(NamedTuple):
    xref: IndividualXref = IndividualXref(String.RECORD)
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
        if str(self.xref) != String.RECORD and self.validate():
            lines = ''.join(
                [lines, DefTag.taginfo(level, Tag.HUSB, str(self.xref))]
            )
            if self.phrase != '':
                lines = ''.join(
                    [
                        lines,
                        DefTag.taginfo(level + 1, Tag.PHRASE, self.phrase),
                    ]
                )
        return lines


class Wife(NamedTuple):
    xref: IndividualXref = IndividualXref(String.RECORD)
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
        if str(self.xref) != String.RECORD and self.validate():
            lines = ''.join(
                [lines, DefTag.taginfo(level, Tag.WIFE, str(self.xref))]
            )
            if self.phrase != '':
                lines = ''.join(
                    [
                        lines,
                        DefTag.taginfo(level + 1, Tag.PHRASE, self.phrase),
                    ]
                )
        return lines


class Child(NamedTuple):
    xref: IndividualXref = IndividualXref(String.RECORD)
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
        if str(self.xref) != String.RECORD and self.validate():
            lines = ''.join(
                [lines, DefTag.taginfo(level, Tag.CHIL, str(self.xref))]
            )
            if self.phrase != '':
                lines = ''.join(
                    [
                        lines,
                        DefTag.taginfo(level + 1, Tag.PHRASE, self.phrase),
                    ]
                )
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
    event_detail: EventDetail
    age: Age = Age(0, 0, 0, 0, '', '')
    phrase: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.event_detail, EventDetail)
            and DefCheck.verify_type(self.age, str)
            and DefCheck.verify_type(self.phrase, str)
        )
        return check

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
        return lines


class IndividualAttribute(NamedTuple):
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
    tag: str
    tag_type: str = ''
    event_detail: IndividualEventDetail | None = None
    family_child: str = ''
    adoption: str = ''
    phrase: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.tag, str)
            and DefCheck.verify_type(self.tag_type, str)
            and DefCheck.verify_type(
                self.event_detail, IndividualEventDetail | None
            )
            and DefCheck.verify_type(self.family_child, str)
            and DefCheck.verify_type(self.adoption, str)
            and DefCheck.verify_type(self.phrase, str)
        )
        return check

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
        return lines


class Alias(NamedTuple):
    xref: str
    phrase: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = DefCheck.verify_type(
            self.xref, str
        ) and DefCheck.verify_type(self.phrase, str)
        return check

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
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
    """Generate a GEDCOM Family Record.

    Parameters:

    - `xref`: typed string obtained by running `chrono.family_xref()`.
    - `resn`: restriction codes with the default being no restriction.
    - `attributes`: a tuple of type Attribute.
    """

    xref: FamilyXref = FamilyXref(String.RECORD)
    resn: Resn = Resn.NONE
    attributes: Any = None
    events: Any = None
    husband: Husband = Husband(IndividualXref(String.RECORD), '')
    wife: Wife = Wife(IndividualXref(String.RECORD), '')
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

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged(0)
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
            if self.husband != Husband(IndividualXref(String.RECORD), ''):
                lines = ''.join([lines, self.husband.ged(level)])
            if self.wife != Wife(IndividualXref(String.RECORD), ''):
                lines = ''.join([lines, self.wife.ged(level)])
            if self.children is not None:
                for child in self.children:
                    lines = ''.join([lines, child.ged(level)])
            if self.associations is not None:
                for association in self.associations:
                    lines = ''.join([lines, association.ged(level)])
            if self.submitters is not None:
                for submitter in self.submitters:
                    lines = ''.join(
                        [lines, DefTag.taginfo(level, Tag.SUBM, submitter)]
                    )
            if self.lds_spouse_sealings is not None:
                for sealing in self.lds_spouse_sealings:
                    lines = ''.join([lines, sealing.ged(level)])
            if self.identifiers is not None:
                for identifier in self.identifiers:
                    lines = ''.join([lines, identifier.ged(level)])
            if self.notes is not None:
                for note in self.notes:
                    lines = ''.join([lines, note.ged(level)])
            if self.citations is not None:
                for citation in self.citations:
                    lines = ''.join([lines, citation.ged(level)])
            if self.multimedia_links is not None:
                for multimedia_link in self.multimedia_links:
                    lines = ''.join([lines, multimedia_link.ged(level)])
        return lines


class Individual(NamedTuple):
    xref: IndividualXref = IndividualXref(String.RECORD)
    resn: Resn = Resn.NONE
    personal_names: Any = None
    sex: Sex = Sex.NONE
    attributes: Any = None
    events: Any = None
    lds_individual_ordinances: Any = None
    families_child: Any = None
    submitters: Any = None
    associations: Any = None
    aliases: Any = None
    ancestor_interest: Any = None
    descendent_interest: Any = None
    identifiers: Any = None
    notes: Any = None
    sources: Any = None
    multimedia_links: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            DefCheck.verify_type(self.xref, IndividualXref)
            and DefCheck.verify_enum(self.resn.value, Resn)
            and DefCheck.verify_tuple_type(
                self.personal_names, PersonalNamePiece
            )
            and DefCheck.verify_enum(self.sex.value, Sex)
            and DefCheck.verify_tuple_type(self.attributes, IndividualAttribute)
            and DefCheck.verify_tuple_type(self.events, IndividualEvent)
            and DefCheck.verify_tuple_type(
                self.lds_individual_ordinances, LDSIndividualOrdinances
            )
            and DefCheck.verify_tuple_type(self.families_child, FamilyChild)
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

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged(0)
        if self.validate():
            pass
        return lines


class Multimedia(NamedTuple):
    xref: MultimediaXref = MultimediaXref(String.RECORD)
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

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged(0)
        if self.validate():
            pass
        return lines


class Repository(NamedTuple):
    xref: RepositoryXref = RepositoryXref(String.RECORD)
    name: str = ''
    address: Address | None = None
    phones: Any = None
    emails: Any = None
    faxes: Any = None
    wwws: Any = None
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

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged(0)
        if self.validate():
            pass
        return lines


class SharedNote(NamedTuple):
    xref: SharedNoteXref = SharedNoteXref(String.RECORD)
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

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged(0)
        if self.validate():
            pass
        return lines


class Source(NamedTuple):
    xref: SourceXref = SourceXref(String.RECORD)
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

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged(0)
        if self.validate():
            pass
        return lines


class Submitter(NamedTuple):
    xref: SubmitterXref = SubmitterXref(String.RECORD)
    name: str = ''
    address: Address | None = None
    phones: Any = None
    emails: Any = None
    faxes: Any = None
    wwws: Any = None
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

    def ged(self, level: int = 1) -> str:  # noqa: ARG002
        """Format to meet GEDCOM standards."""
        lines: str = self.xref.ged(0)
        if str(self.xref) != String.RECORD and self.validate():
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
            and DefCheck.verify_enum(self.tag.value, Choice.EXTENSION_TAG)
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
    address: Any = None
    phones: Any = None
    emails: Any = None
    faxes: Any = None
    wwws: Any = None
    data: str = ''
    dest: str = ''
    date: Date = Date(0, 0, 0)
    time: Time = Time(0, 0, 0)
    copr: str = ''
    language: str = ''
    place: Any = None
    note: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = True
        return check

    def ged(self, level: int = 0) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''.join(
            [
                DefTag.taginfo(level, Tag.HEAD),
                DefTag.taginfo(level + 1, Tag.GEDC),
                DefTag.taginfo(level + 2, Tag.VERS, String.VERSION),
            ]
        )
        if self.schemas is not None:
            lines = DefTag.empty_to_str(lines, level + 1, Tag.SCHMA)
            #lines = DefTag.list_to_str(lines, level + 1, Tag.TAG, self.schemas)
        return lines  
