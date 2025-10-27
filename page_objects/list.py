from playwright.sync_api import expect, Page, Locator
import utils.utilities as util
from tests.conftest import logger


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
        util.select_date(self.page)
        options = self.page.locator('#assignName option').all_text_contents()
        assert util.new_item_data[0] in options
        self.page.locator('input[list="assignName"]').fill(util.new_item_data[0])
        self.page.locator('textarea[name="new_notes"]').fill(util.new_item_data[1])
        self.page.locator('input[name="new_complete"]').check()
        item_name = self.page.locator('input[placeholder*="Add New Task"]').input_value()
        due = self.page.locator('input[name="new_due_date"]').input_value()
        assignee = util.new_item_data[0]
        notes = util.new_item_data[1]
        complete = util.new_item_data[2]
        list_item.append((item_name, due, assignee, notes, complete))
        self.page.locator('a[onclick*="add_item_"]').click()
        return list_item

    def validate_new_item(self):
        rows = self.page.locator('table.task-table > tbody > tr')
        last_index = rows.count() - 2  # don't want the add new task row and index starts from 0
        logger.info(f'last index is {last_index}')
        last_item = []
        item_name = self.page.locator(f'input[name*="task_{str(last_index)}"]').input_value()
        due = self.page.locator(f'input[name*="due_{str(last_index)}"]').input_value()
        assignee = self.page.locator(f'input[name*="assign_{str(last_index)}"]').input_value()
        notes = self.page.locator(f'textarea[name*="notes_{str(last_index)}"]').input_value()
        checkbox = self.page.locator(f'input[name*="complete_{str(last_index)}"]')
        complete = False
        if checkbox.is_checked():
            complete = True
        last_item.append((item_name, due, assignee, notes, complete))
        return last_item

    def delete_list_item(self):
        cells = self.page.locator('table.task-table > tbody > tr > td')
        if cells.count() < 10:  # list has no items; need to add an item first
            self.add_list_item()
            self.validate_new_item()
        cell_count_before_delete = self.page.locator('table.task-table > tbody > tr > td').count()
        logger.info(cell_count_before_delete)
        rows = self.page.locator('table.task-table > tbody > tr')
        last_index = rows.count() - 2  # don't want the add new task row and index starts from 0
        logger.info(f'last index is {last_index}')
        row = self.page.locator('table.task-table > tbody > tr').nth(last_index)
        row.locator('td > div > a').first.click()
        cell_count_after_delete = self.page.locator('table.task-table > tbody > tr > td').count()
        logger.info(cell_count_after_delete)
        expect(self.page.locator('table.task-table > tbody > tr > td')).to_have_count(
            cell_count_after_delete)
        return cell_count_before_delete, cell_count_after_delete

    def update_list_item(self, update_details):
        cells = self.page.locator('table.task-table > tbody > tr > td')
        if cells.count() < 10:  # list has no items; need to add an item first
            self.add_list_item()
        rows = self.page.locator('table.task-table > tbody > tr')
        last_index = rows.count() - 2  # don't want the add new task row and index starts from 0
        logger.info(f'last index is {last_index}')

        # clear values
        self.page.locator(f'input[name*="task_{str(last_index)}"]').fill('')
        self.page.locator(f'input[name*="assign_{str(last_index)}"]').fill('')
        self.page.locator(f'textarea[name*="notes_{str(last_index)}"]').fill('')

        self.page.locator(f'input[name*="task_{str(last_index)}"]').fill(update_details[0])
        util.select_date(self.page, update_details[1], last_index)
        self.page.locator(f'input[name*="assign_{str(last_index)}"]').fill(update_details[2])
        self.page.locator(f'textarea[name*="notes_{str(last_index)}"]').fill(update_details[3])
        if update_details[4]:
            self.page.locator(f'input[name*="complete_{str(last_index)}"]').uncheck()
        else:
            self.page.locator(f'input[name*="complete_{str(last_index)}"]').uncheck()

        self.page.locator('a[onclick*="item_list"]').click()

        updated_item = []
        item_name = self.page.locator(f'input[name*="task_{str(last_index)}"]').input_value()
        due = self.page.locator(f'input[name*="due_{str(last_index)}"]').input_value()
        assignee = self.page.locator(f'input[name*="assign_{str(last_index)}"]').input_value()
        notes = self.page.locator(f'textarea[name*="notes_{str(last_index)}"]').input_value()
        checkbox = self.page.locator(f'input[name*="complete_{str(last_index)}"]')
        complete = False
        if checkbox.is_checked():
            complete = True
        updated_item.append(item_name)
        updated_item.append(due)
        updated_item.append(assignee)
        updated_item.append(notes)
        updated_item.append(complete)

        return updated_item

    def select_clone(self):
        # get list name and list details
        list_items_original = []
        list_items_clone = []

        list_name = self.page.wait_for_selector('input[name="list_name"]', state='visible')
        list_name_original = list_name.input_value()

        try:
            cells_original = self.page.wait_for_selector('table.task-table > tbody > tr:not(:last-child) > td:nth-child(-n+5)',
                                                         state='visible', timeout=500)
            cells_original = self.page.locator('table.task-table > tbody > tr:not(:last-child) > td:nth-child(-n+5)')


            if cells_original.count() > 0:
                for cell in cells_original.all():
                    checkbox = cell.locator("input[type='checkbox']")
                    text_area = cell.locator('textarea')
                    text_input = cell.locator('input:not([type="checkbox"])')

                    if checkbox.count() > 0:
                        value = checkbox.first.is_checked()
                    elif text_area.count() > 0:
                        value = text_area.first.input_value()
                    elif text_input.count() > 0:
                        value = text_input.first.input_value()
                    else:
                        value = cell.inner_text().strip()

                    list_items_original.append(value)

            self.page.locator('li a').first.click(force=True)

            # import Locator and Page from playwright and then this syntax allows for auto suggestions
            clone_link: Locator = self.page.locator('a[href*="clone"]')
            clone_link.click()

            #Pauses the script execution for the given number of milliseconds.
            # 500 → 0.5 seconds.
            # It does nothing else: it doesn’t check for elements, conditions, or any page state.
            # It just sleeps.Effectively, it’s equivalent to:
            # import time
            # time.sleep(0.5)
            # but in a Playwright-friendly way that integrates with the event loop.

            self.page.wait_for_timeout(500)

            # get the cloned list details:

            list_name = self.page.wait_for_selector('input[name="list_name"]', state='visible')
            list_name_clone = list_name.input_value()
            cells = self.page.wait_for_selector('table.task-table > tbody > tr:not(:last-child) > td:nth-child(-n+5)',
                                                state='visible')
            cells_clone = self.page.locator('table.task-table > tbody > tr:not(:last-child) > td:nth-child(-n+5)')

            if cells_clone.count() > 0:
                for cell in cells_clone.all():
                    checkbox = cell.locator("input[type='checkbox']")
                    text_area = cell.locator('textarea')
                    text_input = cell.locator('input:not([type="checkbox"])')

                    if checkbox.count() > 0:
                        value = checkbox.first.is_checked()
                    elif text_area.count() > 0:
                        value = text_area.first.input_value()
                    elif text_input.count() > 0:
                        value = text_input.first.input_value()
                    else:
                        value = cell.inner_text().strip()

                    list_items_clone.append(value)

        except:
            self.page.locator('li a').first.click(force=True)

            # import Locator and Page from playwright and then this syntax allows for auto suggestions
            clone_link: Locator = self.page.locator('a[href*="clone"]')
            clone_link.click()

            self.page.wait_for_timeout(500)

            # get the cloned list details:

            list_name = self.page.wait_for_selector('input[name="list_name"]', state='visible')
            list_name_clone = list_name.input_value()

        return list_name_original, list_name_clone, list_items_original, list_items_clone
