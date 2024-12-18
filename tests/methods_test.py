"""------------------------------------------------------------------------------
                            Defs Class Tests

    These tests cover the `Defs` NamedTuple class.

------------------------------------------------------------------------------"""

import pytest

from chronodata.enums import Record, Tag
from chronodata.messages import Msg
from chronodata.methods import Defs
from chronodata.tuples import Date, Time

testdata = [
    ('taginfo1', '1 TIME 01:01:01Z\n'),
    ('taginfo2', '2 DATA\n'),
    ('taginit1', '0 @1@ INDI\n'),
    ('taginit2', '0 @1@ INDI someone\n'),
    ('taginfo3', '1 TIME 01:01:01Z hello\n'),
    ('Defs.verify_type(1,int)', True),
    ('Defs.verify_type("a",str)', True),
    ('Defs.verify_type(1.5,float)', True),
    ('Defs.verify_tuple_type(("b","a"),str)', True),
    ('Defs.verify_tuple_type((1,2),int)', True),
    ('Defs.verify_range(1,0,2)', True),
    ('Defs.verify_range(1,1,2)', True),
    ('Defs.verify_range(2,1,2)', True),
    ('Defs.verify_range(59.9999999999,50.0,59.9999999999)', True),
    ('Defs.verify_not_negative(2)', True),
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
    taginfo1 = Defs.taginfo(1, Tag.TIME, '01:01:01Z')  # noqa: F841
    taginfo2 = Defs.taginfo(2, Tag.DATA)  # noqa: F841
    taginfo3 = Defs.taginfo(1, Tag.TIME, '01:01:01Z', 'hello')  # noqa: F841

    # Test the taginit method.
    taginit1 = Defs.taginit('@1@', Record.INDI)  # noqa: F841
    taginit2 = Defs.taginit('@1@', Record.INDI, 'someone')  # noqa: F841

    # Test the verify_enum method.
    enum = Defs.verify_enum(Tag.HUSB, Tag)  # noqa: F841

    # test the clean_input method.
    clean1 = Defs.clean_input('hell\u0000o to you')  # noqa: F841
    clean2 = Defs.clean_input(  # noqa: F841
        'A\uffffB\ufffeC\udfffD\ud800E\u007fF\u001fG\u0000'
    )
    clean3 = Defs.clean_input(  # noqa: F841
        'A\u0001B\u0002C\u0003D\u0004E\u0005F\u0006G\u0007'
    )
    clean4 = Defs.clean_input(  # noqa: F841
        'A\u0001B\u0001C\u0001D\u0001E\u0001F\u0001G\u0001'
    )
    clean5 = Defs.clean_input(  # noqa: F841
        '\u0009\u0009\u0009'
    )

    assert eval(test_input) == expected


def test_int_as_string_type() -> None:
    with pytest.raises(TypeError):
        Defs.verify_type(1, str)


def test_string_as_int_type() -> None:
    with pytest.raises(TypeError):
        Defs.verify_type('1', int)


def test_tuple_type() -> None:
    with pytest.raises(TypeError):
        Defs.verify_type(Date(2000, 1, 1), int)


def test_tuple_type_time() -> None:
    with pytest.raises(TypeError):
        Defs.verify_type(Date(2000, 1, 1), type(Time))


def test_tuple_of_types_str_error() -> None:
    t: tuple[Date] = (  # type: ignore[assignment]
        Date(2000, 1, 1),
        Date(3000, 1, 10),
        Date(-100, 1, 10),
        'hello',
        Date(1000, 8, 4),
    )
    with pytest.raises(TypeError):
        Defs.verify_tuple_type(t, Date)


def test_tuple_of_types_time_error() -> None:
    t: tuple[Date] = (  # type: ignore[assignment]
        Date(2000, 1, 1),
        Date(3000, 1, 10),
        Date(-100, 1, 10),
        Time(1, 1, 1),
        Date(1000, 8, 4),
    )
    with pytest.raises(TypeError):
        Defs.verify_tuple_type(t, Date)


def test_not_negative_int() -> None:
    with pytest.raises(ValueError, match=Msg.NEGATIVE_ERROR.format(-1)):
        Defs.verify_not_negative(-1)


def test_not_negative_float() -> None:
    with pytest.raises(ValueError, match=Msg.NEGATIVE_ERROR.format(-1.9)):
        Defs.verify_not_negative(-1.9)


def test_range_int_low() -> None:
    with pytest.raises(ValueError, match=Msg.RANGE_ERROR.format(1, 5, 10)):
        Defs.verify_range(1, 5, 10)


def test_range_int_high() -> None:
    with pytest.raises(ValueError, match=Msg.RANGE_ERROR.format(11, 5, 10)):
        Defs.verify_range(11, 5, 10)


def test_range_float_low() -> None:
    with pytest.raises(
        ValueError, match=Msg.RANGE_ERROR.format(1.1, 5.1, 10.1)
    ):
        Defs.verify_range(1.1, 5.1, 10.1)


def test_range_float_high() -> None:
    with pytest.raises(
        ValueError, match=Msg.RANGE_ERROR.format(11.5, 5.1, 10.9)
    ):
        Defs.verify_range(11.5, 5.1, 10.9)


def test_tag_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format('hello', Tag)
    ):
        Defs.verify_enum('hello', Tag)
