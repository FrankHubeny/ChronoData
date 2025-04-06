# tests_test.py
"""Test the functionality of the Tests class in the prep module."""

from genedata.constants import Default
from genedata.generate import Tests
from genedata.specifications70 import Enumeration, EnumerationSet, Structure


def test_all_retrieval() -> None:
    """Retrieve test data for the All test module."""
    lookfor: str = "'''This module contains All tests to be run with pytest."
    out: str = Default.EMPTY
    out = Tests.all(Structure, EnumerationSet, Enumeration)
    assert out[0 : len(lookfor)] == lookfor


def test_not_permitted_retrieval() -> None:
    """Retrieve test data for the Not Permitted test module."""
    lookfor: str = "'''This module contains Not Permitted tests to be run with pytest."
    out: str = Default.EMPTY
    out = Tests.not_permitted(Structure, EnumerationSet, Enumeration)
    assert out[0 : len(lookfor)] == lookfor


def test_bad_payload_retrieval() -> None:
    """Retrieve test data for the Bad Payload test module."""
    lookfor: str = '# mypy: disable-error-code="arg-type, unused-ignore"'
    out: str = Default.EMPTY
    out = Tests.bad_payload(Structure, EnumerationSet, Enumeration)
    assert out[0 : len(lookfor)] == lookfor


def test_bad_enum_retrieval() -> None:
    """Retrieve test data for the Bad Enum test module."""
    lookfor: str = "'''This module contains Bad Enum tests to be run with pytest."
    out: str = Default.EMPTY
    out = Tests.bad_enum(Structure, EnumerationSet, Enumeration)
    assert out[0 : len(lookfor)] == lookfor


def test_bad_singular_retrieval() -> None:
    """Retrieve test data for the Bad Singular test module."""
    lookfor: str = "'''This module contains Bad Singular tests to be run with pytest."
    out: str = Default.EMPTY
    out = Tests.bad_singular(Structure, EnumerationSet, Enumeration)
    assert out[0 : len(lookfor)] == lookfor


def test_missing_required_retrieval() -> None:
    """Retrieve test data for the Missing Required test module."""
    lookfor: str = "'''This module contains Missing Required tests to be run with pytest."
    out: str = Default.EMPTY
    out = Tests.missing_required(Structure, EnumerationSet, Enumeration)
    assert out[0 : len(lookfor)] == lookfor


def test_empty_subs_retrieval() -> None:
    """Retrieve test data for the Empty Subs test module."""
    lookfor: str = "'''This module contains Empty Subs tests to be run with pytest."
    out: str = Default.EMPTY
    out = Tests.empty_subs(Structure, EnumerationSet, Enumeration)
    assert out[0 : len(lookfor)] == lookfor


def test_empty_value_retrieval() -> None:
    """Retrieve test data for the Empty Value test module."""
    lookfor: str = "'''This module contains Empty Value tests to be run with pytest."
    out: str = Default.EMPTY
    out = Tests.empty_value(Structure, EnumerationSet, Enumeration)
    assert out[0 : len(lookfor)] == lookfor
