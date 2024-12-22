# Licensed under a 3-clause BSD style license - see LICENSE.md
"""NamedTuples to build a chronology based on the GEDCOM standard."""

import logging
from typing import Any, NamedTuple

from chronodata.constants import Cal, GEDSpecial, Nul, Value
from chronodata.enums import (
    Adop,
    ApproxDate,
    EvenAttr,
    Event,
    FamAttr,
    FamcStat,
    FamEven,
    GreaterLessThan,
    Id,
    IndiAttr,
    IndiEven,
    Medi,
    MediaType,
    NameType,
    Pedi,
    PersonalNamePieceTag,
    Quay,
    RangeDate,
    Record,
    Resn,
    RestrictDate,
    Role,
    Sex,
    Stat,
    Tag,
)
from chronodata.langs import Lang
from chronodata.messages import Msg
from chronodata.methods import Defs
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
    """Add address information.

    Args:
        - address (str): Each line of the mailing label is separated by `\n`.
        - city (str): The city or and empty string to leave this blank.
        - state (str): The state or an empty string to leave this blank.
        - postal (str): The postal code or an empty string to leave this blank.
        - country (str): The country or an empty string to leave this blank.

    Example:
        The following is the minimum amount of information for an address.
        >>> from chronodata.tuples import Address
        >>> mailing_address = Address(
        ...     ['12345 ABC Street', 'South North City, My State 23456']
        ... )
        >>> print(mailing_address.ged(1))
        1 ADDR 12345 ABC Street
        1 CONT South North City, My State 23456
        <BLANKLINE>

        There are five named strings stored in this NamedTuple.
        >>> from chronodata.tuples import Address
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

        Lines with empty ('') strings are moved.
        >>> from chronodata.tuples import Address
        >>> blanks_address = Address(
        ...     [
        ...         '',
        ...         '',
        ...         '12345 ABC Street',
        ...         '',
        ...         '',
        ...         'South North City, My State 23456',
        ...         '',
        ...     ]
        ... )
        >>> print(blanks_address.ged(1))
        1 ADDR 12345 ABC Street
        1 CONT South North City, My State 23456
        <BLANKLINE>

        One can also merely validate that the values stored can be displayed.
        >>> blanks_address.validate()
        True


    Reference:
        - [GEDCOM Specifications](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#substructures)
    """

    address: Any = None
    city: str = ''
    state: str = ''
    postal: str = ''
    country: str = ''

    def validate(self) -> bool:
        check: bool = (
            Defs.verify_type(self.address, list)
            and Defs.verify_type(self.city, str)
            and Defs.verify_type(self.state, str)
            and Defs.verify_type(self.postal, str)
            and Defs.verify_type(self.country, str)
        )
        return check

    def ged(self, level: int = 1) -> str | None:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate() and self.address != []:
            filtered_address: list[str] = list(filter(None, self.address))
            if len(filtered_address) > 0:
                lines = ''.join(
                    [
                        lines,
                        Defs.taginfo(
                            level,
                            Tag.ADDR,
                            filtered_address[0],
                        ),
                    ]
                )
                for line in filtered_address[1:]:
                    lines = ''.join(
                        [
                            lines,
                            Defs.taginfo(level, Tag.CONT, line),
                        ]
                    )
            if self.city != '':
                lines = ''.join(
                    [lines, Defs.taginfo(level + 1, Tag.CITY, self.city)]
                )
            if self.state != '':
                lines = ''.join(
                    [
                        lines,
                        Defs.taginfo(level + 1, Tag.STAE, self.state),
                    ]
                )
            if self.postal != '':
                lines = ''.join(
                    [
                        lines,
                        Defs.taginfo(
                            level + 1,
                            Tag.POST,
                            self.postal
                        ),
                    ]
                )
            if self.country != '':
                lines = ''.join(
                    [
                        lines,
                        Defs.taginfo(
                            level + 1,
                            Tag.CTRY,
                            self.country
                        ),
                    ]
                )
        return lines


