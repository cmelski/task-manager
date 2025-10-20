import pytest
from pytest_bdd import given, when, then, parsers, scenarios, scenario

from conftest import logger
from page_objects.login import LoginPage
# from utils.api_base_framework import APIBase
import time

# define the path to the feature file
#scenarios('features/login.feature')


# define a fixture and update the fixture as you go with data you will need in each function
@pytest.fixture
def shared_data():
    return {}


# valid login
# use these tags to run a specific scenario when multiple scenarios are in feature file
# terminal pytest -m delete_list
@pytest.mark.login
@scenario('features/login.feature', 'Verify successful login to Task Manager')
def test_login(clean_auth_state_before_login):
    pass


@given('The user is on landing page')
def user_on_landing_page(browser_instance, shared_data):
    login_page = LoginPage(browser_instance)
    shared_data['login_page'] = login_page


@when(parsers.parse('I log into Task Manager with {user_email} and {password}'))
def login_to_portal(user_email, password, shared_data):
    login_page = shared_data['login_page']
    dashboard_page = login_page.login(user_email, password)
    shared_data['dashboard_page'] = dashboard_page
    time.sleep(2)


@then('Successful login result is achieved')
def validate_login(shared_data):
    dashboard_page = shared_data['dashboard_page']
    user = dashboard_page.verify_dashboard()
    logger.info(user)
    assert len(user) > 0


# invalid login
@pytest.mark.invalid_login
@scenario('features/login.feature', 'Verify unsuccessful login to Task Manager')
def test_invalid_login(clean_auth_state_before_login):
    pass


@given('The user is on landing page')
def user_on_landing_page(browser_instance, shared_data):
    login_page = LoginPage(browser_instance)
    shared_data['login_page'] = login_page


@when(parsers.parse('I log into Task Manager using wrong password with {user_email} and {password}'))
def login_to_portal(user_email, password, shared_data):
    login_page = shared_data['login_page']
    login_page.invalid_login(user_email, password)
    time.sleep(2)


@then('Unsuccessful login result is achieved')
def validate_unsuccessful_login(shared_data):
    login_page = shared_data['login_page']
    login_page.validate_bad_login()
