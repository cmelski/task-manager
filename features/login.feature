Feature: Login to Task Manager
  Tests related to login function

  @smoke
  Scenario: Verify successful login to Task Manager Single User
    Given The user is on landing page single user
    When I log into task manager with user_email and password single user
    Then Successful login result is achieved single user


  Scenario: Verify unsuccessful login to Task Manager
    Given The user is on landing page single user
    When I navigate to the Login Page
    Then Login is rejected when incorrect user_email "user_email" and/or password "password" is entered

  Scenario: Verify successful login to Task Manager by 2 users with own context
    Given The user is on landing page mult context
    When I log into Task Manager with user_email and password mult context
    Then Successful login result is achieved mult context
