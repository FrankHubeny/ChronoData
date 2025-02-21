# map_test
"""Tests to cover the Map NamedTuple.

1. Validate: Exercise all validation checks.

2. Ged: Exercise the generation of ged data.

3. Code: Exercise the code method with both full output and non-empty output.

"""

import pytest

from genedata.messages import Msg
from genedata.store import Extension, ExtTag, Map

ext_taga = ExtTag('_EXTA', 'tests/data/_EXT.yaml')
ext_tagb = ExtTag('_EXTB', 'tests/data/_EXT.yaml')
extrec_tag = ExtTag('EXTREC', 'tests/data/_EXTREC.yaml')
extsuba_tag = ExtTag('_EXTSUBA', 'tests/data/_EXTSUBA.yaml')
extsubb_tag = ExtTag('_EXTSUBB', 'tests/data/_EXTSUBB.yaml')
extsubc_tag = ExtTag('_EXTSUBC', 'tests/data/_EXTSUBC.yaml')
extsubm_tag = ExtTag('_EXTSUBM', 'tests/data/_EXTSUBM.yaml')
extsubsuba_tag = ExtTag('_EXTSUBSUBA', 'tests/data/_EXTSUBSUBA.yaml')
extsubsubb_tag = ExtTag('_EXTSUBSUBB', 'tests/data/_EXTSUBSUBB.yaml')
extsubsubm_tag = ExtTag('_EXTSUBSUBM', 'tests/data/_EXTSUBSUBM.yaml')
extsubsubr_tag = ExtTag('_EXTSUBSUBR', 'tests/data/_EXTSUBSUBR.yaml')
bad_ext_tag = ExtTag('_BADEXT', 'tests/data/_BAD_EXT.yaml')

exta = Extension(ext_taga, payload='something', extra='else')
extb = Extension(ext_tagb, payload='something', extra='else')
extrec = Extension(extrec_tag, payload='something', extra='else')
extsuba = Extension(extsuba_tag, payload='something', extra='else')
extsuba2 = Extension(extsuba_tag, payload='some', extra='thing')
extsubb = Extension(extsubb_tag, payload='something', extra='else')
extsubc = Extension(extsubc_tag, payload='something', extra='else')
extsubm = Extension(extsubm_tag, payload='something', extra='else')
extsubsuba = Extension(extsubsuba_tag, payload='something', extra='else')
extsubsubb = Extension(extsubsubb_tag, payload='something', extra='else')
extsubsubm = Extension(extsubsubm_tag, payload='something', extra='else')
extsubsubr = Extension(extsubsubr_tag, payload='something', extra='else')
bad_ext = Extension(bad_ext_tag, payload='something', extra='else')
exta_one = Extension(ext_taga, payload='something', extra='else', substructures=extsuba)
exta_two = Extension(ext_taga, payload='something', extra='else', substructures=[extsuba, extsubb])
exta_two_single = Extension(ext_taga, payload='something', extra='else', substructures=[extsuba, extsuba2])


# Validate Section


def test_latitude_float() -> None:
    """Check that only float values are permitted by checking int which is close to float."""
    with pytest.raises(TypeError, match=Msg.WRONG_TYPE.format(10, int, float)):
        Map(10, 50.0).validate()


def test_longitude_float() -> None:
    """Check that only float values are permitted by checking int which is close to float."""
    with pytest.raises(TypeError, match=Msg.WRONG_TYPE.format(50, int, float)):
        Map(10.0, 50).validate()


def test_latitude_no_list() -> None:
    """Check that the no_list parameter when true triggers a TypeError."""
    with pytest.raises(TypeError, match=Msg.NO_LIST):
        Map([91.0], 10.0).validate()  # type: ignore[arg-type]


def test_longitude_no_list() -> None:
    """Check that the no_list parameter when true triggers a TypeError."""
    with pytest.raises(TypeError, match=Msg.NO_LIST):
        Map(1.0, [200.0]).validate()  # type: ignore[arg-type]


def test_latitude_range() -> None:
    """Check that values outside of the accepted range trigger a ValueError."""
    with pytest.raises(
        ValueError, match=Msg.RANGE_ERROR.format('91.0', '-90.0', '90.0')
    ):
        Map(91.0, 10.0).validate()


