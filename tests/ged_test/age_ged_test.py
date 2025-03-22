# age_ged_test.py
"""Reproduce the `age.ged` output.

This does not include the trailer line.  Nor does it write the file.

Reference:
    [GEDCOM Age test file](https://gedcom.io/testfiles/gedcom70/age.ged)
"""

from genedata.build import Genealogy
from genedata.classes7 import (
    Age,
    Chr,
    Gedc,
    GedcVers,
    Head,
    Note,
    Phrase,
    RecordIndi,
    Trlr,
)
from genedata.constants import Config
from genedata.structure import IndividualXref  # noqa: F401
from genedata.util import Util


def test_age_ged() -> None:
    """Reproduce the age_ged example file."""
    file = Util.read('tests\\ged_test\\age.ged')
    g = Genealogy('testing')
    indi_xref = g.individual_xref('I1')

    head = Head(
        [
            Gedc(GedcVers(Config.GEDVERSION)),
            Note(
                'This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.'
            ),
        ]
    )

    indi = RecordIndi(
        indi_xref,
        [
            Note('There are many ways to express an age of "zero".'),
            Chr('', Age('0y')),
            Chr('', Age('< 0y')),
            Chr('', Age('0m')),
            Chr('', Age('< 0m')),
            Chr('', Age('0w')),
            Chr('', Age('< 0w')),
            Chr('', Age('0d')),
            Chr('', Age('< 0d')),
            Chr('', Age('0y 0m')),
            Chr('', Age('< 0y 0m')),
            Chr('', Age('0y 0w')),
            Chr('', Age('< 0y 0w')),
            Chr('', Age('0y 0d')),
            Chr('', Age('< 0y 0d')),
            Chr('', Age('0m 0w')),
            Chr('', Age('< 0m 0w')),
            Chr('', Age('0m 0d')),
            Chr('', Age('< 0m 0d')),
            Chr('', Age('0w 0d')),
            Chr('', Age('< 0w 0d')),
            Chr('', Age('0y 0m 0w')),
            Chr('', Age('< 0y 0m 0w')),
            Chr('', Age('0y 0m 0d')),
            Chr('', Age('< 0y 0m 0d')),
            Chr('', Age('0y 0w 0d')),
            Chr('', Age('< 0y 0w 0d')),
            Chr('', Age('0m 0w 0d')),
            Chr('', Age('< 0m 0w 0d')),
            Chr('', Age('0y 0m 0w 0d')),
            Chr('', Age('< 0y 0m 0w 0d')),
            Chr('', Age('', Phrase('Zero'))),
            Note('Various combinations of non-zero ages and age ranges.'),
            Chr('', Age('> 0y')),
            Chr('', Age('99y')),
            Chr('', Age('> 99y')),
            Chr('', Age('< 99y')),
            Chr('', Age('> 0m')),
            Chr('', Age('11m')),
            Chr('', Age('> 11m')),
            Chr('', Age('< 11m')),
            Chr('', Age('> 0w')),
            Chr('', Age('3w')),
            Chr('', Age('> 3w')),
            Chr('', Age('< 3w')),
            Chr('', Age('> 0d')),
            Chr('', Age('6d')),
            Chr('', Age('> 6d')),
            Chr('', Age('< 6d')),
            Chr('', Age('> 0y 0m')),
            Chr('', Age('99y 11m')),
            Chr('', Age('> 99y 11m')),
            Chr('', Age('< 99y 11m')),
            Chr('', Age('> 0y 0w')),
            Chr('', Age('99y 3w')),
            Chr('', Age('> 99y 3w')),
            Chr('', Age('< 99y 3w')),
            Chr('', Age('> 0y 0d')),
            Chr('', Age('99y 6d')),
            Chr('', Age('> 99y 6d')),
            Chr('', Age('< 99y 6d')),
            Chr('', Age('> 0m 0w')),
            Chr('', Age('11m 3w')),
            Chr('', Age('> 11m 3w')),
            Chr('', Age('< 11m 3w')),
            Chr('', Age('> 0m 0d')),
            Chr('', Age('11m 6d')),
            Chr('', Age('> 11m 6d')),
            Chr('', Age('< 11m 6d')),
            Chr('', Age('> 0w 0d')),
            Chr('', Age('3w 6d')),
            Chr('', Age('> 3w 6d')),
            Chr('', Age('< 3w 6d')),
            Chr('', Age('> 0y 0m 0w')),
            Chr('', Age('99y 11m 3w')),
            Chr('', Age('> 99y 11m 3w')),
            Chr('', Age('< 99y 11m 3w')),
            Chr('', Age('> 0y 0m 0d')),
            Chr('', Age('99y 11m 6d')),
            Chr('', Age('> 99y 11m 6d')),
            Chr('', Age('< 99y 11m 6d')),
            Chr('', Age('> 0y 0w 0d')),
            Chr('', Age('99y 3w 6d')),
            Chr('', Age('> 99y 3w 6d')),
            Chr('', Age('< 99y 3w 6d')),
            Chr('', Age('> 0m 0w 0d')),
            Chr('', Age('99m 3w 6d')),
            Chr('', Age('> 99m 3w 6d')),
            Chr('', Age('< 99m 3w 6d')),
            Chr('', Age('> 0y 0m 0w 0d')),
            Chr('', Age('99y 11m 3w 6d')),
            Chr('', Age('> 99y 11m 3w 6d')),
            Chr('', Age('< 99y 11m 3w 6d')),
            Note('Age payloads do not have range restrictions.'),
            Chr('', Age('1y 30m')),
            Chr('', Age('1y 100w')),
            Chr('', Age('1y 400d')),
            Chr('', Age('1m 40d')),
            Chr('', Age('1m 10w')),
            Chr('', Age('1w 30d')),
            Chr('', Age('1y 30m 100w 400d')),
        ],
    )
    gedcom = ''.join([head.ged(), indi.ged(), Trlr().ged()])
    assert file == gedcom


