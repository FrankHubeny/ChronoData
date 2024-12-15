"""------------------------------------------------------------------------------
                            Defs Class Tests

    These tests cover the `Defs` NamedTuple class.

------------------------------------------------------------------------------"""

from typing import Any

import pytest

from chronodata.chrono import Chronology, Date, Defs, Time
from chronodata.g7 import Enum, EnumName, Gedcom, Record
from chronodata.messages import Msg

testdata = [
    ('taginfo1', '1 TIME 01:01:01Z\n'),
    ('taginfo2', '2 DATA\n'),
    ('taginit1', '0 @1@ INDI\n'),
    ('taginit2', '0 @1@ INDI someone\n'),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_time(test_input: str, expected: str | int | bool) -> None:
    taginfo1 = Defs.taginfo(1, Gedcom.TIME, '01:01:01Z')  # noqa: F841
    taginfo2 = Defs.taginfo(2, Gedcom.DATA)  # noqa: F841
    taginit1 = Defs.taginit('@1@', Gedcom.INDI)  # noqa: F841
    taginit2 = Defs.taginit('@1@', Gedcom.INDI, 'someone')  # noqa: F841

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
    t: tuple[Any] = (  # type: ignore[assignment]
        Date(2000, 1, 1),
        Date(3000, 1, 10),
        Date(-100, 1, 10),
        'hello',
        Date(1000, 8, 4),
    )
    with pytest.raises(
        TypeError, match=Msg.WRONG_TYPE.format(t[3], type(t[3]), Date)
    ):
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
        ValueError, match=Msg.NOT_VALID_ENUM.format(Gedcom.INDI, EnumName.ADOP)
    ):
        Defs.verify_enum(Gedcom.INDI, Enum.ADOP, EnumName.ADOP)


def test_even_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format(Gedcom.INDI, EnumName.EVEN)
    ):
        Defs.verify_enum(Gedcom.INDI, Enum.EVEN, EnumName.EVEN)


def test_evenattr_enum() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_VALID_ENUM.format(Gedcom.INDI, EnumName.EVENATTR),
    ):
        Defs.verify_enum(Gedcom.INDI, Enum.EVENATTR, EnumName.EVENATTR)


def test_famc_enum() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_VALID_ENUM.format(Gedcom.INDI, EnumName.FAMC_STAT),
    ):
        Defs.verify_enum(Gedcom.INDI, Enum.FAMC_STAT, EnumName.FAMC_STAT)


def test_fam_attr_enum() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_VALID_ENUM.format(Gedcom.INDI, EnumName.FAM_ATTR),
    ):
        Defs.verify_enum(Gedcom.INDI, Enum.FAM_ATTR, EnumName.FAM_ATTR)


def test_fam_even_enum() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_VALID_ENUM.format(Gedcom.INDI, EnumName.FAM_EVEN),
    ):
        Defs.verify_enum(Gedcom.INDI, Enum.FAM_EVEN, EnumName.FAM_EVEN)


def test_id_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format(Gedcom.INDI, EnumName.ID)
    ):
        Defs.verify_enum(Gedcom.INDI, Enum.ID, EnumName.ID)


def test_indi_attr_enum() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_VALID_ENUM.format(Gedcom.INDI, EnumName.INDI_ATTR),
    ):
        Defs.verify_enum(Gedcom.INDI, Enum.INDI_ATTR, EnumName.INDI_ATTR)


def test_indi_even_enum() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_VALID_ENUM.format(Gedcom.INDI, EnumName.INDI_EVEN),
    ):
        Defs.verify_enum(Gedcom.INDI, Enum.INDI_EVEN, EnumName.INDI_EVEN)


def test_medi_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format(Gedcom.INDI, EnumName.MEDI)
    ):
        Defs.verify_enum(Gedcom.INDI, Enum.MEDI, EnumName.MEDI)


def test_media_type_enum() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_VALID_ENUM.format(Gedcom.INDI, EnumName.MEDIA_TYPE),
    ):
        Defs.verify_enum(Gedcom.INDI, Enum.MEDIA_TYPE, EnumName.MEDIA_TYPE)


def test_name_type_enum() -> None:
    with pytest.raises(
        ValueError,
        match=Msg.NOT_VALID_ENUM.format(Gedcom.INDI, EnumName.NAME_TYPE),
    ):
        Defs.verify_enum(Gedcom.INDI, Enum.NAME_TYPE, EnumName.NAME_TYPE)


def test_pedi_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format(Gedcom.INDI, EnumName.PEDI)
    ):
        Defs.verify_enum(Gedcom.INDI, Enum.PEDI, EnumName.PEDI)


def test_quay_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format(Gedcom.INDI, EnumName.QUAY)
    ):
        Defs.verify_enum(Gedcom.INDI, Enum.QUAY, EnumName.QUAY)


def test_resn_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format(Gedcom.INDI, EnumName.RESN)
    ):
        Defs.verify_enum(Gedcom.INDI, Enum.RESN, EnumName.RESN)


def test_role_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format(Gedcom.INDI, EnumName.ROLE)
    ):
        Defs.verify_enum(Gedcom.INDI, Enum.ROLE, EnumName.ROLE)


def test_sex_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format(Gedcom.INDI, EnumName.SEX)
    ):
        Defs.verify_enum(Gedcom.INDI, Enum.SEX, EnumName.SEX)


def test_stat_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format(Gedcom.INDI, EnumName.STAT)
    ):
        Defs.verify_enum(Gedcom.INDI, Enum.STAT, EnumName.STAT)


def test_empty_string_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format('', EnumName.STAT)
    ):
        Defs.verify_enum('', Enum.STAT, EnumName.STAT)

def test_not_negative_int() -> None:
    with pytest.raises(
        ValueError, match=Msg.NEGATIVE_ERROR.format(-1)
    ):
        Defs.verify_not_negative(-1)

def test_not_negative_float() -> None:
    with pytest.raises(
        ValueError, match=Msg.NEGATIVE_ERROR.format(-1.9)
    ):
        Defs.verify_not_negative(-1.9)

def test_range_int_low() -> None:
    with pytest.raises(
        ValueError, match=Msg.RANGE_ERROR.format(1, 5, 10)
    ):
        Defs.verify_range(1, 5, 10)

def test_range_int_high() -> None:
    with pytest.raises(
        ValueError, match=Msg.RANGE_ERROR.format(11, 5, 10)
    ):
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
        