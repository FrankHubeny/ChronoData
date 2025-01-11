"""------------------------------------------------------------------------------
                    Three Generation Genealogy Tests

    This builds an imaginary genealogy of the three generations
    that uses all of the features multiple times.
------------------------------------------------------------------------------"""

import pytest

from chronodata.build import Genealogy

testdata = [('joe_someone', '@JOE_SOMEONE@')]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_address(test_input: str, expected: str | int | bool) -> None:
    a = Genealogy(name='genesis5')
    # first generation
    joe_someone = str(a.individual_xref(' Joe Someone '))  # noqa: F841
    jill_someone = str(a.individual_xref('Jill Someone'))  # noqa: F841
    # second generation
    betty_someone = str(a.individual_xref('betty someone'))  # noqa: F841
    tom_someone = str(a.individual_xref('tom someone'))  # noqa: F841
    # third generation
    steve_someoneelse = str(a.individual_xref('steve someoneelse'))  # noqa: F841
    nancy_another = str(a.individual_xref('nancy another'))  # noqa: F841
    jim_someonelse = str(a.individual_xref('jim someoneelse'))  # noqa: F841
    joe_someoneelse = str(a.individual_xref('joe_someoneelse'))  # noqa: F841
    cathy_someone = str(a.individual_xref('cathy someone'))  # noqa: F841

    assert eval(test_input) == expected
