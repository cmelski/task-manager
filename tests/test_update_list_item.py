from datetime import date, timedelta

import pytest
from pytest_bdd import given, when, then, scenario, parsers
from tests.conftest import logger
from page_objects.dashboard import DashboardPage
import time

# define the path to the feature file
#scenarios('features/list.feature')

#use these tags to run a specific scenario when multiple scenarios are in feature file
#terminal pytest -m delete_list
@pytest.mark.update_list_item
@scenario('../features/list.feature', 'Verify successful list item modification')
def test_update_list_item(set_auth_state):
    pass

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

@when(parsers.cfparse(
    'Amend a list item task_name "{task_name}", assignee "{assignee}", notes "{notes}", '
    'complete "{complete}" and click Save'
))
def update_list_item(shared_data, task_name, assignee, notes, complete):
    is_complete = complete.lower() == "true"
    list_page = shared_data['list_page']
    due_date = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    update_details = [task_name, due_date, assignee, notes, is_complete]
    updated_list_item = list_page.update_list_item(update_details)
    shared_data['updated_list_item'] = [updated_list_item,update_details]


@then('The list item is updated')
def validate_list_item_update(shared_data):
    item_to_update = shared_data['updated_list_item'][0][0]
    update_details = shared_data['updated_list_item'][1]
    item_after_update = shared_data['updated_list_item'][0][1]
    logger.info(f'Item to update: {item_to_update}')
    logger.info(f'Update Details: {update_details}')
    logger.info(f'Item after update: {item_after_update}')

    for i in range(0,len(update_details)):
        assert update_details[i] == item_after_update[i]
