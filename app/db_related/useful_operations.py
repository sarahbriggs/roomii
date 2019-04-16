import sqlite3
# from useful_queries import execute_query, still_has_questions



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
	weiter(conn, query, tup)

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
	current_rating = useful_queries.get_user_rating(conn, reported_netid)
	update_rating(conn, current_rating[0], current_rating[1], current_rating[2], current_rating[3],
		current_rating[4], current_rating[5], current_rating[6] + 1)


def recommend_user(conn, recommender_netid, recommendee_netid, recommended__netid, reason):
	tup = (recommender_netid, recommendee_netid, recommended__netid, reason)
	query = "INSERT INTO recommend VALUES (?, ?, ?, ?);"
	weiter(conn, query, tup)


def new_review(conn, reviewer_netid, reviewed_netid, text, overall_rating, cleanliness, 
	friendliness, conscientiousness, self_report_accuracy):
	tup = (reviewer_netid, reviewed_netid, text, overall_rating, cleanliness, 
	friendliness, conscientiousness, self_report_accuracy)
	query = "INSERT INTO review VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
	number_of_reviews = useful_queries.get_number_of_reviews_of_user(conn, reviewed_netid)
	weiter(conn, query, tup)
	if number_of_reviews == 0:
		create_rating(conn, reviewed_netid, overall_rating, cleanliness, friendliness, 
			conscientiousness, self_report_accuracy, 0)
	else:
		current_rating = useful_queries.get_user_rating(conn, reviewed_netid)
		new_overall = (current_rating[1] * number_of_reviews + overall_rating) / (number_of_reviews + 1)
		new_cleanliness = (current_rating[2] * number_of_reviews + cleanliness) / (number_of_reviews + 1)
		new_friendliness = (current_rating[3] * number_of_reviews + friendliness) / (number_of_reviews + 1)
		new_cons = (current_rating[4] * number_of_reviews + conscientiousness) / (number_of_reviews + 1)
		new_self_report = (current_rating[5] * number_of_reviews + self_report_accuracy) / (number_of_reviews + 1)
		update_rating(conn, reviewed_netid, new_overall, new_cleanliness, new_friendliness,
			new_cons, new_self_report, current_rating[6])

def create_rating(conn, netid, avg_overall, avg_cleanliness, avg_friendliness, avg_conscientiousness, 
	self_report_accuracy, number_of_reports): # do we need this? isn't this included in new review?
	#todo: when this is called, reaggregate rating
	tup = (netid, avg_overall, avg_cleanliness, avg_friendliness, 
		avg_conscientiousness, self_report_accuracy, number_of_reports) 
	query = "INSERT INTO ratings VALUES (?, ?, ?, ?, ?, ?, ?);"
	weiter(conn, query, tup)

def friend_request(conn, sender, recipient):
	tup = (sender, recipient, 0)
	query = "INSERT INTO friends VALUES (?,?,?);"
	weiter(conn, query, tup)

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
		return None
	total = 0
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
	query = "SELECT netid FROM users WHERE netid != ?;"
	query2 = "INSERT INTO matchups VALUES (?, ?, ?);"
	cursor = conn.cursor(); #we're going to do this one-at-a-time
	cursor2 = conn.cursor()
	cursor.execute(query,tup1)
	tk = 0
	for user in cursor:
		matchup = calculate_matchup(conn, netid, user[0])
		tup2 = (netid, user[0], matchup)
		cursor2.execute(query2, tup2)
		print (tup2)
		tk += 1
	cursor.close()
	cursor2.close()
	conn.commit()
	return tk


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

# def 


if __name__ == '__main__':
	import useful_queries
	conn = sqlite3.connect('fakedata.db')
	conn.execute("PRAGMA foreign_keys = 1")
	try:
		new_user(conn, "rjf19", "Ryan", "Ferner", "lolidk.png", "i'm just tryna find a roomie lol", True)
		# new_user(conn, "seb103", "Sarah", profpic = "same.png")
		# report_user(conn,"rjf19","seb103","my code is sinful and i deserve to be reported")
		new_user(conn, "zz105", "Zhiyuan", None, "haha", "haha", True)
		new_user(conn, "dummy", "Im", "Dummy", "dum", "dum", True)
		new_question(conn, 0, 0, "from time to time, when it's really cold outside, do you or do you not want to breathe really heavily and pretend that you're a train?")
		new_answer_text(conn, 0, 0, "absolutely")
		new_answer_text(conn, 0, 1, "lolno why")
		answer_question(conn, "rjf19", 0, 1, 5)
		answer_question(conn, "zz105", 0, 1, 5)
		answer_question(conn, "dummy", 0, 2, 5)
		new_review(conn, "zz105", "rjf19", "good!", 5, 5, 5, 5, 5)
		new_review(conn, "rjf19", "zz105", "good!", 5, 5, 5, 5, 5)
		new_review(conn, "dummy", "zz105", "bad", 0, 0, 0, 0, 0)
	except:
		pass
	print(all_matchups(conn, "rjf19"))
