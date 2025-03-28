# construct_test.py
"""Test the functionality of the Construct class in the prep module."""

from typing import Any

import pytest

from genedata.constants import Default
from genedata.messages import Msg
from genedata.prep import Construct, Convert

directory: str = 'tests/prep_test/gedtest/'
empty_directory: str = 'tests/prep_test/gedtest_empty/'
onlydir_directory: str = 'tests/prep_test/gedtest_onlydir/'
structure: dict[str, Any] = eval(Convert.structure_dictionary(directory))
enumeration: dict[str, Any] = eval(Convert.enumeration_dictionary(directory))


def test_generate_specification_retrieval() -> None:
    """Retrieve data from the `generate_specification` method."""
    lookfor: str = """
    GEDCOM Specification:"""
    all_specs: str = Default.EMPTY
    all_specs = Construct.generate_specification('MAP', structure)
    assert all_specs[0:len(lookfor)] == lookfor

def test_generate_examples_retrieval() -> None:
    """Retrieve data from the `generate_examples` method."""
    lookfor: str = """

    Examples:"""
    all_specs: str = Default.EMPTY
    all_specs = Construct.generate_examples('LATI')
    assert all_specs[0:len(lookfor)] == lookfor

def test_generate_examples_retrieval_empty() -> None:
    """Retrieve data from the `generate_examples` method."""
    lookfor: str = Default.EMPTY
    all_specs: str = Default.EMPTY
    all_specs = Construct.generate_examples('MAP')
    assert all_specs[0:len(lookfor)] == lookfor

def test_generate_substructures_retrieval() -> None:
    """Retrieve data from the `generate_substructures` method."""
    lookfor: str = '\n\n    Substructures:'
    all_specs: str = Default.EMPTY
    all_specs = Construct.generate_substructures('MAP', structure)
    assert all_specs[0:len(lookfor)] == lookfor

def test_generate_substructures_retrieval_empty() -> None:
    """Retrieve data from the `generate_substructures` method."""
    lookfor: str = Default.EMPTY
    all_specs: str = Default.EMPTY
    all_specs = Construct.generate_substructures('LATI', structure)
    assert all_specs[0:len(lookfor)] == lookfor

def test_generate_superstructures_retrieval() -> None:
    """Retrieve data from the `generate_superstructures` method."""
    lookfor: str = '\n\n    Superstructures:'
    all_specs: str = Default.EMPTY
    all_specs = Construct.generate_superstructures('LATI', structure)
    assert all_specs[0:len(lookfor)] == lookfor

def test_generate_superstructures_retrieval_empty() -> None:
    """Retrieve data from the `generate_superstructures` method."""
    lookfor: str = Default.EMPTY
    all_specs: str = Default.EMPTY
    all_specs = Construct.generate_superstructures('HEAD', structure)
    assert all_specs[0:len(lookfor)] == lookfor

def test_generate_enumerations_retrieval_empty() -> None:
    """Retrieve data from the `generate_enumerations` method."""
    lookfor: str = Default.EMPTY
    all_specs: str = Default.EMPTY
    all_specs = Construct.generate_enumerations('LATI', structure, enumeration)
    assert all_specs[0:len(lookfor)] == lookfor

def test_generate_enumerations_retrieval() -> None:
    """Retrieve data from the `generate_enumerations` method."""
    lookfor: str = '\n\n    Enumeration Values:'
    all_specs: str = Default.EMPTY
    all_specs = Construct.generate_enumerations('SEX', structure, enumeration)
    assert all_specs[0:len(lookfor)] == lookfor

def test_generate_value_of_retrieval() -> None:
    """Retrieve data from the `generate_value_of` method."""
    lookfor: str = """

    Enumeration Value Of:"""
    all_specs: str = Default.EMPTY
    all_specs = Construct.generate_value_of('ADOP', structure)
    assert all_specs[0:len(lookfor)] == lookfor

def test_generate_value_of_retrieval_empty() -> None:
    """Retrieve data from the `generate_value_of` method."""
    lookfor: str = Default.EMPTY
    all_specs: str = Default.EMPTY
    all_specs = Construct.generate_value_of('LATI', structure)
    assert all_specs[0:len(lookfor)] == lookfor

def test_generate_args_retrieval() -> None:
    """Retrieve data from the `generate_args` method."""
    lookfor: str = """
        
    Args:"""
    all_specs: str = Default.EMPTY
    all_specs = Construct.generate_args('LATI', structure)
    assert all_specs[0:len(lookfor)] == lookfor

def test_generate_references_retrieval() -> None:
    """Retrieve data from the `generate_references` method."""
    lookfor: str = '\n\n    References:'
    all_specs: str = Default.EMPTY
    all_specs = Construct.generate_references('LATI', structure)
    assert all_specs[0:len(lookfor)] == lookfor

def test_generate_class_retrieval() -> None:
    """Retrieve data from the `generate_class` method."""
    lookfor: str = """

class"""
    all_specs: str = Default.EMPTY
    all_specs = Construct.generate_class('LATI', directory, structure, enumeration)
    assert all_specs[0:len(lookfor)] == lookfor

def test_generate_class_retrieval_with_none() -> None:
    """Retrieve data from the `generate_class` method."""
    lookfor: str = """

class"""
    all_specs: str = Default.EMPTY
    all_specs = Construct.generate_class('LATI', directory, None, None)
    assert all_specs[0:len(lookfor)] == lookfor

def test_build_all_retrieval() -> None:
    """Retrieve data from the build_all method."""
    lookfor: str = "'''This module of classes"
    all_specs: str = Default.EMPTY
    all_specs = Construct.build_all('GED', '7.0', directory)
    assert all_specs[0:len(lookfor)] == lookfor

def test_onlydir_generate_all() -> None:
    """Test that nothing should be returned if yaml fir in the directory."""
    all_list: str = Construct.generate__all__(onlydir_directory)
    assert all_list == Default.EMPTY

def test_empty_generate_all() -> None:
    """Test that nothing should be returned if yaml fir in the directory."""
    with pytest.raises(ValueError, match=Msg.DIRECTORY_NOT_FOUND.format('tests/prep_test/gedtest_empty/structure/standard/')):
        all_list: str = Construct.generate__all__(empty_directory)  # noqa: F841
    