"""
Create paths to serve different dashboards.  Add new paths in the display_page callback.
"""

import logging
import os

from dash import dcc, html, Input, Output, State
from gov_uk_dashboards.components.dash.filter_panel import hidden_filter
from gov_uk_dashboards.components.dash.banners import message_banner
from gov_uk_dashboards.components.dash.dashboard_container import dashboard_container
from gov_uk_dashboards.components.dash.phase_banner import phase_banner_with_feedback
from gov_uk_dashboards.components.dash.footer import footer
from gov_uk_dashboards.components.dash.side_navbar import side_navbar
from gov_uk_dashboards.components.dash.header import header
from constants import ACCESSIBILITY_PATHNAME, ACCESSIBILITY_PAGE_NAME

from app import app
from dashboards.template_dashboard import template_dashboard
from dashboards.accessibility_statement import accessibility_statement
from lib.dashboard_page import DashboardPage
from lib.dashboard_storage_and_lookup import DashboardStorageAndLookup
from lib.generate_navbar import generate_side_navbar
from lib.url import selected_filters, dict_to_query_string

app.title = "Template Dashboard"  # UPDATE

app.layout = html.Div(
    [
        html.A(
            "Skip to main content",
            href="#main-content",
            className="govuk-skip-link",
        ),
        header(app.title),
        html.Div(
            id="nav-section",
            style={"display": "none"},
        ),
        html.Div(
            [
                phase_banner_with_feedback(
                    phase="alpha",
                    # #UPDATE Add an e-mail address for people to provide feedback.
                    feedback_link="mailto:<contact e-mail address>?"
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
            **{"aria-live": "polite", "aria-atomic": "true"},
        ),
        footer([dcc.Link(ACCESSIBILITY_PAGE_NAME, href=ACCESSIBILITY_PATHNAME)]),
    ]
)
dashboards = DashboardStorageAndLookup()

dashboards.add_dashboards(
    [
        DashboardPage(
            title="Dashboard 1",
            pathname="/dashboard-1",
            function_to_call=template_dashboard,
            filters=["example_dropdown"],
        ),
        DashboardPage(
            title=ACCESSIBILITY_PAGE_NAME,
            pathname=ACCESSIBILITY_PATHNAME,
            function_to_call=accessibility_statement,
            filters=[],
            hide_from_menu=True,
        ),
    ]
)

all_filters = ["example_dropdown"]


@app.callback(
    Output("protective-marking", "children"),
    Output("page-content", "children"),
    Output("nav-section", "children"),
    Output("feedback-link", "href"),
    Input("url", "pathname"),
    State("url", "search"),
)
def display_page(pathname, query_string):
    """Show the user the correct dashboard for the given path"""
    # UPDATE uncomment when setting up caching
    # if os.environ.get("DFI_TEST_PLATFORM") == "azure":
    #     ClearCachedData()()
    try:
        dashboard = dashboards.get_dashboard_from_pathname(pathname)

        hidden_filters = create_missing_filters_for_dashboard(dashboard)

        side_nav_links = generate_side_navbar(dashboards, pathname, query_string)

        return (
            dashboard.protective_marking,
            dashboard_container(
                [
                    side_navbar(side_nav_links, identifier="navigation-items"),
                    dashboard.display_dashboard(query_string),
                    hidden_filters,
                ]
            ),
            side_navbar(
                side_nav_links,
                identifier="mobile-navigation-items",
                nav_id="mobile-nav-section",
            ),
            "mailto:<contact e-mail address>?"  # #UPDATE Add an e-mail address
            # for people to provide feedback.
            f"subject=Feedback on {app.title} - {dashboard.title}",
        )

    except Exception as exception:
        if os.environ.get("STAGE") == "production":
            dashboard = dashboards.error_dashboard
            logging.exception(exception)
            return (
                dashboard.protective_marking,
                dashboard_container([dashboard.display_dashboard(query_string)]),
                [],
                "mailto:<contact e-mail address>?"  # #UPDATE Add an e-mail address
                # for people to provide feedback.
                f"subject=Feedback on {app.title} - {dashboard.title}",
            )

        raise exception


def create_missing_filters_for_dashboard(dashboard):
    """Finds filters missing from the dashboard & creates div containing matching hidden filters"""
    return html.Div(
        [
            hidden_filter(filter_name)
            for filter_name in all_filters
            if filter_name not in dashboard.filters
        ]
    )


@app.callback(
    Output(component_id="url", component_property="search"),
    Output(component_id="mobile-navigation-items", component_property="children"),
    Output(component_id="navigation-items", component_property="children"),
    State(component_id="url", component_property="pathname"),
    State(component_id="url", component_property="search"),
    Input(component_id="submit-button", component_property="n_clicks"),
    [
        State(component_id=filter_name, component_property="value")
        for filter_name in all_filters
    ],
)
def update_url(
    pathname, query_string, filters_submitted, *filter_values
):  # pylint: disable= unused-argument
    """When the user changes any filter panel elements, update the URL query parameters"""

    dashboard = dashboards.get_dashboard_from_pathname(pathname)

    # We're having to access the query string so that we can only update the value that has changed
    # in the dropdown, otherwise we lose those filters which created dynamically.
    params = selected_filters(query_string)

    for filter_name, filter_value in zip(all_filters, filter_values):
        if filter_name in dashboard.filters:
            params[filter_name] = filter_value

    query_string = dict_to_query_string(**params)

    nav_bar = generate_side_navbar(dashboards, pathname, query_string)

    return query_string, nav_bar, nav_bar
