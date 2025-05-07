# ged_to_code_extensions_test.py
"""Tests for the ged_to_code method."""

import pytest

from genedata.build import Genealogy
from genedata.messages import Msg

extensions_file: str = 'tests/data/ged_examples/extensions-modified.ged'

def test_ged_to_code_extensions() -> None:
    g = Genealogy(extensions_file)
    with pytest.raises(ValueError, match=Msg.NOT_DOCUMENTED_TAG.format('_EXT1')):
        g.ged_to_code()
    