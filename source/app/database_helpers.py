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
    try:
        newUser = models.User(
            username        = new_user_info['username'],
            email           = new_user_info['email'],
            password        = new_user_info['password'],
            phonenumber     = new_user_info['phone'],
            personalemail   = new_user_info['personalemail'],
            bio             = new_user_info['bio'],
            rating          = float(new_user_info['rating']),
            numRatings      = int(new_user_info['numRatings']),
        )
        db.session.add(newUser)
        db.session.commit()
        db.session.refresh(newUser)
        if newUser.userid is None:
            return False
        return True
    except Exception as e:
        return False
    return False

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
        current_user.password = result['password']
    current_user.phonenumber = result['phonenumber']
    current_user.personalemail = result['personalemail']
    current_user.bio = result['bio']
    db.session.commit()
    return True

def get_posting_by_id(postid):
    posting_info = models.Posting.query.filter_by(postid=postid).first()
    if posting_info is None:
        return None, None
    if posting_info.contactmethod == 'personalemail':
        poster_info = models.User.query.filter_by(userid=posting_info.userid).with_entities(
            models.User.personalemail, models.User.rating, models.User.userid, models.User.username
        ).first()
    elif posting_info.contactmethod == "phonenumber":
        poster_info = models.User.query.filter_by(userid=posting_info.userid).with_entities(
            models.User.phonenumber, models.User.rating, models.User.userid, models.User.username
        ).first()
    else:
        poster_info = models.User.query.filter_by(userid=posting_info.userid).with_entities(
            models.User.email, models.User.rating, models.User.userid, models.User.username
        ).first()
    return posting_info, poster_info

def remove_user(userid):
    User.query.filter_by(userid=userid).delete()
    db.session.commit()

def remove_post_archive(postid):
    Posting.query.filter_by(postid=postid).delete()
    db.session.commit()

def get_user_by_email(email):
    return models.User.query.filter_by(email=email).first()

def add_claim(form, postid, user):
    try:
        post_info, poster_info = get_posting_by_id(postid)
        if user.userid == post_info.userid and not form['buyeremail'] == False:
            buyer_info = get_user_by_email(form['buyeremail'])
            newClaim = models.Claim(
                postid          = postid,
                sellerid        = user.userid,
                buyerid         = buyer_info.userid,
                usersubmitted   = user.userid,
                date            = datetime.now(),
                Rating          = form['rating']
            )
            db.session.add(newClaim)
            db.session.commit()
            db.session.refresh(newClaim)
            if newClaim.claimid is None:
                return False, False
            return True, newClaim
        elif not user.userid == post_info.userid:
            newClaim = models.Claim(
                postid          = postid,
                sellerid        = post_info.userid,
                buyerid         = user.userid,
                usersubmitted   = user.userid,
                date            = datetime.now(),
                Rating          = form['rating']
            )
            db.session.add(newClaim)
            db.session.commit()
            db.session.refresh(newClaim)
            if newClaim.claimid is None:
                return False, False
            return True, newClaim
    except Exception as e:
        db.session.rollback()
        return False, False

def check_for_transaction(claim):
    other_claim = models.Claim.query.filter(
        models.Claim.postid==claim.postid,
        models.Claim.sellerid==claim.sellerid,
        models.Claim.buyerid==claim.buyerid,
        models.Claim.claimid!=claim.claimid
    ).first()
    if other_claim is not None:
        newTransaction = models.Transaction(
            claimidseller   = claim.sellerid,
            claimidbuyer    = claim.buyerid
        )
        db.session.add(newTransaction)
        db.session.commit()
        db.session.refresh(newTransaction)
        if newTransaction.transactionid is not None:
            archive_posting(claim.postid)
            return True
        db.session.rollback()
    return False

def archive_posting(postid):
    try:
        models.Posting.query.filter_by(postid=postid).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
