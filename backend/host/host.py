__author__ = 'Atle'
from backend import database
import random

def create_game():
    room_id = random.randint(1000, 9999)
    while database.db_insert_game(room_id) == False:
        room_id = random.randint(1000, 9999)
    return room_id