__author__ = 'Atle'
from flask import Flask, request, render_template, url_for
import json
from backend.database import *
from backend.host.host import *
from backend.client.client import *

app = Flask(__name__)

@app.route('/create_db')
def createDb():
    create_db()
    return "OK, Database (re)created"

@app.route('/')
def index():
    return "HEI HEI WHOOOO"

@app.route('/game/create')
def createGame():
    return json.dumps(create_game())

@app.route('/game/join')
def joinGame():
    room = request.args.get('room')
    nick = request.args.get('nick')
    role = request.args.get('role')
    return json.dumps(join_game(room, nick, role))

@app.route('/game/doClientAction')
def doClientAction():
    uid = request.avgs.get('uid')
    action = request.avgs.get('action')
    return json.dumps(do_client_action(uid, action))

@app.route('/game/getPlayerStatus')
def getPlayerStatus():
    uid = request.avgs.get('uid')
    return json.dumps(get_player_status(uid))

@app.route('/game/start')
def startGame():
    uid = request.args.get('uid')
    return json.dumps(start_game(uid))

@app.route('/game/getPlayerState')
def gameStatus():
    uid = request.args.get('uid')
    return json.dumps(get_player_state(uid))

@app.route('/game/getHostState')
def getHostState():
    room_id = request.args.get('room_id')
    return json.dumps(get_host_state(room_id))

@app.route('/game/getHostStatus')
def getHostStatus():
    room_id = request.args.get('room_id')
    return json.dumps(get_host_status(room_id))

@app.route('/game/getHostQuestStory')
def getHostQuestStory():
    room_id = request.args.get('room_id')
    return json.dumps({"Title": "Lorem Ipsum", "Text": "There once was a BEEP doing BEEP to a BEEP while singing", "Imgurl": url_for('static', filename="images/bg_cave_blur_10.jpg")})

@app.route('/game/getHostRandomEvent')
def getHostRandomEvent():
    room_id = request.args.get('room_id')
    return json.dumps(get_host_randomEvent(room_id))

@app.route('/game/getHostBossStory')
def getHostBossStory():
    room_id = request.args.get('room_id')
    return json.dumps("Pew")

@app.route('/game/preGameDone')
def setPreGameDone():
    room_id = request.args.get('room_id')
    return json.dumps(set_host_preGameDone(room_id))

@app.route('/game/randomEventDone')
def setRandomEventDone():
    room_id = request.args.get('room_id')
    return json.dumps(set_host_randomEventDone(room_id))

@app.route('/game/bossStoryDone')
def setBossStoryDone():
    room_id = request.args.get('room_id')
    return json.dumps(set_host_bossStoryDone(room_id))

@app.route('/game/roundResultDone')
def setRoundResultDone():
    room_id = request.args.get('room_id')
    return json.dumps(set_host_roundResultDone(room_id))

@app.route('/host')
def host():
    return render_template('/host/host.html')

@app.route('/join')
def join():
    return render_template("/client/client.html")

if __name__ == '__main__':
    app.Debug = True
    app.run()