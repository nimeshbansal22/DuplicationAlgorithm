import concurrent.futures

from CommonConstants import FIRST, LAST, EMAIL, CLASS, DOB, ONE, ZERO, TWO
from Helper import create_profiles, get_combined_data, get_combined_data_ratio, \
    get_total_score, get_ignored_parameters, get_duplicates, get_combined_data_score, \
    get_field_score_all
from Validators.ProfileNumberValidator import profile_number_validator


def run():
    total_number_profiles = int(input("Enter the number of profiles you wanna compare (Required atleast 2)"))
    while not profile_number_validator(total_number_profiles):
        total_number_profiles = int(input("Number of profiles are less than two, please Enter the number of profiles "
                                          "you wanna compare (Required atleast 2)"))
    profiles = create_profiles(total_number_profiles)
    field_values = input("Enter the parameters on which you wanna compare the duplicacy")
    field_values = field_values.split(",")
    is_valid = False
    ignore_parameters = [get_ignored_parameters(field_values)]
    non_matching_parameter_temp = {}
    non_matching_parameter = []
    matching_parameter_temp = {}
    matching_parameter = []
    calculate_first_last_email_score = []
    total_score = []
    counter = 0

    if FIRST in field_values or LAST in field_values or EMAIL in field_values:
        is_valid = True
        combined_list = []
        if FIRST in field_values:
            combined_list.append(FIRST)
        if LAST in field_values:
            combined_list.append(LAST)
        if EMAIL in field_values:
            combined_list.append(EMAIL)
        combined_data_list = []
        for i in range(total_number_profiles):
            combined_data_list.append(combined_list)
        combined_data = get_combined_data(profiles, combined_data_list)

    if is_valid:
        get_first_last_email_ratio = []
        get_first_last_email_ratio_with_index = []
        combine_data = []
        for data in combined_data:
            combine_data.append(data)

        for i in range(len(combine_data) - 1):
            for j in range(1, len(combine_data)):
                if i >= j:
                    pass
                else:
                    ratio_data = get_combined_data_ratio(combine_data[i], combine_data[j])
                    get_first_last_email_ratio.append(ratio_data)
                    index_tuple = (i + 1, j + 1, ratio_data)
                    get_first_last_email_ratio_with_index.append(index_tuple)
                    counter += 1

        calculate_first_last_email_score_temp = get_combined_data_score(get_first_last_email_ratio)

        for score in calculate_first_last_email_score_temp:
            calculate_first_last_email_score.append(score)
        for i in range(len(calculate_first_last_email_score)):
            if calculate_first_last_email_score[i] != ONE:
                if FIRST in field_values:
                    if i + 1 not in non_matching_parameter_temp:
                        non_matching_parameter_temp[i + 1] = [FIRST]
                    else:
                        non_matching_parameter_temp[i + 1].append(FIRST)
                if LAST in field_values:
                    if i + 1 not in non_matching_parameter_temp:
                        non_matching_parameter_temp[i + 1] = [LAST]
                    else:
                        non_matching_parameter_temp[i + 1].append(LAST)
                if EMAIL in field_values:
                    if i + 1 not in non_matching_parameter_temp:
                        non_matching_parameter_temp[i + 1] = [EMAIL]
                    else:
                        non_matching_parameter_temp[i + 1].append(EMAIL)
            else:
                if FIRST in field_values:
                    if i + 1 not in matching_parameter_temp:
                        matching_parameter_temp[i + 1] = [FIRST]
                    else:
                        matching_parameter_temp[i + 1].append(FIRST)
                if LAST in field_values:
                    if i + 1 not in matching_parameter_temp:
                        matching_parameter_temp[i + 1] = [LAST]
                    else:
                        matching_parameter_temp[i + 1].append(LAST)
                if EMAIL in field_values:
                    if i + 1 not in matching_parameter_temp:
                        matching_parameter_temp[i + 1] = [EMAIL]
                    else:
                        matching_parameter_temp[i + 1].append(EMAIL)

    get_class_score = []
    if CLASS in field_values:
        get_class_score_temp = get_field_score_all(profiles, CLASS)
        for score in concurrent.futures.as_completed(get_class_score_temp):
            get_class_score.append(score.result())
        for i in range(len(get_class_score)):
            if get_class_score[i] == ONE:
                if i + 1 not in matching_parameter_temp:
                    matching_parameter_temp[i + 1] = [CLASS]
                else:
                    matching_parameter_temp[i + 1].append(CLASS)
            else:
                if i + 1 not in non_matching_parameter_temp:
                    non_matching_parameter_temp[i + 1] = [CLASS]
                else:
                    non_matching_parameter_temp[i + 1].append(CLASS)

    get_DOB_score = []
    if DOB in field_values:
        get_DOB_score_temp = get_field_score_all(profiles, DOB)
        for score in concurrent.futures.as_completed(get_DOB_score_temp):
            get_DOB_score.append(score.result())
        for i in range(len(get_DOB_score)):
            if get_DOB_score[i] == ONE:
                if i + 1 not in matching_parameter_temp:
                    matching_parameter_temp[i + 1] = [DOB]
                else:
                    matching_parameter_temp[i + 1].append(DOB)
            else:
                if i + 1 not in non_matching_parameter_temp:
                    non_matching_parameter_temp[i + 1] = [DOB]
                else:
                    non_matching_parameter_temp[i + 1].append(DOB)

    if len(get_class_score) == 0:
        for _ in range(counter):
            get_class_score.append(0)

    if len(get_DOB_score) == 0:
        for i in range(counter):
            get_DOB_score.append(0)

    if len(calculate_first_last_email_score) == 0:
        for j in range(counter):
            calculate_first_last_email_score.append(0)

    total_score_temp = get_total_score(calculate_first_last_email_score, get_class_score, get_DOB_score)

    for _ in total_score_temp:
        total_score.append(_)

    score_with_index = []
    for i in range(len(total_score)):
        x = get_first_last_email_ratio_with_index.pop()
        y = list(x)
        y[2] = total_score[i]
        x = tuple(y)
        score_with_index.append(x)
    score_with_index.sort()

    counter = 0
    for score in score_with_index:
        counter += 1
        if score[TWO] > ZERO:
            if len(matching_parameter_temp) != ZERO and counter in matching_parameter_temp:
                matching_parameter.append(matching_parameter_temp[counter])
            if len(non_matching_parameter_temp) != ZERO and counter in non_matching_parameter_temp:
                non_matching_parameter.append(non_matching_parameter_temp[counter])
            result = get_duplicates(score[TWO], score[ZERO], score[ONE], matching_parameter,
                                    non_matching_parameter, ignore_parameters)
            if len(matching_parameter) == 1:
                matching_parameter = []
            if len(non_matching_parameter) == 1:
                non_matching_parameter = []
            print(result)


if __name__ == '__main__':
    run()
