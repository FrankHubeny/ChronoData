# medi_test.py
"""Tests to cover the Medi and Phrase substructure.

1. Validate: Exercise all validation checks.
    a. Good run.
    b. Catch not permitted substructure.
    c. Catch not included but required substructures.
       No structures are required for Medi.
    d. Catch more than one when only one permitted.
    e. Catch bad input.

2. Ged: Exercise the generation of ged data.

3. Code: Exercise the code method.
"""

import re

import pytest

import genedata.classes7 as gc
from genedata.messages import Msg


# 1. Validate: Exercise all validation checks.
#     a. Good run.
def test_good_run_using_list() -> None:
    """Run a successful use of the structure."""
    m = gc.Medi('BOOK', [gc.Phrase('A book')])
    assert m.validate()


def test_good_run_using_single_substructure() -> None:
    """Run a successful use of the structure."""
    m = gc.Medi('BOOK', gc.Phrase('A book'))
    assert m.validate()


def test_good_run_no_subs() -> None:
    """Run a successful use of the structure."""
    m = gc.Medi('BOOK')
    assert m.validate()


#     b. Catch not permitted substructure.


def test_not_permitted() -> None:
    """Check that a substructure not in the permitted list cannot be used by the structure."""
    m = gc.Medi('VIDEO', [gc.Phrase('A video'), gc.Lati('N30.0')])
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_PERMITTED.format('Lati', m.permitted, m.class_name)
        ),
    ):
        m.validate()


#     c. Catch not included but required substructures.
#        No structures are required for Medi.

#     d. Catch more than one when only one permitted.


def test_phrase_only_one() -> None:
    """Check that the Phrase substructure can be used only once by Medi."""
    m = gc.Medi('MAGAZINE', [gc.Phrase('a magazine'), gc.Phrase('another magazine')])
    with pytest.raises(
        ValueError, match=Msg.ONLY_ONE_PERMITTED.format('Phrase', m.class_name)
    ):
        m.validate()


#     e. Catch bad input.


def test_bad_enum() -> None:
    """Check that the wrong enumeration is caught."""
    m = gc.Medi('abc')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_VALID_ENUM.format('ABC', m.enum_tags, m.class_name)
        ),
    ):
        m.validate()


# 2. Ged: Exercise the generation of ged data.


def test_ged() -> None:
    """Illustrate the standard use of the class."""
    m = gc.Medi('BOOK', gc.Phrase('a book'))
    assert m.ged(1) == '1 MEDI BOOK\n2 PHRASE a book\n'


def test_ged_with_list() -> None:
    """Illustrate the standard use of the class."""
    m = gc.Medi('BOOK', [gc.Phrase('a book')])
    assert m.ged(1) == '1 MEDI BOOK\n2 PHRASE a book\n'


# 3. Code: Exercise the code method.


def test_code() -> None:
    """Illustrate code running."""
    m = gc.Medi('BOOK', gc.Phrase('a book'))
    assert m.code(as_name='gc') == "\ngc.Medi('BOOK', gc.Phrase('a book'))"


def test_code_with_list() -> None:
    """Illustrate code running."""
    m = gc.Medi('BOOK', [gc.Phrase('a book')])
    assert m.code(as_name='gc') == "\ngc.Medi('BOOK',\n    [\n        gc.Phrase('a book'),\n    ]\n)"
