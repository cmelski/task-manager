import time

from playwright.sync_api import expect
from .list import ListPage


class DashboardPage:

    def __init__(self, page):
        self.page = page

    def verify_dashboard(self):
        self.page.locator('.tooltip').first.hover()
        # Get the tooltip text
        expect(self.page.locator('.tooltip .tooltiptext').nth(0)).not_to_be_empty()
        self.page.context.storage_state(path="auth_state.json")

    def add_new_list(self):
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
