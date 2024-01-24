"""create_download_button"""
from gov_uk_dashboards.components.plotly import download_button
from dash import html


def create_download_button(button_text: str):
    """
    Creates a styled HTML Div with a download button.
    Args:
    - button_text (str): Text for the button.
    Returns:
    - html.Div: A Div element with a styled download button.
    """
    return html.Div(
        download_button(
            button_text,
            button_id="download-button",
        ),
        style={"display": "flex", "justify-content": "flex-end", "padding": "0px"},
    )
