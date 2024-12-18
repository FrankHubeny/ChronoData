"""------------------------------------------------------------------------------
                            Counter Tests

    This set of tests covers the following methods individually and how they
    are expected to be used together.:
    - `family_xref`
    - `individual_xref`
    - `next_counter`
------------------------------------------------------------------------------"""

import pytest

from chronodata.chrono import Chronology
from chronodata.enums import Record

testdata = [
    ('oldxref', 1),
    ('xref', '@1@'),
    ('a.individual_xreflist[0]', '@1@'),
    ('a.family_xreflist[0]', '@2@'),
    ('newxref', 2),
    ('a.multimedia_xreflist[0]', '@3@'),
    ('a.repository_xreflist[0]', '@4@'),
    ('a.source_xreflist[0]', '@5@'),
    ('a.submitter_xreflist[0]', '@6@'),
    ('a.shared_note_xreflist[0]', '@7@'),
    ('adam.fullname', '@8@'),
    ('adam_eve.fullname', '@9@'),
    ('adam_xref', '@ADAM@'),
    ('eve_xref.fullname', '@EVE@'),
    ('adam_eve_xref', '@ADAMEVE@'),
    ('eve_adam_xref.fullname', '@EVE_ADAM@'),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_counter(test_input: str, expected: str | int | bool) -> None:
    a = Chronology(name='testing')
    oldxref = a.xref_counter  # noqa: F841
    xref = a.next_counter(a.individual_xreflist)  # noqa: F841
    newxref = a.xref_counter  # noqa: F841
    xref_family = a.next_counter(a.family_xreflist)  # noqa: F841
    xref_multimedia = a.next_counter(a.multimedia_xreflist)  # noqa: F841
    xref_repository = a.next_counter(a.repository_xreflist)  # noqa: F841
    xref_source = a.next_counter(a.source_xreflist)  # noqa: F841
    xref_submitter = a.next_counter(a.submitter_xreflist)  # noqa: F841
    xref_shared_note = a.next_counter(a.shared_note_xreflist)  # noqa: F841
    adam = a.individual_xref()  # noqa: F841
    adam_eve = a.family_xref()  # noqa: F841
    b = Chronology(name='test name')
    adam_xref = a.next_counter(a.individual_xreflist, xref_name=' Adam   ')  # noqa: F841
    adam_eve_xref = a.next_counter(a.family_xreflist, xref_name='AdamEve')  # noqa: F841
    eve_xref = a.individual_xref(xref_name=' Eve ')  # noqa: F841
    eve_adam_xref = a.family_xref(xref_name='Eve Adam')  # noqa: F841

    assert eval(test_input) == expected
