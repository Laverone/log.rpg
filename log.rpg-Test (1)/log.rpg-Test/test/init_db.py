import sqlite3
from flask import Flask, render_template, request

app = Flask('__name__')


@app.route('/home', methods = ["GET"])
def player_list():
	con = sqlite3.connect('logRPG.db')
	con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from LogRPG_Character")
    rows = cur.fetchall()
    return render_template("home.html", rows = rows)
    
#c.execute("INSERT INTO logRPG_Character VALUES (1, 'QuilleLianne', 'shette', 'void, I am empty bro', 5)")

#c.execute("SELECT * FROM LogRPG_Character WHERE LogRPG_Character_Name='QuilleLianne'")