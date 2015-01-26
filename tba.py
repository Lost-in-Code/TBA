__author__ = 'Atle'
import os, random, threading
from flask import Flask, request, render_template, url_for
import json
from game import *
from backend.database import *
from backend.host.host import *
from backend.client.client import *

app = Flask(__name__)

@app.route('/create_db')
def createDb():
    create_db()
    return "OK, Database (re)created"

@app.route('/')
def join():
    return render_template("/client/client.html")

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
    uid = request.args.get('uid')
    action = request.args.get('action')
    return json.dumps(do_client_action(uid, action))

@app.route('/game/getPlayerStatus')
def getPlayerStatus():
    uid = request.args.get('uid')
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
    return json.dumps(get_host_questStory(room_id))

@app.route('/game/getHostRandomEvent')
def getHostRandomEvent():
    room_id = request.args.get('room_id')
    return json.dumps(get_host_randomEvent(room_id))

@app.route('/game/getHostBossStory')
def getHostBossStory():
    room_id = request.args.get('room_id')
    return json.dumps(get_host_bossStory(room_id))

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

@app.route('/game/getHostRound')
def getHostRound():
    room_id = request.args.get('room_id')
    return json.dumps(get_host_round(room_id))

@app.route('/game/getHostRoundResult')
def getHostRoundResult():
    room_id = request.args.get('room_id')
    return json.dumps(get_host_round_result(room_id))

@app.route('/host')
def host():
    return render_template('/host/host.html')

@app.route("/game/generateBoss")
def generateBoss():
    head = random.choice(os.listdir(os.path.join(os.path.dirname(__file__), 'static/images/boss2/head')))
    torso = random.choice(os.listdir(os.path.join(os.path.dirname(__file__), 'static/images/boss2/torso')))
    leftarm = random.choice(os.listdir(os.path.join(os.path.dirname(__file__), 'static/images/boss2/leftarm')))
    rightarm = random.choice(os.listdir(os.path.join(os.path.dirname(__file__), 'static/images/boss2/rightarm')))
    legs = random.choice(os.listdir(os.path.join(os.path.dirname(__file__), 'static/images/boss2/legs')))
    weapon = random.choice(os.listdir(os.path.join(os.path.dirname(__file__), 'static/images/boss2/weapon')))
    return json.dumps({"head": url_for('static', filename='images/boss2/head/' + head),
                       "leftarm": url_for('static', filename='images/boss2/leftarm/' + leftarm),
                       "legs": url_for('static', filename='images/boss2/legs/' + legs),
                       "rightarm": url_for('static', filename='images/boss2/rightarm/' + rightarm),
                       "torso": url_for('static', filename='images/boss2/torso/' + torso),
                       "weapon": url_for('static', filename='images/boss2/weapon/' + weapon)})


if __name__ == '__main__':
    #start the game thread
    t = threading.Thread(target=loop)
    t.start()
    
    #start the web server
    app.Debug = True
    app.run(host='0.0.0.0')