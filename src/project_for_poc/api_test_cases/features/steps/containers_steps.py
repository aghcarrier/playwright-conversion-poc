import json
import random
import requests as requests
from behave import given, when, then
from monitors_steps import create_monitor_s_for_trip_test_id, get_list_of_monitor_ids_for_trip_test_id, \
    update_monitor_usage_and_type_for_monitor_id_and_serial_number
from APICommon.APICommonFuncs import common_funcs
import pyodbc
from storage import token
from storage import base_url


@when('I create a new Zone Spec with the name "{zone_spec_name}"')
@then('I create a new Zone Spec with the name "{zone_spec_name}"')
def create_new_zone_spec_if_does_not_exist(context, zone_spec_name):
    # =====================================================================
    # A new Zone Spec will not be created
    # If Zone Spec with "{zone_spec_name}" already exist
    # =====================================================================
    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + "/api/admin/containerzonespec"

    # Read create_zone_spec.json file
    with open("../test_data/payloads/create_zone_spec.json", "r") as file:
        payload = json.load(file)

    # Make updates to payload components
    payload["name"] = zone_spec_name
    payload["programId"] = context.program_id

    response = requests.post(api_url, json=payload, headers=headers)
    response_status_code = response.status_code

    if response_status_code == 200:
        print(f"A new Zone Spec has been created with the name '{zone_spec_name}'.")
    elif response_status_code == 400:
        try:
            print(response.text)
            assert (f'"Error number 2627 in the THROW statement is outside the valid range. Specify an error number in the valid range of 50000 to 2147483647."' in response.text
                    or '42704: unrecognized exception condition \\"2627\\"' in response.text
                    or 'ContainerZoneSpec Name already exists. Please enter a different name.' in response.text ), 'Add Zone Spec API call failed'
            # assert response.text == f'"Error number 2627 in the THROW statement is outside the valid range. Specify an error number in the valid range of 50000 to 2147483647."'
            print(f"A Zone Spec with the name '{zone_spec_name}' already exist.")
        except:
            raise AssertionError(f"Add Zone Spec API call failed. \nStatus Code: {response_status_code} \nReason: {response.reason} \nJSON Response: {response.json()}")
    else:
        raise AssertionError(f"Failed to create new Zone Spec: \nStatus Code: {response_status_code} \nReason: {response.reason}")


@when('I create a new Container with the name "{container_name}" and "{zone_spec_name}" zone spec')
@then('I create a new Container with the name "{container_name}" and "{zone_spec_name}" zone spec')
def create_new_container_with_one_zone_spec_if_does_not_exist(context, container_name, zone_spec_name):
    # =====================================================================
    # A new Container will not be created
    # If Container with "{container_name}" already exist
    # =====================================================================
    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    # Create URL for GET Zone Specs API call
    get_zone_spec_id_api_url = base_url + (f"/api/admin/containerzonespecs/programId/{context.program_id}?id=null&skip=0&take=9999&sort"
                                   f"=id&filter=&showDisabled=false&showLocked=false&showProgramUnassigned=false")
    response = requests.get(get_zone_spec_id_api_url, headers=headers)
    response_status_code = response.status_code

    assert response_status_code == 200, f"Get Zone Specs API call failed with '{response_status_code}' status code."
    zone_specs_json_data = response.json()

    # Check if there is existing data with zone_spec_name
    found_match = False
    for item in zone_specs_json_data["items"]:
        if item.get("name").lower() == zone_spec_name.lower():
            zone_spec_id = item.get("id")
            found_match = True
            break  # Exit the loop when a match is found
    # If there is No data with zone_spec_name then raise an error
    if not found_match:
        raise ValueError(f"Zone Spec with '{zone_spec_name}' name Does Not exist.")

    # Create URL for Add Container POST API call
    api_url = base_url + "/api/admin/containers"

    # Read create_one_zone_container.json file
    with open("../test_data/payloads/create_one_zone_container.json", "r") as file:
        payload = json.load(file)

    # Make updates to payload components
    payload["name"] = container_name
    payload["programId"] = context.program_id
    payload["containerZones"][0]["containerZoneSpecId"] = zone_spec_id

    response = requests.post(api_url, json=payload, headers=headers)
    response_status_code = response.status_code

    if response_status_code == 201:
        print(f"A new Container has been created with the name '{container_name}'")
    elif response_status_code == 400:
        try:
            assert response.text == '"DUPLICATED_NAME_CONTAINER"'
            print(f"A Container with the name '{container_name}' already exist.")
        except:
            raise AssertionError(f"Add Container API call failed. \nStatus Code: {response_status_code} \nReason: {response.reason} \nJSON Response: {response.json()}")
    else:
        raise AssertionError(f"Failed to create new Container: \nStatus Code: {response_status_code} \nReason: {response.reason}")


