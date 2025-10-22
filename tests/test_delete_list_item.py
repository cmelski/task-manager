import pytest
from pytest_bdd import given, when, then, scenario
from page_objects.dashboard import DashboardPage
import time


# define the path to the feature file
# scenarios('features/list.feature')

# use these tags to run a specific scenario when multiple scenarios are in feature file
# terminal pytest -m delete_list
@pytest.mark.delete_list_item
@scenario('../features/list.feature', 'Verify successful list item deletion')
def test_delete_list_item(set_auth_state):
    pass


# define a fixture and update the fixture as you go with data you will need in each function
@pytest.fixture
def shared_data():
    return {}


@given('The User is on dashboard page')
def user_on_dashboard_page(browser_instance, shared_data):
    # state = "auth_state.json" if os.path.exists("auth_state.json") else None
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


@when('Click delete on a list item')
def delete_list_name(shared_data):
    list_page = shared_data['list_page']
    list_item_to_delete = list_page.delete_list_item()
    shared_data['list_item_to_delete'] = list_item_to_delete


@then('The list item is deleted')
def validate_new_list(shared_data):
    list_item_to_delete = shared_data['list_item_to_delete']
    assert list_item_to_delete[1] < list_item_to_delete[0]
