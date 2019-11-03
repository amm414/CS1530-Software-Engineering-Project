from flask import Flask
from flask import render_template
app = Flask(__name__)

# generate the linked files such as the CSS Stylesheets and JavaScripts
def generate_linked_files(filename):
    linked_css_files_and_javascripts = "stylesheets/{f}-styles.css".format(f=filename)
    return linked_css_files_and_javascripts

def generate_postings():
    postings = []
    base = {'title': "A Used Couch", 'poster_username': "abd142", 'stars': int(3), 'price': '42.00', 'post_id': 1, 'link': "/posting/1", 'description': "The couch is in very good condition. Got it 1 year ago and need to get rid of it before I move. I am willing to bargain if needed." }
    for i in range(30):
        postings.append(base.copy())
    ind = 1
    for post in postings:
        post['post_id'] = str(ind)
        post['link'] = '/posting/' + str(ind)
        ind = ind + 1
    return postings

@app.route('/')
@app.route('/index')
@app.route('/login.html')
def index():
    title = "Login to Craigversity!"
    return render_template('login.html', page_title=title, css_file=generate_linked_files('login'), )


@app.route('/create-account')
@app.route('/create-account.html')
def create_account():
    title = "Welcome to Craigversity!"
    return render_template('create-account.html', page_title=title, css_file=generate_linked_files('create-account'), )


@app.route('/search-and-filter-postings')
@app.route('/search-and-filter-postings.html')
def user_home_screen():
    title = "Search and Filter Postings!"
    postings = generate_postings()
    return render_template('user-view.html', page_title=title, css_file=generate_linked_files('user-view'), filtered_postings=postings)


if __name__=="__main__":
    app.run(debug=True)
