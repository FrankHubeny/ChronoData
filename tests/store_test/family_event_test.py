# family_event_test.py
"""Tests to cover the functionality of the FamilyEvent NamedTuple."""

import pytest

from chronodata.constants import String
from chronodata.enums import Tag
from chronodata.messages import Msg
from chronodata.store import FamilyEvent

testdata_minimal = [
    ('anul[0]', '1 ANUL Y'),
    ('anul2[0]', '1 ANUL'),
    ('cens[0]', '1 CENS Y'),
    ('div[0]', '1 DIV Y'),
    ('divf[0]', '1 DIVF Y'),
    ('enga[0]', '1 ENGA Y'),
    ('marb[0]', '1 MARB Y'),
    ('marc[0]', '1 MARC Y'),
    ('marl[0]', '1 MARL Y'),
    ('marr[0]', '1 MARR Y'),
    ('mars[0]', '1 MARS Y'),
    ('even[0]', '1 EVEN Y'),
]


@pytest.mark.parametrize('test_input,expected', testdata_minimal)  # noqa: PT006
def test_minimal(test_input: str, expected: str | int | bool) -> None:
    anul = FamilyEvent(  # noqa: F841
        tag = Tag.ANUL,
        payload = String.OCCURRED,
    ).ged(1).split('\n')
    anul2 = FamilyEvent(  # noqa: F841
        tag = Tag.ANUL,
        payload = String.EMPTY,
    ).ged(1).split('\n')
    cens = FamilyEvent(  # noqa: F841
        tag = Tag.CENS,
        payload = String.OCCURRED,
    ).ged(1).split('\n')
    div = FamilyEvent(  # noqa: F841
        tag = Tag.DIV,
        payload = String.OCCURRED,
    ).ged(1).split('\n')
    divf = FamilyEvent(  # noqa: F841
        tag = Tag.DIVF,
        payload = String.OCCURRED,
    ).ged(1).split('\n')
    enga = FamilyEvent(  # noqa: F841
        tag = Tag.ENGA,
        payload = String.OCCURRED,
    ).ged(1).split('\n')
    marb = FamilyEvent(  # noqa: F841
        tag = Tag.MARB,
        payload = String.OCCURRED,
    ).ged(1).split('\n')
    marc = FamilyEvent(  # noqa: F841
        tag = Tag.MARC,
        payload = String.OCCURRED,
    ).ged(1).split('\n')
    marl = FamilyEvent(  # noqa: F841
        tag = Tag.MARL,
        payload = String.OCCURRED,
    ).ged(1).split('\n')
    marr = FamilyEvent(  # noqa: F841
        tag = Tag.MARR,
        payload = String.OCCURRED,
    ).ged(1).split('\n')
    mars = FamilyEvent(  # noqa: F841
        tag = Tag.MARS,
        payload = String.OCCURRED,
    ).ged(1).split('\n')
    even = FamilyEvent(  # noqa: F841
        tag = Tag.EVEN,
        event_type = 'some string',
    ).ged(1).split('\n')

    assert eval(test_input) == expected


def test_payload() -> None:
    anul = FamilyEvent(Tag.ANUL, 'S')
    with pytest.raises(ValueError, match=Msg.TAG_PAYLOAD.format(Tag.ANUL.value)):
        anul.validate()

def test_event_type() -> None:
    even = FamilyEvent(Tag.EVEN, 'S')
    with pytest.raises(ValueError, match=Msg.EMPTY_EVENT_TYPE.format(Tag.EVEN.value)):
        even.validate()