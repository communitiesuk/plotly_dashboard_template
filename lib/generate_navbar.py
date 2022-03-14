"""generate_navbar"""
from dash import html

from gov_uk_dashboards.components.plotly.navbar import (
    navbar_link,
    navbar_link_active,
    navbar,
)

from lib.dashboard_storage_and_lookup import DashboardStorageAndLookup


def generate_navbar(
    dashboards: DashboardStorageAndLookup, pathname: str, query_string: str
) -> html.Nav:
    """Creates a navigation bar with current page highlighted
    Uses the DashboardStorageAndLookup list of pages"""
    cur_page = dashboards.get_dashboard_from_pathname(pathname)

    navbar_links = [
        navbar_link_active(
            page.title,
            href=page.pathname + query_string,
        )
        if page is cur_page
        else navbar_link(
            page.title,
            href=page.pathname + query_string,
        )
        for page in dashboards.get_dashboards()
    ]

    return navbar(navbar_links)
