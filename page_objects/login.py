from .dashboard import DashboardPage
from playwright.sync_api import expect


class LoginPage:

    def __init__(self, page):
        self.page = page

    def login(self, user_email, password):

        self.page.locator('li a').first.click()
        self.page.locator('a:has-text("Log In")').click()
        self.page.locator('#email').fill(user_email)
        self.page.locator('#password').fill(password)
        self.page.locator('#submit').click()


        dashboard_page = DashboardPage(self.page)
        return dashboard_page

    def invalid_login(self, user_email, password):
        self.page.locator('li a').first.click()
        self.page.locator('a:has-text("Log In")').click()
        self.page.locator('input#email').fill('')
        self.page.locator('input#email').fill(user_email)
        self.page.locator('input#password').fill('')
        self.page.locator('input#password').fill(password)
        self.page.locator('#submit').click()

    def validate_bad_login(self):
        expect(self.page.get_by_text('Invalid password')).to_be_visible()


