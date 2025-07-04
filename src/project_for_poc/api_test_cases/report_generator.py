"""
- does not have the charts

"""
import json
import argparse
import os
import re

parser = argparse.ArgumentParser()
parser.add_argument('--input_json_file',
                    required=True,
                    help="Path of input json file. JSON file is output of Behave test run")
parser.add_argument('--output_html_file',
                    required=True,
                    help="Path of the output html file to be generated")

args = parser.parse_args()

input_file = args.input_json_file
output_html_path = args.output_html_file


feature_count = 0
feature_failed_count = 0
feature_passed_count = 0
scenario_count = 0
scenario_failed_count = 0
scenario_passed_count = 0

all_rows = ""
feature_row_template = '''<tr class="feature">
                            <td class="feature_td">{fe_name}</td>
                            <td class="status" style="background: {feature_status_background};">{fe_status}</td>
                        </tr>'''

scenario_row_template = '''<tr class="scenario" scenario_name="{sce_name}" onClick="{on_click}">    
                                <td class="scenario_td">{sce_name}</td>
                                <td class="status" style="color: {sc_status_color}; font-weight: {sc_status_font_weight}">{sce_status}</td>
                            </tr>'''

error_row_template = '''<tr class="error_row" scenario_name="{sce_name}" style="background: #ffaaaa; display: none;">
                            <td class="err_sc_name scenario_td">{step_name}</td>
                            <td class="error_message">{err}</td>
                        </tr>'''

report_styles = """
    <style>
        tr.feature {
            background: #e1e3e1;
        }
        td.scenario_td {
            width:50%;
        }

        td.status {
            width: 10%;
        }

        td.err_sc_name {
            max-width: 100%;
        }

        td.feature_td {
            min-width:50;
        }

        # td.error_message {
        #     white-space: pre-wrap;
        # }

        table, th, td {
            border: 1px solid #1a7ade;
        }
    </style>
"""

report_javascript = """
    <script>
        function justalert(sc_name){
            var locator = 'tr.error_row[scenario_name="' + sc_name + '"]'
            var errRow = document.querySelector(locator)
            
            if ( errRow.style.display == "block") {
                errRow.style.display = "none";
            } else {
                errRow.style.display = "block";
            }
        }
    </script>
"""

# read the report json file
with open(input_file) as f:
    temp_file = f.read()
    if 'PYCHARM_HOSTED' in os.environ:
        reports = json.loads(temp_file)
    else:
        temp_file = temp_file + ']'
        reports = json.loads(temp_file)

def calcuate_percent_passed():
    global scenario_failed_count
    global scenario_passed_count
    global scenario_count

    total_scenarios = scenario_failed_count + scenario_passed_count
    if total_scenarios != scenario_count:
        raise Exception("Number of total scenario count and failed + passed does not match.")
    try:
        pct_pass = round((scenario_passed_count/total_scenarios) * 100, 2)
    except ZeroDivisionError:
        pct_pass = 100

    return pct_pass

