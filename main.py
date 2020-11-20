from flask import Flask, render_template, request, jsonify, redirect, g
import sqlite3
import random

app = Flask(__name__)
DATABASE = 'LogRPG.db'


def connect_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.route('/login', methods=['POST', 'GET'])
def home():
    if request.method == 'GET':
        with connect_db() as con:
            cur = con.cursor()
        try:
            username = request.form['username']
            password = request.form['password']
            cur.execute('select * from people where LogRPG_Account_Login = ?', [username])
            if cur.fetchone() is not None:
                con.close()
                return render_template('login.html', msg="That username is already taken, please choose another")
            else:
                cur = con.cursor()
                cur.execute("INSERT INTO LogRPG_Account (LogRPG_Account_Login, LogRPG_Account_Password) VALUES (?, ?)", [username, password])
                con.commit()
                con.close()
                return render_template('login.html', msg="Successfully registrated ! You can log in.")
        except:
            con.rollback()
            con.close()
            return render_template('login.html', msg="Error in insert operation")

    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        validate_user = validate(username, password)

        if validate_user == False:
            return render_template('login.html', msg="Invalid username or password please try again")
        else:
            return redirect('home.html')

    else:
        return render_template('login.html', msg="Invalid operation")


def query_db(query, args=(), one=False):
    cur = connect_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()

    return (rv[0] if rv else None) if one else rv


def validate(username, password):
    g.db = connect_db()
    id = g.db.execute('SELECT * FROM LogRPG_Account WHERE LogRPG_Account_Login = ?', [username])
    for row in id:
        user = row[1]
        passw = row[2]
    if passw == password:
        return True
    else:
        return False


@app.route('/')
def redirect_login():
    return redirect("/login")


@app.route('/home', methods=["GET"])
def player_list():
    con = connect_db()
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM LogRPG_Character")
    rows = cur.fetchall()
    return render_template("home.html", rows=rows)


@app.route('/rollNdice/<int:dice>/<int:nbDice>')
def roll_dice(dice, nbDice):
    return jsonify({"result": roll_dices(dice, nbDice)})


# roll the dice and return the result. parameters: d = dice rolled (4, 6, 8, 10, 100), nbD = number of dice rolled
def roll_dices(dice, nbDice):
    result = 0
    for i in range(0, nbDice):
        result += random.randint(1, dice)
    return (str(result))


app.run()