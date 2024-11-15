# Licensed under a 3-clause BSD style license - see LICENSE.md
"""The module provides utilities to read, validate and write GEDCOM files.

It includes constants representing the GEDCOM tags and methods to convert
a chron dictionary to and from GEDCOM.
"""

# from datetime import datetime
# from pathlib import Path
from typing import Literal, TypeAlias, NewType


Media: TypeAlias = Literal['a', 'b']
UserId = NewType('UserId', int)
type ConnectionOptions = dict[str, str]
type Address = tuple[str, int]
type Server = tuple[Address, ConnectionOptions]


class StdTag:
    """Constant definitions of standard tags:

    References
    --------
    [Specifications:\](https://github.com/FamilySearch/GEDCOM/blob/main/specification/gedcom-1-hierarchical-container-format.md)
    """

    AGE: str = 'AGE'
    ASSO: str = 'ASSO'
    BIRT: str = 'BIRT'
    CHIL: str = 'CHIL'
    CONT: str = 'CONT'
    DATE: str = 'DATE'
    FAM: str = 'FAM'
    FAMC: str = 'FAMC'
    GEDC: str = 'GEDC'
    HEAD: str = 'HEAD'
    HUSB: str = 'HUSB'
    INDI: str = 'INDI'
    MARR: str = 'MARR'
    NAME: str = 'NAME'
    NOTE: str = 'NOTE'
    PHRASE: str = 'PHRASE'
    PLAC: str = 'PLAC'
    RESN: str = 'RESN'
    ROLE: str = 'ROLE'
    SCHMA: str = 'SCHMA'
    TAG: str = 'TAG'
    TRLR: str = 'TRLR'
    WIFE: str = 'WIFE'


class ExtTag:
    """Constant definitions for extention tags."""

    _DATE: str = '_DATE'
    _LOC: str = '_LOC'
    _PARTNER: str = 'PARTNER'
    _POP: str = '_POP'
