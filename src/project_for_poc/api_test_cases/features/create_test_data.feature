@smoke @create_test_data

Feature: Create test data for automation
  Scenario: Create basic Test Data
    Given I create access token for "sensitech_admin"
    When I create a new program if it does not exist
    Then I create a new "Origin" type Location Group with name the "Origin Group"
    Then I create a new "Stop" type Location Group with name the "Stops Group"
    Then I create a new "Stop" type Location Group with name the "Final Destination Group"
    Then I create a new Product with the name "DryIce"
    Then I create a new Product with the name "Fruits"
    Then I create a new Product Group with the name "All Products" and add all products
    Then I create a new Zone Spec with the name "Frozen Zone"
    Then I create a new Zone Spec with the name "Vegetable Zone"
    Then I create a new Container with the name "Container With One Zone" and "Frozen zone" zone spec
    Then I create a new Zone Spec with the name "Refrigerated"
    Then I create a new Container with the name "Container With Two Zone" and zone specs "Frozen Zone" and "Refrigerated"
    Then I create a new Container Group with the name "All Containers" and add all containers
    Then I create a new Automation Outbound Rule for Trips(or update if it exist) with "All Containers" container group and the name "Outbound Automation Rule"
    Then I create a new User Group with the name "User Group Created by Automation"
    Then I create a new notification with the name "Departed the Origin" using "Location-Departure" template
    Then I create a new event to "Update Trip Status" with following variables
      | event_name                    | event_severity_name | condition_name  | action_status | action_reason | email_notification_name |
      | Event for Departed the Origin | Information         | Departed Origin | In Transit    | Location      | Departed the Origin     |
    Then I create a new notification with the name "Arrived at Final Destination" using "Location-Arrival at final destination" template
    Then I create a new event to "Update Trip Status" with following variables
      | event_name                             | event_severity_name | condition_name               | action_status | action_reason | email_notification_name      |
      | Event for Arrived at Final Destination | Information         | Arrived at Final Destination | Arrived       | Location      | Arrived at Final Destination |
    Then I create a new notification with the name "Start Trip with First Device Message" using "Started Status" template
    Then I create a new event to "Update Trip Status" with following variables
      | event_name                               | event_severity_name | condition_name       | action_status | action_reason | email_notification_name              |
      | Start the Trip with First Device Message | Information         | First Device Message | Started       |               | Start Trip with First Device Message |
    Then I create a new notification with the name "Notification for Alarmed Product" using "Alarm–Product" template
    Then I create a new email notification event with following variables
      | event_name                | event_severity_name | event_category_name | condition_name | email_notification_name          |
      | Event for Alarmed Product | Critical            | Alarm - Product     | Has hit alarm  | Notification for Alarmed Product |
    Then I create a new notification with the name "Notification for Alarmed Container" using "Alarm–Container" template
    Then I create a new email notification event with following variables
      | event_name                  | event_severity_name | event_category_name | condition_name | email_notification_name            |
      | Event for Alarmed Container | Critical            | Alarm - Container   | Has hit alarm  | Notification for Alarmed Container |