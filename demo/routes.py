from flask import Flask, redirect, render_template, request, session, url_for, abort, g, flash
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

USERS = [
{'userid': '1', 'username': 'abc1234', 'password': 'pbkdf2:sha256:150000$scEFdLrX$9c3882bb4c885dad2d5cb3b93ee694c52963b5b08e60ce95ccb2f7dd15a5d3c7', 'email': 'abc1234@pitt.edu', 'personalemail': 'abcdef@gmail.com', 'phonenumber': '1-412-445-6789', 'rating': '4.02', 'bio': 'Hello I am Bob Ross, and I am an English Lit major. I am in my sophmore year. I am often at campus, so that is where the transactions should take place. '},
{'userid': '2', 'username': 'abd142', 'password': 'pbkdf2:sha256:150000$YqGut7jP$7ca97641e6e1e2c58b40438d2c09219ef4a4582200bc317013393b2eba1d93b3', 'email': 'abd142@pitt.edu', 'personalemail': 'helloworld@yahoo.com', 'phonenumber': '1-561-203-5234', 'rating': '3.65', 'bio': 'Hello, I hope to work with you!'},
{'userid': '3', 'username': 'admin', 'password': 'pbkdf2:sha256:150000$XpqPLa3C$6676364190fea89e3c64a6aa40d3ba9253f5dbf350fcd16f9f060a0f6f0e0416', 'email': 'admin@pitt.edu', 'personalemail': 'admin@admin.edu', 'phonenumber': '1-412-123-4569', 'rating': '0', 'bio': 'This is an admin account!'}
]

POSTINGS = [{'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '1', 'link': '/posting?1', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '2', 'link': '/posting?2', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '3', 'link': '/posting?3', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '4', 'link': '/posting?4', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '5', 'link': '/posting?5', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '6', 'link': '/posting?6', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '7', 'link': '/posting?7', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '8', 'link': '/posting?8', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '9', 'link': '/posting?9', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '10', 'link': '/posting?10', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '11', 'link': '/posting?11', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '12', 'link': '/posting?12', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '13', 'link': '/posting?13', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '14', 'link': '/posting?14', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '15', 'link': '/posting?15', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '16', 'link': '/posting?16', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '17', 'link': '/posting?17', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '18', 'link': '/posting?18', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '19', 'link': '/posting?19', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '20', 'link': '/posting?20', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '21', 'link': '/posting?21', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '22', 'link': '/posting?22', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '23', 'link': '/posting?23', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '24', 'link': '/posting?24', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '25', 'link': '/posting?25', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '26', 'link': '/posting?26', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '27', 'link': '/posting?27', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '28', 'link': '/posting?28', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '29', 'link': '/posting?29', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}, {'title': 'A Used Couch', 'poster_username': 'abd142', 'stars': 3, 'price': '42.00', 'post_id': '30', 'link': '/posting?30', 'description': 'The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed.'}]

CURRENT_USER_ID = 1

# generate the linked files such as the CSS Stylesheets and JavaScripts
def generate_linked_files(filename):
    linked_css_files_and_javascripts = "stylesheets/{f}-styles.css".format(f=filename)
    return linked_css_files_and_javascripts

def generate_postings():
    postings = []
    base = {'title': "A Used Couch", 'poster_username': "abd142", 'stars': int(3), 'requirements': '', 'price': '42.00', 'post_id': 1, 'link': "/posting/1", 'description': "The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed." }
    for i in range(30):
        postings.append(base.copy())
    ind = 1
    for post in postings:
        post['post_id'] = str(ind)
        post['link'] = '/posting?' + str(ind)
        ind = ind + 1
    return postings

#######################################
# ROUTES START HERE
#######################################

### ERROR HANDLING PAGES
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
    if request.method == "POST":
        error = "There was an issue: please retry submitting!"
        CURRENT_USER_ID = -1
        for i, user in enumerate(USERS, start=1):
            if user['email'] == request.form['email']:
                error = "Password is wrong!"
                if check_password_hash(user['password'], request.form['password']):
                    CURRENT_USER_ID = i
        if CURRENT_USER_ID > 0:
            return redirect(url_for('user_home_screen'))
    return render_template('login.html', error=error, page_title=title, css_file=generate_linked_files('login'),)


# The create account screen
@app.route('/create-account')
def create_account():
    if CURRENT_USER_ID == -1:
        redirect("/login")
    title = "Welcome to Craigversity!"
    return render_template('create-account.html', user_id=CURRENT_USER_ID, page_title=title, css_file=generate_linked_files('create-account'), )


# The home user logged in screen that lists postings
@app.route('/search-and-filter-postings')
def user_home_screen():
    if CURRENT_USER_ID == -1:
        redirect("/login")
    title = "Search and Filter Postings!"
    postings = POSTINGS
    return render_template('user-view.html', able_to_filter=True, user_id=CURRENT_USER_ID, page_title=title, css_file=generate_linked_files('user-view'), filtered_postings=postings)


# The new posting submission screen
@app.route('/new-posting-submission')
def new_posting_submission():
    if CURRENT_USER_ID == -1:
        redirect("/login")
    title = "Submit a New Posting!"
    return render_template('create-posting-view.html', user_id=CURRENT_USER_ID, page_title=title, css_file=generate_linked_files('create-posting-view'))


# The HELP page
@app.route('/help-and-FAQ')
def help():
    return render_template('help.html')


# The user screen
@app.route('/users')
def users_account():
    if CURRENT_USER_ID == -1:
        redirect("/login")
    user_id = 1
    account_info = USERS[user_id-1]
    title = "USER: " + account_info['username']
    return render_template('account-view.html', user_id=CURRENT_USER_ID, page_title=title, css_file=generate_linked_files('account-view'), account=account_info)


# The posting screen
@app.route('/posting')
def full_posting_view():
    if CURRENT_USER_ID == -1:
        redirect("/login")
    posting_id = 12
    posting_info = POSTINGS[posting_id-1]
    title = "POSTING: " + posting_info['title']
    return render_template('full-posting-view.html', user_id=CURRENT_USER_ID, page_title=title, css_file=generate_linked_files('full-posting-view'), post=posting_info)


if __name__=="__main__":
    app.run(debug=True)
