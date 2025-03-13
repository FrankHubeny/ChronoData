# input_age_test.py
"""Test the age method in the Input class.

1. Check Input.age().
    a. Good run.
    b. Catch range errors.
"""

from genedata.structure import Input

# 1. Check Input.age().
#     a. Good run.


def test_input_age_just_year() -> None:
    """Check that a good value heading North is returned."""
    assert Input.age(10) == '> 10y'


def test_input_age_full() -> None:
    """Check that a good value heading North is returned."""
    assert Input.age(2.1, 1.1, 1.2, 1.5) == '> 2y 1m 1w 1d'


def test_input_age_less_than() -> None:
    """Check that a good value heading North is returned."""
    assert Input.age(2.1, 1.1, 1.2, 1.5, '<') == '< 2y 1m 1w 1d'


def test_input_empty_age() -> None:
    """Check that a good value heading North is returned."""
    assert Input.age() == ''


#     b. Catch range errors.
