"""
A test bar chart dashboard
"""
from dash import Output, Input, html
import pandas as pd

from uk_gov_dash_components.Dropdown import Dropdown
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

from app import app

from figures.bar_chart import bar_chart

from lib.local_authority import LocalAuthority

data = {
    # authorities should be identified via ONS code rather than name to avoid ambiguity.
    # e.g. here two authorities called "LA2" would have different data for different codes
    # this can happen if authority changes type or area but keeps same name.
    # class LocalAuthority can be used to make this clearer.
    "LA_code": ["E061", "E062", "E071", "E063"],
    "LA_name": ["LA1", "LA2", "LA3", "LA2"],
    "Value": [30, 15, 20, 18],
}
df = pd.DataFrame(data)


def template_dashboard(example_dropdown="option 1"):
    """Create and return the dashboard layout for display in the application."""

    barchart = bar_chart(df, "LA_name", "Value", color="LA_code")
    barchart_dash = graph(element_id="example bar chart", figure=barchart)
    dashboard_content = [card(barchart_dash)]

    dropdown_options = [
        {"label": data["LA_name"][data_index], "value": data["LA_code"][data_index]}
        for data_index in range(len(data["LA_code"]))
    ]

    return main_content(
        [
            filter_panel(
                [
                    Dropdown(
                        label="Example dropdown",
                        id="example_dropdown",
                        source=dropdown_options,
                        value=example_dropdown,
                    ),
                ],
            ),
            format_visualisation_title("Visualisation title"),
            html.Div(
                id="example_commentary",
            ),
            row_component(dashboard_content),
        ],
    )


@app.callback(
    Output(component_id="example_commentary", component_property="children"),
    Input(component_id="example_dropdown", component_property="value"),
)
def update_example_commentary(example_dropdown):
    """Example of how to update commentary with selected option."""

    # create authority object based on selected code from dropdown and the corresponding name
    selected_authority = LocalAuthority(
        example_dropdown, df[df["LA_code"] == example_dropdown]["LA_name"].iloc[0]
    )
    return format_visualisation_commentary(f"{selected_authority.name} selected.")
