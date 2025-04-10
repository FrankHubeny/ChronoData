# minimal70_ged_test
import genedata.classes70 as gc
from genedata.build import Genealogy
from genedata.constants import Default
from genedata.methods import Util


def test_minimal_ged() -> None:
    # Test constructing the minimal70.ged test file.
    file = Util.read('tests\\ged_test\\minimal70.ged')
    g = Genealogy('test')
    g.stage(gc.Head(gc.Gedc(gc.GedcVers('7.0'))))
    assert file == g.show_ged()

def test_minimal_ged_code() -> None:
    # Test generating code, evaluating it and then finding the ged lines from it.
    file = Util.read('tests\\ged_test\\minimal70.ged')
    head = gc.Head(gc.Gedc(gc.GedcVers('7.0')))
    gedcom = f'{eval(head.code(as_name='gc')).ged()}{Default.TRAILER}'
    assert file == gedcom