# Licensed under a 3-clause BSD style license - see LICENSE.md
"""This module provides a namespace for constants."""

from typing import Dict, Iterable, List, Tuple

class String:
    
    LEFT_BRACE = '{'
    NEGATIVE = '-'
    NEWLINE = '\n'
    RIGHT_BRACE = '}'
    SPACE = ' '

class Number:
    DATETIME_EPOCH = 1970

class Msg:
    BAD_DATE = 'The value "{0}" for a date is not properly formatted in the {1} calendar.'
    BAD_LABEL = 'The date "{0}" contains an inappropriate label "{1}" rather than either "{2}" or "{3}" for the {4} calendar.'
    BOTH_NAME_FILE = 'Both a chronology name "{0}" and a filename "{1}" have been specified, but only one can be used.'
    CALENDARS_DONT_MATCH = 'The calendars "{0}" and "{1}" do not match.'
    CHANGED = 'The chronology has been changed to the "{0}" calendar.'
    COUNT_RESERVED = '{0} reserved keys were used.'
    HAS_CALENDAR = 'The chronology already has the "{0}" calendar.'
    KEY_REMOVED = 'The name "{0}" has been removed from the "{0}" dictionary.'
    MISSING_NAME = 'The chronology has neither a name nor a file to load.'
    NO_COMMENTS = 'There are no comments for the {0} chronology.'
    NO_DICT_NAME = 'The chronology "{0}" has no {1}.'
    NOT_IN_DICT = 'The name "{0}" is not in the chronology dictionary "{1}".'
    NOT_REMOVABLE = 'The name "{0}" is a reserved key and cannot be removed.'
    ONE = 'One reserved key were used.'
    OUT_OF_RANGE = 'There are only {0} comments in the list. The index starts at 0.'
    RENAME = 'The chronology has been renamed "{0}".'
    RESERVED = 'The key "{0}" is a reserved key.'

class Datetime:
    unit = {
        'ATTOSECOND' : 'as',
        'DAY' : 'D',
        'FEMTOSECOND' : 'fs',
        'HOUR' : 'h',
        'MICROSECOND' : 'us',
        'MILLISECOND' : 'ms',
        'MINUTE' : 'm',
        'MONTH' : 'M',
        'NANOSECOND' : 'ns',
        'PICOSECOND' : 'ps',
        'SECOND' : 's',
        'WEEK' : 'W',
        'YEAR' : 'Y',
    }

class Key:
    value = {
        'ACTORS' : 'ACTORS',
        'BEFOREPRESENT' : 'Before Present',
        'BEGIN' : 'BEGIN',
        'BIRTH' : 'BIRTH',
        'CALENDAR' : 'CALENDAR',
        'CHALLENGES' : 'CHALLENGES',
        'DATE' : 'DATE',
        'DEATH' : 'DEATH',
        'DESCRIPTION' : 'DESCRIPTION',
        'END' : 'END',
        'EVENTS' : 'EVENTS',
        'EXPERIMENT' : 'Experiment',
        'FATHER' : 'FATHER',
        'FEMALE' : 'FEMALE',
        'FILE' : 'FILENAME',
        'GREGORIAN' : 'Gregorian',
        'LABELS' : 'LABELS',
        'MALE' : 'MALE',
        'MARKERS' : 'MARKERS',
        'MOTHER' : 'MOTHER',
        'NAME' : 'NAME',
        'NEGLABEL' : 'NEG LABEL',
        'OVERVIEW' : 'OVERVIEW',
        'PERIODS' : 'PERIODS',
        'POSLABEL' : 'POS LABEL',
        'SECULAR' : 'Secular',
        'TEXTS' : 'TEXTS',
        'USEZERO' : 'USE ZERO',
        'ZEROYEAR' : 'ZERO YEAR',
    }

class Calendar:
    system = {
        Key.value['BEFOREPRESENT'] : {
            Key.value['NAME'] : 'Before Present',
            Key.value['POSLABEL'] : '',
            Key.value['NEGLABEL'] : ' BP',
            Key.value['ZEROYEAR'] : -Number.DATETIME_EPOCH,
            Key.value['USEZERO'] : False,
        },
        Key.value['EXPERIMENT'] : {
            Key.value['NAME'] : 'Experiment',
            Key.value['POSLABEL'] : '',
            Key.value['NEGLABEL'] : '',
            Key.value['ZEROYEAR'] : -Number.DATETIME_EPOCH,
            Key.value['USEZERO'] : False,
        },
        Key.value['GREGORIAN'] : {
            Key.value['NAME'] : 'Gregorian',
            Key.value['POSLABEL'] : ' AD',
            Key.value['NEGLABEL'] : ' BC',
            Key.value['ZEROYEAR'] : -Number.DATETIME_EPOCH,
            Key.value['USEZERO'] : False,
        },
        Key.value['SECULAR'] : {
            Key.value['NAME'] : 'Secular',
            Key.value['POSLABEL'] : ' CE',
            Key.value['NEGLABEL'] : ' BCE',
            Key.value['ZEROYEAR'] : -Number.DATETIME_EPOCH,
            Key.value['USEZERO'] : False,
        },
    }

