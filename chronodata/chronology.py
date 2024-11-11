# Licensed under a 3-clause BSD style license - see LICENSE.md
"""This module provides procedures to create generic chronologies.
It also provides examples of chronologies of actual chronologies
from historical events around the world to processes either
hypothesized or observed in laboratory conditions.

The module also provides means of testing conflicting chronologies
using constraints that could lead one to falsify the
chronology unless the constraints are answered.
"""

import ast
import copy
import json
from datetime import datetime
from typing import Any, Literal

import numpy as np
import pandas as pd

from chronodata.utils.constants import Calendar, Datetime, Key, Msg, String

__all__ = ['Chronology']
__author__ = 'Frank Hubeny'


class Chronology():
    """Construct a dictionary to represent a chronology.

    The tools provide for storing dates associated with periods and events.
    - One can name an actor with an event.  
    - One can add a defense for each date to answer a challenge.  
    - One can add a challenge to argue against a competing chronology.
    - One can save the chronology to a human readable file.
    - The file may be modified with a text editor.
    - One can retrieve the dictionary from a file to continue building it.

    Routines
    --------

    See Also
    --------
    `Compare`: After two competing Chronologies have been constructed
        with defenses and challenges they may be compared with the
        visualization tools in this class.

    References
    ----------
    - Introduction to Calendars: https://aa.usno.navy.mil/faq/calendars Accessed on Oct 30, 2024

    Examples
    --------
    The first two examples show two competing chronologies for biblical history.

    The following would construct a brief chronology based on James Ussher's history.
    It also provides a defense against and a challenge for the older Byzantine chronology.

    The following constructs a brief chronology based on the Byzantine chronology.
    It contains a defense against and a challenge for the Ussher's history.

    The next two examples show to competing chronologies based on periods
    for the Ancient Near East.

    The following would construct a brief chronology as the basis of a genealogy.


    The following would construct a brief chronology of the decay of uranian-238.

    The following chronology provides a brief history of China using the
    Chinese calendar.

    The following example converts the above chronology of China to a
    Gregorian calendar.

    The following chronology provides a brief history of Islam using the
    Islamic calendar.

    The following example converts the above chronology of Islam to a
    secular calendar using 'CE' rather than 'AD' labels.
    """

    def __init__(
            self,
            name: str,
            calendar: dict[str, dict[str, str]] = Calendar.GREGORIAN,
            labelstrict: bool = False
        ):
        self.chronology: dict[str, Any] = {}
        self.calendar_dict: dict[str, dict[str, str]] = calendar
        self.calendar_name: str = self.calendar_dict[Key.CALENDAR][Key.NAME]
        self.chronology_name: str = name
        self.chronology_dict: dict[str, Any] = {Key.NAME: self.chronology_name}
        self.labelstrict: bool = labelstrict
        self.labelstrict_dict: dict[str, bool] = {Key.LABELS: self.labelstrict}
        self.comments_dict: dict[str, dict[str, dict[str, str]]] = {Key.COMMENTS: {}}
        self.actors_dict: dict[str, Any] = {Key.ACTORS: {}}
        self.challenges_dict: dict[str, Any] = {Key.CHALLENGES: {}}
        self.events_dict: dict[str, Any] = {Key.EVENTS: {}}
        self.markers_dict: dict[str, Any] = {Key.MARKERS: {}}
        self.periods_dict: dict[str, Any] = {Key.PERIODS: {}}
        self.sources_dict: dict[str, dict[str, dict[str, str]]] = {Key.SOURCES: {}}
        self.texts_dict: dict[str, Any] = {Key.TEXTS: {}}
        self.data: dict[str, Any]
        self.filename: str = ''
        if name[-5:] == '.json':
            self.filename = name
            file = open(self.filename)
            self.data = json.load(file)
            file.close()
            self.calendar_name = self.data[Key.CALENDAR][Key.NAME]
            self.chronology_name = self.data[Key.NAME]
            self.labelstrict = self.data[Key.LABELS]
            self.chronology_dict = {Key.NAME : self.chronology_name}
            self.calendar_dict = {Key.CALENDAR : self.data[Key.CALENDAR]}
            self.labelstrict_dict = {Key.LABELS : self.data[Key.LABELS]}
            self.comments_dict = {Key.COMMENTS : self.data[Key.COMMENTS]}
            if Key.ACTORS in self.data.keys():    
                self.actors_dict = {Key.ACTORS : self.data[Key.ACTORS]}
            if Key.CHALLENGES in self.data.keys():
                self.challenges_dict = {Key.CHALLENGES : self.data[Key.CHALLENGES]}
            if Key.EVENTS in self.data.keys():
                self.events_dict = {Key.EVENTS : self.data[Key.EVENTS]}
            if Key.MARKERS in self.data.keys():
                self.markers_dict = {Key.MARKERS : self.data[Key.MARKERS]}
            if Key.PERIODS in self.data.keys():
                self.periods_dict = {Key.PERIODS : self.data[Key.PERIODS]}
            if Key.SOURCES in self.data.keys():
                self.sources_dict = {Key.SOURCES : self.data[Key.SOURCES]}
            if Key.TEXTS in self.data.keys():
                self.texts_dict = {Key.TEXTS : self.data[Key.TEXTS]}
            print(Msg.CHRONOLOGY_LOADED.format(self.chronology_name, name, ))
        else:
            print(Msg.CHRONOLOGY_STARTED.format(self.chronology_name))
        self.poslabel: str = self.calendar_dict[Key.CALENDAR][Key.POSLABEL]
        self.poslabellen: int = len(self.poslabel)
        self.neglabel: str = self.calendar_dict[Key.CALENDAR][Key.NEGLABEL]
        self.neglabellen:int = len(self.neglabel)
        self.usezero: str = self.calendar_dict[Key.CALENDAR][Key.USEZERO]
        self.chronology.update(self.chronology_dict)
        self.chronology.update(self.calendar_dict)
        self.chronology.update(self.comments_dict)
        self.chronology.update(self.labelstrict_dict)
        self.chronology.update(self.actors_dict)
        self.chronology.update(self.challenges_dict)
        self.chronology.update(self.events_dict)
        self.chronology.update(self.markers_dict)
        self.chronology.update(self.periods_dict)
        self.chronology.update(self.sources_dict)
        self.chronology.update(self.texts_dict)

        #self.maindictionaries: list[str] = [key for key in self.chronology if key != Key.OVERVIEW]
        # self.poslabel: str = self.calendar_dict[Key.CALENDAR][Key.POSLABEL]
        # self.poslabellen: int = len(self.poslabel)
        # self.neglabel: str = self.calendar_dict[Key.CALENDAR][Key.NEGLABEL]
        # self.neglabellen: int = len(self.neglabel)
        # self.usezero: bool = self.calendar_dict[Key.CALENDAR][Key.USEZERO]
                        

    def show(self, tab: str = '    ') -> None:
        """Show the entire chronology."""
        self.dictionaries(tab)

    def __str__(self):
        self.show()
        return ''
    
    def rename(self, newname: str) -> None:
        """Rename the chronology."""
        self.chronology_dict.update({Key.NAME : newname})
        self.chronology_name = self.chronology_dict[Key.NAME]
        print(Msg.RENAME.format(self.chronology_name))


    ###### Dictionary Methods


    ###### Calendar Methods


    ###### Astronmical Methods


    ###### ACTORS 

    def actors(self) -> pd.DataFrame:
        """Display the actors in a chronology."""
        return self.show_dictionary(Key.ACTORS)


    def actors_pop(self, pops: list[str]) -> pd.DataFrame:
        """Display the actors defined for the chronology if there are any.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the actors.
            
        """
        return self.dictionary_pop(Key.ACTORS, pops)


    def add_actor(
            self, 
            name: str, 
            father: str = '', 
            mother: str = '', 
            birth: str = '', 
            death: str = '', 
            description: str = '', 
            **keyvalues: str
        ) -> None:
        """Add an actor to the dictionary."""
        if self.check_date(birth) and self.check_date(death): # and self.check_keys(keyvalues):
            self.chronology[Key.ACTORS].update({name : {
                Key.FATHER : father,
                Key.MOTHER : mother,
                Key.BIRTH : self.format_date(birth),
                Key.DEATH : self.format_date(death),
                Key.DESCRIPTION : description,
            }})
            self.chronology[Key.ACTORS][name].update(keyvalues)
            print(Msg.ADDED.format(String.ACTOR, self.chronology[Key.ACTORS][name]))


    def remove_actor(self, actorname: str) -> None:
        """Remove an actor from the dictionary."""
        self.remove_key(Key.ACTORS, actorname)


    ###### CALENDARS 

    def calendars(self) -> pd.DataFrame:
        """Display the CALENDARS constants."""
        return pd.DataFrame.from_dict(self.calendar_dict)
    

    def datetimes(self) -> pd.DataFrame:
        """Display the challenges in a chronology."""
        return pd.DataFrame.from_dict(Datetime.units) 
    

    def enable_strict_labels(self):
        """Set strict formatting for dates."""
        self.labelstrict = True
        self.chronology[Key.OVERVIEW].update({Key.LABELS : False})


    def disable_strict_labels(self):
        """Set relaxed formatting for dates."""
        self.labelstrict = False
        self.chronology[Key.OVERVIEW].update({Key.LABELS : False})


    def check_date(self, date: str) -> bool:
        cleandate = date.upper().strip()
        if cleandate[-self.neglabellen:] == self.neglabel:
            try:
                np.datetime64(cleandate[0:-self.neglabellen:])
            except ValueError:
                print(Msg.BAD_DATE.format(date, self.calendar_dict[Key.NAME]))
                return False
            else:
                return True
        elif cleandate[-self.poslabellen:] == self.poslabel:
            try:
                np.datetime64(cleandate[0:-self.poslabellen:])
            except ValueError:
                print(Msg.BAD_DATE.format(date, self.calendar_dict[Key.NAME]))
                return False
            else:
                return True
        elif not self.labelstrict:
            try:
                np.datetime64(cleandate)
            except ValueError:
                print(Msg.BAD_DATE.format(date, self.calendar_dict[Key.NAME]))
                return False
            else:
                return True
        else:
            print(Msg.BAD_LABEL.format(
                date, 
                date[-self.poslabellen:], 
                self.poslabel, 
                self.neglabel, 
                self.calendar_dict[Key.NAME]))
            return False


    def format_date(self, date: str) -> str:
        formatted_date: str = date.upper().strip()
        if self.labelstrict:
            try:
                np.datetime64(formatted_date)
            except ValueError:
                return formatted_date
            else: 
                return ''.join([formatted_date, self.poslabel])
        else:
            return formatted_date
        

    def to_datetime64(self, date: str) -> str:
        """Convert a calendar date to an ISO 8601 date and time string.
        
        The calendar date may contain labels.  These are removed.
        If the label signals a negative value for the NumPy string, 
        then a negative sign is added to the front of the string.
        
        Parameters
        ----------
        date: str
            The calendar date to be converted to a NumPy datetime64 data type
            extending the ISO 8601 functionality.

        See Also
        --------
        `date_diff`
            This method uses `to_datetime64` to convert a calendar
            date to a NumPy datetime64 data type.

        References
        ----------
        [The ISO 8601 Standard](https://en.wikipedia.org/wiki/ISO_8601)
        [NumPy Datetime64 Documentation](https://numpy.org/doc/stable/reference/arrays.datetime.html)
            
        """
        if date[-self.poslabellen:] == self.poslabel:
            newdate = date[0:-self.poslabellen]
        elif date[-self.neglabellen:] == self.neglabel:
            nolabeldate = date[0:-self.neglabellen]
            try:
                end = nolabeldate.index('-')
            except ValueError:
                end = len(nolabeldate)
            oldyear = nolabeldate[0:end]
            newyear = str(int(oldyear) - 1)
            newdate = ''.join([String.NEGATIVE, newyear, nolabeldate[len(oldyear):]])
            newdate = newdate
        else:
            newdate = date
        return newdate
    
    
    def date_diff(self, older: str, younger: str, unit: str = Datetime.YEAR) -> float:
        olderdate = np.datetime64(self.to_datetime64(older), unit)
        youngerdate = np.datetime64(self.to_datetime64(younger), unit)
        return float((youngerdate - olderdate) / np.timedelta64(1, unit))


    def daysinyear(self, date: str|np.datetime64) -> int:
        """A procedure to count number of days in a Gregorian year given the year.
        
        Parameters
        ----------
        date: np.datetime64
            The date to find the number of days in the year
            
        Examples
        --------

        """
        if isinstance(date, str):
            year = np.datetime64(date, Datetime.YEAR).astype('int') + 1970
        else:
            year = np.datetime_as_string(date, unit=Datetime.YEAR).astype('int') + 1970
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            return 366
        else:
            return 365


    def numericdate(self, date: str, unit: str = Datetime.YEAR) -> np.datetime64:
        """A procedure to convert an ISO string with KEYS to astronomical year numbering.
        This numeric value contains a Year Zero as 0.  Dates labelled as `BC` or `BCE`
        will be converted to a negative value one year larger than the string date with
        the label.
        
        Parameters
        ----------
        date: string
            The date that will be converted to a numeric value.

        Returns
        -------
        np.datetime64
            The numeric value of the date in astronomical time with Year Zero being 0.

        Examples
        --------
        >>> 

        """
        # Look for errors
        if date[0] == String.NEGATIVE:
            if date[-self.neglabellen:] == self.neglabel:
                raise ValueError(f'The year is negative but the date contains a negative label "{date[-self.neglabellen:]}"')
            elif date[-self.poslabellen:] == self.poslabel:
                raise ValueError(f'The year is negative but the date contains a positive label "{date[-self.poslabellen:]}"')

        # If no errors, proceed
        if date[-self.neglabellen:] == self.neglabel:
            if self.usezero:
                numericdate = np.datetime64('-'+date[0:-self.neglabellen])
            else:
                days = self.daysinyear(date[0:-self.neglabellen])
                numericdate = np.datetime64('-'+date[0:-self.neglabellen]) + np.timedelta64(days, Datetime.DAY)
        elif date[-self.poslabellen:] == self.poslabel:
            numericdate = np.datetime64(date[0:-self.poslabellen])
        else:
            numericdate = np.datetime64(date)
        return numericdate

    def stringdate(self, date: np.ndarray[Any, Any], unit: Literal['Y'] = Datetime.YEAR) -> np.ndarray[Any, np.dtype[Any]]:
        """A procedure to convert a numeric date to a date labelled with an epoch label.
        
        Parameters
        ----------
        date: np.datetime64
            The numeric date to be converted to a string

        """
        
        return np.datetime_as_string(date, unit=unit)

    
    def add_calendar(self, name: str, begin: str, end: str, **keyvalues: str) -> None:
        """Add a calendar to the dictionary."""
        pass


    def to(self, calendar: dict[str, dict[str, str]]) -> None:
        """Convert the calendar of the chronology to anther calendar.
        
        Parameter
        ---------
        calendar: str
            The key of the calendar to convert the current calendar to.
        """
        
        if calendar[Key.CALENDAR][Key.NAME] == self.calendar_dict[Key.CALENDAR][Key.NAME]:
            print(Msg.HAS_CALENDAR.format(self.calendar_dict[Key.CALENDAR][Key.NAME]))
        else:
            labelcalendars: list[dict[str, dict[str, str]]] = [Calendar.GREGORIAN, Calendar.SECULAR]
            formercalendar: dict[str, dict[str, str]] = self.calendar_dict
            poslabel: str = formercalendar[Key.CALENDAR][Key.POSLABEL]
            poslabellen: int = -len(poslabel)
            newcalendar = calendar
            if calendar in labelcalendars and self.calendar_dict in labelcalendars:
                self.calendar_dict.update(newcalendar)
                for i in self.periods_dict[Key.PERIODS]:
                    for k in [Key.BEGIN, Key.END]:
                        if self.periods_dict[Key.PERIODS][i][k][-poslabellen:] == poslabel:
                            newvalue = self.periods_dict[Key.PERIODS][i][k].replace(
                                formercalendar[poslabel], 
                                newcalendar[poslabel]
                            )
                        else:
                            newvalue = self.periods_dict[Key.PERIODS][i][k].replace(
                                formercalendar[Key.NEGLABEL], 
                                newcalendar[Key.NEGLABEL]
                            )
                        self.periods_dict[Key.PERIODS][i].update({k : newvalue})
                for i in self.events_dict[Key.EVENTS]:
                    for k in [Key.DATE]:
                        if self.events_dict[Key.EVENTS][i][k][poslabellen:] == poslabel:
                            newvalue = self.events_dict[Key.EVENTS][i][k].replace(
                                formercalendar[Key.POSLABEL], 
                                newcalendar[Key.POSLABEL]
                            )
                        else:
                            newvalue = self.events_dict[Key.EVENTS][i][k].replace(
                                formercalendar[Key.NEGLABEL], 
                                newcalendar[Key.NEGLABEL]
                            )
                        self.events_dict[Key.EVENTS][i].update({k : newvalue})
                self.calendar_name = self.calendar_dict['CALENDAR'][Key.NAME]
                self.poslabel = self.calendar_dict['CALENDAR'][Key.POSLABEL]
                self.poslabellen = len(self.poslabel)
                self.neglabel = self.calendar_dict['CALENDAR'][Key.NEGLABEL]
                self.neglabellen = len(self.neglabel)
                print(Msg.CHANGED.format(self.calendar_name))


    ###### CHALLENGES 

    def challenges(self) -> pd.DataFrame:
        """Display the challenges in a chronology."""
        return self.show_dictionary(Key.CHALLENGES)


    def challenges_pop(self, pops: list[str]) -> pd.DataFrame:
        """Display the challenges defined for the chronology if there are any.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the periods.
            
        """
        return self.dictionary_pop(Key.CHALLENGES, pops)


    def add_challenge(self, name: str, date: str, description: str = '', **keyvalues: str) -> None:
        """Add a challenge to the dictionary."""
        if self.check_date(date): # and self.check_keys(keyvalues):
            self.challenges_dict[Key.CHALLENGES].update({name : {
                Key.DATE : self.format_date(date),
                Key.DESCRIPTION : description,
            }})
            self.challenges_dict[Key.CHALLENGES][name].update(keyvalues)
            print(Msg.ADDED.format(String.CHALLENGE, self.challenges_dict[Key.CHALLENGES][name]))
            


    def remove_challenge(self, challengename: str) -> None:
        """Remove a challenge from the dictionary."""
        self.remove_key(Key.CHALLENGES, challengename)


    ###### COMMENTS 

    def comments(self) -> pd.DataFrame:
        """Display a numbered list of comments."""
        lengthlist: int = len(self.comments_dict[Key.COMMENTS])
        if lengthlist == 0:
            print(Msg.NO_COMMENTS.format(self.chronology_name))
        return pd.DataFrame.from_dict(self.comments_dict[Key.COMMENTS], orient='index')


    def add_comment(self, text: str = '') -> None:
        """Add a comment to a chronology.
        
        To create a comment with more than one line use `\n` to separate the lines.

        Parameters
        ----------
        text: str
            A comment one or more lines long. Each line ended with `\n`.

        See Also
        --------
        `comments`
            Display all comments in the chronology.
        `remove_comment`
            Remove a line from the comment list.
        `remove_all_comments`
            Remove all comments from the chronology.

        Notes
        -----
        Comments are placed at the beginning of the file before the dictionaries.

        The file may be opened and edited with a text editor.

        To add a blank line, accept the default value for `text`.

        Exampless
        ---------
        
        """

        texts: list[str] = text.split(String.NEWLINE)
        timestamp: str = str(datetime.now())
        for i in texts:
            how_many_comments: str = str(len(self.comments_dict[Key.COMMENTS]) + 1)
            self.comments_dict[Key.COMMENTS].update({how_many_comments : {
                Key.MESSAGE : i.strip(),
                Key.TIMESTAMP : timestamp,
            }})
        print(Msg.ADDED_COMMENT.format(text))


    def remove_comment(self, *index: int) -> None:
        """Remove a comment from the chronology by specifying its number in the comments list."""
        for idx in index:
            if str(idx) not in self.comments_dict[Key.COMMENTS].keys():
                print(Msg.OUT_OF_RANGE.format(str(idx)))
            else:
                removed_comment = self.comments_dict[Key.COMMENTS][str(idx)][Key.MESSAGE]
                self.comments_dict[Key.COMMENTS].pop(str(idx))
                comments: list[dict[str, dict[str, str]]] = []
                for i in self.comments_dict[Key.COMMENTS]:
                    comments.append(self.comments_dict[Key.COMMENTS][i])
                self.remove_all_comments(show_message=False)
                for i in range(1, len(comments) + 1):
                    self.comments_dict[Key.COMMENTS].update({str(i) : comments[i-1]})
                print(Msg.COMMENT_REMOVED.format(str(idx), removed_comment))
        

    def remove_all_comments(self, show_message: bool = True) -> None:
        """Remove all comments from the chronology."""
        self.comments_dict = {Key.COMMENTS: {}}
        if show_message:
            print(Msg.ALL_COMMENTS_REMOVED.format(self.chronology_name))


    ###### DICTIONARIES

    def reserved_keys(self) -> pd.DataFrame:
        """Display the KEYS constants."""
        return pd.DataFrame(data=Key.keylist, columns=['Reserved Keys']) 
    
    def check_keys(self, keyvalues: dict[str, str] | dict[str, dict[str, Any]]) -> bool:
        count = 0
        for i in keyvalues.keys():
            if i in Key.keylist:
                print(Msg.RESERVED.format(i))
                count += 1
        if count > 0:
            return False
        else:
            return True

    def dictshow(self, 
                 dictname: str = '', 
                 tab: str = '    ', 
                 expand: int = 0, 
                 as_json: bool = False, 
                 as_pandas: bool = False) -> Any:
        if dictname == '':
            dictionary = self.chronology
        else:
            dictionary = self.chronology[dictname]
        if as_json:
            print(json.dumps(dictionary, indent=len(tab)))
        elif as_pandas:
            return pd.DataFrame.from_dict(dictionary)
        else:
            for key in dictionary.keys():
                if expand > 0 and isinstance(dictionary[key], dict):
                    if len(dictionary[key]) > 0:
                        print(f'{key}: {String.LEFT_BRACE}')
                        for subkey in dictionary[key]:
                            print(f'{tab}{subkey}: {dictionary[key][subkey]}')
                        print(String.RIGHT_BRACE)
                    else:
                        print(f'{key}: {dictionary[key]}')
                else:
                    print(f'{key}: {dictionary[key]}')

    def dictionaries(self, tab: str = '    ', dictname: str = '') -> None:
        for key in self.chronology.keys():
            if isinstance(self.chronology[key], dict):
                if len(self.chronology[key]) > 0:
                    print(f'{key}: {String.LEFT_BRACE}')
                    for subkey in self.chronology[key]:
                        if subkey == Key.COMMENTS and len(self.chronology[key][subkey]) > 0:
                            print(f'{tab}{subkey}: {String.LEFT_BRACE}')
                            for subsubkey in self.chronology[key][subkey]:
                                print(f'{tab}{tab}{subsubkey}: {self.chronology[key][subkey][subsubkey]}')
                            print(f'{tab}{String.RIGHT_BRACE}')
                        else:
                            print(f'{tab}{subkey}: {self.chronology[key][subkey]}')
                    print(String.RIGHT_BRACE)
                else:
                    print(f'{key}: {self.chronology[key]}')
            else:
                print(f'{key}: {self.chronology[key]}')


    def dictionary_pop(self, dictname: str, pops: list[str]) -> pd.DataFrame:
        """Display the dictionary except for specified keys.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the dictionary.
        dictname: str
            The name of the dictionary to display.
            
        """
        dictionary: dict[str, dict[str, Any]] = copy.deepcopy(dict(self.chronology[dictname]))
        for i in pops:
            for j in dictionary:
                try:
                    dictionary[j].pop(i)
                except KeyError:
                    break
        return pd.DataFrame.from_dict(dictionary, orient='index')
    

    def show_dictionary(self, dictname: str) -> pd.DataFrame:
        if len(self.chronology[dictname]) == 0:
            print(Msg.NO_DICT_NAME.format(self.chronology_name, dictname.lower()))
        return pd.DataFrame.from_dict(self.chronology[dictname], orient='index')
         
    
    def remove_key(self, dictname: str, key: str) -> None:
        """Revove a key from a dictionary of the chronology.  
        
        Reserved keys cannot be removed, but they can be hiddened when displaying
        the dictionary or entire chronology.

        Parameters
        ----------
        dictname: str
            The name of the dictionary within the chronology where the key will be removed
        key: str
            The name of the key to be removed from the dictionary
        
        """
        if key in Key.keylist:
            print(Msg.NOT_REMOVABLE.format(key))
        elif key not in self.chronology[dictname].keys():
            print(Msg.NOT_IN_DICT.format(key, dictname))
        else:
            self.chronology[dictname].pop(key)
            print(Msg.KEY_REMOVED.format(key, dictname))


    ###### EVENTS 

    def events(self) -> pd.DataFrame:
        """Display the EVENTS dictionary."""
        return self.show_dictionary(Key.EVENTS)


    def events_pop(self, pops: list[str]) -> pd.DataFrame:
        """Display the events defined for the chronology without some of the keys.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the events.
            
        """
        return self.dictionary_pop(Key.EVENTS, pops)
    
    
    def add_event(
            self, 
            name: str, 
            date: str, 
            description: str = '', 
            **keyvalues: str
        ) -> None:
        """Add an event to the dictionary."""
        if self.check_date(date): #and self.check_keys(keyvalues):
            self.chronology[Key.EVENTS].update({name : {
                Key.DATE : self.format_date(date),
                Key.DESCRIPTION : description,
            }})
            self.chronology[Key.EVENTS][name].update(keyvalues)
            print(Msg.ADDED.format(String.EVENT, self.chronology[Key.EVENTS][name]))


    def remove_event(self, eventname: str) -> None:
        """Remove an event from the dictionary."""
        self.remove_key(Key.EVENTS, eventname)

        
    ###### MARKERS 

    def markers(self) -> pd.DataFrame:
        """Display the markers in a chronology."""
        return self.show_dictionary(Key.MARKERS)


    def markers_pop(self, pops: list[str]) -> pd.DataFrame:
        """Display the markers defined for the chronology if there are any.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the markers.
            
        """
        return self.dictionary_pop(Key.MARKERS, pops)
    

    def add_marker(self, name: str, date: str, description: str = '', **keyvalues: str) -> None:
        """Add a marker to the dictionary."""
        if self.check_date(date) and self.check_keys(keyvalues):
            self.chronology[Key.MARKERS].update({name : {
                Key.DATE : self.format_date(date),
                Key.DESCRIPTION : description,
            }})
            self.chronology[Key.MARKERS][name].update(keyvalues)
            print(Msg.ADDED.format(String.MARKER, self.chronology[Key.MARKERS][name]))
        

    def remove_marker(self, markername: str) -> None:
        """Remove a marker from the dictionary."""
        self.remove_key(Key.MARKERS, markername)


    ###### PERIODS 

    def periods(self) -> pd.DataFrame:
        """Display the periods defined for the chronology if there are any."""
        return self.show_dictionary(Key.PERIODS)


    def periods_pop(self, pops: list[str]) -> pd.DataFrame:
        """Display the periods defined for the chronology except for specified keys.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the periods.
            
        """
        return self.dictionary_pop(Key.PERIODS, pops)

    
    def add_period(self, name: str, begin: str, end: str, **keyvalues: str) -> None:
        """Add a period to the dictionary."""
        if self.check_date(begin) and self.check_date(end) and self.check_keys(keyvalues): 
            self.chronology[Key.PERIODS].update({name : {
                Key.BEGIN : self.format_date(begin),
                Key.END : self.format_date(end),
            }})
            self.chronology[Key.PERIODS][name].update(keyvalues)
            print(Msg.ADDED.format(String.PERIOD, self.chronology[Key.PERIODS][name]))


    def remove_period(self, periodname: str) -> None:
        """Remove a period from the dictionary."""
        self.remove_key(Key.PERIODS, periodname)


    ###### SAVE 

    def save(self, file_name: str = '') -> None:
        if file_name == '':
            if self.filename == '':
                file = ''.join([self.chronology_name, '.json'])
            else:
                file = self.filename
        else:
            file = file_name
        with open(file, 'w') as f:
            json.dump(self.chronology, f, indent=4)
            f.close()
        print(Msg.FILE_SAVED.format(file))


    def save_as_json(self, filename: str) -> None:
        with open(filename, 'w') as file:
            json.dump(self.chronology, file, indent=4)


    # def save_as_html(self) -> None:
    #     pass


    # def save_as_pdf(self) -> None:
    #     pass

    
    ###### TEXTS 

    def texts(self) -> pd.DataFrame:
        """Display the texts referenced to justify a chronology."""
        return self.show_dictionary(Key.TEXTS)


    def texts_pop(self, pops: list[str]) -> pd.DataFrame:
        """Display the texts defined for the chronology except for specified keys.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the texts.
            
        """
        return self.dictionary_pop(Key.TEXTS, pops)


    def add_text(self, name: str, date: str, description: str = '', **keyvalues: str) -> None:
        """Add an event to the dictionary."""
        if self.check_date(date): # and self.check_keys(keyvalues):
            self.chronology[Key.TEXTS].update({name : {
                Key.DATE : self.format_date(date),
                Key.DESCRIPTION : description,
            }})
            self.chronology[Key.TEXTS][name].update(keyvalues)
            print(Msg.ADDED.format(String.TEXT, self.chronology[Key.TEXTS][name]))


    def remove_text(self, textname: str) -> None:
        """Permanently remove a text from the dictionary."""
        self.remove_key(Key.TEXTS, textname)
        