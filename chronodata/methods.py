# Licensed under a 3-clause BSD style license - see LICENSE.md
"""Global methods to build a chronology based on the GEDCOM standard."""

from typing import Any

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
from chronodata.messages import Msg


class Defs:
    """Provide a namespace container for global methods."""

    @staticmethod
    def taginit(xref: str, tag: str, info: str = '') -> str:
        if info == '':
            return f'0 {xref} {tag}\n'
        return f'0 {xref} {tag} {str(info).strip()}\n'

    @staticmethod
    def taginfo(
        level: int,
        tag: str,
        info: str = '',
        extra: str = '',
    ) -> str:
        """Return a GEDCOM formatted line for the information and level.

        This is suitable for most tagged lines to guarantee it is uniformly
        formatted.  Although the user need not worry about calling this line,
        it is provided so the user can see the GEDCOM formatted output
        that would result.

        See Also
        --------

        """

        if extra == '':
            if info == '':
                return f'{level} {tag}\n'
            return f'{level} {tag} {info}\n'
        return f'{level} {tag} {info} {extra}\n'

    @staticmethod
    def verify_type(value: Any, value_type: Any) -> bool:
        """Check if the value has the specified type."""
        if not isinstance(value, value_type):
            raise TypeError(
                Msg.WRONG_TYPE.format(value, type(value), value_type)
            )
        return True

    @staticmethod
    def verify_tuple_type(name: tuple[Any], value_type: Any) -> bool:
        """Check if each member of the tuple has the specified type."""
        for value in name:
            Defs.verify_type(value, value_type)
        return True

    @staticmethod
    # def verify_enum(value: str, enum: frozenset[str], name: str) -> bool:
    #     """Check if the value is in the proper enumation."""
    #     if value not in enum:
    #         raise ValueError(Msg.NOT_VALID_ENUM.format(value, name))
    #     return True
    def verify_enum(value: str, enumeration: Any) -> bool:
        """Check if the value is in the proper enumation."""
        if value not in enumeration:
            raise ValueError(Msg.NOT_VALID_ENUM.format(value, enumeration))
        return True

    @staticmethod
    def verify_range(
        value: int | float, low: int | float, high: int | float
    ) -> bool:
        """Check if the value is inclusively between low and high boundaries."""
        if not low <= value <= high:
            raise ValueError(Msg.RANGE_ERROR.format(value, low, high))
        return True

    @staticmethod
    def verify_not_negative(value: int | float) -> bool:
        """Check if the value is a positive number."""
        if value < 0:
            raise ValueError(Msg.NEGATIVE_ERROR.format(value))
        return True

    # @staticmethod
    # def verify_not_empty(value: str | None, name: str) -> None:
    #     """Check if the value is neither None nor the empty string."""
    #     if value == '' or value is None:
    #         raise ValueError(Msg.EMPTY_ERROR.format(name))
