'''The tests in this file have been generated from the specs module
to test the classes in the classes module.  None of these have required substructures
nor exercise the use ob substructures.

DO NOT MANUALLY MODIFY THIS FILE.
'''

import genedata.classes7 as gc
from genedata.build import Genealogy


def test_no_subs_Abbr() -> None:
    '''Validate the Abbr structure with a value, but without substructures.'''
    m = gc.Abbr('abc')
    assert m.validate()


def test_no_subs_Addr() -> None:
    '''Validate the Addr structure with a value, but without substructures.'''
    m = gc.Addr('abc')
    assert m.validate()


def test_no_subs_AdopFamc() -> None:
    '''Validate the AdopFamc structure with a value, but without substructures.'''
    g = Genealogy('test')
    family = g.family_xref('1')
    m = gc.AdopFamc(family)
    assert m.validate()


def test_no_subs_Adop() -> None:
    '''Validate the Adop structure with a value, but without substructures.'''
    m = gc.Adop('Y')
    assert m.validate()


def test_no_subs_Adr1() -> None:
    '''Validate the Adr1 structure with a value, but without substructures.'''
    m = gc.Adr1('abc')
    assert m.validate()


def test_no_subs_Adr2() -> None:
    '''Validate the Adr2 structure with a value, but without substructures.'''
    m = gc.Adr2('abc')
    assert m.validate()


def test_no_subs_Adr3() -> None:
    '''Validate the Adr3 structure with a value, but without substructures.'''
    m = gc.Adr3('abc')
    assert m.validate()


def test_no_subs_Age() -> None:
    '''Validate the Age structure with a value, but without substructures.'''
    m = gc.Age('> 25y 10m 1d')
    assert m.validate()


def test_no_subs_Agnc() -> None:
    '''Validate the Agnc structure with a value, but without substructures.'''
    m = gc.Agnc('abc')
    assert m.validate()


def test_no_subs_Alia() -> None:
    '''Validate the Alia structure with a value, but without substructures.'''
    g = Genealogy('test')
    individual = g.individual_xref('1')
    m = gc.Alia(individual)
    assert m.validate()


def test_no_subs_Anci() -> None:
    '''Validate the Anci structure with a value, but without substructures.'''
    g = Genealogy('test')
    submitter = g.submitter_xref('1')
    m = gc.Anci(submitter)
    assert m.validate()


def test_no_subs_Anul() -> None:
    '''Validate the Anul structure with a value, but without substructures.'''
    m = gc.Anul('Y')
    assert m.validate()


def test_no_subs_Auth() -> None:
    '''Validate the Auth structure with a value, but without substructures.'''
    m = gc.Auth('abc')
    assert m.validate()


def test_no_subs_Bapl() -> None:
    '''Validate the Bapl structure with a value, but without substructures.'''
    m = gc.Bapl()
    assert m.validate()


def test_no_subs_Bapm() -> None:
    '''Validate the Bapm structure with a value, but without substructures.'''
    m = gc.Bapm('Y')
    assert m.validate()


def test_no_subs_Barm() -> None:
    '''Validate the Barm structure with a value, but without substructures.'''
    m = gc.Barm('Y')
    assert m.validate()


def test_no_subs_Basm() -> None:
    '''Validate the Basm structure with a value, but without substructures.'''
    m = gc.Basm('Y')
    assert m.validate()


def test_no_subs_Birt() -> None:
    '''Validate the Birt structure with a value, but without substructures.'''
    m = gc.Birt('Y')
    assert m.validate()


def test_no_subs_Bles() -> None:
    '''Validate the Bles structure with a value, but without substructures.'''
    m = gc.Bles('Y')
    assert m.validate()


def test_no_subs_Buri() -> None:
    '''Validate the Buri structure with a value, but without substructures.'''
    m = gc.Buri('Y')
    assert m.validate()


def test_no_subs_Caln() -> None:
    '''Validate the Caln structure with a value, but without substructures.'''
    m = gc.Caln('abc')
    assert m.validate()


