import time

from behave import given, when, then
from locations_steps import get_origin_location_id_for_trip_test_id
from locations_steps import get_stops_locations_ids_for_trip_test_id
from products_steps import get_product_id_for_trip_test_id
from monitors_steps import get_list_of_monitor_ids_for_trip_test_id, create_monitor_s_for_trip_test_id
from containers_steps import create_container_for_trip_id, get_container_and_its_attached_monitors_details
from APICommon.APICommonFuncs import common_funcs
import json
import requests as requests
import pyodbc
from storage import token
from storage import base_url


@when('I create a new Trip with Monitors for the test_id "{trip_test_id}"')
@then('I create a new Trip with Monitors for the test_id "{trip_test_id}"')
def create_new_trip_with_monitors(context, trip_test_id):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    # Read the payload file for trip creation
    with open("../test_data/payloads/create_trips/create_trip_with_monitors.json", "r") as file:
        payload = json.load(file)

    # Update the Program ID for the payload
    payload["programId"] = context.program_id

    # Get origin locationID and locationName
    origin_location_name = common_funcs.get_test_data_from_file(context, "../test_data/", "trip_details.csv",
                                                                trip_test_id, "origin_location_name")
    origin_location_id = get_origin_location_id_for_trip_test_id(context, trip_test_id)

    # Update Origin locationID and locationName for the payload
    payload["tripOrigin"]["locations"][0]["locationID"] = origin_location_id
    payload["tripOrigin"]["locations"][0]["locationName"] = origin_location_name

    # Get stops Names and IDs
    stops_locations_names_list = [location_name.strip() for location_name in common_funcs.get_test_data_from_file(context,
        "../test_data/", "trip_details.csv", trip_test_id, "stops_locations_names").split(",")]
    stops_ids_list = get_stops_locations_ids_for_trip_test_id(context, trip_test_id)

    # Get Product Name and ID
    product_name = common_funcs.get_test_data_from_file(context, "../test_data/", "trip_details.csv",
                                                        trip_test_id, "product_name")
    product_id = get_product_id_for_trip_test_id(context, trip_test_id)

    # Create a single destination JSON
    destination_json = {
                          "destinationType": "aa7dd78f-33b9-4937-9da8-d05cb1133b94",
                          "locationID": 0,
                          "locationAddress": "",
                          "locationName": "Update The Name",
                          "products": [
                            {
                              "productID": 0,
                              "productName": "Update The Name"
                            }
                          ],
                          "modeOfTransportation": "",
                          "locationOrder": 1,
                          "vesselOrFlightOperator": None,
                          "vesselNameOrTailNumber": None,
                          "containerNumber": None,
                          "routeOrFlightNumber": None,
                          "masterBillOfLading": None
                       }

    # Create empty list of destinations
    destination_list = []

    # Update the list of destinations
    for i in range(len(stops_ids_list)):
        # Create a copy of the original JSON structure
        temp_destination_json = destination_json.copy()

        # Update values for "locationID" and "locationName"
        temp_destination_json["locationName"] = stops_locations_names_list[i]
        temp_destination_json["locationID"] = stops_ids_list[i]

        # Update Product Name and Product ID
        temp_destination_json["products"][0]["productName"] = product_name
        temp_destination_json["products"][0]["productID"] = product_id

        # Update Location Orders for Stops. Note: "i + 1" is used to start the order from number "1".
        temp_destination_json["locationOrder"] = i + 1

        # Update "Type of Stop" for last stop to be "Final Destination"
        if (i + 1) == len(stops_ids_list):
            temp_destination_json["destinationType"] = "0b8d0f52-be83-4047-8d10-eaf626251ae7"

        # Append the updated item to the list
        destination_list.append(temp_destination_json)

    # Update destinations list for the payload
    payload["destinations"] = destination_list

    # Create monitors for the trip
    create_monitor_s_for_trip_test_id(context, trip_test_id)

    # Get list of Serial Numbers and IDs for monitors
    monitors_serial_number_list = context.modified_monitor_list
    monitors_ids_list = get_list_of_monitor_ids_for_trip_test_id(context, trip_test_id)

    # Create a monitor JSON
    monitor_json = {
                      "monitorID": 0,
                      "serialNumber": "Update The Name"
                   }

    # Create empty list of monitors
    monitors_list = []

    # Update the list of monitors
    for i in range(len(monitors_ids_list)):
        # Create a copy of the original JSON structure
        temp_monitor_json = monitor_json.copy()

        # Update values for "locationID" and "locationName"
        temp_monitor_json["monitorID"] = monitors_ids_list[i]
        temp_monitor_json["serialNumber"] = monitors_serial_number_list[i]

        # Append the updated item to the list
        monitors_list.append(temp_monitor_json)

    # Update monitors list for the payload
    payload["containers"][0]["zones"][0]["monitors"] = monitors_list

    # Update Product ID for "zoneProducts" component of payload.
    payload["containers"][0]["zones"][0]["zoneProducts"][0]["productId"] = product_id
    print(payload)

    create_trip_api_url = base_url + f"/api/trip/trip/programId/{context.program_id}"

    response = requests.post(create_trip_api_url, json=payload, headers=headers)
    response_status_code = response.status_code

    assert response_status_code == 200, f"Failed to create a new Trip: \nStatus Code: {response_status_code} \nReason: {response.reason} \nJSON Response: {response}"
    print(f"A new Trip has been created with the 'Supplier to DC' template and the test_id '{trip_test_id}'. "
          f"\n* Trip Number: '{response.json().get('id')}'\n* Trip GUID: '{response.json().get('shipmentID')}'")

    """
    Using the setattr() function to store the Trip Number and Trip GUID
    in the context object to use in other step definitions.

    You can access the Trip Number and the Trip GUID in other step definitions
    using getattr() function using following format:
        trip_number = getattr(context, trip_number_attr_name)
        trip_guid = getattr(context, trip_guid_attr_name)
    """
    trip_number_attr_name = f"{trip_test_id} + _trip_number"
    trip_guid_attr_name = f"{trip_test_id} + _trip_guid"
    setattr(context, trip_number_attr_name, response.json().get("id"))
    setattr(context, trip_guid_attr_name, response.json().get("shipmentID"))


