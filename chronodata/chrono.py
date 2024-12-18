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

from chronodata.constants import GEDSpecial
from chronodata.core import Base
from chronodata.messages import Msg
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
    Family,
    Individual,
    Multimedia,
    Repository,
    SharedNote,
    Source,
    Submitter,
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

    def family_records(self, records: tuple[Family]) -> None:
        for record in records:
            self.ged_family = ''.join([self.ged_family, record.ged()])
        logging.info('Family records added.')

    def individual_records(self, records: tuple[Individual]) -> None:
        for record in records:
            self.ged_individual = ''.join([self.ged_individual, record.ged()])
        logging.info('Individual records added.')

    def multimedia_records(self, records: tuple[Multimedia]) -> None:
        for record in records:
            self.ged_multimedia = ''.join([self.ged_multimedia, record.ged()])
        logging.info('Multimedia records added.')

    def repository_records(self, records: tuple[Repository]) -> None:
        for record in records:
            self.ged_repository = ''.join([self.ged_repository, record.ged()])
        logging.info('Repository records added.')

    def shared_note_records(self, records: tuple[SharedNote]) -> None:
        for record in records:
            self.ged_shared_note = ''.join([self.ged_shared_note, record.ged()])
        logging.info('Shared note records added.')

    def source_records(self, records: tuple[Source]) -> None:
        for record in records:
            self.ged_source = ''.join([self.ged_source, record.ged()])
        logging.info('Source records added.')

    def submitter_records(self, records: tuple[Submitter]) -> None:
        for record in records:
            self.ged_submitter = ''.join([self.ged_submitter, record.ged()])
        logging.info('submitter records added.')

    def header(self, ged_header: str) -> None:
        self.ged_header = ged_header
