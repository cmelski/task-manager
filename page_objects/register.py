from tests.conftest import logger
from .dashboard import DashboardPage
from playwright.sync_api import expect


class RegisterPage:

    def __init__(self, page):
        self.page = page

    def register(self, user_email, password, name):
        self.page.locator('#email').fill(user_email)
        self.page.locator('#password').fill(password)
        self.page.locator('#name').fill(name)
        self.page.locator('#submit').click()

        dashboard_page = DashboardPage(self.page)
        return dashboard_page

    def invalid_register(self, email, password, name):
        self.page.locator('#email').fill('')
        self.page.locator('#password').fill('')
        self.page.locator('#name').fill('')
        self.page.locator('#email').fill(email)
        self.page.locator('#password').fill(password)
        self.page.locator('#name').fill(name)
        self.page.locator('#submit').click()

    def validate_unsuccessful_registration(self):
        # errors = self.page.locator("text=This field is required.")
        # try:
        #     expect(errors.first).to_be_visible(timeout=1000)  # wait up to 1 second
        #     return True
        # except AssertionError:
        #     return False

        # alternate way

        errors = self.page.locator('.invalid-feedback.d-block')

        if errors.count() > 0:
            expect(errors.first).to_have_text('This field is required.')
            return True
        else:
            return False
