# change_creation_test.py
"""Tests to cover the Chan and Crea structures.

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
from genedata.messages import Msg


# 1. Validate Section
#    a. Good run.
def test_good_run_chan() -> None:
    """Run a successful use of the structure."""
    h = gc.Chan(gc.DateExact('1 JAN 2000', gc.Time('12:12:12')))
    assert h.validate()


def test_good_run_crea() -> None:
    """Run a successful use of the structure."""
    h = gc.Crea(gc.DateExact('1 JAN 2000', gc.Time('12:12:12')))
    assert h.validate()


#    b. Catch not permitted substructure.


def test_not_permitted_chan() -> None:
    """Check that a substructure not in the permitted list cannot be used by the structure."""
    m = gc.Chan([gc.Phrase('test'), gc.DateExact('1 JAN 2000', gc.Time('12:12:12'))])
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_PERMITTED.format('Phrase', m.permitted, m.class_name)
        ),
    ):
        m.validate()


def test_not_permitted_crea() -> None:
    """Check that a substructure not in the permitted list cannot be used by the structure."""
    m = gc.Crea([gc.Phrase('test'), gc.DateExact('1 JAN 2000', gc.Time('12:12:12'))])
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_PERMITTED.format('Phrase', m.permitted, m.class_name)
        ),
    ):
        m.validate()


#    c. Catch not included but required substructures.


#    d. Catch more than one when only one permitted.


def test_chan_only_one() -> None:
    """Check that the lati structure can be used only once by Map."""
    m = gc.Chan(
        [
            gc.DateExact('1 JAN 2000', gc.Time('12:12:12')),
            gc.DateExact('1 JAN 2000', gc.Time('12:12:12')),
        ]
    )
    with pytest.raises(
        ValueError, match=Msg.ONLY_ONE_PERMITTED.format('DateExact', m.class_name)
    ):
        m.validate()


def test_crea_only_one() -> None:
    """Check that the lati structure can be used only once by Map."""
    m = gc.Crea(
        [
            gc.DateExact('1 JAN 2000', gc.Time('12:12:12')),
            gc.DateExact('1 JAN 2000', gc.Time('12:12:12')),
        ]
    )
    with pytest.raises(
        ValueError, match=Msg.ONLY_ONE_PERMITTED.format('DateExact', m.class_name)
    ):
        m.validate()


#    e. Catch bad input.


# 2. Ged Section


# def test_ged() -> None:
#     """Illustrate the standard use of the class."""
#     m = gc.Map([gc.Lati('N18.150944'), gc.Long('E168.150944')])
#     assert m.ged(1) == '1 MAP\n2 LATI N18.150944\n2 LONG E168.150944\n'


# def test_ged_using_input() -> None:
#     """Illustrate the use of the Map class with Input."""
#     m = gc.Map([gc.Lati(Input.lati(18, 9, 3.4)), gc.Long(Input.long(168, 9, 3.4))])
#     assert m.ged(1) == '1 MAP\n2 LATI N18.150944\n2 LONG E168.150944\n'


# 3. Code Section


# def test_code() -> None:
#     """Illustrate code running."""
#     m = gc.Map([gc.Lati(Input.lati(18, 9, 3.4)), gc.Long(Input.long(168, 9, 3.4))])
#     assert (
#         m.code()
#         == "\ngc.Map(\n    [\n        gc.Lati('N18.150944'),\n        gc.Long('E168.150944'),\n    ]\n)"
#     )
