"""------------------------------------------------------------------------------
                            Enum Tests

    These tests cover the Enums.

------------------------------------------------------------------------------"""

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
    Record,
    Resn,
    RestrictDate,
    Role,
    Sex,
    Stat,
    Tag,
)
from chronodata.messages import Msg
from chronodata.methods import Defs


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


def test_record_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format('hello', Record)
    ):
        Defs.verify_enum('hello', Record)


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

def test_tag_enum() -> None:
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format('hello', Tag)
    ):
        Defs.verify_enum('hello', Tag)


def test_empty_string_enum() -> None:
    with pytest.raises(ValueError, match=Msg.NOT_VALID_ENUM.format('', Stat)):
        Defs.verify_enum('', Stat)


