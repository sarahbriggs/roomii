import sqlite3

def weiter(conn, query, tup):
	cursor = conn.cursor()
	cursor.execute(query, tup)
	conn.commit()
	cursor.close()

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

def still_has_questions(conn, netid): #true if netid still has unanswered questions
	num = num_questions(conn)
	tup = (netid,)
	query = "SELECT * FROM answer WHERE netid = ?"
	# print(query,tup)
	result = execute_query(conn,query,tup)
	return num != len(result)

def num_questions(conn):
	query = "SELECT qid FROM questions;"
	results = execute_query(conn,query)
	ct = 0
	for line in results:
		ct+=1
	return ct

'''
-------------------------------
User creation and editing
-------------------------------
'''

def new_user(conn, netid, given_name = None, family_name = None, profpic = None, description = None, status = True):
	tup = (netid, given_name, family_name, profpic, description, status) #last one is true because you don't start out banned
	query = "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?);"
	try:
		weiter(conn, query, tup)
		return 1
	except:
		return 0


def new_password(conn, netid, password, salt = None):
	tup = (netid, password, salt,)
	query = "INSERT INTO password VALUES (?, ?, ?)"
	weiter(conn, query, tup)

def ban_user(conn, netid):
	tup = (netid, )
	query = "UPDATE users SET status = False WHERE netid = ?"
	weiter(conn, query, tup)

def edit_user(conn, netid, status, given_name = None, family_name = None, profpic = None, description = None):
	tup = (given_name, family_name, profpic, description, status, netid)
	query = """UPDATE users SET given_name = ?, family_name = ?, profpic = ?, description = ?, status = ?
	WHERE netid = ?"""
	weiter(conn, query, tup)

def new_contact(conn, netid, phone, email):
	tup = (netid, phone, email,)
	query = "INSERT INTO contact VALUES (?, ?, ?)"
	weiter(conn, query, tup)

# 
#def change_password

'''
-------------------------------
social functions
-------------------------------
'''
def update_rating(conn, netid, avg_overall, avg_cleanliness, avg_friendliness, avg_conscientiousness,
	self_report_accuracy, number_of_reports):
	tup = (avg_overall, avg_cleanliness, avg_friendliness, avg_conscientiousness, self_report_accuracy, number_of_reports, netid)
	query = """UPDATE ratings SET avg_overall = ?, cleanliness = ?, friendliness = ?,
	conscientiousness = ?, self_report_accuracy = ?, number_of_reports = ? WHERE netid = ?"""
	weiter(conn, query, tup)

def report_user(conn, reporter_netid, reported_netid, reason):
	tup = (reporter_netid, reported_netid, reason)
	query = "INSERT INTO report VALUES (?, ?, ?);"
	weiter(conn, query, tup)
	current_rating = get_user_rating(conn, reported_netid)
	update_rating(conn, current_rating[0], current_rating[1], current_rating[2], current_rating[3],
		current_rating[4], current_rating[5], current_rating[6] + 1)

def block_user(conn, blocker_netid, blocked_netid):
	tup = (blocker_netid, blocked_netid)
	query = "INSERT INTO blocked VALUES (?, ?);"
	weiter(conn, query, tup)
	return True

def unblock_user(conn, unblocker_netid, unblocked_netid):
	tup = (unblocker_netid, unblocked_netid)
	query = "DELETE FROM blocked WHERE blocker_netid = ? AND blocked_netid = ?);"
	weiter(conn, query, tup)
	return True

def recommend_user(conn, recommender_netid, recommendee_netid, recommended__netid, reason):
	tup = (recommender_netid, recommendee_netid, recommended__netid, reason)
	query = "INSERT INTO recommend VALUES (?, ?, ?, ?);"
	weiter(conn, query, tup)


def new_review(conn, reviewer_netid, reviewed_netid, text, overall_rating, cleanliness, 
	friendliness, conscientiousness, self_report_accuracy):
	overall_rating = float(overall_rating)
	cleanliness = float(cleanliness)
	friendliness = float(friendliness)
	conscientiousness = float(conscientiousness)
	self_report_accuracy = float(self_report_accuracy)
	tup = (reviewer_netid, reviewed_netid, text, overall_rating, cleanliness, 
	friendliness, conscientiousness, self_report_accuracy)
	query = "INSERT INTO review VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
	number_of_reviews = get_number_of_reviews_of_user(conn, reviewed_netid)
	weiter(conn, query, tup)
	if number_of_reviews == 0:
		create_rating(conn, reviewed_netid, overall_rating, cleanliness, friendliness, 
			conscientiousness, self_report_accuracy, 0)
	else:
		current_rating = get_user_rating(conn, reviewed_netid)
		new_overall = (current_rating[1] * number_of_reviews + float(overall_rating)) / (number_of_reviews + 1)
		new_cleanliness = (current_rating[2] * number_of_reviews + float(cleanliness)) / (number_of_reviews + 1)
		new_friendliness = (current_rating[3] * number_of_reviews + float(friendliness)) / (number_of_reviews + 1)
		new_cons = (current_rating[4] * number_of_reviews + float(conscientiousness)) / (number_of_reviews + 1)
		new_self_report = (current_rating[5] * number_of_reviews + float(self_report_accuracy)) / (number_of_reviews + 1)
		update_rating(conn, reviewed_netid, new_overall, new_cleanliness, new_friendliness,
			new_cons, new_self_report, current_rating[6])

