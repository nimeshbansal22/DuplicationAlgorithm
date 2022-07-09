import itertools

from CommonConstants import ZERO, ONE
from InsertDataHandler import insert_data_into_profiles


class Profile:

    def __init__(self):
        self.id = None

    def setId(self, id):
        self.id = id

    def setProfile(self):
        self.first_name, self.last_name, self.email, self.date_of_birth, self.class_year \
            = insert_data_into_profiles()

    def getFirstName(self):
        return self.first_name

    def getLastName(self):
        return self.last_name

    def getEmail(self):
        return self.email

    def getDateOfBirth(self):
        return self.date_of_birth

    def getClassYear(self):
        return self.class_year

    def getId(self):
        return self.id
