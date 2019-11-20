import pytest
import sys
sys.path.append("../source/app/")

########    ACCOUNT    ########

########    UNIVERSITY EMAIL    ########
from form_submissions import validate_email

def test_valid_uni_email_1():
    input_email = "jky10@pitt.edu"
    expected_output = [True, "jky10@pitt.edu"]
    assert validate_email(input_email) == expected_output, "Test Failed!"

def test_valid_uni_email_2():
    input_email = "jky10@cs.pitt.edu"
    expected_output = [True, "jky10@cs.pitt.edu"]
    assert validate_email(input_email) == expected_output, "Test Failed!"

def test_invalid_uni_email_1():
    input_email = "jky10@gmail.com"
    expected_output = [False, "jky10@pitt.edu"]
    assert validate_email(input_email)[0] == expected_output[0], "Test Failed!"

def test_invalid_uni_email_2():
    input_email = ""
    expected_output = [False, "jky10@pitt.edu"]
    assert validate_email(input_email)[0] == expected_output[0], "Test Failed!"

def test_invalid_uni_email_3():
    input_email = "jk\ay10@pitt.edu"
    expected_output = [False, "jky10@pitt.edu"]
    assert validate_email(input_email)[0] == expected_output[0], "Test Failed!"

def test_invalid_uni_email_4():
    input_email = "thisistoolongthisistoolongthisistoolongthisistoolongthisistoolongthisistoolongthisistoolongthisistoolongthisistoolongthisistoolong@pitt.edu"
    expected_output = [False, "jky10@pitt.edu"]
    assert validate_email(input_email)[0] == expected_output[0], "Test Failed!"


########    PASSWORD    ########
from form_submissions import validate_password

def test_valid_password_1():
    input_password1 = "12345678"
    input_password2 = "12345678"
    expected_output = [True, ""]
    assert validate_password(input_password1, input_password2)[0] == expected_output[0], "Test Failed!"

def test_valid_password_2():
    input_password1 = "12345678123456781234567812345678"
    input_password2 = "12345678123456781234567812345678"
    expected_output = [True, ""]
    assert validate_password(input_password1, input_password2)[0] == expected_output[0], "Test Failed!"

def test_invalid_password_1():
    input_password1 = "1234567"
    input_password2 = "1234567"
    expected_output = [False, ""]
    assert validate_password(input_password1, input_password2)[0] == expected_output[0], "Test Failed!"

def test_invalid_password_2():
    input_password1 = "123456781234567812345678123456780"
    input_password2 = "123456781234567812345678123456780"
    expected_output = [False, ""]
    assert validate_password(input_password1, input_password2)[0] == expected_output[0], "Test Failed!"

def test_invalid_password_3():
    input_password1 = "12345679"
    input_password2 = "12345678"
    expected_output = [False, ""]
    assert validate_password(input_password1, input_password2)[0] == expected_output[0], "Test Failed!"

def test_invalid_password_4():
    input_password1 = "123456\a78"
    input_password2 = "123456\a78"
    expected_output = [False, ""]
    assert validate_password(input_password1, input_password2)[0] == expected_output[0], "Test Failed!"


########    PHONE NUMBER    ########
from form_submissions import validate_phone_number

def test_valid_phone_num_1():
    input_phone_number = "0123456789"
    expected_output = [True, "10123456789"]
    assert validate_phone_number(input_phone_number)[0] == expected_output[0], "Test Failed!"

def test_valid_phone_num_2():
    input_phone_number = "10123456789"
    expected_output = [True, "10123456789"]
    assert validate_phone_number(input_phone_number)[0] == expected_output[0], "Test Failed!"

def test_valid_phone_num_2():
    input_phone_number = "012-345-6789"
    expected_output = [True, "0123456789"]
    assert validate_phone_number(input_phone_number)[0] == expected_output[0], "Test Failed!"

def test_valid_phone_num_2():
    input_phone_number = "1-(012)345-6789"
    expected_output = [True, "0123456789"]
    assert validate_phone_number(input_phone_number)[0] == expected_output[0], "Test Failed!"

def test_invalid_phone_num_1():
    input_phone_number = "10characte"
    expected_output = [False, "10123456789"]
    assert validate_phone_number(input_phone_number)[0] == expected_output[0], "Test Failed!"

def test_invalid_phone_num_2():
    input_phone_number = "11character"
    expected_output = [False, "10123456789"]
    assert validate_phone_number(input_phone_number)[0] == expected_output[0], "Test Failed!"

