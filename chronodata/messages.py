# Licensed under a 3-clause BSD style license - see LICENSE.md
"""Strings to send messages to the user from all modules which may benefit
from internationalization.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Column:
    """The following constants are used for column headings."""

    CHART_COLOR: str = 'Chart Color'
    CHART_LINE_STYLE: str = 'Chart Line Style'
    CHRONO_NAME: str = 'Chronology'
    CODE: str = 'Code'
    DATETIME: str = 'Date/Time'
    DURATION: str = 'Duration Years'
    ISSUE: str = 'Issue'
    SKEW: str = 'Skewness'
    LINE: str = 'Line'
    MEAN: str = 'Mean'
    MEDIAN: str = 'Median'
    RESERVED: str = 'Reserved Keys'
    STD: str = 'Standard Deviation'
    TEST_NAME: str = 'Test Name'
    VALUE: str = 'Value'
    YEARS_AGO: str = 'Years Ago'
    YEARS_SINCE: str = 'Years Since {0}'


@dataclass(frozen=True)
class Issue:
    """Messages to report issues."""

    BAD_INC: str = 'The level incremented more than 1 on this line.'
    LESS_ZERO: str = 'The level decreated below zero on this line.'
    NO_ZERO: str = 'The first character is the file was not zero.'


@dataclass(frozen=True)
class Label:
    """The following constants define messages that are returned acknowledging
    events that happened.
    """

    CHRONOLOGIES: str = 'Chronologies'
    TEST: str = '{0} Tests'
    YEARS: str = 'Years'


@dataclass(frozen=True)
class Msg:
    """The following constants define messages that are returned acknowledging
    events that happened.
    """

    ADDED: str = 'The {0} "{1}" has been added to the chronology.'
    ADD_ACTOR: str = 'The actor "{0}" has been added.'
    ADD_CHALLENGE: str = 'The challenge "{0}" has been added.'
    ADD_COMMENT: str = 'The comment "{0}" has been added.'
    ADD_EVENT: str = 'The event "{0}" has been added to "{1}".'
    ADD_MARKER: str = 'The marker "{0}" has been added.'
    ADD_PERIOD: str = 'The period "{0}" has been added.'
    ADD_SOURCE: str = 'The source "{0}" has been added.'
    ADD_TEXT: str = 'The text "{0}" has been added.'
    ADDED_RECORD: str = 'Added {0} record with xref {1}.'
    BAD_CALENDAR: str = 'The calendar "{0}" is not recognized.'
    BAD_DATE: str = 'The date value "{0}" does not fit a {1} calendar.'
    BAD_LABEL: str = 'The date "{0}" contains an inappropriate label "{1}".'
    BAD_MONTH: str = 'The month "{1}" for calend "{0}" is not recognized.'
    CALENDARS_DONT_MATCH: str = 'The calendars "{0}" and "{1}" do not match.'
    CHALLENGE_BEGIN: str = 'Challenge "{0}" for the {1} chronologies has begun.'
    CHALLENGE_LOADED: str = (
        'Challenge "{0}" for the {1} chronologies has been loaded.'
    )
    CHALLENGE_SAVED: str = 'Challenge "{0}" has been saved in {1}.'
    CHANGED: str = 'The chronology has been changed to the "{0}" calendar.'
    COMMENT_REMOVED: str = 'Comment {0} "{1}" has been removed.'
    COUNT_RESERVED: str = '{0} reserved keys were used.'
    FILE_EXISTS: str = 'The file "{0}" exists. Use `save` with `overwrite=True` to overwrite the file.'
    FILE_SAVED: str = 'The file "{0}" has been saved.'
    HAS_CALENDAR: str = 'The chronology already has the "{0}" calendar.'
    ITEM_ADDED: str = 'Item "{0}" has been added.'
    ITEM_NOT_FOUND: str = 'Item "{0}" was not found.'
    ITEM_REMOVED: str = 'Item "{0}" has been removed.'
    KEY_REMOVED: str = 'The name "{0}" has been removed from "{1}".'
    LOADED: str = 'The "{0}" chronology has been loaded from the "{1}" file.'
    LOAD_FAILED: str = 'The file "{0}" failed to load.'
    NAME_OR_FILENAME: str = 'Either a name or a filename needs to be provided.'
    NEG_YEAR: str = 'Negative year but a negative label "{0}".'
    NO_COMMENTS: str = 'There are no comments for the {0} chronology.'
    NO_DICT_NAME: str = 'The chronology "{0}" has no {1}.'
    NO_NAME: str = 'There is no value for the `name` parameter.'
    NO_TESTS: str = 'There are no tests in the "{0}" challenge.'
    NO_VALUE: str = 'No value was entered for a required parameter.'
    NOT_IN_DICT: str = 'The name "{0}" is not in the "{1}".'
    NOT_RECORD: str = 'The xref value "{0}" is not a {1} xref value.'
    NOT_REMOVABLE: str = 'The name "{0}" is a reserved key.'
    NOT_VALID_ENUM: str = 'The value "{0}" is not in the {1} enumeration.'
    ONE: str = 'One reserved key was used.'
    ONE_TEST: str = 'There is only one test in the "{0}" challenge.'
    OUT_OF_RANGE: str = 'There is no comment at index {0}.'
    POS_YEAR: str = 'Negative year but positive label "{0}".'
    REMOVE_ALL_COMMENTS: str = 'All comments have been removed.'
    RENAME: str = 'The chronology has been renamed "{0}".'
    RESERVED: str = 'The key "{0}" is a reserved key.'
    SAVED: str = 'The chronology "{0}" has been saved to "{1}".'
    SAVE_FIRST: str = 'Write the chronology "{0}" to a named file first.'
    STARTED: str = 'The "{0}" chronology has been started.'
    STRICT: str = 'Strict formatting of dates has been set to "{0}".'
    UNRECOGNIZED: str = 'The file "{0}" has an unrecognized extension.'
