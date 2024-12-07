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

from chronodata.constants import (
    Calendar,
    Value,
)
from chronodata.core import Base
from chronodata.g7 import (
    Enum,
    EnumName,
    Gedcom,
    GEDMonths,
    GEDSpecial,
    ISOMonths,
    Record,
)
from chronodata.messages import Msg


class Chronology(Base):
    """Methods to add, update and remove a specific loaded chronology."""

    def __init__(
        self,
        name: str = Value.EMPTY,
        filename: str = Value.EMPTY,
        calendar: dict[str, Any] = Calendar.GREGORIAN,
        log: bool = True,
    ) -> None:
        super().__init__(name, filename, calendar, log)
        self.xref_counter: int = 1
        self.family_xreflist: list[int] = []
        self.individual_xreflist: list[int] = []
        self.multimedia_xreflist: list[int] = []
        self.repository_xreflist: list[int] = []
        self.shared_note_xreflist: list[int] = []
        self.source_xreflist: list[int] = []
        self.submitter_xreflist: list[int] = []

    def _check_tag(
        self, tag: str, dictionary: dict[str, Any] | None = None
    ) -> None:
        if dictionary is None:
            dictionary = self.chron
        if tag not in dictionary:
            dictionary.update({tag: {}})

    def add_event(self, name: str, when: str) -> None:
        self._check_tag(Gedcom.EVEN)
        self.chron[Gedcom.EVEN].update({name: {Gedcom.DATE: when}})
        logging.info(Msg.ADD_EVENT.format(name, self.chron_name))

    ###### GEDCOM Substructures

    def ged_date(
        self,
        iso_date: str = GEDSpecial.NOW,
        calendar: str = GEDSpecial.GREGORIAN,
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
        ged_time: str = Value.EMPTY.join([time, GEDSpecial.Z])
        good_calendar: str | bool = GEDMonths.CALENDARS.get(
            GEDSpecial.GREGORIAN, False
        )
        if not good_calendar:
            logging.critical(Msg.BAD_CALENDAR.format(calendar))
            raise ValueError(Msg.BAD_CALENDAR.format(calendar))
        month_code: str = GEDMonths.CALENDARS[calendar].get(month, False)
        if not month_code:
            logging.critical(Msg.BAD_MONTH.format(calendar, month))
            raise ValueError(Msg.BAD_MONTH.format(calendar, month))
        ged_date: str = Value.EMPTY
        if epoch and len(date_pieces) == 4:
            ged_date = Value.EMPTY.join(
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
            ged_date = Value.EMPTY.join(
                [day, GEDSpecial.SPACE, month_code, GEDSpecial.SPACE, year]
            )
        return ged_date, ged_time

    def iso_date(
        self,
        ged_date: str,
        ged_time: str = Value.EMPTY,
        calendar: str = GEDSpecial.GREGORIAN,
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
            logging.critical(Msg.BAD_CALENDAR.format(calendar))
            raise ValueError(Msg.BAD_CALENDAR.format(calendar))
        month_code: str = ISOMonths.CALENDARS[calendar].get(month, False)
        if not month_code:
            logging.critical(Msg.BAD_MONTH.format(calendar, month))
            raise ValueError(Msg.BAD_MONTH.format(calendar, month))
        iso_datetime: str = Value.EMPTY.join(
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

    # def address(
    #     self,
    #     fulladdress: str,
    #     city: str = Value.EMPTY,
    #     state: str = Value.EMPTY,
    #     postal: str = Value.EMPTY,
    #     country: str = Value.EMPTY,
    #     counter: int = 1,
    # ) -> dict[str, dict[str, str]]:
    #     counter1: int = counter + 1
    #     new_address: dict[str, dict[str, str]] = {
    #         Gedcom.ADDR: {'FULL': fulladdress}
    #     }
    #     if city != '':
    #         new_address[Gedcom.ADDR].update({Gedcom.CITY: city})
    #     if state != '':
    #         new_address[Gedcom.ADDR].update({Gedcom.STAE: state})
    #     if postal != '':
    #         new_address[Gedcom.ADDR].update({Gedcom.POST: postal})
    #     if country != '':
    #         new_address[Gedcom.ADDR].update({Gedcom.CTRY: country})
    #     return new_address

    # def association(
    #     self,
    #     individual: str,
    #     role: str,
    #     association_phrase: str = Value.EMPTY,
    #     role_phrase: str = Value.EMPTY,
    #     note: dict[str, Any] | None = None,
    #     source_citation: dict[str, Any] | None = None,
    #     counter: int = 1,
    # ) -> dict[str, dict[str, str]]:
    #     counter2: int = counter + 1
    #     counter3: int = counter + 2
    #     if source_citation is None:
    #         source_citation = {}
    #     if note is None:
    #         note = {}
    #     new_association: dict[str, dict[str, str]] = {
    #         Gedcom.ASSO: {Gedcom.IDNO: individual, Gedcom.ROLE: role}
    #     }
    #     if association_phrase != Value.EMPTY:
    #         new_association[Gedcom.ASSO].update(
    #             {Gedcom.PHRASE: association_phrase}
    #         )
    #     if role_phrase != Value.EMPTY:
    #         new_association[Gedcom.ASSO].update({Gedcom.PHRASE: role_phrase})
    #     return new_association

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
        return (
            f'{level} {Gedcom.DATE} {date}\n'
            f'{level + 1} {Gedcom.TIME} {time}\n'
        )

    def change_date(self, note: list[str] | None = None) -> str:
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
            note = []
        # lines: str = f'1 {Gedcom.CHAN}\n'
        # lines.join(self.now())
        # lines.join(self.note_structure(note))
        return Value.EMPTY.join(
            [f'1 {Gedcom.CHAN}\n', self.now(), self.note_structure(note)]
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
        return Value.EMPTY.join([f'1 {Gedcom.CREA}\n', self.now()])

    def date_value(
        self,
        date: str,
        time: str = Value.EMPTY,
        phrase: str = Value.EMPTY,
        level: int = 1,
    ) -> str:
        level2: int = level + 1
        if len(date) == 0:
            logging.error(Msg.NO_VALUE)
            raise ValueError(Msg.NO_VALUE)
        if time == Value.EMPTY and phrase == Value.EMPTY:
            return f'{level} {Gedcom.DATE} {date}\n'
        if time != Value.EMPTY and phrase == Value.EMPTY:
            return (
                f'{level} {Gedcom.DATE} {date}\n'
                f'{level2} {Gedcom.TIME} {time}\n'
            )
        if time == Value.EMPTY and phrase != Value.EMPTY:
            return (
                f'{level} {Gedcom.DATE} {date}\n'
                f'{level2} {Gedcom.PHRASE} {phrase}\n'
            )
        return (
            f'{level} {Gedcom.DATE} {date}\n'
            f'{level2} {Gedcom.TIME} {time}\n'
            f'{level2} {Gedcom.PHRASE} {phrase}\n'
        )

    ###### Methods to Assisting Building GEDCOM Records

    def next_counter(self, record: list[str]) -> str:
        counter: int = self.xref_counter
        xref: str = Value.EMPTY.join(
            [GEDSpecial.ATSIGN, str(counter), GEDSpecial.ATSIGN]
        )
        record.append(xref)
        self.xref_counter += 1
        return xref

    def address_structure(self, address: list[Any], level: int = 1) -> str:
        """Add address information.

        Each address line is a list of five strings:
        - Mailing Address: Each line of the mailing label is separated by `\n`.
        - City: The city or and empty string to leave this blank.
        - State: The state or an empty string to leave this blank.
        - Postal Code: The postal code or an empty string to leave this blank.
        - Country: The country or an empty string to leave this blank.

        One does not have to call this method directly.  The GEDCOM record methods
        call it when creating a chronology.  However, one can use it to
        see what the address information one provides would look like
        in a GEDCOM file.

        Example
        -------
        In the first example note the five strings in the list.  Also note
        that the country was not specified but nonetheless an empty string
        was added as a placeholder for the absent country information.
        Note the `\n` to separate the two address lines.
        [
            '12345 ABC Street\nSouth North City, My State 23456',
            'South North City',
            'My State',
            '23456',
            ''
        ]

        The GEDCOM record would appear as the following:

        1 ADDR 12345 ABC Street
        1 CONT South North City, My State 23456
        2 CITY South North City
        2 STAE My State
        2 POST 23456

        The following is the minimum amount of information for an address.
        [
            '12345 ABC Street\nSouth North City, My State 23456',
        ]

        If one does not want to use the `\n` one can write the following
        provided one imports the GEDSpecial class.  One way to do that is
        by adding the following line at the top of the cell:

        from chronodata.g7 import GEDSpecial

        [
            f'12345 ABC Street:{GEDSpecial.NEWLINE}South North City, My State 23456',
        ]

        The GEDCOM record would appear as the following:

        1 ADDR 12345 ABC Street
        1 CONT South North City, My State 23456

        If the list is empty the method returns the empty list.

        """
        lines: str = Value.EMPTY
        if len(address) > 0:
            address_lines = address[0].split('\n')
            lines = Value.EMPTY.join(
                [lines, f'{level} {Gedcom.ADDR} {address_lines[0]}\n']
            )
            for line in address_lines[1:]:
                lines = Value.EMPTY.join(
                    [lines, f'{level} {Gedcom.CONT} {line}\n']
                )
            if len(address) > 1 and address[1] != Value.EMPTY:
                lines = Value.EMPTY.join(
                    [lines, f'{level + 1} {Gedcom.CITY} {address[1]}\n']
                )
            if len(address) > 2 and address[2] != Value.EMPTY:
                lines = Value.EMPTY.join(
                    [lines, f'{level + 1} {Gedcom.STAE} {address[2]}\n']
                )
            if len(address) > 3 and address[3] != Value.EMPTY:
                lines = Value.EMPTY.join(
                    [lines, f'{level + 1} {Gedcom.POST} {address[3]}\n']
                )
            if len(address) > 4 and address[4] != Value.EMPTY:
                lines = Value.EMPTY.join(
                    [lines, f'{level + 1} {Gedcom.CTRY} {address[4]}\n']
                )
        return lines

    def association_structure(
        self, association: list[Any], level: int = 1
    ) -> str:
        """Add association information."""
        lines: str = Value.EMPTY
        if association[0] in self.individual_xreflist:
            lines = Value.EMPTY.join(
                [lines, f'{level} {Gedcom.ASSO} {association[0]}\n']
            )
            if association[1] != Value.EMPTY:
                lines = Value.EMPTY.join(
                    [lines, f'{level + 1} {Gedcom.PHRASE} {association[1]}\n']
                )
            if association[2] in Enum.ROLE:
                lines = Value.EMPTY.join(
                    [lines, f'{level + 2} {Gedcom.ROLE} {association[2]}\n']
                )
                if association[3] != Value.EMPTY:
                    lines = Value.EMPTY.join(
                        [
                            lines,
                            f'{level + 2} {Gedcom.PHRASE} {association[3]}\n',
                        ]
                    )
            else:
                raise ValueError(
                    Msg.NOT_VALID_ENUM.format(association[2], EnumName.ROLE)
                )
            lines = Value.EMPTY.join(
                [lines, self.note_structure(association[4])]
            )
            lines = Value.EMPTY.join(
                [lines, self.source_citation(association[5])]
            )
        else:
            raise ValueError(
                Msg.NOT_RECORD.format(association[0], Record.INDIVIDUAL)
            )
        return lines

    def event_detail(self, event: list[Any], level: int = 1) -> list[str]:
        """Add event detail information."""
        lines: str = Value.EMPTY
        return lines

    def family_attribute_structure(
        self, attribute: list[Any], level: int = 1
    ) -> str:
        """Add attribute information."""
        lines: str = Value.EMPTY
        return lines

    def family_event_detail(self, detail: list[Any], level: int = 1) -> str:
        """Add family event detail information."""
        lines: str = Value.EMPTY
        return lines

    def family_event_structure(self, event: list[Any], level: int = 1) -> str:
        """Add family event information."""
        lines: str = Value.EMPTY
        return lines

    def identifier_structure(
        self, identifier: list[str], level: int = 1
    ) -> str:
        """Add an identifier to a record.

        Each identifier is a list contain at least two strings and at most three.
        The first string is the kind of identifier.
        The second string is the identifier itself.
        The optional third is the type of identifier.
        """
        lines: str = Value.EMPTY
        if (
            identifier[0] in Enum.ID
            and len(identifier) > 1
            and len(identifier) < 4
        ):
            if len(identifier) > 1:
                lines = Value.EMPTY.join(
                    [lines, f'{level} {identifier[0][0]} {identifier[0][1]}\n']
                )
            if len(identifier) > 2:
                lines = Value.EMPTY.join(
                    [lines, f'{level + 1} {Gedcom.TYPE} {identifier[0][2]}\n']
                )
        return lines

    def individual_attribute_structure(
        self, attribute: list[Any], level: int = 1
    ) -> str:
        """Add individual attribute information."""
        lines: str = Value.EMPTY
        return lines

    def individual_event_detail(self, detail: list[Any], level: int = 1) -> str:
        """Add individual event detail information."""
        lines: str = Value.EMPTY
        return lines

    def individual_event_structure(
        self, event: list[Any], level: int = 1
    ) -> str:
        """Add individual event information."""
        lines: str = Value.EMPTY
        return lines

    def lds_individual_ordinance(
        self, ordinance: list[Any], level: int = 1
    ) -> str:
        """Add LDS individual ordinance information."""
        lines: str = Value.EMPTY
        return lines

    def lds_ordinance_detail(self, detail: list[Any], level: int = 1) -> str:
        """Add LDS ordinance detail information."""
        lines: str = Value.EMPTY
        return lines

    def lds_spouse_sealing(self, spouse: list[Any], level: int = 1) -> str:
        """Add LDS spouse sealing information."""
        lines: str = Value.EMPTY
        return lines

    def multimedia_link(self, media: list[Any], level: int = 1) -> str:
        """Add multimedia information."""
        lines: str = Value.EMPTY
        if len(media) > 0 and media[0] in self.multimedia_xreflist:
            lines = Value.EMPTY.join(
                [lines, f'{level} {Gedcom.OBJE} {media[0]}\n']
            )
            if len(media[1]) == 4:
                lines = Value.EMPTY.join(
                    [
                        lines,
                        f'{level + 1} {Gedcom.CROP}\n',
                        f'{level + 2} {Gedcom.TOP} {media[1][0]}\n',
                        f'{level + 2} {Gedcom.LEFT} {media[1][1]}\n',
                        f'{level + 2} {Gedcom.HEIGHT} {media[1][2]}\n',
                        f'{level + 2} {Gedcom.WIDTH} {media[1][3]}\n',
                    ]
                )
            if len(media) == 3:
                lines = Value.EMPTY.join(
                    [lines, f'{level + 1} {Gedcom.TITL} {media[2]}\n']
                )
        elif media[0] not in Enum.MEDI:
            raise ValueError(Msg.NOT_RECORD.format(media[0], Record.MULTIMEDIA))
        return lines

    def non_event_structure(self, event: list[Any], level: int = 1) -> str:
        """Add non event information."""
        lines: str = Value.EMPTY
        return lines

    def note_structure(self, note: list[Any], level: int = 1) -> str:
        """Add note information."""
        lines: str = Value.EMPTY
        return lines

    def personal_name_pieces(self, note: list[Any], level: int = 1) -> str:
        """Add pieces of personal name information."""
        lines: str = Value.EMPTY
        return lines

    def personal_name_structure(self, name: list[Any], level: int = 1) -> str:
        """Add note information."""
        lines: str = Value.EMPTY
        return lines

    def place_structure(self, place: list[Any], level: int = 1) -> str:
        """Add note information."""
        lines: str = Value.EMPTY
        return lines

    def source_citation(self, source: list[Any], level: int = 1) -> str:
        """Add source citation information."""
        lines: str = Value.EMPTY
        return lines

    def source_repository_citation(
        self, repository: list[Any], level: int = 1
    ) -> str:
        """Add source repository information."""
        lines: str = Value.EMPTY
        return lines

    ###### GEDCOM Records

    def family_xref(self) -> str:
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
        return self.next_counter(self.family_xreflist)

    def individual_xref(self) -> str:
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
        return self.next_counter(self.individual_xreflist)

    def family_record(
        self,
        xref: str,
        resn: str = Value.EMPTY,
        family_attributes: list[Any] | None = None,
        family_events: list[Any] | None = None,
        family_non_events: list[Any] | None = None,
        husband: str = GEDSpecial.VOID,
        husband_phrase: str = Value.EMPTY,
        wife: str = GEDSpecial.VOID,
        wife_phrase: str = Value.EMPTY,
        children: list[Any] | None = None,
        associations: list[Any] | None = None,
        submitters: list[Any] | None = None,
        lds_spouse_sealing: list[Any] | None = None,
        identifiers: list[Any] | None = None,
        notes: list[Any] | None = None,
        sources: list[Any] | None = None,
        multimedia: list[Any] | None = None,
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
        - husband_phrase: str = Value.EMPTY,
        - wife: str = GEDSpecial.VOID,
        - wife_phrase: str = Value.EMPTY,
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
        if resn != Value.EMPTY and resn not in Enum.RESN:
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
        level: int = 0
        ged_family: str = f'{level!s} {xref} {Gedcom.FAM}\n'
        if resn != Value.EMPTY and resn in Enum.RESN:
            ged_family = Value.EMPTY.join([ged_family, f'1 {Gedcom.RESN} {resn}\n'])
        for attribute in family_attributes:
            ged_family = Value.EMPTY.join([ged_family, self.family_attribute_structure(attribute)])
        for event in family_events:
            ged_family = Value.EMPTY.join([ged_family, self.family_event_structure(event)])
        for non_event in family_non_events:
            ged_family = Value.EMPTY.join([ged_family, self.non_event_structure(non_event)])
        ged_family = Value.EMPTY.join([ged_family, f'1 {Gedcom.HUSB} {husband}\n'])
        if husband_phrase != Value.EMPTY:
            ged_family = Value.EMPTY.join([ged_family, f'2 {Gedcom.PHRASE} {husband_phrase}\n'])
        ged_family = Value.EMPTY.join([ged_family, f'1 {Gedcom.WIFE} {wife}\n'])
        if wife_phrase != Value.EMPTY:
            ged_family = Value.EMPTY.join([ged_family, f'2 {Gedcom.PHRASE} {wife_phrase}\n'])
        for child, phrase in children:
            ged_family = Value.EMPTY.join([ged_family, f'1 {Gedcom.CHIL} {child}\n'])
            if phrase != Value.EMPTY:
                ged_family = Value.EMPTY.join([ged_family, f'2 {Gedcom.PHRASE} {phrase}\n'])
        for association in associations:
            ged_family = Value.EMPTY.join([ged_family, self.association_structure(association)])
        for submitter in submitters:
            ged_family = Value.EMPTY.join([ged_family, f'1 {Gedcom.SUBM} {submitter}\n'])
        for spouse in lds_spouse_sealing:
            ged_family = Value.EMPTY.join([ged_family, self.lds_spouse_sealing(spouse)])
        for identifier in identifiers:
            ged_family = Value.EMPTY.join([ged_family, self.identifier_structure(identifier)])
        for note in notes:
            ged_family = Value.EMPTY.join([ged_family, self.note_structure(note)])
        for source in sources:
            ged_family = Value.EMPTY.join([ged_family, self.source_citation(source)])
        for media in multimedia:
            ged_family = Value.EMPTY.join([ged_family, self.multimedia_link(media)])
        ged_family = Value.EMPTY.join([ged_family, self.creation_date()])
        self.ged_family = Value.EMPTY.join([self.ged_family, ged_family])
        logging.info(Msg.ADDED_RECORD.format(Record.FAMILY, xref))

    def individual_record(
        self,
        xref: str,
        resn: str = Value.EMPTY,
        personal_names: list[Any] | None = None,
        sex: str = Value.EMPTY,
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
    ) -> str:
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
        if resn != Value.EMPTY and resn not in Enum.RESN:
            raise ValueError(Msg.NOT_VALID_ENUM.format(resn, EnumName.RESN))
        if sex != Value.EMPTY and sex not in Enum.SEX:
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
        level: int = 0
        ged_individual: str = f'{level!s} {xref} {Gedcom.INDI}\n'
        if resn != Value.EMPTY and resn in Enum.RESN:
            ged_individual = Value.EMPTY.join([ged_individual, f'1 {Gedcom.RESN} {resn}\n'])
        for name in personal_names:
            ged_individual = Value.EMPTY.join([ged_individual, self.personal_name_structure(name)])
        if sex != Value.EMPTY and sex in Enum.SEX:
            ged_individual = Value.EMPTY.join([ged_individual, f'1 {Gedcom.SEX} {sex}\n'])
        for attribute in attributes:
            ged_individual = Value.EMPTY.join([ged_individual, self.individual_attribute_structure(attribute)])
        for event in events:
            ged_individual = Value.EMPTY.join([ged_individual, self.individual_event_structure(event)])
        for non_event in non_events:
            ged_individual = Value.EMPTY.join([ged_individual, self.non_event_structure(non_event)])
        for ordinance in lds_individual_ordinances:
            ged_individual = Value.EMPTY.join([ged_individual, self.lds_individual_ordinance(ordinance)])
        for family in families_child:
            if family[0] in self.family_xreflist:
                ged_individual = Value.EMPTY.join([ged_individual, f'1 {Gedcom.FAMC} {family[0]}\n'])
                if len(family) > 1:
                    ged_individual = Value.EMPTY.join([ged_individual, f'2 {Gedcom.PEDI} {family[1]}\n'])
                    if len(family) > 2:
                        ged_individual = Value.EMPTY.join(
                            [
                                ged_individual, 
                                f'3 {Gedcom.PHRASE} {family[2]}\n'
                            ]
                        )
                if len(family) > 3:
                    ged_individual = Value.EMPTY.join([ged_individual, f'2 {Gedcom.STAT} {family[2]}\n'])
                    if len(family) > 4:
                        ged_individual = Value.EMPTY.join(
                            [ged_individual, f'3 {Gedcom.PHRASE} {family[3]}\n']
                        )
        for family in families_spouse:
            if family[0] in self.family_xreflist:
                ged_individual = Value.EMPTY.join([ged_individual, f'1 {Gedcom.FAMS} {family[0]}\n'])
                if len(family) > 1:
                    ged_individual = Value.EMPTY.join([ged_individual, self.note_structure(family[1])])
        for submitter in submitters:
            if submitter in self.xref_submitter:
                ged_individual = Value.EMPTY.join([ged_individual, f'1 {Gedcom.SUBM} {submitter}\n'])
        for association in associations:
            ged_individual = Value.EMPTY.join([ged_individual, self.association_structure(association)])
        for alias in aliases:
            if alias[0] in self.individual_xreflist:
                ged_individual = Value.EMPTY.join([ged_individual, f'1 {Gedcom.ALIA} {alias[0]}\n\n'])
                if len(alias) > 1 and alias[1] != Value.EMPTY:
                    ged_individual = Value.EMPTY.join([ged_individual, f'2 {Gedcom.PHRASE} {alias[1]}\n'])
        for interest in ancestor_interest:
            if interest in self.submitter_xreflist:
                ged_individual = Value.EMPTY.join([ged_individual, f'1 {Gedcom.ANCI} {interest}\n'])
        for interest in descendent_interest:
            if interest in self.submitter_xreflist:
                ged_individual = Value.EMPTY.join([ged_individual, f'1 {Gedcom.DESI} {interest}\n'])
        for identifier in identifiers:
            ged_individual = Value.EMPTY.join([ged_individual, self.identifier_structure(identifier)])
        for note in notes:
            ged_individual = Value.EMPTY.join([ged_individual, self.note_structure(note)])
        for source in sources:
            ged_individual = Value.EMPTY.join([ged_individual, self.source_citation(source)])
        for media in multimedia:
            ged_individual = Value.EMPTY.join([ged_individual, self.multimedia_link(media)])
        ged_individual = Value.EMPTY.join([ged_individual, self.creation_date()])
        self.ged_individual = Value.EMPTY.join([self.ged_individual, ged_individual])
        logging.info(Msg.ADDED_RECORD.format(Record.INDIVIDUAL, xref))

    def multimedia_record(
        self,
        files: list[Any],
        resn: str = Value.EMPTY,
        identifiers: list[Any] | None = None,
        notes: list[Any] | None = None,
        sources: list[Any] | None = None,
    ) -> str:
        if identifiers is None:
            identifiers = []
        if notes is None:
            notes = []
        if sources is None:
            sources = []
        if resn != Value.EMPTY and resn not in Enum.RESN:
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
        if (
            len(file) > 3
            and file[3] != Value.EMPTY
            and file[3] not in Enum.MEDI
        ):
            raise ValueError(Msg.NOT_VALID_ENUM.format(file[3], EnumName.MEDI))
        level: int = 0
        xref: str = self.next_counter(self.multimedia_xreflist)
        ged_multimedia: str = f'{level!s} {xref} {Gedcom.OBJE}'
        if resn != Value.EMPTY:
            ged_multimedia = Value.EMPTY.join([ged_multimedia, f'1 {Gedcom.RESN} {resn}\n'])
        for file in files:
            ged_multimedia = Value.EMPTY.join([ged_multimedia, 
                    f'1 {Gedcom.FILE} {file[0]}\n',
                    f'2 {Gedcom.FORM} {file[1]}\n',
                ]
            )
            if len(file) > 2 and file[2] != Value.EMPTY:
                ged_multimedia = Value.EMPTY.join([ged_multimedia, f'3 {Gedcom.MEDI} {file[2]}\n'])
            if len(file) > 3 and file[3] != Value.EMPTY:
                ged_multimedia = Value.EMPTY.join([ged_multimedia, f'4 {Gedcom.PHRASE} {file[3]}\n'])
            if len(file) > 4 and file[4] != Value.EMPTY:
                ged_multimedia = Value.EMPTY.join([ged_multimedia, f'2 {Gedcom.TITL} {file[4]}\n'])
            if len(file) > 5 and len(file[5]) > 0:
                for translation in file[5]:
                    ged_multimedia = Value.EMPTY.join([ged_multimedia, 
                            f'2 {Gedcom.TRAN} {translation[0]}\n',
                            f'3 {Gedcom.FORM} {translation[1]}\n',
                        ]
                    )

        for identifier in identifiers:
            ged_multimedia = Value.EMPTY.join([ged_multimedia, self.identifier_structure(identifier)])
        for note in notes:
            ged_multimedia = Value.EMPTY.join([ged_multimedia, self.note_structure(note)])
        for source in sources:
            ged_multimedia = Value.EMPTY.join([ged_multimedia, self.source_citation(source)])
        ged_multimedia = Value.EMPTY.join([ged_multimedia, self.creation_date()])
        self.ged_multimedia = Value.EMPTY.join([self.ged_multimedia, ged_multimedia])
        logging.info(Msg.ADDED_RECORD.format(Record.MULTIMEDIA, xref))
        return xref

    def repository_record(
        self,
        name: str,
        address: list[Any] | None = None,
        phones: list[Any] | None = None,
        emails: list[Any] | None = None,
        faxes: list[Any] | None = None,
        wwws: list[Any] | None = None,
        notes: list[Any] | None = None,
        identifiers: list[Any] | None = None,
    ) -> str:
        if address is None:
            address = []
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
        level: int = 0
        xref: str = self.next_counter(self.repository_xreflist)
        ged_repository: str = f'{level!s} {xref} {Gedcom.REPO}\n'
        ged_repository = Value.EMPTY.join([ged_repository, f'1 {Gedcom.NAME} {name}\n'])
        for addr in address:
            ged_repository = Value.EMPTY.join([ged_repository, self.address_structure(addr)])
        for phone in phones:
            ged_repository = Value.EMPTY.join([ged_repository, f'1 {Gedcom.PHON} {phone}\n'])
        for email in emails:
            ged_repository = Value.EMPTY.join([ged_repository, f'1 {Gedcom.EMAIL} {email}\n'])
        for fax in faxes:
            ged_repository = Value.EMPTY.join([ged_repository, f'1 {Gedcom.FAX} {fax}\n'])
        for www in wwws:
            ged_repository = Value.EMPTY.join([ged_repository, f'1 {Gedcom.WWW} {www}\n'])
        for note in notes:
            ged_repository = Value.EMPTY.join([ged_repository, self.note_structure(note)])
        for identifier in identifiers:
            ged_repository = Value.EMPTY.join([ged_repository, self.identifier_structure(identifier)])
        ged_repository = Value.EMPTY.join([self.ged_repository, self.creation_date()])
        logging.info(Msg.ADDED_RECORD.format(Record.REPOSITORY, xref))
        return xref

    def shared_note_record(
        self,
        mime: str = Value.EMPTY,
        language: str = Value.EMPTY,
        translations: list[Any] | None = None,
        sources: list[Any] | None = None,
        identifiers: list[Any] | None = None,
    ) -> str:
        if translations is None:
            translations = []
        if sources is None:
            sources = []
        if identifiers is None:
            identifiers = []
        level: int = 0
        xref: str = self.next_counter(self.shared_note_xreflist)
        ged_shared_note: str = f'{level!s} {xref} {Gedcom.SNOTE}\n'
        if mime != Value.EMPTY and mime in Enum.MEDIA_TYPE:
            ged_shared_note = Value.EMPTY.join([ged_shared_note, f'1 {Gedcom.MIME} {mime}\n'])
        if language != Value.EMPTY:
            ged_shared_note = Value.EMPTY.join([ged_shared_note, f'1 {Gedcom.LANG} {language}\n'])
        for translation in translations:
            ged_shared_note = Value.EMPTY.join([ged_shared_note, self.add_translation(translation)])
        for source in sources:
            ged_shared_note = Value.EMPTY.join([ged_shared_note, self.source_citation(source)])
        for identifier in identifiers:
            ged_shared_note = Value.EMPTY.join([ged_shared_note, self.identifier_structure(identifier)])
        ged_shared_note = Value.EMPTY.join([ged_shared_note, self.creation_date()])
        self.ged_shared_note = Value.EMPTY.join([self.ged_shared_note, ged_shared_note])
        logging.info(Msg.ADDED_RECORD.format(Record.SHARED_NOTE, xref))
        return xref

    def source_record(
        self,
        events: list[Any] | None = None,
        author: str = Value.EMPTY,
        title: str = Value.EMPTY,
        abbreviation: str = Value.EMPTY,
        publisher: str = Value.EMPTY,
        text: str = Value.EMPTY,
        mime: str = Value.EMPTY,
        language: str = Value.EMPTY,
        sources: list[Any] | None = None,
        identifiers: list[Any] | None = None,
        notes: list[Any] | None = None,
        multimedia: list[Any] | None = None,
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
        if mime != Value.EMPTY and mime not in Enum.MEDIA_TYPE:
            raise ValueError(
                Msg.NOT_VALID_ENUM.format(mime, EnumName.MEDIA_TYPE)
            )
        if len(multimedia) > 0:
            for media in multimedia:
                if media[0] not in self.multimedia_xreflist:
                    raise ValueError(
                        Msg.NOT_RECORD.format(media[0], Record.MULTIMEDIA)
                    )
        if len(identifiers) > 0:
            for id in identifiers:
                if id[0] not in Enum.ID:
                    raise ValueError(
                        Msg.NOT_VALID_ENUM.format(mime, EnumName.ID)
                    )
        level: int = 0
        xref: str = self.next_counter(self.source_xreflist)
        ged_source: str = f'{level!s} {xref} {Gedcom.SOUR}\n'
        if len(events) > 0:
            ged_source = Value.EMPTY.join([ged_source, f'1 {Gedcom.DATA}\n'])
            for event in events:
                ged_source = Value.EMPTY.join([ged_source, f'2 {Gedcom.EVEN} {event[0]}\n'])
                if len(event) > 1:
                    ged_source = Value.EMPTY.join([ged_source, f'3 {Gedcom.DATE} {event[1]}\n'])
                if len(event) > 2:
                    ged_source = Value.EMPTY.join([ged_source, f'4 {Gedcom.PHRASE} {event[2]}\n'])
                if len(event) > 3:
                    ged_source = Value.EMPTY.join([ged_source, f'2 {Gedcom.AGNC} {event[3]}\n'])
                if len(event) > 4:
                    ged_source = Value.EMPTY.join([ged_source, self.note_structure(event[4])])
        if author != Value.EMPTY:
            ged_source = Value.EMPTY.join([ged_source, f'1 {Gedcom.AUTH} {author}\n'])
        if title != Value.EMPTY:
            ged_source = Value.EMPTY.join([ged_source, f'1 {Gedcom.TITL} {title}\n'])
        if abbreviation != Value.EMPTY:
            ged_source = Value.EMPTY.join([ged_source, f'1 {Gedcom.ABBR} {abbreviation}\n'])
        if publisher != Value.EMPTY:
            ged_source = Value.EMPTY.join([ged_source, f'1 {Gedcom.PUBL} {publisher}\n'])
        if text != Value.EMPTY:
            ged_source = Value.EMPTY.join([ged_source, f'1 {Gedcom.TEXT} {text}\n'])
        if mime != Value.EMPTY and mime in Enum.MEDIA_TYPE:
            ged_source = Value.EMPTY.join([ged_source, f'2 {Gedcom.MIME} {mime}\n'])
        if language != Value.EMPTY:
            ged_source = Value.EMPTY.join([ged_source, f'2 {Gedcom.LANG} {language}\n'])
        for source in sources:
            ged_source = Value.EMPTY.join([ged_source, self.source_repository_citation(source)])
        for identifier in identifiers:
            ged_source = Value.EMPTY.join([ged_source, self.identifier_structure(identifier)])
        for note in notes:
            ged_source = Value.EMPTY.join([ged_source, self.note_structure(note)])
        for media in multimedia:
            ged_source = Value.EMPTY.join([ged_source, self.multimedia_link(media)])
        ged_source = Value.EMPTY.join([ged_source, self.creation_date()])
        self.ged_source = Value.EMPTY.join([self.ged_source, ged_source])
        logging.info(Msg.ADDED_RECORD.format(Record.SOURCE, xref))
        return xref

    def submitter_record(
        self,
        name: str,
        address: list[Any] | None = None,
        phones: list[Any] | None = None,
        emails: list[Any] | None = None,
        faxes: list[Any] | None = None,
        wwws: list[Any] | None = None,
        multimedia: list[Any] | None = None,
        languages: list[Any] | None = None,
        identifiers: list[Any] | None = None,
        notes: list[Any] | None = None,
    ) -> str:
        if address is None:
            address = []
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
        level: int = 0
        xref: str = self.next_counter(self.submitter_xreflist)
        ged_submitter: str = f'{level!s} {xref} {Gedcom.SUBM}\n'
        ged_submitter = Value.EMPTY.join([ged_submitter, f'1 {Gedcom.NAME} {name}\n'])
        ged_submitter = Value.EMPTY.join([ged_submitter, self.address_structure(address)])
        for phone in phones:
            ged_submitter = Value.EMPTY.join([ged_submitter, f'1 {Gedcom.PHON} {phone}\n'])
        for email in emails:
            ged_submitter = Value.EMPTY.join([ged_submitter, f'1 {Gedcom.EMAIL} {email}\n'])
        for fax in faxes:
            ged_submitter = Value.EMPTY.join([ged_submitter, f'1 {Gedcom.FAX} {fax}\n'])
        for www in wwws:
            ged_submitter = Value.EMPTY.join([ged_submitter, f'1 {Gedcom.WWW} {www}\n'])
        for media in multimedia:
            ged_submitter = Value.EMPTY.join([ged_submitter, self.multimedia_link(media)])
        for language in languages:
            ged_submitter = Value.EMPTY.join([ged_submitter, f'1 {Gedcom.LANG} {language}\n'])
        for identifier in identifiers:
            ged_submitter = Value.EMPTY.join([ged_submitter, self.identifier_structure(identifier)])
        for note in notes:
            ged_submitter = Value.EMPTY.join([ged_submitter, self.note_structure(note)])
        ged_submitter = Value.EMPTY.join([ged_submitter, self.creation_date()])
        self.ged_submitter = Value.EMPTY.join(
            [self.ged_submitter, ged_submitter]
        )
        logging.info(Msg.ADDED_RECORD.format(Record.SUBMITTER, xref))
        return xref

    ###### GEDCOM Special Records

    def header(
        self,
        schemas: list[str] | None = None,
        source: str = Value.EMPTY,
        vers: str = Value.EMPTY,
        name: str = Value.EMPTY,
        corp: str = Value.EMPTY,
        address: list[Any] | None = None,
        phones: list[str] | None = None,
        emails: list[str] | None = None,
        faxes: list[str] | None = None,
        wwws: list[str] | None = None,
        data: str = Value.EMPTY,
        date: str = Value.EMPTY,
        time: str = Value.EMPTY,
        dest: str = Value.EMPTY,
        submitter: str = Value.EMPTY,
        copr: str = Value.EMPTY,
        language: str = Value.EMPTY,
        place: list[Any] | None = None,
        note: list[Any] | None = None,
    ) -> None:
        if (
            submitter != Value.EMPTY
            and submitter not in self.submitter_xreflist
        ):
            raise ValueError(Msg.NOT_RECORD.format(submitter, Record.SUBMITTER))
        if schemas is None:
            schemas = []
        if address is None:
            address = []
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
            note = []
        ged_header: str = (
            f'0 {Gedcom.HEAD}\n'
            f'1 {Gedcom.GEDC}\n'
            f'2 {Gedcom.VERS} {GEDSpecial.VERSION}\n'
        )
        if len(schemas) > 0:
            ged_header = Value.EMPTY.join([ged_header, f'1 {Gedcom.SCHMA}\n'])
            for schema in schemas:
                ged_header = Value.EMPTY.join(
                    [ged_header, f'2 {Gedcom.TAG} {schema}\n']
                )
        if source != Value.EMPTY:
            ged_header = Value.EMPTY.join(
                [ged_header, f'1 {Gedcom.SOUR} {source}\n']
            )
        if vers != Value.EMPTY:
            ged_header = Value.EMPTY.join(
                [ged_header, f'2 {Gedcom.VERS} {vers}\n']
            )
        if name != Value.EMPTY:
            ged_header = Value.EMPTY.join(
                [ged_header, f'2 {Gedcom.NAME} {name}\n']
            )
        if corp != Value.EMPTY:
            ged_header = Value.EMPTY.join(
                [ged_header, f'2 {Gedcom.CORP} {corp}\n']
            )
        address_out = self.address_structure(address, level=3)
        ged_header = Value.EMPTY.join([ged_header, address_out])
        for phone in phones:
            ged_header = Value.EMPTY.join(
                [ged_header, f'3 {Gedcom.PHON} {phone}\n']
            )
        for email in emails:
            ged_header = Value.EMPTY.join(
                [ged_header, f'3 {Gedcom.EMAIL} {email}\n']
            )
        for fax in faxes:
            ged_header = Value.EMPTY.join(
                [ged_header, f'3 {Gedcom.FAX} {fax}\n']
            )
        for www in wwws:
            ged_header = Value.EMPTY.join([f'3 {Gedcom.WWW} {www}\n'])
        if data != Value.EMPTY:
            ged_header = Value.EMPTY.join(
                [ged_header, f'2 {Gedcom.DATA} {source[9]}\n']
            )
        if date != Value.EMPTY:
            ged_header = Value.EMPTY.join(
                [ged_header, f'3 {Gedcom.DATE} {date}\n']
            )
        if time != Value.EMPTY:
            ged_header = Value.EMPTY.join(
                [ged_header, f'4 {Gedcom.TIME} {time}\n']
            )
        if dest != Value.EMPTY:
            ged_header = Value.EMPTY.join(
                [ged_header, f'1 {Gedcom.DEST} {dest}\n']
            )
        now_out = self.now(level=1)
        ged_header = Value.EMPTY.join([ged_header, now_out])
        if submitter != Value.EMPTY:
            ged_header = Value.EMPTY.join(
                [ged_header, f'1 {Gedcom.SUBM} {submitter}\n']
            )
        if copr != Value.EMPTY:
            ged_header = Value.EMPTY.join([f'1 {Gedcom.COPR} {copr}\n'])
        if language != Value.EMPTY:
            ged_header = Value.EMPTY.join(
                [ged_header, f'1 {Gedcom.LANG} {language}\n']
            )
        if len(place) > 0:
            ged_header = Value.EMPTY.join(
                [
                    ged_header,
                    f'1 {Gedcom.PLAC} {place[0]}\n',
                    f'2 {Gedcom.FORM} {place[1]}\n',
                ]
            )
        note_out: str = self.note_structure(note)
        ged_header = Value.EMPTY.join([ged_header, note_out])
        self.ged_header = ged_header
