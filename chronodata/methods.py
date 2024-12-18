# Licensed under a 3-clause BSD style license - see LICENSE.md
"""Global methods to build a chronology based on the GEDCOM standard."""

import re
from typing import Any

from chronodata.enums import Record, Tag
from chronodata.messages import Msg


class Defs:
    """Provide a namespace container for global methods.

    These functions do various forms of checks and formatting
    of output data.

    The GEDCOM standard only permits UTF-8 character encodings
    with a set of banned characters to explicitely eliminate
    from input sources.

    Reference
    ---------
    - [GEDCOM UTF-8 Characters](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#characters)
    - [Python 3 UTF How To](https://docs.python.org/3/howto/unicode.html)
    - [Python 3 string](https://docs.python.org/3/library/string.html)
    """

    @staticmethod
    def taginit(xref: str, tag: Record, info: str = '') -> str:
        if info == '':
            return f'0 {xref} {tag.value}\n'
        return f'0 {xref} {tag.value} {str(info).strip()}\n'

    @staticmethod
    def taginfo(
        level: int,
        tag: Tag,
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
                return f'{level} {tag.value}\n'
            return f'{level} {tag.value} {info}\n'
        return f'{level} {tag.value} {info} {extra}\n'

    @staticmethod
    def clean_input(input: str) -> str:
        """Remove banned GEDCOM unicode characters from input strings.

        The control characters U+0000 - U+001F and the delete character U+007F 
        are listed in the 
        [C0 Controls and Basic Latin](https://www.unicode.org/charts/PDF/U0000.pdf)
        chart.

        The code points U+D800 - U+DFFF are not interpreted.
        They are described in the
        [High Surrogate Area](https://www.unicode.org/charts/PDF/UD800.pdf) and
        [Low Surrogate Area](https://www.unicode.org/charts/PDF/UDC00.pdf)
        standards.

        The code points U+FFFE and U+FFFF are noncharacters as described in the
        [Specials](https://www.unicode.org/charts/PDF/UFFF0.pdf) standard.
        
        Reference
        ---------
        - [GEDCOM Characters](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#characters)
        - [Unicode Specification](https://www.unicode.org/versions/Unicode16.0.0/#Summary)
        - [Python re Module](https://docs.python.org/3/library/re.html)
        """
        
        return re.sub(r'[\u0000-\u001F\u007F\uD800-\uDFFF\uFFFE\uFFFF]', '', input)

    @staticmethod
    def verify_type(value: Any, value_type: Any) -> bool:
        """Check if the value has the specified type."""
        if not isinstance(value, value_type):
            raise TypeError(
                Msg.WRONG_TYPE.format(value, type(value), value_type)
            )
        # if isinstance(value, str):
        #     Defs.verify_string_input(value)
        # if isinstance(value, int):
        #     Defs.verify_numeric_input(value)
        # if isinstance(value, float):
        #     Defs.verify_numeric_input(value)
        return True

    @staticmethod
    def verify_tuple_type(name: tuple[Any], value_type: Any) -> bool:
        """Check if each member of the tuple has the specified type."""
        for value in name:
            Defs.verify_type(value, value_type)
        return True

    @staticmethod
    def verify_enum(value: Any, enumeration: Any) -> bool:
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
