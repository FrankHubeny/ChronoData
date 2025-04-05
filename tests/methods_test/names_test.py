# names_test.py
"""Tests to cover the Names class.

"""

import logging

from genedata.constants import Default
from genedata.methods import Names
from genedata.specifications7 import Structure


def test_keyname_from_classname() -> None:
    """Check that class names can be converted to a valid Structure key."""
    good: int = 0
    bad: int = 0
    class_name: str = Default.EMPTY
    key_name: str = Default.EMPTY 
    for key in Structure:
        class_name = Names.classname(key)
        key_name = Names.key_from_classname(class_name, Structure)
        if key_name == key:
            good += 1
        else:
            bad += 1
            logging.info(f'"{key_name}" does not equal "{key}"')
    assert bad == 0