__author__ = 'Atle'
from backend import database

def join_game(room_id, nick, role):
    return database.insert_player(room_id, nick, role)