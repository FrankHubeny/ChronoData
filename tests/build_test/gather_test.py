# tests/build_test/gather_test.py
"""Test gathering the seven record types and storing them into a string.

The following example-tests are available.
- `test_empty_record_lists`: None of the seven record type have any records in them.
- `test_one_record`: There is one and only one record in each record type.
- `test_three_records`: There three records of each record type.
- `test_duplicates`: No duplicate records are permitted to be stored.
- `test_reuse_xref`: Different records except for xref are not permitted to be stored.


"""

import pytest

from chronodata.build import Chronology
from chronodata.constants import String  # noqa: F401

# from chronodata.records import FamilyXref, IndividualXref, MultimediaXref, RepositoryXref, SharedNoteXref, SourceXref, SubmitterXref
from chronodata.store import (
    Family,
    Husband,
    Individual,
    Multimedia,
    Repository,
    SharedNote,
    Source,
    Submitter,
)

testdata_empty: list[tuple[str, int]] = [
    ('len(a.ged_family)', 0),
    ('len(a.ged_individual)', 0),
    ('len(a.ged_multimedia)', 0),
    ('len(a.ged_repository)', 0),
    ('len(a.ged_shared_note)', 0),
    ('len(a.ged_source)', 0),
    ('len(a.ged_submitter)', 0),
]


@pytest.mark.parametrize('test_input,expected', testdata_empty)  # noqa: PT006
def test_empty_record_lists(
    test_input: str, expected: str | int | bool
) -> None:
    a = Chronology('test')
    a.families([])
    a.individuals([])
    a.multimedia([])
    a.repositories([])
    a.shared_notes([])
    a.sources([])
    a.submitters([])

    assert eval(test_input) == expected


testdata_one: list[tuple[str, str]] = [
    ('a.ged_family[0:9]', '0 @1@ FAM'),
    ('a.ged_individual[0:10]', '0 @2@ INDI'),
    ('a.ged_multimedia[0:10]', '0 @3@ OBJE'),
    ('a.ged_repository[0:10]', '0 @4@ REPO'),
    ('a.ged_shared_note[0:11]', '0 @5@ SNOTE'),
    ('a.ged_source[0:10]', '0 @6@ SOUR'),
    ('a.ged_submitter[0:10]', '0 @7@ SUBM'),
]


@pytest.mark.parametrize('test_input,expected', testdata_one)  # noqa: PT006
def test_one_record(test_input: str, expected: str | int | bool) -> None:
    a = Chronology('test')
    familyxref = a.family_xref()
    individualxref = a.individual_xref()
    multimediaxref = a.multimedia_xref()
    repositoryxref = a.repository_xref()
    sharednotexref = a.shared_note_xref()
    sourcexref = a.source_xref()
    submitterxref = a.submitter_xref()
    family = Family(familyxref)
    individual = Individual(individualxref)
    multimedia = Multimedia(multimediaxref)
    repository = Repository(repositoryxref)
    shared_note = SharedNote(sharednotexref)
    source = Source(sourcexref)
    submitter = Submitter(submitterxref)
    a.families(
        [
            family,
        ]
    )
    a.individuals(
        [
            individual,
        ]
    )
    a.multimedia(
        [
            multimedia,
        ]
    )
    a.repositories(
        [
            repository,
        ]
    )
    a.shared_notes(
        [
            shared_note,
        ]
    )
    a.sources(
        [
            source,
        ]
    )
    a.submitters(
        [
            submitter,
        ]
    )

    assert eval(test_input) == expected


testdata_three: list[tuple[str, int]] = [
    ('a.ged_family.count(String.NEWLINE)', 3),
    ('a.ged_individual.count(String.NEWLINE)', 3),
    ('a.ged_multimedia.count(String.NEWLINE)', 3),
    ('a.ged_repository.count(String.NEWLINE)', 3),
    ('a.ged_shared_note.count(String.NEWLINE)', 3),
    ('a.ged_source.count(String.NEWLINE)', 3),
    ('a.ged_submitter.count(String.NEWLINE)', 3),
]


