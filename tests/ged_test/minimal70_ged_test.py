# minimal70_ged_test
from genedata.classes7 import (
    Gedc,
    GedcVers,
    Head,
    Trlr,
)
from genedata.constants import Config


def test_xref_ged() -> None:
    # Test constructing the xref_ged test data.

    file = """0 HEAD
1 GEDC
2 VERS 7.0
0 TRLR"""

    head = Head(Gedc(GedcVers(Config.GEDVERSION)))

    gedcom = f'{head.ged()}{Trlr().ged()}'

    assert file == gedcom