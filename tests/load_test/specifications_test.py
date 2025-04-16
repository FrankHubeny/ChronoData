"""Test the functionality of the LoadSpecs class in the load module."""

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
    """Retrieve calendar dictionary."""
    calendar: dict[str, dict[str, Any]] = eval(
        LoadSpecs.calendar_dictionary(directory)
    )
    assert (
        calendar['cal-GREGORIAN'][Default.YAML_TYPE]
        == Default.YAML_TYPE_CALENDAR
    )


def test_datatype_retrieval() -> None:
    """Retrieve the data type dictionary."""
    datatype: dict[str, dict[str, Any]] = eval(
        LoadSpecs.datatype_dictionary(directory)
    )
    assert datatype['type-Age'][Default.YAML_TYPE] == Default.YAML_TYPE_DATATYPE


def test_enumeration_retrieval() -> None:
    """Retrieve the enumeration dictionary."""
    enumeration: dict[str, dict[str, Any]] = eval(
        LoadSpecs.enumeration_dictionary(directory)
    )
    assert (
        enumeration['enum-0'][Default.YAML_TYPE]
        == Default.YAML_TYPE_ENUMERATION
    )


def test_enumerationset_retrieval() -> None:
    """Retrieve the enumeration set dictionary."""
    enumerationset: dict[str, dict[str, Any]] = eval(
        LoadSpecs.enumerationset_dictionary(directory)
    )
    assert (
        enumerationset['enumset-ADOP'][Default.YAML_TYPE]
        == Default.YAML_TYPE_ENUMERATION_SET
    )


def test_month_retrieval() -> None:
    """Retrieve the month dictionary."""
    month: dict[str, dict[str, Any]] = eval(
        LoadSpecs.month_dictionary(directory)
    )
    assert month['month-AAV'][Default.YAML_TYPE] == Default.YAML_TYPE_MONTH


def test_structure_retrieval() -> None:
    """Retrieve the structure dictionary."""
    structure: dict[str, dict[str, Any]] = eval(
        LoadSpecs.structure_dictionary(directory)
    )
    assert structure['ABBR'][Default.YAML_TYPE] == Default.YAML_TYPE_STRUCTURE


def test_uri_retrieval() -> None:
    """Retrieve the uri dictionary."""
    uri: dict[str, dict[str, Any]] = eval(LoadSpecs.uri_dictionary(directory))
    assert uri['AFN'][Default.YAML_TYPE] == Default.YAML_TYPE_URI


def test_build_all_retrieval() -> None:
    """Retrieve the entire specifications module."""
    specs: str = LoadSpecs.build_all('GED', '7.0', directory)
    assert '__all__' in specs


def test_together_retrieval() -> None:
    """Retrive all of the dictionaries."""
    specs: str = LoadSpecs.together('GED', '7.0', directory)
    assert 'Specs: dict' in specs


def test_uri_dictionary_no_slash() -> None:
    """Retrieve the uri dictionary from directory with no final slash."""
    uri: dict[str, dict[str, Any]] = eval(
        LoadSpecs.uri_dictionary(directory_no_slash)
    )
    assert uri['AFN'][Default.YAML_LABEL] == 'Ancestral File Number'


def test_onlydir_uri() -> None:
    """Test that nothing should be returned if no yaml files are in the directory."""
    all_list: dict[str, dict[str, Any]] = eval(
        LoadSpecs.uri_dictionary(onlydir_directory)
    )
    assert all_list == {}


def test_empty_uri() -> None:
    """Test that nothing should be returned if the yaml directory cannot be found."""
    with pytest.raises(
        ValueError,
        match=Msg.DIRECTORY_NOT_FOUND.format(
            'tests/load_test/gedtest_empty/uri/exid-types/'
        ),
    ):
        all_list: dict[str, dict[str, Any]] = eval(  # noqa: F841
            LoadSpecs.uri_dictionary(empty_directory)
        )
