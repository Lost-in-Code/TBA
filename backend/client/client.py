__author__ = 'Atle'
from backend import database

def join_game(room_id, nick, role):
    return dict(zip(['result', 'uid'], database.insert_player(room_id, nick, role)))