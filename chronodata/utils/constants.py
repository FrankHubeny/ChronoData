# Licensed under a 3-clause BSD style license - see LICENSE.md
"""This module provides a namespace for typed constants."""

from typing import Literal


class Msg:
    ADDED: str = 'The {0} "{1}" has been added to the chronology.'
    ADDED_COMMENT: str = 'The comment "{0}" has been added.'
    ALL_COMMENTS_REMOVED: str = 'All comments have been removed from the "{0}" chronology.'
    BAD_DATE: str = 'The value "{0}" for a date is not properly formatted in the {1} calendar.'
    BAD_LABEL: str = 'The date "{0}" contains an inappropriate label "{1}" rather than either "{2}" or "{3}" for the {4} calendar.'
    BOTH_NAME_FILE: str = 'Both a chronology name "{0}" and a filename "{1}" have been specified, but only one can be used.'
    CALENDARS_DONT_MATCH: str = 'The calendars "{0}" and "{1}" do not match.'
    CHANGED: str = 'The chronology has been changed to the "{0}" calendar.'
    CHRONOLOGY_LOADED: str = 'The "{0}" chronology has been loaded from the "{1}" file by "{2}".'
    CHRONOLOGY_STARTED: str = 'The "{0}" chronology has been started by "{1}".'
    COMMENT_REMOVED: str = 'Comment {0} "{1}" has been removed from the chronology.'
    COUNT_RESERVED: str = '{0} reserved keys were used.'
    HAS_CALENDAR: str = 'The chronology already has the "{0}" calendar.'
    KEY_REMOVED: str = 'The name "{0}" has been removed from "{1}".'
    MISSING_NAME: str = 'The chronology has neither a name nor a file to load.'
    NO_COMMENTS: str = 'There are no comments for the {0} chronology.'
    NO_DICT_NAME: str = 'The chronology "{0}" has no {1}.'
    NOT_IN_DICT: str = 'The name "{0}" is not in the "{1}".'
    NOT_REMOVABLE: str = 'The name "{0}" is a reserved key and cannot be removed.'
    ONE: str = 'One reserved key were used.'
    OUT_OF_RANGE: str = 'There is no comment at index {0}.'
    RENAME: str = 'The chronology has been renamed "{0}".'
    RESERVED: str = 'The key "{0}" is a reserved key.'
    USER_REQUIRED: str = 'A named user is required to log comments, challenges and responses for the "{0}" chronology or to load the "{1}" file.'


class Number:
    DATETIME_EPOCH: int = 1970


class String:
    
    ACTOR: Literal['actor'] = 'actor'
    CHALLENGE: Literal['challenge'] = 'challenge'
    EVENT: Literal['event'] = 'event'
    LEFT_BRACE: Literal['{'] = '{'
    LEFT_BRACKET: Literal['['] = '['
    MARKER: Literal['marker'] = 'marker'
    NEGATIVE: Literal['-'] = '-'
    NEWLINE: Literal['\n'] = '\n'
    PERIOD: Literal['period'] = 'period'
    RIGHT_BRACE: Literal['}'] = '}'
    RIGHT_BRACKET: Literal[']'] = ']'
    SPACE: Literal[' '] = ' '
    TEXT: Literal['text'] = 'text'


class Datetime:
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
            'attosecond' : ATTOSECOND,
            'day' :DAY,
            'femtosecond' : FEMTOSECOND,
            'hour' : HOUR,
            'microsecond' : MICROSECOND,
            'millisecond' : MILLISECOND,
            'minute' : MINUTE,
            'month' : MONTH,
            'nanosecond' : NANOSECOND,
            'picosecond' : PICOSECOND,
            'second' : SECOND,
            'week' : WEEK,
            'year' : YEAR,
        }


class Key:
    ACTORS: str = 'ACTORS'
    BEFOREPRESENT: str = 'Before Present'
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
    EXPERIMENT: str = 'Experiment'
    FATHER: str = 'FATHER'
    FEMALE: str = 'FEMALE'
    FILE: str = 'FILENAME'
    GREGORIAN: str = 'Gregorian'
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
    SECULAR: str = 'Secular'
    TEXTS: str = 'TEXTS'
    TIMESTAMP: str = 'TIMESTAMP'
    USER: str = 'USER'
    USEZERO: str = 'USE ZERO'
    ZEROYEAR: str = 'ZERO YEAR'
    keylist: list[str] = [
        ACTORS,
        BEFOREPRESENT,
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
        EXPERIMENT,
        FATHER,
        FEMALE,
        FILE,
        GREGORIAN,
        LABELS,
        MALE,
        MARKERS,
        MOTHER,
        NAME,
        NEGLABEL,
        OVERVIEW,
        PERIODS,
        POSLABEL,
        SECULAR,
        TEXTS,
        USEZERO,
        ZEROYEAR,
    ]

class Calendar:
    BEFORE_PRESENT: dict[str, str | int | bool] = {
        Key.NAME : 'Before Present',
        Key.POSLABEL : '',
        Key.NEGLABEL : ' BP',
        Key.ZEROYEAR : -Number.DATETIME_EPOCH,
        Key.USEZERO : False,
    }
    EXPERIMENT: dict[str, str | int | bool] = {
        Key.NAME : 'Experiment',
        Key.POSLABEL : '',
        Key.NEGLABEL : '',
        Key.ZEROYEAR : -Number.DATETIME_EPOCH,
        Key.USEZERO : False,
    }
    GREGORIAN: dict[str, str | int | bool] = {
        Key.NAME : 'Gregorian',
        Key.POSLABEL : ' AD',
        Key.NEGLABEL : ' BC',
        Key.ZEROYEAR : -Number.DATETIME_EPOCH,
        Key.USEZERO : False,
    }
    SECULAR: dict[str, str | int | bool] = {
        Key.NAME : 'Secular',
        Key.POSLABEL : ' CE',
        Key.NEGLABEL : ' BCE',
        Key.ZEROYEAR : -Number.DATETIME_EPOCH,
        Key.USEZERO : False,
    }

