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
@pytest.mark.tasks_by_assignee_report
@scenario('../features/report.feature', 'Verify Tasks by Assignee report')
def test_tasks_by_assignee_report(set_auth_state):
    pass



@given('The user is on landing page and logged in')
def user_on_dashboard_page(browser_instance, shared_data):

    dashboard_page = DashboardPage(browser_instance)
    shared_data['dashboard_page'] = dashboard_page
    time.sleep(2)


@when('Navigate to Tasks by Assignee report')
def click_tasks_by_assignee_report(shared_data):
    dashboard_page = shared_data['dashboard_page']
    report_page = dashboard_page.select_tasks_by_assignee_report()
    shared_data['report_page'] = report_page
    time.sleep(2)


@then('Tasks by Assignee report is displayed and correctly shows tasks for the user that are not completed')
def validate_tasks_by_assignee_report(shared_data):
    report_page = shared_data['report_page']
    report_page.verify_tasks_by_assignee_report()
