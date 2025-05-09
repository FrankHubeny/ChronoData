# classes_test.py
"""Test the functionality of the Classes class in the load module."""

from genedata.constants import Default
from genedata.examples70 import Examples
from genedata.generate import Classes
from genedata.specifications70 import Specs


def test_specification_retrieval() -> None:
    """Retrieve data from the `specification` method."""
    lookfor: str = """
    GEDCOM Specification:"""
    all_specs: str = Default.EMPTY
    all_specs = Classes.specification('MAP', Specs)
    assert all_specs[0 : len(lookfor)] == lookfor


def test_substructures_retrieval() -> None:
    """Retrieve data from the `substructures` method."""
    lookfor: str = '\n\n    Substructures:'
    all_specs: str = Default.EMPTY
    all_specs = Classes.substructures('MAP', Specs)
    assert all_specs[0 : len(lookfor)] == lookfor


def test_substructures_retrieval_empty() -> None:
    """Retrieve data from the `substructures` method."""
    lookfor: str = Default.EMPTY
    all_specs: str = Default.EMPTY
    all_specs = Classes.substructures(
        'LATI', Specs
    )
    assert all_specs[0 : len(lookfor)] == lookfor


def test_superstructures_retrieval() -> None:
    """Retrieve data from the `superstructures` method."""
    lookfor: str = '\n\n    Superstructures:'
    all_specs: str = Default.EMPTY
    all_specs = Classes.superstructures(
        'LATI', Specs
    )
    assert all_specs[0 : len(lookfor)] == lookfor


def test_generate_superstructures_retrieval_empty() -> None:
    """Retrieve data from the `superstructures` method."""
    lookfor: str = Default.EMPTY
    all_specs: str = Default.EMPTY
    all_specs = Classes.superstructures(
        'HEAD', Specs
    )
    assert all_specs[0 : len(lookfor)] == lookfor


def test_enumerations_retrieval_empty() -> None:
    """Retrieve data from the `enumerations` method."""
    lookfor: str = Default.EMPTY
    all_specs: str = Default.EMPTY
    all_specs = Classes.enumerations(
        'LATI',
        Specs,
    )
    assert all_specs[0 : len(lookfor)] == lookfor


def test_enumerations_retrieval() -> None:
    """Retrieve data from the `enumerations` method."""
    lookfor: str = '\n\n    Enumeration Values:'
    all_specs: str = Default.EMPTY
    all_specs = Classes.enumerations(
        'SEX',
        Specs,
    )
    assert all_specs[0 : len(lookfor)] == lookfor


def test_generate_value_of_retrieval() -> None:
    """Retrieve data from the `value_of` method."""
    lookfor: str = """

    Enumeration Value Of:"""
    all_specs: str = Default.EMPTY
    all_specs = Classes.value_of('ADOP', Specs)
    assert all_specs[0 : len(lookfor)] == lookfor


def test_value_of_retrieval_empty() -> None:
    """Retrieve data from the `value_of` method."""
    lookfor: str = Default.EMPTY
    all_specs: str = Default.EMPTY
    all_specs = Classes.value_of('LATI', Specs)
    assert all_specs[0 : len(lookfor)] == lookfor


def test_args_retrieval() -> None:
    """Retrieve data from the `args` method."""
    lookfor: str = """
        
    Args:"""
    all_specs: str = Default.EMPTY
    all_specs = Classes.arguments(
        'LATI', Specs
    )
    assert all_specs[0 : len(lookfor)] == lookfor


def test_generate_references_retrieval() -> None:
    """Retrieve data from the `references` method."""
    lookfor: str = '\n\n    References:'
    all_specs: str = Default.EMPTY
    all_specs = Classes.references('LATI', Specs)
    assert all_specs[0 : len(lookfor)] == lookfor


def test_generate_class_retrieval() -> None:
    """Retrieve data from the `generate_class` method."""
    lookfor: str = """

class"""
    all_specs: str = Default.EMPTY
    all_specs = Classes.generate_class(
        'LATI',
        Specs,
        Examples['LATI'],
    )
    assert all_specs[0 : len(lookfor)] == lookfor


def test_build_all_retrieval() -> None:
    """Retrieve data from the build_all method."""
    # lookfor: str = "'''This module of classes"
    all_specs: str = Default.EMPTY
    all_specs = Classes.build_all(Specs)
    assert len(all_specs) > 0


def test_all_listing_with_empty_dictionary() -> None:
    """Retrieve the empty set if the dictionary is empty."""
    # lookfor: str = "'''This module of classes"
    all_list: str = Default.EMPTY
    all_list = Classes.all_listing({})
    assert len(all_list) == 0
