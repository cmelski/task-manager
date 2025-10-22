import json
import os

import pytest
from pytest_bdd import given, when, then, parsers, scenarios, scenario

import utils.db_connect as db_connect
from conftest import logger
from page_objects.login import LoginPage
import time


# define the path to the feature file
# scenarios('features/login.feature')


# define a fixture and update the fixture as you go with data you will need in each function
@pytest.fixture
def shared_data():
    return {}


# valid login
# use these tags to run a specific scenario when multiple scenarios are in feature file
# terminal pytest -m delete_list
# feature file path is relative to the directory where the test resides (e.g. in this case test is in 'tests' folder
# under the project root)
@pytest.mark.login
@scenario('../features/login.feature', 'Verify successful login to Task Manager')
def test_login(clean_auth_state_before_login):
    pass


@given('The user is on landing page')
def user_on_landing_page(browser_instance, shared_data):
    login_page = LoginPage(browser_instance)
    shared_data['login_page'] = login_page


@when(parsers.parse('I log into Task Manager with user_email "{user_email}" and password "{password}"'))
def login_to_portal(shared_data):
    login_page = shared_data['login_page']
    login_page.navigate_to_login_page()
    with open('data/credentials.json') as f:  # path is relative to project root
        test_data = json.load(f)
        user_credentials_list = test_data['user_credentials']
        user_credentials_list[0]['user_email'] = os.environ.get('USER_EMAIL')
        user_credentials_list[0]['password'] = os.environ.get('PASS')
        user_email = user_credentials_list[0]['user_email']
        password = user_credentials_list[0]['password']

    dashboard_page = login_page.login(user_email, password)
    shared_data['dashboard_page'] = dashboard_page
    time.sleep(2)


@then('Successful login result is achieved')
def validate_login(shared_data):
    dashboard_page = shared_data['dashboard_page']
    user = dashboard_page.verify_dashboard()
    logger.info(user)
    con = db_connect.DBConnect()
    con.cursor.execute("SELECT id, email, name FROM users WHERE name = %s", (user,))
    row = con.cursor.fetchone()
    con.close()
    logger.info(row)
    assert len(user) > 0
    assert row[2] == user
    assert  row[1] == os.environ.get('USER_EMAIL')


# invalid login


@pytest.mark.invalid_login
@scenario('../features/login.feature', 'Verify unsuccessful login to Task Manager')
def test_invalid_login(clean_auth_state_before_login):
    pass


@given('The user is on landing page')
def user_on_landing_page(browser_instance, shared_data):
    login_page = LoginPage(browser_instance)
    shared_data['login_page'] = login_page
    shared_data['invalid_credentials'] = [
        (os.environ.get('USER_EMAIL'), 'wrongpass'),
        ('wronguser', os.environ.get('PASS')),
        ('baduser', 'badpass')
    ]


@when('I navigate to the Login Page')
def go_to_login_page(shared_data):
    login_page = shared_data[('login_'
                              'page')]
    login_page.navigate_to_login_page()

@then(parsers.parse('Login is rejected when incorrect user_email "{user_email}" and/or password "{'
                    'password}" is entered'))
def attempt_login_to_portal(shared_data):
    login_page = shared_data[('login_'
                              'page')]
    for credentials in shared_data['invalid_credentials']:
        user_email, password = credentials
        login_page.invalid_login(user_email, password)
        login_page.validate_bad_login()
        time.sleep(2)


