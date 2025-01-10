# chronodata/records.py
"""Add a type to a GEDCOM record identification string.

There are seven GEDCOM records. The identifiers in each these seven
record categories are assigned their own type based on record category.
This prevents identifiers from being interchanged by the code
and allows the code to check user input.

Record identifier classes:

- FamilyXref, a family record identifier receives the FamilyXref type.
- IndividualXref, an individual record identifier receives the IndividualXref type.
- MultimediaXref, a multimedia record identifier receives the MultimediaXref type.
- RepositoryXref, a repository record identifier receives the RepositoryXref type.
- SharedNoteXref, a shared note record identifier receives the SharedNoteXref type.
- SourceXref, a source record identifier receives the SourceXref type.
- SubmitterXref, a submitter record identifier receives the SubmitterXref type.

References:
    [GEDCOM Records](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#records)

How To Use This Module
======================

This module is used through the `Chronology` class and the various
classes in the `store` module.  It is not used directly.

See the instructions on building a chronology in the `build` module
where an empty Chronology is instantiated and the `store` module
where data is added to it through the seven GEDCOM records.
"""

import re

from chronodata.constants import String, Tag

__all__ = [
    'FamilyXref',
    'IndividualXref',
    'MultimediaXref',
    'RepositoryXref',
    'SharedNoteXref',
    'SourceXref',
    'SubmitterXref',
]


class Xref:
    def __init__(self, name: str):
        """Initialize an instance of the class.

        Args:
        - `name`: The name of the identifier.
        """
        self.fullname: str = name
        self.name: str = name.replace('@', '').replace('_', ' ')
        self.tag: Tag = Tag.NONE
        self.code_xref = f'{self.tag.value.lower()}_{self.name.lower()}_xref'
        self.code = f'{self.tag.value.lower()}_{self.name.lower()}'

    def __str__(self) -> str:
        """Return the name used by the GEDCOM standard."""
        return self.fullname

    def ged(self, level: int = 0, info: str = '') -> str:
        """Return the identifier formatted according to the GEDCOM standard."""
        if level > 0:
            cleaned_info: str = re.sub(String.BANNED, '', info).strip()
            if info == '':
                return f'{level} {self.tag.value} {self.fullname}\n'
            return f'{level} {self.tag.value} {self.fullname} {cleaned_info}\n'
        return f'{level} {self.fullname} {self.tag.value}\n'


class FamilyXref(Xref):
    """Assign the FamilyXref type to a string.

    This class is not instantiated directly, but only through
    the `chronodata.build.family_xref()` method.

    Args:
        name: The name of the identifier.

    See Also:
        chronodata.build.family_xref()
    """

    def __init__(self, name: str):
        super().__init__(name)
        self.tag = Tag.FAM
        self.code_xref = f'{self.tag.value.lower()}_{self.name.lower()}_xref'
        self.code = f'{self.tag.value.lower()}_{self.name.lower()}'


class IndividualXref(Xref):
    """Assign the IndividualXref type to a string.

    This class is not instantiated directly, but only through
    the `chronodata.build.individual_xref()` method.

    Args:
        name: The name of the identifier.

    See Also:
        `chronodata.build.individual_xref()`

    Reference:
        [GEDCOM INDIVIDUAL Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_RECORD)
    """

    def __init__(self, name: str):
        super().__init__(name)
        self.tag = Tag.INDI
        self.code_xref = f'{self.tag.value.lower()}_{self.name.lower()}_xref'
        self.code = f'{self.tag.value.lower()}_{self.name.lower()}'
        


class MultimediaXref(Xref):
    """Assign Assign the MultimediaXref type to a string.

    This class is not instantiated directly, but only through
    the `chronodata.build.multimedia_xref()` method.

    Args:
        name: The name of the identifier.

    See Also:
        `chronodata.build.multimedia_xref()`

    Reference:
        [GEDCOM MULTIMEDIA Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#MULTIMEDIA_RECORD)
    """

    def __init__(self, name: str):
        super().__init__(name)
        self.tag = Tag.OBJE
        self.code_xref = f'{self.tag.value.lower()}_{self.name.lower()}_xref'
        self.code = f'{self.tag.value.lower()}_{self.name.lower()}'
        


class RepositoryXref(Xref):
    """Assign the RepositoryXref type to a string.

    This class is not instantiated directly, but only through
    the `chronodata.build.repository_xref()` method.

    Args:
        name: The name of the identifier.

    See Also:
        `chronodata.build.repository_xref()`

    Reference:
        https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#REPOSITORY_RECORD
    """

    def __init__(self, name: str):
        super().__init__(name)
        self.tag = Tag.REPO
        self.code_xref = f'{self.tag.value.lower()}_{self.name.lower()}_xref'
        self.code = f'{self.tag.value.lower()}_{self.name.lower()}'


class SharedNoteXref(Xref):
    """Assign the SharedNoteXref type to a string.

    This class is not instantiated directly, but only through
    the `chronodata.build.shared_note_xref()` method.

    Args:
        name: The name of the identifier.

    See Also:
        `chronodata.build.shared_note_xref()`

    Reference:
        - [GEDCOM SHARED_NOTE Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SHARED_NOTE_RECORD)
    """

    def __init__(self, name: str):
        super().__init__(name)
        self.tag = Tag.SNOTE
        self.code_xref = f'{self.tag.value.lower()}_{self.name.lower()}_xref'
        self.code = f'{self.tag.value.lower()}_{self.name.lower()}'


class SourceXref(Xref):
    """Assign the SourceXref type to a string.

    This class is not instantiated directly, but only through
    the `chronodata.build.source_xref()` method.

    Args:
        name: The name of the identifier.

    See Also:
        `chronodata.build.source_xref()`

    Reference:
        [GEDCOM SOURCE Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SHARED_NOTE_RECORD)
    """

    def __init__(self, name: str):
        super().__init__(name)
        self.tag = Tag.SOUR
        self.code_xref = f'{self.tag.value.lower()}_{self.name.lower()}_xref'
        self.code = f'{self.tag.value.lower()}_{self.name.lower()}'


class SubmitterXref(Xref):
    """Assign the SubmitterXref type to a string.

    This class is not instantiated directly, but only through
    the `chronodata.build.submitter_xref()` method.

    Args:
        name: The name of the identifier.

    See Also:
        chronodata.build.submitter_xref()

    Reference:
        [GEDCOM SUBMITTER Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SUBMITTER_RECORD)
    """

    def __init__(self, name: str):
        super().__init__(name)
        self.tag = Tag.SUBM
        self.code_xref = f'{self.tag.value.lower()}_{self.name.lower()}_xref'
        self.code = f'{self.tag.value.lower()}_{self.name.lower()}'


class Void:
    NAME: str = '@VOID@'
    FAM: FamilyXref = FamilyXref(NAME)
    INDI: IndividualXref = IndividualXref(NAME)
    OBJE: MultimediaXref = MultimediaXref(NAME)
    REPO: RepositoryXref = RepositoryXref(NAME)
    SNOTE: SharedNoteXref = SharedNoteXref(NAME)
    SOUR: SourceXref = SourceXref(NAME)
    SUBM: SubmitterXref = SubmitterXref(NAME)
