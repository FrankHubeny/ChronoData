# date_time_test.py
"""Tests to cover the DateExact, Date and Time substructures.

1. Validate: Exercise all validation checks.
    a. Good run.
    b. Catch exceptions.

2. Ged: Exercise the generation of ged data.
"""

import re

import pytest

from genedata.classes70 import (
    DataEvenDate,
    Date,
    DateExact,
    HeadDate,
    NoDate,
    Sdate,
    Time,
)
from genedata.constants import Default
from genedata.messages import Msg
from genedata.specifications70 import Specs

# 1. Validate: Exercise all validation checks.
#    a. Good run.


def test_data_even_date_year() -> None:
    assert DataEvenDate('FROM 2000 TO 2001').validate(specs=Specs)


def test_data_even_data_full() -> None:
    assert DataEvenDate('FROM JULIAN 1 JAN 2000 TO JULIAN 1 JAN 2001').validate(
        specs=Specs
    )


def test_data_even_date_just_to() -> None:
    assert DataEvenDate('TO 2001').validate(specs=Specs)


def test_date_just_year() -> None:
    assert Date('2000').validate(specs=Specs)


def test_sdate_just_year() -> None:
    assert Sdate('2000').validate(specs=Specs)


def test_date_cal_year() -> None:
    assert Date('CAL 2000').validate(specs=Specs)


def test_date_abt_year() -> None:
    assert Date('ABT 2000').validate(specs=Specs)


def test_date_est_year() -> None:
    assert Date('EST 2000').validate(specs=Specs)


def test_date_bef_year() -> None:
    assert Date('BEF 2000').validate(specs=Specs)


def test_date_aft_year() -> None:
    assert Date('AFT 2000').validate(specs=Specs)


def test_date_just_est_year() -> None:
    assert Date('EST 2000').validate(specs=Specs)


def test_date_just_bet_year() -> None:
    assert Date('BET 2000 AND 2001').validate(specs=Specs)


def test_date_just_from_year() -> None:
    assert Date('FROM 2000 TO 2001').validate(specs=Specs)


def test_date_just_to_year() -> None:
    assert Date('TO 2000').validate(specs=Specs)


def test_date_cal_full_year() -> None:
    assert Date('CAL GREGORIAN 1 JAN 2000 BCE').validate(specs=Specs)


def test_date_abt_full_year() -> None:
    assert Date('ABT GREGORIAN 1 JAN 2000 BCE').validate(specs=Specs)


def test_date_est_full_year() -> None:
    assert Date('EST GREGORIAN 1 JAN 2000 BCE').validate(specs=Specs)


def test_date_bef_full_year() -> None:
    assert Date('BEF GREGORIAN 1 JAN 2000 BCE').validate(specs=Specs)


def test_date_aft_full_year() -> None:
    assert Date('AFT GREGORIAN 1 JAN 2000 BCE').validate(specs=Specs)


def test_date_est_full_year2() -> None:
    assert Date('EST GREGORIAN 1 JAN 2000 BCE').validate(specs=Specs)


def test_date_bet_full_year() -> None:
    assert Date(
        'BET GREGORIAN 1 JAN 2000 BCE AND GREGORIAN 1 JAN 2001 BCE'
    ).validate(specs=Specs)


def test_date_from_full_year() -> None:
    assert Date(
        'FROM GREGORIAN 1 JAN 2000 BCE TO GREGORIAN 1 JAN 2001 BCE'
    ).validate(specs=Specs)


def test_date_to_full_year() -> None:
    assert Date('TO GREGORIAN 1 JAN 2000 BCE').validate(specs=Specs)


def test_date_just_cal_year() -> None:
    assert Date('CAL 2000').validate(specs=Specs)


def test_date_just_abt_year() -> None:
    assert Date('ABT 2000').validate(specs=Specs)


def test_date_just_bef_year() -> None:
    assert Date('BEF 2000').validate(specs=Specs)


def test_date_just_aft_year() -> None:
    assert Date('AFT 2000').validate(specs=Specs)


def test_date_just_year_epoch() -> None:
    assert Date('2000 BCE').validate(specs=Specs)


def test_date_just_est_year_epoch() -> None:
    assert Date('EST 2000 BCE').validate(specs=Specs)


def test_date_just_cal_year_epoch() -> None:
    assert Date('CAL 2000 BCE').validate(specs=Specs)


def test_date_just_abt_year_epoch() -> None:
    assert Date('ABT 2000 BCE').validate(specs=Specs)


def test_date_just_bef_year_epoch() -> None:
    assert Date('BEF 2000 BCE').validate(specs=Specs)


def test_date_just_aft_year_epoch() -> None:
    assert Date('AFT 2000 BCE').validate(specs=Specs)


def test_date_just_fullyear() -> None:
    assert Date('1 JAN 2000').validate(specs=Specs)


