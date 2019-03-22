import sqlite3

#so wheras useful_operations.py has lots of insertions n stuff, this one will be used to get info

def zurueck(conn, query, tup): 
	cursor = conn.cursor()
	cursor.execute(query, tup)
	conn.commit()
	cursor.close()
	results = []
	for line in cursor:
		responses.append(line)
	return results

"""
-------------------------------
Questions and answers -general
-------------------------------
"""

def get_question(conn, qid):
	tup = (qid)
	query = "SELECT * FROM question WHERE 'qid' = ?;"
	result = zurueck(conn, query, tup)[0]

#def get_question_answers(conn,qid):

#def 

"""
-------------------------------
Questions and answers -user-specific
-------------------------------
"""