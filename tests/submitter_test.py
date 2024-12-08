"""------------------------------------------------------------------------------
                            Submitter Record Tests
------------------------------------------------------------------------------"""

import pytest

from chronodata.chrono import Chronology
from chronodata.g7 import Gedcom, GEDSpecial

testdata = [
    ('xref', '@1@'),
    ('minimal_result[0]', f'0 @1@ {Gedcom.SUBM}'),
    ('minimal_result[1]', f'1 {Gedcom.NAME} frank'),
    ('len(minimal_result)', 6),
    ('address_result[2]', f'1 {Gedcom.ADDR} 1234 Here Street'), 
    ('address_result[3]', f'1 {Gedcom.CONT} There, CA 22222'), 
    ('address_result[4]', f'1 {Gedcom.CONT} usa'),
    ('address_result[5]', f'2 {Gedcom.CITY} There'),
    ('address_result[6]', f'2 {Gedcom.STAE} CA'),
    ('address_result[7]', f'2 {Gedcom.POST} 22222'),
    ('address_result[8]', f'2 {Gedcom.CTRY} USA'),
    ('len(address_result)', 13),
    ('phone_result[2]', f'1 {Gedcom.PHON} 234-567-8909'),
    ('phone_result[3]', f'1 {Gedcom.PHON} 111-234-5555'),
    ('len(phone_result)', 8),
    ('email_result[2]', f'1 {Gedcom.EMAIL} a@b.com'),
    ('email_result[3]', f'1 {Gedcom.EMAIL} c@d.com'),
    ('len(email_result)', 8),
    ('fax_result[2]', f'1 {Gedcom.FAX} 111-111-1111'),
    ('fax_result[3]', f'1 {Gedcom.FAX} 222-222-2222'),
    ('len(fax_result)', 8),
    ('www_result[2]', f'1 {Gedcom.WWW} http://a.com'),
    ('www_result[3]', f'1 {Gedcom.WWW} http://b.com'),
    ('len(www_result)', 8),
    ('languages_result[2]', f'1 {Gedcom.LANG} en'),
    ('languages_result[3]', f'1 {Gedcom.LANG} fr'),
    ('len(languages_result)', 8),
    #('note_translation_result[6]', f'1 {Gedcom.TRAN} sss'),
    #('note_translation_result[7]', f'2 {Gedcom.MIME} text/html'),
    #('note_translation_result[8]', f'2 {Gedcom.LANG} en'),
    #('note_translation_result[9]', f'1 {Gedcom.TRAN} ddd'),
    #('note_translation_result[10]', f'2 {Gedcom.MIME} text/plain'),
    #('note_translation_result[11]', f'2 {Gedcom.LANG} sp'),
    ('shared_note_result[2]', f'1 {Gedcom.SNOTE} @1@'),
    ('len(shared_note_result)', 7),
    ('id_result[2]', f'1 {Gedcom.REFN} abc'),
    ('id_result[3]', f'2 {Gedcom.TYPE} sss'),
    ('id_result[4]', f'1 {Gedcom.UID} rrr'),
    ('id_result[5]', f'1 {Gedcom.EXID} ccc'),
    ('id_result[6]', f'2 {Gedcom.TYPE} mytype'),
    ('len(id_result)', 11),
    ('multi_result[2]', f'1 {Gedcom.OBJE} @1@'),
    ('multi_result[3]', f'2 {Gedcom.CROP}'),
    ('multi_result[4]', f'3 {Gedcom.TOP} 1'),
    ('multi_result[5]', f'3 {Gedcom.LEFT} 2'),
    ('multi_result[6]', f'3 {Gedcom.HEIGHT} 3'),
    ('multi_result[7]', f'3 {Gedcom.WIDTH} 4'),
    ('multi_result[8]', f'2 {Gedcom.TITL} yes'),
    ('multi_result[9]', f'1 {Gedcom.OBJE} @2@'),
    ('multi_result[10]', f'2 {Gedcom.CROP}'),
    ('multi_result[11]', f'3 {Gedcom.TOP} 10'),
    ('multi_result[12]', f'3 {Gedcom.LEFT} 11'),
    ('multi_result[13]', f'3 {Gedcom.HEIGHT} 12'),
    ('multi_result[14]', f'3 {Gedcom.WIDTH} 13'),
    ('multi_result[15]', f'2 {Gedcom.TITL} no'),
    ('len(multi_result)', 20),
    ('short_multi_result[2]', f'1 {Gedcom.OBJE} @1@'),
    ('short_multi_result[3]', f'2 {Gedcom.TITL} yes'),
    ('short_multi_result[4]', f'1 {Gedcom.OBJE} @2@'),
    ('short_multi_result[5]', f'2 {Gedcom.TITL} no'),
    ('len(short_multi_result)', 10),
    
    
]
@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_submitter(test_input: str, expected: str | int | bool) -> None:
    # Run submitter with only the required name.
    a = Chronology(name='minimal')
    xref = a.submitter_record(name='frank')
    minimal_result = a.ged_submitter.split('\n')

    # Run submitter with name and address.
    b = Chronology(name='address')
    address_xref = b.submitter_record(name='frank',address=['1234 Here Street\nThere, CA 22222\nusa', 'There', 'CA', '22222', 'USA'])
    address_result = b.ged_submitter.split('\n')

    # Run submitter with two phones.
    c = Chronology(name='phone')
    phone_xref = c.submitter_record(name='frank',phones=['234-567-8909', '111-234-5555'])
    phone_result = c.ged_submitter.split('\n')

    # Run submitter with two emails.
    d = Chronology(name='email')
    email_xref = d.submitter_record(name='frank',emails=['a@b.com', 'c@d.com'])
    email_result = d.ged_submitter.split('\n')

    # Run submitter with two faxes.
    e = Chronology(name='fax')
    fax_xref = e.submitter_record(name='frank',faxes=['111-111-1111', '222-222-2222'])
    fax_result = e.ged_submitter.split('\n')

    # Run submitter with two wwws.
    f = Chronology(name='fax')
    www_xref = f.submitter_record(name='frank',wwws=['http://a.com', 'http://b.com'])
    www_result = f.ged_submitter.split('\n')

    # Run submitter with two languages.
    g = Chronology(name='lang')
    languages_xref = g.submitter_record(name='frank',languages=['en', 'fr'])
    languages_result = g.ged_submitter.split('\n')

    # Run submitter with note and translation.
    h = Chronology(name='submitter note translation')
    #note_xref = h.submitter_record(name='frank', notes=['some note', 'text/html', 'en', [['sss', 'text/html', 'en'], ['ddd', 'text/plain', 'sp']], []])
    #note_translation_result = h.ged_submitter.split('\n')

    # Run submitter with shared note.
    i = Chronology(name='shared note')
    shared_note_xref = i.shared_note_record('note')
    snote_xref = i.submitter_record(name='frank', shared_note=shared_note_xref)
    shared_note_result = i.ged_submitter.split('\n')

    # Run submitter with note.

    # Run submitter with identifier.
    j = Chronology(name='id')
    id_xref = j.submitter_record(name='frank', identifiers=[['REFN','abc','sss'],['UID','rrr'],['EXID','ccc','mytype']])
    id_result = j.ged_submitter.split('\n')

    # Run submitter with multimedia.
    k = Chronology(name='multi')
    multi_xref = k.multimedia_record(files=[['here.pdf', 'text/plain']])
    multi2_xref = k.multimedia_record(files=[['yes.doc', 'text/plain']])
    m_xref = k.submitter_record(name='frank', multimedia=[[multi_xref, 1, 2, 3, 4,'yes'], [multi2_xref, 10, 11, 12, 13, 'no']])
    multi_result = k.ged_submitter.split('\n')

    # Run submitter with multimedia.
    l = Chronology(name='multi')
    multi_xref = l.multimedia_record(files=[['here.pdf', 'text/plain']])
    multi2_xref = l.multimedia_record(files=[['yes.doc', 'text/plain']])
    m_xref = l.submitter_record(name='frank', multimedia=[[multi_xref, 'yes'], [multi2_xref, 'no']])
    short_multi_result = l.ged_submitter.split('\n')
    
    
    
    assert eval(test_input) == expected