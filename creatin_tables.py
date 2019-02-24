import sqlite3

conn = sqlite3.connect('fakedata.db')
tablecreatin = open('creatin_tables.sql')
tablecreatin = tablecreatin.read()
conn.executescript(tablecreatin)
conn.commit()
conn.close()