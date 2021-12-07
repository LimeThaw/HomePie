import sqlite3
from sqlite3.dbapi2 import Error
from flask import g

def sqlite_connect(db_path):
    conn = getattr(g, '_sqlite', None)
    if conn is None:
        try:
            conn = g._sqlite = sqlite3.connect(db_path)
            return conn
        except Error as e:
            print(e)
    return conn

def sqlite_execute(conn, command):
    try:
        c = conn.cursor()
        c.execute(command)
        r = c.fetchall()
        print(r)
        return r
    except Error as e:
        print(e)

def sqlite_disconnect():
    conn = getattr(g, '_sqlite', None)
    if conn is not None:
        conn.commit()
        conn.close()