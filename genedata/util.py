# util.py


import urllib.request
from typing import Any

import yaml  # type: ignore[import-untyped]

from genedata.constants import Default
from genedata.messages import Msg


class Util:
    """Utilities to read and write yaml or ged files."""
    @staticmethod
    def read(url: str) -> dict[str, Any]:
        """Read a yaml file and convert it into a dictionary.

        Args:
            url: The name of the file or the internet url.
        """

        # Read the internet file or a local file.
        if url[0:4] == 'http':
            webUrl = urllib.request.urlopen(url)
            result_code = str(webUrl.getcode())
            if result_code == '404':
                raise ValueError(Msg.PAGE_NOT_FOUND.format(url))
            raw: str = webUrl.read().decode(Default.UTF8)
        else:
            with open(url, 'rb') as file:  # noqa: PTH123
                binary_raw = file.read()
            raw = binary_raw.decode('utf-8')

        # Check that file has proper yaml directive.
        if Default.YAML_DIRECTIVE not in raw:
            raise ValueError(
                Msg.YAML_NOT_YAML_FILE.format(url, Default.YAML_DIRECTIVE)
            )

        # Return the dictionary.
        yaml_data = raw
        yaml_dict: dict[str, Any] = yaml.safe_load(yaml_data)
        return yaml_dict