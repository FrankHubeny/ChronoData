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
from genedata.structure import IndividualXref, MultimediaXref  # noqa: F401
from genedata.util import Util


def test_obje1_ged() -> None:
    """Construct the obje1_ged example file."""
    file = Util.read('tests\\ged_test\\obje-1.ged')
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


def test_obje1_ged_code() -> None:
    # Test generating code, evaluating it and then finding the ged lines.
    file = Util.read('tests\\ged_test\\obje-1.ged')
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
        [
            eval(head.code()).ged(),
            eval(obje1.code()).ged(),
            eval(obje2.code()).ged(),
            eval(indi.code()).ged(),
            eval(Trlr().code()).ged(),
        ]
    )
    assert file == gedcom
