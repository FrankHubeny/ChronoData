# util.py

import re
import urllib.request
from typing import Any

import yaml  # type: ignore[import-untyped]

from genedata.constants import Default
from genedata.messages import Msg
from genedata.specs7 import Calendar, Month


class Util:
    """Utilities to read and write yaml or ged files."""
    @staticmethod
    def read(url: str) -> dict[str, Any]:
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
    def compare(first: str, second: str) -> str:
        if first == second:
            return f'{first}\nSuccessful Match'
        lines: str = Default.EMPTY
        split_first = first.split('\n')
        split_second = second.split('\n')
        for i in range(len(split_first)):
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
                        "'"
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
            >>> from genedata.util import Input
            >>> Input.age(1.1, 0, 2.2, 1)
            > 1y 2w 1d
            <BLANKLINE>

            Negative values will not display that unit.
            >>> Input.age(-2, -14.2, -1, 1)
            > 1d
            <BLANKLINE>

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
            FROM 1 JAN 2024 TO 1 JAN 2025

            This example displays the calendar name on the from date:
            >>> Input.date_period(
            ...     Input.date(2024, 1, 1), Input.date(2025, 1, 1, use_tag=True)
            ... )
            FROM GREGORIAN 1 JAN 2024 TO 1 JAN 2025

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
            BET 1 JAN 2024 AND 1 JAN 2025

            This example displays the calendar name on the from date:
            >>> Input.date_period(
            ...     Input.date(2024, 1, 1), Input.date(2025, 1, 1, show=True)
            ... )
            BET GREGORIAN 1 JAN 2024 AND 1 JAN 2025

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
            AFT 1 JAN 2024

            This example displays the calendar name on the date:
            >>> Input.date_after(Input.date(2025, 1, 1, show=True))
            AFT GREGORIAN 1 JAN 2024

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
            BEF 1 JAN 2024

            This example displays the calendar name on the date:
            >>> Input.date_before(Input.date(2025, 1, 1, show=True))
            BEF GREGORIAN 1 JAN 2025

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
            ABT 1 JAN 2024

            This example displays the calendar name on the date:
            >>> Input.date_before(Input.date(2025, 1, 1, show=True))
            AFT GREGORIAN 1 JAN 2025

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
            CAL 1 JAN 2024

            This example displays the calendar name on the date:
            >>> Input.date_calculated(Input.date(2025, 1, 1, show=True))
            CAL GREGORIAN 1 JAN 2025

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
            EST 1 JAN 2024

            This example displays the calendar name on the date:
            >>> Input.date_estimatedd(Input.date(2025, 1, 1, show=True))
            EST GREGORIAN 1 JAN 2025

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
    def name(full: str, surname: str) -> str:
        """Format a personal name to meet GEDCOM name type specifications.

        Example:
            >>> from genedata.structure import Input
            >>> Input.name('Jim Smith', 'Smith')
            Jim /Smith/

            If more than one space separates parts of the name they are removed along with
            spaces at the beginning or end of the name.
            >>> Input.name(' Jim      Smith ', '   Smith ')
            Jim /Smith/

            Line breaks are also removed from both name and surname.
            >>> Input.name(' Jim\n\n\nSmith\n', '\n\nSmith\n')
            Jim /Smith/

            This methods assists formatting a personal name using IndiName.
            >>> from genedata.util import IndiName
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
    def to_decimal(
        degrees: int, minutes: int, seconds: float, precision: int = 6
    ) -> float:
        """Convert degrees, minutes and seconds to a decimal.

        Example:
            The specification for the LATI and LONG structures (tags) offer the
            following example.
            >>> from genedata.structure import Placer
            >>> Placer.to_decimal(168, 9, 3.4, 6)
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

