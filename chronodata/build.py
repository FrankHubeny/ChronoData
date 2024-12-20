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
    Header,
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
        self.family_xreflist: list[str] = ['@0@']
        self.individual_xreflist: list[str] = ['@0@']
        self.multimedia_xreflist: list[str] = ['@0@']
        self.repository_xreflist: list[str] = ['@0@']
        self.shared_note_xreflist: list[str] = ['@0@']
        self.source_xreflist: list[str] = ['@0@']
        self.submitter_xreflist: list[str] = ['@0@']

    def _counter(
        self, xref_list: list[str], xref_name: str = '', initial: bool = False
    ) -> str:
        """
        Return a unique string either named with an incrementing integer or with a name.

        This procedure is called through seven other procedures.  These seven
        other procedures will distinctive type the string so it can be used
        to build a chronology with the `tuples` module.

        Exception:
            ValueError if a name is used twice for this record type.


        Parameters:

        - `xref_list`: a list of string values one for each of the seven record types.
        - `xref_name`: an option name to identify the record with.
        - `initial`: a boolean whether to use xref_name as
          an initial part of a numeric string. By default this is False.

        See Also:

        - `family_xref`: calls this method and types the output as FamilyXref.
        - `individual_xref`: calls this method and types the output as IndividualXref.
        - `multimedia_xref`: calls this method and types the output as MultimediaXref.
        - `repository_xref`: calls this method and types the output as RepositoryXref.
        - `shared_note_xref`: calls this method and types the output as SharedNoteXref.
        - `source_xref`: calls this method and types the output as SourceXref.
        - `submitter_xref`: calls this method and types the output as SubmitterXref.

        Reference:

        - [GEDCOM Standard](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#cb3-5)
        """
        modified_xref: str = ''
        if xref_name == '' or initial:
            modified_xref = ''.join(
                [
                    str(xref_name).strip().upper().replace(' ', '_'),
                    str(self.xref_counter),
                ]
            )
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
            raise ValueError(Msg.XREF_EXISTS.format(modified_xref, xref_name))
        xref_list.append(modified_xref)
        return modified_xref

    def family_xref(
        self, xref_name: str = '', initial: bool = False
    ) -> FamilyXref:
        """
        Create a FamilyXref identifier from a unique string according to the
        GEDCOM standard.

        Args:
            xref_name (str, optional): A name for the identifier. Defaults to ''.
            initial (bool, optional): Whether to use the name as an initial
                value with an integer following. Defaults to False.

        Returns:
            FamilyXref: A unique identifier string with type FamilyXref.

        Examples:
            The first example generates identifier for a family record.
            >>> from chronodata.build import Chronology
            >>> a = Chronology('testing')
            >>> id = a.family_xref()
            >>> print(id)
            @1@

            The second example shows the output when the identifier has a name.
            >>> id2 = a.family_xref('family')
            >>> print(id2)
            @FAMILY@

            The third example shows the output when the name is to be used as the initial
            part of the identifier.
            >>> id3 = a.family_xref('FAM', True)
            >>> print(id3)
            @FAM2@

            The final example shows what happens if we try to assign two different
            records with the same name.  We already have @FAMILY@ so we will try
            creating that name again.
            >>> a.family_xref('family')
            Traceback (most recent call last):
            ValueError: The identifier "family" already exists.

        See Also:
            - `individual_xref`: create a typed identifier for an individual record.
            - `multimedia_xref`: create a typed identifier for a multimedia record.
            - `repository_xref`: create a typed identifier for a repository record.
            - `shared_note_xref`: create a typed identifier for a shared note record.
            - `source_xref`: create a typed identifier for a source record.
            - `submitter_xref`: create a typed identifier for a submitter record.

        Reference:
            [GEDCOM Repository Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_RECORD)
        """
        family_xref = self._counter(
            self.family_xreflist,
            xref_name,
            initial,
        )
        return FamilyXref(family_xref)

    def individual_xref(
        self, xref_name: str = '', initial: bool = False
    ) -> IndividualXref:
        """
        Create an IndividualXref identifier from a unique string according to the
        GEDCOM standard.

        We will likely need many individuals in a single chronology.  When we are comparing
        chronologies we will need to synchronize those names.  Being able to
        name the identifiers helps to synchronize the various chronologies we
        will be comparing.  This method allows us to create named identifiers.

        Args:
            xref_name (str, optional): A name for the identifier. Defaults to ''.
            initial (bool, optional): Whether to use the name as an initial
                value with an integer following. Defaults to False.

        Returns:
            IndividualXref: A unique identifier string with type IndividualXref.

        Examples:
            The first example shows the output of the counter for an individual record
            without a name.
            >>> from chronodata.build import Chronology
            >>> a = Chronology('testing')
            >>> id = a.individual_xref()
            >>> print(id)
            @1@

            The second example shows the output when the identifier has a name.
            >>> id2 = a.individual_xref('joe')
            >>> print(id2)
            @JOE@

            The third example shows the output when the name is to be used as the initial
            part of the identifier.
            >>> id3 = a.individual_xref('N', True)
            >>> print(id3)
            @N2@

            The final example shows what happens if we try to assign two different
            records with the same name.  We already have @JOE@ so we will try
            creating that name again.
            >>> a.individual_xref('joe')
            Traceback (most recent call last):
            ValueError: The identifier "joe" already exists.

        See Also:
            - `family_xref`: create a typed identifier for a family record.
            - `multimedia_xref`: create a typed identifier for a multimedia record.
            - `repository_xref`: create a typed identifier for a repository record.
            - `shared_note_xref`: create a typed identifier for a shared note record.
            - `source_xref`: create a typed identifier for a source record.
            - `submitter_xref`: create a typed identifier for a submitter record.

        Reference:
            [GEDCOM Repository Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_RECORD)
        """
        individual_xref: str = self._counter(
            self.individual_xreflist,
            xref_name,
            initial,
        )
        return IndividualXref(individual_xref)

    def multimedia_xref(
        self, xref_name: str = '', initial: bool = False
    ) -> MultimediaXref:
        """
        Create a MultimediaXref identifier from a unique string according to the
        GEDCOM standard.

        Record identifiers cannot be assumed to be visible in genealogy software.
        In ChronoData they are used to align chronologies for comparisons.
        However, multimedia records are mainly used to document specific
        chronologies.  What is helpful when looking at a GEDCOM file is
        to know immediately what kind of identifier one has.  To show this
        one can put a string in front of the incremented counter.

        Args:
            xref_name (str, optional): A name for the identifier. Defaults to ''.
            initial (bool, optional): Whether to use the name as an initial
                value with an integer following. Defaults to False.

        Returns:
            MultimediaXref: A unique identifier string with type MultimediaXref.

        Examples:
            The first example generates identifier for a multimedia record.
            >>> from chronodata.build import Chronology
            >>> a = Chronology('testing')
            >>> id = a.multimedia_xref()
            >>> print(id)
            @1@

            The second example shows the output when the identifier has a name.
            >>> id2 = a.multimedia_xref('film')
            >>> print(id2)
            @FILM@

            The third example shows the output when the name is to be used as the initial
            part of the identifier.
            >>> id3 = a.multimedia_xref('film', True)
            >>> print(id3)
            @FILM2@

            The final example shows what happens if we try to assign two different
            records with the same name.  We already have @FILM@ so we will try
            creating that name again.
            >>> a.multimedia_xref('film')
            Traceback (most recent call last):
            ValueError: The identifier "film" already exists.

        See Also:
            - `family_xref`: create a typed identifier for a family record.
            - `individual_xref`: create a typed identifier for an individual record.
            - `repository_xref`: create a typed identifier for a repository record.
            - `shared_note_xref`: create a typed identifier for a shared note record.
            - `source_xref`: create a typed identifier for a source record.
            - `submitter_xref`: create a typed identifier for a submitter record.

        Reference:
            - [GEDCOM Repository Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#MULTIMEDIA_RECORD)
        """
        multimedia_xref = self._counter(
            self.multimedia_xreflist,
            xref_name,
            initial,
        )
        return MultimediaXref(multimedia_xref)

    def repository_xref(
        self, xref_name: str = '', initial: bool = False
    ) -> RepositoryXref:
        """
        Create a RepositoryXref identifier from a unique string according to the
        GEDCOM standard.

        Record identifiers cannot be assumed to be visible in genealogy software.
        In ChronoData they are used to align chronologies for comparisons.
        However, repository records are mainly used to document specific
        chronologies.  What is helpful when looking at a GEDCOM file is
        to know immediately what kind of identifier one has.  To show this
        one can put a string in front of the incremented counter.

        Args:
            xref_name (str, optional): A name for the identifier. Defaults to ''.
            initial (bool, optional): Whether to use the name as an initial
                value with an integer following. Defaults to False.

        Returns:
            RepositoryXref: A unique identifier string with type RepositoryXref.

        Examples:
            The first example generates identifier for a repository record.
            >>> from chronodata.build import Chronology
            >>> a = Chronology('testing')
            >>> id = a.repository_xref()
            >>> print(id)
            @1@

            The second example shows the output when the identifier has a name.
            >>> id2 = a.repository_xref('repo')
            >>> print(id2)
            @REPO@

            The third example shows the output when the name is to be used as the initial
            part of the identifier.
            >>> id3 = a.repository_xref('R', True)
            >>> print(id3)
            @R2@

            The final example shows what happens if we try to assign two different
            records with the same name.  We already have @REPO@ so we will try
            creating that name again.
            >>> a.repository_xref('repo')
            Traceback (most recent call last):
            ValueError: The identifier "repo" already exists.

        See Also:
            - `family_xref`: create a typed identifier for a family record.
            - `individual_xref`: create a typed identifier for an individual record.
            - `multimedia_xref`: create a typed identifier for a multimedia record.
            - `shared_note_xref`: create a typed identifier for a shared note record.
            - `source_xref`: create a typed identifier for a source record.
            - `submitter_xref`: create a typed identifier for a submitter record.

        Reference:
            [GEDCOM Repository Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#REPOSITORY_RECORD)
        """
        repository_xref = self._counter(
            self.repository_xreflist,
            xref_name,
            initial,
        )
        return RepositoryXref(repository_xref)

    def shared_note_xref(
        self, xref_name: str = '', initial: bool = False
    ) -> SharedNoteXref:
        """
        Create a SharedNoteXref identifier from a unique string according to the
        GEDCOM standard.

        Args:
            xref_name (str, optional): A name for the identifier. Defaults to ''.
            initial (bool, optional): Whether to use the name as an initial
                value with an integer following. Defaults to False.

        Returns:
            SharedNoteXref: A unique identifier string with type SharedNoteXref.

        Examples:
            The first example generates identifier for a shared note record.
            >>> from chronodata.build import Chronology
            >>> a = Chronology('testing')
            >>> id = a.shared_note_xref()
            >>> print(id)
            @1@

            The second example shows the output when the identifier has a name.
            >>> id2 = a.shared_note_xref('sn')
            >>> print(id2)
            @SN@

            The third example shows the output when the name is to be used as the initial
            part of the identifier.
            >>> id3 = a.shared_note_xref('SN', True)
            >>> print(id3)
            @SN2@

            The final example shows what happens if we try to assign two different
            records with the same name.  We already have @SN@ so we will try
            creating that name again.
            >>> a.shared_note_xref('sn')
            Traceback (most recent call last):
            ValueError: The identifier "sn" already exists.

        See Also:
            - `family_xref`: create a typed identifier for a family record.
            - `individual_xref`: create a typed identifier for an individual record.
            - `multimedia_xref`: create a typed identifier for a multimedia record.
            - `repository_xref`: create a typed identifier for a repository record.
            - `source_xref`: create a typed identifier for a source record.
            - `submitter_xref`: create a typed identifier for a submitter record.

        Reference:
            [GEDCOM Repository Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SHARED_NOTE_RECORD)
        """
        shared_note_xref = self._counter(
            self.shared_note_xreflist,
            xref_name,
            initial,
        )
        return SharedNoteXref(shared_note_xref)

    def source_xref(
        self, xref_name: str = '', initial: bool = False
    ) -> SourceXref:
        """
        Create a SourceXref identifier from a unique string according to the
        GEDCOM standard.

        Args:
            xref_name (str, optional): A name for the identifier. Defaults to ''.
            initial (bool, optional): Whether to use the name as an initial
                value with an integer following. Defaults to False.

        Returns:
            SourceXref: A unique identifier string with type SourceXref.

        Examples:
            The first example generates identifier for a shared note record.
            >>> from chronodata.build import Chronology
            >>> a = Chronology('testing')
            >>> id = a.source_xref()
            >>> print(id)
            @1@

            The second example shows the output when the identifier has a name.
            >>> id2 = a.source_xref('source')
            >>> print(id2)
            @SOURCE@

            The third example shows the output when the name is to be used as the initial
            part of the identifier.
            >>> id3 = a.source_xref('s', True)
            >>> print(id3)
            @S2@

            The final example shows what happens if we try to assign two different
            records with the same name.  We already have @SOURCE@ so we will try
            creating that name again.
            >>> a.source_xref('source')
            Traceback (most recent call last):
            ValueError: The identifier "source" already exists.

        See Also:
            - `family_xref`: create a typed identifier for a family record.
            - `individual_xref`: create a typed identifier for an individual record.
            - `multimedia_xref`: create a typed identifier for a multimedia record.
            - `repository_xref`: create a typed identifier for a repository record.
            - `shared_note_xref`: create a typed identifier for a shared note record.
            - `submitter_xref`: create a typed identifier for a submitter record.

        Reference:
            [GEDCOM Repository Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_RECORD)
        """
        source_xref = self._counter(
            self.source_xreflist,
            xref_name,
            initial,
        )
        return SourceXref(source_xref)

    def submitter_xref(
        self, xref_name: str = '', initial: bool = False
    ) -> SubmitterXref:
        """
        Create a SubmitterXref identifier from a unique string according to the
        GEDCOM standard.

        Args:
            xref_name (str, optional): A name for the identifier. Defaults to ''.
            initial (bool, optional): Whether to use the name as an initial
                value with an integer following. Defaults to False.

        Returns:
            SubmitterXref: A unique identifier string with type SubmitterXref.

        Examples:
            The first example generates identifier for a shared note record.
            >>> from chronodata.build import Chronology
            >>> a = Chronology('testing')
            >>> id = a.submitter_xref()
            >>> print(id)
            @1@

            The second example shows the output when the identifier has a name.
            >>> id2 = a.submitter_xref('sub')
            >>> print(id2)
            @SUB@

            The third example shows the output when the name is to be used as the initial
            part of the identifier.
            >>> id3 = a.submitter_xref('SUB', True)
            >>> print(id3)
            @SUB2@

            The final example shows what happens if we try to assign two different
            records with the same name.  We already have @SUB@ so we will try
            creating that name again.
            >>> a.submitter_xref('sub')
            Traceback (most recent call last):
            ValueError: The identifier "sub" already exists.


        See Also:
            - `family_xref`: create a typed identifier for a family record.
            - `individual_xref`: create a typed identifier for an individual record.
            - `multimedia_xref`: create a typed identifier for a multimedia record.
            - `repository_xref`: create a typed identifier for a repository record.
            - `shared_note_xref`: create a typed identifier for a shared note record.
            - `source_xref`: create a typed identifier for a source record.

        Reference:
            [GEDCOM Repository Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SUBMITTER_RECORD)
        """
        submitter_xref = self._counter(
            self.submitter_xreflist,
            xref_name,
            initial,
        )
        return SubmitterXref(submitter_xref)

    def families(self, records: tuple[Family]) -> None:
        """Collect and store all family records for the chronology.

        After importing `chronodata.build` and `chronodata.tuples`
        one can instantiate a `Chronology` and create a family
        identifier to be used in forming a GEDCOM family record.
        The `tuples.Family` NamedTuple will hold all of this
        particular family's information. When one has constructed
        all of the families that one wants to define for this
        chronology, they are bundled together with this method.
        This stores them as GEDCOM strings waiting to be saved
        to a file.

        Args:
            records (tuple[Family]): a tuple of all Family tuples.

        Examples:
            This is a minimal example illustrating the process.
            >>> from chronodata.build import Chronology
            >>> from chronodata.tuples import Family
            >>> a = Chronology('test')
            >>> family_id = a.family_xref()
            >>> family = Family(xref=family_id)
            >>> a.families((family,))
            >>> print(a.ged_family)
            0 @1@ FAM
            <BLANKLINE>

            There may be more than one family.  This example creates a second
            family and them runs the method.  This second run overwrites
            what was entered earlier.
            >>> family_id2 = a.family_xref()
            >>> family2 = Family(xref=family_id2)
            >>> a.families(
            ...     (
            ...         family,
            ...         family2,
            ...     )
            ... )
            >>> print(a.ged_family)
            0 @1@ FAM
            0 @2@ FAM
            <BLANKLINE>

        See Also:
            - `individuals`: collect and store individual records.
            - `multimedia`: collect and store multimedia records.
            - `repositories`: collect and store repository records.
            - `shared_notes`: collect and store shared notes records.
            - `sources`: collect and store source records.
            - `submitters`: collect and store submitter records.
        """
        self.ged_family = ''
        for record in records:
            self.ged_family = ''.join([self.ged_family, record.ged()])

    def individuals(self, records: tuple[Individual]) -> None:
        """Collect and store all individual records for the chronology.

        Args:
            records (tuple[Individual]): a tuple of all Individual tuples.

        See Also:
            - `families`: collect and store family records.
            - `multimedia`: collect and store multimedia records.
            - `repositories`: collect and store repository records.
            - `shared_notes`: collect and store shared notes records.
            - `sources`: collect and store source records.
            - `submitters`: collect and store submitter records.
        """
        self.ged_individual = ''
        for record in records:
            self.ged_individual = ''.join([self.ged_individual, record.ged()])

    def multimedia(self, records: tuple[Multimedia]) -> None:
        """Collect and store all multimedia records for the chronology.

        Args:
            records (tuple[Multimedia]): a tuple of all Multimedia tuples.

        See Also:
            - `families`: collect and store family records.
            - `individuals`: collect and store individual records.
            - `repositories`: collect and store repository records.
            - `shared_notes`: collect and store shared notes records.
            - `sources`: collect and store source records.
            - `submitters`: collect and store submitter records.
        """
        self.ged_multimedia = ''
        for record in records:
            self.ged_multimedia = ''.join([self.ged_multimedia, record.ged()])

    def repositories(self, records: tuple[Repository]) -> None:
        """Collect and store all repository records for the chronology.

        Args:
            records (tuple[Repository]): a tuple of all Repository tuples.

        See Also:
            - `families`: collect and store family records.
            - `individuals`: collect and store individual records.
            - `multimedia`: collect and store multimedia records.
            - `shared_notes`: collect and store shared notes records.
            - `sources`: collect and store source records.
            - `submitters`: collect and store submitter records.
        """
        self.ged_repository = []
        for record in records:
            self.ged_repository = ''.join([self.ged_repository, record.ged()])

    def shared_notes(self, records: tuple[SharedNote]) -> None:
        """Collect and store all shared note records for the chronology.

        Args:
            records (tuple[SharedNote]): a tuple of all SharedNote tuples.

        See Also:
            - `families`: collect and store family records.
            - `individuals`: collect and store individual records.
            - `multimedia`: collect and store multimedia records.
            - `repositories`: collect and store repository records.
            - `sources`: collect and store source records.
            - `submitters`: collect and store submitter records.
        """
        self.ged_shared_note = ''
        for record in records:
            self.ged_shared_note = ''.join([self.ged_shared_note, record.ged()])

    def sources(self, records: tuple[Source]) -> None:
        """Collect and store all source records for the chronology.

        Args:
            records (tuple[Source]): a tuple of all Source tuples.

        See Also:
            - `families`: collect and store family records.
            - `individuals`: collect and store individual records.
            - `multimedia`: collect and store multimedia records.
            - `repositories`: collect and store repository records.
            - `shared_notes`: collect and store shared notes records.
            - `submitters`: collect and store submitter records.
        """
        self.ged_source = ''
        for record in records:
            self.ged_source = ''.join([self.ged_source, record.ged()])

    def submitters(self, records: tuple[Submitter]) -> None:
        """Collect and store all submitter records for the chronology.

        Args:
            records (tuple[Submitter]): a tuple of all Submitter tuples.

        See Also:
            - `families`: collect and store family records.
            - `individuals`: collect and store individual records.
            - `multimedia`: collect and store multimedia records.
            - `repositories`: collect and store repository records.
            - `shared_notes`: collect and store shared notes records.
            - `sources`: collect and store source records.
        """
        self.ged_submitter = ''
        for record in records:
            self.ged_submitter = ''.join([self.ged_submitter, record.ged()])

    def header(self, ged_header: Header) -> None:
        """Collect and store the header record.

        Args:
            ged_header (str): is the text of the header record.
        """
        self.ged_header = ged_header.ged()
