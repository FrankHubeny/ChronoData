# methods.py

__all__ = [
    'Input',
    'Names',
    'Query',
    'Tagger',
    'Util',
]

import logging
import math
import re
import urllib.request
import zipfile
from pathlib import Path

# from textwrap import indent
from typing import Any

import requests  # type: ignore[import-untyped]
import yaml  # type: ignore[import-untyped]

# from ordered_set import OrderedSet  # type: ignore[import-not-found]
from genedata.constants import Default
from genedata.messages import Msg
from genedata.specifications70 import Specs


class Util:
    """Utilities to read and write yaml or ged files."""

    @staticmethod
    def www_status(url: str) -> str:
        request: str
        try:
            request = requests.head(url)
        except requests.exceptions.RequestException:
            return '<Response [0]>'
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

    @staticmethod
    def read_binary(url: str) -> str:
        """Read a yaml file and convert it into a dictionary.

        Args:
            url: The name of the file or the internet url.
        """
        with open(url, 'rb') as file:  # noqa: PTH123
            binary_raw = file.read()
        return binary_raw.decode('utf-8')

    @staticmethod
    def read(url: str) -> str:
        """Read a yaml file and convert it into a dictionary.

        Args:
            url: The name of the file or the internet url.
        """

        raw: str = Default.EMPTY
        if url[0:4] == 'http':
            webUrl = urllib.request.urlopen(url)
            raw = webUrl.read().decode(Default.UTF8)
        elif Path(url).exists():
            with Path.open(Path(url)) as file:
                raw = file.read()
        else:
            logging.info(Msg.FILE_NOT_FOUND.format(url))
        return raw

    @staticmethod
    def read_ged(url: str) -> str:
        """Read a ged file removing extraneous material from the top and bottom.

        Args:
            url: The name of the file or the internet url.
        """
        raw: str = Default.EMPTY
        # Retrieve the file.
        try:
            raw = Util.read(url)
        except Exception:
            raw = Util.read_binary(url)

        # Check that file has proper ged header and trailer and a recognized version.
        if raw != Default.EMPTY:
            if Default.GED_HEADER not in raw:
                raise ValueError(
                    Msg.GED_NO_HEADER.format(url, Default.GED_HEADER)
                )
            if Default.GED_TRAILER not in raw:
                raise ValueError(
                    Msg.GED_NO_TRAILER.format(url, Default.GED_TRAILER)
                )
            version: str = Query.version(raw)
            if version not in Default.GED_VERSIONS:
                raise ValueError(
                    Msg.GED_VERSION_NOT_RECOGNIZED.format(url, version)
                )

        # Remove anything in the file prior to the ged header.
        _, _, raw_top_trimmed = raw.partition(Default.GED_HEADER)
        raw = ''.join([Default.GED_HEADER, raw_top_trimmed])

        # Remove anything in the file after the ged trailer.
        raw_bottom_trimmed, _, _ = raw.partition(Default.GED_TRAILER)
        return ''.join([raw_bottom_trimmed, Default.GED_TRAILER])

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

        raw: str = Default.EMPTY
        # Retrieve the file.
        try:
            raw = Util.read(url)
        except Exception:
            raw = Util.read_binary(url)

        # Check that file has proper yaml directive.
        if raw != Default.EMPTY and Default.YAML_DIRECTIVE not in raw:
            raise ValueError(
                Msg.YAML_NOT_YAML_FILE.format(url, Default.YAML_DIRECTIVE)
            )

        # Remove anything in the file prior to the yaml directive.
        _, _, raw_top_trimmed = raw.partition(Default.YAML_DIRECTIVE)
        raw = ''.join([Default.YAML_DIRECTIVE, raw_top_trimmed])

        # Remove anything in the file after the yaml end marker.
        raw_bottom_trimmed, _, _ = raw.partition(
            Default.YAML_DOCUMENT_END_MARKER
        )
        raw = ''.join([raw_bottom_trimmed, Default.YAML_DOCUMENT_END_MARKER])

        # Return the dictionary.
        yaml_data = raw  # .replace('\n  - |\n', '\n  - bar\n')
        yaml_dict: dict[str, Any] = yaml.safe_load(yaml_data)

        # Check that a lang field exists and is not empty.
        if (
            Default.YAML_LANG not in yaml_dict
            or yaml_dict[Default.YAML_LANG] == Default.EMPTY
            or yaml_dict[Default.YAML_LANG] is None
        ):
            raise ValueError(Msg.YAML_MISSING_REQUIRED_LANG.format(url))

        # Check that a uri field exists and is not empty.
        if (
            Default.YAML_URI not in yaml_dict
            or yaml_dict[Default.YAML_URI] == Default.EMPTY
            or yaml_dict[Default.YAML_URI] is None
        ):
            raise ValueError(Msg.YAML_MISSING_REQUIRED_URI.format(url))

        # Check that a type field exists and is not empty.
        if (
            Default.YAML_TYPE not in yaml_dict
            or yaml_dict[Default.YAML_TYPE] == Default.EMPTY
            or yaml_dict[Default.YAML_TYPE] is None
        ):
            raise ValueError(Msg.YAML_MISSING_REQUIRED_TYPE.format(url))

        # Check that `calendar``, `enumeration``, `month`` and `structure`` types
        # have either a `standard tag`` or an `extension tags`` fields.
        if yaml_dict[Default.YAML_TYPE] in Default.YAML_TAG_TYPES and (
            Default.YAML_STANDARD_TAG not in yaml_dict
            and Default.YAML_EXTENSION_TAGS not in yaml_dict
        ):
            raise ValueError(Msg.YAML_NO_TAG_NAME)

        # Check for valid type.
        if yaml_dict[Default.YAML_TYPE] not in Default.YAML_TYPE_CODES:
            raise ValueError(
                Msg.YAML_UNRECOGNIZED_TYPE.format(
                    yaml_dict[Default.YAML_TYPE], Default.YAML_TYPE_CODES
                )
            )
        return yaml_dict

    #     @staticmethod
    #     def ged_summary(ged: str) -> str:
    #         """Summarize the contents of a ged file.

    #         Args:
    #             ged: The string obtained from reading or producing a ged file.
    #         """

    #         # Count the number of record types.
    #         fam_count: int = len(re.findall('\n0.+FAM', ged))
    #         indi_count: int = len(re.findall('\n0.+INDI', ged))
    #         obje_count: int = len(re.findall('\n0.+OBJE', ged))
    #         repo_count: int = len(re.findall('\n0.+REPO', ged))
    #         snote_count: int = len(re.findall('\n0.+SNOTE', ged))
    #         sour_count: int = len(re.findall('\n0.+SOUR', ged))
    #         subm_count: int = len(re.findall('\n0.+SUBM', ged))

    #         # Return the number of record types.
    #         return f"""
    # Families      {fam_count!s}
    # Individuals   {indi_count!s}
    # Multimedia    {obje_count!s}
    # Repositories  {repo_count!s}
    # Shared Notes  {snote_count!s}
    # Sources       {sour_count!s}
    # Submitters    {subm_count!s}
    # """

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
                        "'",
                        Msg.DOES_NOT_EQUAL,
                        "'",
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
                    Msg.LONGER_FIRST,
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
                    Msg.LONGER_SECOND,
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
            >>> from genedata.methods import Input
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
        - [GEDCOM Date Type](https://gedcom.io/terms/v7/type-Date)
        """
        calendar_key: str = ''.join(
            [Default.URL_CALENDAR_PREFIX, calendar.upper()]
        )
        calendar_tag: str = Specs[Default.YAML_TYPE_CALENDAR][calendar_key][
            Default.YAML_STANDARD_TAG
        ]
        show_calendar: str = Default.EMPTY
        if show:
            show_calendar = calendar_tag
        epoch_list: list[str] = Specs[Default.YAML_TYPE_CALENDAR][calendar_key][
            Default.YAML_EPOCHS
        ]
        epoch: str = Default.EMPTY
        if year < 0 and len(epoch_list) > 0:
            epoch = epoch_list[0]
            year = abs(year)
        if calendar_tag in ['GREGORIAN', 'JULIAN'] and year == 0:
            raise ValueError(Msg.ZERO_YEAR.format(calendar))
        month_tag: str = Default.EMPTY
        if month > 0:
            month_uri: str = Specs[Default.YAML_TYPE_CALENDAR][calendar_key][
                Default.YAML_MONTHS
            ][month - 1]
            month_tag = Specs[Default.YAML_TYPE_MONTH][Names.stem(month_uri)][
                Default.YAML_STANDARD_TAG
            ]
        day_tag: str = Default.EMPTY
        if day > 0:
            day_tag = str(day)
        return (
            f'{show_calendar} {day_tag} {month_tag} {year!s} {epoch}'.replace(
                Default.SPACE_DOUBLE, Default.SPACE
            )
            .replace(Default.SPACE_DOUBLE, Default.SPACE)
            .replace(Default.SPACE_DOUBLE, Default.SPACE)
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
            >>> from genedata.methods import Input
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
            >>> from genedata.methods import Input
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
            >>> from genedata.methods import Input
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
            >>> from genedata.methods import Input
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
            >>> from genedata.methods import Input
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
            >>> from genedata.methods import Input
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
            >>> from genedata.methods import Input
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
            >>> from genedata.methods import Input
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

    # @staticmethod
    # def from_ged(lines: str | list[list[str]]) -> str:
    #     if isinstance(lines, str):
    #         strlist: list[list[str]] = [
    #             a.split(' ') for a in lines.split('\n') if a != ''
    #         ]
    #         return Input.from_ged(strlist)
    #     level: int = int(lines[0][0])
    #     tag: str = lines[0][1]
    #     payload: str = Default.EMPTY
    #     output: str = Default.EMPTY
    #     number_of_lines: int = len(lines)
    #     if len(lines[0]) == 3:
    #         payload = lines[0][2]
    #     output = f'{tag}({payload}'
    #     intermediate_lines: list[list[str]] = []
    #     number_of_lines = len(lines[1:])
    #     for i in range(number_of_lines):
    #         if int(lines[i][0]) == level and len(intermediate_lines) > 0:
    #             output = ''.join(
    #                 [output, '[', Input.from_ged(intermediate_lines), '])']
    #             )
    #             intermediate_lines = []
    #         elif int(lines[i][0]) == level:
    #             output = ''.join([output, ')'])
    #             if i < number_of_lines:
    #                 return ''.join(
    #                     [',', output, Input.from_ged(lines[i:]), ')']
    #                 )
    #             return output
    #         else:
    #             intermediate_lines.append(lines[i])
    #     return output

    @staticmethod
    def lati(
        degrees: int, minutes: int, seconds: float, precision: int = 6
    ) -> str:
        """Construct a latitude given degrees, minutes and seconds.

        Example:
            In this example not how a string is returned preceded with 'N' for North
            because the degrees integer is positive.
            >>> from genedata.methods import Input
            >>> Input.lati(10, 5, 1)
            'N10.083611'

            If one goes outside the range a ValueError is thrown.
            >>> Input.lati(91, 0, 0)
            Traceback (most recent call last):
            ValueError: The value "91.0" is not between -90.0 and 90.0 in method Input.lati.

        Args:
            degrees: An integer value of degrees, positive or negative,
                between -90 and 90.
            minutes: An integer value of minutes, positive only,
                between 0 and 59.
            seconds: A float value of seconds, positive only,
                between 0 and 60.
            precision: The precision desired for the latitude with default 6.
        """
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
        """Construct a longitude given degrees, minutes and seconds.

        Example:
            In this example not how a string is returned preceded with 'E' for East
            because the degrees integer is positive.
            >>> from genedata.methods import Input
            >>> Input.long(10, 5, 1)
            'E10.083611'

            If one goes outside the range a ValueError is thrown.
            >>> Input.long(181, 0, 0)
            Traceback (most recent call last):
            ValueError: The value "181.0" is not between -180.0 and 180.0 in method Input.long.

        Args:
            degrees: An integer value of degrees, positive or negative,
                between -180 and 180.
            minutes: An integer value of minutes, positive only,
                between 0 and 59.
            seconds: A float value of seconds, positive only,
                between 0 and 60.
            precision: The precision desired for the latitude with default 6.
        """
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
            >>> from genedata.methods import Input
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
            >>> import genedata.classes70 as gc
            >>> m = gc.IndiName(Input.name('Jim Smith', 'Smith'))
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
            >>> from genedata.methods import Input
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
            >>> from genedata.methods import Input
            >>> Input.place('Chicago', 'Illinois', 'Cook', 'USA')
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

        >>> from genedata.methods import Input
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
            >>> from genedata.methods import Input
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
            >>> from genedata.methods import Input
            >>> import genedata.classes70 as gc
            >>> response = gc.Www(Input.www('abc'))
            >>> print(response.ged(1))
            1 WWW abc
            <BLANKLINE>

        Reference:
        - [GEDCOM WWW Structure](https://gedcom.io/terms/v7/WWW)

        """
        response: str = str(Util.www_status(url))
        if response != '<Response [200]>':
            logging.warning(Msg.WWW_RESPONSE.format(url, response))
        return url


class Names:
    """Format various names derived from file names.

    These methods extract information from the name of the yaml file
    containing the specification.  Future versions of the specification
    may require that these names be derived in other ways.
    """

    @staticmethod
    def key_from_classname(
        classname: str, specs: dict[str, dict[str, Any]]
    ) -> str:
        """Return the key from a class name.

        Example:
            Suppose the class name is `RecordIndi`.
            >>> from genedata.methods import Names
            >>> from genedata.specifications70 import Specs
            >>> Names.key_from_classname('RecordIndi', Specs)
            'record-INDI'

            Suppose the class name is `HeadPlacForm`.
            >>> Names.key_from_classname('HeadPlacForm', Specs)
            'HEAD-PLAC-FORM'

            Suppose `classname` is not an actual class name.
            >>> Names.key_from_classname('123456', Specs)
            ''

        Args:
            classname: The name of a class from classes.
            specs: The specification dictionary to search through.
        """
        hyphenated: str = classname[0]
        for letter in classname[1:]:
            if letter.isupper():
                hyphenated = ''.join([hyphenated, Default.HYPHEN, letter])
            else:
                hyphenated = ''.join([hyphenated, letter])

        hyphenated = (
            hyphenated.upper()
            .replace('RECORD-', 'record-')
            .replace('ORD-', 'ord-')
            .replace('-EXACT', '-exact')
        )
        if hyphenated not in specs[Default.YAML_TYPE_STRUCTURE]:
            return Default.EMPTY
        return hyphenated

    @staticmethod
    def keyname(value: str) -> str:
        """Return the name used by the dictionary keys in the specs module.

        The value is expected to be the name of a yaml file where the
        specification of the concept is defined.  This file name contains
        the information needed to produce the key name.

        Example:
            Suppose the file name is 'dir/to/yaml/file/enum-ABCD'. Then
            we want to retrieve 'enum-ABCD' since that will be used as the
            key to this specification in the Enumerations dictionary
            of the specs module.
            >>> from genedata.methods import Names
            >>> Names.keyname('dir/to/yaml/file/enum-ABCD')
            'enum-ABCD'

            If no '/' character is in the name, return the name.
            >>> Names.keyname('abcdef')
            'abcdef'

            If the value is empty return the empty string.
            >>> Names.keyname('')
            ''

        Args:
            value: The name of the yaml file.
        """
        if value == Default.EMPTY or str(value)[-1] == Default.SLASH:
            return Default.EMPTY
        value_str: str = str(value)
        if Default.SLASH in value_str:
            return value_str[value_str.rfind(Default.SLASH) + 1 :].replace(
                Default.QUOTE_DOUBLE, Default.EMPTY
            )
        return value_str.replace(Default.QUOTE_DOUBLE, Default.EMPTY)

    @staticmethod
    def stem(file_name: str) -> str:
        p = Path(file_name)
        return p.stem

    @staticmethod
    def classname(value: str) -> str:
        """Construct the class name from the keyname.

        The class name will have title capitalization of the capital letters.
        Other characters will be removed.

        Examples:
            Suppose the yaml file is '/dir/to/yaml/file/enum-XYZ' Then
            the class name would be 'Xyz'.
            >>> from genedata.methods import Names
            >>> Names.classname('/dir/to/yaml/file/enum-XYZ')
            'Xyz'

        Args:
            value: The name of the yaml file containing the specification.
        """
        base: str = re.sub(
            '[a-z]',
            Default.EMPTY,
            Names.keyname(value)
            .replace('record', 'RECORD')
            .replace('exact', 'EXACT')
            .replace('ord', 'ORD'),
        )
        return (
            base.title()
            .replace(Default.HYPHEN, Default.EMPTY)
            .replace(Default.UNDERLINE, Default.EMPTY)
        )

    @staticmethod
    def slash(url: str) -> str:
        """Add a '/' at the end of a string if one is not there already.

        This makes sure that a directory string ends with a /.

        Example:
            Let `abcdefghi` be the name of the directory.
            >>> from genedata.methods import Names
            >>> print(Names.slash('abcdefghi'))
            abcdefghi/

        """
        if url == Default.EMPTY:
            return url
        if url[-1] == Default.SLASH:
            return url
        return f'{url}{Default.SLASH}'

    @staticmethod
    def tagname(value: str) -> str:
        """Return the standard tag as derived from the yaml file name.

        This is the keyname with lower characters removed starting
        with the last hyphen in the name.  The standard tag is also
        provided in the specification under the key 'standard tag'.

        Example:
            Suppose the yaml file is '/path/to/yaml/file/record-INDI'.
            Then the tag would be 'INDI'.
            >>> from genedata.methods import Names
            >>> Names.tagname('/path/to/yaml/file/record-INDI')
            'INDI'

        Args:
            value: The name of the yaml file containing the specification.
        """
        # base: str = re.sub('[a-z]', Default.EMPTY, Names.keyname(value))
        # if Default.HYPHEN in base:
        #     return base[base.rfind(Default.HYPHEN) + 1 :]
        # return base
        tag: str = str(
            Specs[Default.YAML_TYPE_STRUCTURE][Names.keyname(value)][
                Default.YAML_STANDARD_TAG
            ]
        )
        return tag

    @staticmethod
    def key_tag_to_subkey_class(
        key: str,
        tag: str,
        specs: dict[str, dict[str, Any]],
    ) -> tuple[str, str]:
        """Find the key and class name given the superstructure's key and the class's tag.

        Although the tag is similar to the classname, one tag could reference multiple
        classes.  For example, the tag `INDI` could reference the `Indi` class or
        the `RecordIndi` class.  The the superstructure's key however removes the
        ambiguity.

        There are many structures depending on the version of GEDCOM and the
        availability of extension structures.  To avoid this ambiguity, the structure
        specification needs to be provided as well as the superstructure's key.

        Example:
            The first example is the pattern we would expect to see.
            >>> from genedata.methods import Names
            >>> from genedata.specifications70 import Specs
            >>> Names.key_tag_to_subkey_class('record-INDI', 'NOTE', Specs)
            ('NOTE', 'Note')

            The second example shows that we need to check the specifications
            for the correct subordinate key name and class name derived from it.
            >>> Names.key_tag_to_subkey_class('ADOP-FAMC', 'ADOP', Specs)
            ('FAMC-ADOP', 'FamcAdop')

            If the substructure key and class name cannot be found empty strings
            for both of them are returned.
            >>> Names.key_tag_to_subkey_class('record-INDI', 'MAP', Specs)
            ('', '')

        Args:
            key: The key of the tag's superstructure.
            tag: The tag of the structure's key we are looking for.
            specs: The specification dictionary to search through.
        """
        if key in specs[Default.YAML_TYPE_STRUCTURE]:
            for uri in specs[Default.YAML_TYPE_STRUCTURE][key][
                Default.YAML_SUBSTRUCTURES
            ]:
                sub_key = Names.keyname(uri)
                if (
                    specs[Default.YAML_TYPE_STRUCTURE][sub_key][
                        Default.YAML_STANDARD_TAG
                    ]
                    == tag
                ):
                    return sub_key, Names.classname(sub_key)
        return Default.EMPTY, Default.EMPTY

    @staticmethod
    def quote_text(value: str) -> str:
        """Put quote marks around a string checking for multiline strings
        and single quotes in the string.

        Example:
            Suppose the value to quote is `happy birthday`. This is a single line string
            with no single quote mark in the string.  This should return "'happy birthday'"
            >>> from genedata.methods import Names
            >>> Names.quote_text('happy birthday')
            "'happy birthday'"

            If we put this on two lines `happy\nbirthday` we would get "'''happy\nbirthday'''".
            >> Names.quote_text('happy\nbirthday')
            "'''happy\nbirthday'''"

            If there is a single quote in the string, `Tom's birthday` we would get "Tom's birthday".
            >>> Names.quote_text("Tom's birthday")
            '"Tom\\'s birthday"'

        Args:
            value: The text to be quoted.
        """
        if Default.EOL in value:
            if Default.QUOTE_SINGLE in value:
                return f'"""{value}"""'
            return f"'''{value}'''"
        if Default.QUOTE_SINGLE in value:
            return f'"{value}"'
        return f"'{value}'"
    
    def extension_name(tag: str, url: str) -> str:
        """Construct a variable name for an extension."""
        return ''.join(
            [
                tag.lower(),
                Default.UNDERLINE,
                Names.stem(url),
            ]
        )
    
    def top_class(tag: str) -> str:
        """For a top level tag return the class name or empty."""
        match tag:
            case Default.TAG_EXT:
                return Default.CLASS_EXT
            case Default.TAG_FAM:
                return Default.CLASS_FAM
            case Default.TAG_INDI:
                return Default.CLASS_INDI
            case Default.TAG_OBJE:
                return Default.CLASS_OBJE
            case Default.TAG_REPO:
                return Default.CLASS_REPO
            case Default.TAG_SNOTE:
                return Default.CLASS_SNOTE
            case Default.TAG_SOUR:
                return Default.CLASS_SOUR
            case Default.TAG_SUBM:
                return Default.CLASS_SUBM
            case _:
                return Default.EMPTY
    
    def xref_name(tag: str, xref: str) -> str:
        """Construct a variable name for a cross reference identifier."""
        return ''.join(
            [
                tag.lower(),
                Default.UNDERLINE,
                xref.replace(Default.ATSIGN, Default.EMPTY),
                Default.UNDERLINE,
                'xref',
            ]
        )
    
    def record_name(tag: str, xref: str) -> str:
        """Construct a variable name for a cross reference identifier."""
        return ''.join(
            [
                tag.lower(),
                Default.UNDERLINE,
                xref.replace(Default.ATSIGN, Default.EMPTY),
            ]
        )


class Query:
    """Some potentially useful queries of the specification."""

    @staticmethod
    def enum_key_tags(key: str, specs: dict[str, dict[str, Any]]) -> tuple[str, list[str]]:
        structure: dict[str, Any] = specs[Default.YAML_TYPE_STRUCTURE]
        enumeration_set: dict[str, dict[str, Any]] = specs[
            Default.YAML_TYPE_ENUMERATION_SET
        ]
        enumeration: dict[str, dict[str, Any]] = specs[
            Default.YAML_TYPE_ENUMERATION
        ]
        enum_tags: list[str] = []
        enum_set_key: str = Default.EMPTY
        enum_key: str = Default.EMPTY
        if key in structure and Default.YAML_ENUMERATION_SET in structure[key]:
            enum_set_key = Names.stem(
                structure[key][Default.YAML_ENUMERATION_SET]
            )
            for enum in enumeration_set[enum_set_key][
                Default.YAML_ENUMERATION_VALUES
            ]:
                enum_key = Names.stem(enum)
                if enum_key in enumeration:
                    enum_tags.append(
                        enumeration[enum_key][Default.YAML_STANDARD_TAG]
                    )
                else:
                    enum_tags.append(
                        structure[enum_key][Default.YAML_STANDARD_TAG]
                    )
        return enum_key, enum_tags

    @staticmethod
    def classes_with_tag(
        tag: str, specs: dict[str, dict[str, Any]]
    ) -> list[str]:
        """Provide a list of classes that would display the given tag.

        Example:
            Suppose we want to know what classes would produce the 'FAMC' tag.
            Here is how to use this method to find that information from
            the GEDCOM version 7 specifications.
            >>> from genedata.methods import Query
            >>> from genedata.specifications70 import Specs
            >>> Query.classes_with_tag('FAMC', Specs)
            ['AdopFamc', 'Famc', 'IndiFamc']

        Args:
            tag: The tag that one sees in a ged file.
            specs: The specification dictionary to search over.
        """
        classes: list[str] = []
        tagname: str = tag.upper()
        for key, structure in specs[Default.YAML_TYPE_STRUCTURE].items():
            if structure[Default.YAML_STANDARD_TAG] == tagname:
                classes.append(Names.classname(key))
        return classes

    @staticmethod
    def payload(key: str, specs: dict[str, dict[str, Any]]) -> str:
        result: str = Default.EMPTY
        if (
            key in specs[Default.YAML_TYPE_STRUCTURE]
            and Default.YAML_PAYLOAD in specs[Default.YAML_TYPE_STRUCTURE][key]
            and specs[Default.YAML_TYPE_STRUCTURE][key][Default.YAML_PAYLOAD] is not None
        ):
            result = specs[Default.YAML_TYPE_STRUCTURE][key][
                Default.YAML_PAYLOAD
            ]
        return result

    @staticmethod
    def permitted(key: str, specs: dict[str, dict[str, Any]]) -> list[str]:
        """Provide a list of permitted classes.

        Example:
            We can find the classes that are permitted under the `HEAD` key
            in the GEDCOM version 7 specifications by doing the following:
            >>> from genedata.methods import Query
            >>> from genedata.specifications70 import Specs
            >>> Query.permitted('HEAD', Specs)
            ['Copr', 'Dest', 'Gedc', 'HeadDate', 'HeadLang', 'HeadPlac', 'HeadSour', 'Note', 'Schma', 'Snote', 'Subm']

        Args:
            key: The top level name in the dictionary.
            specs: The specification dictionary one wants to search.
        """
        classes: list[str] = []
        if key in specs[Default.YAML_TYPE_STRUCTURE]:
            for uri, _cardinality in specs[Default.YAML_TYPE_STRUCTURE][key][
                Default.YAML_SUBSTRUCTURES
            ].items():
                classes.append(Names.classname(uri))
        return classes

    @staticmethod
    def permitted_keys(key: str, specs: dict[str, dict[str, Any]]) -> list[str]:
        """Provide a list of keys to the `Structure` subdictionary that represented permitted classes.

        Example:
            We can find the classes that are permitted under the `HEAD` key
            in the GEDCOM version 7 specifications by doing the following:
            >>> from genedata.methods import Query
            >>> from genedata.specifications70 import Specs
            >>> Query.permitted_keys('HEAD', Specs)
            ['COPR', 'DEST', 'GEDC', 'HEAD-DATE', 'HEAD-LANG', 'HEAD-PLAC', 'HEAD-SOUR', 'NOTE', 'SCHMA', 'SNOTE', 'SUBM']

        Args:
            key: The top level name in the dictionary.
            specs: The specification dictionary one wants to search.
        """
        keys: list[str] = []
        if key in specs[Default.YAML_TYPE_STRUCTURE]:
            for uri, _cardinality in specs[Default.YAML_TYPE_STRUCTURE][key][
                Default.YAML_SUBSTRUCTURES
            ].items():
                keys.append(Names.keyname(uri))
        return keys

    @staticmethod
    def required(key: str, specs: dict[str, dict[str, Any]]) -> list[str]:
        """Provide a list of required classes.

        Example:
            We can find the classes that are required under the `HEAD` key
            in the GEDCOM version 7 specifications by doing the following:
            >>> from genedata.methods import Query
            >>> from genedata.specifications70 import Specs
            >>> Query.required('HEAD', Specs)
            ['Gedc']

        Args:
            key: The top level name in the dictionary.
            specs: The specification dictionary one wants to search.
        """
        classes: list[str] = []
        if key in specs[Default.YAML_TYPE_STRUCTURE]:
            for uri, cardinality in specs[Default.YAML_TYPE_STRUCTURE][key][
                Default.YAML_SUBSTRUCTURES
            ].items():
                if Default.CARDINALITY_REQUIRED in cardinality:
                    classes.append(Names.classname(uri))
        return classes

    @staticmethod
    def singular(key: str, specs: dict[str, dict[str, Any]]) -> list[str]:
        """Provide a list of classes that can be used only once as substructures.

        Example:
            We can find the classes that can only be used once as substructures
            in the GEDCOM version 7 specifications under the `HEAD` key by doing the following:
            >>> from genedata.methods import Query
            >>> from genedata.specifications70 import Specs
            >>> Query.singular('HEAD', Specs)
            ['Copr', 'Dest', 'Gedc', 'HeadDate', 'HeadLang', 'HeadPlac', 'HeadSour', 'Note', 'Schma', 'Snote', 'Subm']

        Args:
            key: The top level name in the dictionary.
            specs: The specification dictionary one wants to search.
        """
        classes: list[str] = []
        if key in specs[Default.YAML_TYPE_STRUCTURE]:
            for uri, cardinality in specs[Default.YAML_TYPE_STRUCTURE][key][
                Default.YAML_SUBSTRUCTURES
            ].items():
                if Default.CARDINALITY_SINGULAR in cardinality:
                    classes.append(Names.classname(uri))
        return classes
    
    @staticmethod
    def structure_tag(key: str, specs: dict[str, dict[str, Any]]) -> str:
        tag: str = Default.EMPTY
        if key in specs[Default.YAML_TYPE_STRUCTURE]:
            return specs[Default.YAML_TYPE_STRUCTURE][key][Default.YAML_STANDARD_TAG]
        if key in specs[Default.YAML_TYPE_ENUMERATION]:
            return specs[Default.YAML_TYPE_ENUMERATION][key][Default.YAML_STANDARD_TAG]
        if key in specs[Default.YAML_TYPE_CALENDAR]:
            return specs[Default.YAML_TYPE_CALENDAR][key][Default.YAML_STANDARD_TAG]
        if key in specs[Default.YAML_TYPE_MONTH]:
            return specs[Default.YAML_TYPE_MONTH][key][Default.YAML_STANDARD_TAG]
        return tag

    @staticmethod
    def supers_count(key: str, specs: dict[str, dict[str, Any]]) -> int:
        howmany: int = 0
        if key in specs[Default.YAML_TYPE_STRUCTURE] and (
            key in specs[Default.YAML_TYPE_STRUCTURE]
            and Default.YAML_SUPERSTRUCTURES
            in specs[Default.YAML_TYPE_STRUCTURE][key]
        ):
            howmany = len(
                specs[Default.YAML_TYPE_STRUCTURE][key][
                    Default.YAML_SUPERSTRUCTURES
                ]
            )
        return howmany

    @staticmethod
    def record_counts(
        ged: str,
        specification: dict[str, dict[str, Any]] | None = None,
        column: str = Default.COLUMN_COUNT,
    ) -> dict[str, dict[str, int]]:
        """Return a dictionary of record names and counts from a gedcom string.

        Example:
            Suppose we have this gedcom string: '0 HEAD\\n1 GEDC\\n2 VERS 7.0\\n0 TRLR'
            We would expect the record count to be zero for all records.  This string
            would produce the same report as the empty string.
            >>> file = '0 HEAD\\n1 GEDC\\n2 VERS 7.0\\n0 TRLR'
            >>> Query.record_counts(file)
            {'Count': {'FAM': 0, 'INDI': 0, 'OBJE': 0, 'REPO': 0, 'SNOTE': 0, 'SOUR': 0, 'SUBM': 0}}

            We could generate a better report by placing this in a pandas DataFrame.
            >>> import pandas as pd
            >>> pd.DataFrame(Query.record_counts(file))
                   Count
            FAM        0
            INDI       0
            OBJE       0
            REPO       0
            SNOTE      0
            SOUR       0
            SUBM       0

            Since a dictionary is returned one can do more than report on the results.
            Suppose we only want to know how many INDI records there are.
            We could use the `Count` key and then the `INDI` subkey to find the value `0`.
            >>> Query.record_counts(file)['Count']['INDI']
            0

        Args:
            ged: The gedcom string.
            specification: The specification dictionary needed to identify what the records are.
            count_column: The name of the `count` dictionary key which becomes the
                pandas count column name.
        """
        data: dict[str, dict[str, int]] = {}
        count: dict[str, int] = {}
        searchfor: str = Default.EMPTY
        howmany: int = 0
        if specification is None:
            for record in Default.RECORD_TYPES:
                searchfor = ''.join(
                    [
                        Default.EOL,
                        '0 @.*@ ',
                        record,
                    ]
                )
                howmany = len(re.findall(searchfor, ged))
                count.update({record: howmany})
        data.update({column: count})
        return data

    @staticmethod
    def version(ged: str) -> str:
        """Retrieve the version number from the ged file.

        Example:
            >>> from genedata.methods import Query
            >>> file = '0 HEAD\\nsomething else\\n1 GEDC\\n2 VERS 7.0\\nsomething more\\n0 TRLR'
            >>> Query.version(file)
            '7.0'

        Args:
            ged: The GEDCOM file.
        """
        _, _, version_part = ged.partition(Default.GED_VERSION_START)
        version_value, _, _ = version_part.partition(Default.GED_VERSION_END)
        return version_value

    @staticmethod
    def extensions(ged: str) -> list[list[str]]:
        """Return a list of extention specification tags and uris."""
        tag_uri_list: list[list[str]] = []
        length: int = len(Default.GED_EXT_TAG)
        if Default.GED_EXT_SCHMA in ged:
            _, _, tags = ged.partition(Default.GED_EXT_SCHMA)
            while tags[0:length] == Default.GED_EXT_TAG:
                tag_uri, _, tags = tags[length:].partition(Default.EOL)
                tag_uri_list.append(tag_uri.split(Default.SPACE))
        return tag_uri_list

    @staticmethod
    def top(specs: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
        structure: dict[str, Any] = specs[Default.YAML_TYPE_STRUCTURE]
        top_dict: dict[str, dict[str, Any]] = {}
        for key in structure:
            if (
                key not in Default.IGNORE
                and len(structure[key][Default.YAML_SUPERSTRUCTURES]) == 0
            ):
                top_dict.update(
                    {
                        key: {
                            Default.YAML_KEY: key,
                            Default.YAML_CLASS_NAME: Names.classname(key),
                            Default.YAML_SUBSTRUCTURES: Query.subs(key, specs),
                        }
                    }
                )
        return top_dict

    @staticmethod
    def subs(key: str, specs: dict[str, dict[str, Any]]) -> dict[str, Any]:
        structure: dict[str, dict[str, Any]] = specs[
            Default.YAML_TYPE_STRUCTURE
        ]
        subs_dict: dict[str, Any] = {}
        if len(structure[key][Default.YAML_SUBSTRUCTURES]) > 0:
            for substructure, cardinality in structure[key][
                Default.YAML_SUBSTRUCTURES
            ].items():
                subkey: str = Names.keyname(substructure)
                subclass: str = Names.classname(subkey)
                subtag: str = structure[subkey][Default.YAML_STANDARD_TAG]
                payload: str | None = structure[subkey][Default.YAML_PAYLOAD]
                payload = (
                    Default.NONE if payload is None else Names.keyname(payload)
                )
                subsingular: bool = False
                if Default.YAML_CARDINALITY_SINGULAR in cardinality:
                    subsingular = True
                subrequired: bool = False
                if Default.YAML_CARDINALITY_REQUIRED in cardinality:
                    subrequired = True
                subs_dict.update(
                    {
                        subkey: {
                            Default.YAML_STANDARD_TAG: subtag,
                            Default.YAML_SINGULAR: subsingular,
                            Default.YAML_REQUIRED: subrequired,
                            Default.YAML_CLASS_NAME: subclass,
                            Default.YAML_PAYLOAD: payload,
                            # Default.YAML_SUBSTRUCTURES: Query.subs(
                            #     subkey, specs
                            # ),
                        }
                    }
                )
        return subs_dict

    @staticmethod
    def make_dictionary(ged: str) -> dict[str, Any]:
        ged_dict: dict[str, Any] = {
            'HEAD': {},
            'FAM': {},
            'INDI': {},
            'OBJE': {},
            'REPO': {},
            'SNOTE': {},
            'SOUR': {},
            'SUBM': {},
        }
        ged_list: list[str] = ged.split(Default.EOL)
        for line in ged_list:
            line_list: list[str] = line.split(Default.SPACE, 2)
            if (
                line_list[0] == '0'
                and len(line_list) > 2
                and line_list[2][0:5] != 'SNOTE'
            ):
                ged_dict[line_list[2]].update({line_list[1]: {}})
            ged_dict.update({})
        return ged_dict


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
            >>> from genedata.constants import Default
            >>> from genedata.methods import Tagger
            >>> include_some_banned_characters: str = (
            ...     '\\u001F\\u007F\\uD800' + 'hello'
            ... )
            >>> Tagger.clean_input(include_some_banned_characters)
            'hello'

        Args:
            input: A string value from which banned characters will be removed.

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
            >>> from genedata.methods import Tagger
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
            >>> import genedata.classes70 as gc
            >>> mynote = gc.Note(
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
            >>> from genedata.methods import Tagger
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
            >>> from genedata.methods import Tagger
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
        # flag: str = Default.EMPTY,
        recordkey: Any = Default.EMPTY,
    ) -> str:
        """Join a structure or a list of structure to GEDCOM lines.

        This method hides the concatenation of the already constructed
        GEDCOM file with the new line.  It also hides checking
        whether the string is part of a list or not.

        Examples:
            Suppose there is one structure to write to GEDCOM lines.
            >>> import genedata.classes70 as gc
            >>> from genedata.methods import Tagger
            >>> map1 = gc.Map([gc.Lati('N30.000000'), gc.Long('W30.000000')])
            >>> map2 = gc.Map([gc.Lati('S40.000000'), gc.Long('E20.000000')])
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
            for item in payload:
                # if flag != Default.EMPTY:
                #     lines = ''.join(
                #         [lines, item.ged(level, flag, recordkey=recordkey)]
                #     )
                # else:
                lines = ''.join([lines, item.ged(level, recordkey=recordkey)])
            return lines
        # if flag != Default.EMPTY:
        #     lines = ''.join(
        #         [lines, payload.ged(level, flag, recordkey=recordkey)]
        #     )
        # else:
        return ''.join([lines, payload.ged(level, recordkey=recordkey)])

    # @staticmethod
    # def order(substructure: list[Any] | None) -> list[Any]:
    #     """Order structures by collecting similar ones together, but in the same order as presented."""
    #     if substructure is None:
    #         return []
    #     ordered: list[Any] = []
    #     subs_types: list[str] = [type(sub).__name__ for sub in substructure]
    #     unique_types: list[str] = OrderedSet(subs_types)
    #     for index in range(len(unique_types)):
    #         for sub in substructure:
    #             if unique_types[index] == type(sub).__name__:
    #                 ordered.append(sub)
    #     return ordered
