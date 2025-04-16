# mypy: disable-error-code="name-defined"
"""Load a version of the GEDCOM specifications into python dictionaries.

This is the first step to make a GEDCOM version available.  After the specifications
file is created and stored in a module named `specificationXX.py` where XX is the version
number, then one generates the classes and tests for those closes using the `generate` module.
"""

__all__ = ['LoadSpecs']


from pathlib import Path

from genedata.constants import Default
from genedata.messages import Msg
from genedata.methods import Names, Util


class LoadSpecs:
    """Read and store the GEDCOM specifications into dictionaries from yaml files."""

    @staticmethod
    def preamble(source: str, version: str) -> str:
        """Format the preamble for the specifications module.

        Args:
            source: The source of the yaml specification files.
            version: The version of the GEDCOM specification.
        """
        lines: str = f'''"""Store the GEDCOM verson {version} specifications in a dictionary format from yaml files.

This is a generated module. DO NOT MODIFY THIS MODULE MANUALLY.  

Changes should be made to the `{__class__.__name__}` class in the `{__name__}` module.

The specification was obtained from the [GEDCOM-registeries]({source})
made available under the Apache 2.0 license.

The names of the dictionaries are based on the directories in this registry.  Each yaml file
in the directory is read into the appropriate dictionary with the stem of the yaml file acting as the key
and the contents of the yaml file being its value.

One dictionary is available called `Specs`.  It contains the following subdictionaries.
- `meta` provides information about the source and version of the specifications.
- `calendar` corresponding to yaml files in the calendar directory.
- `data type` corresponding to yaml files in the data-type directory.
- `enumeration` corresponding to yaml files in the enumeration directory.
- `enumeration set` corresponding to yaml files in the enumeration-set directory.
- `month` corresponding to yaml files in the month directory.
- `structure` corresponding to yaml files in the structure/standard directory 
- `uri` corresponding to yaml files in the uri directory.

Documented extensions are added to this dictionary.

Reference:
    [GEDCOM-registeries]({source})
"""

__all__ = ['Specs']


from typing import Any

'''
        return lines

    @staticmethod
    def dictionary(
        url: str,
        base: str,
    ) -> str:
        """Convert an entire directory of yaml files into a dictionary.

        The yaml fields are found in various directories under one 
        common named directory.  This common directory is called `url`.
        The final part of the directory name is given by `base`.
        
        Args:
            url: The main part of the uri. 
            base: The final part of the directory name.
        """
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
    def datatype_dictionary(url: str) -> str:
        """Retrive the data type dictionary as a string that can be sent to `eval`."""
        return LoadSpecs.dictionary(url, Default.URL_DATATYPE)

    @staticmethod
    def enumeration_dictionary(url: str) -> str:
        """Retrive the enumeration dictionary as a string that can be sent to `eval`."""
        return LoadSpecs.dictionary(url, Default.URL_ENUMERATION)

    @staticmethod
    def enumerationset_dictionary(url: str) -> str:
        """Retrive the enumeration set dictionary as a string that can be sent to `eval`."""
        return LoadSpecs.dictionary(url, Default.URL_ENUMERATION_SET)

    @staticmethod
    def month_dictionary(url: str) -> str:
        """Retrive the month dictionary as a string that can be sent to `eval`."""
        return LoadSpecs.dictionary(url, Default.URL_MONTH)

    @staticmethod
    def structure_dictionary(url: str) -> str:
        """Retrive the structure dictionary as a string that can be sent to `eval`."""
        return LoadSpecs.dictionary(url, Default.URL_STRUCTURE)

    @staticmethod
    def uri_dictionary(url: str) -> str:
        """Retrive the uri dictionary as a string that can be sent to `eval`."""
        return LoadSpecs.dictionary(url, Default.URL_URI)

    @staticmethod
    def together(source: str, version: str, url: str) -> str:
        """Return all dictionaries as strings.
        
        Args:
            source: The source of the yaml specification files.
            version: The version of the GEDCOM specification.
            url: The location of the local filesystem where the yaml files
                have been downloaded.
        """
        return ''.join(
            [
                'Specs: dict[str, dict[str, Any]] = {',
                Default.EOL,
                f"    '{Default.YAML_META}': ",
                '{',
                f"'{Default.YAML_SOURCE}': '{source}', '{Default.YAML_VERSION}': '{version}'",
                '},',
                Default.EOL,
                f"    '{Default.YAML_TYPE_CALENDAR}': {LoadSpecs.calendar_dictionary(url)},",
                Default.EOL,
                f"    '{Default.YAML_TYPE_DATATYPE}': {LoadSpecs.datatype_dictionary(url)},",
                Default.EOL,
                f"    '{Default.YAML_TYPE_ENUMERATION}': {LoadSpecs.enumeration_dictionary(url)},",
                Default.EOL,
                f"    '{Default.YAML_TYPE_ENUMERATION_SET}': {LoadSpecs.enumerationset_dictionary(url)},",
                Default.EOL,
                f"    '{Default.YAML_TYPE_MONTH}': {LoadSpecs.month_dictionary(url)},",
                Default.EOL,
                f"    '{Default.YAML_TYPE_STRUCTURE}': {LoadSpecs.structure_dictionary(url)},",
                Default.EOL,
                f"    '{Default.YAML_TYPE_URI}': {LoadSpecs.uri_dictionary(url)},",
                Default.EOL,
                '}',
                Default.EOL,
            ]
        )

    @staticmethod
    def build_all(source: str, version: str, url: str) -> str:
        """Generate the entire specifications module.

        This is the procedure to run from LoadSpecs.  It will output a string
        that when placed saved as a module named `specificationsXX.py` where XX
        is the version number: '70' for version '7.0'.
        
        Args:
            source: The source of the yaml specification files.
            version: The version of the GEDCOM specification.
            url: The location of the local filesystem where the yaml files
                have been downloaded.
        """
        return ''.join(
            [
                LoadSpecs.preamble(source, version),
                LoadSpecs.together(source, version, url),
            ]
        )
