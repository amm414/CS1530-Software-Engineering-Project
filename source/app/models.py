from flask_sqlalchemy import SQLAlchemy
from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


# INITS THE DBs

@app.cli.command('initdb')
def initdb_command():
	# wipeout
	db.drop_all()
	db.create_all()

	# add some default data
	db.session.add(User(username='jmd230', email="jmd230@pitt.edu", password=generate_password_hash('pass'), phonenumber='4121234567', personalemail='jordanmdeller@gmail.com', bio='Serious offers only', rating=5, numRatings=0))
	db.session.add(User(username='admin', email="admin@pitt.edu", password=generate_password_hash('foobiz'), phonenumber='2341172381', personalemail='admin@admin.com', bio='I am an admin. This account is used to manage and test out the APP!', rating=5, numRatings=0))
	db.session.add(User(username='tester1', email="tester1@pitt.edu", password=generate_password_hash('foobar'), phonenumber='2456734224', personalemail='tester1@gmail.com', bio='Tester is testing account for testing...', rating=5, numRatings=0))

	db.session.add(Posting(userid=1, username='jmd230', date=datetime.now(), title='Cool Book', description='Very good quality, barely used.', price=50.00, category='Textbooks', contactmethod='jmd230@pitt.edu', tags='book'))
	db.session.add(Posting(userid=2, username='admin', date=datetime.now(), title='Brown couch', description='No signs of wear.', price=100.00, category='Furniture', contactmethod='phonenumber', tags='furniture, couch, seating, brown, comfy'))
	db.session.add(Posting(userid=3, username='tester1', date=datetime.now(), title='Cheap Book', description='Great quality.', price=20.00, category='Textbooks', contactmethod='test1@gmail.com', tags='book'))

	db.session.commit()

	print('Initialized the database.')


class User(db.Model):
	userid   	 	= db.Column(db.Integer,    primary_key = True)
	username  	 	= db.Column(db.String(24), nullable = False)
	email    	 	= db.Column(db.String(80), nullable = False)
	# hashed password is 128 chars ALWAYS
	password 	 	= db.Column(db.String(128), nullable = False)
	phonenumber  	= db.Column(db.String(64), nullable = False)
	personalemail  	= db.Column(db.String(80))
	bio		  	 	= db.Column(db.String(140))
	rating 			= db.Column(db.Float(2), nullable = False)
	numRatings		= db.Column(db.Integer, nullable = False)

	def __repr__(self):
		return '<User {}>'.format(self.username)

class Posting(db.Model):
	postid 			= db.Column(db.Integer, primary_key = True)
	userid 			= db.Column(db.Integer, nullable = False)
	username        = db.Column(db.String(24), nullable = False)
	date 			= db.Column(db.Date, nullable = False)
	title   		= db.Column(db.String(80), nullable = False)
	description 	= db.Column(db.String(140), nullable = False)
	price 			= db.Column(db.Integer, nullable = False)
	category 		= db.Column(db.String(80), nullable = False)
	contactmethod 	= db.Column(db.String(80), nullable = True)
	tags 			= db.Column(db.String(80), nullable = True)

	def __repr__(self):
		return '<Posting {}: "{}">'.format(self.postid, self.title)

class Claim(db.Model):
	claimid			= db.Column(db.Integer, primary_key = True)
	postid 			= db.Column(db.Integer, nullable = False)
	sellerid 		= db.Column(db.Integer, nullable = False)
	buyerid 		= db.Column(db.Integer, nullable = False)
	date 			= db.Column(db.Date, nullable = False)
	isSeller		= db.Column(db.Boolean, nullable = False)

	def __repr__(self):
		return '<Claim {}: "{}">'.format(self.claimid)

class Transaction(db.Model):
	transactionid	= db.Column(db.Integer, primary_key = True)
	claimidseller	= db.Column(db.Integer, nullable = False)
	claimidbuyer	= db.Column(db.Integer, nullable = False)

	def __repr__(self):
		return '<Transaction {}: "{}">'.format(self.transactionid)
