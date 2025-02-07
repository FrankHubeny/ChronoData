# methods.py
"""Calendar methods for computation, comparison and visualization of multiple calendars."""

import numpy as np
import pandas as pd  # type: ignore[import-untyped]

from calendars.calendars import CalendarDefinition

# from calendars.french_revolution_calendars import CalendarsFrenchRevolution
# from calendars.gregorian_calendars import CalendarsGregorian
# from calendars.hebraic_calendars import CalendarsHebraic
# from calendars.julian_calendars import CalendarsJulian


class Methods:
    @staticmethod
    def date_item(iso: str, calendar: CalendarDefinition) -> list[str]:
        """Calculate the calendar date from an ISO 8601 date.
        
        Examples:
            The ISO 8601 date should be identical to the Gregorian calendar date.
            >> from calendars.gregorian_calendars import CalendarsGregorian
            >> from calendars.methods import Methods
            >> Methods.date_item('2025-01-01', CalendarsGregorian.GREGORIAN)
            ['Gregorian', '2025-01-01']
        
        """
        np_year: np.datetime64 = np.datetime64(iso, 'Y')
        years: np.timedelta64 = np_year - calendar.epoch_year
        np_month: np.datetime64 = np.datetime64(iso, 'M')
        months: np.timedelta64 = np_month - calendar.epoch_month
        np_day: np.datetime64 = np.datetime64(iso, 'Y')
        days: np.timedelta64 = np_day - calendar.epoch_day
        return [calendar.name, str(years)+str(months)+str(days)]

    @staticmethod
    def date_list(iso: str, *args: CalendarDefinition) -> list[list[str]]:
        """Construct a list of date and calendar names associated with the date."""
        items: list[list[str]] = []
        for calendar in args:
            items.append(Methods.date_item(iso, calendar))
        return items

    @staticmethod
    def pr_date(iso: str, *args: CalendarDefinition) -> None:
        """Convert an iso date to one or more defined calendar dates.

        Args:
            iso: The ISO 8601 string representation of a date.
                To use this for the current day set `iso` to `YYYY-MM-DD`.
            args: An arbitrarily long list of CalendarDefinitions.
                If there are no args, the Gregorian calendar is used by default.

        Return:
            A string containing a formatted table of dates in various calendars
            is returned.  Putting `print` around this will display the result
            in a formatted manner.

        """
        print(Methods.date_list(iso, *args))  # noqa: T201

    @staticmethod
    def pd_date(iso: str, *args: CalendarDefinition) -> None:
        """Convert an iso date to one or more defined calendar dates.

        Args:
            iso: The ISO 8601 string representation of a date.
                To use this for the current day set `iso` to `YYYY-MM-DD`.
            args: An arbitrarily long list of CalendarDefinitions.
                If there are no args, the Gregorian calendar is used by default.

        Return:
            A string containing a formatted table of dates in various calendars
            is returned.  Putting `print` around this will display the result
            in a formatted manner.

        """
        data_list: list[list[str]] = Methods.date_list(iso, *args)
        pd.DataFrame(data=data_list)
