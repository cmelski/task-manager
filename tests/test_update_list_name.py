import pytest
from pytest_bdd import given, when, then, scenario
from tests.conftest import logger
from page_objects.dashboard import DashboardPage
import time

# define the path to the feature file
#scenarios('features/list.feature')

#use these tags to run a specific scenario when multiple scenarios are in feature file
#terminal pytest -m delete_list
@pytest.mark.update_list_name
@scenario('../features/list.feature', 'Verify list name can be updated')
def test_update_list_name(set_auth_state):
    pass

# define a fixture and update the fixture as you go with data you will need in each function
@pytest.fixture
def shared_data():
    return {}


@given('The User is on dashboard page')
def user_on_dashboard_page(browser_instance, shared_data):
    #state = "auth_state_test.json" if os.path.exists("auth_state_test.json") else None
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

@when('Change the list name and click Enter')
def update_list_name(shared_data):
    list_page = shared_data['list_page']
    updated_list = list_page.update_list_name()
    shared_data['updated_list'] = updated_list


@then('The list name is successfully updated')
def validate_list_name_update(shared_data):
    list_page = shared_data['list_page']
    lists = list_page.validate_list()[0]
    updated_list_name = list_page.validate_list()[1]
    old_list_name = shared_data['updated_list'][0]
    assert updated_list_name in lists
    assert updated_list_name == shared_data['updated_list'][1]
    assert old_list_name not in lists

    logger.info(f'List {old_list_name} updated to {updated_list_name} successfully!')