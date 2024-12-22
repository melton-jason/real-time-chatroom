import os
import sqlite3
import bcrypt

from settings import read_settings


def setup_DB_connection(connection_path=None):
    settings = read_settings()
    connection_path = settings['DB_PATH'] if connection_path is None else connection_path
    abs_path = os.path.abspath(connection_path)
    conn = sqlite3.connect(abs_path)
    cur = conn.cursor()
    with open(os.path.abspath(settings['DB_SETUP']), 'r') as setup_script:
        setup_sql = setup_script.read()
    cur.executescript(setup_sql)
    conn.commit()
    conn.close()
    return conn


def get_DB_connection(connection_path=None):
    settings = read_settings()
    connection_path = settings['DB_PATH'] if connection_path is None else connection_path
    conn = sqlite3.connect(os.path.abspath(connection_path))
    return conn


def hash_password(password: str, salt=None):
    salt = bcrypt.gensalt() if salt is None else salt
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed, salt
