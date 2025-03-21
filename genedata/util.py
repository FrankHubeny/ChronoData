# util.py

__all__ = [
    #'Checker',
    'Formatter',
    'Input',
    'Tagger',
    'Util',
]

import logging
import math
import re
import urllib.request
import zipfile
from textwrap import indent
from typing import Any

import requests  # type: ignore[import-untyped]
import yaml  # type: ignore[import-untyped]
from ordered_set import OrderedSet  # type: ignore[import-not-found]

from genedata.constants import Default
from genedata.messages import Msg
from genedata.specs7 import Calendar, Month


class Util:
    """Utilities to read and write yaml or ged files."""

    @staticmethod
    def www_status(url: str) -> int:
        request: int = 0
        try:
            request = requests.head(url)
        except requests.exceptions.RequestException:
            return 0
        return request

    @staticmethod
    def list_gdz(gdz: str) -> str:
        """List the files in a GEDCOM gdz archive file.

        Args:
            gdz: The path to the archive gdz file.
        """
        lines: str = Default.EMPTY
        with zipfile.ZipFile(gdz, 'r') as zip_ref:
            # List all the file names in the zip
            for file_name in zip_ref.namelist():
                lines = ''.join([lines, file_name, Default.EOL])
        return lines

    @staticmethod
    def read_gdz_ged_file(file: str, gdz: str) -> str:
        """Read a file from a GEDCOM gdz archive file.

        Args:
            gdz: The path to the archive gdz file.
        """
        with zipfile.ZipFile(gdz, 'r') as zip_ref:
            for file_name in zip_ref.namelist():
                if file_name == file:
                    with zip_ref.open(file_name) as f:
                        return (
                            f.read()
                            .decode('utf-8')
                            .replace('\r\n', '\n')
                            .replace('\ufeff', '')
                        )
        return Default.EMPTY

    @staticmethod
    def extract(
        file: str,
        zipped_files: str,
        to_directory: str,
        password: bytes = b'',
    ) -> None:
        # Create a ZipFile object without a password.
        if password == b'':
            with zipfile.ZipFile(zipped_files, 'r') as zip_ref:
                zip_ref.extract(file, to_directory)
        # else:
        #     with zipfile.ZipFile(
        #         zipped_files, 'r', zipfile.ZipFile.setpassword(pwd=password)
        #     ) as zip_ref:
        #         zip_ref.extract(file, to_directory)

    @staticmethod
    def read_binary(url: str) -> str:
        """Read a yaml file and convert it into a dictionary.

        Args:
            url: The name of the file or the internet url.
        """

        # Read the internet file or a local file.
        if url[0:4] == 'http':
            webUrl = urllib.request.urlopen(url)
            result_code = str(webUrl.getcode())
            if result_code == '404':
                raise ValueError(Msg.PAGE_NOT_FOUND.format(url))
            raw: str = webUrl.read().decode(Default.UTF8)
        else:
            with open(url, 'rb') as file:  # noqa: PTH123
                binary_raw = file.read()
            raw = binary_raw.decode('utf-8')
        return raw

    @staticmethod
    def read(url: str) -> str:
        """Read a yaml file and convert it into a dictionary.

        Args:
            url: The name of the file or the internet url.
        """

        # Read the internet file or a local file.
        if url[0:4] == 'http':
            webUrl = urllib.request.urlopen(url)
            result_code = str(webUrl.getcode())
            if result_code == '404':
                raise ValueError(Msg.PAGE_NOT_FOUND.format(url))
            raw: str = webUrl.read().decode(Default.UTF8)
        else:
            with open(url) as file:  # noqa: PTH123
                raw = file.read()
        return raw

    @staticmethod
    def write_ged(ged: str, file: str) -> None:
        """Write a ged string to a file in a directory.

        Args:
            ged: The string to write to the file.
            file: The full path of the file.
        """
        with open(file, 'w') as f:  # noqa: PTH123
            f.write(ged)

    @staticmethod
    def read_yaml(url: str) -> dict[str, Any]:
        """Read a yaml file and convert it into a dictionary.

        Args:
            url: The name of the file or the internet url.
        """

        # Retrieve the file.
        raw: str = Util.read_binary(url)

        # Check that file has proper yaml directive.
        if Default.YAML_DIRECTIVE not in raw:
            raise ValueError(
                Msg.YAML_NOT_YAML_FILE.format(url, Default.YAML_DIRECTIVE)
            )

        # Return the dictionary.
        yaml_data = raw
        yaml_dict: dict[str, Any] = yaml.safe_load(yaml_data)
        return yaml_dict

    @staticmethod
    def ged_summary(ged: str) -> str:
        """Summarize the contents of a ged file.

        Args:
            ged: The string obtained from reading or producing a ged file.
        """

        # Count the number of record types.
        fam_count: int = len(re.findall('\n0.+FAM', ged))
        indi_count: int = len(re.findall('\n0.+INDI', ged))
        obje_count: int = len(re.findall('\n0.+OBJE', ged))
        repo_count: int = len(re.findall('\n0.+REPO', ged))
        snote_count: int = len(re.findall('\n0.+SNOTE', ged))
        sour_count: int = len(re.findall('\n0.+SOUR', ged))
        subm_count: int = len(re.findall('\n0.+SUBM', ged))

        # Return the number of record types.
        return f"""
Families      {fam_count!s}
Individuals   {indi_count!s}
Multimedia    {obje_count!s}
Repositories  {repo_count!s}
Shared Notes  {snote_count!s}
Sources       {sour_count!s}
submitters    {subm_count!s}
"""

    @staticmethod
    def compare(first: str, second: str) -> str:
        if first == second:
            return f'{first}\nSuccessful Match'
        lines: str = Default.EMPTY
        split_first: list[str] = first.split('\n')
        split_second: list[str] = second.split('\n')
        len_split_first: int = len(split_first)
        len_split_second: int = len(split_second)
        for i in range(min(len_split_first, len_split_second)):
            problem: str = Default.EMPTY
            if split_first[i] != split_second[i]:
                problem = 'PROBLEM:   '
                lines = ''.join(
                    [
                        lines,
                        Default.EOL,
                        problem,
                        "'",
                        split_first[i],
                        "' does not equal '",
                        split_second[i],
                        "'",
                    ]
                )
            else:
                lines = ''.join(
                    [
                        lines,
                        Default.EOL,
                        split_first[i],
                    ]
                )
        if len_split_first > len_split_second:
            lines = ''.join(
                [
                    lines,
                    Default.EOL,
                    'The first string is longer than the second.  Here are the remaining lines:',
                ]
            )
            for line in split_first[len_split_second:]:
                lines = ''.join(
                    [
                        lines,
                        Default.EOL,
                        line,
                    ]
                )
        elif len_split_first < len_split_second:
            lines = ''.join(
                [
                    lines,
                    Default.EOL,
                    'The second string is longer than the first.  Here are the remaining lines:',
                ]
            )
            for line in split_second[len_split_first:]:
                lines = ''.join(
                    [
                        lines,
                        Default.EOL,
                        line,
                    ]
                )
        return lines
    


