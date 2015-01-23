__author__ = 'Atle'
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    return "HEI HEI WHOOOO"

@app.route('game/join')
def join():
    room = request.args.get('room')
    nick = request.args.get('nick')
    role = request.args.get('role')
    return ' - '.join([room, nick, role])

if __name__ == '__main__':
    app.run()