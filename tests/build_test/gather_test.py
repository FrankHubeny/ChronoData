# tests/build_test/gather_test.py
"""Test gathering the seven record types and storing them into a string.

The following example-tests are available.
- `test_empty_record_lists`: None of the seven record type have any records in them.
- `test_one_record`: There is one and only one record in each record type.
- `test_three_records`: There three records of each record type.
- `test_duplicates`: No duplicate records are permitted to be stored.
- `test_reuse_xref`: Different records except for xref are not permitted to be stored.


"""

import re

import pytest

import genedata.classes7 as gc
from genedata.build import Genealogy
from genedata.constants import Default  # noqa: F401
from genedata.messages import Msg

testdata_empty = [
    ('len(a.ged_family)', 0),
    ('len(a.ged_individual)', 0),
]


@pytest.mark.parametrize('test_input,expected', testdata_empty)  # noqa: PT006
def test_empty_record_lists(
    test_input: str, expected: str | int | bool
) -> None:
    a = Genealogy('test')
    a.families([])
    a.individuals([])
    a.multimedia([])
    a.repositories([])
    a.shared_notes([])
    a.sources([])
    a.submitters([])

    assert eval(test_input) == expected


# testdata_one = (
#     ('a.ged_family[0:9]', '0 @1@ FAM'),
#     ('a.ged_individual[0:10]', '0 @2@ INDI'),
#     ('a.ged_multimedia[0:10]', '0 @3@ OBJE'),
#     ('a.ged_repository[0:10]', '0 @4@ REPO'),
#     ('a.ged_shared_note[0:11]', '0 @5@ SNOTE'),
#     ('a.ged_source[0:10]', '0 @6@ SOUR'),
#     ('a.ged_submitter[0:10]', '0 @7@ SUBM'),
# )


# @pytest.mark.parametrize('test_input,expected', testdata_one)
# def test_one_record(test_input: str, expected: str) -> None:
#     a = Genealogy('test')
#     familyxref = a.family_xref()
#     individualxref = a.individual_xref()
#     multimediaxref = a.multimedia_xref()
#     repositoryxref = a.repository_xref()
#     sharednotexref = a.shared_note_xref()
#     sourcexref = a.source_xref()
#     submitterxref = a.submitter_xref()
#     family = Family(familyxref)
#     individual = Individual(individualxref)
#     multimedia = Multimedia(multimediaxref)
#     repository = Repository(repositoryxref)
#     shared_note = SharedNote(sharednotexref)
#     source = Source(sourcexref)
#     submitter = Submitter(submitterxref)
#     a.families([family])
#     a.individuals([individual])
#     a.multimedia([multimedia])
#     a.repositories([repository])
#     a.shared_notes([shared_note])
#     a.sources([source])
#     a.submitters([submitter])

#     assert eval(test_input) == expected


testdata_three: list[tuple[str, int]] = [
    ('a.ged_family.count(Default.EOL)', 3),
    ('a.ged_individual.count(Default.EOL)', 3),
    ('a.ged_multimedia.count(Default.EOL)', 9),  # 3 ged lines per multimedia record: OBJE, FILE, FORM
    ('a.ged_repository.count(Default.EOL)', 6),  # 2 ged lines per repository record: REPO, NAME
    ('a.ged_shared_note.count(Default.EOL)', 3),
    ('a.ged_source.count(Default.EOL)', 3),
    ('a.ged_submitter.count(Default.EOL)', 6),   # 2 ged line per submitter record: SUBM, NAME
]


