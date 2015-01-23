__author__ = 'Atle'
import sqlite3

def create_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS games''')
    c.execute('''DROP TABLE IF EXISTS players''')
    c.execute('''CREATE TABLE players
                (room_id, nick, role)''')
    c.execute(''' CREATE TABLE games
                (room_id)''')
    conn.commit()
    conn.close()