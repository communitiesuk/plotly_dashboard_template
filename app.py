"""
Data visualizations for the Department of Levelling Up, Housing and Communities
"""

import dash
from gov_uk_dashboards.template import read_template
from gov_uk_dashboards.lib.http_headers import setup_application_http_response_headers
from gov_uk_dashboards.lib.logging import configure_logging

configure_logging()

app = dash.Dash(__name__, update_title=None)
app.config.suppress_callback_exceptions = True
app.index_string = read_template()

server = app.server

setup_application_http_response_headers(app)