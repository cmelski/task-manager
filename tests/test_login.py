import json
import os

import pytest
from pytest_bdd import given, when, then, parsers, scenario

import utils.db_connect as db_connect
from dao.user_dao import User_DAO
from tests.conftest import logger
from page_objects.login import LoginPage
from page_objects.dashboard import DashboardPage
import time


# define the path to the feature file
# scenarios('features/login.feature')


# define a fixture and update the fixture as you go with data you will need in each function
@pytest.fixture()
def shared_data():
    return {}


# valid login
# use these tags to run a specific scenario when multiple scenarios are in feature file
# terminal pytest -m delete_list
# feature file path is relative to the directory where the test resides (e.g. in this case test is in 'tests' folder
# under the project root)
@pytest.mark.login
@scenario('../features/login.feature', 'Verify successful login to Task Manager Single User')
def test_login_single_user(clean_auth_state_before_login):
    pass


@given('The user is on landing page single user')
def user_on_landing_page_single_user(browser_instance, shared_data):
    dashboard_page = DashboardPage(browser_instance)
    shared_data['dashboard_page'] = dashboard_page


@when(parsers.parse('I log into task manager with user_email and password single user'))
def login_to_portal_single_user(shared_data):
    dashboard_page = shared_data['dashboard_page']
    login_page = dashboard_page.navigate_to_login_page()
    with open('data/credentials.json') as f:  # path is relative to project root
        test_data = json.load(f)
        user_credentials_list = test_data['user_credentials']
        user_credentials_list[0]['user_email'] = os.environ.get('USER_EMAIL')
        user_credentials_list[0]['password'] = os.environ.get('PASS')
        user_email = user_credentials_list[0]['user_email']
        password = user_credentials_list[0]['password']
        user_credentials_list[1]['user_email'] = os.environ.get('USER_EMAIL_2')
        user_credentials_list[1]['password'] = os.environ.get('PASS_2')
        user_email_2 = user_credentials_list[1]['user_email']
        password_2 = user_credentials_list[1]['password']

    dashboard_page = login_page.login(user_email, password)
    shared_data['dashboard_page'] = dashboard_page
    time.sleep(2)


@then('Successful login result is achieved single user')
def validate_login_single_user(shared_data):
    dashboard_page = shared_data['dashboard_page']
    logged_in_user = dashboard_page.verify_dashboard()
    logger.info(f'logged in user: {logged_in_user}')
    user_name = str(logged_in_user).split('/')[0]
    user_email = str(logged_in_user).split('/')[1]
    logger.info(user_name)
    logger.info(user_email)
    user_dao = User_DAO(db_connect.DBConnect())
    user = user_dao.get_user_by_email(user_email)
    logger.info(user)
    assert len(user_name) > 0
    assert user[2] == user_name
    assert user[1] == os.environ.get('USER_EMAIL')
    assert user[1] == user_email
    logger.info(f'User {user_name} : {user[1]} successfully logged in!')


# invalid login


@pytest.mark.invalid_login
@scenario('../features/login.feature', 'Verify unsuccessful login to Task Manager')
def test_invalid_login(clean_auth_state_before_login):
    pass


@given('The user is on landing page single user')
def user_on_landing_page_single_user_invalid(browser_instance, shared_data):
    dashboard_page = DashboardPage(browser_instance)
    shared_data['dashboard_page'] = dashboard_page
    shared_data['invalid_credentials'] = [
        (os.environ.get('USER_EMAIL'), 'wrongpass'),
        ('wronguser', os.environ.get('PASS')),
        ('baduser', 'badpass')
    ]


@when('I navigate to the Login Page')
def go_to_login_page_single_user_invalid(shared_data):
    dashboard_page = shared_data[('dashboard_'
                                  'page')]
    login_page = dashboard_page.navigate_to_login_page()
    shared_data['login_page'] = login_page


@then(parsers.parse('Login is rejected when incorrect user_email "{user_email}" and/or password "{'
                    'password}" is entered'))