def test_no_subs_Cast() -> None:
    '''Validate the Cast structure with a value, but without substructures.'''
    m = gc.Cast('abc')
    assert m.validate()


def test_no_subs_Caus() -> None:
    '''Validate the Caus structure with a value, but without substructures.'''
    m = gc.Caus('abc')
    assert m.validate()


def test_no_subs_Chil() -> None:
    '''Validate the Chil structure with a value, but without substructures.'''
    g = Genealogy('test')
    individual = g.individual_xref('1')
    m = gc.Chil(individual)
    assert m.validate()


def test_no_subs_Chr() -> None:
    '''Validate the Chr structure with a value, but without substructures.'''
    m = gc.Chr('Y')
    assert m.validate()


def test_no_subs_Chra() -> None:
    '''Validate the Chra structure with a value, but without substructures.'''
    m = gc.Chra('Y')
    assert m.validate()


def test_no_subs_City() -> None:
    '''Validate the City structure with a value, but without substructures.'''
    m = gc.City('abc')
    assert m.validate()


def test_no_subs_Conf() -> None:
    '''Validate the Conf structure with a value, but without substructures.'''
    m = gc.Conf('Y')
    assert m.validate()


def test_no_subs_Conl() -> None:
    '''Validate the Conl structure with a value, but without substructures.'''
    m = gc.Conl()
    assert m.validate()


def test_no_subs_Copr() -> None:
    '''Validate the Copr structure with a value, but without substructures.'''
    m = gc.Copr('abc')
    assert m.validate()


def test_no_subs_Corp() -> None:
    '''Validate the Corp structure with a value, but without substructures.'''
    m = gc.Corp('abc')
    assert m.validate()


def test_no_subs_Crem() -> None:
    '''Validate the Crem structure with a value, but without substructures.'''
    m = gc.Crem('Y')
    assert m.validate()


def test_no_subs_Crop() -> None:
    '''Validate the Crop structure with a value, but without substructures.'''
    m = gc.Crop()
    assert m.validate()


def test_no_subs_Ctry() -> None:
    '''Validate the Ctry structure with a value, but without substructures.'''
    m = gc.Ctry('abc')
    assert m.validate()


def test_no_subs_DataEvenDate() -> None:
    '''Validate the DataEvenDate structure with a value, but without substructures.'''
    m = gc.DataEvenDate('FROM 1 DEC 2000 TO 5 DEC 2000')
    assert m.validate()


def test_no_subs_DataEven() -> None:
    '''Validate the DataEven structure with a value, but without substructures.'''
    m = gc.DataEven('CENS')
    assert m.validate()


def test_no_subs_Data() -> None:
    '''Validate the Data structure with a value, but without substructures.'''
    m = gc.Data()
    assert m.validate()


def test_no_subs_DateExact() -> None:
    '''Validate the DateExact structure with a value, but without substructures.'''
    m = gc.DateExact('1 JAN 2026')
    assert m.validate()


def test_no_subs_Date() -> None:
    '''Validate the Date structure with a value, but without substructures.'''
    m = gc.Date('1 JAN 2026')
    assert m.validate()


def test_no_subs_Deat() -> None:
    '''Validate the Deat structure with a value, but without substructures.'''
    m = gc.Deat('Y')
    assert m.validate()


def test_no_subs_Desi() -> None:
    '''Validate the Desi structure with a value, but without substructures.'''
    g = Genealogy('test')
    submitter = g.submitter_xref('1')
    m = gc.Desi(submitter)
    assert m.validate()


def test_no_subs_Dest() -> None:
    '''Validate the Dest structure with a value, but without substructures.'''
    m = gc.Dest('abc')
    assert m.validate()


def test_no_subs_Div() -> None:
    '''Validate the Div structure with a value, but without substructures.'''
    m = gc.Div('Y')
    assert m.validate()


def test_no_subs_Divf() -> None:
    '''Validate the Divf structure with a value, but without substructures.'''
    m = gc.Divf('Y')
    assert m.validate()


