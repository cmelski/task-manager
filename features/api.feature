Feature: API Tests in the Task Manager
  Tests related to Task Manager API function

  Scenario: GET lists for logged in user
    Given The user is logged in and on the Dashboard page
    When The get user lists API GET request is made
    Then The lists belonging to the user are retrieved and match the Dashboard

  Scenario: Add list via API
    Given The user is logged in and on the Dashboard page
    When The add list API POST request is made and page is reloaded
    Then The list added via the API is displayed on the Dashboard

  Scenario: GET lists mock for no lists for logged in user
    Given The user is logged in and on the Dashboard page
    When The get user lists mock API API response is triggered
    Then The user does not have any lists message is received from the API

  Scenario: Log in via API
    Given The user logs in via API
    When The API response token is received
    Then The user bypasses the login screen

