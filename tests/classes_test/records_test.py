# records.py
# head_gedc_gedcvers_test
"""Tests to cover the records structures.

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
def test_good_run_obje() -> None:
    """Run a successful use of the structure."""
    g = Genealogy('test')
    obje = g.multimedia_xref('a')
    h = gc.RecordObje(obje, gc.File('test.text', gc.Form('text/plain')))
    assert h.validate()

def test_good_run_repo() -> None:
    """Run a successful use of the structure."""
    g = Genealogy('test')
    repo = g.repository_xref('a')
    h = gc.RecordRepo(repo, gc.Name('test.text'))
    assert h.validate()

def test_good_run_sour() -> None:
    """Run a successful use of the structure."""
    g = Genealogy('test')
    sour = g.source_xref('a')
    h = gc.RecordSour(sour)
    assert h.validate()

def test_good_run_subm() -> None:
    """Run a successful use of the structure."""
    g = Genealogy('test')
    subm = g.submitter_xref('a')
    h = gc.RecordSubm(subm, gc.Name('this'))
    assert h.validate()

#    b. Catch not permitted substructure.


def test_not_permitted_obje() -> None:
    """Check that a substructure not in the permitted list cannot be used by the structure."""
    g = Genealogy('test')
    obje = g.multimedia_xref('a')
    m = gc.RecordObje(obje, [gc.File('test.text', gc.Form('text/plain')),gc.Phrase('test')])
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_PERMITTED.format('Phrase', m.permitted, m.class_name)
        ),
    ):
        m.validate()

def test_not_permitted_subm() -> None:
    """Check that a substructure not in the permitted list cannot be used by the structure."""
    g = Genealogy('test')
    subm = g.submitter_xref('a')
    m = gc.RecordSubm(subm, [gc.Name('this'),gc.Phrase('test')])
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_PERMITTED.format('Phrase', m.permitted, m.class_name)
        ),
    ):
        m.validate()

def test_not_permitted_sour() -> None:
    """Check that a substructure not in the permitted list cannot be used by the structure."""
    g = Genealogy('test')
    sour = g.source_xref('a')
    m = gc.RecordSour(sour, gc.Phrase('test'))
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_PERMITTED.format('Phrase', m.permitted, m.class_name)
        ),
    ):
        m.validate()

def test_not_permitted_repo() -> None:
    """Check that a substructure not in the permitted list cannot be used by the structure."""
    g = Genealogy('test')
    repo = g.repository_xref('a')
    m = gc.RecordRepo(repo, [gc.Phrase('test'), gc.Name('this')])
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_PERMITTED.format('Phrase', m.permitted, m.class_name)
        ),
    ):
        m.validate()


#    d. Catch more than one when only one permitted.

