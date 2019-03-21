import sqlite3

def weiter(conn, query, tup):
	cursor = conn.cursor()
	cursor.execute(query, tup)
	conn.commit()
	cursor.close()

'''
-------------------------------
User creation and editing
-------------------------------
'''

def new_user(conn, netid, given_name = None, family_name = None, profpic = None, description = None):
	tup = (netid, given_name, family_name, profpic, description, False) #last one is false because you don't start out banned
	query = "INSERT INTO users VALUES (?, ?, ?, ?, ?);"
	weiter(conn, query, tup)

#def ban_user

#def edit_user

#def change_password

'''
-------------------------------
social functions
-------------------------------
'''
def report_user(conn, reporter_netid, reported_netid, reason):
	tup = (reporter_netid, reported_netid, reason)
	query = "INSERT INTO report VALUES (?, ?, ?);"
	weiter(conn, query, tup)

def recommend_user(conn, recommender_netid, recommendee_netid, recommended__netid, reason):
	tup = (recommender_netid, recommendee_netid, recommended__netid, reason)
	query = "INSERT INTO recommend VALUES (?, ?, ?, ?);"
	weiter(conn, query, tup)


def new_review(conn, reviewer_netid, reviewed_netid, text, overall_rating, cleanliness, 
	friendliness, conscientiousness):
	tup = (reviewer_netid, reviewed_netid, text, overall_rating, cleanliness, 
	friendliness, conscientiousness)
	query = "INSERT INTO review VALUES (?, ?, ?, ?, ?, ?, ?);"
	weiter(conn, query, tup)

def create_rating(conn, netid, avg_overall, avg_cleanliness, avg_friendliness, avg_conscientiousness, 
	self_report_accuracy, number_of_reports):
	#todo: when this is called, reaggregate rating
	tup = (netid, avg_overall, avg_cleanliness, avg_friendliness, 
		avg_conscientiousness, self_report_accuracy, number_of_reports) 
	query = "INSERT INTO ratings VALUES (?, ?, ?, ?, ?, ?, ?);"
	weiter(conn, query, tup)

def friend_request(conn, sender, recipient):
	tup = (sender, recipient, 0)
	query = "INSERT INTO friends VALUES (?,?,?);"
	weiter(conn,query,tup)

def request_accepted(conn, sender, recipient):
	tup1 = (1, sender, recipient)
	tup2 = (recipient, sender, 1)
	query = "UPDATE friends SET status = ? WHERE netid1 = ? AND netid2 = ?"
	weiter(conn,query, tup1)
	query = "INSERT INTO friends VALUES (?,?,?);"
	weiter(conn,query, tup2)
#def request_rejected


'''
-------------------------------
Questions and answers
-------------------------------
'''
def new_question(conn, qid, question_content):
	tup = (qid, question_content)
	query = "INSERT INTO questions VALUES (?, ?);"
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
	conn = sqlite3.connect('fakedata.db')
	new_user(conn, "rjf19", "Ryan", "Ferner", "lolidk.png", "i'm just tryna find a roomie lol")
	# new_user(conn, "seb103", "Sarah", profpic = "same.png")
	# report_user(conn,"rjf19","seb103","my code is sinful and i deserve to be reported")
	new_question(conn, 0, "from time to time, when it's really cold outside, do you or do you not want to breathe really heavily and pretend that you're a train?")
	new_answer_text(conn, 0, 0, "absolutely")
	new_answer_text(conn, 0, 1, "lolno why")
	answer_question(conn, "rjf19", 0, 1, 5)

