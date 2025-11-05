import os
import shutil
import logging
import time
from pathlib import Path

import psycopg
import pytest
import psutil

# load prod.env file variables
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError

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
        "--url_start", action="store", default="test", help="starting url"
    )

    parser.addoption(
        "--env", action="store", default="test", help="Environment to run tests against")


@pytest.fixture(scope="session")
def env(request):
    env_name = request.config.getoption("--env")
    # Load the corresponding .env file
    load_dotenv(f"{env_name}.env")
    return env_name

@pytest.fixture(scope="session")
def url_start(env):  # env fixture ensures .env is loaded first
    return os.environ.get("BASE_URL")

@pytest.fixture(scope="session")
def db_connection(env):
    if env == 'test':
        conn = psycopg.connect(
            dbname=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT')
        )
    else:
        conn = psycopg.connect(os.environ.get('DB_HOST'))

    yield conn
    conn.close()


load_dotenv(f"{env}.env")


@pytest.fixture(scope='session')
def user_credentials(request):
    return request.param


# call this fixture for login tests
@pytest.fixture
def clean_auth_state_before_login(env):
    if env == 'test':
        file_path = Path(__file__).parent.parent / "auth_state_test.json"
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info("Deleted auth_state_test.json before login test.")
    else:
        file_path = Path(__file__).parent.parent / "auth_state_prod.json"
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info("Deleted auth_state_prod.json before login test.")


# call this fixture to set auth state to bypass login
@pytest.fixture
def set_auth_state(env):
    # Path to the file to copy

    if env == 'test':

        src = Path(__file__).parent.parent / "utils" / "auth_state_test.json"

        # Destination in project root

        dst = Path(__file__).parent.parent / "auth_state_test.json"

        logger.info('auth_state_test.json does not exist')

        if not dst.exists():
            shutil.copy(src, dst)
            logger.info(f"Copied {src} → {dst}")
            logger.info("Set the auth_state_test.json before login test.")
        else:
            logger.info(f"File already exists at {dst}")

        # You can return the path if needed
        return dst
    else:
        src = Path(__file__).parent.parent / "utils" / "auth_state_prod.json"

        # Destination in project root

        dst = Path(__file__).parent.parent / "auth_state_prod.json"

        logger.info('auth_state_prod.json does not exist')

        if not dst.exists():
            shutil.copy(src, dst)
            logger.info(f"Copied {src} → {dst}")
            logger.info("Set the auth_state_prod.json before login test.")
        else:
            logger.info(f"File already exists at {dst}")

        # You can return the path if needed
        return dst


def safe_goto(page, url, retries=3, delay=5):
    for attempt in range(1, retries + 1):
        try:
            page.goto(url, timeout=20000)
            return
        except TimeoutError:
            print(f"⚠️ Attempt {attempt} failed to reach {url}, retrying in {delay}s...")
            time.sleep(delay)
    raise TimeoutError(f"Failed to load {url} after {retries} retries")


# main tests fixture that yields page object and then closes context and browser after yield as part of teardown
@pytest.fixture(scope='function')
def browser_instance(request, url_start):
    browser_name = request.config.getoption('browser_name')
    #url_start = request.config.getoption('url_start')
    url_start = url_start

    with sync_playwright() as p:
        if browser_name == 'chrome':
            browser = p.chromium.launch(headless=False, timeout=120000)
        elif browser_name == 'firefox':
            browser = p.firefox.launch(headless=False)

        state = "auth_state_test.json" if os.path.exists("auth_state_test.json") else None

        if state:
            context = browser.new_context(storage_state=state)
        else:
            context = browser.new_context()

        page = context.new_page()

        safe_goto(page, url_start)
        try:

            yield page
        finally:
            context.close()
            browser.close()
            file_path = Path(__file__).parent.parent / "auth_state_test.json"
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info("Deleted auth_state_test.json.")


@pytest.fixture(scope='function')
def browser_instance_mult_context(request):
    browser_name = request.config.getoption('browser_name')
    url_start = request.config.getoption('url_start')
    with sync_playwright() as p:
        if browser_name == 'chrome':
            browser = p.chromium.launch(headless=False, timeout=120000)
        elif browser_name == 'firefox':
            browser = p.firefox.launch(headless=False)

        state = "auth_state_test.json" if os.path.exists("auth_state_test.json") else None
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


@pytest.fixture(scope='function')
def browser_instance_api(request):
    browser_name_api = request.config.getoption('browser_name')
    url_start_api = request.config.getoption('url_start')
    with sync_playwright() as p:
        if browser_name_api == 'chrome':
            browser_api = p.chromium.launch(headless=False, timeout=120000)
        elif browser_name_api == 'firefox':
            browser_api = p.firefox.launch(headless=False)

        state_api = "auth_state_test.json" if os.path.exists("auth_state_test.json") else None

        if state_api:
            context_api = browser_api.new_context(storage_state=state_api)
        else:
            context_api = browser_api.new_context()

        page_api = context_api.new_page()

        from helpers.api_helper import APIHelper
        api_helper = APIHelper()
        api_helper.login(data={'email': os.environ.get('USER_EMAIL_TEST'),
                               'password': os.environ.get('PASS_TEST')},
                         params={'mock': 1})
        # logger.info(f'Login API response: {login_api_response}')

        safe_goto(page_api, url_start_api)

        try:

            yield page_api
        finally:
            context_api.close()
            browser_api.close()
            # file_path = Path(__file__).parent.parent / "auth_state_test.json"
            # if os.path.exists(file_path):
            #     os.remove(file_path)
            #     logger.info("Deleted auth_state_test.json.")
