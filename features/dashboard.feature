Feature: Dashboard functionality in Task Manager
  Tests related to Dashboard function

Scenario: Verify user can logout of the Task Manager
    Given The user is on landing page and logged in
    When Select Logout from the Main Menu
    Then User is logged out of the Task Manager