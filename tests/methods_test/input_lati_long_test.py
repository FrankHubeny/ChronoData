# input_lati_long.py
"""Test the lati and long methods in the Input class.

1. Check Input.lati().
    a. Good run.
    b. Catch range errors.

2. Check Input.long().
    a. Good run.
    b. Catch range errors.
"""

import pytest

from genedata.constants import Default
from genedata.messages import Msg
from genedata.methods import Input

# 2. Check Input.lati().
#     a. Good run.


def test_input_lati_north() -> None:
    """Check that a good value heading North is returned."""
    assert Input.lati(10, 0, 0) == 'N10.0'


def test_input_lati_south() -> None:
    """Check that a good value heading South is returned."""
    assert Input.lati(-10, 0, 0) == 'S10.0'


#     b. Catch range errors.


def test_input_lati_range_high() -> None:
    """Check that the latitude high stays within its range."""
    with pytest.raises(
        ValueError,
        match=Msg.LATI_RANGE_METHOD.format(
            '90.166944', str(Default.LATI_LOW), str(Default.LATI_HIGH)
        ),
    ):
        Input.lati(90, 10, 1)


def test_input_lati_range_low() -> None:
    """Check that the latitude low stays within its range."""
    with pytest.raises(
        ValueError,
        match=Msg.LATI_RANGE_METHOD.format(
            '-91.0', str(Default.LATI_LOW), str(Default.LATI_HIGH)
        ),
    ):
        Input.lati(-91, 0, 0)


# 2. Check Input.long().
#     a. Good run.


def test_input_long_east() -> None:
    """Check that a good value heading East is returned."""
    assert Input.long(10, 0, 0) == 'E10.0'


def test_input_long_west() -> None:
    """Check that a good value heading West is returned."""
    assert Input.long(-10, 0, 0) == 'W10.0'


#     b. Catch range errors.


def test_input_long_range_high() -> None:
    """Check that the longitude high stays within its range."""
    with pytest.raises(
        ValueError,
        match=Msg.LONG_RANGE_METHOD.format(
            '181.0', str(Default.LONG_LOW), str(Default.LONG_HIGH)
        ),
    ):
        Input.long(181, 0, 0)


def test_input_long_range_low() -> None:
    """Check that the longitude low stays within its range."""
    with pytest.raises(
        ValueError,
        match=Msg.LONG_RANGE_METHOD.format(
            '-181.0', str(Default.LONG_LOW), str(Default.LONG_HIGH)
        ),
    ):
        Input.long(-181, 0, 0)
