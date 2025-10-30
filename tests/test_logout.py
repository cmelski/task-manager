import json
import os

import pytest
from pytest_bdd import given, when, then, parsers, scenario

import utils.db_connect as db_connect
from dao.user_dao import User_DAO
from tests.conftest import logger
from page_objects.dashboard import DashboardPage

@pytest.fixture()
def shared_data():
    return {}


# use these tags to run a specific scenario when multiple scenarios are in feature file
# terminal pytest -m delete_list
# feature file path is relative to the directory where the test resides (e.g. in this case test is in 'tests' folder
# under the project root)
@pytest.mark.logout
@scenario('../features/dashboard.feature', 'Verify user can logout of the Task Manager')
def test_logout(clean_auth_state_before_login):
    pass


@given('The user is on landing page and logged in')
def new_user_on_landing_page(browser_instance, shared_data):
    dashboard_page = DashboardPage(browser_instance)
    login_page = dashboard_page.navigate_to_login_page()
    email = os.environ.get('USER_EMAIL')
    password = os.environ.get('PASS')
    dashboard_page = login_page.login(email, password)
    shared_data['dashboard_page'] = dashboard_page

@when('Select Logout from the Main Menu')
def select_logout(shared_data):
    dashboard_page = shared_data['dashboard_page']
    dashboard_page.logout()

@then('User is logged out of the Task Manager')
def validate_logout(shared_data):
    dashboard_page = shared_data['dashboard_page']
    logged_out = dashboard_page.verify_logout()
    assert logged_out == True


