# input_test.py
"""Tests to cover the Input class.

"""

import pytest

from genedata.constants import Default
from genedata.messages import Msg
from genedata.methods import Input


def test_phone() -> None:
    assert Input.phone(1,222,333,4444) == '+1 222 333 4444'

def test_phone_bad_country_min() -> None:
    with pytest.raises(ValueError, match=(Msg.PHONE_COUNTRY_CODE.format(
                    '0',
                    Default.PHONE_COUNTRY_MIN,
                    Default.PHONE_COUNTRY_MAX,
                )
            )): 
        Input.phone(0,111,222,3333)

def test_phone_bad_country_max() -> None:
    with pytest.raises(ValueError, match=(Msg.PHONE_COUNTRY_CODE.format(
                    '1000',
                    Default.PHONE_COUNTRY_MIN,
                    Default.PHONE_COUNTRY_MAX,
                )
            )): 
        Input.phone(1000,111,222,3333)

def test_phone_bad_area_min() -> None:
    with pytest.raises(ValueError, match=(Msg.PHONE_AREA_CODE.format(
                    '0',
                    Default.PHONE_AREA_MIN,
                    Default.PHONE_AREA_MAX,
                )
            )): 
        Input.phone(1,0,222,3333)

def test_phone_bad_area_max() -> None:
    with pytest.raises(ValueError, match=(Msg.PHONE_AREA_CODE.format(
                    '1000',
                    Default.PHONE_AREA_MIN,
                    Default.PHONE_AREA_MAX,
                )
            )): 
        Input.phone(1,1000,222,3333)

def test_phone_bad_prefix_min() -> None:
    with pytest.raises(ValueError, match=(Msg.PHONE_PREFIX_CODE.format(
                    '0',
                    Default.PHONE_PREFIX_MIN,
                    Default.PHONE_PREFIX_MAX,
                )
            )): 
        Input.phone(1,100,0,3333)

def test_phone_bad_prefix_max() -> None:
    with pytest.raises(ValueError, match=(Msg.PHONE_PREFIX_CODE.format(
                    '1000',
                    Default.PHONE_PREFIX_MIN,
                    Default.PHONE_PREFIX_MAX,
                )
            )): 
        Input.phone(1,100,1000,3333)

def test_phone_bad_line_min() -> None:
    with pytest.raises(ValueError, match=(Msg.PHONE_LINE_CODE.format(
                    '0',
                    Default.PHONE_LINE_MIN,
                    Default.PHONE_LINE_MAX,
                )
            )): 
        Input.phone(1,100,222,0)

def test_phone_bad_line_max() -> None:
    with pytest.raises(ValueError, match=(Msg.PHONE_LINE_CODE.format(
                    '10000',
                    Default.PHONE_LINE_MIN,
                    Default.PHONE_LINE_MAX,
                )
            )): 
        Input.phone(1,100,222,10000)

def test_place() -> None:
    assert Input.place('Chicago', 'Illinois', 'Cook', 'USA') == 'Chicago, Illinois, Cook, USA'