def test_invalid_phone_num_3():
    input_phone_number = "012345678"
    expected_output = [False, "10123456789"]
    assert validate_phone_number(input_phone_number)[0] == expected_output[0], "Test Failed!"

def test_invalid_phone_num_4():
    input_phone_number = "01234567891"
    expected_output = [False, "10123456789"]
    assert validate_phone_number(input_phone_number)[0] == expected_output[0], "Test Failed!"

def test_invalid_phone_num_5():
    input_phone_number = "101234567891"
    expected_output = [False, "10123456789"]
    assert validate_phone_number(input_phone_number)[0] == expected_output[0], "Test Failed!"


########    PERSONAL EMAIL    ########
from form_submissions import validate_personal_email

def test_valid_personal_email_1():
    input_email = "jky10@gmail.com"
    expected_output = [True, "jky10@gmail.com"]
    assert validate_personal_email(input_email)[0] == expected_output[0], "Test Failed!"

def test_invalid_personal_email_1():
    input_email = "jky\a10@gmail.com"
    expected_output = [False, "jky10@gmail.com"]
    assert validate_personal_email(input_email)[0] == expected_output[0], "Test Failed!"

def test_invalid_personal_email_2():
    input_email = "@gmail.com"
    expected_output = [False, "jky10@gmail.com"]
    assert validate_personal_email(input_email)[0] == expected_output[0], "Test Failed!"

def test_invalid_personal_email_3():
    input_email = "jky10@.com"
    expected_output = [False, "jky10@gmail.com"]
    assert validate_personal_email(input_email)[0] == expected_output[0], "Test Failed!"

def test_invalid_personal_email_4():
    input_email = "jky10@gmail."
    expected_output = [False, "jky10@gmail.com"]
    assert validate_personal_email(input_email)[0] == expected_output[0], "Test Failed!"

def test_invalid_personal_email_5():
    input_email = ""
    expected_output = [False, "jky10@gmail.com"]
    assert validate_personal_email(input_email)[0] == expected_output[0], "Test Failed!"

def test_invalid_personal_email_6():
    input_email = "thisistoolongthisistoolongthisistoolongthisistoolongthisistoolongthisistoolongthisistoolongthisistoolongthisistoolongthisistoolong@gmail.com"
    expected_output = [False, "jky10@gmail.com"]
    assert validate_personal_email(input_email)[0] == expected_output[0], "Test Failed!"


########    PERSONAL BIO    ########
from form_submissions import validate_bio

def test_valid_personal_bio_1():
    input_bio = "This is my persional bio"
    expected_output = [True, "This is my persional bio"]
    assert validate_bio(input_bio)[0] == expected_output[0], "Test Failed!"

def test_valid_personal_bio_2():
    input_bio = ""
    expected_output = [True, ""]
    assert validate_bio(input_bio)[0] == expected_output[0], "Test Failed!"

def test_valid_personal_bio_3():
    input_bio = "PERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBI"
    expected_output = [True, "This is my persional bio"]
    assert validate_bio(input_bio)[0] == expected_output[0], "Test Failed!"

def test_invalid_personal_bio_1():
    input_bio = "This is my \a persional bio"
    expected_output = [False, "This is my persional bio"]
    assert validate_bio(input_bio)[0] == expected_output[0], "Test Failed!"

def test_invalid_personal_bio_2():
    input_bio = "PERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIOPERSONALBIO"
    expected_output = [False, "This is my persional bio"]
    assert validate_bio(input_bio)[0] == expected_output[0], "Test Failed!"


########    POSTINGS    ########

########    TITLE    ########
from form_submissions import validate_title

def test_valid_title_1():
    input_title = "Title"
    expected_output = [True, "Title"]
    assert validate_title(input_title)[0] == expected_output[0], "Test Failed!"

def test_valid_title_2():
    input_title = "TITLETITLETITLETITLETITLETITLE"
    expected_output = [True, "Title"]
    assert validate_title(input_title)[0] == expected_output[0], "Test Failed!"

def test_valid_title_3():
    input_title = "T"
    expected_output = [True, "Title"]
    assert validate_title(input_title)[0] == expected_output[0], "Test Failed!"
    
def test_invalid_title_1():
    input_title = ""
    expected_output = [False, "Title"]
    assert validate_title(input_title)[0] == expected_output[0], "Test Failed!"

