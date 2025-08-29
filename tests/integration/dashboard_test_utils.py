"""
Test utils for dashboard testing
"""

import dash
from dash.testing.composite import DashComposite


class DashboardTestUtils:
    """Class for dashboard test utils"""

    def __init__(self, dash_duo: DashComposite):
        self.dash_duo = dash_duo

    def start_app(self) -> dash.Dash:
        """
        1. Start server
        """

        from index import app  # pylint: disable=import-outside-toplevel

        test_server_port_to_avoid_conflicts_with_dev_server = 8052
        self.dash_duo.server(
            app, port=test_server_port_to_avoid_conflicts_with_dev_server
        )

        return app

    def start_app_and_visit_page(self, url: str) -> dash.Dash:
        """
        1. Start server
        2. Visit URL
        """

        app = self.start_app()
        self.dash_duo.server_url = self.dash_duo.server.url + url

        return app

    def select_first_option_in_dropdown(self, selector: str):
        """
        Select the first option in the dropdown matching the selector
        """
        return self.select_option_in_dropdown(selector, 0)

    def select_option_in_dropdown(self, selector: str, index=0):
        """
        Select the option matching the index provided
        """
        option_selector = selector + "__option--" + str(index)
        return self.dash_duo.find_element(option_selector)


def run_smoke_test_for_page(
    dash_duo: DashComposite,
    dashboard_utils: DashboardTestUtils,
    pathname: str,
    wait_selector: str = '[id^="main-content"]',
    timeout: int = 30,
):
    """Reusable smoke test to check that a page loads without browser console errors."""
    dashboard_utils.start_app_and_visit_page(pathname)
    dash_duo.wait_for_element(wait_selector, timeout=timeout)

    assert dash_duo.get_logs() in ([], None), "browser console should contain no error"