# class Checker:
#     """Global methods supporting validation of data."""

#     @staticmethod
#     def verify_type(value: Any, value_type: Any, no_list: bool = False) -> bool:
#         """Check if the value has the specified type."""
#         check: bool = True
#         if value is None:
#             return check
#         if isinstance(value, list):
#             if no_list and isinstance(value, list):
#                 raise TypeError(Msg.NO_LIST)
#             for item in value:
#                 if not isinstance(item, value_type):
#                     raise TypeError(
#                         Msg.WRONG_TYPE.format(item, type(item), value_type)
#                     )
#             return check
#         if not isinstance(value, value_type):
#             raise TypeError(
#                 Msg.WRONG_TYPE.format(value, type(value), value_type)
#             )
#         return check

#     @staticmethod
#     def verify_tuple_type(name: Any, value_type: Any) -> bool:
#         """Check if each member of the tuple has the specified type."""
#         if name != [] and name is not None:
#             for value in name:
#                 Checker.verify_type(value, value_type)
#         return True

#     @staticmethod
#     def verify_not_empty(value: Any) -> bool:
#         if value is None:
#             raise ValueError(Msg.NO_NONE)
#         if isinstance(value, str) and value == Default.EMPTY:
#             raise ValueError(Msg.NO_EMPTY_STRING)
#         if isinstance(value, list) and len(value) == 0:
#             raise ValueError(Msg.NO_EMPTY_LIST)
#         # if isinstance(value, Xref) and value.fullname == Default.VOID_POINTER:
#         #     raise ValueError(Msg.NO_EMPTY_POINTER)
#         return True


