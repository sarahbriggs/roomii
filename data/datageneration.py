#import statements
import xml.etree.ElementTree as ET
import random
################
#Name Generation
################
names = open("nameslist.txt", "w")
first = open("firstnamelist.txt", "r")
last = open("lastnamelist.txt", "r")

firstlines = first.readlines()
lastlines = last.readlines()

for i in range(0,len(firstlines)):
	for j in range(0,len(lastlines)):
		names.write(firstlines[i].strip() + " " + lastlines[j].strip() + "\n")
names.close()
first.close()
last.close()

########################
#creating ratings relation
########################

names = open("nameslist.txt", "r")
nameslist = names.readlines()
names.close()
ratings_root = ET.Element("ratings")
#netids will include initials plus number so we can create list of tuples where we record current number
netids = []
for i in range(0, len(nameslist)):
	#generate netid 
	name = nameslist[i]
	netid = name.split()[0][0] + name.split()[1][0]
	num = 1
	initialExists = False
	#choosing number at end of initials- start from 1
	for n_id in netids:
		if (n_id[0] == netid):
			num = n_id[1] + 1
			n_id[1] = num
			initialExists = True
	netid += str(num)
	if (not initialExists):
		netids.append([netid, 1])
	#create subelement = one for each person
	ET.SubElement(ratings_root, netid)	
	#generate cleanliness
	cleanliness = random.randint(0, 6)
	#generate friendliness
	friendliness = random.randint(0,6)
	#generate conscientiousness
	conscientiousness = random.randint(0,6)
	#self-report accuracy andd num times reported maybe generated later so just assign 0?
	accuracy = 0
	times_reported = 0
	#overall rating
	overall = round((cleanliness + friendliness + conscientiousness)/3, 2)
	person = ET.SubElement(ratings_root, netid)

	overall_element = ET.Element("overall_rating")
	overall_element.text = str(overall)
	person.insert(0, overall_element)

	cleanliness_element = ET.Element("cleanliness")
	cleanliness_element.text = str(cleanliness)
	person.insert(1, cleanliness_element)

	friendliness_element = ET.Element("friendliness")
	friendliness_element.text = str(friendliness)
	person.insert(2, friendliness_element)

	conscientiousness_element = ET.Element("conscientiousness")
	conscientiousness_element.text = str(conscientiousness)
	person.insert(3, conscientiousness_element)

	accuracy_element = ET.Element("self_report_accuracy")
	accuracy_element.text = str(accuracy)
	person.insert(4, accuracy_element)

	times_reported_element = ET.Element("number_of_reports")
	times_reported_element.text = str(times_reported)
	person.insert(5, times_reported_element)

ratings_tree = ET.ElementTree(ratings_root)
ratings_tree.write("ratings.xml")

####################
#Reviewer Generation
####################

reviews_root = ET.Element("reviews")
for id_initials in netids:
	id_initial = id_initials[0]
	highest = id_initials[1]
	for i in range(1, highest+1):
		reviewer = id_initial+str(i)#each person write a review for random person
		randindex = random.randint(0, len(netids)-1)
		reviewed = netids[randindex][0] + str(random.randint(1,netids[randindex][1]))
		while(reviewer == reviewed): #so we dont get person reviewing themselves
			randindex = random.randint(0, len(netids)-1)
			reviewed = netids[randindex][0] + str(random.randint(1,netids[randindex][1]))
		text = "replace with random text function"
		#generate cleanliness
		cleanliness = random.randint(0, 6)
		#generate friendliness
		friendliness = random.randint(0,6)
		#generate conscientiousness
		conscientiousness = random.randint(0,6)
		overall = round((cleanliness + friendliness + conscientiousness)/3, 2)
		review_element = ET.Element("review")
		reviews_root.insert(i-1, review_element)

		reviewer_element = ET.Element("reviewer_netid")
		reviewer_element.text = reviewer
		review_element.insert(0, reviewer_element)

		reviewed_element = ET.Element("reviewed_netid")
		reviewed_element.text = reviewed
		review_element.insert(1, reviewed_element)

		overall_element = ET.Element("overall_rating")
		overall_element.text = str(overall)
		review_element.insert(2, overall_element)

		cleanliness_element = ET.Element("cleanliness")
		cleanliness_element.text = str(cleanliness)
		review_element.insert(3, cleanliness_element)

		friendliness_element = ET.Element("friendliness")
		friendliness_element.text = str(friendliness)
		review_element.insert(4, friendliness_element)

		conscientiousness_element = ET.Element("conscientiousness")
		conscientiousness_element.text = str(conscientiousness)
		review_element.insert(5, conscientiousness_element)
reviews_tree = ET.ElementTree(reviews_root)
reviews_tree.write("reviews.xml")


