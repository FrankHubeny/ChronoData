# Licensed under a 3-clause BSD style license - see LICENSE.md
"""This module provides procedures to create generic chronologies.
It also provides examples of chronologies of actual chronologies
from historical events around the world to processes either
hypothesized or observed in laboratory conditions.

The module also provides means of testing conflicting chronologies
using constraints that could lead one to falsify the
chronology unless the constraints are answered.
"""

from datetime import datetime
import numpy as np
import pandas as pd
import json
import ast
import copy
from typing import Any, Literal

from chronodata.utils.constants import String, Msg, Datetime, Key, Calendar

__all__ = ['Chronology']
__author__ = 'Frank Hubeny'


#class Compare():
    # """Compare two or more chronologies for the same events.

    # Routines
    # --------

    # See Also
    # --------
    # `Chronology`: The compared chronologies being were created or read
    #     from files using this class.  

    # References
    # ----------

    # Examples
    # --------
    # The following example compares James Ussher's history of the world
    # with a modern version of the older Byzantine church chronology.
    # The challenges by each of these chronologies are used
    # """

    # def __init__(self, chronologies: list):
    #     self.chronologies = chronologies


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

    USER: str = ''

    def __init__(
            self,
            chronologyname: str = '',
            filename: str = '',
            calendar: str = Key.GREGORIAN,
            user: str = '',
            labelstrict: bool = False
        ):
        self.chronologyname: str = ''
        self.filename: str = ''
        self.name: str = ''
        self.calendar: str = ''
        if chronologyname == '' and filename == '':
            print(Msg.MISSING_NAME)
        elif chronologyname != '' and filename != '':
            print(Msg.BOTH_NAME_FILE.format(chronologyname, filename)) 
        elif chronologyname != '':
            self.chronologyname = chronologyname
        else: 
            self.filename = filename  
        if self.chronologyname != '' or self.filename != '':
            self.user: str = ''
            if user == '' and self.USER == '':
                print(Msg.USER_REQUIRED.format(chronologyname, filename))
            elif user == '' and self.USER != '':
                self.user = self.USER
            elif user != '' and self.USER == '':
                self.user = user
                self.USER = self.user
            else:
                self.user = self.USER
            if self.user != '':
                self.labelstrict: bool = labelstrict
                self.chronology = {}
                if chronologyname != '':
                    self.chronology.update({
                        Key.OVERVIEW : {
                            Key.NAME : chronologyname,
                            Key.COMMENTS : {},
                            Key.CALENDAR : Calendar.system[calendar],
                            Key.LABELS : self.labelstrict,
                        },
                        Key.ACTORS : {},
                        Key.CHALLENGES : {},
                        Key.EVENTS : {},
                        Key.MARKERS : {},
                        Key.PERIODS : {},
                        Key.TEXTS : {},
                    })
                    self.name = self.chronologyname
                    self.calendar = calendar 
                    print(Msg.CHRONOLOGY_STARTED.format(self.chronologyname, self.user))
                else:
                    with open(filename, 'r') as file:
                        for line in file:
                            self.chronology.update(ast.literal_eval(line))
                        # data = json.load(file)
                        # self.chronology = ast.literal_eval(data)
                        file.close()
                    self.name = self.chronology[Key.OVERVIEW][Key.NAME]
                    self.calendar = self.chronology[Key.OVERVIEW][Key.CALENDAR][Key.NAME]
                    print(Msg.CHRONOLOGY_LOADED.format(self.chronology[Key.OVERVIEW][Key.NAME], self.filename, self.user))
                self.maindictionaries: list[str] = [key for key in self.chronology if key != Key.OVERVIEW]
                self.poslabel: str = Calendar.system[self.calendar][Key.POSLABEL]
                self.poslabellen: int = len(self.poslabel)
                self.neglabel: str = Calendar.system[self.calendar][Key.NEGLABEL]
                self.neglabellen: int = len(self.neglabel)
                self.usezero: bool = Calendar.system[self.calendar][Key.USEZERO]
                        

    def show(self, tab: str = '    '):
        """Show the entire chronology of both comments and dictionaries."""
        self.dictionaries(tab)

    def __str__(self):
        self.show()
        return ''
    
    def rename(self, newname: str) -> str:
        """Rename the chronology."""
        self.chronology[Key.OVERVIEW].update({Key.NAME : newname})
        self.name = self.chronology[Key.OVERVIEW][Key.NAME]
        print(Msg.RENAME.format(self.name))

    def combine(self, newname: str, chronology: dict):
        """Return a new chronology containing a combination of the current one and another chronology.

        The two source chronologies are not changed.  A new chronology containing both 
        of them is returned.  The two chronologies must have the same calendar. Use
        the `to` method to convert one of the chronologies to the other if their
        calendars do not agree.

        See Also
        --------
        to
        
        Parameters
        ----------
        chronologyname: str
            The name of the new chronology
        chronology: dict
            The chronology to combine with the present one.
        comments: list (optional)
            The comments from the combined chronology.
        keepcomments: bool (default True)
            Add the comments from the self chronology into the new chronology.
        """

        if self.calendar == chronology[Key.OVERVIEW][Key.CALENDAR][Key.NAME]:
            newchron: Chronology = Chronology(user=self.user, chronologyname=newname, calendar=self.calendar)
            for key in self.maindictionaries:
                newchron.chronology.update(self.chronology[key])
                newchron.chronology.update(chronology[key])
            return newchron
        else:
            print(Msg.CALENDARS_DONT_MATCH.format(
                self.calendar, 
                chronology[Key.OVERVIEW][Key.CALENDAR][Key.NAME]
            ))


    ###### ACTORS 

    def actors(self) -> pd.DataFrame:
        """Display the actors in a chronology."""
        return self.show_dictionary(Key.ACTORS)


    def actors_pop(self, pops: list[str]):
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
            **keyvalues
        ) -> str:
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


    def remove_actor(self, actorname: str) -> str:
        """Remove an actor from the dictionary."""
        self.remove_key(Key.ACTORS, actorname)


    ###### CALENDARS 

    def calendars(self) -> pd.DataFrame:
        """Display the CALENDARS constants."""
        return pd.DataFrame.from_dict(Calendar.system)
    

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
                print(Msg.BAD_DATE.format(date, self.calendar))
                return False
            else:
                return True
        elif cleandate[-self.poslabellen:] == self.poslabel:
            try:
                np.datetime64(cleandate[0:-self.poslabellen:])
            except ValueError:
                print(Msg.BAD_DATE.format(date, self.calendar))
                return False
            else:
                return True
        elif not self.labelstrict:
            try:
                np.datetime64(cleandate)
            except ValueError:
                print(Msg.BAD_DATE.format(date, self.calendar))
                return False
            else:
                return True
        else:
            print(Msg.BAD_LABEL.format(date, date[-self.poslabellen:], self.poslabel, self.neglabel, self.calendar))
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


    def numericdate(self, date: str, unit: str = Datetime.YEAR) -> float:
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

    def stringdate(self, date: np.ndarray[Any, Any], unit: Literal['Y'] = Datetime.YEAR) -> str:
        """A procedure to convert a numeric date to a date labelled with an epoch label.
        
        Parameters
        ----------
        date: np.datetime64
            The numeric date to be converted to a string

        """
        if date is None:
            return ''
        else:
            return np.datetime_as_string(date, unit=unit)

    
    def add_calendar(self, name: str, begin: str, end: str, **keyvalues) -> None:
        """Add a calendar to the dictionary."""
        pass


    def to(self, calendar: str) -> None:
        """Convert the calendar of the chronology to anther calendar.
        
        Parameter
        ---------
        calendar: str
            The key of the calendar to convert the current calendar to.
        """
        
        if Calendar.system[calendar][Key.NAME] == self.calendar:
            print(Msg.HAS_CALENDAR.format(self.calendar))
        else:
            labelcalendars: list[str] = [Key.GREGORIAN, Key.SECULAR]
            formercalendar = Calendar.system[self.calendar]
            poslabel: str = formercalendar[Key.POSLABEL]
            poslabellen: int = -len(poslabel)
            newcalendar = Calendar.system[calendar]
            if calendar in labelcalendars and self.calendar in labelcalendars:
                self.chronology[Key.OVERVIEW][Key.CALENDAR].update(newcalendar)
                for i in self.chronology[Key.PERIODS]:
                    for k in [Key.BEGIN, Key.END]:
                        if self.chronology[Key.PERIODS][i][k][-poslabellen:] == poslabel:
                            newvalue = self.chronology[Key.PERIODS][i][k].replace(
                                formercalendar[poslabel], 
                                newcalendar[poslabel]
                            )
                        else:
                            newvalue = self.chronology[Key.PERIODS][i][k].replace(
                                formercalendar[Key.NEGLABEL], 
                                newcalendar[Key.NEGLABEL]
                            )
                        self.chronology[Key.PERIODS][i].update({k : newvalue})
                for i in self.chronology[Key.EVENTS]:
                    for k in [Key.DATE]:
                        if self.chronology[Key.EVENTS][i][k][poslabellen:] == poslabel:
                            newvalue = self.chronology[Key.EVENTS][i][k].replace(
                                formercalendar[Key.POSLABEL], 
                                newcalendar[Key.POSLABEL]
                            )
                        else:
                            newvalue = self.chronology[Key.EVENTS][i][k].replace(
                                formercalendar[Key.NEGLABEL], 
                                newcalendar[Key.NEGLABEL]
                            )
                        self.chronology[Key.EVENTS][i].update({k : newvalue})
                self.calendar = self.chronology[Key.OVERVIEW][Key.CALENDAR][Key.NAME]
                self.poslabel = Calendar.system[self.calendar][Key.POSLABEL]
                self.poslabellen = len(self.poslabel)
                self.neglabel = Calendar.system[self.calendar][Key.NEGLABEL]
                self.neglabellen = len(self.neglabel)
                print(Msg.CHANGED.format(self.calendar))


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


    def add_challenge(self, name: str, date: str, description: str = '', **keyvalues) -> None:
        """Add a challenge to the dictionary."""
        if self.check_date(date): # and self.check_keys(keyvalues):
            self.chronology[Key.CHALLENGES].update({name : {
                Key.DATE : self.format_date(date),
                Key.DESCRIPTION : description,
            }})
            self.chronology[Key.CHALLENGES][name].update(keyvalues)
            print(Msg.ADDED.format(String.CHALLENGE, self.chronology[Key.CHALLENGES][name]))
            


    def remove_challenge(self, challengename: str) -> None:
        """Remove a challenge from the dictionary."""
        self.remove_key(Key.CHALLENGES, challengename)


    ###### COMMENTS 

    def comments(self) -> pd.DataFrame:
        """Display a numbered list of comments."""
        lengthlist: int = len(self.chronology[Key.OVERVIEW][Key.COMMENTS])
        if lengthlist == 0:
            print(Msg.NO_COMMENTS.format(self.name))
        else:
            return pd.DataFrame.from_dict(self.chronology[Key.OVERVIEW][Key.COMMENTS], orient='index')


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
            how_many_comments: str = str(len(self.chronology[Key.OVERVIEW][Key.COMMENTS]) + 1)
            self.chronology[Key.OVERVIEW][Key.COMMENTS].update({how_many_comments : {
                Key.MESSAGE : i.strip(),
                Key.USER : self.user,
                Key.TIMESTAMP : timestamp,
            }})
        print(Msg.ADDED_COMMENT.format(text))


    def remove_comment(self, *index) -> None:
        """Remove a comment from the chronology by specifying its number in the comments list."""
        for idx in index:
            if str(idx) not in self.chronology[Key.OVERVIEW][Key.COMMENTS].keys():
                print(Msg.OUT_OF_RANGE.format(str(idx)))
            else:
                removed_comment = self.chronology[Key.OVERVIEW][Key.COMMENTS][str(idx)][Key.MESSAGE]
                self.chronology[Key.OVERVIEW][Key.COMMENTS].pop(str(idx))
                comments: list[dict[str, str, str]] = []
                for i in self.chronology[Key.OVERVIEW][Key.COMMENTS]:
                    comments.append(self.chronology[Key.OVERVIEW][Key.COMMENTS][i])
                self.remove_all_comments(show_message=False)
                for i in range(1, len(comments) + 1):
                    self.chronology[Key.OVERVIEW][Key.COMMENTS].update({str(i) : comments[i-1]})
                print(Msg.COMMENT_REMOVED.format(str(idx), removed_comment))
        

    def remove_all_comments(self, show_message: bool = True) -> None:
        """Remove all comments from the chronology."""
        keylist: list[str] = [key for key in self.chronology[Key.OVERVIEW][Key.COMMENTS]]
        for key in keylist:
            self.chronology[Key.OVERVIEW][Key.COMMENTS].pop(key)
        if show_message:
            print(Msg.ALL_COMMENTS_REMOVED.format(self.chronologyname))


    ###### DICTIONARIES

    def reserved_keys(self) -> pd.DataFrame:
        """Display the KEYS constants."""
        return pd.DataFrame(data=Key.keylist, columns=['Reserved Keys']) 
    
    def check_keys(self, keyvalues: dict[str, str] | dict[str, dict]) -> bool:
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
                 as_pandas: bool = False) -> None:
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
                        print('{}: {}'.format(key, String.LEFT_BRACE))
                        for subkey in dictionary[key]:
                            print('{}{}: {}'.format(tab, subkey, dictionary[key][subkey]))
                        print(String.RIGHT_BRACE)
                    else:
                        print('{}: {}'.format(key, dictionary[key]))
                else:
                    print('{}: {}'.format(key, dictionary[key]))

    def dictionaries(self, tab: str = '    ', dictname: str = '') -> None:
        for key in self.chronology.keys():
            if isinstance(self.chronology[key], dict):
                if len(self.chronology[key]) > 0:
                    print('{}: {}'.format(key, String.LEFT_BRACE))
                    for subkey in self.chronology[key]:
                        if subkey == Key.COMMENTS and len(self.chronology[key][subkey]) > 0:
                            print('{}{}: {}'.format(tab, subkey, String.LEFT_BRACE))
                            for subsubkey in self.chronology[key][subkey]:
                                print('{}{}{}: {}'.format(tab, tab, subsubkey, self.chronology[key][subkey][subsubkey]))
                            print('{}{}'.format(tab,String.RIGHT_BRACE))
                        else:
                            print('{}{}: {}'.format(tab, subkey, self.chronology[key][subkey]))
                    print(String.RIGHT_BRACE)
                else:
                    print('{}: {}'.format(key, self.chronology[key]))
            else:
                print('{}: {}'.format(key, self.chronology[key]))


    def dictionary_pop(self, dictname: str, pops: list[str]) -> pd.DataFrame:
        """Display the dictionary except for specified keys.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the dictionary.
        dictname: str
            The name of the dictionary to display.
            
        """
        dictionary: dict = copy.deepcopy(dict(self.chronology[dictname]))
        for i in pops:
            for j in dictionary:
                try:
                    dictionary[j].pop(i)
                except KeyError:
                    break
        return pd.DataFrame.from_dict(dictionary, orient='index')
    

    def show_dictionary(self, dictname: str) -> pd.DataFrame:
        if len(self.chronology[dictname]) > 0:
            return pd.DataFrame.from_dict(self.chronology[dictname], orient='index')
        else:
            print(Msg.NO_DICT_NAME.format(self.name, dictname.lower()))
            
    
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


    def events_pop(self, pops: list[str]) -> None:
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
            **keyvalues
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


    def markers_pop(self, pops: list[str]) -> None:
        """Display the markers defined for the chronology if there are any.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the markers.
            
        """
        return self.dictionary_pop(Key.MARKERS, pops)
    

    def add_marker(self, name: str, date: str, description: str = '', **keyvalues) -> None:
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


    def periods_pop(self, pops: list) -> None:
        """Display the periods defined for the chronology except for specified keys.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the periods.
            
        """
        return self.dictionary_pop(Key.PERIODS, pops)

    
    def add_period(self, name: str, begin: str, end: str, **keyvalues) -> None:
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

    def save(self, file: str) -> None:
        with open(file, 'w') as f:
            for key, value in self.chronology.items():
                if isinstance(value, dict):
                    f.write("{'%s': %s}\n" % (key, value))
                else:
                    f.write("{'%s': '%s'}\n" % (key, value))
            f.close()


    def save_as_json(self, filename: str) -> None:
        with open(filename, 'w') as file:
            json.dump(self.chronology, file, indent=4)


    def save_as_html(self) -> None:
        pass


    def save_as_pdf(self) -> None:
        pass

    
    ###### TEXTS 

    def texts(self) -> pd.DataFrame:
        """Display the texts referenced to justify a chronology."""
        return self.show_dictionary(Key.TEXTS)


    def texts_pop(self, pops: list) -> None:
        """Display the texts defined for the chronology except for specified keys.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the texts.
            
        """
        return self.dictionary_pop(Key.TEXTS, pops)


    def add_text(self, name: str, date: str, description: str = '', **keyvalues) -> None:
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
        