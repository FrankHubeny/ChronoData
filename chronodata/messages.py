# Licensed under a 3-clause BSD style license - see LICENSE.md
"""Strings to send messages to the user from all modules which may benefit
from internationalization.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Example:
    EMPTY_CODE: str = 'Empty Example'
    FULL: str = 'First Example'
    ALTERNATE: str = 'Second Example'
    LANGUAGE: str = 'Third Example'
    EMPTY_GEDCOM: str = 'There should be no GEDCOM lines produced.'
    GEDCOM: str = 'The following GEDCOM lines are produced.'


@dataclass(frozen=True)
class Issue:
    """Messages to report issues."""

    BAD_INC: str = 'The level incremented more than 1 on this line.'
    LESS_ZERO: str = 'The level decreated below zero on this line.'
    NO_ZERO: str = 'The first character is the file was not zero.'


@dataclass(frozen=True)
class Msg:
    """The following constants define messages that are returned acknowledging
    events that happened.
    """

    BAD_CALENDAR: str = 'The calendar "{0}" is not recognized.'
    BAD_MONTH: str = 'The month "{1}" for calend "{0}" is not recognized.'
    DUPLICATE_RECORD: str = (
        'The cross-reference identifier {0} has already been used.'
    )
    EMPTY_EVENT_TYPE: str = 'The event type for tag {0} must have some value.'
    EXID_TYPE: str = 'The EXID identifier requires a type description of it.'
    INVALID_VALUES: str = '"{0}" is not in the valid values of "{1}".'
    LOADED: str = 'The "{0}" genealogy has been loaded from the "{1}" file.'
    LOAD_FAILED: str = 'The file "{0}" failed to load.'
    MISSING: str = 'These xref values {0} are missing record definitions.'
    NEGATIVE_ERROR: str = 'The value "{0}" is less than zero.'
    NEG_YEAR: str = 'Negative year but a negative label "{0}".'
    NOT_DEFAULT: str = 'The value "{0}" cannot be the default value "{1}".'
    NOT_FLOAT: str = 'The {1} value "{0}" is not a float.'
    NOT_RECORD: str = 'The value "{0}" is not an appropriate xref value.'
    NOT_UNICODE: str = 'The file "{0}" is not unicode encoded.'
    NOT_VALID_ENUM: str = 'The tag {0} is not in the list of valid tags.'
    RANGE: str = 'The value "{0}" is not greater than or equal to "{1}" but strictly less than "{2}".'
    RANGE_ERROR: str = '"{0}" must be greater than or equal to "{1}" and less than or equal to "{2}".'
    SLGC_REQUIRES_FAM: str = 'The Tag.SLGC requires a valid family cross reference identifier.'
    STARTED: str = 'The "{0}" genealogy has been started.'
    TAG_PAYLOAD: str = (
        'The tag {0} cannot have a payload different from "Y" or "".'
    )
    WRONG_TYPE: str = '"{0}" has type {1} but should have type {2}.'
    XREF_EXISTS: str = 'The identifier "{0}" built from "{1}" already exists.'
