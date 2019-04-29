import sqlite3
import xml.etree.ElementTree as ET
import useful_operations
import useful_queries as uq 
import cheapSecurity as sec


conn = sqlite3.connect('fakedata.db')

print("start")

answerstexttree = ET.parse('../../data/answers.xml')
answerstextroot = answerstexttree.getroot()
for answer in answerstextroot.iter(tag = "answer"):
	qid = answer.find("qid").text
	aid = answer.find("answer_id").text
	text = answer.find("text").text
	#print(qid)
	#print(aid)
	#print(text)
	useful_operations.new_answer_text(conn, qid, aid, text)
	#print("one answer done")


questionstree = ET.parse('../../data/questions.xml')
questionsroot = questionstree.getroot()
for question in questionsroot.iter(tag = "question"):
	qid = question.find("qid").text
	category_number = question.find("category_number").text
	question_content = question.find("question_content").text
	useful_operations.new_question(conn, qid, category_number, question_content)


userstree = ET.parse('../../data/users.xml')
usersroot = userstree.getroot()
for user in usersroot.iter(tag = "user"):
	netid = user.find("netid").text
	given_name = user.find("given_name").text
	family_name = user.find("family_name").text
	prof_pic = user.find("prof_pic").text
	description = user.find("description").text
	#no status since just set to true
	useful_operations.new_user(conn, netid, given_name, family_name, prof_pic, description)

#a super user that is friends with everyone else
sup_netid = "sup123"
useful_operations.new_user(conn, sup_netid, "super", "user", "", "placeholder")
for user in usersroot.iter(tag = "user"):
	netid = user.find("netid").text
	useful_operations.add_roommates(conn, sup_netid, netid)
	useful_operations.add_roommates(conn, netid, sup_netid)

sec.register(conn, netid, "mypassword")

#all answers are 1???
answerstree = ET.parse('../../data/user_answers.xml')
answersroot = answerstree.getroot()
for answer in answersroot.iter(tag = "answer"):
	netid = answer.find("netid").text
	qid = answer.find("qid").text
	aid = answer.find("answer_id").text
	weight = answer.find("weight").text
	useful_operations.answer_question(conn, netid, qid, aid, weight)


#dont do this, ratings updated through new added reviews
'''
ratingstree = ET.parse('../../data/ratings.xml')
ratingsroot = ratingstree.getroot()2
for rating in ratingsroot.iter(tag = "rating"):
	netid = rating.find("netid").text
	overall_rating = rating.find("overall_rating").text
	cleanliness = rating.find("cleanliness").text
	friendliness = rating.find("friendliness").text
	conscientiousness = rating.find ("conscientiousness").text
	accuracy = rating.find ("self_report_accuracy").text
	times = rating.find("number_of_reports").text
	print(netid)
	print(overall_rating)
	print(cleanliness)
	print(friendliness)
	print(conscientiousness)
	print(accuracy)
	print(times)
	useful_operations.create_rating(conn, netid, overall_rating, cleanliness, friendliness, conscientiousness, accuracy, times)
'''

recommendtree = ET.parse('../../data/recommends.xml')
recommendroot = recommendtree.getroot()
for recommend in recommendroot.iter(tag = "recommend"):
	recommender = recommend.find("recommender_netid").text
	recommendee = recommend.find("recommendee_netid").text
	recommended = recommend.find("recommended_netid").text
	reason = recommend.find("reason").text
	print(recommender)
	print(recommendee)
	print(recommended)
	print(reason)
	useful_operations.recommend_user(conn, recommender, recommendee, recommended, reason)


#inserting should be working, but not sure about the useful queries reference in useful_operations
'''
reporttree = ET.parse('../../data/reports.xml')
reportroot = reporttree.getroot()
for report in reportroot.iter(tag = "report"):
	reporter = report.find("reporter_netid").text
	reported = report.find("reported_netid").text
	reason = report.find("reason").text
	useful_operations.report_user(conn, reporter, reported, reason)
'''

#works with some of the stuff in useful operations commented out
reviewtree = ET.parse('../../data/reviews.xml')
reviewroot = reviewtree.getroot()
for review in reviewroot.iter(tag = "review"):
	reviewer = review.find("reviewer_netid").text
	reviewed = review.find("reviewed_netid").text
	text = review.find("text").text
	overall = review.find("overall_rating").text
	cleanliness = review.find("cleanliness").text
	friendliness = review.find("friendliness").text
	conscientiousness = review.find("conscientiousness").text
	useful_operations.new_review(conn, reviewer, reviewed, text, overall, cleanliness, friendliness, conscientiousness, 0)

# <<<<<<< HEAD
# import useful_queries

# =======

#inserting should be working, but not sure about the useful queries reference in useful_operations
#report after review because it needs calls to get user rating
#useful_queries return result[0] in get_user_rating out of range???
'''
reporttree = ET.parse('../../data/reports.xml')
reportroot = reporttree.getroot()
for report in reportroot.iter(tag = "report"):
	reporter = report.find("reporter_netid").text
	reported = report.find("reported_netid").text
	reason = report.find("reason").text
	useful_operations.report_user(conn, reporter, reported, reason)
'''

#contacts

# contacttree = ET.parse('../../data/contact.xml')
# contactroot = contacttree.getroot()
# for contact in contactroot.iter(tag = "contact"):
# 	netid = contact.find("netid").text
# 	email = contact.find("email").text
# 	phone = contact.find("phone").text
# 	useful_operations.new_contact(conn, netid, phone, email)


# #friends

# #requests first
# requeststree = ET.parse('../../data/requests.xml')
# requestsroot = requeststree.getroot()
# for request in requestsroot.iter(tag = "request"):
# 	sender = request.find("sender").text
# 	recipient = request.find("recipient").text
# 	useful_operations.friend_request(conn, sender, recipient)

# friendtree = ET.parse('../../data/friends.xml')
# friendroot = friendtree.getroot()
# ctr = 0
# for friend in friendroot.iter(tag = "friend"):
# 	user1 = friend.find("user1").text
# 	user2 = friend.find("user2").text
# 	useful_operations.friend_request(conn, user1, user2)
# 	if (ctr%2 == 0):
# 		useful_operations.request_accepted(conn, user1, user2)
# 	else:
		# user_operations.request_rejected(conn, user1, user2)

print("done")

# conn = sqlite3.connect('fakedata.db')
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
# print(all_matchups(conn, "rjf19"))

# conn = sqlite3.connect('./fakedata.db')
try:
	sec.register(conn,"rjf19", "password")
except:
	pass
print(sec.validate(conn,"rjf19","password"))

print("done")
