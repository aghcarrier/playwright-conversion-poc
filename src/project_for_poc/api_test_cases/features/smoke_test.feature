@smoke

Feature: Create a new users and login to CSS
  Scenario: Create a new user and verify successful login to CSS
    Given I login to CSS as a siteadmin
    And I create a new user
    And I logout
    When I login as new user
    Then I see home page