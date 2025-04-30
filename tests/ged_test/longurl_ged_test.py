# longurl_ged_test.py
import genedata.classes70 as gc
from genedata.build import Genealogy
from genedata.constants import Default
from genedata.methods import Util
from genedata.structure import SubmitterXref  # noqa: F401

ged_version: str = '7.0'

def test_longurl_ged() -> None:
    # Test constructing the xref_ged test data.
    file = Util.read('tests\\data\\ged_examples\\long-url.ged')

    # Instantiate a Genealogy class.
    g = Genealogy()

    # Instantiate the cross reference identifiers.
    # There were 1 xref identifiers and 0 void identifiers.
    subm_S1_xref = g.submitter_xref('S1')

    # Instantiate the header record.
    header = gc.Head([
        gc.Gedc([
            gc.GedcVers('7.0'),
        ]),
        gc.Note('This file is intended to provide coverage of parts of the specification and does not contain meaningful historical or genealogical data.'),
        gc.Subm(subm_S1_xref),
    ])

    # Instantiate the records holding the GED data.
    subm_S1 = gc.RecordSubm(subm_S1_xref, [
        gc.Name('John Doe'),
        gc.Www('https://www.subdomain.example.com/alfa/bravo/charlie/delta/echo/foxtrot/golf/hotel/india/juliett/kilo/lima/mike/november/oscar/papa/quebec/romeo/sierra/tango/uniform/victor/whiskey/xray/yankee/zulu/Lorem%20ipsum%20dolor%20sit%20amet,%20consectetur%20adipiscing%20elit,%20sed%20do%20eiusmod%20tempor%20incididunt%20ut%20labore%20et%20dolore%20magna%20aliqua.%20Ut%20enim%20ad%20minim%20veniam,%20quis%20nostrud%20exercitation%20ullamco%20laboris%20nisi%20ut%20aliquip%20ex%20ea%20commodo%20consequat.%20Duis%20aute%20irure%20dolor%20in%20reprehenderit%20in%20voluptate%20velit%20esse%20cillum%20dolore%20eu%20fugiat%20nulla%20pariatur.%20Excepteur%20sint%20occaecat%20cupidatat%20non%20proident,%20sunt%20in%20culpa%20qui%20officia%20deserunt%20mollit%20anim%20id%20est%20laborum./filename.html'),
    ])

    # Stage the GEDCOM records to generate the ged lines.
    g.stage(header)
    g.stage(subm_S1)

    # Run the following to show the ged file that the above code would produce.
    ged_file: str = g.show_ged()


    assert file == ged_file
    

