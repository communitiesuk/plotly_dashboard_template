"""
Data visualizations for the Department of Levelling Up, Housing and Communities
"""

import dash
from gov_uk_dashboards.assets import get_assets_folder
from gov_uk_dashboards.lib.logging import configure_logging
from gov_uk_dashboards.template import read_template
from gov_uk_dashboards.lib.http_headers import setup_application_http_response_headers

# UPDATE uncomment when setting up sentry
# if os.environ.get("STAGE") == "production":
#     sentry.configure_sentry()
configure_logging()

app = dash.Dash(__name__, assets_folder=get_assets_folder(), update_title=None)
app.config.suppress_callback_exceptions = True
app.index_string = read_template()

server = app.server

setup_application_http_response_headers(app)
