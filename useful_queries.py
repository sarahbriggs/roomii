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

def get_user_info_general(netid):
	#

def get_user_info_friend(netid):
	#

def get_user_rating(netid):
	#

def get_review(reviewer_netid, reviewed_netid):
	#

def get_all_reviews(reviewed_netid):
	#

def get_answers(netid):
	#

def get_similarities(netid_1, netid_2):
	#

def get_differences(netid_1, netid_2):
	#

def get_question_text(qid):
	#

def get_answer_text(qid, answer_id):
	#

def get_user_answer_for_question(netid, qid):
	#


