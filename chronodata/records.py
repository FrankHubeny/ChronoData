# Licensed under a 3-clause BSD style license - see LICENSE.md
"""Add a type to each generated GEDCOM record identification string.

There are seven GEDCOM records. The identifiers in each these seven
record categories are assigned their own type based on record category.
This prevents identifiers from being interchanged by the code 
and allows the code to check user input.

- FamilyXref, a family record identifier receives the FamilyXref type.
- IndividualXref, an individual record identifier receives the IndividualXref type.
- MultimediaXref, a multimedia record identifier receives the MultimediaXref type.
- RepositoryXref, a repository record identifier receives the RepositoryXref type.
- SharedNoteXref, a shared note record identifier receives the SharedNoteXref type.
- SourceXref, a source record identifier receives the SourceXref type.
- SubmitterXref, a submitter record identifier receives the SubmitterXref type.

References
----------
- [GEDCOM Records](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#records)
"""


class FamilyXref:
    """Assign the FamilyXref type to a string.

    Parameters:
        - `fullname` The name that is used in the GEDCOM file.
        - `name` The name the user entered except that it is now capitalized.

    Examples:
    This example verifies that the type has been assigned to the 'my family' string.
    >>> from chronodata.chrono import Chronology
    >>> a = Chronology('testing')
    >>> family_xref = a.family_xref('my family')
    >>> (
    ...     isinstance(family_xref, FamilyXref),
    ...     family_xref.name,
    ...     str(family_xref),
    ... )
    (True, 'MY FAMILY', '@MY_FAMILY@')

    See Also:
    - `IndividualXref`, the class for GEDCOM Individual Record identifiers.
    - `MultimediaXref`, the class for GEDCOM Multimedia Record identifiers.
    - `RepositoryXref`, the class for GEDCOM Repository Record identifiers.
    - `SharedNoteXref`, the class for GEDCOM Shared Note Record identifiers.
    - `SourceXref`, the class for GEDCOM Source Record identifiers.
    - `SubmitterXref`, the class for GEDCOM Submitter Record identifiers.

    Reference:
    - [GEDCOM FAMILY Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_RECORD)
    """

    def __init__(self, name: str):
        """
        Initialize an instance of the FamilyXref class.

        Parameters:
            fullname (str): The name used by the GEDCOM standard.
            name (str): The name used for comparison across chronologies.
        """
        self.fullname: str = name
        self.name: str = name.replace('@', '').replace('_', ' ')

    def __str__(self) -> str:
        """Return the name used by the GEDCOM standard."""
        return self.fullname


class IndividualXref:
    """Assign the IndividualXref type to string.

    A specific name need not be assigned, but for the purposes of comparing
    different chronologies it is helpful to have the same name for the individual
    across all chronologies under comparison.

    Parameters:
        - `fullname` The name that is used in the GEDCOM file.
        - `name` The name the user entered except that it is now capitalized.

    Examples:
    This example verifies that the IndividualXref type has been assigned to the
    identifier of the record associated with the name "Joe Smith".
    If a name is not specified an integer will be used to represent the record.
    >>> from chronodata.chrono import Chronology
    >>> a = Chronology('testing')
    >>> joe = a.individual_xref('Joe Smith')
    >>> isinstance(joe, IndividualXref), joe.name, str(joe)
    (True, 'JOE SMITH', '@JOE_SMITH@')

    Using this identifier for any of the other records would generate
    a type error because the required type is not the same.

    See Also:
    - `FamilyXref`, the class for GEDCOM Family Record identifiers.
    - `MultimediaXref`, the class for GEDCOM Multimedia Record identifiers.
    - `RepositoryXref`, the class for GEDCOM Repository Record identifiers.
    - `SharedNoteXref`, the class for GEDCOM Shared Note Record identifiers.
    - `SourceXref`, the class for GEDCOM Source Record identifiers.
    - `SubmitterXref`, the class for GEDCOM Submitter Record identifiers.

    Reference:
    - [GEDCOM INDIVIDUAL Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_RECORD)
    """

    def __init__(self, name: str):
        """
        Initialize an instance of the IndividualXref class.

        Parameters:
            fullname (str): The name used by the GEDCOM standard.
            name (str): The name used for comparison across chronologies.
        """
        self.fullname: str = name
        self.name: str = name.replace('@', '').replace('_', ' ')

    def __str__(self) -> str:
        """Return the name used by the GEDCOM standard."""
        return self.fullname


