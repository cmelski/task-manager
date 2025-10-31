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


# method to mock the api response
def intercept_response(route):
    route.fulfill(
        empty_list=[]
    )


# define the path to the feature file
#scenarios('features/list.feature')

#use these tags to run a specific scenario when multiple scenarios are in feature file
#terminal pytest -m delete_list
@pytest.mark.outstanding_tasks_report_none_outstanding
@scenario('../features/report.feature', 'Verify no outstanding tasks in the Outstanding Tasks report')
def test_outstanding_tasks_report_none_outstanding(set_auth_state):
    pass



@given('The user is on landing page and logged in')
def user_on_dashboard_page(browser_instance, shared_data):
    #state = "auth_state.json" if os.path.exists("auth_state.json") else None
    #if state:
    dashboard_page = DashboardPage(browser_instance)
    #else:
     #   login_page = LoginPage(browser_instance)
      #  dashboard_page = login_page.login(user_credentials_list[0]['user_email'],user_credentials_list[0]['password'])

    shared_data['dashboard_page'] = dashboard_page
    time.sleep(2)


@when('Navigate to Outstanding Tasks report')
def click_outstanding_tasks_report(shared_data):
    dashboard_page = shared_data['dashboard_page']
    report_page = dashboard_page.select_outstanding_tasks(intercept_response)
    shared_data['report_page'] = report_page
    time.sleep(2)


@then('No outstanding tasks message is displayed')
def validate_no_outstanding_tasks_message(shared_data):
    pass
