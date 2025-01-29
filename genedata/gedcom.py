# GEDCOM constants

__all__ = [
    'Specs',
]

from dataclasses import dataclass


@dataclass(frozen=True)
class Specs:
    ADDRESS: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#ADDRESS_STRUCTURE'
    AGE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#age'
    ALIAS: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#ALIA'
    ASSOCIATION: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#ASSOCIATION_STRUCTURE'
    CHANGE_DATE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#CHANGE_DATE'
    CHILD: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#CHIL'
    CREATION_DATE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#CREATION_DATE'
    DATE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#date'
    DATE_VALUE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#DATE_VALUE'
    EVENT_DETAIL: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#EVENT_DETAIL'
    EXID: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#EXID'
    EXTENSION: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#extensions'
    FAMILY: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_RECORD'
    FAMILY_ATTRIBUTE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_ATTRIBUTE_STRUCTURE'
    FAMILY_CHILD: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMC'
    FAMILY_EVENT: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_EVENT_STRUCTURE'
    FAMILY_EVENT_DETAIL: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_EVENT_DETAIL'
    FAMILY_SPOUSE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMS'
    FILE: str = ''
    FILE_TRANSLATION: str = ''
    FRENCH_R: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FRENCH_R'
    GREGORIAN: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#GREGORIAN'
    HEADER: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#HEADER'
    HEBREW: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#HEBREW'
    HUSBAND: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#HUSB'
    IDENTIFIER: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#IDENTIFIER_STRUCTURE'
    INDIVIDUAL: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_RECORD'
    INDIVIDUAL_ATTRIBUTE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_ATTRIBUTE_STRUCTURE'
    INDIVIDUAL_EVENT: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_EVENT_STRUCTURE'
    INDIVIDUAL_EVENT_DETAIL: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_EVENT_DETAIL'
    JULIAN: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#JULIAN'
    LDS_INDIVIDUAL_ORDINANCE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#LDS_INDIVIDUAL_ORDINANCE'
    LDS_ORDINANCE_DETAIL: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#LDS_ORDINANCE_DETAIL'
    LDS_SPOUSE_SEALING: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#LDS_SPOUSE_SEALING'
    MAP: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#MAP'
    MULTIMEDIA: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#MULTIMEDIA_RECORD'
    MULTIMEDIA_LINK: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#MULTIMEDIA_LINK'
    NON_EVENT: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#NON_EVENT_STRUCTURE'
    NOTE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#NOTE_STRUCTURE'
    PERSONAL_NAME: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PERSONAL_NAME_STRUCTURE'
    PERSONAL_NAME_PIECES: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PERSONAL_NAME_PIECES'
    PLACE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PLACE_STRUCTURE'
    REPOSITORY: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#REPOSITORY_RECORD'
    SCHEMA: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SCHMA'
    SHARED_NOTE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SHARED_NOTE_RECORD'
    SOURCE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_RECORD'
    SOURCE_EVENT: str = ''
    SOURCE_CITATION: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_CITATION'
    SOURCE_REPOSITORY_CITATION: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_REPOSITORY_CITATION'
    SUBMITTER: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SUBMITTER_RECORD'
    TIME: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#time'
    WIFE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#WIFE'
    
    