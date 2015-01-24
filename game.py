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
    c = conn.cursor()
    c.execute('''UPDATE players SET state = 3 WHERE room_id=?''', [room_id])
    c.execute('''UPDATE games SET state = 2 WHERE room_id=?''', [room_id])
    logging.info("Updated state for players in game: %s" % (room_id))
    print("Updated state for players in game: %s" % (room_id))
    db_close_conn(conn)

def round_countdown_done(room_id):
    conn = db_get_conn()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''UPDATE players SET state = 5 WHERE room_id=?''', [room_id])
    c.execute('''UPDATE games SET state = 6, round_countdown = 0 WHERE room_id=?''', [room_id])
    c.execute('''SELECT count(*) FROM players WHERE room_id = ?''', [room_id])
    num_players = c.fetchone()[0]
    c.execute('''SELECT count(*) FROM players WHERE room_id = ? AND role = "1" AND action = "1" AND hp > 0''', [room_id])
    num_dps_action1 = c.fetchone()[0]
    c.execute('''SELECT count(*) FROM players WHERE room_id = ? AND role = "1" AND action = "2" AND hp > 0''', [room_id])
    num_dps_action2 = c.fetchone()[0]
    c.execute('''SELECT count(*) FROM players WHERE room_id = ? AND role = "1" AND action = "3" AND hp > 0''', [room_id])
    num_dps_action3 = c.fetchone()[0]
    c.execute('''SELECT count(*) FROM players WHERE room_id = ? AND role = "2" AND action = "1" AND hp > 0''', [room_id])
    num_tank_action1 = c.fetchone()[0]
    c.execute('''SELECT count(*) FROM players WHERE room_id = ? AND role = "2" AND action = "2" AND hp > 0''', [room_id])
    num_tank_action2 = c.fetchone()[0]
    c.execute('''SELECT count(*) FROM players WHERE room_id = ? AND role = "2" AND action = "3" AND hp > 0''', [room_id])
    num_tank_action3 = c.fetchone()[0]
    c.execute('''SELECT count(*) FROM players WHERE room_id = ? AND role = "3" AND action = "1" AND mana > 25 AND hp > 0''', [room_id])
    num_heal_action1 = c.fetchone()[0]
    c.execute('''SELECT count(*) FROM players WHERE room_id = ? AND role = "3" AND action = "2" AND mana > 20 AND hp > 0''', [room_id])
    num_heal_action2 = c.fetchone()[0]
    c.execute('''SELECT count(*) FROM players WHERE room_id = ? AND role = "3" AND action = "3" AND hp > 0''', [room_id])
    num_heal_action3 = c.fetchone()[0]
    c.execute('''SELECT * FROM bosses WHERE room_id = ? AND hp > 0''', [room_id])
    boss = c.fetchone()
    dmg_taken_tank = 0
    dmg_taken_group = 0
    dmg_done_melee = 0
    dmg_done_range = 0
    healing_done_tank = 0
    healing_done_group = 0
    if boss['action'] == 0:
        dmg_taken_tank = max(40 * (1 - ((num_tank_action1 * 3)  / num_players)), 0)
        dmg_done_range = 7 * (num_dps_action2 * 3 / num_players)
        dmg_done_melee = 13 * (num_dps_action1 * 3 / num_players)
        healing_done_tank = abs(max(30 * (-1 + (num_heal_action1 / num_players / 3)), 0))
        healing_done_group = abs(max(15 * (-1 + (num_heal_action2 / num_players / 3)), 0))
    elif boss['action'] == 1:
        dmg_taken_group = max(20 * (1 - ((num_tank_action2 * 3)  / num_players)), 0)
        dmg_done_range = 13 * (num_dps_action2 * 3 / num_players)
        dmg_done_melee = 7 * (num_dps_action1 * 3 / num_players)
        healing_done_tank = abs(max(30 * (-1 + (num_heal_action1 / num_players / 3)), 0))
        healing_done_group = abs(max(15 * (-1 + (num_heal_action2 / num_players / 3)), 0))
    elif boss['action'] == 2:
        dmg_done_range = abs(max(0 * (-1 + (num_dps_action2 / num_players / 3)), 0))
        dmg_done_melee = abs(max(0 * (-1 + (num_dps_action1 / num_players / 3)), 0))
        healing_done_tank = abs(max(30 * (-1 + (num_heal_action1 / num_players / 3)), 0))
        healing_done_group = abs(max(15 * (-1 + (num_heal_action2 / num_players / 3)), 0))
    elif boss['action'] == 3:
        dmg_done_range = abs(max(7 * (-1 + (num_dps_action2 / num_players / 3)), 0))
        dmg_done_melee = abs(max(13 * (-1 + (num_dps_action1 / num_players / 3)), 0))
        healing_done_tank = abs(max(30 * (-1 + (num_heal_action1 / num_players / 3)), 0))
        healing_done_group = abs(max(15 * (-1 + (num_heal_action2 / num_players / 3)), 0))

    c.execute('''UPDATE bosses SET hp = ? WHERE room_id = ? AND hp > 0''', [boss['hp'] - (dmg_done_melee + dmg_done_range), room_id])
    c.execute('''SELECT * FROM players WHERE room_id = ?''', [room_id])
    print("Group did %s damage, took %s dmg and healed %s" % (dmg_done_range + dmg_done_melee, dmg_taken_tank + dmg_taken_group, healing_done_group + healing_done_tank))
    players = c.fetchall()
    for player in players:
        if player['role'] == "2":
            c.execute('''UPDATE players SET hp = ?, action = 0 WHERE uid = ? AND hp > 0''', [min(player['hp'] - dmg_taken_tank - dmg_taken_group + healing_done_group + healing_done_tank, 100),
                                                                                  player['uid']])
        elif player['role'] == "1":
            c.execute('''UPDATE players SET hp = ?, action = 0 WHERE uid = ? AND hp > 0''', [min(player['hp'] - dmg_taken_group + healing_done_group, 100), player['uid']])
        elif player['role'] == "3":
            mana_used = 0
            if player['action'] == "1":
                mana_used = -25
            elif player['action'] == "2":
                mana_used = -20
            elif player['action'] == "3":
                mana_used = +50
            c.execute('''UPDATE players SET hp = ?, action = 0, mana = ? WHERE uid = ? AND hp > 0''', [min(player['hp'] - dmg_taken_group + healing_done_group, 100),
                                                                                            min(player['mana'] + mana_used, 100)])
    logging.info("Updated round state for players in game: %s" % (room_id))
    print("Updated round state for players in game: %s" % (room_id))
    db_close_conn(conn)

def loop():
    time.sleep(2)
    conn = db_get_conn()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''SELECT * FROM games WHERE ready_countdown = 1 and state=0''')
    rows = c.fetchall()
    for row in rows:
        c.execute('''UPDATE games SET state=1 WHERE room_id=?''', [row["room_id"]])
        t = Timer(15.0,ready_countdown_done, args=[row["room_id"]])
        t.start()
        logging.info("Started timer for game: %s" % (row["room_id"]))
        print("Started timer for game: %s" % (row["room_id"]))
    c.execute('''SELECT * FROM games WHERE state = 5 and round_countdown = 0''')
    rows = c.fetchall()
    for row in rows:
        c.execute('''UPDATE games SET round_countdown = 1 WHERE room_id = ?''', [row["room_id"]])
        t = Timer(15.0, round_countdown_done, args=[row["room_id"]])
        t.start()
        logging.info("Started timer for game: %s" % (row["room_id"]))
        print("Started timer for game: %s" % (row["room_id"]))
    db_close_conn(conn)

if __name__ == '__main__':
    while(True): loop()