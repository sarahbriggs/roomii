from flask import Flask, render_template
import db_related.useful_operations as uo
import db_related.useful_queries as uq
import sqlite3

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("base.html")

@app.route("/questions")
def questions():
	conn = sqlite3.connect("fakedata.db")
	question = uq.get_question_text(conn,0)
	return render_template("questions.html", question = question)

if __name__ == '__main__':
	app.run()