def attempt_login_to_portal_single_user_invalid(shared_data):
    login_page = shared_data[('login_'
                              'page')]
    for credentials in shared_data['invalid_credentials']:
        user_email, password = credentials
        login_page.invalid_login(user_email, password)
        login_page.validate_bad_login()
        time.sleep(2)


@pytest.mark.login_mult_context
@scenario('../features/login.feature', 'Verify successful login to Task Manager by 2 users with own context')
def test_login_mult_context(clean_auth_state_before_login):
    pass


@given('The user is on landing page mult context')
def user_on_landing_page_mult_context(browser_instance_mult_context, shared_data):
    dashboard_page_user_1 = DashboardPage(browser_instance_mult_context[0])
    dashboard_page_user_2 = DashboardPage(browser_instance_mult_context[1])
    shared_data['dashboard_page_user_1'] = dashboard_page_user_1
    shared_data['dashboard_page_user_2'] = dashboard_page_user_2


@when(parsers.parse('I log into Task Manager with user_email and password mult context'))
def login_to_portal_mult_context(shared_data):
    with open('data/credentials.json') as f:  # path is relative to project root
        test_data = json.load(f)
        user_credentials_list = test_data['user_credentials']
        user_credentials_list[0]['user_email'] = os.environ.get('USER_EMAIL')
        user_credentials_list[0]['password'] = os.environ.get('PASS')
        user_1_email = user_credentials_list[0]['user_email']
        user_1_password = user_credentials_list[0]['password']
        user_credentials_list[1]['user_email'] = os.environ.get('USER_EMAIL_2')
        user_credentials_list[1]['password'] = os.environ.get('PASS_2')
        user_2_email = user_credentials_list[1]['user_email']
        user_2_password = user_credentials_list[1]['password']

    dashboard_page_user_1 = shared_data['dashboard_page_user_1']
    login_page_user_1 = dashboard_page_user_1.navigate_to_login_page()
    dashboard_page_user_1 = login_page_user_1.login(user_1_email, user_1_password)
    shared_data['dashboard_page_user_1'] = dashboard_page_user_1
    logger.info('User 1 logged in')
    time.sleep(2)

    dashboard_page_user_2 = shared_data['dashboard_page_user_2']
    login_page_user_2 = dashboard_page_user_2.navigate_to_login_page()
    dashboard_page_user_2 = login_page_user_2.login(user_2_email, user_2_password)
    shared_data['dashboard_page_user_2'] = dashboard_page_user_2
    logger.info('User 2 logged in')
    time.sleep(2)


@then('Successful login result is achieved mult context')
def validate_login_mult_context(shared_data):
    con = db_connect.DBConnect()

    dashboard_page_user_1 = shared_data['dashboard_page_user_1']
    user_1 = dashboard_page_user_1.verify_dashboard()
    user_1_name = str(user_1).split('/')[0]
    user_1_email = str(user_1).split('/')[1]
    logger.info(user_1)
    user_dao = User_DAO(db_connect.DBConnect())
    user = user_dao.get_user_by_email(user_1_email)
    logger.info(user)
    assert len(user_1_name) > 0
    assert user[2] == user_1_name
    assert user[1] == os.environ.get('USER_EMAIL')
    assert user[1] == user_1_email
    logger.info(f'User {user_1_name} : {user[1]} successfully logged in!')

    dashboard_page_user_2 = shared_data['dashboard_page_user_2']
    user_2 = dashboard_page_user_2.verify_dashboard()
    logger.info(user_2)
    user_2_name = str(user_2).split('/')[0]
    user_2_email = str(user_2).split('/')[1]
    user_dao = User_DAO(db_connect.DBConnect())
    user = user_dao.get_user_by_email(user_2_email)
    logger.info(user)
    assert len(user_2_name) > 0
    assert user[2] == user_2_name
    assert user[1] == os.environ.get('USER_EMAIL_2')
    assert user[1] == user_2_email
    logger.info(f'User {user_2_name} : {user[2]} successfully logged in!')

    con.close()
