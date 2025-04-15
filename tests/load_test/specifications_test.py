# convert_test.py
"""Test the functionality of the Convert class in the prep module."""

from typing import Any

import pytest

from genedata.constants import Default
from genedata.load import LoadSpecs
from genedata.messages import Msg

directory: str = 'tests/load_test/gedtest/'
directory_no_slash: str = 'tests/load_test/gedtest'
empty_directory: str = 'tests/load_test/gedtest_empty/'
onlydir_directory: str = 'tests/load_test/gedtest_onlydir/'


def test_calendar_retrieval() -> None:
    """Retrieve test data for the calendar specification."""
    lookfor: str = 'calendar: dict'
    uri: str = Default.EMPTY
    uri = LoadSpecs.calendar(directory)
    assert uri[0 : len(lookfor)] == lookfor


def test_datatype_retrieval() -> None:
    """Retrieve test data for the data type specification."""
    lookfor: str = 'data type: dict'
    uri: str = Default.EMPTY
    uri = LoadSpecs.datatype(directory)
    assert uri[0 : len(lookfor)] == lookfor


def test_enumeration_retrieval() -> None:
    """Retrieve test data for the enumeration specification."""
    lookfor: str = 'enumeration: dict'
    uri: str = Default.EMPTY
    uri = LoadSpecs.enumeration(directory)
    assert uri[0 : len(lookfor)] == lookfor


def test_enumerationset_retrieval() -> None:
    """Retrieve test data for the enumeration set specification."""
    lookfor: str = 'enumeration set: dict'
    uri: str = Default.EMPTY
    uri = LoadSpecs.enumerationset(directory)
    assert uri[0 : len(lookfor)] == lookfor


def test_month_retrieval() -> None:
    """Retrieve test data for the month specification."""
    lookfor: str = 'month: dict'
    uri: str = Default.EMPTY
    uri = LoadSpecs.month(directory)
    assert uri[0 : len(lookfor)] == lookfor


def test_structure_retrieval() -> None:
    """Retrieve test data for the structure specification."""
    lookfor: str = 'structure: dict'
    uri: str = Default.EMPTY
    uri = LoadSpecs.structure(directory)
    assert uri[0 : len(lookfor)] == lookfor


def test_uri_retrieval() -> None:
    """Retrieve test data for the uri specification."""
    lookfor: str = 'uri: dict'
    uri: str = Default.EMPTY
    uri = LoadSpecs.uri(directory)
    assert uri[0 : len(lookfor)] == lookfor


def test_build_all_retrieval() -> None:
    """Retrieve data from the build_all method."""
    lookfor: str = '"""Store the GEDCOM verson 7.0 specifications'
    all_specs: str = Default.EMPTY
    all_specs = LoadSpecs.build_all('GED', '7.0', directory)
    assert all_specs[0 : len(lookfor)] == lookfor


def test_uri_dictionary() -> None:
    """Retrieve the uri dictionary."""
    uri: dict[str, dict[str, Any]] = eval(LoadSpecs.uri_dictionary(directory))
    assert uri['AFN']['label'] == 'Ancestral File Number'


def test_uri_dictionary_no_slash() -> None:
    """Retrieve the uri dictionary from directory with no final slash."""
    uri: dict[str, dict[str, Any]] = eval(
        LoadSpecs.uri_dictionary(directory_no_slash)
    )
    assert uri['AFN']['label'] == 'Ancestral File Number'


def test_onlydir_uri() -> None:
    """Test that nothing should be returned if a yaml file is not in the directory."""
    all_list: str = LoadSpecs.uri_dictionary(onlydir_directory)
    assert all_list == '{}'


def test_empty_uri() -> None:
    """Test that nothing should be returned if yaml fir in the directory."""
    with pytest.raises(
        ValueError,
        match=Msg.DIRECTORY_NOT_FOUND.format(
            'tests/load_test/gedtest_empty/uri/exid-types/'
        ),
    ):
        all_list: str = LoadSpecs.uri_dictionary(empty_directory)  # noqa: F841
