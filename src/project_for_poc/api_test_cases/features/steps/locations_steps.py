import requests as requests
from behave import given, when, then
import json
from APICommon.APICommonFuncs import common_funcs
from helpers.payload_builder import build_location_payload
import pyodbc
from storage import token
from storage import base_url


@when('I create a new "{location_group_type}" type Location Group with name the "{location_group_name}"')
@then('I create a new "{location_group_type}" type Location Group with name the "{location_group_name}"')
def create_new_location_group_if_does_not_exist(context, location_group_type, location_group_name):
    # =====================================================================
    # A new location group will not be created
    # If location group with "{location_group_name}" already exist
    # =====================================================================
    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey
    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + "/api/admin/locationgroups"

    if location_group_type == "Origin":
        type_id = 1
    elif location_group_type == "Stop":
        type_id = 2
    elif location_group_type == "Site":
        type_id = 3
    else:
        raise ValueError(f"'{location_group_type}' is not acceptable location group type. The location group type should be 'Origin', 'Stop' or 'Site'")

    payload={
               "programId": f"{context.program_id}",
               "name": f"{location_group_name}",
               "description": "Created by API Automation",
               "typeId": f"{type_id}",
               "locationIds": [],
               "enabled": "true"
            }

    response = requests.post(api_url, json=payload, headers=headers)
    response_status_code = response.status_code

    if response_status_code == 201:
        print(f"A new Location Group has been created with the name '{location_group_name}'.")
    elif response_status_code == 400:
        try:
            assert response.json().get("message") == "DUPLICATED_NAME_LOCATIONGROUP"
            print(f"A Location Group with the name '{location_group_name}' already exist.")
        except:
            raise AssertionError(f"Add Location Group API call failed. \nStatus Code: {response_status_code} \nReason: {response.reason} \nJSON Response: {response.json()}")
    else:
        raise AssertionError(f"Failed to create new Location Group: \nStatus Code: {response_status_code} \nReason: {response.reason}")


@when('I get location group IDs if name contains "{part_of_loc_group_name}"')
@then('I get location group IDs if name contains "{part_of_loc_group_name}"')
def get_location_group_ids_by_provided_partial_name(context, part_of_loc_group_name):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey
    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + (f"/api/admin/locationgroups/programId/{context.program_id}?id=null&skip=0&take=99999&sort"
                          f"=name&filter=&showDisabled=false&showLocked=false&showProgramUnassigned=false")

    response = requests.get(api_url, headers=headers)
    response_status_code = response.status_code

    assert response_status_code == 200, f"Get location group API call failed with '{response_status_code}' status code."
    json_data = response.json()

    context.location_group_ids_for_partial_name = [item["id"] for item in json_data["items"] if f"{part_of_loc_group_name}".lower() in item["name"].lower()]
    return context.location_group_ids_for_partial_name


@when('I get location groups IDs')
@then('I get location groups IDs')
def get_location_groups_ids(context):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey
    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + (f"/api/admin/locationgroups/programId/{context.program_id}?id=null&skip=0&take=99999&sort"
                          f"=name&filter=&showDisabled=false&showLocked=false&showProgramUnassigned=false")

    response = requests.get(api_url, headers=headers)
    response_status_code = response.status_code

    assert response_status_code == 200, f"Get location group API call failed with '{response_status_code}' status code."
    json_data = response.json()

    context.location_group_ids = [item["id"] for item in json_data["items"]]
    return context.location_group_ids


