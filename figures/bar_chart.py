"""bar_chart"""
import plotly.express as px

from lib.govuk_colors import GovUKColors


def bar_chart(
    dataframe,
    xaxis,
    yaxis,
    color=None,
):
    """Create and return a bar chart visualisation from the Plotly Express library"""

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
        color_discrete_sequence=GovUKColors.BLUE_LIGHT_TO_DARK.value,
    )
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig
