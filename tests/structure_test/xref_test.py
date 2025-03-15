# xref_test.py
"""Test the functionality of the Xref class through classes which inherit from it.

1. FamilyXref
    a. Good run.
    b. Run ged.
    c. Run code.
    d. Exceptions raised

2. IndividualXref
    a. Good run.
    b. Run ged.
    c. Run code.
    d. Exceptions raised

3. MultimediaXref
    a. Good run.
    b. Run ged.
    c. Run code.
    d. Exceptions raised

4. RepositoryXref
    a. Good run.
    b. Run ged.
    c. Run code.
    d. Exceptions raised

5. SharedNoteXref
    a. Good run.
    b. Run ged.
    c. Run code.
    d. Exceptions raised

6. SourceXref
    a. Good run.
    b. Run ged.
    c. Run code.
    d. Exceptions raised

7. SubmitterXref
    a. Good run.
    b. Run ged.
    c. Run code.
    d. Exceptions raised

8. ExtensionXref
    a. Good run.
    b. Run ged.
    c. Run code.
    d. Exceptions raised
"""

import re

import pytest

from genedata.build import Genealogy
from genedata.classes7 import (
    # Ext,
    File,
    Form,
    Name,
    RecordFam,
    RecordIndi,
    RecordObje,
    RecordRepo,
    RecordSnote,
    RecordSour,
    RecordSubm,
)
from genedata.messages import Msg

# 1. FamilyXref
#     a. Good run.
#     b. Run ged.


def test_good_family_xref() -> None:
    """Instantiate a minimal family Xref."""
    g = Genealogy('test')
    fam = g.family_xref('fam')
    assert fam.ged() == '0 @FAM@ FAM\n'


def test_good_family_record() -> None:
    """Instantiate a minimal RecordFam."""
    g = Genealogy('test')
    fam = g.family_xref('fam')
    m = RecordFam(fam)
    assert m.ged() == '0 @FAM@ FAM\n'


#     c. Run code.


def test_family_record_code() -> None:
    """Generate the code to run the minimal RecordFam."""
    g = Genealogy('test')
    fam = g.family_xref('fam')
    m = RecordFam(fam)
    assert m.code() == "\nRecordFam(FamilyXref('@FAM@'))"


#     d. Exceptions raised


def test_bad_family_xref() -> None:
    """Check that the wrong cross reference identifier is caught."""
    g = Genealogy('test')
    indi = g.individual_xref('indi')
    m = RecordFam(indi)  # type: ignore[arg-type]
    with pytest.raises(
        ValueError,
        match=re.escape(Msg.NOT_FAMILY_XREF.format(str(m.value), m.class_name)),
    ):
        m.validate()


# 2. IndividualXref
#     a. Good run.
#     b. Run ged.


def test_good_individual_xref() -> None:
    """Instantiate a minimal individual Xref."""
    g = Genealogy('test')
    indi = g.individual_xref('indi')
    assert indi.ged() == '0 @INDI@ INDI\n'


def test_good_individual_record() -> None:
    """Instantiate a minimal RecordIndi."""
    g = Genealogy('test')
    indi = g.individual_xref('indi')
    m = RecordIndi(indi)
    assert m.ged() == '0 @INDI@ INDI\n'


#     c. Run code.


def test_individual_record_code() -> None:
    """Generate the code to run the minimal RecordIndi."""
    g = Genealogy('test')
    indi = g.individual_xref('indi')
    m = RecordIndi(indi)
    assert m.code() == "\nRecordIndi(IndividualXref('@INDI@'))"


#     d. Exceptions raised


def test_bad_individual_xref() -> None:
    """Check that the wrong cross reference identifier is caught."""
    g = Genealogy('test')
    fam = g.family_xref('fam')
    m = RecordIndi(fam)  # type: ignore[arg-type]
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_INDIVIDUAL_XREF.format(str(m.value), m.class_name)
        ),
    ):
        m.validate()


# 3. MultimediaXref
#     a. Good run.
#     b. Run ged.


def test_good_multimedia_xref() -> None:
    """Instantiate a minimal multimedia Xref."""
    g = Genealogy('test')
    obje = g.multimedia_xref('obje')
    assert obje.ged() == '0 @OBJE@ OBJE\n'


def test_good_multimedia_record() -> None:
    """Instantiate a minimal RecordObje."""
    g = Genealogy('test')
    obje = g.multimedia_xref('obje')
    m = RecordObje(obje, subs=File('a file', Form('text/html')))
    assert m.ged() == '0 @OBJE@ OBJE\n1 FILE a file\n2 FORM text/html\n'


#     c. Run code.


def test_multimedia_record_code() -> None:
    """Generate the code to run the minimal RecordObje."""
    g = Genealogy('test')
    obje = g.multimedia_xref('obje')
    m = RecordObje(obje, subs=File('a file', Form('text/html')))
    assert (
        m.code()
        == "\nRecordObje(MultimediaXref('@OBJE@'), File('a file', Form('text/html')))"
    )


#     d. Exceptions raised


def test_bad_multimedia_xref() -> None:
    """Check that the wrong cross reference identifier is caught."""
    g = Genealogy('test')
    indi = g.individual_xref('indi')
    m = RecordObje(indi, subs=File('a file', Form('text/html')))  # type: ignore[arg-type]
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_MULTIMEDIA_XREF.format(str(m.value), m.class_name)
        ),
    ):
        m.validate()


# 4. RepositoryXref
#     a. Good run.
#     b. Run ged.


def test_good_repository_xref() -> None:
    """Instantiate a minimal repository Xref."""
    g = Genealogy('test')
    repo = g.repository_xref('repo')
    assert repo.ged() == '0 @REPO@ REPO\n'


