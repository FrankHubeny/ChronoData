# convert_test.py
"""Test the functionality of the Convert class in the prep module."""

from typing import Any

import pytest

from genedata.constants import Default
from genedata.messages import Msg
from genedata.prep import Convert

directory: str = 'tests/prep_test/gedtest/'
empty_directory: str = 'tests/prep_test/gedtest_empty/'
onlydir_directory: str = 'tests/prep_test/gedtest_onlydir/'

def test_calendar_retrieval() -> None:
    """Retrieve test data for the calendar specification."""
    lookfor: str = 'Calendar: dict'
    uri: str = Default.EMPTY
    uri = Convert.calendar(directory)
    assert uri[0:len(lookfor)] == lookfor

def test_datatype_retrieval() -> None:
    """Retrieve test data for the data type specification."""
    lookfor: str = 'DataType: dict'
    uri: str = Default.EMPTY
    uri = Convert.datatype(directory)
    assert uri[0:len(lookfor)] == lookfor

def test_enumeration_retrieval() -> None:
    """Retrieve test data for the enumeration specification."""
    lookfor: str = 'Enumeration: dict'
    uri: str = Default.EMPTY
    uri = Convert.enumeration(directory)
    assert uri[0:len(lookfor)] == lookfor

def test_enumerationset_retrieval() -> None:
    """Retrieve test data for the enumeration set specification."""
    lookfor: str = 'EnumerationSet: dict'
    uri: str = Default.EMPTY
    uri = Convert.enumerationset(directory)
    assert uri[0:len(lookfor)] == lookfor

def test_month_retrieval() -> None:
    """Retrieve test data for the month specification."""
    lookfor: str = 'Month: dict'
    uri: str = Default.EMPTY
    uri = Convert.month(directory)
    assert uri[0:len(lookfor)] == lookfor

def test_structure_retrieval() -> None:
    """Retrieve test data for the structure specification."""
    lookfor: str = 'Structure: dict'
    uri: str = Default.EMPTY
    uri = Convert.structure(directory)
    assert uri[0:len(lookfor)] == lookfor

def test_structure_extension_retrieval() -> None:
    """Retrieve test data for the structure extension specification."""
    lookfor: str = 'ExtensionStructure: dict'
    uri: str = Default.EMPTY
    uri = Convert.structure_extension(directory)
    assert uri[0:len(lookfor)] == lookfor

def test_uri_retrieval() -> None:
    """Retrieve test data for the uri specification."""
    lookfor: str = 'Uri: dict'
    uri: str = Default.EMPTY
    uri = Convert.uri(directory)
    assert uri[0:len(lookfor)] == lookfor

def test_build_all_retrieval() -> None:
    """Retrieve data from the build_all method."""
    lookfor: str = '"""Store the GEDCOM verson 7.0 specifications'
    all_specs: str = Default.EMPTY
    all_specs = Convert.build_all('GED', '7.0', directory)
    assert all_specs[0:len(lookfor)] == lookfor

def test_uri_dictionary() -> None:
    """Retrieve the uri dictionary."""
    uri: dict[str, dict[str, Any]] = eval(Convert.uri_dictionary(directory))
    assert uri['AFN']['label'] == 'Ancestral File Number'

def test_onlydir_uri() -> None:
    """Test that nothing should be returned if a yaml file is not in the directory."""
    all_list: str = Convert.uri_dictionary(onlydir_directory)
    assert all_list == '{}'

def test_empty_uri() -> None:
    """Test that nothing should be returned if yaml fir in the directory."""
    with pytest.raises(ValueError, match=Msg.DIRECTORY_NOT_FOUND.format('tests/prep_test/gedtest_empty/uri/exid-types/')):
        all_list: str = Convert.uri_dictionary(empty_directory)  # noqa: F841