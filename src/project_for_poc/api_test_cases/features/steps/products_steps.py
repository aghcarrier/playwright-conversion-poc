import json
import requests as requests
from behave import given, when, then
import pyodbc
from storage import token
from storage import base_url
from APICommon.APICommonFuncs import common_funcs


@when('I create a new Product with the name "{product_name}"')
@then('I create a new Product with the name "{product_name}"')
def create_new_product_if_does_not_exist(context, product_name):
    # =====================================================================
    # A new product will not be created
    # If product with "{product_name}" already exist
    # =====================================================================
    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + "/api/admin/products"

    # Read create_product.json file
    with open("../test_data/payloads/create_product.json", "r") as file:
        payload = json.load(file)

    # Make updates to payload components
    payload["name"] = product_name
    payload["programId"] = context.program_id

    response = requests.post(api_url, json=payload, headers=headers)
    response_status_code = response.status_code

    if response_status_code == 201:
        print(f"A new Product has been created with the name '{product_name}'.")
    elif response_status_code == 400:
        try:
            assert response.json().get('message') == "DUPLICATED_NAME_PRODUCT"
            print(f"A Product with the name '{product_name}' already exist.")
        except:
            raise AssertionError(f"Add Product API call failed. \nStatus Code: {response_status_code} \nReason: {response.reason} \nJSON Response: {response.json()}")
    else:
        raise AssertionError(f"Failed to create new Product: \nStatus Code: {response_status_code} \nReason: {response.reason}")


@when('I get product IDs')
@then('I get product IDs')
def get_product_ids(context):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + (f"/api/admin/products/programId/{context.program_id}?take=50&skip=0&sort=name&filter=&showDisabled=false")

    response = requests.get(api_url, headers=headers)
    response_status_code = response.status_code

    assert response_status_code == 200, f"Get products list API call failed with status code: '{response_status_code}'."
    json_data = response.json()

    context.product_ids = [item["id"] for item in json_data.get("items", [])]
    return context.product_ids


@when('I create a new Product Group with the name "{product_group_name}" and add all products')
@then('I create a new Product Group with the name "{product_group_name}" and add all products')
def create_new_product_group_if_does_not_exist(context, product_group_name):
    # =====================================================================
    # A new product group will not be created
    # If product group with "{product_group_name}" already exist
    # =====================================================================
    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + "/api/admin/productgroups"

    # Get All Product IDs to update the payload
    all_product_ids = get_product_ids(context)

    payload = {
                  "id": None,
                  "programId": context.program_id,
                  "name": product_group_name,
                  "description": "Created by API Automation",
                  "productIds": all_product_ids,
                  "productCount": None,
                  "enabled": "true",
                  "createdBy": None,
                  "createdOn": None,
                  "modifiedBy": None,
                  "modifiedOn": None
              }

    response = requests.post(api_url, json=payload, headers=headers)
    response_status_code = response.status_code

    if response_status_code == 201:
        print(f"A new Product Group has been created with the name '{product_group_name}'.")
    elif response_status_code == 400:
        try:
            assert response.json().get('message') == "DUPLICATED_NAME_PRODUCTGROUP"
            print(f"A Product Group with the name '{product_group_name}' already exist.")
        except:
            raise AssertionError(f"Add Product Group API call failed. \nStatus Code: {response_status_code} \nReason: {response.reason} \nJSON Response: {response.json()}")
    else:
        raise AssertionError(f"Failed to create new Product Group: \nStatus Code: {response_status_code} \nReason: {response.reason}")


@when('I get product id for the trip with test_id "{trip_test_id}"')
@then('I get product id for the trip with test_id "{trip_test_id}"')
def get_product_id_for_trip_test_id(context, trip_test_id):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    product_name = common_funcs.get_test_data_from_file(context, "../test_data/", "trip_details.csv",
                                                                trip_test_id, "product_name")

    api_url = base_url + f"/api/admin/products/programId/{context.program_id}?take=50&skip=0&sort=name&filter={product_name}&showDisabled=false"

    response = requests.get(api_url, headers=headers)
    response_json = response.json()
    context.product_id = next(item["id"] for item in response_json["items"] if item["name"] == product_name)
    return context.product_id


@when('I get Product Groups IDs')
@then('I get Product Groups IDs')
def get_product_groups_ids(context):

    base_url = context.base_url
    authorization_token = context.token
    ocpkey = context.ocpkey

    headers = {"Content-Type": "application/json",
               "Authorization": authorization_token,
               "Ocp-Apim-Subscription-Key": ocpkey}

    api_url = base_url + f"/api/admin/productgroups/programId/{context.program_id}"

    response = requests.get(api_url, headers=headers)
    response_status_code = response.status_code

    assert response_status_code == 200, f"Get Product Groups list API call failed with status code: '{response_status_code}'."

    response_json = response.json()
    context.product_groups_ids = [item["id"] for item in response_json["items"]]
    return context.product_groups_ids