# mypy: disable-error-code="name-defined"
"""Load a version of the GEDCOM specifications into python dictionaries,
generate classes from the loaded specifications and generate test modules for those classes.

"""

__all__ = ['LoadSpecs']


from pathlib import Path

from genedata.constants import Default
from genedata.messages import Msg
from genedata.methods import Names, Util


class LoadSpecs:
    """Read and store GEDCOM specification."""

    # enumerationset_dict: ClassVar[dict[str, Any]] = {}

    @staticmethod
    def preamble(source: str, version: str) -> str:
        lines: str = f'''"""Store the GEDCOM verson {version} specifications in a dictionary format from yaml files.

This is a generated module. DO NOT MODIFY THIS MODULE MANUALLY.  

Changes should be made to the `{__class__.__name__}` class in the `{__name__}` module.

The specification was obtained from the [GEDCOM-registeries]({source})
made available under the Apache 2.0 license.

The names of the dictionaries are based on the directories in this registry.  Each yaml file
in the directory is read into the appropriate dictionary with the stem of the yaml file acting as the key
and the contents of the yaml file being its value.

The following dictionaries are available.  Each key in the dictionary corresponds to a
single yaml file.
- `Calendar` corresponding to yaml files in the calendar directory.
- `DataType` corresponding to yaml files in the data-type directory.
- `Enumeration` corresponding to yaml files in the enumeration directory.
- `EnumerationSet` corresponding to yaml files in the enumeration-set directory.
- `Month` corresponding to yaml files in the month directory.
- `Structure` corresponding to yaml files in the structure/standard directory.
- `ExtensionStructure` corresponding to yaml files in the structure/extenion directory.
- `Uri` corresponding to yaml files in the uri directory.

Reference:
    [GEDCOM-registeries]({source})
"""

__all__ = [
    '{Default.SPECS_CALENDAR}',
    '{Default.SPECS_DATATYPE}',
    '{Default.SPECS_ENUMERATION}',
    '{Default.SPECS_ENUMERATION_SET}',
    '{Default.SPECS_EXTENSIONSTRUCTURE}',
    '{Default.SPECS_MONTH}',
    'Specs',
    '{Default.SPECS_STRUCTURE}',
    '{Default.SPECS_URI}',
]

from typing import Any

'''
        return lines

    @staticmethod
    def dictionary(
        url: str,
        base: str,
    ) -> str:
        lines: str = Default.BRACE_LEFT
        directory: str = f'{Names.slash(url)}{base}'
        p = Path(directory)
        if p.exists():
            for file in p.iterdir():
                if file.suffix == Default.YAML_FILE_END:
                    yamldict = Util.read_yaml(str(file))
                    lines = (
                        f"{lines}{Default.EOL}    '{file.stem}': {yamldict},"
                    )
        else:
            raise ValueError(Msg.DIRECTORY_NOT_FOUND.format(directory))
        if lines == Default.BRACE_LEFT:
            return ''.join([lines, Default.BRACE_RIGHT])
        return ''.join([lines, Default.EOL, Default.BRACE_RIGHT])

    @staticmethod
    def calendar_dictionary(url: str) -> str:
        """Retrive the calendar dictionary as a string that can be sent to `eval`."""
        return LoadSpecs.dictionary(url, Default.URL_CALENDAR)

    @staticmethod
    def calendar(url: str) -> str:
        """Format the calendar dictionary for use in the specs module."""
        return ''.join(
            [
                f'{Default.SPECS_CALENDAR}: dict[str, dict[str, Any]] = ',
                LoadSpecs.calendar_dictionary(url),
                Default.EOL,
                Default.EOL,
            ]
        )

    @staticmethod
    def datatype_dictionary(url: str) -> str:
        """Retrive the data type dictionary as a string that can be sent to `eval`."""
        return LoadSpecs.dictionary(url, Default.URL_DATATYPE)

    @staticmethod
    def datatype(url: str) -> str:
        """Format the data type dictionary for use in the specs module."""
        return ''.join(
            [
                f'{Default.SPECS_DATATYPE}: dict[str, dict[str, Any]] = ',
                LoadSpecs.datatype_dictionary(url),
                Default.EOL,
                Default.EOL,
            ]
        )

    @staticmethod
    def enumeration_dictionary(url: str) -> str:
        """Retrive the enumeration dictionary as a string that can be sent to `eval`."""
        return LoadSpecs.dictionary(url, Default.URL_ENUMERATION)

    @staticmethod
    def enumeration(url: str) -> str:
        """Format the enumeration dictionary for use in the specs module."""
        return ''.join(
            [
                f'{Default.SPECS_ENUMERATION}: dict[str, dict[str, Any]] = ',
                LoadSpecs.enumeration_dictionary(url),
                Default.EOL,
                Default.EOL,
            ]
        )

    @staticmethod
    def enumerationset_dictionary(url: str) -> str:
        """Retrive the enumeration set dictionary as a string that can be sent to `eval`."""
        return LoadSpecs.dictionary(url, Default.URL_ENUMERATION_SET)

    @staticmethod
    def enumerationset(url: str) -> str:
        """Format the enumeration set dictionary for use in the specs module."""
        return ''.join(
            [
                f'{Default.SPECS_ENUMERATION_SET}: dict[str, dict[str, Any]] = ',
                LoadSpecs.enumerationset_dictionary(url),
                Default.EOL,
                Default.EOL,
            ]
        )

    @staticmethod
    def month_dictionary(url: str) -> str:
        """Retrive the month dictionary as a string that can be sent to `eval`."""
        return LoadSpecs.dictionary(url, Default.URL_MONTH)

    @staticmethod
    def month(url: str) -> str:
        """Format the month dictionary for use in the specs module."""
        return ''.join(
            [
                f'{Default.SPECS_MONTH}: dict[str, dict[str, Any]] = ',
                LoadSpecs.month_dictionary(url),
                Default.EOL,
                Default.EOL,
            ]
        )

    @staticmethod
    def structure_dictionary(url: str) -> str:
        """Retrive the structure dictionary as a string that can be sent to `eval`."""
        return LoadSpecs.dictionary(url, Default.URL_STRUCTURE)

    @staticmethod
    def structure(url: str) -> str:
        """Format the structure dictionary for use in the specs module."""
        return ''.join(
            [
                f'{Default.SPECS_STRUCTURE}: dict[str, dict[str, Any]] = ',
                LoadSpecs.structure_dictionary(url).replace(
                    "'payload': None,", "'payload': 'None',"
                ),
                Default.EOL,
                Default.EOL,
            ]
        )

    @staticmethod
    def structure_extension_dictionary(url: str) -> str:
        """Retrive the extension structure dictionary as a string that can be sent to `eval`."""
        return LoadSpecs.dictionary(
            url,
            Default.URL_STRUCTURE_EXTENSION,
        )

    @staticmethod
    def structure_extension(url: str) -> str:
        """Format the extension structure dictionary for use in the specs module."""
        return ''.join(
            [
                f'{Default.SPECS_EXTENSIONSTRUCTURE}: dict[str, dict[str, Any]] = ',
                LoadSpecs.structure_extension_dictionary(url),
                Default.EOL,
                Default.EOL,
            ]
        )

    @staticmethod
    def uri_dictionary(url: str) -> str:
        """Retrive the uri dictionary as a string that can be sent to `eval`."""
        return LoadSpecs.dictionary(url, Default.URL_URI)

    @staticmethod
    def uri(url: str) -> str:
        """Format the uri dictionary for use in the specs module."""
        return ''.join(
            [
                'Uri: dict[str, dict[str, Any]] = ',
                LoadSpecs.uri_dictionary(url),
                Default.EOL,
                Default.EOL,
            ]
        )

    @staticmethod
    def together() -> str:
        return ''.join(
            [
                'Specs: dict[str, dict[str, Any]] = {',
                Default.EOL,
                f"    '{Default.SPECS_CALENDAR}': {Default.SPECS_CALENDAR},",
                Default.EOL,
                f"    '{Default.SPECS_DATATYPE}': {Default.SPECS_DATATYPE},",
                Default.EOL,
                f"    '{Default.SPECS_ENUMERATION}': {Default.SPECS_ENUMERATION},",
                Default.EOL,
                f"    '{Default.SPECS_ENUMERATION_SET}': {Default.SPECS_ENUMERATION_SET},",
                Default.EOL,
                f"    '{Default.SPECS_EXTENSIONSTRUCTURE}': {Default.SPECS_EXTENSIONSTRUCTURE},",
                Default.EOL,
                f"    '{Default.SPECS_MONTH}': {Default.SPECS_MONTH},",
                Default.EOL,
                f"    '{Default.SPECS_STRUCTURE}': {Default.SPECS_STRUCTURE},",
                Default.EOL,
                f"    '{Default.SPECS_URI}': {Default.SPECS_URI},",
                Default.EOL,
                '}',
                Default.EOL,
            ]
        )

    @staticmethod
    def build_all(source: str, version: str, url: str) -> str:
        return ''.join(
            [
                LoadSpecs.preamble(source, version),
                LoadSpecs.calendar(url),
                LoadSpecs.datatype(url),
                LoadSpecs.enumeration(url),
                LoadSpecs.enumerationset(url),
                LoadSpecs.month(url),
                LoadSpecs.structure(url),
                LoadSpecs.structure_extension(url),
                LoadSpecs.uri(url),
                LoadSpecs.together(),
            ]
        )
