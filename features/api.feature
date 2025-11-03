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