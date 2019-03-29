import sqlite3
import xml.etree.ElementTree as ET
import useful_operations

conn = sqlite3.connect('fakedata.db')

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
#getting integrity check, not sure why
''' 
answerstree = ET.parse('../../data/user_answers.xml')
answersroot = answerstree.getroot()
for answer in answersroot.iter(tag = "answer"):
	netid = answer.find("netid").text
	qid = answer.find("qid").text
	aid = answer.find("answer_id").text
	weight = answer.find("weight").text
	useful_operations.answer_question(conn, netid, qid, aid, weight)
'''