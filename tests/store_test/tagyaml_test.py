# tagdata_test
"""Tests to cover the class TagYaml containing static methods.

1. Get: Errors Caught
    a. Not a yaml file
    b. Missing a required section
    c. Unrecognized type
    d. No tag names
    e. No calendars defined, but months or epochs

2. Get: Successful Result
    a. Structure type
    b. Enumeration type
    c. Enumeration set type
    d. Calendar type
    e. Month type
    f. Data Type type
    g. Uri type

"""

import pytest

from genedata.gedcom import Default
from genedata.messages import Msg
from genedata.store import TagYaml

# Get: Errors Caught

## Not a yaml file

def test_not_yaml_file() -> None:
    """Check that the yaml file has the proper directive."""
    with pytest.raises(
        ValueError,
        match=Msg.YAML_NOT_YAML_FILE.format(
            'tests/data/bad_not_yaml_file.yaml', Default.YAML_DIRECTIVE
        ),
    ):
        TagYaml.get(url='tests/data/bad_not_yaml_file.yaml')

## Missing a required section

def test_missing_required_lang() -> None:
    """Check that the yaml file has a missing `lang` section."""
    with pytest.raises(
        ValueError,
        match=Msg.YAML_MISSING_REQUIRED_LANG.format(
            'tests/data/bad_missing_required_lang.yaml'
        ),
    ):
        TagYaml.get(url='tests/data/bad_missing_required_lang.yaml')


def test_missing_required_type() -> None:
    """Check that the yaml file has a missing `type` section."""
    with pytest.raises(
        ValueError,
        match=Msg.YAML_MISSING_REQUIRED_TYPE.format(
            'tests/data/bad_missing_required_type.yaml'
        ),
    ):
        TagYaml.get(url='tests/data/bad_missing_required_type.yaml')


def test_missing_required_uri() -> None:
    """Check that the yaml file has a missing `uri` section."""
    with pytest.raises(
        ValueError,
        match=Msg.YAML_MISSING_REQUIRED_URI.format(
            'tests/data/bad_missing_required_uri.yaml'
        ),
    ):
        TagYaml.get(url='tests/data/bad_missing_required_uri.yaml')

def test_empty_required_lang() -> None:
    """Check that the yaml file has an empty `lang` entry."""
    with pytest.raises(
        ValueError,
        match=Msg.YAML_MISSING_REQUIRED_LANG.format(
            'tests/data/bad_empty_required_lang.yaml'
        ),
    ):
        TagYaml.get(url='tests/data/bad_empty_required_lang.yaml')


def test_empty_required_type() -> None:
    """Check that the yaml file has an empty `type` entry."""
    with pytest.raises(
        ValueError,
        match=Msg.YAML_MISSING_REQUIRED_TYPE.format(
            'tests/data/bad_empty_required_type.yaml'
        ),
    ):
        TagYaml.get(url='tests/data/bad_empty_required_type.yaml')


def test_empty_required_uri() -> None:
    """Check that the yaml file has an empty `uri` entry."""
    with pytest.raises(
        ValueError,
        match=Msg.YAML_MISSING_REQUIRED_URI.format(
            'tests/data/bad_empty_required_uri.yaml'
        ),
    ):
        TagYaml.get(url='tests/data/bad_empty_required_uri.yaml')

## Unrecognized type

def test_unrecognized_type() -> None:
    """Check that the yaml file a recognized type value."""
    with pytest.raises(
        ValueError,
        match=Msg.YAML_UNRECOGNIZED_TYPE.format(
            'abcdef'
        ),
    ):
        TagYaml.get(url='tests/data/bad_unrecognized_type.yaml')

## No tag names

def test_no_tag_name() -> None:
    """Check that the yaml file has either a standard or extension tag."""
    with pytest.raises(
        ValueError,
        match=Msg.YAML_NO_TAG_NAME,
    ):
        TagYaml.get(url='tests/data/bad_no_tag_names.yaml')

## No calendars defined, but months or epochs

# Get: Successful Result

## Structure type

structure_test = [
    ('s.value', 'MAP'),
    ('s.lang', 'en-US'),
    ('s.type', 'structure'),
    ('s.uri', 'https://gedcom.io/terms/v7/MAP'),
    ('s.standard_tag', 'MAP'),
    ('s.extension_tags', None),
    ('s.label', 'Map'),
    ('s.help_text', None),
    ('s.documentation', None),
    ('s.payload', 'null'),
    ('s.contact', 'https://gedcom.io/community/'),
    ('s.supers[0]', 'PLAC'),
    ('s.subs[0]', 'LATI'),
    ('s.subs[1]', 'LONG'),
    ('s.required[0]', 'LATI'),
    ('s.required[1]', 'LONG'),
    ('s.single[0]', 'LATI'),
    ('s.single[1]', 'LONG'),
    ('s.value_of', None),
    ('s.calendars', None),
    ('s.months', None),
    ('s.epochs', None),
    ('s.contact', ''),
    ('s.change_controller', ''),
]


