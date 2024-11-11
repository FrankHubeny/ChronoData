# Licensed under a 3-clause BSD style license - see LICENSE.md
"""This module provides a namespace for typed constants."""

from typing import Literal


class Msg:
    """The following constants define messages that are returned acknowledging
    events that happened.
    """

    ADDED: str = 'The {0} "{1}" has been added to the chronology.'
    ADDED_COMMENT: str = 'The comment "{0}" has been added.'
    ALL_COMMENTS_REMOVED: str = 'All comments have been removed.'
    BAD_DATE: str = 'The date value "{0}" does not fit a {1} calendar.'
    BAD_LABEL: str = (
        'The date "{0}" contains an inappropriate label "{1}" rather than \
either "{2}" or "{3}" for the {4} cSalendar.'
    )
    CALENDARS_DONT_MATCH: str = 'The calendars "{0}" and "{1}" do not match.'
    CHANGED: str = 'The chronology has been changed to the "{0}" calendar.'
    CHRONOLOGY_LOADED: str = (
        'The "{0}" chronology has been loaded from the "{1}" file.'
    )
    CHRONOLOGY_STARTED: str = 'The "{0}" chronology has been started.'
    COMMENT_REMOVED: str = (
        'Comment {0} "{1}" has been removed from the chronology.'
    )
    COUNT_RESERVED: str = '{0} reserved keys were used.'
    FILE_SAVED: str = 'The file "{0}" has been saved.'
    HAS_CALENDAR: str = 'The chronology already has the "{0}" calendar.'
    KEY_REMOVED: str = 'The name "{0}" has been removed from "{1}".'
    NO_COMMENTS: str = 'There are no comments for the {0} chronology.'
    NO_DICT_NAME: str = 'The chronology "{0}" has no {1}.'
    NOT_IN_DICT: str = 'The name "{0}" is not in the "{1}".'
    NOT_REMOVABLE: str = (
        'The name "{0}" is a reserved key and cannot be removed.'
    )
    ONE: str = 'One reserved key was used.'
    OUT_OF_RANGE: str = 'There is no comment at index {0}.'
    RENAME: str = 'The chronology has been renamed "{0}".'
    RESERVED: str = 'The key "{0}" is a reserved key.'
    USER_REQUIRED: str = (
        'A named user is required to log comments, challenges and responses \
for the "{0}" chronology or to load the "{1}" file.'
    )


class Number:
    """The following constants numeric datatypes."""

    DATETIME_EPOCH: int = 1970


class String:
    """The following constants define literal strings that could be used
    as values of keys in a dictionary or for control or reporting functions
    in the programming."""

    ACTOR: Literal['actor'] = 'actor'
    AD: Literal[' AD'] = ' AD'
    BC: Literal[' BC'] = ' BC'
    BCE: Literal[' BCE'] = ' BCE'
    BP: Literal[' BP'] = ' BP'
    BEFORE_PRESENT: Literal['BEFORE PRESENT'] = 'BEFORE PRESENT'
    CE: Literal[' CE'] = ' CE'
    CHALLENGE: Literal['challenge'] = 'challenge'
    GREGORIAN: Literal['GREGORIAN'] = 'GREGORIAN'
    EMPTY: Literal[''] = ''
    EVENT: Literal['event'] = 'event'
    EXPERIMENT: Literal['EXPERIMENT'] = 'EXPERIMENT'
    LEFT_BRACE: Literal['{'] = '{'
    LEFT_BRACKET: Literal['['] = '['
    MARKER: Literal['marker'] = 'marker'
    NEGATIVE: Literal['-'] = '-'
    NEWLINE: Literal['\n'] = '\n'
    PERIOD: Literal['period'] = 'period'
    RIGHT_BRACE: Literal['}'] = '}'
    RIGHT_BRACKET: Literal[']'] = ']'
    SECULAR: Literal['SECULAR'] = 'SECULAR'
    SPACE: Literal[' '] = ' '
    TEXT: Literal['text'] = 'text'


