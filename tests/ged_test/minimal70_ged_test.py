# minimal70_ged_test
from genedata.classes7 import (
    Gedc,
    GedcVers,
    Head,
    Trlr,
)
from genedata.constants import Config
from genedata.util import Util


def test_xref_ged() -> None:
    # Test constructing the xref_ged test data.
    file = Util.read('tests\\ged_test\\minimal70.ged')

    head = Head(Gedc(GedcVers(Config.GEDVERSION)))

    gedcom = f'{head.ged()}{Trlr().ged()}'

    assert file == gedcom

def test_xref_ged_code() -> None:
    # Test generating code, evaluating it and then finding the ged lines.
    file = Util.read('tests\\ged_test\\minimal70.ged')

    head = Head(Gedc(GedcVers(Config.GEDVERSION)))

    gedcom = f'{eval(head.code()).ged()}{eval(Trlr().code()).ged()}'

    assert file == gedcom