# tests/counter.py
"""
Tests for the `_counter` method of the `build` module
=====================================================

This module contains tests for the _counter method verify the returned values are as expected.
"""

import pytest

from chronodata.build import Genealogy
from chronodata.messages import Msg
from chronodata.store import Void

testdata = [
    # TEST Initial counter value.
    ('oldxref', 1),
    # TEST Initial counter used.
    ('usedxref', '@1@'),
    ('newxref', 2),
    # TEST See if the initial values are in their correct xref lists.
    ('individual', '@1@'),
    ('family', '@2@'),
    ('multimedia', '@3@'),
    ('repository', '@4@'),
    ('shared_note', '@5@'),
    ('source', '@6@'),
    ('submitter', '@7@'),
    # TEST See that identifiers are correctly be named.
    ('name1', '@ADAM@'),
    ('name2', '@ADAMEVE@'),
    ('name3', '@ADAM__EVE@'),
    # TEST Use string for initial part of the identifier.
    ('initial1', '@M8@'),
]


@pytest.mark.description('Testing the _counter method of the build module.')
@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_counter(test_input: str, expected: str | int | bool) -> None:
    # SETUP Instantiate a Genealogy.
    a = Genealogy(name='testing')

    # TEST Initial counter value.
    oldxref = a.xref_counter  # noqa: F841

    # TEST Initial counter used.
    usedxref = a._counter(a.individual_xreflist)  # noqa: F841
    newxref = a.xref_counter  # noqa: F841

    # SETUP: Create xrefs for the other record types.
    x1 = a._counter(a.family_xreflist)  # noqa: F841
    x2 = a._counter(a.multimedia_xreflist)  # noqa: F841
    x3 = a._counter(a.repository_xreflist)  # noqa: F841
    x4 = a._counter(a.shared_note_xreflist)  # noqa: F841
    x5 = a._counter(a.source_xreflist)  # noqa: F841
    x6 = a._counter(a.submitter_xreflist)  # noqa: F841

    # TEST See if the initial values are in their correct xref lists.
    individual = a.individual_xreflist[1]  # noqa: F841
    family = a.family_xreflist[1]  # noqa: F841
    multimedia = a.multimedia_xreflist[1]  # noqa: F841
    repository = a.repository_xreflist[1]  # noqa: F841
    shared_note = a.shared_note_xreflist[1]  # noqa: F841
    source = a.source_xreflist[1]  # noqa: F841
    submitter = a.submitter_xreflist[1]  # noqa: F841

    # TEST See that identifiers are correctly named.
    name1 = a._counter(a.individual_xreflist, xref_name=' Adam   ')  # noqa: F841
    name2 = a._counter(a.family_xreflist, xref_name='AdamEve')  # noqa: F841
    name3 = a._counter(a.family_xreflist, xref_name=' Adam  Eve ')  # noqa: F841

    # TEST Use string for initial part of the identifier.
    initial1 = a._counter(a.multimedia_xreflist, xref_name='M', initial=True)  # noqa: F841

    assert eval(test_input) == expected


def test_use_empty_identifier() -> None:
    """Test that the empty identifier cannot be used."""
    a = Genealogy('test')
    with pytest.raises(ValueError, match=Msg.XREF_EXISTS.format(Void.NAME, 'VOID')):
        a._counter(a.individual_xreflist, 'VOID')


def test_reused_identifier() -> None:
    """Test that an identifier cannot be reused."""
    a = Genealogy('test')
    a._counter(a.individual_xreflist, ' joe ')
    with pytest.raises(
        ValueError, match=Msg.XREF_EXISTS.format('@JOE@', ' joe ')
    ):
        a._counter(a.individual_xreflist, ' joe ')
