import re


def email_validator(email):
    email_regex = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(email_regex, email):
        return True
    print("Email not in correct format try again")
    return False
