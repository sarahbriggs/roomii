import datetime,sqlite3
import werkzeug.security as ws
def make(password): #i really wanted to make 
	password = str(password)
	salt = str(datetime.datetime.now())
	phrase = ws.generate_password_hash(salt + password)
	return (salt,phrase)

def compare(password, phrase, salt):
	password = str(password)
	return  ws.check_password_hash(phrase, salt+password)

def register(conn, netid, password):
	cursor = conn.cursor()
	salt, phrase = make(password)
	tup = (netid, phrase, salt)
	cursor.execute('INSERT INTO password VALUES (?,?,?);', tup)
	conn.commit()
	cursor.close()
	return 

def validate(conn, netid, password):
	cursor = conn.cursor()
	tup = (netid,)
	cursor.execute('SELECT pass, salt FROM password WHERE netid = ?;', tup)
	tup2 = None
	for val in cursor:
		tup2 = val
		break
	if not tup2:
		return False
	phrase, salt = tup2
	return compare(password,phrase,salt)

if __name__ == '__main__':
	conn = sqlite3.connect('./fakedata.db')
	try:
		register(conn,"rjf19", "password")
	except:
		pass
	print(validate(conn,"rjf19","password"))
