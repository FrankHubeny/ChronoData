# xref_test.py
"""Test the functionality of the Xref class through classes which inherit from it.

1. FamilyXref
    a. Good run.
    b. Run ged.
    c. Run code.
    d. Exceptions raised

2. IndividualXref
    a. Good run.
    b. Run ged.
    c. Run code.
    d. Exceptions raised

3. MultimediaXref
    a. Good run.
    b. Run ged.
    c. Run code.
    d. Exceptions raised

4. RepositoryXref
    a. Good run.
    b. Run ged.
    c. Run code.
    d. Exceptions raised

5. SharedNoteXref
    a. Good run.
    b. Run ged.
    c. Run code.
    d. Exceptions raised

6. SourceXref
    a. Good run.
    b. Run ged.
    c. Run code.
    d. Exceptions raised

7. SubmitterXref
    a. Good run.
    b. Run ged.
    c. Run code.
    d. Exceptions raised

8. ExtensionXref
    a. Good run.
    b. Run ged.
    c. Run code.
    d. Exceptions raised
"""

import pytest

from genedata.build import Genealogy
from genedata.structure import (
    File,
    Form,
    Name,
    RecordFam,
    RecordIndi,
    RecordObje,
    RecordRepo,
    RecordSnote,
    RecordSour,
    RecordSubm,
)

g = Genealogy('test')
fam = g.family_xref()
indi = g.individual_xref()
obje = g.multimedia_xref()
snote = g.shared_note_xref()
sour = g.source_xref()
subm = g.submitter_xref()
ext = g.extension_xref()
repo = g.repository_xref()

# 1. FamilyXref
#     a. Good run.

def test_good_family_record() -> None:
    """Instantiate a minimal RecordFam."""
    m = RecordFam(fam)
    assert m.validate()
#     b. Run ged.
#     c. Run code.
#     d. Exceptions raised

# 2. IndividualXref
#     a. Good run.

def test_good_individual_record() -> None:
    """Instantiate a minimal RecordIndi."""
    m = RecordIndi(indi)
    assert m.validate()

#     b. Run ged.
#     c. Run code.
#     d. Exceptions raised

# 3. MultimediaXref
#     a. Good run.

def test_good_multimedia_xref() -> None:
    """Instantiate a minimal RecordObje."""
    m = RecordObje(obje, File('myfile', Form('text/html')))
    assert m.validate()

#     b. Run ged.
#     c. Run code.
#     d. Exceptions raised

# 4. RepositoryXref
#     a. Good run.

def test_good_repository_xref() -> None:
    """Instantiate a minimal RecordRepo."""
    m = RecordRepo(repo, Name('you'))
    assert m.validate()

#     b. Run ged.
#     c. Run code.
#     d. Exceptions raised

# 5. SharedNoteXref
#     a. Good run.

def test_good_shared_note_xref() -> None:
    """Instantiate a minimal RecordSnote."""
    m = RecordSnote(snote)
    assert m.validate()

#     b. Run ged.
#     c. Run code.
#     d. Exceptions raised

# 6. SourceXref
#     a. Good run.

def test_good_source_xref() -> None:
    """Instantiate a minimal RecordSour."""
    m = RecordSour(sour)
    assert m.validate()

#     b. Run ged.
#     c. Run code.
#     d. Exceptions raised

# 7. SubmitterXref
#     a. Good run.

def test_good_submitter_xref() -> None:
    """Instantiate a minimal RecordSubm."""
    m = RecordSubm(subm, Name('me'))
    assert m.validate()

#     b. Run ged.
#     c. Run code.
#     d. Exceptions raised

# 8. ExtensionXref
#     a. Good run.
#     b. Run ged.
#     c. Run code.
#     d. Exceptions raised

