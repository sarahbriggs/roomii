print("start")
import xml.etree.ElementTree as ET
import random

names = open("nameslist.txt", "r")
nameslist = names.readlines()
names.close()
ratings_root = ET.Element("ratings")

users_root = ET.Element("users")
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
	if (not initialExists):
		netids.append([netid, 1])
	netid += str(num)
	#generate users relation here
	user = ET.Element("user")
	users_root.insert(i, user)

	netid_element = ET.Element("netid")
	netid_element.text = netid
	user.insert(0, netid_element)

	given_name_element = ET.Element("given_name")
	given_name_element.text = name.split()[0]
	user.insert(1, given_name_element)

	family_name_element = ET.Element("family_name")
	family_name_element.text = name.split()[1]
	user.insert(2, family_name_element)

	prof_pic_element = ET.Element("prof_pic")
	prof_pic_element.text = "placeholder"
	user.insert(3, prof_pic_element)

	description_element = ET.Element("description")
	description_element.text = "placeholder1"
	user.insert(4, description_element)

	status_element = ET.Element("status")
	#status_element.text =  automatically set to ttrue
	user.insert(5, status_element)




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

users_tree = ET.ElementTree(users_root)
users_tree.write("users.xml")