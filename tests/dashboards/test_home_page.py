"""Integration test for home page"""
from dash.testing.composite import DashComposite

from tests.dashboards.dashboard_test_utils import DashboardTestUtils


def test_home_page_loads_without_error(
    dash_duo: DashComposite, dashboard_utils: DashboardTestUtils
):
    """A smoke test to make sure the dashboard loads and has no error messages (exceptions)"""

    dashboard_utils.start_app_and_visit_page("/")
    dash_duo.wait_for_element("#main-content")

    assert dash_duo.get_logs() in ([], None), "browser console should contain no error"