class Age(NamedTuple):
    """Implement the Age data type in the GEDCOM specification.

    Args:
        - greater_less_than
        The default is '', which means that the age is exact
        to the day.  The option `>` means that the actual age
        is greater than the one provided.  The option `<` means
        that the actual age is less than the one provided.
        - years
        The number of whole years in the age. The specification
        requires this to be rounded down.  Here an error is thrown
        if an integer is not used. One can add information in the
        phrase parameter to clarify the year.
        - months
        The number of months in addition to the years. The specification
        requires this to be rounded down.  Here an error is thrown
        if an integer is not used. One can add information in the
        phrase parameter to clarify the year.
        - weeks
        The number of weeks in addition to the years and months.
        The specification
        requires this to be rounded down.  Here an error is thrown
        if an integer is not used. One can add information in the
        phrase parameter to clarify the year.
        - days
        The number of days in addition to any years, months, or weeks provided.
        The specification requires this to be rounded down.  Here an error is thrown
        if an integer is not used. One can add information in the
        phrase parameter to clarify the year.

    The default values for these parameters is 0 for the integers and '' for the
    strings.

    Exceptions:
        - If greater_less_than is not one of {'', '<', '>'} a ValueError will be issued.
        - If any value (except `phrase`) is not an integer, a ValueError will be issued.
        - If any value (except `phrase`) is less than 0, a ValueError will be issued.

    Examples:
        >>> from chronodata.tuples import Age
        >>> from chronodata.enums import GreaterLessThan
        >>> print(
        ...     Age(
        ...         10,
        ...         greater_less_than=GreaterLessThan.GREATER,
        ...         phrase='Estimated',
        ...     ).ged(1)
        ... )
        1 AGE > 10y
        2 PHRASE Estimated
        <BLANKLINE>
        >>> print(Age(10, 2, 1, 2).ged(2))
        2 AGE 10y 2m 1w 2d
        <BLANKLINE>

    Reference:
        [GEDCOM Specification](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#age)
    """

    years: int = 0
    months: int = 0
    weeks: int = 0
    days: int = 0
    greater_less_than: GreaterLessThan = GreaterLessThan.EQUAL
    phrase: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Defs.verify_enum(self.greater_less_than.value, GreaterLessThan)
            and Defs.verify_type(self.years, int)
            and Defs.verify_type(self.months, int)
            and Defs.verify_type(self.weeks, int)
            and Defs.verify_type(self.days, int)
            and Defs.verify_type(self.phrase, str)
            and Defs.verify_not_negative(self.years)
            and Defs.verify_not_negative(self.months)
            and Defs.verify_not_negative(self.weeks)
            and Defs.verify_not_negative(self.days)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format the GEDCOM Age data type."""
        line: str = ''
        info: str = self.greater_less_than.value
        if self.validate():
            if self.years > 0:
                info = ''.join([info, f' {self.years!s}y'])
            if self.months > 0:
                info = ''.join([info, f' {self.months!s}m'])
            if self.weeks > 0:
                info = ''.join([info, f' {self.weeks!s}w'])
            if self.days > 0:
                info = ''.join([info, f' {self.days!s}d'])
            line = Defs.taginfo(
                level,
                Tag.AGE,
                info.replace('  ', ' ').replace('  ', ' ').strip(),
            )
            if self.phrase != '':
                line = ''.join(
                    [line, Defs.taginfo(level + 1, Tag.PHRASE, self.phrase)]
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


    Args:
        tag (PersonalNamePieceTag): One of six tags used for a personal name pieces.
        text (str): The string value associated with that tag.


    Example:
        This example includes all six of the Personal Name Piece tags.
        >>> from chronodata.tuples import PersonalNamePiece
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
        ValueError: The value "NAME" is not in the <enum 'PersonalNamePieceTag'> enumeration.

        The error in the above example did not occur immediately, but one had to
        attempt to use the NamedTuple by displaying it as a GEDCOM line.  One could
        also run the `validate` method on `bad piece` to trigger the error.  This
        method is called by `ged` prior to displaying the GEDCOM line.
        >>> bad_piece.validate()
        Traceback (most recent call last):
        ValueError: The value "NAME" is not in the <enum 'PersonalNamePieceTag'> enumeration.

    Reference:
        [GEDCOM Personal Name Pieces](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PERSONAL_NAME_PIECES)
    """

    tag: PersonalNamePieceTag = PersonalNamePieceTag.NONE
    text: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = Defs.verify_enum(
            self.tag.value, PersonalNamePieceTag
        ) and Defs.verify_type(self.text, str)
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        name_piece: str = ''
        if self.validate():
            name_piece = Defs.taginfo(
                level, self.tag, self.text
            )
        return name_piece


