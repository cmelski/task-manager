Feature: Login to Task Manager
  Tests related to login function

  Scenario Outline: Verify successful login to Task Manager
    Given The user is on landing page
    When I log into Task Manager with <user_email> and <password>
    Then Successful login result is achieved
    Examples:
      | user_email            | password    |
      | c_melski@yahoo.com    | render2011$ |

  Scenario Outline: Verify unsuccessful login to Task Manager
    Given The user is on landing page
    When I log into Task Manager using wrong password with <user_email> and <password>
    Then Unsuccessful login result is achieved
    Examples:
      | user_email            | password    |
      | c_melski@yahoo.com    | render2011 |