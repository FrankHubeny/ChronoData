"""------------------------------------------------------------------------------
                            Date Tests
------------------------------------------------------------------------------"""

import pytest

from chronodata.dates import DT

testdata = [
    ('creation_pieces[0][0]', '1'),
    ('creation_pieces[1][0]', '2'),
    ('creation_pieces[2][0]', '3'),
    ('creation_pieces[0][2:6]', 'CREA'),
    ('creation_pieces[1][2:6]', 'DATE'),
    ('creation_pieces[2][2:6]', 'TIME'),
]


@pytest.mark.parametrize('test_input,expected', testdata)  # noqa: PT006
def test_date(test_input: str, expected: str | int | bool) -> None:
    creation_pieces: list[str] = DT.creation_date().split('\n')  # noqa: F841

    assert eval(test_input) == expected
