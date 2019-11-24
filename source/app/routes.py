from app import app, helper_functions, socketio, form_submissions, database_helpers
from app.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, render_template, request, session, url_for, abort, g, flash
from random import shuffle
from datetime import datetime
from sqlalchemy import and_, or_

CATEGORIES = ['All', 'Textbooks', 'Furniture', 'Food', 'Events', 'Software', 'Electronics',
 'Beauty and Personal Care', 'Clothes', 'School Supplies', 'Appliances']
CONTACT_METHOD = {
    "email": "Email (university provided)",
    "phonenumber": "Phone Number (if provided)",
    "personalemail": "Personal Email (if provided)"
}

# forces logout on browser close(); aka senses packets have stopped flowing
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
########################## LOGIN ###########################################
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

############################ ACCOUNT ROUTES ###############################
# The create account screen
@app.route('/create-account', methods=['GET', 'POST'])
def create_account(error=""):
    title = "Welcome to Craigversity!"
    CREATE_ERROR = "Need to fill in ALL fields marked with an '*'"
    errors = []
    if g.user:
        return redirect(url_for('user_home_screen'))
    if request.method == 'POST':
        [results, errors] = form_submissions.generate_new_account_form(request.form)
        if len(errors) == 0:
            added_successfully = database_helpers.add_user(results)
            if added_successfully:
                return redirect(url_for('login'))
            errors = "Could not process. Try again."
    return render_template('create-account.html', current_user_is_auth=False, error=errors, page_title=title, css_file=helper_functions.generate_linked_files('create-account'), )

# The user screen
@app.route('/user', methods=['GET', 'POST'])
def users_account():
    if g.user is None:
        return redirect(url_for('login'))
    account_info = g.user
    title = "USER: " + g.user.username
    if request.method == "GET":
        userid = (request.args.get('userid'))
        account_info = User.query.filter_by(userid=userid).first()
        if account_info is None:
            return redirect(url_for('not_found_error_item'))
        title = "USER: " + account_info.username
    return render_template('account-view.html',current_user_id=g.user.userid, current_user_is_auth=(g.user.userid > 0),  user_id=g.user.userid, CURRENT_USER_ID=g.user.userid, page_title=title, css_file=helper_functions.generate_linked_files('account-view'), account=account_info)

# The edit account screen
@app.route('/edit-account', methods=['GET', 'POST'])
def edit_account(error=""):
    if g.user is None:
        return redirect(url_for('login'))
    title = 'Edit Account'
    current_user = g.user
    error = ''
    if request.method == 'POST':
        [result, error] = form_submissions.get_modified_account_info(request.form, g.user.userid)
        if len(error) == 0 and check_password_hash(g.user.password, str(result['oldpassword'])):
            if result['deleteaccount'] == "delete":
                database_helpers.remove_user(g.user.userid)
            if database_helpers.update_current_user(g.user, result):
                return redirect(url_for('login'))
    return render_template('edit-account.html', current_user_id=g.user.userid, current_user_is_auth=(g.user.userid > 0),  error=error, current_user=current_user, CURRENT_USER_ID=g.user.userid, page_title=title, css_file=helper_functions.generate_linked_files('create-account'), )

###################################################################
###################### POSTINGS ###################################
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
            database_helpers.add_new_post(results, g.user)
            return redirect(url_for('login'))
    return render_template('create-posting-view.html', contact_options=CONTACT_METHOD, categories=CATEGORIES, current_user_id=g.user.userid, js_file="tag-javascript.js", current_user_is_auth=(g.user.userid > 0), page_title=title, error=error, css_file=helper_functions.generate_linked_files('create-posting-view'))

# NEED TO REWORK CONTACT METHOD!!!
@app.route('/edit-posting', methods=['GET', 'POST'])
def edit_posting(error=""):
    title = 'Edit Posting'
    if g.user is None:
        return redirect(url_for('login'))

    posting_info = database_helpers.get_post_id(request.args.get('postid'))
    if posting_info is None or g.user.userid != posting_info.userid:
        return redirect(url_for('user_home_screen'))

    if request.method == 'POST':
        [results, error] = form_submissions.get_form_create_post(request.form, CATEGORIES)
        if len(error) == 0:
            if result['deletepost']:
                database_helpers.remove_post_archive(results['postid'])
            database_helpers.modify_post_by_id(results, posting_info[0])
            return redirect(url_for('user_home_screen'))
    return render_template('edit-posting-view.html',contact_options=CONTACT_METHOD,  categories=CATEGORIES, js_file="tag-javascript.js", current_user_id=g.user.userid, current_user_is_auth=(g.user.userid > 0),  user_id=g.user.userid,  CURRENT_USER_ID=g.user.userid, page_title=title, error=error, css_file=helper_functions.generate_linked_files('create-posting-view'), post=posting_info)

# The posting screen
@app.route('/posting', methods=['GET'])
def full_posting_view():
    if g.user is None:
        return redirect(url_for('login'))
    #posting_info = {}
    if request.method == 'GET':
        [posting_info, user_info] = database_helpers.get_posting_by_id(request.args.get('postid'))
        if posting_info is None:
            return redirect(url_for('not_found_error_item'))
        title = "POSTING: " + posting_info.title
    return render_template('full-posting-view.html',current_user_id=g.user.userid, current_user_is_auth=(g.user.userid > 0), page_title=title, css_file=helper_functions.generate_linked_files('full-posting-view'), post=posting_info, poster_info=user_info)