class Input:
    @staticmethod
    def age(
        years: int | float = -1,
        months: int | float = -1,
        weeks: int | float = -1,
        days: int | float = -1,
        greater_less_than: str = Default.GREATER_LESS_THAN,
    ) -> str:
        """The formatted age based on the GEDCOM specification.

        Example:
            The following example has 1.1 years, 2.2 weeks and 1 day.  Since the values
            are rounded down it is best to include non-negative integers for the years, months,
            weeks and days.
            >>> from genedata.util import Input
            >>> Input.age(1.1, -1, 2.2, 1)
            '> 1y 2w 1d'

            Negative values will not display that unit.
            >>> Input.age(-2, -14.2, -1, 1)
            '> 1d'

        args:
            years: The number of years rounded down to an integer value.
            months: The number of months in addition to the years rounded down to an integer value.
            weeks: The number of weeks in addition to the years and months rounded down to an integer value.
            days: The number of days in addition to the years, months and weeks rounded down to an integer value.
            greater_less_than: A choice between ">", greater than, "<", less than, or "" equal.

        Reference:
        - [GEDCOM Age type](https://gedcom.io/terms/v7/type-Age)
        """
        info: str = Default.EMPTY
        if years >= 0:
            info = ''.join([info, f' {int(years)!s}{Default.AGE_YEAR}'])
        if months >= 0:
            info = ''.join([info, f' {int(months)!s}{Default.AGE_MONTH}'])
        if weeks >= 0:
            info = ''.join([info, f' {int(weeks)!s}{Default.AGE_WEEK}'])
        if days >= 0:
            info = ''.join([info, f' {int(days)!s}{Default.AGE_DAY}'])
        info.replace(Default.SPACE_DOUBLE, Default.SPACE).replace(
            Default.SPACE_DOUBLE, Default.SPACE
        ).strip()
        if info == Default.EMPTY:
            greater_less_than = Default.EMPTY
        return f'{greater_less_than}{info}'.strip()

    @staticmethod
    def date(
        year: int,
        month: int = 0,
        day: int = 0,
        calendar: str = 'GREGORIAN',
        show: bool = False,
    ) -> str:
        """Format a date based on GEDCOM specifications.

        Args:
            year: The integer value of the year.
            month: The integer value of the month in the year.
            day: The integer value of the day in the year.
            calendar: The calendar to use.
            show: If True then the calendar name will be displayed in front of the date.

        Reference:
        - [GEDCOM Date Type](https://gedcom.io/terms/v7/type-Date)"""
        calendar_tag: str = Default.EMPTY
        if show:
            calendar_tag = Calendar[calendar]['standard tag']
        epoch_list: list[str] = Calendar[calendar]['epochs']
        epoch: str = Default.EMPTY
        if year < 0 and len(epoch_list) > 0:
            epoch = epoch_list[0]
            year = abs(year)
        if calendar in ['GREGORIAN', 'JULIAN'] and year == 0:
            raise ValueError(Msg.ZERO_YEAR.format(calendar))
        month_tag: str = Default.EMPTY
        if month > 0:
            month_spec: str = Calendar[calendar]['months'][month - 1]
            month_tag = Month[month_spec[month_spec.rfind('month-') + 6 :]][
                'standard tag'
            ]
        day_tag: str = Default.EMPTY
        if day > 0:
            day_tag = str(day)
        return (
            f'{calendar_tag} {day_tag} {month_tag} {year!s} {epoch}'.replace(
                '  ', ' '
            )
            .replace('  ', ' ')
            .replace('  ', ' ')
            .strip()
        )

    @staticmethod
    def date_period(
        from_date: str = Default.EMPTY, to_date: str = Default.EMPTY
    ) -> str:
        """Display a date period according to GEDCOM specifications.

        The date_period may be empty.

        Examples:
            This example constructs a date period using the Input.date method to construct the from and to dates.
            >>> from genedata.util import Input
            >>> Input.date_period(
            ...     Input.date(2024, 1, 1), Input.date(2025, 1, 1)
            ... )
            'FROM 1 JAN 2024 TO 1 JAN 2025'

            This example displays the calendar name on the from date:
            >>> Input.date_period(
            ...     Input.date(2024, 1, 1), Input.date(2025, 1, 1, show=True)
            ... )
            'FROM 1 JAN 2024 TO GREGORIAN 1 JAN 2025'

        Args:
            from_date: The earliest date of the period.
            to_date: The latest date of the period which may be the only date entered of the period.


        References:
        - [GEDCOM Date Type](https://gedcom.io/terms/v7/type-Date)
        """
        to_value: str = Default.EMPTY
        from_value: str = Default.EMPTY
        if to_date != Default.EMPTY:
            to_value = f'TO {to_date}'
        if from_date != Default.EMPTY:
            from_value = f'FROM {from_date} '
        return f'{from_value}{to_value}'.strip()

    @staticmethod
    def date_between_and(
        between_date: str = Default.EMPTY, and_date: str = Default.EMPTY
    ) -> str:
        """Display a date period according to GEDCOM specifications.

        The date_period may be empty.

        Examples:
            This example constructs a date period using the Input.date method to construct each date.
            The default calendar is the Gregorian calendar.
            >>> from genedata.util import Input
            >>> Input.date_between_and(
            ...     Input.date(2024, 1, 1), Input.date(2025, 1, 1)
            ... )
            'BET 1 JAN 2024 AND 1 JAN 2025'

            This example displays the calendar name on the from date:
            >>> Input.date_between_and(
            ...     Input.date(2024, 1, 1), Input.date(2025, 1, 1, show=True)
            ... )
            'BET 1 JAN 2024 AND GREGORIAN 1 JAN 2025'

        Args:
            between_date: The date following the BET tag.
            and_date: The date following the AND tag.

        References:
        - [GEDCOM Date Type](https://gedcom.io/terms/v7/type-Date)
        """
        between_value: str = Default.EMPTY
        and_value: str = Default.EMPTY
        if between_date != Default.EMPTY:
            between_value = f'BET {between_date}'
        if and_date != Default.EMPTY:
            and_value = f' AND {and_date} '
        return f'{between_value}{and_value}'.strip()

    @staticmethod
    def date_after(date: str = Default.EMPTY) -> str:
        """Format a date with the AFT tag in front of it.

        Examples:
            This example constructs a date after using the Input.date method to construct date.
            >>> from genedata.util import Input
            >>> Input.date_after(Input.date(2024, 1, 1))
            'AFT 1 JAN 2024'

            This example displays the calendar name on the date:
            >>> Input.date_after(Input.date(2025, 1, 1, show=True))
            'AFT GREGORIAN 1 JAN 2025'

        Args:
            date: The date following the AFT tag.

        References:
        - [GEDCOM Date Type](https://gedcom.io/terms/v7/type-Date)
        """
        value: str = Default.EMPTY
        if date != Default.EMPTY:
            value = f'AFT {date}'
        return value

    @staticmethod
    def date_before(date: str = Default.EMPTY) -> str:
        """Display a date with the BEF tag according to GEDCOM specifications.

        Examples:
            This example constructs a date from the Input.date method.
            This method attached the BEF tag in front of that date.
            >>> from genedata.util import Input
            >>> Input.date_before(Input.date(2024, 1, 1))
            'BEF 1 JAN 2024'

            This example displays the calendar name on the date:
            >>> Input.date_before(Input.date(2025, 1, 1, show=True))
            'BEF GREGORIAN 1 JAN 2025'

        Args:
            date: The date following the BEF tag.

        References:
        - [GEDCOM Date Type](https://gedcom.io/terms/v7/type-Date)
        """
        value: str = Default.EMPTY
        if date != Default.EMPTY:
            value = f'BEF {date}'
        return value

    @staticmethod
    def date_about(date: str = Default.EMPTY) -> str:
        """Display a date with the ABT tag according to GEDCOM specifications.

        Examples:
            This example constructs a date from the Input.date method.
            This method attaches the ABT tag in front of that date.
            >>> from genedata.util import Input
            >>> Input.date_about(Input.date(2024, 1, 1))
            'ABT 1 JAN 2024'

            This example displays the calendar name on the date:
            >>> Input.date_about(Input.date(2025, 1, 1, show=True))
            'ABT GREGORIAN 1 JAN 2025'

        Args:
            date: The date following the AFT tag.

        References:
        - [GEDCOM Date Type](https://gedcom.io/terms/v7/type-Date)
        """
        value: str = Default.EMPTY
        if date != Default.EMPTY:
            value = f'ABT {date}'
        return value

    @staticmethod
    def date_calculated(date: str = Default.EMPTY) -> str:
        """Display a date with the CAL tag according to GEDCOM specifications.

        Examples:
            This example constructs a date from the Input.date method.
            This method attaches the CAL tag in front of that date.
            >>> from genedata.util import Input
            >>> Input.date_calculated(Input.date(2024, 1, 1))
            'CAL 1 JAN 2024'

            This example displays the calendar name on the date:
            >>> Input.date_calculated(Input.date(2025, 1, 1, show=True))
            'CAL GREGORIAN 1 JAN 2025'

        Args:
            date: The date following the AFT tag.

        References:
        - [GEDCOM Date Type](https://gedcom.io/terms/v7/type-Date)
        """
        value: str = Default.EMPTY
        if date != Default.EMPTY:
            value = f'CAL {date}'
        return value

    @staticmethod
    def date_estimated(date: str = Default.EMPTY) -> str:
        """Display a date with the EST tag according to GEDCOM specifications.

        Examples:
            This example constructs a date from the Input.date method.
            This method attaches the EST tag in front of that date.
            >>> from genedata.util import Input
            >>> Input.date_estimated(Input.date(2024, 1, 1))
            'EST 1 JAN 2024'

            This example displays the calendar name on the date:
            >>> Input.date_estimated(Input.date(2025, 1, 1, show=True))
            'EST GREGORIAN 1 JAN 2025'

        Args:
            date: The date following the AFT tag.

        References:
        - [GEDCOM Date Type](https://gedcom.io/terms/v7/type-Date)
        """
        value: str = Default.EMPTY
        if date != Default.EMPTY:
            value = f'EST {date}'
        return value

    @staticmethod
    def form(form1: str, form2: str, form3: str, form4: str) -> str:
        """Format the place form separating each component with a comma.

        Example:
            This example illustrates the formatting provided.
            >>> from genedata.util import Input
            >>> Input.form('City', 'State', 'County', 'Country')
            'City, State, County, Country'
        """
        return ''.join(
            [
                form1,
                Default.LIST_ITEM_SEPARATOR,
                form2,
                Default.LIST_ITEM_SEPARATOR,
                form3,
                Default.LIST_ITEM_SEPARATOR,
                form4,
            ]
        )

    @staticmethod
    def from_ged(lines: str | list[list[str]]) -> str:
        if isinstance(lines, str):
            strlist: list[list[str]] = [
                a.split(' ') for a in lines.split('\n') if a != ''
            ]
            return Input.from_ged(strlist)
        level: int = int(lines[0][0])
        tag: str = lines[0][1]
        payload: str = Default.EMPTY
        output: str = Default.EMPTY
        number_of_lines: int = len(lines)
        if len(lines[0]) == 3:
            payload = lines[0][2]
        output = f'{tag}({payload}'
        intermediate_lines: list[list[str]] = []
        number_of_lines = len(lines[1:])
        for i in range(number_of_lines):
            if int(lines[i][0]) == level and len(intermediate_lines) > 0:
                output = ''.join(
                    [output, '[', Input.from_ged(intermediate_lines), '])']
                )
                intermediate_lines = []
            elif int(lines[i][0]) == level:
                output = ''.join([output, ')'])
                if i < number_of_lines:
                    return ''.join(
                        [',', output, Input.from_ged(lines[i:]), ')']
                    )
                return output
            else:
                intermediate_lines.append(lines[i])
        return output

    @staticmethod
    def lati(
        degrees: int, minutes: int, seconds: float, precision: int = 6
    ) -> str:
        latitude = Input.to_decimal(degrees, minutes, seconds, precision)
        if latitude > Default.LATI_HIGH or latitude < Default.LATI_LOW:
            raise ValueError(
                Msg.LATI_RANGE_METHOD.format(
                    latitude, Default.LATI_LOW, Default.LATI_HIGH
                )
            )
        if degrees >= 0:
            return f'{Default.LATI_NORTH}{latitude!s}'
        return f'{Default.LATI_SOUTH}{abs(latitude)!s}'

    @staticmethod
    def long(
        degrees: int, minutes: int, seconds: float, precision: int = 6
    ) -> str:
        longitude = Input.to_decimal(degrees, minutes, seconds, precision)
        if longitude > Default.LONG_HIGH or longitude < Default.LONG_LOW:
            raise ValueError(
                Msg.LONG_RANGE_METHOD.format(
                    longitude, Default.LONG_LOW, Default.LONG_HIGH
                )
            )
        if degrees >= 0:
            return f'{Default.LONG_EAST}{longitude!s}'
        return f'{Default.LONG_WEST}{abs(longitude)!s}'

    @staticmethod
    def name(full: str, surname: str) -> str:
        """Format a personal name to meet GEDCOM name type specifications.

        Example:
            >>> from genedata.util import Input
            >>> Input.name('Jim Smith', 'Smith')
            'Jim /Smith/'

            If more than one space separates parts of the name they are removed along with
            spaces at the beginning or end of the name.
            >>> Input.name(' Jim      Smith ', '   Smith ')
            'Jim /Smith/'

            Line breaks are also removed from both name and surname.
            >>> Input.name(' Jim\\n\\n\\nSmith\\n', '\\n\\nSmith\\n')
            'Jim /Smith/'

            This methods assists formatting a personal name using IndiName.
            >>> from genedata.classes7 import IndiName
            >>> m = IndiName(Input.name('Jim Smith', 'Smith'))
            >>> print(m.ged())
            1 NAME Jim /Smith/
            <BLANKLINE>

        Args:
            full: The full name of the person.
            surname: The surname of the person. This will be used to put a "/" around the surname
                in the full name.

        Reference:
        - [GEDCOM type Name](https://gedcom.io/terms/v7/type-Name)
        """

        # Remove extraneous characters from full.
        edited_name: str = full
        edited_name = re.sub(Default.EOL, Default.SPACE, edited_name)
        while Default.SPACE_DOUBLE in edited_name:
            edited_name = re.sub(
                Default.SPACE_DOUBLE, Default.SPACE, edited_name
            )
        edited_name = edited_name.strip()

        # Remove extraneous characters from surname.
        edited_surname: str = surname
        edited_surname = re.sub(Default.EOL, Default.SPACE, edited_surname)
        while Default.SPACE_DOUBLE in edited_surname:
            edited_surname = re.sub(
                Default.SPACE_DOUBLE, Default.SPACE, edited_surname
            )
        edited_surname = edited_surname.strip()

        # Replace surname in full with slashed surname.
        if edited_surname in edited_name:
            surname_slash = f'{Default.SLASH}{edited_surname}{Default.SLASH}'
            edited_name = re.sub(edited_surname, surname_slash, edited_name)
        return edited_name

    @staticmethod
    def phone(country: int, area: int, prefix: int, line: int) -> str:
        """Format a phone string to meet the GEDCOM standard.

        The International Notation from the ITU-T E.123 standard
        are followed.  Spaces are used between the country, area_code, prefix and line numbers.
        A `+` precedes the country code.

        The GEDCOM standard does not require this international notation, but recommends it.
        This method formats for the optional international notation should the user
        choose to have a method format the number in a uniform manner.

        If the number cannot be formatted correctly with this method any string is accepted
        as a phone number.

        One may use this for fax numbers as well.

        Examples:
            The first example shows the use of the default, US, international number.
            >>> from genedata.util import Input
            >>> Input.phone(1, 123, 456, 7890)
            '+1 123 456 7890'

            The second example provides a non-US country number.
            >>> Input.phone(44, 123, 456, 7890)
            '+44 123 456 7890'

        Args:
            country: The country code greater than 0 and and less than 1000.
            area: The area code for the phone number greater than 0 and less than 1000.
            prefix: The prefix portion of the phone number greater than 0 and less than 1000.
            line: The line portion of the phone number greater than 0 and less than 10000.

        Reference:
            [GEDCOM Standard](https://gedcom.io/terms/v7/PHON)
            [ITU-T E.123 Standard](https://www.itu.int/rec/T-REC-E.123-200102-I/en)
        """
        if not Default.PHONE_COUNTRY_MIN < country < Default.PHONE_COUNTRY_MAX:
            raise ValueError(
                Msg.PHONE_COUNTRY_CODE.format(
                    country,
                    Default.PHONE_COUNTRY_MIN,
                    Default.PHONE_COUNTRY_MAX,
                )
            )
        if not Default.PHONE_AREA_MIN < area < Default.PHONE_AREA_MAX:
            raise ValueError(
                Msg.PHONE_AREA_CODE.format(
                    area, Default.PHONE_AREA_MIN, Default.PHONE_AREA_MAX
                )
            )
        if not Default.PHONE_PREFIX_MIN < prefix < Default.PHONE_PREFIX_MAX:
            raise ValueError(
                Msg.PHONE_PREFIX_CODE.format(
                    prefix, Default.PHONE_PREFIX_MIN, Default.PHONE_PREFIX_MAX
                )
            )
        if not Default.PHONE_LINE_MIN < line < Default.PHONE_LINE_MAX:
            raise ValueError(
                Msg.PHONE_LINE_CODE.format(
                    line, Default.PHONE_LINE_MIN, Default.PHONE_LINE_MAX
                )
            )
        return f'+{country!s} {area!s} {prefix!s} {line!s}'

    @staticmethod
    def place(place1: str, place2: str, place3: str, place4: str) -> str:
        """Format the place components separating them with a comma.

        Example:
            This example illustrates the formatting provided.
            >>> from genedata.util import Input
            >>> Input.form('Chicago', 'Illinois', 'Cook', 'USA')
            'Chicago, Illinois, Cook, USA'
        """
        return ''.join(
            [
                place1,
                Default.LIST_ITEM_SEPARATOR,
                place2,
                Default.LIST_ITEM_SEPARATOR,
                place3,
                Default.LIST_ITEM_SEPARATOR,
                place4,
            ]
        )

    @staticmethod
    def to_dms(position: float, precision: int = 6) -> tuple[int, int, float]:
        """Convert a measurment in decimals to one showing degrees, minutes
        and sconds.

        >>> from genedata.util import Input
        >>> Input.to_dms(49.29722222222, 10)
        (49, 17, 49.999999992)

        See Also:
            - `to_decimal`: Convert degrees, minutes, seconds with precision to a decimal.

        """
        minutes_per_degree = 60
        seconds_per_degree = 3600
        degrees: int = math.floor(position)
        minutes: int = math.floor((position - degrees) * minutes_per_degree)
        seconds: float = round(
            (position - degrees - (minutes / minutes_per_degree))
            * seconds_per_degree,
            precision,
        )
        return (degrees, minutes, seconds)

    @staticmethod
    def to_decimal(
        degrees: int, minutes: int, seconds: float, precision: int = 6
    ) -> float:
        """Convert degrees, minutes and seconds to a decimal.

        Example:
            The specification for the LATI and LONG structures (tags) offer the
            following example.
            >>> from genedata.util import Input
            >>> Input.to_decimal(168, 9, 3.4, 6)
            168.150944

        Args:
            degrees: The degrees in the angle whether latitude or longitude.
            minutes: The minutes in the angle.
            seconds: The seconds in the angle.
            precision: The number of digits to the right of the decimal point.

        See Also:
            - `to_dms`: Convert a decimal to degrees, minutes, seconds to a precision.

        Reference:
            [GEDCOM LONG structure](https://gedcom.io/terms/v7/LONG)
            [GEDCOM LATI structure](https://gedcom.io/terms/v7/LATI)

        """
        sign: int = -1 if degrees < 0 else 1
        degrees = abs(degrees)
        minutes_per_degree = 60
        seconds_per_degree = 3600
        return round(
            sign * degrees
            + (minutes / minutes_per_degree)
            + (seconds / seconds_per_degree),
            precision,
        )

    @staticmethod
    def www(url: str) -> str:
        """Test a url to see if it can be reached.

        If the site cannot be reached a warning message through the
        logging system is sent.  In all cases the url is returned.

        This may be helpful when using the WWW structure (class Www) to
        test the url that one enters into that structure.

        Args:
            url: The address of the site.

        Example:
            The following example would send a logging message warning
            that the site "abc" cannot be reached.
            >>> from genedata.util import Input
            >>> from genedata.classes7 import Www
            >>> response = Www(Input.www('abc'))
            >>> print(response.ged(1))
            1 WWW abc
            <BLANKLINE>

        Reference:
        - [GEDCOM WWW Structure](https://gedcom.io/terms/v7/WWW)

        """
        response: int = Util.www_status(url)
        if response != 200:
            logging.warning(Msg.WWW_RESPONSE.format(url, response))
        return url


