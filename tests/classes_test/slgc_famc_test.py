# slgc_famc_test.py
"""Tests to cover the Slgc and Famc structures.

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

import genedata.classes7 as gc
from genedata.build import Genealogy
from genedata.messages import Msg


# 1. Validate Section
#    a. Good run.
def test_good_run() -> None:
    """Run a successful use of the structure."""
    g = Genealogy('test')
    fam = g.family_xref('a')
    h = gc.Slgc(gc.Famc(fam))
    assert h.validate()

#    b. Catch not permitted substructure.


def test_not_permitted_head() -> None:
    """Check that a substructure not in the permitted list cannot be used by the structure."""
    g = Genealogy('test')
    fam = g.family_xref('a')
    m = gc.Slgc([gc.Famc(fam), gc.Phrase('test')])
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_PERMITTED.format('Phrase', m.permitted, m.class_name)
        ),
    ):
        m.validate()

