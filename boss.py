import os, random
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def boss():
    head = random.choice(os.listdir(os.path.join(os.path.dirname(__file__), 'static/images/boss/head')))
    torso = random.choice(os.listdir(os.path.join(os.path.dirname(__file__), 'static/images/boss/torso')))
    leftarm = random.choice(os.listdir(os.path.join(os.path.dirname(__file__), 'static/images/boss/leftarm')))
    rightarm = random.choice(os.listdir(os.path.join(os.path.dirname(__file__), 'static/images/boss/rightarm')))
    legs = random.choice(os.listdir(os.path.join(os.path.dirname(__file__), 'static/images/boss/legs')))
    weapon = random.choice(os.listdir(os.path.join(os.path.dirname(__file__), 'static/images/boss/weapon')))

    return render_template('boss.html', head=head, torso=torso, leftarm=leftarm, rightarm=rightarm, legs=legs, weapon=weapon)

if __name__ == "__main__":
    app.debug = True
    app.run()