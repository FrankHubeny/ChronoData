# date_time_test.py
"""Tests to cover the DateExact, Date and Time substructures.

1. Validate: Exercise all validation checks.
    a. Good run.
    b. Catch exceptions.

2. Ged: Exercise the generation of ged data.
"""

import re

import pytest

from genedata.classes70 import Date, DateExact, HeadDate, Time
from genedata.constants import Default
from genedata.messages import Msg

# 1. Validate: Exercise all validation checks.
#    a. Good run.


def test_dateexact_nozero() -> None:
    assert DateExact('1 JAN 2000').validate()


def test_dateexact_zero() -> None:
    assert DateExact('01 JAN 2000').validate()


def test_headdate_nozero() -> None:
    assert HeadDate('1 JAN 2000').validate()


def test_headdate_zero() -> None:
    assert HeadDate('01 JAN 2000').validate()


def test_time_nozero() -> None:
    assert Time('2:30').validate()


def test_time_zero() -> None:
    assert Time('02:30').validate()


def test_time_seconds_int() -> None:
    assert Time('2:30:30').validate()


def test_time_seconds_float() -> None:
    assert Time('2:30:30.5').validate()


def test_time_seconds_float_utc() -> None:
    assert Time('2:30:30.5Z').validate()


#    a. Catch exceptions.


def test_dateexact_not_string() -> None:
    m = DateExact(12345)
    with pytest.raises(
        ValueError,
        match=re.escape(Msg.NOT_STRING.format(str(m.value), m.class_name)),
    ):
        m.validate()


def test_not_dateexact_lowercase() -> None:
    m = DateExact('1 JAn 2000')
    with pytest.raises(
        ValueError,
        match=re.escape(Msg.NOT_DATE_EXACT.format(str(m.value), m.class_name)),
    ):
        m.validate()


def test_not_dateexact_no_digit() -> None:
    m = DateExact(' JAN ')
    with pytest.raises(
        ValueError,
        match=re.escape(Msg.NOT_DATE_EXACT.format(str(m.value), m.class_name)),
    ):
        m.validate()


def test_not_dateexact_too_large() -> None:
    m = DateExact('01 JAN -2000 ')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_EXACT_TOO_LARGE.format(
                m.value, m.class_name, 13, Default.DATE_EXACT_MAX_SIZE
            )
        ),
    ):
        m.validate()


def test_not_dateexact_extra_space() -> None:
    m = DateExact('1 JAN 2000 ')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_EXACT_SPACES.format(
                m.value, m.class_name, str(3), Default.DATE_EXACT_SPACES
            )
        ),
    ):
        m.validate()


def test_not_dateexact_too_few_spaces() -> None:
    m = DateExact('1JAN 2000')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_EXACT_SPACES.format(
                m.value,
                m.class_name,
                str(1),
                Default.DATE_EXACT_SPACES,
            )
        ),
    ):
        m.validate()


def test_not_dateexact_month() -> None:
    m = DateExact('1 JA 2000')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_EXACT_MONTH.format(
                m.value,
                m.class_name,
                'JA',
            ),
        ),
    ):
        m.validate()


def test_not_dateexact_day_zero() -> None:
    m = DateExact('0 JAN 2000')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_EXACT_DAY.format(
                m.value,
                m.class_name,
                '0',
                '31',
            ),
        ),
    ):
        m.validate()


def test_not_dateexact_day_32() -> None:
    m = DateExact('32 JAN 2000')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_EXACT_DAY.format(
                m.value,
                m.class_name,
                '32',
                '31',
            ),
        ),
    ):
        m.validate()


def test_not_dateexact_feb_not_leapyear() -> None:
    m = DateExact('29 FEB 2001')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_EXACT_DAY.format(
                m.value,
                m.class_name,
                '29',
                '28',
            ),
        ),
    ):
        m.validate()


def test_not_dateexact_feb_leapyear() -> None:
    m = DateExact('30 FEB 2004')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_EXACT_DAY.format(
                m.value,
                m.class_name,
                '30',
                '29',
            ),
        ),
    ):
        m.validate()


def test_not_dateexact_year_zero() -> None:
    m = DateExact('15 FEB 0')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_EXACT_YEAR.format(m.value, m.class_name, '0')
        ),
    ):
        m.validate()


def test_time_not_string() -> None:
    m = Time(12345)
    with pytest.raises(
        ValueError,
        match=re.escape(Msg.NOT_STRING.format(str(m.value), m.class_name)),
    ):
        m.validate()


def test_not_time() -> None:
    m = Time('abcde')
    with pytest.raises(
        ValueError,
        match=re.escape(Msg.NOT_TIME.format(str(m.value), m.class_name)),
    ):
        m.validate()


def test_not_time_colon_count() -> None:
    m = Time('01:01:02:')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_TIME_COLON_COUNT.format(str(m.value), m.class_name, str(3))
        ),
    ):
        m.validate()


def test_not_time_zero_colon_count() -> None:
    m = Time('010102')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_TIME_COLON_COUNT.format(str(m.value), m.class_name, str(0))
        ),
    ):
        m.validate()


def test_not_time_negative_hours() -> None:
    m = Time('-1:01:02.1')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_TIME_HOURS.format(
                m.value,
                m.class_name,
                str(-1),
                Default.TIME_MIN_HOUR,
                Default.TIME_MAX_HOUR,
            )
        ),
    ):
        m.validate()


def test_not_time_over_24_hours() -> None:
    m = Time('24:01:02.1')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_TIME_HOURS.format(
                m.value,
                m.class_name,
                str(24),
                Default.TIME_MIN_HOUR,
                Default.TIME_MAX_HOUR,
            )
        ),
    ):
        m.validate()

def test_not_time_negative_minutes() -> None:
    m = Time('01:-1:02.1')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_TIME_MINUTES.format(
                m.value,
                m.class_name,
                str(-1),
                Default.TIME_MIN_MINUTE,
                Default.TIME_MAX_MINUTE,
            )
        ),
    ):
        m.validate()


def test_not_time_over_59_minutes() -> None:
    m = Time('01:60:02.1')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_TIME_MINUTES.format(
                m.value,
                m.class_name,
                str(60),
                Default.TIME_MIN_MINUTE,
                Default.TIME_MAX_MINUTE,
            )
        ),
    ):
        m.validate()

def test_not_time_negative_seconds() -> None:
    m = Time('01:01:-1.1')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_TIME_SECONDS.format(
                m.value,
                m.class_name,
                str(-1.1),
                Default.TIME_MIN_SECOND,
                Default.TIME_MAX_SECOND,
            )
        ),
    ):
        m.validate()


def test_not_time_over_or_equal_60_seconds() -> None:
    m = Time('01:50:60.0')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_TIME_SECONDS.format(
                m.value,
                m.class_name,
                str(60.0),
                Default.TIME_MIN_SECOND,
                Default.TIME_MAX_SECOND,
            )
        ),
    ):
        m.validate()
