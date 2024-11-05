"""------------------------------------------------------------------------------
                            Chronology Sysout Tests
------------------------------------------------------------------------------"""

import sys  
import os 
import pytest

from chronodata.chronology import Chronology
from chronodata.utils.constants import String, Number, Msg, Datetime, Key, Calendar

"""------------------------------------------------------------------------------
                            Msg.BAD_DATE
------------------------------------------------------------------------------"""

def test_baddate(capsys):
    date = '200x'
    a = Chronology('testname')
    a.add_event('eventname', date)
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.BAD_DATE.format(date),'\n'])

"""------------------------------------------------------------------------------
                            Msg.BAD_LABEL
------------------------------------------------------------------------------"""

def test_badlabel(capsys):
    a = Chronology('testname')
    date = '2000 Ax'
    a.enable_strict_labels()
    a.check_date(date)
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.BAD_LABEL.format(date, ' Ax', Calendar.system[a.calendar][Key.value['POSLABEL']], Calendar.system[a.calendar][Key.value['NEGLABEL']], a.calendar),'\n'])

"""------------------------------------------------------------------------------
                            Msg.BOTH_NAME_FILE
------------------------------------------------------------------------------"""

def test_bothnamefile(capsys):
    a = Chronology(chronologyname='chronname', filename='filename')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.BOTH_NAME_FILE.format('chronname', 'filename'), '\n'])

"""------------------------------------------------------------------------------
                            Msg.CALENDARS_DONT_MATCH
------------------------------------------------------------------------------"""

def test_calendarsdontmatch(capsys):
    a = Chronology('one')
    b = Chronology('two', calendar='Secular')
    a.combine(b.name, b.chronology)
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.CALENDARS_DONT_MATCH.format(Key.value['GREGORIAN'], Key.value['SECULAR']), '\n'])

"""------------------------------------------------------------------------------
                            Msg.CHANGED
------------------------------------------------------------------------------"""

def test_changed(capsys):
    a = Chronology('one')
    a.to(Calendar.system[Key.value['SECULAR']][Key.value['NAME']])
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.CHANGED.format(Calendar.system[Key.value['SECULAR']][Key.value['NAME']]), '\n'])

"""------------------------------------------------------------------------------
                            Msg.HAS_CALENDAR
------------------------------------------------------------------------------"""

def test_hascalendar(capsys):
    a = Chronology('one')
    a.to(a.calendar)
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.HAS_CALENDAR.format(a.calendar), '\n'])

"""------------------------------------------------------------------------------
                            Msg.KEY_REMOVED
------------------------------------------------------------------------------"""

def test_keyremoved(capsys):
    a = Chronology('one')
    a.add_event('event', '2000 AD', keyvalues={'yes' : 'now', 'no' : 'my'})
    a.remove_event('event')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.KEY_REMOVED.format('event', 'EVENTS'), '\n'])

"""------------------------------------------------------------------------------
                            Msg.MISSING_NAME
------------------------------------------------------------------------------"""

def test_missingname(capsys):
    a = Chronology()
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.MISSING_NAME, '\n'])

"""------------------------------------------------------------------------------
                            Msg.NO_COMMENTS
------------------------------------------------------------------------------"""

def test_nocomments(capsys):
    a = Chronology('one')
    a.comments()
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.NO_COMMENTS.format(a.name), '\n'])

"""------------------------------------------------------------------------------
                            Msg.NO_DICT_NAME
------------------------------------------------------------------------------"""

def test_nodictname(capsys):
    a = Chronology('none')
    a.show_dictionary('EVENTS')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.NO_DICT_NAME.format(a.name, 'events'), '\n'])

"""------------------------------------------------------------------------------
                            Msg.NOT_IN_DICT
------------------------------------------------------------------------------"""

def test_notindict(capsys):
    a = Chronology('one')
    a.remove_event('happy')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.NOT_IN_DICT.format('happy', 'EVENTS'), '\n'])

"""------------------------------------------------------------------------------
                           Msg.NOT_REMOVABLE
------------------------------------------------------------------------------"""

def test_notremovable(capsys):
    a = Chronology('one')
    a.remove_key('EVENTS', 'DATE')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.NOT_REMOVABLE.format('DATE'), '\n'])

"""------------------------------------------------------------------------------
                            Msg.OUT_OF_RANGE
------------------------------------------------------------------------------"""

def test_outofrange(capsys):
    a = Chronology('one')
    a.remove_comment(3)
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.OUT_OF_RANGE.format(str(0)), '\n'])

"""------------------------------------------------------------------------------
                            Msg.RENAME
------------------------------------------------------------------------------"""

def test_rename(capsys):  
    a = Chronology('one')
    a.rename('two')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.RENAME.format('two'), '\n'])

"""------------------------------------------------------------------------------
                            Msg.RESERVED
------------------------------------------------------------------------------"""

def test_reserved(capsys):
    a = Chronology('one')
    a.check_keys({'DATE' : '2001 AD'})
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.RESERVED.format('DATE'), '\n'])





