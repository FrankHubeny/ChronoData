# read_write_ged.py
"""Test methods to help reading and writing ged files."""

import pytest

from genedata.build import Genealogy
from genedata.classes70 import Gedc, GedcVers, Head
from genedata.constants import Default
from genedata.messages import Msg
from genedata.methods import Util

ged_version: str = '7.0'


def test_show_ged_no_header() -> None:
    g = Genealogy(version=ged_version)
    with pytest.raises(ValueError, match=Msg.MISSING_HEADER):
        g.show_ged()


def test_file_recognized_at_init() -> None:
    filename: str = 'tests/ged_test/minimal70.ged'
    g = Genealogy(filename=filename)
    assert g.filename == filename


def test_save_ged() -> None:
    g = Genealogy(version=ged_version)
    file: str = 'tests/build_test/simple.ged'
    ged: str = """0 HEAD
1 GEDC
2 VERS 7.0
0 TRLR"""
    head: Head = Head(Gedc(GedcVers('7.0')))
    g.stage(head)
    g.save_ged(file)
    read_back: str = Util.read(file)
    assert read_back == ged


def test_add_calendar_tag() -> None:
    g = Genealogy()
    g.add_tag('_GREGORIAN', 'tests/data/good_calendar.yaml')
    assert (
        g.specification[Default.YAML_TYPE_CALENDAR][1][Default.YAML_TYPE]
        == Default.YAML_TYPE_CALENDAR
    )


def test_add_calendar_tag_underline_upper() -> None:
    g = Genealogy()
    g.add_tag('gregorian', 'tests/data/good_calendar.yaml')
    assert (
        g.specification[Default.YAML_TYPE_CALENDAR][1][
            Default.YAML_STANDARD_TAG
        ]
        == 'GREGORIAN'
    )
