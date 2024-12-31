"""------------------------------------------------------------------------------
                            Defs Class Tests

    These tests cover the `Defs` NamedTuple class.

------------------------------------------------------------------------------"""

import pytest

from chronodata.enums import Tag
from chronodata.messages import Msg
from chronodata.methods import DefCheck, DefTag
from chronodata.store import Date, Time

testdata = [
    ('taginfo1', '1 TIME 01:01:01Z\n'),
    ('taginfo2', '2 DATA\n'),
    ('taginfo3', '1 TIME 01:01:01Z hello\n'),
    ('DefCheck.verify_type(1,int)', True),
    ('DefCheck.verify_type("a",str)', True),
    ('DefCheck.verify_type(1.5,float)', True),
    ('DefCheck.verify_tuple_type(("b","a"),str)', True),
    ('DefCheck.verify_tuple_type((1,2),int)', True),
    ('DefCheck.verify_range(1,0,2)', True),
    ('DefCheck.verify_range(1,1,2)', True),
    ('DefCheck.verify_range(2,1,2)', True),
    ('DefCheck.verify_range(59.9999999999,50.0,59.9999999999)', True),
    ('DefCheck.verify_not_negative(2)', True),
    ('enum', True),
    ('clean1', 'hello to you'),
    ('clean2', 'ABCDEFG'),
    ('clean3', 'ABCDEFG'),
    ('clean4', 'ABCDEFG'),
    ('clean5', ''),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_defs_tags_classes(test_input: str, expected: str | int | bool) -> None:
    # Test the taginfo method.
    taginfo1 = DefTag.taginfo(1, Tag.TIME, '01:01:01Z')  # noqa: F841
    taginfo2 = DefTag.taginfo(2, Tag.DATA)  # noqa: F841
    taginfo3 = DefTag.taginfo(1, Tag.TIME, '01:01:01Z', 'hello')  # noqa: F841

    # Test the verify_enum method.
    enum = DefCheck.verify_enum(Tag.HUSB.value, Tag)  # noqa: F841

    # test the clean_input method.
    clean1 = DefTag.clean_input('hell\u0000o to you')  # noqa: F841
    clean2 = DefTag.clean_input(  # noqa: F841
        'A\uffffB\ufffeC\udfffD\ud800E\u007fF\u001fG\u0000'
    )
    clean3 = DefTag.clean_input(  # noqa: F841
        'A\u0001B\u0002C\u0003D\u0004E\u0005F\u0006G\u0007'
    )
    clean4 = DefTag.clean_input(  # noqa: F841
        'A\u0001B\u0001C\u0001D\u0001E\u0001F\u0001G\u0001'
    )
    clean5 = DefTag.clean_input(  # noqa: F841
        '\u0009\u0009\u0009'
    )

    assert eval(test_input) == expected


def test_int_as_string_type() -> None:
    with pytest.raises(TypeError):
        DefCheck.verify_type(1, str)


def test_string_as_int_type() -> None:
    with pytest.raises(TypeError):
        DefCheck.verify_type('1', int)


def test_tuple_type() -> None:
    with pytest.raises(TypeError):
        DefCheck.verify_type(Date(2000, 1, 1), int)


def test_tuple_type_time() -> None:
    with pytest.raises(TypeError):
        DefCheck.verify_type(Date(2000, 1, 1), type(Time))


def test_tuple_of_types_str_error() -> None:
    t: list[Date] = (  # type: ignore[assignment]
        Date(2000, 1, 1),
        Date(3000, 1, 10),
        Date(-100, 1, 10),
        'hello',
        Date(1000, 8, 4),
    )
    with pytest.raises(TypeError):
        DefCheck.verify_tuple_type(t, Date)


def test_tuple_of_types_time_error() -> None:
    t: list[Date] = (  # type: ignore[assignment]
        Date(2000, 1, 1),
        Date(3000, 1, 10),
        Date(-100, 1, 10),
        Time(1, 1, 1),
        Date(1000, 8, 4),
    )
    with pytest.raises(TypeError):
        DefCheck.verify_tuple_type(t, Date)


def test_not_negative_int() -> None:
    with pytest.raises(ValueError, match=Msg.NEGATIVE_ERROR.format(-1)):
        DefCheck.verify_not_negative(-1)


def test_not_negative_float() -> None:
    with pytest.raises(ValueError, match=Msg.NEGATIVE_ERROR.format(-1.9)):
        DefCheck.verify_not_negative(-1.9)


def test_range_int_low() -> None:
    with pytest.raises(ValueError, match=Msg.RANGE_ERROR.format(1, 5, 10)):
        DefCheck.verify_range(1, 5, 10)


def test_range_int_high() -> None:
    with pytest.raises(ValueError, match=Msg.RANGE_ERROR.format(11, 5, 10)):
        DefCheck.verify_range(11, 5, 10)


def test_range_float_low() -> None:
    with pytest.raises(
        ValueError, match=Msg.RANGE_ERROR.format(1.1, 5.1, 10.1)
    ):
        DefCheck.verify_range(1.1, 5.1, 10.1)


def test_range_float_high() -> None:
    with pytest.raises(
        ValueError, match=Msg.RANGE_ERROR.format(11.5, 5.1, 10.9)
    ):
        DefCheck.verify_range(11.5, 5.1, 10.9)


def test_tag_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format('hello', Tag)
    ):
        DefCheck.verify_enum('hello', Tag)
