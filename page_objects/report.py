from tests.conftest import logger
from .dashboard import DashboardPage
from playwright.sync_api import expect



class ReportPage:

    def __init__(self, page):
        self.page = page

    def verify_no_outstanding_tasks_message(self):
        expect(self.page.get_by_text('There are no outstanding tasks')).to_be_visible()

    def verify_tasks_by_assignee_report(self):
        expect(self.page.get_by_text('Tasks by Assignee Report')).to_be_visible()

