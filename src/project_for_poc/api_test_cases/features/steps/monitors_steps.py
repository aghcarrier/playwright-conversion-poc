from behave import given, when, then
from APICommon.APICommonFuncs import common_funcs
import requests as requests
import random
import json
import pyodbc
from storage import token
from storage import base_url


@when('I add monitor/s for the trip with test_id "{trip_test_id}"')
@then('I add monitor/s for the trip with test_id "{trip_test_id}"')
def create_monitor_s_for_trip_test_id(context, trip_test_id):
    # =====================================================================
    # This step will fail if monitor(s) already added.
    # =====================================================================
    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + "/api/admin/monitors"

    payload = {
                 "serialNumber": "Update Serial Number",
                 "enabled": True
              }

    # Get monitor list from trip_details.csv file based in "{trip_test_id}"
    original_monitor_list = [monitor.strip() for monitor in common_funcs.get_test_data_from_file(context, "../test_data/",
                                                     "trip_details.csv", trip_test_id,"monitors").split(",")]

    random_int = str(random.randint(1, 9999)).zfill(4)

    context.modified_monitor_list = [monitor + f"_{random_int}" for monitor in original_monitor_list]

    for monitor in context.modified_monitor_list:

        payload["serialNumber"] = monitor

        response = requests.post(api_url, json=payload, headers=headers)
        response_status_code = response.status_code

        if response_status_code == 201:
            print(f"A new Monitor with '{monitor}' Serial Number added.")
        elif response_status_code == 400 and response.json().get("message") == "Serial Number Exists in Program None":
            raise ValueError(f"Monitor with '{monitor}' Serial Number exists and Can Not be added second time.")
        else:
            raise AssertionError(f"Failed to add Monitor with '{monitor}' Serial Number: \nStatus Code: {response_status_code} \nReason: {response.reason}")


@when('I update monitor usage to be "{usage_name}" and type to be "{monitor_type_name}" for ID: "{monitor_id}" and Serial Number: "{monitor_serial_number}"')
@then('I update monitor usage to be "{usage_name}" and type to be "{monitor_type_name}" for ID: "{monitor_id}" and Serial Number: "{monitor_serial_number}"')
def update_monitor_usage_and_type_for_monitor_id_and_serial_number(context, usage_name, monitor_type_name, monitor_id, monitor_serial_number):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + "/api/admin/monitor"

    # "monitor_type_and_type_id" is dictionary(map) for Monitor Type and Monitor Type IDs
    monitor_type_and_type_id = {
        "SensiWatch Gateway": 5,
        "SensiWatch Sensor": 6,
        "Sentry 500": 23,
        "TempTale Eagle w/ Beeper": 7,
        "TempTale GEO": 4,
        "TempTale GEO 7": 26,
        "TempTale GEO 7 Extended": 27,
        "TempTale GEO Eagle": 0,
        "TempTale GEO Eagle 2G Extended": 1,
        "TempTale GEO Eagle 3G": 2,
        "TempTale GEO Eagle CO2": 3,
        "TempTale GEO Hawk": 22,
        "TempTale GEO LTE": 8,
        "TempTale GEO LTE + Probe": 24,
        "TempTale GEO LTE + Steel Probe": 34,
        "TempTale GEO LTE Extended": 18,
        "TempTale GEO LTE Extended + Probe": 25,
        "TempTale GEO LTE Extended + Steel Probe": 35,
        "TempTale GEO Ultra": 16,
        "TempTale GEO Ultra Dry Ice": 17,
        "TempTale GEO Ultra Dry Ice Extended": 20,
        "TempTale GEO Ultra Extended": 19,
        "TempTale GEO X": 36,
        "TempTale GEO X Blue Alkaline": 40,
        "TempTale GEO X Blue Lithium": 41,
        "TempTale GEO XE": 38,
        "TempTale GEO XEP": 39,
        "TempTale GEO XP": 37,
        "VizComm Geo Tracker": 14,
        "VizComm Prime": 9,
        "VizComm Prime 7": 32,
        "VizComm Prime 7 Extended": 33,
        "VizComm Prime Extended": 10,
        "VizComm View": 11,
        "VizComm View 3G": 13,
        "VizComm View 7": 28,
        "VizComm View 7 Extended": 29,
        "VizComm View Extended": 12,
        "VizComm View LTE": 15,
        "VizComm View LTE Extended": 21,
        "VizComm View Ultra": 30,
        "VizComm View Ultra Extended": 31,
        "Unknown": -1
    }
    # Get monitor_type_id from monitor_type_and_type_id on monitor_type_name
    if monitor_type_name in monitor_type_and_type_id:
        monitor_type_id = monitor_type_and_type_id.get(monitor_type_name)
    else:
        raise ValueError(
            f"'{monitor_type_name}' is not in the list of Monitor Type. Please provide right Monitor Type name")

    payload = {
                 "id": monitor_id,
                 "serialNumber": f"{monitor_serial_number}",
                 "usage": f"{usage_name}",
                 "monitorTypeId": monitor_type_id,
                 "hasTemperature": True,
                 "hasTemperatureProbe": True,
                 "hasLight": True,
                 "hasHumidity": True,
                 "hasCO2": True,
                 "partNumber": "Unknown"
              }

    response = requests.put(api_url, json=payload, headers=headers)
    response_status_code = response.status_code

    if response_status_code == 200:
        print(f"A new Monitor with '{monitor_serial_number}' Serial Number is updated to be '{usage_name}'.")
    else:
        raise AssertionError(f"Failed to update the Monitor with '{monitor_serial_number}' Serial Number: \nStatus "
                             f"Code: {response_status_code} \nReason: {response.reason}")


@when('I get list of monitor IDs for the trip with test_id "{trip_test_id}"')
@then('I get list of monitor IDs for the trip with test_id "{trip_test_id}"')
def get_list_of_monitor_ids_for_trip_test_id(context, trip_test_id):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    context.monitors_ids = []

    for monitor in context.modified_monitor_list:
        api_url = base_url + (f"/api/admin/monitors/programId/{context.program_id}?id=null&skip=0&take=1000&sort=name"
                              f"&filter=/{monitor}&showDisabled=false&showLocked=false&showProgramUnassigned=false")

        get_monitors_response = requests.get(api_url, headers=headers)
        get_monitors_response_json = get_monitors_response.json()
        # Assuming there is at least one item in the response
        monitor_id = get_monitors_response_json["items"][0]["id"]
        context.monitors_ids.append(monitor_id)

    return context.monitors_ids