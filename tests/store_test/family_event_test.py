# family_event_test.py
"""Tests to cover the functionality of the FamilyEvent NamedTuple."""

import pytest

from chronodata.constants import String
from chronodata.enums import FamEven, Tag
from chronodata.messages import Msg
from chronodata.store import FamilyEvent, FamilyEventDetail

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
    """Test that all the available tags can be used and payload can be empty."""
    anul = (  # noqa: F841
        FamilyEvent(
            tag=Tag.ANUL,
            payload=String.OCCURRED,
        )
        .ged(1)
        .split('\n')
    )
    anul2 = (  # noqa: F841
        FamilyEvent(
            tag=Tag.ANUL,
            payload=String.EMPTY,
        )
        .ged(1)
        .split('\n')
    )
    cens = (  # noqa: F841
        FamilyEvent(
            tag=Tag.CENS,
            payload=String.OCCURRED,
        )
        .ged(1)
        .split('\n')
    )
    div = (  # noqa: F841
        FamilyEvent(
            tag=Tag.DIV,
            payload=String.OCCURRED,
        )
        .ged(1)
        .split('\n')
    )
    divf = (  # noqa: F841
        FamilyEvent(
            tag=Tag.DIVF,
            payload=String.OCCURRED,
        )
        .ged(1)
        .split('\n')
    )
    enga = (  # noqa: F841
        FamilyEvent(
            tag=Tag.ENGA,
            payload=String.OCCURRED,
        )
        .ged(1)
        .split('\n')
    )
    marb = (  # noqa: F841
        FamilyEvent(
            tag=Tag.MARB,
            payload=String.OCCURRED,
        )
        .ged(1)
        .split('\n')
    )
    marc = (  # noqa: F841
        FamilyEvent(
            tag=Tag.MARC,
            payload=String.OCCURRED,
        )
        .ged(1)
        .split('\n')
    )
    marl = (  # noqa: F841
        FamilyEvent(
            tag=Tag.MARL,
            payload=String.OCCURRED,
        )
        .ged(1)
        .split('\n')
    )
    marr = (  # noqa: F841
        FamilyEvent(
            tag=Tag.MARR,
            payload=String.OCCURRED,
        )
        .ged(1)
        .split('\n')
    )
    mars = (  # noqa: F841
        FamilyEvent(
            tag=Tag.MARS,
            payload=String.OCCURRED,
        )
        .ged(1)
        .split('\n')
    )
    even = (  # noqa: F841
        FamilyEvent(
            tag=Tag.EVEN,
            event_type='some string',
        )
        .ged(1)
        .split('\n')
    )

    assert eval(test_input) == expected


def test_payload() -> None:
    """The payload for all tags except EVEN must be either 'Y' or ''."""
    bad = FamilyEvent(Tag.ANUL, 'S')
    with pytest.raises(
        ValueError, match=Msg.TAG_PAYLOAD.format(Tag.ANUL.value)
    ):
        bad.validate()


def test_event_type() -> None:
    """The event_type for the EVEN tag cannot be empty."""
    bad = FamilyEvent(Tag.EVEN, 'S')
    with pytest.raises(
        ValueError, match=Msg.EMPTY_EVENT_TYPE.format(Tag.EVEN.value)
    ):
        bad.validate()


def test_bad_enum() -> None:
    """This event checks that the tag is for family events."""
    bad = FamilyEvent(Tag.FAM, event_type='something')
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format(Tag.FAM.value, FamEven)
    ):
        bad.validate()


def test_payload_bad_type() -> None:
    """This event checks that the payload fails a type test."""
    bad = FamilyEvent(Tag.ANUL, payload=1)  # type: ignore[arg-type]
    with pytest.raises(
        TypeError,
        match=Msg.WRONG_TYPE.format(bad.payload, type(bad.payload), str),
    ):
        bad.validate()


def test_event_type_bad_type() -> None:
    """This event checks that the event_type fails a type test."""
    bad = FamilyEvent(Tag.ANUL, event_type=1)  # type: ignore[arg-type]
    with pytest.raises(
        TypeError,
        match=Msg.WRONG_TYPE.format(bad.event_type, type(bad.event_type), str),
    ):
        bad.validate()


def test_event_detail_bad_type() -> None:
    """This event checks that the event_detail fails a type test."""
    bad = FamilyEvent(Tag.ANUL, event_detail=1)  # type: ignore[arg-type]
    with pytest.raises(
        TypeError,
        match=Msg.WRONG_TYPE.format(
            bad.event_detail, type(bad.event_detail), FamilyEventDetail | None
        ),
    ):
        bad.validate()
