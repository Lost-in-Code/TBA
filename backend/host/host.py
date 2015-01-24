__author__ = 'Atle'
from backend import database
import random
from flask import url_for
import json

def create_game():
    room_id = random.randint(1000, 9999)
    while database.db_insert_game(room_id) == False:
        room_id = random.randint(1000, 9999)
    return {"room_id": room_id}

def get_host_status(room_id):
    return database.db_get_host_status(room_id)

def get_host_state(room_id):
    return database.db_get_host_state(room_id)

def set_host_preGameDone(room_id):
    return database.db_set_preGameDone(room_id)

def set_host_randomEventDone(room_id):
    return database.db_set_randomEventDone(room_id)

def set_host_bossStoryDone(room_id):
    return database.db_set_bossStoryDone(room_id)

def set_host_roundResultDone(room_id):
    return database.db_set_roundResultDone(room_id)

def get_host_randomEvent(room_id):
    json_data = open('content/events.json')
    data = json.load(json_data)
    event = random.choice(data['events'])
    database.db_set_randomEvent(room_id, event['id'])
    return event

def get_host_bossStory(room_id):
    json_data = open('content/bosses.json')
    data = json.load(json_data)
    return random.choice(data['bosses'])

def get_host_questStory(room_id):
    json_data = open('content/quests.json')
    data = json.load(json_data)
    return random.choice(data['quests'])

def get_host_round(room_id):
    return "pew"

def get_host_round_result(room_id):
    return "pew"