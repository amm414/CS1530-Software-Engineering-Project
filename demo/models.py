from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy()
db.init_app(app)

@app.cli.command('initdb')
def initdb_command():
	# wipeout
	db.drop_all()
	db.create_all()

	# add some default data
	db.session.add(User(username='jmd230', email="jmd230@pitt.edu", password='pass', phonenumber='4121234567', personalemail='jordanmdeller@gmail.com', contactmethod=1, bio='Serious offers only'))

	db.session.commit()

	print('Initialized the database.')


class User(db.Model):
	user_id   	 	= db.Column(db.Integer,    primary_key = True)
	username  	 	= db.Column(db.String(24), nullable = False)
	email    	 	= db.Column(db.String(80), nullable = False)
	password 	 	= db.Column(db.String(64), nullable = False)
	phonenumber  	= db.Column(db.String(64), nullable = False)
	personalemail  	= db.Column(db.String(80))
	contactmethod   = db.Column(db.Integer, nullable = False)
	bio		  	 	= db.Column(db.String(140))

	def __repr__(self):
		return '<User {}>'.format(self.username)

class Posting(db.Model):
	post_id 		= db.Column(db.Integer, primary_key = True)
	user_id 		= db.Column(db.Integer, nullable = False)
	date 			= db.Column(db.Date, nullable = False)
	title   		= db.Column(db.String(80), nullable = False)
	description 	= db.Column(db.String(140), nullable = False)
	price 			= db.Column(db.Integer, nullable = False)
	category 		= db.Column(db.String(80), nullable = False)
	contactmethod 	= db.Column(db.String(80), nullable = False)
	tag 			= db.Column(db.String(80), nullable = False)

	def __repr__(self):
		return '<Posting {}: "{}">'.format(self.post_id, self.title)
