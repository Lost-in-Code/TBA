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
    c.execute('''DROP TABLE IF EXISTS bosses''')
    c.execute('''CREATE TABLE players
                (room_id, nick, role, uid, ready, state, hp, mana, action)''')
    c.execute('''CREATE TABLE games
                (room_id, ready_countdown, state, round_countdown, event)''')
    c.execute('''CREATE TABLE bosses
                (room_id, name, hp, action)''')
    db_close_conn(conn)
    logging.info("Created DB")

def db_insert_game(room_id):
    db_setup_logging()
    conn = db_get_conn()
    c = conn.cursor()
    c.execute('''SELECT * FROM games WHERE room_id = ?''', [room_id])
    if c.fetchone() is None:
        c.execute('''INSERT INTO games VALUES (?, 0, 0, 0, 0)''', [str(room_id)])
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
        c.execute('''INSERT INTO players (room_id, nick, role, uid, ready, state, hp, mana, action) VALUES(?, ?, ?, ?, 0, 1, 100, 100, "0")''', [room_id, nick, role, str(uid)])
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
    c.execute('''SELECT nick, ready, role, uid FROM players WHERE room_id=?''', [room_id])
    returnValue = {"Players": [{"Nick": row[0], "Ready": row[1], "Role": row[2], "Uid": row[3] } for row in c.fetchall()]}
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
    c.execute('''SELECT hp FROM bosses WHERE room_id = ? AND hp > 0''', [room_id])
    boss_dead = c.fetchone() is None
    c.execute('''SELECT hp FROM players WHERE room_id = ? AND hp > 0''', [room_id])
    players_dead = c.fetchone() is None
    if boss_dead:
        num_bosses = c.execute('''SELECT count(*) FROM bosses WHERE room_id = ?''', [room_id]).fetchone()[0]
        if num_bosses < 4:
            c.execute('''UPDATE games SET state = 3 WHERE room_id = ?''', [room_id])
            c.execute('''UPDATE players SET state = 3 WHERE room_id = ?''', [room_id])
        else:
            c.execute('''UPDATE games SET state = 7 WHERE room_id = ?''', [room_id])
            c.execute('''UPDATE players SET state = 0 WHERE room_id = ?''', [room_id])
    elif players_dead:
        c.execute('''UPDATE games SET state = 99 WHERE room_id = ?''', [room_id])
        c.execute('''UPDATE players SET state = 0 WHERE room_id = ?''', [room_id])
    else:
        c.execute('''UPDATE games SET state = 5 WHERE room_id = ?''', [room_id])
        c.execute('''UPDATE players SET state = 4 WHERE room_id = ?''', [room_id])
    db_close_conn(conn)
    return True

def db_do_client_action(uid, action):
    conn = db_get_conn()
    c = conn.cursor()
    c.execute('''SELECT * FROM players WHERE uid = ?''', [uid])
    if c.fetchone() is None: return False
    c.execute('''UPDATE players SET action = ?, state = 5 WHERE uid = ?''', [str(action), uid])
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

def db_set_randomEvent(room_id, event_id):
    conn = db_get_conn()
    c = conn.cursor()
    c.execute('''SELECT * FROM games WHERE room_id = ?''', [room_id])
    if c.fetchone() is None: return False
    c.execute('''UPDATE games SET event = ? WHERE room_id = ?''', [event_id, room_id])
    db_close_conn(conn)
    return True

def db_insert_boss(room_id, boss_name):
    conn = db_get_conn()
    c = conn.cursor()
    c.execute('''SELECT * FROM games WHERE room_id = ?''', [room_id])
    if c.fetchone() is None: return False
    c.execute('''INSERT INTO bosses (room_id, name, hp, action) VALUES (?, ?, 100, "0")''', [room_id, boss_name])
    db_close_conn(conn)
    return True

def db_get_boss_id(room_id):
    conn = db_get_conn()
    c = conn.cursor()
    c.execute('''SELECT * FROM games WHERE room_id = ?''', [room_id])
    if c.fetchone() is None: return False
    c.execute('''SELECT count(*) FROM bosses WHERE room_id = ?''', [room_id])
    return c.fetchone()[0]

def db_boss_attack(room_id, action):
    conn = db_get_conn()
    c = conn.cursor()
    c.execute('''SELECT * FROM games WHERE room_id = ?''', [room_id])
    if c.fetchone() is None: return False
    c.execute('''UPDATE bosses SET action = ? WHERE room_id = ? AND hp > 0''', [str(action), room_id])
    db_close_conn(conn)
    return True

def db_get_boss_action(room_id):
    conn = db_get_conn()
    c = conn.cursor()
    c.execute('''SELECT * FROM games WHERE room_id = ?''', [room_id])
    if c.fetchone() is None: return False
    c.execute('''SELECT action FROM bosses WHERE room_id = ? AND hp > 0''', [room_id])
    boss = c.fetchone()
    if boss is not None:
        return boss[0]
    else: return False

def db_get_boss_hp(room_id):
    conn = db_get_conn()
    c = conn.cursor()
    c.execute('''SELECT * FROM games WHERE room_id = ?''', [room_id])
    if c.fetchone() is None: return False
    c.execute('''SELECT hp FROM bosses WHERE room_id = ? AND hp > 0''', [room_id])
    boss_hp = c.fetchone()
    if boss_hp is not None:
        return boss_hp[0]
    else: return False