def test_no_subs_Dscr() -> None:
    '''Validate the Dscr structure with a value, but without substructures.'''
    m = gc.Dscr('abc')
    assert m.validate()


def test_no_subs_Educ() -> None:
    '''Validate the Educ structure with a value, but without substructures.'''
    m = gc.Educ('abc')
    assert m.validate()


def test_no_subs_Email() -> None:
    '''Validate the Email structure with a value, but without substructures.'''
    m = gc.Email('abc')
    assert m.validate()


def test_no_subs_Emig() -> None:
    '''Validate the Emig structure with a value, but without substructures.'''
    m = gc.Emig('Y')
    assert m.validate()


def test_no_subs_Endl() -> None:
    '''Validate the Endl structure with a value, but without substructures.'''
    m = gc.Endl()
    assert m.validate()


def test_no_subs_Enga() -> None:
    '''Validate the Enga structure with a value, but without substructures.'''
    m = gc.Enga('Y')
    assert m.validate()


def test_no_subs_ExidType() -> None:
    '''Validate the ExidType structure with a value, but without substructures.'''
    m = gc.ExidType('abc')
    assert m.validate()


def test_no_subs_Exid() -> None:
    '''Validate the Exid structure with a value, but without substructures.'''
    m = gc.Exid('abc')
    assert m.validate()


def test_no_subs_FamCens() -> None:
    '''Validate the FamCens structure with a value, but without substructures.'''
    m = gc.FamCens('Y')
    assert m.validate()


def test_no_subs_FamHusb() -> None:
    '''Validate the FamHusb structure with a value, but without substructures.'''
    g = Genealogy('test')
    individual = g.individual_xref('1')
    m = gc.FamHusb(individual)
    assert m.validate()


def test_no_subs_FamNchi() -> None:
    '''Validate the FamNchi structure with a value, but without substructures.'''
    m = gc.FamNchi(1)
    assert m.validate()


def test_no_subs_FamResi() -> None:
    '''Validate the FamResi structure with a value, but without substructures.'''
    m = gc.FamResi('abc')
    assert m.validate()


def test_no_subs_FamWife() -> None:
    '''Validate the FamWife structure with a value, but without substructures.'''
    g = Genealogy('test')
    individual = g.individual_xref('1')
    m = gc.FamWife(individual)
    assert m.validate()


def test_no_subs_FamcAdop() -> None:
    '''Validate the FamcAdop structure with a value, but without substructures.'''
    m = gc.FamcAdop('HUSB')
    assert m.validate()


def test_no_subs_FamcStat() -> None:
    '''Validate the FamcStat structure with a value, but without substructures.'''
    m = gc.FamcStat('CHALLENGED')
    assert m.validate()


def test_no_subs_Famc() -> None:
    '''Validate the Famc structure with a value, but without substructures.'''
    g = Genealogy('test')
    family = g.family_xref('1')
    m = gc.Famc(family)
    assert m.validate()


def test_no_subs_Fams() -> None:
    '''Validate the Fams structure with a value, but without substructures.'''
    g = Genealogy('test')
    family = g.family_xref('1')
    m = gc.Fams(family)
    assert m.validate()


def test_no_subs_Fax() -> None:
    '''Validate the Fax structure with a value, but without substructures.'''
    m = gc.Fax('abc')
    assert m.validate()


def test_no_subs_Fcom() -> None:
    '''Validate the Fcom structure with a value, but without substructures.'''
    m = gc.Fcom('Y')
    assert m.validate()


def test_no_subs_Form() -> None:
    '''Validate the Form structure with a value, but without substructures.'''
    m = gc.Form('mime/text')
    assert m.validate()


def test_no_subs_GedcVers() -> None:
    '''Validate the GedcVers structure with a value, but without substructures.'''
    m = gc.GedcVers('abc')
    assert m.validate()


