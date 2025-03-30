'''The tests in this file have been generated from the specs module
to test the classes in the classes module.  These tests are for classes that 
permit at least one substructure and require less than one.  Some of the classes
tested in the no_subs_test are tested again here.

DO NOT MANUALLY MODIFY THIS FILE.
'''

import genedata.classes7 as gc
from genedata.build import Genealogy


def test_one_sub_Adop() -> None:
    '''Validate the Adop structure with a value and one substructure.'''
    m = gc.Adop('Y', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_Age() -> None:
    '''Validate the Age structure with a value and one substructure.'''
    m = gc.Age('> 25y 10m 1d', gc.Phrase('abc'))
    assert m.validate()


def test_one_sub_Alia() -> None:
    '''Validate the Alia structure with a value and one substructure.'''
    g = Genealogy('test')
    individual = g.individual_xref('1')
    m = gc.Alia(individual, gc.Phrase('abc'))
    assert m.validate()


def test_one_sub_Anul() -> None:
    '''Validate the Anul structure with a value and one substructure.'''
    m = gc.Anul('Y', gc.Note('abc'))
    assert m.validate()


def test_one_sub_Asso() -> None:
    '''Validate the Asso structure with a value and one substructure.'''
    g = Genealogy('test')
    individual = g.individual_xref('1')
    m = gc.Asso(individual, gc.Role('WITN'))
    assert m.validate()


def test_one_sub_Bapm() -> None:
    '''Validate the Bapm structure with a value and one substructure.'''
    m = gc.Bapm('Y', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_Barm() -> None:
    '''Validate the Barm structure with a value and one substructure.'''
    m = gc.Barm('Y', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_Basm() -> None:
    '''Validate the Basm structure with a value and one substructure.'''
    m = gc.Basm('Y', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_Birt() -> None:
    '''Validate the Birt structure with a value and one substructure.'''
    m = gc.Birt('Y', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_Bles() -> None:
    '''Validate the Bles structure with a value and one substructure.'''
    m = gc.Bles('Y', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_Buri() -> None:
    '''Validate the Buri structure with a value and one substructure.'''
    m = gc.Buri('Y', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_Cast() -> None:
    '''Validate the Cast structure with a value and one substructure.'''
    m = gc.Cast('abc', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_Chil() -> None:
    '''Validate the Chil structure with a value and one substructure.'''
    g = Genealogy('test')
    individual = g.individual_xref('1')
    m = gc.Chil(individual, gc.Phrase('abc'))
    assert m.validate()


def test_one_sub_Chr() -> None:
    '''Validate the Chr structure with a value and one substructure.'''
    m = gc.Chr('Y', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_Chra() -> None:
    '''Validate the Chra structure with a value and one substructure.'''
    m = gc.Chra('Y', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_Conf() -> None:
    '''Validate the Conf structure with a value and one substructure.'''
    m = gc.Conf('Y', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_Corp() -> None:
    '''Validate the Corp structure with a value and one substructure.'''
    m = gc.Corp('abc', gc.Phon('abc'))
    assert m.validate()


def test_one_sub_Crem() -> None:
    '''Validate the Crem structure with a value and one substructure.'''
    m = gc.Crem('Y', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_DataEvenDate() -> None:
    '''Validate the DataEvenDate structure with a value and one substructure.'''
    m = gc.DataEvenDate('FROM 1 DEC 2000 TO 5 DEC 2000', gc.Phrase('abc'))
    assert m.validate()


def test_one_sub_Date() -> None:
    '''Validate the Date structure with a value and one substructure.'''
    m = gc.Date('1 JAN 2026', gc.Phrase('abc'))
    assert m.validate()


def test_one_sub_Deat() -> None:
    '''Validate the Deat structure with a value and one substructure.'''
    m = gc.Deat('Y', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_Div() -> None:
    '''Validate the Div structure with a value and one substructure.'''
    m = gc.Div('Y', gc.Note('abc'))
    assert m.validate()


def test_one_sub_Divf() -> None:
    '''Validate the Divf structure with a value and one substructure.'''
    m = gc.Divf('Y', gc.Note('abc'))
    assert m.validate()


def test_one_sub_Dscr() -> None:
    '''Validate the Dscr structure with a value and one substructure.'''
    m = gc.Dscr('abc', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_Educ() -> None:
    '''Validate the Educ structure with a value and one substructure.'''
    m = gc.Educ('abc', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_Emig() -> None:
    '''Validate the Emig structure with a value and one substructure.'''
    m = gc.Emig('Y', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_Enga() -> None:
    '''Validate the Enga structure with a value and one substructure.'''
    m = gc.Enga('Y', gc.Note('abc'))
    assert m.validate()


def test_one_sub_FamCens() -> None:
    '''Validate the FamCens structure with a value and one substructure.'''
    m = gc.FamCens('Y', gc.Note('abc'))
    assert m.validate()


def test_one_sub_FamEven() -> None:
    '''Validate the FamEven structure with a value and one substructure.'''
    m = gc.FamEven('abc', gc.Type('Bishop'))
    assert m.validate()


def test_one_sub_FamFact() -> None:
    '''Validate the FamFact structure with a value and one substructure.'''
    m = gc.FamFact('abc', gc.Type('Bishop'))
    assert m.validate()


def test_one_sub_FamHusb() -> None:
    '''Validate the FamHusb structure with a value and one substructure.'''
    g = Genealogy('test')
    individual = g.individual_xref('1')
    m = gc.FamHusb(individual, gc.Phrase('abc'))
    assert m.validate()


def test_one_sub_FamNchi() -> None:
    '''Validate the FamNchi structure with a value and one substructure.'''
    m = gc.FamNchi(1, gc.Note('abc'))
    assert m.validate()


def test_one_sub_FamResi() -> None:
    '''Validate the FamResi structure with a value and one substructure.'''
    m = gc.FamResi('abc', gc.Note('abc'))
    assert m.validate()


def test_one_sub_FamWife() -> None:
    '''Validate the FamWife structure with a value and one substructure.'''
    g = Genealogy('test')
    individual = g.individual_xref('1')
    m = gc.FamWife(individual, gc.Phrase('abc'))
    assert m.validate()


def test_one_sub_FamcAdop() -> None:
    '''Validate the FamcAdop structure with a value and one substructure.'''
    m = gc.FamcAdop('HUSB', gc.Phrase('abc'))
    assert m.validate()


def test_one_sub_FamcStat() -> None:
    '''Validate the FamcStat structure with a value and one substructure.'''
    m = gc.FamcStat('CHALLENGED', gc.Phrase('abc'))
    assert m.validate()


def test_one_sub_Fams() -> None:
    '''Validate the Fams structure with a value and one substructure.'''
    g = Genealogy('test')
    family = g.family_xref('1')
    m = gc.Fams(family, gc.Note('abc'))
    assert m.validate()


def test_one_sub_Fcom() -> None:
    '''Validate the Fcom structure with a value and one substructure.'''
    m = gc.Fcom('Y', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_FileTran() -> None:
    '''Validate the FileTran structure with a value and one substructure.'''
    m = gc.FileTran('dir/to/somewhere', gc.Form('text/html'))
    assert m.validate()


def test_one_sub_File() -> None:
    '''Validate the File structure with a value and one substructure.'''
    m = gc.File('dir/to/somewhere', gc.Form('text/html'))
    assert m.validate()


def test_one_sub_Grad() -> None:
    '''Validate the Grad structure with a value and one substructure.'''
    m = gc.Grad('Y', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_HeadSourData() -> None:
    '''Validate the HeadSourData structure with a value and one substructure.'''
    m = gc.HeadSourData('abc', gc.DateExact('1 JAN 2000'))
    assert m.validate()


def test_one_sub_Idno() -> None:
    '''Validate the Idno structure with a value and one substructure.'''
    m = gc.Idno('abc', gc.Type('Bishop'))
    assert m.validate()


def test_one_sub_Immi() -> None:
    '''Validate the Immi structure with a value and one substructure.'''
    m = gc.Immi('Y', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_IndiCens() -> None:
    '''Validate the IndiCens structure with a value and one substructure.'''
    m = gc.IndiCens('Y', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_IndiEven() -> None:
    '''Validate the IndiEven structure with a value and one substructure.'''
    m = gc.IndiEven('abc', gc.Type('Bishop'))
    assert m.validate()


def test_one_sub_IndiFact() -> None:
    '''Validate the IndiFact structure with a value and one substructure.'''
    m = gc.IndiFact('abc', gc.Type('Bishop'))
    assert m.validate()


def test_one_sub_IndiFamc() -> None:
    '''Validate the IndiFamc structure with a value and one substructure.'''
    g = Genealogy('test')
    family = g.family_xref('1')
    m = gc.IndiFamc(family, gc.Note('abc'))
    assert m.validate()


def test_one_sub_IndiName() -> None:
    '''Validate the IndiName structure with a value and one substructure.'''
    m = gc.IndiName('John /Doe/', gc.Note('abc'))
    assert m.validate()


def test_one_sub_IndiNchi() -> None:
    '''Validate the IndiNchi structure with a value and one substructure.'''
    m = gc.IndiNchi(1, gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_IndiReli() -> None:
    '''Validate the IndiReli structure with a value and one substructure.'''
    m = gc.IndiReli('abc', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_IndiResi() -> None:
    '''Validate the IndiResi structure with a value and one substructure.'''
    m = gc.IndiResi('abc', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_IndiTitl() -> None:
    '''Validate the IndiTitl structure with a value and one substructure.'''
    m = gc.IndiTitl('abc', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_Marb() -> None:
    '''Validate the Marb structure with a value and one substructure.'''
    m = gc.Marb('Y', gc.Note('abc'))
    assert m.validate()


def test_one_sub_Marc() -> None:
    '''Validate the Marc structure with a value and one substructure.'''
    m = gc.Marc('Y', gc.Note('abc'))
    assert m.validate()


def test_one_sub_Marl() -> None:
    '''Validate the Marl structure with a value and one substructure.'''
    m = gc.Marl('Y', gc.Note('abc'))
    assert m.validate()


def test_one_sub_Marr() -> None:
    '''Validate the Marr structure with a value and one substructure.'''
    m = gc.Marr('Y', gc.Note('abc'))
    assert m.validate()


def test_one_sub_Mars() -> None:
    '''Validate the Mars structure with a value and one substructure.'''
    m = gc.Mars('Y', gc.Note('abc'))
    assert m.validate()


def test_one_sub_Medi() -> None:
    '''Validate the Medi structure with a value and one substructure.'''
    m = gc.Medi('AUDIO', gc.Phrase('abc'))
    assert m.validate()


def test_one_sub_NameTran() -> None:
    '''Validate the NameTran structure with a value and one substructure.'''
    m = gc.NameTran('John /Doe/', gc.Lang('abc'))
    assert m.validate()


def test_one_sub_NameType() -> None:
    '''Validate the NameType structure with a value and one substructure.'''
    m = gc.NameType('AKA', gc.Phrase('abc'))
    assert m.validate()


def test_one_sub_Nati() -> None:
    '''Validate the Nati structure with a value and one substructure.'''
    m = gc.Nati('abc', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_Natu() -> None:
    '''Validate the Natu structure with a value and one substructure.'''
    m = gc.Natu('Y', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_Nmr() -> None:
    '''Validate the Nmr structure with a value and one substructure.'''
    m = gc.Nmr(1, gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_NoDate() -> None:
    '''Validate the NoDate structure with a value and one substructure.'''
    m = gc.NoDate('FROM 1 DEC 2000 TO 5 DEC 2000', gc.Phrase('abc'))
    assert m.validate()


def test_one_sub_No() -> None:
    '''Validate the No structure with a value and one substructure.'''
    m = gc.No('CENS', gc.Note('abc'))
    assert m.validate()


def test_one_sub_Occu() -> None:
    '''Validate the Occu structure with a value and one substructure.'''
    m = gc.Occu('abc', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_OrdStat() -> None:
    '''Validate the OrdStat structure with a value and one substructure.'''
    m = gc.OrdStat('BIC', gc.DateExact('1 JAN 2000'))
    assert m.validate()


def test_one_sub_Ordn() -> None:
    '''Validate the Ordn structure with a value and one substructure.'''
    m = gc.Ordn('Y', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_Pedi() -> None:
    '''Validate the Pedi structure with a value and one substructure.'''
    m = gc.Pedi('ADOPTED', gc.Phrase('abc'))
    assert m.validate()


def test_one_sub_PlacTran() -> None:
    '''Validate the PlacTran structure with a value and one substructure.'''
    m = gc.PlacTran('abc', gc.Lang('abc'))
    assert m.validate()


def test_one_sub_Plac() -> None:
    '''Validate the Plac structure with a value and one substructure.'''
    m = gc.Plac('abc', gc.Note('abc'))
    assert m.validate()


def test_one_sub_Prob() -> None:
    '''Validate the Prob structure with a value and one substructure.'''
    m = gc.Prob('Y', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_Prop() -> None:
    '''Validate the Prop structure with a value and one substructure.'''
    m = gc.Prop('abc', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_RecordFam() -> None:
    '''Validate the RecordFam structure with a value and one substructure.'''
    g = Genealogy('test')
    family = g.family_xref('1')
    m = gc.RecordFam(family, gc.Note('abc'))
    assert m.validate()


def test_one_sub_RecordIndi() -> None:
    '''Validate the RecordIndi structure with a value and one substructure.'''
    g = Genealogy('test')
    individual = g.individual_xref('1')
    m = gc.RecordIndi(individual, gc.Note('abc'))
    assert m.validate()


def test_one_sub_Refn() -> None:
    '''Validate the Refn structure with a value and one substructure.'''
    m = gc.Refn('abc', gc.Type('Bishop'))
    assert m.validate()


def test_one_sub_Repo() -> None:
    '''Validate the Repo structure with a value and one substructure.'''
    g = Genealogy('test')
    repository = g.repository_xref('1')
    m = gc.Repo(repository, gc.Note('abc'))
    assert m.validate()


def test_one_sub_Reti() -> None:
    '''Validate the Reti structure with a value and one substructure.'''
    m = gc.Reti('Y', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_Role() -> None:
    '''Validate the Role structure with a value and one substructure.'''
    m = gc.Role('CHIL', gc.Phrase('abc'))
    assert m.validate()


def test_one_sub_Sdate() -> None:
    '''Validate the Sdate structure with a value and one substructure.'''
    m = gc.Sdate('1 JAN 2026', gc.Phrase('abc'))
    assert m.validate()


def test_one_sub_SourEven() -> None:
    '''Validate the SourEven structure with a value and one substructure.'''
    m = gc.SourEven('CENS', gc.Phrase('abc'))
    assert m.validate()


def test_one_sub_Sour() -> None:
    '''Validate the Sour structure with a value and one substructure.'''
    g = Genealogy('test')
    source = g.source_xref('1')
    m = gc.Sour(source, gc.Note('abc'))
    assert m.validate()


def test_one_sub_Ssn() -> None:
    '''Validate the Ssn structure with a value and one substructure.'''
    m = gc.Ssn('abc', gc.Age('> 25y'))
    assert m.validate()


def test_one_sub_Will() -> None:
    '''Validate the Will structure with a value and one substructure.'''
    m = gc.Will('Y', gc.Age('> 25y'))
    assert m.validate()
