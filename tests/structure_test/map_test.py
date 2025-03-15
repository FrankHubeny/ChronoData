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

from genedata.classes7 import Lati, Long, Map, Phrase
from genedata.constants import Default
from genedata.messages import Msg
from genedata.structure import Input


# 1. Validate Section
#    a. Good run.
def test_good_run() -> None:
    """Run a successful use of the structure."""
    m = Map([Lati('N18.150944'), Long('E168.150944')])
    assert m.validate()


#    b. Catch not permitted substructure.


def test_not_permitted() -> None:
    """Check that a substructure not in the permitted list cannot be used by the structure."""
    m = Map([Lati('N18.150944'), Phrase('test'), Long('E168.150944')])
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
    m = Map([Long('E168.150944')])
    with pytest.raises(
        ValueError,
        match=Msg.MISSING_REQUIRED.format('Lati', m.class_name),
    ):
        m.validate()


def test_long_not_present() -> None:
    """Check that the Long structure is used by Map."""
    m = Map([Lati('N68.150944')])
    with pytest.raises(
        ValueError,
        match=Msg.MISSING_REQUIRED.format('Long', m.class_name),
    ):
        m.validate()


#    d. Catch more than one when only one permitted.


def test_lati_only_one() -> None:
    """Check that the lati structure can be used only once by Map."""
    m = Map([Lati('N18.150944'), Lati('N18.150944'), Long('E168.150944')])
    with pytest.raises(
        ValueError, match=Msg.ONLY_ONE_PERMITTED.format('Lati', m.class_name)
    ):
        m.validate()


def test_long_only_one() -> None:
    """Check that the lati structure can be used only once by Map."""
    m = Map([Lati('N18.150944'), Long('E168.150944'), Long('E168.150944')])
    with pytest.raises(
        ValueError, match=Msg.ONLY_ONE_PERMITTED.format('Long', m.class_name)
    ):
        m.validate()


#    e. Catch bad input.


def test_lati_bad_direction() -> None:
    """Check that the latitude direction is either N or S."""
    m = Map([Lati('A10.1'), Long('E168.150944')])
    with pytest.raises(
        ValueError,
        match=Msg.LATI_NORTH_SOUTH.format(
            'A', 'A10.1', Default.LATI_NORTH, Default.LATI_SOUTH, 'Lati'
        ),
    ):
        m.validate()


def test_long_bad_direction() -> None:
    """Check that the longitude direction is either E or W."""
    m = Map([Lati('N10.1'), Long('K168.150944')])
    with pytest.raises(
        ValueError,
        match=Msg.LONG_EAST_WEST.format(
            'K', 'K168.150944', Default.LONG_EAST, Default.LONG_WEST, 'Long'
        ),
    ):
        m.validate()


def test_lati_range_high() -> None:
    """Check that the latitude high stays within its range."""
    m = Map([Lati('N90.1'), Long('E168.150944')])
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.LATI_RANGE.format(
                'N90.1', str(Default.LATI_LOW), str(Default.LATI_HIGH), 'Lati'
            )
        ),
    ):
        m.validate()


def test_lati_range_low() -> None:
    """Check that the latitude low stays within its range."""
    m = Map([Lati('S90.1'), Long('E168.150944')])
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.LATI_RANGE.format(
                'S90.1', str(Default.LATI_LOW), str(Default.LATI_HIGH), 'Lati'
            )
        ),
    ):
        m.validate()


def test_long_range_high() -> None:
    """Check that the longitude high stays within its range."""
    m = Map([Lati('N80.1'), Long('E180.1')])
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.LONG_RANGE.format(
                'E180.1', str(Default.LONG_LOW), str(Default.LONG_HIGH), 'Long'
            )
        ),
    ):
        m.validate()


def test_long_range_low() -> None:
    """Check that the longitude low stays within its range."""
    m = Map([Lati('S80.1'), Long('W180.1')])
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.LONG_RANGE.format(
                'W180.1', str(Default.LONG_LOW), str(Default.LONG_HIGH), 'Long'
            )
        ),
    ):
        m.validate()


# 2. Ged Section


def test_ged() -> None:
    """Illustrate the standard use of the class."""
    m = Map([Lati('N18.150944'), Long('E168.150944')])
    assert m.ged(1) == '1 MAP\n2 LATI N18.150944\n2 LONG E168.150944\n'


def test_ged_using_input() -> None:
    """Illustrate the use of the Map class with Input."""
    m = Map([Lati(Input.lati(18, 9, 3.4)), Long(Input.long(168, 9, 3.4))])
    assert m.ged(1) == '1 MAP\n2 LATI N18.150944\n2 LONG E168.150944\n'


# 3. Code Section


def test_code() -> None:
    """Illustrate code running."""
    m = Map([Lati(Input.lati(18, 9, 3.4)), Long(Input.long(168, 9, 3.4))])
    assert (
        m.code()
        == "\nMap(\n    subs = [\n        Lati('N18.150944'),\n        Long('E168.150944'),\n    ],\n)"
    )