@when('I create a new Container with the name "{container_name}" and zone specs "{first_zone_spec_name}" and "{second_zone_spec_name}"')
@then('I create a new Container with the name "{container_name}" and zone specs "{first_zone_spec_name}" and "{second_zone_spec_name}"')
def create_new_container_with_two_zone_spec_if_does_not_exist(context, container_name, first_zone_spec_name, second_zone_spec_name):
    # =====================================================================
    # A new Container will not be created
    # If Container with "{container_name}" already exist
    # =====================================================================
    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    # Create URL for GET Zone Specs API call
    get_zone_spec_id_api_url = base_url + (f"/api/admin/containerzonespecs/programId/{context.program_id}?id=null&skip=0&take=9999&sort"
                                   f"=id&filter=&showDisabled=false&showLocked=false&showProgramUnassigned=false")
    response = requests.get(get_zone_spec_id_api_url, headers=headers)
    response_status_code = response.status_code

    assert response_status_code == 200, f"Get Zone Specs API call failed with '{response_status_code}' status code"
    zone_specs_json_data = response.json()

    # Check if there is existing data with first_zone_spec_name and second_zone_spec_name
    first_zone_spec_id = None
    second_zone_spec_id = None
    for item in zone_specs_json_data["items"]:
        if item.get("name").lower() == first_zone_spec_name.lower():
            first_zone_spec_id = item.get("id")
        elif item.get("name").lower() == second_zone_spec_name.lower():
            second_zone_spec_id = item.get("id")

    if first_zone_spec_id is None or second_zone_spec_id is None:
        raise ValueError(f"'{first_zone_spec_name}' Zone Spec, '{second_zone_spec_name}' Zone Spec or both Zone Specs do not exist.")

    # Create URL for Add Container POST API call
    api_url = base_url + "/api/admin/containers"

    # Read create_two_zone_container.json file
    with open("../test_data/payloads/create_two_zone_container.json", "r") as file:
        payload = json.load(file)

    # Make updates to payload components
    payload["name"] = container_name
    payload["programId"] = context.program_id
    payload["containerZones"][0]["containerZoneSpecId"] = first_zone_spec_id
    payload["containerZones"][1]["containerZoneSpecId"] = second_zone_spec_id

    response = requests.post(api_url, json=payload, headers=headers)
    response_status_code = response.status_code

    if response_status_code == 201:
        print(f"A new Container has been created with the name '{container_name}'.")
    elif response_status_code == 400:
        try:
            assert response.text == '"DUPLICATED_NAME_CONTAINER"'
            print(f"A Container with the name '{container_name}' already exist.")
        except:
            raise AssertionError(f"Add Container API call failed. \nStatus Code: {response_status_code} \nReason: {response.reason} \nJSON Response: {response.json()}")
    else:
        raise AssertionError(f"Failed to create new Container: \nStatus Code: {response_status_code} \nReason: {response.reason}")


