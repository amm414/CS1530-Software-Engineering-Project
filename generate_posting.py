import random
import string
import urllib.request

def populate():
	word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
	response = urllib.request.urlopen(word_site)
	txt = response.read()
	WORDS = txt.splitlines()

	category = ["All", "Textbooks", "Furniture", "Food", "Events", "Software", "Electronics", "Beauty and Personal Care", "Clothes", "School Supplies", "Appliances"]
	contact = ["email", "phonenumber", "personalemail"]
	
	for i in range(0, 100):
		title = WORDS[random.randint(0, len(WORDS))].decode('utf8') + " " + WORDS[random.randint(0, len(WORDS))].decode('utf8') + " " + WORDS[random.randint(0, len(WORDS))].decode('utf8')
		if len(title) > 30:
			title = title[:30]

		description = WORDS[random.randint(0, len(WORDS))].decode('utf8') + " " + WORDS[random.randint(0, len(WORDS))].decode('utf8') + " " + WORDS[random.randint(0, len(WORDS))].decode('utf8') + " " + WORDS[random.randint(0, len(WORDS))].decode('utf8') + " " + WORDS[random.randint(0, len(WORDS))].decode('utf8') + " " + WORDS[random.randint(0, len(WORDS))].decode('utf8') + " " + WORDS[random.randint(0, len(WORDS))].decode('utf8') + " " + WORDS[random.randint(0, len(WORDS))].decode('utf8') + " " + WORDS[random.randint(0, len(WORDS))].decode('utf8')
		if len(description) > 250:
			description = description[:250]
		with open('postingsData.csv', 'a') as the_file:
			the_file.write(str(random.randint(1, 400)) + "," + title + "," + description + "," + str(random.randint(100, 20000)/100.0) + "," + category[random.randint(0, len(category) - 1)] + "," + contact[random.randint(0, len(contact) - 1)] + "\n")


populate()
