Feature: Resister to use Task Manager
  Tests related to Register function

  @smoke
  Scenario: Verify successful user registration to Task Manager
    Given The new user is on landing page
    When Navigate to Register page
    And Enter registration details and click Submit
    Then Successful registration is achieved

  Scenario Outline: Verify unsuccessful user registration to Task Manager
    Given The new user is on landing page
    When Navigate to Register page
    And Enter invalid email "<email>", password "<password>", name "<name>"
    Then Registration is not permitted
    Examples:
      | email              | password      | name |
      | ""                 | ""            | ""   |
      | test27@yahoo.com   | ""            | ""   |
      | test28@hotmail.com | test_password | ""   |

  Scenario: Verify user is redirected to login page if they are already registered
    Given The user is on landing page
    When Navigate to Register page
    And Enter an email that is already registered along with a password and name
    Then User is redirected to the Login page