# queries_test.py
"""Tests to cover the Queries class.

"""

import pytest

from genedata.methods import Queries
from genedata.specifications70 import Structure


def test_required() -> None:
    """Verify that the required methods runs."""
    key: str = 'LATI'
    assert Queries.required(key, Structure) == []

def test_required_empty() -> None:
    """Verify that the empty key raises an error."""
    key: str = ''
    with pytest.raises(KeyError, match=('')):
        Queries.required(key, Structure)

def test_required_bad_key() -> None:
    """Verify that a bad key raises an error."""
    key: str = 'abc'
    with pytest.raises(KeyError, match=('abc')):
        Queries.required(key, Structure)

def test_required_good_key() -> None:
    """Verify that the required methods runs."""
    key: str = 'MAP'
    assert Queries.required(key, Structure) == ['Lati', 'Long']

def test_permitted_keys() -> None:
    """Verify that the required methods runs."""
    key: str = 'LATI'
    assert Queries.permitted_keys(key, Structure) == []

def test_permitted_keys_empty() -> None:
    """Verify that the empty key raises an error."""
    key: str = ''
    with pytest.raises(KeyError, match=('')):
        Queries.permitted_keys(key, Structure)

def test_permitted_keys_bad_key() -> None:
    """Verify that a bad key raises an error."""
    key: str = 'abc'
    with pytest.raises(KeyError, match=('abc')):
        Queries.permitted_keys(key, Structure)

def test_permitted_keys_good_key() -> None:
    """Verify that the required methods runs."""
    key: str = 'MAP'
    assert Queries.permitted_keys(key, Structure) == ['LATI', 'LONG']

def test_permitted() -> None:
    """Verify that the required methods runs."""
    key: str = 'LATI'
    assert Queries.permitted(key, Structure) == []

def test_permitted_empty() -> None:
    """Verify that the empty key raises an error."""
    key: str = ''
    with pytest.raises(KeyError, match=('')):
        Queries.permitted(key, Structure)

def test_permitted_bad_key() -> None:
    """Verify that a bad key raises an error."""
    key: str = 'abc'
    with pytest.raises(KeyError, match=('abc')):
        Queries.permitted(key, Structure)

def test_permitted_good_key() -> None:
    """Verify that the required methods runs."""
    key: str = 'MAP'
    assert Queries.permitted(key, Structure) == ['Lati', 'Long']

def test_classes_with_tag() -> None:
    """Verify that the required methods runs."""
    key: str = 'LATI'
    assert Queries.classes_with_tag(key, Structure) == ['Lati']

def test_classes_with_tag_empty() -> None:
    """Verify that the empty key raises an error."""
    key: str = ''
    assert Queries.classes_with_tag(key, Structure) == []

def test_classes_with_tag_bad_key() -> None:
    """Verify that a bad key raises an error."""
    key: str = 'abc'
    assert Queries.classes_with_tag(key, Structure) == []

def test_classes_with_tag_good_key() -> None:
    """Verify that the required methods runs."""
    key: str = 'MAP'
    assert Queries.classes_with_tag(key, Structure) == ['Map']

def test_singular() -> None:
    """Verify that the required methods runs."""
    key: str = 'LATI'
    assert Queries.singular(key, Structure) == []

def test_singular_empty() -> None:
    """Verify that the empty key raises an error."""
    key: str = ''
    with pytest.raises(KeyError, match=('')):
        Queries.singular(key, Structure)

def test_singular_bad_key() -> None:
    """Verify that a bad key raises an error."""
    key: str = 'abc'
    with pytest.raises(KeyError, match=('abc')):
        Queries.singular(key, Structure)

def test_singular_good_key() -> None:
    """Verify that the required methods runs."""
    key: str = 'MAP'
    assert Queries.singular(key, Structure) == ['Lati', 'Long']
