"""------------------------------------------------------------------------------
                                Chronology Tests
------------------------------------------------------------------------------"""

import pytest

from chronodata.chronology import Chronology, KEYS, CALENDARS, CONSTANTS, DATETIMES

"""------------------------------------------------------------------------------
                                   Constants
------------------------------------------------------------------------------"""

testdata = [
    ############### Constants
    # keys
    ('KEYS["EVENTS"]', 'EVENTS'),
    ('KEYS["ACTORS"]', 'ACTORS'),
    ('KEYS["BEFOREPRESENT"]', 'Before Present'),
    ('KEYS["BEGIN"]', 'BEGIN'),
    ('KEYS["BIRTH"]', 'BIRTH'),
    ('KEYS["CALENDAR"]', 'CALENDAR'),
    ('KEYS["CHALLENGES"]', 'CHALLENGES'),
    ('KEYS["DATE"]', 'DATE'),
    ('KEYS["DEATH"]', 'DEATH'),
    ('KEYS["DESCRIPTION"]', 'DESCRIPTION'),
    ('KEYS["END"]', 'END'),
    ('KEYS["EVENTS"]', 'EVENTS'),
    ('KEYS["EXPERIMENT"]', 'Experiment'),
    ('KEYS["FATHER"]', 'FATHER'),
    ('KEYS["FEMALE"]', 'FEMALE'),
    ('KEYS["FILE"]', 'FILENAME'),
    ('KEYS["GREGORIAN"]', 'Gregorian'),
    ('KEYS["MALE"]', 'MALE'),
    ('KEYS["MARKERS"]', 'MARKERS'),
    ('KEYS["MOTHER"]', 'MOTHER'),
    ('KEYS["NAME"]', 'NAME'),
    ('KEYS["NEGLABEL"]', 'NEG LABEL'),
    ('KEYS["OVERVIEW"]', 'OVERVIEW'),
    ('KEYS["PERIODS"]', 'PERIODS'),
    ('KEYS["POSLABEL"]', 'POS LABEL'),
    ('KEYS["SECULAR"]', 'Secular'),
    ('KEYS["TEXTS"]', 'TEXTS'),
    ('KEYS["USEZERO"]', 'USE ZERO'),
    ('KEYS["ZEROYEAR"]', 'ZERO YEAR'),
    # calendars
    ('CALENDARS["Gregorian"]["NAME"]', 'Gregorian'),
    ('CALENDARS[KEYS["GREGORIAN"]]["NAME"]', 'Gregorian'),
    ('CALENDARS[KEYS["SECULAR"]]["NAME"]', 'Secular'),
    ('CALENDARS[KEYS["BEFOREPRESENT"]]["NAME"]', 'Before Present'),
    ('CALENDARS[KEYS["EXPERIMENT"]]["NAME"]', 'Experiment'),
    # constants
    ('CONSTANTS["DATETIME_EPOCH"]', 1970),
    ('CONSTANTS["LEFTBRACE"]', '{'),
    ('CONSTANTS["NEGATIVE"]', '-'),
    ('CONSTANTS["NEWLINE"]', '\n'),
    ('CONSTANTS["SPACE"]', ' '),
    # datetimes
    ('DATETIMES["ATTOSECOND"]', 'as'),
    ('DATETIMES["DAY"]', 'D'),
    ('DATETIMES["FEMTOSECOND"]', 'fs'),
    ('DATETIMES["HOUR"]', 'h'),
    ('DATETIMES["MICROSECOND"]', 'us'),
    ('DATETIMES["MILLISECOND"]', 'ms'),
    ('DATETIMES["MINUTE"]', 'm'),
    ('DATETIMES["MONTH"]', 'M'),
    ('DATETIMES["NANOSECOND"]', 'ns'),
    ('DATETIMES["PICOSECOND"]', 'ps'),
    ('DATETIMES["SECOND"]', 's'),
    ('DATETIMES["WEEK"]', 'W'),
    ('DATETIMES["YEAR"]', 'Y'),
]

@pytest.mark.parametrize("input_n,expected", testdata)
def test_constants(input_n, expected):
    assert eval(input_n) == expected
    