@when('I create a container for the trip with the test_id "{trip_test_id}"')
@then('I create a container for the trip with the test_id "{trip_test_id}"')
def create_container_for_trip_id(context, trip_test_id):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + "/api/admin/containers"

    random_int = str(random.randint(1, 9999)).zfill(4)
    context.container_name = common_funcs.get_test_data_from_file(context, "../test_data/", "trip_details.csv",
                                                                             trip_test_id, "container_name") + f"_{random_int}"
    container_zone_name_list = [zone.strip() for zone in common_funcs.get_test_data_from_file(context, "../test_data/",
                                 "trip_details.csv", trip_test_id, "container_zone_names").split(",")]
    container_group_name = common_funcs.get_test_data_from_file(context, "../test_data/", "trip_details.csv",
                                                                             trip_test_id, "container_group_name")

    # Get container zone IDs using container zone names and create container_zone_id_list
    container_zone_id_list = []
    for container_zone_name in container_zone_name_list:
        zone_id = get_zone_spec_id_by_name(context, container_zone_name)
        container_zone_id_list.append(zone_id)

    # Create monitors for the trip
    create_monitor_s_for_trip_test_id(context, trip_test_id)

    # Get list of Serial Numbers and IDs for monitors
    if len(get_list_of_monitor_ids_for_trip_test_id(context, trip_test_id)) == len(container_zone_name_list):
        # if number of monitors match with number of spec zones then getaway does not have monitor attached to it
        context.monitors_serial_number_list = context.modified_monitor_list
        context.monitors_ids_list = get_list_of_monitor_ids_for_trip_test_id(context, trip_test_id)
        context.gateway_monitor_id = None
    else:
        # Assign first element for monitor id to gateway_monitor_id
        context.gateway_monitor_id = get_list_of_monitor_ids_for_trip_test_id(context, trip_test_id)[0]
        context.gateway_monitor_serial_number = context.modified_monitor_list[0]
        # Remove first element from lists, because it is for getaway
        context.monitors_serial_number_list = context.modified_monitor_list[1:]
        context.monitors_ids_list = get_list_of_monitor_ids_for_trip_test_id(context, trip_test_id)[1:]

    # Update monitors to be "Continuous use"
    for monitor_id, monitor_serial_number in zip(context.monitors_ids_list, context.monitors_serial_number_list):
        update_monitor_usage_and_type_for_monitor_id_and_serial_number(context, "Continuous use", "SensiWatch Sensor",
                                                                       monitor_id, monitor_serial_number)

    # Update Gateway Monitor if it exists
    if context.gateway_monitor_id is not None:
        update_monitor_usage_and_type_for_monitor_id_and_serial_number(context, "Continuous use", "SensiWatch Gateway",
                                                                       context.gateway_monitor_id, context.gateway_monitor_serial_number)

    # Get existing container list
    existing_container_list = get_container_names(context)
    # Check if container_name is in existing_container_list, then update it. If not, then create a new one
    if context.container_name in existing_container_list:
        """If container_name is in existing_container_list, then update it"""
        # Read update_container.json file
        with open("../test_data/payloads/update_container.json", "r") as file:
            payload = json.load(file)

        # Get container_id and container_group_id
        context.container_id = get_container_id_by_name(context, context.container_name)
        container_group_id = get_container_groups_id_by_name(context, container_group_name)

        # Update "container id", "container name", "programId" and "container group id" in the payload
        payload["id"] = context.container_id
        payload["name"] = context.container_name
        payload["programId"] = context.program_id
        payload["containerGroupIds"] = [container_group_id]

        # Update "gatewayMonitorId" in the payload if it is not None
        if context.gateway_monitor_id is not None:
            payload["gatewayMonitorId"] = context.gateway_monitor_id

        single_container_zone_list = []
        for zone_spec_name, zone_spec_id, monitor_id, monitor_name in zip(container_zone_name_list,
                                                                          container_zone_id_list,
                                                                          context.monitors_ids_list,
                                                                          context.monitors_serial_number_list):
            # Read single_container_zone_to_update_container.json file
            with open("../test_data/payloads/single_container_zone_to_update_container.json", "r") as file:
                single_container_zone = json.load(file)
            single_container_zone["name"] = zone_spec_name
            single_container_zone["containerZoneSpecId"] = zone_spec_id
            single_container_zone["monitorIds"] = [monitor_id]
            single_container_zone["monitorsAddedDetails"][0]["id"] = monitor_id
            single_container_zone["monitorsAddedDetails"][0]["name"] = monitor_name

            # Add single_container_zone to single_container_zone_list
            single_container_zone_list.append(single_container_zone)

        # Update payload for container zone list
        payload["containerZones"] = single_container_zone_list

        response = requests.put(api_url, json=payload, headers=headers)
        response_status_code = response.status_code

        if response_status_code == 200:
            print(f"'{context.container_name}' container is updated.")
            return context.container_id
        else:
            raise AssertionError(
                f"Failed to update container with name '{context.container_name}': \nStatus Code: {response_status_code} \nReason: {response.reason}")
    else:
        """if container_name is NOT in existing_container_list, create a new container"""
        with open("../test_data/payloads/create_container_for_trip.json", "r") as file:
            payload = json.load(file)

        # Get container_group_id
        container_group_id = get_container_groups_id_by_name(context, container_group_name)
        # Update "container name", "programId" and "container group id" in the payload
        payload["name"] = context.container_name
        payload["programId"] = context.program_id
        payload["containerGroupIds"] = [container_group_id]

        # Update "gatewayMonitorId" in the payload if it is not None
        if context.gateway_monitor_id is not None:
            payload["gatewayMonitorId"] = context.gateway_monitor_id

        single_container_zone_list = []
        for zone_spec_name, zone_spec_id, monitor_id, monitor_name in zip(container_zone_name_list,
                                                                          container_zone_id_list,
                                                                          context.monitors_ids_list,
                                                                          context.monitors_serial_number_list):
            # Read single_container_zone_to_update_container.json file
            with open("../test_data/payloads/single_container_zone_to_create_container.json", "r") as file:
                single_container_zone = json.load(file)

            single_container_zone["name"] = zone_spec_name
            single_container_zone["containerZoneSpecId"] = zone_spec_id
            single_container_zone["monitorIds"] = [monitor_id]

            # Create one monitor detail
            monitor_detail = {"id": 0, "name": "Update the Serial Number"}

            # Update monitor_detail
            monitor_detail["id"] = monitor_id
            monitor_detail["name"] = monitor_name
            # Add monitor_detail to single_container_zone["monitorsAddedDetails"] list
            single_container_zone["monitorsAddedDetails"] = [monitor_detail]

            # Add single_container_zone to single_container_zone_list
            single_container_zone_list.append(single_container_zone)

        # Update payload for container zone list
        payload["containerZones"] = single_container_zone_list

        response = requests.post(api_url, json=payload, headers=headers)
        response_status_code = response.status_code

        if response_status_code == 201:
            print(f"'{context.container_name}' container is created.")
            context.container_id = response.json()["id"]
            return context.container_id
        else:
            raise AssertionError(
                f"Failed to create container with name '{context.container_name}': \nStatus Code: {response_status_code} \nReason: {response.reason}")


