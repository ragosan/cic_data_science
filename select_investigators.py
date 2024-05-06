import sqlite3
con = sqlite3.connect("cic.db")

cur = con.cursor()

res = cur.execute("SELECT yearly_salary FROM investigators")

res.fetchone()

print(res.fetchone())

con.close()