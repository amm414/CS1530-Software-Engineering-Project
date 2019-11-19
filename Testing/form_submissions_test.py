import sys
sys.path.append("../source/app/")
from form_submissions import validate_email

sql_injection = ""

# university email test
assert validate_email("jky10@pitt.edu")[0] == True
assert validate_email("jky10@cs.pitt.edu")[0] == True
assert validate_email("jky10@gmail.com")[0] == False
assert validate_email(sql_injection)[0] == False
assert validate_email("jk\ay10@pitt.edu")[0] == False
assert validate_email("")[0] == False
assert validate_email("@pitt.edu")[0] == False
assert validate_email("thisistoolongthisistoolongthisistoolongthisistoolongthisistoolongthisistoolongthisistoolongthisistoolongthisistoolongthisistoolong@pitt.edu")[0] == False
