import sqlite3

def new_user(conn, netid, name, profpic):
	query = "INSERT INTO users VALUES (?, ?, ?);"
	cursor = conn.cursor()
	cursor.execute(query, (netid, name, profpic))
	conn.commit()
	cursor.close()

if __name__ == '__main__':
	conn = sqlite3.connect('fakedata.db')
	new_user(conn, "rjf19", "Ryan", "lolidk.png")