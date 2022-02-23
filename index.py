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
from gov_uk_dashboards.components.plotly.header import header

from app import app
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


def dashboard_argument_values(url, argument_values):
    """Assigns required arguments for each dashboard"""
    return {x: selected_filters(url).get(x) for x in argument_values}


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
                    df, **dashboard_argument_values(query_string, ["example_dropdown"])
                ),
            }
        }

        for path, route in paths.items():
            if pathname == path:
                return [
                    route["protective_marking"],
                    dashboard_container(
                        [
                            generate_navbar(path, **selected_filters(query_string)),
                            route["dashboard"](),
                        ]
                    ),
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


def generate_navbar(active_page, example_dropdown=None):

    """Creates a navigation bar with current page highlighted"""
    if active_page == "/":
        highlight_page = "Dashboard 1"
    else:
        highlight_page = active_page[1:].replace("-", " ").capitalize()

    page_titles = [
        "Dashboard 1",
    ]
    combined_navbar_links = []
    query_string = dict_to_query_string(example_dropdown=example_dropdown)

    for page in page_titles:
        link = "/" + page.replace(" ", "-").lower()

        if page == highlight_page:
            combined_navbar_links.append(
                navbar_link_active(
                    page,
                    href=link + query_string,
                )
            )
        else:
            combined_navbar_links.append(
                navbar_link(
                    page,
                    href=link + query_string,
                )
            )

    return navbar(combined_navbar_links)
