import sqlite3, os

try:
	os.remove('data.db')
	print('data.db removed')
except FileNotFoundError:
	print('data.db didn\'t exist')


conn = sqlite3.connect('data.db')
tablecreatin = open('creatin_tables.sql')
tablecreatin = tablecreatin.read()
conn.executescript(tablecreatin)
conn.commit()
conn.close()

print('db reinitialized')