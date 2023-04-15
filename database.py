from flask import g
import sqlite3

def connection():
    conn = sqlite3.connect('C:/Users/mirji/personal projects/emp_management_system/crudapp.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_database():
    if not hasattr(g, 'crudapp_db'):
        g.crudapp_db = connection()
    return g.crudapp_db