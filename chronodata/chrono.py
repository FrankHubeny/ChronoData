# Licensed under a 3-clause BSD style license - see LICENSE.md
"""Add, update and remove methods for a specific loaded chronology."""


import logging
from typing import Any

from chronodata.constants import (
    Arg,
    Calendar,
    Column,
    Issue,
    Key,
    Line,
    String,
    Tag,
    Unit,
    Value,
)
from chronodata.core import Base
from chronodata.messages import Msg


class Chronology(Base):
    """Methods to add, update and remove a specific loaded chronology."""

    def __init__(
        self,
        name: str = Value.EMPTY,
        filename: str = Value.EMPTY,
        calendar: dict[str, Any] = Calendar.GREGORIAN,
    ) -> None:
        super().__init__(name,filename,calendar)
        
    def add_event(self, name: str, when: str):
        self.chron[Tag.EVEN].update({name : when})