def test_date_just_est_fullyear() -> None:
    assert Date('EST 1 JAN 2000').validate(specs=Specs)


def test_date_just_cal_fullyear() -> None:
    assert Date('CAL 1 JAN 2000').validate(specs=Specs)


def test_date_just_abt_fullyear() -> None:
    assert Date('ABT 1 JAN 2000').validate(specs=Specs)


def test_date_just_bef_fullyear() -> None:
    assert Date('BEF 1 JAN 2000').validate(specs=Specs)


def test_date_just_aft_fullyear() -> None:
    assert Date('AFT 1 JAN 2000').validate(specs=Specs)


def test_date_just_monthyear() -> None:
    assert Date('1 JAN 2000').validate(specs=Specs)


def test_date_just_est_monthyear() -> None:
    assert Date('EST JAN 2000').validate(specs=Specs)


def test_date_just_cal_monthyear() -> None:
    assert Date('CAL JAN 2000').validate(specs=Specs)


def test_date_just_abt_monthyear() -> None:
    assert Date('ABT JAN 2000').validate(specs=Specs)


def test_date_just_bef_monthyear() -> None:
    assert Date('BEF JAN 2000').validate(specs=Specs)


def test_date_just_aft_monthyear() -> None:
    assert Date('AFT JAN 2000').validate(specs=Specs)


def test_date_just_julian_year() -> None:
    assert Date('JULIAN 1 JAN 2000').validate(specs=Specs)


def test_date_just_est_julian_year() -> None:
    assert Date('EST JULIAN 1 JAN 2000').validate(specs=Specs)


def test_date_just_cal_julian_year() -> None:
    assert Date('CAL JULIAN 1 JAN 2000').validate(specs=Specs)


def test_date_just_abt_julian_year() -> None:
    assert Date('ABT JULIAN 1 JAN 2000').validate(specs=Specs)


def test_date_just_bef_julian_year() -> None:
    assert Date('BEF JULIAN 1 JAN 2000').validate(specs=Specs)


def test_date_just_aft_julian_year() -> None:
    assert Date('AFT JULIAN 1 JAN 2000').validate(specs=Specs)


def test_date_just_julian_fullyear() -> None:
    assert Date('GREGORIAN 1 JAN 2000 BCE').validate(specs=Specs)


def test_date_just_est_julian_fullyear() -> None:
    assert Date('EST GREGORIAN 1 JAN 2000 BCE').validate(specs=Specs)


def test_date_just_cal_julian_fullyear() -> None:
    assert Date('CAL GREGORIAN 1 JAN 2000 BCE').validate(specs=Specs)


def test_date_just_abt_julian_fullyear() -> None:
    assert Date('ABT GREGORIAN 1 JAN 2000 BCE').validate(specs=Specs)


def test_date_just_bef_julian_fullyear() -> None:
    assert Date('BEF GREGORIAN 1 JAN 2000 BCE').validate(specs=Specs)


def test_date_just_aft_julian_fullyear() -> None:
    assert Date('AFT GREGORIAN 1 JAN 2000 BCE').validate(specs=Specs)


def test_date_empty() -> None:
    assert Date('').validate(specs=Specs)


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


def test_date_not_string() -> None:
    m = Date(12345)  # type: ignore[arg-type]
    with pytest.raises(
        ValueError,
        match=re.escape(Msg.NOT_STRING.format(str(m.value), m.class_name)),
    ):
        m.validate(specs=Specs)


def test_date_not_gregorian_month() -> None:
    m = Date('1 XYZ 2000')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_MONTH.format(
                m.value,
                m.class_name,
                str(
                    [
                        'APR',
                        'AUG',
                        'DEC',
                        'FEB',
                        'JAN',
                        'JUL',
                        'JUN',
                        'MAR',
                        'MAY',
                        'NOV',
                        'OCT',
                        'SEP',
                    ]
                ),
            )
        ),
    ):
        m.validate(specs=Specs)


def test_date_not_julian_month() -> None:
    m = Date('JULIAN 1 XYZ 2000')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_MONTH.format(
                m.value,
                m.class_name,
                str(
                    [
                        'APR',
                        'AUG',
                        'DEC',
                        'FEB',
                        'JAN',
                        'JUL',
                        'JUN',
                        'MAR',
                        'MAY',
                        'NOV',
                        'OCT',
                        'SEP',
                    ]
                ),
            )
        ),
    ):
        m.validate(specs=Specs)


def test_date_not_hebrew_month() -> None:
    m = Date('HEBREW 1 XYZ 2000')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_MONTH.format(
                m.value,
                m.class_name,
                str(['AAV', 'ADR', 'ADS', 'CSH', 'ELL', 'IYR', 'KSL', 'NSN', 'SHV', 'SVN', 'TMZ', 'TSH', 'TVT']),
            )
        ),
    ):
        m.validate(specs=Specs)