@when('I get Zone Spec ID for "{zone_spec_name}"')
@then('I get Zone Spec ID for "{zone_spec_name}"')
def get_zone_spec_id_by_name(context, zone_spec_name):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + (f"/api/admin/containerzonespecs/programId/{context.program_id}?id=null&skip=0&take=999999"
                          f"&sort=id&filter=&showDisabled=false&showLocked=false&showProgramUnassigned=false")

    response = requests.get(api_url, headers=headers)
    response_status_code = response.status_code

    assert response_status_code == 200, f"Get Zone Spec API call failed with status code: '{response_status_code}'."
    json_data = response.json()

    for item in json_data["items"]:
        if item["name"] == zone_spec_name:
            context.container_zone_spec_id = item["id"]
            break
    else:
        raise ValueError(f"Container with the specified name '{zone_spec_name}' does not exist.")
    return context.container_zone_spec_id


@when('I get container ID for "{container_name}"')
@then('I get container ID for "{container_name}"')
def get_container_id_by_name(context, container_name):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + (f"/api/admin/containers/programId/{context.program_id}?take=1000&skip=0&sort=name&filter"
                          f"=&showDisabled=false")

    response = requests.get(api_url, headers=headers)
    response_status_code = response.status_code

    assert response_status_code == 200, f"Get containers list API call failed with status code: '{response_status_code}'."
    json_data = response.json()

    for item in json_data["items"]:
        if item["name"] == container_name:
            context.container_id = item["id"]
            break
    else:
        raise ValueError(f"Container with the specified name '{container_name}' does not exist.")
    return context.container_id


