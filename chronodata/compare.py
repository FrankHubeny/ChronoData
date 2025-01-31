# Licensed under a 3-clause BSD style license - see LICENSE.md
"""Methods to compare a set of chronologies with savable challenges."""

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd  # type: ignore[import-untyped]  

from chronodata.messages import Column, Msg
from chronodata.readwrite import Base


@dataclass(frozen=True)
class String:
    """The following constants define strings that are neither keys
    nor values of a dictionary, but are used in generating comments,
    formatting numbers or other processes.
    """

    ATSIGN: str = '@'
    BANNED: str = r'[\u0000-\u001F\u007F\uD800-\uDFFF\uFFFE\uFFFF]'
    BC: str = 'BCE'
    CHRON_NAMES: str = 'CHRON NAMES'
    CHRONS: str = 'CHRONS'
    COLON: str = ':'
    CSV: str = '.csv'
    DATA: str = 'DATA'
    DATE: str = 'DATE'
    DAY: str = 'd'
    DOUBLE_NEWLINE: str = '\n\n'
    EMPTY: str = ''
    EVENT: str = 'EVENT'
    FORM_DEFAULT1: str = 'City'
    FORM_DEFAULT2: str = 'County'
    FORM_DEFAULT3: str = 'State'
    FORM_DEFAULT4: str = 'Country'
    FRENCH_R: str = 'FRENCH_R'
    GED: str = '.ged'
    GRAMPS: str = '.gramps'
    GREATER_THAN: str = '>'
    GREGORIAN: str = 'GREGORIAN'
    HEBREW: str = 'HEBREW'
    HYPHEN: str = '-'
    INDENT: str = '    '
    INDEX: str = 'index'
    INT: str = 'int'
    JSON: str = '.json'
    JULIAN: str = 'JULIAN'
    LANG_URI: str = 'http://'
    LESS_THAN: str = '<'
    LOCATION: str = 'lower right'
    MAX_MONTHS: str = 'Max Months'
    MONTH: str = 'm'
    MONTH_NAMES: str = 'Month Names'
    MONTH_MAX_DAYS: str = 'Month Max Days'
    NAME: str = 'NAME'
    NEGATIVE: str = '-'
    NEWLINE: str = '\n'
    NOW: str = 'now'
    OCCURRED: Literal['Y'] = 'Y'
    PLACE_FULL = 'F'
    PLACE_SHORT = 'S'
    PLACE_TRANSLATION = 'T'
    MAX = 'MAX'
    MIN = 'MIN'
    READ: str = 'r'
    SPACE: str = ' '
    T: str = 'T'
    TESTCASES: str = 'TEST CASES'
    UNDERLINE: str = '_'
    UNDETERMINED: str = 'und'
    VERSION: str = '7.0'
    WEEK: str = 'w'
    WRITE: str = 'w'
    YEAR: str = 'y'
    Z: str = 'Z'

