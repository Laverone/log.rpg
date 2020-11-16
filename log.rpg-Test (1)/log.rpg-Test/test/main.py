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






c.execute("""CREATE TABLE LogRPG_Character (
  LogRPG_Character_Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  LogRPG_Character_Name TEXT(255) NOT NULL,
  LogRPG_Character_Sheet TEXT,
  LogRPG_Character_Inventory TEXT,
  LogRPG_Character_Senario_Id INTEGER NOT NULL
)""")

c.execute("""CREATE TABLE LogRPG_Account (
  LogRPG_Account_Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  LogRPG_Account_Login TEXT(50) NOT NULL,
  LogRPG_Account_Password TEXT NOT NULL
)""")

c.execute("""CREATE TABLE LogRPG_Senario (
  LogRPG_Senario_Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  LogRPG_Senario_Title TEXT NOT NULL,
  LogRPG_Senario_Text TEXT,
  LogRPG_Senario_Account_Id INTEGER NOT NULL
)""")
