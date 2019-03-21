import sqlite3

#so wheras useful_operations.py has lots of insertions n stuff, this one will be used to get info

def weiter(conn, query, tup):
	cursor = conn.cursor()
	cursor.execute(query, tup)
	conn.commit()
	cursor.close()

"""
-------------------------------
Questions and answers
-------------------------------
"""

def get_question_text(conn, qid):
	tup = (netid, qid, answer_id, weight)
	query = "INSERT INTO answer VALUES (?, ?, ?, ?);"
	weiter(conn, query, tup)