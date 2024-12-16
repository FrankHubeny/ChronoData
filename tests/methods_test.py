"""------------------------------------------------------------------------------
                            Defs Class Tests

    These tests cover the `Defs` NamedTuple class.

------------------------------------------------------------------------------"""

#from typing import Any

import pytest

from chronodata.enums import (
    Adop,
    ApproxDate,
    EvenAttr,
    FamAttr,
    FamcStat,
    FamEven,
    GreaterLessThan,
    Id,
    IndiAttr,
    IndiEven,
    Medi,
    MediaType,
    NameType,
    Pedi,
    PersonalNamePiece,
    Quay,
    RangeDate,
    Records,
    Resn,
    RestrictDate,
    Role,
    Sex,
    Stat,
)
from chronodata.g7 import Gedcom
from chronodata.messages import Msg
from chronodata.methods import Defs
from chronodata.tuples import Date, Time

testdata = [
    ('taginfo1', '1 TIME 01:01:01Z\n'),
    ('taginfo2', '2 DATA\n'),
    ('taginit1', '0 @1@ INDI\n'),
    ('taginit2', '0 @1@ INDI someone\n'),
    ('Defs.verify_type(1,int)', True),
    ('Defs.verify_type("a",str)', True),
    ('Defs.verify_tuple_type(("b","a"),str)', True),
    ('Defs.verify_tuple_type((1,2),int)', True),
    ('Defs.verify_range(1,0,2)', True),
    ('Defs.verify_range(1,1,2)', True),
    ('Defs.verify_range(2,1,2)', True),
    ('Defs.verify_range(59.9999999999,50.0,59.9999999999)', True),
    ('Defs.verify_not_negative(2)', True),
    ('enum', True),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_time(test_input: str, expected: str | int | bool) -> None:
    taginfo1 = Defs.taginfo(1, Gedcom.TIME, '01:01:01Z')  # noqa: F841
    taginfo2 = Defs.taginfo(2, Gedcom.DATA)  # noqa: F841
    taginit1 = Defs.taginit('@1@', Gedcom.INDI)  # noqa: F841
    taginit2 = Defs.taginit('@1@', Gedcom.INDI, 'someone')  # noqa: F841
    enum = Defs.verify_enum(Gedcom.HUSB, Adop)  # noqa: F841

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


def test_adop_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format('hello', Adop)
    ):
        Defs.verify_enum('hello', Adop)

def test_approxdate_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format('hello', ApproxDate)
    ):
        Defs.verify_enum('hello', ApproxDate)

def test_greaterlessthan_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format('hello', GreaterLessThan)
    ):
        Defs.verify_enum('hello', GreaterLessThan)

def test_personalnamepiece_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format('hello', PersonalNamePiece)
    ):
        Defs.verify_enum('hello', PersonalNamePiece)

def test_rangedate_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format('hello', RangeDate)
    ):
        Defs.verify_enum('hello', RangeDate)

def test_records_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format('hello', Records)
    ):
        Defs.verify_enum('hello', Records)

def test_restrictdate_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format('hello', RestrictDate)
    ):
        Defs.verify_enum('hello', RestrictDate)

def test_even_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format('hello', EvenAttr)
    ):
        Defs.verify_enum('hello', EvenAttr)


def test_evenattr_enum() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_VALID_ENUM.format('hello', EvenAttr),
    ):
        Defs.verify_enum('hello', EvenAttr)


def test_famc_enum() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_VALID_ENUM.format('hello', FamcStat),
    ):
        Defs.verify_enum('hello', FamcStat)


def test_fam_attr_enum() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_VALID_ENUM.format('hello', FamAttr),
    ):
        Defs.verify_enum('hello', FamAttr)


def test_fam_even_enum() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_VALID_ENUM.format('hello', FamEven),
    ):
        Defs.verify_enum('hello', FamEven)


def test_id_enum() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_VALID_ENUM.format('hello', Id),
    ):
        Defs.verify_enum('hello', Id)


def test_indi_attr_enum() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_VALID_ENUM.format('hello', IndiAttr),
    ):
        Defs.verify_enum('hello', IndiAttr)


def test_indi_even_enum() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_VALID_ENUM.format('hello', IndiEven),
    ):
        Defs.verify_enum('hello', IndiEven)


def test_medi_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format('hello', Medi)
    ):
        Defs.verify_enum('hello', Medi)


def test_media_type_enum() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_VALID_ENUM.format('hello', MediaType),
    ):
        Defs.verify_enum('hello', MediaType)


def test_name_type_enum() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_VALID_ENUM.format('hello', NameType),
    ):
        Defs.verify_enum('hello', NameType)


def test_pedi_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format('hello', Pedi)
    ):
        Defs.verify_enum('hello', Pedi)


def test_quay_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format('hello', Quay)
    ):
        Defs.verify_enum('hello', Quay)


def test_resn_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format('hello', Resn)
    ):
        Defs.verify_enum('hello', Resn)


def test_role_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format('hello', Role)
    ):
        Defs.verify_enum('hello', Role)


def test_sex_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format('hello', Sex)
    ):
        Defs.verify_enum('hello', Sex)


def test_stat_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format('hello', Stat)
    ):
        Defs.verify_enum('hello', Stat)


def test_empty_string_enum() -> None:
    with pytest.raises(ValueError, match=Msg.NOT_VALID_ENUM.format('', Stat)):
        Defs.verify_enum('', Stat)


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


# def test_xref_individual() -> None:
#     a = Chronology('test')
#     with pytest.raises(
#         ValueError, match=Msg.NOT_RECORD.format('rec', Record.INDIVIDUAL)):
#         Defs.verify_xref('rec', a.individual_xreflist, Record.INDIVIDUAL)

# def test_xref_family() -> None:
#     a = Chronology('test')
#     with pytest.raises(
#         ValueError, match=Msg.NOT_RECORD.format('rec', Record.FAMILY)):
#         Defs.verify_xref('rec', a.family_xreflist, Record.FAMILY)

# def test_xref_medialink() -> None:
#     a = Chronology('test')
#     with pytest.raises(
#         ValueError, match=Msg.NOT_RECORD.format('rec', Record.MULTIMEDIA)):
#         Defs.verify_xref('rec', a.multimedia_xreflist, Record.MULTIMEDIA)

# def test_xref_source() -> None:
#     a = Chronology('test')
#     with pytest.raises(
#         ValueError, match=Msg.NOT_RECORD.format('rec', Record.SOURCE)):
#         Defs.verify_xref('rec', a.source_xreflist, Record.SOURCE)

# def test_xref_repository() -> None:
#     a = Chronology('test')
#     with pytest.raises(
#         ValueError, match=Msg.NOT_RECORD.format('rec', Record.REPOSITORY)):
#         Defs.verify_xref('rec', a.repository_xreflist, Record.REPOSITORY)

# def test_xref_submitter() -> None:
#     a = Chronology('test')
#     with pytest.raises(
#         ValueError, match=Msg.NOT_RECORD.format('rec', Record.SUBMITTER)):
#         Defs.verify_xref('rec', a.submitter_xreflist, Record.SUBMITTER)

# def test_xref_shared_note() -> None:
#     a = Chronology('test')
#     with pytest.raises(
#         ValueError, match=Msg.NOT_RECORD.format('rec', Record.SHARED_NOTE)):
#         Defs.verify_xref('rec', a.shared_note_xreflist, Record.SHARED_NOTE)
