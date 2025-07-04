"""
Module containing common function used in several tests.
Functions that are not test or feature specific.
"""
import csv
import behave
from behave.userdata import absolute_import


def get_test_data_from_file(context, file_path, file_name, test_id, column_name):

    try:
        # Old
        # reader = csv.DictReader(open("../test_data/" + file_name, "r"))
        reader = csv.DictReader(open(f"{file_path}" + file_name, "r"))
        for raw in reader:
            if raw["test_id"].lower() == test_id.lower():
                return str(raw[column_name])
    except FileNotFoundError:
        print(f"The file '{file_name}' does not exist or '{file_path}' path is incorrect.")
