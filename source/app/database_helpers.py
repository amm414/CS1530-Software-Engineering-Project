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

def get_post_id(postid):
    try:
        if postid is None and not int(postid) > 0:
            return None
    except Exception as e:
        return None
    current_post_info = models.Posting.query.filter_by(postid=postid).join(
        models.User).with_entities(
        models.Posting.postid, models.Posting.title, models.Posting.category,
        models.Posting.price, models.Posting.description,
        models.Posting.contactmethod, models.Posting.tags,
        models.User.phonenumber, models.User.email, models.User.userid,
        models.User.username, models.User.rating, models.User.personalemail
    ).first()
    return current_post_info

def modify_post_by_id(results, postid):
    models.Posting.query.filter_by(postid=postid).update(dict(results))
    db.session.commit()

def update_current_user(current_user, result):
    if 'password' in result:
        print("change password")
        current_user.password = result['password']
    current_user.phonenumber = result['phonenumber']
    current_user.personalemail = result['personalemail']
    current_user.bio = result['bio']
    db.session.commit()
    return True

def get_posting_by_id(postid):
    posting_info = models.Posting.query.filter_by(postid=postid).first()
    if posting_info.contactmethod == 'personalemail':
        poster_info = models.User.query.filter_by(userid=posting_info.userid).with_entities(
            models.User.personalemail, models.User.rating
        ).first()
    elif posting_info.contactmethod == "phonenumber":
        poster_info = models.User.query.filter_by(userid=posting_info.userid).with_entities(
            models.User.phonenumber, models.User.rating
        ).first()
    else:
        poster_info = models.User.query.filter_by(userid=posting_info.userid).with_entities(
            models.User.email, models.User.rating
        ).first()
    return posting_info, poster_info