def test_longitude_range() -> None:
    """Check that values outside of the accepted range trigger a ValueError."""
    with pytest.raises(
        ValueError, match=Msg.RANGE_ERROR.format('200.0', '-180.0', '180.0')
    ):
        Map(1.0, 200.0).validate()


def test_ext_none() -> None:
    """No exceptions validate as true."""
    assert Map(1.0, 90.0, map_ext=None).validate() is True


def test_ext_empty_list() -> None:
    """Empty list of exceptions validate as true."""
    assert Map(1.0, 90.0, map_ext=[]).validate() is True


def test_map_ext() -> None:
    """Check that the tag is not in the superstructures of the extension tag."""
    with pytest.raises(
        ValueError, match=Msg.NOT_DEFINED_FOR_STRUCTURE.format('MAP')
    ):
        Map(1.0, 10.0, map_ext=bad_ext).validate()


def test_lati_ext() -> None:
    """Check that the tag is not in the superstructures of the extension tag."""
    with pytest.raises(
        ValueError, match=Msg.NOT_DEFINED_FOR_STRUCTURE.format('LATI')
    ):
        Map(1.0, 10.0, lati_ext=bad_ext).validate()


def test_long_ext() -> None:
    """Check that the tag is not in the superstructures of the extension tag."""
    with pytest.raises(
        ValueError, match=Msg.NOT_DEFINED_FOR_STRUCTURE.format('LONG')
    ):
        Map(1.0, 10.0, long_ext=bad_ext).validate()

def test_map_ext_one_substructure() -> None:
    """Check that the tag is not in the superstructures of the extension tag."""
    assert Map(1.0, 10.0, map_ext=exta_one).validate() is True


def test_lati_ext_one_substructure() -> None:
    """Check that the tag is not in the superstructures of the extension tag."""
    assert Map(1.0, 10.0, lati_ext=exta_one).validate() is True


def test_long_ext_one_substructure() -> None:
    """Check that the tag is not in the superstructures of the extension tag."""
    assert Map(1.0, 10.0, long_ext=exta_one).validate() is True

def test_map_ext_two_substructures() -> None:
    """Check that the tag is not in the superstructures of the extension tag."""
    assert Map(1.0, 10.0, map_ext=exta_two).validate() is True


def test_lati_ext_two_substructures() -> None:
    """Check that the tag is not in the superstructures of the extension tag."""
    assert Map(1.0, 10.0, lati_ext=exta_two).validate() is True


def test_long_ext_two_substructures() -> None:
    """Check that the tag is not in the superstructures of the extension tag."""
    assert Map(1.0, 10.0, long_ext=exta_two).validate() is True

def test_map_ext_single_test() -> None:
    """Check that a tag restricted to appearing only once does not appear more than once."""
    with pytest.raises(
        ValueError, match=Msg.ONLY_ONCE.format('_EXTSUBA', '_EXT')
    ):
        Map(1.0, 10.0, map_ext=exta_two_single).validate()


# Ged Section


standard = [
    ('first[0]', '3 MAP'),
    ('first[1]', '4 LATI N10.000000'),
    ('first[2]', '4 LONG E50.000000'),
    ('second[0]', '4 MAP'),
    ('second[1]', '5 LATI S10.000000'),
    ('second[2]', '5 LONG W50.000000'),
    ('third[0]', '1 MAP'),
    ('third[1]', '2 LATI N0.000000'),
    ('third[2]', '2 LONG E0.000000'),
    ('fourth[0]', '1 MAP'),
    ('fourth[1]', '2 LATI N90.000000'),
    ('fourth[2]', '2 LONG E180.000000'),
    ('fifth[0]', '1 MAP'),
    ('fifth[1]', '2 LATI S90.000000'),
    ('fifth[2]', '2 LONG W180.000000'),
]


@pytest.mark.parametrize('test_input,expected', standard)  # noqa: PT006
def test_standard(test_input: str, expected: str) -> None:  # noqa: ARG001
    """Illustrate the standard use of the class."""
    m = Map(10.0, 50.0)
    first = m.ged(3).split('\n')  # noqa: F841
    n = Map(-10.0, -50.0)
    second = n.ged(4).split('\n')  # noqa: F841
    p = Map(0.0, 0.0)
    third = p.ged(1).split('\n')  # noqa: F841
    r = Map(90.0, 180.0)
    fourth = r.ged(1).split('\n')  # noqa: F841
    s = Map(-90.0, -180.0)
    fifth = s.ged(1).split('\n')  # noqa: F841


