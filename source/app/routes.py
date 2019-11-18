from app import app, helper_functions, socketio, form_submissions, database_helpers
from app.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, render_template, request, session, url_for, abort, g, flash
from random import shuffle
from datetime import datetime

CATEGORIES = ['All', 'Textbooks', 'Furniture', 'Food', 'Events', 'Software', 'Electronics',
 'Beauty and Personal Care', 'Clothes', 'School Supplies', 'Appliances']

@socketio.on('disconnect')
def disconnect_user():
    logout()

#######################################
# ROUTES START HERE
#######################################
# Log the user out
@app.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect(url_for('login'))

# Run at the beginning of each request before functions run to check if logged in
@app.before_request
def request_authentication():
    g.user = None
    if 'userid' in session:
        g.user = User.query.filter_by(userid=session['userid']).first()

# Given a email (universit), gives
def get_userid(email):
	rv = User.query.filter_by(email=email).first()
	return rv.userid if rv else None


### ERROR HANDLING PAGES
@app.route('/error')
def not_found_error_item():
    return render_template('404.html'), 404

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/')
def slash_redirect():
    return redirect(url_for('login'))


# The login screen
@app.route('/login', methods=['GET', 'POST'])
def login(error=""):
    title = "Login to Craigversity!"
    LOGIN_ERROR = "Invalid information was submitted. Please try again!"
    error = ''
    if g.user:
        return redirect(url_for('user_home_screen'))
    if request.method == "POST":
        error = LOGIN_ERROR
        email = form_submissions.get_email(request.form['email'])
        if not email == False:
            user = User.query.filter_by(email=email).first()
            if form_submissions.verify_password(user, request.form['password']):
                session['userid'] = user.userid
                return redirect(url_for('user_home_screen'))
    return render_template('login.html', current_user_is_auth=False, error=error, page_title=title, css_file=helper_functions.generate_linked_files('login'))


# The create account screen
@app.route('/create-account', methods=['GET', 'POST'])
def create_account(error=""):
    title = "Welcome to Craigversity!"
    CREATE_ERROR = "Need to fill in ALL fields marked with an '*'"
    if g.user:
        return redirect(url_for('user_home_screen'))
    if request.method == 'POST':

        if not request.form['email'] or '@pitt.edu' not in request.form['email']:
            error = 'You have to enter a valid Pitt email address'
        elif get_userid(request.form['email']) is not None:
            error = 'That email is already taken'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        else:
            db.session.add(User(
                username = request.form['email'].split('@')[0],
				email = request.form['email'],
				password = generate_password_hash(request.form['password']),
                phonenumber = request.form['phonenumber'],
                personalemail = request.form['personalemail'],
                bio = request.form['bio'],
                rating = 5,
                numRatings = 0))
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('create-account.html', current_user_is_auth=False, error=error, page_title=title, css_file=helper_functions.generate_linked_files('create-account'), )


# The home user logged in screen that lists postings
@app.route('/search-and-filter-postings', methods=['GET'])
def user_home_screen():
    title = "Search and Filter Postings!"
    if g.user is None:
        return redirect(url_for('login'))
    if request.method == 'GET':
        [submitted, randomize] = form_submissions.get_filters(request.form)
        # need to filter somehow
        if randomize:
            postings = database_helpers.generate_random_postings()
        else:
            # this is where the FILTERING should go
            postings = database_helpers.generate_random_postings()

    else:
        # do not bother filtering at all...
        submitted = form_submissions.get_filters('', True)
        # randomize
        postings = database_helpers.generate_random_postings()
    for elem in postings:
        print(elem)
    return render_template('user-view.html', able_to_filter=True, submitted=submitted, current_user_id=g.user.userid, current_user_is_auth=(g.user.userid > 0), page_title=title, css_file=helper_functions.generate_linked_files('user-view'), filtered_postings=postings)


# The new posting submission screen
@app.route('/new-posting-submission', methods=['GET', 'POST'])
def new_posting_submission(error=""):
    title = "Submit a New Posting!"
    error = []
    if g.user is None:
        return redirect(url_for('login'))
    if request.method == 'POST':
        [results, error] = form_submissions.get_form_create_post(request.form, CATEGORIES)
        if len(error) == 0:
            print(results['preferredContact'])
            results['preferredContact'] = form_submissions.validate_contact_method(g.user, results['preferredContact'])
            database_helpers.add_new_post(results, g.user)
            return redirect(url_for('login'))
    return render_template('create-posting-view.html', categories=CATEGORIES, current_user_id=g.user.userid, js_file="tag-javascript.js", current_user_is_auth=(g.user.userid > 0), page_title=title, error=error, css_file=helper_functions.generate_linked_files('create-posting-view'))


