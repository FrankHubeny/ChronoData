# extension_record_ged_test.py
"""Construct the GEDCOM file """

from genedata.methods import Util

file = Util.read('tests/data/ged_examples/extension-record.ged')

def test_extension_record_ged() -> None:
    ged_file = ''


    assert file == ged_file
