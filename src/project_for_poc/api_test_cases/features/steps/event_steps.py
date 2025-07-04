import requests as requests
from behave import given, when, then
import json
from locations_steps import get_location_groups_ids
from products_steps import get_product_groups_ids
from containers_steps import get_container_groups_ids
from notifications_steps import get_notification_id_by_provided_name
from steps import users_steps
from storage import token
from storage import base_url
from APICommon.APICommonFuncs import common_funcs


@when('I create a new event to "Update Trip Status" with following variables')
@then('I create a new event to "Update Trip Status" with following variables')
def create_new_event_with_following_variables(context):
    """
    # =====================================================================
    # A new event will not be created
    # If event with "{event_name}" already exist
    # =====================================================================
    """

    """
    # Access values for "event_name", "event_severity_name", "condition_name", "action_status"
    # and "action_reason" from the data table for this step.
    """
    for row in context.table:
        event_name = row["event_name"]
        event_severity_name = row["event_severity_name"]
        condition_name = row["condition_name"]
        action_status = row["action_status"]
        # action_reason is either "Departure Reason" or "Arrival Reason", e.g. "Location" or "Stop Button" or "First Message"
        action_reason = row["action_reason"]
        email_notification_name = row["email_notification_name"]

        base_url = context.base_url
        authorization_token = context.token
        ocpkey = context.ocpkey

        headers = {"Content-Type": "application/json",
                   "Authorization": authorization_token,
                   "Ocp-Apim-Subscription-Key": ocpkey}

        api_url = base_url + f"/api/rule/Rule/programId/{context.program_id}"

        with open("../test_data/payloads/create_event_to_update_trip_status.json", "r") as file:
            payload = json.load(file)

        # Get Product Groups IDs to update the payload
        get_product_groups_ids(context)

        # Get Location Groups IDs to update the payload
        get_location_groups_ids(context)

        # Get Container Groups IDs to update the payload
        get_container_groups_ids(context)

        # Get Email Notification ID for provided email_notification_name to update the payload
        get_notification_id_by_provided_name(context, email_notification_name)

        # Update payload for program id, event name and user_names
        payload["programId"] = context.program_id
        payload["eventName"] = f"{event_name}"
        payload["lastUpdatedBy"] = context.user_name
        payload["createdBy"] = context.user_name

        # "event_severity_name_and_id" is dictionary(map) for Event Severity Names and IDs
        event_severity_name_and_id = {
            "Information": 1,
            "Warning": 2,
            "Critical": 3
        }
        # Get event_severity_id from event_severity_name_and_id based on event_severity_name
        if event_severity_name in event_severity_name_and_id:
            event_severity_id = event_severity_name_and_id.get(event_severity_name)
        else:
            raise ValueError(
                f"'{event_severity_name}' is not in the list of Event Severity. Please provide right Event Severity name")
        # Update payload for eventSeverity
        payload["eventSeverity"] = event_severity_id

        # "condition_name_and_id" is dictionary(map) for Condition Names and IDs
        condition_name_and_id = {
            "Extended Stop Identified": 1,
            "Departed Origin": 2,
            "Arrived at all Stops": 3,
            "Arrived at Final Destination": 5,
            "Draft Trip due to depart": 6,
            "Incomplete Trip Departed": 7,
            "Delayed Trip Arrival": 8,
            "Trip has not reported any Data": 9,
            "Trip has not reported any data after Planned Departure Time": 10,
            "Trip has stopped reporting data": 11,
            "Draft Trip due to depart - data complete": 12,
            "Draft Trip due to depart - data incomplete": 13,
            "Stop Button Pressed": 14,
            "First Device Message": 15
        }
        # Get condition_id from condition_name_and_id based on condition_name
        if condition_name in condition_name_and_id:
            condition_id = condition_name_and_id.get(condition_name)
        else:
            raise ValueError(
                f"'{condition_name}' is not in the list of Conditions. Please provide right Condition name")
        # Update payload for ruleConditions
        payload["ruleConditions"][0]["condition"]["id"] = condition_id
        payload["ruleConditions"][0]["condition"]["name"] = condition_name

        # Update Action Status and Reason
        if action_status.lower() == "arrived":
            payload["ruleActions"][0]["actionVariableId1"] = 4
            payload["ruleActions"][0]["actionVariableValue1"] = "Arrived"
            payload["ruleActions"][0]["arrivalReason"] = action_reason
        elif action_status.lower() == "in transit":
            payload["ruleActions"][0]["actionVariableId1"] = 3
            payload["ruleActions"][0]["actionVariableValue1"] = "In Transit"
            payload["ruleActions"][0]["departureReason"] = action_reason
        elif action_status.lower() == "started":
            payload["ruleActions"][0]["actionVariableId1"] = 6
            payload["ruleActions"][0]["actionVariableValue1"] = "Started"
        else:
            raise ValueError(f"'{action_status}' is not in the list of Status. Please provide right Status name")

        # Update event second action
        # payload["ruleActions"][1]["actionVariableId1"] = context.notification_id
        # payload["ruleActions"][1]["actionVariableValue1"] = context.notification_name
        # payload["ruleActions"][1]["locationGroups"] = context.location_group_ids
        # payload["ruleActions"][1]["originGroups"] = context.location_group_ids
        # payload["ruleActions"][1]["stopGroups"] = context.location_group_ids
        # payload["ruleActions"][1]["productGroups"] = context.product_groups_ids
        # payload["ruleActions"][1]["containerGroups"] = context.container_groups_ids

        response = requests.post(api_url, json=payload, headers=headers)
        response_status_code = response.status_code

        if response_status_code == 200:
            print(f"A new Event has been created with the name '{event_name}'.")
        elif response_status_code == 409:
            try:
                assert response.text == 'Event Name already exists. Please enter a different name.'
                print(f"A Event with the name '{event_name}' already exist.")
            except:
                raise AssertionError(
                    f"Add Event API call failed. \nStatus Code: {response_status_code} \nReason: {response.reason}")
        else:
            raise AssertionError(
                f"Failed to create new Event: \nStatus Code: {response_status_code} \nReason: {response.reason} \nJSON: {response.text}")


