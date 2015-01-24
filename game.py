__author__ = 'Atle'
import time
import sqlite3
import logging
from threading import Timer

def db_get_conn():
    return sqlite3.connect('database.db', timeout=15)

def db_setup_logging():
    logging.basicConfig(filename='tba.log',level=logging.INFO)

def db_close_conn(conn):
    conn.commit()
    conn.close()

def ready_countdown_done(room_id):
    conn = db_get_conn()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''UPDATE players SET state=3 WHERE room_id=?''', [room_id])
    c.execute('''UPDATE games SET state = 2 WHERE room_id?''', [room_id])
    logging.info("Updated state for players in game: %s" % (room_id))
    print("Updated state for players in game: %s" % (room_id))
    db_close_conn()

def loop():
    time.sleep(1)
    conn = db_get_conn()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''SELECT * FROM games WHERE ready_countdown=1 and state=0''')
    rows = c.fetchall()
    for row in rows:
        c.execute('''UPDATE games SET state=1 WHERE room_id=?''', [row["room_id"]])
        t = Timer(15.0,ready_countdown_done, args=(row["room_id"]))
        t.start()
        logging.info("Started timer for game: %s" % (row["room_id"]))
        print("Started timer for game: %s" % (row["room_id"]))
    db_close_conn(conn)

if __name__ == '__main__':
    while(True): loop()