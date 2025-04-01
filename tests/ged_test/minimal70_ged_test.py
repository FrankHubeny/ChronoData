# minimal70_ged_test
import genedata.classes7 as gc
from genedata.build import Genealogy
from genedata.constants import Config, Default
from genedata.methods import Util


def test_minimal_ged() -> None:
    # Test constructing the minimal70.ged test file.
    file = Util.read('tests\\ged_test\\minimal70.ged')
    g = Genealogy('test')
    g.stage(gc.Head(gc.Gedc(gc.GedcVers(Config.GEDVERSION))))
    assert file == g.show_ged()

def test_minimal_ged_code() -> None:
    # Test generating code, evaluating it and then finding the ged lines from it.
    file = Util.read('tests\\ged_test\\minimal70.ged')
    head = gc.Head(gc.Gedc(gc.GedcVers(Config.GEDVERSION)))
    gedcom = f'{eval(head.code()).ged()}{Default.TRAILER}'
    assert file == gedcom