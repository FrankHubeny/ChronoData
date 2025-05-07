# Licensed under a 3-clause BSD style license - see LICENSE.md
"""Methods to build a genealogy based on the GEDCOM standard.

This module implements reading and writing genealogy files according to the
[FamilySearch GEDCOM Version 7](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html)
standard.
"""

import importlib
import logging
import re
from copy import deepcopy
from typing import Any, NamedTuple

from genedata.constants import Default
from genedata.messages import Msg
from genedata.methods import Names, Query, Util
from genedata.structure import (
    ExtensionAttributes,
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


class Line(NamedTuple):
    level: int = 0
    xref: str = Default.EMPTY
    tag: str = Default.EMPTY
    payload: str = Default.EMPTY
    keyname: str = Default.EMPTY
    classname: str = Default.EMPTY


class RecordName(NamedTuple):
    name: str = Default.EMPTY
    xref_name: str = Default.EMPTY
    record: str = Default.EMPTY
    has_xref: bool = True


class Genealogy:
    """Methods to add, update and remove a specific loaded genealogy."""

    def __init__(
        self,
        filename: str = Default.EMPTY,
        archive: str = Default.EMPTY,
        version: str = '7.0',
    ) -> None:
        """Initiate a GEDCOM genealogy.

        If one does not know the contents of the archive file, one can find that out by using
        the `Util.list_gdz` method.

        Args:
            filename: The full path the the file is an archive directory is not provided,
                otherwise the name of the file in the archive.
            archive: The full path to the archive (gdz) file if this is where the gedcom file
                and/or yaml specification files are stored.
            version: This value is set by the gedcom file if one is read,
                otherwise set this to a value for the gedcom file that will be created.
        """
        # Store the input values.
        self.filename: str = filename
        self.archive: str = archive
        self.version: str = version

        # Prepare to load the ged file if filename is not empty.
        self.tag_counter: int = 0
        self.ged_file: str = Default.EMPTY
        self.ged_ext_tags: list[list[Any]] = []
        self.tag_uri: list[list[str]] = []
        if self.filename != Default.EMPTY:
            if self.archive == Default.EMPTY:
                self.ged_file = Util.read_ged(self.filename)
            else:
                self.ged_file = Util.read_gdz_ged_file(
                    self.filename, self.archive
                )
            self.tag_uri = Query.extensions(self.ged_file)
            self.version = Query.version(self.ged_file)

        # Remove the periods from the version.
        self.version_no_periods: str = self.version.replace(
            Default.PERIOD, Default.EMPTY
        )

        # Import the version's specification module and load the Genealogy's specification with it.
        self.specs = importlib.import_module(
            f'genedata.specifications{self.version_no_periods}'
        )
        self.specification: dict[str, dict[str, Any]] = deepcopy(
            self.specs.Specs
        )
        self.all_structure_tags: list[str] = Query.all_structure_tags(self.specification)
        if len(self.tag_uri) > 0:
            for item in self.tag_uri:
                self.document_tag(item[0], item[1])

        # Load into the Genealogy's specification any extension tags from the file. Set tag counter.

        self.classes = importlib.import_module(
            f'genedata.classes{self.version_no_periods}'
        )

        # Storage areas for ged data that is created through the classes and not read from the file.
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
        self.ged_file_records: list[str] = []
        self.named_records: list[RecordName] = []
        self.record_counter: int = 0
        self.records: list[Any] = []
        # self.classes.RecordFam
        # | self.classes.RecordIndi
        # | self.classes.RecordObje
        # | self.classes.RecordRepo
        # | self.classes.RecordSnote
        # | self.classes.RecordSour
        # | self.classes.RecordSubm
        # ] = []
        self.record_header: Any = None  # self.classes.Head | None = None
        # self.schma: str = Default.EMPTY

        # self.filename_type: str = self._get_filename_type(self.filename)
        self.xref_counter: int = 1

        # self.extension_specification: dict[str, dict[str, Any]] = {
        #     Default.YAML_TYPE_CALENDAR: {},
        #     Default.YAML_TYPE_DATATYPE: {},
        #     Default.YAML_TYPE_ENUMERATION_SET: {},
        #     Default.YAML_TYPE_ENUMERATION: {},
        #     Default.YAML_TYPE_MONTH: {},
        #     Default.YAML_TYPE_STRUCTURE: {},
        #     Default.YAML_TYPE_URI: {},
        # }
        self.all_xrefs: dict[str, str] = {}
        self.extension_xreflist: list[str] = [Void.NAME]
        self.family_xreflist: list[str] = [Void.NAME]
        self.individual_xreflist: list[str] = [Void.NAME]
        self.multimedia_xreflist: list[str] = [Void.NAME]
        self.repository_xreflist: list[str] = [Void.NAME]
        self.shared_note_xreflist: list[str] = [Void.NAME]
        self.source_xreflist: list[str] = [Void.NAME]
        self.submitter_xreflist: list[str] = [Void.NAME]
        self.record_dict: dict[str, dict[str, str]] = {
            'EXT': {
                'key': 'record-FAM',
                'type': Default.EXT_RECORD_TYPE,
                'class': 'Ext',
                'call': 'extension_xref',
            },
            'FAM': {
                'key': 'record-FAM',
                'type': Default.FAM_RECORD_TYPE,
                'class': 'RecordFam',
                'call': 'family_xref',
            },
            'INDI': {
                'key': 'record-INDI',
                'type': Default.INDI_RECORD_TYPE,
                'class': 'RecordIndi',
                'call': 'individual_xref',
            },
            'OBJE': {
                'key': 'record-OBJE',
                'type': Default.OBJE_RECORD_TYPE,
                'class': 'RecordObje',
                'call': 'multimedia_xref',
            },
            'REPO': {
                'key': 'record-REPO',
                'type': Default.REPO_RECORD_TYPE,
                'class': 'RecordRepo',
                'call': 'repository_xref',
            },
            'SNOTE': {
                'key': 'record-SNOTE',
                'type': Default.SNOTE_RECORD_TYPE,
                'class': 'RecordSnote',
                'call': 'shared_note_xref',
            },
            'SOUR': {
                'key': 'record-SOUR',
                'type': Default.SOUR_RECORD_TYPE,
                'class': 'RecordSour',
                'call': 'source_xref',
            },
            'SUBM': {
                'key': 'record-SUBM',
                'type': Default.SUBM_RECORD_TYPE,
                'class': 'RecordSubm',
                'call': 'submitter_xref',
            },
        }
        self.split_ged()

    def split_ged(self) -> None:
        """Split the ged string into records without the trailer."""

        if self.ged_file != Default.EMPTY:
            # Remove the trailer along with everything after it.
            ged: str = Default.EMPTY
            ged, _, _ = self.ged_file.partition(Default.TRAILER)

            # Remove anything before the header record the end of line character.
            ged_temp: str = Default.EMPTY
            _, _, ged_temp = ged.partition(Default.GED_HEADER)
            ged = ''.join([Default.GED_HEADER, ged_temp])

            # Replace CONT and escaped @ with special string to remove later.
            ged = re.sub('\n\\d CONT @', Default.GED_REPLACE_THIS, ged)

            # Replace CONT with a non-empty payload to remove later.
            ged = re.sub('\n\\d CONT ', Default.GED_REPLACE_THIS, ged)

            # Replace CONT with no payload to remove later.
            ged = re.sub('\n\\d CONT', Default.GED_REPLACE_THIS, ged)

            # Split the rest into a list of ged records.
            self.ged_file_records = []
            self.ged_file_records = ged.split(f'{Default.EOL}0{Default.SPACE}')

            # Name each record with a unique name based on cross reference identifier if present.
            for record in self.ged_file_records:
                first_line, _, _ = record.partition(Default.EOL)
                # if first_line == Default.GED_HEADER:
                #     self.named_records.append(
                #         RecordName(name='header', record=record, has_xref=False)
                #     )
                # else:
                spaces = first_line.count(Default.SPACE)
                match spaces:
                    case 0:
                        name: str = ''.join(
                            [first_line, str(self.record_counter)]
                        )
                        if first_line in [
                            Default.TAG_FAM,
                            Default.TAG_INDI,
                            Default.TAG_OBJE,
                            Default.TAG_REPO,
                            Default.TAG_SNOTE,
                            Default.TAG_SOUR,
                            Default.TAG_SUBM,
                        ]:
                            xref_name: str = f'Void.{first_line}'
                        # else:
                        #     xref_name = 'Void.EXT'
                        self.record_counter += 1
                        self.named_records.append(
                            RecordName(
                                name=name,
                                record=record,
                                xref_name=xref_name,
                            )
                        )
                    case _:
                        xref_tag: list[str] = first_line.split(
                            Default.SPACE, 2
                        )
                        name = Names.record_name(xref_tag[1], xref_tag[0])
                        xref_name = ''.join(
                            [
                                name,
                                Default.UNDERLINE,
                                Default.XREF,
                            ]
                        )
                        self.named_records.append(
                            RecordName(
                                name=name,
                                xref_name=xref_name,
                                record=record,
                            )
                        )

    def view_extensions(self) -> tuple[list[list[str]], list[str], list[str]]:
        """Display a list of available extensions to use or be aware of.

        There are three lists returned.  The first list corresponds to the
        pandas DataFrame `data` argument.  The second corresponds to the `index` argument.
        The third corresponds to the `columns` argument.

        The final value is the full yaml_dictionary read by the `document_tag` method.
        This may be worth checking if something doesn't look right.
        Since this final value will likely take up many lines, one can simply type
        the variable assigned to this first returned list in a Jupyter notebook
        to see all of the values.
        """
        values: list[list[str]] = []
        keys: list[str] = []
        labels: list[str] = [
            'Tag',
            'Specification',
            'Type',
            'Payload',
            'Supers',
            'Superstructures',
            'Required',
            'Permitted',
            'Single',
            'Enumset Key',
            'Enum Tags',
            'Yaml Dictionary',
        ]
        for tag in self.ged_ext_tags:
            keys.append(tag[0])
            values.append(
                [
                    tag[1],
                    tag[2],
                    tag[3],
                    tag[4],
                    tag[5],
                    tag[6],
                    tag[7],
                    tag[8],
                    tag[9],
                    tag[10],
                    tag[11],
                    tag[12],
                ]
            )
        return values, keys, labels

    def document_tag(self, tag: str, yaml_file: str) -> ExtensionAttributes:
        """Add an extension tag to the extension specifications.

        Run this on a specific yaml file to make the specification
        available when building the ged files.

        The GEDCOM specifications provide the following recommendation
        that this application follows (1.5.2):
        > It is recommended that applications not use undocumented extension tags.

        Undocumented extension tags will be noted as such but not made available
        until a readable yaml specification file is made available.

        The GEDCOM specification states the following:
        > A given schema should map only one tag to each URI.

        To implement this a ValueError is thrown if a yaml_file has already been used.

        Examples:
            With the `good_calendar.yaml` file in the testing data directory
            one can create an extension tag `_MYTAG` by running the following:
            >>> from genedata.build import Genealogy
            >>> g = Genealogy()
            >>> mytag = g.document_tag(
            ...     '_MYTAG', 'tests/data/good_calendar.yaml'
            ... )

            If one tries to use the same file again, an error is produced.
            >>> yourtag = g.document_tag(
            ...     '_YOURTAG', 'tests/data/good_calendar.yaml'
            ... )
            Traceback (most recent call last):
            ValueError: The yaml file "tests/data/good_calendar.yaml" has already been used for another extension.

        Args:
            tag: The extension tag with an initial underline and all capitals
                that must be in the `extension tags` list or which must be
                the `standard tag`.
            yaml_file: The location of the yaml_file as either a url or a file
                in a regular or compressed directory such as a GDZ archive.

        References:
            [GEDCOM Extensions](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#extensions)
        """
        for tag_line in self.ged_ext_tags:
            if tag_line[2] == yaml_file:
                raise ValueError(Msg.YAML_FILE_HAS_BEEN_USED.format(yaml_file))
        yaml_dict: dict[str, dict[str, Any]] = {}
        yaml_type: str = Default.EMPTY
        required: list[str] = []
        single: list[str] = []
        permitted: list[str] = []
        payload: str = Default.EMPTY
        enumset_key: str = Default.EMPTY
        enum_tags: list[str] = []
        supers: int = 0
        superstructures: list[str] | None = None
        supers_required: list[str] = []
        supers_single: list[str] = []
        tag_edited: str = tag.upper()
        extension_key: str = Default.EMPTY
        if tag_edited[0] != Default.UNDERLINE:
            tag_edited = ''.join([Default.UNDERLINE, tag_edited])
        documented: bool = True
        try:
            yaml_dict = Util.read_yaml(yaml_file)
        except Exception:
            logging.info(
                Msg.CANNOT_READ_YAML_FILE.format(yaml_file, tag_edited)
            )
            documented = False
        self.tag_counter += 1
        if documented:
            self.all_structure_tags.append(tag)
            yaml_type = str(yaml_dict[Default.YAML_TYPE])
            extension_key = Names.keyname(str(yaml_dict[Default.YAML_URI]))
            # if extension_key in self.specification[yaml_type]:
            #     raise ValueError(Msg.EXTENSION_EXISTS.format(extension_key, yaml_type))
            self.specification[yaml_type].update({extension_key: yaml_dict})
            # match yaml_type:
            #     case Default.YAML_TYPE_STRUCTURE:
            required = Query.required(extension_key, self.specification)
            single = Query.singular(extension_key, self.specification)
            permitted = Query.permitted(extension_key, self.specification)
            payload = Query.payload(extension_key, self.specification)
            supers = Query.supers_count(extension_key, self.specification)
            superstructures = Query.superstructures(
                extension_key, self.specification
            )
            supers_required = Query.supers_required(
                extension_key, self.specification
            )
            supers_single = Query.supers_singular(
                extension_key, self.specification
            )
            logging.info(f'superstructures = {superstructures}')
            # case Default.YAML_TYPE_ENUMERATION:
            enumset_key, enum_tags = Query.enum_key_tags(
                extension_key, self.specification
            )
            self.ged_ext_tags.append(
                [
                    str(self.tag_counter),
                    tag,
                    yaml_file,
                    yaml_type,
                    payload,
                    supers,
                    superstructures,
                    supers_required,
                    supers_single,
                    required,
                    single,
                    permitted,
                    enumset_key,
                    enum_tags,
                    yaml_dict,
                ]
            )
        return ExtensionAttributes(
            id=self.tag_counter,
            key=extension_key,
            tag=tag,
            yaml_file=yaml_file,
            yaml_type=yaml_type,
            required=required,
            single=single,
            permitted=permitted,
            enumset_key=enumset_key,
            enum_tags=enum_tags,
            payload=payload,
            supers=supers,
            superstructures=superstructures,
            supers_required=supers_required,
            supers_single=supers_single,
        )

    def stage(
        self,
        record: Any,
    ) -> None:
        # if not isinstance(
        #     record,
        #     self.classes.Head
        #     | self.classes.RecordFam
        #     | self.classes.RecordIndi
        #     | self.classes.RecordObje
        #     | self.classes.RecordRepo
        #     | self.classes.RecordSnote
        #     | self.classes.RecordSour
        #     | self.classes.RecordSubm
        #     | Ext,
        # ):
        #     raise ValueError(Msg.ONLY_RECORDS.format(str(record)))
        if isinstance(record, self.classes.Head):
            self.record_header = record
        else:
            self.records.append(record)

    def show_ged(self) -> str:
        """Display the ged file constructed by this instance of the Genealogy class.

        Examples:
            This example has a minimal header, two records and a trailer.  It is constructed
            using the following steps.
            >>> from genedata.build import Genealogy
            >>> import genedata.classes70 as gc
            >>> g = Genealogy()
            >>> indi_xref = g.individual_xref('1')
            >>> fam_xref = g.family_xref('2')
            >>> indi = gc.RecordIndi(indi_xref)
            >>> fam = gc.RecordFam(fam_xref)
            >>> head = gc.Head(gc.Gedc(gc.GedcVers('7.0')))
            >>> g.stage(head)
            >>> g.stage(fam)
            >>> g.stage(indi)
            >>> print(g.show_ged())
            0 HEAD
            1 GEDC
            2 VERS 7.0
            0 @2@ FAM
            0 @1@ INDI
            0 TRLR

        """
        if self.record_header is None:
            raise ValueError(Msg.MISSING_HEADER)

        # Construct the ged lines for each record.
        lines = self.record_header.ged(specs=self.specification)
        for record in self.records:
            lines = ''.join([lines, record.ged(specs=self.specification)])
        return ''.join([lines, Default.TRAILER])

    def save_ged(self, file_name: str = Default.EMPTY) -> None:
        """Save the ged file constructed by this instance of the Genealogy class."""
        Util.write_ged(self.show_ged(), file_name)

    def ged_to_code(self) -> str:
        """Convert the loaded ged file to code that produces the ged file."""

        level_key: dict[int, str] = {}

        # def split_subs(ged: str, level: int = 0) -> list[str]:
        #     """Split a ged string on substructures at the specified level."""
        #     marker: str = f'{Default.EOL}{level}{Default.SPACE}'
        #     return ged.split(marker)

        def parse(line: str) -> Line:
            """Parse a GEDCOM line into level, xref, tag and payload."""

            # Initialize the local variables for type checking.
            words: list[str] = []
            level: int = 0
            xref: str = Default.EMPTY
            tag: str = Default.EMPTY
            payload: str = Default.EMPTY
            payload_type: str = Default.EMPTY
            keyname: str = Default.EMPTY
            classname: str = Default.EMPTY

            # Get the level as an integer.
            if line != Default.EMPTY:
                words = line.split(Default.SPACE, 2)
                level = int(words[0])

                # If the level is greater than 0 there is only a level, tag and payload.
                # We only need to split on space twice to get these if they are all there.
                # Remove the extra `@` on the payload.
                if level > 0:
                    tag = words[1]
                    if len(words) > 2:
                        payload = words[2]

                # Raise an error if the tag is neither a standard tag nor a documented extension tag.
                if tag not in self.all_structure_tags:
                    raise ValueError(Msg.NOT_DOCUMENTED_TAG.format(tag))

                # If the level equals 0, this is a record with also an xref value.
                # Resplit on space three times and assign values.  Remove the extra `@`
                # on the payload.
                # else:
                #     words = line.split(Default.SPACE, 3)
                #     if words[1][0:1] == Default.ATSIGN:
                #         xref = words[1]
                #         tag = words[2]
                #         if len(words) > 3:
                #             payload = words[3]
                #     else:
                #         tag = words[1]
                #         if len(words) > 2:
                #             payload = words[2]

                key = level_key[level - 1]
                if key in self.specification[Default.YAML_TYPE_STRUCTURE]:
                    for uri in self.specification[Default.YAML_TYPE_STRUCTURE][
                        key
                    ][Default.YAML_SUBSTRUCTURES]:
                        sub_key = Names.keyname(uri)
                        if (
                            self.specification[Default.YAML_TYPE_STRUCTURE][
                                sub_key
                            ][Default.YAML_STANDARD_TAG]
                            == tag
                        ):
                            keyname = sub_key
                            classname = Names.classname(sub_key)
                            break
                level_key.update({level: keyname})
                payload_type = Query.payload(keyname, self.specification)
                match payload_type:
                    case 'http://www.w3.org/2001/XMLSchema#string':
                        payload = Names.quote_text(remove_at(payload))
                    case 'Y|<NULL>':
                        payload = "''" if payload == Default.EMPTY else "'Y'"
                    case 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger':
                        pass
                    case 'https://gedcom.io/terms/v7/type-List#Enum':
                        payload = Names.quote_text(payload)
                    case 'https://gedcom.io/terms/v7/type-Enum':
                        payload = Names.quote_text(payload)
                    case '@<https://gedcom.io/terms/v7/record-INDI>@':
                        payload = Names.xref_name(Default.TAG_INDI, payload)
                    case '@<https://gedcom.io/terms/v7/record-FAM>@':
                        payload = Names.xref_name(Default.TAG_FAM, payload)
                    case 'https://gedcom.io/terms/v7/type-List#Text':
                        payload = Names.quote_text(payload)
                    case '@<https://gedcom.io/terms/v7/record-SUBM>@':
                        payload = Names.xref_name(Default.TAG_SUBM, payload)
                    case 'http://www.w3.org/2001/XMLSchema#Language':
                        payload = Names.quote_text(payload)
                    case 'https://gedcom.io/terms/v7/type-Date#period':
                        payload = Names.quote_text(payload)
                    case 'https://gedcom.io/terms/v7/type-Date#exact':
                        payload = Names.quote_text(payload)
                    case 'https://gedcom.io/terms/v7/type-Date':
                        payload = Names.quote_text(payload)
                    case 'https://gedcom.io/terms/v7/type-FilePath':
                        payload = Names.quote_text(payload)
                    case 'https://gedcom.io/terms/v7/type-Name':
                        payload = Names.quote_text(payload)
                    case 'https://gedcom.io/terms/v7/type-Age':
                        payload = Names.quote_text(payload)
                    case 'http://www.w3.org/ns/dcat#mediaType':
                        payload = Names.quote_text(payload)
                    case '@<https://gedcom.io/terms/v7/record-OBJE>@':
                        payload = Names.xref_name(Default.TAG_OBJE, payload)
                    case '@<https://gedcom.io/terms/v7/record-REPO>@':
                        payload = Names.xref_name(Default.TAG_REPO, payload)
                    case '@<https://gedcom.io/terms/v7/record-SNOTE>@':
                        payload = Names.xref_name(Default.TAG_SNOTE, payload)
                    case '@<https://gedcom.io/terms/v7/record-SOUR>@':
                        payload = Names.xref_name(Default.TAG_SOUR, payload)
                    case 'https://gedcom.io/terms/v7/type-Time':
                        payload = Names.quote_text(payload)
                    # case 'None':
                    #     payload = Default.EMPTY
                    case _:
                        payload = Default.EMPTY

            # Now return the values as a NamedTuple.
            return Line(level, xref, tag, payload, keyname, classname)

        def remove_at(value: str) -> str:
            """Remove the first `@` which escapes the second `@`
            at the beginning of a string value.
            """
            if value[0:2] == '@@':
                return value[1:]
            return value

        def record_subs(bottom: str) -> str:
            """Convert the GEDCOM lines after the first lines of the record to code."""

            # Initial local variables with typing.
            line: str = Default.EMPTY
            current_level: int = 0
            next_level: int = 1
            endline: str = Default.EMPTY
            subs_list: list[str] = []
            next_level_list: list[int] = []
            parsed_subs: list[Line] = []

            # Split the remaining part of the record string into a list breaking on end of lines.
            subs_list = bottom.split(Default.EOL)

            # Loop through the list parsing each line keeping a separate list of the levels.
            for sub in subs_list:
                parsed_item = parse(sub)
                next_level_list.append(parsed_item.level)
                parsed_subs.append(parsed_item)
            next_level_list.append(0)

            # Loop through the parsed list formatting the code output.
            for i in range(len(parsed_subs)):
                # Provide variables for current and next level for clarity.
                current_level = parsed_subs[i].level
                next_level = next_level_list[i + 1]

                # Paths to format the end of a line.
                # If there is no payload.
                if parsed_subs[i].payload == Default.EMPTY:
                    # If there are substructures.
                    if next_level > current_level:
                        endline = f'{Default.BRACKET_LEFT}{Default.EOL}'

                    # if substructures have ended.
                    elif next_level < current_level:
                        endline = f'{Default.PARENS_RIGHT}{Default.COMMA}'

                    # If there are no more substructures.
                    elif next_level == 0:
                        endline = ''.join(
                            [
                                Default.PARENS_RIGHT,
                                Default.COMMA,
                                Default.EOL,
                                Default.BRACKET_RIGHT,
                                Default.PARENS_RIGHT,
                            ]
                        )

                    # If there are more substructures.
                    # else:
                    #     endline = f'{Default.PARENS_RIGHT}{Default.COMMA}'

                # If there is a payload and there are substructures.
                elif next_level > current_level:
                    endline = f'{Default.COMMA}{Default.SPACE}{Default.BRACKET_LEFT}{Default.EOL}'

                # If there are no more substructures.
                elif next_level < current_level:
                    endline = ''.join(
                        [
                            Default.PARENS_RIGHT,
                            Default.COMMA,
                        ]
                    )
                    if current_level > 1:
                        for level in range(current_level, next_level + 1, -1):
                            endline = ''.join(
                                [
                                    endline,
                                    Default.EOL,
                                    (level - 1) * Default.INDENT,
                                    Default.BRACKET_RIGHT,
                                    Default.PARENS_RIGHT,
                                    Default.COMMA,
                                ]
                            )
                    if next_level == 0:
                        endline = ''.join(
                            [
                                endline,
                                Default.EOL,
                                Default.BRACKET_RIGHT,
                                Default.PARENS_RIGHT,
                                Default.EOL,
                            ]
                        )
                    else:
                        endline = ''.join(
                            [
                                endline,
                                Default.EOL,
                                next_level * Default.INDENT,
                                Default.BRACKET_RIGHT,
                                Default.PARENS_RIGHT,
                                Default.COMMA,
                                Default.EOL,
                            ]
                        )

                # If there is a payload and there are more substructures.
                else:
                    endline = (
                        f'{Default.PARENS_RIGHT}{Default.COMMA}{Default.EOL}'
                    )

                # Add to line the additional code details.
                if parsed_subs[i].classname != Default.EMPTY:
                    line = ''.join(
                        [
                            line,
                            current_level * Default.INDENT,
                            Default.CODE_CLASS,
                            parsed_subs[i].classname,
                            Default.PARENS_LEFT,
                            parsed_subs[i].payload,
                            endline,
                        ]
                    )
            return line

        def header() -> str:
            """Generate the header record."""

            # Initialize local variables.
            classname: str = 'Head'
            line: str = """
# Instantiate the header record.
"""
            recordname: str = self.named_records[0].name

            # Partition on end of life to get the first line of the record
            # which may be all there is.
            _, _, bottom = self.ged_file_records[0].partition(Default.EOL)

            # Record that we are starting at the 0 level with the HEAD record.
            level_key.update(
                {0: Names.key_from_classname(classname, self.specification)}
            )

            # Added the parsed contents to the output line.
            line = ''.join(
                [
                    line,
                    recordname,
                    Default.EQUAL,
                    Default.CODE_CLASS,
                    classname,
                    Default.PARENS_LEFT,
                    Default.BRACKET_LEFT,
                    Default.EOL,
                ]
            )

            # If there is more, then prepare for substructures.
            if bottom != Default.EMPTY:
                line = ''.join([line, record_subs(bottom)])

            # End the record because there are no substructures which should not be the case.
            # else:
            #     line = ''.join([line, Default.PARENS_RIGHT])
            return line

        def imports() -> str:
            """Construct the section of the code where the imports are made."""
            return f"""# Import the required packages and classes.
import genedata.classes{self.version_no_periods} as {Default.CODE_CLASS_VARIABLE}
from genedata.build import Genealogy
{structure_module}
"""

        def initialize() -> str:
            """Construct the section of the code where the Genealogy class is instantiated."""
            return f"""# Instantiate a Genealogy class.
{Default.CODE_GENEALOGY_VARIABLE} = Genealogy()
"""

        def extensions() -> str:
            """Construct the extension assignments."""

            # If there are any extensions, this will introduce them in the generated code.
            intro: str = """
# Add any extensions that were registered in the header record.
"""
            # Initialize the return value.
            lines: str = Default.EMPTY

            # The SCHMA take is the superstructure for the desired TAG lines.
            # Without this being present, return the empty string.
            if Default.GED_EXT_SCHMA in self.ged_file_records[0]:
                # Initialize and type the local variables used.
                tag_words: list[str] = []
                tag_list: list[str] = []
                ext_name: str = Default.EMPTY

                # Split the string based on the TAG identifier which begins each TAG line.
                tag_list = self.ged_file_records[0].split('\n2 TAG ')

                # Ignoring the first item in the list, obtain tag information from the others.
                last_index: int = len(tag_list[1:]) - 1
                for index, tag in enumerate(tag_list[1:]):
                    # The end of line was left in the first split to identify the end of the TAG line.
                    tag_line: str = tag
                    if index == last_index:
                        tag_line, _, _ = tag.partition(Default.EOL)

                    # There is only one space in the string separating the tag from the url.
                    tag_words = tag_line.split(Default.SPACE)

                    # Construct the variable name that will be used in the code from these two items.
                    ext_name = Names.extension_name(tag_words[0], tag_words[1])

                    # Construct the code line for the external tag.
                    lines = ''.join(
                        [
                            lines,
                            ext_name,
                            Default.EQUAL,
                            Default.CODE_GENEALOGY,
                            'document_tag',
                            Default.PARENS_LEFT,
                            Names.quote_text(tag_words[0]),
                            Default.COMMA,
                            Default.SPACE,
                            Names.quote_text(tag_words[1]),
                            Default.PARENS_RIGHT,
                            Default.EOL,
                        ]
                    )

            # If there were any tags, then add in the intro, otherwise return the empty string.
            if lines != Default.EMPTY:
                lines = ''.join([intro, lines])
            return lines  # .replace(Default.GED_REPLACE_THIS, Default.EOL)

        def xrefs() -> str:
            """Construct the section of the code where the cross reference identifiers are instantiated."""
            lines: str = """
# Instantiate the cross reference identifiers.
"""
            xref_lines: str = Default.EMPTY
            xref_count: int = 0
            if record_count > 1:
                # For all records except the first which is the header record.
                for named_record in self.named_records[1:]:
                    if named_record.has_xref:
                        name = named_record.xref_name
                        # Partition on the first end of line character keeping the first and last parts.
                        first, _, last = named_record.record.partition(
                            Default.EOL
                        )

                        if first.count(Default.SPACE) > 0:
                            # Split the first part into two or three strings.
                            words: list[str] = first.split(Default.SPACE, 2)
                            xref_count += 1

                            # Get the name for the method to call to create that variable.
                            if words[1] in self.record_dict:
                                call: str = self.record_dict[words[1]]['call']
                            else:
                                call = 'extension_xref'

                            # If the record has a payload, such as SNOTE has, include it.
                            payload: str = Default.EMPTY
                            add_comma: str = Default.EMPTY

                            # A payload would be text in the third string.
                            if len(words) > 2:
                                payload = remove_at(words[2])
                                add_comma = ', '

                                # This text might be continued or an indefinite number of lines.
                                # while last[0:7] == '1 CONT':
                                #     first, _, last = last.partition(Default.EOL)
                                #     _, _, more_payload = first.partition(
                                #         '1 CONT'
                                #     )
                                #     payload = ''.join(
                                #         [
                                #             payload,
                                #             Default.EOL,
                                #             remove_at(more_payload[1:]),
                                #         ]
                                #     )
                                payload = Names.quote_text(payload)

                            # Add each to the code lines to be generated.
                            xref_lines = ''.join(
                                [
                                    xref_lines,
                                    name,
                                    Default.EQUAL,
                                    Default.CODE_GENEALOGY,
                                    call,
                                    Default.PARENS_LEFT,
                                    Default.QUOTE_SINGLE,
                                    words[0].replace(
                                        Default.ATSIGN, Default.EMPTY
                                    ),
                                    Default.QUOTE_SINGLE,
                                    add_comma,
                                    payload,
                                    Default.PARENS_RIGHT,
                                    Default.EOL,
                                ]
                            )
                lines = ''.join(
                    [
                        lines,
                        f'# There were {xref_count} cross reference identifiers.',
                        Default.EOL,
                        xref_lines,
                    ]
                )
            else:
                lines = ''.join(
                    [
                        lines,
                        '# There were no cross reference identifiers.',
                        Default.EOL,
                    ]
                )
            return lines  # .replace(Default.GED_REPLACE_THIS, Default.EOL)

        def record_loop() -> str:
            """Construct the code for a record."""

            # Initialize and type the local variables.
            line: str = """
# Instantiate the records holding the GED data.
"""
            parts: list[str] = []
            classname: str = Default.EMPTY
            spaces: int = 0

            # Skip if there aren't any records except for the header record.
            if record_count > 1:
                # Loop through all the records excluding the header record at index 0.
                for named_record in self.named_records[1:]:
                    # Partition on end of life to get the first line of the record
                    # which may be all there is.
                    top, _, bottom = named_record.record.partition(Default.EOL)

                    # Parse the first line into its components and format the names.
                    spaces = top.count(Default.SPACE)
                    match spaces:
                        case 0:
                            classname = Names.top_class(top)
                        case 1:
                            parts = top.split(Default.SPACE, 1)
                            classname = Names.top_class(parts[1])
                        case _:
                            parts = top.split(Default.SPACE, 2)
                            classname = Names.top_class(parts[1])
                    level_key.update(
                        {
                            0: Names.key_from_classname(
                                classname, self.specification
                            )
                        }
                    )

                    # Added the parsed contents to the output line.
                    line = ''.join(
                        [
                            line,
                            named_record.name,
                            Default.EQUAL,
                            Default.CODE_CLASS,
                            classname,
                            Default.PARENS_LEFT,
                            named_record.xref_name,
                        ]
                    )

                    # If there is more, then construct the substructures.
                    if bottom != Default.EMPTY:
                        line = ''.join(
                            [
                                line,
                                Default.COMMA,
                                Default.SPACE,
                                Default.BRACKET_LEFT,
                                Default.EOL,
                                record_subs(bottom),
                            ]
                        )

                    # End the record because there are no substructures.
                    else:
                        line = ''.join(
                            [line, Default.PARENS_RIGHT, Default.EOL]
                        )
            else:
                line = ''.join(
                    [
                        line,
                        '# There were no records outside of the header record.',
                        Default.EOL,
                    ]
                )
            return line

        def stage() -> str:
            """Generate a call for each record variable to be staged."""
            lines: str = f"""
# Stage the {record_count} GEDCOM records to generate the ged lines.
"""
            for record in self.named_records:
                lines = ''.join(
                    [
                        lines,
                        Default.CODE_GENEALOGY,
                        Default.STAGE,
                        Default.PARENS_LEFT,
                        record.name,
                        Default.PARENS_RIGHT,
                        Default.EOL,
                    ]
                )
            return lines

        def run_code() -> str:
            lines: str = f"""
# Run the following to show the ged file that the above code would produce.
ged_file = {Default.CODE_GENEALOGY}show_ged()

# Then print this file to view it.
print(ged_file)
"""
            return lines

        # Run the methods to generate the code to produce the ged file.
        # self.split_ged()
        record_count: int = len(self.ged_file_records)
        structure_module: str = Default.EMPTY
        if Default.VOID_POINTER in self.ged_file:
            structure_module = (
                f'from genedata.structure import Void{Default.EOL}'
            )
        return ''.join(
            [
                imports(),
                initialize(),
                xrefs(),
                extensions(),
                header(),
                record_loop(),
                stage(),
                run_code(),
            ]
        )

    def _get_counter(self) -> str:
        counter = str(self.xref_counter)
        self.xref_counter += 1
        return str(counter)

    def _set_xref(
        self, xref_list: list[str], xref: str, xref_name: str = ''
    ) -> None:
        if xref in self.all_xrefs:
            raise ValueError(Msg.XREF_EXISTS.format(xref, xref_name))
        self.all_xrefs.update({xref: f'xref_{xref.replace(Default.ATSIGN, Default.EMPTY)}'})
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
            ValueError if a name is used twice.


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
            >>> a = Genealogy()
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
            >>> a = Genealogy()
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
            >>> a = Genealogy()
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
            >>> a = Genealogy()
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
            >>> a = Genealogy()
            >>> id = a.shared_note_xref('1', 'This is a shared note.')
            >>> print(id)
            @1@

            The second example shows the output when the identifier has a name.
            >>> id2 = a.shared_note_xref('sn', 'This is a shared note.')
            >>> print(id2)
            @SN@

            The third example shows the output when the name is to be used as the initial
            part of the identifier.
            >>> id3 = a.shared_note_xref('SNOTE', '  ')
            >>> print(id3)
            @SNOTE@

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
            >>> a = Genealogy()
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
            >>> a = Genealogy()
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

    def extension_xref(
        self, xref_name: str = '', initial: bool = False
    ) -> ExtensionXref:
        """
        Create an ExtensionXref identifier from a unique string according to the
        GEDCOM standard.

        Args:
            xref_name (str, optional): A name for the identifier. Defaults to ''.
            initial (bool, optional): Whether to use the name as an initial
                value with an integer following. Defaults to False.

        Returns:
            ExtensionXref: A unique identifier string with type ExtensionXref.

        Examples:
            The first example generates identifier for a shared note record.
            >>> from genedata.build import Genealogy
            >>> a = Genealogy()
            >>> id = a.extension_xref()
            >>> print(id)
            @1@

            The second example shows the output when the identifier has a name.
            >>> id2 = a.extension_xref('sub')
            >>> print(id2)
            @SUB@

            The third example shows the output when the name is to be used as the initial
            part of the identifier.
            >>> id3 = a.extension_xref('SUB', True)
            >>> print(id3)
            @SUB2@

            The final example shows what happens if we try to assign two different
            records with the same name.  We already have @SUB@ so we will try
            creating that name again.
            >>> a.extension_xref('sub')
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
        extension_xref = self._counter(
            self.extension_xreflist,
            xref_name,
            initial,
        )
        return ExtensionXref(extension_xref)

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

    def families(self, records: list[Any]) -> None:
        """Collect and store all family records for the genealogy.

        Args:
            records: a list of all Family records.

        Examples:
            This is a minimal example illustrating the process.
            >>> from genedata.build import Genealogy
            >>> from genedata.classes70 import RecordFam
            >>> a = Genealogy()
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

    def individuals(self, records: list[Any]) -> None:
        """Collect and store all individual records for the genealogy.

        Args:
            records: a list of all Individual records.

        Examples:
            This is a minimal example illustrating the process.
            >>> from genedata.build import Genealogy
            >>> from genedata.classes70 import RecordIndi
            >>> a = Genealogy()
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

    def multimedia(self, records: list[Any]) -> None:
        """Collect and store all multimedia records for the genealogy.

        Args:
            records: a list of all Multimedia records.

        Examples:
            This is a minimal example illustrating the process.
            >>> from genedata.build import Genealogy
            >>> from genedata.classes70 import File, Form, RecordObje
            >>> a = Genealogy()
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

    def repositories(self, records: list[Any]) -> None:
        """Collect and store all repository records for the genealogy.

        Args:
            records: a list of all Repository records.

        Examples:
            This is a minimal example illustrating the process.
            >>> from genedata.build import Genealogy
            >>> from genedata.classes70 import RecordRepo, Name
            >>> a = Genealogy()
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

    def shared_notes(self, records: list[Any]) -> None:
        """Collect and store all shared note records for the genealogy.

        Args:
            records: a tuple of all SharedNote records.

        Examples:
            This is a minimal example illustrating the process.
            >>> from genedata.build import Genealogy
            >>> from genedata.classes70 import RecordSnote, Name
            >>> a = Genealogy()
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

    def sources(self, records: list[Any]) -> None:
        """Collect and store all source records for the genealogy.

        Args:
            records: a list of all Source records.

        Examples:
            This is a minimal example illustrating the process.
            >>> from genedata.build import Genealogy
            >>> from genedata.classes70 import RecordSour
            >>> a = Genealogy()
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

    def submitters(self, records: list[Any]) -> None:
        """Collect and store all submitter records for the genealogy.

        Args:
            records: a list of all Submitter records.

        Examples:
            This is a minimal example illustrating the process.
            >>> from genedata.build import Genealogy
            >>> from genedata.classes70 import RecordSubm, Name
            >>> a = Genealogy()
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

    # def header(self, ged_header: Any) -> None:
    #     """Collect and store the header record.

    #     Args:
    #         ged_header: is the text of the header record.

    #     References:
    #         [GEDCOM Example Files](https://gedcom.io/tools/#example-familysearch-gedcom-70-files)
    #     """
    #     self.ged_header = ged_header.ged()

    def query_record_counts(
        self,
        column: str = Default.COLUMN_COUNT,
    ) -> dict[str, dict[str, int]]:
        """Return the dictionary for record counts using the loaded ged file.

        This assumes that a gedcom file has been loaded into the Genealogy class.
        If it is not then the report will be run on the empty string.  The counts
        for all records would then be 0.  For example:
        >>> from genedata.build import Genealogy
        >>> g = Genealogy()
        >>> g.query_record_counts()
        {'Count': {'FAM': 0, 'INDI': 0, 'OBJE': 0, 'REPO': 0, 'SNOTE': 0, 'SOUR': 0, 'SUBM': 0}}

        This would be better formatted if the dictionary were passed through pandas.
        >>> import pandas as pd
        >>> pd.DataFrame(g.query_record_counts())
               Count
        FAM        0
        INDI       0
        OBJE       0
        REPO       0
        SNOTE      0
        SOUR       0
        SUBM       0

        Args:
            column: The name of the main dictionary key which would be the column
                name if a pandas DataFrame were used to display the dictionary."""
        return Query.record_counts(
            self.ged_file,
            column=column,
        )
