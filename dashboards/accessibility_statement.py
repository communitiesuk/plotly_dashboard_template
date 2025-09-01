"""
A page to give the accessibility statement to the user.
"""

from dash import html
from dash.development.base_component import Component

from gov_uk_dashboards.components.dash import (
    main_content,
    paragraph,
    heading1,
    heading2,
)

from constants import ACCESSIBILITY_PAGE_NAME

EMAIL_ADDRESS = "team_email@org.domain"


def accessibility_statement() -> list[Component]:
    "Function to create page to assist accessibility info for user"
    return main_content(guidance_text(), ACCESSIBILITY_PAGE_NAME)


def guidance_text() -> list[Component]:
    """
    Create the accessibility guidance text

    Returns:
        list[Component]: A list of dash components that make up the guidance text
    """
    return [
        heading1(ACCESSIBILITY_PAGE_NAME),
        paragraph("*Insert accessibility statement here*"),
        paragraph(
            html.A(
                "Email the dashboard team",
                href=f"mailto:{EMAIL_ADDRESS}?Accessibility feedback",
                className="govuk-link",
            )
        ),
        heading2("Enforcement procedure"),
        paragraph(
            children=[
                "The Equality and Human Rights Commission (EHRC) is responsible for enforcing the "
                "Public Sector Bodies (Websites and Mobile Applications) (No. 2) Accessibility "
                "Regulations 2018 (the 'accessibility regulations'). If you're not happy with how "
                "we respond to your complaint, contact the ",
                html.A(
                    "Equality Advisory and Support Service (EASS).",
                    href="https://www.equalityadvisoryservice.com/",
                    className="govuk-link",
                ),
            ]
        ),
        heading2("Compliance status"),
        paragraph(
            children=[
                "This website is partially compliant with the ",
                html.A(
                    "Web Content Accessibility Guidelines version 2.1",
                    href="https://www.w3.org/TR/WCAG21/",
                    className="govuk-link",
                ),
                " AA standard, due to the non-compliances listed below...",
            ]
        ),
    ]
