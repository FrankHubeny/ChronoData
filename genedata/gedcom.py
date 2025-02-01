# gedcom.py
"""Store GEDCOM specific constants, tags, enumeration sets and structure representations.

These are values that may be used in the Tag position of a GEDCOM line
    where a line contains the following components:
        - Required Level: A non-negative integer denoting the level of the line.
        - Optional Xref: A cross-reference identifier.
        - Required Tag: A value from this enumeration class or an extended Tag defined by the `Schema` class.
        - Optional LineVal: A string or value from a GEDCOM enumeration set.
            This is also called the payload.

    Values from this enumeration class are defined as enumeration sets to validate the use of the tag
    in a structure type.  The following are such Tag subenumerations:
        - `FamAttr`:
        - `IndiAttr`:
        - `IndiEven`:
        - `PersonalNamePieceTag`:
        - `Record`:

    The GEDCOM enumeration sets are implemented as enumeration classes with the similar names.  These
    are not Tags nor subenumerations of Tag, but independent enumeration classes.
        - `Adop`: [ADOP enumset]()
        - `Even`: [EVEN enumset]()
        - `EvenAttr`: [EVEN-ATTR enumset]()
        - `FamcStat`: [FAMC-STAT enumset]()
        - `Medium`: [MEDI enumset]()
        - `NameType`: [NAME-TYPE enumset]()
        - `Pedi`: [PEDI enumset]()
        - `Quay`: [QUAY enumset]()
        - `Resn`: [RESN enumset]()
        - `Role`: [ROLE enumset]()
        - `Sex`: [SEX enumset]()
        - `Stat`: [ord-STAT enumset]()


These enumation sets should not be confused with Tags.  They are used in the LineVal part of
a GEDCOM line rather than the Tag part of the line.

    References:
        [GEDCOM Enumeration Values](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#enumeration-values)
        [GEDCOM Line](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#lines)
        [GEDCOM Structure Types](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#structure-types)
        [GEDCOM Specification](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html)
"""

__all__ = [
    'Adop',
    'EvenAttr',
    'FamAttr',
    'FamEven',
    'FamcStat',
    'Id',
    'IndiAttr',
    'IndiEven',
    'LineVal',
    'Medium',
    'NameType',
    'OverView',
    'Pedi',
    'PersonalNamePieceTag',
    'Quay',
    'Record',
    'Resn',
    'Role',
    'Sex',
    'Specs',
    'Stat',
    'Tag',
]

from dataclasses import dataclass
from enum import Enum
from typing import Any, NamedTuple


class String(Enum):
    EMPTY: str = ''


class DataType(Enum):
    """Enumerate the GEDCOM data types.

    Reference:
        [GEDCOM Data Types](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#datatypes)
    """

    TEXT = 'Text'
    INTEGER = 'Integer'
    ENUMERATION = 'Enumeration'
    DATE = 'Date'
    TIME = 'Time'
    AGE = 'Age'
    LIST = 'List'
    PERSONAL_NAME = 'Personal Name'
    LANGUAGE = 'Language'
    MEDIA_TYPE = 'Media Type'
    SPECIAL = 'Special'
    FILE_PATH = 'File Path'


