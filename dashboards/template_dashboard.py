"""
A dashboard that shows statistics about housing supply in England on a choropleth map.
"""
from dash import dcc

from components.dropdowns import dropdown
from components.filter_panel import filter_panel
from components.main_content import main_content
from components.navbar import navbar, navbar_link_active
from components.row_component import row_component
from components.visualisation_title import format_visualisation_title
from components.visualisation_commentary import format_visualisation_commentary
from components.card import card

from figures.bar_chart import bar_chart


def template_dashboard(df, example_dropdown="option 1"):
    """Create and return the dashboard layout for display in the application."""

    barchart = bar_chart(df, "Category", "Value", color="Category")
    barchart_dash = dcc.Graph(id="example bar chart", responsive=True, figure=barchart)
    dashboard_content = [card(barchart_dash)]

    return [
        navbar(
            [
                navbar_link_active(
                    "Dashboard 1",
                    href="/",
                )
            ]
        ),
        main_content(
            [
                filter_panel(
                    [
                        dropdown(
                            label="Example dropdown",
                            element_id="example_dropdown",
                            options=[
                                {"label": metric, "value": metric}
                                for metric in ["option 1", "option 2"]
                            ],
                            selected=example_dropdown,
                            optionHeight=50,
                        ),
                    ],
                ),
                format_visualisation_title("Visualisation title"),
                format_visualisation_commentary(f"{example_dropdown} selected."),
                row_component(dashboard_content),
            ],
        ),
    ]
