"""------------------------------------------------------------------------------
                            Personal Name Tests
------------------------------------------------------------------------------"""

import pytest

from chronodata.build import (
    Chronology,
    PersonalName,
)
from chronodata.g7 import Gedcom

testdata = [
    ('name1.ged(1)', '1 NPFX Joe\n'),
    ('name2.ged(2)', '2 GIVN Joe\n'),
    ('name3.ged(3)', '3 NICK Joe\n'),
    ('name4.ged(4)', '4 SPFX Joe\n'),
    ('name5.ged(5)', '5 SURN Joe\n'),
    ('name6.ged(6)', '6 NSFX Joe\n'),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_personal_name(test_input: str, expected: str | int | bool) -> None:
    a = Chronology(name='testing')
    name1 = PersonalName(Gedcom.NPFX, 'Joe')  # noqa: F841
    name2 = PersonalName(Gedcom.GIVN, '   Joe   ')  # noqa: F841
    name3 = PersonalName(Gedcom.NICK, '   Joe   ')  # noqa: F841
    name4 = PersonalName(Gedcom.SPFX, '   Joe   ')  # noqa: F841
    name5 = PersonalName(Gedcom.SURN, '   Joe   ')  # noqa: F841
    name6 = PersonalName(Gedcom.NSFX, '   Joe   ')  # noqa: F841

    assert eval(test_input) == expected
