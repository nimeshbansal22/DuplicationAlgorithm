import concurrent.futures
from fuzzywuzzy import fuzz

from CommonConstants import FIRST, LAST, EMAIL, EIGHTY, CLASS, DOB, ZERO, FIELD_LIST, ONE
from Profile import Profile


def create_profiles(no_of_profiles):
    profiles = []
    for i in range(no_of_profiles):
        print("Profile " + str(i + 1) + " :")
        profile = Profile()
        profile.setId(i + 1)
        profile.setProfile()
        profiles.append(profile)
    return profiles


def convert_list_2_string(field_list):
    if len(field_list) == 0:
        return "None"
    field_list = field_list[0]
    str1 = ", "
    return str1.join(field_list)


def get_duplicates(total_score, profileone_id, profiletwo_id, matching_parameters, non_matching_parameters,
                   ignored_parameters):
    return "Profile " + str(profileone_id) + " Profile " + str(profiletwo_id) + \
           " total match rate : " + str(total_score) + ", " + "matching_attributes : " + \
           convert_list_2_string(matching_parameters) + ", " + "non_matching_attributes :" + \
           convert_list_2_string(non_matching_parameters) + ", " + "ignored_attributes :" + \
           convert_list_2_string(ignored_parameters)


def check_dupliactes(total_score):
    return total_score > ZERO


# imp
def get_field_score(profileone: Profile, profiletwo: Profile, field):
    if field == CLASS:
        if profileone.getId() != profiletwo.getId():
            if profileone.getClassYear() is not None and profiletwo.getClassYear() is not None:
                if profileone.getClassYear() == profiletwo.getClassYear():
                    return 1
                else:
                    return -1
            return 0
        return 0

    if field == DOB:
        if profileone.getId() != profiletwo.getId():
            if profileone.getDateOfBirth() is not None and profiletwo.getDateOfBirth() is not None:
                if profileone.getDateOfBirth() == profiletwo.getDateOfBirth():
                    return 1
                else:
                    return -1
            return 0
        return 0
    return None


def get_field_score_all(profile: Profile, field):
    with concurrent.futures.ThreadPoolExecutor() as executors:
        for profileone in profile:
            field_scores = [executors.submit(get_field_score, profileone, profiletwo, field) for profiletwo in
                            profile]
    return field_scores


def get_single_profile_combined_data(profile: Profile, field_parameters):
    first_last_email_profile = ''
    for field in field_parameters:
        if field == FIRST:
            first_last_email_profile += profile.getFirstName()
        if field == LAST:
            first_last_email_profile += profile.getLastName()
        if field == EMAIL:
            first_last_email_profile += profile.getEmail()
    return first_last_email_profile


# imp
def get_combined_data(profile: Profile, field_parameters):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        datas = executor.map(get_single_profile_combined_data, profile, field_parameters)
    return datas


# imp
def get_combined_data_ratio(first_last_email_profileone, first_last_email_profiletwo):
    return fuzz.token_sort_ratio(first_last_email_profileone, first_last_email_profiletwo)


def get_final_score(get_first_last_email_score, get_class_score, get_DOB_score):
    return get_DOB_score + get_class_score + get_first_last_email_score


# imp
def get_total_score(get_first_last_email_score, get_class_score, get_DOB_score):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        total_score = executor.map(get_final_score, get_first_last_email_score, get_class_score, get_DOB_score)
    return total_score


def get_single_data_score(get_first_last_email_ratio):
    if get_first_last_email_ratio > EIGHTY:
        return ONE
    return ZERO


def get_combined_data_score(get_first_last_email_ratio):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        score = executor.map(get_single_data_score, get_first_last_email_ratio)
    return score


# imp
def get_ignored_parameters(field_parameters):
    ignore = []
    for field in FIELD_LIST:
        if field not in field_parameters:
            ignore.append(field)
    return ignore
