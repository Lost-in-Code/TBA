__author__ = 'Atle'
import sqlite3

def db_get_conn():
    return sqlite3.connect('database.db')

def db_close_conn(conn):
    conn.commit()
    conn.close()

def create_db():
    conn = db_get_conn()
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS games''')
    c.execute('''DROP TABLE IF EXISTS players''')
    c.execute('''CREATE TABLE players
                (room_id, nick, role)''')
    c.execute(''' CREATE TABLE games
                (room_id)''')
    db_close_conn(conn)


def db_insert_game(room_id):
    conn = db_get_conn()
    c = conn.cursor()
    c.execute('''SELECT * FROM games WHERE room_id = ?''', [room_id])
    if c.fetchone() is None:
        c.execute('''INSERT INTO games VALUES (?)''', [room_id])
        db_close_conn(conn)
        return True
    db_close_conn(conn)
    return False

