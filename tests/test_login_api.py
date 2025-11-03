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
from unittest.mock import patch


# define a fixture and update the fixture as you go with data you will need in each function
@pytest.fixture
def shared_data():
    return {}



# define the path to the feature file
# scenarios('features/list.feature')

# use these tags to run a specific scenario when multiple scenarios are in feature file
# terminal pytest -m delete_list
@pytest.mark.login_api
@scenario('../features/api.feature', 'Log in via API')
def test_login_api():
    pass


@given('The user logs in via API')
def login_api(shared_data):
    api_helper = APIHelper()
    login_api_response = api_helper.login(
        data={'email': os.environ.get('USER_EMAIL'), 'password': os.environ.get('PASS')})
    logger.info(f'Login API response: {login_api_response}')
    shared_data['login_api_response'] = login_api_response


@when('The API response token is received')
def get_login_api_response(shared_data):
    pass


@then('The user bypasses the login screen')
def validate_login_api_response(shared_data):
    pass

