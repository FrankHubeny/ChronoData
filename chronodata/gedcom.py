# GEDCOM constants

__all__ = [
    'Specs',
]

from dataclasses import dataclass


@dataclass(frozen=True)
class Specs:
    MAP: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#MAP'
    PLACE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PLACE_STRUCTURE'
    DATE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#date'
    