import random

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
                (room_id, nick, role, uid, ready)''')
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

def db_insert_player(room_id, nick, role):
    conn = db_get_conn()
    c = conn.cursor()
    c.execute('''SELECT * FROM players WHERE room_id = ? AND nick = ?''', [room_id, nick])
    row = c.fetchone()
    if row is None:
        uid = random.randint(10000,99999)
        while c.execute('''SELECT * FROM players WHERE uid = ?''', [uid]).fetchone() != None:
            uid = random.randint(10000, 99999)
        c.execute('''INSERT INTO players VALUES(?, ?, ?, ?)''', [room_id, nick, role, uid])
        db_close_conn(conn)
        return (True, uid)
    if row[2] == role:
        return (True, row[3])
    return (False, 0)

def db_set_ready(uid):
    conn = db_get_conn()
    c = conn.cursor()
    c.execute('''UPDATE players SET ready=1 WHERE uid=?''', [uid])
    if c.rowcount == 1: return True
    return False

def db_game_ready(uid):
    conn = db_get_conn()
    c = conn.cursor()
    c.execute('''SELECT room_id FROM players WHERE uid=?''', [uid])
    room_id = c.fetchone()
    c.execute('''SELECT count(*) FROM players WHERE room_id = ?''', [room_id])
    num_players = c.fetchone()
    c.execute('''SELECT count(*) FROM players WHERE room_id = ? AND ready = 1''', [room_id])
    num_players_ready = c.fetchone()
    if num_players_ready >= num_players / 2:
        return True
    return False

def db_get_status(uid):
    return "Urgh"

