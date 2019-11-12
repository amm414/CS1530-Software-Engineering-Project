from app import app, helper_functions, socketio
from app.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, render_template, request, session, url_for, abort, g, flash
from random import shuffle

DEBUG = True
if DEBUG:
    CURRENT_USER_ID = 3
    USERS = helper_functions.get_simple_data_users()
    POSTINGS = helper_functions.get_simple_data_postings()


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
    if g.user:
        return redirect(url_for('user_home_screen'))
    if request.method == "POST":
        error = "Incorrect Information Submitted"
        user = User.query.filter_by(email=request.form['email']).first()
        if user is None or not check_password_hash(user.password, str(request.form['password'])):
            error = "Incorrect Information Submitted"
        else:
            session['userid'] = user.userid
            return redirect(url_for('user_home_screen'))
    return render_template('login.html', CURRENT_USER_ID=CURRENT_USER_ID, error=error, page_title=title, css_file=helper_functions.generate_linked_files('login'),)


# The create account screen
@app.route('/create-account')
def create_account():
    title = "Welcome to Craigversity!"
    return render_template('create-account.html',  CURRENT_USER_ID=CURRENT_USER_ID, user_id=CURRENT_USER_ID, page_title=title, css_file=helper_functions.generate_linked_files('create-account'), )


# The home user logged in screen that lists postings
@app.route('/search-and-filter-postings', methods=['GET'])
def user_home_screen():
    if g.user is None:
        return redirect(url_for('login'))
    title = "Search and Filter Postings!"
    postings = POSTINGS
    submitted = {'minPrice': ''}
    submitted = {'maxPrice': ''}
    submitted = {'search': ''}
    submitted = {'category': ''}
    if request.method == 'GET':
        # need to filter somehow
        userid = (request.args.get('userid'))
        submitted['minPrice'] = request.args.get('minPrice')
        submitted['maxPrice'] = request.args.get('maxPrice')
        submitted['search'] = request.args.get('search')
        submitted['category'] = request.args.get('category')
        shuffle(POSTINGS)

    for key, item in submitted.items():
        if item is None:
            submitted[key] = ''
            if key == "minPrice" or key == "maxPrice":
                submitted[key] = "0"
    return render_template('user-view.html', able_to_filter=True, submitted=submitted, CURRENT_USER_ID=CURRENT_USER_ID, user_id=CURRENT_USER_ID, page_title=title, css_file=helper_functions.generate_linked_files('user-view'), filtered_postings=postings)


# The new posting submission screen
@app.route('/new-posting-submission')
def new_posting_submission():
    if g.user is None:
        return redirect(url_for('login'))
    title = "Submit a New Posting!"
    return render_template('create-posting-view.html', user_id=CURRENT_USER_ID,  CURRENT_USER_ID=CURRENT_USER_ID, page_title=title, css_file=helper_functions.generate_linked_files('create-posting-view'))


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
    account_info = {}
    if request.method == "GET":
        userid = (request.args.get('userid'))
        for user in USERS:
            if user['userid'] == userid:
                account_info = user
    if len(account_info) == 0:
        return redirect(url_for('not_found_error_item'))
    title = "USER: " + account_info['username']
    return render_template('account-view.html', user_id=CURRENT_USER_ID, CURRENT_USER_ID=CURRENT_USER_ID, page_title=title, css_file=helper_functions.generate_linked_files('account-view'), account=account_info)


# The posting screen
@app.route('/posting', methods=['GET'])
def full_posting_view():
    if g.user is None:
        return redirect(url_for('login'))
    posting_info = {}
    if CURRENT_USER_ID == -1:
        return redirect(url_for('login'))
    if request.method == 'GET':
        postid = request.args.get('postid')
        for post in POSTINGS:
            if postid == post['post_id']:
                posting_info = post
        if len(posting_info) == 0:
            return redirect(url_for('not_found_error_item'))

    title = "POSTING: " + posting_info['title']
    return render_template('full-posting-view.html', user_id=CURRENT_USER_ID, CURRENT_USER_ID=CURRENT_USER_ID, page_title=title, css_file=helper_functions.generate_linked_files('full-posting-view'), post=posting_info)
