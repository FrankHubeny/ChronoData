# obje1_ged_test.py
"""Reproduce the `obje-1.ged` output.

Reference:
    [GEDCOM Age test file](https://gedcom.io/testfiles/gedcom70/obje-1.ged)
"""

from genedata.build import Genealogy
from genedata.classes7 import (
    File,
    Form,
    Gedc,
    GedcVers,
    Head,
    Medi,
    Note,
    Obje,
    RecordIndi,
    RecordObje,
    Titl,
    Trlr,
)
from genedata.constants import Config


def test_obje1_ged() -> None:
    """Construct the obje1_ged example file."""
    file = """0 HEAD
1 GEDC
2 VERS 7.0
0 @1@ OBJE
1 FILE example.jpg
2 FORM image/jpeg
3 MEDI PHOTO
2 TITL Example Image File
1 FILE example.mp3
2 FORM application/x-mp3
2 TITL Sound Clip
1 NOTE note in OBJE record
0 @X1@ OBJE
1 FILE gifts.webm
2 FORM application/x-other
3 MEDI VIDEO
1 FILE cake.webm
2 FORM application/x-other
3 MEDI VIDEO
1 NOTE note in OBJE link
0 @2@ INDI
1 OBJE @1@
1 OBJE @X1@
2 TITL fifth birthday party
0 TRLR"""

    g = Genealogy('test')
    indi_xref = g.individual_xref('2')
    obje1_xref = g.multimedia_xref('1')
    obje2_xref = g.multimedia_xref('X1')

    head = Head(Gedc(GedcVers(Config.GEDVERSION)))

    obje1 = RecordObje(
        obje1_xref,
        [
            File(
                'example.jpg',
                [
                    Form('image/jpeg', Medi('PHOTO')),
                    Titl('Example Image File'),
                ],
            ),
            File(
                'example.mp3',
                [
                    Form('application/x-mp3'),
                    Titl('Sound Clip'),
                ],
            ),
            Note('note in OBJE record'),
        ],
    )
    obje2 = RecordObje(
        obje2_xref,
        [
            File(
                'gifts.webm',
                Form('application/x-other', Medi('VIDEO')),
            ),
            File(
                'cake.webm',
                Form('application/x-other', Medi('VIDEO')),
            ),
            Note('note in OBJE link'),
        ],
    )
    indi = RecordIndi(
        indi_xref,
        [
            Obje(obje1_xref),
            Obje(obje2_xref, Titl('fifth birthday party')),
        ],
    )

    gedcom = ''.join(
        [head.ged(), obje1.ged(), obje2.ged(), indi.ged(), Trlr().ged()]
    )
    assert file == gedcom