class Challenge:
    """Load a set of chronologies, construct challenges, view and save."""

    def __init__(
        self,
        name: str = '',
        filename: str = '',
        begin_event: str = '',
        end_event: str = '',
        chrons: list[str] | None = None,
        test_cases: list[list[Any]] | None = None,
    ):
        if chrons is None:
            chrons = []
        if test_cases is None:
            test_cases = []
        self.name: str = name
        self.filename: str = filename
        self.begin_event: str = begin_event
        self.end_event: str = end_event
        self.chrons: list[str] = chrons
        self.chronologies: list[Base] = []
        for file in self.chrons:
            self.chronologies.append(Base(filename=file, log=False))
        self.test_cases: list[list[Any]] = test_cases
        self.test_columns = [
            Column.TEST_NAME,
            Column.YEARS_AGO,
            Column.CHART_COLOR,
            Column.CHART_LINE_STYLE,
        ]
        self.chron_names: list[str] = [
            chronology.chron_name for chronology in self.chronologies
        ]
        self.chron_columns: list[str] = []
        today = datetime.now()
        if end_event == '':
            self.chron_columns = [
                begin_event,
                Column.YEARS_SINCE.format(str(today.year)),
            ]
        else:
            self.chron_columns = [
                begin_event,
                end_event,
                Column.DURATION,
            ]
        self.chron_data: list[list[Any]] = []
        # for chronology in self.chronologies:
        #     begin_event_date = chronology.chron[Tag.EVEN][begin_event][Tag.DATE]
        #     #begin_years_since = chronology.date_diff(
        #     #    begin_event_date, str(today)
        #     #)
        #     if end_event != '':
        #         end_event_date = chronology.chron[Tag.EVEN][end_event][Tag.DATE]
        #         #begin_end_duration = chronology.date_diff(
        #         #    begin_event_date, end_event_date
        #         #)
        #         # self.chron_data.append(
        #         #     [
        #         #         begin_event_date,
        #         #         end_event_date,
        #         #         begin_end_duration,
        #         #     ]
        #         # )
        #     else:
        #         self.chron_data.append([begin_event_date, begin_years_since])
        self.challenge: dict[str, Any] = {
            String.NAME: self.name,
            String.CHRONS: self.chrons,
            String.TESTCASES: self.test_cases,
            String.DATA: self.chron_data,
            String.CHRON_NAMES: self.chron_names,
        }
        if self.name == '' and self.filename == '':
            logging.info(Msg.NAME_OR_FILENAME)
        elif self.filename != '':
            with Path.open(Path(self.filename), String.READ) as openfile:
                self.challenge = json.load(openfile)
                openfile.close()
            self.name = self.challenge[String.NAME]
            for file in self.challenge[String.CHRONS]:
                self.chrons.append(file)
                self.chronologies.append(Base(filename=file, log=False))
            for test_item in self.challenge[String.TESTCASES]:
                self.test_cases.append(test_item)
            for data_list in self.challenge[String.DATA]:
                self.chron_data.append(data_list)
            for chron_name in self.challenge[String.CHRON_NAMES]:
                self.chron_names.append(chron_name)
            logging.info(
                Msg.CHALLENGE_LOADED.format(self.name, self.chron_names)
            )
        else:
            # for file in self.chrons:
            #     self.chronologies.append(Base(filename=file))
            logging.info(
                Msg.CHALLENGE_BEGIN.format(self.name, self.chron_names)
            )

    def add_age_test_case(
        self, item: str, age: float, color: str, line: str
    ) -> None:
        """Add items with ages that conflict with some chronologies.

        Parameters
        ----------
        item
            The name of the test case.
        age
            A float value representing the age of the item.
        color
            The color used on the chart to identify this test case.
        line
            The line style used on the chart to identify this test case.

        Examples
        --------

        """
        self.test_cases.append([item, age, color, line])
        logging.info(Msg.ITEM_ADDED.format(item))

    def save(self, filename: str = '', overwrite: bool = False) -> None:
        if filename == '':
            filename = self.filename
        else:
            self.filename = filename
        if Path.exists(Path(filename)) and not overwrite:
            logging.info(Msg.FILE_EXISTS.format(filename))
        else:
            with Path.open(Path(self.filename), String.WRITE) as file:
                json.dump(self.challenge, file)
                file.close()
            logging.info(Msg.CHALLENGE_SAVED.format(self.name, self.filename))

    def remove_age_testcase(self, item: str) -> None:
        for index, value in enumerate(self.test_cases):
            if value[0] == item:
                self.test_cases.pop(index)
                logging.info(Msg.ITEM_REMOVED.format(item))
                return
        logging.info(Msg.ITEM_NOT_FOUND.format(item))
        return

    def test_data(self) -> pd.DataFrame:
        """Display the set of test cases used in this challenge.

        Returns
        -------
        A Pandas DataFrame is returned.
        """
        test_index = list(range(1, len(self.test_cases) + 1))
        return pd.DataFrame(
            data=self.test_cases, columns=self.test_columns, index=test_index
        )

    def test_description(self) -> pd.DataFrame | None:
        """Describe the set of test cases giving mean, standard deviation,
        median and skewness.

        Rounding decimal values is based on the
        American Psychological Association. (2024).
        [APA Style numbers and statistics guide](https://apastyle.apa.org/instructional-aids/numbers-statistics-guide.pdf).

        Returns
        -------
        A Pandas DataFrame is returned if there is more than one test case.
        If there is less than two test cases a message is returned.
        """
        match len(self.test_cases):
            case 0:
                logging.info(Msg.NO_TESTS.format(self.name))
                return None
            case 1:
                logging.info(Msg.ONE_TEST.format(self.name))
                return None
            case _:
                data = [data_item[1] for data_item in self.test_cases]
                centers = []
                mean = np.mean(data)
                standard_deviation = np.std(data)
                median = np.median(data)
                skewness = 3 * (mean - median) / standard_deviation
                centers.append([str(np.round(mean, 1))])
                centers.append([str(np.round(standard_deviation, 1))])
                centers.append([str(np.round(median, 1))])
                centers.append([str(np.round(skewness, 2))])
                return pd.DataFrame(
                    data=centers,
                    columns=[self.name],
                    # index=[Column.MEAN, Column.STD, Column.MEDIAN, Column.SKEW],
                )

    def chronology_data(self) -> pd.DataFrame:
        """Display the data that will be compared from all chronologies."""
        return pd.DataFrame(
            data=self.chron_data,
            columns=self.chron_columns,
            index=self.chron_names,
        )

    def chart(
        self,
        bar_width: float = 0.5,
        figure_height: int = 10,
        figure_width: int = 8,
        number_format: float = 0.5,
    ) -> None:
        """Display a chart comparing the chronologies with tests cases."""
        # Collect data for the chart.
        if self.end_event == '':
            bar_heights = [year[1] for year in self.chron_data]
        else:
            bar_heights = [year[2] for year in self.chron_data]
        tests = [test[1] for test in self.test_cases]
        maxtests = max(tests)
        dev_pct = [(value - maxtests) / maxtests * 100 for value in bar_heights]
        colors = [
            'green' if (value > maxtests) else 'grey' for value in bar_heights
        ]

        # Construct the bar chart with labels, title and keys
        keys = [
            f'{dev_pct[i]!s:{number_format}}%\n{bar_heights[i]} years\n{self.chron_names[i]}'
            for i in range(len(self.chron_names))
        ]
        plt.figure(figsize=(figure_height, figure_width))
        plt.bar(keys, bar_heights, color=colors, width=bar_width)
        # plt.xlabel(Label.CHRONOLOGIES, fontweight='bold', fontsize=15)
        # plt.ylabel(Label.YEARS, fontweight='bold', fontsize=15)
        # plt.title(Label.TEST.format(self.name), fontweight='bold', fontsize=20)

        # Add in the tests as horizontal lines with a legend
        for test in self.test_cases:
            plt.axhline(
                y=test[1], color=test[2], linestyle=test[3], label=test[0]
            )
        plt.legend(loc=String.LOCATION)

        # Display the chart with both bars and tests
        plt.show()
