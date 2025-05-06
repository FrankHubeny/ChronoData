# validate_test.py
"""Tests to cover the Validate class."""

import re

import pytest

import genedata.classes70 as gc
from genedata.build import Genealogy
from genedata.constants import Default
from genedata.messages import Msg
from genedata.methods import Validate
from genedata.specifications70 import Specs
from genedata.structure import Void


# age tests
def test_age() -> None:
    assert Validate.age('< 30y', 'Age')


def test_bad_age_1() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_AGE.format('!', 'Age'),
    ):
        Validate.age('!', 'Age')


def test_bad_age_2() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_AGE.format('yy', 'Age'),
    ):
        Validate.age('yy', 'Age')


def test_bad_age_3() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_AGE.format('ab9', 'Age'),
    ):
        Validate.age('ab9', 'Age')


def test_bad_age_4() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_AGE.format('< y', 'Age'),
    ):
        Validate.age('< y', 'Age')


def test_bad_age_5() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_AGE.format(1234, 'Age'),
    ):
        Validate.age(str(1234), 'Age')


def test_clean_value_1() -> None:
    assert (
        Validate.clean_value(
            ' 1  JAN   2000 ', 'https://gedcom.io/terms/v7/type-Date#exact'
        )
        == '1 JAN 2000'
    )


# clean_value tests
def test_clean_value_2() -> None:
    assert (
        Validate.clean_value(
            'a,b,   c,d,    ', 'https://gedcom.io/terms/v7/type-List#Text'
        )
        == 'a, b, c, d,'
    )


def test_clean_value_3() -> None:
    assert (
        Validate.clean_value(
            '      ABC', 'https://gedcom.io/terms/v7/type-Enum'
        )
        == 'ABC'
    )


def test_clean_value_4() -> None:
    assert Validate.clean_value('  y  ', 'Y|<NULL>') == 'Y'


# date tests
def test_date_abt() -> None:
    assert Validate.date('ABT 2000', 'Date', Specs)


def test_date_aft() -> None:
    assert Validate.date('AFT 2000', 'Date', Specs)


def test_date_bef() -> None:
    assert Validate.date('BEF 2000', 'Date', Specs)


def test_date_cal() -> None:
    assert Validate.date('CAL 2000', 'Date', Specs)


def test_date_est() -> None:
    assert Validate.date('EST 2000', 'Date', Specs)


def test_date_to() -> None:
    assert Validate.date('TO 2000', 'Date', Specs)


def test_date_bet_and() -> None:
    assert Validate.date('BET 2000 AND 2001', 'Date', Specs)


def test_date_from_to() -> None:
    assert Validate.date('FROM 2000 TO 2001', 'Date', Specs)


# date_exact tests
def test_date_exact() -> None:
    assert Validate.date_exact('1 JAN 2000', 'DateExact')


def test_date_exact_leapyear() -> None:
    assert Validate.date_exact('29 FEB 2004', 'DateExact')


def test_date_exact_lowercase_ok() -> None:
    m = gc.DateExact('29 feb 2004')
    assert m.validate()


def test_date_exact_no_numbers() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_DATE_EXACT.format('A BCD EFGH', 'DateExact')
    ):
        Validate.date_exact('A BCD EFGH', 'DateExact')


def test_date_exact_too_many_spaces() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_DATE_EXACT_SPACES.format(
            '1 JAN 2000 BC', 'DateExact', str(3), str(2)
        ),
    ):
        Validate.date_exact('1 JAN 2000 BC', 'DateExact')


def test_date_exact_too_few_spaces() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_DATE_EXACT_SPACES.format(
            'JAN 2000', 'DateExact', str(1), str(2)
        ),
    ):
        Validate.date_exact('JAN 2000', 'DateExact')


# date_general tests
def test_date_general_four_spaces() -> None:
    assert Validate.date_general('GREGORIAN 1 JAN 2000 BCE', 'Date', Specs)


def test_date_general_four_spaces_julian() -> None:
    assert Validate.date_general('JULIAN 1 JAN 2000 BCE', 'Date', Specs)


def test_date_general_three_spaces_epoch() -> None:
    assert Validate.date_general('1 JAN 2000 BCE', 'Date', Specs)


def test_date_general_three_spaces_calendar() -> None:
    assert Validate.date_general('JULIAN 1 JAN 2000', 'Date', Specs)


def test_date_general_two_spaces() -> None:
    assert Validate.date_general('1 JAN 2000', 'Date', Specs)


def test_date_general_two_spaces_calendar_epoch() -> None:
    assert Validate.date_general('GREGORIAN 2000 BCE', 'Date', Specs)


def test_date_general_one_space_calendar() -> None:
    assert Validate.date_general('GREGORIAN 2000', 'Date', Specs)


