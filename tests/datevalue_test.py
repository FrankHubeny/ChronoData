"""------------------------------------------------------------------------------
                            DaveValue NamedTuple Class Tests

    Reference
    ---------
    >n DATE <DateValue>                         {1:1}  g7:DATE
    >  +1 TIME <Time>                           {0:1}  g7:TIME
    >  +1 PHRASE <Text>                         {0:1}  g7:PHRASE

------------------------------------------------------------------------------"""

import pytest

from chronodata.build import Date, DateValue, Time
from chronodata.messages import Msg

testdata = [
    ('dv1.ged(1)', '1 DATE 01 DEC 2000\n2 TIME 10:10:10\n'),
    ('dv2.ged(1)', '1 DATE 01 DEC 2000\n'),
    (
        'dv3.ged(1)',
        '1 DATE 01 DEC 2000\n2 TIME 10:10:10Z\n2 PHRASE date-time\n',
    ),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_time(test_input: str, expected: str | int | bool) -> None:
    dv1 = DateValue(Date(2000, 12, 1), Time(10, 10, 10))  # noqa: F841
    dv2 = DateValue(Date(2000, 12, 1))  # noqa: F841
    dv3 = DateValue(Date(2000, 12, 1), Time(10, 10, 10, UTC=True), 'date-time')  # noqa: F841

    assert eval(test_input) == expected


def test_zero_year() -> None:
    with pytest.raises(
        ValueError, match=Msg.NO_ZERO_YEAR.format(0, 'GREGORIAN')
    ):
        DateValue(Date(0, 0, 0), Time(10, 10, 10, UTC=True), 'date-time').ged(1)
