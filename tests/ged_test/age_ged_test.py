# age_ged_test.py
"""Reproduce the `age.ged` output.

This does not include the trailer line.  Nor does it write the file.

Reference:
    [GEDCOM Age test file](https://gedcom.io/testfiles/gedcom70/age.ged)
"""

import genedata.classes7 as gc
from genedata.build import Genealogy
from genedata.constants import Config, Default
from genedata.structure import IndividualXref  # noqa: F401
from genedata.methods import Util


def test_age_ged() -> None:
    """Reproduce the age_ged example file."""
    file = Util.read('tests\\ged_test\\age.ged')
    g = Genealogy('testing')
    indi_xref = g.individual_xref('I1')

    head = gc.Head(
        [
            gc.Gedc(gc.GedcVers(Config.GEDVERSION)),
            gc.Note(
                'This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.'
            ),
        ]
    )

    indi = gc.RecordIndi(
        indi_xref,
        [
            gc.Note('There are many ways to express an age of "zero".'),
            gc.Chr('', gc.Age('0y')),
            gc.Chr('', gc.Age('< 0y')),
            gc.Chr('', gc.Age('0m')),
            gc.Chr('', gc.Age('< 0m')),
            gc.Chr('', gc.Age('0w')),
            gc.Chr('', gc.Age('< 0w')),
            gc.Chr('', gc.Age('0d')),
            gc.Chr('', gc.Age('< 0d')),
            gc.Chr('', gc.Age('0y 0m')),
            gc.Chr('', gc.Age('< 0y 0m')),
            gc.Chr('', gc.Age('0y 0w')),
            gc.Chr('', gc.Age('< 0y 0w')),
            gc.Chr('', gc.Age('0y 0d')),
            gc.Chr('', gc.Age('< 0y 0d')),
            gc.Chr('', gc.Age('0m 0w')),
            gc.Chr('', gc.Age('< 0m 0w')),
            gc.Chr('', gc.Age('0m 0d')),
            gc.Chr('', gc.Age('< 0m 0d')),
            gc.Chr('', gc.Age('0w 0d')),
            gc.Chr('', gc.Age('< 0w 0d')),
            gc.Chr('', gc.Age('0y 0m 0w')),
            gc.Chr('', gc.Age('< 0y 0m 0w')),
            gc.Chr('', gc.Age('0y 0m 0d')),
            gc.Chr('', gc.Age('< 0y 0m 0d')),
            gc.Chr('', gc.Age('0y 0w 0d')),
            gc.Chr('', gc.Age('< 0y 0w 0d')),
            gc.Chr('', gc.Age('0m 0w 0d')),
            gc.Chr('', gc.Age('< 0m 0w 0d')),
            gc.Chr('', gc.Age('0y 0m 0w 0d')),
            gc.Chr('', gc.Age('< 0y 0m 0w 0d')),
            gc.Chr('', gc.Age('', gc.Phrase('Zero'))),
            gc.Note('Various combinations of non-zero ages and age ranges.'),
            gc.Chr('', gc.Age('> 0y')),
            gc.Chr('', gc.Age('99y')),
            gc.Chr('', gc.Age('> 99y')),
            gc.Chr('', gc.Age('< 99y')),
            gc.Chr('', gc.Age('> 0m')),
            gc.Chr('', gc.Age('11m')),
            gc.Chr('', gc.Age('> 11m')),
            gc.Chr('', gc.Age('< 11m')),
            gc.Chr('', gc.Age('> 0w')),
            gc.Chr('', gc.Age('3w')),
            gc.Chr('', gc.Age('> 3w')),
            gc.Chr('', gc.Age('< 3w')),
            gc.Chr('', gc.Age('> 0d')),
            gc.Chr('', gc.Age('6d')),
            gc.Chr('', gc.Age('> 6d')),
            gc.Chr('', gc.Age('< 6d')),
            gc.Chr('', gc.Age('> 0y 0m')),
            gc.Chr('', gc.Age('99y 11m')),
            gc.Chr('', gc.Age('> 99y 11m')),
            gc.Chr('', gc.Age('< 99y 11m')),
            gc.Chr('', gc.Age('> 0y 0w')),
            gc.Chr('', gc.Age('99y 3w')),
            gc.Chr('', gc.Age('> 99y 3w')),
            gc.Chr('', gc.Age('< 99y 3w')),
            gc.Chr('', gc.Age('> 0y 0d')),
            gc.Chr('', gc.Age('99y 6d')),
            gc.Chr('', gc.Age('> 99y 6d')),
            gc.Chr('', gc.Age('< 99y 6d')),
            gc.Chr('', gc.Age('> 0m 0w')),
            gc.Chr('', gc.Age('11m 3w')),
            gc.Chr('', gc.Age('> 11m 3w')),
            gc.Chr('', gc.Age('< 11m 3w')),
            gc.Chr('', gc.Age('> 0m 0d')),
            gc.Chr('', gc.Age('11m 6d')),
            gc.Chr('', gc.Age('> 11m 6d')),
            gc.Chr('', gc.Age('< 11m 6d')),
            gc.Chr('', gc.Age('> 0w 0d')),
            gc.Chr('', gc.Age('3w 6d')),
            gc.Chr('', gc.Age('> 3w 6d')),
            gc.Chr('', gc.Age('< 3w 6d')),
            gc.Chr('', gc.Age('> 0y 0m 0w')),
            gc.Chr('', gc.Age('99y 11m 3w')),
            gc.Chr('', gc.Age('> 99y 11m 3w')),
            gc.Chr('', gc.Age('< 99y 11m 3w')),
            gc.Chr('', gc.Age('> 0y 0m 0d')),
            gc.Chr('', gc.Age('99y 11m 6d')),
            gc.Chr('', gc.Age('> 99y 11m 6d')),
            gc.Chr('', gc.Age('< 99y 11m 6d')),
            gc.Chr('', gc.Age('> 0y 0w 0d')),
            gc.Chr('', gc.Age('99y 3w 6d')),
            gc.Chr('', gc.Age('> 99y 3w 6d')),
            gc.Chr('', gc.Age('< 99y 3w 6d')),
            gc.Chr('', gc.Age('> 0m 0w 0d')),
            gc.Chr('', gc.Age('99m 3w 6d')),
            gc.Chr('', gc.Age('> 99m 3w 6d')),
            gc.Chr('', gc.Age('< 99m 3w 6d')),
            gc.Chr('', gc.Age('> 0y 0m 0w 0d')),
            gc.Chr('', gc.Age('99y 11m 3w 6d')),
            gc.Chr('', gc.Age('> 99y 11m 3w 6d')),
            gc.Chr('', gc.Age('< 99y 11m 3w 6d')),
            gc.Note('Age payloads do not have range restrictions.'),
            gc.Chr('', gc.Age('1y 30m')),
            gc.Chr('', gc.Age('1y 100w')),
            gc.Chr('', gc.Age('1y 400d')),
            gc.Chr('', gc.Age('1m 40d')),
            gc.Chr('', gc.Age('1m 10w')),
            gc.Chr('', gc.Age('1w 30d')),
            gc.Chr('', gc.Age('1y 30m 100w 400d')),
        ],
    )
    gedcom = ''.join([head.ged(), indi.ged(), Default.TRAILER])
    assert file == gedcom


