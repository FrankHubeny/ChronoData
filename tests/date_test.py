"""------------------------------------------------------------------------------
                            Date Tests
------------------------------------------------------------------------------"""

import pytest

from chronodata.chrono import Chronology

testdata = [
    ('date', '01 JAN 2000'),
    ('time', '05:10:40Z'),
    ('date2', '01 JAN 2000'),
    ('time2', '05:10:40Z'),
    ('date3', '01 JAN 2000 BCE'),
    ('time3', '05:10:40Z'),
    ('creation_pieces[0][0]', '1'),
    ('creation_pieces[1][0]', '2'),
    ('creation_pieces[2][0]', '3'),
    ('creation_pieces[0][2:6]', 'CREA'),
    ('creation_pieces[1][2:6]', 'DATE'),
    ('creation_pieces[2][2:6]', 'TIME'),
    ('change_pieces[0]', '1 CHAN'),
    ('change_pieces[1][0:6]', '2 DATE'),
    ('change_pieces[2][0:6]', '3 TIME'),
    ('iso', '2000-01-01T05:10:40'),
    ('datevalue1[0]', '1 DATE 01 JAN 2000'),
    ('datevalue2[1]', '2 TIME 01:01:01'),
    ('datevalue3[1]', '2 PHRASE hello'),
    ('datevalue4[2]', '2 PHRASE hello'),
    ('datevalue5[1]', '6 PHRASE hello'),
    ('datetime[0][0:6]', '2 DATE'),
    ('datetime[1][0:6]', '3 TIME'),
]
@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_date(test_input: str, expected: str | int | bool) -> None:
    a = Chronology(name='testing')
    date, time = a.ged_date('2000-01-01T05:10:40')
    date2, time2 = a.ged_date('-2000-01-01T05:10:40', epoch=False)
    date3, time3 = a.ged_date('-2000-01-01T05:10:40')
    #creation: str = a.creation_date()
    creation_pieces: list = a.creation_date().split('\n')
    #change: str = a.change_date()
    change_pieces: list = a.change_date().split('\n')
    iso: str = a.iso_date(date, time)
    datevalue1 = a.date_value('01 JAN 2000').split('\n')
    datevalue2 = a.date_value('01 JAN 2000', '01:01:01').split('\n')
    datevalue3 = a.date_value('01 JAN 2000', phrase='hello').split('\n')
    datevalue4 = a.date_value('01 JAN 2000', '01:01:01', 'hello').split('\n')
    datevalue5 = a.date_value('01 JAN 2000', phrase='hello', level=5).split('\n')
    datetime = a.now().split('\n')
    
    assert eval(test_input) == expected