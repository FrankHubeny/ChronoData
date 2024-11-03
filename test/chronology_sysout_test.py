"""------------------------------------------------------------------------------
                            Chronology Sysout Tests
------------------------------------------------------------------------------"""

import sys  
import os 
import pytest

from chronodata.chronology import Chronology, KEYS, CALENDARS, CONSTANTS, DATETIMES

def test_badlabel(capsys):
    date = '2000'
    a = Chronology('testname')
    a.add_event('eventname', date)
    captured = capsys.readouterr()  
    assert captured.out == ''.join([a.MSG['badlabel'].format(date, '000', CALENDARS[a.calendar][KEYS['POSLABEL']], CALENDARS[a.calendar][KEYS['NEGLABEL']], a.calendar),'\n'])

def test_bothnamefile(capsys):
    a = Chronology(chronologyname='chronname', filename='filename')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([a.MSG['bothnamefile'].format('chronname', 'filename'), '\n'])

def test_calendarsdontmatch(capsys):
    a = Chronology('one')
    b = Chronology('two', calendar='Secular')
    a.combine(b.name, b.chronology)
    captured = capsys.readouterr()  
    assert captured.out == ''.join([a.MSG['calendarsdontmatch'].format(KEYS['GREGORIAN'], KEYS['SECULAR']), '\n'])

def test_changed(capsys):
    a = Chronology('one')
    a.to(CALENDARS[KEYS['SECULAR']][KEYS['NAME']])
    captured = capsys.readouterr()  
    assert captured.out == ''.join([a.MSG['changed'].format(CALENDARS[KEYS['SECULAR']][KEYS['NAME']]), '\n'])

def test_hascalendar(capsys):
    a = Chronology('one')
    a.to(a.calendar)
    captured = capsys.readouterr()  
    assert captured.out == ''.join([a.MSG['hascalendar'].format(a.calendar), '\n'])

def test_keyremoved(capsys):
    a = Chronology('one')
    a.add_event('event', '2000 AD', keyvalues={'yes' : 'now', 'no' : 'my'})
    a.remove_event('event')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([a.MSG['keyremoved'].format('event', 'EVENTS'), '\n'])

def test_missingname(capsys):
    a = Chronology()
    captured = capsys.readouterr()  
    assert captured.out == ''.join([a.MSG['missingname'], '\n'])

def test_nocomments(capsys):
    a = Chronology('one')
    a.comments()
    captured = capsys.readouterr()  
    assert captured.out == ''.join([a.MSG['nocomments'].format(a.name), '\n'])

def test_nodictname(capsys):
    a = Chronology('none')
    a.show_dictionary('EVENTS')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([a.MSG['nodictname'].format(a.name, 'events'), '\n'])

def test_notindict(capsys):
    a = Chronology('one')
    a.remove_event('happy')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([a.MSG['notindict'].format('happy', 'EVENTS'), '\n'])

def test_notremovable(capsys):
    a = Chronology('one')
    a.remove_key('EVENTS', 'DATE')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([a.MSG['notremovable'].format('DATE'), '\n'])

def test_outofrange(capsys):
    a = Chronology('one')
    a.remove_comment(3)
    captured = capsys.readouterr()  
    assert captured.out == ''.join([a.MSG['outofrange'].format(str(0)), '\n'])

def test_rename(capsys):  
    a = Chronology('one')
    a.rename('two')
    captured = capsys.readouterr()  
    assert captured.out == ''.join([a.MSG['rename'].format('two'), '\n'])

def test_reserved(capsys):
    a = Chronology('one')
    a.check_keys({'DATE' : '2001 AD'})
    captured = capsys.readouterr()  
    assert captured.out == ''.join([a.MSG['reserved'].format('DATE'), '\n'])





