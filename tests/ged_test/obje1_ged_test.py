# obje1_ged_test.py
"""Reproduce the `obje-1.ged` output.

Reference:
    [GEDCOM Age test file](https://gedcom.io/testfiles/gedcom70/obje-1.ged)
"""

import genedata.classes7 as gc
from genedata.build import Genealogy
from genedata.constants import Config, Default
from genedata.structure import IndividualXref, MultimediaXref  # noqa: F401
from genedata.methods import Util


def test_obje1_ged() -> None:
    """Construct the obje1_ged example file."""
    file = Util.read('tests\\ged_test\\obje-1.ged')
    g = Genealogy('test')
    indi_xref = g.individual_xref('2')
    obje1_xref = g.multimedia_xref('1')
    obje2_xref = g.multimedia_xref('X1')

    head = gc.Head(gc.Gedc(gc.GedcVers(Config.GEDVERSION)))

    obje1 = gc.RecordObje(
        obje1_xref,
        [
            gc.File(
                'example.jpg',
                [
                    gc.Form('image/jpeg', gc.Medi('PHOTO')),
                    gc.Titl('Example Image File'),
                ],
            ),
            gc.File(
                'example.mp3',
                [
                    gc.Form('application/x-mp3'),
                    gc.Titl('Sound Clip'),
                ],
            ),
            gc.Note('note in OBJE record'),
        ],
    )
    obje2 = gc.RecordObje(
        obje2_xref,
        [
            gc.File(
                'gifts.webm',
                gc.Form('application/x-other', gc.Medi('VIDEO')),
            ),
            gc.File(
                'cake.webm',
                gc.Form('application/x-other', gc.Medi('VIDEO')),
            ),
            gc.Note('note in OBJE link'),
        ],
    )
    indi = gc.RecordIndi(
        indi_xref,
        [
            gc.Obje(obje1_xref),
            gc.Obje(obje2_xref, gc.Titl('fifth birthday party')),
        ],
    )

    gedcom = ''.join(
        [head.ged(), obje1.ged(), obje2.ged(), indi.ged(), Default.TRAILER]
    )
    assert file == gedcom


def test_obje1_ged_code() -> None:
    # Test generating code, evaluating it and then finding the ged lines.
    file = Util.read('tests\\ged_test\\obje-1.ged')
    g = Genealogy('test')
    indi_xref = g.individual_xref('2')
    obje1_xref = g.multimedia_xref('1')
    obje2_xref = g.multimedia_xref('X1')

    head = gc.Head(gc.Gedc(gc.GedcVers(Config.GEDVERSION)))

    obje1 = gc.RecordObje(
        obje1_xref,
        [
            gc.File(
                'example.jpg',
                [
                    gc.Form('image/jpeg', gc.Medi('PHOTO')),
                    gc.Titl('Example Image File'),
                ],
            ),
            gc.File(
                'example.mp3',
                [
                    gc.Form('application/x-mp3'),
                    gc.Titl('Sound Clip'),
                ],
            ),
            gc.Note('note in OBJE record'),
        ],
    )
    obje2 = gc.RecordObje(
        obje2_xref,
        [
            gc.File(
                'gifts.webm',
                gc.Form('application/x-other', gc.Medi('VIDEO')),
            ),
            gc.File(
                'cake.webm',
                gc.Form('application/x-other', gc.Medi('VIDEO')),
            ),
            gc.Note('note in OBJE link'),
        ],
    )
    indi = gc.RecordIndi(
        indi_xref,
        [
            gc.Obje(obje1_xref),
            gc.Obje(obje2_xref, gc.Titl('fifth birthday party')),
        ],
    )

    gedcom = ''.join(
        [
            eval(head.code()).ged(),
            eval(obje1.code()).ged(),
            eval(obje2.code()).ged(),
            eval(indi.code()).ged(),
            Default.TRAILER,
        ]
    )
    assert file == gedcom