##################
#Report Generation
##################
reports_root = ET.Element("reports")
for i in range(0, 1000):
	reporter_index = random.randint(0, len(netids)-1)
	reported_index = random.randint(0, len(netids)-1) 
	while(reporter_index == reported_index):
		reported_index = random.randint(0, len(netids)-1) 
	reporter_initials = netids[reporter_index][0]
	reported_initials = netids[reported_index][0]
	reporter = reporter_initials + str(range(1,netids[reporter_index][1]))
	reported = reported_initials + str(range(1,netids[reported_index][1]))
	reason = "generate reason text here"
	report_element = ET.Element("report")
	reports_root.insert(i, report_element)

	reporter_element = ET.Element("reporter_netid")
	reporter_element.text = reporter
	report_element.insert(0, reporter_element)

	reported_element = ET.Element("reported_netid")
	reported_element.text = reported
	report_element.insert(1, reported_element)

	reason_element = ET.Element("reason")
	reason_element.text = reason
	report_element.insert(2, reason_element)

reports_tree = ET.ElementTree(reports_root)
reports_tree.write("reports.xml")

################
#generate recommend
################
recommends_root = ET.Element("recommends")
for i in range(0, 1000):
	recommender_index = random.randint(0, len(netids)-1)
	recommended_index = random.randint(0, len(netids)-1) 
	while(recommender_index == recommended_index):
		reported_index = random.randint(0, len(netids)-1) 
	recommender_initials = netids[recommender_index][0]
	recommended_initials = netids[recommended_index][0]
	recommender = recommender_initials + str(range(1,netids[recommender_index][1]))
	recommended = recommended_initials + str(range(1,netids[recommended_index][1]))
	reason = "generate reason text here"
	recommend_element = ET.Element("recommend")
	recommends_root.insert(i, report_element)

	recommender_element = ET.Element("recommender_netid")
	recommender_element.text = recommender
	recommend_element.insert(0, recommender_element)

	recommended_element = ET.Element("reported_netid")
	recommended_element.text = recommended
	recommend_element.insert(1, recommended_element)

	reason_element = ET.Element("reason")
	reason_element.text = reason
	report_element.insert(2, reason_element)

recommends_tree = ET.ElementTree(recommends_root)
recommends_tree.write("recommends.xml")


###################
#generate questions
###################

question_file = open("question.txt")
questions = question_file.readlines()
question_file.close()

questions_root = ET.Element("questions")

for i in range(0, len(questions)):
	question_element = ET.Element(str(i))
	question_element.text = questions[i]
	questions_root.insert(i, question_element)

questions_tree = ET.ElementTree(questions_root)
questions_tree.write("questions.xml")

##################
#answer textx generation
##################


answers_file = open("answers.txt")
answers = answers_file.readlines()
answers_file.close()

answers_root = ET.Element("answers_text")

questions_list_tuples = []
for i in range(0, len(answers)):
	answer_element = ET.Element("answer")
	answers_root.insert(i, answer_element)
	answer = answers[i]
	number = answer.split()[0]
	numbers = number.split(".")
	q_id = numbers[0]
	a_id = numbers[1]
	questions_list_tuples.append([q_id, a_id])

	answer_text_list = answer.split()[1: len(answer.split())]
	answer_text = " ".join(answer_text_list)

	qid_element = ET.Element("qid")
	qid_element.text = q_id
	answer_element.insert(0, qid_element)

	aid_element = ET.Element("answer_id")
	aid_element.text = a_id
	answer_element.insert(1, aid_element)

	text_element = ET.Element("text")
	text_element.text = answer_text
	answer_element.insert(2, text_element)

answers_tree = ET.ElementTree(answers_root)
answers_tree.write("answers.xml")


#########################
#answer generation
########################
user_answers_root = ET.Element("answers")

#each netid needs a set of answers
for id_initials in netids:
	id_initial = id_initials[0]
	highest = id_initials[1]
	for i in range(1, highest+1): #iterate through all netids
		current_netid = id_initial + str(i)
		for j in range(0, len(questions)): #iterates through all qids
			max_a_id = 0
			for element in questions_list_tuples:
				if element[0] == j and element[1] > max_a_id:
					max_a_id = element[1]
			user_answer_element = ET.Element("answer")
			user_answers_root.append(user_answer_element)

			netid_element = ET.Element("netid")
			netid_element.text = current_netid
			user_answer_element.insert(0, netid_element)

			qid_element = ET.Element("qid")
			qid_element.text = str(j+1)
			user_answer_element.insert(1, qid_element)

			answer_id_element = ET.Element("answer_id")
			answer_id_element.text = str(random.randint(1, max_a_id+1))
			user_answer_element.insert(2, answer_id_element)

			weight_element = ET.Element("weight")
			weight_element.text = str(random.randint(-5, 6))
			user_answer_element.insert(3, weight_element)

user_answers_tree = ET.ElementTree(user_answers_root)
user_answers_tree.write("user_answers.xml")

