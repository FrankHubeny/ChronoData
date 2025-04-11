# examples.py
"""Store examples for doctest and user help in the generated classes moduele.
"""

__all__ = [
    'Examples',
]


from genedata.constants import Config, Default

Examples: dict[str, str] = {
    'ASSO': f"""

    Examples:
        This example illustrates how one may construct the example in the
        specification. First create two individual cross reference identifiers.
        The add the data to a RecordIndi class for the first individual.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> from genedata.build import Genealogy
        >>> from genedata.structure import Void
        >>> {Default.CODE_GENEALOGY} = Genealogy('example')
        >>> indi1 = {Default.CODE_GENEALOGY}.individual_xref('I1')
        >>> indi2 = {Default.CODE_GENEALOGY}.individual_xref('I2')
        >>> indi = {Default.CODE_CLASS}.RecordIndi(indi1,
        ...     [
        ...         {Default.CODE_CLASS}.Asso(Void.INDI, 
        ...             [
        ...                 {Default.CODE_CLASS}.Phrase('Mr Stockdale'),
        ...                 {Default.CODE_CLASS}.Role('OTHER', {Default.CODE_CLASS}.Phrase('Teacher')),
        ...             ]
        ...         ),
        ...         {Default.CODE_CLASS}.Bapm('',
        ...             [
        ...                 {Default.CODE_CLASS}.Date('1930'),
        ...                 {Default.CODE_CLASS}.Asso(indi2, {Default.CODE_CLASS}.Role('CLERGY')),
        ...             ]
        ...         ),
        ...     ]
        ... )
        >>> print(indi.ged())
        0 @I1@ INDI
        1 ASSO @VOID@
        2 PHRASE Mr Stockdale
        2 ROLE OTHER
        3 PHRASE Teacher
        1 BAPM
        2 DATE 1930
        2 ASSO @I2@
        3 ROLE CLERGY
        <BLANKLINE>""",
    'FILE-TRAN': f"""

    Examples:
        The following example shows how to construct the example in the specification.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> from genedata.build import Genealogy
        >>> {Default.CODE_GENEALOGY} = Genealogy('example')
        >>> obje_xref = {Default.CODE_GENEALOGY}.multimedia_xref('EX')
        >>> obje = {Default.CODE_CLASS}.RecordObje(obje_xref,
        ...     [
        ...         {Default.CODE_CLASS}.File('media/original.mp3',
        ...             [
        ...                 {Default.CODE_CLASS}.Form('audio/mp3'),
        ...                 {Default.CODE_CLASS}.FileTran('media/derived.oga', {Default.CODE_CLASS}.Form('audio/ogg')),
        ...                 {Default.CODE_CLASS}.FileTran('media/transcript.vtt', {Default.CODE_CLASS}.Form('text/vtt')),
        ...             ]
        ...         ),
        ...     ]
        ... )
        >>> print(obje.ged())
        0 @EX@ OBJE
        1 FILE media/original.mp3
        2 FORM audio/mp3
        2 TRAN media/derived.oga
        3 FORM audio/ogg
        2 TRAN media/transcript.vtt
        3 FORM text/vtt
        <BLANKLINE>""",
    'HEAD': f"""

    Example:
        The following is the header structure.
        [HEADER](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#HEADER)
        n HEAD                                     {{1:1}}  g7:HEAD
          +1 GEDC                                  {{1:1}}  g7:GEDC
             +2 VERS <Special>                     {{1:1}}  g7:GEDC-VERS
          +1 SCHMA                                 {{0:1}}  g7:SCHMA
             +2 TAG <Special>                      {{0:M}}  g7:TAG
          +1 SOUR <Special>                        {{0:1}}  g7:HEAD-SOUR
             +2 VERS <Special>                     {{0:1}}  g7:VERS
             +2 NAME <Text>                        {{0:1}}  g7:NAME
             +2 CORP <Text>                        {{0:1}}  g7:CORP
                +3 <<ADDRESS_STRUCTURE>>           {{0:1}}
                +3 PHON <Special>                  {{0:M}}  g7:PHON
                +3 EMAIL <Special>                 {{0:M}}  g7:EMAIL
                +3 FAX <Special>                   {{0:M}}  g7:FAX
                +3 WWW <Special>                   {{0:M}}  g7:WWW
             +2 DATA <Text>                        {{0:1}}  g7:HEAD-SOUR-DATA
                +3 DATE <DateExact>                {{0:1}}  g7:DATE-exact
                   +4 TIME <Time>                  {{0:1}}  g7:TIME
                +3 COPR <Text>                     {{0:1}}  g7:COPR
          +1 DEST <Special>                        {{0:1}}  g7:DEST
          +1 DATE <DateExact>                      {{0:1}}  g7:HEAD-DATE
             +2 TIME <Time>                        {{0:1}}  g7:TIME
          +1 SUBM @<XREF:SUBM>@                    {{0:1}}  g7:SUBM
          +1 COPR <Text>                           {{0:1}}  g7:COPR
          +1 LANG <Language>                       {{0:1}}  g7:HEAD-LANG
          +1 PLAC                                  {{0:1}}  g7:HEAD-PLAC
             +2 FORM <List:Text>                   {{1:1}}  g7:HEAD-PLAC-FORM
          +1 <<NOTE_STRUCTURE>>                    {{0:1}}
        It can be implemented as follows using data from the 
        [GEDCOM Maximal70 Test File]
        First, import the required classes.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> from genedata.build import Genealogy

        Second, instantiate a Genealogy along with any cross reference identifiers
        that will be needed.  In this case, we need a source and a submitter xref.
        >>> {Default.CODE_GENEALOGY} = Genealogy('header test')
        >>> subm_xref = {Default.CODE_GENEALOGY}.submitter_xref('U1')
        >>> sour_xref = {Default.CODE_GENEALOGY}.source_xref('S1')

        Third, construct the header record.
        >>> head = {Default.CODE_CLASS}.Head([
        ...     {Default.CODE_CLASS}.Gedc({Default.CODE_CLASS}.GedcVers('7.0')),
        ...     {Default.CODE_CLASS}.Note('This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.',[
        ...         {Default.CODE_CLASS}.Mime('text/plain'),
        ...         {Default.CODE_CLASS}.Lang('en-US'),
        ...         {Default.CODE_CLASS}.NoteTran('Diese Datei soll Teile der Spezifikation abdecken und enthält keine aussagekräftigen historischen oder genealogischen Daten.', gc.Lang('de')),
        ...         {Default.CODE_CLASS}.Sour(sour_xref, {Default.CODE_CLASS}.Page('1')),
        ...         {Default.CODE_CLASS}.Sour(sour_xref, {Default.CODE_CLASS}.Page('2')),
        ...     ]),
        ...     {Default.CODE_CLASS}.Schma([
        ...         {Default.CODE_CLASS}.Tag('_SKYPEID http://xmlns.com/foaf/0.1/skypeID'),
        ...         {Default.CODE_CLASS}.Tag('_JABBERID http://xmlns.com/foaf/0.1/jabberID'),
        ...     ]),
        ...     {Default.CODE_CLASS}.HeadSour('https://gedcom.io/',[
        ...         {Default.CODE_CLASS}.Vers('0.4'),
        ...         {Default.CODE_CLASS}.Name('GEDCOM Steering Committee'),
        ...         {Default.CODE_CLASS}.Corp('FamilySearch',[
        ...             {Default.CODE_CLASS}.Addr('Family History Department\\\\n15 East South Temple Street\\\\nSalt Lake City, UT 84150 USA',[
        ...                 {Default.CODE_CLASS}.Adr1('Family History Department'),
        ...                 {Default.CODE_CLASS}.Adr2('15 East South Temple Street'),
        ...                 {Default.CODE_CLASS}.Adr3('Salt Lake City, UT 84150 USA'),
        ...                 {Default.CODE_CLASS}.City('Salt Lake City'),
        ...                 {Default.CODE_CLASS}.Stae('UT'),
        ...                 {Default.CODE_CLASS}.Post('84150'),
        ...                 {Default.CODE_CLASS}.Ctry('USA'),
        ...             ]),
        ...             {Default.CODE_CLASS}.Phon('+1 (555) 555-1212'),
        ...             {Default.CODE_CLASS}.Phon('+1 (555) 555-1234'),
        ...             {Default.CODE_CLASS}.Email('GEDCOM@FamilySearch.org'),
        ...             {Default.CODE_CLASS}.Email('GEDCOM@example.com'),
        ...             {Default.CODE_CLASS}.Fax('+1 (555) 555-1212'),
        ...             {Default.CODE_CLASS}.Fax('+1 (555) 555-1234'),
        ...             {Default.CODE_CLASS}.Www('http://gedcom.io'),
        ...             {Default.CODE_CLASS}.Www('http://gedcom.info'),
        ...         ]),
        ...         {Default.CODE_CLASS}.HeadSourData('HEAD-SOUR-DATA',[
        ...             {Default.CODE_CLASS}.DateExact('1 NOV 2022', {Default.CODE_CLASS}.Time('8:38')),
        ...             {Default.CODE_CLASS}.Copr('copyright statement'),
        ...         ]),
        ...     ]),
        ...     {Default.CODE_CLASS}.Dest('https://gedcom.io/'),
        ...     {Default.CODE_CLASS}.HeadDate('10 JUN 2022', {Default.CODE_CLASS}.Time('15:43:20.48Z')),
        ...     {Default.CODE_CLASS}.Subm(subm_xref),
        ...     {Default.CODE_CLASS}.Copr('another copyright statement'),
        ...     {Default.CODE_CLASS}.HeadLang('en-US'),
        ...     {Default.CODE_CLASS}.HeadPlac({Default.CODE_CLASS}.HeadPlacForm('City, County, State, Country')),
        ... ])

        Finally, generate and print the ged lines to see how they look.  If this were in
        a full ged file the Genealogy class would produce the ged file.
        >>> print(head.ged())
        0 HEAD
        1 GEDC
        2 VERS 7.0
        1 NOTE This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.
        2 MIME text/plain
        2 LANG en-US
        2 TRAN Diese Datei soll Teile der Spezifikation abdecken und enthält keine aussagekräftigen historischen oder genealogischen Daten.
        3 LANG de
        2 SOUR @S1@
        3 PAGE 1
        2 SOUR @S1@
        3 PAGE 2
        1 SCHMA
        2 TAG _SKYPEID http://xmlns.com/foaf/0.1/skypeID
        2 TAG _JABBERID http://xmlns.com/foaf/0.1/jabberID
        1 SOUR https://gedcom.io/
        2 VERS 0.4
        2 NAME GEDCOM Steering Committee
        2 CORP FamilySearch
        3 ADDR Family History Department
        4 CONT 15 East South Temple Street
        4 CONT Salt Lake City, UT 84150 USA
        4 ADR1 Family History Department
        4 ADR2 15 East South Temple Street
        4 ADR3 Salt Lake City, UT 84150 USA
        4 CITY Salt Lake City
        4 STAE UT
        4 POST 84150
        4 CTRY USA
        3 PHON +1 (555) 555-1212
        3 PHON +1 (555) 555-1234
        3 EMAIL GEDCOM@FamilySearch.org
        3 EMAIL GEDCOM@example.com
        3 FAX +1 (555) 555-1212
        3 FAX +1 (555) 555-1234
        3 WWW http://gedcom.io
        3 WWW http://gedcom.info
        2 DATA HEAD-SOUR-DATA
        3 DATE 1 NOV 2022
        4 TIME 8:38
        3 COPR copyright statement
        1 DEST https://gedcom.io/
        1 DATE 10 JUN 2022
        2 TIME 15:43:20.48Z
        1 SUBM @U1@
        1 COPR another copyright statement
        1 LANG en-US
        1 PLAC
        2 FORM City, County, State, Country
        <BLANKLINE>""",
    'HEIGHT': f"""

    Examples:
        The following example shows how to construct the example in the specification.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> from genedata.build import Genealogy
        >>> {Default.CODE_GENEALOGY} = Genealogy('example')
        >>> indi_xref = {Default.CODE_GENEALOGY}.individual_xref('I45')
        >>> indi = {Default.CODE_CLASS}.RecordIndi(indi_xref, 
        ...     [
        ...         {Default.CODE_CLASS}.Dscr('brown eyes, 5ft 10in, 198 pounds'),
        ...     ]
        ... )
        >>> print(indi.ged())
        0 @I45@ INDI
        1 DSCR brown eyes, 5ft 10in, 198 pounds
        <BLANKLINE>""",
    'INDI-EVEN': f"""

    Example:
        The following example shows how to construct the example in the specification.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> from genedata.build import Genealogy
        >>> {Default.CODE_GENEALOGY} = Genealogy('example')
        >>> indi_xref = {Default.CODE_GENEALOGY}.individual_xref('I1')
        >>> indi = {Default.CODE_CLASS}.RecordIndi(indi_xref, 
        ...     [
        ...         {Default.CODE_CLASS}.IndiEven('',
        ...             [
        ...                 {Default.CODE_CLASS}.Type('Land Lease'),
        ...                 {Default.CODE_CLASS}.Date('2 OCT 1837'),
        ...             ]
        ...         ),
        ...         {Default.CODE_CLASS}.IndiEven('Mining equipment',
        ...             [
        ...                 {Default.CODE_CLASS}.Type('Equipment Lease'),
        ...                 {Default.CODE_CLASS}.Date('4 NOV 1837'),
        ...             ]
        ...         ),
        ...     ]
        ... )
        >>> print(indi.ged())
        0 @I1@ INDI
        1 EVEN
        2 TYPE Land Lease
        2 DATE 2 OCT 1837
        1 EVEN Mining equipment
        2 TYPE Equipment Lease
        2 DATE 4 NOV 1837
        <BLANKLINE>""",
    'INDI-FACT': f"""
    
    Examples:
        The following example shows how to construct the example in the specification.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> from genedata.build import Genealogy
        >>> {Default.CODE_GENEALOGY} = Genealogy('example')
        >>> indi_xref = {Default.CODE_GENEALOGY}.individual_xref('I1')
        >>> indi = {Default.CODE_CLASS}.RecordIndi(indi_xref, 
        ...     {Default.CODE_CLASS}.IndiFact('Woodworking', {Default.CODE_CLASS}.Type('Skills'))
        ... )
        >>> print(indi.ged())
        0 @I1@ INDI
        1 FACT Woodworking
        2 TYPE Skills
        <BLANKLINE>""",
    'INDI-RESI': f"""

    Examples:
        The following examples show how to construct the examples in the specification.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> resi = {Default.CODE_CLASS}.IndiResi('living with an aunt', {Default.CODE_CLASS}.Date('ABT MAR 1894'))
        >>> print(resi.ged())
        1 RESI living with an aunt
        2 DATE ABT MAR 1894
        <BLANKLINE>

        >>> resi2 = {Default.CODE_CLASS}.IndiResi('in a mobile caravan', 
        ...     {Default.CODE_CLASS}.Plac(', , Austro-Hungarian Empire',
        ...         {Default.CODE_CLASS}.PlacForm('City, County, Country'))
        ... )
        >>> print(resi2.ged())
        1 RESI in a mobile caravan
        2 PLAC , , Austro-Hungarian Empire
        3 FORM City, County, Country
        <BLANKLINE>""",
    'LATI': f"""

    Examples:
        The following example shows how to enter the latitude (Lati))
        coordinates into a Map structure to produce the GEDCOM example
        mentioned in the GEDCOM Specification section.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.Map(
        ...     [
        ...         {Default.CODE_CLASS}.Lati('N18.150944'), 
        ...         {Default.CODE_CLASS}.Long('E168.150944')
        ...     ]
        ... )
        >>> print(m.ged())
        1 MAP
        2 LATI N18.150944
        2 LONG E168.150944
        <BLANKLINE>
        
        Since it may be difficult to convert from degrees, minutes
        and seconds to a floating point value, the `Input` class provides
        a utility to do so for Lati.  A similar one exists for Long.
        >>> from genedata.methods import Input
        >>> m = {Default.CODE_CLASS}.Map(
        ...     [
        ...         {Default.CODE_CLASS}.Lati(Input.lati(18, 9, 3.4)), 
        ...         {Default.CODE_CLASS}.Long('E168.150944'),
        ...     ]
        ... )
        >>> print(m.ged())
        1 MAP
        2 LATI N18.150944
        2 LONG E168.150944
        <BLANKLINE>""",
    'LONG': f"""

    Examples:
        The following example howss how to enter the longitude (Long)
        coordinates into a map structure to produce the GEDCOM output
        mentioned in the GEDCOM Specification.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.Map(
        ...     [
        ...         {Default.CODE_CLASS}.Lati('N18.150944'), 
        ...         {Default.CODE_CLASS}.Long('E168.150944')
        ...     ]
        ... )
        >>> print(m.ged())
        1 MAP
        2 LATI N18.150944
        2 LONG E168.150944
        <BLANKLINE>
        
        Since it may be difficult to convert from degrees, minutes
        and seconds to a floating point value, the `Input` class provides
        a utility to do so for Long.  A similar one exists for Lati.
        >>> from genedata.methods import Input
        >>> m = {Default.CODE_CLASS}.Map(
        ...     [
        ...         {Default.CODE_CLASS}.Lati('N18.150944'), 
        ...         {Default.CODE_CLASS}.Long(Input.long(168, 9, 3.4)),
        ...     ]
        ... )
        >>> print(m.ged())
        1 MAP
        2 LATI N18.150944
        2 LONG E168.150944
        <BLANKLINE>""",
    'MAP': f"""

    Examples:
        The following example illustrates how to enter latitude (Lati) and longitude (Long)
        coordinates into a map structure to produce the GEDCOM output.
        >>> from genedata.methods import Input
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.Map(
        ...     [
        ...         {Default.CODE_CLASS}.Lati('N18.150944'), 
        ...         {Default.CODE_CLASS}.Long('E168.150944'),
        ...     ]
        ... )
        >>> print(m.ged())
        1 MAP
        2 LATI N18.150944
        2 LONG E168.150944
        <BLANKLINE>""",
    'MEDI': f"""

    Examples:
        These are the steps to build the example in the specification.
        First import the classes and build a multimedia cross reference identifier.
        >>> from genedata.build import Genealogy
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> {Default.CODE_GENEALOGY} = Genealogy('example')
        >>> obje_xref = {Default.CODE_GENEALOGY}.multimedia_xref('M1')

        Next construct the ged lines.  Let `photo.jpg` be the file name of the photo.
        >>> m = {Default.CODE_CLASS}.RecordObje(obje_xref, 
        ...     {Default.CODE_CLASS}.File('photo.jpg', 
        ...         {Default.CODE_CLASS}.Form('image/jpeg', 
        ...             {Default.CODE_CLASS}.Medi('PHOTO')
        ...         )
        ...     )
        ... )
        >>> print(m.ged())
        0 @M1@ OBJE
        1 FILE photo.jpg
        2 FORM image/jpeg
        3 MEDI PHOTO
        <BLANKLINE>

        This example shows a successful run of the Medi structure using
        the enumeration value 'AUDIO'.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.Medi('AUDIO')
        >>> print(m.ged(2))
        2 MEDI AUDIO
        <BLANKLINE>""",
    'NAME-TRAN': f"""

    Example:
        These are the steps to build the example in the specification.
        First the classes are imported which construct the ged lines.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.IndiName('/孔/德庸',
        ...         [
        ...             {Default.CODE_CLASS}.Givn('德庸'),
        ...             {Default.CODE_CLASS}.Surn('孔'),
        ...             {Default.CODE_CLASS}.NameTran('/Kǒng/ Déyōng',
        ...                 [
        ...                     {Default.CODE_CLASS}.Givn('Déyōng'),
        ...                     {Default.CODE_CLASS}.Surn('Kǒng'),
        ...                     {Default.CODE_CLASS}.Lang('zh-pinyin'),
        ...                 ]
        ...             )
        ...         ]
        ... )
        >>> print(m.ged(1))
        1 NAME /孔/德庸
        2 GIVN 德庸
        2 SURN 孔
        2 TRAN /Kǒng/ Déyōng
        3 GIVN Déyōng
        3 SURN Kǒng
        3 LANG zh-pinyin
        <BLANKLINE>""",
    'NOTE-TRAN': f"""

    Example:
        These are the steps to build the example in the specification.
        First the classes are imported which construct the ged lines.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.IndiName('Arete /Hernandez/', 
        ...     {Default.CODE_CLASS}.Note('Named after Arete from <i>The Odyssey</i>',
        ...         [
        ...             {Default.CODE_CLASS}.Lang('en'),
        ...             {Default.CODE_CLASS}.Mime('text/html'),
        ...             {Default.CODE_CLASS}.NoteTran('Named after Arete from "The Odyssey"', 
        ...                 {Default.CODE_CLASS}.Mime('text/plain')
        ...             ),
        ...             {Default.CODE_CLASS}.NoteTran('Nombrada en honor a Arete de <i>La Odisea</i>', 
        ...                 {Default.CODE_CLASS}.Lang('es')
        ...             ),
        ...         ]
        ...     )
        ... ) 
        >>> print(m.ged(1))
        1 NAME Arete /Hernandez/
        2 NOTE Named after Arete from <i>The Odyssey</i>
        3 LANG en
        3 MIME text/html
        3 TRAN Named after Arete from "The Odyssey"
        4 MIME text/plain
        3 TRAN Nombrada en honor a Arete de <i>La Odisea</i>
        4 LANG es
        <BLANKLINE>""",
    'ord-STAT': f"""

    Examples:
        This example shows a successful run of the OrdStat structure using
        the enumeration value 'BIC' occurring on January 15, 2020.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.OrdStat('BIC', 
        ...     {Default.CODE_CLASS}.DateExact('15 JAN 2020')
        ... )
        >>> print(m.ged(1))
        1 STAT BIC
        2 DATE 15 JAN 2020
        <BLANKLINE>""",
    'PAGE': f"""

    Examples:
        These are the steps to build the examples in the specification.
        First we will import the classes and then create a source cross reference `S1`.
        The void cross reference identifier comes from the Void class.
        >>> from genedata.build import Genealogy
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS} 
        >>> from genedata.structure import Void
        >>> {Default.CODE_GENEALOGY} = Genealogy('example')
        >>> sour_xref = {Default.CODE_GENEALOGY}.source_xref('S1')

        These are the steps to build the first example:
        >>> m = {Default.CODE_CLASS}.Sour(sour_xref, 
        ...     {Default.CODE_CLASS}.Page('Film: 1234567, Frame: 344, Line: 28')
        ... )
        >>> print(m.ged(2))
        2 SOUR @S1@
        3 PAGE Film: 1234567, Frame: 344, Line: 28
        <BLANKLINE>

        These are the steps to build the second example:
        >>> m = {Default.CODE_CLASS}.Dscr('Tall enough his head touched the ceiling', 
        ...     {Default.CODE_CLASS}.Sour(Void.SOUR, 
        ...         {Default.CODE_CLASS}.Page('His grand-daughter Lydia told me this in 1980')
        ...     )
        ... )
        >>> print(m.ged(1))
        1 DSCR Tall enough his head touched the ceiling
        2 SOUR @VOID@
        3 PAGE His grand-daughter Lydia told me this in 1980
        <BLANKLINE>""",
    'PEDI': f"""

    Examples:
        This example shows a successful run of the Pedi structure using
        the enumeration value 'ADOPTED'.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.Pedi('ADOPTED')
        >>> print(m.ged(1))
        1 PEDI ADOPTED
        <BLANKLINE>""",
    'PHRASE': f"""

    Examples:
        The following steps would generate the examples in the specification.
        We will need the following imports for these examples along with one
        individual cross reference identifier `I2` for the fifth example:
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> from genedata.build import Genealogy
        >>> {Default.CODE_GENEALOGY} = Genealogy('example')
        >>> indi = {Default.CODE_GENEALOGY}.individual_xref('I2')
        
        These are the steps for the first example.
        >>> m = {Default.CODE_CLASS}.Date('24 JUN 1852', 
        ...     {Default.CODE_CLASS}.Phrase('During the feast of St John')
        ... )
        >>> print(m.ged(2))
        2 DATE 24 JUN 1852
        3 PHRASE During the feast of St John
        <BLANKLINE>

        These are the steps for the second example.
        >>> m = {Default.CODE_CLASS}.Date('30 JAN 1649', 
        ...     {Default.CODE_CLASS}.Phrase('30th of January, 1648/9')
        ... )
        >>> print(m.ged(2))
        2 DATE 30 JAN 1649
        3 PHRASE 30th of January, 1648/9
        <BLANKLINE>

        These are the steps for the third example.
        >>> m = {Default.CODE_CLASS}.Date('BET 1648 AND 1649', 
        ...     {Default.CODE_CLASS}.Phrase('1648/9')
        ... )
        >>> print(m.ged(2))
        2 DATE BET 1648 AND 1649
        3 PHRASE 1648/9
        <BLANKLINE>

        These are the steps for the fourth example.
        >>> m = {Default.CODE_CLASS}.Date('BET 1 JAN 1867 AND 31 MAR 1867', 
        ...     {Default.CODE_CLASS}.Phrase('Q1 1867')
        ... )
        >>> print(m.ged(2))
        2 DATE BET 1 JAN 1867 AND 31 MAR 1867
        3 PHRASE Q1 1867
        <BLANKLINE>

        These are the steps for the fifth example.
        >>> m = {Default.CODE_CLASS}.Marr('', 
        ...     {Default.CODE_CLASS}.Asso(indi, 
        ...         {Default.CODE_CLASS}.Role('OTHER', 
        ...             {Default.CODE_CLASS}.Phrase('Maid of Honor')
        ...         )
        ...     )
        ... )
        >>> print(m.ged(1))
        1 MARR
        2 ASSO @I2@
        3 ROLE OTHER
        4 PHRASE Maid of Honor
        <BLANKLINE>""",
    'PLAC': f"""

    Example:
        The following steps would generate the example in the specification.  
        First create source cross reference identifier `S1` and then build the ged lines
        in a RecordSour.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> from genedata.build import Genealogy
        >>> {Default.CODE_GENEALOGY} = Genealogy('example')
        >>> sour = {Default.CODE_GENEALOGY}.source_xref('S1')
        >>> m = {Default.CODE_CLASS}.RecordSour(sour, 
        ...     {Default.CODE_CLASS}.Data(
        ...         {Default.CODE_CLASS}.DataEven('BIRT', 
        ...             {Default.CODE_CLASS}.Plac(', Oneida, Idaho, USA', 
        ...                 {Default.CODE_CLASS}.PlacForm('City, County, State, Country')
        ...             )
        ...         )
        ...     )
        ... )
        >>> print(m.ged())
        0 @S1@ SOUR
        1 DATA
        2 EVEN BIRT
        3 PLAC , Oneida, Idaho, USA
        4 FORM City, County, State, Country
        <BLANKLINE>""",
    'PLAC-FORM': f"""

    Example:
        The following steps would generate the example in the specifications:
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.Plac('Baltimore, , Maryland, USA', 
        ...     {Default.CODE_CLASS}.PlacForm('City, County, State, Country')
        ... )
        >>> print(m.ged(2))
        2 PLAC Baltimore, , Maryland, USA
        3 FORM City, County, State, Country
        <BLANKLINE>""",
    'PLAC-TRAN': f"""

    Example:
        The following steps would generate the example in the specifications.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.Plac('千代田, 東京, 日本',
        ...     [
        ...         {Default.CODE_CLASS}.PlacForm('区, 都, 国'),
        ...         {Default.CODE_CLASS}.Lang('ja'),
        ...         {Default.CODE_CLASS}.PlacTran('Chiyoda, Tokyo, Nihon', 
        ...             {Default.CODE_CLASS}.Lang('ja-Latn')
        ...         ),
        ...         {Default.CODE_CLASS}.PlacTran('Chiyoda, Tokyo, Japan', 
        ...             {Default.CODE_CLASS}.Lang('en')
        ...         ),
        ...     ]
        ... )
        >>> print(m.ged(2))
        2 PLAC 千代田, 東京, 日本
        3 FORM 区, 都, 国
        3 LANG ja
        3 TRAN Chiyoda, Tokyo, Nihon
        4 LANG ja-Latn
        3 TRAN Chiyoda, Tokyo, Japan
        4 LANG en
        <BLANKLINE>""",
    'QUAY': f"""

    Examples:
        This example shows a successful run of the Quay structure using
        the enumeration value '0'.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.Quay('0')
        >>> print(m.ged(1))
        1 QUAY 0
        <BLANKLINE>""",
    'record-INDI': f"""

    Example:
        Here is the way to construct the ged lines in the example from the specification.
        First create the two individual cross reference identifiers.  Then let a
        RecordIndi class format them into the desired ged lines.
        >>> from genedata.build import Genealogy
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> {Default.CODE_GENEALOGY} = Genealogy('example')
        >>> indi_i1_xref = {Default.CODE_GENEALOGY}.individual_xref('I1')
        >>> indi_i2_xref = {Default.CODE_GENEALOGY}.individual_xref('I2')
        >>> m = {Default.CODE_CLASS}.RecordIndi(indi_i1_xref, 
        ...     {Default.CODE_CLASS}.Asso(indi_i2_xref, {Default.CODE_CLASS}.Role('GODP'))
        ... )
        >>> print(m.ged())
        0 @I1@ INDI
        1 ASSO @I2@
        2 ROLE GODP
        <BLANKLINE>""",
    'record-SNOTE': f"""

    Example:
        The example in the specification has two records: the source record
        `GORDON` and an individual `I1`.  We will create those cross
        reference identifiers first.
        >>> from genedata.build import Genealogy
        >>> {Default.CODE_GENEALOGY} = Genealogy('example')
        >>> snote_xref = {Default.CODE_GENEALOGY}.shared_note_xref('GORDON', '"Gordon" is a traditional Scottish surname.\\\\nIt became a given name in honor of Charles George Gordon.')
        >>> indi_xref = {Default.CODE_GENEALOGY}.individual_xref('I1')

        Next create the record for the shared note:
        >>> import genedata.classes70 as {Default.CODE_CLASS}
        >>> snote = {Default.CODE_CLASS}.RecordSnote(snote_xref)

        Next create the individual record.
        >>> indi = {Default.CODE_CLASS}.RecordIndi(
        ...     indi_xref,
        ...     {Default.CODE_CLASS}.IndiName('Gordon /Jones/',
        ...         [
        ...             {Default.CODE_CLASS}.Note('Named after the astronaut Gordon Cooper'),
        ...             {Default.CODE_CLASS}.Snote(snote_xref),
        ...         ]
        ...     )
        ... )
        
        Now generate the ged lines for each record separately:
        >>> print(''.join([snote.ged(), indi.ged()]))
        0 @GORDON@ SNOTE "Gordon" is a traditional Scottish surname.
        1 CONT It became a given name in honor of Charles George Gordon.
        0 @I1@ INDI
        1 NAME Gordon /Jones/
        2 NOTE Named after the astronaut Gordon Cooper
        2 SNOTE @GORDON@
        <BLANKLINE>""",
    'RESN': f"""

    Examples:
        This example shows a successful run of the Resn structure using
        the enumeration value 'CONFIDENTIAL'.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.Resn('CONFIDENTIAL')
        >>> print(m.ged(1))
        1 RESN CONFIDENTIAL
        <BLANKLINE>

        More than one enumeration value may be entered for this particular
        enumeration set by separating the values with a comma.  For example,
        >>> n = {Default.CODE_CLASS}.Resn('CONFIDENTIAL, LOCKED')
        >>> print(n.ged(1))
        1 RESN CONFIDENTIAL, LOCKED
        <BLANKLINE>""",
    'ROLE': f"""

    Examples:
        The first example of the specification could be coded by first creating
        the cross reference identifiers for the individual `I1` and the source `S1`.  
        This would be done as follows:
        >>> from genedata.build import Genealogy
        >>> {Default.CODE_GENEALOGY} = Genealogy('example')
        >>> indi = {Default.CODE_GENEALOGY}.individual_xref('I1')
        >>> sour = {Default.CODE_GENEALOGY}.source_xref('S1')

        With these cross reference identifiers we can create the ged lines:
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.RecordIndi(indi, 
        ...     {Default.CODE_CLASS}.IndiName('Mary //', 
        ...         {Default.CODE_CLASS}.Sour(sour, 
        ...             {Default.CODE_CLASS}.SourEven('BIRT', 
        ...                 {Default.CODE_CLASS}.Role('MOTH')
        ...             )
        ...         )
        ...     )
        ... )
        >>> print(m.ged(1))
        0 @I1@ INDI
        1 NAME Mary //
        2 SOUR @S1@
        3 EVEN BIRT
        4 ROLE MOTH
        <BLANKLINE>

        The second example from the specification would be created as follows.
        There are two individuals in this example, `I2` and `I3`.  First
        create cross reference identifiers for them.
        >>> indi2 = {Default.CODE_GENEALOGY}.individual_xref('I2')
        >>> indi3 = {Default.CODE_GENEALOGY}.individual_xref('I3')

        With those cross reference identifiers we can complete the ged lines
        after importing the additional classes.
        Now create the lines:
        >>> m = {Default.CODE_CLASS}.RecordIndi(indi2,
        ...     [
        ...         {Default.CODE_CLASS}.Asso(indi3, 
        ...             {Default.CODE_CLASS}.Role('FRIEND', 
        ...                 {Default.CODE_CLASS}.Phrase('best friend')
        ...             )
        ...         ),
        ...         {Default.CODE_CLASS}.Bapm('', 
        ...             {Default.CODE_CLASS}.Asso(indi3, 
        ...                 {Default.CODE_CLASS}.Role('WITN')
        ...             )
        ...         ),
        ...     ]
        ... )
        >>> print(m.ged())
        0 @I2@ INDI
        1 ASSO @I3@
        2 ROLE FRIEND
        3 PHRASE best friend
        1 BAPM
        2 ASSO @I3@
        3 ROLE WITN
        <BLANKLINE>

        As a simpler example shows a successful run of the Role structure using
        the enumeration value 'CHIL'.  However, ultimately these lines would
        have to be part of a larger record.
        >>> import genedata.classes70 as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.Role('CHIL')
        >>> print(m.ged(1))
        1 ROLE CHIL
        <BLANKLINE>""",
    'SEX': f"""

    Examples:
        This example shows a successful run of the Sex structure using
        the enumeration value 'F'.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.Sex('F')
        >>> print(m.ged(1))
        1 SEX F
        <BLANKLINE>""",
    'TITL': f"""

    Examples:
        Assume that letter.pdf is a scanned copy of a letter from Ann to her husband Henry 
        on April 6, 1920.  Based on the specification one could enter this as follows.
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> m = {Default.CODE_CLASS}.File('letter.pdf', 
        ...     [
        ...         {Default.CODE_CLASS}.Form('application/pdf'), 
        ...         {Default.CODE_CLASS}.Titl('Letter from Ann to Henry April 6, 1920'),
        ...     ]
        ... )
        >>> print(m.ged(1))
        1 FILE letter.pdf
        2 FORM application/pdf
        2 TITL Letter from Ann to Henry April 6, 1920
        <BLANKLINE>""",
    'TYPE': f"""

    Examples:
        To see how the example could be produced from the specification
        first create an individual cross reference identifier then add the
        ordination event as a substructure of the RecordIndi record.
        >>> from genedata.build import Genealogy
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> {Default.CODE_GENEALOGY} = Genealogy('test')
        >>> indi_xref = {Default.CODE_GENEALOGY}.individual_xref('I1')
        >>> m = {Default.CODE_CLASS}.RecordIndi(indi_xref, 
        ...     {Default.CODE_CLASS}.Ordn('', 
        ...         {Default.CODE_CLASS}.Type('Bishop')
        ...     )
        ... )
        >>> print(m.ged())
        0 @I1@ INDI
        1 ORDN
        2 TYPE Bishop
        <BLANKLINE>""",
    'WWW': f"""

    Examples:
        The following example would send a logging message warning
        that the site "abc" cannot be reached.
        >>> from genedata.methods import Input
        >>> import genedata.classes{Config.VERSION} as {Default.CODE_CLASS}
        >>> response = Www(Input.www('abc'))
        >>> print(response.ged(1))
        1 WWW abc
        <BLANKLINE>
        
        If one doesn't want the check, one can just enter the url.
        According to the specification the url should be retained even
        it is not available.
        >>> m = Www('abc')
        >>> print(m.ged(1))
        1 WWW abc
        <BLANKLINE>""",
}