def create_rating(conn, netid, avg_overall, avg_cleanliness, avg_friendliness, avg_conscientiousness, 
	self_report_accuracy, number_of_reports): # do we need this? isn't this included in new review?
	#todo: when this is called, reaggregate rating
	tup = (netid, avg_overall, avg_cleanliness, avg_friendliness, 
		avg_conscientiousness, self_report_accuracy, number_of_reports) 
	query = "INSERT INTO ratings VALUES (?, ?, ?, ?, ?, ?, ?);"
	weiter(conn, query, tup)

def check_friends(conn, sender, recipient):
	tup = (sender, recipient, 1)
	query = "SELECT COUNT(*) FROM friends WHERE netid1 = ? and netid2 = ? and status = ? GROUP BY netid1;"
	val = execute_query(conn, query, tup)
	if len(val) == 0: 
		return False
	elif val[-1]==1:
		return True
	else:
		return False

def friend_request(conn, sender, recipient):
	alreadyFriends = check_friends(conn, sender, recipient)
	if not alreadyFriends: 
		tup = (sender, recipient, 0)
		query = "INSERT INTO friends VALUES (?,?,?);"
		weiter(conn, query, tup)
		return True

def request_accepted(conn, sender, recipient):
	tup1 = (1, sender, recipient)
	tup2 = (recipient, sender, 1)
	query = "UPDATE friends SET status = ? WHERE netid1 = ? AND netid2 = ?"
	weiter(conn,query, tup1)
	query = "INSERT INTO friends VALUES (?,?,?);"
	weiter(conn,query, tup2)

def request_rejected(conn,sender,recipient):
	tup1 = (-1, sender, recipient)
	tup2 = (recipient, sender, -1)
	query = "UPDATE friends SET status = ? WHERE netid1 = ? AND netid2 = ?"
	weiter(conn,query, tup1)
	query = "INSERT INTO friends VALUES (?,?,?);"
	weiter(conn,query, tup2)

def calculate_matchup(conn, matcher, matchee):
	tup1 = (matcher,)
	tup2 = (matchee,)
	query = "SELECT answer_id,weight FROM answer WHERE netid = ?;"

	res1 = execute_query(conn,query,tup1)
	res2 = execute_query(conn,query,tup2)
	if still_has_questions(conn,matchee):
		return -100
	total = 0
	if res1[0][0]!=res2[0][0]:
		return -100

	for i in range(len(res1)):
		ans1 = res1[i][0]
		ans2 = res2[i][0]
		imp = res1[i][1]
		b = 0
		if ans1 == ans2:
			b = 1
		else:
			b = -1
		total += b*imp
	return total

def all_matchups(conn,netid):
	tup1 = (netid,)
	query0 = "DELETE FROM matchups WHERE netid1 = ?;"
	query = "SELECT netid FROM users WHERE netid != ?;"
	query2 = "INSERT INTO matchups VALUES (?, ?, ?);"
	cursor = conn.cursor() #we're going to do this one-at-a-time
	cursor2 = conn.cursor()
	cursor.execute(query0,tup1)
	cursor.execute(query,tup1)
	tk = 0
	for user in cursor:
		matchup = calculate_matchup(conn, netid, user[0])
		tup2 = (netid, user[0], matchup)
		cursor2.execute(query2, tup2)
		tk += 1
	cursor.close()
	cursor2.close()
	conn.commit()
	return tk

def get_matchups(conn, netid, num = 20):
	# allMatchups = all_matchups(conn, netid)
	tup = (netid, num,)
	cursor = conn.cursor()
	query = "SELECT DISTINCT * FROM matchups WHERE netid1 = ? ORDER BY matchRating DESC, netid2 ASC LIMIT ?;"
	return execute_query(conn, query, tup)


def add_roommates(conn, netid1, netid2):
	tup = (netid1, netid2)
	query = "INSERT INTO roommate VALUES (?, ?);"
	weiter(conn, query, tup)
	return True

def were_roommates(connn, netid1, netid2):
	tup = (netid1, netid2)
	query = "SELECT * FROM roommate WHERE netid1 = ? AND netid2 = ?"
	result = execute_query(conn, query, tup)
	if len(result) < 1:
		return False
	return True


'''
-------------------------------
Questions and answers
-------------------------------
'''
def new_question(conn, qid, category_number, question_content):
	tup = (qid, category_number, question_content)
	query = "INSERT INTO questions VALUES (?, ?, ?);"
	weiter(conn, query, tup)

def new_answer_text(conn, qid, answer_id, text):
	tup = (qid, answer_id, text)
	query = "INSERT INTO answer_text VALUES (?, ?, ?);"
	weiter(conn, query, tup)

def answer_question(conn, netid, qid, answer_id, weight):
	tup = (netid, qid, answer_id, weight)
	query = "INSERT INTO answer VALUES (?, ?, ?, ?);"
	weiter(conn, query, tup)

def remove_answers(conn, netid):
	tup = (netid, )
	query = "DELETE FROM answer WHERE netid = ?"
	weiter(conn, query, tup)


def change_pic(conn,netid,pic):
	tup = (pic, netid)
	query = "UPDATE user SET profpic = ? WHERE netid = ?;"
	weiter(conn, query, tup)

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

