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