def test_date_general_one_space_epoch() -> None:
    assert Validate.date_general('2000 BCE', 'Date', Specs)


def test_date_general_no_space() -> None:
    assert Validate.date_general('2000', 'Date', Specs)


def test_date_general_empty() -> None:
    assert Validate.date_general('', 'Date', Specs)

def test_date_general_leapyear() -> None:
    assert Validate.date_general('29 FEB 2004', 'Date', Specs)


def test_date_calendar_month_extension() -> None:
    mycalendar: str = (
        'tests/data/extension_tests/calendars/cal-_MYGREGORIAN.yaml'
    )
    myjan: str = 'tests/data/extension_tests/months/month-_MYJAN.yaml'
    g = Genealogy()
    g.document_tag('_MYGREGORIAN', mycalendar)
    g.document_tag('_MYJAN', myjan)
    assert gc.Date('_MYGREGORIAN 1 _MYJAN 2000 BC').validate(
        specs=g.specification
    )

def test_date_calendar_month_extension_tag_in_list() -> None:
    mycalendar: str = (
        'tests/data/extension_tests/calendars/cal-_MYGREGORIANLIST.yaml'
    )
    myjan: str = 'tests/data/extension_tests/months/month-_MYJANLIST.yaml'
    g = Genealogy()
    g.document_tag('_MYGREGORIANLIST', mycalendar)
    g.document_tag('_MYJAN', myjan)
    assert gc.Date('_MYGREGORIANLIST 1 _MYJANLIST 2000 BC').validate(
        specs=g.specification
    )


def test_bad_date_general_not_string_int() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_STRING.format(repr(123), 'Date')
    ):
        Validate.date_general(123, 'Date', Specs)


def test_bad_calendar() -> None:
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_CALENDAR.format(
                'XYZ 1 JAN 2000 BCE',
                'Date',
                'XYZ',
                ['FRENCH_R', 'GREGORIAN', 'HEBREW', 'JULIAN'],
            )
        ),
    ):
        gc.Date('XYZ 1 JAN 2000 BCE').validate()

def test_bad_calendar_shorter() -> None:
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_CALENDAR.format(
                'XYZ 2000 BCE',
                'Date',
                'XYZ',
                ['FRENCH_R', 'GREGORIAN', 'HEBREW', 'JULIAN'],
            )
        ),
    ):
        gc.Date('XYZ 2000 BCE').validate()


def test_bad_date_general_not_string_xref() -> None:
    with pytest.raises(
        ValueError,
        match=re.escape(Msg.NOT_STRING.format(repr(Void.FAM), 'Date')),
    ):
        Validate.date_general(Void.FAM, 'Date', Specs)


def test_bad_date_general_not_string_none() -> None:
    with pytest.raises(
        ValueError, match=re.escape(Msg.NOT_STRING.format(repr(None), 'Date'))
    ):
        Validate.date_general(None, 'Date', Specs)


def test_bad_date_general_not_month() -> None:
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_MONTH.format(
                '1 XYZ 2000',
                'Date',
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
        Validate.date_general('1 XYZ 2000', 'Date', Specs)


def test_bad_date_general_calendar() -> None:
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_CALENDAR.format(
                'SOMETHING 1 JAN 2000',
                'Date',
                'SOMETHING',
                ['FRENCH_R', 'GREGORIAN', 'HEBREW', 'JULIAN'],
            ),
        ),
    ):
        Validate.date_general('SOMETHING 1 JAN 2000', 'Date', Specs)


def test_bad_date_general_epoch() -> None:
    with pytest.raises(
        ValueError,
        match=re.escape(Msg.NOT_DATE_EPOCH.format('2000 BC', 'Date', ['BCE'])),
    ):
        Validate.date_general('2000 BC', 'Date', Specs)


def test_bad_date_spaces() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_DATE_SPACES.format(
            'GREGORIAN 1 JAN 2000 BCE MORE', 'Date', str(5)
        ),
    ):
        Validate.date_general('GREGORIAN 1 JAN 2000 BCE MORE', 'Date', Specs)


def test_bad_date_month_day_too_many() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_DATE_EXACT_DAY.format(
            '32 JAN 2000',
            'Date',
            str(32),
            str(31),
        ),
    ):
        Validate.date_general('32 JAN 2000', 'Date', Specs)


def test_bad_date_month_day_too_few() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_DATE_EXACT_DAY.format(
            '0 JAN 2000',
            'Date',
            str(0),
            str(31),
        ),
    ):
        Validate.date_general('0 JAN 2000', 'Date', Specs)


def test_bad_date_month_day_leapyear_gregorian() -> None:
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_EXACT_DAY.format(
                '29 FEB 2002',
                'Date',
                str(29),
                str(28),
            )
        ),
    ):
        Validate.date_general('29 FEB 2002', 'Date', Specs)