class Tagger:
    """Global methods to tag GEDCOM information.

    There are five methods.
    - `clean_input` makes sure that user input does not contain banned utf-8 strings.
    - `taginfo` performs the base tagging process calling clean_input on user input.
    - `empty` constructs a tag where there is no user input.
    - `string` constructs a tag on user input or a list of a similar type of user input.
    - `structure` runs the ged method on an already tagged structure or a list of
        similar structures adding them to the final GEDCOM string.
    """

    @staticmethod
    def clean_input(input: str) -> str:
        """Remove banned GEDCOM unicode characters from input strings.

        The control characters U+0000 - U+001F and the delete character U+007F
        are listed in the
        [C0 Controls and Basic Latin](https://www.unicode.org/charts/PDF/U0000.pdf)
        chart.

        The code points U+D800 - U+DFFF are not interpreted.
        They are described in the
        [High Surrogate Area](https://www.unicode.org/charts/PDF/UD800.pdf) and
        [Low Surrogate Area](https://www.unicode.org/charts/PDF/UDC00.pdf)
        standards.

        The code points U+FFFE and U+FFFF are noncharacters as described in the
        [Specials](https://www.unicode.org/charts/PDF/UFFF0.pdf) standard.

        Examples:


        Reference:
            - [GEDCOM Characters](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#characters)
            - [Unicode Specification](https://www.unicode.org/versions/Unicode16.0.0/#Summary)
            - [Python re Module](https://docs.python.org/3/library/re.html)
        """

        return re.sub(Default.BANNED, Default.EMPTY, input)

    @staticmethod
    def taginfo(
        level: int,
        tag: str,
        payload: str = Default.EMPTY,
        extra: str = Default.EMPTY,
        format: bool = True,
        xref: str = Default.EMPTY,
    ) -> str:
        """Return a GEDCOM formatted line for the information and level.

        This is suitable for most tagged lines to guarantee it is uniformly
        formatted.  Although the user need not worry about calling this line,
        it is provided so the user can see the GEDCOM formatted output
        that would result.

        Example:
            The main use of this method generates a GEDCOM line.
            Note how the initial and ending spaces have been stripped from
            the input value.
            >>> from genedata.util import Tagger
            >>> print(Tagger.taginfo(1, 'NAME', '  Some Name'))
            1 NAME   Some Name
            <BLANKLINE>

            There can also be an extra parameter.
            >>> print(Tagger.taginfo(1, 'NAME', 'SomeName', 'Other info'))
            1 NAME SomeName Other info
            <BLANKLINE>

            This example comes from the [GEDCOM lines standard](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#lines):
            Note how the `@me` was reformatted as `@@me`.
            > 1 NOTE me@example.com is my email
            > 2 CONT @@me and @I are my social media handles
            >>> from genedata.classes7 import Note
            >>> mynote = Note(
            ...     '''me@example.com is my email
            ... @me and @I are my social media handles'''
            ... )
            >>> print(mynote.ged(1))
            1 NOTE me@example.com is my email
            2 CONT @@me and @I are my social media handles
            <BLANKLINE>

            However, escaping the '@' should not occur when this is part of a cross-reference identifier.


        Reference:
            [GEDCOM Lines](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#lines)

        """
        lineval: str = payload
        if format and lineval != Default.EMPTY and lineval[0] == Default.ATSIGN:
            lineval = ''.join([Default.ATSIGN, lineval])
        if xref == Default.EMPTY:
            if extra == Default.EMPTY:
                if lineval == Default.EMPTY:
                    return f'{level} {tag}{Default.EOL}'
                return (
                    f'{level} {tag} {Tagger.clean_input(lineval)}{Default.EOL}'
                )
            return f'{level} {tag} {Tagger.clean_input(lineval)} {Tagger.clean_input(extra)}{Default.EOL}'
        if extra == Default.EMPTY:
            if lineval == Default.EMPTY:
                return f'{level} {xref} {tag}{Default.EOL}'
            return f'{level} {xref} {tag} {Tagger.clean_input(lineval)}{Default.EOL}'
        return f'{level} {xref} {tag} {Tagger.clean_input(lineval)} {Tagger.clean_input(extra)}{Default.EOL}'

    @staticmethod
    def empty(
        lines: str, level: int, tag: str, xref: str = Default.EMPTY
    ) -> str:
        """Join a GEDCOM line that has only a level and a tag to a string.

        This method implements the
        [GEDCOM empty LineVal standard](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#lines) which reads:
        > Note that production LineVal does not match the empty string.
        > Because empty payloads and missing payloads are considered equivalent,
        > both a structure with no payload and a structure with the empty string
        > as its payload are encoded with no LineVal and no space after the Tag.

        Example:
            >>> from genedata.util import Tagger
            >>> lines = ''
            >>> lines = Tagger.empty(lines, 1, 'MAP')
            >>> print(lines)
            1 MAP
            <BLANKLINE>

        Args:
            lines: The prefix of the returned string.
            level: The GEDCOM level of the structure.
            tag: The tag to apply to this line.
            xref: The cross reference identifier.

        """
        if xref == Default.EMPTY:
            return ''.join([lines, Tagger.taginfo(level, tag)])
        return ''.join([lines, Tagger.taginfo(level, tag, xref=xref)])

    @staticmethod
    def string(
        lines: str,
        level: int,
        tag: str,
        payload: list[str] | str | None,
        extra: str = Default.EMPTY,
        format: bool = True,
        xref: str = Default.EMPTY,
    ) -> str:
        """Join a string or a list of string to GEDCOM lines.

        This method hides the concatenation of the already constructed
        GEDCOM file with the new line and the check that this should only
        be done if the payload is not empty.  It also hides checking
        whether the string is part of a list or not.

        Examples:
            Suppose there is only one string that should be tagged.
            >>> from genedata.util import Tagger
            >>> lines = ''
            >>> lines = Tagger.empty(lines, 1, 'MAP')
            >>> lines = Tagger.string(lines, 2, 'LATI', 'N30.0')
            >>> lines = Tagger.string(lines, 2, 'LONG', 'W30.0')
            >>> print(lines)
            1 MAP
            2 LATI N30.0
            2 LONG W30.0
            <BLANKLINE>

            Suppose there are a list of strings that should be tagged.
            >>> lines = ''
            >>> wwws = [
            ...     'https://here.com',
            ...     'https://there.com',
            ...     'https://everywhere.com',
            ... ]
            >>> lines = Tagger.string(lines, 3, 'WWW', wwws)
            >>> print(lines)
            3 WWW https://here.com
            3 WWW https://there.com
            3 WWW https://everywhere.com
            <BLANKLINE>

        Args:
            lines: The prefix string that will be appended to.
            level: The GEDCOM level of the structure.
            tag: The tag to apply to this line.
            records: The list of strings to tag.
            format: If true and '@' begins the line then escape it with another '@' otherwise not.
            xref: The cross reference identifier.
        """

        if payload is None:
            return lines
        if isinstance(payload, list):
            for item in payload:
                if Default.EOL in item:
                    items: list[str] = item.split(Default.EOL)
                    lines = Tagger.string(
                        lines, level, tag, items[0], format=format, xref=xref
                    )
                    lines = Tagger.string(
                        lines,
                        level + 1,
                        Default.CONT,
                        items[1:],
                        format=format,
                    )
                else:
                    lines = ''.join(
                        [
                            lines,
                            Tagger.taginfo(
                                level, tag, item, format=format, xref=xref
                            ),
                        ]
                    )
            return lines
        if payload != Default.EMPTY and payload is not None:
            if Default.EOL in payload:
                payloads: list[str] = payload.split(Default.EOL)
                lines = Tagger.string(
                    lines, level, tag, payloads[0], format=format, xref=xref
                )
                lines = Tagger.string(
                    lines,
                    level + 1,
                    Default.CONT,
                    payloads[1:],
                    format=format,
                )
            else:
                return ''.join(
                    [
                        lines,
                        Tagger.taginfo(
                            level, tag, payload, extra, format=format, xref=xref
                        ),
                    ]
                )
        return lines

    @staticmethod
    def structure(
        lines: str,
        level: int,
        payload: list[Any] | Any,
        flag: str = Default.EMPTY,
        recordkey: Any = Default.EMPTY,
    ) -> str:
        """Join a structure or a list of structure to GEDCOM lines.

        This method hides the concatenation of the already constructed
        GEDCOM file with the new line.  It also hides checking
        whether the string is part of a list or not.

        Examples:
            Suppose there is one structure to write to GEDCOM lines.
            >>> from genedata.classes7 import Lati, Long, Map
            >>> from genedata.util import Tagger
            >>> map1 = Map([Lati('N30.000000'), Long('W30.000000')])
            >>> map2 = Map([Lati('S40.000000'), Long('E20.000000')])
            >>> lines = ''
            >>> lines = Tagger.structure(lines, 2, map1)
            >>> print(lines)
            2 MAP
            3 LATI N30.000000
            3 LONG W30.000000
            <BLANKLINE>

            Now include both defined maps into a list.
            >>> lines = ''
            >>> lines = Tagger.structure(lines, 4, [map1, map2])
            >>> print(lines)
            4 MAP
            5 LATI N30.000000
            5 LONG W30.000000
            4 MAP
            5 LATI S40.000000
            5 LONG E20.000000
            <BLANKLINE>

        Args:
            lines: The prefix string that will be appended to.
            level: The GEDCOM level of the structure.
            payload: The structure or list of structures from which the lines will be formed.
            flag: An optional item passed to the structure's ged method to modify its behavior.
        """

        if payload is None or payload == Default.EMPTY:
            return lines
        if isinstance(payload, list):
            # unique_payload = OrderedSet(payload)
            for item in payload:  # unique_payload:
                # for item in payload:
                if flag != Default.EMPTY:
                    lines = ''.join(
                        [lines, item.ged(level, flag, recordkey=recordkey)]
                    )
                else:
                    lines = ''.join(
                        [lines, item.ged(level, recordkey=recordkey)]
                    )
            return lines
        # if payload != default:
        if flag != Default.EMPTY:
            lines = ''.join(
                [lines, payload.ged(level, flag, recordkey=recordkey)]
            )
        else:
            lines = ''.join([lines, payload.ged(level, recordkey=recordkey)])
        return lines

    @staticmethod
    def order(substructure: list[Any] | None) -> list[Any]:
        """Order structures by collecting similar ones together, but in the same order as presented."""
        if substructure is None:
            return []
        ordered: list[Any] = []
        subs_types: list[str] = [type(sub).__name__ for sub in substructure]
        unique_types: list[str] = OrderedSet(subs_types)
        for index in range(len(unique_types)):
            for sub in substructure:
                if unique_types[index] == type(sub).__name__:
                    ordered.append(sub)
        return ordered


