from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager
from flask_materialize import Material  
import db_related.useful_operations as uo
import db_related.useful_queries as uq
import db_related.cheapSecurity as sec
import sqlite3

app = Flask(__name__)
login = LoginManager(app)
Material(app)

@app.route('/')
def hello():
    return render_template("index.html", display_error = 0) # 0 - not showing, 1 - showing

@app.route('/login', methods = ['GET', 'POST'])
def login():
	ip = request.environ['REMOTE_ADDR'] #maybe we can use this to only allow the correct user
	# print(ip)
	if (request.method == 'POST'):
		# try:
		conn = sqlite3.connect("db_related/fakedata.db")
		cur = conn.cursor()
		netid = request.form['netid']
		global currentNetid
		currentNetid = netid
		global loggedIn
		# print(currentNetid)
		password = request.form['password']
		
		if (sec.validate(conn,netid,password)):
			loggedIn = True
			conn.close()
			if (check_if_answered_questions(netid)):
				return redirect(url_for('homepage'))
			else:
				return redirect(url_for('displaySurvey'))
		else:
			loggedIn = False
			return render_template("index.html", display_error = 1)
		# except:
		# 	conn.rollback()
		# 	print("error in getting password")
	else:
		return redirect(url_for('index'))
				
@app.route('/homepage', methods = ['GET', 'POST'])
def homepage():
	netid = currentNetid
	conn = sqlite3.connect("db_related/fakedata.db")
	cur = conn.cursor()
	info = uq.get_user_info_friends(conn, netid)
	given_name = info[1]
	family_name = info[2]
	profpic = info[3]
	if profpic == "":
		profpic = "http://friendoprod.blob.core.windows.net/missionpics/images/4846/member/f9d9c34c-d5c8-495a-bd84-45b693edf7a2.jpg" # pikachu photo
	description = info[4]
	phone = info[6]
	email = info[7]
	rating = uq.get_user_rating(conn, netid)
	overall = None
	clean = None
	friendly = None
	consc = None
	self_accuracy = None
	num_reports = 0
	if (rating != False):
		overall = rating[1]
		clean = rating[2]
		friendly = rating[3]
		consc = rating[4]
		self_accuracy = rating[5]
		num_reports = rating[6]

	if (request.method == 'GET'):
		conn.close()
	else:
		numQuestions = uq.num_questions(conn)
		for i in range(numQuestions):
			strI = str(i)
			rangeID = "Range" + str(i);
			answerID = request.form[strI]
			value = int(request.form[rangeID])
			uo.answer_question(conn, netid, i, answerID, value)
	return render_template("homepage.html", 
		netid = netid,
		given_name = given_name,
		family_name = family_name,
		profpic = profpic,
		description = description,
		phone = phone,
		email = email,
		overall = overall,
		clean = clean,
		friendly = friendly,
		consc = consc,
		self_accuracy = self_accuracy,
		num_reports = num_reports
	)

@app.route('/matches', methods = ['GET', 'POST'])
def matches():
	if not loggedIn: 
		return render_template("index.html", display_error = 2)
	else:
		if request.method == 'GET':
			conn = sqlite3.connect("db_related/fakedata.db")
			print(loggedIn)
			print(currentNetid)
			allMatches = uo.get_matchups(conn, currentNetid)
			num = len(allMatches)
			if (num > 20): 
				num = 20
			matchups = []
			checkFriends = []
			for i in range(num):
				netid = allMatches[i][1]
				friends = uo.check_friends(conn, currentNetid, netid)
				checkFriends.append(friends)
				info = uq.get_user_info_general(conn, netid)
				tup = info[0]
				if friends:
					info = uq.get_user_info_friends(conn, netid)
					tup += (friends,)
				matchups.append(tup)
			conn.close()
			return render_template("matches.html", matchups = matchups, checkFriends = checkFriends)
		else:
			# add friends
			# visit profile
			return; 

@app.route('/register', methods=['GET', 'POST'])
def register():
	if (request.method == 'GET'):
		return redirect(url_for('regform'))

	#return render_template("register.html");
	'''
	#form is requested
	if(request.method == 'GET'):
		return render_template("register.html")
	#form is submitted
	if(request.method == 'POST'):
		return redirect(url_for('survey'))
		#return render_template("survey.html")
	'''
@app.route('/regform', methods=['GET', 'POST'])
def regform():
	if (request.method == 'GET'):
		return render_template("register.html", display_error = 0)
	else:
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		netid = request.form['netid']
		password = request.form['password']
		phone = request.form['phone']
		email = request.form['email']
		profpic = request.form['profile photo']
		description = request.form['Self Description']
		if profpic == "":
			profpic = "http://friendoprod.blob.core.windows.net/missionpics/images/4846/member/f9d9c34c-d5c8-495a-bd84-45b693edf7a2.jpg" # pikachu photo
		if phone == "":
			phone = None
		if email == "":
			email = None
		conn = sqlite3.connect("db_related/fakedata.db")
		try:
			uo.new_user(conn, netid, first_name, last_name, profpic, description)
			sec.register(conn,netid,password)
			uo.new_contact(conn, netid, phone, email)
			global currentNetid
			currentNetid = netid
			print(netid)
			return redirect(url_for('displaySurvey'))
		except:
			conn.rollback()
			conn.close()
			return render_template("register.html", display_error = 1)
		conn.close()