@when('I create origin location for the trip with test_id "{trip_test_id}"')
@then('I create origin location for the trip with test_id "{trip_test_id}"')
def create_origin_location_for_test_id(context, trip_test_id):
    # =====================================================================
    # Created location will be added to location groups, that contain the word "Origin" in their names
    # =====================================================================
    # A new location will not be created
    # If location name already exist
    # =====================================================================
    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + "/api/admin/locations"

    origin_location_name = common_funcs.get_test_data_from_file(context, "../test_data/", "trip_details.csv",
                                                                trip_test_id,"origin_location_name")
    file_name_for_json_payload = origin_location_name + ".json"

    try:
        with open(f"../test_data/payloads/locations/{file_name_for_json_payload}", "r") as file:
            payload = json.load(file)
            # print(payload)
    except json.JSONDecodeError as e:
        print(f"JSON decoding failed: {e}")

    # Update name, programId and locationGroupIds in payload
    payload["name"] = origin_location_name
    payload["programId"] = context.program_id

    # get Stops Locations Names List
    stops_locations_names_list = [location_name.strip() for location_name in common_funcs.get_test_data_from_file(context,
       "../test_data/", "trip_details.csv", trip_test_id, "stops_locations_names").split(",")]
    # Retrieve Location Group IDs for groups that contain the word "Origin" in their names.
    origin_locations_id_list = get_location_group_ids_by_provided_partial_name(context, "Origin")
    # Check if origin location also exist in stops location list as well, then add it to Stops or Final group as well
    if origin_location_name not in stops_locations_names_list:
        # Retrieve Location Group IDs for groups that contain the word "Origin" in their names.
        payload["locationGroupIds"] = get_location_group_ids_by_provided_partial_name(context, "Origin")
    else:
        # Check if the origin location, which exists in the stops location list, is the last element,
        # then add it to Final groups + Origin groups
        if origin_location_name == stops_locations_names_list[-1] and stops_locations_names_list.count(origin_location_name) == 1:
            # Retrieve Location Group IDs for groups that contain the word "Stops" in their names.
            final_locations_id_list = get_location_group_ids_by_provided_partial_name(context, "Final")

            # Combine "Origin" and "Final" Location Group IDs then update the payload
            payload["locationGroupIds"] = origin_locations_id_list + final_locations_id_list

        # else if the origin location, which exists in the stops location list, exist twice or more times,
        # and also it is the last element as well, then add it to Stops groups + Final groups + Origin groups
        elif origin_location_name == stops_locations_names_list[-1] and stops_locations_names_list.count(origin_location_name) >= 2:
            # Retrieve Location Group IDs for groups that contain the word "Stops" in their names.
            stops_locations_id_list = get_location_group_ids_by_provided_partial_name(context, "Stops")
            # Retrieve Location Group IDs for groups that contain the word "Final" in their names.
            final_locations_id_list = get_location_group_ids_by_provided_partial_name(context, "Final")

            # Combine "Origin", "Stops" and "Final" Location Group IDs then update the payload
            payload["locationGroupIds"] = origin_locations_id_list + stops_locations_id_list + final_locations_id_list

        # else if the origin location, which exists in the stops location list, is NOT the last element,
        # then add it to Stops groups + Origin groups
        else:
            # Retrieve Location Group IDs for groups that contain the word "Stops" in their names.
            stops_locations_id_list = get_location_group_ids_by_provided_partial_name(context, "Stops")

            # Combine "Origin" and "Stops" Location Group IDs then update the payload
            payload["locationGroupIds"] = origin_locations_id_list + stops_locations_id_list

    response = requests.post(api_url, json=payload, headers=headers)
    response_status_code = response.status_code

    if response_status_code == 201:
        print(f"A new Origin Location has been created with the name '{origin_location_name}'.")
    elif response_status_code == 400:
        try:
            assert response.json().get("message") == "DUPLICATED_NAME_LOCATION"
            print(f"A Location with the name '{origin_location_name}' already exist.")
        except:
            raise AssertionError(
                f"Add Location API call failed. \nStatus Code: {response_status_code} \nReason: {response.reason} \nJSON Response: {response.json()}")
    else:
        raise AssertionError(
            f"Failed to create new Location: \nStatus Code: {response_status_code} \nReason: {response.reason}")


