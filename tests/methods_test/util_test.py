# util_test.py
"""Tests to cover the Util class."""

import logging
import re
from typing import Any

import pytest

from genedata.constants import Default
from genedata.messages import Msg
from genedata.methods import Util


def test_list_gdz() -> None:
    file: str = 'tests/ged_test/minimal70.gdz'
    assert Util.list_gdz(file) == 'gedcom.ged\n'


def test_list_gdz_not_found() -> None:
    file: str = 'tests/ged_test/bad_minimal70.gdz'
    with pytest.raises(FileNotFoundError):
        Util.list_gdz(file)


def test_read_gdz_ged_file() -> None:
    file: str = 'tests/ged_test/minimal70.gdz'
    assert (
        Util.read_gdz_ged_file('gedcom.ged', file)
        == '0 HEAD\n1 GEDC\n2 VERS 7.0\n0 TRLR\n'
    )


def test_extract() -> None:
    gdz: str = 'tests/ged_test/minimal70.gdz'
    to_dir: str = 'tests/methods_test/write_out_test/'
    Util.extract('gedcom.ged', gdz, to_dir)
    read_in: str = Util.read_ged(f'{to_dir}gedcom.ged')
    assert read_in == '0 HEAD\n1 GEDC\n2 VERS 7.0\n0 TRLR'


def test_read_gdz_ged_file_not_exists() -> None:
    file: str = 'tests/ged_test/minimal70.gdz'
    assert Util.read_gdz_ged_file('gedcom_not_exists.ged', file) == ''


def test_read() -> None:
    file: str = 'tests/ged_test/minimal70.ged'
    assert Util.read(file) == '0 HEAD\n1 GEDC\n2 VERS 7.0\n0 TRLR'


def test_read_bad_file(caplog: Any) -> None:
    file: str = 'tests/ged_test/minimal70.ged123'
    with caplog.at_level(logging.INFO):
        Util.read(file)
    assert Msg.FILE_NOT_FOUND.format(file) in caplog.text

# def test_read_bad_yaml_file() -> None:
#     file: str = 'tests/ged_test/minimal70.ged123'
#     with pytest.raises(TypeError):
#         Util.read_yaml(file)
    

def test_read_binary() -> None:
    file: str = 'tests/ged_test/minimal70.ged'
    assert Util.read(file) == '0 HEAD\n1 GEDC\n2 VERS 7.0\n0 TRLR'


def test_read_url() -> None:
    url: str = 'https://gedcom.io/terms/v7/PAGE'
    data: str = Util.read(url)
    assert len(data) > 0


# def test_read_bad_url() -> None:
#     url: str = 'https://gedcom.io/terms/v7/PAGEAAAAA'
#     with pytest.raises(ValueError, match=(Msg.PAGE_NOT_FOUND)):
#         Util.read(url)


def test_read_yaml_not_yaml_file() -> None:
    file: str = 'tests/ged_test/minimal70.ged'
    with pytest.raises(
        ValueError,
        match=(Msg.YAML_NOT_YAML_FILE.format(file, Default.YAML_DIRECTIVE)),
    ):
        Util.read_yaml(file)


def test_read_yaml_bad_not_yaml_file() -> None:
    file: str = 'tests/data/bad_not_yaml_file.yaml'
    with pytest.raises(
        ValueError,
        match=(Msg.YAML_NOT_YAML_FILE.format(file, Default.YAML_DIRECTIVE)),
    ):
        Util.read_yaml(file)


def test_read_yaml_bad_unrecognized_type() -> None:
    file: str = 'tests/data/bad_unrecognized_type.yaml'
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.YAML_UNRECOGNIZED_TYPE.format('abcdef', Default.YAML_TYPE_CODES)
        ),
    ):
        Util.read_yaml(file)


def test_read_yaml_bad_no_tag_names() -> None:
    file: str = 'tests/data/bad_no_tag_names.yaml'
    with pytest.raises(
        ValueError,
        match=(Msg.YAML_NO_TAG_NAME),
    ):
        Util.read_yaml(file)


