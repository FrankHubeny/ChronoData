"""------------------------------------------------------------------------------
                            Chrono(logy) Tests

    These texts cover the `chrono` module which gathers together the data
    constructed from the `tuples` module and sends it to the `core` module for 
    storing.

------------------------------------------------------------------------------"""

import pytest

from chronodata.chrono import Chronology
from chronodata.tuples import Family, Individual

testdata = [
    ('str(joe)', 'JOE'),
    ('str(mary)', 'MARY'),
    ('str(joe_mary)', 'JOE & MARY'),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_chrono(test_input: str, expected: str | int | bool) -> None:
    a = Chronology('test')
    joe = a.individual_xref('joe')  # noqa: F841
    mary = a.individual_xref('mary')  # noqa: F841
    joe_mary = a.family_xref('joe & mary')  # noqa: F841


    assert eval(test_input) == expected
