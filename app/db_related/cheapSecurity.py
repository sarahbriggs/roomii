import datetime,sqlite3
# def make(password): #i really wanted to make 
# 	password = str(password)
# 	salt = str(datetime.datetime.now())
# 	phrase = hash(salt + password)
# 	return (salt,phrase)

# def compare(password, phrase, salt):
# 	password = str(password)
# 	phrase2 = hash(salt+password)
# 	return phrase2 == phrase

def make(password): #**** it, plaintext it is then
	return (None, password)
def compare(password, phrase, salt):
	return phrase == password

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
	print (tup2)
	return compare(password,phrase,salt)

if __name__ == '__main__':
	conn = sqlite3.connect('./fakedata.db')
	try:
		register(conn,"rjf19", "password")
	except:
		pass
	print(validate(conn,"rjf19","password"))
