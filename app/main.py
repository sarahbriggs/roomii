from flask import Flask, render_template
from flask_login import LoginManager
from flask_materialize import Material  
import db_related.useful_operations as uo
import db_related.useful_queries as uq
import db_related.cheapSecurity as sec
import sqlite3

app = Flask(__name__)
login = LoginManager(app)
Material(app)

@app.route("/")
def hello():
    return render_template("base.html")

@app.route("/register")
def register():
	conn = sqlite3.connect("db_related/fakedata.db")
	return render_template("register.html")

@app.route("/questions")
def questions():
	conn = sqlite3.connect("db_related/fakedata.db")
	question = uq.get_question_text(conn,0)[0][0]
	answer = uq.get_all_answer_text(conn,0)
	return render_template("questions.html", question = question, answers = answer)

if __name__ == '__main__':
	app.run()

