import re
from werkzeug.security import check_password_hash

# Returns email if in valid format; else returns false
def get_email(email_field):
    if re.search('.+@(.*.)*pitt.edu', str(email_field)) is not None:
        return email_field
    return False

# verify password given in form; true for correct password, otherwise false
def verify_password(user, password):
    if user is None or not check_password_hash(user.password, str(password)):
        return False
    return True


#########################################################################
# Home View Search and filter methods

def get_category(field):
    if str(field) == "All":
        return ''
    return str(field)

################## MAY WANT TO EDIT THIS ##################
# takes inputted search textbox input for backend search
def get_search_text(field):
    if str(field).strip() == '':
        return ''
    return field

def get_max_price(field, min_field):
    field = float(field)
    min_field = float(min_field)
    if field > 0 and field > min_field and field <= 2000:
        return str(field)
    elif field > 2000:
        return '2000'
    else:
        return '0'

def get_max_price(field):
    field = float(field)
    if field > 0 and field <= 2000:
        return str(field)
    elif field > 2000:
        return '2000'
    else:
        return '0'

def should_randomize(submitted):
    return submitted == {'minPrice': '0', 'maxPrice': '0', 'search': '', 'category': ''}

def get_filters(forms, get_recieved=False):
    if get_recieved:
        submitted = {}
        submitted['minPrice'] = get_min_price(forms['minPrice'])
        submitted['maxPrice'] = get_max_price(forms['maxPrice'], submitted['minPrice'])
        submitted['search'] = get_search_text(forms['search'])
        submitted['category'] = get_category(forms['category'])
        return [submitted, should_randomize(submitted)]
    else:
        return [{'minPrice': '0', 'maxPrice': '0', 'search': '', 'category': ''}, True]


############################## New Posting Submission #####################
# verifies it is 30 chars or shorter
def validate_title(field):
    try:
        field = str(field)
        if len(field) > 0 and len(field) <31:
            return [True, field]
    except Exception as e:
        return [False, "Title is too long. Needs to be 1-30 characters long. Your input was " + str(len(field))]
    return [False, "Title is too long. Needs to be 1-30 characters long. Your input was " + str(len(field))]

# this should never really fail. It is on us if it does
def validate_category(field, CATEGORIES):
    try:
        field = str(field)
        if field in CATEGORIES:
            return [True, field]
    except Exception as e:
        return [False, "Category was not specified. Try resubmitting!"]
    return [False, "Invalid preffered contact method. Try resubmitting."]

# validates that price is in range of 0-2000; cuts of after 2nd decimal place
def validate_price(field):
    try:
        field = round(float(field), 2)
        if field > 0 and field <= 2000:
            return [True, field]
        raise ValueError
    except ValueError as e:
        return [False, "Invalid price. Needs to be in the range of 0 to 2,000 inclusive."]
    return [False, "Invalid preffered contact method. Try resubmitting."]

# ensure description is less than 1001 chars long.
def validate_desc(field):
    try:
        field = str(field)
        if len(field) > 1000:
            return [False, "Your short description cannot be longer than 1,000 characters long."]
    except Exception as e:
        return [False, "Invalid short description."]
    return [True, field]

# returns preferred contact value; should alk
def validate_preferred_contact(field):
    try:
        field = str(field)
        if field == "Email" or field == "Phone" or field == "PersonalEmail":
            return [True, field]
    except Exception as e:
        return [False, "Invalid preffered contact method. Try resubmitting."]
    return [False, "Invalid preffered contact method. Try resubmitting."]

def validate_preferred_tags(field):
    try:
        field = str(field)
        if len(field) < 1000:
            if len(field.split(',')) > 50:
                return [False, "Too many tags. The maximum tags are 50. Maximum character limit is 1,000"]
            return [True, field]
        raise ValueError
    except Exception as e:
        return [False, "Too many tags. Maximum character limit is 1,000"]

def validate_input(forms, CATEGORIES):
    result = {}
    result['title'] = validate_title(forms['title'])
    result['category'] = validate_category(forms['category'], CATEGORIES)
    result['price'] = validate_price(forms['price'])
    result['description'] = validate_desc(forms['description'])
    result['preferredContact'] = validate_preferred_contact(forms['preferredContact'])
    result['tags'] = validate_preferred_tags(forms['tags'])
    return result


def validate_contact_method(current_user, method):
    try:
        if form_input['preferredContact'] == 'PersonalEmail':
            return current_user.personalemail
        elif form_input['preferredContact'] == 'Phone':
            return current_user.phone
    except Exception as e:
        return current_user.email
    return current_user.email


def get_form_create_post(forms, CATEGORIES):
    initial = validate_input(forms, CATEGORIES)
    error = []
    good_results = {}
    for key, elem in initial.items():
        if elem[0]:
            good_results[key] = elem[1]
        else:
            error.append(str(elem[1]))
    return good_results, error
