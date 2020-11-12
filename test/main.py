from flask import Flask
app = Flask(__name__)

app.route("/main")
def main():
     con = sqlite3.connect("LogRPG.sql")
     con.row_factory = sqlite3.Row
     cur = con.cursor()
     cur.execute("select * from LogRPG_Character")
     rows = cur.fetchall()
     return render_template("main.html", rows = rows)
