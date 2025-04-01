# classes_test.py
"""Test the functionality of the Classes class in the load module."""

from genedata.constants import Default
from genedata.examples import Examples7
from genedata.load import Classes
from genedata.specifications7 import Enumeration, EnumerationSet, Structure


def test_specification_retrieval() -> None:
    """Retrieve data from the `specification` method."""
    lookfor: str = """
    GEDCOM Specification:"""
    all_specs: str = Default.EMPTY
    all_specs = Classes.specification(Structure['MAP'])
    assert all_specs[0:len(lookfor)] == lookfor


def test_substructures_retrieval() -> None:
    """Retrieve data from the `substructures` method."""
    lookfor: str = '\n\n    Substructures:'
    all_specs: str = Default.EMPTY
    all_specs = Classes.substructures(Structure['MAP'])
    assert all_specs[0:len(lookfor)] == lookfor

def test_substructures_retrieval_empty() -> None:
    """Retrieve data from the `substructures` method."""
    lookfor: str = Default.EMPTY
    all_specs: str = Default.EMPTY
    all_specs = Classes.substructures(Structure['LATI'])
    assert all_specs[0:len(lookfor)] == lookfor

def test_superstructures_retrieval() -> None:
    """Retrieve data from the `superstructures` method."""
    lookfor: str = '\n\n    Superstructures:'
    all_specs: str = Default.EMPTY
    all_specs = Classes.superstructures(Structure['LATI'])
    assert all_specs[0:len(lookfor)] == lookfor

def test_generate_superstructures_retrieval_empty() -> None:
    """Retrieve data from the `superstructures` method."""
    lookfor: str = Default.EMPTY
    all_specs: str = Default.EMPTY
    all_specs = Classes.superstructures(Structure['HEAD'])
    assert all_specs[0:len(lookfor)] == lookfor

def test_enumerations_retrieval_empty() -> None:
    """Retrieve data from the `enumerations` method."""
    lookfor: str = Default.EMPTY
    all_specs: str = Default.EMPTY
    all_specs = Classes.enumerations('LATI', Structure, EnumerationSet, Enumeration)
    assert all_specs[0:len(lookfor)] == lookfor

def test_enumerations_retrieval() -> None:
    """Retrieve data from the `enumerations` method."""
    lookfor: str = '\n\n    Enumeration Values:'
    all_specs: str = Default.EMPTY
    all_specs = Classes.enumerations('SEX', Structure, EnumerationSet, Enumeration)
    assert all_specs[0:len(lookfor)] == lookfor

def test_generate_value_of_retrieval() -> None:
    """Retrieve data from the `value_of` method."""
    lookfor: str = """

    Enumeration Value Of:"""
    all_specs: str = Default.EMPTY
    all_specs = Classes.value_of(Structure['ADOP'])
    assert all_specs[0:len(lookfor)] == lookfor

def test_value_of_retrieval_empty() -> None:
    """Retrieve data from the `value_of` method."""
    lookfor: str = Default.EMPTY
    all_specs: str = Default.EMPTY
    all_specs = Classes.value_of(Structure['LATI'])
    assert all_specs[0:len(lookfor)] == lookfor

def test_args_retrieval() -> None:
    """Retrieve data from the `args` method."""
    lookfor: str = """
        
    Args:"""
    all_specs: str = Default.EMPTY
    all_specs = Classes.arguments('LATI', Structure['LATI'])
    assert all_specs[0:len(lookfor)] == lookfor

def test_generate_references_retrieval() -> None:
    """Retrieve data from the `references` method."""
    lookfor: str = '\n\n    References:'
    all_specs: str = Default.EMPTY
    all_specs = Classes.references(Structure['LATI'])
    assert all_specs[0:len(lookfor)] == lookfor

def test_generate_class_retrieval() -> None:
    """Retrieve data from the `generate_class` method."""
    lookfor: str = """

class"""
    all_specs: str = Default.EMPTY
    all_specs = Classes.generate_class('LATI', Structure, EnumerationSet, Enumeration, Examples7['LATI'])
    assert all_specs[0:len(lookfor)] == lookfor

def test_build_all_retrieval() -> None:
    """Retrieve data from the build_all method."""
    #lookfor: str = "'''This module of classes"
    all_specs: str = Default.EMPTY
    all_specs = Classes.build_all('GED', '7.0', Structure, EnumerationSet, Enumeration, Examples7)
    assert len(all_specs) > 0
