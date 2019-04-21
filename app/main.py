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
	if (request.method == 'POST'):
		try:
			conn = sqlite3.connect("db_related/fakedata.db")
			cur = conn.cursor()
			netid = request.form['netid']
			global currentNetid
			currentNetid = netid
			print(currentNetid)
			password = request.form['password']
			actual_password = uq.get_user_password(conn, netid)
			print(password)
			print(actual_password)
			print("Get password successfully")
			if (actual_password != False and password == actual_password):
				conn.close()
				if (check_if_answered_questions(netid)):
					return redirect(url_for('homepage'))
				else:
					return redirect(url_for('displaySurvey'))
			else:
				return render_template("index.html", display_error = 1)
		except:
			conn.rollback()
			print("error in getting password")
	else:
		return redirect(url_for('index'))
				
@app.route('/homepage', methods = ['GET', 'POST'])
def homepage():
	netid = currentNetid
	conn = sqlite3.connect("db_related/fakedata.db")
	cur = conn.cursor()
	print("NETID")
	print(netid)
	info = uq.get_user_info_friends(conn, netid)
	given_name = info[1]
	family_name = info[2]
	profpic = info[3]
	description = info[4]
	phone = info[6]
	email = info[7]
	if (request.method == 'GET'):
		conn.close()
	else:
		numQuestions = uq.num_questions(conn)
		print("testing here")
		for i in range(numQuestions):
			strI = str(i)
			answerID = request.form[strI]
			uo.answer_question(conn, netid, i, answerID, 5)
	return render_template("homepage.html", netid = netid,
		given_name = given_name,
		family_name = family_name,
		profpic = profpic,
		description = description,
		phone = phone,
		email = email
	)


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
		conn = sqlite3.connect("db_related/fakedata.db")
		cur = conn.cursor()
		try:
			uo.new_user(conn, netid, first_name, last_name)
			uo.new_password(conn, netid, password)
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
	if (request.method == 'POST'):
		try:
			first_name = request.form['first_name']
			last_name = request.form['last_name']
			netid = request.form['netid']
			password = request.form['password']
			conn = sqlite3.connect("db_related/fakedata.db")
			cur = conn.cursor()
			uo.new_user(conn, netid, first_name, last_name)
			uo.new_password(conn, netid, password)
			print("Record successfully added")
		except:
			conn.rollback()
			print("error in insert operation")
		finally:
			return redirect(url_for('displaySurvey'))
			conn.close()


@app.route('/displaySurvey')
def displaySurvey():
	conn = sqlite3.connect("db_related/fakedata.db")
	numQuestions = uq.num_questions(conn)
	question = []
	answers = []
	for i in range(numQuestions):
		question.append(uq.get_question_text(conn,i))
		answers.append(uq.get_all_answer_text(conn,i))
	return render_template("displayQuestion.html", answers = answers, question = question)

@app.route('/questions')
def questions():
	conn = sqlite3.connect("db_related/fakedata.db")
	question = uq.get_question_text(conn,0)[0][0]
	answer = uq.get_all_answer_text(conn,0)
	return render_template("questions.html", question = question, answers = answer)

def check_if_answered_questions(netid):
	conn = sqlite3.connect("db_related/fakedata.db")
	answers = uq.get_answer(conn, netid)
	if (answers != False):
		return True
	else:
		return False

currentNetid = ""

if __name__ == '__main__':
	currentNetid = ""
	app.run()