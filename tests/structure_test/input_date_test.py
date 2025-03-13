# input_date_test.py
"""Test the various date methods in the Input class.

1. Check Input.date().
    a. Good run.
    b. Catch range errors.

2. Check Input.date_period().
    a. Good run.
    b. Catch range errors.

3. Check Input.date_between_and().
    a. Good run.
    b. Catch range errors.

4. Check Input.date_before().
    a. Good run.
    b. Catch range errors.

5. Check Input.date_after().
    a. Good run.
    b. Catch range errors.

6. Check Input.date_about().
    a. Good run.
    b. Catch range errors.

7. Check Input.date_calculated().
    a. Good run.
    b. Catch range errors.

8. Check Input.date_estimated().
    a. Good run.
    b. Catch range errors.

"""

import pytest

from genedata.messages import Msg
from genedata.structure import Input

# 1. Check Input.date().
#     a. Good run.


def test_input_date() -> None:
    """Check that a good value for the date is returned."""
    assert Input.date(2000, 6, 4) == '4 JUN 2000'


def test_input_date_show_calendar() -> None:
    """Check that the calendar name is shown when requested."""
    assert Input.date(2000, 6, 4, show=True) == 'GREGORIAN 4 JUN 2000'


def test_input_date_bc() -> None:
    """Check that an epoch is returned for years less than zero."""
    assert Input.date(-2000, 6, 4) == '4 JUN 2000 BCE'


def test_input_date_julian() -> None:
    """Check that a good value for the Julian calendar."""
    assert Input.date(2000, 6, 4, 'JULIAN') == '4 JUN 2000'


def test_input_date_hebrew() -> None:
    """Check that a good value for the Hebrew calendar."""
    assert Input.date(2000, 6, 4, 'HEBREW') == '4 ADR 2000'


def test_input_date_french_revolution() -> None:
    """Check that a good value for the French revolution calendar."""
    assert Input.date(1, 6, 4, 'FRENCH_R') == '4 VENT 1'


#     b. Catch range errors.


def test_input_date_zero_year_gregorian() -> None:
    """Check that zero is not used for the Gregorian or Julian calendars."""
    calendar: str = 'GREGORIAN'
    with pytest.raises(
        ValueError,
        match=Msg.ZERO_YEAR.format(calendar),
    ):
        Input.date(0, 1, 1, calendar=calendar)


def test_input_date_zero_year_julian() -> None:
    """Check that zero is not used for the Gregorian or Julian calendars."""
    calendar: str = 'JULIAN'
    with pytest.raises(
        ValueError,
        match=Msg.ZERO_YEAR.format(calendar),
    ):
        Input.date(0, 1, 1, calendar=calendar)


# 2. Check Input.date_period().
#     a. Good run.

def test_input_date_period() -> None:
    """Check that a good value for a date period is returned."""
    assert Input.date_period(Input.date(1950, 1, 1), Input.date(2000,1,1)) == 'FROM 1 JAN 1950 TO 1 JAN 2000'

def test_input_date_period_with_show() -> None:
    """Check that a good value for a date period is returned with the calendar nam."""
    assert Input.date_period(Input.date(1950, 1, 1, show=True), Input.date(2000,1,1)) == 'FROM GREGORIAN 1 JAN 1950 TO 1 JAN 2000'

#     b. Catch range errors.

# 3. Check Input.date_between_and().
#     a. Good run.

def test_input_date_between_and() -> None:
    """Check that a good value for a between date and date is returned."""
    assert Input.date_between_and(Input.date(1950, 1, 1), Input.date(2000,1,1)) == 'BET 1 JAN 1950 AND 1 JAN 2000'

def test_input_date_between_and_with_show() -> None:
    """Check that a good value for a between date and date is returned with the calendar nam."""
    assert Input.date_between_and(Input.date(1950, 1, 1, show=True), Input.date(2000,1,1)) == 'BET GREGORIAN 1 JAN 1950 AND 1 JAN 2000'


