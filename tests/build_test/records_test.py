"""------------------------------------------------------------------------------
                            Defs Class Tests

    These tests cover the seven classes created for the identifiers
    of the seven GEDCOM records.  These types were defined in the
    `records` module.

    They also cover the assignment of strings as those types.
    These assignments occurred in the `chrono` module.

    To perform some tests methods from the `methods` module were used.

------------------------------------------------------------------------------"""

# from typing import Any

import pytest

from genedata.build import Genealogy
from genedata.classes70 import Gedc, GedcVers, Head, RecordIndi
from genedata.messages import Msg
from genedata.structure import (
    FamilyXref,
    IndividualXref,
    MultimediaXref,
    RepositoryXref,
    SharedNoteXref,
    SourceXref,
    SubmitterXref,
)

testdata_individual = [
    ('indi_type', True),
    ('indi_name', '1'),
    ('indi_fullname', '@1@'),
    ('indi_string', '@1@'),
    ('indi_named_name', 'INDIVIDUAL'),
    ('indi_named_fullname', '@INDIVIDUAL@'),
    ('indi_named_string', '@INDIVIDUAL@'),
    ('indi_spaces_name', 'NAME WITH SPACES'),
    ('indi_spaces_fullname', '@NAME_WITH_SPACES@'),
    ('indi_spaces_string', '@NAME_WITH_SPACES@'),
    ('indi_ged0', '0 @1@ INDI\n'),
]


@pytest.mark.parametrize('test_input,expected', testdata_individual)  # noqa: PT006
def test_individual(test_input: str, expected: str | int | bool) -> None:
    a = Genealogy(version='7.0')

    # Test creation of the IndividualXref type without names.
    individual = a.individual_xref()
    indi_type = isinstance(individual, IndividualXref)  # noqa: F841
    indi_name = individual.name  # noqa: F841
    indi_fullname = individual.fullname  # noqa: F841
    indi_string = str(individual)  # noqa: F841
    indi_ged0 = individual.ged()  # noqa: F841
    #indi_ged1 = individual.ged(1)  
    #indi_ged1_info = individual.ged(1, 'info')  

    # Test creation of IndividualXref type with a name.
    indi_named = a.individual_xref('individual')
    indi_named_name = indi_named.name  # noqa: F841
    indi_named_fullname = indi_named.fullname  # noqa: F841
    indi_named_string = str(indi_named)  # noqa: F841

    # Test creation of IndividualXref type with spaces.
    indi_spaces = a.individual_xref('name with spaces')
    indi_spaces_name = indi_spaces.name  # noqa: F841
    indi_spaces_fullname = indi_spaces.fullname  # noqa: F841
    indi_spaces_string = str(indi_spaces)  # noqa: F841

    assert eval(test_input) == expected


def test_individual_dup() -> None:
    """Test whether a duplicate record can be created."""
    xref_name = 'hello individual'
    a = Genealogy(version='7.0')
    name1 = a.individual_xref(xref_name)
    with pytest.raises(ValueError, match=Msg.XREF_EXISTS.format(name1.fullname, xref_name)):
        name2 = a.individual_xref(xref_name)  # noqa: F841


testdata_family = [
    ('family_type', True),
    ('family_name', 'A FAMILY'),
    ('family_fullname', '@A_FAMILY@'),
    ('family_string', '@A_FAMILY@'),
]


@pytest.mark.parametrize('test_input,expected', testdata_family)  # noqa: PT006
def test_family(test_input: str, expected: str | int | bool) -> None:
    a = Genealogy(version='7.0')
    family = a.family_xref('a family')
    family_type = isinstance(family, FamilyXref)  # noqa: F841
    family_name = family.name  # noqa: F841
    family_fullname = family.fullname  # noqa: F841
    family_string = str(family)  # noqa: F841

    assert eval(test_input) == expected


def test_family_dup() -> None:
    """Test whether a duplicate record can be created."""
    xref_name = 'hello family'
    a = Genealogy(version='7.0')
    name1 = a.family_xref(xref_name)
    with pytest.raises(ValueError, match=Msg.XREF_EXISTS.format(name1.fullname, xref_name)):
        name2 = a.family_xref(xref_name)  # noqa: F841


testdata_multimedia = [
    ('multimedia_type', True),
    ('multimedia_name', '1'),
    ('multimedia_fullname', '@1@'),
    ('multimedia_string', '@1@'),
]


@pytest.mark.parametrize('test_input,expected', testdata_multimedia)  # noqa: PT006
def test_multimedia(test_input: str, expected: str | int | bool) -> None:
    a = Genealogy(version='7.0')
    multimedia = a.multimedia_xref()
    multimedia_type = isinstance(multimedia, MultimediaXref)  # noqa: F841
    multimedia_name = multimedia.name  # noqa: F841
    multimedia_fullname = multimedia.fullname  # noqa: F841
    multimedia_string = str(multimedia)  # noqa: F841

    assert eval(test_input) == expected


