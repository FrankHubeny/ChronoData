# Licensed under a 3-clause BSD style license - see LICENSE.md
"""This module provides a namespace for typed constants."""

from typing import ClassVar, Literal

# DT: type = Literal['Y','M','D','h','m','s','as','fs','us','ns','ps','W']


class Arg:
    """The following constants are used as arguments to procedure calls
    such as Pandas DataFrames or NumPy."""

    JSON: str = '.json'
    JSONLENGTH: int = len(JSON)
    INDEX: Literal['index'] = 'index'
    INT: str = 'int'
    WRITE: Literal['w'] = 'w'


class Msg:
    """The following constants define messages that are returned acknowledging
    events that happened.
    """

    ADDED: str = 'The {0} "{1}" has been added to the chronology.'
    ADD_ACTOR: str = 'The actor "{0}" has been added.'
    ADD_CHALLENGE: str = 'The challenge "{0}" has been added.'
    ADD_COMMENT: str = 'The comment "{0}" has been added.'
    ADD_EVENT: str = 'The event "{0}" has been added.'
    ADD_MARKER: str = 'The marker "{0}" has been added.'
    ADD_PERIOD: str = 'The period "{0}" has been added.'
    ADD_SOURCE: str = 'The source "{0}" has been added.'
    ADD_TEXT: str = 'The text "{0}" has been added.'
    BAD_DATE: str = 'The date value "{0}" does not fit a {1} calendar.'
    BAD_LABEL: str = 'The date "{0}" contains an inappropriate label "{1}".'
    CALENDARS_DONT_MATCH: str = 'The calendars "{0}" and "{1}" do not match.'
    CHANGED: str = 'The chronology has been changed to the "{0}" calendar.'
    COMMENT_REMOVED: str = 'Comment {0} "{1}" has been removed.'
    COUNT_RESERVED: str = '{0} reserved keys were used.'
    FILE_SAVED: str = 'The file "{0}" has been saved.'
    HAS_CALENDAR: str = 'The chronology already has the "{0}" calendar.'
    KEY_REMOVED: str = 'The name "{0}" has been removed from "{1}".'
    LOADED: str = 'The "{0}" chronology has been loaded from the "{1}" file.'
    NEG_YEAR: str = 'Negative year but a negative label "{0}".'
    NO_COMMENTS: str = 'There are no comments for the {0} chronology.'
    NO_DICT_NAME: str = 'The chronology "{0}" has no {1}.'
    NOT_IN_DICT: str = 'The name "{0}" is not in the "{1}".'
    NOT_REMOVABLE: str = 'The name "{0}" is a reserved key.'
    ONE: str = 'One reserved key was used.'
    OUT_OF_RANGE: str = 'There is no comment at index {0}.'
    POS_YEAR: str = 'Negative year but positive label "{0}".'
    REMOVE_ALL_COMMENTS: str = 'All comments have been removed.'
    RENAME: str = 'The chronology has been renamed "{0}".'
    RESERVED: str = 'The key "{0}" is a reserved key.'
    STARTED: str = 'The "{0}" chronology has been started.'
    STRICT: str = 'Strict formatting of dates has been set to "{0}".'


class Value:
    """The following constants are dictionary values."""

    AD: str = ' AD'
    BC: str = ' BC'
    BCE: str = ' BCE'
    BEFORE_PRESENT: str = 'BEFORE PRESENT'
    BP: str = ' BP'
    CE: str = ' CE'
    DATETIME_EPOCH: int = 1970
    EMPTY: str = ''
    EXPERIMENT: str = 'EXPERIMENT'
    GREGORIAN: str = 'GREGORIAN'
    SECULAR: str = 'SECULAR'


class Column:
    """The following constants are used for column headings."""

    RESERVED: str = 'Reserved Keys'


class String:
    """The following constants define strings that are neither keys
    nor values of a dictionary, but are used in displaying messages.
    """

    NEGATIVE: str = '-'
    NEWLINE: str = '\n'
    SPACE: str = ' '


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
    units: ClassVar = {
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
    CAL: str = 'CALENDAR'
    CHALLENGES: str = 'CHALLENGES'
    COMMENTS: str = 'COMMENTS'
    DATE: str = 'DATE'
    DEATH: str = 'DEATH'
    DESC: str = 'DESC'
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
    PRE: str = 'PRE'
    PERIODS: str = 'PERIODS'
    POST: str = 'POST'
    SOURCES: str = 'SOURCES'
    STRICT: str = 'STRICT'
    TEXTS: str = 'TEXTS'
    TIMESTAMP: str = 'TIMESTAMP'
    ZERO: str = 'ZERO'
    keylist: ClassVar = [
        ACTORS,
        BEGIN,
        BIRTH,
        CAL,
        CHALLENGES,
        COMMENTS,
        DATE,
        DEATH,
        DESC,
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
        PERIODS,
        POST,
        PRE,
        SOURCES,
        STRICT,
        TEXTS,
        ZERO,
    ]


class Calendar:
    """The following dictionaries define the constants for
    particular calendars using previously defined constants.
    """

    BEFORE_PRESENT: ClassVar = {
        Key.NAME: Value.BEFORE_PRESENT,
        Key.POST: Value.EMPTY,
        Key.PRE: Value.BP,
        Key.STRICT: True,
        Key.ZERO: False,
    }
    EXPERIMENT: ClassVar = {
        Key.NAME: Value.EXPERIMENT,
        Key.POST: Value.EMPTY,
        Key.PRE: Value.EMPTY,
        Key.STRICT: True,
        Key.ZERO: False,
    }
    GREGORIAN: ClassVar = {
        Key.NAME: Value.GREGORIAN,
        Key.POST: Value.AD,
        Key.PRE: Value.BC,
        Key.STRICT: True,
        Key.ZERO: False,
    }
    SECULAR: ClassVar = {
        Key.NAME: Value.SECULAR,
        Key.POST: Value.CE,
        Key.PRE: Value.BCE,
        Key.STRICT: True,
        Key.ZERO: False,
    }
