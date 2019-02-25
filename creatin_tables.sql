CREATE TABLE users(
	netid text PRIMARY KEY, 
	name text,
	profpic text);
CREATE TABLE passwords(
	netid text,
	salt text,
	password text,
	FOREIGN KEY (netid) REFERENCES users(netid));
CREATE TABLE ratings(
	netid text PRIMARY KEY, 
	cleanliness real CHECK(cleanliness >= 0 AND cleanliness <= 5), 
	friendliness real CHECK(friendliness >= 0 AND friendliness <= 5), 
	conscientiousness real CHECK(conscientiousness >= 0 AND conscientiousness <= 5), 
	self_report_accuracy real CHECK(self_report_accuracy >= 0 AND self_report_accuracy <= 5),
	number_of_reports integer NOT NULL CHECK(number_of_reports >= 0),
	FOREIGN KEY (netid) REFERENCES users(netid));
CREATE TABLE review(
	reviewer_netid text, 
	reviewed_netid text, 
	review_text text, 
	overall_rating real NOT NULL CHECK(overall_rating >= 0 AND overall_rating <= 5), 
	cleanliness real CHECK(cleanliness >= 0 AND cleanliness <= 5), 
	friendliness real CHECK(friendliness >= 0 AND friendliness <= 5), 
	conscientiousness real CHECK(conscientiousness >= 0 AND conscientiousness <= 5), 
	PRIMARY KEY (reviewer_netid, reviewed_netid),
	FOREIGN KEY (reviewer_netid) REFERENCES users(netid),
	FOREIGN KEY (reviewed_netid) REFERENCES users(netid));
CREATE TABLE report(
	reporter_netid text, 
	reported_netid text,
	reason text, 
	PRIMARY KEY (reported_netid, reported_netid),
	FOREIGN KEY (reporter_netid) REFERENCES users(netid),
	FOREIGN KEY (reported_netid) REFERENCES users(netid));
CREATE TABLE recommend(
	recommender_netid text, 
	recommendee_netid text, 
	recommended_netid text, 
	reason text, 
	PRIMARY KEY (recommender_netid, recommendee_netid, recommended_netid),
	FOREIGN KEY (recommender_netid) REFERENCES users(netid),
	FOREIGN KEY (recommendee_netid) REFERENCES users(netid),
	FOREIGN KEY (recommended_netid) REFERENCES users(netid));
-- recommender - A, recommendee - B, recommended C. So A recommends C to B
CREATE TABLE questions(
	qid integer PRIMARY KEY,
	question_content text NOT NULL);
CREATE TABLE answer_text(
	qid integer, 
	answer_id integer CHECK(answer_id >= 0), 
	answer_content text NOT NULL, 
	PRIMARY KEY (qid, answer_id),
	FOREIGN KEY (qid) REFERENCES questions(qid));
-- choices related to a question
CREATE TABLE answer(
	netid text, 
	qid integer, 
	answer_id integer CHECK(answer_id >= 0), 
	weight real CHECK(weight >= -5 AND weight <= 5), 
	PRIMARY KEY (netid, qid),
	FOREIGN KEY (netid) REFERENCES users(netid),
	FOREIGN KEY (qid) REFERENCES questions(qid));