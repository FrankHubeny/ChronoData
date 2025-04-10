# names_test.py
"""Tests to cover the Names class.

"""

import logging

import pytest

from genedata.constants import Default
from genedata.methods import Names
from genedata.specifications70 import Structure


def test_keyname_from_classname() -> None:
    """Check that class names can be converted to a valid Structure key."""
    good: int = 0
    bad: int = 0
    class_name: str = Default.EMPTY
    key_name: str = Default.EMPTY 
    for key in Structure:
        class_name = Names.classname(key)
        key_name = Names.key_from_classname(class_name, Structure)
        if key_name == key:
            good += 1
        else:
            bad += 1
            logging.info(f'"{key_name}" does not equal "{key}"')
    assert bad == 0

def test_key_from_classname_not_present() -> None:
    key = 'abc'
    assert Names.key_from_classname(key, Structure) == ''

def test_quote_text_single_line_no_quotes() -> None:
    text: str = 'happy'
    assert Names.quote_text(text[1:3]) == "'ap'"

def test_quote_text_single_line_single_quote() -> None:
    text: str = "ha'ppy"
    assert Names.quote_text(text[1:4]) == '"a\'p"'

def test_quote_text_single_line_double_quote() -> None:
    text: str = 'ha"ppy'
    assert Names.quote_text(text[1:4]) == "'a\"p'"

def test_quote_text_multi_line_no_quotes() -> None:
    text: str = '''ha
ppy'''
    assert Names.quote_text(text[1:3]) == "'''a\n'''"

def test_quote_text_multi_line_single_quote() -> None:
    text: str = """ha'
ppy"""
    assert Names.quote_text(text[1:4]) == '"""a\'\n"""'

def test_quote_text_multi_line_double_quote() -> None:
    text: str = '''ha"
ppy'''
    assert Names.quote_text(text[1:4]) == "'''a\"\n'''"

def test_add_slash() -> None:
    text: str = 'abcdefg'
    assert Names.slash(text) == 'abcdefg/'

def test_has_slash() -> None:
    text: str = 'abcdefg/'
    assert Names.slash(text) == 'abcdefg/'

def test_slash_empty() -> None:
    text: str = ''
    assert Names.slash(text) == ''

def test_classname_full() -> None:
    text: str = 'record-YES-NO___'
    assert Names.classname(text) == 'RecordYesNo'

def test_classname_full2() -> None:
    text: str = 'ord-YES-__NO-MAYBE-'
    assert Names.classname(text) == 'OrdYesNoMaybe'

def test_classname_full3() -> None:
    text: str = 'ord-YES-exact'
    assert Names.classname(text) == 'OrdYesExact'

def test_stem() -> None:
    text: str = 'sev/eigh/nigh/four.txt'
    assert Names.stem(text) == 'four'

def test_stem2() -> None:
    text: str = 'sev/eigh/nigh/four.txttexttext'
    assert Names.stem(text) == 'four'

def test_keyname_empty() -> None:
    text: str = ''
    assert Names.keyname(text) == ''

def test_keyname_slash() -> None:
    text: str = 'abcdef/'
    assert Names.keyname(text) == ''

def test_keyname_value() -> None:
    text: str = 'abc/record-HIGH'
    assert Names.keyname(text) == 'record-HIGH'

def test_keyname_value_with_quotes() -> None:
    text: str = '"abc/record-HIGH"'
    assert Names.keyname(text) == 'record-HIGH'

def test_tagname() -> None:
    text: str = 'HEAD'
    assert Names.tagname(text) == 'HEAD'

def test_tagname_indi() -> None:
    text: str = 'record-INDI'
    assert Names.tagname(text) == 'INDI'

def test_tagname_empty() -> None:
    text: str = ''
    with pytest.raises(KeyError, match=('')):
        Names.tagname(text)

def test_tagname_not_key() -> None:
    text: str = 'abc'
    with pytest.raises(KeyError, match=('abc')):
        Names.tagname(text)
