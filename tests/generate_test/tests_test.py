# tests_test.py
"""Test the functionality of the Tests class in the prep module."""

from genedata.constants import Default
from genedata.generate import Tests
from genedata.specifications7 import EnumerationSet, Structure


# def test_no_subs_retrieval() -> None:
#     """Retrieve test data for the no subs Lati structure."""
#     lookfor: str = '\n\ndef test_no_subs_Lati() -> None:\n'
#     out: str = Default.EMPTY
#     out = Tests.no_subs_good_test('LATI', 'N10.1')
#     assert out[0 : len(lookfor)] == lookfor


# def test_no_subs_indi_retrieval() -> None:
#     """Retrieve test data for the no subs RecordIndi structure."""
#     lookfor: str = '\n\ndef test_no_subs_RecordIndi() -> None:\n'
#     out: str = Default.EMPTY
#     out = Tests.no_subs_good_test('record-INDI', '', 'individual')
#     assert out[0 : len(lookfor)] == lookfor


# def test_no_subs_fam_retrieval() -> None:
#     """Retrieve test data for the no subs RecordFam structure."""
#     lookfor: str = '\n\ndef test_no_subs_RecordFam() -> None:\n'
#     out: str = Default.EMPTY
#     out = Tests.no_subs_good_test('record-FAM', '', 'family')
#     assert out[0 : len(lookfor)] == lookfor


# def test_no_subs_snote_retrieval() -> None:
#     """Retrieve test data for the no subs RecordSnote structure."""
#     lookfor: str = '\n\ndef test_no_subs_RecordSnote() -> None:\n'
#     out: str = Default.EMPTY
#     out = Tests.no_subs_good_test('record-SNOTE', '', 'shared_note')
#     assert out[0 : len(lookfor)] == lookfor


# def test_one_sub_retrieval() -> None:
#     """Retrieve test data for the Adop structure."""
#     lookfor: str = '\n\ndef test_one_sub_Adop() -> None:\n'
#     out: str = Default.EMPTY
#     out = Tests.one_sub_good_test('ADOP', 'Y', 'Age')
#     assert out[0 : len(lookfor)] == lookfor


# def test_one_sub_xref_retrieval() -> None:
#     """Retrieve test data for the RecordRepo structure."""
#     lookfor: str = '\n\ndef test_one_sub_RecordRepo() -> None:'
#     out: str = Default.EMPTY
#     out = Tests.one_sub_good_test('record-REPO', '', 'Note', 'repository')
#     assert out[0 : len(lookfor)] == lookfor


# def test_no_subs_all() -> None:
#     """Retrieve test data for all no subs tests."""
#     lookfor: str = "'''The tests in this file "
#     out: str = Default.EMPTY
#     out = Tests.build_no_subs_good_tests(Structure, EnumerationSet)
#     assert out[0 : len(lookfor)] == lookfor


# def test_one_sub_all() -> None:
#     """Retrieve test data for all no subs tests."""
#     lookfor: str = "'''The tests in this file "
#     out: str = Default.EMPTY
#     out = Tests.build_one_sub_good_tests(Structure, EnumerationSet)
#     assert out[0 : len(lookfor)] == lookfor
