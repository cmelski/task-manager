import json
import os

import pytest
from pytest_bdd import given, when, then, parsers, scenarios, scenario

from page_objects.dashboard import DashboardPage
from page_objects.login import LoginPage
import time

# define the path to the feature file
scenarios('features/list.feature')

with open('data/credentials.json') as f:
    test_data = json.load(f)
    user_credentials_list = test_data['user_credentials']
    user_credentials_list[0]['password'] = os.environ.get('PASS')


# define a fixture and update the fixture as you go with data you will need in each function
@pytest.fixture
def shared_data():
    return {}


#use these tags to run a specific scenario when multiple scenarios are in feature file
#terminal pytest -m delete_list
@pytest.mark.delete_list
@scenario('features/list.feature', 'Verify successful deletion of a list')
def test_delete_list():
    pass


@given('The User is on dashboard page')
def user_on_dashboard_page(browser_instance, shared_data):
    state = "auth_state.json" if os.path.exists("auth_state.json") else None
    if state:
        dashboard_page = DashboardPage(browser_instance)
    else:
        login_page = LoginPage(browser_instance)
        dashboard_page = login_page.login(user_credentials_list[0]['user_email'], user_credentials_list[0]['password'])

    shared_data['dashboard_page'] = dashboard_page
    time.sleep(2)


@when('I locate an existing list')
def find_list(shared_data):
    dashboard_page = shared_data['dashboard_page']
    list_index_to_delete = dashboard_page.find_list_to_delete()[0]
    shared_data['list_index_to_delete'] = list_index_to_delete
    list_name_to_delete = dashboard_page.find_list_to_delete()[1]
    print(list_name_to_delete)
    shared_data['list_name_to_delete'] = list_name_to_delete
    time.sleep(2)


@when('Click Delete')
def delete_list(shared_data):
    dashboard_page = shared_data['dashboard_page']
    dashboard_page.delete_list(shared_data['list_index_to_delete'])
    time.sleep(2)


@then('The list is deleted')
def validate_list_deletion(shared_data):
    dashboard_page = shared_data['dashboard_page']
    lists = dashboard_page.validate_list_deletion()
    assert shared_data['list_name_to_delete'] not in lists
    assert  len(lists) == shared_data['list_index_to_delete']

