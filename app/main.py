from flask import Flask, render_template
import useful_operations, useful_queries
import sqlite3

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("base.html")

@app.route("/questions")
def questions():
	conn = sqlite3.connect("fakedata.db")
	question = useful_queries.get_question_text(conn,0)
	return render_template("questions.html", question = question)

def launch():
	app.run()
