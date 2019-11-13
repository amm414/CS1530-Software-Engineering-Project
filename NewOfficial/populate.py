import random
import string

def populate():
	#Users
	userInfo = []
	for i in range(10):
		userInfo[0] = randomString(5)
		userInfo[1] = userInfo[0] + "@pitt.edu"
		userInfo[2] = randomPassword(15)
		userInfo[3] = randomStringNumbers(10)
		userInfo[4] = randomString(10) + "@gmail.com"

		db.session.add(userid=i, username=userInfo[0], email=userInfo[1], password=userInfo[2], phonenumber=userInfo[3], personalemail=userInfo[4], bio='Pitt 2021')

def randomStringLetters(stringLength):
    """Generate a random string of fixed length """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

def randomStringNumbers(stringLength):
    """Generate a random string of fixed length """
    letters = string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))

def randomPassword(stringLength):
	password_characters = string.ascii_letters + string.digits + string.punctuation
	return ''.join(random.choice(password_characters) for i in range(stringLength))
