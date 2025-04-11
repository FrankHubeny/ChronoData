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

import importlib
import logging
import re
from typing import Any, NamedTuple

# from genedata.classes70 import (
#     Head,
#     RecordFam,
#     RecordIndi,
#     RecordObje,
#     RecordRepo,
#     RecordSnote,
#     RecordSour,
#     RecordSubm,
# )
from genedata.constants import (
    Config,
    Default,
    Number,
    String,
)
from genedata.messages import Msg
from genedata.methods import Names, Query, Util

#from genedata.specifications70 import Structure
from genedata.structure import (
    FamilyXref,
    IndividualXref,
    MultimediaXref,
    RepositoryXref,
    SharedNoteXref,
    SourceXref,
    SubmitterXref,
    Void,
)


class StructureSpecs(NamedTuple):
    tag: str
    key: str
    class_name: str


class Genealogy:
    """Methods to add, update and remove a specific loaded genealogy."""

    def __init__(
        self,
        name: str = '',
        filename: str = '',
        version: str = '7.0',
        calendar: str = String.GREGORIAN,
    ) -> None:
        self.chron_name: str = name
        self.version: str = version
        self.version_no_periods: str = self.version.replace(Default.PERIOD, Default.EMPTY)
        self.specs = importlib.import_module(f'genedata.specifications{self.version_no_periods}')
        self.classes = importlib.import_module(f'genedata.classes{self.version_no_periods}')
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
        self.ged_file: str = ''
        self.ged_file_records: list[str] = []
        self.records: list[Any] = []
            # self.classes.RecordFam
            # | self.classes.RecordIndi
            # | self.classes.RecordObje
            # | self.classes.RecordRepo
            # | self.classes.RecordSnote
            # | self.classes.RecordSour
            # | self.classes.RecordSubm
        #] = []
        self.record_header: Any = None #self.classes.Head | None = None
        self.schma: str = Default.EMPTY
        self.filename: str = filename
        self.filename_type: str = self._get_filename_type(self.filename)
        self.xref_counter: int = 1
        self.specification: dict[str, dict[str, Any]] = self.specs.Specs
        self.extension_specification: dict[str, dict[str, Any]] = {
            Default.YAML_TYPE_CALENDAR: {},
            Default.YAML_TYPE_DATATYPE: {},
            Default.YAML_TYPE_ENUMERATION_SET: {},
            Default.YAML_TYPE_ENUMERATION: {},
            Default.YAML_TYPE_MONTH: {},
            Default.YAML_TYPE_STRUCTURE: {},
            Default.YAML_TYPE_URI: {},
        }
        self.extension_xreflist: list[str] = [Void.NAME]
        self.family_xreflist: list[str] = [Void.NAME]
        self.individual_xreflist: list[str] = [Void.NAME]
        self.multimedia_xreflist: list[str] = [Void.NAME]
        self.repository_xreflist: list[str] = [Void.NAME]
        self.shared_note_xreflist: list[str] = [Void.NAME]
        self.source_xreflist: list[str] = [Void.NAME]
        self.submitter_xreflist: list[str] = [Void.NAME]
        self.record_dict: dict[str, dict[str, str]] = {
            # 'EXT': {
            #     'key': 'record-EXT',
            #     'type': 'extension',
            #     'class': 'RecordExt',
            #     'call': 'extension_xref',
            # },
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
        match self.filename_type:
            case '':
                self.chron: dict[str, str] = {
                    # Tag.NAME: name,
                    # Key.CAL: calendar,
                }
                # if log:
                #     logging.info(Msg.STARTED.format(self.chron_name))
            # case String.JSON:
            #     self.read_json()
            #     if log:
            #         logging.info(Msg.LOADED.format(self.chron_name, filename))
            case String.GED:
                self.load_ged(self.filename)
                # if log:
                #     logging.info(Msg.LOADED.format(self.chron_name, filename))
            # case String.CSV:
            #     self.read_csv()
            #     if log:
            #         logging.info(Msg.LOADED.format(self.chron_name, filename))
            case _:
                raise ValueError(Msg.UNRECOGNIZED.format(self.filename))

    # def __str__(self) -> str:
    #     return json.dumps(self.chron)

    def add_tag(self, tag: str, yaml_file: str) -> None:
        """Add an extension tag to the extension specifications.

        Run this on a specific yaml file to make the specification
        available when building the ged files.

        Args:
            tag: The extension tag with an initial underline and all capitals
                that must be in the `extension tags` list or which must be
                the `standard tag`.
            yaml_file: The location of the yaml_file as either a url or a file
                in a regular or compressed directory."""
        tag_edited: str = tag.upper()
        if tag_edited[0] != Default.UNDERLINE:
            tag_edited = ''.join([Default.UNDERLINE, tag_edited])

        yaml_dict: dict[str, Any] = Util.read_yaml(yaml_file)
        yaml_dict.update({Default.YAML_LOAD_FILE: yaml_file})
        yaml_dict.update({Default.YAML_LOAD_TAG: tag})
        type_key: str = str(yaml_dict[Default.YAML_TYPE])
        self.extension_specification[type_key].update({tag_edited: yaml_dict})

    def stage(
        self,
        record: Any,
        # Head
        # | RecordFam
        # | RecordIndi
        # | RecordObje
        # | RecordRepo
        # | RecordSnote
        # | RecordSour
        # | RecordSubm,
    ) -> None:
        if not isinstance(
            record,
            self.classes.Head
            | self.classes.RecordFam
            | self.classes.RecordIndi
            | self.classes.RecordObje
            | self.classes.RecordRepo
            | self.classes.RecordSnote
            | self.classes.RecordSour
            | self.classes.RecordSubm,
        ):
            raise ValueError(Msg.ONLY_RECORDS.format(str(record)))
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
            >>> g = Genealogy('minimal example')
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

        # Add in any SCHMA TAG values by replacing `0 HEAD` with complete header lines.
        lines = self.record_header.ged()
        if Default.HEADER not in lines:
            lines = self.record_header.ged().replace(
                Default.HEAD_LINE,
                f'{Default.HEADER}{self.version}{Default.EOL}{self.schma}',
            )

        # Construct the ged lines for each record.
        for record in self.records:
            lines = ''.join([lines, record.ged()])
        return ''.join([lines, Default.TRAILER])

    def save_ged(self, file_name: str = Default.EMPTY) -> None:
        """Save the ged file constructed by this instance of the Genealogy class."""
        Util.write_ged(self.show_ged(), file_name)

    def load_ged(self, file_name: str) -> None:
        """Load a ged file."""
        self.filename = file_name
        if self.ged_file != Default.EMPTY:
            raise ValueError(Msg.GED_FILE_ALREADY_LOADED)
        self.ged_file = Util.read(self.filename)

    def ged_to_code(self) -> str:
        """Convert the loaded ged file to code that produces the ged file."""

        def split_subs(ged: str, level: int = 0) -> list[str]:
            """Split a ged string on substructures at the specified level."""
            marker: str = f'{Default.EOL}{level}{Default.SPACE}'
            return ged.split(marker)

        def split_ged() -> None:
            """Validate the ged string then split it into records without the trailer."""

            # A trailer record `0 TRLR` must be in the file.
            if Default.TRAILER not in self.ged_file:
                raise ValueError(Msg.NO_TRAILER.format(Default.TRAILER))

            # A header record `0 HEAD` must be in the file.
            if Default.HEADER not in self.ged_file:
                raise ValueError(Msg.NO_HEADER.format(Default.HEADER))

            # Each line starts with a digit.
            if re.search('\n\\D', self.ged_file):
                raise ValueError(Msg.NOT_GED_STRINGS)

            # Remove the trailer along with everything after it.
            ged: str = Default.EMPTY
            ged, _, _ = self.ged_file.partition(Default.TRAILER)

            # Remove anything before the header record the end of line character.
            ged_temp: str = Default.EMPTY
            _, _, ged_temp = ged.partition(Default.HEADER)
            ged = ''.join([Default.HEADER, ged_temp])

            # Remove CONT tags.
            ged = re.sub('\n[0-9] CONT @', Default.EOL, ged)
            ged = re.sub('\n[0-9] CONT ', Default.EOL, ged)

            # Split the rest into a list of ged records.
            self.ged_file_records = split_subs(ged, 0)

        def header() -> str:
            header_subs: list[str] = split_subs(self.ged_file_records[0], 1)
            value_pieces: list[str] = header_subs[0].split(Default.SPACE, 2)
            lines: str = f"""
# Instantiate the header record.
header = {Default.CODE_CLASS}{Default.PERIOD}{Names.classname(value_pieces[1])}{Default.PARENS_LEFT}"""
            return ''.join(
                [
                    lines,
                    format_subs(
                        header_subs, value_pieces[1], 1, value=Default.EMPTY
                    ),
                ]
            )

        def end_subs(level: int = 0) -> str:
            if level == 0:
                return ''.join(
                    [
                        Default.BRACKET_RIGHT,
                        Default.PARENS_RIGHT,
                    ]
                )
            return ''.join(
                [
                    Default.INDENT * level,
                    Default.BRACKET_RIGHT,
                    Default.PARENS_RIGHT,
                    Default.COMMA,
                ]
            )

        def start_value(class_name: str, level: int = 0) -> str:
            return ''.join(
                [
                    Default.CODE_CLASS,
                    Default.PERIOD,
                    class_name,
                    Default.PARENS_LEFT,
                ]
            )

        def format_xref(xref: str) -> str:
            return xref.replace(Default.ATSIGN, Default.EMPTY).lower()

        def get_subs_specs(key: str) -> list[StructureSpecs]:
            """Associate the permitted substructure classes with the tags in the ged file."""
            subs: list[StructureSpecs] = []
            permitted_keys: list[str] = Query.permitted_keys(key, self.specs.Structure)
            for sub in permitted_keys:
                subs.append(
                    StructureSpecs(
                        tag=self.specs.Structure[sub][Default.YAML_STANDARD_TAG],
                        key=sub,
                        class_name=Names.classname(sub),
                    )
                )
            return subs

        def substructure(
            ged: str, level: int, class_name: str, key_name: str
        ) -> str:
            lines: str = Default.EMPTY
            ged_structures: list[str] = split_subs(ged, level)
            first_line_words: list[str] = ged_structures[0].split(
                Default.SPACE, 1
            )
            if len(first_line_words) > 1:
                value: str = format_value(key_name, first_line_words)
                return ''.join(
                    [
                        lines,
                        start_value(class_name, level),
                        value,
                        format_subs(
                            ged_structures, key_name, level, value=value
                        ),
                    ]
                )
            return ''.join(
                [
                    lines,
                    start_value(class_name, level),
                    format_subs(ged_structures[1:], key_name, level),
                ]
            )

        def format_value(key: str, words: list[str]) -> str:
            if len(words) == 1:
                return Default.EMPTY
            payload: str = self.specs.Structure[key][Default.YAML_PAYLOAD]
            match payload:
                case 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger':
                    return f'{words[1]}'
                case '@<https://gedcom.io/terms/v7/record-FAM>@':
                    return f'family_{format_xref(words[1])}_xref'
                case '@<https://gedcom.io/terms/v7/record-INDI>@':
                    return f'individual_{format_xref(words[1])}_xref'
                case '@<https://gedcom.io/terms/v7/record-OBJE>@':
                    return f'multimedia_{format_xref(words[1])}_xref'
                case '@<https://gedcom.io/terms/v7/record-REPO>@':
                    return f'repository_{format_xref(words[1])}_xref'
                case '@<https://gedcom.io/terms/v7/record-SNOTE>@':
                    return f'shared_note_{format_xref(words[1])}_xref'
                case '@<https://gedcom.io/terms/v7/record-SOUR>@':
                    return f'source_{format_xref(words[1])}_xref'
                case '@<https://gedcom.io/terms/v7/record-OBJE>@':
                    return f'submitter_{format_xref(words[1])}_xref'
            return Names.quote_text(words[1])

        def format_subs(
            ged: list[str],
            key_name: str,
            level: int = 0,
            value: str = Default.EMPTY,
        ) -> str:
            logging.info(
                f'format_subs: ged={ged}, key_name={key_name}, level={level}, value={value}'
            )
            permitted: list[StructureSpecs] = get_subs_specs(key_name)
            lines: str = Default.EMPTY
            if len(ged) > 1:
                if value != Default.EMPTY:
                    lines = ''.join(
                        [lines, ', ', Default.BRACKET_LEFT, Default.EOL]
                    )
                else:
                    lines = ''.join([lines, Default.BRACKET_LEFT, Default.EOL])
                for structure in ged:
                    tag: str = structure.split(Default.SPACE, 2)[0]
                    for good in permitted:
                        if tag == good.tag:
                            lines = ''.join(
                                [
                                    lines,
                                    Default.INDENT * level,
                                    substructure(
                                        structure,
                                        level + 1,
                                        good.class_name,
                                        good.key,
                                    ),
                                ]
                            )
                lines = ''.join(
                    [
                        lines,
                        end_subs(level - 1),
                        Default.EOL,
                    ]
                )
            else:
                lines = ''.join(
                    [lines, Default.PARENS_RIGHT, Default.COMMA, Default.EOL]
                )
            return lines

        def xref_name(xref: str) -> str:
            return xref.replace(Default.ATSIGN, Default.EMPTY)

        def imports() -> str:
            """Construct the section of the code where the imports are made."""
            return f"""# Import the required packages and classes.
from genedata.build import Genealogy
import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}

"""

        def initialize() -> str:
            """Construct the section of the code where the Genealogy class is instantiated."""
            return f"""# Instantiate a Genealogy class with the name of the ged file.
{Default.CODE_GENEALOGY} = Genealogy('{self.filename}')
"""

        def extensions() -> str:
            intro: str = """
# Add any extensions that were registered in the header record.
"""
            lines: str = Default.EMPTY
            split_lines: list[str] = self.ged_file_records[0].split(Default.EOL)
            for line in split_lines:
                if line[0:6] == '0 TAG ':
                    words: list[str] = line[6:].split(Default.SPACE, 1)
                    lines = ''.join(
                        [
                            lines,
                            Default.CODE_GENEALOGY,
                            Default.PERIOD,
                            Default.PARENS_LEFT,
                            words[0],
                            Default.COMMA,
                            Default.SPACE,
                            words[1],
                            Default.PARENS_RIGHT,
                            Default.EOL,
                        ]
                    )
            if lines != Default.EMPTY:
                lines = ''.join([intro, lines])
            return lines

        def xrefs() -> str:
            """Construct the section of the code where the cross reference identifiers are instantiated."""
            lines: str = """
# Instantiate the cross reference identifiers.
"""
            for record in self.ged_file_records:
                # Remove the first lines prior to the first substructure starting with 1.
                record_subs: list[str] = split_subs(record, 1)

                # Split the first two strings from the first split.
                line_words: list[str] = record_subs[0].split(Default.SPACE, 2)

                # Avoid the header record which still has a '0' string.
                if line_words[0] != '0':
                    name: str = xref_name(line_words[0])
                    tag: str = line_words[1].lower()
                    call: str = self.record_dict[line_words[1]]['call']
                    text: str = Default.EMPTY
                    if tag == Default.SNOTE_RECORD_TYPE:
                        text = Names.quote_text(line_words[2])
                        text = f', {text}'
                    lines = ''.join(
                        [
                            lines,
                            tag,
                            Default.UNDERLINE,
                            name,
                            Default.UNDERLINE,
                            Default.XREF,
                            Default.EQUAL,
                            Default.CODE_GENEALOGY,
                            Default.PERIOD,
                            call,
                            Default.PARENS_LEFT,
                            Default.QUOTE_SINGLE,
                            name,
                            Default.QUOTE_SINGLE,
                            text,
                            Default.PARENS_RIGHT,
                            Default.EOL,
                        ]
                    )
            return lines

        def records() -> str:
            lines: str = """
# Instantiate the records holding the GED data.
"""
            for record in self.ged_file_records:
                record_lines: list[str] = record.split(Default.EOL)
                record_subs: list[str] = split_subs(record, 1)
                line_words: list[str] = record_lines[0].split(Default.SPACE)
                if line_words[0] != '0':
                    record_name: str = xref_name(line_words[0])
                    tag: str = line_words[1]
                    record_key: str = self.record_dict[tag]['key']
                    record_class: str = self.record_dict[tag]['class']
                    record_type: str = self.record_dict[tag]['type']
                    lines = ''.join(
                        [
                            lines,
                            record_type,
                            Default.UNDERLINE,
                            record_name,
                            Default.EQUAL,
                            Default.CODE_CLASS,
                            Default.PERIOD,
                            record_class,
                            Default.PARENS_LEFT,
                            record_type,
                            Default.UNDERLINE,
                            record_name,
                            Default.UNDERLINE,
                            Default.XREF,
                            format_subs(record_subs, record_key, 1, value=' '),
                        ]
                    )
            return lines

        def stage() -> str:
            lines: str = f"""
# Stage the GEDCOM records to generate the ged lines.
{Default.CODE_GENEALOGY}.stage(header)
"""
            for record in self.ged_file_records:
                record_lines: list[str] = record.split(Default.EOL)
                line_words: list[str] = record_lines[0].split(Default.SPACE)
                if line_words[0] != '0':
                    name: str = xref_name(line_words[0])
                    tag: str = line_words[1].lower()
                    lines = ''.join(
                        [
                            lines,
                            Default.CODE_GENEALOGY,
                            Default.PERIOD,
                            Default.STAGE,
                            Default.PARENS_LEFT,
                            tag,
                            Default.UNDERLINE,
                            name,
                            Default.PARENS_RIGHT,
                            Default.EOL,
                        ]
                    )
            return lines

        split_ged()
        return ''.join(
            [
                imports(),
                initialize(),
                xrefs(),
                extensions(),
                header(),
                records(),
                stage(),
            ]
        )

    def _get_filename_type(self, filename: str) -> str:
        filename_type: str = ''
        # if filename[-Number.JSONLEN :] == String.JSON:
        #     filename_type = String.JSON
        if filename[-Number.GEDLEN :] == String.GED:
            filename_type = String.GED
        return filename_type

    # def read_ged(self) -> None:
    #     """Read and validate the GEDCOM file."""
    #     # try:
    #     with Path.open(
    #         Path(self.filename), encoding='utf-8', mode=String.READ
    #     ) as infile:
    #         data: Any = infile.readlines()
    #         self.ged_data.append(Tagger.clean_input(data))

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

    def families(self, records: list[Any]) -> None:
        """Collect and store all family records for the genealogy.

        Args:
            records: a list of all Family records.

        Examples:
            This is a minimal example illustrating the process.
            >>> from genedata.build import Genealogy
            >>> from genedata.classes70 import RecordFam
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

    def individuals(self, records: list[Any]) -> None:
        """Collect and store all individual records for the genealogy.

        Args:
            records: a list of all Individual records.

        Examples:
            This is a minimal example illustrating the process.
            >>> from genedata.build import Genealogy
            >>> from genedata.classes70 import RecordIndi
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

    def multimedia(self, records: list[Any]) -> None:
        """Collect and store all multimedia records for the genealogy.

        Args:
            records: a list of all Multimedia records.

        Examples:
            This is a minimal example illustrating the process.
            >>> from genedata.build import Genealogy
            >>> from genedata.classes70 import File, Form, RecordObje
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

    def repositories(self, records: list[Any]) -> None:
        """Collect and store all repository records for the genealogy.

        Args:
            records: a list of all Repository records.

        Examples:
            This is a minimal example illustrating the process.
            >>> from genedata.build import Genealogy
            >>> from genedata.classes70 import RecordRepo, Name
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

    def shared_notes(self, records: list[Any]) -> None:
        """Collect and store all shared note records for the genealogy.

        Args:
            records: a tuple of all SharedNote records.

        Examples:
            This is a minimal example illustrating the process.
            >>> from genedata.build import Genealogy
            >>> from genedata.classes70 import RecordSnote, Name
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

    def sources(self, records: list[Any]) -> None:
        """Collect and store all source records for the genealogy.

        Args:
            records: a list of all Source records.

        Examples:
            This is a minimal example illustrating the process.
            >>> from genedata.build import Genealogy
            >>> from genedata.classes70 import RecordSour
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

    def submitters(self, records: list[Any]) -> None:
        """Collect and store all submitter records for the genealogy.

        Args:
            records: a list of all Submitter records.

        Examples:
            This is a minimal example illustrating the process.
            >>> from genedata.build import Genealogy
            >>> from genedata.classes70 import RecordSubm, Name
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

    # def header(self, ged_header: Head) -> None:
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
        >>> g = Genealogy('test')
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