extension_one_layer = [
    ('first[0]', '3 MAP'),
    ('first[1]', '4 _EXTA something else'),
    ('first[2]', '4 LATI N10.000000'),
    ('first[3]', '4 LONG E50.000000'),
    ('second[0]', '4 MAP'),
    ('second[1]', '5 LATI S10.000000'),
    ('second[2]', '6 _EXTA something else'),
    ('second[3]', '5 LONG W50.000000'),
    ('third[0]', '1 MAP'),
    ('third[1]', '2 LATI N0.000000'),
    ('third[2]', '2 LONG E0.000000'),
    ('third[3]', '3 _EXTA something else'),
]


@pytest.mark.parametrize('test_input,expected', extension_one_layer)  # noqa: PT006
def test_extension_one_layer(test_input: str, expected: str) -> None:  # noqa: ARG001
    """Illustrate the extension use of the class for only one extension substructure."""
    m = Map(10.0, 50.0, map_ext=exta)
    first = m.ged(3).split('\n')  # noqa: F841
    n = Map(-10.0, -50.0, lati_ext=exta)
    second = n.ged(4).split('\n')  # noqa: F841
    p = Map(0.0, 0.0, long_ext=exta)
    third = p.ged(1).split('\n')  # noqa: F841


extension_one_layer_many = [
    ('first[0]', '3 MAP'),
    ('first[1]', '4 _EXTA something else'),
    ('first[2]', '4 _EXTB something else'),
    ('first[3]', '4 LATI N10.000000'),
    ('first[4]', '4 LONG E50.000000'),
    ('second[0]', '4 MAP'),
    ('second[1]', '5 LATI S10.000000'),
    ('second[2]', '6 _EXTA something else'),
    ('second[3]', '6 _EXTB something else'),
    ('second[4]', '5 LONG W50.000000'),
    ('third[0]', '1 MAP'),
    ('third[1]', '2 LATI N0.000000'),
    ('third[2]', '2 LONG E0.000000'),
    ('third[3]', '3 _EXTA something else'),
    ('third[4]', '3 _EXTB something else'),
]


@pytest.mark.parametrize('test_input,expected', extension_one_layer_many)  # noqa: PT006
def test_extension_one_layer_many(test_input: str, expected: str) -> None:  # noqa: ARG001
    """Illustrate the extension use of the class for only one extension substructure."""
    m = Map(10.0, 50.0, map_ext=[exta, extb])
    first = m.ged(3).split('\n')  # noqa: F841
    n = Map(-10.0, -50.0, lati_ext=[exta, extb])
    second = n.ged(4).split('\n')  # noqa: F841
    p = Map(0.0, 0.0, long_ext=[exta, extb])
    third = p.ged(1).split('\n')  # noqa: F841
    

# Code Section


code = [
    ('first[1]', '    Map('),
    ('first[2]', '        latitude = -90.0,'),
    ('first[3]', '        longitude = -180.0,'),
    ('first[4]', '        map_ext = None,'),
    ('first[5]', '        latitude_ext = None,'),
    ('first[6]', '        longitude_ext = None,'),
    ('first[7]', '    )'),
    ('second[1]', 'Map('),
    ('second[2]', '    latitude = -90.0,'),
    ('second[3]', '    longitude = -180.0,'),
    ('second[4]', '    map_ext = None,'),
    ('second[5]', '    latitude_ext = None,'),
    ('second[6]', '    longitude_ext = None,'),
    ('second[7]', ')'),
    ('third[1]', 'Map('),
    ('third[2]', '    latitude = -90.0,'),
    ('third[3]', '    longitude = -180.0,'),
    ('third[4]', ')'),
]


@pytest.mark.parametrize('test_input,expected', code)  # noqa: PT006
def test_code(test_input: str, expected: str) -> None:  # noqa: ARG001
    """Illustrate code running under different tabs and full arguments."""
    t = Map(-90.0, -180.0)
    first = t.code(tabs=1, full=True).split('\n')  # noqa: F841
    second = t.code(tabs=0, full=True).split('\n')  # noqa: F841
    third = t.code(tabs=0, full=False).split('\n')  # noqa: F841
