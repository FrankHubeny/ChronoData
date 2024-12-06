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
        self.xref_family: list[int] = []
        self.xref_individual: list[int] = []
        self.xref_multimedia: list[int] = []
        self.xref_repository: list[int] = []
        self.xref_shared_note: list[int] = []
        self.xref_source: list[int] = []
        self.xref_submitter: list[int] = []

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

    def now(self, level: int = 2) -> list[str]:
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
        return [
            f'{level} {Gedcom.DATE} {date}',
            f'{level + 1} {Gedcom.TIME} {time}',
        ]

    def change_date(self, note: list[str] | None = None) -> list[str]:
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
        lines = [f'1 {Gedcom.CHAN}']
        lines.extend(self.now())
        lines.extend(self.note_structure(note))
        return lines

    def creation_date(self) -> list[str]:
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
        lines = [f'1 {Gedcom.CREA}']
        lines.extend(self.now())
        return lines

    def date_value(
        self,
        date: str,
        time: str = Value.EMPTY,
        phrase: str = Value.EMPTY,
        level: int = 1,
    ) -> list[str]:
        level2: int = level + 1
        if len(date) == 0:
            logging.error(Msg.NO_VALUE)
            raise ValueError(Msg.NO_VALUE)
        if time == Value.EMPTY and phrase == Value.EMPTY:
            return [f'{level} {Gedcom.DATE} {date}']
        if time != Value.EMPTY and phrase == Value.EMPTY:
            return [
                f'{level} {Gedcom.DATE} {date}',
                f'{level2} {Gedcom.TIME} {time}',
            ]
        if time == Value.EMPTY and phrase != Value.EMPTY:
            return [
                f'{level} {Gedcom.DATE} {date}',
                f'{level2} {Gedcom.PHRASE} {phrase}',
            ]
        return [
            f'{level} {Gedcom.DATE} {date}',
            f'{level2} {Gedcom.TIME} {time}',
            f'{level2} {Gedcom.PHRASE} {phrase}',
        ]

    # def note(
    #     self,
    #     text: str,
    #     mime: str = Value.EMPTY,
    #     lang: str = Value.EMPTY,
    #     trans: list | None = None,
    #     source: list | None = None,
    #     counter: int = 1,
    # ) -> dict[str, dict[str, str]]:
    #     counter2: int = counter + 1
    #     counter3: int = counter + 1
    #     line1 = f'{counter} {Gedcom.TEXT} {text}\n'
    #     line2: str = Value.EMPTY
    #     line3: str = Value.EMPTY
    #     transline: str = Value.EMPTY
    #     sourceline: str = Value.EMPTY
    #     if mime in Enum.MEDIA_TYPE:
    #         line2 = f'{counter2} {Gedcom.MIME} {mime}\n'
    #     if lang != Value.EMPTY:
    #         line3 = f'{counter2} {Gedcom.LANG} {lang}\n'
    #     for translation in trans:
    #         transline = Value.EMPTY.join(
    #             [
    #                 transline,
    #                 f'{counter2} {Gedcom.TRAN} {translation[0]}\n',
    #                 f'{counter3} {Gedcom.MIME} {translation[1]}\n',
    #                 f'{counter3} {Gedcom.LANG} {translation[2]}\n',
    #             ]
    #         )
    #     for reference in source:
    #         sourceline = Value.EMPTY.join(
    #             [sourceline, f'{counter} {Gedcom.SOUR} {reference}\n']
    #         )
    #     return Value.EMPTY.join([line1, line2, line3, transline, sourceline])

    ###### Methods to Assisting Building GEDCOM Records

    def next_counter(self, record: list[int]) -> str:
        counter: int = self.xref_counter
        xref: str = Value.EMPTY.join(
            [GEDSpecial.ATSIGN, str(counter), GEDSpecial.ATSIGN]
        )
        record.append(xref)
        self.xref_counter += 1
        return xref

    def address_structure(
        self, address: list[Any], level: int = 1
    ) -> list[str]:
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
        lines: list[str] = []
        if len(address) > 0:
            address_lines = address[0].split('\n')
            lines.extend([f'{level} {Gedcom.ADDR} {address_lines[0]}'])
            for line in address_lines[1:]:
                lines.extend([f'{level} {Gedcom.CONT} {line}'])
            if len(address) > 1 and address[1] != Value.EMPTY:
                lines.extend([f'{level + 1} {Gedcom.CITY} {address[1]}'])
            if len(address) > 2 and address[2] != Value.EMPTY:
                lines.extend([f'{level + 1} {Gedcom.STAE} {address[2]}'])
            if len(address) > 3 and address[3] != Value.EMPTY:
                lines.extend([f'{level + 1} {Gedcom.POST} {address[3]}'])
            if len(address) > 4 and address[4] != Value.EMPTY:
                lines.extend([f'{level + 1} {Gedcom.CTRY} {address[4]}'])
        return lines

    # def add_anci(self, anci: list[Any], level: int = 1) -> list[str]:
    #     """Add anci information."""
    #     lines: list[str] = []
    #     return lines

    def association_structure(
        self, association: list[Any], level: int = 1
    ) -> list[str]:
        """Add association information."""
        lines: list[str] = []
        if association[0] in self.xref_individual:
            lines.extend([f'{level} {Gedcom.ASSO} {association[0]}'])
            if association[1] != Value.EMPTY:
                lines.extend([f'{level + 1} {Gedcom.PHRASE} {association[1]}'])
            if association[2] in Enum.ROLE:
                lines.extend([f'{level + 2} {Gedcom.ROLE} {association[2]}'])
                if association[3] != Value.EMPTY:
                    lines.extend(
                        [f'{level + 2} {Gedcom.PHRASE} {association[3]}']
                    )
            else:
                raise ValueError(
                    Msg.NOT_VALID_ENUM.format(association[2], EnumName.ROLE)
                )
            lines.extend(self.note_structure(association[4]))
            lines.extend(self.source_citation(association[5]))
        else:
            raise ValueError(
                Msg.NOT_RECORD.format(association[0], Record.INDIVIDUAL)
            )
        return lines

    def event_detail(self, event: list[Any], level: int = 1) -> list[str]:
        """Add event detail information."""
        lines: list[str] = []
        return lines

    def family_attribute_structure(
        self, attribute: list[Any], level: int = 1
    ) -> list[str]:
        """Add attribute information."""
        lines: list[str] = []
        return lines

    def family_event_detail(
        self, detail: list[Any], level: int = 1
    ) -> list[str]:
        """Add family event detail information."""
        lines: list[str] = []
        return lines

    def family_event_structure(
        self, event: list[Any], level: int = 1
    ) -> list[str]:
        """Add family event information."""
        lines: list[str] = []
        return lines

    def identifier_structure(
        self, identifier: list[str], level: int = 1
    ) -> list[str]:
        """Add an identifier to a record.

        Each identifier is a list contain at least two strings and at most three.
        The first string is the kind of identifier.
        The second string is the identifier itself.
        The optional third is the type of identifier.
        """
        lines: list[str] = []
        if (
            identifier[0] in Enum.ID
            and len(identifier) > 1
            and len(identifier) < 4
        ):
            if len(identifier) > 1:
                lines.extend([f'{level} {identifier[0][0]} {identifier[0][1]}'])
            if len(identifier) > 2:
                lines.extend(f'{level + 1} {Gedcom.TYPE} {identifier[0][2]}')
        return lines

    def individual_attribute_structure(
        self, attribute: list[Any], level: int = 1
    ) -> list[str]:
        """Add individual attribute information."""
        lines: list[str] = []
        return lines

    def individual_event_detail(
        self, detail: list[Any], level: int = 1
    ) -> list[str]:
        """Add individual event detail information."""
        lines: list[str] = []
        return lines

    def individual_event_structure(
        self, event: list[Any], level: int = 1
    ) -> list[str]:
        """Add individual event information."""
        lines: list[str] = []
        return lines

    def lds_individual_ordinance(
        self, ordinance: list[Any], level: int = 1
    ) -> list[str]:
        """Add LDS individual ordinance information."""
        lines: list[str] = []
        return lines

    def lds_ordinance_detail(
        self, detail: list[Any], level: int = 1
    ) -> list[str]:
        """Add LDS ordinance detail information."""
        lines: list[str] = []
        return lines

    def lds_spouse_sealing(
        self, spouse: list[Any], level: int = 1
    ) -> list[str]:
        """Add LDS spouse sealing information."""
        lines: list[str] = []
        return lines

    def multimedia_link(self, media: list[Any], level: int = 1) -> list[str]:
        """Add multimedia information."""
        lines: list[str] = []
        if len(media) > 0 and media[0] in self.xref_multimedia:
            lines.extend([f'{level} {Gedcom.OBJE} {media[0]}'])
            if len(media[1]) == 4:
                lines.extend(
                    [
                        f'{level + 1} {Gedcom.CROP}',
                        f'{level + 2} {Gedcom.TOP} {media[1][0]}',
                        f'{level + 2} {Gedcom.LEFT} {media[1][1]}',
                        f'{level + 2} {Gedcom.HEIGHT} {media[1][2]}',
                        f'{level + 2} {Gedcom.WIDTH} {media[1][3]}',
                    ]
                )
            if len(media) == 3:
                lines.extend([f'{level + 1} {Gedcom.TITL} {media[2]}'])
        elif media[0] not in Enum.MEDI:
            raise ValueError(Msg.NOT_RECORD.format(media[0], Record.MULTIMEDIA))
        return lines

    def non_event_structure(
        self, event: list[Any], level: int = 1
    ) -> list[str]:
        """Add non event information."""
        lines: list[str] = []
        return lines

    def note_structure(self, note: list[Any], level: int = 1) -> list[str]:
        """Add note information."""
        lines: list[str] = []
        return lines

    def personal_name_pieces(
        self, note: list[Any], level: int = 1
    ) -> list[str]:
        """Add pieces of personal name information."""
        lines: list[str] = []
        return lines

    def personal_name_structure(
        self, name: list[Any], level: int = 1
    ) -> list[str]:
        """Add note information."""
        lines: list[str] = []
        return lines

    def place_structure(self, place: list[Any], level: int = 1) -> list[str]:
        """Add note information."""
        lines: list[str] = []
        return lines

    def source_citation(self, source: list[Any], level: int = 1) -> list[str]:
        """Add source citation information."""
        lines: list[str] = []
        return lines

    def source_repository_citation(
        self, repository: list[Any], level: int = 1
    ) -> list[str]:
        """Add source repository information."""
        lines: list[str] = []
        return lines

    # def add_data(self, data: list[Any], level: int = 1) -> list[str]:
    #     """Add data information."""
    #     lines: list[str] = []
    #     return lines

    # def add_desi(self, desi: list[Any], level: int = 1) -> list[str]:
    #     """Add desi information."""
    #     lines: list[str] = []
    #     return lines

    # def add_fam(self, fam: list[Any], level: int = 1) -> list[str]:
    #     """Add fam information."""
    #     lines: list[str] = []
    #     return lines

    # def add_family(self, family: list[Any], level: int = 1) -> list[str]:
    #     """Add family information."""
    #     lines: list[str] = []
    #     return lines

    # def add_family_attribute(
    #     self, attribute: list[Any], level: int = 1
    # ) -> list[str]:
    #     """Add family attribute information."""
    #     lines: list[str] = []
    #     return lines

    # def add_family_event(self, event: list[Any], level: int = 1) -> list[str]:
    #     """Add family event information."""
    #     lines: list[str] = []
    #     return lines

    # def add_family_non_event(
    #     self, event: list[Any], level: int = 1
    # ) -> list[str]:
    #     """Add family non-event information."""
    #     lines: list[str] = []
    #     return lines

    # def add_file(self, file: list[Any], level: int = 1) -> list[str]:
    #     """Add file information."""
    #     lines: list[str] = []
    #     return lines

    # def add_header_source(self, source: list[Any], level: int = 1) -> list[str]:
    #     """Add source information for the header."""
    #     lines: list[str] = []
    #     return lines

    # def add_individual_event(
    #     self, event: list[Any], level: int = 1
    # ) -> list[str]:
    #     """Add individual event information."""
    #     lines: list[str] = []
    #     return lines

    # def add_lds_spouse(self, spouse: list[Any], level: int = 1) -> list[str]:
    #     """Add LDS spouse information."""
    #     lines: list[str] = []
    #     return lines

    # def add_name(self, name: list[Any], level: int = 1) -> list[str]:
    #     """Add name information."""
    #     lines: list[str] = []
    #     return lines

    # def add_ordinance(self, ordinance: list[Any], level: int = 1) -> list[str]:
    #     """Add LDS ordinance information."""
    #     lines: list[str] = []
    #     return lines

    # def add_place(self, place: list[Any], level: int = 1) -> list[str]:
    #     """Add place information."""
    #     lines: list[str] = []
    #     return lines

    # def source_citation(self, source: list[Any], level: int = 1) -> list[str]:
    #     """Add source information."""
    #     lines: list[str] = []
    #     return lines

    # def add_submitter(self, submitter: list[Any], level: int = 1) -> list[str]:
    #     """Add submitter information."""
    #     lines: list[str] = []
    #     return lines

    # def add_translation(
    #     self, translation: list[Any], level: int = 1
    # ) -> list[str]:
    #     """Add translation information."""
    #     lines: list[str] = []
    #     return lines

    ###### GEDCOM Records

    def family_record(
        self,
        resn: str = Value.EMPTY,
        family_attributes: list[Any] | None = None,
        family_events: list[Any] | None = None,
        family_non_events: list[Any] | None = None,
        husband: str = Value.EMPTY,
        husband_phrase: str = Value.EMPTY,
        wife: str = Value.EMPTY,
        wife_phrase: str = Value.EMPTY,
        children: list[Any] | None = None,
        associations: list[Any] | None = None,
        submitters: list[Any] | None = None,
        lds_spouse_sealing: list[Any] | None = None,
        identifiers: list[Any] | None = None,
        notes: list[Any] | None = None,
        sources: list[Any] | None = None,
        multimedia: list[Any] | None = None,
    ) -> str:
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
        level: int = 0
        xref: str = self.next_counter(self.xref_family)
        json_family: dict[str, dict[str, str]] = {}
        ged_family: list[str] = [
            f'{level!s} {xref} {Gedcom.FAM}',
        ]
        if resn != Value.EMPTY and resn in Enum.RESN:
            ged_family.extend([f'1 {Gedcom.RESN} {resn}'])
        for attribute in family_attributes:
            ged_family.extend(self.family_attribute_structure(attribute))
        for event in family_events:
            ged_family.extend(self.family_event_structure(event))
        for non_event in family_non_events:
            ged_family.extend(self.non_event_structure(non_event))
        if husband != Value.EMPTY:
            ged_family.extend([f'1 {Gedcom.HUSB} {husband}'])
            if husband_phrase != Value.EMPTY:
                ged_family.extend([f'2 {Gedcom.PHRASE} {husband_phrase}'])
        if wife != Value.EMPTY:
            ged_family.extend([f'1 {Gedcom.WIFE} {wife}'])
            if wife_phrase != Value.EMPTY:
                ged_family.extend([f'2 {Gedcom.PHRASE} {wife_phrase}'])
        for child, phrase in children:
            ged_family.extend(f'1 {Gedcom.CHIL} {child}')
            if phrase != Value.EMPTY:
                ged_family.extend(f'2 {Gedcom.PHRASE} {phrase}')
        for association in associations:
            ged_family.extend(self.association_structure(association))
        for submitter in submitters:
            ged_family.extend(f'1 {Gedcom.SUBM} {submitter}')
        for spouse in lds_spouse_sealing:
            ged_family.extend(self.lds_spouse_sealing(spouse))
        for identifier in identifiers:
            ged_family.extend(self.identifier_structure(identifier))
        for note in notes:
            ged_family.extend(self.note_structure(note))
        for source in sources:
            ged_family.extend(self.source_citation(source))
        for media in multimedia:
            ged_family.extend(self.multimedia_link(media))
        ged_family.extend(self.creation_date())
        self.ged_family.extend(ged_family)

        self.chron[Gedcom.FAM].update(json_family)
        logging.info(Msg.ADDED_RECORD.format(Record.FAMILY, xref))
        return xref

    def individual_record(
        self,
        resn: str = Value.EMPTY,
        personal_names: list[Any] | None = None,
        sex: str = Value.EMPTY,
        attributes: list[Any] | None = None,
        events: list[Any] | None = None,
        non_events: list[Any] | None = None,
        lds_individual_ordinances: list[Any] | None = None,
        families: list[Any] | None = None,
        fams: list[Any] | None = None,
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
        if resn != Value.EMPTY and resn not in Enum.RESN:
            raise ValueError(
                Msg.NOT_VALID_ENUM.format(resn, EnumName.RESN)
            )
        if sex != Value.EMPTY and sex not in Enum.SEX:
            raise ValueError(
                Msg.NOT_VALID_ENUM.format(sex, EnumName.SEX)
            )
        for family in families:
            if len(family) > 1 and family[1] not in Enum.PEDI:
                raise ValueError(
                    Msg.NOT_VALID_ENUM.format(family[3], EnumName.PEDI)
                )
            if len(family) > 3 and family[3] not in Enum.STAT:
                raise ValueError(
                    Msg.NOT_VALID_ENUM.format(family[3], EnumName.STAT)
                )
        for alias in aliases:
            if alias[0] not in self.xref_individual:
                raise ValueError(
                    Msg.NOT_RECORD.format(alias[0], Record.INDIVIDUAL)
                )
        for interest in ancestor_interest:
            if interest not in self.xref_submitter:
                raise ValueError(
                    Msg.NOT_RECORD.format(interest, Record.SUBMITTER)
                )
        for interest in descendent_interest:
            if interest not in self.xref_submitter:
                raise ValueError(
                    Msg.NOT_RECORD.format(interest, Record.SUBMITTER)
                )
        for submitter in submitters:
            if submitter not in self.xref_submitter:
                raise ValueError(
                    Msg.NOT_RECORD.format(submitter, Record.SUBMITTER)
                )
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
        if families is None:
            families = []
        if fams is None:
            fams = []
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
        level: int = 0
        xref: str = self.next_counter(self.xref_individual)
        json_individual: dict[str, dict[str, str]] = {}

        ged_individual: list[str] = [
            f'{level!s} {xref} {Gedcom.INDI}',
        ]
        if resn != Value.EMPTY and resn in Enum.RESN:
            ged_individual.extend([f'1 {Gedcom.RESN} {resn}'])
        for name in personal_names:
            ged_individual.extend(self.personal_name_structure(name))
        if sex != Value.EMPTY and sex in Enum.SEX:
            ged_individual.extend([f'1 {Gedcom.SEX} {sex}'])
        for attribute in attributes:
            ged_individual.extend(
                self.individual_attribute_structure(attribute)
            )
        for event in events:
            ged_individual.extend(self.individual_event_structure(event))
        for non_event in non_events:
            ged_individual.extend(self.non_event_structure(non_event))
        for ordinance in lds_individual_ordinances:
            ged_individual.extend(self.lds_individual_ordinance(ordinance))
        for family in families:
            if family[0] in self.xref_family:
                ged_individual.extend([f'1 {Gedcom.FAMC} {family[0]}'])
                if len(family) > 1:
                    ged_individual.extend([f'2 {Gedcom.PEDI} {family[1]}'])
                    if len(family) > 2:
                        ged_individual.extend(
                            [f'3 {Gedcom.PHRASE} {family[2]}']
                        )
                if len(family) > 3:
                    ged_individual.extend([f'2 {Gedcom.STAT} {family[2]}'])
                    if len(family) > 4:
                        ged_individual.extend(
                            [f'3 {Gedcom.PHRASE} {family[3]}']
                        )
        for family in fams:
            if family[0] in self.xref_family:
                ged_individual.extend([f'1 {Gedcom.FAMS} {family[0]}'])
                if len(family) > 1:
                    ged_individual.extend(self.note_structure(family[1]))
        for submitter in submitters:
            if submitter in self.xref_submitter:
                ged_individual.extend([f'1 {Gedcom.SUBM} {submitter}'])
        for association in associations:
            ged_individual.extend(self.association_structure(association))
        for alias in aliases:
            if alias[0] in self.xref_individual:
                ged_individual.extend([f'1 {Gedcom.ALIA} {alias[0]}'])
                if len(alias) > 1 and alias[1] != Value.EMPTY:
                    ged_individual.extend([f'2 {Gedcom.PHRASE} {alias[1]}'])
        for interest in ancestor_interest:
            if interest in self.xref_submitter:
                ged_individual.extend([f'1 {Gedcom.ANCI} {interest}'])
        for interest in descendent_interest:
            if interest in self.xref_submitter:
                ged_individual.extend([f'1 {Gedcom.DESI} {interest}'])
        for identifier in identifiers:
            ged_individual.extend(self.identifier_structure(identifier))
        for note in notes:
            ged_individual.extend(self.note_structure(note))
        for source in sources:
            ged_individual.extend(self.source_citation(source))
        for media in multimedia:
            ged_individual.extend(self.multimedia_link(media))
        ged_individual.extend(self.creation_date())
        self.ged_individual.extend(ged_individual)

        self.chron[Gedcom.INDI].update(json_individual)
        logging.info(Msg.ADDED_RECORD.format(Record.INDIVIDUAL, xref))
        return xref

    def multimedia_record(
        self,
        resn: str = Value.EMPTY,
        files: list[Any] | None = None,
        identifiers: list[Any] | None = None,
        notes: list[Any] | None = None,
        sources: list[Any] | None = None,
    ) -> str:
        if files is None:
            files = []
        if identifiers is None:
            identifiers = []
        if notes is None:
            notes = []
        if sources is None:
            sources = []
        level: int = 0
        xref: str = self.next_counter(self.xref_multimedia)
        json_multimedia: dict[str, dict[str, str]] = {}

        ged_multimedia: list[str] = [
            f'{level!s} {xref} {Gedcom.OBJE}',
        ]
        if resn != Value.EMPTY and resn in Enum.RESN:
            ged_multimedia.extend([f'1 {Gedcom.RESN} {resn}'])
        ged_multimedia.extend(self.creation_date())
        for file in files:
            ged_multimedia.extend(self.add_file(file))
        for identifier in identifiers:
            ged_multimedia.extend(self.identifier_structure(identifier))
        for note in notes:
            ged_multimedia.extend(self.note_structure(note))
        for source in sources:
            ged_multimedia.extend(self.source_citation(source))
        self.ged_multimedia.extend(ged_multimedia)

        self.chron[Gedcom.OBJE].update(json_multimedia)
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
        if name == Value.EMPTY:
            raise ValueError(Msg.NO_NAME)
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
        xref: str = self.next_counter(self.xref_repository)
        json_repository: dict[str, dict[str, str]] = {}

        ged_repository: list[str] = [
            f'{level!s} {xref} {Gedcom.REPO}',
        ]
        ged_repository.extend([f'1 {Gedcom.NAME} {name}'])
        for addr in address:
            ged_repository.extend(self.address_structure(addr))
        for phone in phones:
            ged_repository.extend(f'1 {Gedcom.PHON} {phone}')
        for email in emails:
            ged_repository.extend(f'1 {Gedcom.EMAIL} {email}')
        for fax in faxes:
            ged_repository.extend(f'1 {Gedcom.FAX} {fax}')
        for www in wwws:
            ged_repository.extend(f'1 {Gedcom.WWW} {www}')
        for note in notes:
            ged_repository.extend(self.note_structure(note))
        for identifier in identifiers:
            ged_repository.extend(self.identifier_structure(identifier))
        ged_repository.extend(self.creation_date())

        self.chron[Gedcom.REPO].update(json_repository)
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
        xref: str = self.next_counter(self.xref_shared_note)
        json_shared_note: dict[str, dict[str, str]] = {}

        ged_shared_note: list[str] = [
            f'{level!s} {xref} {Gedcom.SNOTE}',
        ]
        if mime != Value.EMPTY and mime in Enum.MEDIA_TYPE:
            ged_shared_note.extend(f'1 {Gedcom.MIME} {mime}')
        if language != Value.EMPTY:
            ged_shared_note.extend(f'1 {Gedcom.LANG} {language}')
        for translation in translations:
            ged_shared_note.extend(self.add_translation(translation))
        for source in sources:
            ged_shared_note.extend(self.source_citation(source))
        for identifier in identifiers:
            ged_shared_note.extend(self.identifier_structure(identifier))
        ged_shared_note.extend(self.creation_date())
        self.ged_shared_note.extend(ged_shared_note)

        self.chron[Gedcom.SNOTE].update(json_shared_note)
        logging.info(Msg.ADDED_RECORD.format(Record.SHARED_NOTE, xref))
        return xref

    def source_record(
        self,
        data: list[Any] | None = None,
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
        if data is None:
            data = []
        if identifiers is None:
            identifiers = []
        if multimedia is None:
            multimedia = []
        if notes is None:
            notes = []
        if sources is None:
            sources = []
        level: int = 0
        xref: str = self.next_counter(self.xref_source)
        json_source: dict[str, dict[str, str]] = {}

        ged_source: list[str] = [
            f'{level!s} {xref} {Gedcom.SOUR}',
        ]
        for item in data:
            ged_source.extend(self.add_data(item))
        if author != Value.EMPTY:
            ged_source.extend([f'1 {Gedcom.AUTH} {author}'])
        if title != Value.EMPTY:
            ged_source.extend([f'1 {Gedcom.TITL} {title}'])
        if abbreviation != Value.EMPTY:
            ged_source.extend([f'1 {Gedcom.ABBR} {abbreviation}'])
        if publisher != Value.EMPTY:
            ged_source.extend([f'1 {Gedcom.PUBL} {publisher}'])
        if text != Value.EMPTY:
            ged_source.extend([f'1 {Gedcom.TEXT} {text}'])
        if mime != Value.EMPTY and mime in Enum.MEDIA_TYPE:
            ged_source.extend([f'2 {Gedcom.MIME} {mime}'])
        if language != Value.EMPTY:
            ged_source.extend([f'2 {Gedcom.LANG} {language}'])
        for source in sources:
            ged_source.extend(self.source_repository_citation(source))
        for identifier in identifiers:
            ged_source.extend(self.identifier_structure(identifier))
        for note in notes:
            ged_source.extend(self.note_structure(note))
        for media in multimedia:
            ged_source.extend(self.multimedia_link(media))
        ged_source.extend(self.creation_date())
        self.ged_source.extend(ged_source)

        self.chron[Gedcom.SOUR].update(json_source)
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
        xref: str = self.next_counter(self.xref_submitter)
        json_submitter: dict[str, dict[str, str]] = {}

        ged_submitter: list[str] = [
            f'{level!s} {xref} {Gedcom.SUBM}',
        ]
        ged_submitter.extend([f'1 {Gedcom.NAME} {name}'])
        ged_submitter.extend(self.address_structure(address))
        for phone in phones:
            ged_submitter.extend([f'1 {Gedcom.PHON} {phone}'])
        for email in emails:
            ged_submitter.extend([f'1 {Gedcom.EMAIL} {email}'])
        for fax in faxes:
            ged_submitter.extend([f'1 {Gedcom.FAX} {fax}'])
        for www in wwws:
            ged_submitter.extend([f'1 {Gedcom.WWW} {www}'])
        for media in multimedia:
            ged_submitter.extend(self.multimedia_link(media))
        for language in languages:
            ged_submitter.extend([f'1 {Gedcom.LANG} {language}'])
        for identifier in identifiers:
            ged_submitter.extend(self.identifier_structure(identifier))
        for note in notes:
            ged_submitter.extend(self.note_structure(note))
        ged_submitter.extend(self.creation_date())
        self.ged_submitter.extend(ged_submitter)

        self.chron[Gedcom.SUBM].update(json_submitter)
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
        if submitter != Value.EMPTY and submitter not in self.xref_submitter:
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
        ged_header: list[str] = [
            f'0 {Gedcom.HEAD}',
            f'1 {Gedcom.GEDC}',
            f'2 {Gedcom.VERS} {GEDSpecial.VERSION}',
        ]
        if len(schemas) > 0:
            ged_header.extend([f'1 {Gedcom.SCHMA}'])
            for schema in schemas:
                ged_header.extend(f'2 {Gedcom.TAG} {schema}')
        if source != Value.EMPTY:
            ged_header.extend([f'1 {Gedcom.SOUR} {source}'])
        if vers != Value.EMPTY:
            ged_header.extend([f'2 {Gedcom.VERS} {vers}'])
        if name != Value.EMPTY:
            ged_header.extend([f'2 {Gedcom.NAME} {name}'])
        if corp != Value.EMPTY:
            ged_header.extend([f'2 {Gedcom.CORP} {corp}'])
        ged_header.extend(self.address_structure(address, level=3))
        for phone in phones:
            ged_header.extend([f'3 {Gedcom.PHON} {phone}'])
        for email in emails:
            ged_header.extend([f'3 {Gedcom.EMAIL} {email}'])
        for fax in faxes:
            ged_header.extend([f'3 {Gedcom.FAX} {fax}'])
        for www in wwws:
            ged_header.extend([f'3 {Gedcom.WWW} {www}'])
        if data != Value.EMPTY:
            ged_header.extend(f'2 {Gedcom.DATA} {source[9]}')
        if date != Value.EMPTY:
            ged_header.extend(f'3 {Gedcom.DATE} {date}')
        if time != Value.EMPTY:
            ged_header.extend(f'4 {Gedcom.TIME} {time}')
        if dest != Value.EMPTY:
            ged_header.extend([f'1 {Gedcom.DEST} {dest}'])
        ged_header.extend(self.now(level=1))
        if submitter != Value.EMPTY:
            ged_header.extend([f'1 {Gedcom.SUBM} {submitter}'])
        if copr != Value.EMPTY:
            ged_header.extend([f'1 {Gedcom.COPR} {copr}'])
        if language != Value.EMPTY:
            ged_header.extend([f'1 {Gedcom.LANG} {language}'])
        if len(place) > 0:
            ged_header.extend(
                [
                    f'1 {Gedcom.PLAC} {place[0]}',
                    f'2 {Gedcom.FORM} {place[1]}',
                ]
            )
        ged_header.extend(self.note_structure(note))
        self.ged_header.extend(ged_header)
