__author__ = 'Atle'
import sqlite3
import random
import logging

'''
    user state:
        1 - Waiting
            -> Ready -> 2
        2 - Countdown started
            -> Timer out -> 3
        3 - Round started
            -> Action -> 4
            -> Time out -> 4
        4 - Round end
            -> Monster not dead -> 3
            -> Monster dead -> 1

    game state
        0 - Init...
            -> > Half players ready ->
        1 - Ready countdown going

'''
def db_get_conn():
    return sqlite3.connect('database.db', timeout=15)

def db_setup_logging():
    logging.basicConfig(filename='tba.log',level=logging.INFO)

def db_close_conn(conn):
    conn.commit()
    conn.close()

def create_db():
    db_setup_logging()
    conn = db_get_conn()
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS games''')
    c.execute('''DROP TABLE IF EXISTS players''')
    c.execute('''CREATE TABLE players
                (room_id, nick, role, uid, ready, state, hp, mana, action)''')
    c.execute('''CREATE TABLE games
                (room_id, ready_countdown, state, round_countdown)''')
    c.execute('''CREATE TABLE bosses
                (room_id, name, hp)''')
    db_close_conn(conn)
    logging.info("Created DB")


def db_insert_game(room_id):
    db_setup_logging()
    conn = db_get_conn()
    c = conn.cursor()
    c.execute('''SELECT * FROM games WHERE room_id = ?''', [room_id])
    if c.fetchone() is None:
        c.execute('''INSERT INTO games VALUES (?, 0, 0, 0)''', [str(room_id)])
        db_close_conn(conn)
        logging.info("Created new room with ID: %s" % (room_id))
        return True
    db_close_conn(conn)
    return False

def db_insert_player(room_id, nick, role):
    db_setup_logging()
    conn = db_get_conn()
    c = conn.cursor()
    c.execute('''SELECT * FROM games WHERE room_id = ?''', [room_id])
    if c.fetchone() is None: return (False, 0)
    c.execute('''SELECT * FROM players WHERE room_id = ? AND nick = ?''', [room_id, nick])
    row = c.fetchone()
    if row is None:
        uid = random.randint(10000,99999)
        while c.execute('''SELECT * FROM players WHERE uid = ?''', [str(uid)]).fetchone() != None:
            uid = random.randint(10000, 99999)
        c.execute('''INSERT INTO players (room_id, nick, role, uid, ready, state, hp, mana) VALUES(?, ?, ?, ?, 0, 1, 100, 100)''', [room_id, nick, role, str(uid)])
        db_close_conn(conn)
        logging.info("Added new player %s to room %s with nick %s and role %s" % (uid, room_id, nick, role))
        return (True, uid)
    if row[2] == role:
        return (True, row[3])
    return (False, 0)

def db_set_ready(uid):
    db_setup_logging()
    conn = db_get_conn()
    c = conn.cursor()
    c.execute('''UPDATE players SET ready=1, state=2 WHERE uid=?''', [uid])
    if c.rowcount == 1:
        db_close_conn(conn)
        logging.info("Player %s ready" % (uid))
        return True
    return False

def db_game_ready(uid):
    db_setup_logging()
    conn = db_get_conn()
    c = conn.cursor()
    c.execute('''SELECT room_id FROM players WHERE uid=?''', [uid])
    room_id = c.fetchone()
    if room_id == None: return False
    room_id = room_id[0]
    c.execute('''SELECT count(*) FROM players WHERE room_id = ?''', [room_id])
    num_players = c.fetchone()[0]
    c.execute('''SELECT count(*) FROM players WHERE room_id = ? AND ready = 1''', [room_id])
    num_players_ready = c.fetchone()[0]
    if num_players_ready >= num_players / 2:
        c.execute('''UPDATE players SET state = 2 WHERE room_id=?''', [room_id])
        c.execute('''UPDATE games SET ready_countdown = 1 WHERE room_id=? and ready_countdown = 0 and state = 0''', [room_id])
        if c.rowcount == 1:
            logging.info("Countdown started for room %s" % (room_id))
        db_close_conn(conn)
    return True

def db_get_host_status(room_id):
    conn = db_get_conn()
    c = conn.cursor()
    c.execute('''SELECT nick, ready, role FROM players WHERE room_id=?''', [room_id])
    returnValue = {"Players": [{"Nick": row[0], "Ready": row[1], "Role": row[2] } for row in c.fetchall()]}
    return returnValue

def db_get_host_state(room_id):
    conn = db_get_conn()
    c = conn.cursor()
    c.execute('''SELECT state FROM games WHERE room_id=?''', [room_id])
    return c.fetchone()[0]

def db_get_client_state(uid):
    conn = db_get_conn()
    c = conn.cursor()
    c.execute('''SELECT state FROM players WHERE uid=?''', [uid])
    state = c.fetchone()
    if state == None: return False
    return state[0]

def db_set_preGameDone(room_id):
    conn = db_get_conn()
    c = conn.cursor()
    c.execute('''SELECT * FROM games WHERE room_id = ?''', [room_id])
    if c.fetchone() is None: return False
    c.execute('''UPDATE games SET state = 3 WHERE room_id = ?''', [room_id])
    db_close_conn(conn)
    return True

def db_set_randomEventDone(room_id):
    conn = db_get_conn()
    c = conn.cursor()
    c.execute('''SELECT * FROM games WHERE room_id = ?''', [room_id])
    if c.fetchone() is None: return False
    c.execute('''UPDATE games SET state = 4 WHERE room_id = ?''', [room_id])
    db_close_conn(conn)
    return True

def db_set_bossStoryDone(room_id):
    conn = db_get_conn()
    c = conn.cursor()
    c.execute('''SELECT * FROM games WHERE room_id = ?''', [room_id])
    if c.fetchone() is None: return False
    c.execute('''UPDATE games SET state = 5 WHERE room_id = ?''', [room_id])
    c.execute('''UPDATE players SET state = 4 WHERE room_id = ?''', [room_id])
    db_close_conn(conn)
    return True

def db_set_roundResultDone(room_id):
    conn = db_get_conn()
    c = conn.cursor()
    c.execute('''SELECT * FROM games WHERE room_id = ?''', [room_id])
    if c.fetchone() is None: return False
    c.execute('''UPDATE games SET state = 5 WHERE room_id = ?''', [room_id])
    c.execute('''UPDATE players SET state = 4 WHERE room_id = ?''', [room_id])
    db_close_conn(conn)
    return True
    # Implement new states based on stuff that has happend. HP on people, boss etc.

def db_do_client_action(uid, action):
    conn = db_get_conn()
    c = conn.cursor()
    c.execute('''SELECT * FROM players WHERE uid = ?''', [uid])
    if c.fetchone() is None: return False
    c.execute('''UPDATE players SET action = ? WHERE uid = ?''', [action, uid])
    db_close_conn(conn)
    return True

def db_get_client_status(uid):
    conn = db_get_conn()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''SELECT * FROM players WHERE uid = ?''', [uid])
    client = c.fetchone()
    if client is None: return False
    return {"HP": client['hp'], "Mana": client['mana']}
