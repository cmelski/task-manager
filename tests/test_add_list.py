import json
import os
import pytest
from pytest_bdd import given, when, then, parsers, scenarios, scenario
from page_objects.dashboard import DashboardPage
import time

from tests.conftest import logger


# define a fixture and update the fixture as you go with data you will need in each function
@pytest.fixture
def shared_data():
    return {}


# define the path to the feature file
#scenarios('features/list.feature')

#use these tags to run a specific scenario when multiple scenarios are in feature file
#terminal pytest -m delete_list
@pytest.mark.add_list
@scenario('../features/list.feature', 'Verify successful adding of a new list to Task Manager')
def test_add_list(set_auth_state):
    pass



@given('The user is on dashboard page')
def user_on_dashboard_page(browser_instance, shared_data):
    #state = "auth_state.json" if os.path.exists("auth_state.json") else None
    #if state:
    dashboard_page = DashboardPage(browser_instance)
    #else:
     #   login_page = LoginPage(browser_instance)
      #  dashboard_page = login_page.login(user_credentials_list[0]['user_email'],user_credentials_list[0]['password'])

    shared_data['dashboard_page'] = dashboard_page
    time.sleep(2)


@when('I click on add list')
def click_new_list(shared_data):
    dashboard_page = shared_data['dashboard_page']
    list_page = dashboard_page.add_new_list()
    shared_data['list_page'] = list_page
    time.sleep(2)

@when('Enter a list name')
def add_list_name(shared_data):
    list_page = shared_data['list_page']
    list_page.enter_list_name()
    time.sleep(2)


@then('A new list is created')
def validate_new_list(shared_data):
    list_page = shared_data['list_page']
    lists = list_page.validate_list()[0]
    list_name = list_page.validate_list()[1]
    assert list_name in lists
    logger.info(f'New List {list_name} added successfully!')


@pytest.mark.add_list_redirect
@scenario('../features/dashboard.feature', 'Verify user redirected to Login Page if trying to add a new list while logged out')
def test_add_list_redirect(clean_auth_state_before_login):
    pass



@given('The user is on dashboard page and logged out')
def user_on_dashboard_page(browser_instance, shared_data):
    #state = "auth_state.json" if os.path.exists("auth_state.json") else None
    #if state:
    dashboard_page = DashboardPage(browser_instance)
    #else:
     #   login_page = LoginPage(browser_instance)
      #  dashboard_page = login_page.login(user_credentials_list[0]['user_email'],user_credentials_list[0]['password'])

    shared_data['dashboard_page'] = dashboard_page
    time.sleep(2)


@when('I try to Add a new list')
def click_new_list(shared_data):
    dashboard_page = shared_data['dashboard_page']
    login_page = dashboard_page.add_new_list()
    shared_data['login_page'] = login_page
    time.sleep(2)

@then('I am redirected to the Login Page')
def login_redirect(shared_data):
    login_page = shared_data['login_page']
    login_page.validate_on_login_page()


