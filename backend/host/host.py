__author__ = 'Atle'
from backend import database
import random

def create_game():
    room_id = random.randint(1000, 9999)
    while database.db_insert_game(room_id) == False:
        room_id = random.randint(1000, 9999)
    return {"room_id": room_id}

def get_host_status(room_id):
    return database.db_get_host_status(room_id)

def get_host_state(room_id):
    return database.db_get_host_state(room_id)