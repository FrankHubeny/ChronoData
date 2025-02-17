# test/chrono_test.py
"""These tests completely cover the `store` module."""

import pytest

from genedata.build import Genealogy
from genedata.gedcom import Tag
from genedata.store import (
    Checker,
    Child,
    Family,
    FamilyChild,
    FamilyXref,
    Individual,
    IndividualXref,
    Phrase,
)

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
    # Validate the objects.
    ('joe.validate()', True),
    ('mary.validate()', True),
    ('jesus.validate()', True),
    ('joe_mary.validate()', True),
    ('jesus_child_type', True),
    ('joe_mary_type', True),
    # Validate the above objects.
    ('jesus_child.validate()', True),
    # Check display at this point
    ('family[0]', '0 @JOE_&_MARY@ FAM'),
    ('family[1]', '1 HUSB @JOSEPH@'),
    ('family[2]', '2 PHRASE Joe is the husband.'),
    ('family[3]', '1 WIFE @MARY@'),
    ('family[4]', '2 PHRASE Mary is the wife.'),
    ('family[5]', '1 CHIL @JESUS@'),
    ('family[6]', '2 PHRASE Jesus is the child.'),
]


@pytest.mark.parametrize('test_input,expected', testdata_indi_xref)  # noqa: PT006
def test_create_individual_xrefs(
    test_input: str, expected: str | int | bool
) -> None:
    a = Genealogy('test')

    # Create the individual xrefs.
    joe_xref = a.individual_xref('joseph')
    mary_xref = a.individual_xref('mary')
    jesus_xref = a.individual_xref('jesus')
    joe_xref_type = Checker.verify_type(joe_xref, IndividualXref)  # noqa: F841
    mary_xref_type = Checker.verify_type(mary_xref, IndividualXref)  # noqa: F841
    jesus_xref_type = Checker.verify_type(jesus_xref, IndividualXref)  # noqa: F841

    # Create the family xref.
    joe_mary_xref = a.family_xref('joe & mary')
    joe_mary_xref_type = Checker.verify_type(joe_mary_xref, FamilyXref)  # noqa: F841

    # Create the individual records.
    joe = Individual(xref=joe_xref, sex=Tag.M)
    mary = Individual(xref=mary_xref, sex=Tag.F)
    jesus = Individual(
        xref=jesus_xref, sex=Tag.M, families_child=[FamilyChild(joe_mary_xref),]
    )
    joe_type = Checker.verify_type(joe, Individual)  # noqa: F841
    mary_type = Checker.verify_type(mary, Individual)  # noqa: F841
    jesus_type = Checker.verify_type(jesus, Individual)  # noqa: F841

    # Create the family record.
    # joe_husband = Husband(joe_xref, 'Joe is the husband.')
    # mary_wife = Wife(mary_xref, 'Mary is the wife.')
    jesus_child = Child(jesus_xref, Phrase('Jesus is the child.'))

    # Create the roles of Joe, Mary and Jesus in the family.
    # joe_husband_type = Checker.verify_type(joe_husband, Husband)  
    # mary_wife_type = Checker.verify_type(mary_wife, Wife)  
    jesus_child_type = Checker.verify_type(jesus_child, Child)  # noqa: F841

    # Create the family.
    joe_mary = Family(
        xref=joe_mary_xref,
        husband=joe_xref,
        husband_phrase=Phrase('Joe is the husband.'),
        wife=mary_xref,
        wife_phrase=Phrase('Mary is the wife.'),
        children=[jesus_child,],
    )
    joe_mary_type = Checker.verify_type(joe_mary, Family)  # noqa: F841

    # Create the display at this point.
    family = joe_mary.ged().splitlines()  # noqa: F841

    assert eval(test_input) == expected
