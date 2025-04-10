# queries_test.py
"""Tests to cover the Query class.

"""

import pytest

from genedata.methods import Query
from genedata.specifications70 import Structure


def test_required() -> None:
    """Verify that the required methods runs."""
    key: str = 'LATI'
    assert Query.required(key, Structure) == []

def test_required_empty() -> None:
    """Verify that the empty key raises an error."""
    key: str = ''
    with pytest.raises(KeyError, match=('')):
        Query.required(key, Structure)

def test_required_bad_key() -> None:
    """Verify that a bad key raises an error."""
    key: str = 'abc'
    with pytest.raises(KeyError, match=('abc')):
        Query.required(key, Structure)

def test_required_good_key() -> None:
    """Verify that the required methods runs."""
    key: str = 'MAP'
    assert Query.required(key, Structure) == ['Lati', 'Long']

def test_permitted_keys() -> None:
    """Verify that the required methods runs."""
    key: str = 'LATI'
    assert Query.permitted_keys(key, Structure) == []

def test_permitted_keys_empty() -> None:
    """Verify that the empty key raises an error."""
    key: str = ''
    with pytest.raises(KeyError, match=('')):
        Query.permitted_keys(key, Structure)

def test_permitted_keys_bad_key() -> None:
    """Verify that a bad key raises an error."""
    key: str = 'abc'
    with pytest.raises(KeyError, match=('abc')):
        Query.permitted_keys(key, Structure)

def test_permitted_keys_good_key() -> None:
    """Verify that the required methods runs."""
    key: str = 'MAP'
    assert Query.permitted_keys(key, Structure) == ['LATI', 'LONG']

def test_permitted() -> None:
    """Verify that the required methods runs."""
    key: str = 'LATI'
    assert Query.permitted(key, Structure) == []

def test_permitted_empty() -> None:
    """Verify that the empty key raises an error."""
    key: str = ''
    with pytest.raises(KeyError, match=('')):
        Query.permitted(key, Structure)

def test_permitted_bad_key() -> None:
    """Verify that a bad key raises an error."""
    key: str = 'abc'
    with pytest.raises(KeyError, match=('abc')):
        Query.permitted(key, Structure)

def test_permitted_good_key() -> None:
    """Verify that the required methods runs."""
    key: str = 'MAP'
    assert Query.permitted(key, Structure) == ['Lati', 'Long']

def test_classes_with_tag() -> None:
    """Verify that the required methods runs."""
    key: str = 'LATI'
    assert Query.classes_with_tag(key, Structure) == ['Lati']

def test_classes_with_tag_empty() -> None:
    """Verify that the empty key raises an error."""
    key: str = ''
    assert Query.classes_with_tag(key, Structure) == []

def test_classes_with_tag_bad_key() -> None:
    """Verify that a bad key raises an error."""
    key: str = 'abc'
    assert Query.classes_with_tag(key, Structure) == []

def test_classes_with_tag_good_key() -> None:
    """Verify that the required methods runs."""
    key: str = 'MAP'
    assert Query.classes_with_tag(key, Structure) == ['Map']

def test_singular() -> None:
    """Verify that the required methods runs."""
    key: str = 'LATI'
    assert Query.singular(key, Structure) == []

def test_singular_empty() -> None:
    """Verify that the empty key raises an error."""
    key: str = ''
    with pytest.raises(KeyError, match=('')):
        Query.singular(key, Structure)

def test_singular_bad_key() -> None:
    """Verify that a bad key raises an error."""
    key: str = 'abc'
    with pytest.raises(KeyError, match=('abc')):
        Query.singular(key, Structure)

def test_singular_good_key() -> None:
    """Verify that the required methods runs."""
    key: str = 'MAP'
    assert Query.singular(key, Structure) == ['Lati', 'Long']
