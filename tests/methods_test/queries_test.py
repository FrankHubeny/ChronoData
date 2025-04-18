# queries_test.py
"""Tests to cover the Query class.

"""

from genedata.methods import Query
from genedata.specifications70 import Specs


def test_required() -> None:
    """Verify that the required methods runs."""
    key: str = 'LATI'
    assert Query.required(key, Specs) == []

def test_required_empty() -> None:
    """Verify that the empty key raises an error."""
    key: str = ''
    assert Query.required(key, Specs) == []

def test_required_bad_key() -> None:
    """Verify that a bad key raises an error."""
    key: str = 'abc'
    assert Query.required(key, Specs) == []

def test_required_good_key() -> None:
    """Verify that the required methods runs."""
    key: str = 'MAP'
    assert Query.required(key, Specs) == ['Lati', 'Long']

def test_permitted_keys() -> None:
    """Verify that the required methods runs."""
    key: str = 'LATI'
    assert Query.permitted_keys(key, Specs) == []

def test_permitted_keys_empty() -> None:
    """Verify that the empty key raises an error."""
    key: str = ''
    assert Query.permitted_keys(key, Specs) == []

def test_permitted_keys_bad_key() -> None:
    """Verify that a bad key raises an error."""
    key: str = 'abc'
    assert Query.permitted_keys(key, Specs) == []

def test_permitted_keys_good_key() -> None:
    """Verify that the required methods runs."""
    key: str = 'MAP'
    assert Query.permitted_keys(key, Specs) == ['LATI', 'LONG']

def test_permitted() -> None:
    """Verify that the required methods runs."""
    key: str = 'LATI'
    assert Query.permitted(key, Specs) == []

def test_permitted_empty() -> None:
    """Verify that the empty key raises an error."""
    key: str = ''
    assert Query.permitted(key, Specs) == []

def test_permitted_bad_key() -> None:
    """Verify that a bad key raises an error."""
    key: str = 'abc'
    assert Query.permitted(key, Specs) == []

def test_permitted_good_key() -> None:
    """Verify that the required methods runs."""
    key: str = 'MAP'
    assert Query.permitted(key, Specs) == ['Lati', 'Long']

def test_classes_with_tag() -> None:
    """Verify that the required methods runs."""
    key: str = 'LATI'
    assert Query.classes_with_tag(key, Specs) == ['Lati']

def test_classes_with_tag_empty() -> None:
    """Verify that the empty key raises an error."""
    key: str = ''
    assert Query.classes_with_tag(key, Specs) == []

def test_classes_with_tag_bad_key() -> None:
    """Verify that a bad key raises an error."""
    key: str = 'abc'
    assert Query.classes_with_tag(key, Specs) == []

def test_classes_with_tag_good_key() -> None:
    """Verify that the required methods runs."""
    key: str = 'MAP'
    assert Query.classes_with_tag(key, Specs) == ['Map']

def test_singular() -> None:
    """Verify that the required methods runs."""
    key: str = 'LATI'
    assert Query.singular(key, Specs) == []

def test_singular_empty() -> None:
    """Verify that the empty key raises an error."""
    key: str = ''
    assert Query.singular(key, Specs) == []

def test_singular_bad_key() -> None:
    """Verify that a bad key raises an error."""
    key: str = 'abc'
    assert Query.singular(key, Specs) == []

def test_singular_good_key() -> None:
    """Verify that the required methods runs."""
    key: str = 'MAP'
    assert Query.singular(key, Specs) == ['Lati', 'Long']
