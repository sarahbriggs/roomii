import useful_queries as q
import useful_operations as o
import sqlite3

if __name__ == '__main__':
	conn = sqlite3.connect('fakedata.db')
	# o.create_rating(conn, "zz105", 5, 5, 5, 5, 5, 0)
	# o.report_user(conn, "dummy", "zz105", "shit person!")
	q.get_number_of_reviews_of_user(conn, "zz105")

