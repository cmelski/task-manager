Feature: Login to Task Manager
  Tests related to login function

  Scenario Outline: Verify successful login to Task Manager
    Given The user is on landing page
    When I log into Task Manager with user_email "<user_email>" and password "<password>"
    Then Successful login result is achieved
    Examples:
      | user_email            | password    |
      | user_email            | password |

  Scenario: Verify unsuccessful login to Task Manager
    Given The user is on landing page
    When I navigate to the Login Page
    Then Login is rejected when incorrect user_email "user_email" and/or password "password" is entered
