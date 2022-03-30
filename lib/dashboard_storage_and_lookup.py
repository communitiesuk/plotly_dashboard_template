"""DashboardStorageAndLookup"""

from lib.dashboard_page import DashboardPage
from dashboards.error_page import error_page


class DashboardStorageAndLookup:
    """A class for storing and looking up DashboardPages"""

    def __init__(self):
        self.dashboards = {}
        self.home_dashboard = None
        self.error_dashboard = DashboardPage(
            title="Error page", pathname="", function_to_call=error_page, filters=[]
        )

    def add_dashboard(self, dashboard: DashboardPage) -> None:
        """Adds a dashboard to the DashboardStorageAndLookup
        If no home dashboard is set, sets it to the passed dashboard"""
        self.dashboards[dashboard.pathname] = dashboard
        if not self.home_dashboard:
            self.home_dashboard = dashboard

    def add_dashboards(self, dashboards: list[DashboardPage]) -> None:
        """Adds a list of dashboards for convenience"""
        for dashboard in dashboards:
            self.add_dashboard(dashboard)

    def get_dashboard_from_pathname(self, pathname) -> DashboardPage:
        """Return the dashboard page matching the specified pathname
        If the pathname is '/', returns the home dashboard."""
        if pathname == "/":
            return self.home_dashboard
        if pathname in self.dashboards:
            return self.dashboards[pathname]
        return self.error_dashboard

    def get_dashboards(self) -> list[DashboardPage]:
        """Returns list of stored dashboards"""
        return [dashboard for _, dashboard in self.dashboards.items()]
