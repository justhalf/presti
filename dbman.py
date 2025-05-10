# -*- coding: utf-8 -*-
"""
Database manager for Presti
"""
from __future__ import print_function, division
__author__ = 'Aldrian Obaja Muis'
__date__ = '2025-05-10'

# Import statements
import sys
import os
from pathlib import Path
import sqlite3 as sql
import json
from dotenv import load_dotenv
load_dotenv()

DB_PATH = Path(os.environ['DB_PATH'])

def init_db():
    if not DB_PATH.exists():
        con = sql.connect(str(DB_PATH))
        cur = con.cursor()
        try:
            cur.execute('CREATE TABLE message(channel_id, timestamp, blob)')
        finally:
            cur.close()
            con.close()

def fetch(channel_id):
    con = sql.connect(str(DB_PATH))
    try:
        refresh(con)
        cur.execute('SELECT timestamp, blob FROM message WHERE channel_id = ?', (channel_id,))
        messages = cur.fetchall()
        result = []
        for message in messages:
            result.append({'channel_id':message[0], 'timestamp':message[1], 'data':json.loads(message[2])})
    finally:
        cur.close()
        con.close()
    return result

def insert(channel_id, timestamp, data):
    data = json.dumps(data)
    con = sql.connect(str(DB_PATH))
    try:
        refresh(con)
        cur.execute('INSERT INTO message (channel_id, timestamp, blob) VALUES (?, ?, ?)',
                    (channel_id, timestamp, data,))
        con.commit()
    except:
        return False
    finally:
        cur.close()
        con.close()
    return True

def refresh(con):
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM message WHERE timestamp < strftime('%s', 'now') - 3")
    finally:
        cur.close()
