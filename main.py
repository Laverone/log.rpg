from flask import Flask, render_template, request, jsonify, redirect, g, session, url_for, escape, request
import os
import sqlite3
import random

app = Flask(__name__)
DATABASE = 'LogRPG.db'


@app.route('/')
def redirect_login():
    return redirect("/login")


def connect_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        con = connect_db()
        cur = con.cursor()
        cur.execute("SELECT * FROM LogRPG_Account WHERE (LogRPG_Account_Login = ? AND LogRPG_Account_Password = ?)", [username, password])
        account = cur.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = username
            con.close()
            return redirect(url_for('home'))
        return render_template('login.html', msg = "Incorrect username / password !  ")

    return render_template('login.html')


@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            con = connect_db()
            cur = con.cursor()
            cur.execute('SELECT * FROM LogRPG_Account WHERE LogRPG_Account_Login = ?', [username])
            if cur.fetchone() is not None:
                con.close()
                return render_template('register.html', msg = "That username is already taken, please choose another")
            else:
                cur = con.cursor()
                cur.execute("INSERT INTO LogRPG_Account (LogRPG_Account_Login, LogRPG_Account_Password) VALUES (?, ?)", [username, password])
                con.commit()
                con.close()
                return redirect(url_for('login'))
        except:
            con.rollback()
            con.close()
            return render_template('register.html', msg = "Error in insert operation")

    return render_template('register.html')


@app.route('/home', methods = ["GET"])
def home():
    con = connect_db()
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM LogRPG_Character")
    rows = cur.fetchall()
    return render_template("home.html", rows = rows)


@app.route('/rollNdice/<int:dice>/<int:nbDice>')
def roll_dice(dice, nbDice):
    return jsonify({"result": roll_dices(dice, nbDice)})


# roll the dice and return the result. parameters: d = dice rolled (4, 6, 8, 10, 100), nbD = number of dice rolled
def roll_dices(dice, nbDice):
    result = 0
    for i in range(0, nbDice):
        result += random.randint(1, dice)
    return (str(result))


app.secret_key = os.urandom(24)
app.run()