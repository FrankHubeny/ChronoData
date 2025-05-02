# ged_to_code_maximal_test.py
"""Tests for the ged_to_code method."""

from genedata.build import Genealogy

maximal_file: str = 'tests/data/ged_examples/maximal70.ged'

def test_ged_to_code_maximal() -> None:
    expected = """
"""
    g = Genealogy(maximal_file)
    code = g.ged_to_code()
    assert code == expected