########################################################################
# The home user logged in screen that lists postings
@app.route('/search-and-filter-postings', methods=['GET'])
def user_home_screen():
    title = "Search and Filter Postings!"
    if g.user is None:
        return redirect(url_for('login'))
    if request.method == 'GET':
        [submitted, randomize] = form_submissions.get_filters(request.args, True)
        # need to filter somehow
        categoryIsAll = True if submitted['category'] == 'All' else False
        if randomize:
            postings = database_helpers.generate_random_postings()
        else:
            # this is where the FILTERING should go
            #postings = database_helpers.generate_random_postings()
            if submitted['search'] == '':
                postings = Posting.query.filter(
                                    and_(
                                        Posting.price >= float(submitted['minPrice']),
                                        Posting.price <= float(submitted['maxPrice']),
                                         or_(Posting.category.contains(submitted['category']), categoryIsAll)
                                         )
                                    ).join(User).with_entities(
                                        Posting.postid, Posting.userid, User.username,
                                        Posting.title, Posting.price, Posting.description,
                                        User.rating).limit(30)
            else:
                postings = Posting.query.filter(
                                    and_(
                                        Posting.title.contains(submitted['search']),
                                        Posting.price >= float(submitted['minPrice']),
                                        Posting.price <= float(submitted['maxPrice']),
                                        or_(Posting.category.contains(submitted['category']), categoryIsAll)
                                        )
                                    ).join(User).with_entities(
                                        Posting.postid, Posting.userid, User.username,
                                        Posting.title, Posting.price, Posting.description,
                                        User.rating).limit(30)
    else:
        # do not bother filtering at all...
        submitted = form_submissions.get_filters('', True)
        # randomize
        postings = database_helpers.generate_random_postings()
    return render_template('user-view.html', categories=CATEGORIES, able_to_filter=True, submitted=submitted, current_user_id=g.user.userid, current_user_is_auth=(g.user.userid > 0), page_title=title, css_file=helper_functions.generate_linked_files('user-view'), filtered_postings=postings)

########################### CLAIMS ##########################################
# the claim pages
@app.route('/claim', methods=['GET', 'POST'])
def claim_submission():
    if g.user is None:
        return redirect(url_for('login'))
    title = "Claim Submission"
    error = ''
    IsSeller = False
    post_info = {'title': '', 'postid': '', 'username': '' }
    try:
        [posting_info, poster_info] = database_helpers.get_posting_by_id(request.args.get('postid'))
        if posting_info is None:
            return redirect(url_for('error'))
        post_info = helper_functions.get_post_info_claims(posting_info, poster_info)
        isSeller = (posting_info.userid == g.user.userid)
        if isSeller:
            title = "Seller " + title
        else:
            title = "Buyer " + title
    except Exception as e:
        error = "Please Try Resubmitting. Something went Wrong."
        return render_template('claim.html', error=error, post=post_info, isSeller=False, current_user_id=g.user.userid, current_user_is_auth=(g.user.userid > 0), page_title=title, css_file=helper_functions.generate_linked_files('claim') )

    if request.method == 'POST':
        [submitted, error] = form_submissions.get_new_claims_form(request.form, g.user, post_info['postid'])
        if len(error) == 0:
            [completed_claim, claim] = database_helpers.add_claim(submitted, post_info['postid'], g.user)
            if completed_claim:
                if database_helpers.check_for_transaction(claim):
                    print("Archived!: should give altered claim completion")
                    return redirect(url_for('claim_completion', is_transaction_complete=True ))
                return redirect(url_for('claim_completion', is_transaction_complete=False ))
            else:
                error = "Please resubmit your claim. There was an issue. You may have entered invalid data."


    return render_template('claim.html', error=error, post=post_info, isSeller=isSeller, current_user_id=g.user.userid, current_user_is_auth=(g.user.userid > 0), page_title=title, css_file=helper_functions.generate_linked_files('claim') )

@app.route('/claim-complete', methods=['GET', 'POST'])
def claim_completion(is_transaction_complete=False):
    if g.user is None:
        return redirect(url_for('login'))
    is_transaction_complete = request.args.get('is_transaction_complete')
    print(is_transaction_complete)
    return render_template('claim-complete.html', is_transaction_complete=is_transaction_complete=="True", title="Claim Complete", error='', current_user_id=g.user.userid, current_user_is_auth=(g.user.userid > 0), css_file=helper_functions.generate_linked_files('claim'))

# The HELP page
@app.route('/help-and-FAQ')
def help():
    return render_template('help.html')


@app.route('/remove-posting', methods=['GET', 'POST'])
def remove_posting_view(error=""):
    title = 'Remove Posting'
    if g.user is None:
        return redirect(url_for('login'))

    posting_info = database_helpers.get_post_id(request.args.get('postid'))
    if posting_info is None or g.user.userid != posting_info.userid:
        return redirect(url_for('user_home_screen'))

    if request.method == 'POST':
        posting_info_remove = Posting.query.filter_by(postid=request.args.get('postid')).first()
        db.session.delete(posting_info_remove)
        db.session.commit()
        return redirect(url_for('user_home_screen'))

    return render_template('remove-posting-view.html',contact_options=CONTACT_METHOD,  categories=CATEGORIES, js_file="tag-javascript.js", current_user_id=g.user.userid, current_user_is_auth=(g.user.userid > 0),  user_id=g.user.userid,  CURRENT_USER_ID=g.user.userid, page_title=title, error=error, css_file=helper_functions.generate_linked_files('create-posting-view'), post=posting_info)
