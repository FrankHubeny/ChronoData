# tagger_test.py
"""Tests to cover the Tagger class.

"""

from genedata.methods import Tagger


def test_clean_input() -> None:
    value: str = '\u0000\u001F\u007F\uD800\uDFFF\uFFFE\uFFFFhello'
    assert Tagger.clean_input(value) == 'hello'

def test_taginfo_basic() -> None:
    assert Tagger.taginfo(3, 'LATI', 'N10.1') == '3 LATI N10.1\n'

def test_taginfo_xref() -> None:
    assert Tagger.taginfo(3, 'INDI', xref='@1@') == '3 @1@ INDI\n'

def test_taginfo_xref_plus() -> None:
    assert Tagger.taginfo(3, 'INDI', 'hello', xref='@1@') == '3 @1@ INDI hello\n'

def test_taginfo_xref_plus_with_atsign() -> None:
    assert Tagger.taginfo(3, 'INDI', '@hello', xref='@1@') == '3 @1@ INDI @@hello\n'

def test_taginfo_xref_plus_with_atsign_multi() -> None:
    assert Tagger.taginfo(3, 'INDI', '@hello\nthere', xref='@1@') == '3 @1@ INDI @@hello\n4 CONT there\n'

def test_taginfo_xref_plus_with_atsign_multi_again() -> None:
    assert Tagger.taginfo(3, 'INDI', '@hello\n@there', xref='@1@') == '3 @1@ INDI @@hello\n4 CONT @@there\n'

def test_taginfo_xref_full() -> None:
    assert Tagger.taginfo(3, 'INDI', '@hello', 'extra', xref='@1@') == '3 @1@ INDI @@hello extra\n'

def test_empty_earlier_lines() -> None:
    assert Tagger.empty('earlier lines\n', 1, 'MAP') == 'earlier lines\n1 MAP\n'

def test_empty_no_earlier_lines() -> None:
    assert Tagger.empty('', 1, 'MAP') == '1 MAP\n'

def test_empty_with_xref() -> None:
    assert Tagger.empty('', 0, 'INDI', '@1@') == '0 @1@ INDI\n'

def test_string_basic() -> None:
    assert Tagger.string('', 3, 'LATI', 'N10.1') == '3 LATI N10.1\n'

def test_string_payload_none() -> None:
    assert Tagger.string('previous\n', 3, 'LATI', None) == 'previous\n'

def test_string_payload_multiline() -> None:
    assert Tagger.string('previous\n', 3, 'NOTE', 'This\nis\na note.') == 'previous\n3 NOTE This\n4 CONT is\n4 CONT a note.\n'

def test_string_payload_multiline_with_atsign() -> None:
    assert Tagger.string('previous\n', 3, 'NOTE', 'This\n@is\na note.') == 'previous\n3 NOTE This\n4 CONT @@is\n4 CONT a note.\n'

def test_string_payload_format() -> None:
    assert Tagger.string('',1,'NOTE','@test\n@again', format=False) == '1 NOTE @test\n2 CONT @again\n'

# def test_string_xref() -> None:
#     assert Tagger.string('', 3, 'INDI', xref='@1@') == '3 @1@ INDI\n'

def test_string_xref_plus() -> None:
    assert Tagger.string('', 3, 'INDI', 'hello', xref='@1@') == '3 @1@ INDI hello\n'

def test_string_xref_plus_with_atsign() -> None:
    assert Tagger.string('', 3, 'INDI', '@hello', xref='@1@') == '3 @1@ INDI @@hello\n'

def test_string_xref_plus_with_atsign_multi() -> None:
    assert Tagger.string('', 3, 'INDI', '@hello\nthere', xref='@1@') == '3 @1@ INDI @@hello\n4 CONT there\n'

def test_string_xref_plus_with_atsign_multi_again() -> None:
    assert Tagger.string('', 3, 'INDI', '@hello\n@there', xref='@1@') == '3 @1@ INDI @@hello\n4 CONT @@there\n'

def test_string_xref_full() -> None:
    assert Tagger.string('', 3, 'INDI', '@hello', 'extra', xref='@1@') == '3 @1@ INDI @@hello extra\n'

def test_string_with_list() -> None:
    assert Tagger.string('', 3, 'WWW', ['https://here.com', 'https://there.com']) == '3 WWW https://here.com\n3 WWW https://there.com\n'