def test_read_yaml_bad_missing_required_uri() -> None:
    file: str = 'tests/data/bad_missing_required_uri.yaml'
    with pytest.raises(
        ValueError, match=(Msg.YAML_MISSING_REQUIRED_URI.format(file))
    ):
        Util.read_yaml(file)


def test_read_yaml_bad_missing_required_type() -> None:
    file: str = 'tests/data/bad_missing_required_type.yaml'
    with pytest.raises(
        ValueError, match=(Msg.YAML_MISSING_REQUIRED_TYPE.format(file))
    ):
        Util.read_yaml(file)


def test_read_yaml_bad_missing_required_lang() -> None:
    file: str = 'tests/data/bad_missing_required_lang.yaml'
    with pytest.raises(
        ValueError, match=(Msg.YAML_MISSING_REQUIRED_LANG.format(file))
    ):
        Util.read_yaml(file)


def test_read_yaml_bad_empty_required_uri() -> None:
    file: str = 'tests/data/bad_empty_required_uri.yaml'
    with pytest.raises(
        ValueError, match=(Msg.YAML_MISSING_REQUIRED_URI.format(file))
    ):
        Util.read_yaml(file)


def test_read_yaml_bad_empty_required_type() -> None:
    file: str = 'tests/data/bad_empty_required_type.yaml'
    with pytest.raises(
        ValueError, match=(Msg.YAML_MISSING_REQUIRED_TYPE.format(file))
    ):
        Util.read_yaml(file)


def test_read_bad_yaml() -> None:
    file: str = 'tests/ged_test/minimal70.ged'
    with pytest.raises(
        ValueError,
        match=(Msg.YAML_NOT_YAML_FILE.format(file, Default.YAML_DIRECTIVE)),
    ):
        Util.read_yaml(file)


def test_read_good_calendar_yaml() -> None:
    file: str = 'tests/data/good_calendar.yaml'
    assert len(Util.read_yaml(file)) > 0


def test_read_good_datatype_yaml() -> None:
    file: str = 'tests/data/good_datatype.yaml'
    assert len(Util.read_yaml(file)) > 0


def test_read_good_enumeration_set_yaml() -> None:
    file: str = 'tests/data/good_enumeration_set.yaml'
    assert len(Util.read_yaml(file)) > 0


def test_read_good_month_yaml() -> None:
    file: str = 'tests/data/good_month.yaml'
    assert len(Util.read_yaml(file)) > 0


def test_read_good_structure_yaml() -> None:
    file: str = 'tests/data/good_structure.yaml'
    assert len(Util.read_yaml(file)) > 0


def test_summary() -> None:
    file: str = 'tests/data/good_structure.yaml'
    ged: str = Default.EMPTY
    ged = Util.read(file)
    assert len(ged) > 0


def test_compare() -> None:
    file1: str = '0 HEAD\n1 GEDC\n2 VERS 7.0\n0 TRLR\n'
    file2: str = '0 HEAD\n1 GEDC\n2 VERS 7.0\n0 TRLR\n'
    assert (
        Util.compare(file1, file2)
        == '0 HEAD\n1 GEDC\n2 VERS 7.0\n0 TRLR\n\nSuccessful Match'
    )


def test_compare_fail() -> None:
    file1: str = '0 HEAD\n1 GEDC\n2 VERS 7.0\n0 TRLR\n'
    file2: str = '0 HEAD\n1 GEDC\n2 VERS 7.0\n'
    assert '* DOES NOT EQUAL *' in Util.compare(file1, file2)


def test_compare_fail_switch() -> None:
    file1: str = '0 HEAD\n1 GEDC\n2 VERS 7.0\n0 TRLR\n'
    file2: str = '0 HEAD\n1 GEDC\n2 VERS 7.0\n'
    assert '* DOES NOT EQUAL *' in Util.compare(file2, file1)


def test_write_ged() -> None:
    text: str = '0 HEAD\n1 GEDC\n2 VERS 7.0\n0 TRLR\n'
    filename: str = 'tests/methods_test/ged_test_file.ged'
    Util.write_ged(text, filename)
    read_text = Util.read(filename)
    assert text == read_text



def test_www_status() -> None:
    url: str = 'https://gedcom.io/terms/v7/HEAD'
    assert str(Util.www_status(url)) == '<Response [200]>'