class Datetime:
    """The following constants define NumPy units used in datetime64 object."""

    ATTOSECOND: Literal['as'] = 'as'
    DAY: Literal['D'] = 'D'
    FEMTOSECOND: Literal['fs'] = 'fs'
    HOUR: Literal['h'] = 'h'
    MICROSECOND: Literal['us'] = 'us'
    MILLISECOND: Literal['ms'] = 'ms'
    MINUTE: Literal['m'] = 'm'
    MONTH: Literal['M'] = 'M'
    NANOSECOND: Literal['ns'] = 'ns'
    PICOSECOND: Literal['ps'] = 'ps'
    SECOND: Literal['s'] = 's'
    WEEK: Literal['W'] = 'W'
    YEAR: Literal['Y'] = 'Y'
    units: dict[str, str] = {
        'attosecond': ATTOSECOND,
        'day': DAY,
        'femtosecond': FEMTOSECOND,
        'hour': HOUR,
        'microsecond': MICROSECOND,
        'millisecond': MILLISECOND,
        'minute': MINUTE,
        'month': MONTH,
        'nanosecond': NANOSECOND,
        'picosecond': PICOSECOND,
        'second': SECOND,
        'week': WEEK,
        'year': YEAR,
    }


class Key:
    """The following constants define the keys that are used
    for dictionaries."""

    ACTORS: str = 'ACTORS'
    BEGIN: str = 'BEGIN'
    BIRTH: str = 'BIRTH'
    CALENDAR: str = 'CALENDAR'
    CHALLENGES: str = 'CHALLENGES'
    COMMENTS: str = 'COMMENTS'
    DATE: str = 'DATE'
    DEATH: str = 'DEATH'
    DESCRIPTION: str = 'DESCRIPTION'
    END: str = 'END'
    EVENTS: str = 'EVENTS'
    FATHER: str = 'FATHER'
    FEMALE: str = 'FEMALE'
    FILE: str = 'FILENAME'
    LABELS: str = 'LABELS'
    MALE: str = 'MALE'
    MARKERS: str = 'MARKERS'
    MESSAGE: str = 'MSG'
    MOTHER: str = 'MOTHER'
    NAME: str = 'NAME'
    NEGLABEL: str = 'NEG LABEL'
    OVERVIEW: str = 'OVERVIEW'
    PERIODS: str = 'PERIODS'
    POSLABEL: str = 'POS LABEL'
    SOURCES: str = 'SOURCES'
    TEXTS: str = 'TEXTS'
    TIMESTAMP: str = 'TIMESTAMP'
    USER: str = 'USER'
    USEZERO: str = 'USE ZERO'
    ZEROYEAR: str = 'ZERO YEAR'
    keylist: list[str] = [
        ACTORS,
        BEGIN,
        BIRTH,
        CALENDAR,
        CHALLENGES,
        COMMENTS,
        DATE,
        DEATH,
        DESCRIPTION,
        END,
        EVENTS,
        FATHER,
        FEMALE,
        FILE,
        LABELS,
        MALE,
        MARKERS,
        MOTHER,
        NAME,
        NEGLABEL,
        OVERVIEW,
        PERIODS,
        POSLABEL,
        SOURCES,
        TEXTS,
        USEZERO,
        ZEROYEAR,
    ]


class Calendar:
    """The following dictionaries define the constants for
    particular calendars using previously defined constants.
    """

    BEFORE_PRESENT: dict[str, dict[str, str]] = {Key.CALENDAR: {
        Key.NAME: String.BEFORE_PRESENT,
        Key.POSLABEL: String.EMPTY,
        Key.NEGLABEL: String.BP,
        #Key.ZEROYEAR: -Number.DATETIME_EPOCH,
        #Key.USEZERO: False,
    }}
    EXPERIMENT: dict[str, dict[str, str]] = {Key.CALENDAR: {
        Key.NAME: String.EXPERIMENT,
        Key.POSLABEL: String.EMPTY,
        Key.NEGLABEL: String.EMPTY,
        #Key.ZEROYEAR: -Number.DATETIME_EPOCH,
        #Key.USEZERO: False,
    }}
    GREGORIAN: dict[str, dict[str, str]] = {Key.CALENDAR: {
        Key.NAME: String.GREGORIAN,
        Key.POSLABEL: String.AD,
        Key.NEGLABEL: String.BC,
        #Key.ZEROYEAR: -Number.DATETIME_EPOCH,
        #Key.USEZERO: False,
    }}
    SECULAR: dict[str, dict[str, str]]  = {Key.CALENDAR: {
        Key.NAME: String.SECULAR,
        Key.POSLABEL: String.CE,
        Key.NEGLABEL: String.BCE,
        #Key.ZEROYEAR: -Number.DATETIME_EPOCH,
        #Key.USEZERO: False,
    }}
