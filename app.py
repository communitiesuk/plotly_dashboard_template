"""
Data visualizations for the Department of Levelling Up, Housing and Communities
"""

import dash
from gov_uk_dashboards.assets import get_assets_folder
from gov_uk_dashboards.lib.http_headers import setup_application_http_response_headers
from gov_uk_dashboards.lib.logging import configure_logging
from gov_uk_dashboards.template import read_template
#from gov_uk_dashboards.lib.enable_basic_auth import enable_basic_auth

configure_logging()

app = dash.Dash(__name__, assets_folder=get_assets_folder(), update_title=None)
app.config.suppress_callback_exceptions = True
app.index_string = read_template()

server = app.server

#enable_basic_auth(app)

setup_application_http_response_headers(app)