import re
from werkzeug.security import check_password_hash, generate_password_hash

# Returns email if in valid format; else returns false
def get_email(email_field):
    try:
        if re.search('\w+@(\w+.)*pitt.edu', str(email_field)) is not None:
            return email_field
        raise ValueError
    except Exception as e:
        return False

# verify password given in form; true for correct password, otherwise false
# user: takes USER class from model;
#       for TESTING object with value string of HASHED password
# password: string of UNhashed password passed in by the user on login
def verify_password(user, password):
    try:
        if user is None or not check_password_hash(user.password, str(password)):
            return False
        return True
    except Exception as e:
        raise



#########################################################################
# Home View Search and filter methods

def get_category(field):
    try:
        if str(field) == "All":
            return ''
        return str(field)
    except Exception as e:
        return ''

#               MAY WANT TO EDIT THIS
# takes inputted search textbox input for backend search
def get_search_text(field):
    try:
        if str(field).strip() == '':
            return ''
        return field
    except Exception as e:
        return ''

def get_max_price(field, min_field):
    try:
        field = float(field)
        min_field = float(min_field)
        if field > 0 and field > min_field and field <= 2000:
            return str(field)
        elif field > 2000:
            return '2000'
        else:
            return '0'
    except ValueError as e:
        return '0'

def get_min_price(field):
    try:
        field = float(field)
        if field > 0 and field > min_field and field <= 2000:
            return str(field)
        elif field > 2000:
            return '2000'
        else:
            return '0'
    except ValueError as e:
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
        return [False, "The title needs to be 1-30 characters long."]
    return [False, "The title needs to be 1-30 characters long. Your input was " + str(len(field)) + " characters."]

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
        if field == "email" or field == "phonenumber" or field == "personalemail":
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
    result['contactmethod'] = validate_preferred_contact(forms['preferredContact'])
    result['tags'] = validate_preferred_tags(forms['tags'])
    return result

def generate_return_values(given):
    error = []
    good_results = {}
    for key, elem in given.items():
        print("ELEM: is " + str(key) + "..." + str(elem))
        if elem[0]:
            good_results[key] = elem[1]
        else:
            error.append(str(elem[1]))
    return good_results, error


def get_form_create_post(forms, CATEGORIES):
    initial = validate_input(forms, CATEGORIES)
    return generate_return_values(initial)

#######################################################################
# The CREATE ACCOUNT Functions
def generate_new_account_form(forms):
    results = generate_fields_create_account(forms)
    return generate_return_values(results)


def get_username(email):
    try:
        username = str(email).split('@')
        if len(username) == 2 and username[0] != '':
            return [True, username[0]]
        raise ValueError
    except Exception as e:
        return [False, 'An unexpected error has occurred.']


def generate_fields_create_account(forms):
    new_account_info = {}
    new_account_info['email']           = validate_email(forms['email'])
    new_account_info['username']        = get_username(new_account_info['email'][1])
    new_account_info['password']        = validate_password(forms['password'], forms['password2'])
    new_account_info['phone']           = validate_phone_number(forms['phonenumber'])
    new_account_info['personalemail']   = validate_personal_email(forms['personalemail'])
    new_account_info['bio']             = validate_bio(forms['bio'])
    new_account_info['rating']          = [True, '5']
    new_account_info['numRatings']      = [True, '0']
    print(forms['phonenumber'])
    return new_account_info

def validate_email(field):
    try:
        field = get_email(str(field))
        if not field == False:
            return [True, field]
        raise ValueError
    except Exception as e:
        return [False, "The university email must end with a school domain (pitt.edu)."]

def validate_password(password1, password2):
    try:
        password1 = str(password1)
        password2 = str(password2)
        if password1 == password2:
            if len(password1) > 7 and len(password1) < 33:
                return [True, generate_password_hash(password1)]
        raise ValueError
    except Exception as e:
        return [False, "Both Password fields must match and have between 8 and 32 characters (inclusive)."]

### ADD MORE HERE ###
def validate_phone_number(field):
    try:
        phone_number = str(field)
        if len(phone_number) == 10:
            phone_number = '1' + phone_number
            return [True, phone_number]
        elif len(phone_number) == 11 and phone_number[0] == '1':
            return [True, phone_number]
        elif phone_number.split() == '':
            return [True, '']
    except Exception as e:
        return [False, "Phone number must be 10 characters long or 11 characters long with the country code being '1' in order to be processed."]
    return [True, '']


def validate_personal_email(field):
    try:
        field = str(field)
        if re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", field) is not None:
            return [True, field]
    except Exception as e:
        return [False, "The personal email address is not a legal value."]
    return [True, ""]

def validate_bio(field):
    try:
        field = str(field)
        return [True, field]
    except Exception as e:
        return [False, "The biography is unable to be processed. Possibly an invalid symbol."]

def get_modified_account_info(forms, userid):
    result = generate_fields_edit_account(forms, userid)
    print(result)
    return generate_return_values(result)

def validate_password_simple(password):
    try:
        password = str(password)
        return [True, password]
    except Exception as e:
        return [False, "Try Resubmitting information."]

def generate_fields_edit_account(forms, userid):
    new_account_info = {}
    new_account_info['userid']          = [True, str(userid)]
    if forms['newpassword'] and forms['newpassword'] != '':
        new_account_info['password']    = validate_password(forms['newpassword'], forms['newpassword2'])
    new_account_info['oldpassword']     = validate_password_simple(forms['oldpassword'])
    new_account_info['phonenumber']     = validate_phone_number(forms['phonenumber'])
    new_account_info['personalemail']   = validate_personal_email(forms['personalemail'])
    new_account_info['bio']             = validate_bio(forms['bio'])
    return new_account_info

#############################################################################
# Claims
def get_new_claims_form(forms, current_user, postid):
    results = generate_claims_forms(forms, current_user)
    return generate_return_values(results)

def generate_claims_forms(forms, current_user, postid):
    claim_info = {}
    claim_info['postid'] = [True, postid]