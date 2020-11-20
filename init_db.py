import sqlite3
"""
conn = sqlite3.connect('LogRPG.db')
cur = conn.cursor()

req = "CREATE TABLE LogRPG_Account(LogRPG_Account_Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, LogRPG_Account_Login TEXT(50) NOT NULL, LogRPG_Account_Password TEXT NOT NULL);"
cur.execute(req)
conn.commit()

req = "CREATE TABLE LogRPG_Senario(LogRPG_Senario_Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, LogRPG_Senario_Title TEXT NOT NULL, LogRPG_Senario_Text TEXT, LogRPG_Senario_Account_Id INTEGER NOT NULL, CONSTRAINT fk_LogRPG_Senario_LogRPG_Account_1 FOREIGN KEY (LogRPG_Senario_Account_Id) REFERENCES LogRPG_Account(LogRPG_Account_Id));"
cur.execute(req)
conn.commit()

req = "CREATE TABLE LogRPG_Character(LogRPG_Character_Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, LogRPG_Character_Name TEXT(255) NOT NULL, LogRPG_Character_Sheet TEXT, LogRPG_Character_Inventory TEXT, LogRPG_Character_Senario_Id INTEGER NOT NULL, CONSTRAINT fk_LogRPG_Character_LogRPG_Senario_1 FOREIGN KEY (LogRPG_Character_Senario_ID) REFERENCES LogRPG_Senario(LogRPG_Senario_Id));"
cur.execute(req)
conn.commit()

conn.close
"""
con = sqlite3.connect('LogRPG.db')
cur = con.cursor()
cur.execute("INSERT INTO LogRPG_Character (LogRPG_Character_Name, LogRPG_Senario_, LogRPG_Senario_Account_Id) VALUES (?, ?, ?)", ["Hello", "Yo", 1])
con.commit()
cur.execute("INSERT INTO LogRPG_Character (LogRPG_Senario_Title, LogRPG_Senario_Account_Id) VALUES (?, ?)", ["Hello", 1])
con.commit()
con.close()