def test_no_subs_Givn() -> None:
    '''Validate the Givn structure with a value, but without substructures.'''
    m = gc.Givn('abc')
    assert m.validate()


def test_no_subs_Grad() -> None:
    '''Validate the Grad structure with a value, but without substructures.'''
    m = gc.Grad('Y')
    assert m.validate()


def test_no_subs_HeadDate() -> None:
    '''Validate the HeadDate structure with a value, but without substructures.'''
    m = gc.HeadDate('1 JAN 2026')
    assert m.validate()


def test_no_subs_HeadLang() -> None:
    '''Validate the HeadLang structure with a value, but without substructures.'''
    m = gc.HeadLang('en-US')
    assert m.validate()


def test_no_subs_HeadPlacForm() -> None:
    '''Validate the HeadPlacForm structure with a value, but without substructures.'''
    m = gc.HeadPlacForm('abc')
    assert m.validate()


def test_no_subs_HeadSourData() -> None:
    '''Validate the HeadSourData structure with a value, but without substructures.'''
    m = gc.HeadSourData('abc')
    assert m.validate()


def test_no_subs_HeadSour() -> None:
    '''Validate the HeadSour structure with a value, but without substructures.'''
    m = gc.HeadSour('abc')
    assert m.validate()


def test_no_subs_Height() -> None:
    '''Validate the Height structure with a value, but without substructures.'''
    m = gc.Height(1)
    assert m.validate()


def test_no_subs_Immi() -> None:
    '''Validate the Immi structure with a value, but without substructures.'''
    m = gc.Immi('Y')
    assert m.validate()


def test_no_subs_IndiCens() -> None:
    '''Validate the IndiCens structure with a value, but without substructures.'''
    m = gc.IndiCens('Y')
    assert m.validate()


def test_no_subs_IndiFamc() -> None:
    '''Validate the IndiFamc structure with a value, but without substructures.'''
    g = Genealogy('test')
    family = g.family_xref('1')
    m = gc.IndiFamc(family)
    assert m.validate()


def test_no_subs_IndiName() -> None:
    '''Validate the IndiName structure with a value, but without substructures.'''
    m = gc.IndiName('John /Doe/')
    assert m.validate()


def test_no_subs_IndiNchi() -> None:
    '''Validate the IndiNchi structure with a value, but without substructures.'''
    m = gc.IndiNchi(1)
    assert m.validate()


def test_no_subs_IndiReli() -> None:
    '''Validate the IndiReli structure with a value, but without substructures.'''
    m = gc.IndiReli('abc')
    assert m.validate()


def test_no_subs_IndiResi() -> None:
    '''Validate the IndiResi structure with a value, but without substructures.'''
    m = gc.IndiResi('abc')
    assert m.validate()


def test_no_subs_IndiTitl() -> None:
    '''Validate the IndiTitl structure with a value, but without substructures.'''
    m = gc.IndiTitl('abc')
    assert m.validate()


def test_no_subs_Inil() -> None:
    '''Validate the Inil structure with a value, but without substructures.'''
    m = gc.Inil()
    assert m.validate()


def test_no_subs_Lang() -> None:
    '''Validate the Lang structure with a value, but without substructures.'''
    m = gc.Lang('en-US')
    assert m.validate()


def test_no_subs_Lati() -> None:
    '''Validate the Lati structure with a value, but without substructures.'''
    m = gc.Lati('N10.1')
    assert m.validate()


def test_no_subs_Left() -> None:
    '''Validate the Left structure with a value, but without substructures.'''
    m = gc.Left(1)
    assert m.validate()


def test_no_subs_Long() -> None:
    '''Validate the Long structure with a value, but without substructures.'''
    m = gc.Long('E10.1')
    assert m.validate()


def test_no_subs_Marb() -> None:
    '''Validate the Marb structure with a value, but without substructures.'''
    m = gc.Marb('Y')
    assert m.validate()


def test_no_subs_Marc() -> None:
    '''Validate the Marc structure with a value, but without substructures.'''
    m = gc.Marc('Y')
    assert m.validate()


