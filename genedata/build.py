# Licensed under a 3-clause BSD style license - see LICENSE.md
"""Methods to build a genealogy based on the GEDCOM standard.

This module implements reading and writing genealogy files according to the
[FamilySearch GEDCOM Version 7](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html)
standard.  It also allows reading files in the GEDCOM 5.5.1 standard,
but will write the output in compliance with GEDCOM 7.0.

The underlying datastructure for the genealogy is a Python dictionary.
This dictionary can be read and written in JSON.

Rather than introduce extensions to the GEDCOM standards new data items
are placed under `FACT` and `EVEN` tags as
[Tamura Jones](https://www.tamurajones.net/GEDCOMExtensions.xhtml) recommended.
Some extensions are the use of ISO dates as implemented by NumPy's `datetime64`
data type."""

import json
import logging
from pathlib import Path
from typing import Any

from genedata.classes7 import (
    Head,
    RecordFam,
    RecordIndi,
    RecordObje,
    RecordRepo,
    RecordSnote,
    RecordSour,
    RecordSubm,
    Trlr,
)
from genedata.constants import (
    Config,
    Default,
    Number,
    String,
)
from genedata.messages import Issue, Msg
from genedata.structure import (
    ExtensionXref,
    FamilyXref,
    IndividualXref,
    MultimediaXref,
    RepositoryXref,
    SharedNoteXref,
    SourceXref,
    SubmitterXref,
    Void,
)
from genedata.util import Tagger, Util


