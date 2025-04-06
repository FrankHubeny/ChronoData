# famcstat_test.py
"""Tests to cover the FamcStat and Phrase substructure.

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

# 1. Validate: Exercise all validation checks.
#     a. Good run.


def test_good_run_using_list() -> None:
    """Run a successful use of the structure with list using lower case."""
    m = gc.FamcStat('proven', [gc.Phrase('proven')])
    assert m.validate()


def test_good_run_using_single_substructure() -> None:
    """Run a successful use of the structure."""
    m = gc.FamcStat('PROVEN', gc.Phrase('proven'))
    assert m.validate()


def test_good_run_no_subs() -> None:
    """Run a successful use of the structure."""
    m = gc.FamcStat('Proven')
    assert m.validate()


#     b. Catch not permitted substructure.


def test_not_permitted() -> None:
    """Check that a substructure not in the permitted list cannot be used by the structure."""
    m = gc.FamcStat('PROVEN', [gc.Phrase('proven'), gc.Lati('N30.0')])
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
    m = gc.FamcStat('PROVEN', [gc.Phrase('proven'), gc.Phrase('friend2')])
    with pytest.raises(
        ValueError, match=Msg.ONLY_ONE_PERMITTED.format('Phrase', m.class_name)
    ):
        m.validate()


#     e. Catch bad input.


def test_bad_enum() -> None:
    """Check that the wrong enumeration is caught."""
    m = gc.FamcStat('%$@')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_VALID_ENUM.format('%$@', m.enum_tags, m.class_name)
        ),
    ):
        m.validate()


# 2. Ged: Exercise the generation of ged data.


def test_ged() -> None:
    """Illustrate the standard use of the class."""
    m = gc.FamcStat('Proven', gc.Phrase('proven'))
    assert m.ged(1) == '1 STAT PROVEN\n2 PHRASE proven\n'


def test_ged_with_list() -> None:
    """Illustrate the standard use of the class."""
    m = gc.FamcStat('Proven', [gc.Phrase('proven')])
    assert m.ged(1) == '1 STAT PROVEN\n2 PHRASE proven\n'


# 3. Code: Exercise the code method.


def test_code() -> None:
    """Illustrate code running."""
    m = gc.FamcStat('PROven', gc.Phrase('proven'))
    assert m.code(as_name='gc') == "\ngc.FamcStat('PROVEN', gc.Phrase('proven'))"


def test_code_with_list() -> None:
    """Illustrate code running."""
    m = gc.FamcStat('PROVEN', [gc.Phrase('proven')])
    assert m.code(as_name='gc') == "\ngc.FamcStat('PROVEN',\n    [\n        gc.Phrase('proven'),\n    ]\n)"