@app.route('/survey', methods=['GET', 'POST'])
def survey():
	if(request.method == 'GET'):
		return redirect(url_for('displaySurvey'))
	# if (request.method == 'POST'):
	# 	try:
	# 		first_name = request.form['first_name']
	# 		last_name = request.form['last_name']
	# 		netid = request.form['netid']
	# 		password = request.form['password']
	# 		conn = sqlite3.connect("db_related/fakedata.db")
	# 		cur = conn.cursor()
	# 		uo.new_user(conn, netid, first_name, last_name)
	# 		sec.register(conn, netid, password)
	# 		print("Record successfully added")
	# 	except:
	# 		conn.rollback()
	# 		print("error in insert operation")
	# 	finally:
	# 		return redirect(url_for('displaySurvey'))
	# 		conn.close()

@app.route('/displaySurvey')
def displaySurvey():
	conn = sqlite3.connect("db_related/fakedata.db")
	numQuestions = uq.num_questions(conn)
	question = []
	answers = []
	for i in range(numQuestions):
		question.append(uq.get_question_text(conn,i))
		answers.append(uq.get_all_answer_text(conn,i))
	conn.close()
	return render_template("displayQuestion.html", answers = answers, question = question)

@app.route('/questions')
def questions():
	conn = sqlite3.connect("db_related/fakedata.db")
	question = uq.get_question_text(conn,0)[0][0]
	answer = uq.get_all_answer_text(conn,0)
	conn.close()
	return render_template("questions.html", question = question, answers = answer)

@app.route('/searchUser', methods = ['GET', 'POST'])
def searchUser():
	conn = sqlite3.connect("db_related/fakedata.db")
	searchedNetid = request.form['netid']
	info = uq.get_user_info_friends(conn, searchedNetid)
	rating = uq.get_user_rating(conn, searchedNetid)
	overall = None
	clean = None
	friendly = None
	consc = None
	self_accuracy = None
	num_reports = 0
	if (rating != False):
		overall = rating[1]
		clean = rating[2]
		friendly = rating[3]
		consc = rating[4]
		self_accuracy = rating[5]
		num_reports = rating[6]
	if (info != False):
		given_name = info[1]
		family_name = info[2]
		profpic = info[3]
		if profpic == "":
			profpic = "http://friendoprod.blob.core.windows.net/missionpics/images/4846/member/f9d9c34c-d5c8-495a-bd84-45b693edf7a2.jpg" # pikachu photo
		description = info[4]
		phone = info[6]
		email = info[7]
		sourceNetid = currentNetid
		areFriends = uq.are_friends(conn, searchedNetid, sourceNetid) or uq.are_friends(conn, sourceNetid, searchedNetid) or (searchedNetid == sourceNetid)
		conn.close()
		if areFriends:
			return render_template("searchUser.html", 
				searchedNetid = searchedNetid,
				given_name = given_name,
				family_name = family_name,
				profpic = profpic,
				description = description,
				phone = phone,
				email = email,
				overall = overall,
				clean = clean,
				friendly = friendly,
				consc = consc,
				self_accuracy = self_accuracy,
				num_reports = num_reports)
		else:
			return render_template("searchUser.html", 
				searchedNetid = searchedNetid,
				given_name = given_name,
				family_name = family_name,
				profpic = profpic,
				description = description,
				phone = None,
				email = None,
				overall = overall,
				clean = clean,
				friendly = friendly,
				consc = consc,
				self_accuracy = self_accuracy,
				num_reports = num_reports)
	else:
		return render_template("searchUser.html", 
			areFriends = None, 
			searchedNetid = None,
			given_name = None,
			family_name = None,
			profpic = None,
			description = None,
			phone = None,
			email = None,
			overall = overall,
			clean = clean,
			friendly = friendly,
			consc = consc,
			self_accuracy = self_accuracy,
			num_reports = num_reports)

def displayUser(areFriends, searchedNetid, given_name, family_name, profpic, description, phone, email):
	return render_template("searchUser.html",
		areFriends = areFriends,
		searchedNetid = searchedNetid,
		given_name = given_name,
		family_name = family_name,
		profpic = profpic,
		description = description,
		phone = phone,
		email = email)

def check_if_answered_questions(netid):
	conn = sqlite3.connect("db_related/fakedata.db")
	answers = uq.get_answer(conn, netid)
	if (answers != False):
		return True
	else:
		return False

currentNetid = ""
loggedIn = False

if __name__ == '__main__':
	currentNetids = {}
	currentNetid = ""
	loggedIn = False
	app.run()