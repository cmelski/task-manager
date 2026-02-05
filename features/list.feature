Feature: List functionality in Task Manager
  Tests related to List function

  @smoke
  Scenario: Verify successful adding of a new list to Task Manager
    Given The user is on dashboard page
    When I click on add list
    And Enter a list name
    Then A new list is created


  Scenario: Verify successful deletion of a list
    Given The User is on dashboard page
    When I locate an existing list
    And Click Delete
    Then The list is deleted

  @smoke
  Scenario: Verify list name can be updated
    Given The User is on dashboard page
    When I locate and click an existing list
    And Change the list name and click Enter
    Then The list name is successfully updated

  @smoke
  Scenario: Verify successful list item creation
    Given The User is on dashboard page
    When I locate and click an existing list
    And Add a list item
    Then The list item is created

  Scenario: Verify successful list item deletion
    Given The User is on dashboard page
    When I locate and click an existing list
    And Click delete on a list item
    Then The list item is deleted

  Scenario Outline: Verify successful list item modification
    Given The User is on dashboard page
    When I locate and click an existing list
    And Amend a list item task_name "<task_name>", assignee "<assignee>", notes "<notes>", complete "<complete>" and click Save
    Then The list item is updated
    Examples:
      | task_name            |assignee  | notes | complete
      | updated task name    | Karen      | updated notes | False

  Scenario: Verify successful list cloning
    Given The User is on dashboard page
    When I locate and click an existing list
    And Click Clone
    Then The list is cloned

  Scenario: Verify successful csv upload
    Given The User is on dashboard page
    When I create a new list and view the list details
    And Upload a csv template of tasks
    Then The upload is successful

  Scenario: Verify duplicate tasks message
    Given The User is on dashboard page
    When I create a new list and view the list details
    And Upload the same csv template of tasks twice
    Then Duplicate tasks message is displayed
