"""------------------------------------------------------------------------------
                            Personal Name Structure Tests
------------------------------------------------------------------------------"""

import pytest

from chronodata.chrono import (
    Chronology,
    PersonalName,
)
from chronodata.g7 import Gedcom

testdata = [
    (
        's1',
        '1 NAME Joe\n2 TYPE AKA\n3 PHRASE this is joey\n2 NPFX Joe\n2 GIVN Joe\n',
    ),
    ('s2', '1 NAME Joe\n2 TYPE AKA\n3 PHRASE this is joey\n'),
    # ('t1', '2 TRAN sss\n3 LANG en\n3 NICK jjj\n'),
    # ('s3', '1 NAME Joe\n2 TYPE AKA\n3 PHRASE this is joey\n2 TRAN sss\n3 LANG en\n3 NICK jjj\n'),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_personal_name(test_input: str, expected: str | int | bool) -> None:
    a = Chronology(name='testing')
    s1 = a.personal_name_structure(  # noqa: F841
        name='Joe',
        type_name=Gedcom.AKA,
        phrase='this is joey',
        pieces=[
            PersonalName(Gedcom.NPFX, 'Joe'),
            PersonalName(Gedcom.GIVN, '   Joe   '),
        ],
    )
    s2 = a.personal_name_structure(  # noqa: F841
        name='Joe', type_name=Gedcom.AKA, phrase='this is joey'
    )
    # t1 = a.translation(Name_Translation('sss', 'en', Personal_Name(Gedcom.NICK, 'jjj')), level=2)
    # s3 = a.personal_name_structure(
    #    name='Joe',
    #    type_name=Gedcom.AKA,
    #    phrase='this is joey',
    #    translations=(Name_Translation('sss', 'en', Personal_Name(Gedcom.NICK, 'jjj')))
    # )

    assert eval(test_input) == expected
