
def get_post_info_claims(posting_info, poster_info):
    return {
        'title': posting_info.title, 
        'postid': posting_info.postid,
        'username': poster_info.username
    }


# generate the linked files such as the CSS Stylesheets and JavaScripts
def generate_linked_files(filename):
    linked_css_files_and_javascripts = "stylesheets/{f}-styles.css".format(f=filename)
    return linked_css_files_and_javascripts
