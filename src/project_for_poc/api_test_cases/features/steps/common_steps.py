from behave import given
from steps.APICommon.APICommonFuncs import common_funcs
import requests
import json
from steps.storage import base_url
from steps.storage import token


@given('I create access token for "{user}"')
def create_access_token(context, user):

    base_url = context.base_url
    authorization = context.authorization
    ocpkey = context.ocpkey

    test_id = context.environment.lower() + "_" + user.lower()

    context.user_name = common_funcs.get_test_data_from_file(context, "../test_data/", "users.csv", test_id, "user_name")
    password = common_funcs.get_test_data_from_file(context, "../test_data/", "users.csv", test_id, "password")

    api_url = base_url + "/api/auth/connect/token"
    context.request_parameters = {"grant_type": "password",
                                  "scope": "rtweb.api",
                                  "username": context.user_name,
                                  "password": password }
    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "Authorization": authorization,
               "Ocp-Apim-Subscription-Key": ocpkey}
    response = requests.post(api_url, data=context.request_parameters, headers=headers)
    context.response = response
    assert context.response.status_code == 200, f"Expected status code 200, but got '{context.response.status_code}'."
    response_data = json.loads(context.response.text)
    context.token = "Bearer " + response_data["access_token"]

    # Following steps are for storing token and base_url then accessing them in other python files
    #    * token.set_token(context.authorization)
    #    * base_url.set_base_url(base_url)
    # Token and base_url can be retrieved in other python files:
    #    * from storage import token
    #    * from storage import base_url
    #    * token.get_token()
    #    * base_url.get_base_url()