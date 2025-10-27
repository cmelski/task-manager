import os
import shutil
import logging
from pathlib import Path

import pytest
import psutil

# load .env file variables
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

# set up logging
# Configure once (e.g., in conftest.py)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


# set up hooks
@pytest.hookimpl
def pytest_bdd_before_scenario(request, feature, scenario):
    logger.info(f"\n🟢 Starting scenario: {scenario.name}")


@pytest.hookimpl
def pytest_bdd_after_scenario(request, feature, scenario):
    logger.info(f"🔴 Finished scenario: {scenario.name}")


@pytest.hookimpl
def pytest_bdd_step_error(request, feature, scenario, step, exception):
    logger.info(f"❌ Step failed: {step.name} -> {exception}")


# define test run parameters
# in terminal you can run for e.g. 'pytest test_web_framework_api.py --browser_name firefox'
def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="browser selection"
    )

    parser.addoption(
        "--url_start", action="store", default=os.environ.get('BASE_URL'), help="starting url"
    )


@pytest.fixture(scope='session')
def user_credentials(request):
    return request.param


# call this fixture for login tests
@pytest.fixture
def clean_auth_state_before_login():
    file_path = Path(__file__).parent.parent / "auth_state.json"
    if os.path.exists(file_path):
        os.remove(file_path)
        logger.info("Deleted auth_state.json before login test.")


# call this fixture to set auth state to bypass login
@pytest.fixture
def set_auth_state():
    # Path to the file to copy

    src = Path(__file__).parent.parent / "utils" / "auth_state.json"


    # Destination in project root

    dst = Path(__file__).parent.parent / "auth_state.json"

    logger.info('auth_state.json does not exist')

    if not dst.exists():
        shutil.copy(src, dst)
        logger.info(f"Copied {src} → {dst}")
        logger.info("Set the auth_state.json before login test.")
    else:
        logger.info(f"File already exists at {dst}")

        # You can return the path if needed
    return dst



# main tests fixture that yields page object and then closes context and browser after yield as part of teardown
@pytest.fixture(scope='function')
def browser_instance(request):
    browser_name = request.config.getoption('browser_name')
    url_start = request.config.getoption('url_start')
    with sync_playwright() as p:
        if browser_name == 'chrome':
            browser = p.chromium.launch(headless=False, timeout=120000)
        elif browser_name == 'firefox':
            browser = p.firefox.launch(headless=False)

        state = "auth_state.json" if os.path.exists("auth_state.json") else None

        if state:
            context = browser.new_context(storage_state=state)
        else:
            context = browser.new_context()

        page = context.new_page()
        page.goto(url_start)
        try:
            yield page
        finally:
            context.close()
            browser.close()


@pytest.fixture(scope='function')
def browser_instance_mult_context(request):
    browser_name = request.config.getoption('browser_name')
    url_start = request.config.getoption('url_start')
    with sync_playwright() as p:
        if browser_name == 'chrome':
            browser = p.chromium.launch(headless=False, timeout=120000)
        elif browser_name == 'firefox':
            browser = p.firefox.launch(headless=False)

        state = "auth_state.json" if os.path.exists("auth_state.json") else None
        if state:
            context_user_1 = browser.new_context(storage_state=state)
            context_user_2 = browser.new_context(storage_state=state)
        else:
            context_user_1 = browser.new_context()
            context_user_2 = browser.new_context()

        page_user_1 = context_user_1.new_page()
        page_user_2 = context_user_2.new_page()
        page_user_1.goto(url_start)
        page_user_2.goto(url_start)

        try:
            yield page_user_1, page_user_2
        finally:
        # ensures closure even if test fails
            for ctx in (context_user_1, context_user_2):
                try:
                    ctx.close()
                except Exception:
                    pass
            try:
                browser.close()
            except Exception:
                pass