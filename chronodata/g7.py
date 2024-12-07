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


@dataclass(frozen=True)
class ExtTag:
    """Constant definitions for extention tags."""

    _DATE: str = '_DATE'
    _LOC: str = '_LOC'
    _PARTNER: str = 'PARTNER'
    _POP: str = '_POP'


@dataclass(frozen=True)
class Record:
    FAMILY: str = 'family'
    INDIVIDUAL: str = 'individual'
    MULTIMEDIA: str = 'multimedia'
    REPOSITORY: str = 'repository'
    SHARED_NOTE: str = 'shared note'
    SOURCE: str = 'source'
    SUBMITTER: str = 'submitter'


@dataclass(frozen=True)
class GEDSpecial:
    """Constant definitions for special GEDCOM string."""

    ATSIGN: str = '@'
    BC: str = 'BCE'
    COLON: str = ':'
    DAY: str = 'd'
    FRENCH_R: str = 'FRENCH_R'
    GREATER_THAN: str = '>'
    GREGORIAN: str = 'GREGORIAN'
    HEBREW: str = 'HEBREW'
    HYPHEN: str = '-'
    JULIAN: str = 'JULIAN'
    LESS_THAN: str = '<'
    MONTH: str = 'm'
    NEWLINE: str = '\n'
    NOW: str = 'now'
    SPACE: str = ' '
    T: str = 'T'
    VERSION: str = '7.0'
    VOID: str = '@VOID@'
    WEEK: str = 'w'
    YEAR: str = 'y'
    Z: str = 'Z'


# @dataclass(frozen=True)
class GEDMonths:
    """GEDCOM Month codes for various calendars."""

    CALENDARS: ClassVar = {
        'GREGORIAN': {
            '01': 'JAN',
            '02': 'FEB',
            '03': 'MAR',
            '04': 'APR',
            '05': 'MAY',
            '06': 'JUN',
            '07': 'JUL',
            '08': 'AUG',
            '09': 'SEP',
            '10': 'OCT',
            '11': 'NOV',
            '12': 'DEC',
        }
    }


class ISOMonths:
    """ISO month values for GEDCOM month codes."""

    CALENDARS: ClassVar = {
        'GREGORIAN': {
            'JAN': '01',
            'FEB': '02',
            'MAR': '03',
            'APR': '04',
            'MAY': '05',
            'JUN': '06',
            'JUL': '07',
            'AUG': '08',
            'SEP': '09',
            'OCT': '10',
            'NOV': '11',
            'DEC': '12',
        }
    }