@when('I create a new Trip with Container for the test_id "{trip_test_id}"')
@then('I create a new Trip with Container for the test_id "{trip_test_id}"')
def create_new_trip_with_container(context, trip_test_id):
    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    # Read the payload file for trip creation
    with open("../test_data/payloads/create_trips/create_trip_with_container.json", "r") as file:
        payload = json.load(file)

    # Update the Program ID for the payload
    payload["programId"] = context.program_id

    # Get origin locationID and locationName
    origin_location_name = common_funcs.get_test_data_from_file(context, "../test_data/", "trip_details.csv",
                                                                trip_test_id, "origin_location_name")
    origin_location_id = get_origin_location_id_for_trip_test_id(context, trip_test_id)

    # Update Origin locationID and locationName for the payload
    payload["tripOrigin"]["locations"][0]["locationID"] = origin_location_id
    payload["tripOrigin"]["locations"][0]["locationName"] = origin_location_name

    # Get stops Names and IDs
    stops_locations_names_list = [location_name.strip() for location_name in common_funcs.get_test_data_from_file(context,
                                                                       "../test_data/", "trip_details.csv",
                                                                       trip_test_id, "stops_locations_names").split(",")]
    stops_ids_list = get_stops_locations_ids_for_trip_test_id(context, trip_test_id)

    # Get Product Name and ID
    product_name = common_funcs.get_test_data_from_file(context, "../test_data/", "trip_details.csv",
                                                        trip_test_id, "product_name")
    product_id = get_product_id_for_trip_test_id(context, trip_test_id)

    # Create a single destination JSON
    destination_json = {
        "destinationType": "aa7dd78f-33b9-4937-9da8-d05cb1133b94",
        "locationID": 0,
        "locationAddress": "",
        "locationName": "Update The Name",
        "products": [
            {
                "productID": 0,
                "productName": "Update The Name"
            }
        ],
        "modeOfTransportation": "",
        "locationOrder": 1,
        "vesselOrFlightOperator": None,
        "vesselNameOrTailNumber": None,
        "containerNumber": None,
        "routeOrFlightNumber": None,
        "masterBillOfLading": None
    }

    # Create empty list of destinations
    destination_list = []

    # Update the list of destinations
    for i in range(len(stops_ids_list)):
        # Create a copy of the original JSON structure
        temp_destination_json = destination_json.copy()

        # Update values for "locationID" and "locationName"
        temp_destination_json["locationName"] = stops_locations_names_list[i]
        temp_destination_json["locationID"] = stops_ids_list[i]

        # Update Product Name and Product ID
        temp_destination_json["products"][0]["productName"] = product_name
        temp_destination_json["products"][0]["productID"] = product_id

        # Update Location Orders for Stops. Note: "i + 1" is used to start the order from number "1".
        temp_destination_json["locationOrder"] = i + 1

        # Update "Type of Stop" for last stop to be "Final Destination"
        if (i + 1) == len(stops_ids_list):
            temp_destination_json["destinationType"] = "0b8d0f52-be83-4047-8d10-eaf626251ae7"

        # Append the updated item to the list
        destination_list.append(temp_destination_json)

    # Update destinations list for the payload
    payload["destinations"] = destination_list

    # Create Container for the trip
    create_container_for_trip_id(context, trip_test_id)

    # Update Container name and ID in payload
    payload["containers"][0]["containerID"] = context.container_id
    payload["containers"][0]["containerName"] = context.container_name

    # get container and its attached monitors details
    container_and_its_attached_monitors_details = get_container_and_its_attached_monitors_details(context, context.container_id)

    # Create container zone list with details
    container_zone_list = []
    for zone_name, zone_id, monitor_serial_number, monitor_id in zip(*container_and_its_attached_monitors_details):
        # Read single_container_zone_to_update_container.json file
        with open("../test_data/payloads/single_container_zone_to_create_trip.json", "r") as file:
            single_container_zone = json.load(file)
        single_container_zone["zoneID"] = zone_id
        single_container_zone["zoneName"] = zone_name
        single_container_zone["monitors"][0]["serialNumber"] = monitor_serial_number
        single_container_zone["monitors"][0]["monitorID"] = monitor_id
        # append single_container_zone to container_zone_list
        container_zone_list.append(single_container_zone)
    # Update container zones in payload
    payload["containers"][0]["zones"] = container_zone_list
    print(payload)

    create_trip_api_url = base_url + f"/api/trip/trip/programId/{context.program_id}"

    response = requests.post(create_trip_api_url, json=payload, headers=headers)
    response_status_code = response.status_code

    assert response_status_code == 200, f"Failed to create a new Trip: \nStatus Code: {response_status_code} \nReason: {response.reason} \nJSON Response: {response}"
    # time.sleep(int(10))
    print(f"A new Trip has been created with the 'Supplier to DC' template and the test_id '{trip_test_id}'. "
          f"\n* Trip Number: '{response.json().get('id')}'\n* Trip GUID: '{response.json().get('shipmentID')}'")

    """
    Using the setattr() function to store the Trip Number and Trip GUID
    in the context object to use in other step definitions.

    You can access the Trip Number and the Trip GUID in other step definitions
    using getattr() function using following format:
        trip_number = getattr(context, trip_number_attr_name)
        trip_guid = getattr(context, trip_guid_attr_name)
    """
    trip_number_attr_name = f"{trip_test_id} + _trip_number"
    trip_guid_attr_name = f"{trip_test_id} + _trip_guid"
    setattr(context, trip_number_attr_name, response.json().get("id"))
    setattr(context, trip_guid_attr_name, response.json().get("shipmentID"))