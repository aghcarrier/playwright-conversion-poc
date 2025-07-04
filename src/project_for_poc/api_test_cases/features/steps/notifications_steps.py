import requests as requests
from behave import given, when, then
import pyodbc
import json
from storage import token
from storage import base_url
from APICommon.APICommonFuncs import common_funcs


@when('I create a new notification with the name "{notification_name}" using "{template_name}" template')
@then('I create a new notification with the name "{notification_name}" using "{template_name}" template')
def create_new_notification_if_does_not_exist(context, notification_name, template_name):
    # =====================================================================
    # A new notification will not be created
    # If notification with "{notification_name}" already exist
    # =====================================================================
    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + f"/api/notification/organizations/{context.program_id}/definition"

    template_id = get_notification_template_id_by_provided_name(context, template_name)

    payload={
               "definitionName": f"{notification_name}",
               "description": "Created by API Automation",
               "defaultCultureId": "en-US",
               "sendMethod": "Email",
               "enabled": True,
               "template": f"{template_name}",
               "contents": [
                   template_id
               ],
               "recipients": [],
               "temperatureUnitTypeId": 1,
               "humidityUnitTypeId": 1,
               "lightUnitTypeId": 1,
               "cO2UnitTypeId": 1,
               "distanceUnitTypeId": 1,
               "lengthUnitTypeId": 2,
               "weightUnitTypeId": 2,
               "maximumNotificationAge": 30,
               "dateTimeFormatId": "1",
               "numberFormatId": "1",
               "timeZone": "US/Eastern",
               "statusId": "1",
               "statusName": ""
            }
    response = requests.post(api_url, json=payload, headers=headers)
    response_status_code = response.status_code

    if response_status_code == 200:
        print(f"A new Notification has been created with the name '{notification_name}'.")
    elif response_status_code == 409:
        try:
            # assert response.text == "The Notification definition name already exists"
            assert ("The Notification definition name already exists" in response.text
                    or "The Notification definition name already exists" in response.text), "A Notification with the name"
            print(f"A Notification with the name '{notification_name}' already exist.")
        except:
            raise AssertionError(f"Add Notification API call failed. \nStatus Code: {response_status_code} \nReason: {response.reason} \nJSON Response: {response.json()}")
    else:
        raise AssertionError(f"Failed to create new Notification: \nStatus Code: {response_status_code} \nReason: {response.reason}")


@when('I get Notification Template id for "{notification_template_name}"')
@then('I get Notification Template id for "{notification_template_name}"')
def get_notification_template_id_by_provided_name(context, notification_template_name):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + f"/api/notification/notificationtemplate/programId/{context.program_id}?showDisabled=true&take=1000"

    response = requests.get(api_url, headers=headers)
    response_status_code = response.status_code

    assert response_status_code == 200, f"Get notification API call failed with status code: '{response_status_code}'."
    json_data = response.json()

    # Check if there is existing data with notification_name
    found_match = False
    for item in json_data["searchResults"]:
        if item.get("name").lower() == notification_template_name.lower():
            context.notification_id = item.get("id")
            found_match = True
            break # Exit the loop when a match is found
    # If there is No data with notification_name then raise an error
    if not found_match:
        raise ValueError(f"Notification Template '{notification_template_name}' Does Not exist.")

    context.notification_name = notification_template_name
    return context.notification_id


@when('I get notification id for "{notification_name}"')
@then('I get notification id for "{notification_name}"')
def get_notification_id_by_provided_name(context, notification_name):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + f"/api/notification/organizations/{context.program_id}/definition?showDisabled=true"

    response = requests.get(api_url, headers=headers)
    response_status_code = response.status_code

    assert response_status_code == 200, f"Get notification API call failed with status code: '{response_status_code}'."
    json_data = response.json()

    # Check if there is existing data with notification_name
    found_match = False
    for item in json_data:
        if item.get("definitionName").lower() == notification_name.lower():
            context.notification_id = item.get("definitionId")
            found_match = True
            break # Exit the loop when a match is found
    # If there is No data with notification_name then raise an error
    if not found_match:
        raise ValueError(f"Notification with '{notification_name}' Does Not exist.")

    context.notification_name = notification_name
    return context.notification_id