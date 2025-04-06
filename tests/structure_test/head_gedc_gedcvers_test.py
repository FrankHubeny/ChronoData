# head_gedc_gedcvers_test
"""Tests to cover the Head, Gedc and GedcVers structures.

1. Validate: Exercise all validation checks.
    a. Good run.
    b. Catch not permitted substructure.
    c. Catch not included but required substructures.
    d. Catch more than one when only one permitted.
    e. Catch bad input.

2. Ged: Exercise the generation of ged data.

3. Code: Exercise the code method.
"""

import re

import pytest

import genedata.classes70 as gc
from genedata.messages import Msg


# 1. Validate Section
#    a. Good run.
def test_good_run() -> None:
    """Run a successful use of the structure."""
    h = gc.Head([gc.Gedc(gc.GedcVers('7.0')), gc.HeadPlac(gc.HeadPlacForm('City, County, State, Country'))])
    assert h.validate()

#    b. Catch not permitted substructure.


def test_not_permitted_head() -> None:
    """Check that a substructure not in the permitted list cannot be used by the structure."""
    m = gc.Head([gc.Phrase('test'), gc.Gedc(gc.GedcVers('7.0'))])
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_PERMITTED.format('Phrase', m.permitted, m.class_name)
        ),
    ):
        m.validate()

# def test_not_permitted_gedc() -> None:
#     """Check that a substructure not in the permitted list cannot be used by the structure."""
#     m = gc.Head(gc.Gedc([gc.Phrase('test'), gc.GedcVers('7.0')]))
#     with pytest.raises(
#         ValueError,
#         match=re.escape(
#             Msg.NOT_PERMITTED.format('Phrase', m.permitted, m.class_name)
#         ),
#     ):
#         m.validate()

# def test_not_permitted_gedcvers() -> None:
#     """Check that a substructure not in the permitted list cannot be used by the structure."""
#     m = gc.Head(gc.Gedc(gc.GedcVers('7.0', gc.Phrase('test'))))
#     with pytest.raises(
#         ValueError,
#         match=re.escape(
#             Msg.NO_SUBS.format('Phrase', m.permitted, m.class_name)
#         ),
#     ):
#         m.validate()


#    d. Catch more than one when only one permitted.

