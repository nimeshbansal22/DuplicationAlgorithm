import datetime


def dob_validator(dob):
    try:
        datetime.datetime.strptime(dob, '%Y-%m-%d')
        return True
    except:
        print("Date of Birth is not in correct format, try again")
        return False