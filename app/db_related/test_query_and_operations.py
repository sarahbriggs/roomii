import useful_queries as q
import useful_operations as o
import sqlite3

if __name__ == '__main__':
	conn = sqlite3.connect('fakedata.db')
	conn.execute("PRAGMA foreign_keys = 1")
	# o.create_rating(conn, "zz105", 5, 5, 5, 5, 5, 0)
	# o.report_user(conn, "dummy", "zz105", "shit person!")
	# q.get_number_of_reviews_of_user(conn, "zz105")
	# o.friend_request(conn, "zz105", "dummy")
	# o.recommend_user(conn, "zz105", "dummy", "rjf19", "dumbdumb")
	o.new_password(conn, "zz105", "hellokitty")
	print(q.get_user_password(conn, "zz105"))
	print(q.get_user_password(conn, 'll'))