def test_no_subs_Marl() -> None:
    '''Validate the Marl structure with a value, but without substructures.'''
    m = gc.Marl('Y')
    assert m.validate()


def test_no_subs_Marr() -> None:
    '''Validate the Marr structure with a value, but without substructures.'''
    m = gc.Marr('Y')
    assert m.validate()


def test_no_subs_Mars() -> None:
    '''Validate the Mars structure with a value, but without substructures.'''
    m = gc.Mars('Y')
    assert m.validate()


def test_no_subs_Medi() -> None:
    '''Validate the Medi structure with a value, but without substructures.'''
    m = gc.Medi('AUDIO')
    assert m.validate()


def test_no_subs_Mime() -> None:
    '''Validate the Mime structure with a value, but without substructures.'''
    m = gc.Mime('mime/text')
    assert m.validate()


def test_no_subs_NameType() -> None:
    '''Validate the NameType structure with a value, but without substructures.'''
    m = gc.NameType('AKA')
    assert m.validate()


def test_no_subs_Name() -> None:
    '''Validate the Name structure with a value, but without substructures.'''
    m = gc.Name('abc')
    assert m.validate()


def test_no_subs_Nati() -> None:
    '''Validate the Nati structure with a value, but without substructures.'''
    m = gc.Nati('abc')
    assert m.validate()


def test_no_subs_Natu() -> None:
    '''Validate the Natu structure with a value, but without substructures.'''
    m = gc.Natu('Y')
    assert m.validate()


def test_no_subs_Nick() -> None:
    '''Validate the Nick structure with a value, but without substructures.'''
    m = gc.Nick('abc')
    assert m.validate()


def test_no_subs_Nmr() -> None:
    '''Validate the Nmr structure with a value, but without substructures.'''
    m = gc.Nmr(1)
    assert m.validate()


def test_no_subs_NoDate() -> None:
    '''Validate the NoDate structure with a value, but without substructures.'''
    m = gc.NoDate('FROM 1 DEC 2000 TO 5 DEC 2000')
    assert m.validate()


def test_no_subs_No() -> None:
    '''Validate the No structure with a value, but without substructures.'''
    m = gc.No('CENS')
    assert m.validate()


def test_no_subs_NoteTran() -> None:
    '''Validate the NoteTran structure with a value, but without substructures.'''
    m = gc.NoteTran('abc')
    assert m.validate()


def test_no_subs_Note() -> None:
    '''Validate the Note structure with a value, but without substructures.'''
    m = gc.Note('abc')
    assert m.validate()


def test_no_subs_Npfx() -> None:
    '''Validate the Npfx structure with a value, but without substructures.'''
    m = gc.Npfx('abc')
    assert m.validate()


def test_no_subs_Nsfx() -> None:
    '''Validate the Nsfx structure with a value, but without substructures.'''
    m = gc.Nsfx('abc')
    assert m.validate()


def test_no_subs_Obje() -> None:
    '''Validate the Obje structure with a value, but without substructures.'''
    g = Genealogy('test')
    multimedia = g.multimedia_xref('1')
    m = gc.Obje(multimedia)
    assert m.validate()


def test_no_subs_Occu() -> None:
    '''Validate the Occu structure with a value, but without substructures.'''
    m = gc.Occu('abc')
    assert m.validate()


def test_no_subs_Ordn() -> None:
    '''Validate the Ordn structure with a value, but without substructures.'''
    m = gc.Ordn('Y')
    assert m.validate()


def test_no_subs_Page() -> None:
    '''Validate the Page structure with a value, but without substructures.'''
    m = gc.Page('abc')
    assert m.validate()


def test_no_subs_Pedi() -> None:
    '''Validate the Pedi structure with a value, but without substructures.'''
    m = gc.Pedi('ADOPTED')
    assert m.validate()


def test_no_subs_Phon() -> None:
    '''Validate the Phon structure with a value, but without substructures.'''
    m = gc.Phon('abc')
    assert m.validate()


