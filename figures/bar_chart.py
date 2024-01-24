"""bar_chart"""
import plotly.express as px

from gov_uk_dashboards.colours import GovUKColours


def bar_chart(
    dataframe,
    xaxis,
    yaxis,
    color=None,
):
    """Create and return a bar chart visualisation from the Plotly Express library
        Plotly Graph Objects is advised for extra customisation."""

    fig = px.bar(
        dataframe,
        x=xaxis,
        y=yaxis,
        labels={
            xaxis: xaxis,
            yaxis: yaxis,
        },
        range_x=[dataframe[[xaxis]].min(), dataframe[[xaxis]].max()],
        hover_data=dataframe.columns,
        color=color,
        color_discrete_sequence=GovUKColours.BLUE_LIGHT_TO_DARK.value,
    )
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig
