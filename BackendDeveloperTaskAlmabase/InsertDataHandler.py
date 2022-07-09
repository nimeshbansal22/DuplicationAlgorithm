from CommonConstants import EMPTY
from Validators.DobValidator import dob_validator
from Validators.EmailValidator import email_validator


def insert_data_into_profiles():
    first_name = input("Enter the first name for profile")
    if first_name is EMPTY:
        first_name = input("Enter the first name for profile, its a required field")
    last_name = input("Enter the last name for profile")
    if last_name is EMPTY:
        print("Last name is required field")
        last_name = input("Enter the Last name for profile, its a required field")
    email = input("Enter the email for profile")
    while email is EMPTY or not email_validator(email):
        email = input("Enter the email for profile, its a Required field")
    dob = input("Enter the DOB for profile in YYYY-MM-DD format (optional)")
    if dob is not EMPTY:
        if not dob_validator(dob):
            dob = input("Enter the DOB for profile in YYYY-MM-DD format (optional)")
    class_year = input("Enter the class year for profile in YYYY format(optional)")
    if class_year is not EMPTY:
        class_year = int(class_year)
    return [first_name, last_name, email, dob, class_year]
