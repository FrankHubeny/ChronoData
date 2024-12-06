"""------------------------------------------------------------------------------
                            Counter Tests
------------------------------------------------------------------------------"""

import pytest

from chronodata.chrono import Chronology

testdata = [
    ('oldxref', 1),
    ('xref', '@1@'),
    ('a.xref_individual[0]', '@1@'),
    ('a.xref_family[0]', '@2@'),
    ('newxref', 2),
    ('a.xref_multimedia[0]', '@3@'),
    ('a.xref_repository[0]', '@4@'),
    ('a.xref_source[0]', '@5@'),
    ('a.xref_submitter[0]', '@6@'),
    ('a.xref_shared_note[0]', '@7@'),
   
]
@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_counter(test_input: str, expected: str | int | bool) -> None:
    a = Chronology(name='testing')
    oldxref = a.xref_counter
    xref = a.next_counter(a.xref_individual)
    newxref = a.xref_counter
    xref_family = a.next_counter(a.xref_family)
    xref_multimedia = a.next_counter(a.xref_multimedia)
    xref_repository = a.next_counter(a.xref_repository)
    xref_source = a.next_counter(a.xref_source)
    xref_submitter = a.next_counter(a.xref_submitter)
    xref_shared_note = a.next_counter(a.xref_shared_note)
    
    assert eval(test_input) == expected