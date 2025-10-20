import json
import os
import pytest
from pytest_bdd import given, when, then, parsers, scenarios, scenario

from conftest import logger
from page_objects.dashboard import DashboardPage
from page_objects.login import LoginPage
import time

# define the path to the feature file
#scenarios('features/list.feature')

#use these tags to run a specific scenario when multiple scenarios are in feature file
#terminal pytest -m delete_list
@pytest.mark.add_list_item
@scenario('features/list.feature', 'Verify successful list item creation')
def test_add_list_item(set_auth_state):
    pass

with open('data/credentials.json') as f:
    test_data = json.load(f)
    user_credentials_list = test_data['user_credentials']
    user_credentials_list[0]['password'] = os.environ.get('PASS')

# define a fixture and update the fixture as you go with data you will need in each function
@pytest.fixture
def shared_data():
    return {}


@given('The User is on dashboard page')
def user_on_dashboard_page(browser_instance, shared_data):
    #state = "auth_state.json" if os.path.exists("auth_state.json") else None
    #if state:
    dashboard_page = DashboardPage(browser_instance)
    #else:
     #   login_page = LoginPage(browser_instance)
      #  dashboard_page = login_page.login(user_credentials_list[0]['user_email'],user_credentials_list[0]['password'])

    shared_data['dashboard_page'] = dashboard_page
    time.sleep(2)



@when('I locate and click an existing list')
def select_existing_list(shared_data):
    dashboard_page = shared_data['dashboard_page']
    list_page = dashboard_page.select_existing_list()
    shared_data['list_page'] = list_page
    time.sleep(2)

@when('Add a list item')
def add_list_name(shared_data):
    list_page = shared_data['list_page']
    list_item = list_page.add_list_item()
    shared_data['list_item'] = list_item



@then('The list item is created')
def validate_new_list(shared_data):
    list_page = shared_data['list_page']
    list_item = shared_data['list_item']
    last_item = list_page.validate_new_item()
    logger.info(list_item)

    for i in range(0,len(list_item[0])):
        assert list_item[0][i] == last_item[0][i]