@dataclass(frozen=True)
class Gedcom:
    """Constant definitions of GEDCOM tags."""

    ABBR: str = 'ABBR'
    ADDR: str = 'ADDR'
    ADOP: str = 'ADOP'
    ADOP_FAMC: str = 'ADOPT-FAMC'
    ADOPTED: str = 'ADOPTED'  # ?#
    ADR1: str = 'ADR1'
    ADR2: str = 'ADR2'
    ADR3: str = 'ADR3'
    AFN: str = 'AFN'
    AGE: str = 'AGE'
    AGNC: str = 'AGNC'
    AKA: str = 'AKA'  # ?#
    ALIA: str = 'ALIA'
    ANCI: str = 'ANCI'
    ANUL: str = 'ANUL'
    ASSO: str = 'ASSO'
    AUDIO: str = 'AUDIO'  # ?#
    AUTH: str = 'AUTH'
    BAPL: str = 'BAPL'
    BAPM: str = 'BAPM'
    BARM: str = 'BARM'
    BASM: str = 'BASM'
    BIRT: str = 'BIRT'
    BIRTH: str = 'BIRTH'  # ?#
    BLES: str = 'BLES'
    BOTH: str = 'BOTH'  # ?#
    BTC: str = 'BTC'  # ?#
    BURI: str = 'BURI'
    CALN: str = 'CALN'
    CANCELED: str = 'CANCELED'  # ?#
    CARD: str = 'CARD'  # ?#
    CAST: str = 'CAST'
    CAUS: str = 'CAUS'
    CENS: str = 'CENS'  # ?#
    CHALLENGED: str = 'CHALLENGED'  # ?#
    CHAN: str = 'CHAN'
    CHIL: str = 'CHIL'
    CHILD: str = 'CHILD'  # ?#
    CHALLENGE: str = 'CHALLENGE'
    CHR: str = 'CHR'
    CHRON_NAMES: str = 'CHRON NAMES'
    CHRONS: str = 'CHRONOS'
    CHRA: str = 'CHRA'
    CITY: str = 'CITY'
    CLERGY: str = 'CLERGY'  # ?#
    COMPLETED: str = 'COMPLETED'  # ?#
    CONF: str = 'CONF'
    CONFIDENTIAL: str = 'CONFIDENTIAL'  # ?#
    CONL: str = 'CONL'
    CONT: str = 'CONT'
    COPR: str = 'COPR'
    CORP: str = 'CORP'
    CREA: str = 'CREA'
    CREM: str = 'CREM'
    CROP: str = 'CROP'
    CTRY: str = 'CTRY'
    DATA: str = 'DATA'
    DATA_EVEN: str = 'DATA-EVEN'
    DATA_EVEN_DATE: str = 'DATA-EVEN-DATE'
    DATE: str = 'DATE'
    DATE_exact: str = 'DATA-exact'
    DEAT: str = 'DEAT'
    DESI: str = 'DESI'
    DEST: str = 'DEST'
    DISPROVEN: str = 'DISPROVEN'  # ?#
    DIV: str = 'DIV'
    DIVF: str = 'DIVF'
    DNS: str = 'DNS'  # ?#
    DNS_CAN: str = 'DNS_CAN'  # ?#
    DSCR: str = 'DSCR'
    EDUC: str = 'EDUC'
    ELECTRONIC: str = 'ELECTRONIC'  # ?#
    EMAIL: str = 'EMAIL'
    EMIG: str = 'EMIG'
    ENDL: str = 'ENDL'
    ENGA: str = 'ENGA'
    EVEN: str = 'EVEN'  # ?#
    EXCLUDED: str = 'EXCLUDED'  # ?#
    EXID: str = 'EXID'
    EXID_TYPE: str = 'EXID-TYPE'
    F: str = 'F'  # ?#
    FACT: str = 'FACT'  # ?#
    FAM: str = 'FAM'  # ?#
    FATH: str = 'FATH'  # ?#
    FAM_CENS: str = 'FAM-CENS'
    FAM_EVEN: str = 'FAM-EVEN'
    FAM_FACT: str = 'FAM-FACT'
    FAM_HUSB: str = 'FAM-HUSB'
    FAM_NCHI: str = 'FAM-NCHI'
    FAM_RESI: str = 'FAM-RESI'
    FAM_WIFE: str = 'FAM-WIFE'
    FAMC: str = 'FAMC'
    FAMC_ADOPT: str = 'FAMC-ADOPT'
    FAMC_STAT: str = 'FAMC-STAT'
    FAMS: str = 'FAMS'
    FAX: str = 'FAX'
    FCOM: str = 'FCOM'
    FICHE: str = 'FICHE'  # ?#
    FILE: str = 'FILE'
    FILE_TRAN: str = 'FILE-TRAN'
    FILM: str = 'FILM'  # ?#
    FORM: str = 'FORM'
    FOSTER: str = 'FOSTER'  # ?#
    FRIEND: str = 'FRIEND'  # ?#
    GEDC: str = 'GEDC'
    GIVN: str = 'GIVN'
    GODP: str = 'GODP'  # ?#
    GRAD: str = 'GRAD'
    HEAD: str = 'HEAD'
    HEAD_DATE: str = 'HEAD-DATE'
    HEAD_LANG: str = 'HEAD-LANG'
    HEAD_PLAC: str = 'HEAD-PLAC'
    HEAD_PLAC_FORM: str = 'HEAD-PLAC-FORM'
    HEAD_SOUR: str = 'HEAD-SOUR'
    HEAD_SOUR_DATA: str = 'HEAD-SOUR-DATA'
    HEIGHT: str = 'HEIGHT'
    HUSB: str = 'HUSB'
    IDNO: str = 'IDNO'
    IMMI: str = 'IMMI'
    IMMIGRANT: str = 'IMMIGRANT'  # ?#
    INDI: str = 'INDI'
    INDI_CENS: str = 'INDI-CENS'
    INDI_EVEN: str = 'INDI-EVEN'
    INDI_FACT: str = 'INDI-FACT'
    INDI_FAMC: str = 'INDI-FAMC'
    INDI_NAME: str = 'INDI-NAME'
    INDI_NCHI: str = 'INDI-NCHI'
    INDI_RELI: str = 'INDI-RELI'
    INDI_RESI: str = 'INDI-RESI'
    INDI_TITL: str = 'INDI-TITLE'
    INFANT: str = 'INFANT'  # ?#
    INIL: str = 'INIL'
    LANG: str = 'LANG'
    LATI: str = 'LATI'
    LEFT: str = 'LEFT'
    LOCKED: str = 'LOCKED'  # ?#
    LONG: str = 'LONG'
    M: str = 'M'  # ?#
    MAGAZINE: str = 'MAGAZINE'  # ?#
    MAIDEN: str = 'MAIDEN'  # ?#
    MAP: str = 'MAP'
    MARB: str = 'MARB'
    MARC: str = 'MARC'
    MARL: str = 'MARL'
    MARR: str = 'MARR'
    MARRIED: str = 'MARRIED'  # ?#
    MARS: str = 'MARS'
    MEDI: str = 'MEDI'
    MIME: str = 'MIME'
    MOTH: str = 'MOTH'  # ?#
    MULTIPLE: str = 'MULTIPLE'  # ?#
    NAME: str = 'NAME'
    NAME_TRAN: str = 'NAME-TRAN'
    NAME_TYPE: str = 'NAME-TYPE'
    NATI: str = 'NATI'
    NATU: str = 'NATU'
    NCHI: str = 'NCHI'
    NEWSPAPER: str = 'NEWSPAPER'  # ?#
    NGHBR: str = 'NEIGHBOR'  # ?#
    NICK: str = 'NICK'
    NMR: str = 'NMR'
    NO: str = 'NO'
    NO_DATE: str = 'NO-DATE'
    NOTE: str = 'NOTE'
    NOTE_TRAN: str = 'NOTE-TRAN'
    NPFX: str = 'NPFX'
    NSFX: str = 'NSFX'
    OBJE: str = 'OBJE'
    OCCU: str = 'OCCU'
    OFFICIATOR: str = 'OFFICIATOR'  # ?#
    ORDN: str = 'ORDN'
    OTHER: str = 'OTHER'  # ?#
    PAGE: str = 'PAGE'
    PEDI: str = 'PEDI'
    PARENT: str = 'PARENT'  # ?#
    PHON: str = 'PHON'
    PHOTO: str = 'PHOTO'  # ?#
    PHRASE: str = 'PHRASE'
    PLAC: str = 'PLAC'
    PLAC_FORM: str = 'PLAC-FORM'
    PLAC_TRAN: str = 'PLAC-TRAN'
    POST: str = 'POST'
    PRE_1970: str = 'PRE_1970'  # ?#
    PRIVACY: str = 'PRIVACY'  # ?#
    PROB: str = 'PROB'
    PROFESSIONAL: str = 'PROFESSIONAL'  # ?#
    PROP: str = 'PROP'
    PROVEN: str = 'PROVEN'
    PUBL: str = 'PUBL'
    QUAY: str = 'QUAY'
    QUAY0: str = '0'  # ?#
    QUAY1: str = '1'  # ?#
    QUAY2: str = '2'  # ?#
    QUAY3: str = '3'  # ?#
    REFN: str = 'REFN'
    RELI: str = 'RELI'
    REPO: str = 'REPO'
    RESN: str = 'RESN'
    RETI: str = 'RETI'
    RIN: str = 'RIN'
    ROLE: str = 'ROLE'
    SCHMA: str = 'SCHMA'
    SDATE: str = 'SDATE'
    SEALING: str = 'SEALING'  # ?#
    SEX: str = 'SEX'
    SLGC: str = 'SLGC'
    SLGS: str = 'SLGS'
    SNOTE: str = 'SNOTE'
    SOUR: str = 'SOUR'
    SOUR_DATA: str = 'SOUR-DATA'
    SOUR_EVEN: str = 'SOUR-EVEN'
    SPFX: str = 'SPFX'
    SPOU: str = 'SPOU'  # ?#
    STILLBORN: str = 'STILLBORN'  # ?#
    SUBMITTED: str = 'SUBMITTED'  # ?#
    SSN: str = 'SSN'
    STAE: str = 'STAE'
    STAT: str = 'STAT'  # ?#
    SUBM: str = 'SUBM'
    SUBM_LANG: str = 'SUBM-LANG'
    SURN: str = 'SURN'
    TAG: str = 'TAG'
    TEMP: str = 'TEMP'
    TESTCASES: str = 'TEST CASES'
    TEXT: str = 'TEXT'
    TEXT_HTML: str = 'text/html'
    TEXT_PLAIN: str = 'text/plain'
    TIME: str = 'TIME'
    TITL: str = 'TITL'
    TOMBSTONE: str = 'TOMBSTONE'  # ?#
    TOP: str = 'TOP'
    TRAN: str = 'TRAN'  # ?#
    TRLR: str = 'TRLR'
    TYPE: str = 'TYPE'
    U: str = 'U'  # ?#
    UNCLEARED: str = 'UNCLEARED'  # ?#
    UID: str = 'UID'
    VERS: str = 'VERS'
    VIDEO: str = 'VIDEO'  # ?#
    WIDTH: str = 'WIDTH'
    WIFE: str = 'WIFE'
    WILL: str = 'WILL'
    WITN: str = 'WITN'  # ?#
    WWW: str = 'WWW'
    X: str = 'X'  # ?#
    FRENCH_R: str = 'FRENCH_R'
    GREGORIAN: str = 'GREGORIAN'
    HEBREW: str = 'HEBREW'
    JULIAN: str = 'JULIAN'
    N_0: str = '0'
    N_1: str = '1'
    N_2: str = '2'
    N_3: str = '3'
    ADOP_HUSB: str = 'enum-ADOP-HUSB'
    ADOP_WIFE: str = 'enum-ADOP-WIFE'
    BIC: str = 'enum-BIC'
    BOOK: str = 'BOOK'
    MANUSCRIPT: str = 'MANUSCRIPT'
    RESI: str = 'RESI'


