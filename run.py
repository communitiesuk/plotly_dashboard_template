"""
The entry point for the application to be run from the command line.
"""

from index import app

# Required for use in staging and production
from app import server  # pylint: disable=unused-import

if __name__ == "__main__":
    HOST_REQUIRED_BY_DAP = "0.0.0.0"
    PORT_REQUIRED_BY_DAP = 8080
    app.run_server(host=HOST_REQUIRED_BY_DAP, port=PORT_REQUIRED_BY_DAP, debug=True)