@pytest.mark.parametrize(('test_input', 'expected'), testdata_three)
def test_three_records(test_input: str, expected: str | int | bool) -> None:
    a = Genealogy('test')
    family1 = gc.RecordFam(a.family_xref())
    family2 = gc.RecordFam(a.family_xref())
    family3 = gc.RecordFam(a.family_xref())
    individual1 = gc.RecordIndi(a.individual_xref())
    individual2 = gc.RecordIndi(a.individual_xref())
    individual3 = gc.RecordIndi(a.individual_xref())
    multimedia1 = gc.RecordObje(
        a.multimedia_xref(), gc.File('a.txt', gc.Form('text/html'))
    )
    multimedia2 = gc.RecordObje(
        a.multimedia_xref(), gc.File('b.txt', gc.Form('text/html'))
    )
    multimedia3 = gc.RecordObje(
        a.multimedia_xref(), gc.File('c.txt', gc.Form('text/html'))
    )
    repository1 = gc.RecordRepo(a.repository_xref(), gc.Name('X'))
    repository2 = gc.RecordRepo(a.repository_xref(), gc.Name('Y'))
    repository3 = gc.RecordRepo(a.repository_xref(), gc.Name('Z'))
    shared_note1 = gc.RecordSnote(a.shared_note_xref(text='a'))
    shared_note2 = gc.RecordSnote(a.shared_note_xref(text='b'))
    shared_note3 = gc.RecordSnote(a.shared_note_xref(text='c'))
    source1 = gc.RecordSour(a.source_xref())
    source2 = gc.RecordSour(a.source_xref())
    source3 = gc.RecordSour(a.source_xref())
    submitter1 = gc.RecordSubm(a.submitter_xref(), gc.Name('A'))
    submitter2 = gc.RecordSubm(a.submitter_xref(), gc.Name('B'))
    submitter3 = gc.RecordSubm(a.submitter_xref(), gc.Name('C;'))
    a.families([family1, family2, family3])
    a.individuals([individual1, individual2, individual3])
    a.multimedia([multimedia1, multimedia2, multimedia3])
    a.repositories([repository1, repository2, repository3])
    a.shared_notes([shared_note1, shared_note2, shared_note3])
    a.sources([source1, source2, source3])
    a.submitters([submitter1, submitter2, submitter3])
    assert eval(test_input) == expected


def test_missing_individual() -> None:
    """Test that an individual identifier was not listed in the individual records."""
    a = Genealogy('test')
    sam_xref = a.individual_xref('sam')
    sam = gc.RecordIndi(sam_xref)

    joe = a.individual_xref('joe')
    missing = [joe.fullname]
    with pytest.raises(
        ValueError, match=re.escape(Msg.MISSING.format(missing))
    ):
        a.individuals([sam])


def test_missing_family() -> None:
    """Test that a family identifier was not listed in the family records."""
    a = Genealogy('test')
    one_xref = a.family_xref('one')
    one = gc.RecordFam(one_xref)

    two = a.family_xref('two')
    missing = [two.fullname]
    with pytest.raises(
        ValueError, match=re.escape(Msg.MISSING.format(missing))
    ):
        a.families([one])


# def test_missing_multimedia() -> None:
#     """Test that a multimedia identifier was not listed in the multimedia records."""
#     a = Genealogy('test')
#     one_xref = a.multimedia_xref('one')
#     one = Multimedia(one_xref)

#     two = a.multimedia_xref('two')
#     missing = [two.fullname]
#     with pytest.raises(
#         ValueError, match=re.escape(Msg.MISSING.format(missing))
#     ):
#         a.multimedia([one])


# def test_missing_repository() -> None:
#     """Test that a repository identifier was not listed in the repository records."""
#     a = Genealogy('test')
#     one_xref = a.repository_xref('one')
#     one = Repository(one_xref)

#     two = a.repository_xref('two')
#     missing = [two.fullname]
#     with pytest.raises(
#         ValueError, match=re.escape(Msg.MISSING.format(missing))
#     ):
#         a.repositories([one])


# def test_missing_shared_note() -> None:
#     """Test that a shared note identifier was not listed in the shared note records."""
#     a = Genealogy('test')
#     one_xref = a.shared_note_xref('one')
#     one = SharedNote(one_xref)

#     two = a.shared_note_xref('two')
#     missing = [two.fullname]
#     with pytest.raises(
#         ValueError, match=re.escape(Msg.MISSING.format(missing))
#     ):
#         a.shared_notes([one])


def test_missing_source() -> None:
    """Test that a source identifier was not listed in the source records."""
    a = Genealogy('test')
    one_xref = a.source_xref('one')
    one = gc.RecordSour(one_xref)

    two = a.source_xref('two')
    missing = [two.fullname]
    with pytest.raises(
        ValueError, match=re.escape(Msg.MISSING.format(missing))
    ):
        a.sources([one])


