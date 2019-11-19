import pytest
import sys
sys.path.append("../source/app/")
from form_submissions import validate_email

def test_valid_email_1():
    input_email = "jky10@pitt.edu"
    expected_output = [True, "jky10@pitt.edu"]
    assert validate_email(input_email) == expected_output, "Test Failed!"


def test_valid_email_2():
    input_email = "jky10@cs.pitt.edu"
    expected_output = [True, "jky10@cs.pitt.edu"]
    assert validate_email(input_email) == expected_output, "Test Failed!"


def test_invalid_email_1():
    input_email = "jky10@gmail.com"
    expected_output = [False, "jky10@pitt.edu"]
    assert validate_email(input_email)[0] == expected_output[0], "Test Failed!"


def test_invalid_email_2():
    input_email = ""
    expected_output = [False, "jky10@pitt.edu"]
    assert validate_email(input_email)[0] == expected_output[0], "Test Failed!"


def test_invalid_email_3():
    input_email = "jk\ay10@pitt.edu"
    expected_output = [False, "jky10@pitt.edu"]
    assert validate_email(input_email)[0] == expected_output[0], "Test Failed!"


def test_invalid_email_4():
    input_email = "thisistoolongthisistoolongthisistoolongthisistoolongthisistoolongthisistoolongthisistoolongthisistoolongthisistoolongthisistoolong@pitt.edu"
    expected_output = [False, "jky10@pitt.edu"]
    assert validate_email(input_email)[0] == expected_output[0], "Test Failed!"
