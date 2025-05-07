# ged_to_code_extension_record_test.py
"""Tests for the ged_to_code method."""

import pytest

from genedata.build import Genealogy
from genedata.messages import Msg

extension_record_file: str = 'tests/data/ged_examples/extension-record.ged'


def test_ged_to_code_extension_record() -> None:
    g = Genealogy(extension_record_file)
    with pytest.raises(ValueError, match=Msg.NOT_DOCUMENTED_TAG.format('_LOC')):
        g.ged_to_code()
