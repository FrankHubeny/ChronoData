# map_test.py
"""Tests to cover the Map, Lati and Long structures and Input class for lati and long methods.

1. Validate: Exercise all validation checks.
    a. Good run.
    b. Catch not permitted substructure.
    c. Catch not included but required substructures.
    d. Catch more than one when only one permitted.
    e. Catch bad input.

2. Ged: Exercise the generation of ged data.

3. Code: Exercise the code method.
"""

import re

import pytest

import genedata.classes7 as gc
from genedata.constants import Default
from genedata.messages import Msg
from genedata.util import Input


# 1. Validate Section
#    a. Good run.
def test_good_run() -> None:
    """Run a successful use of the structure."""
    m = gc.Map([gc.Lati('N18.150944'), gc.Long('E168.150944')])
    assert m.validate()


#    b. Catch not permitted substructure.


def test_not_permitted() -> None:
    """Check that a substructure not in the permitted list cannot be used by the structure."""
    m = gc.Map([gc.Lati('N18.150944'), gc.Phrase('test'), gc.Long('E168.150944')])
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_PERMITTED.format('Phrase', m.permitted, m.class_name)
        ),
    ):
        m.validate()


#    c. Catch not included but required substructures.


def test_lati_not_present() -> None:
    """Check that the Lati structure is used by Map."""
    m = gc.Map([gc.Long('E168.150944')])
    with pytest.raises(
        ValueError,
        match=Msg.MISSING_REQUIRED.format('Lati', m.class_name),
    ):
        m.validate()


def test_long_not_present() -> None:
    """Check that the Long structure is used by Map."""
    m = gc.Map([gc.Lati('N68.150944')])
    with pytest.raises(
        ValueError,
        match=Msg.MISSING_REQUIRED.format('Long', m.class_name),
    ):
        m.validate()


#    d. Catch more than one when only one permitted.


def test_lati_only_one() -> None:
    """Check that the lati structure can be used only once by Map."""
    m = gc.Map([gc.Lati('N18.150944'), gc.Lati('N18.150944'), gc.Long('E168.150944')])
    with pytest.raises(
        ValueError, match=Msg.ONLY_ONE_PERMITTED.format('Lati', m.class_name)
    ):
        m.validate()


def test_long_only_one() -> None:
    """Check that the lati structure can be used only once by Map."""
    m = gc.Map([gc.Lati('N18.150944'), gc.Long('E168.150944'), gc.Long('E168.150944')])
    with pytest.raises(
        ValueError, match=Msg.ONLY_ONE_PERMITTED.format('Long', m.class_name)
    ):
        m.validate()


#    e. Catch bad input.


def test_lati_bad_direction() -> None:
    """Check that the latitude direction is either N or S."""
    m = gc.Map([gc.Lati('A10.1'), gc.Long('E168.150944')])
    with pytest.raises(
        ValueError,
        match=Msg.LATI_NORTH_SOUTH.format(
            'A', 'A10.1', Default.LATI_NORTH, Default.LATI_SOUTH, 'gc.Lati'
        ),
    ):
        m.validate()


def test_long_bad_direction() -> None:
    """Check that the longitude direction is either E or W."""
    m = gc.Map([gc.Lati('N10.1'), gc.Long('K168.150944')])
    with pytest.raises(
        ValueError,
        match=Msg.LONG_EAST_WEST.format(
            'K', 'K168.150944', Default.LONG_EAST, Default.LONG_WEST, 'gc.Long'
        ),
    ):
        m.validate()


def test_lati_range_high() -> None:
    """Check that the latitude high stays within its range."""
    m = gc.Map([gc.Lati('N90.1'), gc.Long('E168.150944')])
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.LATI_RANGE.format(
                'N90.1', str(Default.LATI_LOW), str(Default.LATI_HIGH), 'gc.Lati'
            )
        ),
    ):
        m.validate()


def test_lati_range_low() -> None:
    """Check that the latitude low stays within its range."""
    m = gc.Map([gc.Lati('S90.1'), gc.Long('E168.150944')])
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.LATI_RANGE.format(
                'S90.1', str(Default.LATI_LOW), str(Default.LATI_HIGH), 'gc.Lati'
            )
        ),
    ):
        m.validate()


def test_long_range_high() -> None:
    """Check that the longitude high stays within its range."""
    m = gc.Map([gc.Lati('N80.1'), gc.Long('E180.1')])
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.LONG_RANGE.format(
                'E180.1', str(Default.LONG_LOW), str(Default.LONG_HIGH), 'gc.Long'
            )
        ),
    ):
        m.validate()


def test_long_range_low() -> None:
    """Check that the longitude low stays within its range."""
    m = gc.Map([gc.Lati('S80.1'), gc.Long('W180.1')])
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.LONG_RANGE.format(
                'W180.1', str(Default.LONG_LOW), str(Default.LONG_HIGH), 'gc.Long'
            )
        ),
    ):
        m.validate()


# 2. Ged Section


def test_ged() -> None:
    """Illustrate the standard use of the class."""
    m = gc.Map([gc.Lati('N18.150944'), gc.Long('E168.150944')])
    assert m.ged(1) == '1 MAP\n2 LATI N18.150944\n2 LONG E168.150944\n'


def test_ged_using_input() -> None:
    """Illustrate the use of the Map class with Input."""
    m = gc.Map([gc.Lati(Input.lati(18, 9, 3.4)), gc.Long(Input.long(168, 9, 3.4))])
    assert m.ged(1) == '1 MAP\n2 LATI N18.150944\n2 LONG E168.150944\n'


# 3. Code Section


def test_code() -> None:
    """Illustrate code running."""
    m = gc.Map([gc.Lati(Input.lati(18, 9, 3.4)), gc.Long(Input.long(168, 9, 3.4))])
    assert (
        m.code()
        == "\ngc.Map(\n    [\n        gc.Lati('N18.150944'),\n        gc.Long('E168.150944'),\n    ]\n)"
    )
