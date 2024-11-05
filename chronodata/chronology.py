# Licensed under a 3-clause BSD style license - see LICENSE.md
"""This module provides procedures to create generic chronologies.
It also provides examples of chronologies of actual chronologies
from historical events around the world to processes either
hypothesized or observed in laboratory conditions.

The module also provides means of testing conflicting chronologies
using constraints that could lead one to falsify the
chronology unless the constraints are answered.
"""

import numpy as np
import pandas as pd
import ast
import copy

from chronodata.utils.constants import String, Number, Msg, Datetime, Key, Calendar

__all__ = ['Chronology', 'Compare',]

# CONSTANTS = {
#     'DATETIMEEPOCH': 1970,
#     'LEFTBRACE' : '{',
#     'NEGATIVE' : '-',
#     'NEWLINE' : '\n',
#     'RIGHTBRACE' : '}',
#     'SPACE' : ' ',
# }


# KEYS = {
#     'ACTORS' : 'ACTORS',
#     'BEFOREPRESENT' : 'Before Present',
#     'BEGIN' : 'BEGIN',
#     'BIRTH' : 'BIRTH',
#     'CALENDAR' : 'CALENDAR',
#     'CHALLENGES' : 'CHALLENGES',
#     'DATE' : 'DATE',
#     'DEATH' : 'DEATH',
#     'DESCRIPTION' : 'DESCRIPTION',
#     'END' : 'END',
#     'EVENTS' : 'EVENTS',
#     'EXPERIMENT' : 'Experiment',
#     'FATHER' : 'FATHER',
#     'FEMALE' : 'FEMALE',
#     'FILE' : 'FILENAME',
#     'GREGORIAN' : 'Gregorian',
#     'LABELS' : 'LABELS',
#     'MALE' : 'MALE',
#     'MARKERS' : 'MARKERS',
#     'MOTHER' : 'MOTHER',
#     'NAME' : 'NAME',
#     'NEGLABEL' : 'NEG LABEL',
#     'OVERVIEW' : 'OVERVIEW',
#     'PERIODS' : 'PERIODS',
#     'POSLABEL' : 'POS LABEL',
#     'SECULAR' : 'Secular',
#     'TEXTS' : 'TEXTS',
#     'USEZERO' : 'USE ZERO',
#     'ZEROYEAR' : 'ZERO YEAR',
# }

# CALENDARS = {
#     'Before Present' : {
#         'NAME' : 'Before Present',
#         'POS LABEL' : '',
#         'NEG LABEL' : ' BP',
#         'ZERO YEAR' : -CONSTANTS['DATETIMEEPOCH'],
#         'USE ZERO' : False,
#     },
#     'Experiment' : {
#         'NAME' : 'Experiment',
#         'POS LABEL' : '',
#         'NEG LABEL' : '',
#         'Zero Year' : -CONSTANTS['DATETIMEEPOCH'],
#         'USE ZERO' : False,
#     },
#     'Gregorian' : {
#         'NAME' : 'Gregorian',
#         'POS LABEL' : ' AD',
#         'NEG LABEL' : ' BC',
#         'ZERO YEAR' : -CONSTANTS['DATETIMEEPOCH'],
#         'USE ZERO' : False,
#     },
#     'Secular' : {
#         'NAME' : 'Secular',
#         'POS LABEL' : ' CE',
#         'NEG LABEL' : ' BCE',
#         'ZERO YEAR' : -CONSTANTS['DATETIMEEPOCH'],
#         'USE ZERO' : False,
#     },
# }


# # Date and time units from https://numpy.org/doc/stable/reference/arrays.datetime.html
# DATETIMES = {
#     'ATTOSECOND' : 'as',
#     'DAY' : 'D',
#     'FEMTOSECOND' : 'fs',
#     'HOUR' : 'h',
#     'MICROSECOND' : 'us',
#     'MILLISECOND' : 'ms',
#     'MINUTE' : 'm',
#     'MONTH' : 'M',
#     'NANOSECOND' : 'ns',
#     'PICOSECOND' : 'ps',
#     'SECOND' : 's',
#     'WEEK' : 'W',
#     'YEAR' : 'Y',
# }


