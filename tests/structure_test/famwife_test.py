# famwife_test.py
"""Tests to cover the FamWife and Phrase substructure.

1. Validate: Exercise all validation checks.
    a. Good run.
    b. Catch not permitted substructure.
    c. Catch not included but required substructures.
       No structures are required for this structure.
    d. Catch more than one when only one permitted.
    e. Catch bad input.

2. Ged: Exercise the generation of ged data.

3. Code: Exercise the code method.
"""

import re

import pytest

from genedata.messages import Msg
from genedata.structure import FamilyXref, FamWife, IndividualXref, Lati, Phrase

# 1. Validate: Exercise all validation checks.
#     a. Good run.

indi = IndividualXref('@1@')
fam = FamilyXref('@2@')


def test_good_run_using_list() -> None:
    """Run a successful use of the structure with list using lower case."""
    m = FamWife(indi, [Phrase('indi')])
    assert m.validate()


def test_good_run_using_single_substructure() -> None:
    """Run a successful use of the structure."""
    m = FamWife(indi, Phrase('indi'))
    assert m.validate()


def test_good_run_no_subs() -> None:
    """Run a successful use of the structure."""
    m = FamWife(indi)
    assert m.validate()


#     b. Catch not permitted substructure.


def test_not_permitted() -> None:
    """Check that a substructure not in the permitted list cannot be used by the structure."""
    m = FamWife(indi, [Phrase('indi'), Lati('N30.0')])
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
    """Check that the Phrase substructure can be used only once by Role."""
    m = FamWife(indi, [Phrase('indi'), Phrase('friend2')])
    with pytest.raises(
        ValueError, match=Msg.ONLY_ONE_PERMITTED.format('Phrase', m.class_name)
    ):
        m.validate()


#     e. Catch bad input.


def test_bad_xref() -> None:
    """Check that the wrong cross reference identifier is caught."""
    m = FamWife('indi')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_INDIVIDUAL_XREF.format(str(m.value), m.class_name)
        ),
    ):
        m.validate()

def test_bad_other_xref() -> None:
    """Check that the wrong cross reference identifier is caught."""
    m = FamWife(fam)
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_INDIVIDUAL_XREF.format(str(m.value), m.class_name)
        ),
    ):
        m.validate()


# 2. Ged: Exercise the generation of ged data.


def test_ged() -> None:
    """Illustrate the standard use of the class."""
    m = FamWife(indi, Phrase('proven'))
    assert m.ged(1) == '1 WIFE @1@\n2 PHRASE proven\n'


def test_ged_with_list() -> None:
    """Illustrate the standard use of the class."""
    m = FamWife(indi, [Phrase('proven')])
    assert m.ged(1) == '1 WIFE @1@\n2 PHRASE proven\n'


def test_ged_no_sub() -> None:
    """Illustrate the standard use of the class."""
    m = FamWife(indi)
    assert m.ged(1) == '1 WIFE @1@\n'



# 3. Code: Exercise the code method.


def test_code() -> None:
    """Illustrate code running."""
    m = FamWife(indi, Phrase('proven'))
    assert m.code() == "\nFamWife(IndividualXref('@1@'), Phrase('proven'))"


def test_code_with_list() -> None:
    """Illustrate code running."""
    m = FamWife(indi, [Phrase('proven')])
    assert m.code() == "\nFamWife(IndividualXref('@1@'), Phrase('proven'))"


def test_code_no_sub() -> None:
    """Illustrate code running."""
    m = FamWife(indi)
    assert m.code() == "\nFamWife(IndividualXref('@1@'))"
