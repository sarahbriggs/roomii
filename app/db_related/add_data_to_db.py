import sqlite3
import xml.etree.ElementTree as ET
import useful_operations

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
	useful_operations.new_review(conn, reviewer, reviewed, text, overall, cleanliness, friendliness, conscientiousness, "0") #0 is placeholder for self report accuray-prob shoudln't be tehre


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
'''
contacttree = ET.parse('../../data/contact.xml')
contactroot = contacttree.getroot()
for contact in contactroot.iter(tag = "contact"):
	netid = contact.find("netid")
	email = contact.find("email")
	phone = contact.find("phone")
	useful_operations.net_contact(conn, netid, phone, email)


#friends

#requests first
requeststree = ET.parse('../../data/requests.xml')
requestsroot = requeststree.getroot()
for request in requestsroot.iter(tag = "request"):
	sender = request.find("sender")
	recipient = request.find("recipient")
	useful_operations.friend_request(conn, sender, recipient)

friendtree = ET.parse('../../data/friends.xml')
friendroot = friendtree.getroot()
ctr = 0
for friend in friendroot.iter(tag = "friend"):
	user1 = friend.find("user1")
	user2 = friend.find("user2")
	useful_operations.friend_request(conn, user1, user2)
	if (ctr%2 == 0):
		useful_operations.request_accepted(conn, user1, user2)
	else:
		user_operations.request_rejected(conn, user1, user2)
'''
print("done")