class MultimediaXref:
    """Assign the MultimediaXref type to a media xref string of a GEDCOM Multimedia Record.

    Parameters:
        - `fullname` The name that is used in the GEDCOM file.
        - `name` The name the user entered except that it is now capitalized.

    Examples:
    Although a specific name could be assigned, because only needs to be identified
    within a single chronology, an incremented number will do.
    >>> from chronodata.chrono import Chronology
    >>> a = Chronology('testing')
    >>> multi = a.multimedia_xref()
    >>> isinstance(multi, MultimediaXref), multi.name, str(multi)
    (True, '1', '@1@')

    See Also:
    - `FamilyXref`, the class for GEDCOM Family Record identifiers.
    - `IndividualXref`, the class for GEDCOM Individual Record identifiers.
    - `RepositoryXref`, the class for GEDCOM Repository Record identifiers.
    - `SharedNoteXref`, the class for GEDCOM Shared Note Record identifiers.
    - `SourceXref`, the class for GEDCOM Source Record identifiers.
    - `SubmitterXref`, the class for GEDCOM Submitter Record identifiers.

    Reference:
    - [GEDCOM MULTIMEDIA Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#MULTIMEDIA_RECORD)
    """

    def __init__(self, name: str):
        """
        Initialize an instance of the MultimediaXref class.

        Parameters:
            fullname (str): The name used by the GEDCOM standard.
            name (str): The name used for comparison across chronologies.
        """
        self.fullname: str = name
        self.name: str = name.replace('@', '').replace('_', ' ')

    def __str__(self) -> str:
        """Return the name used by the GEDCOM standard."""
        return self.fullname


class RepositoryXref:
    """Assign the RepositoryXref type to a string.

    Parameters:
        - `fullname` The name that is used in the GEDCOM file.
        - `name` The name the user entered except that it is now capitalized.

    Examples:
    Multiple records records of each type may be created in the same chronology.
    The following example shows the comparison of two repository record identifiers.
    >>> from chronodata.chrono import Chronology
    >>> a = Chronology('testing')
    >>> one = a.repository_xref()
    >>> two = a.repository_xref()
    >>> report_one = f'{one}: Alternate Name {one.name}, Instance Check {isinstance(one, RepositoryXref)}'
    >>> report_two = f'{two}: Alternate Name {two.name}, Instance Check {isinstance(two, RepositoryXref)}'
    >>> print(report_one)
    @1@: Alternate Name 1, Instance Check True
    >>> print(report_two)
    @2@: Alternate Name 2, Instance Check True

    See Also:
    - `FamilyXref`, the class for GEDCOM Family Record identifiers.
    - `IndividualXref`, the class for GEDCOM Individual Record identifiers.
    - `MultimediaXref`, the class for GEDCOM Multimedia Record identifiers.
    - `SharedNoteXref`, the class for GEDCOM Shared Note Record identifiers.
    - `SourceXref`, the class for GEDCOM Source Record identifiers.
    - `SubmitterXref`, the class for GEDCOM Submitter Record identifiers.

    Reference:
    - https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#REPOSITORY_RECORD
    """

    def __init__(self, name: str):
        """
        Initialize an instance of the RepositoryXref class.

        Parameters:
            fullname (str): The name used by the GEDCOM standard.
            name (str): The name used for comparison across chronologies.
        """
        self.fullname: str = name
        self.name: str = name.replace('@', '').replace('_', ' ')

    def __str__(self) -> str:
        """Return the name used by the GEDCOM standard."""
        return self.fullname