@pytest.mark.parametrize('test_input,expected', testdata_three)  # noqa: PT006
def test_three_records(test_input: str, expected: str | int | bool) -> None:
    a = Chronology('test')
    family1 = Family(a.family_xref())
    family2 = Family(a.family_xref())
    family3 = Family(a.family_xref())
    individual1 = Individual(a.individual_xref())
    individual2 = Individual(a.individual_xref())
    individual3 = Individual(a.individual_xref())
    multimedia1 = Multimedia(a.multimedia_xref())
    multimedia2 = Multimedia(a.multimedia_xref())
    multimedia3 = Multimedia(a.multimedia_xref())
    repository1 = Repository(a.repository_xref())
    repository2 = Repository(a.repository_xref())
    repository3 = Repository(a.repository_xref())
    shared_note1 = SharedNote(a.shared_note_xref())
    shared_note2 = SharedNote(a.shared_note_xref())
    shared_note3 = SharedNote(a.shared_note_xref())
    source1 = Source(a.source_xref())
    source2 = Source(a.source_xref())
    source3 = Source(a.source_xref())
    submitter1 = Submitter(a.submitter_xref())
    submitter2 = Submitter(a.submitter_xref())
    submitter3 = Submitter(a.submitter_xref())
    a.families(
        [
            family1,
            family2,
            family3,
        ]
    )
    a.individuals(
        [
            individual1,
            individual2,
            individual3,
        ]
    )
    a.multimedia(
        [
            multimedia1,
            multimedia2,
            multimedia3,
        ]
    )
    a.repositories(
        [
            repository1,
            repository2,
            repository3,
        ]
    )
    a.shared_notes(
        [
            shared_note1,
            shared_note2,
            shared_note3,
        ]
    )
    a.sources(
        [
            source1,
            source2,
            source3,
        ]
    )
    a.submitters(
        [
            submitter1,
            submitter2,
            submitter3,
        ]
    )

    assert eval(test_input) == expected


testdata_duplicates: list[tuple[str, int]] = [
    ('a.ged_family.count(String.NEWLINE)', 1),
    ('a.ged_individual.count(String.NEWLINE)', 1),
    ('a.ged_multimedia.count(String.NEWLINE)', 1),
    ('a.ged_repository.count(String.NEWLINE)', 1),
    ('a.ged_shared_note.count(String.NEWLINE)', 1),
    ('a.ged_source.count(String.NEWLINE)', 1),
    ('a.ged_submitter.count(String.NEWLINE)', 1),
]


@pytest.mark.parametrize('test_input,expected', testdata_duplicates)  # noqa: PT006
def test_duplicates(test_input: str, expected: str | int | bool) -> None:
    a = Chronology('test')
    fam = Family(a.family_xref())
    indi = Individual(a.individual_xref())
    obje = Multimedia(a.multimedia_xref())
    repo = Repository(a.repository_xref())
    snote = SharedNote(a.shared_note_xref())
    sour = Source(a.source_xref())
    subm = Submitter(a.submitter_xref())
    a.families(
        [
            fam,
            fam,
        ]
    )
    a.individuals([indi, indi, indi, indi])
    a.multimedia([obje, obje, obje])
    a.repositories([repo, repo, repo, repo, repo])
    a.shared_notes([snote, snote, snote])
    a.sources(
        [
            sour,
            sour,
            sour,
        ]
    )
    a.submitters([subm, subm])

    assert eval(test_input) == expected


# testdata_reuse_xref: list[tuple[str, int]] = [
#     ('a.ged_family.count(String.NEWLINE)', 1),
#     # ('a.ged_individual.count(String.NEWLINE)', 1),
#     # ('a.ged_multimedia.count(String.NEWLINE)', 1),
#     # ('a.ged_repository.count(String.NEWLINE)', 1),
#     # ('a.ged_shared_note.count(String.NEWLINE)', 1),
#     # ('a.ged_source.count(String.NEWLINE)', 1),
#     # ('a.ged_submitter.count(String.NEWLINE)', 1),
# ]