def test_age_ged_code() -> None:
    """Reproduce the age_ged example file."""
    file = Util.read('tests\\ged_test\\age.ged')
    g = Genealogy('testing')
    indi_xref = g.individual_xref('I1')

    head = gc.Head(
        [
            gc.Gedc(gc.GedcVers(Config.GEDVERSION)),
            gc.Note(
                'This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.'
            ),
        ]
    )

    indi = gc.RecordIndi(
        indi_xref,
        [
            gc.Note('There are many ways to express an age of "zero".'),
            gc.Chr('', gc.Age('0y')),
            gc.Chr('', gc.Age('< 0y')),
            gc.Chr('', gc.Age('0m')),
            gc.Chr('', gc.Age('< 0m')),
            gc.Chr('', gc.Age('0w')),
            gc.Chr('', gc.Age('< 0w')),
            gc.Chr('', gc.Age('0d')),
            gc.Chr('', gc.Age('< 0d')),
            gc.Chr('', gc.Age('0y 0m')),
            gc.Chr('', gc.Age('< 0y 0m')),
            gc.Chr('', gc.Age('0y 0w')),
            gc.Chr('', gc.Age('< 0y 0w')),
            gc.Chr('', gc.Age('0y 0d')),
            gc.Chr('', gc.Age('< 0y 0d')),
            gc.Chr('', gc.Age('0m 0w')),
            gc.Chr('', gc.Age('< 0m 0w')),
            gc.Chr('', gc.Age('0m 0d')),
            gc.Chr('', gc.Age('< 0m 0d')),
            gc.Chr('', gc.Age('0w 0d')),
            gc.Chr('', gc.Age('< 0w 0d')),
            gc.Chr('', gc.Age('0y 0m 0w')),
            gc.Chr('', gc.Age('< 0y 0m 0w')),
            gc.Chr('', gc.Age('0y 0m 0d')),
            gc.Chr('', gc.Age('< 0y 0m 0d')),
            gc.Chr('', gc.Age('0y 0w 0d')),
            gc.Chr('', gc.Age('< 0y 0w 0d')),
            gc.Chr('', gc.Age('0m 0w 0d')),
            gc.Chr('', gc.Age('< 0m 0w 0d')),
            gc.Chr('', gc.Age('0y 0m 0w 0d')),
            gc.Chr('', gc.Age('< 0y 0m 0w 0d')),
            gc.Chr('', gc.Age('', gc.Phrase('Zero'))),
            gc.Note('Various combinations of non-zero ages and age ranges.'),
            gc.Chr('', gc.Age('> 0y')),
            gc.Chr('', gc.Age('99y')),
            gc.Chr('', gc.Age('> 99y')),
            gc.Chr('', gc.Age('< 99y')),
            gc.Chr('', gc.Age('> 0m')),
            gc.Chr('', gc.Age('11m')),
            gc.Chr('', gc.Age('> 11m')),
            gc.Chr('', gc.Age('< 11m')),
            gc.Chr('', gc.Age('> 0w')),
            gc.Chr('', gc.Age('3w')),
            gc.Chr('', gc.Age('> 3w')),
            gc.Chr('', gc.Age('< 3w')),
            gc.Chr('', gc.Age('> 0d')),
            gc.Chr('', gc.Age('6d')),
            gc.Chr('', gc.Age('> 6d')),
            gc.Chr('', gc.Age('< 6d')),
            gc.Chr('', gc.Age('> 0y 0m')),
            gc.Chr('', gc.Age('99y 11m')),
            gc.Chr('', gc.Age('> 99y 11m')),
            gc.Chr('', gc.Age('< 99y 11m')),
            gc.Chr('', gc.Age('> 0y 0w')),
            gc.Chr('', gc.Age('99y 3w')),
            gc.Chr('', gc.Age('> 99y 3w')),
            gc.Chr('', gc.Age('< 99y 3w')),
            gc.Chr('', gc.Age('> 0y 0d')),
            gc.Chr('', gc.Age('99y 6d')),
            gc.Chr('', gc.Age('> 99y 6d')),
            gc.Chr('', gc.Age('< 99y 6d')),
            gc.Chr('', gc.Age('> 0m 0w')),
            gc.Chr('', gc.Age('11m 3w')),
            gc.Chr('', gc.Age('> 11m 3w')),
            gc.Chr('', gc.Age('< 11m 3w')),
            gc.Chr('', gc.Age('> 0m 0d')),
            gc.Chr('', gc.Age('11m 6d')),
            gc.Chr('', gc.Age('> 11m 6d')),
            gc.Chr('', gc.Age('< 11m 6d')),
            gc.Chr('', gc.Age('> 0w 0d')),
            gc.Chr('', gc.Age('3w 6d')),
            gc.Chr('', gc.Age('> 3w 6d')),
            gc.Chr('', gc.Age('< 3w 6d')),
            gc.Chr('', gc.Age('> 0y 0m 0w')),
            gc.Chr('', gc.Age('99y 11m 3w')),
            gc.Chr('', gc.Age('> 99y 11m 3w')),
            gc.Chr('', gc.Age('< 99y 11m 3w')),
            gc.Chr('', gc.Age('> 0y 0m 0d')),
            gc.Chr('', gc.Age('99y 11m 6d')),
            gc.Chr('', gc.Age('> 99y 11m 6d')),
            gc.Chr('', gc.Age('< 99y 11m 6d')),
            gc.Chr('', gc.Age('> 0y 0w 0d')),
            gc.Chr('', gc.Age('99y 3w 6d')),
            gc.Chr('', gc.Age('> 99y 3w 6d')),
            gc.Chr('', gc.Age('< 99y 3w 6d')),
            gc.Chr('', gc.Age('> 0m 0w 0d')),
            gc.Chr('', gc.Age('99m 3w 6d')),
            gc.Chr('', gc.Age('> 99m 3w 6d')),
            gc.Chr('', gc.Age('< 99m 3w 6d')),
            gc.Chr('', gc.Age('> 0y 0m 0w 0d')),
            gc.Chr('', gc.Age('99y 11m 3w 6d')),
            gc.Chr('', gc.Age('> 99y 11m 3w 6d')),
            gc.Chr('', gc.Age('< 99y 11m 3w 6d')),
            gc.Note('Age payloads do not have range restrictions.'),
            gc.Chr('', gc.Age('1y 30m')),
            gc.Chr('', gc.Age('1y 100w')),
            gc.Chr('', gc.Age('1y 400d')),
            gc.Chr('', gc.Age('1m 40d')),
            gc.Chr('', gc.Age('1m 10w')),
            gc.Chr('', gc.Age('1w 30d')),
            gc.Chr('', gc.Age('1y 30m 100w 400d')),
        ],
    )
    gedcom = ''.join(
        [
            eval(head.code()).ged(),
            eval(indi.code()).ged(),
            Default.TRAILER,
        ]
    )
    assert file == gedcom
    