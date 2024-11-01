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


__all__ = [
    'Chronology',
    'Compare',
]

CONSTANTS = {
    'DATETIME_EPOCH': 1970,
    'COMMENT' : '#',
    'LEFTBRACE' : '{',
    'NEGATIVE' : '-',
    'NEWLINE' : '\n',
    'SPACE' : ' ',
}


KEYS = {
    'ACTORS' : 'ACTORS',
    'BEFOREPRESENT' : 'Before Present',
    'BEGIN' : 'BEGIN',
    'BIRTH' : 'BIRTH',
    'CALENDAR' : 'CALENDAR',
    'CHALLENGES' : 'CHALLENGES',
    'DATE' : 'DATE',
    'DEATH' : 'DEATH',
    'DESCRIPTION' : 'DESCRIPTION',
    'END' : 'END',
    'EVENTS' : 'EVENTS',
    'EXPERIMENT' : 'Experiment',
    'FATHER' : 'FATHER',
    'FEMALE' : 'FEMALE',
    'FILE' : 'FILENAME',
    'GREGORIAN' : 'Gregorian',
    'MALE' : 'MALE',
    'MARKERS' : 'MARKERS',
    'MOTHER' : 'MOTHER',
    'NAME' : 'NAME',
    'NEGLABEL' : 'NEG LABEL',
    'PERIODS' : 'PERIODS',
    'POSLABEL' : 'POS LABEL',
    'SECULAR' : 'Secular',
    'TEXTS' : 'TEXTS',
    'USEZERO' : 'USE ZERO',
    'ZEROYEAR' : 'ZERO YEAR',
}

CALENDARS = {
    'Before Present' : {
        'NAME' : 'Before Present',
        'POS LABEL' : '',
        'NEG LABEL' : ' BP',
        'ZERO YEAR' : -CONSTANTS['DATETIME_EPOCH'],
        'USE ZERO' : False,
    },
    'Experiment' : {
        'NAME' : 'Experiment',
        'POS LABEL' : '',
        'NEG LABEL' : '',
        'Zero Year' : -CONSTANTS['DATETIME_EPOCH'],
        'USE ZERO' : False,
    },
    'Gregorian' : {
        'NAME' : 'Gregorian',
        'POS LABEL' : ' AD',
        'NEG LABEL' : ' BC',
        'ZERO YEAR' : -CONSTANTS['DATETIME_EPOCH'],
        'USE ZERO' : False,
    },
    'Secular' : {
        'NAME' : 'Secular',
        'POS LABEL' : ' CE',
        'NEG LABEL' : ' BCE',
        'ZERO YEAR' : -CONSTANTS['DATETIME_EPOCH'],
        'USE ZERO' : False,
    },
}


