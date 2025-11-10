from datetime import date, timedelta

import pytest
from pytest_bdd import given, when, then, scenario, parsers
from tests.conftest import logger
from page_objects.dashboard import DashboardPage
import time


# use these tags to run a specific scenario when multiple scenarios are in feature file
# terminal pytest -m delete_list
@pytest.mark.clone_list
@scenario('../features/list.feature', 'Verify successful list cloning')
def test_clone_list(set_auth_state):
    pass


# define a fixture and update the fixture as you go with data you will need in each function
@pytest.fixture
def shared_data():
    return {}


@given('The User is on dashboard page')
def user_on_dashboard_page(browser_instance, shared_data):
    # state = "auth_state_test.json" if os.path.exists("auth_state_test.json") else None
    # if state:
    dashboard_page = DashboardPage(browser_instance)
    # else:
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


@when('Click Clone')
def clone_list_item(shared_data):
    list_page = shared_data['list_page']
    clone_details = list_page.select_clone()
    shared_data['clone_details'] = clone_details


@then('The list is cloned')
def validate_list_cloning(shared_data):
    clone_details = shared_data['clone_details']
    logger.info(clone_details)

    assert 'Clone' in clone_details[1]
    assert clone_details[0] in clone_details[1]

    if len(clone_details[2]) > 0:
        for i in range(0, len(clone_details[2])):
            if clone_details[2][i] is True or clone_details[2][i] is False:
                assert clone_details[3][i] == False
            else:
                assert clone_details[2][i] == clone_details[3][i]

