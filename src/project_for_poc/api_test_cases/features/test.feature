@smoke

Feature: Create a new users and login to CSS
  Scenario: Create a new user and verify successful login to CSS
    Given I get the URL
    When I do a call
    Then I verify the response code
    Then I print the response