class Compare():
    """Compare two or more chronologies for the same events.

    Routines
    --------

    See Also
    --------
    `Chronology`: The compared chronologies being were created or read
        from files using this class.  

    References
    ----------

    Examples
    --------
    The following example compares James Ussher's history of the world
    with a modern version of the older Byzantine church chronology.
    The challenges by each of these chronologies are used
    """

    def __init__(self, chronologies: list):
        self.chronologies = chronologies


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

    # MSG = {
    #     'baddate' : 'The value "{0}" for a date is not properly formatted.',
    #     'badlabel' : 'The date "{0}" contains an inappropriate label "{1}" rather than either "{2}" or "{3}" for the {4} calendar.',
    #     'bothnamefile' : 'Both a chronology name "{0}" and a filename "{1}" have been specified, but only one can be used.',
    #     'calendarsdontmatch' : 'The calendars "{0}" and "{1}" do not match.',
    #     'changed' : 'The chronology has been changed to the "{0}" calendar.',
    #     'countreserved' : '{0} reserved keys were used.',
    #     'hascalendar' : 'The chronology already has the "{0}" calendar.',
    #     'keyremoved' : 'The name "{0}" has been removed from the "{0}" dictionary.',
    #     'missingname' : 'The chronology has neither a name nor a file to load.',
    #     'nocomments' : 'There are no comments for the {0} chronology.',
    #     'nodictname' : 'The chronology "{0}" has no {1}.',
    #     'notindict' : 'The name "{0}" is not in the chronology dictionary "{1}".',
    #     'notremovable' : 'The name "{0}" is a reserved key and cannot be removed.', 
    #     'one' : 'One reserved key were used.',
    #     'outofrange' : 'There are only {0} comments in the list. The index starts at 0.',
    #     'rename' : 'The chronology has been renamed "{0}".',
    #     'reserved' : 'The key "{0}" is a reserved key.',
    # }

    def __init__(
            self,
            chronologyname: str = '',
            filename: str = '',
            calendar: str = 'Gregorian'
            #calendar: str = Calendar.system['Gregorian']
        ):
        if chronologyname == '' and filename == '':
            print(Msg.MISSING_NAME)
        elif chronologyname != '' and filename != '':
            print(Msg.BOTH_NAME_FILE.format(chronologyname, filename))   
        else:
            self.labelstrict = False
            self.commentlist = []
            self.filename = filename
            self.maindictionaries = [
                Key.value['ACTORS'], 
                Key.value['CHALLENGES'], 
                Key.value['EVENTS'], 
                Key.value['MARKERS'],
                Key.value['PERIODS'], 
                Key.value['TEXTS'], 
            ]
            if chronologyname != '':
                self.chronology = {
                    Key.value['OVERVIEW'] : {
                        Key.value['NAME'] : chronologyname,
                        Key.value['CALENDAR'] : {},
                        Key.value['LABELS'] : self.labelstrict,
                    },
                    Key.value['ACTORS'] : {},
                    Key.value['CHALLENGES'] : {},
                    Key.value['EVENTS'] : {},
                    Key.value['MARKERS'] : {},
                    Key.value['PERIODS'] : {},
                    Key.value['TEXTS'] : {},
                }
                
                self.chronology[Key.value['OVERVIEW']][Key.value['CALENDAR']].update(Calendar.system[calendar])
                self.name = self.chronology[Key.value['OVERVIEW']][Key.value['NAME']]
                self.calendar = self.chronology[Key.value['OVERVIEW']][Key.value['CALENDAR']][Key.value['NAME']]
                self.poslabel = Calendar.system[self.calendar][Key.value['POSLABEL']]
                self.poslabellen = len(Calendar.system[self.calendar][Key.value['POSLABEL']])
                self.neglabel = Calendar.system[self.calendar][Key.value['NEGLABEL']]
                self.neglabellen = len(Calendar.system[self.calendar][Key.value['NEGLABEL']])
            else:
                self.chronology = {}
                with open(filename) as file:
                    for line in file:
                        if line[0] == String.LEFT_BRACE:
                            self.chronology.update(ast.literal_eval(line))
                        else:  
                            self.commentlist.append(line.replace(String.NEWLINE, ''))
                        

    def show(self, tab: str = '    '):
        """Show the entire chronology of both comments and dictionaries."""
        self.comments()
        self.dictionaries(tab)

    def __str__(self):
        self.show()
        return ''
    
    def rename(self, newname: str):
        """Rename the chronology."""
        self.chronology[Key.value['OVERVIEW']].update({Key.value['NAME'] : newname})
        self.name = self.chronology[Key.value['OVERVIEW']][Key.value['NAME']]
        print(Msg.RENAME.format(self.name))

    def combine(self, chronologyname: str, chronology: dict, comments: list = [], keepcomments: bool = True):
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

        newchron = Chronology(chronologyname=chronologyname, calendar=self.calendar)
        if self.calendar == chronology[Key.value['OVERVIEW']][Key.value['CALENDAR']][Key.value['NAME']]:
            if keepcomments:
                newchron.comments.extend(self.comments)
            newchron.comments.extend(comments)
            for key in self.maindictionaries:
                newchron.chronology[key].update(self.chronology[key])
                newchron.chronology[key].update(chronology[key])
            return newchron
        else:
            print(Msg.CALENDARS_DONT_MATCH.format(self.calendar, chronology[Key.value['OVERVIEW']][Key.value['CALENDAR']][Key.value['NAME']]))


    ###### ACTORS 

    def actors(self) -> pd.DataFrame:
        """Display the actors in a chronology."""
        return self.show_dictionary(Key.value['ACTORS'])


    def actors_pop(self, pops: list):
        """Display the actors defined for the chronology if there are any.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the actors.
            
        """
        return self.dictionary_pop(pops, Key.value['ACTORS'])


    def add_actor(
            self, 
            name: str, 
            father: str = '', 
            mother: str = '', 
            birth: str = '', 
            death: str = '', 
            description: str = '', 
            keyvalues: dict = {}
        ):
        """Add an actor to the dictionary."""
        if self.check_date(birth) and self.check_date(death) and self.check_keys(keyvalues):
            self.chronology[Key.value['ACTORS']].update({name : {
                Key.value['FATHER'] : father,
                Key.value['MOTHER'] : mother,
                Key.value['BIRTH'] : self.format_date(birth),
                Key.value['DEATH'] : self.format_date(death),
                Key.value['DESCRIPTION'] : description,
            }})
            self.chronology[KEYS['ACTORS']][name].update(keyvalues)

    def remove_actor(self, actorname):
        """Remove an actor from the dictionary."""
        self.remove_key(Key.value['ACTORS'], actorname)


    ###### CALENDARS 

    def calendars(self) -> pd.DataFrame:
        """Display the CALENDARS constants."""
        return pd.DataFrame.from_dict(Calendar.system)
    

    def datetimes(self) -> pd.DataFrame:
        """Display the DATETIMES constants."""
        return pd.DataFrame.from_dict(Datetime.unit, orient='index', columns=['Value'])
    
    def enable_strict_labels(self):
        """Set strict formatting for dates."""
        self.labelstrict = True
        self.chronology[Key.value['OVERVIEW']].update({Key.value['LABELS'] : False})

    def disable_strict_labels(self):
        """Set relaxed formatting for dates."""
        self.labelstrict = False
        self.chronology[Key.value['OVERVIEW']].update({Key.value['LABELS'] : False})

    def check_date(self, date: str):
        cleandate = date.upper().strip()
        if cleandate[-self.neglabellen:] == self.neglabel:
            try:
                test = np.datetime64(cleandate[0:-self.neglabellen:])
            except ValueError:
                print(Msg.BAD_DATE.format(date))
                return False
            else:
                return True
        elif cleandate[-self.poslabellen:] == self.poslabel:
            try:
                test = np.datetime64(cleandate[0:-self.poslabellen:])
            except ValueError:
                print(Msg.BAD_DATE.format(date))
                return False
            else:
                return True
        elif not self.labelstrict:
            try:
                test = np.datetime64(cleandate)
            except ValueError:
                print(Msg.BAD_DATE.format(date))
                return False
            else:
                return True
        else:
            print(Msg.BAD_LABEL.format(date, date[-self.poslabellen:], self.poslabel, self.neglabel, self.calendar))
            return False

    def format_date(self, date: str):
        formatted_date = date.upper().strip()
        if self.labelstrict:
            try:
                test = np.datetime64(formatted_date)
            except ValueError:
                return formatted_date
            else: 
                return ''.join([formatted_date, self.poslabel])
        else:
            return formatted_date
        

    def to_datetime64(self, date: str):
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
    
    
    def date_diff(self, older: str, younger: str, unit: str = Datetime.unit['YEAR']):
        olderdate = np.datetime64(self.to_datetime64(older), unit)
        youngerdate = np.datetime64(self.to_datetime64(younger), unit)
        return float((youngerdate - olderdate) / np.timedelta64(1, unit))


    # def daysinyear(self, date:str|np.datetime64):
    #     """A procedure to count number of days in a Gregorian year given the year.
        
    #     Parameters
    #     ----------
    #     date: np.datetime64
    #         The date to find the number of days in the year
            
    #     Examples
    #     --------

    #     """
    #     if isinstance(date, str):
    #         year = np.datetime64(date,'Y').astype('int') + 1970
    #     else:
    #         year = date['Y'].astype('int') + 1970
    #     if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
    #         return 366
    #     else:
    #         return 365


    def numericdate(self, date: str, unit: str = Datetime.unit['YEAR']):
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
                numericdate = np.datetime64('-'+date[0:-self.neglabellen]) + np.timedelta64(days, 'D')
        elif date[-self.poslabellen:] == self.poslabel:
            numericdate = np.datetime64(date[0:-self.poslabellen])
        else:
            numericdate = np.datetime64(date)
        return numericdate

    def stringdate(self, date: np.datetime64, unit: str = Datetime.unit['YEAR']):
        """A procedure to convert a numeric date to a date labelled with an epoch label.
        
        Parameters
        ----------
        date: np.datetime64
            The numeric date to be converted to a string

        """
        if date is None:
            return ''
        else:
            return np.datetime_as_string(date, unit='D')

    
    def add_calendar(self, name: str, begin: str, end: str, keyvalues: dict = {}):
        """Add a calendar to the dictionary."""
        pass


    def to(self, calendar: str):
        """Convert the calendar of the chronology to anther calendar.
        
        Parameter
        ---------
        calendar: str
            The key of the calendar to convert the current calendar to.
        """
        name_key = Key.value['NAME']
        poslabel_key = Key.value['POSLABEL']
        neglabel_key = Key.value['NEGLABEL']
        period_key = Key.value['PERIODS']
        event_key = Key.value['EVENTS']
        labelcalendars = [Key.value['GREGORIAN'], Key.value['SECULAR']]
        formercalendar = Calendar.system[self.calendar]
        poslabel = formercalendar[poslabel_key]
        poslabellen = -len(poslabel)
        newcalendar = Calendar.system[calendar]
        if Calendar.system[calendar][name_key] == self.calendar:
            print(Msg.HAS_CALENDAR.format(self.calendar))
        else:
            if calendar in labelcalendars and self.calendar in labelcalendars:
                self.chronology[Key.value['OVERVIEW']][Key.value['CALENDAR']].update(newcalendar)
                for i in self.chronology[period_key]:
                    for k in [Key.value['BEGIN'], Key.value['END']]:
                        if self.chronology[period_key][i][k][poslabellen:] == poslabel:
                            newvalue = self.chronology[period_key][i][k].replace(
                                formercalendar[poslabel], 
                                newcalendar[poslabel]
                            )
                        else:
                            newvalue = self.chronology[period_key][i][k].replace(
                                formercalendar[neglabel_key], 
                                newcalendar[neglabel_key]
                            )
                        self.chronology[period_key][i].update({k : newvalue})
                for i in self.chronology[event_key]:
                    for k in [Key.value['DATE']]:
                        if self.chronology[event_key][i][k][poslabellen:] == poslabel:
                            newvalue = self.chronology[event_key][i][k].replace(
                                formercalendar[poslabel], 
                                newcalendar[poslabel]
                            )
                        else:
                            newvalue = self.chronology[event_key][i][k].replace(
                                formercalendar[neglabel_key], 
                                newcalendar[neglabel_key]
                            )
                        self.chronology[event_key][i].update({k : newvalue})
            self.calendar = self.chronology[Key.value['OVERVIEW']][Key.value['CALENDAR']][name_key]
            self.poslabel = Calendar.system[self.calendar][poslabel_key]
            self.poslabellen = len(Calendar.system[self.calendar][poslabel_key])
            self.neglabel = Calendar.system[self.calendar][neglabel_key]
            self.neglabellen = len(Calendar.system[self.calendar][neglabel_key])
            print(Msg.CHANGED.format(self.calendar))

    ###### CHALLENGES 

    def challenges(self) -> pd.DataFrame:
        """Display the challenges in a chronology."""
        return self.show_dictionary(Key.value['CHALLENGES'])


    def challenges_pop(self, pops: list) -> pd.DataFrame:
        """Display the challenges defined for the chronology if there are any.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the periods.
            
        """
        return self.dictionary_pop(pops, Key.value['CHALLENGES'])


    def add_challenge(self, name: str, date: str, description: str = '', keyvalues: dict = {}):
        """Add a challenge to the dictionary."""
        if self.check_date(date) and self.check_keys(keyvalues):
            self.chronology[Key.value['CHALLENGES']].update({name : {
                Key.value['DATE'] : self.format_date(date),
                Key.value['DESCRIPTION'] : description,
            }})
            self.chronology[Key.value['CHALLENGES']][name].update(keyvalues)

    def remove_challenge(self, challengename):
        """Remove a challenge from the dictionary."""
        self.remove_key(Key.value['CHALLENGES'], challengename)


    ###### COMMENTS 

    def comments(self):
        """Display a numbered list of comments."""
        listlen = len(self.commentlist)
        if listlen == 0:
            print(Msg.NO_COMMENTS.format(self.name))
        else:
            space = int(np.ceil(np.log10(listlen)))
            for i in range(0, len(self.commentlist)):
                print('{i:>{s}} : {c}'.format(i=str(i), c=self.commentlist[i], s=space))

    def add_comment(self, text: str = ''):
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
        
        if text == '':
            self.commentlist.append(String.SPACE)
        else:
            texts = text.split(String.NEWLINE)
            for i in texts:
                self.commentlist.append(i.replace(String.NEWLINE, ''))


    def remove_comment(self, index: int):
        """Remove a comment from the chronology by specifying its number in the comments list."""
        lengthlist = len(self.commentlist)
        if index >= lengthlist:
            print(Msg.OUT_OF_RANGE.format(lengthlist))
        else:
            self.commentlist.pop(index)

    def remove_all_comments(self):
        """Remove all comments from the chronology."""
        self.commentlist = []

    ###### DICTIONARIES

    def keys(self) -> pd.DataFrame:
        """Display the KEYS constants."""
        return pd.DataFrame.from_dict(Key, orient='index', columns=['Value'])
    
    def check_keys(self, keyvalues: dict):
        count = 0
        for i in keyvalues.keys():
            if i in Key.value.keys():
                print(Msg.RESERVED.format(i))
                count += 1
        if count > 0:
            return False
        else:
            return True

    def dictionaries(self, tab: str = '    '):
        for key in self.chronology.keys():
            if isinstance(self.chronology[key], dict):
                if len(self.chronology[key]) > 0:
                    print('{} : {}'.format(key, String.LEFT_BRACE))
                    for subkey in self.chronology[key]:
                        print('{}{} : {}'.format(tab, subkey, self.chronology[key][subkey]))
                    print(String.RIGHT_BRACE)
                else:
                    print('{} : {}'.format(key, self.chronology[key]))
            else:
                print('{} : {}'.format(key, self.chronology[key]))

    def dictionary_pop(self, dictname: str, pops: list):
        """Display the dictionary except for specified keys.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the dictionary.
        dictname: str
            The name of the dictionary to display.
            
        """
        dictionary = copy.deepcopy(dict(self.chronology[dictname]))
        for i in pops:
            for j in dictionary:
                try:
                    dictionary[j].pop(i)
                except KeyError:
                    break
        return pd.DataFrame.from_dict(dictionary, orient='index')
    
    def show_dictionary(self, dictname: str):
        if len(self.chronology[dictname]) > 0:
            return pd.DataFrame.from_dict(self.chronology[dictname], orient='index')
        else:
            print(Msg.NO_DICT_NAME.format(self.name, dictname.lower()))
            
    
    def remove_key(self, dictname: str, key: str):
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
        if key in Key.value.keys():
            print(Msg.NOT_REMOVABLE.format(key))
        elif key not in self.chronology[dictname].keys():
            print(Msg.NOT_IN_DICT.format(key, dictname))
        else:
            self.chronology[dictname].pop(key)
            print(Msg.KEY_REMOVED.format(key, dictname))


    ###### EVENTS 

    def events(self):
        """Display the EVENTS dictionary."""
        return self.show_dictionary(Key.value['EVENTS'])


    def events_pop(self, pops: list) -> pd.DataFrame:
        """Display the events defined for the chronology without some of the keys.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the events.
            
        """
        return self.dictionary_pop(Key.value['EVENTS'], pops)
    
    
    def add_event(
            self, 
            name: str, 
            date: str, 
            description: str = '', 
            keyvalues: dict = {}
        ):
        """Add an event to the dictionary."""
        if self.check_date(date) and self.check_keys(keyvalues):
            self.chronology[Key.value['EVENTS']].update({name : {
                Key.value['DATE'] : self.format_date(date),
                Key.value['DESCRIPTION'] : description,
            }})
            self.chronology[Key.value['EVENTS']][name].update(keyvalues)

    def remove_event(self, eventname):
        """Remove an event from the dictionary."""
        self.remove_key(Key.value['EVENTS'], eventname)

        
    ###### MARKERS 

    def markers(self) -> pd.DataFrame:
        """Display the markers in a chronology."""
        return self.show_dictionary(Key.value['MARKERS'])


    def markers_pop(self, pops: list) -> pd.DataFrame:
        """Display the markers defined for the chronology if there are any.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the markers.
            
        """
        return self.dictionary_pop(Key.value['MARKERS'], pops)
    
    def add_marker(self, name: str, date: str, description: str = '', keyvalues: dict = {}):
        """Add a marker to the dictionary."""
        if self.check_date(date) and self.check_keys(keyvalues):
            self.chronology[Key.value['MARKERS']].update({name : {
                Key.value['DATE'] : self.format_date(date),
                Key.value['DESCRIPTION'] : description,
            }})
            self.chronology[Key.value['MARKERS']][name].update(keyvalues)
        

    def remove_marker(self, markername):
        """Remove a marker from the dictionary."""
        self.remove_key(Key.value['MARKERS'], markername)

    ###### PERIODS 

    def periods(self) -> pd.DataFrame:
        """Display the periods defined for the chronology if there are any."""
        return self.show_dictionary(Key.value['PERIODS'])


    def periods_pop(self, pops: list) -> pd.DataFrame:
        """Display the periods defined for the chronology except for specified keys.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the periods.
            
        """
        return self.dictionary_pop(Key.value['PERIODS'], pops)

    
    def add_period(self, name: str, begin: str, end: str, keyvalues: dict = {}):
        """Add a period to the dictionary."""
        if self.check_date(begin) and self.check_date(end) and self.check_keys(keyvalues): 
            self.chronology[Key.value['PERIODS']].update({name : {
                Key.value['BEGIN'] : self.format_date(begin),
                Key.value['END'] : self.format_date(end),
            }})
            self.chronology[Key.value['PERIODS']][name].update(keyvalues)

    def remove_period(self, periodname):
        """Remove a period from the dictionary."""
        self.remove_key(Key.value['PERIODS'], periodname)

    ###### SAVE 

    def save(self, file: str):
        with open(file, 'w') as f:
            for i in self.commentlist:
                f.write('%s\n' % i)
            for key, value in self.chronology.items():
                if isinstance(value, dict):
                    f.write("{'%s' : %s}\n" % (key, value))
                else:
                    f.write("{'%s' : '%s'}\n" % (key, value))
            f.close()

    def save_as_json(self):
        pass

    def save_as_html(self):
        pass

    def save_as_pdf(self):
        pass

    
    ###### TEXTS 

    def texts(self) -> pd.DataFrame:
        """Display the texts referenced to justify a chronology."""
        return self.show_dictionary(Key.value['TEXTS'])


    def texts_pop(self, pops: list) -> pd.DataFrame:
        """Display the texts defined for the chronology except for specified keys.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the texts.
            
        """
        return self.dictionary_pop(Key.value['TEXTS'], pops)

    def add_text(self, name: str, date: str, description: str = '', keyvalues: dict = {}):
        """Add an event to the dictionary."""
        if self.check_date(date) and self.check_keys(keyvalues):
            self.chronology[Key.value['TEXTS']].update({name : {
                Key.value['DATE'] : self.format_date(date),
                Key.value['DESCRIPTION'] : description,
            }})
            self.chronology[Key.value['TEXTS']][name].update(keyvalues)

    def remove_text(self, textname):
        """Permanently remove a text from the dictionary."""
        self.remove_key(Key.value['TEXTS'], textname)
