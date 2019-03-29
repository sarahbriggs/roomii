import sqlite3

conn = sqlite3.connect('fakedata.db')
delete_tables = open('delete_tables.sql')
delete_tables = delete_tables.read()
tablecreatin = open('creatin_tables.sql')
tablecreatin = tablecreatin.read()
conn.executescript(delete_tables)
conn.executescript(tablecreatin)
conn.commit()
conn.close()