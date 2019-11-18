from app import models, db
from sqlalchemy import *
from datetime import datetime

def generate_random_postings():
    result = models.Posting.query.join(models.User).with_entities(
        models.Posting.postid, models.Posting.userid, models.User.username,
        models.Posting.title, models.Posting.price, models.Posting.description,
        models.User.rating).order_by(func.random()).limit(30)
    return result


def add_new_post(form_input, current_user):
    db.session.add(models.Posting(
        userid = current_user.userid,
        username = current_user.username,
        date = datetime.now(),
        title = form_input['title'],
        description = form_input['description'],
        price = form_input['price'],
        category = form_input['category'],
        contactmethod = form_input['description'],
        tags = form_input['tags']))
    db.session.commit()
    return True

def add_user(new_user_info):
    db.session.add(models.User(
        username        = new_user_info['username'],
        email           = new_user_info['email'],
        password        = new_user_info['password'],
        phonenumber     = new_user_info['phone'],
        personalemail   = new_user_info['personalemail'],
        bio             = new_user_info['bio'],
        rating          = new_user_info['rating'],
        numRatings      = new_user_info['numRatings'],
    ))
