import datetime
def make(password):
	salt = str(datetime.datetime.now())
	phrase = hash(salt + password)
	return (salt,phrase)

def compare(password, phrase, salt):
	phrase2 = hash(salt+password)
	return phrase2 == phrase