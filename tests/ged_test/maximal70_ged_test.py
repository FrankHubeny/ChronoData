# maximal70_ged_test

from genedata.methods import Util


def test_maximal_ged() -> None:
    # Test constructing the minimal70.ged test file.
    file = Util.read('tests/data/ged_examples/maximal70.ged')

    # Import the required packages and classes.
    import genedata.classes70 as gc
    from genedata.build import Genealogy
    from genedata.structure import Void

    # Instantiate a Genealogy class.
    g = Genealogy()

    # Instantiate the cross reference identifiers.
    # There were 16 cross reference identifiers.
    fam_F1_xref = g.family_xref('F1')
    fam_F2_xref = g.family_xref('F2')
    indi_I1_xref = g.individual_xref('I1')
    indi_I2_xref = g.individual_xref('I2')
    indi_I3_xref = g.individual_xref('I3')
    indi_I4_xref = g.individual_xref('I4')
    obje_O1_xref = g.multimedia_xref('O1')
    obje_O2_xref = g.multimedia_xref('O2')
    repo_R1_xref = g.repository_xref('R1')
    repo_R2_xref = g.repository_xref('R2')
    snote_N1_xref = g.shared_note_xref('N1', 'Shared note 1')
    snote_N2_xref = g.shared_note_xref('N2', 'Shared note 2')
    sour_S1_xref = g.source_xref('S1')
    sour_S2_xref = g.source_xref('S2')
    subm_U1_xref = g.submitter_xref('U1')
    subm_U2_xref = g.submitter_xref('U2')

    # Add any extensions that were registered in the header record.
    _skypeid_skypeID = g.document_tag(
        '_SKYPEID', 'http://xmlns.com/foaf/0.1/skypeID'
    )
    _jabberid_jabberID = g.document_tag(
        '_JABBERID', """http://xmlns.com/foaf/0.1/jabberID"""
    )

    # Instantiate the header record.
    header = gc.Head(
        [
            gc.Gedc(
                [
                    gc.GedcVers('7.0'),
                ]
            ),
            gc.Note(
                'This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.',
                [
                    gc.Mime('text/plain'),
                    gc.Lang('en-US'),
                    gc.NoteTran(
                        'Diese Datei soll Teile der Spezifikation abdecken und enthÃ¤lt keine aussagekrÃ¤ftigen historischen oder genealogischen Daten.',
                        [
                            gc.Lang('de'),
                        ],
                    ),
                    gc.Sour(
                        sour_S1_xref,
                        [
                            gc.Page('1'),
                        ],
                    ),
                    gc.Sour(
                        sour_S1_xref,
                        [
                            gc.Page('2'),
                        ],
                    ),
                ],
            ),
            gc.Schma(
                [
                    gc.Tag('_SKYPEID http://xmlns.com/foaf/0.1/skypeID'),
                    gc.Tag('_JABBERID http://xmlns.com/foaf/0.1/jabberID'),
                ]
            ),
            gc.HeadSour(
                'https://gedcom.io/',
                [
                    gc.Vers('0.4'),
                    gc.Name('GEDCOM Steering Committee'),
                    gc.Corp(
                        'FamilySearch',
                        [
                            gc.Addr(
                                """Family History Department
    15 East South Temple Street
    Salt Lake City, UT 84150 USA""",
                                [
                                    gc.Adr1('Family History Department'),
                                    gc.Adr2('15 East South Temple Street'),
                                    gc.Adr3('Salt Lake City, UT 84150 USA'),
                                    gc.City('Salt Lake City'),
                                    gc.Stae('UT'),
                                    gc.Post('84150'),
                                    gc.Ctry('USA'),
                                ],
                            ),
                            gc.Phon('+1 (555) 555-1212'),
                            gc.Phon('+1 (555) 555-1234'),
                            gc.Email('GEDCOM@FamilySearch.org'),
                            gc.Email('GEDCOM@example.com'),
                            gc.Fax('+1 (555) 555-1212'),
                            gc.Fax('+1 (555) 555-1234'),
                            gc.Www('http://gedcom.io'),
                            gc.Www('http://gedcom.info'),
                        ],
                    ),
                    gc.HeadSourData(
                        'HEAD-SOUR-DATA',
                        [
                            gc.DateExact(
                                '1 NOV 2022',
                                [
                                    gc.Time('8:38'),
                                ],
                            ),
                            gc.Copr('copyright statement'),
                        ],
                    ),
                ],
            ),
            gc.Dest('https://gedcom.io/'),
            gc.HeadDate(
                '10 JUN 2022',
                [
                    gc.Time('15:43:20.48Z'),
                ],
            ),
            gc.Subm(subm_U1_xref),
            gc.Copr('another copyright statement'),
            gc.HeadLang('en-US'),
            gc.HeadPlac(
                [
                    gc.HeadPlacForm('City, County, State, Country'),
                ]
            ),
        ]
    )

    # Instantiate the records holding the GED data.
    fam_F1 = gc.RecordFam(
        fam_F1_xref,
        [
            gc.Resn('CONFIDENTIAL, LOCKED'),
            gc.FamNchi(
                2,
                [
                    gc.Type('Type of children'),
                    gc.Husb(
                        [
                            gc.Age(
                                '25y',
                                [
                                    gc.Phrase('Adult'),
                                ],
                            ),
                        ]
                    ),
                    gc.Wife(
                        [
                            gc.Age(
                                '25y',
                                [
                                    gc.Phrase('Adult'),
                                ],
                            ),
                        ]
                    ),
                ],
            ),
            gc.FamResi(
                'Residence',
                [
                    gc.Type('Type of residence'),
                    gc.Husb(
                        [
                            gc.Age(
                                '25y',
                                [
                                    gc.Phrase('Adult'),
                                ],
                            ),
                        ]
                    ),
                    gc.Wife(
                        [
                            gc.Age(
                                '25y',
                                [
                                    gc.Phrase('Adult'),
                                ],
                            ),
                        ]
                    ),
                ],
            ),
            gc.FamFact(
                'Fact',
                [
                    gc.Type('Type of fact'),
                    gc.Husb(
                        [
                            gc.Age(
                                '25y',
                                [
                                    gc.Phrase('Adult'),
                                ],
                            ),
                        ]
                    ),
                    gc.Wife(
                        [
                            gc.Age(
                                '25y',
                                [
                                    gc.Phrase('Adult'),
                                ],
                            ),
                        ]
                    ),
                ],
            ),
            gc.Anul('Y'),
            gc.FamCens('Y'),
            gc.Div('Y'),
            gc.Divf('Y'),
            gc.Enga('Y'),
            gc.Marb('Y'),
            gc.Marc('Y'),
            gc.Marl('Y'),
            gc.Mars('Y'),
            gc.Marr(
                'Y',
                [
                    gc.Husb(
                        [
                            gc.Age(
                                '25y',
                                [
                                    gc.Phrase('Adult'),
                                ],
                            ),
                        ]
                    ),
                    gc.Wife(
                        [
                            gc.Age(
                                '25y',
                                [
                                    gc.Phrase('Adult'),
                                ],
                            ),
                        ]
                    ),
                    gc.Date(
                        '27 MAR 2022',
                        [
                            gc.Time('16:02'),
                            gc.Phrase('Afternoon'),
                        ],
                    ),
                    gc.Plac('Place'),
                    gc.Addr('Address'),
                    gc.Phon('+1 (555) 555-1212'),
                    gc.Phon('+1 (555) 555-1234'),
                    gc.Email('GEDCOM@FamilySearch.org'),
                    gc.Email('GEDCOM@example.com'),
                    gc.Fax('+1 (555) 555-1212'),
                    gc.Fax('+1 (555) 555-1234'),
                    gc.Www('http://gedcom.io'),
                    gc.Www('http://gedcom.info'),
                    gc.Agnc('Agency'),
                    gc.Reli('Religion'),
                    gc.Caus('Cause'),
                    gc.Resn('CONFIDENTIAL, LOCKED'),
                    gc.Sdate(
                        '27 MAR 2022',
                        [
                            gc.Time('16:03'),
                            gc.Phrase('Afternoon'),
                        ],
                    ),
                    gc.Asso(
                        Void.INDI,
                        [
                            gc.Role('OFFICIATOR'),
                        ],
                    ),
                    gc.Asso(
                        Void.INDI,
                        [
                            gc.Role('WITN'),
                            gc.Note('Note text'),
                        ],
                    ),
                    gc.Snote(snote_N1_xref),
                    gc.Sour(
                        sour_S1_xref,
                        [
                            gc.Page('1'),
                        ],
                    ),
                    gc.Sour(
                        sour_S1_xref,
                        [
                            gc.Page('2'),
                        ],
                    ),
                    gc.Obje(obje_O1_xref),
                    gc.Obje(obje_O2_xref),
                    gc.Uid('bbcc0025-34cb-4542-8cfb-45ba201c9c2c'),
                    gc.Uid('9ead4205-5bad-4c05-91c1-0aecd3f5127d'),
                ],
            ),
            gc.FamEven(
                'Event',
                [
                    gc.Type('Event type'),
                ],
            ),
            gc.No(
                'DIV',
                [
                    gc.NoDate(
                        'FROM 1700 TO 1800',
                        [
                            gc.Phrase('No date phrase'),
                        ],
                    ),
                    gc.Note('Note text'),
                    gc.Snote(snote_N2_xref),
                    gc.Sour(
                        sour_S1_xref,
                        [
                            gc.Page('1'),
                        ],
                    ),
                    gc.Sour(
                        sour_S1_xref,
                        [
                            gc.Page('2'),
                        ],
                    ),
                ],
            ),
            gc.No('ANUL'),
            gc.FamHusb(
                indi_I1_xref,
                [
                    gc.Phrase('Husband phrase'),
                ],
            ),
            gc.FamWife(
                indi_I2_xref,
                [
                    gc.Phrase('Wife phrase'),
                ],
            ),
            gc.Chil(
                indi_I4_xref,
                [
                    gc.Phrase('First child'),
                ],
            ),
            gc.Chil(
                Void.INDI,
                [
                    gc.Phrase('Second child'),
                ],
            ),
            gc.Asso(
                indi_I3_xref,
                [
                    gc.Phrase('Association text'),
                    gc.Role(
                        'OTHER',
                        [
                            gc.Phrase('Role text'),
                        ],
                    ),
                    gc.Note('Note text'),
                    gc.Snote(snote_N1_xref),
                    gc.Sour(
                        sour_S1_xref,
                        [
                            gc.Page('1'),
                        ],
                    ),
                    gc.Sour(
                        sour_S2_xref,
                        [
                            gc.Page('2'),
                        ],
                    ),
                ],
            ),
            gc.Asso(
                Void.INDI,
                [
                    gc.Role('CLERGY'),
                ],
            ),
            gc.Subm(subm_U1_xref),
            gc.Subm(subm_U2_xref),
            gc.Subm(Void.SUBM),
            gc.Slgs(
                [
                    gc.Date(
                        '27 MAR 2022',
                        [
                            gc.Time('15:47'),
                            gc.Phrase('Afternoon'),
                        ],
                    ),
                    gc.Temp('LOGAN'),
                    gc.Plac('Place'),
                    gc.OrdStat(
                        'COMPLETED',
                        [
                            gc.DateExact(
                                '27 MAR 2022',
                                [
                                    gc.Time('15:48'),
                                ],
                            ),
                        ],
                    ),
                    gc.Note('Note text'),
                    gc.Snote(snote_N1_xref),
                    gc.Sour(
                        sour_S1_xref,
                        [
                            gc.Page('1'),
                        ],
                    ),
                    gc.Sour(
                        sour_S2_xref,
                        [
                            gc.Page('2'),
                        ],
                    ),
                ]
            ),
            gc.Slgs(
                [
                    gc.Date('27 MAR 2022'),
                    gc.OrdStat(
                        'CANCELED',
                        [
                            gc.DateExact('27 MAR 2022'),
                        ],
                    ),
                ]
            ),
            gc.Slgs(
                [
                    gc.Date('27 MAR 2022'),
                    gc.OrdStat(
                        'EXCLUDED',
                        [
                            gc.DateExact('27 MAR 2022'),
                        ],
                    ),
                ]
            ),
            gc.Slgs(
                [
                    gc.Date('27 MAR 2022'),
                    gc.OrdStat(
                        'DNS',
                        [
                            gc.DateExact('27 MAR 2022'),
                        ],
                    ),
                ]
            ),
            gc.Slgs(
                [
                    gc.Date('27 MAR 2022'),
                    gc.OrdStat(
                        'DNS_CAN',
                        [
                            gc.DateExact('27 MAR 2022'),
                        ],
                    ),
                ]
            ),
            gc.Slgs(
                [
                    gc.Date('27 MAR 2022'),
                    gc.OrdStat(
                        'PRE_1970',
                        [
                            gc.DateExact('27 MAR 2022'),
                        ],
                    ),
                ]
            ),
            gc.Slgs(
                [
                    gc.Date('27 MAR 2022'),
                    gc.OrdStat(
                        'UNCLEARED',
                        [
                            gc.DateExact('27 MAR 2022'),
                        ],
                    ),
                ]
            ),
            gc.Refn(
                '1',
                [
                    gc.Type('User-generated identifier'),
                ],
            ),
            gc.Refn(
                '10',
                [
                    gc.Type('User-generated identifier'),
                ],
            ),
            gc.Uid('f096b664-5e40-40e2-bb72-c1664a46fe45'),
            gc.Uid('1f76f868-8a36-449c-af0d-a29247b3ab50'),
            gc.Exid(
                '123',
                [
                    gc.ExidType('http://example.com'),
                ],
            ),
            gc.Exid(
                '456',
                [
                    gc.ExidType('http://example.com'),
                ],
            ),
            gc.Note('Note text'),
            gc.Snote(snote_N1_xref),
            gc.Sour(
                sour_S1_xref,
                [
                    gc.Page('1'),
                    gc.Quay('1'),
                ],
            ),
            gc.Sour(
                sour_S2_xref,
                [
                    gc.Page('2'),
                    gc.Quay('2'),
                ],
            ),
            gc.Obje(obje_O1_xref),
            gc.Obje(obje_O2_xref),
            gc.Obje(
                Void.OBJE,
                [
                    gc.Titl('Title'),
                ],
            ),
            gc.Chan(
                [
                    gc.DateExact(
                        '27 MAR 2022',
                        [
                            gc.Time('08:56'),
                        ],
                    ),
                    gc.Note('Change date note 1'),
                    gc.Note('Change date note 2'),
                ]
            ),
            gc.Crea(
                [
                    gc.DateExact(
                        '27 MAR 2022',
                        [
                            gc.Time('08:55'),
                        ],
                    ),
                ]
            ),
        ],
    )
    fam_F2 = gc.RecordFam(
        fam_F2_xref,
        [
            gc.Marr(
                '',
                [
                    gc.Date('1998'),
                ],
            ),
            gc.Chil(indi_I1_xref),
        ],
    )
    indi_I1 = gc.RecordIndi(
        indi_I1_xref,
        [
            gc.Resn('CONFIDENTIAL, LOCKED'),
            gc.IndiName(
                'Lt. Cmndr. Joseph "John" /de Allen/ jr.',
                [
                    gc.NameType(
                        'OTHER',
                        [
                            gc.Phrase('Name type phrase'),
                        ],
                    ),
                    gc.Npfx('Lt. Cmndr.'),
                    gc.Givn('Joseph'),
                    gc.Nick('John'),
                    gc.Spfx('de'),
                    gc.Surn('Allen'),
                    gc.Nsfx('jr.'),
                    gc.NameTran(
                        'npfx John /spfx Doe/ nsfx',
                        [
                            gc.Lang('en-GB'),
                            gc.Npfx('npfx'),
                            gc.Givn('John'),
                            gc.Nick('John'),
                            gc.Spfx('spfx'),
                            gc.Surn('Doe'),
                            gc.Nsfx('nsfx'),
                        ],
                    ),
                    gc.NameTran(
                        'John /Doe/',
                        [
                            gc.Lang('en-CA'),
                        ],
                    ),
                    gc.Note('Note text'),
                    gc.Snote(snote_N1_xref),
                    gc.Snote(Void.SNOTE),
                    gc.Sour(
                        sour_S1_xref,
                        [
                            gc.Page('1'),
                        ],
                    ),
                    gc.Sour(sour_S2_xref),
                ],
            ),
            gc.IndiName(
                'John /Doe/',
                [
                    gc.NameType('BIRTH'),
                ],
            ),
            gc.IndiName(
                'Aka',
                [
                    gc.NameType('AKA'),
                ],
            ),
            gc.IndiName(
                'Immigrant Name',
                [
                    gc.NameType('IMMIGRANT'),
                ],
            ),
            gc.Sex('M'),
            gc.Cast(
                'Caste',
                [
                    gc.Type('Caste type'),
                ],
            ),
            gc.Dscr(
                'Description',
                [
                    gc.Type('Description type'),
                    gc.Sour(
                        Void.SOUR,
                        [
                            gc.Page('Entire source'),
                        ],
                    ),
                ],
            ),
            gc.Educ(
                'Education',
                [
                    gc.Type('Education type'),
                ],
            ),
            gc.Idno(
                'ID number',
                [
                    gc.Type('ID number type'),
                ],
            ),
            gc.Nati(
                'Nationality',
                [
                    gc.Type('Nationality type'),
                ],
            ),
            gc.IndiNchi(
                2,
                [
                    gc.Type('nchi type'),
                ],
            ),
            gc.Nmr(
                2,
                [
                    gc.Type('nmr type'),
                ],
            ),
            gc.Occu(
                'occu',
                [
                    gc.Type('occu type'),
                ],
            ),
            gc.Prop(
                'prop',
                [
                    gc.Type('prop type'),
                ],
            ),
            gc.IndiReli(
                'reli',
                [
                    gc.Type('reli type'),
                ],
            ),
            gc.IndiResi(
                'resi',
                [
                    gc.Type('resi type'),
                ],
            ),
            gc.Ssn(
                'ssn',
                [
                    gc.Type('ssn type'),
                ],
            ),
            gc.IndiTitl(
                'titl',
                [
                    gc.Type('titl type'),
                ],
            ),
            gc.IndiFact(
                'fact',
                [
                    gc.Type('fact type'),
                ],
            ),
            gc.Bapm(
                '',
                [
                    gc.Type('bapm type'),
                ],
            ),
            gc.Bapm('Y'),
            gc.Barm(
                '',
                [
                    gc.Type('barm type'),
                ],
            ),
            gc.Basm(
                '',
                [
                    gc.Type('basm type'),
                ],
            ),
            gc.Bles(
                '',
                [
                    gc.Type('bles type'),
                ],
            ),
            gc.Buri(
                '',
                [
                    gc.Type('buri type'),
                    gc.Date('30 MAR 2022'),
                ],
            ),
            gc.IndiCens(
                '',
                [
                    gc.Type('cens type'),
                ],
            ),
            gc.Chra(
                '',
                [
                    gc.Type('chra type'),
                ],
            ),
            gc.Conf(
                '',
                [
                    gc.Type('conf type'),
                ],
            ),
            gc.Crem(
                '',
                [
                    gc.Type('crem type'),
                ],
            ),
            gc.Deat(
                '',
                [
                    gc.Type('deat type'),
                    gc.Date('28 MAR 2022'),
                    gc.Plac('Somewhere'),
                    gc.Addr('Address'),
                    gc.Phon('+1 (555) 555-1212'),
                    gc.Phon('+1 (555) 555-1234'),
                    gc.Email('GEDCOM@FamilySearch.org'),
                    gc.Email('GEDCOM@example.com'),
                    gc.Fax('+1 (555) 555-1212'),
                    gc.Fax('+1 (555) 555-1234'),
                    gc.Www('http://gedcom.io'),
                    gc.Www('http://gedcom.info'),
                    gc.Agnc('Agency'),
                    gc.Reli('Religion'),
                    gc.Caus('Cause of death'),
                    gc.Resn('CONFIDENTIAL, LOCKED'),
                    gc.Sdate(
                        '28 MAR 2022',
                        [
                            gc.Time('16:47'),
                            gc.Phrase('sdate phrase'),
                        ],
                    ),
                    gc.Asso(
                        indi_I3_xref,
                        [
                            gc.Role('CHIL'),
                        ],
                    ),
                    gc.Asso(
                        Void.INDI,
                        [
                            gc.Role('PARENT'),
                        ],
                    ),
                    gc.Note('Note text'),
                    gc.Snote(snote_N1_xref),
                    gc.Sour(
                        sour_S1_xref,
                        [
                            gc.Page('1'),
                        ],
                    ),
                    gc.Sour(
                        sour_S2_xref,
                        [
                            gc.Page('2'),
                        ],
                    ),
                    gc.Obje(obje_O1_xref),
                    gc.Obje(obje_O2_xref),
                    gc.Uid('82092878-6f4f-4bca-ad59-d1ae87c5e521'),
                    gc.Uid('daf4b8c0-4141-42c4-bec8-01d1d818dfaf'),
                ],
            ),
            gc.Emig(
                '',
                [
                    gc.Type('emig type'),
                ],
            ),
            gc.Fcom(
                '',
                [
                    gc.Type('fcom type'),
                ],
            ),
            gc.Grad(
                '',
                [
                    gc.Type('grad type'),
                ],
            ),
            gc.Immi(
                '',
                [
                    gc.Type('immi type'),
                ],
            ),
            gc.Natu(
                '',
                [
                    gc.Type('natu type'),
                ],
            ),
            gc.Ordn(
                '',
                [
                    gc.Type('ordn type'),
                ],
            ),
            gc.Prob(
                '',
                [
                    gc.Type('prob type'),
                ],
            ),
            gc.Reti(
                '',
                [
                    gc.Type('reti type'),
                ],
            ),
            gc.Will(
                '',
                [
                    gc.Type('will type'),
                ],
            ),
            gc.Adop(
                '',
                [
                    gc.Type('adop type'),
                    gc.AdopFamc(
                        Void.FAM,
                        [
                            gc.FamcAdop(
                                'BOTH',
                                [
                                    gc.Phrase('Adoption phrase'),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            gc.Adop(
                '',
                [
                    gc.AdopFamc(
                        Void.FAM,
                        [
                            gc.FamcAdop('HUSB'),
                        ],
                    ),
                ],
            ),
            gc.Adop(
                '',
                [
                    gc.AdopFamc(
                        Void.FAM,
                        [
                            gc.FamcAdop('WIFE'),
                        ],
                    ),
                ],
            ),
            gc.Birt(
                '',
                [
                    gc.Type('birth type'),
                    gc.Date('1 JAN 2000'),
                ],
            ),
            gc.Chr(
                '',
                [
                    gc.Type('chr type'),
                    gc.Date('9 JAN 2000'),
                    gc.Age(
                        '8d',
                        [
                            gc.Phrase('Age phrase'),
                        ],
                    ),
                ],
            ),
            gc.IndiEven(
                'Event',
                [
                    gc.Type('Event type'),
                ],
            ),
            gc.No(
                'NATU',
                [
                    gc.NoDate(
                        'FROM 1700 TO 1800',
                        [
                            gc.Phrase('No date phrase'),
                        ],
                    ),
                    gc.Note('Note text'),
                    gc.Snote(snote_N1_xref),
                    gc.Sour(
                        sour_S1_xref,
                        [
                            gc.Page('1'),
                        ],
                    ),
                    gc.Sour(
                        sour_S1_xref,
                        [
                            gc.Page('2'),
                        ],
                    ),
                ],
            ),
            gc.No('EMIG'),
            gc.Bapl(
                [
                    gc.OrdStat(
                        'STILLBORN',
                        [
                            gc.DateExact('27 MAR 2022'),
                        ],
                    ),
                ]
            ),
            gc.Bapl(
                [
                    gc.OrdStat(
                        'SUBMITTED',
                        [
                            gc.DateExact('27 MAR 2022'),
                        ],
                    ),
                ]
            ),
            gc.Bapl(
                [
                    gc.Date('27 MAR 2022'),
                ]
            ),
            gc.Conl(
                [
                    gc.OrdStat(
                        'INFANT',
                        [
                            gc.DateExact('27 MAR 2022'),
                        ],
                    ),
                ]
            ),
            gc.Conl(
                [
                    gc.Date('27 MAR 2022'),
                ]
            ),
            gc.Endl(
                [
                    gc.OrdStat(
                        'CHILD',
                        [
                            gc.DateExact('27 MAR 2022'),
                        ],
                    ),
                ]
            ),
            gc.Endl(
                [
                    gc.Date('27 MAR 2022'),
                ]
            ),
            gc.Inil(
                [
                    gc.OrdStat(
                        'EXCLUDED',
                        [
                            gc.DateExact('27 MAR 2022'),
                        ],
                    ),
                ]
            ),
            gc.Inil(
                [
                    gc.Date('27 MAR 2022'),
                ]
            ),
            gc.Slgc(
                [
                    gc.Date(
                        '27 MAR 2022',
                        [
                            gc.Time('15:47'),
                            gc.Phrase('Afternoon'),
                        ],
                    ),
                    gc.Temp('SLAKE'),
                    gc.Famc(Void.FAM),
                ]
            ),
            gc.Slgc(
                [
                    gc.Plac('Place'),
                    gc.OrdStat(
                        'BIC',
                        [
                            gc.DateExact(
                                '27 MAR 2022',
                                [
                                    gc.Time('15:48'),
                                ],
                            ),
                        ],
                    ),
                    gc.Note('Note text'),
                    gc.Snote(snote_N1_xref),
                    gc.Sour(
                        sour_S1_xref,
                        [
                            gc.Page('1'),
                        ],
                    ),
                    gc.Sour(
                        sour_S2_xref,
                        [
                            gc.Page('2'),
                        ],
                    ),
                    gc.Famc(Void.FAM),
                ]
            ),
            gc.Slgc(
                [
                    gc.Famc(fam_F2_xref),
                ]
            ),
            gc.IndiFamc(
                Void.FAM,
                [
                    gc.Pedi(
                        'OTHER',
                        [
                            gc.Phrase('Other type'),
                        ],
                    ),
                    gc.FamcStat(
                        'CHALLENGED',
                        [
                            gc.Phrase('Phrase'),
                        ],
                    ),
                ],
            ),
            gc.IndiFamc(
                Void.FAM,
                [
                    gc.Pedi('FOSTER'),
                ],
            ),
            gc.IndiFamc(
                Void.FAM,
                [
                    gc.Pedi('SEALING'),
                ],
            ),
            gc.IndiFamc(
                fam_F2_xref,
                [
                    gc.Pedi('ADOPTED'),
                    gc.FamcStat('PROVEN'),
                ],
            ),
            gc.IndiFamc(
                fam_F2_xref,
                [
                    gc.Pedi('BIRTH'),
                    gc.FamcStat('DISPROVEN'),
                ],
            ),
            gc.Fams(
                Void.FAM,
                [
                    gc.Note('Note text'),
                    gc.Snote(snote_N1_xref),
                ],
            ),
            gc.Fams(fam_F1_xref),
            gc.Subm(subm_U1_xref),
            gc.Subm(subm_U2_xref),
            gc.Asso(
                Void.INDI,
                [
                    gc.Phrase('Mr Stockdale'),
                    gc.Role('FRIEND'),
                ],
            ),
            gc.Asso(
                Void.INDI,
                [
                    gc.Role('NGHBR'),
                ],
            ),
            gc.Asso(
                Void.INDI,
                [
                    gc.Role('FATH'),
                ],
            ),
            gc.Asso(
                Void.INDI,
                [
                    gc.Role('GODP'),
                ],
            ),
            gc.Asso(
                Void.INDI,
                [
                    gc.Role('HUSB'),
                ],
            ),
            gc.Asso(
                Void.INDI,
                [
                    gc.Role('MOTH'),
                ],
            ),
            gc.Asso(
                Void.INDI,
                [
                    gc.Role('MULTIPLE'),
                ],
            ),
            gc.Asso(
                Void.INDI,
                [
                    gc.Role('SPOU'),
                ],
            ),
            gc.Asso(
                Void.INDI,
                [
                    gc.Role('WIFE'),
                ],
            ),
            gc.Alia(Void.INDI),
            gc.Alia(
                indi_I3_xref,
                [
                    gc.Phrase('Alias'),
                ],
            ),
            gc.Anci(subm_U1_xref),
            gc.Anci(Void.SUBM),
            gc.Desi(subm_U1_xref),
            gc.Desi(Void.SUBM),
            gc.Refn(
                '1',
                [
                    gc.Type('User-generated identifier'),
                ],
            ),
            gc.Refn(
                '10',
                [
                    gc.Type('User-generated identifier'),
                ],
            ),
            gc.Uid('3d75b5eb-36e9-40b3-b79f-f088b5c18595'),
            gc.Uid('cb49c361-7124-447e-b587-4c6d36e51825'),
            gc.Exid(
                '123',
                [
                    gc.ExidType('http://example.com'),
                ],
            ),
            gc.Exid(
                '456',
                [
                    gc.ExidType('http://example.com'),
                ],
            ),
            gc.Note("""me@example.com is an example email address.
    @me and @I are example social media handles.
    @@@@ has four @ characters where only the first is escaped."""),
            gc.Snote(snote_N1_xref),
            gc.Sour(
                sour_S1_xref,
                [
                    gc.Page('1'),
                    gc.Quay('3'),
                ],
            ),
            gc.Sour(sour_S2_xref),
            gc.Obje(obje_O1_xref),
            gc.Obje(obje_O2_xref),
            gc.Chan(
                [
                    gc.DateExact(
                        '27 MAR 2022',
                        [
                            gc.Time('08:56'),
                        ],
                    ),
                    gc.Note('Change date note 1'),
                    gc.Note('Change date note 2'),
                ]
            ),
            gc.Crea(
                [
                    gc.DateExact(
                        '27 MAR 2022',
                        [
                            gc.Time('08:55'),
                        ],
                    ),
                ]
            ),
        ],
    )
    indi_I2 = gc.RecordIndi(
        indi_I2_xref,
        [
            gc.IndiName(
                'Maiden Name',
                [
                    gc.NameType('MAIDEN'),
                ],
            ),
            gc.IndiName(
                'Married Name',
                [
                    gc.NameType('MARRIED'),
                ],
            ),
            gc.IndiName(
                'Professional Name',
                [
                    gc.NameType('PROFESSIONAL'),
                ],
            ),
            gc.Sex('F'),
            gc.Fams(fam_F1_xref),
        ],
    )
    indi_I3 = gc.RecordIndi(
        indi_I3_xref,
        [
            gc.Sex('X'),
        ],
    )
    indi_I4 = gc.RecordIndi(
        indi_I4_xref,
        [
            gc.Sex('U'),
            gc.IndiFamc(fam_F1_xref),
        ],
    )
    obje_O1 = gc.RecordObje(
        obje_O1_xref,
        [
            gc.Resn('CONFIDENTIAL, LOCKED'),
            gc.File(
                'file:///path/to/file1',
                [
                    gc.Form(
                        'text/plain',
                        [
                            gc.Medi(
                                'OTHER',
                                [
                                    gc.Phrase('Transcript'),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            gc.File(
                'media/original.mp3',
                [
                    gc.Form(
                        'audio/mp3',
                        [
                            gc.Medi('AUDIO'),
                        ],
                    ),
                    gc.Titl('Object title'),
                    gc.FileTran(
                        'media/derived.oga',
                        [
                            gc.Form('audio/ogg'),
                        ],
                    ),
                    gc.FileTran(
                        'media/transcript.vtt',
                        [
                            gc.Form('text/vtt'),
                        ],
                    ),
                ],
            ),
            gc.Refn(
                '1',
                [
                    gc.Type('User-generated identifier'),
                ],
            ),
            gc.Refn(
                '10',
                [
                    gc.Type('User-generated identifier'),
                ],
            ),
            gc.Uid('69ebdd0e-c78c-4b81-873f-dc8ac30a48b9'),
            gc.Uid('79cae8c4-e673-4e4f-bc5d-13b02d931302'),
            gc.Exid(
                '123',
                [
                    gc.ExidType('http://example.com'),
                ],
            ),
            gc.Exid(
                '456',
                [
                    gc.ExidType('http://example.com'),
                ],
            ),
            gc.Note(
                'American English',
                [
                    gc.Mime('text/plain'),
                    gc.Lang('en-US'),
                    gc.NoteTran(
                        'British English',
                        [
                            gc.Mime('text/plain'),
                            gc.Lang('en-GB'),
                        ],
                    ),
                    gc.NoteTran(
                        'Canadian English',
                        [
                            gc.Mime('text/plain'),
                            gc.Lang('en-CA'),
                        ],
                    ),
                    gc.Sour(
                        sour_S1_xref,
                        [
                            gc.Page('1'),
                        ],
                    ),
                    gc.Sour(
                        sour_S2_xref,
                        [
                            gc.Page('2'),
                        ],
                    ),
                ],
            ),
            gc.Snote(snote_N1_xref),
            gc.Sour(
                sour_S1_xref,
                [
                    gc.Page('1'),
                    gc.SourData(
                        [
                            gc.Date(
                                '28 MAR 2022',
                                [
                                    gc.Time('10:29'),
                                    gc.Phrase('Morning'),
                                ],
                            ),
                            gc.Text(
                                'Text 1',
                                [
                                    gc.Mime('text/plain'),
                                    gc.Lang('en-US'),
                                ],
                            ),
                            gc.Text(
                                'Text 2',
                                [
                                    gc.Mime('text/plain'),
                                    gc.Lang('en-US'),
                                ],
                            ),
                        ]
                    ),
                    gc.SourEven(
                        'BIRT',
                        [
                            gc.Phrase('Event phrase'),
                            gc.Role(
                                'OTHER',
                                [
                                    gc.Phrase('Role phrase'),
                                ],
                            ),
                        ],
                    ),
                    gc.Quay('0'),
                    gc.Obje(
                        obje_O1_xref,
                        [
                            gc.Crop(
                                [
                                    gc.Top(0),
                                    gc.Left(0),
                                    gc.Height(100),
                                    gc.Width(100),
                                ]
                            ),
                            gc.Titl('Title'),
                        ],
                    ),
                    gc.Obje(
                        obje_O1_xref,
                        [
                            gc.Crop(
                                [
                                    gc.Top(100),
                                    gc.Left(100),
                                ]
                            ),
                            gc.Titl('Title'),
                        ],
                    ),
                    gc.Note(
                        'American English',
                        [
                            gc.Mime('text/plain'),
                            gc.Lang('en-US'),
                            gc.NoteTran(
                                'British English',
                                [
                                    gc.Lang('en-GB'),
                                ],
                            ),
                            gc.Sour(
                                sour_S1_xref,
                                [
                                    gc.Page('1'),
                                ],
                            ),
                            gc.Sour(
                                sour_S2_xref,
                                [
                                    gc.Page('2'),
                                ],
                            ),
                        ],
                    ),
                    gc.Snote(snote_N1_xref),
                ],
            ),
            gc.Sour(
                sour_S1_xref,
                [
                    gc.Page('2'),
                ],
            ),
            gc.Chan(
                [
                    gc.DateExact(
                        '27 MAR 2022',
                        [
                            gc.Time('08:56'),
                        ],
                    ),
                    gc.Note('Change date note 1'),
                    gc.Note('Change date note 2'),
                ]
            ),
            gc.Crea(
                [
                    gc.DateExact(
                        '27 MAR 2022',
                        [
                            gc.Time('08:55'),
                        ],
                    ),
                ]
            ),
        ],
    )
    obje_O2 = gc.RecordObje(
        obje_O2_xref,
        [
            gc.Resn('PRIVACY'),
            gc.File(
                'http://host.example.com/path/to/file2',
                [
                    gc.Form(
                        'text/plain',
                        [
                            gc.Medi('ELECTRONIC'),
                        ],
                    ),
                ],
            ),
        ],
    )
    repo_R1 = gc.RecordRepo(
        repo_R1_xref,
        [
            gc.Name('Repository 1'),
            gc.Addr(
                """Family History Department
    15 East South Temple Street
    Salt Lake City, UT 84150 USA""",
                [
                    gc.Adr1('Family History Department'),
                    gc.Adr2('15 East South Temple Street'),
                    gc.Adr3('Salt Lake City, UT 84150 USA'),
                    gc.City('Salt Lake City'),
                    gc.Stae('UT'),
                    gc.Post('84150'),
                    gc.Ctry('USA'),
                ],
            ),
            gc.Phon('+1 (555) 555-1212'),
            gc.Phon('+1 (555) 555-1234'),
            gc.Email('GEDCOM@FamilySearch.org'),
            gc.Email('GEDCOM@example.com'),
            gc.Fax('+1 (555) 555-1212'),
            gc.Fax('+1 (555) 555-1234'),
            gc.Www('http://gedcom.io'),
            gc.Www('http://gedcom.info'),
            gc.Note('Note text'),
            gc.Snote(snote_N1_xref),
            gc.Refn(
                '1',
                [
                    gc.Type('User-generated identifier'),
                ],
            ),
            gc.Refn(
                '10',
                [
                    gc.Type('User-generated identifier'),
                ],
            ),
            gc.Uid('efa7885b-c806-4590-9f1b-247797e4c96d'),
            gc.Uid('d530f6ab-cfd4-44cd-ab2c-e40bddb76bf8'),
            gc.Exid(
                '123',
                [
                    gc.ExidType('http://example.com'),
                ],
            ),
            gc.Exid(
                '456',
                [
                    gc.ExidType('http://example.com'),
                ],
            ),
            gc.Chan(
                [
                    gc.DateExact(
                        '27 MAR 2022',
                        [
                            gc.Time('08:56'),
                        ],
                    ),
                    gc.Note('Change date note 1'),
                    gc.Note('Change date note 2'),
                ]
            ),
            gc.Crea(
                [
                    gc.DateExact(
                        '27 MAR 2022',
                        [
                            gc.Time('08:55'),
                        ],
                    ),
                ]
            ),
        ],
    )
    repo_R2 = gc.RecordRepo(
        repo_R2_xref,
        [
            gc.Name('Repository 2'),
        ],
    )
    snote_N1 = gc.RecordSnote(
        snote_N1_xref,
        [
            gc.Mime('text/plain'),
            gc.Lang('en-US'),
            gc.NoteTran(
                'Shared note 1',
                [
                    gc.Mime('text/plain'),
                    gc.Lang('en-GB'),
                ],
            ),
            gc.NoteTran(
                'Shared note 1',
                [
                    gc.Mime('text/plain'),
                    gc.Lang('en-CA'),
                ],
            ),
            gc.Sour(
                sour_S1_xref,
                [
                    gc.Page('1'),
                ],
            ),
            gc.Sour(
                sour_S2_xref,
                [
                    gc.Page('2'),
                ],
            ),
            gc.Refn(
                '1',
                [
                    gc.Type('User-generated identifier'),
                ],
            ),
            gc.Refn(
                '10',
                [
                    gc.Type('User-generated identifier'),
                ],
            ),
            gc.Uid('6efbee0b-96a1-43ea-83c8-828ec71c54d7'),
            gc.Uid('4094d92a-5525-44ec-973d-6c527aa5535a'),
            gc.Exid(
                '123',
                [
                    gc.ExidType('http://example.com'),
                ],
            ),
            gc.Exid(
                '456',
                [
                    gc.ExidType('http://example.com'),
                ],
            ),
            gc.Chan(
                [
                    gc.DateExact(
                        '27 MAR 2022',
                        [
                            gc.Time('08:56'),
                        ],
                    ),
                    gc.Note('Change date note 1'),
                    gc.Note('Change date note 2'),
                ]
            ),
            gc.Crea(
                [
                    gc.DateExact(
                        '27 MAR 2022',
                        [
                            gc.Time('08:55'),
                        ],
                    ),
                ]
            ),
        ],
    )
    snote_N2 = gc.RecordSnote(snote_N2_xref)
    sour_S1 = gc.RecordSour(
        sour_S1_xref,
        [
            gc.Data(
                [
                    gc.DataEven(
                        'BIRT, DEAT',
                        [
                            gc.DataEvenDate(
                                'FROM 1701 TO 1800',
                                [
                                    gc.Phrase('18th century'),
                                ],
                            ),
                            gc.Plac(
                                'Some City, Some County, Some State, Some Country',
                                [
                                    gc.PlacForm('City, County, State, Country'),
                                    gc.Lang('en-US'),
                                    gc.PlacTran(
                                        'Some City, Some County, Some State, Some Country',
                                        [
                                            gc.Lang('en-GB'),
                                        ],
                                    ),
                                    gc.PlacTran(
                                        'Some City, Some County, Some State, Some Country',
                                        [
                                            gc.Lang('en'),
                                        ],
                                    ),
                                    gc.Map(
                                        [
                                            gc.Lati('N18.150944'),
                                            gc.Long('E168.150944'),
                                        ]
                                    ),
                                    gc.Exid(
                                        '123',
                                        [
                                            gc.ExidType('http://example.com'),
                                        ],
                                    ),
                                    gc.Exid(
                                        '456',
                                        [
                                            gc.ExidType('http://example.com'),
                                        ],
                                    ),
                                    gc.Note(
                                        'American English',
                                        [
                                            gc.Mime('text/plain'),
                                            gc.Lang('en-US'),
                                            gc.NoteTran(
                                                'British English',
                                                [
                                                    gc.Lang('en-GB'),
                                                ],
                                            ),
                                            gc.Sour(
                                                sour_S1_xref,
                                                [
                                                    gc.Page('1'),
                                                ],
                                            ),
                                            gc.Sour(
                                                sour_S2_xref,
                                                [
                                                    gc.Page('2'),
                                                ],
                                            ),
                                        ],
                                    ),
                                    gc.Snote(snote_N1_xref),
                                ],
                            ),
                        ],
                    ),
                    gc.DataEven(
                        'MARR',
                        [
                            gc.DataEvenDate(
                                'FROM 1701 TO 1800',
                                [
                                    gc.Phrase('18th century'),
                                ],
                            ),
                        ],
                    ),
                    gc.Agnc('Agency name'),
                    gc.Note(
                        'American English',
                        [
                            gc.Mime('text/plain'),
                            gc.Lang('en-US'),
                            gc.NoteTran(
                                'British English',
                                [
                                    gc.Lang('en-GB'),
                                ],
                            ),
                            gc.Sour(
                                sour_S1_xref,
                                [
                                    gc.Page('1'),
                                ],
                            ),
                            gc.Sour(
                                sour_S2_xref,
                                [
                                    gc.Page('2'),
                                ],
                            ),
                        ],
                    ),
                    gc.Snote(snote_N1_xref),
                ]
            ),
            gc.Auth('Author'),
            gc.Titl('Title'),
            gc.Abbr('Abbreviation'),
            gc.Publ('Publication info'),
            gc.Text(
                'Source text',
                [
                    gc.Mime('text/plain'),
                    gc.Lang('en-US'),
                ],
            ),
            gc.Repo(
                repo_R1_xref,
                [
                    gc.Note('Note text'),
                    gc.Snote(snote_N1_xref),
                    gc.Caln(
                        'Call number',
                        [
                            gc.Medi(
                                'BOOK',
                                [
                                    gc.Phrase('Booklet'),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            gc.Repo(
                repo_R2_xref,
                [
                    gc.Caln(
                        'Call number',
                        [
                            gc.Medi('VIDEO'),
                        ],
                    ),
                    gc.Caln(
                        'Call number',
                        [
                            gc.Medi('CARD'),
                        ],
                    ),
                    gc.Caln(
                        'Call number',
                        [
                            gc.Medi('FICHE'),
                        ],
                    ),
                    gc.Caln(
                        'Call number',
                        [
                            gc.Medi('FILM'),
                        ],
                    ),
                    gc.Caln(
                        'Call number',
                        [
                            gc.Medi('MAGAZINE'),
                        ],
                    ),
                    gc.Caln(
                        'Call number',
                        [
                            gc.Medi('MANUSCRIPT'),
                        ],
                    ),
                    gc.Caln(
                        'Call number',
                        [
                            gc.Medi('MAP'),
                        ],
                    ),
                    gc.Caln(
                        'Call number',
                        [
                            gc.Medi('NEWSPAPER'),
                        ],
                    ),
                    gc.Caln(
                        'Call number',
                        [
                            gc.Medi('PHOTO'),
                        ],
                    ),
                    gc.Caln(
                        'Call number',
                        [
                            gc.Medi('TOMBSTONE'),
                        ],
                    ),
                ],
            ),
            gc.Refn(
                '1',
                [
                    gc.Type('User-generated identifier'),
                ],
            ),
            gc.Refn(
                '10',
                [
                    gc.Type('User-generated identifier'),
                ],
            ),
            gc.Uid('f065a3e8-5c03-4b4a-a89d-6c5e71430a8d'),
            gc.Uid('9441c3f3-74df-42b4-bbc1-fed42fd7f536'),
            gc.Exid(
                '123',
                [
                    gc.ExidType('http://example.com'),
                ],
            ),
            gc.Exid(
                '456',
                [
                    gc.ExidType('http://example.com'),
                ],
            ),
            gc.Note('Note text'),
            gc.Snote(snote_N1_xref),
            gc.Obje(obje_O1_xref),
            gc.Obje(obje_O2_xref),
            gc.Chan(
                [
                    gc.DateExact(
                        '27 MAR 2022',
                        [
                            gc.Time('08:56'),
                        ],
                    ),
                    gc.Note('Change date note 1'),
                    gc.Note('Change date note 2'),
                ]
            ),
            gc.Crea(
                [
                    gc.DateExact(
                        '27 MAR 2022',
                        [
                            gc.Time('08:55'),
                        ],
                    ),
                ]
            ),
        ],
    )
    sour_S2 = gc.RecordSour(
        sour_S2_xref,
        [
            gc.Titl('Source Two'),
        ],
    )
    subm_U1 = gc.RecordSubm(
        subm_U1_xref,
        [
            gc.Name('GEDCOM Steering Committee'),
            gc.Addr(
                """Family History Department
    15 East South Temple Street
    Salt Lake City, UT 84150 USA""",
                [
                    gc.Adr1('Family History Department'),
                    gc.Adr2('15 East South Temple Street'),
                    gc.Adr3('Salt Lake City, UT 84150 USA'),
                    gc.City('Salt Lake City'),
                    gc.Stae('UT'),
                    gc.Post('84150'),
                    gc.Ctry('USA'),
                ],
            ),
            gc.Phon('+1 (555) 555-1212'),
            gc.Phon('+1 (555) 555-1234'),
            gc.Email('GEDCOM@FamilySearch.org'),
            gc.Email('GEDCOM@example.com'),
            gc.Fax('+1 (555) 555-1212'),
            gc.Fax('+1 (555) 555-1234'),
            gc.Www('http://gedcom.io'),
            gc.Www('http://gedcom.info'),
            gc.Obje(
                obje_O1_xref,
                [
                    gc.Crop(
                        [
                            gc.Top(0),
                            gc.Left(0),
                            gc.Height(100),
                            gc.Width(100),
                        ]
                    ),
                    gc.Titl('Title'),
                ],
            ),
            gc.Obje(
                obje_O1_xref,
                [
                    gc.Crop(
                        [
                            gc.Top(100),
                            gc.Left(100),
                        ]
                    ),
                    gc.Titl('Title'),
                ],
            ),
            gc.SubmLang('en-US'),
            gc.SubmLang('en-GB'),
            gc.Refn(
                '1',
                [
                    gc.Type('User-generated identifier'),
                ],
            ),
            gc.Refn(
                '10',
                [
                    gc.Type('User-generated identifier'),
                ],
            ),
            gc.Uid('24132fe0-26f6-4f87-9924-389a4f40f0ec'),
            gc.Uid('b451c8df-5550-473b-a55c-ed31e65c60c8'),
            gc.Exid(
                '123',
                [
                    gc.ExidType('http://example.com'),
                ],
            ),
            gc.Exid(
                '456',
                [
                    gc.ExidType('http://example.com'),
                ],
            ),
            gc.Note(
                'American English',
                [
                    gc.Mime('text/plain'),
                    gc.Lang('en-US'),
                    gc.NoteTran(
                        'British English',
                        [
                            gc.Lang('en-GB'),
                        ],
                    ),
                    gc.Sour(
                        sour_S1_xref,
                        [
                            gc.Page('1'),
                        ],
                    ),
                    gc.Sour(
                        sour_S2_xref,
                        [
                            gc.Page('2'),
                        ],
                    ),
                ],
            ),
            gc.Snote(snote_N1_xref),
            gc.Chan(
                [
                    gc.DateExact(
                        '27 MAR 2022',
                        [
                            gc.Time('08:56'),
                        ],
                    ),
                    gc.Note('Change date note 1'),
                    gc.Note('Change date note 2'),
                ]
            ),
            gc.Crea(
                [
                    gc.DateExact(
                        '27 MAR 2022',
                        [
                            gc.Time('08:55'),
                        ],
                    ),
                ]
            ),
        ],
    )
    subm_U2 = gc.RecordSubm(
        subm_U2_xref,
        [
            gc.Name('Submitter 2'),
        ],
    )

    # Stage the 17 GEDCOM records to generate the ged lines.
    g.stage(header)
    g.stage(fam_F1)
    g.stage(fam_F2)
    g.stage(indi_I1)
    g.stage(indi_I2)
    g.stage(indi_I3)
    g.stage(indi_I4)
    g.stage(obje_O1)
    g.stage(obje_O2)
    g.stage(repo_R1)
    g.stage(repo_R2)
    g.stage(snote_N1)
    g.stage(snote_N2)
    g.stage(sour_S1)
    g.stage(sour_S2)
    g.stage(subm_U1)
    g.stage(subm_U2)

    # Run the following to show the ged file that the above code would produce.
    ged_file = g.show_ged()

    assert file == ged_file
