import json
import os
import pytest

from pytest_bdd import given, when, then, parsers, scenarios, scenario
from page_objects.dashboard import DashboardPage
import time
from dao.user_dao import User_DAO
from helpers.api_helper import APIHelper
from tests.conftest import logger
from utils import db_connect, utilities



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
@pytest.mark.add_list_api
@scenario('../features/api.feature', 'Add list via API')
def test_add_list_api(set_auth_state):
    pass



@given('The user is logged in and on the Dashboard page')
def user_on_dashboard_page(browser_instance, shared_data):
    #state = "auth_state.json" if os.path.exists("auth_state.json") else None
    #if state:
    dashboard_page = DashboardPage(browser_instance)
    #else:
     #   login_page = LoginPage(browser_instance)
      #  dashboard_page = login_page.login(user_credentials_list[0]['user_email'],user_credentials_list[0]['password'])

    shared_data['dashboard_page'] = dashboard_page
    time.sleep(2)


@when('The add list API POST request is made and page is reloaded')
def add_list_api(shared_data):
    dashboard_page = shared_data['dashboard_page']
    logged_in_user = dashboard_page.verify_dashboard()
    logger.info(f'logged in user: {logged_in_user}')
    user_email = str(logged_in_user).split('/')[1]
    logger.info(user_email)
    user_dao = User_DAO(db_connect.DBConnect())
    user = user_dao.get_user_by_email(user_email)
    logger.info(user)
    user_id = user[0]
    api_helper = APIHelper()
    add_list_api_response = api_helper.add_list(data={'user_id': user_id, 'name': utilities.generate_random_string() + 'List'})
    logger.info(add_list_api_response)
    shared_data['add_list_api'] = add_list_api_response

    time.sleep(2)


@then('The list added via the API is displayed on the Dashboard')
def validate_api_response(shared_data):
    dashboard_page = shared_data['dashboard_page']
    dashboard_page.reload_page()

