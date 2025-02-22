# xref_ged_test.py
"""Reproduce the `xref.ged` output.

This does not include the trailer line.  Nor does it write the file.

Reference:
    [GEDCOM Age test file](https://gedcom.io/testfiles/gedcom70/xref.ged)
"""

import pytest

from genedata.build import Genealogy
from genedata.store import (
    Header,
    Individual,
    Note,
)

xref_data = [
    ('gedcom[0]', '0 HEAD'),
    ('gedcom[1]', '1 GEDC'),
    ('gedcom[2]', '2 VERS 7.0'),
    ('gedcom[3]', '0 INDI'),
    ('gedcom[4]', '1 NOTE This individual has no cross-reference identifier.'),
    ('gedcom[5]', '0 @I1@ INDI'),
    ('gedcom[6]', '0 @I@ INDI'),
    ('gedcom[7]', '0 @1@ INDI'),
    ('gedcom[8]', '0 @_@ INDI'),
    ('gedcom[9]', '0 @0XFFFFFFFF@ INDI'),
    (
        'gedcom[10]',
        '0 @THEXREFPRODUCTIONDOESNOTHAVEAMAXIMUMLENGTHSOTHISISATESTOFALONGCROSSREFERENCEIDENTIFIER@ INDI',
    ),
]


@pytest.mark.parametrize('test_input,expected', xref_data)  # noqa: PT006
def test_xref_ged(test_input: str, expected: str | int | bool) -> None:  # noqa: ARG001
    # Test constructing the xref_ged test data.
    g = Genealogy('testing')
    head = Header(
        note=Note(
            'This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.'
        )
    ).ged()
    indi4 = Individual(xref=g.individual_xref('1')).ged()
    indi1 = Individual(
        notes=Note('This individual has no cross-reference identifier.')
    ).ged()
    indi2 = Individual(xref=g.individual_xref('I', True)).ged()
    indi3 = Individual(xref=g.individual_xref('I')).ged()
    indi5 = Individual(xref=g.individual_xref('_')).ged()
    indi6 = Individual(xref=g.individual_xref('0XFFFFFFFF')).ged()
    indi7 = Individual(
        xref=g.individual_xref(
            'THEXREFPRODUCTIONDOESNOTHAVEAMAXIMUMLENGTHSOTHISISATESTOFALONGCROSSREFERENCEIDENTIFIER'
        )
    ).ged()

    gedcom = ''.join(
        [head, indi1, indi2, indi3, indi4, indi5, indi6, indi7]
    ).split('\n')  # noqa: F841
