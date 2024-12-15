"""------------------------------------------------------------------------------
                            Defs Class Tests

    These tests cover the `Defs` NamedTuple class.

------------------------------------------------------------------------------"""

import pytest

from chronodata.chrono import Chronology
from chronodata.g7 import Record
from chronodata.messages import Msg

testdata = [
    ('indi', True),
    ('fam', True),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_time(test_input: str, expected: str | int | bool) -> None:
    a = Chronology('test')
    indi_xref = a.individual_xref()
    fam_xref = a.family_xref()
    indi: bool = a.verify_xref(  # noqa: F841
        indi_xref, a.individual_xreflist, Record.INDIVIDUAL
    )  
    fam: bool = a.verify_xref(fam_xref, a.family_xreflist, Record.FAMILY)  # noqa: F841

    assert eval(test_input) == expected


def test_xref_individual() -> None:
    a = Chronology('test')
    with pytest.raises(
        ValueError, match=Msg.NOT_RECORD.format('rec', Record.INDIVIDUAL)
    ):
        a.verify_xref('rec', a.individual_xreflist, Record.INDIVIDUAL)


def test_xref_family() -> None:
    a = Chronology('test')
    with pytest.raises(
        ValueError, match=Msg.NOT_RECORD.format('rec', Record.FAMILY)
    ):
        a.verify_xref('rec', a.family_xreflist, Record.FAMILY)


# def test_xref_medialink() -> None:
#     a = Chronology('test')
#     with pytest.raises(
#         ValueError, match=Msg.NOT_RECORD.format('rec', Record.MULTIMEDIA)):
#         a.verify_xref('rec', a.multimedia_xreflist, Record.MULTIMEDIA)

# def test_xref_source() -> None:
#     a = Chronology('test')
#     with pytest.raises(
#         ValueError, match=Msg.NOT_RECORD.format('rec', Record.SOURCE)):
#         a.verify_xref('rec', a.source_xreflist, Record.SOURCE)

# def test_xref_repository() -> None:
#     a = Chronology('test')
#     with pytest.raises(
#         ValueError, match=Msg.NOT_RECORD.format('rec', Record.REPOSITORY)):
#         a.verify_xref('rec', a.repository_xreflist, Record.REPOSITORY)

# def test_xref_submitter() -> None:
#     a = Chronology('test')
#     with pytest.raises(
#         ValueError, match=Msg.NOT_RECORD.format('rec', Record.SUBMITTER)):
#         a.verify_xref('rec', a.submitter_xreflist, Record.SUBMITTER)

# def test_xref_shared_note() -> None:
#     a = Chronology('test')
#     with pytest.raises(
#         ValueError, match=Msg.NOT_RECORD.format('rec', Record.SHARED_NOTE)):
#         a.verify_xref('rec', a.shared_note_xreflist, Record.SHARED_NOTE)