def test_date_not_month_day_high() -> None:
    m = Date('32 JAN 2000')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_EXACT_DAY.format(
                m.value,
                m.class_name,
                str(32),
                str(31),
            )
        ),
    ):
        m.validate(specs=Specs)


def test_date_not_month_day_low() -> None:
    m = Date('0 JAN 2000')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_EXACT_DAY.format(
                m.value,
                m.class_name,
                str(0),
                str(31),
            )
        ),
    ):
        m.validate(specs=Specs)


def test_date_not_feb_day_high_leapyear() -> None:
    m = Date('30 FEB 2004')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_EXACT_DAY.format(
                m.value,
                m.class_name,
                str(30),
                str(29),
            )
        ),
    ):
        m.validate(specs=Specs)


def test_date_not_feb_day_high() -> None:
    m = Date('29 FEB 2000')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_EXACT_DAY.format(
                m.value,
                m.class_name,
                str(29),
                str(28),
            )
        ),
    ):
        m.validate(specs=Specs)


def test_date_not_feb_day_low() -> None:
    m = Date('0 FEB 2000')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_EXACT_DAY.format(
                m.value,
                m.class_name,
                str(0),
                str(28),
            )
        ),
    ):
        m.validate(specs=Specs)


def test_date_not_feb_day_julian_high_leapyear() -> None:
    m = Date('JULIAN 29 FEB 2002')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_EXACT_DAY.format(
                m.value,
                m.class_name,
                str(29),
                str(28),
            )
        ),
    ):
        m.validate(specs=Specs)


def test_date_not_feb_day_julian_high() -> None:
    m = Date('JULIAN 30 FEB 2000')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_EXACT_DAY.format(
                m.value,
                m.class_name,
                str(30),
                str(29),
            )
        ),
    ):
        m.validate(specs=Specs)


def test_date_not_feb_day_julian_low() -> None:
    m = Date('JULIAN 0 FEB 2000')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_EXACT_DAY.format(
                m.value,
                m.class_name,
                str(0),
                str(29),
            )
        ),
    ):
        m.validate(specs=Specs)


def test_date_bad_epoch() -> None:
    m = Date('1 JAN 2000 XYZ')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_EPOCH.format(m.value, m.class_name, str(['BCE']))
        ),
    ):
        m.validate(specs=Specs)


def test_date_zero_year() -> None:
    m = Date('1 JAN 0')
    with pytest.raises(
        ValueError,
        match=re.escape(Msg.NOT_DATE_ZERO_YEAR.format(m.value, m.class_name)),
    ):
        m.validate(specs=Specs)


def test_date_only_zero_year() -> None:
    m = Date('0')
    with pytest.raises(
        ValueError,
        match=re.escape(Msg.NOT_DATE_ZERO_YEAR.format(m.value, m.class_name)),
    ):
        m.validate(specs=Specs)


def test_dateexact_not_string() -> None:
    m = DateExact(12345)  # type: ignore[arg-type]
    with pytest.raises(
        ValueError,
        match=re.escape(Msg.NOT_STRING.format(str(m.value), m.class_name)),
    ):
        m.validate()


def test_not_dateexact_lowercase() -> None:
    m = DateExact('1 JAn 2000')
    assert m.ged() == '1 DATE 1 JAN 2000\n'
    # with pytest.raises(
    #     ValueError,
    #     match=re.escape(Msg.NOT_DATE_EXACT.format(str(m.value), m.class_name)),
    # ):
    #     m.validate()


def test_not_dateexact_no_digit() -> None:
    m = DateExact(' JAN ')
    with pytest.raises(
        ValueError,
        match=re.escape(Msg.NOT_DATE_EXACT.format(str(m.value), m.class_name)),
    ):
        m.validate()


def test_not_dateexact_extra_space() -> None:
    m = DateExact('1 JAN 2000 BCE')
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_EXACT_SPACES.format(
                m.value, m.class_name, str(3), Default.DATE_EXACT_SPACES
            )
        ),
    ):
        m.validate()


def test_not_dateexact_two_spaces_needed() -> None:
    m = DateExact('1JAN 2000')
    with pytest.raises(
        ValueError,
        match=re.escape(Msg.NOT_DATE_EXACT_SPACES.format(m.value, m.class_name, str(1), str(2))),
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


def test_not_dateevendate_not_est() -> None:
    m = DataEvenDate('EST 1 JAN 2000')
    with pytest.raises(
        ValueError,
        match=re.escape(Msg.NOT_DATE_PERIOD.format(m.value, m.class_name)),
    ):
        m.validate()


def test_not_nodate_not_bet_and() -> None:
    m = NoDate('BET 1 JAN 2000 AND 2 JAN 2000')
    with pytest.raises(
        ValueError,
        match=re.escape(Msg.NOT_DATE_PERIOD.format(m.value, m.class_name)),
    ):
        m.validate()


def test_time_not_string() -> None:
    m = Time(12345)  # type: ignore[arg-type]
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
