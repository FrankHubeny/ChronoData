# ged_to_code_extensions_test.py
"""Tests for the ged_to_code method."""

from genedata.build import Genealogy

extensions_file: str = 'tests/data/ged_examples/extensions-modified.ged'

def test_ged_to_code_extensions() -> None:
    expected = """
"""

    g = Genealogy(extensions_file)
    code = g.ged_to_code()
    assert code == expected
    