@when('I get container IDs')
@then('I get container IDs')
def get_container_ids(context):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + (f"/api/admin/containers/programId/{context.program_id}?take=1000&skip=0&sort=name&filter"
                          f"=&showDisabled=false")

    response = requests.get(api_url, headers=headers)
    response_status_code = response.status_code

    assert response_status_code == 200, f"Get containers list API call failed with status code: '{response_status_code}'."
    json_data = response.json()

    context.container_ids = [item["id"] for item in json_data.get("items", [])]
    return context.container_ids


@when('I get container Names')
@then('I get container Names')
def get_container_names(context):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + (f"/api/admin/containers/programId/{context.program_id}?take=1000&skip=0&sort=name&filter"
                          f"=&showDisabled=false")

    response = requests.get(api_url, headers=headers)
    response_status_code = response.status_code

    assert response_status_code == 200, f"Get containers list API call failed with status code: '{response_status_code}'."
    json_data = response.json()

    context.container_names = [item["name"] for item in json_data.get("items", [])]
    return context.container_names


@when('I create a new Container Group with the name "{container_group_name}" and add all containers')
@then('I create a new Container Group with the name "{container_group_name}" and add all containers')
def create_new_container_group_if_does_not_exist(context, container_group_name):
    # =====================================================================
    # A new Container Group will not be created
    # If Container Group with "{container_group_name}" already exist
    # =====================================================================
    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    # Check if Container Group exist with "{container_group_name}"
    container_group_names_list = get_container_groups_names(context)
    # for name in container_group_names_list:
    if any(container_group_name.lower() == name.lower() for name in container_group_names_list):
        print(f"A Container Group with the name '{container_group_name}' already exist.")
    else:
        create_new_container_api_url = base_url + "/api/admin/containergroups"

        # Get All Container IDs to update the payload
        all_container_ids = get_container_ids(context)

        payload = {
                      "name": container_group_name,
                      "description": "Created by API Automation",
                      "enabled": True,
                      "programId": context.program_id,
                      "containerIds": all_container_ids,
                      "useAppContainerDefaults": False
                  }

        response = requests.post(create_new_container_api_url, json=payload, headers=headers)
        response_status_code = response.status_code

        if response_status_code == 201:
            print(f"A new Container Group has been created with the name '{container_group_name}'.")
        else:
            raise AssertionError(f"Failed to create new Container Group: \nStatus Code: {response_status_code} \nReason: {response.reason} \nJSON Response: {response.json()}")