def test_input_date_between_and_bc_with_show() -> None:
    """Check that a good value for a between date and date is returned with the calendar nam."""
    assert Input.date_between_and(Input.date(-1950, 1, 1, show=True), Input.date(2000,1,1)) == 'BET GREGORIAN 1 JAN 1950 BCE AND 1 JAN 2000'

#     b. Catch range errors.

# 4. Check Input.date_before().
#     a. Good run.

def test_input_date_before() -> None:
    """Check that a good value for a before date is returned."""
    assert Input.date_before(Input.date(1950, 1, 1)) == 'BEF 1 JAN 1950'

def test_input_date_before_bc() -> None:
    """Check that a good value for a before date is returned."""
    assert Input.date_before(Input.date(-1950, 1, 1)) == 'BEF 1 JAN 1950 BCE'

def test_input_date_before_bc_with_show() -> None:
    """Check that a good value for a before date is returned."""
    assert Input.date_before(Input.date(-1950, 1, 1, show=True)) == 'BEF GREGORIAN 1 JAN 1950 BCE'

#     b. Catch range errors.

# 5. Check Input.date_after().
#     a. Good run.

def test_input_date_after() -> None:
    """Check that a good value for an after date is returned."""
    assert Input.date_after(Input.date(1950, 1, 1)) == 'AFT 1 JAN 1950'

def test_input_date_after_bc() -> None:
    """Check that a good value for an after date is returned."""
    assert Input.date_after(Input.date(-1950, 1, 1)) == 'AFT 1 JAN 1950 BCE'

def test_input_date_after_bc_with_show() -> None:
    """Check that a good value for an after date and date is returned."""
    assert Input.date_after(Input.date(-1950, 1, 1, show=True)) == 'AFT GREGORIAN 1 JAN 1950 BCE'

#     b. Catch range errors.

# 6. Check Input.date_about().
#     a. Good run.

def test_input_date_about() -> None:
    """Check that a good value for an about date is returned."""
    assert Input.date_about(Input.date(1950, 1, 1)) == 'ABT 1 JAN 1950'

def test_input_date_about_bc() -> None:
    """Check that a good value for an about date is returned."""
    assert Input.date_about(Input.date(-1950, 1, 1)) == 'ABT 1 JAN 1950 BCE'

def test_input_date_about_bc_with_show() -> None:
    """Check that a good value for an about date and date is returned."""
    assert Input.date_about(Input.date(-1950, 1, 1, show=True)) == 'ABT GREGORIAN 1 JAN 1950 BCE'

#     b. Catch range errors.

# 7. Check Input.date_calculated().
#     a. Good run.

def test_input_date_calculated() -> None:
    """Check that a good value for a calculated date is returned."""
    assert Input.date_calculated(Input.date(1950, 1, 1)) == 'CAL 1 JAN 1950'

def test_input_date_calculated_bc() -> None:
    """Check that a good value for a calculated date is returned."""
    assert Input.date_calculated(Input.date(-1950, 1, 1)) == 'CAL 1 JAN 1950 BCE'

def test_input_date_calculated_bc_with_show() -> None:
    """Check that a good value for a calculated date and date is returned."""
    assert Input.date_calculated(Input.date(-1950, 1, 1, show=True)) == 'CAL GREGORIAN 1 JAN 1950 BCE'

#     b. Catch range errors.

# 8. Check Input.date_estimated().
#     a. Good run.

def test_input_date_estimated() -> None:
    """Check that a good value for an estimated date is returned."""
    assert Input.date_estimated(Input.date(1950, 1, 1)) == 'EST 1 JAN 1950'

def test_input_date_estimated_bc() -> None:
    """Check that a good value for an estimated date is returned."""
    assert Input.date_estimated(Input.date(-1950, 1, 1)) == 'EST 1 JAN 1950 BCE'

def test_input_date_estimated_bc_with_show() -> None:
    """Check that a good value for an estimated date and date is returned."""
    assert Input.date_estimated(Input.date(-1950, 1, 1, show=True)) == 'EST GREGORIAN 1 JAN 1950 BCE'

#     b. Catch range errors.
