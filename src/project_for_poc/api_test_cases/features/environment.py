import os
import pyodbc
import requests
from steps import programs_steps, common_steps
from steps import programs_steps
from steps.APICommon.APICommonFuncs import common_funcs
import sys
from datetime import datetime
import configparser
import time


def before_all(context):
    # Retrieve the environment and program names from behave.ini
    context.environment = context.config.userdata.get("test.environment")
    context.program_name = context.config.userdata.get("test.program")
    # Retrieve base_url, authorization, ocpkey and output_address from environment_details.csv
    test_id = context.environment
    context.base_url = common_funcs.get_test_data_from_file(context, "../test_data/",
                                                "environment_details.csv", test_id, "base_url")
    context.authorization = common_funcs.get_test_data_from_file(context, "../test_data/",
                                                "environment_details.csv", test_id, "authorization")
    context.ocpkey = common_funcs.get_test_data_from_file(context, "../test_data/",
                                                "environment_details.csv", test_id, "ocpkey")
    context.output_address = common_funcs.get_test_data_from_file(context, "../test_data/",
                                                "environment_details.csv", test_id, "output_address")

    """
    #=====================================================================
    # Get ProgramId from DB
    #=====================================================================
    """
    # server_name = f"tcp:swp-{context.environment}-server-sql.database.windows.net,1433"
    # database_name = "RealTime.Admin"
    # username = "sqladmin"
    # password = "UTWv0Z9Xr7"
    #
    # connection_string = f"DRIVER={{SQL Server}};SERVER={server_name};DATABASE={database_name};UID={username};PWD={password}"
    #
    # try:
    #     connection = pyodbc.connect(connection_string)
    #     # print("Connected to the SQL Server database.")
    # except pyodbc.Error as ex:
    #     print(f"Error connecting to the database: {ex}")
    #
    # cursor = connection.cursor()
    # query = "SELECT Id FROM [dbo].[Program] WHERE Name = ?"
    # cursor.execute(query, context.program_name)
    #
    # # Fetch the results
    # row = cursor.fetchone()
    #
    # # Check if the row is not None
    # if row:
    #     # Access ProgramId by index
    #     context.program_id = row[0]
    # # print(f"programId: {context.program_id}")
    #
    # connection.close()

    """
    #=====================================================================
    # Get ProgramId by API call
    #=====================================================================
    """

    common_steps.create_access_token(context, "sensitech_admin")
    context.program_id = programs_steps.get_program_id_by_program_name(context, context.program_name)
    if context.program_id is None:
        programs_steps.create_new_program_if_does_not_exist(context)

    # context.program_id = 2102  # QA2 test4

# def after_all(context):
#
#     # print("Current Working Directory:", os.getcwd())
#     # # Uncomment following two lines for custom report. Note: Also Uncomment code in behave.ini file for Custom report.
#     # os.system("python ../report_generator.py --input_json_file ../test_results/behave.reports/api_behave_report.json "
#     #           "--output_html_file ../test_results/output.html")
#     # Following two lines are for Allure report.
#     command = f"allure serve ../test_results_allure/junit-results"
#     os.system(command)