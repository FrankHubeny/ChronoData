# split_ged_test.py
"""Test the split_ged method."""

import pytest

from genedata.build import Genealogy
from genedata.constants import Default
from genedata.messages import Msg

minimal_file: str = 'tests\\data\\ged_examples\\minimal70.ged'
obje_file: str = 'tests\\data\\ged_examples\\obje-1.ged'
minimal_archive: str = 'tests\\data\\ged_examples\\minimal70.gdz'
minimal_archive_file: str = 'gedcom.ged'
maximal_archive: str = 'tests\\data\\ged_examples\\maximal70.gdz'
maximal_archive_file: str = 'gedcom.ged'

def test_split_ged_minimal() -> None:
    g = Genealogy(minimal_file)
    g.split_ged()
    assert len(g.ged_file_records) == 1

def test_split_ged_maximal() -> None:
    g = Genealogy(obje_file)
    g.split_ged()
    assert len(g.ged_file_records) == 4


