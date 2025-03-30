# load.py
"""Load a version of the GEDCOM specifications into python dictionaries, 
generate classes from the loaded specifications and generate test modules for those classes.

"""

__all__ = [
    'Construct',
    'Convert',
    'Examples',
    'Tests',
]

from pathlib import Path
from textwrap import wrap
from typing import Any

from genedata.constants import Config, Default
from genedata.messages import Msg
from genedata.methods import Util

