# Licensed under a 3-clause BSD style license - see LICENSE.md
"""The module provides utilities to read, validate and write GEDCOM files.

It includes constants representing the GEDCOM tags and methods to convert
a chron dictionary to and from GEDCOM.
"""

# from datetime import datetime
from pathlib import Path

# from typing import OpenTextMode  # , TypeAlias, NewType
import pandas as pd

from chronodata.chronology import Chronology
from chronodata.constants import Arg, Column, Tag

__all__ = ['Ged']
__author__ = 'Frank Hubeny'





class Ged:
    """Read, validate, fix and write a GEDCOM file.

    The `read` method will read a file attempting to
    validate it as a GEDCOM 7.0 file.

    If the validation succeeds a ChronoData chronology
    will be returned.

    If the validation fails, a report will be displayed
    showing issues with the file.  If the issues could be
    resolved by the `read` method a ChronoData chronology
    will be returned.  Otherwise an error message will
    be returned saying that the file could not be read.

    - The `write` method takes a chronology and writes
    a GEDCOM 7.0 file based on it.  If the user only wants
    to convert a file from an old version of GEDCOM to
    version 7.0, the user can now write the new file.

    """

    def __init__(self, name: str):
        self.name: str = name
        self.data: list[str] = []
        self.splitdata: list[list[tuple]] = []
        self.issues: list[list[int, str]] = []
        self.chron: Chronology = Chronology('newname')

    def __str__(self) -> str:
        return self.name

    

    def read(self) -> pd.DataFrame | Chronology:
        """Read and validate the GEDCOM file."""
        with Path.open(Path(self.name), 'r') as file:
            self.data = file.readlines()
            file.close()
        # Split each line into components and remove terminator.
        for i in self.data:
            self.splitdata.append(i.replace('\n', '').split(' '))
        # Check the level for bad increments and starting point.
        level: int = 0
        for index, value in enumerate(self.splitdata, start=1):
            if index == 1 and value[0] != '0':
                self.add_issue(index, Issue.NO_ZERO)
            elif int(value[0]) > level + 1:
                self.add_issue(index, Issue.BAD_INC)
            elif int(value[0]) < 0:
                self.add_issue(index, Issue.LESS_ZERO)
            else:
                level = int(value[0])
        # Report the validation results.
        if len(self.issues) > 0:
            return pd.DataFrame(
                data=self.issues, columns=[Column.LINE, Column.ISSUE]
            )
        return self.chron

    def write(self, name: str):
        mode: str = Arg.WRITE
        with Path.open(Path(name), mode) as file:
            file.write(Line.HEAD)
            file.write(Line.SUBM)
            file.write(Line.TAIL)
            file.close()
