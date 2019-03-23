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

def get_question_text(conn, qid):
	tup = (qid,)
	query = "SELECT * FROM questions WHERE qid = ?"
	result = execute_query(conn, query, tup)
	print(result)

def get_answer_text(conn, qid, answer_id):
	tup = (qid, answer_id, )
	query = "SELECT * FROM answer_text WHERE qid = ? AND answer_id = ?"
	result = execute_query(conn, query, tup)

def get_questions_for_category(conn, category_number):
	tup = (category_number,)
	query = "SELECT * FROM questions WHERE category_number = ?"
	result = execute_query(conn, query, tup)

"""
-------------------------------
Questions and answers -user response
-------------------------------
"""

def get_user_answer_for_question(conn, netid, qid):
	tup = (netid, qid, )
	query = "SELECT * FROM answer WHERE nedid = ? AND qid = ?"
	result = execute_query(conn, query, tup)

def get_similarities(conn, netid1, netid2):
	tup = (netid1, netid2,)
	query = "SELECT * FROM answer a1, answer a2 WHERE a1.netid = ? AND a2.netid = ? AND a1.qid = a2.qid AND a1.answer_id = a2.answer_id"
	result = execute_query(conn, query, tup)

def get_differences(conn, netid1, netid2):
	tup = (netid1, netid2, )
	query = "SELECT * FROM answer a1, answer a2 WHERE a1.netid = ? AND a2.netid = ? AND a1.qid = a2.qid AND a1.answer_id <> a2.answer_id"
	result = execute_query(conn, query, tup)

def get_answer(conn, netid):
	tup = (netid,)
	query = "SELECT * FROM answers WHERE netid = ?"
	result = execute_query(conn, query, tup)

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