def test_age_ged_code() -> None:
    """Reproduce the age_ged example file."""
    file = Util.read('tests\\ged_test\\age.ged')
    g = Genealogy('testing')
    indi_xref = g.individual_xref('I1')

    head = Head(
        [
            Gedc(GedcVers(Config.GEDVERSION)),
            Note(
                'This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.'
            ),
        ]
    )

    indi = RecordIndi(
        indi_xref,
        [
            Note('There are many ways to express an age of "zero".'),
            Chr('', Age('0y')),
            Chr('', Age('< 0y')),
            Chr('', Age('0m')),
            Chr('', Age('< 0m')),
            Chr('', Age('0w')),
            Chr('', Age('< 0w')),
            Chr('', Age('0d')),
            Chr('', Age('< 0d')),
            Chr('', Age('0y 0m')),
            Chr('', Age('< 0y 0m')),
            Chr('', Age('0y 0w')),
            Chr('', Age('< 0y 0w')),
            Chr('', Age('0y 0d')),
            Chr('', Age('< 0y 0d')),
            Chr('', Age('0m 0w')),
            Chr('', Age('< 0m 0w')),
            Chr('', Age('0m 0d')),
            Chr('', Age('< 0m 0d')),
            Chr('', Age('0w 0d')),
            Chr('', Age('< 0w 0d')),
            Chr('', Age('0y 0m 0w')),
            Chr('', Age('< 0y 0m 0w')),
            Chr('', Age('0y 0m 0d')),
            Chr('', Age('< 0y 0m 0d')),
            Chr('', Age('0y 0w 0d')),
            Chr('', Age('< 0y 0w 0d')),
            Chr('', Age('0m 0w 0d')),
            Chr('', Age('< 0m 0w 0d')),
            Chr('', Age('0y 0m 0w 0d')),
            Chr('', Age('< 0y 0m 0w 0d')),
            Chr('', Age('', Phrase('Zero'))),
            Note('Various combinations of non-zero ages and age ranges.'),
            Chr('', Age('> 0y')),
            Chr('', Age('99y')),
            Chr('', Age('> 99y')),
            Chr('', Age('< 99y')),
            Chr('', Age('> 0m')),
            Chr('', Age('11m')),
            Chr('', Age('> 11m')),
            Chr('', Age('< 11m')),
            Chr('', Age('> 0w')),
            Chr('', Age('3w')),
            Chr('', Age('> 3w')),
            Chr('', Age('< 3w')),
            Chr('', Age('> 0d')),
            Chr('', Age('6d')),
            Chr('', Age('> 6d')),
            Chr('', Age('< 6d')),
            Chr('', Age('> 0y 0m')),
            Chr('', Age('99y 11m')),
            Chr('', Age('> 99y 11m')),
            Chr('', Age('< 99y 11m')),
            Chr('', Age('> 0y 0w')),
            Chr('', Age('99y 3w')),
            Chr('', Age('> 99y 3w')),
            Chr('', Age('< 99y 3w')),
            Chr('', Age('> 0y 0d')),
            Chr('', Age('99y 6d')),
            Chr('', Age('> 99y 6d')),
            Chr('', Age('< 99y 6d')),
            Chr('', Age('> 0m 0w')),
            Chr('', Age('11m 3w')),
            Chr('', Age('> 11m 3w')),
            Chr('', Age('< 11m 3w')),
            Chr('', Age('> 0m 0d')),
            Chr('', Age('11m 6d')),
            Chr('', Age('> 11m 6d')),
            Chr('', Age('< 11m 6d')),
            Chr('', Age('> 0w 0d')),
            Chr('', Age('3w 6d')),
            Chr('', Age('> 3w 6d')),
            Chr('', Age('< 3w 6d')),
            Chr('', Age('> 0y 0m 0w')),
            Chr('', Age('99y 11m 3w')),
            Chr('', Age('> 99y 11m 3w')),
            Chr('', Age('< 99y 11m 3w')),
            Chr('', Age('> 0y 0m 0d')),
            Chr('', Age('99y 11m 6d')),
            Chr('', Age('> 99y 11m 6d')),
            Chr('', Age('< 99y 11m 6d')),
            Chr('', Age('> 0y 0w 0d')),
            Chr('', Age('99y 3w 6d')),
            Chr('', Age('> 99y 3w 6d')),
            Chr('', Age('< 99y 3w 6d')),
            Chr('', Age('> 0m 0w 0d')),
            Chr('', Age('99m 3w 6d')),
            Chr('', Age('> 99m 3w 6d')),
            Chr('', Age('< 99m 3w 6d')),
            Chr('', Age('> 0y 0m 0w 0d')),
            Chr('', Age('99y 11m 3w 6d')),
            Chr('', Age('> 99y 11m 3w 6d')),
            Chr('', Age('< 99y 11m 3w 6d')),
            Note('Age payloads do not have range restrictions.'),
            Chr('', Age('1y 30m')),
            Chr('', Age('1y 100w')),
            Chr('', Age('1y 400d')),
            Chr('', Age('1m 40d')),
            Chr('', Age('1m 10w')),
            Chr('', Age('1w 30d')),
            Chr('', Age('1y 30m 100w 400d')),
        ],
    )
    gedcom = ''.join(
        [
            eval(head.code()).ged(),
            eval(indi.code()).ged(),
            eval(Trlr().code()).ged(),
        ]
    )
    assert file == gedcom