class Line(NamedTuple):
    """A datastructure to store a GEDCOM line with documentation."""

    tag: str
    data_type: DataType
    required: bool
    many: bool
    documentation: str
    increment: int = 0
    xref: bool = False
    extra: str = ''
    sublines: list[Any] | None = None


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
        >>> print(OverView.HEADER)  # doctest: +ELLIPSIS
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
             2 SOUR @<XREF:SOUR>@                 {1:1}  [g7:SOUR](https://gedcom.io/terms/v7/SOUR)
                3 PAGE <Text>                     {0:1}  [g7:PAGE](https://gedcom.io/terms/v7/PAGE)
                3 DATA                            {0:1}  [g7:SOUR-DATA](https://gedcom.io/terms/v7/SOUR-DATA)
                   4 <<DATE_VALUE>>               {0:1}
                   4 TEXT <Text>                  {0:M}  [g7:TEXT](https://gedcom.io/terms/v7/TEXT)
                      5 MIME <MediaType>          {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
                      5 LANG <Language>           {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
                3 EVEN <Enum>                     {0:1}  [g7:SOUR-EVEN](https://gedcom.io/terms/v7/SOUR-EVEN)
                   4 PHRASE <Text>                {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
                   4 ROLE <Enum>                  {0:1}  [g7:ROLE](https://gedcom.io/terms/v7/ROLE)
                      5 PHRASE <Text>             {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
                3 QUAY <Enum>                     {0:1}  [g7:QUAY](https://gedcom.io/terms/v7/QUAY)
                3 <<MULTIMEDIA_LINK>>             {0:M}
                3 OBJE @<XREF:OBJE>@              {1:1}  [g7:OBJE](https://gedcom.io/terms/v7/OBJE)
                   4 CROP                         {0:1}  [g7:CROP](https://gedcom.io/terms/v7/CROP)
                      5 TOP <Integer>             {0:1}  [g7:TOP](https://gedcom.io/terms/v7/TOP)
                      5 LEFT <Integer>            {0:1}  [g7:LEFT](https://gedcom.io/terms/v7/LEFT)
                      5 HEIGHT <Integer>          {0:1}  [g7:HEIGHT](https://gedcom.io/terms/v7/HEIGHT)
                      5 WIDTH <Integer>           {0:1}  [g7:WIDTH](https://gedcom.io/terms/v7/WIDTH)
                   4 TITL <Text>                  {0:1}  [g7:TITL](https://gedcom.io/terms/v7/TITL)
                3 <<NOTE_STRUCTURE>>              {0:M}  (see above)
          |
          1 SNOTE @<XREF:SNOTE>@                  {1:1}  [g7:SNOTE](https://gedcom.io/terms/v7/SNOTE)
          ]
        <BLANKLINE>

    Reference:
        [The FamilySearch GEDCOM Specifications](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html)
    """

    FAMILY: str = """
0 @XREF:FAM@ FAM                      {1:1}  [g7:record-FAM](https://gedcom.io/terms/v7/record-FAM)
  1 RESN <List:Enum>                  {0:1}  [g7:RESN](https://gedcom.io/terms/v7/RESN)
  1 <<FAMILY_ATTRIBUTE_STRUCTURE>>    {0:M}
  1 <<FAMILY_EVENT_STRUCTURE>>        {0:M}
  1 <<NON_EVENT_STRUCTURE>>           {0:M}
  1 HUSB @<XREF:INDI>@                {0:1}  [g7:FAM-HUSB](https://gedcom.io/terms/v7/FAM-HUSB)
    2 PHRASE <Text>                   {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
  1 WIFE @<XREF:INDI>@                {0:1}  [g7:FAM-WIFE](https://gedcom.io/terms/v7/FAM-WIFE)
    2 PHRASE <Text>                   {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
  1 CHIL @<XREF:INDI>@                {0:M}  [g7:CHIL](https://gedcom.io/terms/v7/CHIL)
    2 PHRASE <Text>                   {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
  1 <<ASSOCIATION_STRUCTURE>>         {0:M}
  1 SUBM @<XREF:SUBM>@                {0:M}  [g7:SUBM](https://gedcom.io/terms/v7/SUBM)
  1 <<LDS_SPOUSE_SEALING>>            {0:M}
  1 <<IDENTIFIER_STRUCTURE>>          {0:M}
  [
  1 REFN <Special>                    {1:1}  [g7:REFN](https://gedcom.io/terms/v7/REFN)
    2 TYPE <Text>                     {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
  |
  1 UID <Special>                     {1:1}  [g7:UID](https://gedcom.io/terms/v7/UID)
  |
  1 EXID <Special>                    {1:1}  [g7:EXID](https://gedcom.io/terms/v7/EXID)
    2 TYPE <Special>                  {0:1}  [g7:EXID-TYPE](https://gedcom.io/terms/v7/EXID-TYPE)
  ]
  1 <<NOTE_STRUCTURE>>                {0:M}
  [
  1 NOTE <Text>                       {1:1}  [g7:NOTE](https://gedcom.io/terms/v7/NOTE)
    2 MIME <MediaType>                {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
    2 LANG <Language>                 {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
    2 TRAN <Text>                     {0:M}  [g7:NOTE-TRAN](https://gedcom.io/terms/v7/NOTE-TRAN)
      3 MIME <MediaType>              {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
      3 LANG <Language>               {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
    2 <<SOURCE_CITATION>>             {0:M}
    2 SOUR @<XREF:SOUR>@              {1:1}  [g7:SOUR](https://gedcom.io/terms/v7/SOUR)
      3 PAGE <Text>                   {0:1}  [g7:PAGE](https://gedcom.io/terms/v7/PAGE)
      3 DATA                          {0:1}  [g7:SOUR-DATA](https://gedcom.io/terms/v7/SOUR-DATA)
        4 <<DATE_VALUE>>              {0:1}
        4 TEXT <Text>                 {0:M}  [g7:TEXT](https://gedcom.io/terms/v7/TEXT)
          5 MIME <MediaType>          {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
          5 LANG <Language>           {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
      3 EVEN <Enum>                   {0:1}  [g7:SOUR-EVEN](https://gedcom.io/terms/v7/SOUR-EVEN)
        4 PHRASE <Text>               {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
        4 ROLE <Enum>                 {0:1}  [g7:ROLE](https://gedcom.io/terms/v7/ROLE)
          5 PHRASE <Text>             {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
      3 QUAY <Enum>                   {0:1}  [g7:QUAY](https://gedcom.io/terms/v7/QUAY)
      3 <<MULTIMEDIA_LINK>>           {0:M}
      3 OBJE @<XREF:OBJE>@            {1:1}  [g7:OBJE](https://gedcom.io/terms/v7/OBJE)
        4 CROP                        {0:1}  [g7:CROP](https://gedcom.io/terms/v7/CROP)
          5 TOP <Integer>             {0:1}  [g7:TOP](https://gedcom.io/terms/v7/TOP)
          5 LEFT <Integer>            {0:1}  [g7:LEFT](https://gedcom.io/terms/v7/LEFT)
          5 HEIGHT <Integer>          {0:1}  [g7:HEIGHT](https://gedcom.io/terms/v7/HEIGHT)
          5 WIDTH <Integer>           {0:1}  [g7:WIDTH](https://gedcom.io/terms/v7/WIDTH)
        4 TITL <Text>                 {0:1}  [g7:TITL](https://gedcom.io/terms/v7/TITL)
      3 <<NOTE_STRUCTURE>>            {0:M}  (see above)
  |
  1 SNOTE @<XREF:SNOTE>@              {1:1}  [g7:SNOTE](https://gedcom.io/terms/v7/SNOTE)
  ]
  1 <<SOURCE_CITATION>>               {0:M}
  1 SOUR @<XREF:SOUR>@              {1:1}  [g7:SOUR](https://gedcom.io/terms/v7/SOUR)
    2 PAGE <Text>                   {0:1}  [g7:PAGE](https://gedcom.io/terms/v7/PAGE)
    2 DATA                          {0:1}  [g7:SOUR-DATA](https://gedcom.io/terms/v7/SOUR-DATA)
      3 <<DATE_VALUE>>              {0:1}
      3 TEXT <Text>                 {0:M}  [g7:TEXT](https://gedcom.io/terms/v7/TEXT)
        4 MIME <MediaType>          {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
        4 LANG <Language>           {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
    2 EVEN <Enum>                   {0:1}  [g7:SOUR-EVEN](https://gedcom.io/terms/v7/SOUR-EVEN)
      3 PHRASE <Text>               {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
      3 ROLE <Enum>                 {0:1}  [g7:ROLE](https://gedcom.io/terms/v7/ROLE)
        4 PHRASE <Text>             {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    2 QUAY <Enum>                   {0:1}  [g7:QUAY](https://gedcom.io/terms/v7/QUAY)
    2 <<MULTIMEDIA_LINK>>           {0:M}
    2 OBJE @<XREF:OBJE>@            {1:1}  [g7:OBJE](https://gedcom.io/terms/v7/OBJE)
      3 CROP                        {0:1}  [g7:CROP](https://gedcom.io/terms/v7/CROP)
        4 TOP <Integer>             {0:1}  [g7:TOP](https://gedcom.io/terms/v7/TOP)
        4 LEFT <Integer>            {0:1}  [g7:LEFT](https://gedcom.io/terms/v7/LEFT)
        4 HEIGHT <Integer>          {0:1}  [g7:HEIGHT](https://gedcom.io/terms/v7/HEIGHT)
        4 WIDTH <Integer>           {0:1}  [g7:WIDTH](https://gedcom.io/terms/v7/WIDTH)
      3 TITL <Text>                 {0:1}  [g7:TITL](https://gedcom.io/terms/v7/TITL)
    2 <<NOTE_STRUCTURE>>            {0:M}  (see above)
  1 <<MULTIMEDIA_LINK>>               {0:M}
  1 OBJE @<XREF:OBJE>@            {1:1}  [g7:OBJE](https://gedcom.io/terms/v7/OBJE)
    2 CROP                        {0:1}  [g7:CROP](https://gedcom.io/terms/v7/CROP)
      3 TOP <Integer>             {0:1}  [g7:TOP](https://gedcom.io/terms/v7/TOP)
      3 LEFT <Integer>            {0:1}  [g7:LEFT](https://gedcom.io/terms/v7/LEFT)
      3 HEIGHT <Integer>          {0:1}  [g7:HEIGHT](https://gedcom.io/terms/v7/HEIGHT)
      3 WIDTH <Integer>           {0:1}  [g7:WIDTH](https://gedcom.io/terms/v7/WIDTH)
    2 TITL <Text>                 {0:1}  [g7:TITL](https://gedcom.io/terms/v7/TITL)
  1 <<CHANGE_DATE>>                   {0:1}
  1 <<CREATION_DATE>>                 {0:1}
"""
    HEADER: str = """
0 HEAD                                {1:1}  [g7:HEAD](https://gedcom.io/terms/v7/HEAD)
  1 GEDC                              {1:1}  [g7:GEDC](https://gedcom.io/terms/v7/GEDC)
    2 VERS <Special>                  {1:1}  [g7:GEDC-VERS](https://gedcom.io/terms/v7/GEDC-VERS)
  1 SCHMA                             {0:1}  [g7:SCHMA](https://gedcom.io/terms/v7/SCHMA)
    2 TAG <Special>                   {0:M}  [g7:TAG](https://gedcom.io/terms/v7/TAG)
  1 SOUR <Special>                    {0:1}  [g7:HEAD-SOUR](https://gedcom.io/terms/v7/HEAD-SOUR)
    2 VERS <Special>                  {0:1}  [g7:VERS](https://gedcom.io/terms/v7/VERS)
    2 NAME <Text>                     {0:1}  [g7:NAME](https://gedcom.io/terms/v7/NAME)
    2 CORP <Text>                     {0:1}  [g7:CORP](https://gedcom.io/terms/v7/CORP)
      3 <<ADDRESS_STRUCTURE>>         {0:1}
      3 ADDR <Special>                {1:1}  [g7:ADDR](https://gedcom.io/terms/v7/ADDR)
        4 ADR1 <Special>              {0:1}  [g7:ADR1](https://gedcom.io/terms/v7/ADR1)
        4 ADR2 <Special>              {0:1}  [g7:ADR2](https://gedcom.io/terms/v7/ADR2)
        4 ADR3 <Special>              {0:1}  [g7:ADR3](https://gedcom.io/terms/v7/ADR3)
        4 CITY <Special>              {0:1}  [g7:CITY](https://gedcom.io/terms/v7/CITY)
        4 STAE <Special>              {0:1}  [g7:STAE](https://gedcom.io/terms/v7/STAE)
        4 POST <Special>              {0:1}  [g7:POST](https://gedcom.io/terms/v7/POST)
        4 CTRY <Special>              {0:1}  [g7:CTRY](https://gedcom.io/terms/v7/CTRY)
      3 PHON <Special>                {0:M}  [g7:PHON](https://gedcom.io/terms/v7/PHON)
      3 EMAIL <Special>               {0:M}  [g7:EMAIL](https://gedcom.io/terms/v7/EMAIL)
      3 FAX <Special>                 {0:M}  [g7:FAX](https://gedcom.io/terms/v7/FAX)
      3 WWW <Special>                 {0:M}  [g7:WWW](https://gedcom.io/terms/v7/WWW)
    2 DATA <Text>                     {0:1}  [g7:HEAD-SOUR-DATA](https://gedcom.io/terms/v7/HEAD-SOUR-DATA)
      3 DATE <DateExact>              {0:1}  [g7:DATE-exact](https://gedcom.io/terms/v7/DATE-exact)
        4 TIME <Time>                 {0:1}  [g7:TIME](https://gedcom.io/terms/v7/TIME)
      3 COPR <Text>                   {0:1}  [g7:COPR](https://gedcom.io/terms/v7/COPR)
  1 DEST <Special>                    {0:1}  [g7:DEST](https://gedcom.io/terms/v7/DEST)
  1 DATE <DateExact>                  {0:1}  [g7:HEAD-DATE](https://gedcom.io/terms/v7/HEAD-DATE)
    2 TIME <Time>                     {0:1}  [g7:TIME](https://gedcom.io/terms/v7/TIME)
  1 SUBM @<XREF:SUBM>@                {0:1}  [g7:SUBM](https://gedcom.io/terms/v7/SUBM)
  1 COPR <Text>                       {0:1}  [g7:COPR](https://gedcom.io/terms/v7/COPR)
  1 LANG <Language>                   {0:1}  [g7:HEAD-LANG](https://gedcom.io/terms/v7/LANG)
  1 PLAC                              {0:1}  [g7:HEAD-PLAC](https://gedcom.io/terms/v7/PLAC)
    2 FORM <List:Text>                {1:1}  [g7:HEAD-PLAC-FORM](https://gedcom.io/terms/v7/PLAC-FORM)
  1 <<NOTE_STRUCTURE>>                {0:1}
  [
  1 NOTE <Text>                       {1:1}  [g7:NOTE](https://gedcom.io/terms/v7/NOTE)
    2 MIME <MediaType>                {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
    2 LANG <Language>                 {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
    2 TRAN <Text>                     {0:M}  [g7:NOTE-TRAN](https://gedcom.io/terms/v7/NOTE-TRAN)
      3 MIME <MediaType>              {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
      3 LANG <Language>               {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
    2 <<SOURCE_CITATION>>             {0:M}
    2 SOUR @<XREF:SOUR>@              {1:1}  [g7:SOUR](https://gedcom.io/terms/v7/SOUR)
      3 PAGE <Text>                   {0:1}  [g7:PAGE](https://gedcom.io/terms/v7/PAGE)
      3 DATA                          {0:1}  [g7:SOUR-DATA](https://gedcom.io/terms/v7/SOUR-DATA)
        4 <<DATE_VALUE>>              {0:1}
        4 TEXT <Text>                 {0:M}  [g7:TEXT](https://gedcom.io/terms/v7/TEXT)
          5 MIME <MediaType>          {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
          5 LANG <Language>           {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
      3 EVEN <Enum>                   {0:1}  [g7:SOUR-EVEN](https://gedcom.io/terms/v7/SOUR-EVEN)
        4 PHRASE <Text>               {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
        4 ROLE <Enum>                 {0:1}  [g7:ROLE](https://gedcom.io/terms/v7/ROLE)
          5 PHRASE <Text>             {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
      3 QUAY <Enum>                   {0:1}  [g7:QUAY](https://gedcom.io/terms/v7/QUAY)
      3 <<MULTIMEDIA_LINK>>           {0:M}
      3 OBJE @<XREF:OBJE>@            {1:1}  [g7:OBJE](https://gedcom.io/terms/v7/OBJE)
        4 CROP                        {0:1}  [g7:CROP](https://gedcom.io/terms/v7/CROP)
          5 TOP <Integer>             {0:1}  [g7:TOP](https://gedcom.io/terms/v7/TOP)
          5 LEFT <Integer>            {0:1}  [g7:LEFT](https://gedcom.io/terms/v7/LEFT)
          5 HEIGHT <Integer>          {0:1}  [g7:HEIGHT](https://gedcom.io/terms/v7/HEIGHT)
          5 WIDTH <Integer>           {0:1}  [g7:WIDTH](https://gedcom.io/terms/v7/WIDTH)
        4 TITL <Text>                 {0:1}  [g7:TITL](https://gedcom.io/terms/v7/TITL)
      3 <<NOTE_STRUCTURE>>            {0:M}  (see above)
  |
  1 SNOTE @<XREF:SNOTE>@              {1:1}  [g7:SNOTE](https://gedcom.io/terms/v7/SNOTE)
  ]
    """
    INDIVIDUAL: str = """
0 @XREF:INDI@ INDI                    {1:1}  [g7:record-INDI](https://gedcom.io/terms/v7/record-INDI)
  1 RESN <List:Enum>                  {0:1}  [g7:RESN](https://gedcom.io/terms/v7/RESN)
  1 <<PERSONAL_NAME_STRUCTURE>>       {0:M}
  1 SEX <Enum>                        {0:1}  [g7:SEX](https://gedcom.io/terms/v7/SEX)
  1 <<INDIVIDUAL_ATTRIBUTE_STRUCTURE>>{0:M}
  1 <<INDIVIDUAL_EVENT_STRUCTURE>>    {0:M}
  1 <<NON_EVENT_STRUCTURE>>           {0:M}
  1 <<LDS_INDIVIDUAL_ORDINANCE>>      {0:M}
  1 FAMC @<XREF:FAM>@                 {0:M}  [g7:INDI-FAMC](https://gedcom.io/terms/v7/INDI-FAMC)
    2 PEDI <Enum>                     {0:1}  [g7:PEDI](https://gedcom.io/terms/v7/PEDI)
      3 PHRASE <Text>                 {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    2 STAT <Enum>                     {0:1}  [g7:FAMC-STAT](https://gedcom.io/terms/v7/FAMC-STAT)
      3 PHRASE <Text>                 {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    2 <<NOTE_STRUCTURE>>              {0:M}
  1 FAMS @<XREF:FAM>@                 {0:M}  [g7:FAMS](https://gedcom.io/terms/v7/FAMS)
    2 <<NOTE_STRUCTURE>>              {0:M}
  1 SUBM @<XREF:SUBM>@                {0:M}  [g7:SUBM](https://gedcom.io/terms/v7/SUBM)
  1 <<ASSOCIATION_STRUCTURE>>         {0:M}
  1 ALIA @<XREF:INDI>@                {0:M}  [g7:ALIA](https://gedcom.io/terms/v7/ALIA)
    2 PHRASE <Text>                   {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
  1 ANCI @<XREF:SUBM>@                {0:M}  [g7:ANCI](https://gedcom.io/terms/v7/ANCI)
  1 DESI @<XREF:SUBM>@                {0:M}  [g7:DESI](https://gedcom.io/terms/v7/DESI)
  1 <<IDENTIFIER_STRUCTURE>>          {0:M}
  [
  1 REFN <Special>                    {1:1}  [g7:REFN](https://gedcom.io/terms/v7/REFN)
    2 TYPE <Text>                     {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
  |
  1 UID <Special>                     {1:1}  [g7:UID](https://gedcom.io/terms/v7/UID)
  |
  1 EXID <Special>                    {1:1}  [g7:EXID](https://gedcom.io/terms/v7/EXID)
    2 TYPE <Special>                  {0:1}  [g7:EXID-TYPE](https://gedcom.io/terms/v7/EXID-TYPE)
  ]
  1 <<NOTE_STRUCTURE>>                {0:M}
  [
  1 NOTE <Text>                       {1:1}  [g7:NOTE](https://gedcom.io/terms/v7/NOTE)
    2 MIME <MediaType>                {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
    2 LANG <Language>                 {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
    2 TRAN <Text>                     {0:M}  [g7:NOTE-TRAN](https://gedcom.io/terms/v7/NOTE-TRAN)
      3 MIME <MediaType>              {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
      3 LANG <Language>               {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
    2 <<SOURCE_CITATION>>             {0:M}
    2 SOUR @<XREF:SOUR>@              {1:1}  [g7:SOUR](https://gedcom.io/terms/v7/SOUR)
      3 PAGE <Text>                   {0:1}  [g7:PAGE](https://gedcom.io/terms/v7/PAGE)
      3 DATA                          {0:1}  [g7:SOUR-DATA](https://gedcom.io/terms/v7/SOUR-DATA)
        4 <<DATE_VALUE>>              {0:1}
        4 TEXT <Text>                 {0:M}  [g7:TEXT](https://gedcom.io/terms/v7/TEXT)
          5 MIME <MediaType>          {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
          5 LANG <Language>           {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
      3 EVEN <Enum>                   {0:1}  [g7:SOUR-EVEN](https://gedcom.io/terms/v7/SOUR-EVEN)
        4 PHRASE <Text>               {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
        4 ROLE <Enum>                 {0:1}  [g7:ROLE](https://gedcom.io/terms/v7/ROLE)
          5 PHRASE <Text>             {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
      3 QUAY <Enum>                   {0:1}  [g7:QUAY](https://gedcom.io/terms/v7/QUAY)
      3 <<MULTIMEDIA_LINK>>           {0:M}
      3 OBJE @<XREF:OBJE>@            {1:1}  [g7:OBJE](https://gedcom.io/terms/v7/OBJE)
        4 CROP                        {0:1}  [g7:CROP](https://gedcom.io/terms/v7/CROP)
          5 TOP <Integer>             {0:1}  [g7:TOP](https://gedcom.io/terms/v7/TOP)
          5 LEFT <Integer>            {0:1}  [g7:LEFT](https://gedcom.io/terms/v7/LEFT)
          5 HEIGHT <Integer>          {0:1}  [g7:HEIGHT](https://gedcom.io/terms/v7/HEIGHT)
          5 WIDTH <Integer>           {0:1}  [g7:WIDTH](https://gedcom.io/terms/v7/WIDTH)
        4 TITL <Text>                 {0:1}  [g7:TITL](https://gedcom.io/terms/v7/TITL)
      3 <<NOTE_STRUCTURE>>            {0:M}  (see above)
  |
  1 SNOTE @<XREF:SNOTE>@              {1:1}  [g7:SNOTE](https://gedcom.io/terms/v7/SNOTE)
  ]
  1 <<SOURCE_CITATION>>               {0:M}
  1 SOUR @<XREF:SOUR>@              {1:1}  [g7:SOUR](https://gedcom.io/terms/v7/SOUR)
    2 PAGE <Text>                   {0:1}  [g7:PAGE](https://gedcom.io/terms/v7/PAGE)
    2 DATA                          {0:1}  [g7:SOUR-DATA](https://gedcom.io/terms/v7/SOUR-DATA)
      3 <<DATE_VALUE>>              {0:1}
      3 TEXT <Text>                 {0:M}  [g7:TEXT](https://gedcom.io/terms/v7/TEXT)
        4 MIME <MediaType>          {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
        4 LANG <Language>           {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
    2 EVEN <Enum>                   {0:1}  [g7:SOUR-EVEN](https://gedcom.io/terms/v7/SOUR-EVEN)
      3 PHRASE <Text>               {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
      3 ROLE <Enum>                 {0:1}  [g7:ROLE](https://gedcom.io/terms/v7/ROLE)
        4 PHRASE <Text>             {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    2 QUAY <Enum>                   {0:1}  [g7:QUAY](https://gedcom.io/terms/v7/QUAY)
    2 <<MULTIMEDIA_LINK>>           {0:M}
    2 OBJE @<XREF:OBJE>@            {1:1}  [g7:OBJE](https://gedcom.io/terms/v7/OBJE)
      3 CROP                        {0:1}  [g7:CROP](https://gedcom.io/terms/v7/CROP)
        4 TOP <Integer>             {0:1}  [g7:TOP](https://gedcom.io/terms/v7/TOP)
        4 LEFT <Integer>            {0:1}  [g7:LEFT](https://gedcom.io/terms/v7/LEFT)
        4 HEIGHT <Integer>          {0:1}  [g7:HEIGHT](https://gedcom.io/terms/v7/HEIGHT)
        4 WIDTH <Integer>           {0:1}  [g7:WIDTH](https://gedcom.io/terms/v7/WIDTH)
      3 TITL <Text>                 {0:1}  [g7:TITL](https://gedcom.io/terms/v7/TITL)
    2 <<NOTE_STRUCTURE>>            {0:M}  (see above)
  1 <<MULTIMEDIA_LINK>>               {0:M}
  1 OBJE @<XREF:OBJE>@            {1:1}  [g7:OBJE](https://gedcom.io/terms/v7/OBJE)
    2 CROP                        {0:1}  [g7:CROP](https://gedcom.io/terms/v7/CROP)
      3 TOP <Integer>             {0:1}  [g7:TOP](https://gedcom.io/terms/v7/TOP)
      3 LEFT <Integer>            {0:1}  [g7:LEFT](https://gedcom.io/terms/v7/LEFT)
      3 HEIGHT <Integer>          {0:1}  [g7:HEIGHT](https://gedcom.io/terms/v7/HEIGHT)
      3 WIDTH <Integer>           {0:1}  [g7:WIDTH](https://gedcom.io/terms/v7/WIDTH)
    2 TITL <Text>                 {0:1}  [g7:TITL](https://gedcom.io/terms/v7/TITL)
  1 <<CHANGE_DATE>>                   {0:1}
  1 <<CREATION_DATE>>                 {0:1}
"""
    MULTIMEDIA: str = """
0 @XREF:OBJE@ OBJE                    {1:1}  [g7:record-OBJE](https://gedcom.io/terms/v7/record-OBJE)
  1 RESN <List:Enum>                  {0:1}  [g7:RESN](https://gedcom.io/terms/v7/RESN)
  1 FILE <FilePath>                   {1:M}  [g7:FILE](https://gedcom.io/terms/v7/FILE)
    2 FORM <MediaType>                {1:1}  [g7:FORM](https://gedcom.io/terms/v7/FORM)
      3 MEDI <Enum>                   {0:1}  [g7:MEDI](https://gedcom.io/terms/v7/MEDI)
        4 PHRASE <Text>               {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    2 TITL <Text>                     {0:1}  [g7:TITL](https://gedcom.io/terms/v7/TITL)
    2 TRAN <FilePath>                 {0:M}  [g7:FILE-TRAN](https://gedcom.io/terms/v7/FILE-TRAN)
      3 FORM <MediaType>              {1:1}  [g7:FORM](https://gedcom.io/terms/v7/FORM)
  1 <<IDENTIFIER_STRUCTURE>>          {0:M}
  [
  1 REFN <Special>                    {1:1}  [g7:REFN](https://gedcom.io/terms/v7/REFN)
    2 TYPE <Text>                     {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
  |
  1 UID <Special>                     {1:1}  [g7:UID](https://gedcom.io/terms/v7/UID)
  |
  1 EXID <Special>                    {1:1}  [g7:EXID](https://gedcom.io/terms/v7/EXID)
    2 TYPE <Special>                  {0:1}  [g7:EXID-TYPE](https://gedcom.io/terms/v7/EXID-TYPE)
  ]
  1 <<NOTE_STRUCTURE>>                {0:M}
  [
  1 NOTE <Text>                       {1:1}  [g7:NOTE](https://gedcom.io/terms/v7/NOTE)
    2 MIME <MediaType>                {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
    2 LANG <Language>                 {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
    2 TRAN <Text>                     {0:M}  [g7:NOTE-TRAN](https://gedcom.io/terms/v7/NOTE-TRAN)
      3 MIME <MediaType>              {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
      3 LANG <Language>               {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
    2 <<SOURCE_CITATION>>             {0:M}
    2 SOUR @<XREF:SOUR>@              {1:1}  [g7:SOUR](https://gedcom.io/terms/v7/SOUR)
      3 PAGE <Text>                   {0:1}  [g7:PAGE](https://gedcom.io/terms/v7/PAGE)
      3 DATA                          {0:1}  [g7:SOUR-DATA](https://gedcom.io/terms/v7/SOUR-DATA)
        4 <<DATE_VALUE>>              {0:1}
        4 TEXT <Text>                 {0:M}  [g7:TEXT](https://gedcom.io/terms/v7/TEXT)
          5 MIME <MediaType>          {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
          5 LANG <Language>           {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
      3 EVEN <Enum>                   {0:1}  [g7:SOUR-EVEN](https://gedcom.io/terms/v7/SOUR-EVEN)
        4 PHRASE <Text>               {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
        4 ROLE <Enum>                 {0:1}  [g7:ROLE](https://gedcom.io/terms/v7/ROLE)
          5 PHRASE <Text>             {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
      3 QUAY <Enum>                   {0:1}  [g7:QUAY](https://gedcom.io/terms/v7/QUAY)
      3 <<MULTIMEDIA_LINK>>           {0:M}
      3 OBJE @<XREF:OBJE>@            {1:1}  [g7:OBJE](https://gedcom.io/terms/v7/OBJE)
        4 CROP                        {0:1}  [g7:CROP](https://gedcom.io/terms/v7/CROP)
          5 TOP <Integer>             {0:1}  [g7:TOP](https://gedcom.io/terms/v7/TOP)
          5 LEFT <Integer>            {0:1}  [g7:LEFT](https://gedcom.io/terms/v7/LEFT)
          5 HEIGHT <Integer>          {0:1}  [g7:HEIGHT](https://gedcom.io/terms/v7/HEIGHT)
          5 WIDTH <Integer>           {0:1}  [g7:WIDTH](https://gedcom.io/terms/v7/WIDTH)
        4 TITL <Text>                 {0:1}  [g7:TITL](https://gedcom.io/terms/v7/TITL)
      3 <<NOTE_STRUCTURE>>            {0:M}  (see above)
  |
  1 SNOTE @<XREF:SNOTE>@              {1:1}  [g7:SNOTE](https://gedcom.io/terms/v7/SNOTE)
  ]
  1 <<SOURCE_CITATION>>               {0:M}
  1 SOUR @<XREF:SOUR>@              {1:1}  [g7:SOUR](https://gedcom.io/terms/v7/SOUR)
    2 PAGE <Text>                   {0:1}  [g7:PAGE](https://gedcom.io/terms/v7/PAGE)
    2 DATA                          {0:1}  [g7:SOUR-DATA](https://gedcom.io/terms/v7/SOUR-DATA)
      3 <<DATE_VALUE>>              {0:1}
      3 TEXT <Text>                 {0:M}  [g7:TEXT](https://gedcom.io/terms/v7/TEXT)
        4 MIME <MediaType>          {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
        4 LANG <Language>           {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
    2 EVEN <Enum>                   {0:1}  [g7:SOUR-EVEN](https://gedcom.io/terms/v7/SOUR-EVEN)
      3 PHRASE <Text>               {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
      3 ROLE <Enum>                 {0:1}  [g7:ROLE](https://gedcom.io/terms/v7/ROLE)
        4 PHRASE <Text>             {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    2 QUAY <Enum>                   {0:1}  [g7:QUAY](https://gedcom.io/terms/v7/QUAY)
    2 <<MULTIMEDIA_LINK>>           {0:M}
    2 OBJE @<XREF:OBJE>@            {1:1}  [g7:OBJE](https://gedcom.io/terms/v7/OBJE)
      3 CROP                        {0:1}  [g7:CROP](https://gedcom.io/terms/v7/CROP)
        4 TOP <Integer>             {0:1}  [g7:TOP](https://gedcom.io/terms/v7/TOP)
        4 LEFT <Integer>            {0:1}  [g7:LEFT](https://gedcom.io/terms/v7/LEFT)
        4 HEIGHT <Integer>          {0:1}  [g7:HEIGHT](https://gedcom.io/terms/v7/HEIGHT)
        4 WIDTH <Integer>           {0:1}  [g7:WIDTH](https://gedcom.io/terms/v7/WIDTH)
      3 TITL <Text>                 {0:1}  [g7:TITL](https://gedcom.io/terms/v7/TITL)
    2 <<NOTE_STRUCTURE>>            {0:M}  (see above)
  1 <<CHANGE_DATE>>                   {0:1}
  1 <<CREATION_DATE>>                 {0:1}
"""
    REPOSITORY: str = """
0 @XREF:REPO@ REPO                    {1:1}  [g7:record-REPO](https://gedcom.io/terms/v7/record-REPO)
  1 NAME <Text>                       {1:1}  [g7:NAME](https://gedcom.io/terms/v7/NAME)
  1 <<ADDRESS_STRUCTURE>>             {0:1}
  1 PHON <Special>                    {0:M}  [g7:PHON](https://gedcom.io/terms/v7/PHON)
  1 EMAIL <Special>                   {0:M}  [g7:EMAIL](https://gedcom.io/terms/v7/EMAIL)
  1 FAX <Special>                     {0:M}  [g7:FAX](https://gedcom.io/terms/v7/FAX)
  1 WWW <Special>                     {0:M}  [g7:WWW](https://gedcom.io/terms/v7/WWW)
  1 <<NOTE_STRUCTURE>>                {0:M}
  [
  1 NOTE <Text>                       {1:1}  [g7:NOTE](https://gedcom.io/terms/v7/NOTE)
    2 MIME <MediaType>                {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
    2 LANG <Language>                 {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
    2 TRAN <Text>                     {0:M}  [g7:NOTE-TRAN](https://gedcom.io/terms/v7/NOTE-TRAN)
      3 MIME <MediaType>              {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
      3 LANG <Language>               {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
    2 <<SOURCE_CITATION>>             {0:M}
    2 SOUR @<XREF:SOUR>@              {1:1}  [g7:SOUR](https://gedcom.io/terms/v7/SOUR)
      3 PAGE <Text>                   {0:1}  [g7:PAGE](https://gedcom.io/terms/v7/PAGE)
      3 DATA                          {0:1}  [g7:SOUR-DATA](https://gedcom.io/terms/v7/SOUR-DATA)
        4 <<DATE_VALUE>>              {0:1}
        4 TEXT <Text>                 {0:M}  [g7:TEXT](https://gedcom.io/terms/v7/TEXT)
          5 MIME <MediaType>          {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
          5 LANG <Language>           {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
      3 EVEN <Enum>                   {0:1}  [g7:SOUR-EVEN](https://gedcom.io/terms/v7/SOUR-EVEN)
        4 PHRASE <Text>               {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
        4 ROLE <Enum>                 {0:1}  [g7:ROLE](https://gedcom.io/terms/v7/ROLE)
          5 PHRASE <Text>             {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
      3 QUAY <Enum>                   {0:1}  [g7:QUAY](https://gedcom.io/terms/v7/QUAY)
      3 <<MULTIMEDIA_LINK>>           {0:M}
      3 OBJE @<XREF:OBJE>@            {1:1}  [g7:OBJE](https://gedcom.io/terms/v7/OBJE)
        4 CROP                        {0:1}  [g7:CROP](https://gedcom.io/terms/v7/CROP)
          5 TOP <Integer>             {0:1}  [g7:TOP](https://gedcom.io/terms/v7/TOP)
          5 LEFT <Integer>            {0:1}  [g7:LEFT](https://gedcom.io/terms/v7/LEFT)
          5 HEIGHT <Integer>          {0:1}  [g7:HEIGHT](https://gedcom.io/terms/v7/HEIGHT)
          5 WIDTH <Integer>           {0:1}  [g7:WIDTH](https://gedcom.io/terms/v7/WIDTH)
        4 TITL <Text>                 {0:1}  [g7:TITL](https://gedcom.io/terms/v7/TITL)
      3 <<NOTE_STRUCTURE>>            {0:M}  (see above)
  |
  1 SNOTE @<XREF:SNOTE>@              {1:1}  [g7:SNOTE](https://gedcom.io/terms/v7/SNOTE)
  ]
  1 <<IDENTIFIER_STRUCTURE>>          {0:M}
  [
  1 REFN <Special>                    {1:1}  [g7:REFN](https://gedcom.io/terms/v7/REFN)
    2 TYPE <Text>                     {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
  |
  1 UID <Special>                     {1:1}  [g7:UID](https://gedcom.io/terms/v7/UID)
  |
  1 EXID <Special>                    {1:1}  [g7:EXID](https://gedcom.io/terms/v7/EXID)
    2 TYPE <Special>                  {0:1}  [g7:EXID-TYPE](https://gedcom.io/terms/v7/EXID-TYPE)
  ]
  1 <<CHANGE_DATE>>                   {0:1}
  1 <<CREATION_DATE>>                 {0:1}
"""
    SHARED_NOTE: str = """
0 @XREF:SNOTE@ SNOTE <Text>           {1:1}  [g7:record-SNOTE](https://gedcom.io/terms/v7/record-SNOTE)
  1 MIME <MediaType>                  {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
  1 LANG <Language>                   {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
  1 TRAN <Text>                       {0:M}  [g7:NOTE-TRAN](https://gedcom.io/terms/v7/NOTE-TRAN)
    2 MIME <MediaType>                {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
    2 LANG <Language>                 {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
  1 <<SOURCE_CITATION>>               {0:M}
  1 SOUR @<XREF:SOUR>@              {1:1}  [g7:SOUR](https://gedcom.io/terms/v7/SOUR)
    2 PAGE <Text>                   {0:1}  [g7:PAGE](https://gedcom.io/terms/v7/PAGE)
    2 DATA                          {0:1}  [g7:SOUR-DATA](https://gedcom.io/terms/v7/SOUR-DATA)
      3 <<DATE_VALUE>>              {0:1}
      3 TEXT <Text>                 {0:M}  [g7:TEXT](https://gedcom.io/terms/v7/TEXT)
        4 MIME <MediaType>          {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
        4 LANG <Language>           {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
    2 EVEN <Enum>                   {0:1}  [g7:SOUR-EVEN](https://gedcom.io/terms/v7/SOUR-EVEN)
      3 PHRASE <Text>               {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
      3 ROLE <Enum>                 {0:1}  [g7:ROLE](https://gedcom.io/terms/v7/ROLE)
        4 PHRASE <Text>             {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
    2 QUAY <Enum>                   {0:1}  [g7:QUAY](https://gedcom.io/terms/v7/QUAY)
    2 <<MULTIMEDIA_LINK>>           {0:M}
    2 OBJE @<XREF:OBJE>@            {1:1}  [g7:OBJE](https://gedcom.io/terms/v7/OBJE)
      3 CROP                        {0:1}  [g7:CROP](https://gedcom.io/terms/v7/CROP)
        4 TOP <Integer>             {0:1}  [g7:TOP](https://gedcom.io/terms/v7/TOP)
        4 LEFT <Integer>            {0:1}  [g7:LEFT](https://gedcom.io/terms/v7/LEFT)
        4 HEIGHT <Integer>          {0:1}  [g7:HEIGHT](https://gedcom.io/terms/v7/HEIGHT)
        4 WIDTH <Integer>           {0:1}  [g7:WIDTH](https://gedcom.io/terms/v7/WIDTH)
      3 TITL <Text>                 {0:1}  [g7:TITL](https://gedcom.io/terms/v7/TITL)
    2 <<NOTE_STRUCTURE>>            {0:M}  (see above)
  1 <<IDENTIFIER_STRUCTURE>>          {0:M}
  [
  1 REFN <Special>                    {1:1}  [g7:REFN](https://gedcom.io/terms/v7/REFN)
    2 TYPE <Text>                     {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
  |
  1 UID <Special>                     {1:1}  [g7:UID](https://gedcom.io/terms/v7/UID)
  |
  1 EXID <Special>                    {1:1}  [g7:EXID](https://gedcom.io/terms/v7/EXID)
    2 TYPE <Special>                  {0:1}  [g7:EXID-TYPE](https://gedcom.io/terms/v7/EXID-TYPE)
  ]
  1 <<CHANGE_DATE>>                   {0:1}
  1 <<CREATION_DATE>>                 {0:1}
"""
    SOURCE: str = """
0 @XREF:SOUR@ SOUR                    {1:1}  [g7:record-SOUR](https://gedcom.io/terms/v7/record-SOUR)
  1 DATA                              {0:1}  [g7:DATA](https://gedcom.io/terms/v7/DATA)
    2 EVEN <List:Enum>                {0:M}  [g7:DATA-EVEN](https://gedcom.io/terms/v7/DATA-EVEN)
      3 DATE <DatePeriod>             {0:1}  [g7:DATA-EVEN-DATE](https://gedcom.io/terms/v7/DATA-EVEN-DATE)
        4 PHRASE <Text>               {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
      3 <<PLACE_STRUCTURE>>           {0:1}
    2 AGNC <Text>                     {0:1}  [g7:AGNC](https://gedcom.io/terms/v7/AGNC)
    2 <<NOTE_STRUCTURE>>              {0:M}
  1 AUTH <Text>                       {0:1}  [g7:AUTH](https://gedcom.io/terms/v7/AUTH)
  1 TITL <Text>                       {0:1}  [g7:TITL](https://gedcom.io/terms/v7/TITL)
  1 ABBR <Text>                       {0:1}  [g7:ABBR](https://gedcom.io/terms/v7/ABBR)
  1 PUBL <Text>                       {0:1}  [g7:PUBL](https://gedcom.io/terms/v7/PUBL)
  1 TEXT <Text>                       {0:1}  [g7:TEXT](https://gedcom.io/terms/v7/TEXT)
    2 MIME <MediaType>                {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
    2 LANG <Language>                 {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
  1 <<SOURCE_REPOSITORY_CITATION>>    {0:M}
  1 <<IDENTIFIER_STRUCTURE>>          {0:M}
  [
  1 REFN <Special>                    {1:1}  [g7:REFN](https://gedcom.io/terms/v7/REFN)
    2 TYPE <Text>                     {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
  |
  1 UID <Special>                     {1:1}  [g7:UID](https://gedcom.io/terms/v7/UID)
  |
  1 EXID <Special>                    {1:1}  [g7:EXID](https://gedcom.io/terms/v7/EXID)
    2 TYPE <Special>                  {0:1}  [g7:EXID-TYPE](https://gedcom.io/terms/v7/EXID-TYPE)
  ]
  1 <<NOTE_STRUCTURE>>                {0:M}
  [
  1 NOTE <Text>                       {1:1}  [g7:NOTE](https://gedcom.io/terms/v7/NOTE)
    2 MIME <MediaType>                {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
    2 LANG <Language>                 {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
    2 TRAN <Text>                     {0:M}  [g7:NOTE-TRAN](https://gedcom.io/terms/v7/NOTE-TRAN)
      3 MIME <MediaType>              {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
      3 LANG <Language>               {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
    2 <<SOURCE_CITATION>>             {0:M}
    2 SOUR @<XREF:SOUR>@              {1:1}  [g7:SOUR](https://gedcom.io/terms/v7/SOUR)
      3 PAGE <Text>                   {0:1}  [g7:PAGE](https://gedcom.io/terms/v7/PAGE)
      3 DATA                          {0:1}  [g7:SOUR-DATA](https://gedcom.io/terms/v7/SOUR-DATA)
        4 <<DATE_VALUE>>              {0:1}
        4 TEXT <Text>                 {0:M}  [g7:TEXT](https://gedcom.io/terms/v7/TEXT)
          5 MIME <MediaType>          {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
          5 LANG <Language>           {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
      3 EVEN <Enum>                   {0:1}  [g7:SOUR-EVEN](https://gedcom.io/terms/v7/SOUR-EVEN)
        4 PHRASE <Text>               {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
        4 ROLE <Enum>                 {0:1}  [g7:ROLE](https://gedcom.io/terms/v7/ROLE)
          5 PHRASE <Text>             {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
      3 QUAY <Enum>                   {0:1}  [g7:QUAY](https://gedcom.io/terms/v7/QUAY)
      3 <<MULTIMEDIA_LINK>>           {0:M}
      3 OBJE @<XREF:OBJE>@            {1:1}  [g7:OBJE](https://gedcom.io/terms/v7/OBJE)
        4 CROP                        {0:1}  [g7:CROP](https://gedcom.io/terms/v7/CROP)
          5 TOP <Integer>             {0:1}  [g7:TOP](https://gedcom.io/terms/v7/TOP)
          5 LEFT <Integer>            {0:1}  [g7:LEFT](https://gedcom.io/terms/v7/LEFT)
          5 HEIGHT <Integer>          {0:1}  [g7:HEIGHT](https://gedcom.io/terms/v7/HEIGHT)
          5 WIDTH <Integer>           {0:1}  [g7:WIDTH](https://gedcom.io/terms/v7/WIDTH)
        4 TITL <Text>                 {0:1}  [g7:TITL](https://gedcom.io/terms/v7/TITL)
      3 <<NOTE_STRUCTURE>>            {0:M}  (see above)
  |
  1 SNOTE @<XREF:SNOTE>@              {1:1}  [g7:SNOTE](https://gedcom.io/terms/v7/SNOTE)
  ]
  1 <<MULTIMEDIA_LINK>>               {0:M}
  1 OBJE @<XREF:OBJE>@            {1:1}  [g7:OBJE](https://gedcom.io/terms/v7/OBJE)
    2 CROP                        {0:1}  [g7:CROP](https://gedcom.io/terms/v7/CROP)
      3 TOP <Integer>             {0:1}  [g7:TOP](https://gedcom.io/terms/v7/TOP)
      3 LEFT <Integer>            {0:1}  [g7:LEFT](https://gedcom.io/terms/v7/LEFT)
      3 HEIGHT <Integer>          {0:1}  [g7:HEIGHT](https://gedcom.io/terms/v7/HEIGHT)
      3 WIDTH <Integer>           {0:1}  [g7:WIDTH](https://gedcom.io/terms/v7/WIDTH)
    2 TITL <Text>                 {0:1}  [g7:TITL](https://gedcom.io/terms/v7/TITL)
  1 <<CHANGE_DATE>>                   {0:1}
  1 <<CREATION_DATE>>                 {0:1}
"""
    SUBMITTER: str = """
0 @XREF:SUBM@ SUBM                    {1:1}  [g7:record-SUBM](https://gedcom.io/terms/v7/record-SUBM)
  1 NAME <Text>                       {1:1}  [g7:NAME](https://gedcom.io/terms/v7/NAME)
  1 <<ADDRESS_STRUCTURE>>             {0:1}
  1 PHON <Special>                    {0:M}  [g7:PHON](https://gedcom.io/terms/v7/PHON)
  1 EMAIL <Special>                   {0:M}  [g7:EMAIL](https://gedcom.io/terms/v7/EMAIL)
  1 FAX <Special>                     {0:M}  [g7:FAX](https://gedcom.io/terms/v7/FAX)
  1 WWW <Special>                     {0:M}  [g7:WWW](https://gedcom.io/terms/v7/WWW)
  1 <<MULTIMEDIA_LINK>>               {0:M}
  1 OBJE @<XREF:OBJE>@            {1:1}  [g7:OBJE](https://gedcom.io/terms/v7/OBJE)
    2 CROP                        {0:1}  [g7:CROP](https://gedcom.io/terms/v7/CROP)
      3 TOP <Integer>             {0:1}  [g7:TOP](https://gedcom.io/terms/v7/TOP)
      3 LEFT <Integer>            {0:1}  [g7:LEFT](https://gedcom.io/terms/v7/LEFT)
      3 HEIGHT <Integer>          {0:1}  [g7:HEIGHT](https://gedcom.io/terms/v7/HEIGHT)
      3 WIDTH <Integer>           {0:1}  [g7:WIDTH](https://gedcom.io/terms/v7/WIDTH)
    2 TITL <Text>                 {0:1}  [g7:TITL](https://gedcom.io/terms/v7/TITL)
  1 LANG <Language>                   {0:M}  [g7:SUBM-LANG](https://gedcom.io/terms/v7/SUBM-LANG)
  1 <<IDENTIFIER_STRUCTURE>>          {0:M}
  [
  1 REFN <Special>                    {1:1}  [g7:REFN](https://gedcom.io/terms/v7/REFN)
    2 TYPE <Text>                     {0:1}  [g7:TYPE](https://gedcom.io/terms/v7/TYPE)
  |
  1 UID <Special>                     {1:1}  [g7:UID](https://gedcom.io/terms/v7/UID)
  |
  1 EXID <Special>                    {1:1}  [g7:EXID](https://gedcom.io/terms/v7/EXID)
    2 TYPE <Special>                  {0:1}  [g7:EXID-TYPE](https://gedcom.io/terms/v7/EXID-TYPE)
  ]
  1 <<NOTE_STRUCTURE>>                {0:M}
  [
  1 NOTE <Text>                       {1:1}  [g7:NOTE](https://gedcom.io/terms/v7/NOTE)
    2 MIME <MediaType>                {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
    2 LANG <Language>                 {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
    2 TRAN <Text>                     {0:M}  [g7:NOTE-TRAN](https://gedcom.io/terms/v7/NOTE-TRAN)
      3 MIME <MediaType>              {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
      3 LANG <Language>               {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
    2 <<SOURCE_CITATION>>             {0:M}
    2 SOUR @<XREF:SOUR>@              {1:1}  [g7:SOUR](https://gedcom.io/terms/v7/SOUR)
      3 PAGE <Text>                   {0:1}  [g7:PAGE](https://gedcom.io/terms/v7/PAGE)
      3 DATA                          {0:1}  [g7:SOUR-DATA](https://gedcom.io/terms/v7/SOUR-DATA)
        4 <<DATE_VALUE>>              {0:1}
        4 TEXT <Text>                 {0:M}  [g7:TEXT](https://gedcom.io/terms/v7/TEXT)
          5 MIME <MediaType>          {0:1}  [g7:MIME](https://gedcom.io/terms/v7/MIME)
          5 LANG <Language>           {0:1}  [g7:LANG](https://gedcom.io/terms/v7/LANG)
      3 EVEN <Enum>                   {0:1}  [g7:SOUR-EVEN](https://gedcom.io/terms/v7/SOUR-EVEN)
        4 PHRASE <Text>               {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
        4 ROLE <Enum>                 {0:1}  [g7:ROLE](https://gedcom.io/terms/v7/ROLE)
          5 PHRASE <Text>             {0:1}  [g7:PHRASE](https://gedcom.io/terms/v7/PHRASE)
      3 QUAY <Enum>                   {0:1}  [g7:QUAY](https://gedcom.io/terms/v7/QUAY)
      3 <<MULTIMEDIA_LINK>>           {0:M}
      3 OBJE @<XREF:OBJE>@            {1:1}  [g7:OBJE](https://gedcom.io/terms/v7/OBJE)
        4 CROP                        {0:1}  [g7:CROP](https://gedcom.io/terms/v7/CROP)
          5 TOP <Integer>             {0:1}  [g7:TOP](https://gedcom.io/terms/v7/TOP)
          5 LEFT <Integer>            {0:1}  [g7:LEFT](https://gedcom.io/terms/v7/LEFT)
          5 HEIGHT <Integer>          {0:1}  [g7:HEIGHT](https://gedcom.io/terms/v7/HEIGHT)
          5 WIDTH <Integer>           {0:1}  [g7:WIDTH](https://gedcom.io/terms/v7/WIDTH)
        4 TITL <Text>                 {0:1}  [g7:TITL](https://gedcom.io/terms/v7/TITL)
      3 <<NOTE_STRUCTURE>>            {0:M}  (see above)
  |
  1 SNOTE @<XREF:SNOTE>@              {1:1}  [g7:SNOTE](https://gedcom.io/terms/v7/SNOTE)
  ]
  1 <<CHANGE_DATE>>                   {0:1}
  1 <<CREATION_DATE>>                 {0:1}
"""


@dataclass(frozen=True)
class Specs:
    ADDRESS: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#ADDRESS_STRUCTURE'
    AGE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#age'
    ALIAS: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#ALIA'
    )
    ASSOCIATION: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#ASSOCIATION_STRUCTURE'
    CHANGE_DATE: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#CHANGE_DATE'
    )
    CHILD: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#CHIL'
    )
    CREATION_DATE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#CREATION_DATE'
    DATE: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#date'
    )
    DATE_VALUE: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#DATE_VALUE'
    )
    EVENT_DETAIL: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#EVENT_DETAIL'
    EXID: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#EXID'
    )
    EXTENSION: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#extensions'
    )
    FAMILY: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_RECORD'
    FAMILY_ATTRIBUTE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_ATTRIBUTE_STRUCTURE'
    FAMILY_CHILD: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMC'
    )
    FAMILY_EVENT: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_EVENT_STRUCTURE'
    FAMILY_EVENT_DETAIL: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_EVENT_DETAIL'
    FAMILY_SPOUSE: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMS'
    )
    FILE: str = ''
    FILE_TRANSLATION: str = ''
    FRENCH_R: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FRENCH_R'
    )
    GREGORIAN: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#GREGORIAN'
    )
    HEADER: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#HEADER'
    )
    HEBREW: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#HEBREW'
    )
    HUSBAND: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#HUSB'
    )
    IDENTIFIER: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#IDENTIFIER_STRUCTURE'
    INDIVIDUAL: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_RECORD'
    INDIVIDUAL_ATTRIBUTE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_ATTRIBUTE_STRUCTURE'
    INDIVIDUAL_EVENT: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_EVENT_STRUCTURE'
    INDIVIDUAL_EVENT_DETAIL: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_EVENT_DETAIL'
    JULIAN: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#JULIAN'
    )
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
    SCHEMA: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SCHMA'
    )
    SHARED_NOTE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SHARED_NOTE_RECORD'
    SOURCE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_RECORD'
    SOURCE_EVENT: str = ''
    SOURCE_CITATION: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_CITATION'
    SOURCE_REPOSITORY_CITATION: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_REPOSITORY_CITATION'
    SUBMITTER: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SUBMITTER_RECORD'
    TIME: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#time'
    )
    WIFE: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#WIFE'
    )


class Tag(Enum):
    """Enumerate all of the standard tags signalling structure types in the GEDCOM specification."""

    ABBR = 'ABBR'
    ADDR = 'ADDR'
    ADOP = 'ADOP'
    ADR1 = 'ADR1'
    ADR2 = 'ADR2'
    ADR3 = 'ADR3'
    AGE = 'AGE'
    AGNC = 'AGNC'
    ALIA = 'ALIA'
    ANCI = 'ANCI'
    ANUL = 'ANUL'
    ASSO = 'ASSO'
    AUTH = 'AUTH'
    BAPL = 'BAPL'
    BAPM = 'BAPM'
    BARM = 'BARM'
    BASM = 'BASM'
    BIRT = 'BIRT'
    BLES = 'BLES'
    BURI = 'BURI'
    CALN = 'CALN'
    CAST = 'CAST'
    CAUS = 'CAUS'
    CENS = 'CENS'
    CHAN = 'CHAN'
    CHIL = 'CHIL'
    CHR = 'CHR'
    CHRA = 'CHRA'
    CITY = 'CITY'
    CONF = 'CONF'
    CONL = 'CONL'
    CONT = 'CONT'
    COPR = 'COPR'
    CORP = 'CORP'
    CREA = 'CREA'
    CREM = 'CREM'
    CROP = 'CROP'
    CTRY = 'CTRY'
    DATA = 'DATA'
    DATE = 'DATE'
    DEAT = 'DEAT'
    DESI = 'DESI'
    DEST = 'DEST'
    DIV = 'DIV'
    DIVF = 'DIVF'
    DSCR = 'DSCR'
    EDUC = 'EDUC'
    EMAIL = 'EMAIL'
    EMIG = 'EMIG'
    ENDL = 'ENDL'
    ENGA = 'ENGA'
    EVEN = 'EVEN'
    EXID = 'EXID'
    FACT = 'FACT'
    FAM = 'FAM'
    FATH = 'FATH'
    FAMC = 'FAMC'
    FAMS = 'FAMS'
    FAX = 'FAX'
    FCOM = 'FCOM'
    FILE = 'FILE'
    FILM = 'FILM'
    FORM = 'FORM'
    FRENCH_R = 'FRENCH_R'
    GEDC = 'GEDC'
    GIVN = 'GIVN'
    GRAD = 'GRAD'
    GREGORIAN = 'GREGORIAN'
    HEAD = 'HEAD'
    HEBREW = 'HEBREW'
    HEIGHT = 'HEIGHT'
    HUSB = 'HUSB'
    IDNO = 'IDNO'
    IMMI = 'IMMI'
    INDI = 'INDI'
    INIL = 'INIL'
    JULIAN = 'JULIAN'
    LANG = 'LANG'
    LANG_ = '_LANG'
    LATI = 'LATI'
    LEFT = 'LEFT'
    LONG = 'LONG'
    MAP = 'MAP'
    MARB = 'MARB'
    MARC = 'MARC'
    MARL = 'MARL'
    MARR = 'MARR'
    MARS = 'MARS'
    MEDI = 'MEDI'
    MIME = 'MIME'
    NAME = 'NAME'
    NATI = 'NATI'
    NATU = 'NATU'
    NCHI = 'NCHI'
    NICK = 'NICK'
    NMR = 'NMR'
    NO = 'NO'
    NOTE = 'NOTE'
    NPFX = 'NPFX'
    NSFX = 'NSFX'
    OBJE = 'OBJE'
    OCCU = 'OCCU'
    ORDN = 'ORDN'
    PAGE = 'PAGE'
    PEDI = 'PEDI'
    PHON = 'PHON'
    PHRASE = 'PHRASE'
    PLAC = 'PLAC'
    POST = 'POST'
    PROB = 'PROB'
    PROP = 'PROP'
    PUBL = 'PUBL'
    QUAY = 'QUAY'
    REFN = 'REFN'
    RELI = 'RELI'
    REPO = 'REPO'
    RESI = 'RESI'
    RESN = 'RESN'
    RETI = 'RETI'
    ROLE = 'ROLE'
    SCHMA = 'SCHMA'
    SDATE = 'SDATE'
    SEX = 'SEX'
    SLGC = 'SLGC'
    SLGS = 'SLGS'
    SNOTE = 'SNOTE'
    SOUR = 'SOUR'
    SPFX = 'SPFX'
    SPOU = 'SPOU'
    SSN = 'SSN'
    STAE = 'STAE'
    STAT = 'STAT'
    SUBM = 'SUBM'
    SURN = 'SURN'
    TAG = 'TAG'
    TEMP = 'TEMP'
    TEXT = 'TEXT'
    TIME = 'TIME'
    TITL = 'TITL'
    TOP = 'TOP'
    TRAN = 'TRAN'
    TRLR = 'TRLR'
    TYPE = 'TYPE'
    UID = 'UID'
    VERS = 'VERS'
    WIDTH = 'WIDTH'
    WIFE = 'WIFE'
    WILL = 'WILL'
    WWW = 'WWW'
    NONE = ''


class FamAttr(Enum):
    """Tags used for family attributes.

    This is a sub-enumeration of the Tag enumeration class.

    Reference:
        [GEDCOM INDIEVEN]()
    """

    NCHI = Tag.NCHI.value
    RESI = Tag.RESI.value
    FACT = Tag.FACT.value
    NONE = Tag.NONE.value


class FamEven(Enum):
    """Tags used for family events.

    This is a sub-enumeration of the Tag enumeration class.

    Reference:
        [GEDCOM FAMC-EVEN](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#family-events)
    """

    ANUL = Tag.ANUL.value
    CENS = Tag.CENS.value
    DIV = Tag.DIV.value
    DIVF = Tag.DIVF.value
    ENGA = Tag.ENGA.value
    MARB = Tag.MARB.value
    MARC = Tag.MARC.value
    MARL = Tag.MARL.value
    MARR = Tag.MARR.value
    MARS = Tag.MARS.value
    EVEN = Tag.EVEN.value
    NONE = Tag.NONE.value


class Id(Enum):
    """Tags used for identifier values.

    This is a sub-enumeration of the Tag enumeration class.

    Reference:
        [GEDCOM Identifiers]()
    """

    REFN = Tag.REFN.value
    UID = Tag.UID.value
    EXID = Tag.EXID.value
    NONE = Tag.NONE.value


class IndiAttr(Enum):
    """Tags used for individual attributes.

    This is a sub-enumeration of the Tag enumeration class.

    Reference:
        [GEDCOM INDIEVEN]()
    """

    CAST = Tag.CAST.value
    DSCR = Tag.DSCR.value
    EDUC = Tag.EDUC.value
    IDNO = Tag.IDNO.value
    NATI = Tag.NATI.value
    NCHI = Tag.NCHI.value
    NMR = Tag.NMR.value
    OCCU = Tag.OCCU.value
    PROP = Tag.PROP.value
    RELI = Tag.RELI.value
    RESI = Tag.RESI.value
    SSN = Tag.SSN.value
    TITL = Tag.TITL.value
    FACT = Tag.FACT.value
    NONE = Tag.NONE.value


class IndiEven(Enum):
    """Tags used for individual events.

    This is a sub-enumeration of the Tag enumeration class.

    Reference:
        [GEDCOM INDIEVEN]()
    """

    ADOP = Tag.ADOP.value
    BAPM = Tag.BAPM.value
    BARM = Tag.BARM.value
    BASM = Tag.BASM.value
    BIRT = Tag.BIRT.value
    BLES = Tag.BLES.value
    BURI = Tag.BURI.value
    CENS = Tag.CENS.value
    CHR = Tag.CHR.value
    CHRA = Tag.CHRA.value
    CONF = Tag.CONF.value
    CREM = Tag.CREM.value
    DEAT = Tag.DEAT.value
    EMIG = Tag.EMIG.value
    FCOM = Tag.FCOM.value
    GRAD = Tag.GRAD.value
    IMMI = Tag.IMMI.value
    NATU = Tag.NATU.value
    ORDN = Tag.ORDN.value
    PROB = Tag.PROB.value
    RETI = Tag.RETI.value
    WILL = Tag.WILL.value
    EVEN = Tag.EVEN.value
    NONE = Tag.NONE.value


class PersonalNamePieceTag(Enum):
    """Tags used for Personal Name Piece lines.

    This is a subenumeration of the Tag enumeration class.

    Reference:
        [GEDCOM]()
    """

    NPFX = Tag.NPFX.value
    GIVN = Tag.GIVN.value
    NICK = Tag.NICK.value
    SPFX = Tag.SPFX.value
    SURN = Tag.SURN.value
    NSFX = Tag.NSFX.value
    NONE = Tag.NONE.value


class Record(str, Enum):
    """Tags used for Records.

    This is a subenumeration of the Tag enumeration class.

    Reference:
        [GEDCOM RECORD]()
    """

    FAM = Tag.FAM.value
    INDI = Tag.INDI.value
    OBJE = Tag.OBJE.value
    REPO = Tag.REPO.value
    SNOTE = Tag.SNOTE.value
    SOUR = Tag.SOUR.value
    SUBM = Tag.SUBM.value
    NONE = Tag.NONE.value


class LineVal(Enum):
    """Fixed values that may be used in the LineVal position of a line.

    Some of these values may be identical to Tag values, but in this implementation
    they are separate from Tag.  For example, even though there is a Tag.HUSB
    definition that may be used in the Tag position of a GEDCOM line there is
    also a LineVal.HUSB definition that may only be used in the LineVal of a
    GEDCOM line.

    Reference:
        [GEDCOM LineVal Definitions]()
    """

    ADOPTED = 'ADOPTED'
    AKA = 'AKA'
    AUDIO = 'AUDIO'
    BIC = 'BIC'
    BIRTH = 'BIRTH'
    BOOK = 'BOOK'
    BOTH = 'BOTH'
    CANCELED = 'CANCELED'
    CARD = 'CARD'
    CHALLENGED = 'CHALLENGED'
    CHIL = 'CHIL'
    CHILD = 'CHILD'
    CLERGY = 'CLERGY'
    COMPLETED = 'COMPLETED'
    CONFIDENTIAL = 'CONFIDENTIAL'
    DISPROVEN = 'DISPROVEN'
    DNS = 'DNS'
    DNS_CAN = 'DNS_CAN'
    ELECTRONIC = 'ELECTRONIC'
    EXCLUDED = 'EXCLUDED'
    F = 'F'
    FATH = 'FATH'
    FICHE = 'FICHE'
    FILM = 'FILM'
    FOSTER = 'FOSTER'
    FRIEND = 'FRIEND'
    GODP = 'GODP'
    HUSB = 'HUSB'
    IMMIGRANT = 'IMMIGRANT'
    INFANT = 'INFANT'
    LOCKED = 'LOCKED'
    MAGAZINE = 'MAGAZINE'
    MAIDEN = 'MAIDEN'
    MANUSCRIPT = 'MANUSCRIPT'
    M = 'M'
    MAP = 'MAP'
    MARRIED = 'MARRIED'
    MOTH = 'MOTH'
    MULTIPLE = 'MULTIPLE'
    NEWSPAPER = 'NEWSPAPER'
    NGHBR = 'NGHBR'
    NONE = ''
    OFFICIATOR = 'OFFICIATOR'
    OTHER = 'OTHER'
    PARENT = 'PARENT'
    PHOTO = 'PHOTO'
    PRE_1970 = 'PRE_1970'
    PRIVACY = 'PRIVACY'
    PROFESSIONAL = 'PROFESSIONAL'
    PROVEN = 'PROVEN'
    QUAY0 = '0'
    QUAY1 = '1'
    QUAY2 = '2'
    QUAY3 = '3'
    SEALING = 'SEALING'
    SPOU = 'SPOU'
    STILLBORN = 'STILLBORN'
    SUBMITTED = 'SUBMITTED'
    TOMBSTONE = 'TOMBSTONE'
    U = 'U'
    UNCLEARED = 'UNCLEARED'
    VIDEO = 'VIDEO'
    WIFE = 'WIFE'
    WITN = 'WITN'
    X = 'X'


class Adop(Enum):
    """Implement the GEDCOM enumeration set ADOP as an enumeration class.

    Reference:
        - [GEDCOM Adop Enumeration](https://gedcom.io/terms/v7/enumset-ADOP)
    """

    HUSB = LineVal.HUSB.value
    WIFE = LineVal.WIFE.value
    BOTH = LineVal.BOTH.value
    NONE = LineVal.NONE.value


class EvenAttr(Enum):
    """Implement the GEDCOM enumeration set EVENATTR as an enumeration class.

    Reference:
        [GEDCOM EVENATTR enumeration set](https://gedcom.io/terms/v7/enumset-EVENATTR)
    """

    CENS = Tag.CENS.value
    NCHI = Tag.NCHI.value
    RESI = Tag.RESI.value
    FACT = Tag.FACT.value
    EVEN = Tag.EVEN.value
    NONE = Tag.NONE.value


class FamcStat(Enum):
    """Implement the GEDCOM enumeration set FAMC-STAT as an enumeration class.

    Reference:
        [GEDCOM FAMC-STAT](https://gedcom.io/terms/v7/enumset-FAMC-STAT)
    """

    CHALLENGED = LineVal.CHALLENGED.value
    DISPROVEN = LineVal.DISPROVEN.value
    PROVEN = LineVal.PROVEN.value
    NONE = LineVal.NONE.value


class Medium(Enum):
    """Implement the GEDCOM enumeration set MEDI as an enumeration class.

    Reference:
        [GEDCOM MEDI enumeration set](https://gedcom.io/terms/v7/enumset-MEDI)
    """

    AUDIO = LineVal.AUDIO.value
    BOOK = LineVal.BOOK.value
    CARD = LineVal.CARD.value
    ELECTRONIC = LineVal.ELECTRONIC.value
    FICHE = LineVal.FICHE.value
    FILM = LineVal.FILM.value
    MAGAZINE = LineVal.MAGAZINE.value
    MANUSCRIPT = LineVal.MANUSCRIPT.value
    MAP = LineVal.MAP.value
    NEWSPAPER = LineVal.NEWSPAPER.value
    PHOTO = LineVal.PHOTO.value
    TOMBSTONE = LineVal.TOMBSTONE.value
    VIDEO = LineVal.VIDEO.value
    OTHER = LineVal.OTHER.value
    NONE = LineVal.NONE.value


class NameType(Enum):
    """Implement the GEDCOM enumeration set NAME-TYPE as an eneration class.

    Reference:
        [GEDCOM NAME-TYPE enumeration set](https://gedcom.io/terms/v7/enumset-NAME-TYPE)
    """

    AKA = LineVal.AKA.value
    BIRTH = LineVal.BIRTH.value
    IMMIGRANT = LineVal.IMMIGRANT.value
    MAIDEN = LineVal.MAIDEN.value
    MARRIED = LineVal.MARRIED.value
    PROFESSIONAL = LineVal.PROFESSIONAL.value
    OTHER = LineVal.OTHER.value
    NONE = LineVal.NONE.value


class Pedi(Enum):
    """Implement the GEDCOM enumeration set PEDI as an enumeration class.

    Reference:
        [GEDCOM PEDI enumeration set](https://gedcom.io/terms/v7/enumset-PEDI)
    """

    ADOPTED = LineVal.ADOPTED.value
    BIRTH = LineVal.BIRTH.value
    FOSTER = LineVal.FOSTER.value
    SEALING = LineVal.SEALING.value
    OTHER = LineVal.OTHER.value
    NONE = LineVal.NONE.value


class Quay(Enum):
    """Implement the GEDCOM enumeration set QUAY as an enumeration class.

    Reference:
        [GEDCOM QUAY enumeration set](https://gedcom.io/terms/v7/enumset-QUAY)
    """

    QUAY0 = LineVal.QUAY0.value
    QUAY1 = LineVal.QUAY1.value
    QUAY2 = LineVal.QUAY2.value
    QUAY3 = LineVal.QUAY3.value
    NONE = LineVal.NONE.value


class Resn(Enum):
    """Implement the GEDCOM enumeration set RESN as an enumeration class.

    Reference:
        [GEDCOM RESN enumeration set](https://gedcom.io/terms/v7/enumset-RESN)
    """

    CONFIDENTIAL = LineVal.CONFIDENTIAL.value
    LOCKED = LineVal.LOCKED.value
    PRIVACY = LineVal.PRIVACY.value
    NONE = LineVal.NONE.value


class Role(Enum):
    """Implement the GEDCOM enumeration set ROLE as an enumeration class.

    Reference:
        [GEDCOM ROLE enumeration set](https://gedcom.io/terms/v7/enumset-ROLE)
    """

    CHIL = LineVal.CHIL.value
    CLERGY = LineVal.CLERGY.value
    FATH = LineVal.FATH.value
    FRIEND = LineVal.FRIEND.value
    GODP = LineVal.GODP.value
    HUSB = LineVal.HUSB.value
    MOTH = LineVal.MOTH.value
    MULTIPLE = LineVal.MULTIPLE.value
    NGHBR = LineVal.NGHBR.value
    OFFICIATOR = LineVal.OFFICIATOR.value
    PARENT = LineVal.PARENT.value
    SPOU = LineVal.SPOU.value
    WIFE = LineVal.WIFE.value
    WITN = LineVal.WITN.value
    OTHER = LineVal.OTHER.value
    NONE = LineVal.NONE.value


class Sex(Enum):
    """Implement the GEDCOM SEX enumeration set as an enumeration class.

    Reference:
        [GEDCOM SEX enumeration set]()
    """

    M = LineVal.M.value
    F = LineVal.F.value
    X = LineVal.X.value
    U = LineVal.U.value
    NONE = LineVal.NONE.value


class Stat(Enum):
    """Implement the GEDCOM enumeration set ord-STAT as an enumeration class.

    Reference:
        [GEDCOM ord-STAT enumeration set](https://gedcom.io/terms/v7/enumset-ord-STAT)
    """

    BIC = LineVal.BIC.value
    CANCELED = LineVal.CANCELED.value
    CHILD = LineVal.CHILD.value
    COMPLETED = LineVal.COMPLETED.value
    EXCLUDED = LineVal.EXCLUDED.value
    DNS = LineVal.DNS.value
    DNS_CAN = LineVal.DNS_CAN.value
    INFANT = LineVal.INFANT.value
    PRE_1970 = LineVal.PRE_1970.value
    STILLBORN = LineVal.STILLBORN.value
    SUBMITTED = LineVal.SUBMITTED.value
    UNCLEARED = LineVal.UNCLEARED.value
    NONE = LineVal.NONE.value
