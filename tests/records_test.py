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

from chronodata.chrono import Chronology
from chronodata.messages import Msg
from chronodata.methods import Defs
from chronodata.records import (
    FamilyXref,
    IndividualXref,
    MultimediaXref,
    RepositoryXref,
    SharedNoteXref,
    SourceXref,
    SubmitterXref,
)

testdata = [
    # IndividualXref
    ('indi1', True),
    ('indi2', '1'),
    ('indi3', '@1@'),
    ('indi4', 'INDIVIDUAL'),
    ('indi5', '@INDIVIDUAL@'),
    ('indi6', 'NAME WITH SPACES'),
    ('indi7', '@NAME_WITH_SPACES@'),
    # FamilyXref
    ('fam1', True),
    ('fam2', 'A FAMILY'),
    ('fam3', '@A_FAMILY@'),
    # MultimediaXref
    ('mm1', True),
    ('mm2', '2'),
    ('mm3', '@2@'),
    # RepositoryXref
    ('repo1', True),
    ('repo2', 'SAME NAME'),
    ('repo3', '@SAME_NAME@'),
    # SharedNoteXref
    ('sn1', True),
    ('sn2', 'SAME NAME'),
    ('sn3', '@SAME_NAME@'),
    # SourceXref
    ('source1', True),
    ('source2', 'SAME NAME'),
    ('source3', '@SAME_NAME@'),
    # SubmitterXref
    ('sub1', True),
    ('sub2', '3'),
    ('sub3', '@3@'),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_defs_tags_classes(test_input: str, expected: str | int | bool) -> None:
    a = Chronology('test')

    # Test creation of the IndividualXref type without names.
    indi_xref1 = a.individual_xref()
    indi1 = Defs.verify_type(indi_xref1, IndividualXref)  # noqa: F841
    indi2 = indi_xref1.name  # noqa: F841
    indi3 = indi_xref1.fullname  # noqa: F841

    # Test creation of IndividualXref type with a name.
    indi_xref2 = a.individual_xref('individual')
    indi4 = str(indi_xref2)  # noqa: F841
    indi5 = indi_xref2.fullname  # noqa: F841

    # Test creation of IndividualXref type with spaces.
    indi_xref3 = a.individual_xref('name with spaces')
    indi6 = indi_xref3.name  # noqa: F841
    indi7 = indi_xref3.fullname  # noqa: F841

    # Test creation of the FamilyXref type.
    fam_xref = a.family_xref('a family')
    fam1 = Defs.verify_type(fam_xref, FamilyXref)  # noqa: F841
    fam2 = str(fam_xref)  # noqa: F841
    fam3 = fam_xref.fullname  # noqa: F841

    # Test creation of the MultimediaXref type.
    mm_xref = a.multimedia_xref()
    mm1 = Defs.verify_type(mm_xref, MultimediaXref)  # noqa: F841
    mm2 = str(mm_xref)  # noqa: F841
    mm3 = mm_xref.fullname  # noqa: F841

    # Test creation of the RepositoryXref type.
    repo_xref = a.repository_xref('same NamE')
    repo1 = Defs.verify_type(repo_xref, RepositoryXref)  # noqa: F841
    repo2 = str(repo_xref)  # noqa: F841
    repo3 = repo_xref.fullname  # noqa: F841

    # Test creation of the SharedNoteXref type.
    sn_xref = a.shared_note_xref('SaMe NaMe')
    sn1 = Defs.verify_type(sn_xref, SharedNoteXref)  # noqa: F841
    sn2 = str(sn_xref)  # noqa: F841
    sn3 = sn_xref.fullname  # noqa: F841

    # Test creation of the SourceXref type.
    source_xref = a.source_xref('Same Name')
    source1 = Defs.verify_type(source_xref, SourceXref)  # noqa: F841
    source2 = str(source_xref)  # noqa: F841
    source3 = source_xref.fullname  # noqa: F841

    # Test creation of the SubmitterXref type.
    sub_xref = a.submitter_xref()
    sub1 = Defs.verify_type(sub_xref, SubmitterXref)  # noqa: F841
    sub2 = str(sub_xref)  # noqa: F841
    sub3 = sub_xref.fullname  # noqa: F841

    assert eval(test_input) == expected


"""The next tests check for duplicate record names. This tests
the chrono module's `next_counter` method for these record types."""


def test_family_dup() -> None:
    xref_name = 'hello1'
    a = Chronology('tttt')
    name1 = a.family_xref(xref_name)  # noqa: F841
    with pytest.raises(ValueError, match=Msg.XREF_EXISTS.format(xref_name)):
        name2 = a.family_xref(xref_name)  # noqa: F841


def test_individual_dup() -> None:
    xref_name = 'hello2'
    a = Chronology('tttt')
    name1 = a.individual_xref(xref_name)  # noqa: F841
    with pytest.raises(ValueError, match=Msg.XREF_EXISTS.format(xref_name)):
        name2 = a.individual_xref(xref_name)  # noqa: F841


def test_multimedia_dup() -> None:
    xref_name = 'hello3'
    a = Chronology('tttt')
    name1 = a.multimedia_xref(xref_name)  # noqa: F841
    with pytest.raises(ValueError, match=Msg.XREF_EXISTS.format(xref_name)):
        name2 = a.multimedia_xref(xref_name)  # noqa: F841


def test_repository_dup() -> None:
    xref_name = 'hello4'
    a = Chronology('tttt')
    name1 = a.repository_xref(xref_name)  # noqa: F841
    with pytest.raises(ValueError, match=Msg.XREF_EXISTS.format(xref_name)):
        name2 = a.repository_xref(xref_name)  # noqa: F841


def test_shared_note_dup() -> None:
    xref_name = 'hello5'
    a = Chronology('tttt')
    name1 = a.shared_note_xref(xref_name)  # noqa: F841
    with pytest.raises(ValueError, match=Msg.XREF_EXISTS.format(xref_name)):
        name2 = a.shared_note_xref(xref_name)  # noqa: F841


def test_source_dup() -> None:
    xref_name = 'hello6'
    a = Chronology('tttt')
    name1 = a.source_xref(xref_name)  # noqa: F841
    with pytest.raises(ValueError, match=Msg.XREF_EXISTS.format(xref_name)):
        name2 = a.source_xref(xref_name)  # noqa: F841


def test_submitter_dup() -> None:
    xref_name = 'hello7'
    a = Chronology('tttt')
    name1 = a.submitter_xref(xref_name)  # noqa: F841
    with pytest.raises(ValueError, match=Msg.XREF_EXISTS.format(xref_name)):
        name2 = a.submitter_xref(xref_name)  # noqa: F841