def test_no_subs_Phrase() -> None:
    '''Validate the Phrase structure with a value, but without substructures.'''
    m = gc.Phrase('abc')
    assert m.validate()


def test_no_subs_PlacForm() -> None:
    '''Validate the PlacForm structure with a value, but without substructures.'''
    m = gc.PlacForm('abc')
    assert m.validate()


def test_no_subs_Plac() -> None:
    '''Validate the Plac structure with a value, but without substructures.'''
    m = gc.Plac('abc')
    assert m.validate()


def test_no_subs_Post() -> None:
    '''Validate the Post structure with a value, but without substructures.'''
    m = gc.Post('abc')
    assert m.validate()


def test_no_subs_Prob() -> None:
    '''Validate the Prob structure with a value, but without substructures.'''
    m = gc.Prob('Y')
    assert m.validate()


def test_no_subs_Prop() -> None:
    '''Validate the Prop structure with a value, but without substructures.'''
    m = gc.Prop('abc')
    assert m.validate()


def test_no_subs_Publ() -> None:
    '''Validate the Publ structure with a value, but without substructures.'''
    m = gc.Publ('abc')
    assert m.validate()


def test_no_subs_Quay() -> None:
    '''Validate the Quay structure with a value, but without substructures.'''
    m = gc.Quay('0')
    assert m.validate()


def test_no_subs_RecordFam() -> None:
    '''Validate the RecordFam structure with a value, but without substructures.'''
    g = Genealogy('test')
    family = g.family_xref('1')
    m = gc.RecordFam(family)
    assert m.validate()


def test_no_subs_RecordIndi() -> None:
    '''Validate the RecordIndi structure with a value, but without substructures.'''
    g = Genealogy('test')
    individual = g.individual_xref('1')
    m = gc.RecordIndi(individual)
    assert m.validate()


def test_no_subs_RecordSnote() -> None:
    '''Validate the RecordSnote structure with a value, but without substructures.'''
    g = Genealogy('test')
    shared_note = g.shared_note_xref('1', 'text')
    m = gc.RecordSnote(shared_note)
    assert m.validate()


def test_no_subs_RecordSour() -> None:
    '''Validate the RecordSour structure with a value, but without substructures.'''
    g = Genealogy('test')
    source = g.source_xref('1')
    m = gc.RecordSour(source)
    assert m.validate()


def test_no_subs_Refn() -> None:
    '''Validate the Refn structure with a value, but without substructures.'''
    m = gc.Refn('abc')
    assert m.validate()


def test_no_subs_Reli() -> None:
    '''Validate the Reli structure with a value, but without substructures.'''
    m = gc.Reli('abc')
    assert m.validate()


def test_no_subs_Repo() -> None:
    '''Validate the Repo structure with a value, but without substructures.'''
    g = Genealogy('test')
    repository = g.repository_xref('1')
    m = gc.Repo(repository)
    assert m.validate()


def test_no_subs_Resn() -> None:
    '''Validate the Resn structure with a value, but without substructures.'''
    m = gc.Resn('CONFIDENTIAL')
    assert m.validate()


def test_no_subs_Reti() -> None:
    '''Validate the Reti structure with a value, but without substructures.'''
    m = gc.Reti('Y')
    assert m.validate()


def test_no_subs_Role() -> None:
    '''Validate the Role structure with a value, but without substructures.'''
    m = gc.Role('CHIL')
    assert m.validate()


def test_no_subs_Schma() -> None:
    '''Validate the Schma structure with a value, but without substructures.'''
    m = gc.Schma()
    assert m.validate()


def test_no_subs_Sdate() -> None:
    '''Validate the Sdate structure with a value, but without substructures.'''
    m = gc.Sdate('1 JAN 2026')
    assert m.validate()


def test_no_subs_Sex() -> None:
    '''Validate the Sex structure with a value, but without substructures.'''
    m = gc.Sex('M')
    assert m.validate()


