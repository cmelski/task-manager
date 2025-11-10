import random
import string

from datetime import date, datetime, timedelta

from tests.conftest import logger


def generate_random_string():
    random_string = ''.join(random.choices(string.ascii_letters, k=10))
    return random_string


new_item_data = ['Chris', 'test notes', True]

from playwright.sync_api import sync_playwright


def select_date(page, due_date='', index=-1):
    if due_date == '':
        tomorrow_str = (date.today() + timedelta(days=0)).strftime("%Y-%m-%d")
    else:
        tomorrow_str = due_date

    day = int(tomorrow_str.split('-')[2])
    """
    Select a date in the table row `row_index` and day number `day` in the calendar widget.
    row_index: zero-based index of the table row
    day: day number to select (1-31)
    """
    # Locate the input in the given row
    if index == -1:
        row_selector = '#task_table > tbody > tr:last-child'
        input_selector = f'{row_selector} .calendar-wrapper .date-input'
    else:
        row_selector = f'#task_table > tbody > tr input[name*="due_{str(index)}"]'
        input_selector = f'{row_selector}.date-input'

    # Click the input to open the calendar popup
    page.click(input_selector)

    # Click the day cell in the calendar
    day_cell_selector = f'{row_selector} .calendar-wrapper .calendar-days td[data-testid="day-{day:02}"]'
    logger.info(f'day cell selector is : {day_cell_selector}')

    # Since your calendar uses full ISO for data-testid, we need year-month-day
    # Let's get the currently displayed month/year from the calendar header
    if index == -1:
        month_label_selector = f'{row_selector} .calendar-wrapper .month-label'
        month_year_text = page.locator(month_label_selector).inner_text()
    else:
        month_label_selector = f'#task_table > tbody > tr:nth-last-child({index + 2}) .calendar-wrapper .month-label'
        month_year_text = page.locator(month_label_selector).inner_text()

    # month_year_text is like "Oct 2025"

    displayed_month = datetime.strptime(month_year_text, '%b %Y')
    iso_day = f'{displayed_month.year}-{displayed_month.month:02}-{day:02}'
    if index == -1:
        day_cell_selector = f'{row_selector} .calendar-wrapper td[data-testid="day-{iso_day}"]'
    else:
        day_cell_selector = f'#task_table > tbody > tr:nth-last-child({index + 2}) .calendar-wrapper td[data-testid="day-{iso_day}"] '

    page.click(day_cell_selector)