class Genealogy:
    """Methods to add, update and remove a specific loaded genealogy."""

    def __init__(
        self,
        name: str = '',
        filename: str = '',
        calendar: str = String.GREGORIAN,
        log: bool = True,
    ) -> None:
        self.chron_name: str = name
        self.calendar: str = calendar
        self.ged_data: list[str] = []
        self.ged_splitdata: list[Any] = []
        self.ged_issues: list[Any] = []
        self.ged_in_version: str = ''
        self.ged_header: str = ''
        self.ged_trailer: str = Default.TRAILER
        self.ged_extension: str = ''
        self.ged_family: str = ''
        self.ged_individual: str = ''
        self.ged_multimedia: str = ''
        self.ged_repository: str = ''
        self.ged_shared_note: str = ''
        self.ged_source: str = ''
        self.ged_submitter: str = ''
        self.records: list[
            RecordFam
            | RecordIndi
            | RecordObje
            | RecordRepo
            | RecordSnote
            | RecordSour
            | RecordSubm
        ] = []
        self.record_header: Head | None = None
        self.csv_data: str = ''
        self.filename: str = filename
        self.filename_type: str = self._get_filename_type(self.filename)
        self.xref_counter: int = 1
        self.extension_xreflist: list[str] = [Void.NAME]
        self.family_xreflist: list[str] = [Void.NAME]
        self.individual_xreflist: list[str] = [Void.NAME]
        self.multimedia_xreflist: list[str] = [Void.NAME]
        self.repository_xreflist: list[str] = [Void.NAME]
        self.shared_note_xreflist: list[str] = [Void.NAME]
        self.source_xreflist: list[str] = [Void.NAME]
        self.submitter_xreflist: list[str] = [Void.NAME]
        match self.filename_type:
            case '':
                self.chron: dict[str, str] = {
                    # Tag.NAME: name,
                    # Key.CAL: calendar,
                }
                if log:
                    logging.info(Msg.STARTED.format(self.chron_name))
            case String.JSON:
                self.read_json()
                if log:
                    logging.info(Msg.LOADED.format(self.chron_name, filename))
            case String.GED:
                self.read_ged()
                if log:
                    logging.info(Msg.LOADED.format(self.chron_name, filename))
            case String.CSV:
                self.read_csv()
                if log:
                    logging.info(Msg.LOADED.format(self.chron_name, filename))
            case _:
                logging.warning(Msg.UNRECOGNIZED.format(self.filename))

    def __str__(self) -> str:
        return json.dumps(self.chron)

    def store(self, record: Head | RecordFam | RecordIndi | RecordObje | RecordRepo | RecordSnote | RecordSour| RecordSubm) -> None:
        if not isinstance(record, Head | RecordFam | RecordIndi | RecordObje | RecordRepo | RecordSnote | RecordSour| RecordSubm):
            raise ValueError(Msg.ONLY_RECORDS.format(str(record)))
        if isinstance(record, Head):
            self.record_header = record
        else:
            self.records.append(record)

    def show_ged(self) -> str:
        if self.record_header is None:
            raise ValueError(Msg.MISSING_HEADER)
        lines = self.record_header.ged()
        for record in self.records:
            lines = ''.join([lines, record.ged()])
        return ''.join([lines, Trlr().ged()])
    
    def save_ged(self, file_name: str = Default.EMPTY) -> None:
        Util.write_ged(self.show_ged(), file_name)
    

    def code(self) -> str:
        lines: str = f"""from genedata.build import Genealogy
import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}

{Default.CODE_GENEALOGY} = Genealogy('{self.chron_name}')
"""
        for ext in self.extension_xreflist:
            item: str = ext.replace(Default.ATSIGN, Default.EMPTY)
            if ext != Default.VOID_POINTER:
                lines = f"{lines}{Default.EOL}ext_{item}_xref = {Default.CODE_GENEALOGY}.extension_xref('{item}')"
        for fam in self.family_xreflist:
            item = fam.replace(Default.ATSIGN, Default.EMPTY)
            if fam != Default.VOID_POINTER:
                lines = f"{lines}{Default.EOL}fam_{item}_xref = {Default.CODE_GENEALOGY}.family_xref('{item}')"
        for indi in self.individual_xreflist:
            item = indi.replace(Default.ATSIGN, Default.EMPTY)
            if indi != Default.VOID_POINTER:
                lines = f"{lines}{Default.EOL}indi_{item}_xref = {Default.CODE_GENEALOGY}.individual_xref('{item}')"
        for obje in self.multimedia_xreflist:
            item = obje.replace(Default.ATSIGN, Default.EMPTY)
            if obje != Default.VOID_POINTER:
                lines = f"{lines}{Default.EOL}obje_{item}_xref = {Default.CODE_GENEALOGY}.multimedia_xref('{item}')"
        for repo in self.repository_xreflist:
            item = repo.replace(Default.ATSIGN, Default.EMPTY)
            if repo != Default.VOID_POINTER:
                lines = f"{lines}{Default.EOL}repo_{item}_xref = {Default.CODE_GENEALOGY}.repository_xref('{item}')"
        for snote in self.shared_note_xreflist:
            item = snote.replace(Default.ATSIGN, Default.EMPTY)
            if snote != Default.VOID_POINTER:
                lines = f"{lines}{Default.EOL}snote_{item}_xref = {Default.CODE_GENEALOGY}.shared_note_xref('{item}')"
        for sour in self.source_xreflist:
            item = sour.replace(Default.ATSIGN, Default.EMPTY)
            if sour != Default.VOID_POINTER:
                lines = f"{lines}{Default.EOL}sour_{item}_xref = {Default.CODE_GENEALOGY}.source_xref('{item}')"
        for subm in self.submitter_xreflist:
            item = subm.replace(Default.ATSIGN, Default.EMPTY)
            if subm != Default.VOID_POINTER:
                lines = f"{lines}{Default.EOL}subm_{item}_xref = {Default.CODE_GENEALOGY}.submitter_xref('{item}')"
        return lines

    def _get_filename_type(self, filename: str) -> str:
        filename_type: str = ''
        if filename[-Number.JSONLEN :] == String.JSON:
            filename_type = String.JSON
        if filename[-Number.GEDLEN :] == String.GED:
            filename_type = String.GED
        return filename_type

    def read_csv(self) -> None:
        try:
            with Path.open(
                Path(self.filename), encoding='utf-8', mode=String.READ
            ) as infile:
                data: Any = infile.readlines()
                self.csv_data = ''.join(
                    [self.csv_data, Tagger.clean_input(data)]
                )
                infile.close()
        except UnicodeDecodeError:
            logging.error(Msg.NOT_UNICODE.format(self.filename))
            raise
        # self.cal_name = self.chron[Key.CAL][Key.NAME]
        # self.chron_name = self.chron[Key.NAME]

    def read_json(self) -> None:
        try:
            with Path.open(
                Path(self.filename), encoding='utf-8', mode=String.READ
            ) as infile:
                self.chron = json.load(infile)
                infile.close()
        except UnicodeDecodeError:
            logging.error(Msg.NOT_UNICODE.format(self.filename))
            raise
        # self.cal_name = self.chron[Key.CAL][Key.NAME]
        # self.chron_name = self.chron[Key.NAME]

    def read_ged(self) -> None:
        """Read and validate the GEDCOM file."""
        try:
            with Path.open(
                Path(self.filename), encoding='utf-8', mode=String.READ
            ) as infile:
                data: Any = infile.readlines()
                self.ged_data.append(Tagger.clean_input(data))
                infile.close()
        except UnicodeDecodeError:
            logging.error(Msg.NOT_UNICODE.format(self.filename))
            raise
        # Split each line into components and remove terminator.
        for i in data:
            self.ged_splitdata.append(i.replace('\n', '').split(' ', 2))
        # Check the level for bad increments and starting point.
        level: int = 0
        for index, value in enumerate(self.ged_splitdata, start=1):
            if index == 1 and value[0] != '0':
                self.ged_issues.append([index, Issue.NO_ZERO])
            elif int(value[0]) > level + 1:
                self.ged_issues.append([index, Issue.BAD_INC])
            elif int(value[0]) < 0:
                self.ged_issues.append([index, Issue.LESS_ZERO])
            else:
                level = int(value[0])
        # Report the validation results which exists the function.
        # if len(issues) > 0:
        #     #if self.log:
        #     #logging.info(Msg.LOAD_FAILED.format(filename))
        #     return pd.DataFrame(
        #         data=issues, columns=[Column.LINE, Column.ISSUE]
        #     )
        # Find version.
        for i in self.ged_splitdata:
            if i[1] == 'VERS':
                self.ged_in_version = i[2]
                break
        # add in the base dictionaries.
        count: int = 0
        tags: list[str] = []
        for line in self.ged_splitdata:
            if line[0] == '0' and len(line) == 3:
                count = count + 1
                if line[2] not in self.chron:
                    self.chron.update({line[2]: {}})
                # self.chron[line[2]].update({line[1]: {}})
                tags = []
                tags.append(line[2])
                tags.append(line[1])
            elif line[0] == '1' and len(line) == 3 and count > 0:
                # t0 = tags[0]
                # t1 = tags[1]
                # self.chron[tags[0]][tags[1]].update({line[1]: line[2]})
                tags.append(line[1])
            # elif line[0] == '2' and len(line) == 3 and count > 0:
            #     self.chron[tags[0]][tags[1]][tags[2]].update({line[1]: line[2]})
            #     tags.append(line[1])
        # logging.info(Msg.LOADED.format(self.chron_name, self.filename))

    def save(self, filename: str = '', overwrite: bool = False) -> None:
        """Save the current genealogy.

        Parameters
        ----------
        filename:
            The name of the file. If empty it will use the name
        """

        if filename == '':
            filename = self.filename
        else:
            self.filename = filename
            self.filename_type = self._get_filename_type(filename)
        if Path.exists(Path(filename)) and not overwrite:
            logging.info(Msg.FILE_EXISTS.format(filename))
        else:
            match self.filename_type:
                # https://stackoverflow.com/questions/10373247/how-do-i-write-a-python-dictionary-to-a-csv-file
                # case String.CSV:
                #     with Path.open(
                #         Path(self.filename), encoding='utf-8', mode=String.WRITE
                #     ) as file:
                #         w = csv.DictWriter(file, self.chron.keys())
                #         w.writerows(self.chron)
                #     logging.info(
                #         Msg.SAVED.format(self.chron_name, self.filename)
                #     )
                case String.JSON:
                    with Path.open(
                        Path(self.filename), encoding='utf-8', mode=String.WRITE
                    ) as file:
                        json.dump(self.chron, file)
                        file.close()
                    logging.info(Msg.SAVED.format(self.filename))
                case String.GED:
                    output: str = ''.join(
                        [
                            self.ged_header,
                            self.ged_family,
                            self.ged_individual,
                            self.ged_multimedia,
                            self.ged_shared_note,
                            self.ged_source,
                            self.ged_submitter,
                            self.ged_trailer,
                        ]
                    )
                    with Path.open(
                        Path(filename), encoding='utf-8', mode=String.WRITE
                    ) as file:
                        file.write(output)
                        file.close()
                    logging.info(
                        Msg.SAVED.format(self.chron_name, self.filename)
                    )
                case _:
                    logging.info(Msg.SAVE_FIRST)

    def _get_counter(self) -> str:
        counter = str(self.xref_counter)
        self.xref_counter += 1
        return str(counter)

    def _set_xref(
        self, xref_list: list[str], xref: str, xref_name: str = ''
    ) -> None:
        if xref in xref_list:
            raise ValueError(Msg.XREF_EXISTS.format(xref, xref_name))
        xref_list.append(xref)

    def _format_name(self, name: str = '', counter: str = '') -> str:
        return ''.join(
            [
                Default.ATSIGN,
                name.strip().upper().replace(' ', '_'),
                counter,
                Default.ATSIGN,
            ]
        )

    def _counter(
        self, xref_list: list[str], xref_name: str = '', initial: bool = False
    ) -> str:
        """
        Return a unique string either named with an incrementing integer or with a name.

        This procedure is called through seven other procedures.  These seven
        other procedures will distinctive type the string so it can be used
        to build a genealogy with the `tuples` module.

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
        xref: str = ''
        if xref_name == '':
            xref = self._format_name(counter=self._get_counter())
            self._set_xref(xref_list, xref)
            return xref
        if initial:
            xref = self._format_name(xref_name, self._get_counter())
        else:
            xref = self._format_name(xref_name)
        self._set_xref(xref_list, xref, xref_name)
        return xref

    def extension_xref(
        self, xref_name: str = '', initial: bool = False
    ) -> ExtensionXref:
        """
        Create a FamilyXref identifier from a unique string according to the
        GEDCOM standard.

        Args:
            xref_name (str, optional): A name for the identifier. Defaults to ''.
            initial (bool, optional): Whether to use the name as an initial
                value with an integer following. Defaults to False.

        Returns:
            ExtensionXref: A unique identifier string with type ExtensionXref.

        Examples:

        See Also:
            - `family_xref`: create a typed identifier for an family record.
            - `individual_xref`: create a typed identifier for an individual record.
            - `multimedia_xref`: create a typed identifier for a multimedia record.
            - `repository_xref`: create a typed identifier for a repository record.
            - `shared_note_xref`: create a typed identifier for a shared note record.
            - `source_xref`: create a typed identifier for a source record.
            - `submitter_xref`: create a typed identifier for a submitter record.

        Reference:
            [GEDCOM Repository Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_RECORD)
        """
        extension_xref = self._counter(
            self.extension_xreflist,
            xref_name,
            initial,
        )
        return ExtensionXref(extension_xref)

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
            >>> from genedata.build import Genealogy
            >>> a = Genealogy('testing')
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
            ValueError: The identifier "@FAMILY@" built from "family" already exists.

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

        We will likely need many individuals in a single genealogy.  When we are comparing
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
            >>> from genedata.build import Genealogy
            >>> a = Genealogy('testing')
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
            ValueError: The identifier "@JOE@" built from "joe" already exists.

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
            >>> from genedata.build import Genealogy
            >>> a = Genealogy('testing')
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
            ValueError: The identifier "@FILM@" built from "film" already exists.

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
            >>> from genedata.build import Genealogy
            >>> a = Genealogy('testing')
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
            ValueError: The identifier "@REPO@" built from "repo" already exists.

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
        self,
        xref_name: str = '',
        text: str = Default.EMPTY,
        initial: bool = False,
    ) -> SharedNoteXref:
        """
        Create a SharedNoteXref identifier from a unique string according to the
        GEDCOM standard.

        Args:
            xref_name: A name for the identifier. Defaults to ''.
            text: The text that is being shared.
            initial (bool, optional): Whether to use the name as an initial
                value with an integer following. Defaults to False.

        Returns:
            SharedNoteXref: A unique identifier string with type SharedNoteXref.

        Examples:
            The first example generates identifier for a shared note record.
            >>> from genedata.build import Genealogy
            >>> a = Genealogy('testing')
            >>> id = a.shared_note_xref('1', 'This is a shared note.')
            >>> print(id)
            @1@

            The second example shows the output when the identifier has a name.
            >>> id2 = a.shared_note_xref('sn', 'This is a shared note.')
            >>> print(id2)
            @SN@

            The third example shows the output when the name is to be used as the initial
            part of the identifier.
            >>> id3 = a.shared_note_xref('SN', '  ')
            >>> print(id3)
            @SN2@

            The final example shows what happens if we try to assign two different
            records with the same name.  We already have @SN@ so we will try
            creating that name again.
            >>> a.shared_note_xref('sn', '  ')
            Traceback (most recent call last):
            ValueError: The identifier "@SN@" built from "sn" already exists.

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
        return SharedNoteXref(shared_note_xref, text=text)

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
            >>> from genedata.build import Genealogy
            >>> a = Genealogy('testing')
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
            ValueError: The identifier "@SOURCE@" built from "source" already exists.

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
            >>> from genedata.build import Genealogy
            >>> a = Genealogy('testing')
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
            ValueError: The identifier "@SUB@" built from "sub" already exists.


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

    def _gather(self, records: list[Any], xref_list: list[str]) -> str:
        destination = ''
        unique_list: list[str] = []
        for record in records:
            # if record.xref.fullname not in unique_list:
            if record.value.fullname not in unique_list:
                unique_list.append(record.value.fullname)
                destination = ''.join([destination, record.ged()])
            else:
                raise ValueError(
                    Msg.DUPLICATE_RECORD.format(record.value.fullname)
                )
        missing = [
            xref
            for xref in xref_list
            if xref not in unique_list and xref != Void.NAME
        ]
        if len(missing) > 0:
            raise ValueError(Msg.MISSING.format(missing))
        return destination

    def families(self, records: list[RecordFam]) -> None:
        """Collect and store all family records for the genealogy.

        Args:
            records: a list of all Family records.

        Examples:
            This is a minimal example illustrating the process.
            >>> from genedata.build import Genealogy
            >>> from genedata.classes7 import RecordFam
            >>> a = Genealogy('test')
            >>> family_id = a.family_xref()
            >>> family = RecordFam(family_id)
            >>> a.families(
            ...     [
            ...         family,
            ...     ]
            ... )
            >>> print(a.ged_family)
            0 @1@ FAM
            <BLANKLINE>

            There may be more than one family.  This example creates a second
            family and them runs the method.  This second run overwrites
            what was entered earlier.
            >>> family_id2 = a.family_xref()
            >>> family2 = RecordFam(family_id2)
            >>> a.families(
            ...     [
            ...         family,
            ...         family2,
            ...     ]
            ... )
            >>> print(a.ged_family)
            0 @1@ FAM
            0 @2@ FAM
            <BLANKLINE>

        See Also:
            - `families`: gather family records.
            - `individuals`: gather individual records.
            - `multimedia`: gather multimedia records.
            - `repositories`: gather repository records.
            - `shared_notes`: gather shared notes records.
            - `sources`: gather source records.
        """
        self.ged_family = self._gather(records, self.family_xreflist)

    def individuals(self, records: list[RecordIndi]) -> None:
        """Collect and store all individual records for the genealogy.

        Args:
            records: a list of all Individual records.

        Examples:
            This is a minimal example illustrating the process.
            >>> from genedata.build import Genealogy
            >>> from genedata.classes7 import RecordIndi
            >>> a = Genealogy('test')
            >>> individual_id = a.individual_xref()
            >>> individual = RecordIndi(individual_id)
            >>> a.individuals(
            ...     [
            ...         individual,
            ...     ]
            ... )
            >>> print(a.ged_individual)
            0 @1@ INDI
            <BLANKLINE>

            There may be more than one family.  This example creates a second
            family and them runs the method.  This second run overwrites
            what was entered earlier.
            >>> individual_id2 = a.individual_xref()
            >>> individual2 = RecordIndi(individual_id2)
            >>> a.individuals(
            ...     [
            ...         individual,
            ...         individual2,
            ...     ]
            ... )
            >>> print(a.ged_individual)
            0 @1@ INDI
            0 @2@ INDI
            <BLANKLINE>

        See Also:
            - `families`: gather family records.
            - `individuals`: gather individual records.
            - `multimedia`: gather multimedia records.
            - `repositories`: gather repository records.
            - `shared_notes`: gather shared notes records.
            - `sources`: gather source records.
        """
        self.ged_individual = self._gather(records, self.individual_xreflist)

    def multimedia(self, records: list[RecordObje]) -> None:
        """Collect and store all multimedia records for the genealogy.

        Args:
            records: a list of all Multimedia records.

        Examples:
            This is a minimal example illustrating the process.
            >>> from genedata.build import Genealogy
            >>> from genedata.classes7 import File, Form, RecordObje
            >>> a = Genealogy('test')
            >>> mm_id = a.multimedia_xref()
            >>> mm = RecordObje(
            ...     mm_id, File('/path/to/file', Form('application/pdf'))
            ... )
            >>> a.multimedia(
            ...     [
            ...         mm,
            ...     ]
            ... )
            >>> print(a.ged_multimedia)
            0 @1@ OBJE
            1 FILE /path/to/file
            2 FORM application/pdf
            <BLANKLINE>

            There may be more than one multimedia record.  This example creates a second
            one and then runs the method.  This second run overwrites
            what was entered earlier.
            >>> mm_id2 = a.multimedia_xref()
            >>> mm2 = RecordObje(
            ...     mm_id2, File('/path/to/otherfile', Form('application/pdf'))
            ... )
            >>> a.multimedia(
            ...     [
            ...         mm,
            ...         mm2,
            ...     ]
            ... )
            >>> print(a.ged_multimedia)
            0 @1@ OBJE
            1 FILE /path/to/file
            2 FORM application/pdf
            0 @2@ OBJE
            1 FILE /path/to/otherfile
            2 FORM application/pdf
            <BLANKLINE>

        See Also:
            - `families`: gather family records.
            - `individuals`: gather individual records.
            - `multimedia`: gather multimedia records.
            - `repositories`: gather repository records.
            - `shared_notes`: gather shared notes records.
            - `sources`: gather source records.
        """
        self.ged_multimedia = self._gather(records, self.multimedia_xreflist)

    def repositories(self, records: list[RecordRepo]) -> None:
        """Collect and store all repository records for the genealogy.

        Args:
            records: a list of all Repository records.

        Examples:
            This is a minimal example illustrating the process.
            >>> from genedata.build import Genealogy
            >>> from genedata.classes7 import RecordRepo, Name
            >>> a = Genealogy('test')
            >>> repo_id = a.repository_xref()
            >>> repo = RecordRepo(repo_id, Name('Repo Name'))
            >>> a.repositories(
            ...     [
            ...         repo,
            ...     ]
            ... )
            >>> print(a.ged_repository)
            0 @1@ REPO
            1 NAME Repo Name
            <BLANKLINE>

            There may be more than one repository record.  This example creates a second
            one and then runs the method.  This second run overwrites
            what was entered earlier.
            >>> repo_id2 = a.repository_xref()
            >>> repo2 = RecordRepo(repo_id2, Name('Second Repo Name'))
            >>> a.repositories(
            ...     [
            ...         repo,
            ...         repo2,
            ...     ]
            ... )
            >>> print(a.ged_repository)
            0 @1@ REPO
            1 NAME Repo Name
            0 @2@ REPO
            1 NAME Second Repo Name
            <BLANKLINE>

        See Also:
            - `families`: gather family records.
            - `individuals`: gather individual records.
            - `multimedia`: gather multimedia records.
            - `repositories`: gather repository records.
            - `shared_notes`: gather shared notes records.
            - `sources`: gather source records.
        """
        self.ged_repository = self._gather(records, self.repository_xreflist)

    def shared_notes(self, records: list[RecordSnote]) -> None:
        """Collect and store all shared note records for the genealogy.

        Args:
            records: a tuple of all SharedNote records.

        Examples:
            This is a minimal example illustrating the process.
            >>> from genedata.build import Genealogy
            >>> from genedata.classes7 import RecordSnote, Name
            >>> a = Genealogy('test')
            >>> sn_id = a.shared_note_xref('1', 'The text of a shared note')
            >>> sn = RecordSnote(sn_id)
            >>> a.shared_notes(
            ...     [
            ...         sn,
            ...     ]
            ... )
            >>> print(a.ged_shared_note)
            0 @1@ SNOTE The text of a shared note
            <BLANKLINE>

            There may be more than one shared note record.  This example creates a second
            one and then runs the method.  This second run overwrites
            what was entered earlier.
            >>> sn_id2 = a.shared_note_xref('2', 'Other text')
            >>> sn2 = RecordSnote(sn_id2)
            >>> a.shared_notes(
            ...     [
            ...         sn,
            ...         sn2,
            ...     ]
            ... )
            >>> print(a.ged_shared_note)
            0 @1@ SNOTE The text of a shared note
            0 @2@ SNOTE Other text
            <BLANKLINE>

        See Also:
            - `families`: gather family records.
            - `individuals`: gather individual records.
            - `multimedia`: gather multimedia records.
            - `repositories`: gather repository records.
            - `shared_notes`: gather shared notes records.
            - `sources`: gather source records.
        """
        self.ged_shared_note = self._gather(records, self.shared_note_xreflist)

    def sources(self, records: list[RecordSour]) -> None:
        """Collect and store all source records for the genealogy.

        Args:
            records: a list of all Source records.

        Examples:
            This is a minimal example illustrating the process.
            >>> from genedata.build import Genealogy
            >>> from genedata.classes7 import RecordSour
            >>> a = Genealogy('test')
            >>> source_id = a.source_xref()
            >>> source = RecordSour(source_id)
            >>> a.sources(
            ...     [
            ...         source,
            ...     ]
            ... )
            >>> print(a.ged_source)
            0 @1@ SOUR
            <BLANKLINE>

            There may be more than one source record.  This example creates a second
            one and then runs the method.  This second run overwrites
            what was entered earlier.
            >>> source_id2 = a.source_xref()
            >>> source2 = RecordSour(source_id2)
            >>> a.sources(
            ...     [
            ...         source,
            ...         source2,
            ...     ]
            ... )
            >>> print(a.ged_source)
            0 @1@ SOUR
            0 @2@ SOUR
            <BLANKLINE>

        See Also:
            - `families`: gather family records.
            - `individuals`: gather individual records.
            - `multimedia`: gather multimedia records.
            - `repositories`: gather repository records.
            - `shared_notes`: gather shared notes records.
            - `sources`: gather source records.
        """
        self.ged_source = self._gather(records, self.source_xreflist)

    def submitters(self, records: list[RecordSubm]) -> None:
        """Collect and store all submitter records for the genealogy.

        Args:
            records: a list of all Submitter records.

        Examples:
            This is a minimal example illustrating the process.
            >>> from genedata.build import Genealogy
            >>> from genedata.classes7 import RecordSubm, Name
            >>> a = Genealogy('test')
            >>> sub_id = a.submitter_xref()
            >>> sub = RecordSubm(sub_id, Name('Tom'))
            >>> a.submitters(
            ...     [
            ...         sub,
            ...     ]
            ... )
            >>> print(a.ged_submitter)
            0 @1@ SUBM
            1 NAME Tom
            <BLANKLINE>

            There may be more than one submitter record.  This example creates a second
            one and then runs the method.  This second run overwrites
            what was entered earlier.
            >>> sub_id2 = a.submitter_xref()
            >>> sub2 = RecordSubm(sub_id2, Name('Joe'))
            >>> a.submitters(
            ...     [
            ...         sub,
            ...         sub2,
            ...     ]
            ... )
            >>> print(a.ged_submitter)
            0 @1@ SUBM
            1 NAME Tom
            0 @2@ SUBM
            1 NAME Joe
            <BLANKLINE>

        See Also:
            - `families`: gather family records.
            - `individuals`: gather individual records.
            - `multimedia`: gather multimedia records.
            - `repositories`: gather repository records.
            - `shared_notes`: gather shared notes records.
            - `sources`: gather source records.
        """
        self.ged_submitter = self._gather(records, self.submitter_xreflist)

    def header(self, ged_header: Head) -> None:
        """Collect and store the header record.

        Args:
            ged_header: is the text of the header record.

        References:
            [GEDCOM Example Files](https://gedcom.io/tools/#example-familysearch-gedcom-70-files)
        """
        self.ged_header = ged_header.ged()