@when('I create origin location for the trip with test_id "{trip_test_id}" from csv')
@then('I create origin location for the trip with test_id "{trip_test_id}" from csv')
def create_origin_location_for_test_id_from_csv(context, trip_test_id):
    # =====================================================================
    # Created location will be added to location groups, that contain the word "Origin" in their names
    # =====================================================================
    # A new location will not be created
    # If location name already exist
    # =====================================================================
    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + "/api/admin/locations"

    origin_location_name = common_funcs.get_test_data_from_file(context, "../test_data/", "trip_details.csv",
                                                                trip_test_id,"origin_location_name")

    payload = build_location_payload(
        program_id = context.program_id,
        name = origin_location_name,
        company = common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                origin_location_name,"company"),
        shipping_reference = common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                origin_location_name,"shipping_reference"),
        geofence_radius_departure = common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                origin_location_name,"geofence_radius_departure"),
        geofence_radius_arrival = common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                origin_location_name,"geofence_radius_arrival"),
        required_data_points_departure = common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                origin_location_name,"required_data_points_departure"),
        required_data_points_arrival = common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                origin_location_name,"required_data_points_arrival"),
        type_id = common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                origin_location_name,"type_id"),
        data_point_sequence_departure_id = common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                origin_location_name,"data_point_sequence_departure_id"),
        data_point_sequence_arrival_id = common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                origin_location_name,"data_point_sequence_arrival_id"),
        time_zone = common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                origin_location_name,"time_zone"),
        address1 = common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                origin_location_name,"address1"),
        address2 = common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                origin_location_name,"address2"),
        city = common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                origin_location_name,"city"),
        state = common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                origin_location_name,"state"),
        zip_code = common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                origin_location_name,"zip_code"),
        country = common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                origin_location_name,"country"),
        latitude = common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                origin_location_name,"latitude"),
        longitude = common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                origin_location_name,"longitude"),
        location_group_ids = common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                origin_location_name,"location_group_ids"),
        product_ids = common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                origin_location_name,"product_ids"),
        location_segment_name = common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                origin_location_name,"location_segment_name"),
    )

    # get Stops Locations Names List
    stops_locations_names_list = [location_name.strip() for location_name in common_funcs.get_test_data_from_file(context,
       "../test_data/", "trip_details.csv", trip_test_id, "stops_locations_names").split(",")]
    # Retrieve Location Group IDs for groups that contain the word "Origin" in their names.
    origin_locations_id_list = get_location_group_ids_by_provided_partial_name(context, "Origin")
    # Check if origin location also exist in stops location list as well, then add it to Stops or Final group as well
    if origin_location_name not in stops_locations_names_list:
        # Retrieve Location Group IDs for groups that contain the word "Origin" in their names.
        payload["locationGroupIds"] = get_location_group_ids_by_provided_partial_name(context, "Origin")
    else:
        # Check if the origin location, which exists in the stops location list, is the last element,
        # then add it to Final groups + Origin groups
        if origin_location_name == stops_locations_names_list[-1] and stops_locations_names_list.count(origin_location_name) == 1:
            # Retrieve Location Group IDs for groups that contain the word "Stops" in their names.
            final_locations_id_list = get_location_group_ids_by_provided_partial_name(context, "Final")

            # Combine "Origin" and "Final" Location Group IDs then update the payload
            payload["locationGroupIds"] = origin_locations_id_list + final_locations_id_list

        # else if the origin location, which exists in the stops location list, exist twice or more times,
        # and also it is the last element as well, then add it to Stops groups + Final groups + Origin groups
        elif origin_location_name == stops_locations_names_list[-1] and stops_locations_names_list.count(origin_location_name) >= 2:
            # Retrieve Location Group IDs for groups that contain the word "Stops" in their names.
            stops_locations_id_list = get_location_group_ids_by_provided_partial_name(context, "Stops")
            # Retrieve Location Group IDs for groups that contain the word "Final" in their names.
            final_locations_id_list = get_location_group_ids_by_provided_partial_name(context, "Final")

            # Combine "Origin", "Stops" and "Final" Location Group IDs then update the payload
            payload["locationGroupIds"] = origin_locations_id_list + stops_locations_id_list + final_locations_id_list

        # else if the origin location, which exists in the stops location list, is NOT the last element,
        # then add it to Stops groups + Origin groups
        else:
            # Retrieve Location Group IDs for groups that contain the word "Stops" in their names.
            stops_locations_id_list = get_location_group_ids_by_provided_partial_name(context, "Stops")

            # Combine "Origin" and "Stops" Location Group IDs then update the payload
            payload["locationGroupIds"] = origin_locations_id_list + stops_locations_id_list

    response = requests.post(api_url, json=payload, headers=headers)
    response_status_code = response.status_code

    if response_status_code == 201:
        print(f"A new Origin Location has been created with the name '{origin_location_name}'.")
    elif response_status_code == 400:
        try:
            assert response.json().get("message") == "DUPLICATED_NAME_LOCATION"
            print(f"A Location with the name '{origin_location_name}' already exist.")
        except:
            raise AssertionError(
                f"Add Location API call failed. \nStatus Code: {response_status_code} \nReason: {response.reason} \nJSON Response: {response.json()}")
    else:
        raise AssertionError(
            f"Failed to create new Location: \nStatus Code: {response_status_code} \nReason: {response.reason}")


