# age_test.py
"""Tests to cover the Age and Phrase substructure with Input.age method.

1. Validate: Exercise all validation checks.
    a. Good run.
    b. Catch not permitted substructure.
    c. Catch not included but required substructures.
       No structures are required for this structure.
    d. Catch more than one when only one permitted.
    e. Catch bad input.

2. Ged: Exercise the generation of ged data.

3. Code: Exercise the code method.

4. Examples:  Demonstrate that all of the examples
    from the [Age testfile](https://gedcom.io/testfiles/gedcom70/age.ged)
    can be constructed.
"""

import re

import pytest

import genedata.classes7 as gc
from genedata.messages import Msg
from genedata.methods import Input

# 1. Validate: Exercise all validation checks.
#     a. Good run.


def test_good_run_using_list() -> None:
    """Run a successful use of the structure with list using lower case."""
    m = gc.Age('> 2y 1m 1w 1d', [gc.Phrase('Original: 2.2y')])
    assert m.validate()


def test_good_run_using_single_substructure() -> None:
    """Run a successful use of the structure."""
    m = gc.Age('> 2y 1m 1w 1d', gc.Phrase('Original: 2.2y'))
    assert m.validate()


def test_good_run_no_subs() -> None:
    """Run a successful use of the structure."""
    m = gc.Age('> 2y 1m 1w 1d')
    assert m.validate()


def test_good_run_only_phrase() -> None:
    """Run a successful use of the structure."""
    m = gc.Age('', gc.Phrase('Original: 2.2y'))
    assert m.validate()


#     b. Catch not permitted substructure.


def test_not_permitted() -> None:
    """Check that a substructure not in the permitted list cannot be used by the structure."""
    m = gc.Age('> 2y 1m 1w 1d', [gc.Phrase('Original: 2.2y'), gc.Lati('N30.0')])
    with pytest.raises(
        ValueError,
        match=re.escape(
            Msg.NOT_PERMITTED.format('Lati', m.permitted, m.class_name)
        ),
    ):
        m.validate()


#     c. Catch not included but required substructures.
#        No structures are required for NameType.

#     d. Catch more than one when only one permitted.


def test_phrase_only_one() -> None:
    """Check that the Phrase substructure can be used only once by Role."""
    m = gc.Age(
        '> 2y 1m 1w 1d', [gc.Phrase('Original: 2.2y'), gc.Phrase('friend2')]
    )
    with pytest.raises(
        ValueError, match=Msg.ONLY_ONE_PERMITTED.format('Phrase', m.class_name)
    ):
        m.validate()


#     e. Catch bad input.


def test_not_string_value() -> None:
    """Check that the wrong cross reference identifier is caught."""
    m = gc.Age(gc.Phrase('Original: 2.2y'))  # type: ignore[arg-type]
    with pytest.raises(
        ValueError,
        match=re.escape(Msg.NOT_STRING.format(m.value, m.class_name)),
    ):
        m.validate()


def test_no_keys() -> None:
    """Check that the wrong cross reference identifier is caught."""
    m = gc.Age('12345')
    with pytest.raises(
        ValueError,
        match=Msg.NOT_AGE.format(str(m.value), m.class_name),
    ):
        m.validate()


def test_wrong_keys() -> None:
    """Check that the wrong cross reference identifier is caught."""
    m = gc.Age('12345x')
    with pytest.raises(
        ValueError,
        match=Msg.NOT_AGE.format(str(m.value), m.class_name),
    ):
        m.validate()


def test_multiple_y() -> None:
    """Check that the wrong cross reference identifier is caught."""
    m = gc.Age('2yy')
    with pytest.raises(
        ValueError,
        match=Msg.NOT_AGE.format(str(m.value), m.class_name),
    ):
        m.validate()


def test_odd_character() -> None:
    """Check that the wrong cross reference identifier is caught."""
    m = gc.Age('> 2y 3m 1w 1dt')
    with pytest.raises(
        ValueError,
        match=Msg.NOT_AGE.format(str(m.value), m.class_name),
    ):
        m.validate()


def test_no_numbers() -> None:
    """Check that numbers must be in a non-empty age."""
    m = gc.Age('> y m w d')
    with pytest.raises(
        ValueError,
        match=Msg.NOT_AGE.format(str(m.value), m.class_name),
    ):
        m.validate()


