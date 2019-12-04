from app import models, db
from sqlalchemy import *
from datetime import datetime

def generate_random_postings():
    result = models.Posting.query.join(models.User).with_entities(
        models.Posting.postid, models.Posting.userid, models.User.username,
        models.Posting.title, models.Posting.price, models.Posting.description,
        models.User.rating)
    return result

def add_new_post(form_input, current_user):
    db.session.add(models.Posting(
        userid = current_user.userid,
        date = datetime.now(),
        title = form_input['title'],
        description = form_input['description'],
        price = form_input['price'],
        category = form_input['category'],
        contactmethod = form_input['contactmethod'],
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
            return True, newClaim
    except Exception as e:
        db.session.rollback()
        return False, False
    return False, False

def check_for_transaction(claim):
    try:
        other_claim = models.Claim.query.filter(
            models.Claim.postid==claim.postid,
            models.Claim.sellerid==claim.sellerid,
            models.Claim.buyerid==claim.buyerid,
            models.Claim.usersubmitted!=claim.usersubmitted
        ).first()
        if other_claim is not None:
            newTransaction = models.Transaction(
                date            = datetime.now(),
                claimidseller   = claim.sellerid,
                claimidbuyer    = claim.buyerid
            )
            db.session.add(newTransaction)
            print("Try to Alter Ratings!")
            alter_ratings(claim, other_claim)
            print("Try to Archive!")
            if archive_posting(claim.postid, newTransaction):
                print("Archived! Now Delete The Claims:")
                delete_claim(claim.claimid)
                delete_claim(other_claim.claimid)
                print("Finished")
                return True
            else:
                raise ValueError
    except Exception as e:
        print("Rollback in check_for_transaction")
        db.session.rollback()
        return None
    return False

def delete_claim(claimid):
    try:
        models.Claim.query.filter_by(claimid=claimid).delete()
    except Exception as e:
        pass

def delete_user(userid):
    try:
        someUser = User.query.filter_by(userid=someUserID).first()
        db.session.delete(someUser)
        db.session.commit()
    except Exception as e:
        pass


def archive_posting(postid, transaction=None):
    try:
        post = models.Posting.query.filter_by(postid=postid).first()
        if transaction is not None:
            print("got Post")
            archivedPost = models.ArchivedPosting(
                transactionid   = transaction.transactionid,
                postid 			= post.postid,
                buyerid         = transaction.claimidbuyer,
                sellerid        = transaction.claimidseller,
                date 			= datetime.now(),
                title   		= post.title,
                description 	= post.description,
                price 			= post.price,
                category 		= post.category,
                contactmethod 	= post.contactmethod,
                tags 			= post.tags
            )
        else:
            archivedPost = models.ArchivedPosting(
                postid 			= post.postid,
                date 			= datetime.now(),
                title   		= post.title,
                description 	= post.description,
                price 			= post.price,
                category 		= post.category,
                contactmethod 	= post.contactmethod,
                tags 			= post.tags
            )

        db.session.add(archivedPost)
        db.session.delete(post)
        return True
    except Exception as e:
        db.session.rollback()
    return False

def get_new_rating(current_rating, current_number, new_rating):
    current_number += 1
    current_rating = current_rating * (current_number-1)/current_number + new_rating * 1/current_number
    return [current_rating, current_number]

def alter_ratings(claim, other_claim):
    print("Getting Ratings")
    user1 = models.User.query.filter_by(userid=claim.usersubmitted).first()
    user2 = models.User.query.filter_by(userid=other_claim.usersubmitted).first()
    print("Update the Ratings Manually")
    [user1.rating, user1.numRatings] = get_new_rating(user1.rating, user1.numRatings, other_claim.Rating)
    [user2.rating, user2.numRatings] = get_new_rating(user2.rating, user2.numRatings, claim.Rating)
    print("FINISHED alter ratings")

def get_postings(userid):
    try:
        postings = models.Posting.query.filter_by(userid=userid).all()
        print("Got postings for user")
        return postings
    except Exception as e:
        pass
    return None

def get_claims(userid):
    try:
        claims = models.Claim.query.filter_by(usersubmitted=userid).join(models.Posting).with_entities(
            models.Claim.date, models.Posting.title, models.Posting.postid
        ).all()
        print("Got Claims")
        return claims
    except Exception as e:
        pass
    return None

def get_sales(userid):
    try:
        sales = models.ArchivedPosting.query.filter_by(sellerid=userid).with_entities(
            models.ArchivedPosting.title, models.ArchivedPosting.buyerid, models.ArchivedPosting.price,
            ).join(
            models.Transaction).join(models.User, models.User.userid == models.ArchivedPosting.buyerid).with_entities(
                    models.Transaction.date, models.ArchivedPosting.title, models.ArchivedPosting.price,
                    models.User.username, models.User.userid).all()
        print("Got sales")
        return sales
    except Exception as e:
        pass
    return None

def get_purchases(userid):
    try:
        purchases = models.ArchivedPosting.query.filter_by(buyerid=userid).with_entities(
            models.ArchivedPosting.title, models.ArchivedPosting.sellerid, models.ArchivedPosting.price,
            ).join(
            models.Transaction).join(models.User, models.User.userid == models.ArchivedPosting.sellerid).with_entities(
                    models.Transaction.date, models.ArchivedPosting.title, models.ArchivedPosting.price,
                    models.User.username, models.User.userid).all()
        print("Got purchases")
        return purchases
    except Exception as e:
        pass
    return None
