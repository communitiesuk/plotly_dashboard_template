"""
A test bar chart dashboard
"""
from components.dropdowns import dropdown
from components.filter_panel import filter_panel, hidden_filter
from components.main_content import main_content
from components.navbar import navbar, navbar_link_active
from components.row_component import row_component
from components.visualisation_title import format_visualisation_title
from components.visualisation_commentary import format_visualisation_commentary


def template_dashboard(
):
    """Create and return the dashboard layout for display in the application."""
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
                            label="Metric",
                            element_id="metric",
                            options=[
                                {"label": metric, "value": metric}
                                for metric in {"option 1", "option 2"}
                            ],
                            selected="option 2",
                            optionHeight=50,
                        ),
                        hidden_filter(html_id="comparison_local_authority"),
                        hidden_filter(html_id="comparison_metric"),
                    ],
                ),
                format_visualisation_title("Visualisation title"),
                format_visualisation_commentary("Calculated commentary"),
                row_component("Dashboard content"),
            ],
        ),
    ]

# ToDo: Add a graph.
# ToDo: hook up dropdown with graph.