"""------------------------------------------------------------------------------
                              Gregorian Chronology
------------------------------------------------------------------------------"""

testdata = [
    ############### Initial variables for a Gregorian chronology
    ('a.name', 'newname'),
    ('a.calendar', 'Gregorian'),
    ('a.poslabel', ' AD'),
    ('a.neglabel', ' BC'),
    ('len(a.chronology)', 7),
    #
    ############### Calendar methods
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
    # date_diff
    ('a.date_diff("1000 AD", "1500 AD")', 500.0),
    ('a.date_diff("1000 BC", "1500 AD")', 2499.0),
    ('a.date_diff("1 BC", "1 AD")', 1.0),
    ('a.date_diff("1000 BC", "1000 AD", unit=DATETIMES["DAY"])', 730120.0),
    #
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
    a.add_period('Period Four', '2020-01-06 01:30:00 AD', '2024-02-05 23:15:4 AD')
    a.add_period('Period Five', '2020-01-06 01:30:00 BC', '2024-02-05 23:15:4 BC')
    a.add_period('Current', '2000 AD', '2100 AD', keyvalues={'Location' : 'Here'})
    a.add_period('Current2', '2000 AD', '2100 AD', keyvalues={'Location' : 'Here', 'Where' : 'There'})
    assert eval(input_n) == expected
    


"""------------------------------------------------------------------------------
                              Secular Chronology
------------------------------------------------------------------------------"""

# Clean test
testdata = [
    ############### Initial variables for a Gregorian chronology
    ('a.name', 'newname'),
    ('a.calendar', 'Secular'),
    ('a.poslabel', ' CE'),
    ('a.neglabel', ' BCE'),
    ('len(a.chronology)', 7),
    #
    ############### Calendar methods
    # to_datetime64
    ('a.to_datetime64("1000 CE")', '1000'),
    ('a.to_datetime64("1000 BCE")', '-999'),
    ('a.to_datetime64("1 BCE")', '-0'),
    ('a.to_datetime64("1000000 BCE")', '-999999'),
    ('a.to_datetime64("1000000 CE")', '1000000'),
    ('a.to_datetime64("1000000-06-03 05:21:50 BCE")', '-999999-06-03 05:21:50'),
    ('a.to_datetime64("1000000-06-03 05:21:50 CE")', '1000000-06-03 05:21:50'),
    ('a.to_datetime64("1000000-06-03T05:21:50 BCE")', '-999999-06-03T05:21:50'),
    ('a.to_datetime64("1000000-06-03T05:21:50 CE")', '1000000-06-03T05:21:50'),
    ('a.to_datetime64("2000-01-01 16:05:30 CE")', '2000-01-01 16:05:30'),
    # date_diff
    ('a.date_diff("1000 CE", "1500 CE")', 500.0),
    ('a.date_diff("1000 BCE", "1500 CE")', 2499.0),
    ('a.date_diff("1 BCE", "1 CE")', 1.0),
    ('a.date_diff("1000 BCE", "1000 CE", unit=DATETIMES["DAY"])', 730120.0),
    #
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
    ## add_period
    ('a.chronology["PERIODS"]["Period One"]', {'BEGIN': '1000 BCE', 'END': '500 BCE'}),
    ('a.chronology["PERIODS"]["Period Five"]["BEGIN"]', '2020-01-06 01:30:00 BCE'),
    #
    # Texts
    # add_text
]

@pytest.mark.parametrize("input_n,expected", testdata)
def test_secular_calendar(input_n, expected):
    a = Chronology('newname', calendar=KEYS['SECULAR'])
    a.add_period('Period One', '1000 BCE', '500 BCE')
    a.add_period('Period Two', '1000 BCE', '1000 CE')
    a.add_period('Period Three', '1000 CE', '2000 CE')
    a.add_period('Period Four', '2020-01-06 01:30:00 CE', '2024-02-05 23:15:4 CE')
    a.add_period('Period Five', '2020-01-06 01:30:00 BCE', '2024-02-05 23:15:4 BCE')
    assert eval(input_n) == expected
    
