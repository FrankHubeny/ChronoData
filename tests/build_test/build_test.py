# test/chrono_test.py
"""These tests completely cover the `store` module."""

import pytest

import genedata.classes70 as gc
from genedata.build import Genealogy
from genedata.structure import FamilyXref, IndividualXref

testdata_indi_xref = [
    # Create the individual xref.
    ('str(joe_xref)', '@JOSEPH@'),
    ('str(mary_xref)', '@MARY@'),
    ('str(jesus_xref)', '@JESUS@'),
    ('joe_xref_type', True),
    ('mary_xref_type', True),
    ('jesus_xref_type', True),
    # Create the family xref.
    ('joe_mary_xref.name', 'JOE & MARY'),
    ('joe_mary_xref_type', True),
    ('joe_type', True),
    ('mary_type', True),
    ('jesus_type', True),
]


@pytest.mark.parametrize('test_input,expected', testdata_indi_xref)  # noqa: PT006
def test_create_individual_xrefs(
    test_input: str, expected: str | int | bool
) -> None:
    a = Genealogy()

    # Create the individual xrefs.
    joe_xref = a.individual_xref('joseph')
    mary_xref = a.individual_xref('mary')
    jesus_xref = a.individual_xref('jesus')
    joe_xref_type = isinstance(joe_xref, IndividualXref)  # noqa: F841
    mary_xref_type = isinstance(mary_xref, IndividualXref)  # noqa: F841
    jesus_xref_type = isinstance(jesus_xref, IndividualXref)  # noqa: F841

    # Create the family xref.
    joe_mary_xref = a.family_xref('joe & mary')
    joe_mary_xref_type = isinstance(joe_mary_xref, FamilyXref)  # noqa: F841

    # Create the individual records.
    joe = gc.RecordIndi(joe_xref, gc.Sex('M'))
    mary = gc.RecordIndi(mary_xref, gc.Sex('F'))
    jesus = gc.RecordIndi(
        jesus_xref, [gc.Sex('M'), gc.Famc(joe_mary_xref)]
    )
    joe_type = isinstance(joe, gc.RecordIndi)  # noqa: F841
    mary_type = isinstance(mary, gc.RecordIndi)  # noqa: F841
    jesus_type = isinstance(jesus, gc.RecordIndi)  # noqa: F841

    # Create the family record.
    # joe_husband = Husband(joe_xref, 'Joe is the husband.')
    # mary_wife = Wife(mary_xref, 'Mary is the wife.')
    #jesus_child = Chil(jesus_xref, Phrase('Jesus is the child.'))

    # Create the roles of Joe, Mary and Jesus in the family.
    # joe_husband_type = Checker.verify_type(joe_husband, Husband)  
    # mary_wife_type = Checker.verify_type(mary_wife, Wife)  
    #jesus_child_type = isinstance(jesus_child, Chil) 

    # Create the family.
    joe_mary = gc.RecordFam(joe_mary_xref, [
            gc.FamHusb(joe_xref, gc.Phrase('Joe is the husband.')),
            gc.FamWife(mary_xref,gc.Phrase('Mary is the wife.')),
        ]
    )
    joe_mary_type = isinstance(joe_mary, gc.RecordFam)  # noqa: F841

    # Create the display at this point.
    family = joe_mary.ged().splitlines()  # noqa: F841

    assert eval(test_input) == expected
