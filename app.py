"""
Data visualizations for the Department of Levelling Up, Housing and Communities
"""

import dash
from gov_uk_dashboards.template import read_template

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.index_string = read_template()

server = app.server
