__author__ = 'Atle'
from flask import Flask, request, render_template
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

@app.route('/game/start')
def startGame():
    uid = request.args.get('uid')
    return json.dumps(start_game(uid))

@app.route('/game/player_status')
def gameStatus():
    uid = request.args.get('uid')
    return json.dumps(get_player_status(uid))

@app.route('/host')
def host():
    return render_template('/host/host.html')

@app.route('/join')
def join():
    return render_template("/client/client.html")

if __name__ == '__main__':
    app.Debug = True
    app.run()