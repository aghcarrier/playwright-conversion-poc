from behave import given, when, then
import requests as requests
from containers_steps import get_container_groups_id_by_name
from locations_steps import get_location_group_ids_by_provided_partial_name
import json
import pyodbc
from storage import token
from storage import base_url


@when('I create a new Automation Outbound Rule for Trips(or update if it exist) with "{container_group_name}" container group and the name "{trip_automation_rule_name}"')
@then('I create a new Automation Outbound Rule for Trips(or update if it exist) with "{container_group_name}" container group and the name "{trip_automation_rule_name}"')
def create_new_automation_outbound_rule_for_trips_or_update_if_it_exist(context, container_group_name, trip_automation_rule_name):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    payload = {
        "enabled": "true",
        "name": trip_automation_rule_name,
        "description": "",
        "timeAtStops": 0,
        "containerGroups": [],
        "originLocationGroups": [],
        "intermediateStopLocationGroups": [],
        "finalDestinationLocationGroups": [],
        "AutomationType": 2
    }

    # Retrieve Location Group IDs for groups that contain the word "Origin" in their names.
    origin_location_groups_ids = get_location_group_ids_by_provided_partial_name(context, "Origin")

    # Retrieve Location Group IDs for groups that contain the word "Stops" in their names.
    stops_location_groups_ids = get_location_group_ids_by_provided_partial_name(context, "Stops")

    # Retrieve Location Group IDs for groups that contain the word "Final" in their names.
    final_destination_location_groups_ids = get_location_group_ids_by_provided_partial_name(context, "Final")

    # Retrieve trip automation rule type for provided name
    automation_rule_type_for_provided_name = get_trip_automation_rule_type_for_the_name(context, trip_automation_rule_name)

    # Update the payload.
    payload["originLocationGroups"] = origin_location_groups_ids
    payload["intermediateStopLocationGroups"] = stops_location_groups_ids
    payload["finalDestinationLocationGroups"] = final_destination_location_groups_ids

    # If Trip Automation Rule with the name "trip_automation_rule_name" does not exist then create a new one.
    if automation_rule_type_for_provided_name is None:

        # Retrieve Container Group ID for container_group_name from available list for trip automation rule
        container_group_id = get_container_group_id_for_provided_name_if_it_is_available_for_trip_automation_rule(context, container_group_name)

        api_url = base_url + f"/api/admin/tripautomationrules/programId/{context.program_id}"

        # Update the payload.
        payload["description"] = "Created by API Automation"
        payload["containerGroups"] = [container_group_id]

        response = requests.post(api_url, json=payload, headers=headers)
        response_status_code = response.status_code

        if response_status_code == 201:
            print(f"A new Outbound Automation Rule for Trips has been created with the name '{trip_automation_rule_name}'.")
        else:
            raise AssertionError(
                f"Failed to create new Outbound Automation Rule for Trips: "
                f"\nStatus Code: {response_status_code} \nReason: {response.reason}")
    # Else Update existing Outbound Automation Rule
    else:

        # If automation rule type is Outbound ("AutomationType": 2) then update it
        if automation_rule_type_for_provided_name == 2:

            # Retrieve Container Group ID for container_group_name
            container_group_id = get_container_groups_id_by_name(context, container_group_name)

            # Retrieve Trip Automation Rule ID for trip_automation_rule_name
            trip_automation_rule_id = get_trip_automation_rule_id_for_the_name(context, trip_automation_rule_name)

            api_url = base_url + f"/api/admin/tripautomationrules/id/{trip_automation_rule_id}/programId/{context.program_id}"

            # Update the payload.
            payload["description"] = "Updated by API Automation"
            payload["containerGroups"] = [container_group_id]

            program_id_element = {"programId": context.program_id}
            payload.update(program_id_element)

            response = requests.put(api_url, json=payload, headers=headers)
            response_status_code = response.status_code

            if response_status_code == 200:
                print(
                    f"Outbound Automation Rule with the name '{trip_automation_rule_name}' has been updated.")
            else:
                raise AssertionError(f"Failed to update '{trip_automation_rule_name}' Outbound Automation Rule for Trips: "
                                     f"\nStatus Code: {response_status_code} \nReason: {response.reason} {response.text}")
        # Else if automation rule type is Inbound ("AutomationType": 2) then raise an error
        else:
            raise ValueError(f"'{trip_automation_rule_name}' is not Outbound rule and can not be updated by this method.")


@when('I get Trip Automation Rule Type for the name "{trip_automation_rule_name}"')
@then('I get Trip Automation Rule Type for the name "{trip_automation_rule_name}"')
def get_trip_automation_rule_type_for_the_name(context, trip_automation_rule_name):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + (f"/api/admin/tripautomationrules/search/programId/{context.program_id}?id=null&skip=0&take"
                          f"=1000&sort=name&filter=&showDisabled=true&showLocked=false&showProgramUnassigned=false")

    response = requests.get(api_url, headers=headers)
    response_status_code = response.status_code

    assert response_status_code == 200, f"Get Trip Automation Rule API call failed with status code: '{response_status_code}'."
    response_json = response.json()

    existing_trip_automation_rule_name_list = [item["name"] for item in response_json["items"]]

    # If trip_automation_rule_name is in existing_trip_automation_rule_name_list then return Automation Rule Type
    if trip_automation_rule_name in existing_trip_automation_rule_name_list:
        for item in response_json["items"]:
            if item["name"] == trip_automation_rule_name:
                return item["automationType"]
    else:
        return None  # Return "None" if the name is not found in the list of names for Trip Automation Rules.


@when('I get Container Group ID for the name "{container_group_name}" if it is available for trip automation rule')
@then('I get Container Group ID for the name "{container_group_name}" if it is available for trip automation rule')
def get_container_group_id_for_provided_name_if_it_is_available_for_trip_automation_rule(context, container_group_name):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + f"/api/admin/tripautomationrules/containergroups/programId/{context.program_id}"

    """Get available Container Groups IDs"""
    response = requests.get(api_url, headers=headers)
    response_status_code = response.status_code

    assert response_status_code == 200, f"Get available Container Groups IDs API call failed with status code: '{response_status_code}'."
    response_json = response.json()

    available_container_group_name_list = [item["name"] for item in response_json]

    # If container_group_name is in available_container_group_name_list then return Container Group ID
    if container_group_name in available_container_group_name_list:
        for item in response_json:
            if item["name"] == container_group_name:
                return item["id"]
    else:
        raise ValueError(f"'{container_group_name}' is not in the list of available Container Group.")


@when('I get Trip Automation Rule ID for the name "{automation_rule_name}"')
@then('I get Trip Automation Rule ID for the name "{automation_rule_name}"')
def get_trip_automation_rule_id_for_the_name(context, automation_rule_name):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + (f"/api/admin/tripautomationrules/search/programId/{context.program_id}?id=null&skip=0&"
                          f"take=999&sort=name&filter=&showDisabled=false&showLocked=false&showProgramUnassigned=false")

    """Get available Container Groups IDs"""
    response = requests.get(api_url, headers=headers)
    response_status_code = response.status_code

    assert response_status_code == 200, f"Get list of Trip Automation Rules API call failed with status code: '{response_status_code}'."
    response_json = response.json()

    context.trip_automation_rules_id = next(item["id"] for item in response_json["items"] if item["name"] == automation_rule_name)
    return context.trip_automation_rules_id