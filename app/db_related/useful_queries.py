import sqlite3
#so wheras useful_operations.py has lots of insertions n stuff, this one will be used to get info

def execute_query(conn, query, tup = None): 
	cursor = conn.cursor()
	if tup:
		cursor.execute(query, tup)
	else:
		cursor.execute(query)
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

def get_question_text(conn, qid): # return (question_content)
	tup = (qid,)
	query = "SELECT question_content FROM questions WHERE qid = ?"
	result = execute_query(conn, query, tup) #execute query will return a list of matching rows
	return result[0][0]

def get_all_qid(conn): # return a list of all qid
	tup = (None)
	query = "SELECT qid FROM questions"
	result = execute_query(conn, query, tup) #execute query will return a list of matching rows
	return result

def get_answer_text(conn, qid, answer_id): # return (answer_content)
	tup = (qid, answer_id, )
	query = "SELECT answer_content FROM answer_text WHERE qid = ? AND answer_id = ?"
	result = execute_query(conn, query, tup)
	return result[0][0]
def get_all_answer_text(conn, qid):
	tup = (qid,)
	query = "SELECT answer_content FROM answer_text WHERE qid = ?"
	result = execute_query(conn, query, tup)
	return result

def get_questions_for_category(conn, category_number): # return (qid, question_content)
	tup = (category_number,)
	query = "SELECT qid, question_content FROM questions WHERE category_number = ?"
	result = execute_query(conn, query, tup)
	return result

def num_questions(conn):
	query = "SELECT count(qid) FROM questions;"
	results = execute_query(conn,query)
	return results[0][0]

def still_has_questions(conn, netid): #true if netid still has unanswered questions
	num = num_questions(conn)
	tup = (netid,)
	query = "SELECT * FROM answer WHERE netid = ?"
	result = execute_query(conn,query,tup)
	return num != len(result)


"""
-------------------------------
Questions and answers -user response
-------------------------------
"""

def get_user_answer_for_question(conn, netid, qid): # return (answer_id, weight)
	tup = (netid, qid, )
	query = "SELECT answer_id, weight FROM answer WHERE netid = ? AND qid = ?"
	result = execute_query(conn, query, tup)
	return result

def get_similarities(conn, netid1, netid2): # return (qid, a1.answer_id, a1.weight, a2.weight)
	tup = (netid1, netid2,)
	query = "SELECT a1.qid, a1.answer_id, a1.weight, a2.weight FROM answer a1, answer a2 WHERE a1.netid = ? AND a2.netid = ? AND a1.qid = a2.qid AND a1.answer_id = a2.answer_id"
	result = execute_query(conn, query, tup)
	return result

def get_differences(conn, netid1, netid2): # return (qid, a1.answer_id, a1.weight, a2.answer_id, a2.weight)
	tup = (netid1, netid2, )
	query = "SELECT a1.qid, a1.answer_id, a1.weight, a2.answer_id, a2.weight FROM answer a1, answer a2 WHERE a1.netid = ? AND a2.netid = ? AND a1.qid = a2.qid AND a1.answer_id <> a2.answer_id"
	result = execute_query(conn, query, tup)
	return result

def get_answer(conn, netid): # return (qid, answer_id, weight)
	tup = (netid,)
	query = "SELECT qid, answer_id, weight FROM answer WHERE netid = ?"
	result = execute_query(conn, query, tup)
	if (len(result) < 1):
		return False
	return result



"""
-------------------------------
User Information
-------------------------------
"""

def get_user_info_friends(conn, netid): # return (netid, given_name, family_name, profpic, description, status, phone, email)
	tup = (netid, )
	query = "SELECT users.netid, given_name, family_name, profpic, description, status, phone, email FROM users LEFT OUTER JOIN contact ON users.netid = contact.netid WHERE users.netid = ?"
	result = execute_query(conn, query, tup)
	if (len(result) < 1):
		return False
	return result[0]

def get_user_info_general(conn, netid): # return (netid, given_name, family_name, profpic, description, status)
	tup = (netid, )
	query = "SELECT * FROM users WHERE netid = ?"
	result = execute_query(conn, query, tup)
	return result

def get_user_rating(conn, netid): # return (netid, overall_rating, clealiness, friendliness, conscientiousness, self_report_accuracy, number_of_reports)
	tup = (netid, )
	query = "SELECT * FROM ratings WHERE netid = ?"
	result = execute_query(conn, query, tup)
	if (len(result) < 1):
		return False
	return result[0]

def get_user_password(conn, netid):
	tup = (netid, )
	query = "SELECT pass FROM password WHERE netid = ?"
	result = execute_query(conn, query, tup)
	if len(result) < 1:
		return False # return false when user does not exist
	else:
		return result[0][0]

def are_friends(conn, netid1, netid2):
	tup = (netid1, netid2, )
	query = "SELECT * FROM friends WHERE netid1 = ? AND netid2 = ?"
	result = execute_query(conn, query, tup)
	if len(result) < 1:
		return False
	val = result[0][2]
	if val != 1:
		return False
	return True

"""
-------------------------------
Review
-------------------------------
"""
def get_review_of_user(conn, netid2): # return (reviewer_netid, reviewed_netid, review_text, overall_rating, cleanliness, friendliness, conscientiousness)
	tup = (netid2, )
	query = "SELECT * FROM review WHERE reviewed_netid = ?"
	result = execute_query(conn, query, tup)
	if (len(result) < 1):
		return False
	return result

def get_review(conn, netid1, netid2): # return (reviewer_netid, reviewed_netid, review_text, overall_rating, cleanliness, friendliness, conscientiousness)
	tup = (netid1, netid2, )
	query = "SELECT * FROM review WHERE reviewer_netid = ? AND reviewed_netid = ?"
	result = execute_query(conn, query, tup)
	return result

def get_number_of_reviews_of_user(conn, netid):
	tup = (netid, )
	query = "SELECT COUNT(*) FROM review WHERE reviewed_netid = ?"
	result = execute_query(conn, query, tup)
	return result[0][0]


"""
-------------------------------
Questions and answers -user-specific
-------------------------------
"""



def pic_name(conn, netid):
	tup = (netid,)
	query = "SELECT profpic FROM user WHERE netid = ?"
	result = execute_query(conn,query,tup)
	return result[0][0]


"""
-------------------------------
Other
-------------------------------
"""

def were_roommates(conn, netid1, netid2):
	tup = (netid1, netid2)
	query = "SELECT * FROM roommate WHERE netid1 = ? AND netid2 = ?"
	result = execute_query(conn, query, tup)
	if len(result) < 1:
		return False
	return True