# def test_missing_submitter() -> None:
#     """Test that a submitter identifier was not listed in the submitter records."""
#     a = Genealogy('test')
#     one_xref = a.submitter_xref('one')
#     one = Submitter(one_xref)

#     two = a.submitter_xref('two')
#     missing = [two.fullname]
#     with pytest.raises(
#         ValueError, match=re.escape(Msg.MISSING.format(missing))
#     ):
#         a.submitters([one])


def test_many_missing_families() -> None:
    """Test that many family identifiers wer not listed in the family records."""
    a = Genealogy('test')
    one = a.family_xref('one')

    two = a.family_xref('two')
    missing = [one.fullname, two.fullname]
    with pytest.raises(
        ValueError, match=re.escape(Msg.MISSING.format(missing))
    ):
        a.families([])


def test_duplicate_family() -> None:
    """Test that an error is raised if a family cross-reference identifier is used twice."""
    a = Genealogy('duplicate')
    fam_one_xref = a.family_xref('one')
    fam = gc.RecordFam(fam_one_xref)
    with pytest.raises(
        ValueError,
        match=re.escape(Msg.DUPLICATE_RECORD.format(fam_one_xref.fullname)),
    ):
        a.families([fam, fam])


def test_duplicate_individual() -> None:
    """Test that an error is raised if an individual cross-reference identifier is used twice."""
    a = Genealogy('duplicate')
    indi_one_xref = a.individual_xref('one')
    indi = gc.RecordIndi(indi_one_xref)
    with pytest.raises(
        ValueError,
        match=re.escape(Msg.DUPLICATE_RECORD.format(indi_one_xref.fullname)),
    ):
        a.individuals([indi, indi])


# def test_duplicate_multimedia() -> None:
#     """Test that an error is raised if a multimedia cross-reference identifier is used twice."""
#     a = Genealogy('duplicate')
#     obje_one_xref = a.multimedia_xref('one')
#     obje = Multimedia(xref=obje_one_xref)
#     with pytest.raises(
#         ValueError,
#         match=re.escape(Msg.DUPLICATE_RECORD.format(obje_one_xref.fullname)),
#     ):
#         a.multimedia([obje, obje])


# def test_duplicate_repository() -> None:
#     """Test that an error is raised if a repository cross-reference identifier is used twice."""
#     a = Genealogy('duplicate')
#     repo_one_xref = a.repository_xref('one')
#     repo = Repository(xref=repo_one_xref)
#     with pytest.raises(
#         ValueError,
#         match=re.escape(Msg.DUPLICATE_RECORD.format(repo_one_xref.fullname)),
#     ):
#         a.repositories([repo, repo])


# def test_duplicate_shared_note() -> None:
#     """Test that an error is raised if a shared note cross-reference identifier is used twice."""
#     a = Genealogy('duplicate')
#     snote_one_xref = a.shared_note_xref('one')
#     snote = SharedNote(xref=snote_one_xref)
#     with pytest.raises(
#         ValueError,
#         match=re.escape(Msg.DUPLICATE_RECORD.format(snote_one_xref.fullname)),
#     ):
#         a.shared_notes([snote, snote])


def test_duplicate_source() -> None:
    """Test that an error is raised if a source cross-reference identifier is used twice."""
    a = Genealogy('duplicate')
    sour_one_xref = a.source_xref('one')
    sour = gc.RecordSour(sour_one_xref)
    with pytest.raises(
        ValueError,
        match=re.escape(Msg.DUPLICATE_RECORD.format(sour_one_xref.fullname)),
    ):
        a.families([sour, sour])  # type: ignore[list-item]


# def test_duplicate_submitter() -> None:
#     """Test that an error is raised if a submitter cross-reference identifier is used twice."""
#     a = Genealogy('duplicate')
#     subm_one_xref = a.submitter_xref('one')
#     subm = Submitter(xref=subm_one_xref)
#     with pytest.raises(
#         ValueError,
#         match=re.escape(Msg.DUPLICATE_RECORD.format(subm_one_xref.fullname)),
#     ):
#         a.families([subm, subm]) # type: ignore[list-item]
