import random
import string

from datetime import date, timedelta


def generate_random_string():
    random_string = ''.join(random.choices(string.ascii_letters, k=10))
    return random_string


new_item_data = ['Chris', 'test notes', True]

from playwright.sync_api import sync_playwright


def select_date(page):
    tomorrow_str = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    day = int(tomorrow_str.split('-')[2])
    """
    Select a date in the table row `row_index` and day number `day` in the calendar widget.
    row_index: zero-based index of the table row
    day: day number to select (1-31)
    """
    # Locate the input in the given row
    row_selector = 'table.task-table > tbody > tr:last-child'
    input_selector = f'{row_selector} .calendar-wrapper .date-input'

    # Click the input to open the calendar popup
    page.click(input_selector)

    # Click the day cell in the calendar
    day_cell_selector = f'{row_selector} .calendar-wrapper .calendar-days td[data-testid="day-{day:02}"]'

    # Since your calendar uses full ISO for data-testid, we need year-month-day
    # Let's get the currently displayed month/year from the calendar header
    month_label_selector = f'{row_selector} .calendar-wrapper .month-label'
    month_year_text = page.locator(month_label_selector).inner_text()
    # month_year_text is like "Oct 2025"
    from datetime import datetime
    displayed_month = datetime.strptime(month_year_text, '%b %Y')
    iso_day = f'{displayed_month.year}-{displayed_month.month:02}-{day:02}'
    day_cell_selector = f'{row_selector} .calendar-wrapper td[data-testid="day-{iso_day}"]'

    page.click(day_cell_selector)