# @pytest.mark.parametrize(
#     'test_input,expected',  
#     testdata_reuse_xref,  
# )
# def test_reuse_xref(
#     test_input: str, expected: str | int | bool
# ) -> None:
#     a = Chronology('test')
#     husband_xref = a.individual_xref()
#     husband1 = Individual(husband_xref)
#     husband2 = Individual(husband_xref)
#     h1 = Husband(husband1)
#     fam_xref = a.family_xref()
#     fam1 = Family(fam_xref)
#     fam2 = Family(fam_xref)
    
#     # obje_xref = a.multimedia_xref()
#     # obje1 = Multimedia(obje_xref)
#     # obje2 = Multimedia(obje_xref)
#     # repo_xref = a.repository_xref()
#     # repo1 = Repository(repo_xref)
#     # repo2 = Repository(repo_xref)
#     # snote_xref = a.shared_note_xref()
#     # snote1 = SharedNote(snote_xref)
#     # snote2 = SharedNote(snote_xref)
#     # sour_xref = a.source_xref()
#     # sour1 = Source(sour_xref)
#     # sour2 = Source(sour_xref)
#     # subm_xref = a.submitter_xref()
#     # subm1 = Submitter(subm_xref)
#     # subm2 = Submitter(subm_xref)
#     a.families(
#         [
#             fam1,
#             fam2,
#         ]
#     )
#     a.individuals([indi1, indi2])
#     a.multimedia(
#         [
#             obje1,
#             obje2,
#         ]
#     )
#     a.repositories(
#         [
#             repo1,
#             repo2,
#         ]
#     )
#     a.shared_notes(
#         [
#             snote1,
#             snote2,
#         ]
#     )
#     a.sources(
#         [
#             sour1,
#             sour2,
#         ]
#     )
#     a.submitters([subm1, subm2])

#     assert eval(test_input) == expected


testdata_same_xref_different_record: list[tuple[str, int | str]] = [
    ('a.ged_family.count(String.NEWLINE)', 1),
    ('a.ged_family','0 FAM @3@\n1 HUSB @1@\n'),
    # ('a.ged_individual.count(String.NEWLINE)', 1),
    # ('a.ged_multimedia.count(String.NEWLINE)', 1),
    # ('a.ged_repository.count(String.NEWLINE)', 1),
    # ('a.ged_shared_note.count(String.NEWLINE)', 1),
    # ('a.ged_source.count(String.NEWLINE)', 1),
    # ('a.ged_submitter.count(String.NEWLINE)', 1),
]


@pytest.mark.parametrize('test_input,expected', testdata_same_xref_different_record)  # noqa: PT006
def test_same_xref_different_record(
    test_input: str, expected: str | int | bool
) -> None:
    a = Chronology('test')
    indi_xref1 = a.individual_xref()
    indi_xref2 = a.individual_xref()
    indi1 = Husband(indi_xref1)
    indi2 = Husband(indi_xref2)
    fam_xref = a.family_xref()
    fam1 = Family(fam_xref, husband=indi1)
    fam2 = Family(fam_xref, husband=indi2)
    
    # obje_xref = a.multimedia_xref()
    # obje1 = Multimedia(obje_xref)
    # obje2 = Multimedia(obje_xref)
    # repo_xref = a.repository_xref()
    # repo1 = Repository(repo_xref)
    # repo2 = Repository(repo_xref)
    # snote_xref = a.shared_note_xref()
    # snote1 = SharedNote(snote_xref)
    # snote2 = SharedNote(snote_xref)
    # sour_xref = a.source_xref()
    # sour1 = Source(sour_xref)
    # sour2 = Source(sour_xref)
    # subm_xref = a.submitter_xref()
    # subm1 = Submitter(subm_xref)
    # subm2 = Submitter(subm_xref)
    a.families(
        [
            fam1,
            fam2,
        ]
    )
    # a.individuals([indi1, indi2])
    # a.multimedia(
    #     [
    #         obje1,
    #         obje2,
    #     ]
    # )
    # a.repositories(
    #     [
    #         repo1,
    #         repo2,
    #     ]
    # )
    # a.shared_notes(
    #     [
    #         snote1,
    #         snote2,
    #     ]
    # )
    # a.sources(
    #     [
    #         sour1,
    #         sour2,
    #     ]
    # )
    # a.submitters([subm1, subm2])

    assert eval(test_input) == expected