class SharedNoteXref:
    """Assign the SharedNoteXref type to a string.

    Parameters:
        - `fullname` The name that is used in the GEDCOM file.
        - `name` The name the user entered except that it is now capitalized.

    Examples:
    The following example shows that the type structure is distinguishing
    the "smith" string as a SharedNoteXref rather than some other type
    such as an IndividualXref type.
    >>> from chronodata.chrono import Chronology
    >>> a = Chronology('testing')
    >>> smith = a.shared_note_xref('some smith')
    >>> (str(smith), smith.name)
    ('@SOME_SMITH@', 'SOME SMITH')
    >>> type(smith)
    <class 'chronodata.records.SharedNoteXref'>
    >>> isinstance(smith, IndividualXref)
    False
    >>> isinstance(smith, SharedNoteXref)
    True

    See Also:
    - `FamilyXref`, the class for GEDCOM Family Record identifiers.
    - `IndividualXref`, the class for GEDCOM Individual Record identifiers.
    - `MultimediaXref`, the class for GEDCOM Multimedia Record identifiers.
    - `RepositoryXref`, the class for GEDCOM Repository Record identifiers.
    - `SourceXref`, the class for GEDCOM Source Record identifiers.
    - `SubmitterXref`, the class for GEDCOM Submitter Record identifiers.

    Reference:
    - [GEDCOM SHARED_NOTE Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SHARED_NOTE_RECORD)
    """

    def __init__(self, name: str):
        """
        Initialize an instance of the SharedNoteXref class.

        Parameters:
            fullname (str): The name used by the GEDCOM standard.
            name (str): The name used for comparison across chronologies.
        """
        self.fullname: str = name
        self.name: str = name.replace('@', '').replace('_', ' ')

    def __str__(self) -> str:
        """Return the name used by the GEDCOM standard."""
        return self.fullname


class SourceXref:
    """Assign the SourceXref type to a string.

    Parameters:
        - `fullname` The name that is used in the GEDCOM file.
        - `name` The name the user entered except that it is now capitalized.

    Examples:
    The following example shows that the string is no longer of `str` type.
    >>> from chronodata.chrono import Chronology
    >>> a = Chronology('testing')
    >>> source = a.source_xref()
    >>> report = f'Is {str(source)} still a string? {isinstance(source, str)}'
    >>> print(report)
    Is @1@ still a string? False

    See Also:
    - `FamilyXref`, the class for GEDCOM Family Record identifiers.
    - `IndividualXref`, the class for GEDCOM Individual Record identifiers.
    - `MultimediaXref`, the class for GEDCOM Multimedia Record identifiers.
    - `RepositoryXref`, the class for GEDCOM Repository Record identifiers.
    - `SharedNoteXref`, the class for GEDCOM Shared Note Record identifiers.
    - `SubmitterXref`, the class for GEDCOM Submitter Record identifiers.

    Reference:
    - [GEDCOM SOURCE Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SHARED_NOTE_RECORD)
    """

    def __init__(self, name: str):
        """
        Initialize an instance of the SourceXref class.

        Parameters:
            fullname (str): The name used by the GEDCOM standard.
            name (str): The name used for comparison across chronologies.
        """
        self.fullname: str = name
        self.name: str = name.replace('@', '').replace('_', ' ')

    def __str__(self) -> str:
        """Return the name used by the GEDCOM standard."""
        return self.fullname


class SubmitterXref:
    """Assign the SubmitterXref type to a string.

    Parameters:
        - `fullname` The name that is used in the GEDCOM file.
        - `name` The name the user entered except that it is now capitalized.

    Examples:
    >>> from chronodata.chrono import Chronology
    >>> a = Chronology('testing')
    >>> me = a.submitter_xref('my own name')
    >>> print(f'{me.name} or {str(me)}')
    MY OWN NAME or @MY_OWN_NAME@

    See Also:
    - `FamilyXref`, the class for GEDCOM Family Record identifiers.
    - `IndividualXref`, the class for GEDCOM Individual Record identifiers.
    - `MultimediaXref`, the class for GEDCOM Multimedia Record identifiers.
    - `RepositoryXref`, the class for GEDCOM Repository Record identifiers.
    - `SharedNoteXref`, the class for GEDCOM Shared Note Record identifiers.
    - `SourceXref`, the class for GEDCOM Source Record identifiers.

    Reference
    - [GEDCOM SUBMITTER Record](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SUBMITTER_RECORD)
    """

    def __init__(self, name: str):
        """
        Initialize an instance of the SubmitterXref class.

        Parameters:
            fullname (str): The name used by the GEDCOM standard.
            name (str): The name used for comparison across chronologies.
        """
        self.fullname: str = name
        self.name: str = name.replace('@', '').replace('_', ' ')

    def __str__(self) -> str:
        """Return the name used by the GEDCOM standard."""
        return self.fullname
