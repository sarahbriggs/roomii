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

def get_question_text(conn, qid): # return (question_content)
	tup = (qid,)
	query = "SELECT question_content FROM questions WHERE qid = ?"
	result = execute_query(conn, query, tup) #execute query will return a list of matching rows
	return result

def get_answer_text(conn, qid, answer_id): # return (answer_content)
	tup = (qid, answer_id, )
	query = "SELECT answer_content FROM answer_text WHERE qid = ? AND answer_id = ?"
	result = execute_query(conn, query, tup)
	return result

def get_questions_for_category(conn, category_number): # return (qid, question_content)
	tup = (category_number,)
	query = "SELECT qid, question_content FROM questions WHERE category_number = ?"
	result = execute_query(conn, query, tup)
	return result

"""
-------------------------------
Questions and answers -user response
-------------------------------
"""

def get_user_answer_for_question(conn, netid, qid): # return (answer_id, weight)
	tup = (netid, qid, )
	query = "SELECT answer_id, weight FROM answer WHERE nedid = ? AND qid = ?"
	result = execute_query(conn, query, tup)
	return result

def get_similarities(conn, netid1, netid2): # return (qid, a1.answer_id, a1.weight, a2.weight)
	tup = (netid1, netid2,)
	query = "SELECT a1.qid, a1.answer_id, a1.weight, a2.weight FROM answer a1, answer a2 WHERE a1.netid = ? AND a2.netid = ? AND a1.qid = a2.qid AND a1.answer_id = a2.answer_id"
	result = execute_query(conn, query, tup)
	print(result)
	return result

def get_differences(conn, netid1, netid2): # return (qid, a1.answer_id, a1.weight, a2.answer_id, a2.weight)
	tup = (netid1, netid2, )
	query = "SELECT a1.qid, a1.answer_id, a1.weight, a2.answer_id, a2.weight FROM answer a1, answer a2 WHERE a1.netid = ? AND a2.netid = ? AND a1.qid = a2.qid AND a1.answer_id <> a2.answer_id"
	result = execute_query(conn, query, tup)
	print(result)
	return result

def get_answer(conn, netid): # return (qid, answer_id, weight)
	tup = (netid,)
	query = "SELECT qid, answer_id, weight FROM answer WHERE netid = ?"
	result = execute_query(conn, query, tup)
	print(result)
	return result

"""
-------------------------------
User Information
-------------------------------
"""

def get_user_info_friends(conn, netid): # return (netid, given_name, family_name, profpic, description, status, phone, email)
	tup = (netid, )
	query = "SELECT netid, given_name, family_name, profpic, description, status, phone, email FROM users LEFT OUTER JOIN contact ON users.netid = contact.netid AND users.netid = ?"
	result = execute_query(conn, query, tup)
	print(result)
	return result

def get_user_info_general(conn, netid): # return (netid, given_name, family_name, profpic, description, status)
	tup = (netid, )
	query = "SELECT * FROM users WHERE netid = ?"
	result = execute_query(conn, query, tup)
	print(result)
	return result

def get_user_rating(conn, netid): # return (netid, overall_rating, clealiness, friendliness, conscientiousness, self_report_accuracy, number_of_reports)
	tup = (netid, )
	query = "SELECT * FROM ratings WHERE netid = ?"
	result = execute_query(conn, query, tup)
	return result[0]

"""
-------------------------------
Review
-------------------------------
"""

def get_review(conn, netid1, netid2): # return (reviewer_netid, reviewed_netid, review_text, overall_rating, cleanliness, friendliness, conscientiousness)
	tup = (netid1, netid2, )
	query = "SELECT * FROM review WHERE reviewer_netid = ? AND reviewed_netid = ?"
	result = execute_query(conn, query, tup)
	# print(result)
	return result

def get_number_of_reviews_of_user(conn, netid):
	tup = (netid, )
	query = "SELECT COUNT(*) FROM review WHERE reviewed_netid = ?"
	result = execute_query(conn, query, tup)
	# print(result[0][0])
	return result[0][0]


"""
-------------------------------
Questions and answers -user-specific
-------------------------------
"""

if __name__ == '__main__':
	conn = sqlite3.connect('fakedata.db')
	get_similarities(conn, "rjf19", "zz105")
	get_differences(conn, "dummy", "rjf19")
	get_answer(conn, "dummy")
	print(get_question_text(conn,0))
	print(get_answer_text(conn, 0, 0))
	get_questions_for_category(conn,0)

