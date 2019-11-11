from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash
from app import *
from models import db, User, Book

#########################################################################################
# Utilities
#########################################################################################

# Given a email (universit), gives
def get_userid(email):
	rv = User.query.filter_by(email=email).first()
	return rv.userid if rv else None

# Run at the beginning of each request before functions run to check if logged in
@app.before_request
def before_request():
	g.user = None
	if 'userid' in session:
		g.user = User.query.filter_by(userid=session['userid']).first()

#########################################################################################
# User account management page routes
#########################################################################################

@app.route('/login', methods=['GET', 'POST'])
def login():
	"""Logs the user in."""
	if g.user:
		return redirect(url_for('home'))
	error = None
	if request.method == 'POST':

		user = User.query.filter_by(username=request.form['username']).first()
		if user is None:
			error = 'Invalid username'
		elif user.password != request.form['password']:
			error = 'Invalid password'
		else:
			flash('You were logged in')
			session['userid'] = user.userid
			return redirect(url_for('home'))

	return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
	"""Registers the user."""
	if g.user:
		return redirect(url_for('home'))

	error = None
	if request.method == 'POST':
		if not request.form['username']:
			error = 'You have to enter a username'
        elif get_userid(request.form['username']) is not None:
        	error = 'The username is already taken'
		elif not request.form['email'] or '@pitt.edu' not in request.form['email']:
			error = 'You have to enter a valid Pitt email address'
		elif not request.form['password']:
			error = 'You have to enter a password'
		elif request.form['password'] != request.form['password2']:
			error = 'The two passwords do not match'
        elif not request.form['phonenumber']:
			error = 'You have to enter a phone number'
        elif not request.form['contactmethod']:
			error = 'You have to enter a contact method'
		else:
			db.session.add(User(
				username = request.form['username'],
				email = request.form['email'],
				password = request.form['password'],
                phonenumber = request.form['phonenumber'],
                personalemail = request.form['personalemail'],
                contactmethod = request.form['contactmethod'],
                bio = request.form['bio']))
			db.session.commit()
			flash('You were successfully registered! Please log in.')
			return redirect(url_for('login'))

	return render_template('register.html', error=error)

@app.route('/logout')
def logout():
	"""Logs the user out."""
	flash('You were logged out. Thanks!')
	session.pop('userid', None)
	return redirect(url_for('home'))

@app.route('/home')
def home():