@when('I get origin location id for the trip with test_id "{trip_test_id}"')
@then('I get origin location id for the trip with test_id "{trip_test_id}"')
def get_origin_location_id_for_trip_test_id(context, trip_test_id):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    origin_location_name = common_funcs.get_test_data_from_file(context, "../test_data/", "trip_details.csv",
                                                                trip_test_id, "origin_location_name")
    api_url = base_url + (f"/api/admin/locations/programId/{context.program_id}?id=null&skip=0&take=50"
                          f"&sort=name&filter={origin_location_name}&showDisabled=false&showLocked=false"
                          f"&showProgramUnassigned=false")

    response = requests.get(api_url, headers=headers)
    response_json = response.json()
    origin_location_id = response_json["items"][0]["id"]
    return origin_location_id


@when('I get location id for the name "{location_name}"')
@then('I get location id for the name "{location_name}"')
def get_location_id_for_the_name(context, location_name):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + (f"/api/admin/locations/programId/{context.program_id}?id=null&skip=0&take=50"
                          f"&sort=name&filter={location_name}&showDisabled=false&showLocked=false"
                          f"&showProgramUnassigned=false")

    response = requests.get(api_url, headers=headers)
    response_json = response.json()
    origin_location_id = response_json["items"][0]["id"]
    return origin_location_id


@when('I create stops locations for the trip with test_id "{trip_test_id}"')
@then('I create stops locations for the trip with test_id "{trip_test_id}"')
def create_stops_locations_for_test_id(context, trip_test_id):
    # =====================================================================
    # Created location will be added to location groups, that contain the word "Stops" in their names.
    # And the last location will be added to location groups, that contain the word "Final" in their names.
    # =====================================================================
    # A new location(s) will not be created
    # If location(s) name already exist
    # =====================================================================
    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + "/api/admin/locations"

    stops_locations_names_list = [location_name.strip() for location_name in common_funcs.get_test_data_from_file(context,
        "../test_data/", "trip_details.csv", trip_test_id,"stops_locations_names").split(",")]

    for index, stop_location_name in enumerate(stops_locations_names_list):
        file_name_for_json_payload = stop_location_name + ".json"

        with open(f"../test_data/payloads/locations/{file_name_for_json_payload}", "r") as file:
            payload = json.load(file)

        # Update name, programId and locationGroupIds in payload
        payload["name"] = stop_location_name
        payload["programId"] = context.program_id

        def perform_api_call(api_url, payload, headers):
            response = requests.post(api_url, json=payload, headers=headers)
            response_status_code = response.status_code

            if response_status_code == 201:
                print(f"A new Stop Location has been created with the name '{stop_location_name}'.")
            elif response_status_code == 400:
                try:
                    assert response.json().get("message") == "DUPLICATED_NAME_LOCATION"
                    print(f"A Location with the name '{stop_location_name}' already exist.")
                except:
                    raise AssertionError(
                        f"Add Location API call failed. \nStatus Code: {response_status_code} \nReason: {response.reason} \nJSON Response: {response.json()}")
            else:
                raise AssertionError(
                    f"Failed to create new Location: \nStatus Code: {response_status_code} \nReason: {response.reason}")

        # Add all locations to Stops groups and the last location to Final groups.
        if (index + 1) < len(stops_locations_names_list):
            # Retrieve Location Group IDs for groups that contain the word "Stops" in their names.
            payload["locationGroupIds"] = get_location_group_ids_by_provided_partial_name(context, "Stops")
            perform_api_call(api_url, payload, headers)
        else:
            # Retrieve Location Group IDs for groups that contain the word "Final" in their names.
            payload["locationGroupIds"] = get_location_group_ids_by_provided_partial_name(context, "Final")
            perform_api_call(api_url, payload, headers)


