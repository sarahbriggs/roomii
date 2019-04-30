CREATE TABLE users(
	netid text PRIMARY KEY, 
	given_name text,
	family_name text,
	profpic text,
	description text, 
	status boolean);
CREATE TABLE roommate(
	netid1 text,
	netid2 text,
	PRIMARY KEY (netid1, netid2)
	FOREIGN KEY (netid1) REFERENCES user(netid),
	FOREIGN KEY (netid2) REFERENCES user(netid));
CREATE TABLE password(
	netid text PRIMARY KEY,
	pass text,
	salt text,
	FOREIGN KEY (netid) REFERENCES users(netid));
CREATE TABLE contact( -- contact info to be shared with friends
	netid text PRIMARY KEY,
	phone text,
	email text,
	FOREIGN KEY (netid) REFERENCES users(netid));
CREATE TABLE matchups(
	netid1 text,
	netid2 text,
	matchRating real,
	FOREIGN KEY (netid1) REFERENCES users(netid),
	FOREIGN KEY (netid2) REFERENCES users(netid));
CREATE TABLE friends( -- netid1 and netid2 are friends, status is 0 if friend is requested, 1 if friend is accepted, and -1 if request was blocked
	netid1 text,
	netid2 text,
	status integer CHECK(status = 0 OR status = 1 OR status = -1),
	-- PRIMARY KEY (netid1, netid2),
	FOREIGN KEY (netid1) REFERENCES users(netid),
	FOREIGN KEY (netid2) REFERENCES users(netid));
CREATE TABLE ratings(
	netid text PRIMARY KEY, 
	avg_overall real CHECK(avg_overall >= 0 AND avg_overall <= 5),
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
	self_report_accuracy real CHECK(self_report_accuracy >= 0 AND self_report_accuracy <= 5),
	PRIMARY KEY (reviewer_netid, reviewed_netid),
	FOREIGN KEY (reviewer_netid) REFERENCES users(netid),
	FOREIGN KEY (reviewed_netid) REFERENCES users(netid));
CREATE TABLE report(
	reporter_netid text, 
	reported_netid text,
	reason text, 
	PRIMARY KEY (reporter_netid, reported_netid),
	FOREIGN KEY (reporter_netid) REFERENCES users(netid),
	FOREIGN KEY (reported_netid) REFERENCES users(netid));
CREATE TABLE blocked(
	blocker_netid text, 
	blocked_netid text,
	PRIMARY KEY(blocker_netid, blocked_netid),
	FOREIGN KEY(blocked_netid) REFERENCES users(netid),
	FOREIGN KEY(blocker_netid) REFERENCES users(netid));
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
	category_number integer NOT NULL CHECK(category_number >= 0),
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