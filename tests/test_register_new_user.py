import json
import os
from pathlib import Path

import pytest
from pytest_bdd import given, when, then, parsers, scenario

import utils.db_connect as db_connect
from dao.user_dao import User_DAO
from tests.conftest import logger
from page_objects.dashboard import DashboardPage
import time


# define the path to the feature file
# scenarios('features/login.feature')


# define a fixture and update the fixture as you go with data you will need in each function
@pytest.fixture()
def shared_data():
    return {}




# use these tags to run a specific scenario when multiple scenarios are in feature file
# terminal pytest -m delete_list
# feature file path is relative to the directory where the test resides (e.g. in this case test is in 'tests' folder
# under the project root)
@pytest.mark.register
@scenario('../features/register.feature', 'Verify successful user registration to Task Manager')
def test_register_new_user(clean_auth_state_before_login):
    pass


@given('The new user is on landing page')
def new_user_on_landing_page(browser_instance, shared_data):
    dashboard_page = DashboardPage(browser_instance)
    shared_data['dashboard_page'] = dashboard_page


@when('Navigate to Register page')
def navigate_to_register_page(shared_data):
    dashboard_page = shared_data['dashboard_page']
    register_page = dashboard_page.navigate_to_register_page()
    shared_data['register_page'] = register_page


@when('Enter registration details and click Submit')
def submit_registration_details(shared_data):
    register_page = shared_data['register_page']
    with open('data/credentials.json') as f:  # path is relative to project root
        test_data = json.load(f)
        email = test_data["register_details"]["email"]
        password = test_data["register_details"]["password"]
        name = test_data["register_details"]["name"]

    dashboard_page = register_page.register(email, password, name)
    shared_data['dashboard_page'] = dashboard_page


@then('Successful registration is achieved')
def validate_successful_registration(shared_data, env, db_connection):
    dashboard_page = shared_data['dashboard_page']
    logged_in_user = dashboard_page.verify_dashboard(env)
    logger.info(logged_in_user)
    user_name = str(logged_in_user).split('/')[0]
    user_email = str(logged_in_user).split('/')[1]
    user_dao = User_DAO(db_connection)
    user = user_dao.get_user_by_email(user_email)
    logger.info(user)
    assert len(user_name) > 0
    assert user[2] == user_name
    logger.info(f'User {user_name} : {user[1]} successfully registered and logged in!')
    user_dao.delete_user_by_user_email(user[1])
    logger.info(f'New user {user_name} successfully deleted')




# invalid registration

@pytest.mark.invalid_register
@scenario('../features/register.feature', 'Verify unsuccessful user registration to Task Manager')
def test_invalid_register_new_user(clean_auth_state_before_login):
    pass


@given('The new user is on landing page')
def new_user_on_landing_page(browser_instance, shared_data):
    dashboard_page = DashboardPage(browser_instance)
    shared_data['dashboard_page'] = dashboard_page


@when('Navigate to Register page')
def navigate_to_register_page(shared_data):
    dashboard_page = shared_data['dashboard_page']
    register_page = dashboard_page.navigate_to_register_page()
    shared_data['register_page'] = register_page


@when(parsers.cfparse('Enter invalid email "{email}", password "{password}", name "{name}"'))
def submit_invalid_registration_details(shared_data, email, password, name):
    register_page = shared_data['register_page']
    email = "" if email == '""' else email
    password = "" if password == '""' else password
    name = "" if name == '""' else name
    register_page.invalid_register(email, password, name)
    shared_data['register_page'] = register_page


@then('Registration is not permitted')
def validate_unsuccessful_registration(shared_data):
    register_page = shared_data['register_page']
    error = register_page.validate_unsuccessful_registration()
    assert error is True

#login page redirect test case

@pytest.mark.redirect_to_login
@scenario('../features/register.feature', 'Verify user is redirected to login page if they are already registered')
def test_redirect_to_login(clean_auth_state_before_login):
    pass


@given('The user is on landing page')
def user_on_landing_page(browser_instance, shared_data):
    dashboard_page = DashboardPage(browser_instance)
    shared_data['dashboard_page'] = dashboard_page


@when('Navigate to Register page')
def navigate_to_register_page(shared_data):
    dashboard_page = shared_data['dashboard_page']
    register_page = dashboard_page.navigate_to_register_page()
    shared_data['register_page'] = register_page


@when('Enter an email that is already registered along with a password and name')
def submit_invalid_registration_details(shared_data):
    register_page = shared_data['register_page']
    dashboard_page = register_page.register()
    shared_data['register_page'] = register_page


@then('User is redirected to the Login page')
def validate_unsuccessful_registration(shared_data):
    register_page = shared_data['register_page']
    pass
