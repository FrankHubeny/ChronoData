# Licensed under a 3-clause BSD style license - see LICENSE.md
"""Add a type to each generated GEDCOM record identification string.

References
----------
- [GEDCOM Records](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#records)
"""

class FamilyXref:
    """Assign a type to a family xref string
    of a GEDCOM Family Record.

    Reference
    ---------
    - [GEDCOM FAMILY Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_RECORD)
    """

    def __init__(self, name: str):
        self.fullname: str = name
        self.name: str = name.replace('@', '').replace('_', ' ')

    def __str__(self) -> str:
        return self.fullname

class IndividualXref:
    """Assign a type to an individual xref string
    of a GEDCOM Individual Record.

    Reference
    ---------
    - [GEDCOM INDIVIDUAL Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_RECORD)
    """

    def __init__(self, name: str):
        self.fullname: str = name
        self.name: str = name.replace('@', '').replace('_', ' ')

    def __str__(self) -> str:
        return self.fullname


class MultimediaXref:
    """Assign a type to a multimedia xref string
    of a GEDCOM Multimedia Record.

    Reference
    ---------
    - [GEDCOM MULTIMEDIA Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#MULTIMEDIA_RECORD)
    """

    def __init__(self, name: str):
        self.fullname: str = name
        self.name: str = name.replace('@', '').replace('_', ' ')

    def __str__(self) -> str:
        return self.fullname


class RepositoryXref:
    """Assign a type to a repository xref string
    of a GEDCOM Repository Record.

    Reference
    ---------
    - https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#REPOSITORY_RECORD
    """

    def __init__(self, name: str):
        self.fullname: str = name
        self.name: str = name.replace('@', '').replace('_', ' ')

    def __str__(self) -> str:
        return self.fullname


class SharedNoteXref:
    """Assign a type to a shared note xref string
    of a GEDCOM Shared_Note Record.

    Reference
    ---------
    - [GEDCOM SHARED_NOTE Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SHARED_NOTE_RECORD)
    """

    def __init__(self, name: str):
        self.fullname: str = name
        self.name: str = name.replace('@', '').replace('_', ' ')

    def __str__(self) -> str:
        return self.fullname


class SourceXref:
    """Assign a type to a source xref string
    of a GEDCOM Source Record.

    Reference
    ---------
    - [GEDCOM SOURCE Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SHARED_NOTE_RECORD)
    """

    def __init__(self, name: str):
        self.fullname: str = name
        self.name: str = name.replace('@', '').replace('_', ' ')

    def __str__(self) -> str:
        return self.fullname


class SubmitterXref:
    """Assign a type to a submitter xref string
    of a GEDCOM Submitter Record.

    Reference
    ---------
    - [GEDCOM SUBMITTER Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SUBMITTER_RECORD)
    """

    def __init__(self, name: str):
        self.fullname: str = name
        self.name: str = name.replace('@', '').replace('_', ' ')

    def __str__(self) -> str:
        return self.fullname