for report in reports:
    # verify each dictionary in the list is a feature
    _type = report['keyword']
    if _type == 'Feature':
        feature = report
    else:
        raise Exception("Unexpected top level keyword '{}'. Only expected 'Feature'".format(_type))

    # update the count of features passed/failed
    if feature['status'] == 'passed':
      feature_passed_count += 1
      feature_status_background = '#a5f1a5'
    elif feature['status'] == 'failed':
      feature_failed_count += 1
      feature_status_background = '#ffaaaa'

    else:
      raise Exception("Unexpected status for feature. Expected 'passed' or 'failed' but found '{}'".format(feature['status']))

    # add the feature as one row in the html table
    all_rows = all_rows + feature_row_template.format(fe_name=feature['name'], fe_status=feature['status'], feature_status_background=feature_status_background)
    feature_count += 1

    scenarios = feature['elements']
    for s in scenarios:
        s_type = s['type']
        if s_type == 'scenario':
            scenario = s
        else:
            raise Exception("Unexpected 'type' in list of elements for feature. Expected 'scenario' but found '{}'".format(s_type))

        scenario_name = scenario['name'].strip()
        if scenario['status'] == 'passed':
          scenario_passed_count += 1
          scenario_count += 1
          on_click = 'na'
          sc_status_color = '#1c881c'
          sc_status_font_weight = 'none'
        elif scenario['status'] == 'failed':
          scenario_failed_count += 1
          scenario_count += 1
          on_click = "justalert('{}')".format(scenario_name)
          sc_status_color = 'red'
          sc_status_font_weight = 'bold'

        else:
            raise Exception("Unexpected 'status' for scenario. Expected 'passed' or 'failed'. Actual: {}. Scenario name: {}".format(scenario['status'], scenario_name))

        # add the scenario row
        all_rows = all_rows + scenario_row_template.format(on_click=on_click, sce_name=scenario_name, sce_status=scenario['status'].upper(),
                                                           sc_status_color=sc_status_color, sc_status_font_weight=sc_status_font_weight)

        # for the failed scenario the error needs to be added to the report so identify the step that failed and add the error
        error_row_template = '''<tr class="error_row" scenario_name="{sce_name}" style="background: #ffaaaa; display: none;">
                                    <td class="err_sc_name scenario_td">{step_name}</td>
                                    <td class="error_message">{err}</td>
                                </tr>'''

        # ...

        # Inside the loop where you populate the error_row_template:
        for scenario in scenarios:
            # ...

            if scenario['status'] == 'failed':
                steps = scenario['steps']

                for step in steps:
                    try:
                        if step['result']['status'] == 'failed':
                            failed_step = step
                            break
                    except:
                        pass
                else:
                    raise Exception(
                        "There should be a failed step but none found in list of steps for scenario. Scenario name: {}".format(
                            scenario_name))

                # handle single-line and multi-line messages differently
                error_message = '<br>'.join(failed_step['result']['error_message'])
                if '\n' not in error_message:
                    # Handle single-line messages without adding spaces
                    error_message = error_message.replace('<br>', '')

                # add the error detail row
                all_rows = all_rows + error_row_template.format(
                    sce_name=scenario_name,
                    step_name=failed_step['keyword'] + ":" + failed_step['name'],
                    err=error_message
                )

# Build the report summary
percent_passed = calcuate_percent_passed()

report_html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    {report_styles}
    <title>My Test Report</title>
</head>
<body>
<div id="test_summary">
         <h1> Scenario Pass Rate: {percent_passed}% ({scenario_passed_count}/{(scenario_failed_count + scenario_passed_count)})</h1>
<table class="table-summary">
    <thead><th></th><th>PASSED</th><th>FAILED</th><th>PASS RATE</th></thead>
    <tbody>
        <tr>
            <th>Features</th><td style="color:green"><center>{feature_passed_count}</center></td>
            <td style="color:red"><center>{feature_failed_count}</center></td>
            <td><center>{round(feature_passed_count /(scenario_failed_count + feature_passed_count), 2) * 100} %</center></td>
        </tr>
        <tr>
            <th>Scenario</th><td style="color:green"><center>{scenario_passed_count}</center></td>
            <td style="color:red"><center>{scenario_failed_count}</center></td>
            <td><center>{round(scenario_passed_count/(scenario_failed_count + scenario_passed_count), 2) * 100} %</center></td>
        </tr>
    </tbody>
</table>
</div>
<br>
<table>
    <thead></thead>
    <tbody>
    {all_rows}
    </tbody>

</table>
{report_javascript}
</body>
</html>"""



# reate the final report html
with open(output_html_path, 'w') as f:
  f.write(report_html_template)

print("***************************")
print("Feature count: {}".format(feature_count))
print("feature_failed_count: {}".format(feature_failed_count))
print("feature_passed_count: {}".format(feature_passed_count))
print("scenario_count: {}".format(scenario_count))
print("scenario_failed_count: {}".format(scenario_failed_count))
print("scenario_failed_count: {}".format(scenario_failed_count))
print("Output html: {}".format(output_html_path))
print("***************************")