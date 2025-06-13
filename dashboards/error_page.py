"""error"""

from dash import html

from gov_uk_dashboards.components.dash import main_content


def error_page():
    """Return a layout showing an error message and a way to contact the Data Dashboards team"""
    data_dashboards_teams_link = (
        "https://teams.microsoft.com/l/team/19"
        "%3aJlkCtA_axw4AtAcLorJqYzHumBGr6cLw-s4hp5hyUQ81%40thread.tacv2"
        "/conversations?groupId=7d4f2fda-52d8-444c-a8cc-9e66e83dcb9d"
        "&tenantId=bf346810-9c7d-43de-a872-24a2ef3995a8 "
    )

    return main_content(
        [
            html.Div(
                [
                    html.H1(
                        "Sorry, there was a problem with that request",
                        className="govuk-heading-l",
                    ),
                    html.P(
                        [
                            "Try refreshing the page, or going back to ",
                            html.A(
                                "the dashboard homepage",
                                href="/",
                                className="govuk-link",
                            ),
                            ".",
                        ],
                        className="govuk-body",
                    ),
                    html.P(
                        [
                            "Contact the Data Dashboards project team on ",
                            html.A(
                                "Microsoft Teams",
                                href=data_dashboards_teams_link,
                                className="govuk-link",
                            ),
                            " if this keeps happening.",
                        ],
                        className="govuk-body",
                    ),
                ],
                style={"align-self": "center"},
            )
        ]
    )