def test_bad_date_month_day_not_leapyear_julian() -> None:
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_EXACT_DAY.format(
                'JULIAN 29 FEB 2002',
                'Date',
                str(29),
                str(28),
            )
        ),
    ):
        Validate.date_general('JULIAN 29 FEB 2002', 'Date', Specs)


def test_bad_date_month_day_leapyear_julian() -> None:
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_EXACT_DAY.format(
                'JULIAN 29 FEB 2000',
                'Date',
                str(29),
                str(28),
            )
        ),
    ):
        Validate.date_general('JULIAN 29 FEB 2000', 'Date', Specs)


def test_bad_date_month_day_not_leapyear_julian_zero() -> None:
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_EXACT_DAY.format(
                'JULIAN 0 FEB 2002',
                'Date',
                str(0),
                str(28),
            )
        ),
    ):
        Validate.date_general('JULIAN 0 FEB 2002', 'Date', Specs)


def test_bad_date_month_day_leapyear_julian_zero() -> None:
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_DATE_EXACT_DAY.format(
                'JULIAN 0 FEB 2000',
                'Date',
                str(0),
                str(28),
            )
        ),
    ):
        Validate.date_general('JULIAN 0 FEB 2000', 'Date', Specs)


# date_period tests
def test_date_period_from_to() -> None:
    assert Validate.date_period('FROM 1 JAN 2000 TO 1 JAN 2001', 'Date', Specs)


def test_date_period_only_to() -> None:
    assert Validate.date_period('TO 1 JAN 2001', 'Date', Specs)


def test_date_period_empty() -> None:
    assert Validate.date_period('', 'Date', Specs)


def test_date_period_bad_prefix() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_DATE_PERIOD.format('HELLO 1 JAN 2000', 'Date')
    ):
        Validate.date_period('HELLO 1 JAN 2000', 'Date', Specs)


def test_date_period_no_lower_case() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_DATE_PERIOD.format('to 1 JAN 2000', 'Date')
    ):
        Validate.date_period('to 1 JAN 2000', 'Date', Specs)


# enum tests
def test_enum_resn() -> None:
    assert Validate.enum(
        'LOCKED', 'INDI', ['LOCKED', 'CONFIDENTIAL'], 'enumset-RESN', Specs
    )


def test_enum_hide_extension() -> None:
    enum_hide: str = (
        'tests\\data\\extension_tests\\enumerations\\enum-_HIDE.yaml'
    )
    g = Genealogy()
    g.document_tag('_HIDE', enum_hide)
    assert gc.Resn('_HIDE').validate(specs=g.specification)

def test_enum_hide_extension_list() -> None:
    enum_hide: str = (
        'tests\\data\\extension_tests\\enumerations\\enum-_HIDELIST.yaml'
    )
    g = Genealogy()
    g.document_tag('_HIDELIST', enum_hide)
    assert gc.Resn('_HIDELIST').validate(specs=g.specification)



# filepath tests
def test_filepath() -> None:
    assert Validate.filepath(
        'tests/data/extension_tests/enum-_HIDE.yaml', 'File'
    )


# language tests
def test_language() -> None:
    assert Validate.language('en-US', 'Lang')


# listing tests
def test_listing() -> None:
    assert Validate.listing(', , here', 'Plac')


# mediatype tests
def test_media_type() -> None:
    assert Validate.mediatype('text/html', 'Medi')


def test_media_type_no_slash() -> None:
    with pytest.raises(
        ValueError, match=Msg.NO_SLASH.format('texthtml', 'Medi')
    ):
        Validate.mediatype('texthtml', 'Medi')


# name tests
def test_name_no_slash() -> None:
    assert Validate.name('John Doe', 'Name')


def test_name_slash() -> None:
    assert Validate.name('John /Doe/', 'Name')


def test_name_too_many_slashes() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_NAME_SLASH.format('John /// Doe', 'Name', str(3)),
    ):
        Validate.name('John /// Doe', 'Name')


def test_name_too_few_slashes() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_NAME_SLASH.format('John / Doe', 'Name', str(1)),
    ):
        Validate.name('John / Doe', 'Name')


# non_negative_integer tests
def test_non_negative_integer() -> None:
    assert Validate.non_negative_integer(1, 'Name')


def test_non_negative_integer_zero() -> None:
    assert Validate.non_negative_integer(0, 'Name')


def test_non_negative_integer_negative() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_INTEGER.format(repr(-1), 'Name')
    ):
        Validate.non_negative_integer(-1, 'Name')


def test_non_negative_integer_string() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_INTEGER.format(repr('1'), 'Name')
    ):
        Validate.non_negative_integer('1', 'Name')


# string tests
def test_string() -> None:
    assert Validate.string('', 'Name')


def test_string_with_eol() -> None:
    assert Validate.string('abc\ndef\nefg', 'Name')


