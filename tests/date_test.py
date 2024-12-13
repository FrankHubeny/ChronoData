"""------------------------------------------------------------------------------
                            Date Tests
------------------------------------------------------------------------------"""

import pytest

from chronodata.chrono import Chronology, Date, Time

testdata = [
  #  ('date', '01 JAN 2000'),
  #  ('time', '05:10:40Z'),
  #  ('date2', '01 JAN 2000'),
  #  ('time2', '05:10:40Z'),
  #  ('date3', '01 JAN 2000 BCE'),
  #  ('time3', '05:10:40Z'),
    ('creation_pieces[0][0]', '1'),
    ('creation_pieces[1][0]', '2'),
    ('creation_pieces[2][0]', '3'),
    ('creation_pieces[0][2:6]', 'CREA'),
    ('creation_pieces[1][2:6]', 'DATE'),
    ('creation_pieces[2][2:6]', 'TIME'),
    ('change_pieces[0]', '1 CHAN'),
    ('change_pieces[1][0:6]', '2 DATE'),
    ('change_pieces[2][0:6]', '3 TIME'),
  #  ('iso', '2000-01-01T05:10:40'),
  #  ('datevalue1[0]', '1 DATE 01 JAN 2000'),
  #  ('datevalue2[1]', '2 TIME 01:01:01'),
  #  ('datevalue3[1]', '2 PHRASE hello'),
  #  ('datevalue4[2]', '2 PHRASE hello'),
  #  ('datevalue5[1]', '6 PHRASE hello'),
  #  ('datetime[0][0:6]', '2 DATE'),
  #  ('datetime[1][0:6]', '3 TIME'),
    #####################
    ('d1.ged(1)', '1 DATE 01 JAN 2000\n'),
    ('d1.ged(10)', '10 DATE 01 JAN 2000\n'),
    ('d2.ged(1)', '1 DATE 2000 BCE\n'),

    ('t1.ged(1)', '1 TIME 04:30:10\n'),
    ('t2.ged(1)', '1 TIME 04:30:10Z\n'),
    ('t3.ged(10)', ''),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_date(test_input: str, expected: str | int | bool) -> None:
    a = Chronology(name='testing')
   # date, time = a.ged_date('2000-01-01T05:10:40')
   # date2, time2 = a.ged_date('-2000-01-01T05:10:40', epoch=False)
  #  date3, time3 = a.ged_date('-2000-01-01T05:10:40')
    creation_pieces: list[str] = a.creation_date().split('\n')  # noqa: F841
    change_pieces: list[str] = a.change_date().split('\n')  # noqa: F841
   # iso: str = a.iso_date(date, time)  # noqa: F841
   # datevalue1: list[str] = a.date_value(Date(2000,1,1)).split('\n')  # noqa: F841
   # datevalue2: list[str] = a.date_value(Date(2000,1,1), Time(1,1,1)).split('\n')  # noqa: F841
   # datevalue3: list[str] = a.date_value(Date(2000,1,1), phrase='hello').split(
   #     '\n'
   # )  # noqa: F841
   # datevalue4: list[str] = a.date_value(
   #     Date(2000,1,1), Time(1,1,1), 'hello'
   # ).split('\n')  # noqa: F841
   # datevalue5: list[str] = a.date_value(
   #     Date(2000,1,1), phrase='hello', level=5
  #  ).split(  # noqa: F841
   #     '\n'
  #  )
  #  datetime: list[str] = a.now().split('\n')  # noqa: F841

    ###################################
    d1 = Date(2000, 1, 1)
    d2 = Date(-2000)

    t1 = Time(4,30,10)
    t2 = Time(4,30,10,UTC=True)
    t3 = Time(0,10,10)

    assert eval(test_input) == expected
