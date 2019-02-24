CREATE TABLE users(
	netid text PRIMARY KEY, 
	profpic text);
CREATE TABLE ratings(
	netid text PRIMARY KEY, 
	cleanliness real, 
	friendliness real, 
	conscientiousness real, 
	self_report_accuracy real,
	number_of_reports integer);
CREATE TABLE review(
	reviewer_netid text, 
	reviewed_netid text, 
	review_text text, 
	overall_rating NOT NULL real, 
	cleanliness real, 
	friendliness real, 
	conscientiousness real, 
	PRIMARY KEY(reviewer_netid, reviewed_netid));
CREATE TABLE report(
	reporter_netid text, 
	reported_netid text,
	reason text, 
	PRIMARY KEY(reported_netid, reported_netid));
CREATE TABLE recommend(
	recommender_netid text, 
	recommendee_netid text, 
	recommended_netid text, 
	reason text, 
	PRIMARY KEY(recommender_netid,recommendee_netid,recommended_netid));
-- recommender - A, recommendee - B, recommended C. So A recommends C to B
CREATE TABLE questions(
	qid integer PRIMARY KEY,
	question_content text);
CREATE TABLE answer_text(
	qid integer, 
	answer_id integer, 
	answer_content text, 
	PRIMARY KEY(qid, answer_id));
-- choices related to a question
CREATE TABLE answer(
	netid text, 
	qid integer, 
	answer_id integer, 
	weight real, 
	PRIMARY KEY(netid, qid));