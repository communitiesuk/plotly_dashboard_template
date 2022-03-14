"""
A test bar chart dashboard
"""
from dash import dcc
import pandas as pd

from gov_uk_dashboards.components.plotly.dropdowns import dropdown
from gov_uk_dashboards.components.plotly.filter_panel import filter_panel
from gov_uk_dashboards.components.plotly.main_content import main_content
from gov_uk_dashboards.components.plotly.row_component import row_component
from gov_uk_dashboards.components.plotly.visualisation_title import (
    format_visualisation_title,
)
from gov_uk_dashboards.components.plotly.visualisation_commentary import (
    format_visualisation_commentary,
)
from gov_uk_dashboards.components.plotly.card import card
from gov_uk_dashboards.components.plotly.graph import graph

from figures.bar_chart import bar_chart

data = {
    "Category": ["Category 1", "Category 2", "Category 3"],
    "Value": [30, 15, 20],
}
df = pd.DataFrame(data)


def template_dashboard(example_dropdown="option 1"):
    """Create and return the dashboard layout for display in the application."""

    barchart = bar_chart(df, "Category", "Value", color="Category")
    barchart_dash = graph(element_id="example bar chart", figure=barchart)
    dashboard_content = [card(barchart_dash)]

    return main_content(
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
    )
