Feature: Reporting in the Task Manager
  Tests related to reporting function

  Scenario: Verify no outstanding tasks in the Outstanding Tasks report
    Given The user is on landing page and logged in
    When Navigate to Outstanding Tasks report
    Then No outstanding tasks message is displayed

  Scenario: Verify Tasks by Assignee report
    Given The user is on landing page and logged in
    When Navigate to Tasks by Assignee report
    Then Tasks by Assignee report is displayed and correctly shows tasks for the user that are not completed