from tests.conftest import logger
from .dashboard import DashboardPage
from playwright.sync_api import expect


class ReportPage:

    def __init__(self, page):
        self.page = page

    def verify_no_outstanding_tasks_message(self):
        expect(self.page.get_by_text('There are no outstanding tasks')).to_be_visible()

    def verify_tasks_by_assignee_report(self, db_result):
        expect(self.page.get_by_text('Tasks by Assignee Report')).to_be_visible()
        if len(db_result) == 0:
            expect(self.page.get_by_text('There are no tasks by assignee')).to_be_visible()
            return

        count_totals = 0
        count_checks = self.page.locator('button').count()
        row = self.page.locator("tr", has=self.page.locator("td:first-child", has_text="Totals"))
        cells = row.locator('td').all()
        for cell in cells:
            if cell.inner_text().strip().isdigit():
                count_totals += int(cell.inner_text().strip())
        logger.info(f'Count checks: {count_checks}')
        logger.info(f'Count totals: {count_totals}')
        assert count_checks == count_totals

        headers = self.page.locator('th').all()
        headers_sliced = headers[1:]
        row_totals_sliced = cells[1:]

        gui_results = []
        for i in range(len(headers_sliced)):
            if headers_sliced[i].inner_text().strip() == 'Unassigned':
                gui_results.append(
                    ('', int(row_totals_sliced[i].inner_text().strip())))
            else:
                gui_results.append(
                    (headers_sliced[i].inner_text().strip(), int(row_totals_sliced[i].inner_text().strip())))
        logger.info(f'GUI totals: {sorted(gui_results)}')

        sorted_gui_results = sorted(gui_results)
        sorted_db_results = sorted(db_result)

        #for result in db_result:
         #   assert result in gui_results

        for i in range(len(sorted_db_results)):
            assert sorted_db_results[i] == sorted_gui_results[i]
