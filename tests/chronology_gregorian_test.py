"""------------------------------------------------------------------------------
                                Chronology Tests
------------------------------------------------------------------------------"""

import pytest

from chronodata.chronology import Chronology
from chronodata.utils.constants import String, Number, Msg, Datetime, Key, Calendar
    
"""------------------------------------------------------------------------------
                              Gregorian Chronology
------------------------------------------------------------------------------"""

testdata = [
    ############### Initial variables for a Gregorian chronology
    ('a.calendar', 'Gregorian'),
    ('a.poslabel', ' AD'),
    ('a.neglabel', ' BC'),
    ############### Calendar methods
    # check_date
    ('a.check_date("20 BC")', True),
    ('a.check_date("2000")', True),
    ('a.check_date("2000 AD")', True),
    ('a.check_date("2000 BC")', True),
    ('a.check_date("2000AD")', False),
    ('a.check_date("2000 ")', True),
    # date_diff
    ('a.date_diff("1000 AD", "1500 AD")', 500.0),
    ('a.date_diff("1000 BC", "1500 AD")', 2499.0),
    ('a.date_diff("1 BC", "1 AD")', 1.0),
    ('a.date_diff("1000 BC", "1000 AD", unit=Datetime.DAY)', 730120.0),
    # to_datetime64
    ('a.to_datetime64("1000 AD")', '1000'),
    ('a.to_datetime64("1000 BC")', '-999'),
    ('a.to_datetime64("1 BC")', '-0'),
    ('a.to_datetime64("1000000 BC")', '-999999'),
    ('a.to_datetime64("1000000 AD")', '1000000'),
    ('a.to_datetime64("1000000-06-03 05:21:50 BC")', '-999999-06-03 05:21:50'),
    ('a.to_datetime64("1000000-06-03 05:21:50 AD")', '1000000-06-03 05:21:50'),
    ('a.to_datetime64("1000000-06-03T05:21:50 BC")', '-999999-06-03T05:21:50'),
    ('a.to_datetime64("1000000-06-03T05:21:50 AD")', '1000000-06-03T05:21:50'),
    ('a.to_datetime64("2000-01-01 16:05:30 AD")', '2000-01-01 16:05:30'),
    ############### Dictionary methods
    #
    # Dictionaries
    #
    # Actors
    # add_actor
    #
    # Challenges
    # add_challenge
    #
    # Events
    # add_event
    #
    # Marker
    # add_marker
    #
    # Periods
    # add_period
    ('a.chronology["PERIODS"]["Period One"]', {'BEGIN': '1000 BC', 'END': '500 BC'}),
    ('a.chronology["PERIODS"]["Period Five"]["BEGIN"]', '2020-01-06 01:30:00 BC'),
    ('a.chronology["PERIODS"]["Current"]["Location"]', 'Here'),
    ('a.chronology["PERIODS"]["Current2"]["Where"]', 'There'),
    #
    # Texts
    # add_text
]

@pytest.mark.parametrize("input_n,expected", testdata)
def test_gregorian_calendar(input_n, expected):
    a = Chronology('newname')
    a.add_period('Period One', '1000 BC', '500 BC')
    a.add_period('Period Two', '1000 BC', '1000 AD')
    a.add_period('Period Three', '1000 AD', '2000 AD')
    a.add_period('Period Four', '2020-01-06 01:30:00 AD', '2024-02-05 23:15:40 AD')
    a.add_period('Period Five', '2020-01-06 01:30:00 BC', '2024-02-05 23:15:40 BC')
    a.add_period('Current', '2000 AD', '2100 AD', keyvalues={'Location' : 'Here'})
    a.add_period('Current2', '2000 AD', '2100 AD', keyvalues={'Location' : 'Here', 'Where' : 'There'})
    assert eval(input_n) == expected
    