# The HELP page
@app.route('/help-and-FAQ')
def help():
    return render_template('help.html')


# The user screen
@app.route('/user', methods=['GET', 'POST'])
def users_account():
    if g.user is None:
        return redirect(url_for('login'))
    global CURRENT_USER_ID
    #account_info = {}
    account_info = g.user
    title = "USER: " + g.user.username
    if request.method == "GET":
        userid = (request.args.get('userid'))
        account_info = User.query.filter_by(userid=userid).first()
        if account_info is None:
            return redirect(url_for('not_found_error_item'))
        title = "USER: " + account_info.username
    return render_template('account-view.html',current_user_id=g.user.userid, current_user_is_auth=(g.user.userid > 0),  user_id=g.user.userid, CURRENT_USER_ID=g.user.userid, page_title=title, css_file=helper_functions.generate_linked_files('account-view'), account=account_info)


# The posting screen
@app.route('/posting', methods=['GET'])
def full_posting_view():
    if g.user is None:
        return redirect(url_for('login'))
    #posting_info = {}
    if request.method == 'GET':
        postid = request.args.get('postid')
        posting_info = Posting.query.filter_by(postid=postid).first()
        if posting_info is None:
            return redirect(url_for('not_found_error_item'))
        user_info = User.query.filter_by(userid=posting_info.userid).first()
    title = "POSTING: " + posting_info.title
    return render_template('full-posting-view.html',current_user_id=g.user.userid, current_user_is_auth=(g.user.userid > 0),  user_id=g.user.userid, CURRENT_USER_ID=g.user.userid, username=user_info.username, page_title=title, css_file=helper_functions.generate_linked_files('full-posting-view'), post=posting_info)

# The edit account screen
@app.route('/edit-account', methods=['GET', 'POST'])
def edit_account(error=""):
    if g.user is None:
        return redirect(url_for('login'))
    title = 'Edit Account'
    if request.method == 'POST':
        if not check_password_hash(g.user.password, str(request.form['oldpassword'])):
            error = "Old password does not match"
        elif request.form['newpassword'] != request.form['newpassword2']:
            error = "New passwords do not match"
        else:
            if not request.form['newpassword']:
                g.user.phonenumber = request.form['phonenumber']
                g.user.personalemail = request.form['personalemail']
                g.user.bio = request.form['bio']
                db.session.commit()
                return redirect(url_for('user_home_screen'))
            else:
                g.user.password = generate_password_hash(request.form['newpassword'])
                g.user.phonenumber = request.form['phonenumber']
                g.user.personalemail = request.form['personalemail']
                g.user.bio = request.form['bio']
                db.session.commit()
                return redirect(url_for('user_home_screen'))
    current_user = g.user
    return render_template('edit-account.html', current_user_id=g.user.userid, current_user_is_auth=(g.user.userid > 0),  error=error, current_user=current_user, CURRENT_USER_ID=g.user.userid, page_title=title, css_file=helper_functions.generate_linked_files('create-account'), )


@app.route('/edit-posting', methods=['GET', 'POST'])
def edit_posting(error=""):
    if g.user is None:
        return redirect(url_for('login'))
    post_id = (request.args.get('postid'))
    if post_id is None:
        return redirect(url_for('user_home_screen'))
    posting_info = Posting.query.filter_by(postid=post_id).first()
    if g.user.userid != posting_info.userid:
        return redirect(url_for('user_home_screen'))
    title = 'Edit Posting'
    if request.method == 'POST':
        if not request.form['title']:
            error = 'You have to enter a title'
        elif not request.form['category']:
            error = 'You have to choose a category'
        elif not request.form['price']:
            error = 'You have to enter a price'
        elif not request.form['description']:
            error = 'You have to enter a description'
        else:
            if request.form['preferredContact'] == "Email":
                contact = g.user.email
            elif request.form['preferredContact'] == "Phone":
                contact = g.user.phonenumber
            else:
                contact = g.user.personalemail
            posting_info.date = datetime.now()
            posting_info.title = request.form['title']
            posting_info.description = request.form['description']
            posting_info.price = request.form['price']
            posting_info.category = request.form['category']
            posting_info.contactmethod = contact
            posting_info.tags = request.form['tags']
            db.session.commit()
            return redirect(url_for('user_home_screen'))
    return render_template('edit-posting-view.html', js_file="tag-javascript.js", current_user_id=g.user.userid, current_user_is_auth=(g.user.userid > 0),  user_id=g.user.userid,  CURRENT_USER_ID=g.user.userid, page_title=title, error=error, css_file=helper_functions.generate_linked_files('create-posting-view'), post=posting_info)
