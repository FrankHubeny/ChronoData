# ged_to_code_maximal_test.py
"""Tests for the ged_to_code method."""

import pytest

from genedata.build import Genealogy
from genedata.messages import Msg

maximal_file: str = 'tests/data/ged_examples/maximal70.ged'


def test_ged_to_code_maximal() -> None:
    g = Genealogy(maximal_file)
    with pytest.raises(
        ValueError,
        match=Msg.NOT_DOCUMENTED_TAG.format('_SKYPEID'),
    ):
        g.ged_to_code()
