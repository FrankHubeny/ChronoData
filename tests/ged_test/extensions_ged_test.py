# extensions_ged_test.py
"""Construct the GEDCOM file """

from genedata.methods import Util

file = Util.read('tests/data/ged_examples/extension-modified.ged')

def test_extension_extensions_ged() -> None:

    ged_file = ''
    assert file == ged_file