# Date and time units from https://numpy.org/doc/stable/reference/arrays.datetime.html
DATETIMES = {
    'ATTOSECOND' : 'as',
    'DAY' : 'D',
    'FEMTOSECOND' : 'fs',
    'HOUR' : 'h',
    'MICROSECOND' : 'us',
    'MILLISECOND' : 'ms',
    'MINUTE' : 'm',
    'MONTH' : 'M',
    'NANOSECOND' : 'ns',
    'PICOSECOND' : 'ps',
    'SECOND' : 's',
    'WEEK' : 'W',
    'YEAR' : 'Y',
}


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

    def __init__(self,
                 chronologyname: str = '',
                 filename: str = '',
                 calendar: str = 'Gregorian'):
        if chronologyname == '' and filename == '':
            raise ValueError('The chronology has neither a name nor a file to load.')
        if chronologyname != '' and filename != '':
            raise ValueError(f'Both a chronology name "{chronologyname}" and a filename "{filename}" have been specified, but only one can be used.')
        self.commentlist = []
        self.filename = filename
        self.maindictionaries = [
            KEYS['ACTORS'], 
            KEYS['CHALLENGES'], 
            KEYS['EVENTS'], 
            KEYS['MARKERS'],
            KEYS['PERIODS'], 
            KEYS['TEXTS'], 
        ]
        if chronologyname != '':
            self.chronology = {
                KEYS['NAME'] : chronologyname,
                KEYS['ACTORS'] : {},
                KEYS['CALENDAR'] : {},
                KEYS['CHALLENGES'] : {},
                KEYS['EVENTS'] : {},
                KEYS['MARKERS'] : {},
                KEYS['PERIODS'] : {},
                KEYS['TEXTS'] : {},
            }
            
            self.chronology[KEYS['CALENDAR']].update(CALENDARS[calendar])
            self.name = self.chronology[KEYS['NAME']]
            self.calendar = self.chronology[KEYS['CALENDAR']][KEYS['NAME']]
            self.poslabel = CALENDARS[self.calendar][KEYS['POSLABEL']]
            self.poslabellen = len(CALENDARS[self.calendar][KEYS['POSLABEL']])
            self.neglabel = CALENDARS[self.calendar][KEYS['NEGLABEL']]
            self.neglabellen = len(CALENDARS[self.calendar][KEYS['NEGLABEL']])
        else:
            self.chronology = {}
            with open(filename) as file:
                for line in file:
                    if line[0] == CONSTANTS['LEFTBRACE']:
                        self.chronology.update(ast.literal_eval(line))
                    else:  
                        self.commentlist.append(line.replace(CONSTANTS['NEWLINE'], ''))
                        

    def show(self, tab: str = '    '):
        """Show the entire chronology of both comments and dictionaries."""
        self.comments()
        self.dictionaries(tab)

    def __str__(self):
        self.show()
        return ''
    
    def rename(self, newname: str):
        """Rename the chronology."""
        self.chronology.update({KEYS['NAME'] : newname})
        self.name = self.chronology[KEYS['NAME']]
        print(f'The chronology has been renamed "{self.name}".')

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

        newchron = Chronology(chronologyname=chronologyname, cal=self.calendar)
        if self.calendar == chronology[KEYS['CALENDAR']]:
            if keepcomments:
                newchron.comments.extend(self.comments)
            newchron.comments.extend(comments)
            for key in self.maindictionaries:
                newchron.chronology[key].update(self.chronology[key])
                newchron.chronology[key].update(chronology[key])
            return newchron
        else:
            raise ValueError(f'The calendars "{self.calendar}" and "{chronology[KEYS['CALENDAR']]}" do not match.')


    ###### ACTORS 

    def actors(self) -> pd.DataFrame:
        """Display the actors in a chronology."""
        return self.show_dictionary(KEYS['ACTORS'])


    def actors_pop(self, pops: list):
        """Display the actors defined for the chronology if there are any.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the actors.
            
        """
        return self.dictionary_pop(pops, KEYS['ACTORS'])


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
        for i in keyvalues.keys():
            if i in KEYS.keys():
                raise ValueError(f'The key "{i}" is a reserved key.')
        else:
            self.chronology[KEYS['ACTORS']].update({name : {
                KEYS['FATHER'] : father,
                KEYS['MOTHER'] : mother,
                KEYS['BIRTH'] : birth,
                KEYS['DEATH'] : death,
                KEYS['DESCRIPTION'] : description,
            }})
            if len(keyvalues) > 0:
                self.chronology[KEYS['ACTORS']][name].update(keyvalues)

    def remove_actor(self, actorname):
        """Remove an actor from the dictionary."""
        self.remove_key(KEYS['ACTORS'], actorname)


    ###### CALENDARS 

    def calendars(self) -> pd.DataFrame:
        """Display the CALENDARS constants."""
        return pd.DataFrame.from_dict(CALENDARS)

    def datetimes(self) -> pd.DataFrame:
        """Display the DATETIMES constants."""
        return pd.DataFrame.from_dict(DATETIMES, orient='index', columns=['Value'])
    
    def daysinyear(self, date:str|np.datetime64):
        """A procedure to count number of days in a Gregorian year given the year.
        
        Parameters
        ----------
        date: np.datetime64
            The date to find the number of days in the year
            
        Examples
        --------

        """
        if isinstance(date, str):
            year = np.datetime64(date,'Y').astype('int') + 1970
        else:
            year = date['Y'].astype('int') + 1970
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            return 366
        else:
            return 365


    def numericdate(self, date: str, unit: str = DATETIMES['YEAR']):
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
        if date[0] == CONSTANTS['NEGATIVE']:
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

    def stringdate(self, date: np.datetime64, unit: str = DATETIMES['YEAR']):
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
        for i in keyvalues.keys():
            if i in KEYS.keys():
                raise ValueError(f'The key "{i}" is a reserved key.')
        else:
            self.chronology[KEYS['PERIODS']].update({name : {
                KEYS['BEGIN'] : begin,
                KEYS['END'] : end,
            }})
            if len(keyvalues) > 0:
                self.chronology[KEYS['PERIODS']][name].update(keyvalues)

    def to(self, calendar: str):
        """Convert the calendar of the chronology to anther calendar.
        
        Parameter
        ---------
        calendar: str
            The key of the calendar to convert the current calendar to.
        """
        labelcalendars = [KEYS['GREGORIAN'], KEYS['SECULAR']]
        formercalendar = CALENDARS[self.calendar]
        poslabel = formercalendar[KEYS['POSLABEL']]
        poslabellen = -len(poslabel)
        newcalendar = CALENDARS[calendar]
        if CALENDARS[calendar][KEYS['NAME']] == self.calendar:
            print(f'The chronology already has the "{self.calendar}" calendar.')
        else:
            if calendar in labelcalendars and self.calendar in labelcalendars:
                self.chronology[KEYS['CALENDAR']].update(newcalendar)
                for i in self.chronology[KEYS['PERIODS']]:
                    for k in [KEYS['BEGIN'], KEYS['END']]:
                        if self.chronology[KEYS['PERIODS']][i][k][poslabellen:] == poslabel:
                            newvalue = self.chronology[KEYS['PERIODS']][i][k].replace(
                                formercalendar[KEYS['POSLABEL']], 
                                newcalendar[KEYS['POSLABEL']]
                            )
                        else:
                            newvalue = self.chronology[KEYS['PERIODS']][i][k].replace(
                                formercalendar[KEYS['NEGLABEL']], 
                                newcalendar[KEYS['NEGLABEL']]
                            )
                        self.chronology[KEYS['PERIODS']][i].update({k : newvalue})
                for i in self.chronology[KEYS['EVENTS']]:
                    for k in [KEYS['DATE']]:
                        if self.chronology[KEYS['EVENTS']][i][k][poslabellen:] == poslabel:
                            newvalue = self.chronology[KEYS['EVENTS']][i][k].replace(
                                formercalendar[KEYS['POSLABEL']], 
                                newcalendar[KEYS['POSLABEL']]
                            )
                        else:
                            newvalue = self.chronology[KEYS['EVENTS']][i][k].replace(
                                formercalendar[KEYS['NEGLABEL']], 
                                newcalendar[KEYS['NEGLABEL']]
                            )
                        self.chronology[KEYS['EVENTS']][i].update({k : newvalue})
            self.calendar = self.chronology[KEYS['CALENDAR']][KEYS['NAME']]
            self.poslabel = CALENDARS[self.calendar][KEYS['POSLABEL']]
            self.poslabellen = len(CALENDARS[self.calendar][KEYS['POSLABEL']])
            self.neglabel = CALENDARS[self.calendar][KEYS['NEGLABEL']]
            self.neglabellen = len(CALENDARS[self.calendar][KEYS['NEGLABEL']])
            print(f'The chronology has been changed to the "{self.calendar}" calendar.')

    ###### CHALLENGES 

    def challenges(self) -> pd.DataFrame:
        """Display the challenges in a chronology."""
        return self.show_dictionary(KEYS['CHALLENGES'])


    def challenges_pop(self, pops: list) -> pd.DataFrame:
        """Display the challenges defined for the chronology if there are any.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the periods.
            
        """
        return self.dictionary_pop(pops, KEYS['CHALLENGES'])


    def add_challenge(self, name: str, date: str, description: str = '', keyvalues: dict = {}):
        """Add a challenge to the dictionary."""
        for i in keyvalues.keys():
            if i in KEYS.keys():
                raise ValueError(f'The key "{i}" is a reserved key.')
        else:
            self.chronology[KEYS['CHALLENGES']].update({name : {
                KEYS['DATE'] : date,
                KEYS['DESCRIPTION'] : description,
            }})
            if len(keyvalues) > 0:
                self.chronology[KEYS['CHALLENGES']][name].update(keyvalues)

    def remove_challenge(self, challengename):
        """Remove a challenge from the dictionary."""
        self.remove_key(KEYS['CHALLENGES'], challengename)


    ###### COMMENTS 

    def comments(self):
        """Display a numbered list of comments."""
        listlen = len(self.commentlist)
        if listlen == 0:
            print(f'There are no comments for the {self.name} chronology.')
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
            self.commentlist.append(CONSTANTS['SPACE'])
        else:
            texts = text.split(CONSTANTS['NEWLINE'])
            for i in texts:
                self.commentlist.append(i.replace(CONSTANTS['NEWLINE'], ''))


    def remove_comment(self, index: int):
        """Remove a comment from the chronology by specifying its number in the comments list."""
        if index >= len(self.commentlist):
            print(f'There are only {len(self.commentlist)} comments in the list. The index starts at 0.')
        else:
            self.commentlist.pop(index)

    def remove_all_comments(self):
        """Remove all comments from the chronology."""
        self.commentlist = []

    ###### DICTIONARIES

    def keys(self) -> pd.DataFrame:
        """Display the KEYS constants."""
        return pd.DataFrame.from_dict(KEYS, orient='index', columns=['Value'])
    

    def dictionaries(self, tab: str = '    '):
        for key in self.chronology.keys():
            if isinstance(self.chronology[key], dict):
                if len(self.chronology[key]) > 0:
                    print('{} : {}'.format(key, '{'))
                    for subkey in self.chronology[key]:
                        print('{}{} : {}'.format(tab, subkey, self.chronology[key][subkey]))
                    print('}')
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
            print(f'The chronology "{self.name}" has no {dictname.lower()}.')
    
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
        if key in KEYS.keys():
            print(f'The name "{key}" is a reserved key and cannot be removed.')
        elif key not in self.chronology[dictname].keys():
            print(f'The name "{key}" is not in the chronology dictionary "{dictname}".')
        else:
            self.chronology[dictname].pop(key)
            print(f'The name "{key}" has been removed from the "{dictname}" dictionary.')


    ###### EVENTS 

    def events(self):
        """Display the EVENTS dictionary."""
        return self.show_dictionary(KEYS['EVENTS'])


    def events_pop(self, pops: list) -> pd.DataFrame:
        """Display the events defined for the chronology without some of the keys.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the events.
            
        """
        return self.dictionary_pop(KEYS['EVENTS'], pops)
    
    
    def add_event(
            self, 
            name: str, 
            date: str, 
            description: str = '', 
            keyvalues: dict = {}
        ):
        """Add an event to the dictionary."""
        for i in keyvalues.keys():
            if i in KEYS.keys():
                raise ValueError(f'The key "{i}" is a reserved key.')
        else:
            self.chronology[KEYS['EVENTS']].update({name : {
                KEYS['DATE'] : date,
                KEYS['DESCRIPTION'] : description,
            }})
            if len(keyvalues) > 0:
                self.chronology[KEYS['EVENTS']][name].update(keyvalues)

    def remove_event(self, eventname):
        """Remove an event from the dictionary."""
        self.remove_key(KEYS['EVENTS'], eventname)

        
    ###### MARKERS 

    def markers(self) -> pd.DataFrame:
        """Display the markers in a chronology."""
        return self.show_dictionary(KEYS['MARKERS'])


    def markers_pop(self, pops: list) -> pd.DataFrame:
        """Display the markers defined for the chronology if there are any.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the markers.
            
        """
        return self.dictionary_pop(KEYS['MARKERS'], pops)
    
    def add_marker(self, name: str, date: str, description: str = '', keyvalues: dict = {}):
        """Add a marker to the dictionary."""
        for i in keyvalues.keys():
            if i in KEYS.keys():
                raise ValueError(f'The key "{i}" is a reserved key.')
        else:
            self.chronology[KEYS['MARKERS']].update({name : {
                KEYS['DATE'] : date,
                KEYS['DESCRIPTION'] : description,
            }})
            if len(keyvalues) > 0:
                self.chronology[KEYS['MARKERS']][name].update(keyvalues)

    def remove_marker(self, markername):
        """Remove a marker from the dictionary."""
        self.remove_key(KEYS['MARKERS'], markername)

    ###### PERIODS 

    def periods(self) -> pd.DataFrame:
        """Display the periods defined for the chronology if there are any."""
        return self.show_dictionary(KEYS['PERIODS'])


    def periods_pop(self, pops: list) -> pd.DataFrame:
        """Display the periods defined for the chronology except for specified keys.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the periods.
            
        """
        return self.dictionary_pop(KEYS['PERIODS'], pops)

    
    def add_period(self, name: str, begin: str, end: str, keyvalues: dict = {}):
        """Add a period to the dictionary."""
        for i in keyvalues.keys():
            if i in KEYS.keys():
                print(f'The key "{i}" is a reserved key.')
        else:
            self.chronology[KEYS['PERIODS']].update({name : {
                KEYS['BEGIN'] : begin,
                KEYS['END'] : end,
            }})
            if len(keyvalues) > 0:
                self.chronology[KEYS['PERIODS']][name].update(keyvalues)

    def remove_period(self, periodname):
        """Remove a period from the dictionary."""
        self.remove_key(KEYS['PERIODS'], periodname)

    ###### SAVE 

    def save(self, filename: str = ''):
        if filename == '':
            if self.filename == '':
                raise ValueError(f'No file name has been provided.')
            else:
                file = self.filename
        else:
            file=filename
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
        return self.show_dictionary(KEYS['TEXTS'])


    def texts_pop(self, pops: list) -> pd.DataFrame:
        """Display the texts defined for the chronology except for specified keys.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the texts.
            
        """
        return self.dictionary_pop(KEYS['TEXTS'], pops)

    def add_text(self, name: str, date: str, description: str = '', keyvalues: dict = {}):
        """Add an event to the dictionary."""
        for i in keyvalues.keys():
            if i in KEYS.keys():
                raise ValueError(f'The key "{i}" is a reserved key.')
        else:
            self.chronology[KEYS['TEXTS']].update({name : {
                KEYS['DATE'] : date,
                KEYS['DESCRIPTION'] : description,
            }})
            if len(keyvalues) > 0:
                self.chronology[KEYS['TEXTS']][name].update(keyvalues)

    def remove_text(self, textname):
        """Permanently remove a text from the dictionary."""
        self.remove_key(KEYS['TEXTS'], textname)




            