@pytest.mark.parametrize('test_input,expected', structure_test)  # noqa: PT006
def test_good_structure(test_input: str, expected: str | int | bool) -> None:  # noqa: ARG001
    # Test reading a structure yaml file.
    s = TagYaml.get(url='tests/data/good_structure.yaml')  # noqa: F841

## Enumeration type
## Enumeration set type

enumeration_set_test = [
    ('s.value', 'RESN'),
    ('s.lang', 'en-US'),
    ('s.type', 'enumeration set'),
    ('s.uri', 'https://gedcom.io/terms/v7/enumset-RESN'),
    ('s.standard_tag', ''),
    ('s.extension_tags', None),
    ('s.enumeration_set', 'https://gedcom.io/terms/v7/enumset-RESN'),
    ('s.enumeration_values[0]', 'https://gedcom.io/terms/v7/enum-CONFIDENTIAL'),
    ('s.enumeration_values[1]', 'https://gedcom.io/terms/v7/enum-LOCKED'),
    ('s.enumeration_values[2]', 'https://gedcom.io/terms/v7/enum-PRIVACY'),
    ('s.label', ''),
    ('s.help_text', None),
    ('s.documentation', None),
    ('s.payload', ''),
    ('s.supers', None),
    ('s.subs', None),
    ('s.required', None),
    ('s.single', None),
    ('s.value_of', None),
    ('s.calendars', None),
    ('s.months', None),
    ('s.epochs', None),
    ('s.contact', 'https://gedcom.io/community/'),
    ('s.change_controller', ''),
]


@pytest.mark.parametrize('test_input,expected', enumeration_set_test)  # noqa: PT006
def test_good_enumeration(test_input: str, expected: str | int | bool) -> None:  # noqa: ARG001
    # Test reading an enumeration set yaml file.
    s = TagYaml.get(url='tests/data/good_enumeration_set.yaml')  # noqa: F841



## Calendar type


calendar_test = [
    ('s.lang', 'en-US'),
    ('s.type', 'calendar'),
    ('s.uri', 'https://gedcom.io/terms/v7/cal-GREGORIAN'),
    ('s.standard_tag', 'GREGORIAN'),
    ('s.extension_tags', None),
    ('s.label', 'Gregorian'),
    ('s.help_text', None),
    ('s.documentation', None),
    ('s.payload', ''),
    ('s.supers', None),
    ('s.subs', None),
    ('s.required', None),
    ('s.single', None),
    ('s.value_of', None),
    ('s.calendars', None),
    ('s.months[0]', "https://gedcom.io/terms/v7/month-JAN"),
    ('s.epochs', 'BCE'),
    ('s.contact', 'https://gedcom.io/community/'),
    ('s.change_controller', ''),
]


@pytest.mark.parametrize('test_input,expected', calendar_test)  # noqa: PT006
def test_good_calendar(test_input: str, expected: str | int | bool) -> None:  # noqa: ARG001
    # Test reading a calendar yaml file.
    s = TagYaml.get(url='tests/data/good_calendar.yaml')  # noqa: F841



## Month type

month_test = [
    ('s.lang', 'en-US'),
    ('s.type', 'month'),
    ('s.uri', 'https://gedcom.io/terms/v7/month-JAN'),
    ('s.standard_tag', 'JAN'),
    ('s.extension_tags', None),
    ('s.label', 'January'),
    ('s.help_text', None),
    ('s.documentation', None),
    ('s.payload', ''),
    ('s.supers', None),
    ('s.subs', None),
    ('s.required', None),
    ('s.single', None),
    ('s.value_of', None),
    ('s.calendars[0]', 'https://gedcom.io/terms/v7/cal-GREGORIAN'),
    ('s.calendars[1]', 'https://gedcom.io/terms/v7/cal-JULIAN'),
    ('s.months', None),
    ('s.epochs', None),
    ('s.contact', 'https://gedcom.io/community/'),
    ('s.change_controller', ''),
]


@pytest.mark.parametrize('test_input,expected', month_test)  # noqa: PT006
def test_good_month(test_input: str, expected: str | int | bool) -> None:  # noqa: ARG001
    # Test reading a month yaml file.
    s = TagYaml.get(url='tests/data/good_month.yaml')  # noqa: F841

## Data Type type


datatype_test = [
    ('s.lang', 'en-US'),
    ('s.type', 'data type'),
    ('s.uri', 'https://gedcom.io/terms/v7/type-Enum'),
    ('s.standard_tag', ''),
    ('s.extension_tags', None),
    ('s.label', ''),
    ('s.help_text', None),
    ('s.documentation', None),
    ('s.payload', ''),
    ('s.supers', None),
    ('s.subs', None),
    ('s.required', None),
    ('s.single', None),
    ('s.value_of', None),
    ('s.calendars', None),
    ('s.months', None),
    ('s.epochs', None),
    ('s.contact', 'https://gedcom.io/community/'),
    ('s.change_controller', ''),
]


@pytest.mark.parametrize('test_input,expected', datatype_test)  # noqa: PT006
def test_good_datatype(test_input: str, expected: str | int | bool) -> None:  # noqa: ARG001
    # Test reading a datatype yaml file.
    s = TagYaml.get(url='tests/data/good_datatype.yaml')  # noqa: F841


## Uri type