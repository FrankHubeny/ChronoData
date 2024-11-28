# Licensed under a 3-clause BSD style license - see LICENSE.md
"""Methods to compare a set of chronologies with savable challenges."""

import json
import logging
from pathlib import Path
from typing import Any

from chronodata.constants import (
    Arg,
    Column,
    Key,
    Line,
    String,
    Tag,
    Value,
)
from chronodata.core import Base
from chronodata.messages import Msg


class Challenge:
    """Load a set of chronologies, construct challenges, view and save."""

    def __init__(
        self,
        name: str = Value.EMPTY,
        filename: str = Value.EMPTY,
        chronos: list[str] | None = None,
    ):
        if chronos is None:
            chronos = []
        self.name = name
        self.filename = filename
        self.chronos = chronos
        self.chronologies = []
        self.challenge: dict[str, dict[str, Any]] = {
            Tag.NAME : self.name,
            Tag.CHRONOS : self.chronos,
            Tag.CHALLENGE : {},
        }
        if self.name == Value.EMPTY and self.filename == Value.EMPTY:
            logging(Msg.NAME_OR_FILENAME)
        elif self.filename != Value.EMPTY:
            with Path.open(Path(self.filename), Arg.READ) as file:
                self.challenge = json.load(file)
                file.close()
            for i in self.chronos:
                self.chronologies.append(Base(filename=i))
            logging(Msg.CHALLENGE_LOADED.format(self.name, self.chronos))
        else:
            for i in self.chronos:
                self.chronologies.append(Base(filename=i).chron)
            logging(Msg.CHALLENGE_BEGIN.format(self.name, self.chronos))

    def add_age_challenge(self, item: str, age: str):
        """Add items with ages that conflict with some chronologies.
        """
        self.challenge[Tag.CHALLENGE].update({item : age})
