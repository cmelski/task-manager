Feature: List functionality in Task Manager
  Tests related to List function


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
