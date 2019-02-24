import sqlite3

conn = sqlite3.connect('fakedata.db')
conn.execute('''
	CREATE TABLE users(netid varchar(16) PRIMARY KEY, profpic varchar(255));
	''')
conn.commit()
conn.close()