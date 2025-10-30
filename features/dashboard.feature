Feature: Dashboard functionality in Task Manager
  Tests related to Dashboard function

Scenario: Verify user can logout of the Task Manager
    Given The user is on landing page and logged in
    When Select Logout from the Main Menu
    Then User is logged out of the Task Manager

@smoke
Scenario: Verify user redirected to Login Page if trying to add a new list while logged out
    Given The user is on dashboard page and logged out
    When I try to Add a new list
    Then I am redirected to the Login Page