"""------------------------------------------------------------------------------
                            Contact Tests

    These texts cover the `contact` method which formats phones,
    emails, faxes and web pages.

------------------------------------------------------------------------------"""

import pytest

from chronodata.chrono import Chronology

testdata = [
    ('empty[0]', ''),
    ('phones[0]', '1 PHON 123'),
    ('phones[2]', '1 PHON 789'),
    ('all[0]', '1 PHON 333'),
    ('all[1]', '1 EMAIL fff'),
    ('all[2]', '1 FAX 333'),
    ('all[3]', '1 FAX 444'),
    ('all[4]', '1 WWW rrr'),
    ('all[5]', '1 WWW sss'),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_contact(test_input: str, expected: str | int | bool) -> None:
    a = Chronology(name='testing')
    empty = a.contact(None, None, None, None).split('\n')
    phones = a.contact(phones=['123', '456', '789']).split('\n')
    all = a.contact(
        phones=['333'],
        emails=['fff'],
        faxes=['333', '444'],
        wwws=['rrr', 'sss', 'zzz'],
    ).split('\n')

    assert eval(test_input) == expected