@when('I create a new email notification event with following variables')
@then('I create a new email notification event with following variables')
def create_new_email_notification_event_with_following_variables(context):
    """
    # =====================================================================
    # A new event will not be created
    # If event with "{event_name}" already exist
    # =====================================================================
    """

    """
    # Access values for "event_name", "event_severity_name", "condition_name", "action_status"
    # and "action_reason" from the data table for this step.
    """
    for row in context.table:
        event_name = row["event_name"]
        event_severity_name = row["event_severity_name"]
        event_category_name = row["event_category_name"]
        condition_name = row["condition_name"]
        email_notification_name = row["email_notification_name"]

        base_url = context.base_url
        authorization_token = context.token
        ocpkey = context.ocpkey

        headers = {"Content-Type": "application/json",
                   "Authorization": authorization_token,
                   "Ocp-Apim-Subscription-Key": ocpkey}

        api_url = base_url + f"/api/rule/Rule/programId/{context.program_id}"

        with open("../test_data/payloads/create_event_to_with_only_email_notification.json", "r") as file:
            payload = json.load(file)

        # Get product groups ids to update the payload
        get_product_groups_ids(context)

        # Get location groups ids to update the payload
        get_location_groups_ids(context)

        # Get container groups ids to update the payload
        get_container_groups_ids(context)

        # Get Email Notification ID for provided email_notification_name to update the payload
        get_notification_id_by_provided_name(context, email_notification_name)

        # Update payload for program id, event name and user_names
        payload["programId"] = context.program_id
        payload["eventName"] = f"{event_name}"
        payload["lastUpdatedBy"] = context.user_name
        payload["createdBy"] = context.user_name

        # "event_severity_name_and_id" is dictionary(map) for Event Severity Names and IDs
        event_severity_name_and_id = {
            "Information": 1,
            "Warning": 2,
            "Critical": 3
        }
        # Get event_severity_id from event_severity_name_and_id based on event_severity_name
        if event_severity_name in event_severity_name_and_id:
            event_severity_id = event_severity_name_and_id.get(event_severity_name)
        else:
            raise ValueError(
                f"'{event_severity_name}' is not in the list of Event Severity. Please provide right Event Severity name")
        # Update payload for eventSeverity
        payload["eventSeverity"] = event_severity_id

        # event_category_and_condition_names_and_ids contains Event Categories(Names and IDs)
        # Also Conditions(Names and IDs) for each Event Category
        event_category_and_condition_names_and_ids = {
            "Sensor": {
                "id": 1,
                "conditions": {
                    "Less than or Equal to": 1,
                    "Greater than or Equal to": 2
                    }
                },
            "Specification - Container": {
                "id": 2,
                "conditions": {
                    "Less than or Equal to": 1,
                    "Greater than or Equal to": 2,
                    "Equal to": 3,
                    "Not Equal to": 4,
                    "Less than": 5,
                    "Greater than": 6,
                    "Within range": 7,
                    "Contains Text": 8
                    }
                },
            "Specification - Product": {
                "id": 3,
                "conditions": {
                    "Less than or Equal to": 1,
                    "Greater than or Equal to": 2,
                    "Equal to": 3,
                    "Not Equal to": 4,
                    "Less than": 5,
                    "Greater than": 6,
                    "Within range": 7,
                    "Contains Text": 8
                    }
                },
            "Alarm - Container": {
                "id": 4,
                "conditions": {
                    "Has hit alarm": 1
                    }
                },
            "Alarm - Product": {
                "id": 5,
                "conditions": {
                    "Has hit alarm": 1
                    }
                },
            "Location": {
                "id": 6,
                "conditions": {
                    "Has left geofence": 1,
                    "Has entered geofence": 2
                    }
                },
            "Time": {
                "id": 7,
                "conditions": {
                    "Device Trip Length + Time Exceeded": 4,
                    "Time since departure": 5,
                    "Time at Final Location": 6,
                    "Time at Location": 7
                    }
                },
            "Monitor": {
                "id": 8,
                "conditions": {
                    "Unassigned Device Message": 1,
                    "Data not received for (data points)": 2,
                    "Has departed with trip in draft status": 3,
                    "Data not received for (time)": 4
                    }
                },
            "Trip": {
                "id": 9,
                "conditions": {
                    "Extended Stop Identified": 1,
                    "Departed Origin": 2,
                    "Arrived at all Stops": 3,
                    "Arrived at Final Destination": 5,
                    "Draft Trip due to depart": 6,
                    "Incomplete Trip Departed": 7,
                    "Delayed Trip Arrival": 8,
                    "Trip has not reported any Data": 9,
                    "Trip has not reported any data after Planned Departure Time": 10,
                    "Trip has stopped reporting data": 11,
                    "Draft Trip due to depart - data complete": 12,
                    "Draft Trip due to depart - data incomplete": 13,
                    "Stop Button Pressed": 14,
                    "First Device Message": 15
                    }
                },
            "Lane": {
                "id": 11,
                "conditions": {
                    "Late Departure": 1,
                    "Late Arrival": 2,
                    "Proximity to Destination": 3
                    }
                },
            "Device - Container": {
                "id": 12,
                "conditions": {
                    "Gateway - Low Battery Level": 1,
                    "Gateway - Communication Failure": 2,
                    "Remote Sensor - Communication Failure": 3
                    }
                },
            "Hardware Alarm": {
                "id": 13,
                "conditions": {
                    "Has hit alarm": 1
                    }
                }
        }
        # Check if event_category_name is in the event_category_and_condition_names_and_ids list
        if event_category_name in event_category_and_condition_names_and_ids:
            # Get event_rule_info which contains event_category_id and condition_name_and_id
            event_rule_info = event_category_and_condition_names_and_ids[event_category_name]

            # Get event_category_id and condition_name_and_id from event_rule_info
            event_category_id = event_rule_info["id"]
            condition_name_and_id = event_rule_info.get("conditions", {})

            # Check if condition_name is provided and get condition_id
            if condition_name in condition_name_and_id:
                condition_id = condition_name_and_id[condition_name]
            elif condition_name:
                raise ValueError(
                    f"'{condition_name}' is not in the list of Conditions for '{event_category_name}'. Please provide the correct Condition name")
        else:
            raise ValueError(
                f"'{event_category_name}' is not in the list of Event Category. Please provide the correct Event Category name")

        # Update payload for ruleConditions
        payload["ruleConditions"][0]["category"]["categoryId"] = event_category_id
        payload["ruleConditions"][0]["category"]["categoryName"] = event_category_name
        payload["ruleConditions"][0]["condition"]["id"] = condition_id
        payload["ruleConditions"][0]["condition"]["name"] = condition_name

        # Update event action
        payload["ruleActions"][0]["actionVariableId1"] = context.notification_id
        payload["ruleActions"][0]["actionVariableValue1"] = context.notification_name
        # payload["ruleActions"][0]["locationGroups"] = context.location_group_ids
        # payload["ruleActions"][0]["originGroups"] = context.location_group_ids
        # payload["ruleActions"][0]["stopGroups"] = context.location_group_ids
        # payload["ruleActions"][0]["productGroups"] = context.product_groups_ids
        # payload["ruleActions"][0]["containerGroups"] = context.container_groups_ids

        # Call to get_user_group_ids get user group ids
        payload["ruleActions"][0]["userGroups"] = users_steps.get_user_group_ids(context)

        response = requests.post(api_url, json=payload, headers=headers)
        response_status_code = response.status_code

        if response_status_code == 200:
            print(f"A new Event has been created with the name '{event_name}'.")
        elif response_status_code == 409:
            try:
                assert response.text == 'Event Name already exists. Please enter a different name.'
                print(f"A Event with the name '{event_name}' already exist.")
            except:
                raise AssertionError(
                    f"Add Event API call failed. \nStatus Code: {response_status_code} \nReason: {response.reason}")
        else:
            raise AssertionError(
                f"Failed to create new Event: \nStatus Code: {response_status_code} \nReason: {response.reason} \nJSON: {response.text}")