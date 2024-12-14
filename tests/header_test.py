"""------------------------------------------------------------------------------
                            Header Tests
------------------------------------------------------------------------------"""

import pytest

from chronodata.chrono import (
    Chronology,
    Note,
    Name_Translation,
    Note_Translation,
)
from chronodata.g7 import Gedcom, GEDSpecial

testdata = [
    ('baseresult[0]', f'0 {Gedcom.HEAD}'),
    ('baseresult[1]', f'1 {Gedcom.GEDC}'),
    ('baseresult[2]', f'2 {Gedcom.VERS} {GEDSpecial.VERSION}'),
    ('len(baseresult)', 4),
    ('datetime_result[0]', f'0 {Gedcom.HEAD}'),
    ('datetime_result[1]', f'1 {Gedcom.GEDC}'),
    ('datetime_result[2]', f'2 {Gedcom.VERS} {GEDSpecial.VERSION}'),
    ('datetime_result[3][0:6]', f'1 {Gedcom.DATE}'),
    ('datetime_result[4][0:6]', f'2 {Gedcom.TIME}'),
    ('len(datetime_result)', 6),
    ('schema_result[3]', f'1 {Gedcom.SCHMA}'),
    ('schema_result[4]', f'2 {Gedcom.TAG} _LOC http:something.blog'),
    ('schema_result[5]', f'2 {Gedcom.TAG} _EASY http:here.it.is.blog'),
    ('len(schema_result)', 7),
    ('source_result[3]', f'1 {Gedcom.SOUR} me'),
    ('source_result[4]', f'2 {Gedcom.VERS} you'),
    ('source_result[5]', f'2 {Gedcom.NAME} hi'),
    ('len(source_result)', 7),
    ('corp_result[4]', f'2 {Gedcom.CORP} mine'),
    ('corp_result[5]', f'3 {Gedcom.ADDR} 1234 Here Street'),
    ('corp_result[6]', f'3 {Gedcom.CONT} There, CA 22222'),
    ('corp_result[7]', f'3 {Gedcom.CONT} usa'),
    ('corp_result[8]', f'3 {Gedcom.PHON} 1-234-456-7654'),
    ('corp_result[9]', f'3 {Gedcom.PHON} 1-333-567-5432'),
    ('corp_result[10]', f'3 {Gedcom.EMAIL} abc@her.com'),
    ('corp_result[11]', f'3 {Gedcom.EMAIL} rrr@there.com'),
    ('corp_result[12]', f'3 {Gedcom.FAX} 1-333-222-3333'),
    ('corp_result[13]', f'3 {Gedcom.FAX} 1-665-789-2345'),
    ('corp_result[14]', f'3 {Gedcom.WWW} https://www.one.com'),
    ('corp_result[15]', f'3 {Gedcom.WWW} www.go.here.com'),
    ('len(corp_result)', 17),
    ('data_result[4]', f'2 {Gedcom.DATA} datatext'),
    ('data_result[5]', f'3 {Gedcom.DATE} 2 DEC 2024'),
    ('data_result[6]', f'4 {Gedcom.TIME} 01:01:01'),
    ('data_result[7]', f'2 {Gedcom.COPR} copr'),
    ('len(data_result)', 9),
    ('submitter_result[3]', f'1 {Gedcom.SUBM} @1@'),
    ('len(submitter_result)', 5),
    ('copr_result[3]', f'1 {Gedcom.COPR} yes'),
    ('len(copr_result)', 5),
    ('language_result[3]', f'1 {Gedcom.LANG} en'),
    ('len(language_result)', 5),
    ('place_result[3]', f'1 {Gedcom.PLAC} here'),
    ('place_result[4]', f'2 {Gedcom.FORM} there'),
    ('len(place_result)', 6),
    ('note_result[3]', f'1 {Gedcom.NOTE} some note'),
    ('note_result[4]', f'2 {Gedcom.MIME} text/html'),
    ('note_result[5]', f'2 {Gedcom.LANG} en'),
    ('len(note_result)', 7),
    ('note_translation_result[6]', f'1 {Gedcom.TRAN} sss'),
    ('note_translation_result[7]', f'2 {Gedcom.MIME} text/html'),
    ('note_translation_result[8]', f'2 {Gedcom.LANG} en'),
    ('note_translation_result[9]', f'1 {Gedcom.TRAN} ddd'),
    ('note_translation_result[10]', f'2 {Gedcom.MIME} text/plain'),
    ('note_translation_result[11]', f'2 {Gedcom.LANG} sp'),
    ('shared_note_result[3]', f'1 {Gedcom.SNOTE} @1@'),
    ('len(shared_note_result)', 5),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_header(test_input: str, expected: str | int | bool) -> None:
    # Run header() without arguments.
    base = Chronology(name='base header')
    base.header()
    baseresult = base.ged_header.split('\n')

    # Run header with date and time arguments.
    a = Chronology(name='date and time')
    a.header(date='1 JAN 2000', time='01:01:01')
    datetime_result = a.ged_header.split('\n')

    # Run header which schema argument.
    b = Chronology(name='schemas')
    b.header(
        schemas=[
            ['_LOC', 'http:something.blog'],
            ['_EASY', 'http:here.it.is.blog'],
        ]
    )
    schema_result = b.ged_header.split('\n')

    # Run header with source, vers and name arguments.
    c = Chronology(name='source')
    c.header(source='me', vers='you', name='hi')
    source_result = c.ged_header.split('\n')

    # Run header with  corp list argument.
    d = Chronology(name='corp')
    d.header(
        source='abc',
        corp='mine',
        address='1234 Here Street\nThere, CA 22222\nusa',
        phones=['1-234-456-7654', '1-333-567-5432'],
        emails=['abc@her.com', 'rrr@there.com'],
        faxes=['1-333-222-3333', '1-665-789-2345'],
        wwws=['https://www.one.com', 'www.go.here.com'],
    )
    corp_result = d.ged_header.split('\n')

    # Run header with data list argument.
    e = Chronology(name='data')
    e.header(
        source='datasource',
        data='datatext',
        data_date='2 DEC 2024',
        data_time='01:01:01',
        data_copr='copr',
    )
    data_result = e.ged_header.split('\n')

    # Run header with submitter.
    f = Chronology(name='submitter')
    submitter_xref = f.submitter_record(name='frank')
    f.header(submitter=submitter_xref)
    submitter_result = f.ged_header.split('\n')

    # Run header with copr
    g = Chronology(name='copr')
    g.header(copr='yes')
    copr_result = g.ged_header.split('\n')

    # Run header with language.
    h = Chronology(name='language')
    h.header(language='en')
    language_result = h.ged_header.split('\n')

    # Run header with place.
    i = Chronology(name='place')
    i.header(place=['here', 'there'])
    place_result = i.ged_header.split('\n')

    # Run header with note.
    j = Chronology(name='note')
    j.header(note=Note('some note', 'text/html', 'en'))
    note_result = j.ged_header.split('\n')

    # Run header with note and translation.
    k = Chronology(name='note translation')
    k.header(
        note=Note(
            'some note',
            'text/html',
            'en',
            (
                Note_Translation('sss', 'text/html', 'en'),
                Note_Translation('ddd', 'text/plain', 'sp'),
            ),
        )
    )
    note_translation_result = k.ged_header.split('\n')

    # Run header with shared note.
    l = Chronology(name='shared note')
    shared_note_xref = l.shared_note_record('note')
    l.header(shared_note=shared_note_xref)
    shared_note_result = l.ged_header.split('\n')

    assert eval(test_input) == expected
