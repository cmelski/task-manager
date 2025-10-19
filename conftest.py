import os

import pytest
from dotenv import load_dotenv
load_dotenv()


# define test run parameters
def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="browser selection"
    )

    parser.addoption(
        "--url_start", action="store", default="https://task-manager-6pqf.onrender.com/", help="starting url"
    )


@pytest.fixture(scope='session')
def user_credentials(request):
    return request.param


@pytest.fixture
def browser_instance(playwright, request):
    browser_name = request.config.getoption('browser_name')
    url_start = request.config.getoption('url_start')
    if browser_name == 'chrome':
        browser = playwright.chromium.launch(headless=False)
    elif browser_name == 'firefox':
        browser = playwright.firefox.launch(headless=False)

    state = "auth_state.json" if os.path.exists("auth_state.json") else None
    if state:
        context = browser.new_context(storage_state=state)
    else:
        context = browser.new_context()

    #context = browser.new_context()
    page = context.new_page()
    page.goto(url_start)
    yield page
    context.close()
    browser.close()
