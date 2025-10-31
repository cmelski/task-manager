from tests.conftest import logger
from .dashboard import DashboardPage
from playwright.sync_api import expect


class ReportPage:

    def __init__(self, page):
        self.page = page
