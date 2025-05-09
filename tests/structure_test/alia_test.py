# alia_test.py
"""Tests to cover the Alia and Phrase substructure.

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

import genedata.classes70 as gc
from genedata.messages import Msg
from genedata.structure import FamilyXref, IndividualXref

# 1. Validate: Exercise all validation checks.
#     a. Good run.


def test_good_run_using_list() -> None:
    """Run a successful use of the structure with list using lower case."""
    indi = IndividualXref('@1@')
    m = gc.Alia(indi, [gc.Phrase('indi')])
    assert m.validate()


def test_good_run_using_single_substructure() -> None:
    """Run a successful use of the structure."""
    indi = IndividualXref('@1@')
    m = gc.Alia(indi, gc.Phrase('indi'))
    assert m.validate()


def test_good_run_no_subs() -> None:
    """Run a successful use of the structure."""
    indi = IndividualXref('@1@')
    m = gc.Alia(indi)
    assert m.validate()


#     b. Catch not permitted substructure.


def test_not_permitted() -> None:
    """Check that a substructure not in the permitted list cannot be used by the structure."""
    m = gc.Alia('HUSB', [gc.Phrase('indi'), gc.Lati('N30.0')])  # type: ignore[arg-type]
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
    indi = IndividualXref('@1@')
    m = gc.Alia(indi, [gc.Phrase('indi'), gc.Phrase('friend2')])
    with pytest.raises(
        ValueError, match=Msg.ONLY_ONE_PERMITTED.format('Phrase', m.class_name)
    ):
        m.validate()


#     e. Catch bad input.


def test_bad_xref() -> None:
    """Check that the wrong cross reference identifier is caught."""
    m = gc.Alia('indi')   # type: ignore[arg-type]
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_INDIVIDUAL_XREF.format(str(m.value), m.class_name)
        ),
    ):
        m.validate()


def test_bad_other_xref() -> None:
    """Check that the wrong cross reference identifier is caught."""
    fam = FamilyXref('@2@')
    m = gc.Alia(fam)  # type: ignore[arg-type]
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
    indi = IndividualXref('@1@')
    m = gc.Alia(indi, gc.Phrase('proven'))
    assert m.ged(1) == '1 ALIA @1@\n2 PHRASE proven\n'


def test_ged_with_list() -> None:
    """Illustrate the standard use of the class."""
    indi = IndividualXref('@1@')
    m = gc.Alia(indi, [gc.Phrase('proven')])
    assert m.ged(1) == '1 ALIA @1@\n2 PHRASE proven\n'


# 3. Code: Exercise the code method.


def test_code() -> None:
    """Illustrate code running."""
    m = gc.Alia(IndividualXref('@1@'), gc.Phrase('proven'))
    assert m.code(as_name='gc') == "\ngc.Alia(IndividualXref('@1@'), gc.Phrase('proven'))"


def test_code_with_list() -> None:
    """Illustrate code running."""
    m = gc.Alia(IndividualXref('@1@'), [gc.Phrase('proven')])
    assert m.code(as_name='gc') == "\ngc.Alia(IndividualXref('@1@'),\n    [\n        gc.Phrase('proven'),\n    ]\n)"
