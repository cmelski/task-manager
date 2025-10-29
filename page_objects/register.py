from .dashboard import DashboardPage
from playwright.sync_api import expect


class RegisterPage:

    def __init__(self, page):
        self.page = page

    def register(self,user_email, password, name):
        self.page.locator('#email').fill(user_email)
        self.page.locator('#password').fill(password)
        self.page.locator('#name').fill(name)
        self.page.locator('#submit').click()

        dashboard_page = DashboardPage(self.page)
        return dashboard_page
