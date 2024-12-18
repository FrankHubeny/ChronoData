# Licensed under a 3-clause BSD style license - see LICENSE.md
"""This module provides a namespace for GEDCOM-related string.

References
---------
    [GEDCOM Specification](https://gedcom.io/specs/)
    [GEDCOM GitHub](https://github.com/familysearch/GEDCOM)
    [Apache License 2.0](https://github.com/FamilySearch/GEDCOM/blob/main/LICENSE)
"""

from dataclasses import dataclass
from typing import ClassVar


# @dataclass(frozen=True)
# class AgeConstants:
#     """Age enumerations for the Age NamedTuple."""

#     UNIT: ClassVar = {
#         'y': 'y',
#         'year': 'y',
#         'm': 'month',
#         'month': 'm',
#         'd': 'd',
#         'day': 'd',
#         'w': 'w',
#         'week': 'w',
#     }
#     BOUND: ClassVar = {'<', '>'}
#     NAME: ClassVar = {'U'}


# @dataclass(frozen=True)
# class GEDSpecial:
#     """Constant definitions for special GEDCOM string."""

#     ATSIGN: str = '@'
#     BC: str = 'BCE'
#     COLON: str = ':'
#     DAY: str = 'd'
#     FRENCH_R: str = 'FRENCH_R'
#     GREATER_THAN: str = '>'
#     GREGORIAN: str = 'GREGORIAN'
#     HEBREW: str = 'HEBREW'
#     HYPHEN: str = '-'
#     JULIAN: str = 'JULIAN'
#     LESS_THAN: str = '<'
#     MAX_MONTHS: str = 'Max Months'
#     MONTH: str = 'm'
#     MONTH_NAMES: str = 'Month Names'
#     MONTH_MAX_DAYS: str = 'Month Max Days'
#     NEWLINE: str = '\n'
#     NOW: str = 'now'
#     SPACE: str = ' '
#     T: str = 'T'
#     VERSION: str = '7.0'
#     VOID: str = '@VOID@'
#     WEEK: str = 'w'
#     YEAR: str = 'y'
#     Z: str = 'Z'


# @dataclass(frozen=True)
# class GEDDateTime:
#     """GEDCOM Month codes for various calendars."""

#     CALENDARS: ClassVar = {
#         GEDSpecial.GREGORIAN: {
#             GEDSpecial.MAX_MONTHS: 12,
#             GEDSpecial.MONTH_NAMES: {
#                 '01': 'JAN',
#                 '02': 'FEB',
#                 '03': 'MAR',
#                 '04': 'APR',
#                 '05': 'MAY',
#                 '06': 'JUN',
#                 '07': 'JUL',
#                 '08': 'AUG',
#                 '09': 'SEP',
#                 '10': 'OCT',
#                 '11': 'NOV',
#                 '12': 'DEC',
#             },
#             GEDSpecial.MONTH_MAX_DAYS: {
#                 '01': 31,
#                 '02': 29,
#                 '03': 31,
#                 '04': 30,
#                 '05': 31,
#                 '06': 30,
#                 '07': 31,
#                 '08': 31,
#                 '09': 30,
#                 '10': 31,
#                 '11': 30,
#                 '12': 31,
#             },
#         }
#     }


# class ISOMonths:
#     """ISO month values for GEDCOM month codes."""

#     CALENDARS: ClassVar = {
#         'GREGORIAN': {
#             'JAN': '01',
#             'FEB': '02',
#             'MAR': '03',
#             'APR': '04',
#             'MAY': '05',
#             'JUN': '06',
#             'JUL': '07',
#             'AUG': '08',
#             'SEP': '09',
#             'OCT': '10',
#             'NOV': '11',
#             'DEC': '12',
#         }
#     }
