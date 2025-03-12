# nametype_test.py
"""Tests to cover the NameType and Phrase substructure.

1. Validate: Exercise all validation checks.
    a. Good run.
    b. Catch not permitted substructure.
    c. Catch not included but required substructures.
       No structures are required for NameType.
    d. Catch more than one when only one permitted.
    e. Catch bad input.

2. Ged: Exercise the generation of ged data.

3. Code: Exercise the code method.
"""

import re

import pytest

from genedata.messages import Msg
from genedata.structure import Lati, NameType, Phrase

# 1. Validate: Exercise all validation checks.
#     a. Good run.

def test_good_run_using_list() -> None:
    """Run a successful use of the structure."""
    m = NameType('AKA', [Phrase('also known as')])
    assert m.validate()


def test_good_run_using_single_substructure() -> None:
    """Run a successful use of the structure."""
    m = NameType('AKA', Phrase('also known as'))
    assert m.validate()


def test_good_run_no_subs() -> None:
    """Run a successful use of the structure."""
    m = NameType('AKA')
    assert m.validate()


#     b. Catch not permitted substructure.


def test_not_permitted() -> None:
    """Check that a substructure not in the permitted list cannot be used by the structure."""
    m = NameType('BIRTH', [Phrase('birth name'), Lati('N30.0')])
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_PERMITTED.format('Lati', m.permitted, m.class_name)
        ),
    ):
        m.validate()


#     c. Catch not included but required substructures.
#        No structures are required for NameType.

#     d. Catch more than one when only one permitted.


def test_phrase_only_one() -> None:
    """Check that the Phrase substructure can be used only once by NameType."""
    m = NameType(
        'MAIDEN', [Phrase('first maiden name'), Phrase('another maiden name')]
    )
    with pytest.raises(
        ValueError, match=Msg.ONLY_ONE_PERMITTED.format('Phrase', m.class_name)
    ):
        m.validate()


#     e. Catch bad input.


def test_medi_bad_enum() -> None:
    """Check that the wrong enumeration is caught."""
    m = NameType('abc')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_VALID_ENUM.format('abc', m.enums, m.class_name)
        ),
    ):
        m.validate()


# 2. Ged: Exercise the generation of ged data.


def test_ged() -> None:
    """Illustrate the standard use of the class."""
    m = NameType('BIRTH', Phrase('birth name'))
    assert m.ged(1) == '1 TYPE BIRTH\n2 PHRASE birth name\n'


def test_ged_with_list() -> None:
    """Illustrate the standard use of the class."""
    m = NameType('BIRTH', [Phrase('birth name')])
    assert m.ged(1) == '1 TYPE BIRTH\n2 PHRASE birth name\n'


# 3. Code: Exercise the code method.


def test_code() -> None:
    """Illustrate code running."""
    m = NameType('BIRTH', Phrase('birth name'))
    assert m.code() == "\nNameType('BIRTH', Phrase('birth name'))"


def test_code_with_list() -> None:
    """Illustrate code running."""
    m = NameType('BIRTH', [Phrase('birth name')])
    assert m.code() == "\nNameType('BIRTH', Phrase('birth name'))"
