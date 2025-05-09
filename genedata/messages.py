# Licensed under a 3-clause BSD style license - see LICENSE.md
"""Strings to send messages to the user from all modules which may benefit
from internationalization.
"""

from dataclasses import dataclass


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
    CANNOT_READ_YAML_FILE: str = 'Cannot read yaml file "{0}" for tag "{1}". The tag will be effectively undocumented.'
    CANNOT_SHOW: str = 'Cannot show item "{0}".'
    CIRCULAR: str = '"{0}" and "{1}" reference each other. The https://gedcom.io/terms/v7/record-SNOTE prohibits this between shared notes and source records.'
    DEPRECATION_WARNING: str = 'The structure "{0}" has been deprecated and should not be used going forward.'
    DIRECTORY_NOT_FOUND: str = 'The directory "{0}" could not be found.'
    DOES_NOT_EQUAL: str = ' * DOES NOT EQUAL * '
    DUPLICATE_RECORD: str = (
        'The cross-reference identifier {0} has already been used.'
    )
    # EMPTY_EVENT_TYPE: str = 'The event type for tag {0} must have some value.'
    EVEN_REQUIRES_TYPE: str = 'The EVEN tag requires a non-empty TYPE.'
    EXID_TYPE: str = 'The EXID identifier requires a type description of it.'
    EXTENSION_DUPLICATES_TAG: str = (
        'The extension tag "{0}" duplicates the standard tag "{1}".'
    )
    EXTENSION_ENUM_TAG: str = (
        'The tag "{0}" is not a value of the enumeration "{1}".'
    )
    # EXTENSION_EXISTS: str = 'The extension key "{0}" based on the uri already exists in the "{1}" dictionary.'
    FACT_REQUIRES_TYPE: str = 'The FACT tag requires a non-empty TYPE.'
    FILE_EXISTS: str = 'The file "{0}" already exists.'
    FILE_NOT_FOUND: str = 'The file "{0}" could not be found.'
    GED_FILE_ALREADY_LOADED: str = 'A ged file has already been loaded.'
    GED_FILE_EMPTY: str = 'The file "{0}" is empty.'
    GED_NO_HEADER: str = 'The file "{0}" does not have the ged header: "{1}".'
    GED_NO_TRAILER: str = 'The file "{0}" does not have the ged trailer: "{1}".'
    GED_INVALID: str = 'The GEDCOM invalidation failed.'
    GED_VERSION_NOT_RECOGNIZED: str = (
        'The file "{0}" has an unrecognized version "{1}".'
    )
    IDNO_REQUIRES_TYPE: str = 'The IDNO tag requires a non-empty TYPE.'
    INVALID_VALUES: str = '"{0}" is not in the valid values of "{1}".'
    KEY_NOT_FOUND: str = (
        'A Structure key could not be derived from the name "{0}".'
    )
    LATI_NORTH_SOUTH: str = (
        'The character "{0}" of the latitude "{1}" is not "N" or "S".'
    )
    LATI_RANGE: str = (
        'The value "{0}" is not between {1} and {2} in structure "{3}".'
    )
    LATI_RANGE_METHOD: str = (
        'The value "{0}" is not between {1} and {2} in method Input.lati.'
    )
    LOADED: str = 'The "{0}" genealogy has been loaded from the "{1}" file.'
    LOAD_FAILED: str = 'The file "{0}" failed to load.'
    LOG_READ_FAILED: str = (
        'Could not read {0} with Util.read. Trying Util.read_binary.'
    )
    LOG_READ_BINARY_FAILED: str = 'Could not read {0} with Util.read_binary.'
    LONG_EAST_WEST: str = 'The character "{0}" of the longitude "{1}" is not "{2}" or "{3}" in structure "{4}".'
    LONG_RANGE: str = (
        'The value "{0}" is not between {1} and {2} in structure "{3}".'
    )
    LONG_RANGE_METHOD: str = (
        'The value "{0}" is not between {1} and {2} in method Input.long.'
    )
    LONGER_FIRST: str = 'The first string is longer than the second.  Here are the remaining lines:'
    LONGER_SECOND: str = 'The second string is longer than the first.  Here are the remaining lines:'
    MISSING: str = 'These xref values {0} are missing record definitions.'
    MISSING_HEADER: str = 'The header record has not been added to the genealogy by the `add_header` method.'
    MISSING_REQUIRED: str = 'One of the substructures in "{0}" are missing from the "{1}" structure.'
    MISSING_URL_AND_DICTIONARIES: str = (
        'Missing both a url and specification dictionaries.'
    )
    NEGATIVE_ERROR: str = (
        'The value "{0}" is less than zero in structure "{1}".'
    )
    NEG_YEAR: str = 'Negative year but a negative label "{0}".'
    NEITHER_TAG_NOR_EXTTAG: str = (
        'The item "{0}" is neither a Tag nor an ExtTag.'
    )
    NO_LIST: str = (
        'Only single values, not lists are permitted for this structure type.'
    )
    NO_NONE: str = 'The value is required to be other than "None".'
    NO_SUBS: str = 'No substructures are permitted for the "{0}" structure.'
    NO_EMPTY_LIST: str = 'The list is required to be not empty.'
    NO_EMPTY_POINTER: str = (
        'The cross reference identifier must be other than VOID'
    )
    NO_EMPTY_STRING: str = (
        'The value is required to be other than the empty string.'
    )
    NO_EMPTY_TAG: str = 'The tag is required to be not the empty tag.'
    NO_SLASH: str = 'The value "{0}" is not a media type for structure "{1}" because it does not have a slash in the value.'
    NO_TRAILER: str = 'The file does not have a ged trailer: {0}'
    NO_HEADER: str = 'The file does not have a ged header: {0}'
    NOT_AGE: str = 'The value "{0}" is not an age for structure "{1}".'
    NOT_DATE: str = 'The value "{0}" is not a date for structure "{1}".'
    NOT_DATE_CALENDAR: str = 'The value "{0}" is not a date for structure "{1}" because the calendar "{2}" is not in the list {3} of available calendars.'
    NOT_DATE_EPOCH: str = (
        'The value "{0}" is not a date period for structure "{1}" since the epoch is not in the list of epochs {2}.'
    )
    NOT_DATE_EXACT: str = (
        'The value "{0}" is not an exact date for structure "{1}".'
    )
    NOT_DATE_EXACT_SPACES: str = (
        'The value "{0}" is not an exact date for structure "{1}" since it has {2} spaces but it should have exactly {3} spaces.'
    )
    NOT_DATE_EXACT_MONTH: str = (
        'The value "{0}" is not an exact date for structure "{1}" since the month value "{2}" is not recognized as a Gregorian month.'
    )
    NOT_DATE_EXACT_DAY: str = (
        'The value "{0}" is not an exact date for structure "{1}" since the day value "{2}" is not greater than 0 but less than or equal to {3}.'
    )
    # NOT_DATE_EXACT_TOO_LARGE: str = (
    #     'The value "{0}" is not an exact date for structure "{1}" since it has {2} character but it should have no more than {3}.'
    # )
    NOT_DATE_EXACT_YEAR: str = (
        'The value "{0}" is not an exact date for structure "{1}" since the year value "{2}" is not an integer different from 0.'
    )
    NOT_DATE_EXACT_YEAR_NOT_INTEGER: str = "invalid literal for int() with base 10: '{0}'"
    NOT_DATE_MONTH: str = (
        'The value "{0}" is not a date period for structure "{1}" since the month is not in the list of months {2}.'
    )
    NOT_DATE_PERIOD: str = (
        'The value "{0}" is not a date period for structure "{1}".'
    )
    NOT_DATE_PREFACE: str = (
        'The value "{0}" is not a date period for structure "{1}" since "{2}" is not recognized.'
    )
    NOT_DATE_SPACES: str = (
        'The value "{0}" is not a date period for structure "{1}" because there are {1} spaces in the string, more than expected.'
    )
    NOT_DATE_ZERO_YEAR: str = (
        'The value "{0}" is not a date period for structure "{1}" since there in no zero year in the calendar.'
    )
    NOT_DEFAULT: str = (
        'GEDCOM requires a specific value different from the default "{0}".'
    )
    NOT_DEFINED_FOR_STRUCTURE: str = (
        'The extension "{0}" is not defined for the current structure.'
    )
    NOT_DOCUMENTED_TAG: str = 'The tag "{0}" is not documented either as a standard tag or as an extension tag.  Provide a yaml file for the tag in the header record.'
    NOT_FAMILY_XREF: str = (
        'The value "{0}" is not a family cross reference for structure "{1}".'
    )
    NOT_FILE_PATH: str = (
        'The value "{0}" is not a file path for structure "{1}".'
    )
    NOT_FLOAT: str = 'The {1} value "{0}" is not a float.'
    NOT_GED_STRINGS: str = 'The string contains end of lines followed by alpha characters rather than numerics.'
    NOT_INDIVIDUAL_XREF: str = 'The value "{0}" is not an individual cross reference for structure "{1}".'
    NOT_INTEGER: str = 'The value "{0}" is not an integer for structure "{1}".'
    NOT_LANGUAGE: str = (
        'The value "{0}" is not a language code for structure "{1}".'
    )
    NOT_LIST: str = 'The value "{0}" is not a list for structure "{1}".'
    NOT_MEDIA_TYPE: str = (
        'The value "{0}" is not a media type for structure "{1}".'
    )
    NOT_MULTIMEDIA_XREF: str = 'The value "{0}" is not a multimedia cross reference for structure "{1}".'
    NOT_NAME: str = 'The value "{0}" is not a name for structure "{1}".'
    NOT_NAME_SLASH: str = 'The value "{0}" is not a name for structure "{1}" since it contains {2} slash marks when it can have either 0 or 2 of them.'
    NOT_PERMITTED: str = 'The substructure "{0}" is not in the permitted list {1} for structure "{2}".'
    NOT_RECORD: str = (
        'The value "{0}" is not an appropriate xref value for structure "{1}".'
    )
    NOT_REPOSITORY_XREF: str = 'The value "{0}" is not a repository cross reference for structure "{1}".'
    NOT_SHARED_NOTE_XREF: str = 'The value "{0}" is not a shared note cross reference for structure "{1}".'
    NOT_SOURCE_XREF: str = (
        'The value "{0}" is not a source cross reference for structure "{1}".'
    )
    NOT_STRING: str = 'The value "{0}" is not a string for structure "{1}".'
    NOT_SUBMITTER_XREF: str = 'The value "{0}" is not a submitter cross reference for structure "{1}".'
    NOT_SUPERSTRUCTURE: str = 'The structure "{0}" contains an extension substructure with tag "{1}" that does not recognize it as a superstructure.'
    NOT_TIME: str = 'The value "{0}" is not a time for structure "{1}".'
    NOT_TIME_COLON_COUNT: str = 'The value "{0}" is not a time for structure "{1}" since it has {2} colons. Only one or two are permitted.'
    NOT_TIME_HOURS: str = 'The value "{0}" is not a time for structure "{1}" since it has hours "{2}" which is not between {3} and {4} for a 24-hour time.'
    NOT_TIME_MINUTES: str = 'The value "{0}" is not a time for structure "{1}" since it has minutes "{2}" which is not between {3} and {4} for a 24-hour time.'
    NOT_TIME_SECONDS: str = 'The value "{0}" is not a time for structure "{1}" since it has seconds "{2}" which is not greater than or equal to {3} and strictly less than {4} for a 24-hour time.'
    NOT_UNICODE: str = 'The file "{0}" is not unicode encoded.'
    NOT_VALID_ENUM: str = 'The value "{0}" is not in the enumeration list {1} for structure "{2}".'

    ONLY_ONCE: str = (
        'The substructure "{0}" can appear only once in structure "{1}".'
    )
    ONLY_ONE_PERMITTED: str = (
        'The substructure "{0}" can appear only once in structure "{1}".'
    )
    ONLY_RECORDS: str = 'The object "{0}" is not a record structure such as RecordExt, RecordFam, RecordIndi, RecordObje, RecordRepo, RecordSnote, RecordSour or RecordSubm.'
    ONLY_HEADER: str = 'The object "{0}" is not a Head record structure.'
    PAGE_NOT_FOUND: str = 'urllib.error.HTTPError: HTTP Error 404: Not Found'
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
    TAG_SPACES: str = 'The TAG value "{0}" must contain one and only one space.'
    UNDOCUMENTED: str = 'Tags without adequate documentation are not supported.'
    UNKNOWN_TAG: str = (
        'The structure at "{0}" does not have a name for its tag.'
    )
    UNRECOGNIZED: str = 'The filename "{0}" is not recognized.'
    UNRECOGNIZED_XREF: str = (
        'The cross reference identifier "{0}" is not recognized.'
    )
    WRONG_TYPE: str = '"{0}" has type {1} but should have type {2}.'
    WWW_RESPONSE: str = (
        'The site "{0}" returned "{1}". The value 200 was expected.'
    )
    VALUE_NOT_Y_OR_NULL: str = 'The value "{0}" is neither "Y" nor the empty string for structure "{1}".'
    XREF_EXISTS: str = 'The identifier "{0}" built from "{1}" already exists.'
    YAML_FILE_HAS_BEEN_USED: str = 'The yaml file "{0}" has already been used for another extension.'
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
    YAML_NO_CALENDAR: str = (
        'Months or epochs are defined but without a calendar type.'
    )
    YAML_NO_TAG_NAME: str = 'Although the type is one of calendar, enumeration, month or structure neither a standard tag nor extension tags were defined.'
    YAML_STRUCTURE_MISSING_VALUES: str = (
        'The structure type has no superstructures nor substructures.'
    )
    YAML_UNRECOGNIZED_TYPE: str = (
        'The type "{0}" is not in the set of valid types "{1}".'
    )
    ZERO_YEAR: str = 'The "{0}" calendar has no zero year.'
