"""------------------------------------------------------------------------------
                    Three Generation Chronology Tests

    This builds an imaginary chronology of the three generations
    that uses all of the features multiple times.
------------------------------------------------------------------------------"""

import pytest

from chronodata.build import Chronology
from chronodata.g7 import Gedcom

testdata = [('joe_someone', '@JOE_SOMEONE@')]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_address(test_input: str, expected: str | int | bool) -> None:
    a = Chronology(name='genesis5')
    # first generation
    joe_someone = a.individual_xref(' Joe Someone ')
    jill_someone = a.individual_xref('Jill Someone')
    # second generation
    betty_someone = a.individual_xref('betty someone')
    tom_someone = a.individual_xref('tom someone')
    # third generation
    steve_someoneelse = a.individual_xref('steve someoneelse')
    nancy_another = a.individual_xref('nancy another')
    jim_someonelse = a.individual_xref('jim someoneelse')
    joe_someoneelse = a.individual_xref('joe_someoneelse')
    cathy_someone = a.individual_xref('cathy someone')

    assert eval(test_input) == expected
