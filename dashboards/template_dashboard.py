"""
A test bar chart dashboard
"""

from dash import Output, Input, State, html, dcc
import polars as pl

from uk_gov_dash_components.Dropdown import Dropdown
from gov_uk_dashboards import colours
from gov_uk_dashboards.components.dash.apply_and_reset_filters_buttons import (
    apply_and_reset_filters_buttons,
)
from gov_uk_dashboards.components.dash.main_content import main_content
from gov_uk_dashboards.components.dash.visualisation_title import (
    format_visualisation_title,
)
from gov_uk_dashboards.components.dash.visualisation_commentary import (
    format_visualisation_commentary,
)

from app import app


from lib.local_authority import LocalAuthority

data = {
    # authorities should be identified via ONS code rather than name to avoid ambiguity.
    # e.g. here two authorities called "LA2" would have different data for different codes
    # this can happen if authority changes type or area but keeps same name.
    # class LocalAuthority can be used to make this easier to work with in the code.
    "LA_code": ["E061", "E062", "E071", "E063"],
    "LA_name": ["LA1", "LA2", "LA3", "LA2"],
    "Value": [30, 15, 20, 18],
}
df = pl.DataFrame(data)


def template_dashboard(example_dropdown="option 1"):
    """Create and return the dashboard layout for display in the application."""

    dropdown_options = [
        {"label": data["LA_name"][data_index], "value": data["LA_code"][data_index]}
        for data_index in range(len(data["LA_code"]))
    ]

    return main_content(
        [
            html.H1("Dashboard 1 Page Title"),
            html.Div(
                [
                    Dropdown(
                        label="Example dropdown",
                        id="example_dropdown",
                        source=dropdown_options,
                        value=example_dropdown,
                    ),
                    apply_and_reset_filters_buttons(),
                ],
                className="container-class",
                style={
                    "backgroundColor": colours.GovUKColours.LIGHT_GREY.value,
                    "padding": "20px 20px 10px 20px",
                    "maxWidth": "800px",
                },
            ),
            format_visualisation_title("Visualisation title"),
            html.Div(
                id="example_commentary",
            ),
            dcc.Download(id="download-data-as-csv"),
        ],
        "Dashboard 1 Page Title",
    )


@app.callback(
    Output(component_id="example_commentary", component_property="children"),
    State(component_id="example_dropdown", component_property="value"),
    Input(component_id="submit-button", component_property="n_clicks"),
)
def update_example_commentary(
    local_authority_code_for_dropdown_selection, filters_submitted
):
    """Example of how to update commentary with selected option."""
    # pylint: disable = unused-argument
    if not local_authority_code_for_dropdown_selection:
        return format_visualisation_commentary("No authority selected.")

    selected_row = df.filter(
        pl.col("LA_code") == local_authority_code_for_dropdown_selection
    )
    la_name = selected_row.select("LA_name").item()

    # create authority object based on selected code from dropdown and the corresponding name

    selected_authority = LocalAuthority(
        local_authority_code_for_dropdown_selection, la_name
    )
    return format_visualisation_commentary(
        f"{selected_authority.name} ({selected_authority.ons_code}) selected."
    )