class PersonalName(NamedTuple):
    """Store, validate and display a personal name.

    Args:
        name (str): the person's name.
        type (str): the type of name. There are seven types to choose from:
            - NameType.AKA or also known as.
            - NameType.BIRTH or birth name.
            - NameType.IMMIGRANT or immigrant name.
            - NameType.MAIDEN or maiden name.
            - NameType.MARRIED or married name.
            - NameType.PROFESSIONAL or professional name
            - NameType.OTHER or another type not listed above.
        phrase (str): a place for uncategorized information about the name.
        pieces (tuple[PersonNamePieces]): an alternate way to split the name.
        translations (tuple[NameTranslation]): an optional tuple of translations of the name.
        notes (tuple[Note]): a tuple of optional notes regarding the name.
        sources (tuple[SourceCitation]): a tuple of citations regarding the name.

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
        >>> from chronodata.tuples import (
        ...     NameTranslation,
        ...     Note,
        ...     PersonalName,
        ...     PersonalNamePiece,
        ...     SourceCitation,
        ... )
        >>> from chronodata.enums import NameType, PersonalNamePieceTag
        >>> adam_note = Note('Here is a place to add more information.')
        >>> adam_nickname = PersonalNamePiece(PersonalNamePieceTag.NICK, 'הָֽאָדָ֖ם')
        >>> adam_english = NameTranslation('Adam', 'English')
        >>> adam_english_nickname = NameTranslation('the man', 'English')
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


    Reference:
        [GEDCOM Person Name Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PERSONAL_NAME_STRUCTURE)
    """

    name: str = ''
    type: NameType = NameType.NONE
    phrase: str = ''
    pieces: Any = None
    translations: Any = None
    notes: Any = None
    sources: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Defs.verify_not_default(self.name, '')
            and Defs.verify_enum(self.type.value, NameType)
            and Defs.verify_type(self.phrase, str)
            and Defs.verify_tuple_type(self.pieces, PersonalNamePiece)
            and Defs.verify_tuple_type(self.translations, NameTranslation)
            and Defs.verify_tuple_type(self.notes, Note)
            and Defs.verify_tuple_type(self.sources, SourceCitation)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = ''.join(
                [
                    Defs.taginfo(level, Tag.NAME, self.name),
                    Defs.taginfo(level + 1, Tag.TYPE, self.type.value),
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

    Args:
        translation (str): the text of the translation.
        language (str): the name of the language.
        name_pieces (tuple): an optional tuple of PersonalNamePieces.

    Example:
        In this example, the name "Joe" will be translated as "喬" in Chinese.
        Although the `ged` method to display preforms a validation first,
        this example will show that and then display the data using
        the GEDCOM standard.  No personal name pieces will be displayed.
        >>> from chronodata.tuples import NameTranslation
        >>> joe_in_chinese = '喬'
        >>> language = 'Chinese'
        >>> nt = NameTranslation(joe_in_chinese, language)
        >>> nt.validate()
        True
        >>> print(nt.ged(1))
        1 TRAN 喬
        2 LANG zh
        <BLANKLINE>

    Reference:
        [GEDCOM Pesonal Name Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PERSONAL_NAME_STRUCTURE)
    """

    translation: str = ''
    language: str = ''
    name_pieces: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Defs.verify_type(self.translation, str)
            and Defs.verify_not_default(self.translation, '')
            and Defs.verify_dict_key(self.language, Lang.CODE)
            and Defs.verify_not_default(self.language, '')
            and Defs.verify_tuple_type(self.name_pieces, PersonalNamePiece)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = ''.join(
                [
                    Defs.taginfo(
                        level, Tag.TRAN, self.translation
                    ),
                    Defs.taginfo(level + 1, Tag.LANG, Lang.CODE[self.language]),
                ]
            )
            if self.name_pieces is not None:
                for piece in self.name_pieces:
                    lines = ''.join([lines, piece.ged(level + 1)])
        return lines


class NoteTranslation(NamedTuple):
    """Store, validate and display the optional note tranlation section of
    the GEDCOM Note Structure.

    Example:
        This example will translation "This is a note." into the Arabic "هذه ملاحظة.".
        >>> from chronodata.tuples import NoteTranslation
        >>> from chronodata.enums import MediaType
        >>> arabic_text = 'هذه ملاحظة.'
        >>> mime = MediaType.TEXT_HTML
        >>> language = 'Arabic'
        >>> nt = NoteTranslation(arabic_text, mime, language)
        >>> nt.validate()
        True
        >>> print(nt.ged(1))
        1 TRAN هذه ملاحظة.
        2 MIME TEXT_HTML
        2 LANG ar
        <BLANKLINE>

    Args:
        translation (str): the text of the translation for the note.
        mime (str): the mime type of the translation.
        language (str): the language of the translation.

    Example

    Reference:
        [GEDCOM Note Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#NOTE_STRUCTURE)]
    """

    translation: str = ''
    mime: MediaType = MediaType.NONE
    language: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Defs.verify_type(self.translation, str)
            and Defs.verify_not_default(self.translation, '')
            and Defs.verify_enum(self.mime.value, MediaType)
            and Defs.verify_dict_key(self.language, Lang.CODE)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = ''.join(
                [
                    lines,
                    Defs.taginfo(
                        level, Tag.TRAN, self.translation
                    ),
                    Defs.taginfo(level + 1, Tag.MIME, self.mime.value),
                    Defs.taginfo(level + 1, Tag.LANG, Lang.CODE[self.language]),
                ]
            )
        return lines


class CallNumber(NamedTuple):
    """Store, validate and display the option call numbers for the
    SourceRepositoryCitation substructure.

    Example:
        This example assumes there is a call number "1111" which is the
        minimal amount of information needed to use this optional feature.
        >>> from chronodata.tuples import CallNumber
        >>> cn = CallNumber('1111')
        >>> cn.validate()
        True
        >>> print(cn.ged(1))
        1 CALN 1111
        <BLANKLINE>

        This next example uses all of the optional positions.
        >>> from chronodata.enums import Medi
        >>> cn_all = CallNumber('1111', Medi.BOOK, 'New Testament')
        >>> print(cn_all.ged(1))
        1 CALN 1111
        2 MEDI BOOK
        3 PHRASE New Testament
        <BLANKLINE>

    See Also:
        `SourceRepositoryCitation`: the superstructure of this NamedTuple.

    """

    call_number: str = ''
    medi: Medi = Medi.NONE
    phrase: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Defs.verify_type(self.call_number, str)
            and Defs.verify_not_default(self.call_number, '')
            and Defs.verify_enum(self.medi.value, Medi)
            and Defs.verify_type(self.phrase, str)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Defs.taginfo(
                level, Tag.CALN, self.call_number
            )
            if self.medi != Medi.NONE:
                lines = ''.join(
                    [lines, Defs.taginfo(level + 1, Tag.MEDI, self.medi.value)]
                )
            if self.phrase != '':
                lines = ''.join(
                    [
                        lines,
                        Defs.taginfo(
                            level + 2, Tag.PHRASE, self.phrase
                        ),
                    ]
                )
        return lines


class SourceRepositoryCitation(NamedTuple):
    """Store, validate and display the optional Source Repository Citation
     substructure of the GEDCOM standard.

    Args:
        repo (RepositoryXref): the reference identifier for the repository.
        notes (tuple[Note]): a tuple of Notes.
        call_numbers (tuple[CallNumber]): a tuple of call numbers.

    Reference:
        [GEDCOM Source Repository Citation](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_REPOSITORY_CITATION)
    """

    repo: RepositoryXref
    notes: Any = None
    call_numbers: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Defs.verify_type(self.repo, RepositoryXref)
            and Defs.verify_not_default(self.repo, RepositoryXref(Nul.RECORD))
            and Defs.verify_tuple_type(self.notes, Note)
            and Defs.verify_type(self.call_numbers, CallNumber)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Defs.taginfo(level, Tag.SOUR, str(self.repo))
            if self.notes is not None:
                for note in self.notes:
                    lines = ''.join([lines, note.ged(level + 1)])
            if self.call_numbers is not None:
                for call_number in self.call_numbers:
                    lines = ''.join([lines, call_number.ged(level + 1)])
        return lines


class Text(NamedTuple):
    text: str = ''
    mime: MediaType = MediaType.NONE
    language: str = ''


class SourceData(NamedTuple):
    date_value: str = ''
    texts: Any = None


class SourceCitation(NamedTuple):
    """Store, validate and display the Source Citation
     substructure of the GEDCOM standard.

    Args:
        xref (SourceXref): the source identifier
        page (str):

    Reference:
        [GEDCOM Source Citation](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_CITATION)
    """

    xref: SourceXref = SourceXref(Nul.RECORD)
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
            Defs.verify_not_default(str(self.xref), Nul.RECORD)
            and Defs.verify_type(self.xref, SourceXref)
            and Defs.verify_type(self.page, str)
            and Defs.verify_tuple_type(self.texts, Text)
            and Defs.verify_enum(self.event.value, Event)
            and Defs.verify_type(self.phrase, str)
            and Defs.verify_enum(self.role.value, Role)
            and Defs.verify_type(self.role_phrase, str)
            and Defs.verify_enum(self.quality.value, Quay)
            and Defs.verify_tuple_type(self.multimedia, MultimediaLink)
            and Defs.verify_tuple_type(self.notes, Note)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Defs.taginfo(level, Tag.SOUR, str(self.xref))
            if self.page != '':
                lines = Defs.taginfo(level + 1, Tag.PAGE, self.page)

        return lines


class SNote(NamedTuple):
    """Use an already defined shared note in a GEDCOM structure.

    Args:
        shared_note (SharedNoteXref): the identifier of the shared note record.

    Example:
        If one has already defined a shared note record then one can reference it
        in a note substructure of a GEDCOM structure.  Here is an example of
        how that is done.  First, we will create a chronology to get a shared note
        reference id.  Then we will use it in a note.  The details of the note
        will not be included in the example.
        >>> from chronodata.build import Chronology
        >>> from chronodata.tuples import SNote
        >>> a = Chronology('illustrating shared notes usage')
        >>> sn = a.shared_note_xref()
        >>> referenced_sn = SNote(sn)
        >>> print(referenced_sn.ged(1))
        1 SNOTE @1@
        <BLANKLINE>

    Reference:
        [GEDCOM Note Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#NOTE_STRUCTURE)
    """

    shared_note: SharedNoteXref

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = Defs.verify_type(self.shared_note, SharedNoteXref)
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Defs.taginfo(level, Tag.SNOTE, str(self.shared_note))
        return lines


class Note(NamedTuple):
    """Store, validate and display a note substructure of the GEDCOM standard.

    Args:
        text (str): the text of the note.
        mime (str): the optional media type of the note.
        language (str): the optional language used in the note.
        translations (tuple): an optional tuple of translations of the text.
        citations (tuple): an optional tuple of translations of the text.

    Example:
        This example is a note without other information.
        >>> from chronodata.tuples import Note
        >>> note = Note('This is my note.')
        >>> print(note.ged(1))
        1 NOTE This is my note.
        <BLANKLINE>

        This example uses the Hebrew language translating "This is my note." as "זו ההערה שלי."
        The translation comes from [Google Translate](https://translate.google.com/?sl=en&tl=iw&text=This%20is%20my%20note.&op=translate).
        >>> hebrew_note = Note('זו ההערה שלי.', language='Hebrew')
        >>> print(hebrew_note.ged(1))
        1 NOTE זו ההערה שלי.
        2 LANG he
        <BLANKLINE>

        The next example adds translations of the previous example to the note.
        >>> from chronodata.enums import MediaType
        >>> english_translation = NoteTranslation(
        ...     'This is my note.', MediaType.TEXT_PLAIN, 'English'
        ... )
        >>> urdu_translation = NoteTranslation(
        ...     'یہ میرا نوٹ ہے۔', MediaType.TEXT_PLAIN, 'Urdu'
        ... )
        >>> hebrew_note_with_translations = Note(
        ...     'זו ההערה שלי.',
        ...     language='Hebrew',
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


    Reference:
        [GEDCOM Note Structure](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#NOTE_STRUCTURE)
    """

    text: str = ''
    mime: MediaType = MediaType.NONE
    language: str = ''
    translations: Any = None
    citations: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Defs.verify_not_default(self.text, '')
            and Defs.verify_enum(self.mime.value, MediaType)
            and Defs.verify_dict_key(self.language, Lang.CODE)
            and Defs.verify_tuple_type(self.translations, NoteTranslation)
            and Defs.verify_tuple_type(self.citations, SourceCitation)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            lines = Defs.taginfo(level, Tag.NOTE, self.text)
            if self.mime != MediaType.NONE:
                lines = ''.join(
                    [lines, Defs.taginfo(level + 1, Tag.MIME, self.mime.value)]
                )
            if self.language != '':
                lines = ''.join(
                    [
                        lines,
                        Defs.taginfo(
                            level + 1, Tag.LANG, Lang.CODE[self.language]
                        ),
                    ]
                )
            if self.translations is not None:
                for translation in self.translations:
                    lines = ''.join([lines, translation.ged(level + 1)])
            if self.citations is not None:
                for citation in self.citations:
                    lines = ''.join([lines, citation.ged(level + 1)])
        return lines


class Association(NamedTuple):
    xref: IndividualXref
    role: Role = Role.NONE
    association_phrase: str = ''
    role_phrase: str = ''
    notes: Any = None
    citations: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Defs.verify_enum(self.role.value, Role)
            and Defs.verify_type(self.association_phrase, str)
            and Defs.verify_type(self.role_phrase, str)
            and Defs.verify_tuple_type(self.notes, Note)
            and Defs.verify_tuple_type(self.citations, SourceCitation)
            and Defs.verify_enum(self.role.value, Role)
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
                        Defs.taginfo(
                            level + 1,
                            Tag.PHRASE,
                            self.association_phrase,
                        ),
                    ]
                )
            lines = ''.join(
                [
                    lines,
                    Defs.taginfo(level + 2, Tag.ROLE, self.role.value),
                ]
            )
            if self.role_phrase != '':
                lines = ''.join(
                    [
                        lines,
                        Defs.taginfo(
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
    crop: str = ''
    top: int = 0
    left: int = 0
    height: int = 0
    width: int = 0
    title: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Defs.verify_type(self.crop, str)
            and Defs.verify_type(self.top, int)
            and Defs.verify_type(self.left, int)
            and Defs.verify_type(self.height, int)
            and Defs.verify_type(self.width, int)
            and Defs.verify_type(self.title, str)
        )
        return check

    def ged(self, level: int = 1) -> str:
        lines: str = ''
        if self.validate():
            pass
        return lines


class Exid(NamedTuple):
    exid: str
    exid_type: str

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = Defs.verify_type(self.exid, str) and Defs.verify_type(
            self.exid_type, str
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        return ''.join(
            [
                Defs.taginfo(level, Tag.EXID, self.exid),
                Defs.taginfo(level + 1, Tag.TYPE, self.exid_type),
            ]
        )


class PlaceTranslation(NamedTuple):
    text: str
    language: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = Defs.verify_type(self.text, str) and Defs.verify_type(
            self.language, str
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
        return lines


class Map(NamedTuple):
    latitude: float
    longitude: float

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = Defs.verify_type(
            self.latitude, float
        ) and Defs.verify_type(self.longitude, float)
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
        return lines


class Place(NamedTuple):
    text: str
    form: str = ''
    language: str = ''
    translations: Any = None
    maps: Any = None
    exids: Any = None
    notes: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Defs.verify_type(self.text, str)
            and Defs.verify_type(self.form, str)
            and Defs.verify_tuple_type(self.translations, PlaceTranslation)
            and Defs.verify_tuple_type(self.maps, Map)
            and Defs.verify_tuple_type(self.exids, Exid)
            and Defs.verify_tuple_type(self.notes, Note)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
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
            Defs.verify_type(self.year, int)
            and Defs.verify_type(self.month, int)
            and Defs.verify_type(self.day, int)
            and Defs.verify_type(self.week, int)
            and Defs.verify_range(self.week, 0, 52)
            and Defs.verify_range(self.month, 0, 12)
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

    def iso(self) -> str | None:
        """Return the validated ISO format for the date.

        References
        ----------
        - [ISO 8601 Standard](https://www.iso.org/iso-8601-date-and-time-format.html)
        - [Wikipedia Overview](https://en.wikipedia.org/wiki/ISO_8601)
        """
        if self.validate():
            return f'{self.year}-{self.month}-{self.day}'
        return None


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
            Defs.verify_type(self.hour, int)
            and Defs.verify_type(self.minute, int)
            and Defs.verify_type(self.second, int | float)
            and Defs.verify_type(self.UTC, bool)
            and Defs.verify_range(self.hour, 0, 23)
            and Defs.verify_range(self.minute, 0, 59)
            and Defs.verify_range(self.second, 0, 59.999999999999)
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
            return Defs.taginfo(
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
            Defs.verify_type(self.phrase, str)
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
                    [lines, Defs.taginfo(level + 1, Tag.PHRASE, self.phrase)]
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
            Defs.verify_type(self.phrase, str)
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
                    [lines, Defs.taginfo(level + 1, Tag.PHRASE, self.phrase)]
                )
        return lines


# class DateTimeStatus(NamedTuple):
#     date: Date = Date(0, 0, 0)
#     time: Time = Time(0, 0, 0)
#     status: str = ''

#     def validate(self) -> bool:
#         check: bool = (
#             Defs.verify_type(self.status, str)
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
    date_value: DateValue | None = None
    place: Place | None = None
    address: Address | None = None
    phones: tuple[str] | None = None
    emails: tuple[str] | None = None
    faxes: tuple[str] | None = None
    wwws: tuple[str] | None = None
    agency: str = ''
    religion: str = ''
    cause: str = ''
    resn: str = ''
    # sort_date: SortDate = ()
    associations: tuple[Association] | None = None
    notes: tuple[Note] | None = None
    sources: tuple[SourceCitation] | None = None
    multimedia_links: tuple[MultimediaLink] | None = None
    utd: tuple[str] | None = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = True
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
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
            Defs.verify_type(self.husband_age, int)
            and Defs.verify_type(self.wife_age, int)
            and Defs.verify_type(self.husband_phrase, str)
            and Defs.verify_type(self.wife_phrase, str)
            and Defs.verify_type(self.event_detail, EventDetail)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        if self.validate():
            pass
        return ''


class FamilyEventDetail(NamedTuple):
    husband_wife_ages: HusbandWife

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = Defs.verify_type(self.husband_wife_ages, HusbandWife)
        return check

    def ged(self, level: int = 1) -> str:
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
            Defs.verify_type(self.tag, str)
            and Defs.verify_type(self.attribute_type, str)
            and Defs.verify_type(
                self.family_event_detail, FamilyEventDetail | None
            )
        )
        return check

    def ged(self, level: int = 1) -> str:
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
            Defs.verify_type(self.event, str)
            and Defs.verify_type(self.event_type, str)
            and Defs.verify_type(self.event_detail, FamilyEventDetail | None)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            pass
        return lines


class Husband(NamedTuple):
    xref: IndividualXref = IndividualXref(Nul.RECORD)
    phrase: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = Defs.verify_type(self.phrase, str) and Defs.verify_type(
            self.xref, IndividualXref
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if str(self.xref) != self.xref.empty and self.validate():
            lines = ''.join(
                [lines, Defs.taginfo(level, Tag.HUSB, str(self.xref))]
            )
            if self.phrase != '':
                lines = ''.join(
                    [
                        lines,
                        Defs.taginfo(
                            level + 1, Tag.PHRASE, self.phrase
                        ),
                    ]
                )
        return lines


class Wife(NamedTuple):
    xref: IndividualXref = IndividualXref(Nul.RECORD)
    phrase: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = Defs.verify_type(self.phrase, str) and Defs.verify_type(
            self.xref, IndividualXref
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if str(self.xref) != self.xref.empty and self.validate():
            lines = ''.join(
                [lines, Defs.taginfo(level, Tag.WIFE, str(self.xref))]
            )
            if self.phrase != '':
                lines = ''.join(
                    [
                        lines,
                        Defs.taginfo(
                            level + 1, Tag.PHRASE, self.phrase
                        ),
                    ]
                )
        return lines


class Child(NamedTuple):
    xref: IndividualXref = IndividualXref(Nul.RECORD)
    phrase: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = Defs.verify_type(self.phrase, str) and Defs.verify_type(
            self.xref, IndividualXref
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if str(self.xref) != self.xref.empty and self.validate():
            lines = ''.join(
                [lines, Defs.taginfo(level, Tag.CHIL, str(self.xref))]
            )
            if self.phrase != '':
                lines = ''.join(
                    [
                        lines,
                        Defs.taginfo(
                            level + 1, Tag.PHRASE, self.phrase
                        ),
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
            Defs.verify_type(self.date_value, DateValue | None)
            and Defs.verify_type(self.temp, str)
            and Defs.verify_type(self.place, Place | None)
            and Defs.verify_enum(self.status.value, Stat)
            and Defs.verify_tuple_type(self.notes, Note)
            and Defs.verify_tuple_type(self.sources, SourceCitation)
        )
        return check

    def ged(self, level: int = 1) -> str:
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
        check: bool = Defs.verify_type(self.tag, str) and Defs.verify_type(
            self.detail, LDSOrdinanceDetail | None
        )
        return check

    def ged(self, level: int = 1) -> str:
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
            Defs.verify_type(self.tag, str)
            and Defs.verify_type(
                self.ordinance_detail, LDSOrdinanceDetail | None
            )
            and Defs.verify_type(self.family_xref, str)
        )
        return check

    def ged(self, level: int = 1) -> str:
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
            Defs.verify_enum(self.tag.value, Id)
            and Defs.verify_type(self.tag_info, str)
            and Defs.verify_type(self.tag_type, str)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = ''
        if self.validate():
            if self.tag != Id.NONE:
                lines = Defs.taginfo(
                    level, self.tag.value, self.tag_info
                )
            if self.tag != Id.UID:
                lines = ''.join(
                    [lines, Defs.taginfo(level + 1, Tag.TYPE, self.tag_type)]
                )
            if self.tag == Id.EXID and self.tag_type == '':
                logging.warning(Msg.EXID_TYPE)
        return lines


class IndividualEventDetail(NamedTuple):
    event_detail: EventDetail
    age: Age = Age(0, 0, 0, 0, GreaterLessThan.EQUAL, '')
    phrase: str = ''

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Defs.verify_type(self.event_detail, EventDetail)
            and Defs.verify_type(self.age, str)
            and Defs.verify_type(self.phrase, str)
        )
        return check

    def ged(self, level: int = 1) -> str:
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
            Defs.verify_enum(self.tag.value, IndiAttr)
            and Defs.verify_type(self.tag_type, str)
            and Defs.verify_type(
                self.event_detail, IndividualEventDetail | None
            )
        )
        return check

    def ged(self, level: int = 1) -> str:
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
            Defs.verify_type(self.tag, str)
            and Defs.verify_type(self.tag_type, str)
            and Defs.verify_type(
                self.event_detail, IndividualEventDetail | None
            )
            and Defs.verify_type(self.family_child, str)
            and Defs.verify_type(self.adoption, str)
            and Defs.verify_type(self.phrase, str)
        )
        return check

    def ged(self, level: int = 1) -> str:
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
        check: bool = Defs.verify_type(self.xref, str) and Defs.verify_type(
            self.phrase, str
        )
        return check

    def ged(self, level: int = 1) -> str:
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
            Defs.verify_type(self.family_xref, str)
            and Defs.verify_type(self.pedigree, str)
            and Defs.verify_type(self.pedigree_phrase, str)
            and Defs.verify_type(self.status, str)
            and Defs.verify_type(self.status_phrase, str)
            and Defs.verify_tuple_type(self.notes, Note)
        )
        return check

    def ged(self, level: int = 1) -> str:
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
        check: bool = Defs.verify_type(
            self.family_xref, str
        ) and Defs.verify_tuple_type(self.notes, Note)
        return check

    def ged(self, level: int = 1) -> str:
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
        check: bool = Defs.verify_type(self.path, str) and Defs.verify_type(
            self.media_type, str
        )
        return check

    def ged(self, level: int = 1) -> str:
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
#             Defs.verify_type(self.text, str)
#             and Defs.verify_type(self.mime, MediaType)
#             and Defs.verify_type(self.language, Lang)
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
            Defs.verify_type(self.path, str)
            and Defs.verify_type(self.media_type, str)
            and Defs.verify_type(self.media, str)
            and Defs.verify_type(self.phrase, str)
            and Defs.verify_type(self.title, str)
            and Defs.verify_tuple_type(self.file_translations, FileTranslations)
        )
        return check

    def ged(self, level: int = 1) -> str:
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
            Defs.verify_type(self.event, str)
            and Defs.verify_type(self.date_period, str)
            and Defs.verify_type(self.phrase, str)
            and Defs.verify_type(self.place, str)
            and Defs.verify_type(self.agency, str)
            and Defs.verify_tuple_type(self.notes, Note)
        )
        return check

    def ged(self, level: int = 1) -> str:
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
            Defs.verify_type(self.no, str)
            and Defs.verify_type(self.date, Date | None)
            and Defs.verify_type(self.phrase, str)
            and Defs.verify_tuple_type(self.notes, Note)
            and Defs.verify_tuple_type(self.sources, SourceEvent)
        )
        return check

    def ged(self, level: int = 1) -> str:
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

    xref: FamilyXref = FamilyXref(Nul.RECORD)
    resn: Resn = Resn.NONE
    attributes: Any = None
    events: Any = None
    husband: Husband = Husband(IndividualXref(Nul.RECORD), '')
    wife: Wife = Wife(IndividualXref(Nul.RECORD), '')
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
            Defs.verify_type(self.xref, FamilyXref)
            and Defs.verify_enum(self.resn.value, Resn)
            and Defs.verify_tuple_type(self.attributes, FamilyAttribute)
            and Defs.verify_tuple_type(self.events, FamilyEvent)
            and Defs.verify_type(self.husband, Husband)
            and Defs.verify_type(self.wife, Wife)
            and Defs.verify_tuple_type(self.children, Child)
            and Defs.verify_tuple_type(self.associations, Association)
            and Defs.verify_tuple_type(self.submitters, SubmitterXref)
            and Defs.verify_tuple_type(
                self.lds_spouse_sealings, LDSSpouseSealing
            )
            and Defs.verify_tuple_type(self.identifiers, Identifier)
            and Defs.verify_tuple_type(self.notes, Note)
            and Defs.verify_tuple_type(self.citations, SourceCitation)
            and Defs.verify_tuple_type(self.multimedia_links, MultimediaLink)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = Defs.taginit(self.xref, Record.FAM)
        if self.validate():
            if self.resn != Resn.NONE:
                lines = ''.join(
                    [lines, Defs.taginfo(level, Tag.RESN, self.resn.value)]
                )
            if self.attributes is not None:
                for attribute in self.attributes:
                    lines = ''.join([lines, attribute.ged(level)])
            if self.events is not None:
                for event in self.events:
                    lines = ''.join([lines, event.ged(level)])
            if self.husband != Husband(IndividualXref(Nul.RECORD), ''):
                lines = ''.join([lines, self.husband.ged(level)])
            if self.wife != Wife(IndividualXref(Nul.RECORD), ''):
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
                        [lines, Defs.taginfo(level, Tag.SUBM, submitter)]
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
    xref: IndividualXref = IndividualXref(Nul.RECORD)
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
            Defs.verify_type(self.xref, IndividualXref)
            and Defs.verify_enum(self.resn.value, Resn)
            and Defs.verify_tuple_type(self.personal_names, PersonalNamePiece)
            and Defs.verify_enum(self.sex.value, Sex)
            and Defs.verify_tuple_type(self.attributes, IndividualAttribute)
            and Defs.verify_tuple_type(self.events, IndividualEvent)
            and Defs.verify_tuple_type(
                self.lds_individual_ordinances, LDSIndividualOrdinances
            )
            and Defs.verify_tuple_type(self.families_child, FamilyChild)
            and Defs.verify_tuple_type(self.submitters, str)
            and Defs.verify_tuple_type(self.associations, Association)
            and Defs.verify_tuple_type(self.aliases, Alias)
            and Defs.verify_tuple_type(self.ancestor_interest, str)
            and Defs.verify_tuple_type(self.descendent_interest, str)
            and Defs.verify_tuple_type(self.identifiers, Identifier)
            and Defs.verify_tuple_type(self.notes, Note)
            and Defs.verify_tuple_type(self.sources, Source)
            and Defs.verify_tuple_type(self.multimedia_links, MultimediaLink)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = Defs.taginit(self.xref, Record.INDI)
        if self.validate():
            pass
        return lines


class Multimedia(NamedTuple):
    xref: MultimediaXref = MultimediaXref(Nul.RECORD)
    resn: Resn = Resn.NONE
    files: Any = None
    identifiers: Any = None
    notes: Any = None
    sources: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Defs.verify_type(self.xref, MultimediaXref)
            and Defs.verify_enum(self.resn.value, Resn)
            and Defs.verify_tuple_type(self.files, File)
            and Defs.verify_tuple_type(self.identifiers, Identifier)
            and Defs.verify_tuple_type(self.notes, Note)
            and Defs.verify_tuple_type(self.sources, Source)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = Defs.taginit(self.xref, Record.OBJE)
        if self.validate():
            pass
        return lines


class Repository(NamedTuple):
    xref: RepositoryXref = RepositoryXref(Nul.RECORD)
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
            Defs.verify_type(self.xref, RepositoryXref)
            and Defs.verify_type(self.name, str)
            and Defs.verify_type(self.address, Address | None)
            and Defs.verify_tuple_type(self.emails, str)
            and Defs.verify_tuple_type(self.faxes, str)
            and Defs.verify_tuple_type(self.wwws, str)
            and Defs.verify_tuple_type(self.notes, Note)
            and Defs.verify_tuple_type(self.identifiers, Identifier)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = Defs.taginit(self.xref, Record.REPO)
        if self.validate():
            pass
        return lines


class SharedNote(NamedTuple):
    xref: SharedNoteXref = SharedNoteXref(Nul.RECORD)
    text: str = ''
    mime: MediaType = MediaType.NONE
    language: Lang = Lang.CODE['NONE']
    translations: Any = None
    sources: Any = None
    identifiers: Any = None

    def validate(self) -> bool:
        """Validate the stored value."""
        check: bool = (
            Defs.verify_type(self.xref, SharedNoteXref)
            and Defs.verify_type(self.text, str)
            and Defs.verify_enum(self.mime.value, MediaType)
            and Defs.verify_type(self.language, str)
            and Defs.verify_tuple_type(self.translations, NoteTranslation)
            and Defs.verify_tuple_type(self.sources, Source)
            and Defs.verify_tuple_type(self.identifiers, Identifier)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = Defs.taginit(self.xref, Record.SNOTE)
        if self.validate():
            pass
        return lines


class Source(NamedTuple):
    xref: SourceXref = SourceXref(Nul.RECORD)
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
            Defs.verify_type(self.xref, SourceXref)
            and Defs.verify_type(self.author, str)
            and Defs.verify_type(self.title, str)
            and Defs.verify_type(self.abbreviation, str)
            and Defs.verify_type(self.published, str)
            and Defs.verify_tuple_type(self.events, SourceEvent)
            and Defs.verify_tuple_type(self.text, Text)
            and Defs.verify_tuple_type(self.repositories, Repository)
            and Defs.verify_tuple_type(self.identifiers, Identifier)
            and Defs.verify_tuple_type(self.notes, Note)
            and Defs.verify_tuple_type(self.multimedia_links, MultimediaLink)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = Defs.taginit(self.xref, Record.SOUR)
        if self.validate():
            pass
        return lines


class Submitter(NamedTuple):
    xref: SubmitterXref = SubmitterXref(Nul.RECORD)
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
            Defs.verify_type(self.xref, SubmitterXref)
            and Defs.verify_type(self.name, str)
            and Defs.verify_type(self.address, Address | None)
            and Defs.verify_tuple_type(self.phones, str)
            and Defs.verify_tuple_type(self.emails, str)
            and Defs.verify_tuple_type(self.faxes, str)
            and Defs.verify_tuple_type(self.wwws, str)
            and Defs.verify_tuple_type(self.multimedia_links, MultimediaLink)
            and Defs.verify_tuple_type(self.languages, str)
            and Defs.verify_tuple_type(self.identifiers, Identifier)
            and Defs.verify_tuple_type(self.notes, Note)
        )
        return check

    def ged(self, level: int = 1) -> str:
        """Format to meet GEDCOM standards."""
        lines: str = Defs.taginit(self.xref, Record.SUBM)
        if str(self.xref) != self.xref.empty and self.validate():
            pass
        return lines


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
    language: Lang = Lang.CODE['NONE']
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
                Defs.taginfo(level, Tag.HEAD),
                Defs.taginfo(level + 1, Tag.GEDC),
                Defs.taginfo(level + 2, Tag.VERS, GEDSpecial.VERSION),
            ]
        )
        return lines
