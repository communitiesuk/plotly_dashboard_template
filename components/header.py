"""header"""
from dash import html


def header(title):
    """
    The header component, shared across all dashboard views.

    Based on the header component provided by the GOV.UK Design System.
    https://design-system.service.gov.uk/components/header/
    """
    return html.Header(
        html.Div(
            html.Div(
                [
                    html.Img(
                        src="assets\\images\\DLUHC_WHITE_Master_AW_sm.png",
                        srcSet="assets\\images\\DLUHC_WHITE_Master_AW_sm.png 490w",
                        sizes="(min-width: 600px) 200px, 30vw",
                        className="header-image",
                        style={"max-width": "200px"},
                    ),
                    html.A(
                        title,
                        href="/",
                        className=" ".join(
                            [
                                "govuk-header__link",
                                "govuk-header__link--service-name",
                                "dashboard-title",
                            ],
                        ),
                    ),
                    html.Strong(
                        "OFFICIAL",
                        className="govuk-tag protective-marking",
                        id="protective-marking",
                    ),
                ],
                className="govuk-header__content",
            ),
            className="govuk-header__container govuk-width-container",
        ),
        style={"alignItems": "center", "justifyContent": "center"},
        className="govuk-header",
        role="banner",
        **{"data-module": "govuk-header"},
    )
