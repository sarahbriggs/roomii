from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_login import LoginManager
from flask_materialize import Material  
import db_related.useful_operations as uo
import db_related.useful_queries as uq
import db_related.cheapSecurity as sec
import sqlite3
import os

app = Flask(__name__)
login = LoginManager(app)
app.config['UPLOAD_FOLDER'] = "./uploads"
Material(app)

@app.route('/')
def hello():
	global currentNetid
	currentNetid = ""
	return render_template("index.html", display_error = 0) # 0 - not showing, 1 - showing

@app.route('/login', methods = ['GET', 'POST'])
def login():
	ip = request.environ['REMOTE_ADDR'] #maybe we can use this to only allow the correct user
	# print(ip)
	if (request.method == 'POST'):
		# try:
		conn = sqlite3.connect("db_related/fakedata.db")
		cur = conn.cursor()
		netid = request.form['netid'].upper()
		global currentNetid
		currentNetid = netid
		# print(currentNetid)
		password = request.form['password']
		global loggedIn
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
	if not loggedIn: 
		return render_template("index.html", display_error = 2)

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
		overall = round(rating[1], 1)
		clean = round(rating[2], 1)
		friendly = round(rating[3], 1)
		consc = round(rating[4], 1)
		self_accuracy = round(rating[5], 1)
		num_reports = rating[6]

	# if (request.method == 'GET'):
	conn.close()
	return render_template("homepage.html", 
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
		conn = sqlite3.connect("db_related/fakedata.db")
		if request.method == 'GET':
			allMatches = uo.get_matchups(conn, currentNetid)
			blocked = uq.get_blocked_by_user(conn, currentNetid)
			print(blocked)
			if blocked == False:
				num = len(allMatches)
			else:
				num = len(allMatches) - len(blocked)
			print(num)
			if (num > 20): 
				num = 20
			matchups = []
			checkFriends = []
			scores = []
			for i in range(num):
				netid = allMatches[i][1].upper()
				flag = True
				if (blocked != False):
					for j in range(len(blocked)):
						if netid == blocked[j][0]:
							flag = False
							break
				if flag == True :
					score = allMatches[i][2]
					scores.append(score)
					friends = uq.are_friends(conn, currentNetid, netid) or uq.are_friends(conn, netid, currentNetid)
					checkFriends.append(friends)
					info = uq.get_user_info_general(conn, netid)
					tup = info[0]
					if friends:
						info = uq.get_user_info_friends(conn, netid)
					matchups.append(tup)
			conn.close()
			return render_template("matches.html", matchups = matchups, checkFriends = checkFriends, scores = scores)
		else:
			toAdd = request.form['addID']
			check = toAdd.split(":")
			if check[0]=="Add Friend":
				print("Adding friend: " + check[1])
				added = uo.friend_request(conn, currentNetid, check[1])
				#accept = uo.request_accepted(conn, currentNetid, check[1])
				test = uq.are_friends(conn, currentNetid, check[1]) or uq.are_friends(conn, check[1], currentNetid)
				return redirect(url_for('matches'))
			if check[0]=="Block":
				print("Blocking: " + check[1])
				blocked = uo.block_user(conn, currentNetid, check[1])
				conn.close()
				return redirect(url_for('matches'))

def sanit(tup):
	tup = list(tup)
	new = []
	for thing in tup:
		if thing == None:
			new.append("")
		else:
			new.append(thing)
	return tuple(new)



@app.route('/processReport', methods = ['GET', 'POST'])
def processReport():
	reporter = currentNetid;
	reported = request.form['netid'].upper()
	if reported == None:
		return redirect(url_for('homepage'))
	conn = sqlite3.connect("db_related/fakedata.db")
	reason = request.form['reason']
	try:
		uo.report_user(conn, reporter, reported, reason)
		return redirect(url_for('homepage'))
	except:
		return redirect(url_for('homepage'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if (request.method == 'GET'):
		return redirect(url_for('regform'))

@app.route('/regform', methods=['GET', 'POST'])
def regform():
	if (request.method == 'GET'):
		return render_template("register.html", display_error = 0)
	else:
		key1 = None
		for key in request.files.keys():
			key1 = key
			break
		
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		netid = request.form['netid'].upper()
		password = request.form['password']
		phone = request.form['phone']
		email = request.form['email']
		# profpic = request.form['profile photo']
		description = request.form['Self Description']
		file = None
		if key1:
			file = request.files[key1]
		profpic = ""
		if file:
			profpic = file.filename
			profpic = str(hash(profpic+netid))[:16]+".jpg"
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], profpic))
			profpic = "/uploads/"+profpic
		else:
			profpic = "/uploads/generic.jpg"
		
		if phone == "":
			phone = None
		if email == "":
			email = None

		conn = sqlite3.connect("db_related/fakedata.db")
		
		if (uo.new_user(conn, netid, first_name, last_name, profpic, description)):
			sec.register(conn, netid, password)
			uo.new_contact(conn, netid, phone, email)
			global currentNetid
			currentNetid = netid
			global loggedIn
			loggedIn = True
			return redirect(url_for('displaySurvey'))
		else:
			conn.rollback()
			conn.close()
			return render_template("register.html", display_error = 1)
		conn.close()