def test_not_proper_beginning() -> None:
    """Check that numbers must be in a non-empty age."""
    m = gc.Age('y 1m 1w 1d')
    with pytest.raises(
        ValueError,
        match=Msg.NOT_AGE.format(str(m.value), m.class_name),
    ):
        m.validate()


# 2. Ged: Exercise the generation of ged data.


def test_ged() -> None:
    """Illustrate the standard use of the class."""
    m = gc.Age('> 2y 1m 1w 1d', gc.Phrase('Original: 2.2y'))
    assert m.ged(1) == '1 AGE > 2y 1m 1w 1d\n2 PHRASE Original: 2.2y\n'


def test_ged_with_list() -> None:
    """Illustrate the standard use of the class."""
    m = gc.Age('> 2y 1m 1w 1d', [gc.Phrase('Original: 2.2y')])
    assert m.ged(1) == '1 AGE > 2y 1m 1w 1d\n2 PHRASE Original: 2.2y\n'


def test_ged_only_phrase() -> None:
    """Run a successful use of the structure."""
    m = gc.Age('', gc.Phrase('Original: 2.2y'))
    assert m.ged(1) == '1 AGE\n2 PHRASE Original: 2.2y\n'


# 3. Code: Exercise the code method.


def test_code() -> None:
    """Illustrate code running."""
    m = gc.Age('> 2y 1m 1w 1d', gc.Phrase('Original: 2.2y'))
    assert m.code(as_name='gc') == "\ngc.Age('> 2y 1m 1w 1d', gc.Phrase('Original: 2.2y'))"


def test_code_with_list() -> None:
    """Illustrate code running."""
    m = gc.Age('> 2y 1m 1w 1d', [gc.Phrase('Original: 2.2y')])
    assert (
        m.code(as_name='gc')
        == "\ngc.Age('> 2y 1m 1w 1d',\n    [\n        gc.Phrase('Original: 2.2y'),\n    ]\n)"
    )


# 4. Examples:  Demonstrate that all of the examples
#     from the [Age testfile](https://gedcom.io/testfiles/gedcom70/age.ged)
#     can be constructed and validated.

