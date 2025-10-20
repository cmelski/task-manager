import time

from playwright.sync_api import expect
import utils.utilities as util


class ListPage:

    def __init__(self, page):
        self.page = page

    def enter_list_name(self):
        locator = self.page.locator('input[name="list_name"]')
        list_name = util.generate_random_string() + ' List'
        locator.fill(list_name)
        locator.press('Enter')

    def validate_list(self):
        list_name = self.page.locator('input[name="list_name"]').input_value()
        self.page.locator('li a').first.click(force=True)

        # Wait for the list container or at least one link to appear
        self.page.wait_for_selector('object a', state="visible", timeout=5000)

        lists = self.page.locator('object a').all_text_contents()
        return lists, list_name

    def add_list_item(self):
        list_item = []
        self.page.locator('input[placeholder*="Add New Task"]').fill(util.generate_random_string() + ' item')
        options = self.page.locator('#assignName option').all_text_contents()
        assert util.new_item_data[0] in options
        self.page.locator('input[list="assignName"]').fill(util.new_item_data[0])
        self.page.locator('textarea[name="new_notes"]').fill(util.new_item_data[1])
        self.page.locator('input[name="new_complete"]').check()
        item_name = self.page.locator('input[placeholder*="Add New Task"]').input_value()
        assignee = util.new_item_data[0]
        notes = util.new_item_data[1]
        complete = util.new_item_data[2]
        list_item.append((item_name, assignee, notes, complete))
        self.page.locator('a[onclick*="add_item_"]').click()
        return list_item

    def validate_new_item(self):
        rows = self.page.locator('table tbody tr')
        last_index = rows.count() - 2 #don't want the add new task row
        last_item = []
        item_name = self.page.locator(f'input[name*="task_{str(last_index)}"]').input_value()
        assignee = self.page.locator(f'input[name*="assign_{str(last_index)}"]').input_value()
        notes = self.page.locator(f'textarea[name*="notes_{str(last_index)}"]').input_value()
        checkbox = self.page.locator(f'input[name*="complete_{str(last_index)}"]')
        complete = False
        if checkbox.is_checked():
            complete = True
        last_item.append((item_name, assignee, notes, complete))
        return last_item
