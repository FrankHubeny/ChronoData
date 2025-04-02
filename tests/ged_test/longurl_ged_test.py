# longurl_ged_test.py
import genedata.classes7 as gc
from genedata.build import Genealogy
from genedata.constants import Config, Default
from genedata.structure import SubmitterXref  # noqa: F401
from genedata.methods import Util


def test_longurl_ged() -> None:
    # Test constructing the xref_ged test data.
    file = Util.read('tests\\ged_test\\long-url.ged')
    g = Genealogy('test')
    subm_xref = g.submitter_xref('S1')

    subm = gc.RecordSubm(
        subm_xref,
        [
            gc.Name('John Doe'),
            gc.Www('https://www.subdomain.example.com/alfa/bravo/charlie/delta/echo/foxtrot/golf/hotel/india/juliett/kilo/lima/mike/november/oscar/papa/quebec/romeo/sierra/tango/uniform/victor/whiskey/xray/yankee/zulu/Lorem%20ipsum%20dolor%20sit%20amet,%20consectetur%20adipiscing%20elit,%20sed%20do%20eiusmod%20tempor%20incididunt%20ut%20labore%20et%20dolore%20magna%20aliqua.%20Ut%20enim%20ad%20minim%20veniam,%20quis%20nostrud%20exercitation%20ullamco%20laboris%20nisi%20ut%20aliquip%20ex%20ea%20commodo%20consequat.%20Duis%20aute%20irure%20dolor%20in%20reprehenderit%20in%20voluptate%20velit%20esse%20cillum%20dolore%20eu%20fugiat%20nulla%20pariatur.%20Excepteur%20sint%20occaecat%20cupidatat%20non%20proident,%20sunt%20in%20culpa%20qui%20officia%20deserunt%20mollit%20anim%20id%20est%20laborum./filename.html'),
        ]
    )

    head = gc.Head(
        [
            gc.Gedc(gc.GedcVers(Config.GEDVERSION)),
            gc.Note('This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.'),
            gc.Subm(subm_xref),
        ]
    )
        
    gedcom = ''.join(
        [
            head.ged(), 
            subm.ged(),
            Default.TRAILER,
        ]
    )

    assert file == gedcom
    

def test_longurl_ged_code() -> None:
    # Test generating code, evaluating it and then finding the ged lines.
    file = Util.read('tests\\ged_test\\long-url.ged')
    g = Genealogy('test')
    subm_xref = g.submitter_xref('S1')

    subm = gc.RecordSubm(
        subm_xref,
        [
            gc.Name('John Doe'),
            gc.Www('https://www.subdomain.example.com/alfa/bravo/charlie/delta/echo/foxtrot/golf/hotel/india/juliett/kilo/lima/mike/november/oscar/papa/quebec/romeo/sierra/tango/uniform/victor/whiskey/xray/yankee/zulu/Lorem%20ipsum%20dolor%20sit%20amet,%20consectetur%20adipiscing%20elit,%20sed%20do%20eiusmod%20tempor%20incididunt%20ut%20labore%20et%20dolore%20magna%20aliqua.%20Ut%20enim%20ad%20minim%20veniam,%20quis%20nostrud%20exercitation%20ullamco%20laboris%20nisi%20ut%20aliquip%20ex%20ea%20commodo%20consequat.%20Duis%20aute%20irure%20dolor%20in%20reprehenderit%20in%20voluptate%20velit%20esse%20cillum%20dolore%20eu%20fugiat%20nulla%20pariatur.%20Excepteur%20sint%20occaecat%20cupidatat%20non%20proident,%20sunt%20in%20culpa%20qui%20officia%20deserunt%20mollit%20anim%20id%20est%20laborum./filename.html'),
        ]
    )

    head = gc.Head(
        [
            gc.Gedc(gc.GedcVers(Config.GEDVERSION)),
            gc.Note('This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.'),
            gc.Subm(subm_xref),
        ]
    )
        
    gedcom = ''.join(
        [
            eval(head.code(as_name='gc')).ged(), 
            eval(subm.code(as_name='gc')).ged(),
            Default.TRAILER,
        ]
    )

    assert file == gedcom
    