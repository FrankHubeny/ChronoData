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


def test_age_ged() -> None:
    """Reproduce the age_ged example file."""

    file = """0 HEAD
1 GEDC
2 VERS 7.0
1 NOTE This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.
0 @I1@ INDI
1 NOTE There are many ways to express an age of "zero".
1 CHR
2 AGE 0y
1 CHR
2 AGE < 0y
1 CHR
2 AGE 0m
1 CHR
2 AGE < 0m
1 CHR
2 AGE 0w
1 CHR
2 AGE < 0w
1 CHR
2 AGE 0d
1 CHR
2 AGE < 0d
1 CHR
2 AGE 0y 0m
1 CHR
2 AGE < 0y 0m
1 CHR
2 AGE 0y 0w
1 CHR
2 AGE < 0y 0w
1 CHR
2 AGE 0y 0d
1 CHR
2 AGE < 0y 0d
1 CHR
2 AGE 0m 0w
1 CHR
2 AGE < 0m 0w
1 CHR
2 AGE 0m 0d
1 CHR
2 AGE < 0m 0d
1 CHR
2 AGE 0w 0d
1 CHR
2 AGE < 0w 0d
1 CHR
2 AGE 0y 0m 0w
1 CHR
2 AGE < 0y 0m 0w
1 CHR
2 AGE 0y 0m 0d
1 CHR
2 AGE < 0y 0m 0d
1 CHR
2 AGE 0y 0w 0d
1 CHR
2 AGE < 0y 0w 0d
1 CHR
2 AGE 0m 0w 0d
1 CHR
2 AGE < 0m 0w 0d
1 CHR
2 AGE 0y 0m 0w 0d
1 CHR
2 AGE < 0y 0m 0w 0d
1 CHR
2 AGE
3 PHRASE Zero
1 NOTE Various combinations of non-zero ages and age ranges.
1 CHR
2 AGE > 0y
1 CHR
2 AGE 99y
1 CHR
2 AGE > 99y
1 CHR
2 AGE < 99y
1 CHR
2 AGE > 0m
1 CHR
2 AGE 11m
1 CHR
2 AGE > 11m
1 CHR
2 AGE < 11m
1 CHR
2 AGE > 0w
1 CHR
2 AGE 3w
1 CHR
2 AGE > 3w
1 CHR
2 AGE < 3w
1 CHR
2 AGE > 0d
1 CHR
2 AGE 6d
1 CHR
2 AGE > 6d
1 CHR
2 AGE < 6d
1 CHR
2 AGE > 0y 0m
1 CHR
2 AGE 99y 11m
1 CHR
2 AGE > 99y 11m
1 CHR
2 AGE < 99y 11m
1 CHR
2 AGE > 0y 0w
1 CHR
2 AGE 99y 3w
1 CHR
2 AGE > 99y 3w
1 CHR
2 AGE < 99y 3w
1 CHR
2 AGE > 0y 0d
1 CHR
2 AGE 99y 6d
1 CHR
2 AGE > 99y 6d
1 CHR
2 AGE < 99y 6d
1 CHR
2 AGE > 0m 0w
1 CHR
2 AGE 11m 3w
1 CHR
2 AGE > 11m 3w
1 CHR
2 AGE < 11m 3w
1 CHR
2 AGE > 0m 0d
1 CHR
2 AGE 11m 6d
1 CHR
2 AGE > 11m 6d
1 CHR
2 AGE < 11m 6d
1 CHR
2 AGE > 0w 0d
1 CHR
2 AGE 3w 6d
1 CHR
2 AGE > 3w 6d
1 CHR
2 AGE < 3w 6d
1 CHR
2 AGE > 0y 0m 0w
1 CHR
2 AGE 99y 11m 3w
1 CHR
2 AGE > 99y 11m 3w
1 CHR
2 AGE < 99y 11m 3w
1 CHR
2 AGE > 0y 0m 0d
1 CHR
2 AGE 99y 11m 6d
1 CHR
2 AGE > 99y 11m 6d
1 CHR
2 AGE < 99y 11m 6d
1 CHR
2 AGE > 0y 0w 0d
1 CHR
2 AGE 99y 3w 6d
1 CHR
2 AGE > 99y 3w 6d
1 CHR
2 AGE < 99y 3w 6d
1 CHR
2 AGE > 0m 0w 0d
1 CHR
2 AGE 99m 3w 6d
1 CHR
2 AGE > 99m 3w 6d
1 CHR
2 AGE < 99m 3w 6d
1 CHR
2 AGE > 0y 0m 0w 0d
1 CHR
2 AGE 99y 11m 3w 6d
1 CHR
2 AGE > 99y 11m 3w 6d
1 CHR
2 AGE < 99y 11m 3w 6d
1 NOTE Age payloads do not have range restrictions.
1 CHR
2 AGE 1y 30m
1 CHR
2 AGE 1y 100w
1 CHR
2 AGE 1y 400d
1 CHR
2 AGE 1m 40d
1 CHR
2 AGE 1m 10w
1 CHR
2 AGE 1w 30d
1 CHR
2 AGE 1y 30m 100w 400d
0 TRLR"""

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
