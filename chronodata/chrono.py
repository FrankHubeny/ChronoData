# Licensed under a 3-clause BSD style license - see LICENSE.md
"""Methods to build a chronology based on the GEDCOM standard.

This module implements reading and writing chronology files according to the
[FamilySearch GEDCOM Version 7](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html)
standard.  It also allows reading files in the GEDCOM 5.5.1 standard,
but will write the output in compliance with GEDCOM 7.0.

The underlying datastructure for the chronology is a Python dictionary.
This dictionary can be read and written in JSON.

Rather than introduce extensions to the GEDCOM standards new data items
are placed under `FACT` and `EVEN` tags as
[Tamura Jones](https://www.tamurajones.net/GEDCOMExtensions.xhtml) recommended.
Some extensions are the use of ISO dates as implemented by NumPy's `datetime64`
data type."""

import logging
from typing import Any

import numpy as np

from chronodata.core import Base
from chronodata.enums import Tag
from chronodata.g7 import (
    #Enum,
    #EnumName,
    GEDDateTime,
    GEDSpecial,
    ISOMonths,
    #Record,
)
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
from chronodata.tuples import (
    Address,
    Age,
    Association,
    Citation,
    Date,
    NameTranslation,
    Note,
    Time,
)


class Chronology(Base):
    """Methods to add, update and remove a specific loaded chronology."""

    def __init__(
        self,
        name: str = '',
        filename: str = '',
        calendar: str = GEDSpecial.GREGORIAN,
        log: bool = True,
    ) -> None:
        super().__init__(name, filename, calendar, log)
        self.xref_counter: int = 1
        self.family_xreflist: list[str] = []
        self.individual_xreflist: list[str] = []
        self.multimedia_xreflist: list[str] = []
        self.repository_xreflist: list[str] = []
        self.shared_note_xreflist: list[str] = []
        self.source_xreflist: list[str] = []
        self.submitter_xreflist: list[str] = []

    # def _check_tag(
    #     self, tag: Tag, dictionary: dict[str, Any] | None = None
    # ) -> None:
    #     if dictionary is None:
    #         dictionary = self.chron
    #     if tag not in dictionary:
    #         dictionary.update({tag: {}})

    def add_event(self, name: str, when: str) -> None:
        #self._check_tag(Tag.EVEN)
        self.chron[Tag.EVEN.value].update({name: {Tag.DATE.value: when}})
        logging.info(Msg.ADD_EVENT.format(name, self.chron_name))

    ###### GEDCOM Substructures

    def verify_xref(self, xref: str, xreflist: list[str], name: str) -> bool:
        """Check if an xref value in in the proper xreflist."""
        if xref not in xreflist:
            raise ValueError(Msg.NOT_RECORD.format(xref, name))
        return True

    def ged_date(
        self,
        iso_date: str = GEDSpecial.NOW,
        epoch: bool = True,
    ) -> tuple[str, str]:
        """Obtain the GEDCOM date and time from an ISO date and time or the
        current UTC timestamp in GEDCOM format.

        Parameters
        ----------
            iso_date: The ISO date or `now` for the current date and time.
            calendar: The GEDCOM calendar to use when returning the date.
            epoch: Return the epoch, `BCE`, for the GEDCOM date if it is before
                the current epoch.  Set this to `False` to not return the epoch.
                This only applies to dates prior to 1 AD.

        References
        ----------

        Exceptions:

        """
        datetime: str = str(np.datetime64(iso_date))
        date, time = datetime.split(GEDSpecial.T)
        date_pieces = date.split(GEDSpecial.HYPHEN)
        if len(date_pieces) == 3:
            year: str = date_pieces[0]
            month: str = date_pieces[1]
            day: str = date_pieces[2]
        else:
            year = date_pieces[1]
            month = date_pieces[2]
            day = date_pieces[3]
        ged_time: str = ''.join([time, GEDSpecial.Z])
        good_calendar: str | bool = GEDDateTime.CALENDARS.get(
            GEDSpecial.GREGORIAN, False
        )
        if not good_calendar:
            logging.critical(Msg.BAD_CALENDAR.format(self.calendar))
            raise ValueError(Msg.BAD_CALENDAR.format(self.calendar))
        month_code: str = GEDDateTime.CALENDARS[self.calendar][
            GEDSpecial.MONTH_NAMES
        ].get(month, False)
        if not month_code:
            logging.critical(Msg.BAD_MONTH.format(self.calendar, month))
            raise ValueError(Msg.BAD_MONTH.format(self.calendar, month))
        ged_date: str = ''
        if epoch and len(date_pieces) == 4:
            ged_date = ''.join(
                [
                    day,
                    GEDSpecial.SPACE,
                    month_code,
                    GEDSpecial.SPACE,
                    year,
                    GEDSpecial.SPACE,
                    GEDSpecial.BC,
                ]
            )
        else:
            ged_date = ''.join(
                [day, GEDSpecial.SPACE, month_code, GEDSpecial.SPACE, year]
            )
        return ged_date, ged_time

    def iso_date(
        self,
        ged_date: str,
        ged_time: str = '',
        # calendar: str = GEDSpecial.GREGORIAN,
    ) -> str:
        """Return an ISO date and time given a GEDCOM date and time."""
        day: str
        month: str
        year: str
        day, month, year = ged_date.split(GEDSpecial.SPACE)
        time: str = ged_time.split(GEDSpecial.Z)[0]
        good_calendar: str | bool = ISOMonths.CALENDARS.get(
            GEDSpecial.GREGORIAN, False
        )
        if not good_calendar:
            logging.critical(Msg.BAD_CALENDAR.format(self.calendar))
            raise ValueError(Msg.BAD_CALENDAR.format(self.calendar))
        month_code: str = ISOMonths.CALENDARS[self.calendar].get(month, False)
        if not month_code:
            logging.critical(Msg.BAD_MONTH.format(self.calendar, month))
            raise ValueError(Msg.BAD_MONTH.format(self.calendar, month))
        iso_datetime: str = ''.join(
            [
                year,
                GEDSpecial.HYPHEN,
                month_code,
                GEDSpecial.HYPHEN,
                day,
                GEDSpecial.T,
                time,
            ]
        )
        return iso_datetime

    def now(self, level: int = 2) -> str:
        """Return the current UTC date and time rather than an entered value.

        This will be returned as a list of two lines for a GEDCOM file.
        This method will not likely be needed by the builder of a chronology
        unless the builder wants to enter the current date and time into
        the chronology. The current date and time is automatically
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
        >>> a = Chronology(name='testing')
        >>> a.now()
        ['2 DATE 05 DEC 2024', '3 TIME 02:58:19Z']

        Changing the level adjusts the level numbers for the two returned strings.

        >>> a = Chronology(name='testing')
        >>> a.now(level=5)
        ['5 DATE 05 DEC 2024', '6 TIME 02:58:19Z']

        See Also
        --------
        - `creation_date`
        - `change_date`
        - `header`
        """
        date: str
        time: str
        date, time = self.ged_date()
        return ''.join(
            [
                Defs.taginfo(level, Tag.DATE, date),
                Defs.taginfo(level + 1, Tag.TIME, time),
            ]
        )

    def change_date(self, note: Note | None = None) -> str:
        """Return three GEDCOM lines showing a line with a change tag
        and then two automatically generated
        UTC date and time lines.  These are used to
        show when a record has been modified.

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
        if note is None:
            # note = Note('', '', '', [], [])
            return ''.join(
                [
                    Defs.taginfo(1, Tag.CHAN),
                    self.now(),
                ]
            )
        return ''.join(
            [
                Defs.taginfo(1, Tag.CHAN),
                self.now(),
                self.note_structure(note),
            ]
        )

    def creation_date(self) -> str:
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
        return ''.join([Defs.taginfo(1, Tag.CREA), self.now()])

    def date_value(
        self,
        date: Date,
        time: Time | None = None,
        phrase: str = '',
        level: int = 1,
        epoch: str = '',
    ) -> str:
        if time is None:
            time = Time(0, 0, 0)
        # Do checks on numeric input.
        if date.day < 1 or not isinstance(date.day, int):
            raise ValueError(Msg.NOT_POSITIVE.format(str(date.day)))
        if date.month < 1 or not isinstance(date.month, int):
            raise ValueError(Msg.NOT_POSITIVE.format(str(date.month)))
        if not isinstance(date.year, int):
            raise ValueError(Msg.NOT_POSITIVE.format(str(date.year)))
        if time.hour < 0 or not isinstance(time.hour, int):
            raise ValueError(Msg.NOT_POSITIVE.format(str(time.hour)))
        if time.minute < 0:
            raise ValueError(Msg.NOT_POSITIVE.format(str(time.minute)))
        if time.second < 0:
            raise ValueError(Msg.NOT_POSITIVE.format(str(time.second)))

        # Format for insertion.
        day_str: str = str(date.day)
        month_str: str = str(date.month)
        if len(month_str) == 1:
            month_str = ''.join(['0', month_str])
        max_months: int = GEDDateTime.CALENDARS[self.calendar][
            GEDSpecial.MAX_MONTHS
        ]
        if date.month > max_months:
            raise ValueError(Msg.TOO_MANY_MONTHS.format(str(date.month)))
        max_days: int = GEDDateTime.CALENDARS[self.calendar][
            GEDSpecial.MONTH_MAX_DAYS
        ][month_str]
        month_str = GEDDateTime.CALENDARS[self.calendar][
            GEDSpecial.MONTH_NAMES
        ][month_str]
        if date.day > max_days:
            raise ValueError(Msg.TOO_MANY_DAYS.format(str(date.day), month_str))
        year_str: str = str(date.year)
        hour_str: str = str(time.hour)
        minute_str: str = str(time.minute)
        second_str: str = str(time.second)
        if len(day_str) == 1:
            day_str = ''.join(['0', day_str])

        if len(hour_str) == 1:
            hour_str = ''.join(['0', hour_str])
        if len(minute_str) == 1:
            minute_str = ''.join(['0', minute_str])
        if len(second_str) == 1:
            second_str = ''.join(['0', second_str])

        if date.year < 0 and epoch != '':
            year_str = ''.join([str(-date.year), ' ', epoch])
        time_str = ''.join([hour_str, ':', minute_str, ':', second_str])
        date_str = ''.join([day_str, ' ', month_str, ' ', year_str])
        # if len(date) == 0:
        #     logging.error(Msg.NO_VALUE)
        #     raise ValueError(Msg.NO_VALUE)
        if time == Time(0, 0, 0) and phrase == '':
            return Defs.taginfo(level, Tag.DATE, date_str)
        if time != Time(0, 0, 0) and phrase == '':
            return ''.join(
                [
                    Defs.taginfo(level, Tag.DATE, date_str),
                    Defs.taginfo(level + 1, Tag.TIME, time_str),
                ]
            )
        if time == Time(0, 0, 0) and phrase != '':
            return ''.join(
                [
                    Defs.taginfo(level, Tag.DATE, date_str),
                    Defs.taginfo(level + 1, Tag.PHRASE, phrase),
                ]
            )
        return ''.join(
            [
                Defs.taginfo(level, Tag.DATE, date_str),
                Defs.taginfo(level + 1, Tag.TIME, time_str),
                Defs.taginfo(level + 1, Tag.PHRASE, phrase),
            ]
        )

    ###### Methods to Assisting Building GEDCOM Records

    def association_structure(
        self, xref: str, association: Association, level: int = 1
    ) -> str:
        """Add association information."""
        lines: str = ''
        if self.verify_xref(xref, self.individual_xreflist, Record.INDIVIDUAL):
            lines = ''.join([lines, Defs.taginfo(level, Tag.ASSO, xref)])
            association.ged(1)
        #     if association.association_phrase != '':
        #         lines = ''.join(
        #             [
        #                 lines,
        #                 Defs.taginfo(
        #                     level + 1,
        #                     Gedcom.PHRASE,
        #                     association.association_phrase,
        #                 ),
        #             ]
        #         )
        #     if association.role in Enum.ROLE:
        #         lines = ''.join(
        #             [
        #                 lines,
        #                 Defs.taginfo(level + 2, Gedcom.ROLE, association.role),
        #             ]
        #         )
        #         if association.role_phrase != '':
        #             lines = ''.join(
        #                 [
        #                     lines,
        #                     Defs.taginfo(
        #                         level + 2,
        #                         Gedcom.PHRASE,
        #                         association.role_phrase,
        #                     ),
        #                 ]
        #             )
        #     else:
        #         raise ValueError(
        #             Msg.NOT_VALID_ENUM.format(association.role, EnumName.ROLE)
        #         )
        #     for note in association.notes:
        #         lines = ''.join([lines, self.note_structure(note)])
        #     for citation in association.citations:
        #         lines = ''.join([lines, self.source_citation(citation)])
        # else:
        #     raise ValueError(
        #         Msg.NOT_RECORD.format(association.xref, Record.INDIVIDUAL)
        #     )
        return lines

    # def event_detail(self, event: list[Any], level: int = 1) -> str:
    #     """Add event detail information."""
    #     lines: str = ''
    #     return lines

    # def family_attribute_structure(
    #     self, attribute: list[Any], level: int = 1
    # ) -> str:
    #     """Add attribute information."""
    #     lines: str = ''
    #     return lines

    # def family_event_detail(self, detail: list[Any], level: int = 1) -> str:
    #     """Add family event detail information."""
    #     lines: str = ''
    #     return lines

    # def family_event_structure(self, event: list[Any], level: int = 1) -> str:
    #     """Add family event information."""
    #     lines: str = ''
    #     return lines

    def identifier_structure(
        self, identifier: list[str], level: int = 1
    ) -> str:
        """Add an identifier to a record.

        Each identifier is a list contain at least two strings and at most three.
        The first string is the kind of identifier.
        The second string is the identifier itself.
        The optional third is the type of identifier.
        """
        lines: str = ''
        if (
            identifier[0] in Enum.ID
            and len(identifier) > 1
            and len(identifier) < 4
        ):
            if len(identifier) > 1:
                lines = ''.join(
                    [lines, Defs.taginfo(level, identifier[0], identifier[1])]
                )
            if len(identifier) > 2:
                lines = ''.join(
                    [lines, Defs.taginfo(level + 1, Tag.TYPE, identifier[2])]
                )
        return lines

    # def individual_attribute_structure(
    #     self, attribute: list[Any], level: int = 1
    # ) -> str:
    #     """Add individual attribute information."""
    #     lines: str = ''
    #     return lines

    # def individual_event_detail(self, detail: list[Any], level: int = 1) -> str:
    #     """Add individual event detail information."""
    #     lines: str = ''
    #     return lines

    # def individual_event_structure(
    #     self, event: list[Any], level: int = 1
    # ) -> str:
    #     """Add individual event information."""
    #     lines: str = ''
    #     return lines

    # def lds_individual_ordinance(
    #     self, ordinance: list[Any], level: int = 1
    # ) -> str:
    #     """Add LDS individual ordinance information."""
    #     lines: str = ''
    #     return lines

    # def lds_ordinance_detail(self, detail: list[Any], level: int = 1) -> str:
    #     """Add LDS ordinance detail information."""
    #     lines: str = ''
    #     return lines

    # def lds_spouse_sealing(self, spouse: list[Any], level: int = 1) -> str:
    #     """Add LDS spouse sealing information."""
    #     lines: str = ''
    #     return lines

    def multimedia_link(self, media: list[Any], level: int = 1) -> str:
        """Add multimedia information."""
        lines: str = ''
        if len(media) > 0:
            lines = ''.join([lines, Defs.taginfo(level, Tag.OBJE, media[0])])
            if len(media) == 6:
                lines = ''.join(
                    [
                        lines,
                        Defs.taginfo(level + 1, Tag.CROP),
                        Defs.taginfo(level + 2, Tag.TOP, media[1]),
                        Defs.taginfo(level + 2, Tag.LEFT, media[2]),
                        Defs.taginfo(level + 2, Tag.HEIGHT, media[3]),
                        Defs.taginfo(level + 2, Tag.WIDTH, media[4]),
                        Defs.taginfo(level + 1, Tag.TITL, media[5]),
                    ]
                )
            if len(media) == 2:
                lines = ''.join(
                    [lines, Defs.taginfo(level + 1, Tag.TITL, media[1])]
                )
        return lines

    # def non_event_structure(self, event: list[Any], level: int = 1) -> str:
    #     """Add non event information."""
    #     lines: str = ''
    #     return lines

    def note_structure(self, note: Note, level: int = 1) -> str:
        """Add note information."""
        # if note is None:
        #     note = ()
        lines: str = ''
        # if note != ():
        if note.mime != '' and note.mime not in Enum.MEDIA_TYPE:
            raise ValueError(
                Msg.NOT_VALID_ENUM.format(note.mime, EnumName.MEDIA_TYPE)
            )
        if note.text != '':
            lines = ''.join([lines, Defs.taginfo(level, Tag.NOTE, note.text)])
            if note.mime != '':
                lines = ''.join(
                    [lines, Defs.taginfo(level + 1, Tag.MIME, note.mime)]
                )
            if note.language != '':
                lines = ''.join(
                    [lines, Defs.taginfo(level + 1, Tag.LANG, note.language)]
                )
            for trans in note.translation:
                lines = ''.join(
                    [lines, Defs.taginfo(level, Tag.TRAN, trans.text)]
                )

                if trans.mime not in Enum.MEDIA_TYPE:
                    raise ValueError(
                        Msg.NOT_VALID_ENUM.format(
                            trans.mime, EnumName.MEDIA_TYPE
                        )
                    )
                lines = ''.join(
                    [lines, Defs.taginfo(level + 1, Tag.MIME, trans.mime)]
                )
                lines = ''.join(
                    [
                        lines,
                        Defs.taginfo(level + 1, Tag.LANG, trans.language),
                    ]
                )
        for cite in note.citations:
            lines = ''.join([lines, self.source_citation(cite)])
        return lines

    # def personal_name_pieces(self, name: PersonalName, level: int = 1) -> str:
    #     """Add pieces of personal name information."""
    #     if name.tag in Enum.PERSONAL_NAME:
    #         personal_name = Defs.taginfo(level, name.tag, name.text.strip())
    #     return personal_name

    def personal_name_structure(
        self,
        name: str,
        type_name: str,
        phrase: str,
        pieces: Any = None,
        translations: Any = None,
        notes: Any = None,
        sources: Any = None,
        level: int = 1,
    ) -> str:
        """Add note information."""
        Defs.verify_enum(type_name, Enum.NAME_TYPE)
        lines: str = ''.join(
            [
                Defs.taginfo(level, Tag.NAME, name),
                Defs.taginfo(level + 1, Tag.TYPE, type_name),
            ]
        )
        if phrase != '':
            lines = ''.join(
                [lines, Defs.taginfo(level + 2, Tag.PHRASE, phrase)]
            )
        if pieces is not None and len(pieces) > 0:
            for piece in pieces:
                lines = ''.join(
                    # [lines, self.personal_name_pieces(piece, level + 1)]
                    [lines, piece.ged(level + 1)]
                )
        if translations is not None and len(translations) > 0:
            for translation in translations:
                lines = ''.join(
                    [lines, self.translation(translation, level=level + 1)]
                )
        return lines

    # def place_structure(self, place: list[Any], level: int = 1) -> str:
    #     """Add note information."""

    #     lines: str = ''
    #     return lines

    def source_citation(self, source: Citation, level: int = 1) -> str:
        """Add source citation information."""
        lines: str = ''
        return lines

    # def source_repository_citation(
    #     self, repository: Any, level: int = 1
    # ) -> str:
    #     """Add source repository information."""
    #     lines: str = ''
    #     return lines

    def translation(self, trans: NameTranslation, level: int = 1) -> str:
        lines: str = ''.join(
            [
                Defs.taginfo(level, Tag.TRAN, trans.text),
                Defs.taginfo(level + 1, Tag.LANG, trans.language),
                Defs.taginfo(level + 1, trans.piece.tag, trans.piece.text),
            ]
        )
        return lines

    ###### GEDCOM Records

    def contact(
        self,
        phones: list[str] | None = None,
        emails: list[str] | None = None,
        faxes: list[str] | None = None,
        wwws: list[str] | None = None,
        level: int = 1,
    ) -> str:
        """Return a string of contact options.

        Although this method is not expected to be used directly by the user,
        the user may find it useful to how how the specific contact information
        would be represented in a GEDCOM file.

        See Also
        --------
        """
        if phones is None:
            phones = []
        if emails is None:
            emails = []
        if faxes is None:
            faxes = []
        if wwws is None:
            wwws = []
        lines: str = ''
        for phone in phones:
            lines = ''.join([lines, Defs.taginfo(level, Tag.PHON, phone)])
        for email in emails:
            lines = ''.join([lines, Defs.taginfo(level, Tag.EMAIL, email)])
        for fax in faxes:
            lines = ''.join([lines, Defs.taginfo(level, Tag.FAX, fax)])
        for www in wwws:
            lines = ''.join([lines, Defs.taginfo(level, Tag.WWW, www)])
        return lines

    def next_counter(self, xref_list: list[str], xref_name: str = '') -> str:
        """Allows one to override a numeric counter for a name as identifier for a record.

        This overriding works for family and individual records.

        The identifier name can be composed of upper case letters, digits or the underscore
        based on the GEDCOM specification.

        The value of naming individuals and families is for comparison purposes
        between two different chronologies that reference the same individuals or
        familys.  With the same identifiers they can more easily be searched.

        See Also
        --------
        - `family_xref`
        - `individual_xref`
        - `named_family_xref`
        - `named_individual_xref`

        Reference
        ---------
        - [GEDCOM Standard](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#cb3-5)
        """
        modified_xref: str = ''
        if xref_name == '':
            modified_xref = str(self.xref_counter)
            self.xref_counter += 1
        else:
            modified_xref = str(xref_name).strip().upper().replace(' ', '_')
        modified_xref = ''.join(
            [
                GEDSpecial.ATSIGN,
                modified_xref,
                GEDSpecial.ATSIGN,
            ]
        )
        if modified_xref in xref_list:
            raise ValueError(Msg.XREF_EXISTS.format(xref_name))
        xref_list.append(modified_xref)
        return modified_xref

    def family_xref(self, xref_name: str = '') -> FamilyXref:
        """Create a cross reference identifier for a family.

        A family may reference many individuals.  An individual
        may reference many families.  This method creates
        the reference identifier for a family without specifying
        reference identifiers for its members.

        See Also
        --------
        - `individual_xref`: create a cross reference identifier for an individual.

        Examples
        --------
        Examples of both `individual_xref` and `family_xref` are provided
        with the `individual_xref` documentation.

        The following chronology has only two events in it both under a family record.

        >>> from chronodata.chrono import Chronology
        >>>
        >>> c = Chronology('mankind')
        >>> c.family_record(
        >>>    xref_family=c.family_xref(),
        >>>    family_events=[]
        >>> )

        The GEDCOM file for this chronology would look like the following.

        For an example of how ChronoData was used to compare various such
        chronologies, see
        """
        family_xref = self.next_counter(
            self.family_xreflist,
            xref_name,
        )
        return FamilyXref(family_xref)
    
    def multimedia_xref(self, xref_name: str = '') -> MultimediaXref:
        multimedia_xref = self.next_counter(
            self.multimedia_xreflist,
            xref_name,
        )
        return MultimediaXref(multimedia_xref)
    
    def repository_xref(self, xref_name: str = '') -> RepositoryXref:
        repository_xref = self.next_counter(
            self.repository_xreflist,
            xref_name,
        )
        return RepositoryXref(repository_xref)
    
    def shared_note_xref(self, xref_name: str = '') -> SharedNoteXref:
        shared_note_xref = self.next_counter(
            self.shared_note_xreflist,
            xref_name,
        )
        return SharedNoteXref(shared_note_xref)
    
    def source_xref(self, xref_name: str = '') -> SourceXref:
        source_xref = self.next_counter(
            self.source_xreflist,
            xref_name,
        )
        return SourceXref(source_xref)
    
    def submitter_xref(self, xref_name: str = '') -> SubmitterXref:
        submitter_xref = self.next_counter(
            self.submitter_xreflist,
            xref_name,
        )
        return SubmitterXref(submitter_xref)

    # def named_xref(self, search_for: str = '', pandas: bool = True) -> pd.DataFrame | list[list[str]]:
    #     """Report on the family and individuals with named identifiers."""
    #     names_index = list(range(1, len(self.named_xreflist) + 1))
    #     if pandas:
    #         return pd.DataFrame(
    #             data=self.named_xreflist,
    #             columns=['Group', 'Name'],
    #             index=names_index,
    #         )
    #     return self.named_

    def individual_xref(self, xref_name: str = '') -> IndividualXref:
        """Create a cross reference identifier for an individual.

        A individual may reference different families one where
        the individual is a parent in one marriage and another where the individual
        is a child or has been adopted or may be a distant descendent.  This method creates
        the reference identifier for an individual without associating
        it with reference identifiers for its families.

        The other five record types (`multimedia`, `repository`, `shared_note`,
        `source` and `submitter`) return a cross reference identifier
        which should be saved since they will be needed in individual and family
        records.

        See Also
        --------
        - `family_xref`: create a cross reference identifier for a family.

        Example
        -------
        One could start a chronology by getting reference identifiers
        for the individuals and the families in any order.  Once one has
        the identifiers one can build out the individual and family records.

        >>> from chronodata.chrono import Chronology
        >>>
        >>> c = Chronology('adam to seth')
        >>> adam = c.individual_xref()
        >>> adameve = c.family_xref()
        >>> eve = c.individual_xref()
        >>> cain = c.individual_xref()
        >>> abel = c.individual_xref()
        >>> seth = c.individual_xref()
        >>> c.family_record(
        >>>     xref_family=adameve,
        >>>     husband=adam,
        >>>     wife=eve,
        >>>     children=[cain,abel,seth]
        >>> )
        >>> c.individual_record(
        >>>     xref_individual=adam,
        >>>     families_spouse=[adameve]
        >>> )
        >>> c.individual_record(
        >>>    xref_individual=eve,
        >>>    families_spouse=[adameve]
        >>> )
        >>> c.individual_record(
        >>>    xref_individual=cain,
        >>>    families_child=[adameve]
        >>> )
        >>> c.individual_record(
        >>>    xref_individual=abel,
        >>>    families_child=[adameve]
        >>> )
        >>> c.individual_record(
        >>>    xref_individual=seth,
        >>>    families_child=[adameve]
        >>> )

        One would get the following GEDCOM record:


        Various chronologies for the Ancient Near East have been constructed.
        They do not all agree with each other, but one can compare them
        to identifiy specifically where they disagree and decide which
        represents the best view of ancient history.


        Something similar could be even for non-biological transitions
        such as the decay of uranium-238 to lead-206.

        >>> from chronodata.chrono import Chronology
        >>>
        >>> c = Chronology('uranium to lead')
        >>> uranium = c.individual_xref()
        >>> lead = c.individual_xref()
        >>> uranium_lead = c.family_xref()
        >>> c.individual_record(
        >>>     xref_individual=uranium,
        >>>     families_spouse=[uranium_lead],
        >>> )
        >>> c.individual_record(
        >>>     xref_individual=lead,
        >>>     families_child=[uranium_lead]
        >>> )
        >>> c.family_record(
        >>>     xref_family=uranium_lead,
        >>>     wife=uranium,
        >>>     child=[lead]
        >>> )

        A complete example of the state transitions from uranium-238 to
        lead is provided in the example section.


        """
        individual_xref: str = self.next_counter(
            xref_list=self.individual_xreflist,
            xref_name=xref_name,
        )
        return IndividualXref(individual_xref)

    def family_record(
        self,
        xref: FamilyXref,
        resn: str = '',
        family_attributes: Any = None,
        family_events: Any = None,
        family_non_events: Any = None,
        husband: str = GEDSpecial.VOID,
        husband_phrase: str = '',
        wife: str = GEDSpecial.VOID,
        wife_phrase: str = '',
        children: Any = None,
        associations: Any = None,
        submitters: Any = None,
        lds_spouse_sealing: Any = None,
        identifiers: Any = None,
        notes: Any = None,
        sources: Any = None,
        multimedia: Any = None,
    ) -> None:
        """Create a detailed record for a family.

        Prior to calling this one will need a family cross reference
        identifier.  This can be obtained by running the `family_xref`
        method which will return the needed identifier.

        Parameter
        ---------
        - xref_family: The cross reference identifier obtained from the
            `family_xref` method.
        - resn: A flag specifying if access to the record must be restricted.
        - family_attributes: list[Any] | None = None,
        - family_events: list[Any] | None = None,
        - family_non_events: list[Any] | None = None,
        - husband: str = GEDSpecial.VOID,
        - husband_phrase: str = '',
        - wife: str = GEDSpecial.VOID,
        - wife_phrase: str = '',
        - children: list[Any] | None = None,
        - associations: list[Any] | None = None,
        - submitters: list[Any] | None = None,
        - lds_spouse_sealing: list[Any] | None = None,
        - identifiers: list[Any] | None = None,
        - notes: list[Any] | None = None,
        - sources: list[Any] | None = None,
        - multimedia: list[Any] | None = None,

        Exceptions
        ----------
        - A value error is raised if the family cross reference identifier
        has not been created in advance and used for the `xref_family` parameter.
        ` A value error is raised if the `husband` cross reference identifier
        has not been created in advance using the `individual_xref` method.
        ` A value error is raised if the `wife` cross reference identifier
        has not been created in advance using the `individual_xref` method.
        ` A value error is raised if any of the `children`
        do not have a cross reference identifier that was
        created in advance using the `individual_xref` method.
        - A value error is raised if the
        [reason code](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#enumset-RESN)
        for restricting
        the record is not in the set of valid reason codes.

        Reference
        ---------
        - [GEDCOM Specification](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html)

        See Also
        --------
        - family_xref: Create a family cross reference identifier.
        - individual_xref: Create an individual cross reference identifier.
        """

        if associations is None:
            associations = []
        if children is None:
            children = []
        if family_attributes is None:
            family_attributes = []
        if family_events is None:
            family_events = []
        if family_non_events is None:
            family_non_events = []
        if identifiers is None:
            identifiers = []
        if lds_spouse_sealing is None:
            lds_spouse_sealing = []
        if multimedia is None:
            multimedia = []
        if notes is None:
            notes = []
        if sources is None:
            sources = []
        if submitters is None:
            submitters = []
        if xref not in self.family_xreflist:
            raise ValueError(Msg.NOT_RECORD.format(xref, Record.FAMILY))
        if resn != '' and resn not in Enum.RESN:
            raise ValueError(Msg.NOT_VALID_ENUM.format(resn, EnumName.RESN))
        if (
            husband != GEDSpecial.VOID
            and husband not in self.individual_xreflist
        ):
            raise ValueError(Msg.NOT_RECORD.format(husband, Record.INDIVIDUAL))
        if wife != GEDSpecial.VOID and wife not in self.individual_xreflist:
            raise ValueError(Msg.NOT_RECORD.format(wife, Record.INDIVIDUAL))
        for child in children:
            if (
                child != GEDSpecial.VOID
                and child not in self.individual_xreflist
            ):
                raise ValueError(
                    Msg.NOT_RECORD.format(child, Record.INDIVIDUAL)
                )
        ged_family: str = Defs.taginit(xref, Tag.FAM)
        if resn != '' and resn in Enum.RESN:
            ged_family = ''.join([ged_family, Defs.taginfo(1, Tag.RESN, resn)])
        for attribute in family_attributes:
            ged_family = ''.join(
                [ged_family, self.family_attribute_structure(attribute)]
            )
        for event in family_events:
            ged_family = ''.join(
                [ged_family, self.family_event_structure(event)]
            )
        for non_event in family_non_events:
            ged_family = ''.join(
                [ged_family, self.non_event_structure(non_event)]
            )
        ged_family = ''.join([ged_family, Defs.taginfo(1, Tag.HUSB, husband)])
        if husband_phrase != '':
            ged_family = ''.join(
                [ged_family, Defs.taginfo(2, Tag.PHRASE, husband_phrase)]
            )
        ged_family = ''.join([ged_family, Defs.taginfo(1, Tag.WIFE, wife)])
        if wife_phrase != '':
            ged_family = ''.join(
                [ged_family, Defs.taginfo(2, Tag.PHRASE, wife_phrase)]
            )
        for child, phrase in children:
            ged_family = ''.join([ged_family, Defs.taginfo(1, Tag.CHIL, child)])
            if phrase != '':
                ged_family = ''.join(
                    [ged_family, Defs.taginfo(2, Tag.PHRASE, phrase)]
                )
        for association in associations:
            ged_family = ''.join(
                [ged_family, self.association_structure(association)]
            )
        for submitter in submitters:
            ged_family = ''.join(
                [ged_family, Defs.taginfo(1, Tag.SUBM, submitter)]
            )
        for spouse in lds_spouse_sealing:
            ged_family = ''.join([ged_family, self.lds_spouse_sealing(spouse)])
        for identifier in identifiers:
            ged_family = ''.join(
                [ged_family, self.identifier_structure(identifier)]
            )
        for note in notes:
            ged_family = ''.join([ged_family, self.note_structure(note)])
        for source in sources:
            ged_family = ''.join([ged_family, self.source_citation(source)])
        for media in multimedia:
            ged_family = ''.join([ged_family, self.multimedia_link(media)])
        ged_family = ''.join([ged_family, self.creation_date()])
        self.ged_family = ''.join([self.ged_family, ged_family])
        logging.info(Msg.ADDED_RECORD.format(Record.FAMILY, xref))

    def individual_record(
        self,
        xref: str,
        resn: str = '',
        personal_names: list[Any] | None = None,
        sex: str = '',
        attributes: list[Any] | None = None,
        events: list[Any] | None = None,
        non_events: list[Any] | None = None,
        lds_individual_ordinances: list[Any] | None = None,
        families_child: list[Any] | None = None,
        families_spouse: list[Any] | None = None,
        submitters: list[Any] | None = None,
        associations: list[Any] | None = None,
        aliases: list[str] | None = None,
        ancestor_interest: list[str] | None = None,
        descendent_interest: list[str] | None = None,
        identifiers: list[Any] | None = None,
        notes: list[Any] | None = None,
        sources: list[Any] | None = None,
        multimedia: list[Any] | None = None,
    ) -> None:
        if aliases is None:
            aliases = []
        if ancestor_interest is None:
            ancestor_interest = []
        if associations is None:
            associations = []
        if attributes is None:
            attributes = []
        if descendent_interest is None:
            descendent_interest = []
        if events is None:
            events = []
        if families_child is None:
            families_child = []
        if families_spouse is None:
            families_spouse = []
        if identifiers is None:
            identifiers = []
        if lds_individual_ordinances is None:
            lds_individual_ordinances = []
        if multimedia is None:
            multimedia = []
        if non_events is None:
            non_events = []
        if notes is None:
            notes = []
        if personal_names is None:
            personal_names = []
        if sources is None:
            sources = []
        if submitters is None:
            submitters = []
        if xref not in self.individual_xreflist:
            raise ValueError(Msg.NOT_RECORD.format(xref, Record.INDIVIDUAL))
        if resn != '' and resn not in Enum.RESN:
            raise ValueError(Msg.NOT_VALID_ENUM.format(resn, EnumName.RESN))
        if sex != '' and sex not in Enum.SEX:
            raise ValueError(Msg.NOT_VALID_ENUM.format(sex, EnumName.SEX))
        for family in families_child:
            if len(family) > 1 and family[1] not in Enum.PEDI:
                raise ValueError(
                    Msg.NOT_VALID_ENUM.format(family[3], EnumName.PEDI)
                )
            if len(family) > 3 and family[3] not in Enum.STAT:
                raise ValueError(
                    Msg.NOT_VALID_ENUM.format(family[3], EnumName.STAT)
                )
        for alias in aliases:
            if alias[0] not in self.individual_xreflist:
                raise ValueError(
                    Msg.NOT_RECORD.format(alias[0], Record.INDIVIDUAL)
                )
        for interest in ancestor_interest:
            if interest not in self.submitter_xreflist:
                raise ValueError(
                    Msg.NOT_RECORD.format(interest, Record.SUBMITTER)
                )
        for interest in descendent_interest:
            if interest not in self.submitter_xreflist:
                raise ValueError(
                    Msg.NOT_RECORD.format(interest, Record.SUBMITTER)
                )
        for submitter in submitters:
            if submitter not in self.submitter_xreflist:
                raise ValueError(
                    Msg.NOT_RECORD.format(submitter, Record.SUBMITTER)
                )
        ged_individual: str = Defs.taginit(xref, Tag.INDI)
        if resn != '' and resn in Enum.RESN:
            ged_individual = ''.join(
                [ged_individual, Defs.taginfo(1, Tag.RESN, resn)]
            )
        for name in personal_names:
            ged_individual = ''.join(
                [ged_individual, self.personal_name_structure(name)]
            )
        if sex != '' and sex in Enum.SEX:
            ged_individual = ''.join(
                [ged_individual, Defs.taginfo(1, Tag.SEX, sex)]
            )
        for attribute in attributes:
            ged_individual = ''.join(
                [ged_individual, self.individual_attribute_structure(attribute)]
            )
        for event in events:
            ged_individual = ''.join(
                [ged_individual, self.individual_event_structure(event)]
            )
        for non_event in non_events:
            ged_individual = ''.join(
                [ged_individual, self.non_event_structure(non_event)]
            )
        for ordinance in lds_individual_ordinances:
            ged_individual = ''.join(
                [ged_individual, self.lds_individual_ordinance(ordinance)]
            )
        for family in families_child:
            if family[0] in self.family_xreflist:
                ged_individual = ''.join(
                    [ged_individual, Defs.taginfo(1, Tag.FAMC, family[0])]
                )
                if len(family) > 1:
                    ged_individual = ''.join(
                        [
                            ged_individual,
                            Defs.taginfo(2, Tag.PEDI, family[1]),
                        ]
                    )
                    if len(family) > 2:
                        ged_individual = ''.join(
                            [
                                ged_individual,
                                Defs.taginfo(3, Tag.PHRASE, family[2]),
                            ]
                        )
                if len(family) > 3:
                    ged_individual = ''.join(
                        [
                            ged_individual,
                            Defs.taginfo(2, Tag.STAT, family[2]),
                        ]
                    )
                    if len(family) > 4:
                        ged_individual = ''.join(
                            [
                                ged_individual,
                                Defs.taginfo(3, Tag.PHRASE, family[3]),
                            ]
                        )
        for family in families_spouse:
            if family[0] in self.family_xreflist:
                ged_individual = ''.join(
                    [ged_individual, Defs.taginfo(1, Tag.FAMS, family[0])]
                )
                if len(family) > 1:
                    ged_individual = ''.join(
                        [ged_individual, self.note_structure(family[1])]
                    )
        for submitter in submitters:
            if submitter in self.submitter_xreflist:
                ged_individual = ''.join(
                    [ged_individual, Defs.taginfo(1, Tag.SUBM, submitter)]
                )
        for association in associations:
            ged_individual = ''.join(
                [ged_individual, self.association_structure(association)]
            )
        for alias in aliases:
            if alias[0] in self.individual_xreflist:
                ged_individual = ''.join(
                    [ged_individual, Defs.taginfo(1, Tag.ALIA, alias[0])]
                )
                if len(alias) > 1 and alias[1] != '':
                    ged_individual = ''.join(
                        [
                            ged_individual,
                            Defs.taginfo(2, Tag.PHRASE, alias[1]),
                        ]
                    )
        for interest in ancestor_interest:
            if interest in self.submitter_xreflist:
                ged_individual = ''.join(
                    [ged_individual, Defs.taginfo(1, Tag.ANCI, interest)]
                )
        for interest in descendent_interest:
            if interest in self.submitter_xreflist:
                ged_individual = ''.join(
                    [ged_individual, Defs.taginfo(1, Tag.DESI, interest)]
                )
        for identifier in identifiers:
            ged_individual = ''.join(
                [ged_individual, self.identifier_structure(identifier)]
            )
        for note in notes:
            ged_individual = ''.join(
                [ged_individual, self.note_structure(note)]
            )
        for source in sources:
            ged_individual = ''.join(
                [ged_individual, self.source_citation(source)]
            )
        for media in multimedia:
            ged_individual = ''.join(
                [ged_individual, self.multimedia_link(media)]
            )
        ged_individual = ''.join([ged_individual, self.creation_date()])
        self.ged_individual = ''.join([self.ged_individual, ged_individual])
        logging.info(Msg.ADDED_RECORD.format(Record.INDIVIDUAL, xref))

    def multimedia_record(
        self,
        files: list[Any],
        resn: str = '',
        identifiers: list[Any] | None = None,
        notes: list[Any] | None = None,
        sources: list[Any] | None = None,
        xref_name: str = '',
    ) -> str:
        if identifiers is None:
            identifiers = []
        if notes is None:
            notes = []
        if sources is None:
            sources = []
        if resn != '' and resn not in Enum.RESN:
            raise ValueError(Msg.NOT_VALID_ENUM.format(resn, EnumName.RESN))
        for file in files:
            if file[1] not in Enum.MEDIA_TYPE:
                raise ValueError(
                    Msg.NOT_VALID_ENUM.format(file[1], EnumName.MEDIA_TYPE)
                )
        if len(file) > 5 and len(file[5]) > 0:
            for translation in file[5]:
                if translation[1] not in Enum.MEDIA_TYPE:
                    raise ValueError(
                        Msg.NOT_VALID_ENUM.format(file[1], EnumName.MEDIA_TYPE)
                    )
        if len(file) > 3 and file[3] != '' and file[3] not in Enum.MEDI:
            raise ValueError(Msg.NOT_VALID_ENUM.format(file[3], EnumName.MEDI))
        xref: str = self.next_counter(
            self.multimedia_xreflist, Tag.OBJE, xref_name
        )
        ged_multimedia: str = Defs.taginit(xref, Tag.OBJE)
        if resn != '':
            ged_multimedia = ''.join(
                [ged_multimedia, Defs.taginfo(1, Tag.RESN, resn)]
            )
        for file in files:
            ged_multimedia = ''.join(
                [
                    ged_multimedia,
                    Defs.taginfo(1, Tag.FILE, file[0]),
                    Defs.taginfo(2, Tag.FORM, file[1]),
                ]
            )
            if len(file) > 2 and file[2] != '':
                ged_multimedia = ''.join(
                    [ged_multimedia, Defs.taginfo(3, Tag.MEDI, file[2])]
                )
            if len(file) > 3 and file[3] != '':
                ged_multimedia = ''.join(
                    [ged_multimedia, Defs.taginfo(4, Tag.PHRASE, file[3])]
                )
            if len(file) > 4 and file[4] != '':
                ged_multimedia = ''.join(
                    [ged_multimedia, Defs.taginfo(2, Tag.TITL, file[4])]
                )
            if len(file) > 5 and len(file[5]) > 0:
                for translation in file[5]:
                    ged_multimedia = ''.join(
                        [
                            ged_multimedia,
                            Defs.taginfo(2, Tag.TRAN, translation[0]),
                            Defs.taginfo(3, Tag.FORM, translation[1]),
                        ]
                    )
        for identifier in identifiers:
            ged_multimedia = ''.join(
                [ged_multimedia, self.identifier_structure(identifier)]
            )
        for note in notes:
            ged_multimedia = ''.join(
                [ged_multimedia, self.note_structure(note)]
            )
        for source in sources:
            ged_multimedia = ''.join(
                [ged_multimedia, self.source_citation(source)]
            )
        ged_multimedia = ''.join([ged_multimedia, self.creation_date()])
        self.ged_multimedia = ''.join([self.ged_multimedia, ged_multimedia])
        logging.info(Msg.ADDED_RECORD.format(Record.MULTIMEDIA, xref))
        return xref

    def repository_record(
        self,
        name: str,
        address: str = '',
        city: str = '',
        state: str = '',
        postal: str = '',
        country: str = '',
        phones: list[Any] | None = None,
        emails: list[Any] | None = None,
        faxes: list[Any] | None = None,
        wwws: list[Any] | None = None,
        notes: list[Any] | None = None,
        identifiers: list[Any] | None = None,
        xref_name: str = '',
    ) -> str:
        if phones is None:
            phones = []
        if emails is None:
            emails = []
        if faxes is None:
            faxes = []
        if wwws is None:
            wwws = []
        if identifiers is None:
            identifiers = []
        if notes is None:
            notes = []
        for id in identifiers:
            if id[0] not in Enum.ID:
                raise ValueError(Msg.NOT_VALID_ENUM.format(id[0], EnumName.ID))
        xref: str = self.next_counter(
            self.repository_xreflist, Tag.REPO, xref_name
        )
        ged_repository: str = Defs.taginit(xref, Tag.REPO)
        ged_repository = ''.join(
            [ged_repository, Defs.taginfo(1, Tag.NAME, name)]
        )
        ged_repository = ''.join(
            [
                ged_repository,
                Address(address, city, state, postal, country),
            ]
        )
        ged_repository = ''.join(
            [ged_repository, self.contact(phones, emails, faxes, wwws)]
        )
        for note in notes:
            ged_repository = ''.join(
                [ged_repository, self.note_structure(note)]
            )
        for identifier in identifiers:
            ged_repository = ''.join(
                [ged_repository, self.identifier_structure(identifier)]
            )
        ged_repository = ''.join([self.ged_repository, self.creation_date()])
        logging.info(Msg.ADDED_RECORD.format(Record.REPOSITORY, xref))
        return xref

    def shared_note_record(
        self,
        note: str,
        mime: str = '',
        language: str = '',
        translations: list[Any] | None = None,
        sources: list[Any] | None = None,
        identifiers: list[Any] | None = None,
        xref_name: str = '',
    ) -> str:
        if translations is None:
            translations = []
        if sources is None:
            sources = []
        if identifiers is None:
            identifiers = []
        if mime != '' and mime not in Enum.MEDIA_TYPE:
            raise ValueError(
                Msg.NOT_VALID_ENUM.format(mime, EnumName.MEDIA_TYPE)
            )
        for translation in translations:
            if len(translation) > 1 and translation[1] not in Enum.MEDIA_TYPE:
                raise ValueError(
                    Msg.NOT_VALID_ENUM.format(
                        translation[1], EnumName.MEDIA_TYPE
                    )
                )
        for id in identifiers:
            if id[0] not in Enum.ID:
                raise ValueError(Msg.NOT_VALID_ENUM.format(id[0], EnumName.ID))
        xref: str = self.next_counter(
            self.shared_note_xreflist, Tag.SNOTE, xref_name
        )
        ged_shared_note: str = Defs.taginit(xref, Tag.SNOTE, note)
        if mime != '' and mime in Enum.MEDIA_TYPE:
            ged_shared_note = ''.join(
                [ged_shared_note, Defs.taginfo(1, Tag.MIME, mime)]
            )
        if language != '':
            ged_shared_note = ''.join(
                [ged_shared_note, Defs.taginfo(1, Tag.LANG, language)]
            )
        for translation in translations:
            ged_shared_note = ''.join(
                [ged_shared_note, Defs.taginfo(1, Tag.TRAN, translation[0])]
            )
            if len(translation) > 1:
                ged_shared_note = ''.join(
                    [
                        ged_shared_note,
                        Defs.taginfo(2, Tag.MIME, translation[1]),
                    ]
                )
            if len(translation) > 2:
                ged_shared_note = ''.join(
                    [
                        ged_shared_note,
                        Defs.taginfo(2, Tag.LANG, translation[2]),
                    ]
                )
        for source in sources:
            ged_shared_note = ''.join(
                [ged_shared_note, self.source_citation(source)]
            )
        for identifier in identifiers:
            ged_shared_note = ''.join(
                [ged_shared_note, self.identifier_structure(identifier)]
            )
        ged_shared_note = ''.join([ged_shared_note, self.creation_date()])
        self.ged_shared_note = ''.join([self.ged_shared_note, ged_shared_note])
        logging.info(Msg.ADDED_RECORD.format(Record.SHARED_NOTE, xref))
        return xref

    def source_record(
        self,
        events: list[Any] | None = None,
        author: str = '',
        title: str = '',
        abbreviation: str = '',
        publisher: str = '',
        text: str = '',
        mime: str = '',
        language: str = '',
        sources: list[Any] | None = None,
        identifiers: list[Any] | None = None,
        notes: list[Any] | None = None,
        multimedia: list[Any] | None = None,
        xref_name: str = '',
    ) -> str:
        if events is None:
            events = []
        if identifiers is None:
            identifiers = []
        if multimedia is None:
            multimedia = []
        if notes is None:
            notes = []
        if sources is None:
            sources = []
        if mime != '' and mime not in Enum.MEDIA_TYPE:
            raise ValueError(
                Msg.NOT_VALID_ENUM.format(mime, EnumName.MEDIA_TYPE)
            )
        for media in multimedia:
            if media[0] not in self.multimedia_xreflist:
                raise ValueError(
                    Msg.NOT_RECORD.format(media[0], Record.MULTIMEDIA)
                )
        for id in identifiers:
            if id[0] not in Enum.ID:
                raise ValueError(Msg.NOT_VALID_ENUM.format(mime, EnumName.ID))
        xref: str = self.next_counter(self.source_xreflist, Tag.SOUR, xref_name)
        ged_source: str = Defs.taginit(xref, Tag.SOUR)
        if len(events) > 0:
            ged_source = ''.join([ged_source, Defs.taginfo(1, Tag.DATA)])
            for event in events:
                ged_source = ''.join(
                    [ged_source, Defs.taginfo(2, Tag.EVEN, event[0])]
                )
                if len(event) > 1:
                    ged_source = ''.join(
                        [ged_source, Defs.taginfo(3, Tag.DATE, event[1])]
                    )
                if len(event) > 2:
                    ged_source = ''.join(
                        [ged_source, Defs.taginfo(4, Tag.PHRASE, event[2])]
                    )
                if len(event) > 3:
                    ged_source = ''.join(
                        [ged_source, Defs.taginfo(2, Tag.AGNC, event[3])]
                    )
                if len(event) > 4:
                    ged_source = ''.join(
                        [ged_source, self.note_structure(event[4])]
                    )
        if author != '':
            ged_source = ''.join(
                [ged_source, Defs.taginfo(1, Tag.AUTH, author)]
            )
        if title != '':
            ged_source = ''.join([ged_source, Defs.taginfo(1, Tag.TITL, title)])
        if abbreviation != '':
            ged_source = ''.join(
                [ged_source, Defs.taginfo(1, Tag.ABBR, abbreviation)]
            )
        if publisher != '':
            ged_source = ''.join(
                [ged_source, Defs.taginfo(1, Tag.PUBL, publisher)]
            )
        if text != '':
            ged_source = ''.join([ged_source, Defs.taginfo(1, Tag.TEXT, text)])
        if mime != '' and mime in Enum.MEDIA_TYPE:
            ged_source = ''.join([ged_source, Defs.taginfo(2, Tag.MIME, mime)])
        if language != '':
            ged_source = ''.join(
                [ged_source, Defs.taginfo(2, Tag.LANG, language)]
            )
        for source in sources:
            ged_source = ''.join(
                [ged_source, self.source_repository_citation(source)]
            )
        for identifier in identifiers:
            ged_source = ''.join(
                [ged_source, self.identifier_structure(identifier)]
            )
        for note in notes:
            ged_source = ''.join([ged_source, self.note_structure(note)])
        for media in multimedia:
            ged_source = ''.join([ged_source, self.multimedia_link(media)])
        ged_source = ''.join([ged_source, self.creation_date()])
        self.ged_source = ''.join([self.ged_source, ged_source])
        logging.info(Msg.ADDED_RECORD.format(Record.SOURCE, xref))
        return xref

    def submitter_record(
        self,
        name: str,
        address: str = '',
        city: str = '',
        state: str = '',
        postal: str = '',
        country: str = '',
        phones: list[str] | None = None,
        emails: list[str] | None = None,
        faxes: list[str] | None = None,
        wwws: list[str] | None = None,
        multimedia: list[Any] | None = None,
        languages: list[str] | None = None,
        identifiers: list[list[str]] | None = None,
        notes: list[Any] | None = None,
        shared_note: str = '',
        xref_name: str = '',
    ) -> str:
        if phones is None:
            phones = []
        if emails is None:
            emails = []
        if faxes is None:
            faxes = []
        if wwws is None:
            wwws = []
        if multimedia is None:
            multimedia = []
        if languages is None:
            languages = []
        if identifiers is None:
            identifiers = []
        if notes is None:
            notes = []
        for id in identifiers:
            if id[0] not in Enum.ID:
                raise ValueError(Msg.NOT_VALID_ENUM.format(id[0], EnumName.ID))
        for media in multimedia:
            if media[0] not in self.multimedia_xreflist:
                raise ValueError(
                    Msg.NOT_RECORD.format(media[0], Record.MULTIMEDIA)
                )
        xref: str = self.next_counter(
            self.submitter_xreflist, Tag.SUBM, xref_name
        )
        ged_submitter: str = Defs.taginit(xref, Tag.SUBM)
        ged_submitter = ''.join(
            [ged_submitter, Defs.taginfo(1, Tag.NAME, name)]
        )
        ged_submitter = ''.join(
            [
                ged_submitter,
                self.address_structure(address, city, state, postal, country),
            ]
        )
        ged_submitter = ''.join(
            [ged_submitter, self.contact(phones, emails, faxes, wwws)]
        )
        for media in multimedia:
            ged_submitter = ''.join(
                [ged_submitter, self.multimedia_link(media)]
            )
        for language in languages:
            ged_submitter = ''.join(
                [ged_submitter, Defs.taginfo(1, Tag.LANG, language)]
            )
        for identifier in identifiers:
            ged_submitter = ''.join(
                [ged_submitter, self.identifier_structure(identifier)]
            )
        for note in notes:
            ged_submitter = ''.join([ged_submitter, self.note_structure(note)])
        if shared_note != '':
            ged_submitter = ''.join(
                [ged_submitter, Defs.taginfo(1, Tag.SNOTE, shared_note)]
            )
        ged_submitter = ''.join([ged_submitter, self.creation_date()])
        self.ged_submitter = ''.join([self.ged_submitter, ged_submitter])
        logging.info(Msg.ADDED_RECORD.format(Record.SUBMITTER, xref))
        return xref

    ###### GEDCOM Special Records

    def header(
        self,
        schemas: list[Any] | None = None,
        source: str = '',
        vers: str = '',
        name: str = '',
        corp: str = '',
        address: str = '',
        city: str = '',
        state: str = '',
        postal: str = '',
        country: str = '',
        phones: list[str] | None = None,
        emails: list[str] | None = None,
        faxes: list[str] | None = None,
        wwws: list[str] | None = None,
        data: str = '',
        data_date: str = '',
        data_time: str = '',
        data_copr: str = '',
        date: str = '',
        time: str = '',
        dest: str = '',
        submitter: str = '',
        copr: str = '',
        language: str = '',
        place: list[Any] | None = None,
        note: Note | None = None,
        shared_note: str = '',
    ) -> None:
        if submitter != '' and submitter not in self.submitter_xreflist:
            raise ValueError(Msg.NOT_RECORD.format(submitter, Record.SUBMITTER))
        if schemas is None:
            schemas = []
        if phones is None:
            phones = []
        if emails is None:
            emails = []
        if faxes is None:
            faxes = []
        if wwws is None:
            wwws = []
        if place is None:
            place = []
        if note is None:
            note = Note('', '', '', [], [])
        ged_header: str = ''.join(
            [
                Defs.taginfo(0, Tag.HEAD),
                Defs.taginfo(1, Tag.GEDC),
                Defs.taginfo(2, Tag.VERS, GEDSpecial.VERSION),
            ]
        )
        if len(schemas) > 0:
            ged_header = ''.join([ged_header, Defs.taginfo(1, Tag.SCHMA)])
            for schema in schemas:
                tag, ref = schema
                ged_header = ''.join(
                    [ged_header, Defs.taginfo(2, Tag.TAG, tag, ref)]
                )
        if source != '':
            ged_header = ''.join(
                [ged_header, Defs.taginfo(1, Tag.SOUR, source)]
            )
            if vers != '':
                ged_header = ''.join(
                    [ged_header, Defs.taginfo(2, Tag.VERS, vers)]
                )
            if name != '':
                ged_header = ''.join(
                    [ged_header, Defs.taginfo(2, Tag.NAME, name)]
                )
            if corp != '':
                ged_header = ''.join(
                    [ged_header, Defs.taginfo(2, Tag.CORP, corp)]
                )
            ged_header = ''.join(
                [
                    ged_header,
                    Address(address, city, state, postal, country, level=3),
                ]
            )
            ged_header = ''.join(
                [ged_header, self.contact(phones, emails, faxes, wwws, level=3)]
            )
            if data != '':
                ged_header = ''.join(
                    [ged_header, Defs.taginfo(2, Tag.DATA, data)]
                )
                if data_date != '':
                    ged_header = ''.join(
                        [ged_header, Defs.taginfo(3, Tag.DATE, data_date)]
                    )
                if data_time != '':
                    ged_header = ''.join(
                        [ged_header, Defs.taginfo(4, Tag.TIME, data_time)]
                    )
                if data_copr != '':
                    ged_header = ''.join(
                        [ged_header, Defs.taginfo(2, Tag.COPR, data_copr)]
                    )
        if dest != '':
            ged_header = ''.join([ged_header, Defs.taginfo(1, Tag.DEST, dest)])
        if date != '':
            ged_header = ''.join([ged_header, Defs.taginfo(1, Tag.DATE, date)])
        if time != '':
            ged_header = ''.join([ged_header, Defs.taginfo(2, Tag.TIME, time)])
        if submitter != '':
            ged_header = ''.join(
                [ged_header, Defs.taginfo(1, Tag.SUBM, submitter)]
            )
        if copr != '':
            ged_header = ''.join([ged_header, Defs.taginfo(1, Tag.COPR, copr)])
        if language != '':
            ged_header = ''.join(
                [ged_header, Defs.taginfo(1, Tag.LANG, language)]
            )
        if len(place) > 0:
            ged_header = ''.join(
                [
                    ged_header,
                    Defs.taginfo(1, Tag.PLAC, place[0]),
                    Defs.taginfo(2, Tag.FORM, place[1]),
                ]
            )
        if shared_note != '':
            ged_header = ''.join(
                [ged_header, Defs.taginfo(1, Tag.SNOTE, shared_note)]
            )
        ged_header = ''.join([ged_header, self.note_structure(note)])
        self.ged_header = ged_header
