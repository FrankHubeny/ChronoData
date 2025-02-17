# family_event_test.py
"""Tests to cover the functionality of the FamilyEvent NamedTuple."""

import pytest

from genedata.gedcom import FamEven, Tag
from genedata.messages import Msg
from genedata.store import (
    FamilyEvent,
    FamilyEventDetail,
)

testdata_minimal = [
    ('anul[0]', '1 ANUL Y'),
    ('anul2[0]', '1 ANUL'),
    ('cens[0]', '1 CENS Y'),
    ('div[0]', '1 DIV'),
    ('divf[0]', '1 DIVF Y'),
    ('enga[0]', '1 ENGA'),
    ('marb[0]', '1 MARB Y'),
    ('marc[0]', '1 MARC'),
    ('marl[0]', '1 MARL Y'),
    ('marr[0]', '1 MARR'),
    ('mars[0]', '1 MARS Y'),
    ('even[0]', '1 EVEN'),
]


@pytest.mark.parametrize('test_input,expected', testdata_minimal)  # noqa: PT006
def test_minimal(test_input: str, expected: str | int | bool) -> None:
    """Test that all the available tags can be used and payload can be empty."""
    anul = (  # noqa: F841
        FamilyEvent(
            Tag.ANUL,
            True,
            event_detail=None,
        )
        .ged(1)
        .split('\n')
    )
    anul2 = (  # noqa: F841
        FamilyEvent(
            Tag.ANUL,
            False,
            event_detail=None,
        )
        .ged(1)
        .split('\n')
    )
    cens = (  # noqa: F841
        FamilyEvent(
            Tag.CENS,
            True,
            event_detail=None,
        )
        .ged(1)
        .split('\n')
    )
    div = (  # noqa: F841
        FamilyEvent(
            Tag.DIV,
            False,
            event_detail=None,
        )
        .ged(1)
        .split('\n')
    )
    divf = (  # noqa: F841
        FamilyEvent(
            Tag.DIVF,
            True,
            event_detail=None,
        )
        .ged(1)
        .split('\n')
    )
    enga = (  # noqa: F841
        FamilyEvent(
            Tag.ENGA,
            False,
            event_detail=None,
        )
        .ged(1)
        .split('\n')
    )
    marb = (  # noqa: F841
        FamilyEvent(
            Tag.MARB,
            True,
            event_detail=None,
        )
        .ged(1)
        .split('\n')
    )
    marc = (  # noqa: F841
        FamilyEvent(
            Tag.MARC,
            False,
            event_detail=None,
        )
        .ged(1)
        .split('\n')
    )
    marl = (  # noqa: F841
        FamilyEvent(
            Tag.MARL,
            True,
            event_detail=None,
        )
        .ged(1)
        .split('\n')
    )
    marr = (  # noqa: F841
        FamilyEvent(
            Tag.MARR,
            False,
            event_detail=None,
        )
        .ged(1)
        .split('\n')
    )
    mars = (  # noqa: F841
        FamilyEvent(
            Tag.MARS,
            True,
            event_detail=None,
        )
        .ged(1)
        .split('\n')
    )
    even = (  # noqa: F841
        FamilyEvent(
            Tag.EVEN,
            False,
            event_type='some string',
            event_detail=None,
        )
        .ged(1)
        .split('\n')
    )

    assert eval(test_input) == expected



def test_bad_enum() -> None:
    """This event checks that the tag is for family events."""
    bad = FamilyEvent(Tag.FAM, event_type='something')
    with pytest.raises(
        ValueError, match=Msg.NOT_VALID_ENUM.format(Tag.FAM.value, FamEven)
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
            bad.event_detail, type(bad.event_detail), FamilyEventDetail
        ),
    ):
        bad.validate()
