import os
import shutil

import pytest
from dotenv import load_dotenv

load_dotenv()

import logging

# Configure once (e.g., in conftest.py)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


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
def clean_auth_state_before_login():
    file_path = "auth_state.json"
    if os.path.exists(file_path):
        os.remove(file_path)
        logger.info("Deleted auth_state.json before login test.")


@pytest.fixture
def set_auth_state():
    source = 'utils/auth_state.json'
    if os.path.exists(source):
        destination = "auth_state.json"
        if os.path.exists(destination):
            pass
        else:
        # Move the file
            shutil.copy(source, destination)


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

    # context = browser.new_context()

    page = context.new_page()
    page.goto(url_start)
    yield page
    context.close()
    browser.close()
