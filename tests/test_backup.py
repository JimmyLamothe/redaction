""" Tests for backup modulOAAe

Not all functions have tests written for them. Write missing tests if bugs arise.
"""

from datetime import date, timedelta
import backup

values = [
    date.today(), #0
    date.today() - timedelta(days=1), #1
    date.today() - timedelta(days=6), #2
    date.today() - timedelta(days=7), #3
    date.today() - timedelta(days=29), #4
    date.today() - timedelta(days=30), #5
    date.today() - timedelta(days=364), #6
    date.today() - timedelta(days=365), #7
    date.today() - timedelta(days=400), #8
    date.today() - timedelta(days=965) #9
]


def test_new_day(monkeypatch):
    monkeypatch.setitem(backup.backup_date_dict, 'day', values[0])
    assert backup.new_day() == False
    monkeypatch.setitem(backup.backup_date_dict, 'day', values[1])
    assert backup.new_day()
    monkeypatch.setitem(backup.backup_date_dict, 'day', values[7])
    assert backup.new_day()

def test_new_week(monkeypatch):
    monkeypatch.setitem(backup.backup_date_dict, 'week', values[0])
    assert backup.new_week() == False
    monkeypatch.setitem(backup.backup_date_dict, 'week', values[2])
    assert backup.new_week() == False
    monkeypatch.setitem(backup.backup_date_dict, 'week', values[3])
    assert backup.new_week()
    monkeypatch.setitem(backup.backup_date_dict, 'week', values[8])
    assert backup.new_week()

def test_new_month(monkeypatch):
    monkeypatch.setitem(backup.backup_date_dict, 'month', values[0])
    assert backup.new_month() == False
    monkeypatch.setitem(backup.backup_date_dict, 'month', values[3])
    assert backup.new_month() == False
    monkeypatch.setitem(backup.backup_date_dict, 'month', values[4])
    assert backup.new_month() == False
    monkeypatch.setitem(backup.backup_date_dict, 'month', values[5])
    assert backup.new_month()
    monkeypatch.setitem(backup.backup_date_dict, 'month', values[8])
    assert backup.new_month()

def test_new_year(monkeypatch):
    monkeypatch.setitem(backup.backup_date_dict, 'year', values[0])
    assert backup.new_year() == False
    monkeypatch.setitem(backup.backup_date_dict, 'year', values[3])
    assert backup.new_year() == False
    monkeypatch.setitem(backup.backup_date_dict, 'year', values[5])
    assert backup.new_year() == False
    monkeypatch.setitem(backup.backup_date_dict, 'year', values[6])
    assert backup.new_year() == False
    monkeypatch.setitem(backup.backup_date_dict, 'year', values[7])
    assert backup.new_year()
    monkeypatch.setitem(backup.backup_date_dict, 'year', values[9])
    assert backup.new_year()