def test_no_subs_Slgs() -> None:
    '''Validate the Slgs structure with a value, but without substructures.'''
    m = gc.Slgs()
    assert m.validate()


def test_no_subs_Snote() -> None:
    '''Validate the Snote structure with a value, but without substructures.'''
    g = Genealogy('test')
    shared_note = g.shared_note_xref('1', 'text')
    m = gc.Snote(shared_note)
    assert m.validate()


def test_no_subs_SourData() -> None:
    '''Validate the SourData structure with a value, but without substructures.'''
    m = gc.SourData()
    assert m.validate()


def test_no_subs_SourEven() -> None:
    '''Validate the SourEven structure with a value, but without substructures.'''
    m = gc.SourEven('CENS')
    assert m.validate()


def test_no_subs_Sour() -> None:
    '''Validate the Sour structure with a value, but without substructures.'''
    g = Genealogy('test')
    source = g.source_xref('1')
    m = gc.Sour(source)
    assert m.validate()


def test_no_subs_Spfx() -> None:
    '''Validate the Spfx structure with a value, but without substructures.'''
    m = gc.Spfx('abc')
    assert m.validate()


def test_no_subs_Ssn() -> None:
    '''Validate the Ssn structure with a value, but without substructures.'''
    m = gc.Ssn('abc')
    assert m.validate()


def test_no_subs_Stae() -> None:
    '''Validate the Stae structure with a value, but without substructures.'''
    m = gc.Stae('abc')
    assert m.validate()


def test_no_subs_SubmLang() -> None:
    '''Validate the SubmLang structure with a value, but without substructures.'''
    m = gc.SubmLang('en-US')
    assert m.validate()


def test_no_subs_Subm() -> None:
    '''Validate the Subm structure with a value, but without substructures.'''
    g = Genealogy('test')
    submitter = g.submitter_xref('1')
    m = gc.Subm(submitter)
    assert m.validate()


def test_no_subs_Surn() -> None:
    '''Validate the Surn structure with a value, but without substructures.'''
    m = gc.Surn('abc')
    assert m.validate()


def test_no_subs_Tag() -> None:
    '''Validate the Tag structure with a value, but without substructures.'''
    m = gc.Tag('abc')
    assert m.validate()


def test_no_subs_Temp() -> None:
    '''Validate the Temp structure with a value, but without substructures.'''
    m = gc.Temp('abc')
    assert m.validate()


def test_no_subs_Text() -> None:
    '''Validate the Text structure with a value, but without substructures.'''
    m = gc.Text('abc')
    assert m.validate()


def test_no_subs_Time() -> None:
    '''Validate the Time structure with a value, but without substructures.'''
    m = gc.Time('12:12:12')
    assert m.validate()


def test_no_subs_Titl() -> None:
    '''Validate the Titl structure with a value, but without substructures.'''
    m = gc.Titl('abc')
    assert m.validate()


def test_no_subs_Top() -> None:
    '''Validate the Top structure with a value, but without substructures.'''
    m = gc.Top(1)
    assert m.validate()


def test_no_subs_Type() -> None:
    '''Validate the Type structure with a value, but without substructures.'''
    m = gc.Type('abc')
    assert m.validate()


def test_no_subs_Uid() -> None:
    '''Validate the Uid structure with a value, but without substructures.'''
    m = gc.Uid('abc')
    assert m.validate()


def test_no_subs_Vers() -> None:
    '''Validate the Vers structure with a value, but without substructures.'''
    m = gc.Vers('abc')
    assert m.validate()


def test_no_subs_Width() -> None:
    '''Validate the Width structure with a value, but without substructures.'''
    m = gc.Width(1)
    assert m.validate()


def test_no_subs_Will() -> None:
    '''Validate the Will structure with a value, but without substructures.'''
    m = gc.Will('Y')
    assert m.validate()


def test_no_subs_Www() -> None:
    '''Validate the Www structure with a value, but without substructures.'''
    m = gc.Www('abc')
    assert m.validate()
