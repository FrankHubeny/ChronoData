"""------------------------------------------------------------------------------
                            Association Structure Tests
------------------------------------------------------------------------------"""

import pytest

from chronodata.chrono import Association, Chronology
from chronodata.g7 import Gedcom

testdata = [
    (
        'result1',
        '1 ASSO @1@\n2 PHRASE just joe\n3 ROLE HUSB\n3 PHRASE just a husband\n',
    ),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_family_individual(test_input: str, expected: str | int | bool) -> None:
    a = Chronology(name='testing')
    joe = a.individual_xref()
    assoc = Association(
        role=Gedcom.HUSB,
        association_phrase='just joe',
        role_phrase='just a husband',
    )
    result1 = a.association_structure(joe, assoc, 1)  # noqa: F841

    assert eval(test_input) == expected