def test_good_repository_record() -> None:
    """Instantiate a minimal RecordRepo."""
    g = Genealogy('test')
    repo = g.repository_xref('repo')
    m = RecordRepo(repo, Name('my name'))
    assert m.ged() == '0 @REPO@ REPO\n1 NAME my name\n'


#     c. Run code.


def test_repository_record_code() -> None:
    """Generate the code to run the minimal RecordRepo."""
    g = Genealogy('test')
    repo = g.repository_xref('repo')
    m = RecordRepo(repo, subs=Name('my name'))
    assert m.code() == "\nRecordRepo(RepositoryXref('@REPO@'), Name('my name'))"


#     d. Exceptions raised


def test_bad_repository_xref() -> None:
    """Check that the wrong cross reference identifier is caught."""
    g = Genealogy('test')
    indi = g.individual_xref('indi')
    m = RecordRepo(indi, subs=Name('my name'))  # type: ignore[arg-type]
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_REPOSITORY_XREF.format(str(m.value), m.class_name)
        ),
    ):
        m.validate()


# 5. SharedNoteXref
#     a. Good run.
#     b. Run ged.


def test_good_shared_note_xref() -> None:
    """Instantiate a minimal shared_note Xref."""
    g = Genealogy('test')
    snote = g.shared_note_xref('snote', text='A shared note.')
    assert snote.ged() == '0 @SNOTE@ SNOTE A shared note.\n'


def test_good_shared_note_record() -> None:
    """Instantiate a minimal RecordSnote."""
    g = Genealogy('test')
    snote = g.shared_note_xref('snote', text='A shared note.')
    m = RecordSnote(snote)
    assert m.ged() == '0 @SNOTE@ SNOTE A shared note.\n'


#     c. Run code.


def test_shared_note_record_code() -> None:
    """Generate the code to run the minimal RecordSnote."""
    g = Genealogy('test')
    snote = g.shared_note_xref('snote', text='A shared note.')
    m = RecordSnote(snote)
    assert (
        m.code()
        == "\nRecordSnote(SharedNoteXref('@SNOTE@', text='A shared note.'))"
    )


#     d. Exceptions raised


def test_bad_shared_note_xref() -> None:
    """Check that the wrong cross reference identifier is caught."""
    g = Genealogy('test')
    indi = g.individual_xref('indi')
    m = RecordSnote(indi)  # type: ignore[arg-type]
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_SHARED_NOTE_XREF.format(str(m.value), m.class_name)
        ),
    ):
        m.validate()


# 6. SourceXref
#     a. Good run.
#     b. Run ged.


def test_good_source_xref() -> None:
    """Instantiate a minimal source Xref."""
    g = Genealogy('test')
    sour = g.source_xref('sour')
    assert sour.ged() == '0 @SOUR@ SOUR\n'


def test_good_source_record() -> None:
    """Instantiate a minimal RecordSour."""
    g = Genealogy('test')
    sour = g.source_xref('sour')
    m = RecordSour(sour)
    assert m.ged() == '0 @SOUR@ SOUR\n'


#     c. Run code.


def test_source_record_code() -> None:
    """Generate the code to run the minimal RecordSour."""
    g = Genealogy('test')
    sour = g.source_xref('sour')
    m = RecordSour(sour)
    assert m.code() == "\nRecordSour(SourceXref('@SOUR@'))"


#     d. Exceptions raised


def test_bad_source_xref() -> None:
    """Check that the wrong cross reference identifier is caught."""
    g = Genealogy('test')
    indi = g.individual_xref('indi')
    m = RecordSour(indi)  # type: ignore[arg-type]
    with pytest.raises(
        ValueError,
        match=Msg.NOT_SOURCE_XREF.format(str(m.value), m.class_name),
    ):
        m.validate()


# 7. SubmitterXref
#     a. Good run.
#     b. Run ged.


def test_good_submitter_xref() -> None:
    """Instantiate a minimal submitter Xref."""
    g = Genealogy('test')
    subm = g.submitter_xref('subm')
    assert subm.ged() == '0 @SUBM@ SUBM\n'


def test_good_submitter_record() -> None:
    """Instantiate a minimal RecordSubm."""
    g = Genealogy('test')
    subm = g.submitter_xref('subm')
    m = RecordSubm(subm, Name('my name'))
    assert m.ged() == '0 @SUBM@ SUBM\n1 NAME my name\n'


#     c. Run code.


def test_submitter_record_code() -> None:
    """Generate the code to run the minimal RecordSubm."""
    g = Genealogy('test')
    subm = g.submitter_xref('subm')
    m = RecordSubm(subm, Name('my name'))
    assert m.code() == "\nRecordSubm(SubmitterXref('@SUBM@'), Name('my name'))"


#     d. Exceptions raised


def test_bad_submitter_xref() -> None:
    """Check that the wrong cross reference identifier is caught."""
    g = Genealogy('test')
    indi = g.individual_xref('indi')
    m = RecordSubm(indi, Name('my name'))  # type: ignore[arg-type]
    with pytest.raises(
        ValueError,
        match=Msg.NOT_SUBMITTER_XREF.format(str(m.value), m.class_name),
    ):
        m.validate()


# 8. ExtensionXref
#     a. Good run.
#     b. Run ged.


def test_good_extension_xref() -> None:
    """Instantiate a minimal extension Xref."""
    g = Genealogy('test')
    ext = g.extension_xref('ext')
    assert ext.ged() == '0 @EXT@ EXT\n'


# def test_good_extension_record() -> None:
#     """Instantiate a minimal RecordExt."""
#     g = Genealogy('test')
#     ext = g.extension_xref('ext')
#     m = Ext(ext)
# assert m.ged() == '0 @EXT@ EXT\n'


#     c. Run code.
#     d. Exceptions raised
