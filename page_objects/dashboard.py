import os
import time

from playwright.sync_api import expect

from tests.conftest import logger
from .list import ListPage
from unittest.mock import patch


class DashboardPage:

    def __init__(self, page):

        self.page = page


    def navigate_to_login_page(self):
        from .login import LoginPage
        self.page.locator('li a').first.click()
        login_page = LoginPage(self.page)
        self.page.locator('a:has-text("Log In")').click()
        return login_page

    def verify_dashboard(self,env):
        self.page.locator('.tooltip').first.hover()
        # Get the tooltip text
        user = self.page.locator('.tooltip .tooltiptext').nth(0).inner_text()
        expect(self.page.locator('.tooltip .tooltiptext').nth(0)).not_to_be_empty()
        if env == 'test':
            self.page.context.storage_state(path="auth_state_test.json")
        else:
            self.page.context.storage_state(path="auth_state_prod.json")
        return user

    def add_new_list(self):

        # check if logged in
        self.page.locator('li a').first.click()
        menu_options = self.page.locator('li a').all()
        for option in menu_options:
            menu_text = option.inner_text()
            logger.info(f'Menu option: {menu_text}')
            if menu_text == 'Log In':
                from .login import LoginPage
                login_page = LoginPage(self.page)
                self.page.locator('.close').click()
                self.page.locator('a[href="/add_list"]').click()
                return login_page

        self.page.locator('.close').click()
        self.page.locator('a[href="/add_list"]').click()
        new_list_page = ListPage(self.page)
        return new_list_page

    def find_list_to_delete(self):
        active_lists = self.page.locator('a[href*="/delete_list"]')

        if active_lists.count() > 0:
            last_index = active_lists.count() - 1
            list_name = self.page.locator('a[href*="/list_details"]').nth(last_index).inner_text()
            return last_index, list_name
        else:
            # Add a new list
            new_list_page = self.add_new_list()
            new_list_page.enter_list_name()

            # Navigate back home
            self.page.locator('li a').first.click()
            self.page.locator('a:has-text("Home")').click()

            # Wait for the new list to appear
            self.page.locator('a[href*="/delete_list"]').first.wait_for(state="visible")

            # Retry — now the new list exists
            return self.find_list_to_delete()

    def select_existing_list(self):
        active_lists = self.page.locator('a[href*="/list_details"]')

        if active_lists.count() > 0:
            self.page.locator('a[href*="/list_details"]').last.click()
            new_list_page = ListPage(self.page)
            return new_list_page

        else:
            # Add a new list
            new_list_page = self.add_new_list()
            new_list_page.enter_list_name()

            # Navigate back home
            self.page.locator('li a').first.click()
            self.page.locator('a:has-text("Home")').click()

            # Wait for the new list to appear
            self.page.locator('a[href*="/list_details"]').first.wait_for(state="visible")
            time.sleep(2)

            # Retry — now the new list exists

            return self.select_existing_list()

    def delete_list(self, index):
        self.page.locator('a[href*="/delete_list"]').nth(index).click()

    def validate_list_deletion(self):
        lists = self.page.locator('a[href*="/list_details"]').all_text_contents()
        return lists

    def navigate_to_register_page(self):
        self.page.locator('li a').first.click()
        self.page.locator('a:has-text("Register")').click()
        from .register import RegisterPage
        register_page = RegisterPage(self.page)
        return register_page

    def logout(self):

        self.page.locator('li a').first.click()
        self.page.locator('a:has-text("Log Out")').click()

    def verify_logout(self):

        self.page.wait_for_timeout(2000)
        self.page.locator('li a').first.click()
        menu_options = self.page.locator('li a').all()
        for option in menu_options:
            menu_text = option.inner_text()
            logger.info(f'Menu option: {menu_text}')
            if 'Log Out' in menu_text:
                return False

        return True

    def select_outstanding_tasks_report(self):
        self.page.goto('https://task-manager-6pqf.onrender.com/outstanding_tasks?mock_empty=true')
        from .report import ReportPage
        report_page = ReportPage(self.page)
        return report_page

    # @patch("main.con.cursor.fetchall", return_value=[])
    # def select_outstanding_tasks_report(self, mock_fetch):
    #     self.page.goto('https://task-manager-6pqf.onrender.com/outstanding_tasks')

    def get_user_lists(self):
        number_of_lists = self.page.locator('text=Active Lists').inner_text()
        number_of_lists = int(number_of_lists.split('(')[1].replace(')', ''))
        logger.info(f'Number of Lists: {number_of_lists}')

        lists = self.page.locator('object a[href*="list_details"]').all()
        lists = [list.inner_text() for list in lists]
        logger.info(f'Lists on Dashboard: {lists}')
        return lists

    def reload_page(self):
        self.page.reload()







