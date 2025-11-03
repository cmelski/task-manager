import json
import os
import pytest

from pytest_bdd import given, when, then, parsers, scenarios, scenario
from page_objects.dashboard import DashboardPage
import time
from dao.user_dao import User_DAO
from helpers.api_helper import APIHelper
from tests.conftest import logger
from utils import db_connect



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
@pytest.mark.get_user_lists_api
@scenario('../features/api.feature', 'GET lists for logged in user')
def test_get_user_lists_api(set_auth_state):
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


@when('The get user lists API GET request is made')
def get_user_lists_api(shared_data):
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
    user_lists_api = api_helper.get_user_lists(params={'user_id': user_id})
    logger.info(user_lists_api)
    shared_data['user_lists_api'] = user_lists_api

    time.sleep(2)


@then('The lists belonging to the user are retrieved and match the Dashboard')
def validate_api_response(shared_data):
    dashboard_page = shared_data['dashboard_page']
    user_lists_dashboard = dashboard_page.get_user_lists()
    user_lists_api = shared_data['user_lists_api']['lists']
    logger.info(f'User lists dashboard: {user_lists_dashboard}')
    logger.info((f'User lists api: {user_lists_api}'))

    assert len(user_lists_dashboard) == len(user_lists_api)
    for i in range(0,len(user_lists_api)):
        assert user_lists_api[i][2] in user_lists_dashboard