@when('I update the Container Group with the name "{container_group_name}" and add all containers')
@then('I update the Container Group with the name "{container_group_name}" and add all containers')
def update_container_group_and_add_all_containers(context, container_group_name):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + "/api/admin/containergroups"

    # Check if Container Group exist with "container_group_name"
    container_group_names_list = get_container_groups_names(context)
    # for name in container_group_names_list:
    if any(container_group_name.lower() == name.lower() for name in container_group_names_list):

        # Get Container Group ID
        container_group_id = get_container_groups_id_by_name(context, container_group_name)

        # Get All Container IDs to update the payload
        all_container_ids = get_container_ids(context)

        payload = {
            "name": container_group_name,
            "description": "Updated by API Automation",
            "enabled": True,
            "programId": context.program_id,
            "containerIds": all_container_ids,
            "useAppContainerDefaults": False,
            "id": container_group_id
        }

        response = requests.put(api_url, json=payload, headers=headers)
        response_status_code = response.status_code

        if response_status_code == 200:
            print(f"'{container_group_name}' Container Group has been updated and all containers are added into it.")
        else:
            raise AssertionError(
                f"Failed to update '{container_group_name}' Container Group: \nStatus Code: {response_status_code} "
                f"\nReason: {response.reason} \nJSON Response: {response.json()}")
    else:
        AssertionError(
            f"Container Group with the name {container_group_name} does not exist")


@when('I get Container Groups ID for "{container_group_name}"')
@then('I get Container Groups ID for "{container_group_name}"')
def get_container_groups_id_by_name(context, container_group_name):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + (f"/api/admin/containergroups/programId/{context.program_id}?id=null&skip=0&take=1000&sort"
                          f"=name&filter=&showDisabled=false&showLocked=false&showProgramUnassigned=false")

    response = requests.get(api_url, headers=headers)
    response_status_code = response.status_code

    assert response_status_code == 200, f"Get Container Groups list API call failed with status code: '{response_status_code}'."
    response_json = response.json()

    for item in response_json["items"]:
        if item["name"] == container_group_name:
            context.container_group_id = item["id"]
            break
    else:
        raise ValueError(f"Container with the specified name '{container_group_name}' does not exist.")
    return context.container_group_id


@when('I get Container Groups IDs')
@then('I get Container Groups IDs')
def get_container_groups_ids(context):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + (f"/api/admin/containergroups/programId/{context.program_id}?id=null&skip=0&take=1000&sort"
                          f"=name&filter=&showDisabled=false&showLocked=false&showProgramUnassigned=false")

    response = requests.get(api_url, headers=headers)
    response_status_code = response.status_code

    assert response_status_code == 200, f"Get Container Groups list API call failed with status code: '{response_status_code}'."

    response_json = response.json()
    context.container_groups_ids = [item["id"] for item in response_json["items"]]
    return context.container_groups_ids


@when('I get Container Groups Names')
@then('I get Container Groups Names')
def get_container_groups_names(context):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + (f"/api/admin/containergroups/programId/{context.program_id}?id=null&skip=0&take=1000&sort"
                          f"=name&filter=&showDisabled=false&showLocked=false&showProgramUnassigned=false")

    response = requests.get(api_url, headers=headers)
    response_status_code = response.status_code

    assert response_status_code == 200, f"Get Container Groups list API call failed with status code: '{response_status_code}'."

    response_json = response.json()
    context.container_groups_names = [item["name"] for item in response_json["items"]]
    return context.container_groups_names


@when('I get Container and its attached monitors details for "{container_id}"')
@then('I get Container and its attached monitors details for "{container_id}"')
def get_container_and_its_attached_monitors_details(context, container_id):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + (f"/api/admin/containers/{container_id}/programId/{context.program_id}")

    response = requests.get(api_url, headers=headers)
    response_status_code = response.status_code

    assert response_status_code == 200, f"Get Container Details API call failed with status code: '{response_status_code}'."
    response_json = response.json()

    context.zone_name_list = [zone["name"] for zone in response_json.get("containerZones", [])]
    context.zone_id_list = [zone["id"] for zone in response_json.get("containerZones", [])]
    context.attached_monitors_serial_numbers_list = [monitor["serialNumber"] for zone in response_json.get("containerZones", []) for monitor in zone.get("monitors", [])]
    context.attached_monitors_id_list = [monitor["id"] for zone in response_json.get("containerZones", []) for monitor in zone.get("monitors", [])]

    return context.zone_name_list, context.zone_id_list, context.attached_monitors_serial_numbers_list, context.attached_monitors_id_list