import csv
from werkzeug.security import generate_password_hash

with open('users.csv', 'r') as file:
    a = [{k: (v) for k, v in row.items()}
        for row in csv.DictReader(file, skipinitialspace=True)]

for user in a:
    user['password'] = generate_password_hash(user['password'])
    user['email'] = user['username'] + "@pitt.edu"

print(a)
