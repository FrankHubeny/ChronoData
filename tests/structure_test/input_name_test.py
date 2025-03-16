# input_name_test.py
"""Test the name method in the Input class.

1. Check Input.name().
    a. Good run.
    b. Catch range errors.
"""

from genedata.util import Input

# 1. Check Input.name().
#     a. Good run.

def test_input_name() -> None:
    """Check that a name is formatted as expected."""
    assert Input.name('Steve Smith', 'Smith') == 'Steve /Smith/'

def test_input_name_with_spaces() -> None:
    """Check that a name is formatted even with abnormal use of spaces."""
    assert Input.name('    Steve    Smith   ', '   Smith ') == 'Steve /Smith/'

def test_input_name_with_linebreaks() -> None:
    """Check that a name is formatted even with abnormal use of linebreaks."""
    assert Input.name('\n    Steve\n\n\nSmith   \n', '\n Smith \n') == 'Steve /Smith/'

#     b. Catch range errors.