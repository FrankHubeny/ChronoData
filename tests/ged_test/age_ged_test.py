# age_ged_test.py
"""Reproduce the `age.ged` output.

This does not include the trailer line.  Nor does it write the file.

Reference:
    [GEDCOM Age test file](https://gedcom.io/testfiles/gedcom70/age.ged)
"""

import genedata.classes70 as gc
from genedata.build import Genealogy
from genedata.methods import Util

ged_version: str = '7.0'
def test_age_ged() -> None:
    """Reproduce the age_ged example file."""
    file = Util.read_ged('tests\\data\\ged_examples\\age.ged')
    
    # Instantiate a Genealogy class.
    g = Genealogy()

    # Instantiate the cross reference identifiers.
    # There were 1 xref identifiers and 0 void identifiers.
    indi_I1_xref = g.individual_xref('I1')

    # Instantiate the header record.
    header = gc.Head([
        gc.Gedc([
            gc.GedcVers('7.0'),
        ]),
        gc.Note('This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.'),
    ])


    # Instantiate the records holding the GED data.
    indi_I1 = gc.RecordIndi(indi_I1_xref, [
        gc.Note('There are many ways to express an age of "zero".'),
        gc.Chr('', [
            gc.Age('0y'),
        ]),
        gc.Chr('', [
            gc.Age('< 0y'),
        ]),
        gc.Chr('', [
            gc.Age('0m'),
        ]),
        gc.Chr('', [
            gc.Age('< 0m'),
        ]),
        gc.Chr('', [
            gc.Age('0w'),
        ]),
        gc.Chr('', [
            gc.Age('< 0w'),
        ]),
        gc.Chr('', [
            gc.Age('0d'),
        ]),
        gc.Chr('', [
            gc.Age('< 0d'),
        ]),
        gc.Chr('', [
            gc.Age('0y 0m'),
        ]),
        gc.Chr('', [
            gc.Age('< 0y 0m'),
        ]),
        gc.Chr('', [
            gc.Age('0y 0w'),
        ]),
        gc.Chr('', [
            gc.Age('< 0y 0w'),
        ]),
        gc.Chr('', [
            gc.Age('0y 0d'),
        ]),
        gc.Chr('', [
            gc.Age('< 0y 0d'),
        ]),
        gc.Chr('', [
            gc.Age('0m 0w'),
        ]),
        gc.Chr('', [
            gc.Age('< 0m 0w'),
        ]),
        gc.Chr('', [
            gc.Age('0m 0d'),
        ]),
        gc.Chr('', [
            gc.Age('< 0m 0d'),
        ]),
        gc.Chr('', [
            gc.Age('0w 0d'),
        ]),
        gc.Chr('', [
            gc.Age('< 0w 0d'),
        ]),
        gc.Chr('', [
            gc.Age('0y 0m 0w'),
        ]),
        gc.Chr('', [
            gc.Age('< 0y 0m 0w'),
        ]),
        gc.Chr('', [
            gc.Age('0y 0m 0d'),
        ]),
        gc.Chr('', [
            gc.Age('< 0y 0m 0d'),
        ]),
        gc.Chr('', [
            gc.Age('0y 0w 0d'),
        ]),
        gc.Chr('', [
            gc.Age('< 0y 0w 0d'),
        ]),
        gc.Chr('', [
            gc.Age('0m 0w 0d'),
        ]),
        gc.Chr('', [
            gc.Age('< 0m 0w 0d'),
        ]),
        gc.Chr('', [
            gc.Age('0y 0m 0w 0d'),
        ]),
        gc.Chr('', [
            gc.Age('< 0y 0m 0w 0d'),
        ]),
        gc.Chr('', [
            gc.Age('', [
                gc.Phrase('Zero'),
            ]),
        ]),
        gc.Note('Various combinations of non-zero ages and age ranges.'),
        gc.Chr('', [
            gc.Age('> 0y'),
        ]),
        gc.Chr('', [
            gc.Age('99y'),
        ]),
        gc.Chr('', [
            gc.Age('> 99y'),
        ]),
        gc.Chr('', [
            gc.Age('< 99y'),
        ]),
        gc.Chr('', [
            gc.Age('> 0m'),
        ]),
        gc.Chr('', [
            gc.Age('11m'),
        ]),
        gc.Chr('', [
            gc.Age('> 11m'),
        ]),
        gc.Chr('', [
            gc.Age('< 11m'),
        ]),
        gc.Chr('', [
            gc.Age('> 0w'),
        ]),
        gc.Chr('', [
            gc.Age('3w'),
        ]),
        gc.Chr('', [
            gc.Age('> 3w'),
        ]),
        gc.Chr('', [
            gc.Age('< 3w'),
        ]),
        gc.Chr('', [
            gc.Age('> 0d'),
        ]),
        gc.Chr('', [
            gc.Age('6d'),
        ]),
        gc.Chr('', [
            gc.Age('> 6d'),
        ]),
        gc.Chr('', [
            gc.Age('< 6d'),
        ]),
        gc.Chr('', [
            gc.Age('> 0y 0m'),
        ]),
        gc.Chr('', [
            gc.Age('99y 11m'),
        ]),
        gc.Chr('', [
            gc.Age('> 99y 11m'),
        ]),
        gc.Chr('', [
            gc.Age('< 99y 11m'),
        ]),
        gc.Chr('', [
            gc.Age('> 0y 0w'),
        ]),
        gc.Chr('', [
            gc.Age('99y 3w'),
        ]),
        gc.Chr('', [
            gc.Age('> 99y 3w'),
        ]),
        gc.Chr('', [
            gc.Age('< 99y 3w'),
        ]),
        gc.Chr('', [
            gc.Age('> 0y 0d'),
        ]),
        gc.Chr('', [
            gc.Age('99y 6d'),
        ]),
        gc.Chr('', [
            gc.Age('> 99y 6d'),
        ]),
        gc.Chr('', [
            gc.Age('< 99y 6d'),
        ]),
        gc.Chr('', [
            gc.Age('> 0m 0w'),
        ]),
        gc.Chr('', [
            gc.Age('11m 3w'),
        ]),
        gc.Chr('', [
            gc.Age('> 11m 3w'),
        ]),
        gc.Chr('', [
            gc.Age('< 11m 3w'),
        ]),
        gc.Chr('', [
            gc.Age('> 0m 0d'),
        ]),
        gc.Chr('', [
            gc.Age('11m 6d'),
        ]),
        gc.Chr('', [
            gc.Age('> 11m 6d'),
        ]),
        gc.Chr('', [
            gc.Age('< 11m 6d'),
        ]),
        gc.Chr('', [
            gc.Age('> 0w 0d'),
        ]),
        gc.Chr('', [
            gc.Age('3w 6d'),
        ]),
        gc.Chr('', [
            gc.Age('> 3w 6d'),
        ]),
        gc.Chr('', [
            gc.Age('< 3w 6d'),
        ]),
        gc.Chr('', [
            gc.Age('> 0y 0m 0w'),
        ]),
        gc.Chr('', [
            gc.Age('99y 11m 3w'),
        ]),
        gc.Chr('', [
            gc.Age('> 99y 11m 3w'),
        ]),
        gc.Chr('', [
            gc.Age('< 99y 11m 3w'),
        ]),
        gc.Chr('', [
            gc.Age('> 0y 0m 0d'),
        ]),
        gc.Chr('', [
            gc.Age('99y 11m 6d'),
        ]),
        gc.Chr('', [
            gc.Age('> 99y 11m 6d'),
        ]),
        gc.Chr('', [
            gc.Age('< 99y 11m 6d'),
        ]),
        gc.Chr('', [
            gc.Age('> 0y 0w 0d'),
        ]),
        gc.Chr('', [
            gc.Age('99y 3w 6d'),
        ]),
        gc.Chr('', [
            gc.Age('> 99y 3w 6d'),
        ]),
        gc.Chr('', [
            gc.Age('< 99y 3w 6d'),
        ]),
        gc.Chr('', [
            gc.Age('> 0m 0w 0d'),
        ]),
        gc.Chr('', [
            gc.Age('99m 3w 6d'),
        ]),
        gc.Chr('', [
            gc.Age('> 99m 3w 6d'),
        ]),
        gc.Chr('', [
            gc.Age('< 99m 3w 6d'),
        ]),
        gc.Chr('', [
            gc.Age('> 0y 0m 0w 0d'),
        ]),
        gc.Chr('', [
            gc.Age('99y 11m 3w 6d'),
        ]),
        gc.Chr('', [
            gc.Age('> 99y 11m 3w 6d'),
        ]),
        gc.Chr('', [
            gc.Age('< 99y 11m 3w 6d'),
        ]),
        gc.Note('Age payloads do not have range restrictions.'),
        gc.Chr('', [
            gc.Age('1y 30m'),
        ]),
        gc.Chr('', [
            gc.Age('1y 100w'),
        ]),
        gc.Chr('', [
            gc.Age('1y 400d'),
        ]),
        gc.Chr('', [
            gc.Age('1m 40d'),
        ]),
        gc.Chr('', [
            gc.Age('1m 10w'),
        ]),
        gc.Chr('', [
            gc.Age('1w 30d'),
        ]),
        gc.Chr('', [
            gc.Age('1y 30m 100w 400d'),
        ]),
    ])


    # Stage the GEDCOM records to generate the ged lines.
    g.stage(header)
    g.stage(indi_I1)

    # Run the following to show the ged file that the above code would produce.
    ged_file = g.show_ged()


    assert file == ged_file