@app.route('/uploads/<filename>', methods = ['GET'])
def profpicGet(filename):
	return send_from_directory("uploads", filename)


@app.route('/survey', methods=['GET', 'POST'])
def survey():
	if(request.method == 'GET'):
		return redirect(url_for('displaySurvey'))
	if(request.method == 'POST'):
		conn = sqlite3.connect("db_related/fakedata.db")
		numQuestions = uq.num_questions(conn)
		print(numQuestions)
		netid = currentNetid
		for i in range(numQuestions):
			strI = str(i)
			rangeID = "Range" + str(i)
			answerID = 0
			try:
				answerID = request.form[strI]
			except:
				pass
			value = int(request.form[rangeID])
			uo.answer_question(conn, netid, i, answerID, value)
		uo.all_matchups(conn,netid)
		return redirect(url_for('homepage'))


@app.route('/displaySurvey')
def displaySurvey():
	if not loggedIn: 
		return render_template("index.html", display_error = 2)
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

@app.route('/report')
def report():
	reportedNetid = request.args.get('netid').upper()
	if reportedNetid == None:
		return redirect(url_for("homepage"))
	return render_template("report.html", netid = reportedNetid)

@app.route('/redoSurvey', methods = ['GET'])
def redoSurvey():
	if not loggedIn:
		return render_template("index.html", display_error = 2)
	conn = sqlite3.connect("db_related/fakedata.db")
	uo.remove_answers(conn, currentNetid)
	return redirect(url_for("displaySurvey"))

@app.route('/searchUser', methods = ['GET', 'POST'])
def searchUser():
	if not loggedIn: 
		return render_template("index.html", display_error = 2)
	if (request.method == 'GET'):
		conn = sqlite3.connect("db_related/fakedata.db")
		searchedNetid = request.args.get('netid').upper()
		print(searchedNetid)
		searchedNetid = searchedNetid.upper()
		if (searchedNetid == currentNetid.upper()):
			return redirect(url_for("homepage"))
		info = uq.get_user_info_friends(conn, searchedNetid)
		rating = uq.get_user_rating(conn, searchedNetid)
		overall = None
		clean = None
		friendly = None
		consc = None
		self_accuracy = None
		num_reports = 0
		if (rating != False):
			overall = round(rating[1], 1)
			clean = round(rating[2], 1)
			friendly = round(rating[3], 1)
			consc = round(rating[4], 1)
			self_accuracy = round(rating[5], 1)
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
			areFriends = True
			wereRoommates = uq.were_roommates(conn, searchedNetid, sourceNetid)
			num_reviews = uq.get_number_of_reviews_of_user(conn, searchedNetid)
			reviews = None
			if num_reviews != 0:
				reviews = uq.get_review_of_user(conn, searchedNetid)

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
					num_reports = num_reports,
					wereRoommates = True,
					reviews = reviews)
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
					num_reports = num_reports,
					wereRoommates = True,
					reviews = reviews)
		else:
			return render_template("notExist.html")
	else:
		return render_template("notExist.html")


@app.route('/review', methods=['GET', 'POST'])
def review():
	reviewed = request.args.get('netid')
	if reviewed == None:
		return redirect(url_for("homepage"))
	return render_template("review.html", netid = reviewed)

@app.route('/reviewform', methods=['GET', 'POST'])
def reviewform():
	if not loggedIn: 
		return render_template("index.html", display_error = 2)
	reviewed = request.form["netid"]
	if reviewed == None:
		return redirect(url_for("homepage"))
	cleanliness = float(request.form["cleanliness"])
	friendliness = float(request.form["friendliness"])
	conscientiousness = float(request.form["conscientiousness"])
	overall_rating =  round((cleanliness + friendliness + conscientiousness)/3, 2)
	text = request.form["reviewtext"]
	self_accuracy = request.form['self-report accuracy']
	conn = sqlite3.connect("db_related/fakedata.db")
	try:
		uo.new_review(conn, currentNetid, reviewed, text, overall_rating, friendliness, cleanliness, conscientiousness, self_accuracy)
		return redirect(url_for('homepage'))
	except:
		conn.rollback()
		conn.close()
		print("excepting here")
		return render_template("review.html", display_error = 1)
	conn.close()


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