@when('I create stops locations for the trip with test_id "{trip_test_id}" from csv')
@then('I create stops locations for the trip with test_id "{trip_test_id}" from csv')
def create_stops_locations_for_test_id_from_csv(context, trip_test_id):
    # =====================================================================
    # Created location will be added to location groups, that contain the word "Stops" in their names.
    # And the last location will be added to location groups, that contain the word "Final" in their names.
    # =====================================================================
    # A new location(s) will not be created
    # If location(s) name already exist
    # =====================================================================
    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + "/api/admin/locations"

    stops_locations_names_list = [location_name.strip() for location_name in common_funcs.get_test_data_from_file(context,
        "../test_data/", "trip_details.csv", trip_test_id,"stops_locations_names").split(",")]

    for index, stop_location_name in enumerate(stops_locations_names_list):
        payload = build_location_payload(
            program_id=context.program_id,
            name=stop_location_name,
            company=common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                         stop_location_name, "company"),
            shipping_reference=common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                    stop_location_name, "shipping_reference"),
            geofence_radius_departure=common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                           stop_location_name, "geofence_radius_departure"),
            geofence_radius_arrival=common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                         stop_location_name, "geofence_radius_arrival"),
            required_data_points_departure=common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                                stop_location_name, "required_data_points_departure"),
            required_data_points_arrival=common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                              stop_location_name, "required_data_points_arrival"),
            type_id=common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                         stop_location_name, "type_id"),
            data_point_sequence_departure_id=common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                                  stop_location_name, "data_point_sequence_departure_id"),
            data_point_sequence_arrival_id=common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                                stop_location_name, "data_point_sequence_arrival_id"),
            time_zone=common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                           stop_location_name, "time_zone"),
            address1=common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                          stop_location_name, "address1"),
            address2=common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                          stop_location_name, "address2"),
            city=common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                      stop_location_name, "city"),
            state=common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                       stop_location_name, "state"),
            zip_code=common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                          stop_location_name, "zip_code"),
            country=common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                         stop_location_name, "country"),
            latitude=common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                          stop_location_name, "latitude"),
            longitude=common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                           stop_location_name, "longitude"),
            location_group_ids=common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                    stop_location_name, "location_group_ids"),
            product_ids=common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                             stop_location_name, "product_ids"),
            location_segment_name=common_funcs.get_test_data_from_file(context, "../test_data/", "locations.csv",
                                                                       stop_location_name, "location_segment_name"),
        )

        def perform_api_call(api_url, payload, headers):
            response = requests.post(api_url, json=payload, headers=headers)
            response_status_code = response.status_code

            if response_status_code == 201:
                print(f"A new Stop Location has been created with the name '{stop_location_name}'.")
            elif response_status_code == 400:
                try:
                    assert response.json().get("message") == "DUPLICATED_NAME_LOCATION"
                    print(f"A Location with the name '{stop_location_name}' already exist.")
                except:
                    raise AssertionError(
                        f"Add Location API call failed. \nStatus Code: {response_status_code} \nReason: {response.reason} \nJSON Response: {response.json()}")
            else:
                raise AssertionError(
                    f"Failed to create new Location: \nStatus Code: {response_status_code} \nReason: {response.reason}")

        # Add all locations to Stops groups and the last location to Final groups.
        if (index + 1) < len(stops_locations_names_list):
            # Retrieve Location Group IDs for groups that contain the word "Stops" in their names.
            payload["locationGroupIds"] = get_location_group_ids_by_provided_partial_name(context, "Stops")
            perform_api_call(api_url, payload, headers)
        else:
            # Retrieve Location Group IDs for groups that contain the word "Final" in their names.
            payload["locationGroupIds"] = get_location_group_ids_by_provided_partial_name(context, "Final")
            perform_api_call(api_url, payload, headers)


@when('I get list of stops locations ids for the trip with test_id "{trip_test_id}"')
@then('I get list of stops locations ids for the trip with test_id "{trip_test_id}"')
def get_stops_locations_ids_for_trip_test_id(context, trip_test_id):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    stops_locations_names_list = [location_name.strip() for location_name in common_funcs.get_test_data_from_file(context,
       "../test_data/", "trip_details.csv", trip_test_id, "stops_locations_names").split(",")]

    origin_location_ids = []

    for stop_location_name in stops_locations_names_list:
        api_url = base_url + (f"/api/admin/locations/programId/{context.program_id}?id=null&skip=0&take=50"
                                            f"&sort=name&filter={stop_location_name}&showDisabled=false&showLocked=false"
                                            f"&showProgramUnassigned=false")

        get_locations_response = requests.get(api_url, headers=headers)
        get_locations_response_json = get_locations_response.json()
        # Assuming there is at least one item in the response
        origin_location_id = get_locations_response_json["items"][0]["id"]
        origin_location_ids.append(origin_location_id)

    return origin_location_ids