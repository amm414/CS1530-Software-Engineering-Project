from app import app, helper_functions
from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, render_template, request, session, url_for, abort, g, flash

DEBUG = True
if DEBUG:
    CURRENT_USER_ID = 3
    USERS = helper_functions.get_simple_data_users()
    POSTINGS = helper_functions.get_simple_data_postings()



#######################################
# ROUTES START HERE
#######################################




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
    CURRENT_USER_ID = -1
    title = "Login to Craigversity!"
    if request.method == "POST":
        error = "Incorrect Information Submitted"
        for i, user in enumerate(USERS, start=1):
            if user['email'] == request.form['email']:
                error = "Password is wrong!"
                if check_password_hash(user['password'], request.form['password']):
                    CURRENT_USER_ID = i
        if CURRENT_USER_ID > 0:
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
    if CURRENT_USER_ID == -1:
        return redirect(url_for('login'))
    title = "Search and Filter Postings!"
    postings = POSTINGS
    return render_template('user-view.html', able_to_filter=True, CURRENT_USER_ID=CURRENT_USER_ID, user_id=CURRENT_USER_ID, page_title=title, css_file=helper_functions.generate_linked_files('user-view'), filtered_postings=postings)


# The new posting submission screen
@app.route('/new-posting-submission')
def new_posting_submission():
    if CURRENT_USER_ID == -1:
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
    posting_info = {}
    if CURRENT_USER_ID == -1:
        return redirect(url_for('login'))
    if request.method == 'GET':
        postid = request.args.get('postid')
        for post in POSTINGS:
            if postid == post['post_id']:
                posting_info = post

    title = "POSTING: " + posting_info['title']
    return render_template('full-posting-view.html', user_id=CURRENT_USER_ID, CURRENT_USER_ID=CURRENT_USER_ID, page_title=title, css_file=helper_functions.generate_linked_files('full-posting-view'), post=posting_info)
