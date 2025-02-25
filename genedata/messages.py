# Licensed under a 3-clause BSD style license - see LICENSE.md
"""Strings to send messages to the user from all modules which may benefit
from internationalization.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Example:
    EMPTY_CODE: str = 'Empty Example'
    EMPTY_GEDCOM: str = 'There should be no GEDCOM lines produced.'
    ERROR_EXPECTED: str = 'An error is expected since the default must be changed to use the structure.'
    FULL: str = 'First Example'
    FIRST: str = 'First Example'
    GEDCOM: str = 'The following GEDCOM lines are produced.'
    GEDCOM_SPECIFICATION: str = '\n\nGEDCOM Specification\n'
    SECOND: str = 'Second Example'
    SUBSTRUCTURES: str = '\n\nSubstructures\n'
    SUPERSTRUCTURES: str = '\nSuperstructures\n'
    THIRD: str = 'Third Example'
    USER_PROVIDED: str = 'User Provided Example'
    USER_PROVIDED_EXAMPLE: str = 'The example data was provided by the user.'


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
    BAD_CHAR: str = 'The character "{0}" is not in the set of characters "{1}".'
    BAD_MONTH: str = 'The month "{1}" for calend "{0}" is not recognized.'
    CANNOT_READ_SCHEMA_DEFINITION: str = 'The schema file "{0}" cannot be read.'
    DUPLICATE_RECORD: str = (
        'The cross-reference identifier {0} has already been used.'
    )
    # EMPTY_EVENT_TYPE: str = 'The event type for tag {0} must have some value.'
    EVEN_REQUIRES_TYPE: str = 'The EVEN tag requires a non-empty TYPE.'
    EXID_TYPE: str = 'The EXID identifier requires a type description of it.'
    EXTENSION_ENUM_TAG: str = (
        'The tag "{0}" is not a value of the enumeration "{1}".'
    )
    FACT_REQUIRES_TYPE: str = 'The FACT tag requires a non-empty TYPE.'
    FILE_EXISTS: str = 'The file "{0}" already exists.'
    GED_INVALID: str = 'The GEDCOM invalidation failed.'
    IDNO_REQUIRES_TYPE: str = 'The IDNO tag requires a non-empty TYPE.'
    INVALID_VALUES: str = '"{0}" is not in the valid values of "{1}".'
    LOADED: str = 'The "{0}" genealogy has been loaded from the "{1}" file.'
    LOAD_FAILED: str = 'The file "{0}" failed to load.'
    MISSING: str = 'These xref values {0} are missing record definitions.'
    NEGATIVE_ERROR: str = 'The value "{0}" is less than zero.'
    NEG_YEAR: str = 'Negative year but a negative label "{0}".'
    NEITHER_TAG_NOR_EXTTAG: str = (
        'The item "{0}" is neither a Tag nor an ExtTag.'
    )
    NO_LIST: str = (
        'Only single values, not lists are permitted for this structure type.'
    )
    NO_NONE: str = 'The value is required to be other than "None".'
    NO_EMPTY_LIST: str = 'The list is required to be not empty.'
    NO_EMPTY_POINTER: str = (
        'The cross reference identifier must be other than VOID'
    )
    NO_EMPTY_STRING: str = (
        'The value is required to be other than the empty string.'
    )
    NO_EMPTY_TAG: str = 'The tag is required to be not the empty tag.'
    NOT_DEFAULT: str = (
        'GEDCOM requires a specific value different from the default "{0}".'
    )
    NOT_DEFINED_FOR_STRUCTURE: str = (
        'The extension "{0}" is not defined for the current structure.'
    )
    NOT_FLOAT: str = 'The {1} value "{0}" is not a float.'
    NOT_RECORD: str = 'The value "{0}" is not an appropriate xref value.'
    NOT_UNICODE: str = 'The file "{0}" is not unicode encoded.'
    NOT_VALID_ENUM: str = 'The tag "{0}" is not an enumerated value.'

    ONLY_ONCE: str = 'The substructure "{0}" can appear only once under "{1}".'
    PAGE_NOT_FOUND: str = 'The page at "{0}" was not found.'
    PAYLOAD_IS_Y: str = 'The payload is "Y" or the default empty string.'
    PHONE_COUNTRY_CODE: str = 'The phone country code "{0}" is not greater than {1} and less than {2}.'
    PHONE_AREA_CODE: str = (
        'The phone area code "{0}" is not greater than {1} and less than {2}.'
    )
    PHONE_PREFIX_CODE: str = (
        'The phone prefix code "{0}" is not greater than {1} and less than {2}.'
    )
    PHONE_LINE_CODE: str = (
        'The phone line code "{0}" is not greater than {1} and less than {2}.'
    )
    PIECES_EMPTY: str = (
        'All personal name pieces are the empty string or the empty list.'
    )
    RANGE: str = 'The value "{0}" is not greater than or equal to "{1}" but strictly less than "{2}".'
    RANGE_ERROR: str = '"{0}" must be greater than or equal to "{1}" and less than or equal to "{2}".'
    SAME_INDIVIDUAL: str = (
        'The individual "{0}" is the same individual aliased to it.'
    )
    SAVED: str = 'The file "{0}" has been saved.'
    SAVE_FIRST: str = 'First stave the genealogy to a file.'
    SCHEMA_NAME: str = 'The tag "{0}" contain the character "{1}" that is not a digit, an upper case character or the underscore.'
    SCHEMA_NEEDS_URL: str = (
        'The schema tag "{0}" needs a non-empty url as its definition.'
    )
    SLGC_REQUIRES_FAM: str = (
        'The Tag.SLGC requires a valid family cross reference identifier.'
    )
    STARTED: str = 'The "{0}" genealogy has been started.'
    STAT_REQUIRES_DATE: str = 'The STAT tag requires a non-empty DATE.'
    TAG_PAYLOAD: str = (
        'The tag {0} cannot have a payload different from "Y" or "".'
    )
    TAG_REQUIRED: str = 'The substructure "{0}" is required by "{0}".'
    UNDOCUMENTED: str = 'Tags without adequate documentation are not supported.'
    UNKNOWN_TAG: str = (
        'The structure at "{0}" does not have a name for its tag.'
    )
    UNRECOGNIZED: str = 'The filename "{0}" is not recognized.'
    WRONG_TYPE: str = '"{0}" has type {1} but should have type {2}.'
    XREF_EXISTS: str = 'The identifier "{0}" built from "{1}" already exists.'
    YAML_NOT_YAML_FILE: str = (
        'The file "{0}" does not contain the YAML directive "{1}".'
    )
    YAML_MISSING_REQUIRED_LANG: str = (
        'The yaml file "{0}" did not have the required `lang` specification.'
    )
    YAML_MISSING_REQUIRED_TYPE: str = (
        'The yaml file "{0}" did not have the required `type` specification.'
    )
    YAML_MISSING_REQUIRED_URI: str = (
        'The yaml file "{0}" did not have the required `uri` specification.'
    )
    YAML_NO_CALENDAR: str = 'Months or epochs are defined but without a calendar type.'
    YAML_NO_TAG_NAME: str = 'Neither standard nor extension tags were defined.'
    YAML_STRUCTURE_MISSING_VALUES: str = 'The structure type has no superstructures nor substructures.'
    YAML_UNRECOGNIZED_TYPE: str = ('The type "{0}" is not a valid type')
    ZERO_YEAR: str = 'The calendar has no zero year.'
