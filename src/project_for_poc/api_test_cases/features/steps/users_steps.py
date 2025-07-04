import json
import requests as requests
from behave import given, when, then
import pyodbc
from storage import token
from storage import base_url
from APICommon.APICommonFuncs import common_funcs


@when('I create a new User Group with the name "{user_group_name}"')
@then('I create a new User Group with the name "{user_group_name}"')
def create_new_product_group_if_does_not_exist(context, user_group_name):
    # =====================================================================
    # A new user group will not be created
    # If user group with "{user_group_name}" already exist
    # =====================================================================
    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + f"/api/security/UserGroup/organization/{context.program_id}"

    payload = {
                  "id": 0,
                  "name": user_group_name,
                  "assignedRoles": [],
                  "assignedUsers": [],
                  "assignedExternalUsers": [],
                  "enabled": True
              }

    response = requests.post(api_url, json=payload, headers=headers)
    response_status_code = response.status_code

    if response_status_code == 200:
        print(f"A new Product Group has been created with the name '{user_group_name}'.")
    elif response_status_code == 409:
        try:
            assert response.text == "User group name is duplicated"
            print(f"A Product Group with the name '{user_group_name}' already exist.")
        except:
            raise AssertionError(f"Add Product Group API call failed. \nStatus Code: {response_status_code} \nReason: {response.reason} \nJSON Response: {response.json()}")
    else:
        raise AssertionError(f"Failed to create new Product Group: \nStatus Code: {response_status_code} \nReason: {response.reason}")


@when('I get User Group id by "{user_group_name}"')
@then('I get User Group id by "{user_group_name}"')
def get_user_group_id_by_user_group_name(context, user_group_name):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + (f"/api/security/UserGroup/List/organization/{context.program_id}?id=null&skip=0&take=500&"
                          f"sort=name&filter=&showDisabled=false&showLocked=false&showProgramUnassigned=false")

    response = requests.get(api_url, headers=headers)
    response_json = response.json()
    context.product_id = next(item["id"] for item in response_json["items"] if item["name"] == user_group_name)
    return context.user_group_name


@when('I get User Group ids')
@then('I get User Group ids')
def get_user_group_ids(context):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + (f"/api/security/UserGroup/List/organization/{context.program_id}?id=null&skip=0&take=50&"
                          f"sort=name&filter=&showDisabled=false&showLocked=false&showProgramUnassigned=false")

    response = requests.get(api_url, headers=headers)

    response_json = response.json()
    context.user_group_ids = [item["id"] for item in response_json["items"]]
    return context.user_group_ids