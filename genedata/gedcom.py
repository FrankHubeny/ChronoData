# GEDCOM constants

__all__ = [
    'Specs',
]

from dataclasses import dataclass


@dataclass(frozen=True)
class OverView:
    """Provide a description of the seven record types and the header record.

    Descriptions of structures between `<<` and `>>` are structure names.  Below
    these structure names are their expansion.  
    If the expansion has been given earlier, it is not repeated.
    Since these start at level 0 the `+` is removed and the `n` is replaced
    with 0 for this overview.
    Individual tags have links to their yaml definitions.

    The first number is the level of the line. Then comes the tag with payload description.
    To the right is a quantity key `{optionality:quantity}`.  The optionality flag
    can be either 1 for mandatory or 0 for optiona.  The quantity flag can be either 
    1 for single or M for multiple.  Following this is a link to the tag specfication.

    The actual GEDCOM file does not contain the indentations.  The indentations are used here 
    and in the GEDCOM specification to make the different levels more evident.

    Example:
        To display this information import `OverView` from the gedcom module and print the 
        the desired record.  To print the Header record do the following.  Only the first line
        is displayed in the example.
        >>> from genedata.gedcom import OverView
        >>> print(OverView.HEADER) #doctest: +ELLIPSIS
        <BLANKLINE>
        0 HEAD                                    {1:1}  [g7:HEAD](https://gedcom.io/terms/v7/HEAD)
          1 GEDC                                  {1:1}  [g7:GEDC](https://gedcom.io/terms/v7/GEDC)
             2 VERS <Special>                     {1:1}  [g7:GEDC-VERS](https://gedcom.io/terms/v7/GEDC-VERS)
          1 SCHMA                                 {0:1}  [g7:SCHMA](https://gedcom.io/terms/v7/SCHMA)
             2 TAG <Special>                      {0:M}  [g7:TAG](https://gedcom.io/terms/v7/TAG)
          1 SOUR <Special>                        {0:1}  [g7:HEAD-SOUR](https://gedcom.io/terms/v7/HEAD-SOUR)
             2 VERS <Special>                     {0:1}  [g7:VERS](https://gedcom.io/terms/v7/VERS)
             2 NAME <Text>                        {0:1}  [g7:NAME](https://gedcom.io/terms/v7/NAME)
             2 CORP <Text>                        {0:1}  [g7:CORP](https://gedcom.io/terms/v7/CORP)
                3 <<ADDRESS_STRUCTURE>>           {0:1}
                3 ADDR <Special>                  {1:1}  [g7:ADDR](https://gedcom.io/terms/v7/ADDR)
                   4 ADR1 <Special>               {0:1}  [g7:ADR1](https://gedcom.io/terms/v7/ADR1)
                   4 ADR2 <Special>               {0:1}  [g7:ADR2](https://gedcom.io/terms/v7/ADR2)
                   4 ADR3 <Special>               {0:1}  [g7:ADR3](https://gedcom.io/terms/v7/ADR3)
                   4 CITY <Special>               {0:1}  [g7:CITY](https://gedcom.io/terms/v7/CITY)
                   4 STAE <Special>               {0:1}  [g7:STAE](https://gedcom.io/terms/v7/STAE)
                   4 POST <Special>               {0:1}  [g7:POST](https://gedcom.io/terms/v7/POST)
                   4 CTRY <Special>               {0:1}  [g7:CTRY](https://gedcom.io/terms/v7/CTRY)
                3 PHON <Special>                  {0:M}  [g7:PHON](https://gedcom.io/terms/v7/PHON)
                3 EMAIL <Special>                 {0:M}  [g7:EMAIL](https://gedcom.io/terms/v7/EMAIL)
                3 FAX <Special>                   {0:M}  [g7:FAX](https://gedcom.io/terms/v7/FAX)
                3 WWW <Special>                   {0:M}  [g7:WWW](https://gedcom.io/terms/v7/WWW)
             2 DATA <Text>                        {0:1}  [g7:HEAD-SOUR-DATA](https://gedcom.io/terms/v7/HEAD-SOUR-DATA)
                3 DATE <DateExact>                {0:1}  [g7:DATE-exact](https://gedcom.io/terms/v7/DATE-exact)
                   4 TIME <Time>                  {0:1}  [g7:TIME](https://gedcom.io/terms/v7/TIME)
                3 COPR <Text>                     {0:1}  [g7:COPR](https://gedcom.io/terms/v7/COPR)
          1 DEST <Special>                        {0:1}  [g7:DEST](https://gedcom.io/terms/v7/DEST)
          1 DATE <DateExact>                      {0:1}  [g7:HEAD-DATE](https://gedcom.io/terms/v7/HEAD-DATE)
             2 TIME <Time>                        {0:1}  [g7:TIME](https://gedcom.io/terms/v7/TIME)
          1 SUBM @<XREF:SUBM>@                    {0:1}  [g7:SUBM](https://gedcom.io/terms/v7/SUBM)
          1 COPR <Text>                           {0:1}  [g7:COPR](https://gedcom.io/terms/v7/COPR)
          1 LANG <Language>                       {0:1}  [g7:HEAD-LANG](https://gedcom.io/terms/v7/LANG)
          1 PLAC                                  {0:1}  [g7:HEAD-PLAC](https://gedcom.io/terms/v7/PLAC)
             2 FORM <List:Text>                   {1:1}  [g7:HEAD-PLAC-FORM](https://gedcom.io/terms/v7/PLAC-FORM)
          1 <<NOTE_STRUCTURE>>                    {0:1}
          [
          1 NOTE <Text>                           {1:1}  [g7:NOTE](https://gedcom.io/terms/v7/NOTE)
             2 MIME <MediaType>                   {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
             2 LANG <Language>                    {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
             2 TRAN <Text>                        {0:M}  [g7:NOTE-TRAN](https://gedcom.io/terms/v7/NOTE-TRAN)
                3 MIME <MediaType>                {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
                3 LANG <Language>                 {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
             2 <<SOURCE_CITATION>>                {0:M}
          |
          1 SNOTE @<XREF:SNOTE>@                  {1:1}  [g7:SNOTE](https://gedcom.io/terms/v7/SNOTE)
          ]
        <BLANKLINE>
    
    Reference:
        [The FamilySearch GEDCOM Specifications](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html)
    """
    FAMILY: str = """
n @XREF:FAM@ FAM                           {1:1}  g7:record-FAM
  +1 RESN <List:Enum>                      {0:1}  g7:RESN
  +1 <<FAMILY_ATTRIBUTE_STRUCTURE>>        {0:M}
  +1 <<FAMILY_EVENT_STRUCTURE>>            {0:M}
  +1 <<NON_EVENT_STRUCTURE>>               {0:M}
  +1 HUSB @<XREF:INDI>@                    {0:1}  g7:FAM-HUSB
     +2 PHRASE <Text>                      {0:1}  g7:PHRASE
  +1 WIFE @<XREF:INDI>@                    {0:1}  g7:FAM-WIFE
     +2 PHRASE <Text>                      {0:1}  g7:PHRASE
  +1 CHIL @<XREF:INDI>@                    {0:M}  g7:CHIL
     +2 PHRASE <Text>                      {0:1}  g7:PHRASE
  +1 <<ASSOCIATION_STRUCTURE>>             {0:M}
  +1 SUBM @<XREF:SUBM>@                    {0:M}  g7:SUBM
  +1 <<LDS_SPOUSE_SEALING>>                {0:M}
  +1 <<IDENTIFIER_STRUCTURE>>              {0:M}
  +1 <<NOTE_STRUCTURE>>                    {0:M}
  +1 <<SOURCE_CITATION>>                   {0:M}
  +1 <<MULTIMEDIA_LINK>>                   {0:M}
  +1 <<CHANGE_DATE>>                       {0:1}
  +1 <<CREATION_DATE>>                     {0:1}
"""
    HEADER: str = """
0 HEAD                                    {1:1}  [g7:HEAD](https://gedcom.io/terms/v7/HEAD)
  1 GEDC                                  {1:1}  [g7:GEDC](https://gedcom.io/terms/v7/GEDC)
     2 VERS <Special>                     {1:1}  [g7:GEDC-VERS](https://gedcom.io/terms/v7/GEDC-VERS)
  1 SCHMA                                 {0:1}  [g7:SCHMA](https://gedcom.io/terms/v7/SCHMA)
     2 TAG <Special>                      {0:M}  [g7:TAG](https://gedcom.io/terms/v7/TAG)
  1 SOUR <Special>                        {0:1}  [g7:HEAD-SOUR](https://gedcom.io/terms/v7/HEAD-SOUR)
     2 VERS <Special>                     {0:1}  [g7:VERS](https://gedcom.io/terms/v7/VERS)
     2 NAME <Text>                        {0:1}  [g7:NAME](https://gedcom.io/terms/v7/NAME)
     2 CORP <Text>                        {0:1}  [g7:CORP](https://gedcom.io/terms/v7/CORP)
        3 <<ADDRESS_STRUCTURE>>           {0:1}
        3 ADDR <Special>                  {1:1}  [g7:ADDR](https://gedcom.io/terms/v7/ADDR)
           4 ADR1 <Special>               {0:1}  [g7:ADR1](https://gedcom.io/terms/v7/ADR1)
           4 ADR2 <Special>               {0:1}  [g7:ADR2](https://gedcom.io/terms/v7/ADR2)
           4 ADR3 <Special>               {0:1}  [g7:ADR3](https://gedcom.io/terms/v7/ADR3)
           4 CITY <Special>               {0:1}  [g7:CITY](https://gedcom.io/terms/v7/CITY)
           4 STAE <Special>               {0:1}  [g7:STAE](https://gedcom.io/terms/v7/STAE)
           4 POST <Special>               {0:1}  [g7:POST](https://gedcom.io/terms/v7/POST)
           4 CTRY <Special>               {0:1}  [g7:CTRY](https://gedcom.io/terms/v7/CTRY)
        3 PHON <Special>                  {0:M}  [g7:PHON](https://gedcom.io/terms/v7/PHON)
        3 EMAIL <Special>                 {0:M}  [g7:EMAIL](https://gedcom.io/terms/v7/EMAIL)
        3 FAX <Special>                   {0:M}  [g7:FAX](https://gedcom.io/terms/v7/FAX)
        3 WWW <Special>                   {0:M}  [g7:WWW](https://gedcom.io/terms/v7/WWW)
     2 DATA <Text>                        {0:1}  [g7:HEAD-SOUR-DATA](https://gedcom.io/terms/v7/HEAD-SOUR-DATA)
        3 DATE <DateExact>                {0:1}  [g7:DATE-exact](https://gedcom.io/terms/v7/DATE-exact)
           4 TIME <Time>                  {0:1}  [g7:TIME](https://gedcom.io/terms/v7/TIME)
        3 COPR <Text>                     {0:1}  [g7:COPR](https://gedcom.io/terms/v7/COPR)
  1 DEST <Special>                        {0:1}  [g7:DEST](https://gedcom.io/terms/v7/DEST)
  1 DATE <DateExact>                      {0:1}  [g7:HEAD-DATE](https://gedcom.io/terms/v7/HEAD-DATE)
     2 TIME <Time>                        {0:1}  [g7:TIME](https://gedcom.io/terms/v7/TIME)
  1 SUBM @<XREF:SUBM>@                    {0:1}  [g7:SUBM](https://gedcom.io/terms/v7/SUBM)
  1 COPR <Text>                           {0:1}  [g7:COPR](https://gedcom.io/terms/v7/COPR)
  1 LANG <Language>                       {0:1}  [g7:HEAD-LANG](https://gedcom.io/terms/v7/LANG)
  1 PLAC                                  {0:1}  [g7:HEAD-PLAC](https://gedcom.io/terms/v7/PLAC)
     2 FORM <List:Text>                   {1:1}  [g7:HEAD-PLAC-FORM](https://gedcom.io/terms/v7/PLAC-FORM)
  1 <<NOTE_STRUCTURE>>                    {0:1}
  [
  1 NOTE <Text>                           {1:1}  [g7:NOTE](https://gedcom.io/terms/v7/NOTE)
     2 MIME <MediaType>                   {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
     2 LANG <Language>                    {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
     2 TRAN <Text>                        {0:M}  [g7:NOTE-TRAN](https://gedcom.io/terms/v7/NOTE-TRAN)
        3 MIME <MediaType>                {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
        3 LANG <Language>                 {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
     2 <<SOURCE_CITATION>>                {0:M}
  |
  1 SNOTE @<XREF:SNOTE>@                  {1:1}  [g7:SNOTE](https://gedcom.io/terms/v7/SNOTE)
  ]
    """
    INDIVIDUAL: str = ''
    MULTIMEDIA: str = ''
    REPOSITORY: str = ''
    SHARED_NOTE: str = ''
    SOURCE: str = ''
    SUBMITTER: str = ''

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
    
    