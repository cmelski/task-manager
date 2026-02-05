import csv
import os

import pytest
from pytest_bdd import given, when, then, scenario, parsers
from tests.conftest import logger
from page_objects.dashboard import DashboardPage
import time


# use these tags to run a specific scenario when multiple scenarios are in feature file
# terminal pytest -m delete_list
@pytest.mark.csv_upload
@scenario('../features/list.feature', 'Verify successful csv upload')
def test_csv_upload(set_auth_state):
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


@when('I create a new list and view the list details')
def add_list_and_view(shared_data):
    dashboard_page = shared_data['dashboard_page']
    list_page = dashboard_page.add_new_list()
    list_page.enter_list_name()
    shared_data['list_page'] = list_page
    time.sleep(2)


@when('Upload a csv template of tasks')
def upload_csv_file(shared_data):
    list_page = shared_data['list_page']
    uploaded_tasks = list_page.upload_csv()
    shared_data['uploaded_tasks'] = uploaded_tasks
    time.sleep(2)


@then('The upload is successful')
def validate_csv_upload(shared_data):
    csv_path = os.path.abspath("data/test_csv.csv")

    uploaded_tasks = shared_data['uploaded_tasks']
    logger.info(uploaded_tasks)
    start_index = 0
    end_index = 5
    with open(csv_path, mode='r') as file:
        csvFile = csv.reader(file)
        # skip header row
        next(csvFile)
        for lines in csvFile:
            logger.info(lines)
            for i in range(len(lines)):
                if lines[i] == 'true':
                    assert uploaded_tasks[start_index:end_index][i]
                elif lines[i] == 'false':
                    assert uploaded_tasks[start_index:end_index][i] is False
                else:
                    assert lines[i] == uploaded_tasks[start_index:end_index][i]
            start_index += 5
            end_index += 5


@pytest.mark.csv_upload_duplicate_tasks
@scenario('../features/list.feature', 'Verify duplicate tasks message')
def test_csv_upload_duplicate_tasks(set_auth_state):
    pass


@given('The User is on dashboard page')
def user_on_dashboard_page(browser_instance, shared_data):
    dashboard_page = DashboardPage(browser_instance)
    shared_data['dashboard_page'] = dashboard_page
    time.sleep(2)


@when('I create a new list and view the list details')
def add_list_and_view(shared_data):
    dashboard_page = shared_data['dashboard_page']
    list_page = dashboard_page.add_new_list()
    list_page.enter_list_name()
    shared_data['list_page'] = list_page
    time.sleep(2)


@when('Upload the same csv template of tasks twice')
def upload_csv_file(shared_data):
    list_page = shared_data['list_page']
    list_page.upload_csv()
    time.sleep(2)
    list_page.upload_csv()
    time.sleep(2)



@then('Duplicate tasks message is displayed')
def validate_duplicate_tasks_message(shared_data):
    list_page = shared_data['list_page']
    list_page.validate_duplicate_tasks()

