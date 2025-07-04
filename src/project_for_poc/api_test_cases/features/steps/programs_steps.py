import requests as requests
from behave import given, when, then
import json
from steps.storage import token, base_url
from steps.APICommon.APICommonFuncs import common_funcs


@given('I create a new program if it does not exist')
@when('I create a new program if it does not exist')
def create_new_program_if_does_not_exist(context):
    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    program_name = context.program_name
    api_url = base_url + "/api/admin/programs"
    payload={
              "name": f"{program_name}",
              "description": "Created by API Automation",
              "typeId": "1",
              "enabled": "true",
              "enableExpressSync": "false",
              "languageIds": [],
              "e9Id": "",
              "erpSystem": "",
              "linkedProgramIds": [],
              "linkedAnalyticsIds": [
                  8,
                  9
              ],
              "temperatureUnitId": 1,
              "humidityUnitId": 1,
              "co2UnitId": 1,
              "lightUnitId": 1,
              "distanceUnitId": 1,
              "dateTimeFormatId": 1,
              "numberFormatId": 1,
              "lengthUnitId": 2,
              "weightUnitId": 2,
              "powerBIWorkspaces": [
                  "42447d16-43e2-4526-9e90-41d8194cb80a",
                  "aa7374a3-e2dc-4b1c-8f90-b7b089c9820b",
                  "491f96d3-3ab0-48fe-9524-5e90e13ba195",
                  "a3939b9d-39dd-4ff5-9d45-0bc9448f821a",
                  "dca775b3-3aba-4c67-911f-70da2b1ea96e",
                  "9973633f-850c-4175-97a1-387b2a462b65",
                  "3db1f1c1-f1fb-4228-b840-b9b2246c8306",
                  "92ee4a21-cdf3-4c8e-ba57-8dd1132e201a"
              ],
              "regionId": "1",
              "allowPublicTrips": "true",
              "linkedPublicTripsIds": [
                  4,
                  7,
                  8,
                  6,
                  1,
                  2,
                  3,
                  9,
                  10,
                  5
              ],
              "timeZone": "Etc/UCT",
              "maximumGatewayReadingAgeThreshold": 120,
              "maximumSensorReadingAgeThreshold": 120,
              "minimumBatteryLevelThreshold": 20
            }
    response = requests.post(api_url, json=payload, headers=headers)
    response_status_code = response.status_code

    if response_status_code == 201:
        context.program_id = response.json()["id"]
        print(f"A new Program has been created with the name '{program_name}'.")
    elif response_status_code == 400:
        try:
            assert response.json().get('message') == 'DUPLICATED_NAME_PROGRAM'
            print(f"A Program with the name '{program_name}' already exist.")
        except:
            raise AssertionError(f"Create New Program API call failed. \nStatus Code: {response_status_code} \nReason: {response.reason} \nJSON Response: {response.json()}")
    else:
        raise AssertionError(f"Failed to create new Program: \nStatus Code: {response_status_code} \nReason: {response.reason}")


@when('I get program id by "{program_name}"')
@then('I get program id by "{program_name}"')
def get_program_id_by_program_name(context, program_name):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + "/api/admin/programs?id=null&skip=0&take=99999&sort=name&filter=&showDisabled=false&showLocked=false&showProgramUnassigned=false"

    response = requests.get(api_url, headers=headers)
    response_json = response.json()
    context.program_id = next((item["id"] for item in response_json["items"] if item["name"] == program_name), None)
    return context.program_id