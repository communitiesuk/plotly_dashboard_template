"""
Create paths to serve different dashboards.  Add new paths in the display_page callback.
"""
import logging
import os

from dash import dcc, html, Input, Output
import pandas as pd

from gov_uk_dashboards.components.plotly.navbar import (
    navbar_link_active,
    navbar_link,
    navbar,
)
from gov_uk_dashboards.components.plotly.banners import message_banner
from gov_uk_dashboards.components.plotly.dashboard_container import dashboard_container
from gov_uk_dashboards.components.plotly.phase_banner import phase_banner_with_feedback

from app import app
from components.header import header
from dashboards.error_page import error_page
from dashboards.template_dashboard import template_dashboard
from lib.url import selected_filters, dict_to_query_string


data = {
    "Category": ["Category 1", "Category 2", "Category 3"],
    "Value": [30, 15, 20],
}
df = pd.DataFrame(data)

app.title = "Template Dashboard"

app.layout = html.Div(
    [
        header(app.title),
        html.Div(
            [
                phase_banner_with_feedback(
                    phase="alpha",
                    feedback_link="mailto:<contact e-mail address>?"  # Add an e-mail address for people to provide feedback.
                    f"subject=Feedback on {app.title}",
                    link_id="feedback-link",
                ),
                html.Div(
                    [
                        dcc.Location(id="url", refresh=False),
                        message_banner(
                            category="UPDATE",
                            message="This is an example update banner",
                        ),
                        html.Div(id="page-content"),
                    ],
                    className="govuk-main-wrapper--auto-spacing govuk-!-padding-top-2",
                ),
            ],
            className="govuk-width-container",
        ),
    ]
)


def dashboard_argument_values(url, argument_values):
    """Assigns required arguments for each dashboard"""
    return {x: selected_filters(url).get(x) for x in argument_values}


@app.callback(
    Output("protective-marking", "children"),
    Output("page-content", "children"),
    Output("feedback-link", "href"),
    Input("url", "pathname"),
    Input("url", "search"),
)
def display_page(pathname, query_string):
    """Show the user the correct dashboard for the given path"""
    try:
        paths = {
            "/": {
                "protective_marking": "OFFICIAL",
                "title": "Dashboard 1",
                "dashboard": lambda: template_dashboard(
                    df, **dashboard_argument_values(query_string, ["example_dropdown"])
                ),
            },
            "/dashboard-1": {
                "protective_marking": "OFFICIAL",
                "title": "Dashboard 1",
                "dashboard": lambda: template_dashboard(
                    df, **dashboard_argument_values(query_string, ["example_dropdown"])
                ),
            },
        }

        for path, route in paths.items():
            if pathname == path:
                return [
                    route["protective_marking"],
                    dashboard_container(
                        [
                            generate_navbar(
                                active_page=route["title"],
                                pages_info=paths,
                                **selected_filters(query_string),
                            ),
                            route["dashboard"](),
                        ]
                    ),
                    "mailto:<contact e-mail address>?"  # Add an e-mail address for people to provide feedback.
                    f"subject=Feedback on {app.title} - {route['title']}",
                ]
    except Exception as exception:
        if os.environ.get("STAGE") == "production":
            logging.exception(exception)
            return ["OFFICIAL", dashboard_container(error_page())]

        raise exception

    page_not_found = "404"
    return page_not_found


def generate_navbar(active_page: str, pages_info: dict, **query_filters):
    """Creates a navigation bar with current page highlighted"""

    query_string = create_defaulted_query_string(**query_filters)

    navbar_links = [
        navbar_link_active(
            page_info["title"],
            href=page_key + query_string,
        )
        if page_info["title"] == active_page
        else navbar_link(
            page_info["title"],
            href=page_key + query_string,
        )
        for page_key, page_info in pages_info.items()
        if page_key != "/"
    ]

    return navbar(navbar_links)


def create_defaulted_query_string(example_dropdown=None):
    """Create a query string with default parameters unless specified otherwise"""
    return dict_to_query_string(example_dropdown=example_dropdown)


@app.callback(
    Output("url", "search"),
    Input("example_dropdown", "value"),
)
def update_url(*query_filters):
    """When the user changes any filter panel elements, update the URL query parameters"""
    return create_defaulted_query_string(*query_filters)
