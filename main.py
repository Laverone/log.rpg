from flask import Flask, render_template, request, jsonify, redirect, g, session, url_for
import os
import sqlite3
import random

app = Flask(__name__)
DATABASE = 'LogRPG.db'


@app.route('/')
def redirect_login():
    return redirect(url_for('login'))


def connect_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.route('/login', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        con = connect_db()
        cur = con.cursor()
        cur.execute("SELECT * FROM LogRPG_Account WHERE (LogRPG_Account_Login = ? AND LogRPG_Account_Password = ?)", [username, password])
        row = cur.fetchone()
        if row is not None:
            session['loggedin'] = True
            session['Id'] = row[0]
            session['username'] = username
            con.close()
            return redirect(url_for('home'))
        return render_template('login.html', msg = "Incorrect username / password !")

    return render_template('login.html')


@app.route('/register', methods = ["POST", "GET"])
def register():
    if request.method == "POST":
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
    if 'loggedin' in session:
        con = connect_db()
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM LogRPG_Senario")
        rows = cur.fetchall()
        return render_template("home.html", rows = rows, accountName = session['username'])

    else:
        return redirect(url_for('login'))


@app.route('/displayScenario/<string:name>')
def displayScenario(name):
    return jsonify({"scenario": getScenarioText(name)})


def getScenarioText(name):
    con = connect_db()
    cur = con.cursor()
    cur.execute('SELECT LogRPG_Senario_Text FROM LogRPG_Senario WHERE LogRPG_Senario_Title = ?', [name])
    text = cur.fetchone()
    return text


@app.route('/home', methods = ["POST"])
def scenario():
    if request.method == "POST":
        try:
            scenarioTitle = request.form['scenarioTitle']
            scenarioText = request.form['scenarioText']

            con = connect_db()
            cur = con.cursor()
            cur.execute('SELECT * FROM LogRPG_Senario WHERE LogRPG_Senario_Title = ?', [scenarioTitle])
            if cur.fetchone() is not None:
                cur = con.cursor()
                if scenarioText is None:
                    cur.execute('UPDATE LogRPG_Senario SET LogRPG_Senario_Text = NULL WHERE LogRPG_Senario_Title = ?', [scenarioTitle])
                else:
                    cur.execute('UPDATE LogRPG_Senario SET LogRPG_Senario_Text = ? WHERE LogRPG_Senario_Title = ?', [scenarioText, scenarioTitle])
            else:
                cur = con.cursor()
                if scenarioText is None:
                    cur.execute("INSERT INTO LogRPG_Senario (LogRPG_Senario_Title, LogRPG_Senario_Account_Id) VALUES (?, ?)", [scenarioTitle, session['Id']])
                else:
                    cur.execute("INSERT INTO LogRPG_Senario (LogRPG_Senario_Title, LogRPG_Senario_Text, LogRPG_Senario_Account_Id) VALUES (?, ?, ?)", [scenarioTitle, scenarioText, session['Id']])
            con.commit()

        except:
            return home()

    return home()


@app.route('/character', methods = ["POST", "GET"])
def character():
    if request.method == "POST":
        try:
            name = request.form['name']
            sheet = request.form['sheet']

            con = connect_db()
            cur = con.cursor()

        except:
            return render_template("character.html", msg = "Error in insertion method, please retry")
    return redirect(url_for('home'))


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