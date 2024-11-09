"""------------------------------------------------------------------------------
                            Chronology Sysout Tests
------------------------------------------------------------------------------"""

import sys  
import os 
import pytest

from chronodata.chronology import Chronology
from chronodata.utils.constants import String, Number, Msg, Datetime, Key, Calendar

A = Chronology(user='Frank', chronologyname='testname')
B = Chronology(user='Frank', chronologyname='two', calendar='Secular')

"""------------------------------------------------------------------------------
                            Msg.ADDED
------------------------------------------------------------------------------"""

def test_actor_added(capsys):
    A.add_actor('actorname')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.ADDED.format(String.ACTOR, A.chronology[Key.ACTORS]['actorname']),'\n'])

def test_challenge_added(capsys):
    A.add_challenge('challengename', '2000 AD')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.ADDED.format(String.CHALLENGE, A.chronology[Key.CHALLENGES]['challengename']),'\n'])

def test_event_added(capsys):
    A.add_event('eventname', '2000 AD')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.ADDED.format(String.EVENT, A.chronology[Key.EVENTS]['eventname']),'\n'])

def test_marker_added(capsys):
    A.add_marker('markername', '2000 AD')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.ADDED.format(String.MARKER, A.chronology[Key.MARKERS]['markername']),'\n'])

def test_period_added(capsys):
    A.add_period('periodname', begin='2000 AD', end='2024 AD')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.ADDED.format(String.PERIOD, A.chronology[Key.PERIODS]['periodname']),'\n'])

def test_text_added(capsys):
    A.add_text('textname', '2000 AD')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.ADDED.format(String.TEXT, A.chronology[Key.TEXTS]['textname']),'\n'])


"""------------------------------------------------------------------------------
                            Msg.BAD_DATE
------------------------------------------------------------------------------"""

def test_baddate(capsys):
    date = '200x'
    A.add_event('baddate', date)
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.BAD_DATE.format(date, A.calendar),'\n'])

"""------------------------------------------------------------------------------
                            Msg.BAD_LABEL
------------------------------------------------------------------------------"""

def test_badlabel(capsys):
    date = '2000 Ax'
    A.enable_strict_labels()
    A.check_date(date)
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.BAD_LABEL.format(date, ' Ax', Calendar.system[A.calendar][Key.POSLABEL], Calendar.system[A.calendar][Key.NEGLABEL], A.calendar),'\n'])

"""------------------------------------------------------------------------------
                            Msg.BOTH_NAME_FILE
------------------------------------------------------------------------------"""

def test_bothnamefile(capsys):
    a = Chronology(user='Frank', chronologyname='chronname', filename='filename')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.BOTH_NAME_FILE.format('chronname', 'filename'), '\n'])

"""------------------------------------------------------------------------------
                            Msg.CALENDARS_DONT_MATCH
------------------------------------------------------------------------------"""

#def test_calendarsdontmatch(capsys):
#    A.combine('combinedname', B.chronology)
#    captured = capsys.readouterr()  
#    assert captured.out == ''.join([Msg.CALENDARS_DONT_MATCH.format(A.calendar, B.chronology[Key.OVERVIEW][Key.CALENDAR][Key.NAME]), '\n'])

"""------------------------------------------------------------------------------
                            Msg.CHANGED
------------------------------------------------------------------------------"""

def test_changed(capsys):
    A.to(Calendar.system[Key.SECULAR][Key.NAME])
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.CHANGED.format(Calendar.system[Key.SECULAR][Key.NAME]), '\n'])

"""------------------------------------------------------------------------------
                            Msg.HAS_CALENDAR
------------------------------------------------------------------------------"""

def test_hascalendar(capsys):
    A.to(A.calendar)
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.HAS_CALENDAR.format(A.calendar), '\n'])

"""------------------------------------------------------------------------------
                            Msg.KEY_REMOVED
------------------------------------------------------------------------------"""

def test_actor_removed(capsys):
    A.remove_actor('actorname')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.KEY_REMOVED.format('actorname', Key.ACTORS),'\n'])

def test_challenge_removed(capsys):
    A.remove_challenge('challengename')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.KEY_REMOVED.format('challengename', Key.CHALLENGES),'\n'])

def test_event_removed(capsys):
    A.remove_event('eventname')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.KEY_REMOVED.format('eventname', Key.EVENTS),'\n'])

def test_marker_removed(capsys):
    A.remove_marker('markername')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.KEY_REMOVED.format('markername', Key.MARKERS),'\n'])

def test_period_removed(capsys):
    A.remove_period('periodname')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.KEY_REMOVED.format('periodname', Key.PERIODS),'\n'])

def test_text_removed(capsys):
    A.remove_text('textname')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.KEY_REMOVED.format('textname', Key.TEXTS),'\n'])


"""------------------------------------------------------------------------------
                            Msg.MISSING_NAME
------------------------------------------------------------------------------"""

def test_missingname(capsys):
    a = Chronology(user='Frank' )
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.MISSING_NAME, '\n'])

"""------------------------------------------------------------------------------
                            Msg.NO_COMMENTS
------------------------------------------------------------------------------"""

def test_nocomments(capsys):
    A.comments()
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.NO_COMMENTS.format(A.name), '\n'])

"""------------------------------------------------------------------------------
                            Msg.NO_DICT_NAME
------------------------------------------------------------------------------"""

def test_nodictname(capsys):
    A.show_dictionary('EVENTS')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.NO_DICT_NAME.format(A.name, 'events'), '\n'])

"""------------------------------------------------------------------------------
                            Msg.NOT_IN_DICT
------------------------------------------------------------------------------"""

def test_notindict(capsys):
    A.remove_event('happy')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.NOT_IN_DICT.format('happy', 'EVENTS'), '\n'])

"""------------------------------------------------------------------------------
                           Msg.NOT_REMOVABLE
------------------------------------------------------------------------------"""

def test_notremovable(capsys):
    A.remove_key('EVENTS', 'DATE')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.NOT_REMOVABLE.format('DATE'), '\n'])

"""------------------------------------------------------------------------------
                            Msg.OUT_OF_RANGE
------------------------------------------------------------------------------"""

def test_outofrange(capsys):
    A.remove_comment(3)
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.OUT_OF_RANGE.format(str(3)), '\n'])

"""------------------------------------------------------------------------------
                            Msg.RENAME
------------------------------------------------------------------------------"""

def test_rename(capsys):  
    A.rename('two')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.RENAME.format('two'), '\n'])

"""------------------------------------------------------------------------------
                            Msg.RESERVED
------------------------------------------------------------------------------"""

def test_reserved(capsys):
    A.check_keys({'DATE' : '2001 AD'})
    captured = capsys.readouterr()  
    assert captured.out == ''.join([Msg.RESERVED.format('DATE'), '\n'])





