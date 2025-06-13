"""generate_navbar"""

from dash import html

from gov_uk_dashboards.components.dash.side_navbar import (
    side_navbar_link,
    side_navbar_link_active,
)
from lib.dashboard_page import DashboardPage


from lib.dashboard_storage_and_lookup import DashboardStorageAndLookup


def generate_side_navbar(
    dashboards: DashboardStorageAndLookup, pathname: str, query_string: str
) -> html.Nav:
    """Creates a navigation bar with current page highlighted
    Uses the DashboardStorageAndLookup list of pages"""
    cur_page = dashboards.get_dashboard_from_pathname(pathname)

    def exclude_hidden_from_menu(dash: DashboardPage):
        return not dash.hide_from_menu

    navbar_links = [
        (
            side_navbar_link_active(
                page.title,
                href=page.pathname + query_string,
            )
            if page is cur_page
            else side_navbar_link(
                page.title,
                href=page.pathname + query_string,
            )
        )
        for page in filter(exclude_hidden_from_menu, dashboards.get_dashboards())
    ]

    return navbar_links