def test_string_large() -> None:
    assert Validate.string(
        'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'Name'
    )


def test_not_string_none() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_STRING.format(repr(None), 'Name')
    ):
        Validate.string(None, 'Name')


def test_not_string_int() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_STRING.format(repr(1), 'Name')
    ):
        Validate.string(1, 'Name')


def test_not_string_xref() -> None:
    with pytest.raises(
        ValueError,
        match=re.escape(Msg.NOT_STRING.format(repr(Void.FAM), 'Name')),
    ):
        Validate.string(Void.FAM, 'Name')


# remove_double_spaces tests
def test_remove_double_spaces() -> None:
    assert Validate.remove_double_spaces('   a  b    c d ') == ' a b c d '


def test_remove_double_spaces_none() -> None:
    assert Validate.remove_double_spaces('a b c d') == 'a b c d'


# time tests
def test_time_hours_minutes_seconds() -> None:
    assert Validate.time('12:12:12', 'Time')


def test_time_minimal() -> None:
    assert Validate.time('00:00:00.000001', 'Time')


def test_time_minimal_single_digits() -> None:
    assert Validate.time('0:0:0', 'Time')


def test_time_minimal_single_nonzero_digits() -> None:
    assert Validate.time('1:2:3', 'Time')


def test_time_minimal_int() -> None:
    assert Validate.time('00:00:00', 'Time')


def test_time_maximal() -> None:
    assert Validate.time('23:59:59.999999', 'Time')


def test_time_maximal_int() -> None:
    assert Validate.time('23:59:59', 'Time')


def test_time_hours_minutes_secondsfloat() -> None:
    assert Validate.time('12:12:12.50', 'Time')


def test_time_hours_minutes() -> None:
    assert Validate.time('12:12', 'Time')


def test_time_not_string() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_STRING.format(repr(111), 'Time')
    ):
        Validate.time(111, 'Time')


def test_time_bad_letters() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_TIME.format('12:12:12.1a', 'Time')
    ):
        Validate.time('12:12:12.1a', 'Time')


def test_time_colon_count_too_many() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_TIME_COLON_COUNT.format('12:12:12:', 'Time', str(3)),
    ):
        Validate.time('12:12:12:', 'Time')


def test_time_colon_count_too_few() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_TIME_COLON_COUNT.format('12', 'Time', str(0)),
    ):
        Validate.time('12', 'Time')


def test_time_hours_too_few() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_TIME_HOURS.format(
            '-1:12:12',
            'Time',
            str(-1),
            Default.TIME_MIN_HOUR,
            Default.TIME_MAX_HOUR,
        ),
    ):
        Validate.time('-1:12:12', 'Time')


def test_time_hours_too_many() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_TIME_HOURS.format(
            '24:12:12',
            'Time',
            str(24),
            Default.TIME_MIN_HOUR,
            Default.TIME_MAX_HOUR,
        ),
    ):
        Validate.time('24:12:12', 'Time')


def test_time_minutes_too_many() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_TIME_MINUTES.format(
            '12:60:12',
            'Time',
            '60',
            Default.TIME_MIN_MINUTE,
            Default.TIME_MAX_MINUTE,
        ),
    ):
        Validate.time('12:60:12', 'Time')


def test_time_minutes_too_few() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_TIME_MINUTES.format(
            '12:-1:12',
            'Time',
            '-1',
            Default.TIME_MIN_MINUTE,
            Default.TIME_MAX_MINUTE,
        ),
    ):
        Validate.time('12:-1:12', 'Time')


def test_time_seconds_too_few() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_TIME_SECONDS.format(
            '12:12:-1',
            'Time',
            '-1',
            Default.TIME_MIN_SECOND,
            Default.TIME_MAX_SECOND,
        ),
    ):
        Validate.time('12:12:-1', 'Time')


def test_time_seconds_too_many() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_TIME_SECONDS.format(
            '12:12:60',
            'Time',
            '60',
            Default.TIME_MIN_SECOND,
            Default.TIME_MAX_SECOND,
        ),
    ):
        Validate.time('12:12:60', 'Time')


# y_or_null tests


def test_y_or_null_1() -> None:
    assert Validate.y_or_null('Y', 'Name')


def test_y_or_null_2() -> None:
    assert Validate.y_or_null('', 'Name')


def test_bad_y_or_null_1() -> None:
    value: str = 'A'
    with pytest.raises(
        ValueError, match=Msg.VALUE_NOT_Y_OR_NULL.format(value, 'Name')
    ):
        Validate.y_or_null(value, 'Name')


def test_bad_y_or_null_2() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_STRING.format(repr(None), 'Name')
    ):
        Validate.y_or_null(None, 'Name')


def test_bad_y_or_null_3() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_STRING.format(repr(1), 'Name')
    ):
        Validate.y_or_null(1, 'Name')
