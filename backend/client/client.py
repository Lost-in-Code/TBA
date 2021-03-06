__author__ = 'Atle'
from backend import database

def join_game(room_id, nick, role):
    return dict(zip(['result', 'uid'], database.db_insert_player(room_id, nick, role)))

def start_game(uid):
    if not database.db_set_ready(uid): return False
    return database.db_game_ready(uid)

def get_player_state(uid):
    return database.db_get_client_state(uid)

def do_client_action(uid, action):
    return database.db_do_client_action(uid, action)

def get_player_status(uid):
    return database.db_get_client_status(uid)