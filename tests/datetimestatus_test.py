"""------------------------------------------------------------------------------
                            Tag Tests

    This includes calls to format information that is tagged.
    - `taginfo`
    - `taginit`
------------------------------------------------------------------------------"""

import pytest

from chronodata.chrono import DateTimeStatus
from chronodata.g7 import Gedcom

testdata = [
    # ('result', '3 TIME here it is\n'),
    # ('result2', '0 DATE 12 JAN 2002\n'),
    # ('result3', '0 @1@ INDI\n'),
    # ('result4', '17 NOTE yes this is extra information\n'),
    # ('result5', '17 NOTE yes " this is extra information "\n'),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_datetimestatus(test_input: str, expected: str | int | bool) -> None:
    # result = a.taginfo(3, Gedcom.TIME, 'here it is')  # noqa: F841
    # result2 = a.taginfo(0, Gedcom.DATE, '12 JAN 2002')  # noqa: F841
    # result3 = a.taginit('@1@', Gedcom.INDI)  # noqa: F841
    # result4 = a.taginfo(17, Gedcom.NOTE, 'yes', 'this is extra information')  # noqa: F841
    # result5 = a.taginfo(17, Gedcom.NOTE, 'yes', '" this is extra information "')  # noqa: F841
    assert eval(test_input) == expected