def test_multimedia_dup() -> None:
    """Test whether a duplicate record can be created."""
    xref_name = 'hello multimedia'
    a = Genealogy(version='7.0')
    name1 = a.multimedia_xref(xref_name)
    with pytest.raises(ValueError, match=Msg.XREF_EXISTS.format(name1.fullname, xref_name)):
        name2 = a.multimedia_xref(xref_name)  # noqa: F841


testdata_repository = [
    ('repository_type', True),
    ('repository_name', '1'),
    ('repository_fullname', '@1@'),
    ('repository_string', '@1@'),
]


@pytest.mark.parametrize('test_input,expected', testdata_repository)  # noqa: PT006
def test_repository(test_input: str, expected: str | int | bool) -> None:
    a = Genealogy(version='7.0')
    repository = a.repository_xref()
    repository_type = isinstance(repository, RepositoryXref)  # noqa: F841
    repository_name = repository.name  # noqa: F841
    repository_fullname = repository.fullname  # noqa: F841
    repository_string = str(repository)  # noqa: F841

    assert eval(test_input) == expected


def test_repository_dup() -> None:
    """Test whether a duplicate record can be created."""
    xref_name = 'hello repository'
    a = Genealogy(version='7.0')
    name1 = a.repository_xref(xref_name)  
    with pytest.raises(ValueError, match=Msg.XREF_EXISTS.format(name1.fullname, xref_name)):
        name2 = a.repository_xref(xref_name)  # noqa: F841


testdata_shared_note = [
    ('shared_note_type', True),
    ('shared_note_name', '1'),
    ('shared_note_fullname', '@1@'),
    ('shared_note_string', '@1@'),
]


@pytest.mark.parametrize('test_input,expected', testdata_shared_note)  # noqa: PT006
def test_shared_note(test_input: str, expected: str | int | bool) -> None:
    a = Genealogy(version='7.0')
    shared_note = a.shared_note_xref()
    shared_note_type = isinstance(shared_note, SharedNoteXref)  # noqa: F841
    shared_note_name = shared_note.name  # noqa: F841
    shared_note_fullname = shared_note.fullname  # noqa: F841
    shared_note_string = str(shared_note)  # noqa: F841

    assert eval(test_input) == expected


def test_shared_note_dup() -> None:
    """Test whether a duplicate record can be created."""
    xref_name = 'hello shared note'
    a = Genealogy(version='7.0')
    name1 = a.shared_note_xref(xref_name)  
    with pytest.raises(ValueError, match=Msg.XREF_EXISTS.format(name1.fullname, xref_name)):
        name2 = a.shared_note_xref(xref_name)  # noqa: F841


testdata_source = [
    ('source_type', True),
    ('source_name', '1'),
    ('source_fullname', '@1@'),
    ('source_string', '@1@'),
]


@pytest.mark.parametrize('test_input,expected', testdata_source)  # noqa: PT006
def test_source(test_input: str, expected: str | int | bool) -> None:
    a = Genealogy(version='7.0')
    source = a.source_xref()
    source_type = isinstance(source, SourceXref)  # noqa: F841
    source_name = source.name  # noqa: F841
    source_fullname = source.fullname  # noqa: F841
    source_string = str(source)  # noqa: F841

    assert eval(test_input) == expected


def test_source_dup() -> None:
    """Test whether a duplicate record can be created."""
    xref_name = 'hello source'
    a = Genealogy(version='7.0')
    name1 = a.source_xref(xref_name)  
    with pytest.raises(ValueError, match=Msg.XREF_EXISTS.format(name1.fullname, xref_name)):
        name2 = a.source_xref(xref_name)  # noqa: F841


testdata_submitter = [
    ('submitter_type', True),
    ('submitter_name', '1'),
    ('submitter_fullname', '@1@'),
    ('submitter_string', '@1@'),
]


@pytest.mark.parametrize('test_input,expected', testdata_submitter)  # noqa: PT006
def test_submitter(test_input: str, expected: str | int | bool) -> None:
    a = Genealogy()
    submitter = a.submitter_xref()
    submitter_type = isinstance(submitter, SubmitterXref)  # noqa: F841
    submitter_name = submitter.name  # noqa: F841
    submitter_fullname = submitter.fullname  # noqa: F841
    submitter_string = str(submitter)  # noqa: F841

    assert eval(test_input) == expected


def test_submitter_dup() -> None:
    """Test whether a duplicate record can be created."""
    xref_name = 'hello submitter'
    a = Genealogy(version='7.0')
    name1 = a.submitter_xref(xref_name)  
    with pytest.raises(ValueError, match=Msg.XREF_EXISTS.format(name1.fullname, xref_name)):
        name2 = a.submitter_xref(xref_name)  # noqa: F841


# Test staging records including header.

def test_stage_individual() -> None:
    g = Genealogy()
    indi_xref = g.individual_xref()
    indi = RecordIndi(indi_xref)
    g.stage(indi)
    assert len(g.records) == 1

def test_stage_header() -> None:
    g = Genealogy()
    head = Head(Gedc(GedcVers('7.0')))
    g.stage(head)
    assert g.record_header is not None



        