import sqlite3

def weiter(conn, query, tup):
	cursor = conn.cursor()
	cursor.execute(query, tup)
	conn.commit()
	cursor.close()

def new_user(conn, netid, name, profpic):
	tup = (netid, name, profpic)
	query = "INSERT INTO users VALUES (?, ?, ?);"
	weiter(conn, query, tup)

def report_user(conn, reporter_netid, reported_netid, reason):
	tup = (reporter_netid, reported_netid, reason)
	query = "INSERT INTO report VALUES (?, ?, ?);"
	weiter(conn, query, tup)


def recommend_user(conn, recommender_netid, recommendee_netid, recommended__netid, reason):
	tup = (recommender_netid, recommendee_netid, recommended__netid, reason)
	query = "INSERT INTO recommend VALUES (?, ?, ?, ?);"
	weiter(conn, query, tup)
	

if __name__ == '__main__':
	conn = sqlite3.connect('fakedata.db')
	new_user(conn, "rjf19", "Ryan", "lolidk.png")
	report_user(conn,"rjf19","rjf19","my code is sinful and i deserve to be reported")

