import os
from behave import given, when, then
from locations_steps import get_origin_location_id_for_trip_test_id
from locations_steps import get_stops_locations_ids_for_trip_test_id
from products_steps import get_product_id_for_trip_test_id
from monitors_steps import get_list_of_monitor_ids_for_trip_test_id
from APICommon.APICommonFuncs import common_funcs
import requests as requests
import csv
import json
import pyodbc
from storage import token
from storage import base_url


@when('I process trip for the test_id "{trip_test_id}" using API call')
@then('I process trip for the test_id "{trip_test_id}" using API call')
def process_trip_using_api_call(context, trip_test_id):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    # Build SerialNumberSubstitutions
    original_monitor_list = [monitor.strip() for monitor in common_funcs.get_test_data_from_file(context,
                  "../test_data/", "trip_details.csv", trip_test_id, "monitors").split(",")]

    serial_number_substitutions_values = ','.join([f'{x}:{y}' for x, y in zip(original_monitor_list, context.modified_monitor_list)])
    """
    # Also 'map' function along with the 'lambda' function can be used to create serial_number_substitutions_values
    # * See below example:
    # serial_number_substitutions_values = ','.join(map(lambda x, y: f'{x}:{y}', original_monitor_list, context.modified_monitor_list))
    """

    device_simulator_file_name = common_funcs.get_test_data_from_file(context, "../test_data/", "trip_details.csv",
                                                                      trip_test_id, "device_simulator_file_name")
    number_of_protobufs_in_file = common_funcs.get_test_data_from_file(context, "../test_data/", "trip_details.csv",
                                                                       trip_test_id, "number_of_protobufs_in_file")

    request_parameters = {
                            "adjustTimestampstoPresent": str(True),
                            "ReplayDelayMilliseconds": str(10),
                            "SpeedupFactor": str(1),
                            "SerialNUmberOverride": None,
                            "HardwareIdOverride": None,
                            "Limit": number_of_protobufs_in_file,
                            "SerialNumberSubstitutions": serial_number_substitutions_values
                         }

    # Define the file that will be attached to the API request
    file_path = f"../test_data/device_simulator_files/{device_simulator_file_name}"
    files = {
        "files": (device_simulator_file_name, open(file_path, "rb"), "text/plain"),
    }

    api_url = base_url + "/api/devicesimulator/DeviceSimulator"

    response = requests.post(api_url, files=files, data=request_parameters, headers=headers)
    response_status_code = response.status_code
    assert response_status_code == 200, (f"Device Simulator API call failed with status code: '{response_status_code}' "
                                         f"and response: {response.text}.")


@when('I process trip for the test_id "{trip_test_id}" using "Command Prompt"')
@then('I process trip for the test_id "{trip_test_id}" using "Command Prompt"')
def process_trip_using_command_prompt(context, trip_test_id):

    csv_file_name = common_funcs.get_test_data_from_file(context, "../test_data/", "trip_details.csv",
                                                                      trip_test_id, "device_simulator_file_name")
    number_of_protobufs_in_file = common_funcs.get_test_data_from_file(context, "../test_data/", "trip_details.csv",
                                                                       trip_test_id, "number_of_protobufs_in_file")

    # Define the .csv file path
    csv_file = os.path.abspath(os.path.join(r"..\test_data\device_simulator_files", csv_file_name))

    # Build SerialNumberSubstitutions
    original_monitor_list = [monitor.strip() for monitor in common_funcs.get_test_data_from_file(context, "../test_data/",
                                                    "trip_details.csv", trip_test_id, "monitors").split(",")]

    serial_number_substitutions_values = '|'.join(
        [f'{x}:{y}' for x, y in zip(original_monitor_list, context.modified_monitor_list)])
    print(f'Seial Number Substitutions is "{serial_number_substitutions_values}"')

    # Save the current working directory
    original_directory = os.getcwd()

    # Change to the directory where the executable is located
    exe_directory = r"..\test_data\device_simulator_exe"
    os.chdir(exe_directory)

    """
    # Also 'map' function along with the 'lambda' function can be used to create serial_number_substitutions_values
    # * See below example:
    # serial_number_substitutions_values = ','.join(map(lambda x, y: f'{x}:{y}', original_monitor_list, context.modified_monitor_list))
    """

    # Construct the command with variables
    command = f"DeviceSimulatorConsoleSingle.exe -i {csv_file} -a -sns \"{serial_number_substitutions_values}\" -d 50 -o {context.output_address} -l {number_of_protobufs_in_file} -checksum"
    print(f'Command to process the trip is: {command}')

    # Run the command
    os.system(command)
    os.chdir(original_directory)