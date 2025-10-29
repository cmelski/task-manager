Feature: Resister to use Task Manager
  Tests related to Register function

  Scenario: Verify successful user registration to Task Manager
    Given The new user is on landing page
    When Navigate to Register page
    And Enter registration details and click Submit
    Then Successful registration is achieved