testdata = [
    ('a1', '2 AGE 0y\n'),
    ('a2', '2 AGE < 0y\n'),
    ('a3', '2 AGE 0m\n'),
    ('a4', '2 AGE < 0m\n'),
    ('a5', '2 AGE 0w\n'),
    ('a6', '2 AGE < 0w\n'),
    ('a7', '2 AGE 0d\n'),
    ('a8', '2 AGE < 0d\n'),
    ('a9', '2 AGE 0y 0m\n'),
    ('a10', '2 AGE < 0y 0m\n'),
    ('a11', '2 AGE 0y 0w\n'),
    ('a12', '2 AGE < 0y 0w\n'),
    ('a13', '2 AGE 0y 0d\n'),
    ('a14', '2 AGE < 0y 0d\n'),
    ('a15', '2 AGE 0m 0w\n'),
    ('a16', '2 AGE < 0m 0w\n'),
    ('a17', '2 AGE 0m 0d\n'),
    ('a18', '2 AGE < 0m 0d\n'),
    ('a19', '2 AGE 0w 0d\n'),
    ('a20', '2 AGE < 0w 0d\n'),
    ('a21', '2 AGE 0y 0m 0w\n'),
    ('a22', '2 AGE < 0y 0m 0w\n'),
    ('a23', '2 AGE 0y 0m 0d\n'),
    ('a24', '2 AGE < 0y 0m 0d\n'),
    ('a25', '2 AGE 0y 0w 0d\n'),
    ('a26', '2 AGE < 0y 0w 0d\n'),
    ('a27', '2 AGE 0m 0w 0d\n'),
    ('a28', '2 AGE < 0m 0w 0d\n'),
    ('a29', '2 AGE 0y 0m 0w 0d\n'),
    ('a30', '2 AGE < 0y 0m 0w 0d\n'),
    ('a31', '2 AGE\n'),
    ('a32', '2 AGE > 0y\n'),
    ('a33', '2 AGE 99y\n'),
    ('a34', '2 AGE > 99y\n'),
    ('a35', '2 AGE < 99y\n'),
    ('a36', '2 AGE > 0m\n'),
    ('a37', '2 AGE 11m\n'),
    ('a38', '2 AGE > 11m\n'),
    ('a39', '2 AGE < 11m\n'),
    ('a40', '2 AGE > 0w\n'),
    ('a41', '2 AGE 3w\n'),
    ('a42', '2 AGE > 3w\n'),
    ('a43', '2 AGE < 3w\n'),
    ('a44', '2 AGE > 0d\n'),
    ('a45', '2 AGE 6d\n'),
    ('a46', '2 AGE > 6d\n'),
    ('a47', '2 AGE < 6d\n'),
    ('a48', '2 AGE > 0y 0m\n'),
    ('a49', '2 AGE 99y 11m\n'),
    ('a50', '2 AGE > 99y 11m\n'),
    ('a51', '2 AGE < 99y 11m\n'),
    ('a52', '2 AGE > 0y 0w\n'),
    ('a53', '2 AGE 99y 3w\n'),
    ('a54', '2 AGE > 99y 3w\n'),
    ('a55', '2 AGE < 99y 3w\n'),
    ('a56', '2 AGE > 0y 0d\n'),
    ('a57', '2 AGE 99y 6d\n'),
    ('a58', '2 AGE > 99y 6d\n'),
    ('a59', '2 AGE < 99y 6d\n'),
    ('a60', '2 AGE > 0m 0w\n'),
    ('a61', '2 AGE 11m 3w\n'),
    ('a62', '2 AGE > 11m 3w\n'),
    ('a63', '2 AGE < 11m 3w\n'),
    ('a64', '2 AGE > 0m 0d\n'),
    ('a65', '2 AGE 11m 6d\n'),
    ('a66', '2 AGE > 11m 6d\n'),
    ('a67', '2 AGE < 11m 6d\n'),
    ('a68', '2 AGE > 0w 0d\n'),
    ('a69', '2 AGE 3w 6d\n'),
    ('a70', '2 AGE > 3w 6d\n'),
    ('a71', '2 AGE < 3w 6d\n'),
    ('a72', '2 AGE > 0y 0m 0w\n'),
    ('a73', '2 AGE 99y 11m 3w\n'),
    ('a74', '2 AGE > 99y 11m 3w\n'),
    ('a75', '2 AGE < 99y 11m 3w\n'),
    ('a76', '2 AGE > 0y 0m 0d\n'),
    ('a77', '2 AGE 99y 11m 6d\n'),
    ('a78', '2 AGE > 99y 11m 6d\n'),
    ('a79', '2 AGE < 99y 11m 6d\n'),
    ('a80', '2 AGE > 0y 0w 0d\n'),
    ('a81', '2 AGE 99y 3w 6d\n'),
    ('a82', '2 AGE > 99y 3w 6d\n'),
    ('a83', '2 AGE < 99y 3w 6d\n'),
    ('a84', '2 AGE > 0m 0w 0d\n'),
    ('a85', '2 AGE 99m 3w 6d\n'),
    ('a86', '2 AGE > 99m 3w 6d\n'),
    ('a87', '2 AGE < 99m 3w 6d\n'),
    ('a88', '2 AGE > 0y 0m 0w 0d\n'),
    ('a89', '2 AGE 99y 11m 3w 6d\n'),
    ('a90', '2 AGE > 99y 11m 3w 6d\n'),
    ('a91', '2 AGE < 99y 11m 3w 6d\n'),
    ('a92', '2 AGE 1y 30m\n'),
    ('a93', '2 AGE 1y 100w\n'),
    ('a94', '2 AGE 1y 400d\n'),
    ('a95', '2 AGE 1m 40d\n'),
    ('a96', '2 AGE 1m 10w\n'),
    ('a97', '2 AGE 1w 30d\n'),
    ('a98', '2 AGE 1y 30m 100w 400d\n'),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_age_from_age_ged_example_file(
    test_input: str, expected: str | int | bool
) -> None:
    """Test that these constructions are not rejected by the validation checks.

    Reference:
    - [GEDCOM Age Example File](https://gedcom.io/testfiles/gedcom70/age.ged)"""
    a1 = gc.Age('0y').ged(2)  # noqa: F841
    a2 = gc.Age('< 0y').ged(2)  # noqa: F841
    a3 = gc.Age('0m').ged(2)  # noqa: F841
    a4 = gc.Age('< 0m').ged(2)  # noqa: F841
    a5 = gc.Age('0w').ged(2)  # noqa: F841
    a6 = gc.Age('< 0w').ged(2)  # noqa: F841
    a7 = gc.Age('0d').ged(2)  # noqa: F841
    a8 = gc.Age('< 0d').ged(2)  # noqa: F841
    a9 = gc.Age('0y 0m').ged(2)  # noqa: F841
    a10 = gc.Age('< 0y 0m').ged(2)  # noqa: F841
    a11 = gc.Age('0y 0w').ged(2)  # noqa: F841
    a12 = gc.Age('< 0y 0w').ged(2)  # noqa: F841
    a13 = gc.Age('0y 0d').ged(2)  # noqa: F841
    a14 = gc.Age('< 0y 0d').ged(2)  # noqa: F841
    a15 = gc.Age('0m 0w').ged(2)  # noqa: F841
    a16 = gc.Age('< 0m 0w').ged(2)  # noqa: F841
    a17 = gc.Age('0m 0d').ged(2)  # noqa: F841
    a18 = gc.Age('< 0m 0d').ged(2)  # noqa: F841
    a19 = gc.Age('0w 0d').ged(2)  # noqa: F841
    a20 = gc.Age('< 0w 0d').ged(2)  # noqa: F841
    a21 = gc.Age('0y 0m 0w').ged(2)  # noqa: F841
    a22 = gc.Age('< 0y 0m 0w').ged(2)  # noqa: F841
    a23 = gc.Age('0y 0m 0d').ged(2)  # noqa: F841
    a24 = gc.Age('< 0y 0m 0d').ged(2)  # noqa: F841
    a25 = gc.Age('0y 0w 0d').ged(2)  # noqa: F841
    a26 = gc.Age('< 0y 0w 0d').ged(2)  # noqa: F841
    a27 = gc.Age('0m 0w 0d').ged(2)  # noqa: F841
    a28 = gc.Age('< 0m 0w 0d').ged(2)  # noqa: F841
    a29 = gc.Age('0y 0m 0w 0d').ged(2)  # noqa: F841
    a30 = gc.Age('< 0y 0m 0w 0d').ged(2)  # noqa: F841
    a31 = gc.Age('').ged(2)  # noqa: F841
    a32 = gc.Age('> 0y').ged(2)  # noqa: F841
    a33 = gc.Age('99y').ged(2)  # noqa: F841
    a34 = gc.Age('> 99y').ged(2)  # noqa: F841
    a35 = gc.Age('< 99y').ged(2)  # noqa: F841
    a36 = gc.Age('> 0m').ged(2)  # noqa: F841
    a37 = gc.Age('11m').ged(2)  # noqa: F841
    a38 = gc.Age('> 11m').ged(2)  # noqa: F841
    a39 = gc.Age('< 11m').ged(2)  # noqa: F841
    a40 = gc.Age('> 0w').ged(2)  # noqa: F841
    a41 = gc.Age('3w').ged(2)  # noqa: F841
    a42 = gc.Age('> 3w').ged(2)  # noqa: F841
    a43 = gc.Age('< 3w').ged(2)  # noqa: F841
    a44 = gc.Age('> 0d').ged(2)  # noqa: F841
    a45 = gc.Age('6d').ged(2)  # noqa: F841
    a46 = gc.Age('> 6d').ged(2)  # noqa: F841
    a47 = gc.Age('< 6d').ged(2)  # noqa: F841
    a48 = gc.Age('> 0y 0m').ged(2)  # noqa: F841
    a49 = gc.Age('99y 11m').ged(2)  # noqa: F841
    a50 = gc.Age('> 99y 11m').ged(2)  # noqa: F841
    a51 = gc.Age('< 99y 11m').ged(2)  # noqa: F841
    a52 = gc.Age('> 0y 0w').ged(2)  # noqa: F841
    a53 = gc.Age('99y 3w').ged(2)  # noqa: F841
    a54 = gc.Age('> 99y 3w').ged(2)  # noqa: F841
    a55 = gc.Age('< 99y 3w').ged(2)  # noqa: F841
    a56 = gc.Age('> 0y 0d').ged(2)  # noqa: F841
    a57 = gc.Age('99y 6d').ged(2)  # noqa: F841
    a58 = gc.Age('> 99y 6d').ged(2)  # noqa: F841
    a59 = gc.Age('< 99y 6d').ged(2)  # noqa: F841
    a60 = gc.Age('> 0m 0w').ged(2)  # noqa: F841
    a61 = gc.Age('11m 3w').ged(2)  # noqa: F841
    a62 = gc.Age('> 11m 3w').ged(2)  # noqa: F841
    a63 = gc.Age('< 11m 3w').ged(2)  # noqa: F841
    a64 = gc.Age('> 0m 0d').ged(2)  # noqa: F841
    a65 = gc.Age('11m 6d').ged(2)  # noqa: F841
    a66 = gc.Age('> 11m 6d').ged(2)  # noqa: F841
    a67 = gc.Age('< 11m 6d').ged(2)  # noqa: F841
    a68 = gc.Age('> 0w 0d').ged(2)  # noqa: F841
    a69 = gc.Age('3w 6d').ged(2)  # noqa: F841
    a70 = gc.Age('> 3w 6d').ged(2)  # noqa: F841
    a71 = gc.Age('< 3w 6d').ged(2)  # noqa: F841
    a72 = gc.Age('> 0y 0m 0w').ged(2)  # noqa: F841
    a73 = gc.Age('99y 11m 3w').ged(2)  # noqa: F841
    a74 = gc.Age('> 99y 11m 3w').ged(2)  # noqa: F841
    a75 = gc.Age('< 99y 11m 3w').ged(2)  # noqa: F841
    a76 = gc.Age('> 0y 0m 0d').ged(2)  # noqa: F841
    a77 = gc.Age('99y 11m 6d').ged(2)  # noqa: F841
    a78 = gc.Age('> 99y 11m 6d').ged(2)  # noqa: F841
    a79 = gc.Age('< 99y 11m 6d').ged(2)  # noqa: F841
    a80 = gc.Age('> 0y 0w 0d').ged(2)  # noqa: F841
    a81 = gc.Age('99y 3w 6d').ged(2)  # noqa: F841
    a82 = gc.Age('> 99y 3w 6d').ged(2)  # noqa: F841
    a83 = gc.Age('< 99y 3w 6d').ged(2)  # noqa: F841
    a84 = gc.Age('> 0m 0w 0d').ged(2)  # noqa: F841
    a85 = gc.Age('99m 3w 6d').ged(2)  # noqa: F841
    a86 = gc.Age('> 99m 3w 6d').ged(2)  # noqa: F841
    a87 = gc.Age('< 99m 3w 6d').ged(2)  # noqa: F841
    a88 = gc.Age('> 0y 0m 0w 0d').ged(2)  # noqa: F841
    a89 = gc.Age('99y 11m 3w 6d').ged(2)  # noqa: F841
    a90 = gc.Age('> 99y 11m 3w 6d').ged(2)  # noqa: F841
    a91 = gc.Age('< 99y 11m 3w 6d').ged(2)  # noqa: F841
    a92 = gc.Age('1y 30m').ged(2)  # noqa: F841
    a93 = gc.Age('1y 100w').ged(2)  # noqa: F841
    a94 = gc.Age('1y 400d').ged(2)  # noqa: F841
    a95 = gc.Age('1m 40d').ged(2)  # noqa: F841
    a96 = gc.Age('1m 10w').ged(2)  # noqa: F841
    a97 = gc.Age('1w 30d').ged(2)  # noqa: F841
    a98 = gc.Age('1y 30m 100w 400d').ged(2)  # noqa: F841

    assert eval(test_input) == expected


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_input_age_from_age_ged_example_file(
    test_input: str, expected: str | int | bool
) -> None:
    """Test that these constructions are not rejected by the validation checks.

    Reference:
    - [GEDCOM Age Example File](https://gedcom.io/testfiles/gedcom70/age.ged)"""
    a1 = gc.Age(Input.age(years=0, greater_less_than='')).ged(2)  # noqa: F841
    a2 = gc.Age(Input.age(years=0, greater_less_than='<')).ged(2)  # noqa: F841
    a3 = gc.Age(Input.age(months=0, greater_less_than='')).ged(2)  # noqa: F841
    a4 = gc.Age(Input.age(months=0, greater_less_than='<')).ged(2)  # noqa: F841
    a5 = gc.Age(Input.age(weeks=0, greater_less_than='')).ged(2)  # noqa: F841
    a6 = gc.Age(Input.age(weeks=0, greater_less_than='<')).ged(2)  # noqa: F841
    a7 = gc.Age(Input.age(days=0, greater_less_than='')).ged(2)  # noqa: F841
    a8 = gc.Age(Input.age(days=0, greater_less_than='<')).ged(2)  # noqa: F841
    a9 = gc.Age(Input.age(years=0, months=0, greater_less_than='')).ged(2)  # noqa: F841
    a10 = gc.Age(Input.age(years=0, months=0, greater_less_than='<')).ged(2)  # noqa: F841
    a11 = gc.Age(Input.age(years=0, weeks=0, greater_less_than='')).ged(2)  # noqa: F841
    a12 = gc.Age(Input.age(years=0, weeks=0, greater_less_than='<')).ged(2)  # noqa: F841
    a13 = gc.Age(Input.age(years=0, days=0, greater_less_than='')).ged(2)  # noqa: F841
    a14 = gc.Age(Input.age(years=0, days=0, greater_less_than='<')).ged(2)  # noqa: F841
    a15 = gc.Age(Input.age(months=0, weeks=0, greater_less_than='')).ged(2)  # noqa: F841
    a16 = gc.Age(Input.age(months=0, weeks=0, greater_less_than='<')).ged(2)  # noqa: F841
    a17 = gc.Age(Input.age(months=0, days=0, greater_less_than='')).ged(2)  # noqa: F841
    a18 = gc.Age(Input.age(months=0, days=0, greater_less_than='<')).ged(2)  # noqa: F841
    a19 = gc.Age(Input.age(weeks=0, days=0, greater_less_than='')).ged(2)  # noqa: F841
    a20 = gc.Age(Input.age(weeks=0, days=0, greater_less_than='<')).ged(2)  # noqa: F841
    a21 = gc.Age(  # noqa: F841
        Input.age(years=0, months=0, weeks=0, greater_less_than='')
    ).ged(2)
    a22 = gc.Age(  # noqa: F841
        Input.age(years=0, months=0, weeks=0, greater_less_than='<')
    ).ged(2)
    a23 = gc.Age(  # noqa: F841
        Input.age(years=0, months=0, days=0, greater_less_than='')
    ).ged(2)
    a24 = gc.Age(  # noqa: F841
        Input.age(years=0, months=0, days=0, greater_less_than='<')
    ).ged(2)
    a25 = gc.Age(Input.age(years=0, weeks=0, days=0, greater_less_than='')).ged(  # noqa: F841
        2
    )
    a26 = gc.Age(  # noqa: F841
        Input.age(years=0, weeks=0, days=0, greater_less_than='<')
    ).ged(2)
    a27 = gc.Age(  # noqa: F841
        Input.age(months=0, weeks=0, days=0, greater_less_than='')
    ).ged(2)
    a28 = gc.Age(  # noqa: F841
        Input.age(months=0, weeks=0, days=0, greater_less_than='<')
    ).ged(2)
    a29 = gc.Age(  # noqa: F841
        Input.age(years=0, months=0, weeks=0, days=0, greater_less_than='')
    ).ged(2)
    a30 = gc.Age(  # noqa: F841
        Input.age(years=0, months=0, weeks=0, days=0, greater_less_than='<')
    ).ged(2)
    a31 = gc.Age(Input.age()).ged(2)  # noqa: F841
    a32 = gc.Age(Input.age(years=0, greater_less_than='>')).ged(2)  # noqa: F841
    a33 = gc.Age(Input.age(years=99, greater_less_than='')).ged(2)  # noqa: F841
    a34 = gc.Age(Input.age(years=99, greater_less_than='>')).ged(2)  # noqa: F841
    a35 = gc.Age(Input.age(years=99, greater_less_than='<')).ged(2)  # noqa: F841
    a36 = gc.Age(Input.age(months=0, greater_less_than='>')).ged(2)  # noqa: F841
    a37 = gc.Age(Input.age(months=11, greater_less_than='')).ged(2)  # noqa: F841
    a38 = gc.Age(Input.age(months=11, greater_less_than='>')).ged(2)  # noqa: F841
    a39 = gc.Age(Input.age(months=11, greater_less_than='<')).ged(2)  # noqa: F841
    a40 = gc.Age(Input.age(weeks=0, greater_less_than='>')).ged(2)  # noqa: F841
    a41 = gc.Age(Input.age(weeks=3, greater_less_than='')).ged(2)  # noqa: F841
    a42 = gc.Age(Input.age(weeks=3, greater_less_than='>')).ged(2)  # noqa: F841
    a43 = gc.Age(Input.age(weeks=3, greater_less_than='<')).ged(2)  # noqa: F841
    a44 = gc.Age(Input.age(days=0, greater_less_than='>')).ged(2)  # noqa: F841
    a45 = gc.Age(Input.age(days=6, greater_less_than='')).ged(2)  # noqa: F841
    a46 = gc.Age(Input.age(days=6, greater_less_than='>')).ged(2)  # noqa: F841
    a47 = gc.Age(Input.age(days=6, greater_less_than='<')).ged(2)  # noqa: F841
    a48 = gc.Age(Input.age(years=0, months=0, greater_less_than='>')).ged(2)  # noqa: F841
    a49 = gc.Age(Input.age(years=99, months=11, greater_less_than='')).ged(2)  # noqa: F841
    a50 = gc.Age(Input.age(years=99, months=11, greater_less_than='>')).ged(2)  # noqa: F841
    a51 = gc.Age(Input.age(years=99, months=11, greater_less_than='<')).ged(2)  # noqa: F841
    a52 = gc.Age(Input.age(years=0, weeks=0, greater_less_than='>')).ged(2)  # noqa: F841
    a53 = gc.Age(Input.age(years=99, weeks=3, greater_less_than='')).ged(2)  # noqa: F841
    a54 = gc.Age(Input.age(years=99, weeks=3, greater_less_than='>')).ged(2)  # noqa: F841
    a55 = gc.Age(Input.age(years=99, weeks=3, greater_less_than='<')).ged(2)  # noqa: F841
    a56 = gc.Age(Input.age(years=0, days=0, greater_less_than='>')).ged(2)  # noqa: F841
    a57 = gc.Age(Input.age(years=99, days=6, greater_less_than='')).ged(2)  # noqa: F841
    a58 = gc.Age(Input.age(years=99, days=6, greater_less_than='>')).ged(2)  # noqa: F841
    a59 = gc.Age(Input.age(years=99, days=6, greater_less_than='<')).ged(2)  # noqa: F841
    a60 = gc.Age(Input.age(months=0, weeks=0, greater_less_than='>')).ged(2)  # noqa: F841
    a61 = gc.Age(Input.age(months=11, weeks=3, greater_less_than='')).ged(2)  # noqa: F841
    a62 = gc.Age(Input.age(months=11, weeks=3, greater_less_than='>')).ged(2)  # noqa: F841
    a63 = gc.Age(Input.age(months=11, weeks=3, greater_less_than='<')).ged(2)  # noqa: F841
    a64 = gc.Age(Input.age(months=0, days=0, greater_less_than='>')).ged(2)  # noqa: F841
    a65 = gc.Age(Input.age(months=11, days=6, greater_less_than='')).ged(2)  # noqa: F841
    a66 = gc.Age(Input.age(months=11, days=6, greater_less_than='>')).ged(2)  # noqa: F841
    a67 = gc.Age(Input.age(months=11, days=6, greater_less_than='<')).ged(2)  # noqa: F841
    a68 = gc.Age(Input.age(weeks=0, days=0, greater_less_than='>')).ged(2)  # noqa: F841
    a69 = gc.Age(Input.age(weeks=3, days=6, greater_less_than='')).ged(2)  # noqa: F841
    a70 = gc.Age(Input.age(weeks=3, days=6, greater_less_than='>')).ged(2)  # noqa: F841
    a71 = gc.Age(Input.age(weeks=3, days=6, greater_less_than='<')).ged(2)  # noqa: F841
    a72 = gc.Age(  # noqa: F841
        Input.age(years=0, months=0, weeks=0, greater_less_than='>')
    ).ged(2)
    a73 = gc.Age(  # noqa: F841
        Input.age(years=99, months=11, weeks=3, greater_less_than='')
    ).ged(2)
    a74 = gc.Age(  # noqa: F841
        Input.age(years=99, months=11, weeks=3, greater_less_than='>')
    ).ged(2)
    a75 = gc.Age(  # noqa: F841
        Input.age(years=99, months=11, weeks=3, greater_less_than='<')
    ).ged(2)
    a76 = gc.Age(  # noqa: F841
        Input.age(years=0, months=0, days=0, greater_less_than='>')
    ).ged(2)
    a77 = gc.Age(  # noqa: F841
        Input.age(years=99, months=11, days=6, greater_less_than='')
    ).ged(2)
    a78 = gc.Age(  # noqa: F841
        Input.age(years=99, months=11, days=6, greater_less_than='>')
    ).ged(2)
    a79 = gc.Age(  # noqa: F841
        Input.age(years=99, months=11, days=6, greater_less_than='<')
    ).ged(2)
    a80 = gc.Age(  # noqa: F841
        Input.age(years=0, weeks=0, days=0, greater_less_than='>')
    ).ged(2)
    a81 = gc.Age(  # noqa: F841
        Input.age(years=99, weeks=3, days=6, greater_less_than='')
    ).ged(2)
    a82 = gc.Age(  # noqa: F841
        Input.age(years=99, weeks=3, days=6, greater_less_than='>')
    ).ged(2)
    a83 = gc.Age(  # noqa: F841
        Input.age(years=99, weeks=3, days=6, greater_less_than='<')
    ).ged(2)
    a84 = gc.Age(  # noqa: F841
        Input.age(months=0, weeks=0, days=0, greater_less_than='>')
    ).ged(2)
    a85 = gc.Age(  # noqa: F841
        Input.age(months=99, weeks=3, days=6, greater_less_than='')
    ).ged(2)
    a86 = gc.Age(  # noqa: F841
        Input.age(months=99, weeks=3, days=6, greater_less_than='>')
    ).ged(2)
    a87 = gc.Age(  # noqa: F841
        Input.age(months=99, weeks=3, days=6, greater_less_than='<')
    ).ged(2)
    a88 = gc.Age(  # noqa: F841
        Input.age(years=0, months=0, weeks=0, days=0, greater_less_than='>')
    ).ged(2)
    a89 = gc.Age(  # noqa: F841
        Input.age(years=99, months=11, weeks=3, days=6, greater_less_than='')
    ).ged(2)
    a90 = gc.Age(  # noqa: F841
        Input.age(years=99, months=11, weeks=3, days=6, greater_less_than='>')
    ).ged(2)
    a91 = gc.Age(  # noqa: F841
        Input.age(years=99, months=11, weeks=3, days=6, greater_less_than='<')
    ).ged(2)
    a92 = gc.Age(Input.age(years=1, months=30, greater_less_than='')).ged(2)  # noqa: F841
    a93 = gc.Age(Input.age(years=1, weeks=100, greater_less_than='')).ged(2)  # noqa: F841
    a94 = gc.Age(Input.age(years=1, days=400, greater_less_than='')).ged(2)  # noqa: F841
    a95 = gc.Age(Input.age(months=1, days=40, greater_less_than='')).ged(2)  # noqa: F841
    a96 = gc.Age(Input.age(months=1, weeks=10, greater_less_than='')).ged(2)  # noqa: F841
    a97 = gc.Age(Input.age(weeks=1, days=30, greater_less_than='')).ged(2)  # noqa: F841
    a98 = gc.Age(  # noqa: F841
        Input.age(years=1, months=30, weeks=100, days=400, greater_less_than='')
    ).ged(2)

    assert eval(test_input) == expected
