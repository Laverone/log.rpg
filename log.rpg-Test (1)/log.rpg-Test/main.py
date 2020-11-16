from flask import Flask, render_template, request
import sqlite3
import random

app = Flask(__name__)

@app.route('/login')
def index():
    return render_template('login')

#roll the dice and return the result. parameters: d = dice rolled (4,6,8,10,100), nbD = number of dice rolled
def rollTheDice(d,nbD=1):
    rnd=0
    for i in range(0,nbD) :
        rnd+=random.randint(1,d)
    return(str(rnd))

@app.route("/rollTheDice/", methods = ["POST","GET"])
def event_dice():
    dice = request.form.dice
    nbD = request.form["de"]
    rollTheDice(dice, nbD)

@app.route('/home', methods = ["GET"])
def player_list():
	con = sqlite3.connect('logRPG.db')
	con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from LogRPG_Character")
    rows = cur.fetchall()
    return render_template("home.html", rows = rows)