class Formatter:
    """Methods to support formatting strings to meet the GEDCOM standard."""

    @staticmethod
    def codes_single(item: Any, tabs: int, full: bool) -> str:
        if isinstance(item, str):
            return f'{item!r}'
        if isinstance(item, int | float):
            return f'{item!r}'
        # if isinstance(item, Xref):
        #     return f'{item!r}'
        code_lines: str = (
            item.code(tabs - 1, full=full)
            .replace(Default.EOL, Default.EMPTY, 1)
            .replace(Default.INDENT, Default.EMPTY, 1)
        )
        return code_lines

    @staticmethod
    def codes(
        items: Any, tabs: int = 1, full: bool = False, required: bool = False
    ) -> str:
        if items is None:
            return Default.NONE
        if isinstance(items, list):
            if len(items) == 0:
                return Default.BRACKET_LEFT_RIGHT
            if len(items) == 1:
                return Formatter.codes_single(items[0], tabs, full)
            lines: str = Default.BRACKET_LEFT
            for item in items:
                line_end = Default.COMMA
                if required:
                    line_end = Default.COMMA_REQUIRED
                if isinstance(item, int | float):
                    lines = ''.join(
                        [
                            lines,
                            Default.EOL,
                            Default.INDENT * (tabs),
                            str(item),
                            line_end,
                        ]
                    )
                elif isinstance(item, str):
                    quote_mark: str = Default.QUOTE_SINGLE
                    if quote_mark in str(item):
                        quote_mark = Default.QUOTE_DOUBLE
                    lines = ''.join(
                        [
                            lines,
                            Default.EOL,
                            Default.INDENT * (tabs),
                            quote_mark,
                            str(item),
                            quote_mark,
                            line_end,
                        ]
                    )
                else:
                    lines = ''.join(
                        [lines, item.code(tabs, full=full), Default.COMMA]
                    )
            return ''.join(
                [
                    lines,
                    Default.EOL,
                    Default.INDENT * (tabs - 1),
                    Default.BRACKET_RIGHT,
                ]
            )
        return Formatter.codes_single(items, tabs, full)

    @staticmethod
    def codes_line(initial: str, items: Any, tabs: int, full: bool) -> str:
        line_end: str = Default.COMMA
        result: str = Formatter.codes(items, tabs, full)
        keep: bool = full or result not in ['None']
        if keep:
            return ''.join([initial, result, line_end])
        return Default.EMPTY

    @staticmethod
    def display_code(
        name: str, *code_lines: tuple[str, Any, int, bool, bool]
    ) -> str:
        if len(code_lines) > 0:
            lines: str = ''.join([Default.EOL, name, '('])
            for line in code_lines:
                returned_line = Formatter.codes_line(
                    line[0], line[1], line[2], line[3]
                )
                if returned_line != Default.EMPTY:
                    lines = ''.join([lines, Default.EOL, returned_line])
            return ''.join([lines, Default.EOL, ')'])
        return ''.join([Default.EOL, name])