@dataclass(frozen=True)
class Enum:
    """Sets of GEDCOM tags that are valid for specific structures.

    Reference
    ---------
    - [Individual Events (EVEN)](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#events)

    """

    ADOP: frozenset[str] = frozenset([Gedcom.HUSB, Gedcom.WIFE, Gedcom.BOTH])
    EVEN: frozenset[str] = frozenset([Gedcom.CENS])
    EVENATTR: frozenset[str] = frozenset(
        [Gedcom.CENS, Gedcom.NCHI, Gedcom.RESI, Gedcom.FACT, Gedcom.EVEN]
    )
    FAMC_STAT: frozenset[str] = frozenset(
        [Gedcom.CHALLENGED, Gedcom.DISPROVEN, Gedcom.PROVEN]
    )
    FAM_ATTR: frozenset[str] = frozenset(
        [
            Gedcom.NCHI,
            Gedcom.RESI,
            Gedcom.FACT,
        ]
    )
    FAM_EVEN: frozenset[str] = frozenset(
        [
            Gedcom.ANUL,
            Gedcom.CENS,
            Gedcom.DIV,
            Gedcom.DIVF,
            Gedcom.ENGA,
            Gedcom.MARB,
            Gedcom.MARC,
            Gedcom.MARL,
            Gedcom.MARR,
            Gedcom.MARS,
            Gedcom.EVEN,
        ]
    )
    ID: frozenset[str] = frozenset([Gedcom.REFN, Gedcom.UID, Gedcom.EXID])
    INDI_ATTR: frozenset[str] = frozenset(
        [
            Gedcom.CAST,
            Gedcom.DSCR,
            Gedcom.EDUC,
            Gedcom.IDNO,
            Gedcom.NATI,
            Gedcom.NCHI,
            Gedcom.NMR,
            Gedcom.OCCU,
            Gedcom.PROP,
            Gedcom.RELI,
            Gedcom.RESI,
            Gedcom.SSN,
            Gedcom.TITL,
            Gedcom.FACT,
        ]
    )
    INDI_EVEN: frozenset[str] = frozenset(
        [
            Gedcom.ADOP,
            Gedcom.BAPM,
            Gedcom.BARM,
            Gedcom.BASM,
            Gedcom.BIRT,
            Gedcom.BLES,
            Gedcom.BURI,
            Gedcom.CENS,
            Gedcom.CHR,
            Gedcom.CHRA,
            Gedcom.CONF,
            Gedcom.CREM,
            Gedcom.DEAT,
            Gedcom.EMIG,
            Gedcom.FCOM,
            Gedcom.GRAD,
            Gedcom.IMMI,
            Gedcom.NATU,
            Gedcom.ORDN,
            Gedcom.PROB,
            Gedcom.RETI,
            Gedcom.WILL,
            Gedcom.EVEN,
        ]
    )
    MEDI: frozenset[str] = frozenset(
        [
            Gedcom.AUDIO,
            Gedcom.BOOK,
            Gedcom.CARD,
            Gedcom.ELECTRONIC,
            Gedcom.FICHE,
            Gedcom.FILM,
            Gedcom.MAGAZINE,
            Gedcom.MANUSCRIPT,
            Gedcom.MAP,
            Gedcom.NEWSPAPER,
            Gedcom.PHOTO,
            Gedcom.TOMBSTONE,
            Gedcom.VIDEO,
            Gedcom.OTHER,
        ]
    )
    MEDIA_TYPE: frozenset[str] = frozenset(
        [
            Gedcom.TEXT_HTML,
            Gedcom.TEXT_PLAIN,
        ]
    )
    NAME_TYPE: frozenset[str] = frozenset(
        [
            Gedcom.AKA,
            Gedcom.BIRTH,
            Gedcom.IMMIGRANT,
            Gedcom.MAIDEN,
            Gedcom.MARRIED,
            Gedcom.PROFESSIONAL,
            Gedcom.OTHER,
        ]
    )
    PEDI: frozenset[str] = frozenset(
        [
            Gedcom.ADOPTED,
            Gedcom.BIRTH,
            Gedcom.FOSTER,
            Gedcom.SEALING,
            Gedcom.OTHER,
        ]
    )
    QUAY: frozenset[str] = frozenset(
        [Gedcom.QUAY0, Gedcom.QUAY1, Gedcom.QUAY2, Gedcom.QUAY3]
    )
    RESN: frozenset[str] = frozenset(
        [Gedcom.CONFIDENTIAL, Gedcom.LOCKED, Gedcom.PRIVACY]
    )
    ROLE: frozenset[str] = frozenset(
        [
            Gedcom.CHIL,
            Gedcom.CLERGY,
            Gedcom.FATH,
            Gedcom.FRIEND,
            Gedcom.GODP,
            Gedcom.HUSB,
            Gedcom.MOTH,
            Gedcom.MULTIPLE,
            Gedcom.NGHBR,
            Gedcom.OFFICIATOR,
            Gedcom.PARENT,
            Gedcom.SPOU,
            Gedcom.WIFE,
            Gedcom.WITN,
            Gedcom.OTHER,
        ]
    )
    SEX: frozenset[str] = frozenset([Gedcom.M, Gedcom.F, Gedcom.X, Gedcom.U])
    STAT: frozenset[str] = frozenset(
        [
            Gedcom.BIC,
            Gedcom.CANCELED,
            Gedcom.CHILD,
            Gedcom.COMPLETED,
            Gedcom.EXCLUDED,
            Gedcom.DNS,
            Gedcom.DNS_CAN,
            Gedcom.INFANT,
            Gedcom.PRE_1970,
            Gedcom.STILLBORN,
            Gedcom.SUBMITTED,
            Gedcom.UNCLEARED,
        ]
    )


@dataclass(frozen=True)
class EnumName:
    ADOP: str = 'ADOP'
    EVEN: str = 'EVEN (Event)'
    EVENATTR: str = 'EVENATTR'
    FAMC: str = 'FAMC'
    FAM_ATTR: str = 'family attributes'
    FAM_EVEN: str = 'family events'
    ID: str = 'ID'
    INDI_ATTR: str = 'individual attributes'
    INDI_EVEN: str = 'individual events'
    MEDI: str = 'MEDI'
    MEDIA_TYPE: str = 'MEDIA_TYPE'
    NAME_TYPE: str = 'NAME_TYPE'
    PEDI: str = 'PEDI'
    QUAY: str = 'QUAY'
    RESN: str = 'RESN'
    ROLE: str = 'ROLE'
    SEX: str = 'SEX'
    STAT: str = 'STAT'
