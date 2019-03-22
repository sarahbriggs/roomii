import sqlite3

#so wheras useful_operations.py has lots of insertions n stuff, this one will be used to get info

def execute_query(conn, query, tup): 
	cursor = conn.cursor()
	cursor.execute(query, tup)
	conn.commit()
	results = []
	for line in cursor:
		results.append(line)
	cursor.close()
	return results

"""
-------------------------------
Questions and answers -general
-------------------------------
"""

def get_question(conn, qid):
	tup = (qid,)
	query = "SELECT * FROM questions WHERE qid = ?"
	result = execute_query(conn, query, tup)
	print(result)

"""
-------------------------------
User Information
-------------------------------
"""

def get_user_info_friends(conn, netid):
	tup = (netid, )
	query = "SELECT * FROM users LEFT OUTER JOIN contact ON users.netid = contact.netid AND users.netid = ?"
	result = execute_query(conn, query, tup)
	print(result)

def get_user_info_general(conn, netid):
	tup = (netid, )
	query = "SELECT * FROM users WHERE netid = ?"
	result = execute_query(conn, query, tup)
	print(result)

def get_user_rating(conn, netid):
	tup = (netid, )
	query = "SELECT * FROM ratings WHERE netid = ?"
	result = execute_query(conn, query, tup)

"""
-------------------------------
Review
-------------------------------
"""

def get_review(conn, netid1, netid2):
	tup = (netid1, netid2, )
	query = "SELECT * FROM review WHERE reviewer_netid = ? AND reviewed_netid = ?"
	result = execute_query(conn, query, tup)
	print(result)

#def get_question_answers(conn,qid):

#def 

"""
-------------------------------
Questions and answers -user-specific
-------------------------------
"""

if __name__ == '__main__':
	conn = sqlite3.connect('fakedata.db')
	get_user_info_general(conn, "rjf19")
	get_review(conn, "zz105", "rjf19")

