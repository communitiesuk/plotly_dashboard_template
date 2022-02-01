"""
Create paths to serve different dashboards.  Add new paths in the display_page callback.
"""
import logging
import os

from dash import dcc, html, Input, Output
import pandas as pd

from app import app
from components.banners import message_banner
from components.dashboard_container import dashboard_container
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
                )
            ],
            className="govuk-width-container",
        ),
    ]
)


@app.callback(
    Output("protective-marking", "children"),
    Output("page-content", "children"),
    Input("url", "pathname"),
    Input("url", "search"),
)
def display_page(pathname, query_string):
    """Show the user the correct dashboard for the given path"""
    try:
        paths = {
            "/": {
                "protective_marking": "OFFICIAL",
                "dashboard": lambda: template_dashboard(
                    df, **selected_filters(query_string)
                ),
            }
        }

        for key, route in paths.items():
            if pathname == key:
                return [
                    route["protective_marking"],
                    dashboard_container(route["dashboard"]()),
                ]
    except Exception as exception:
        if os.environ.get("STAGE") == "production":
            logging.exception(exception)
            return ["OFFICIAL", dashboard_container(error_page())]

        raise exception

    page_not_found = "404"
    return page_not_found


@app.callback(Output("url", "search"), Input("example_dropdown", "value"))
def update_url(example_dropdown):
    """When the user changes any filter panel elements, update the URL query parameters"""
    return dict_to_query_string(example_dropdown=example_dropdown)
