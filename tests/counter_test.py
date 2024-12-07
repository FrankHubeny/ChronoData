"""------------------------------------------------------------------------------
                            Counter Tests
------------------------------------------------------------------------------"""

import pytest

from chronodata.chrono import Chronology

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
    ('adam', '@8@'),
    ('adam_eve', '@9@'),
    ('adam_xref', '@Adam@'),
    ('eve_xref', '@Eve@'),
    ('adam_eve_xref', '@AdamEve@'),
    ('eve_adam_xref', '@EveAdam@'),
   
]
@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_counter(test_input: str, expected: str | int | bool) -> None:
    a = Chronology(name='testing')
    oldxref = a.xref_counter
    xref = a.next_counter(a.individual_xreflist)
    newxref = a.xref_counter
    xref_family = a.next_counter(a.family_xreflist)
    xref_multimedia = a.next_counter(a.multimedia_xreflist)
    xref_repository = a.next_counter(a.repository_xreflist)
    xref_source = a.next_counter(a.source_xreflist)
    xref_submitter = a.next_counter(a.submitter_xreflist)
    xref_shared_note = a.next_counter(a.shared_note_xreflist)
    adam = a.individual_xref()
    adam_eve = a.family_xref()
    b = Chronology(name='test name')
    adam_xref = a.next_counter(a.individual_xreflist, name='Adam')
    adam_eve_xref = a.next_counter(a.family_xreflist, name='AdamEve')
    eve_xref = a.individual_xref(name='Eve')
    eve_adam_xref = a.family_xref(name='EveAdam')
    
    assert eval(test_input) == expected