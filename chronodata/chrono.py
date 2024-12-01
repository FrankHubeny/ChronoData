# Licensed under a 3-clause BSD style license - see LICENSE.md
"""Add, update and remove methods for a specific loaded chronology."""

import logging
from typing import Any

from chronodata.constants import (
    Calendar,
    Tag,
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
        super().__init__(name, filename, calendar)
        # self.chrono_name = name
        # self.filename = filename
        # self.calendar = calendar

    def _check_tag(
        self, tag: str, dictionary: dict[str, Any] | None = None
    ) -> None:
        if dictionary is None:
            dictionary = self.chron
        if tag not in dictionary:
            dictionary.update({tag: {}})

    def add_event(self, name: str, when: str) -> None:
        self._check_tag(Tag.EVENT)
        self.chron[Tag.EVENT].update({name: {Tag.DATE: when}})
        logging.info(Msg.ADD_EVENT.format(name, self.chron_name))