def test_invalid_title_1():
    input_title = "TITLETITLETITLETITLETITLETITLET"
    expected_output = [False, "Title"]
    assert validate_title(input_title)[0] == expected_output[0], "Test Failed!"

def test_invalid_title_1():
    input_title = "Title\a"
    expected_output = [False, "Title"]
    assert validate_title(input_title)[0] == expected_output[0], "Test Failed!"


########    PRICE    ########
from form_submissions import validate_price

def test_valid_price_1():
    input_price = "1.00"
    expected_output = [True, "1.00"]
    assert validate_price(input_price)[0] == expected_output[0], "Test Failed!"

def test_valid_price_2():
    input_price = "2000"
    expected_output = [True, "2000"]
    assert validate_price(input_price)[0] == expected_output[0], "Test Failed!"

def test_valid_price_3():
    input_price = "19.999"
    expected_output = [True, "19.99"]
    assert validate_price(input_price)[0] == expected_output[0], "Test Failed!"

def test_valid_price_4():
    input_price = ".99"
    expected_output = [True, "0.99"]
    assert validate_price(input_price)[0] == expected_output[0], "Test Failed!"

def test_invalid_price_1():
    input_price = "FREE"
    expected_output = [False, "0"]
    assert validate_price(input_price)[0] == expected_output[0], "Test Failed!"

def test_invalid_price_2():
    input_price = "2001"
    expected_output = [False, "0"]
    assert validate_price(input_price)[0] == expected_output[0], "Test Failed!"

def test_invalid_price_3():
    input_price = "-1"
    expected_output = [False, "0"]
    assert validate_price(input_price)[0] == expected_output[0], "Test Failed!"

def test_invalid_price_4():
    input_price = "0"
    expected_output = [False, "0"]
    assert validate_price(input_price)[0] == expected_output[0], "Test Failed!"

########    DESCRIPTION    ########
from form_submissions import validate_desc

def test_valid_description_1():
    input_desc = "description"
    expected_output = [True, "description"]
    assert validate_desc(input_desc)[0] == expected_output[0], "Test Failed!"

def test_valid_description_2():
    input_desc = ""
    expected_output = [True, ""]
    assert validate_desc(input_desc)[0] == expected_output[0], "Test Failed!"

def test_valid_description_3():
    input_desc = "descriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescriptio"
    expected_output = [True, "description"]
    assert validate_desc(input_desc)[0] == expected_output[0], "Test Failed!"

def test_invalid_description_1():
    input_desc = "description\a"
    expected_output = [False, ""]
    assert validate_desc(input_desc)[0] == expected_output[0], "Test Failed!"

    
    
########    PREFERRED CONTACT    ########
from form_submissions import validate_preferred_contact

def test_valid_contact_1():
    input_contact = "email"
    expected_output = [True, "email"]
    assert validate_preferred_contact(input_contact)[0] == expected_output[0], "Test Failed!"

def test_valid_contact_2():
    input_contact = "phonenumber"
    expected_output = [True, "phonenumber"]
    assert validate_preferred_contact(input_contact)[0] == expected_output[0], "Test Failed!"
    
def test_valid_contact_3():
    input_contact = "personalemail"
    expected_output = [True, "personalemail"]
    assert validate_preferred_contact(input_contact)[0] == expected_output[0], "Test Failed!"
        
def test_invalid_contact_1():
    input_contact = "other"
    expected_output = [False, "personalemail"]
    assert validate_preferred_contact(input_contact)[0] == expected_output[0], "Test Failed!"

    
########    TAGS    ########
from form_submissions import validate_preferred_tags

def test_valid_tags_1():
    input_contact = "this,that"
    expected_output = [True, ""]
    assert validate_preferred_tags(input_contact)[0] == expected_output[0], "Test Failed!"
  
    
def test_valid_tags_2():
    input_contact = "this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,thatt"
    expected_output = [True, ""]
    assert validate_preferred_tags(input_contact)[0] == expected_output[0], "Test Failed!"  

def test_valid_tags_3():
    input_contact = ""
    expected_output = [True, ""]
    assert validate_preferred_tags(input_contact)[0] == expected_output[0], "Test Failed!"  

def test_invalid_tags_1():
    input_contact = "this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,that,this,thattt"
    expected_output = [False, ""]
    assert validate_preferred_tags(input_contact)[0] == expected_output[0], "Test Failed!"

def test_invalid_tags_1():
    input_contact = "thi\as,that"
    expected_output = [False, ""]
    assert validate_preferred_tags(input_contact)[0] == expected_output[0], "Test Failed!"