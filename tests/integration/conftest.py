"""Pytest automatically loads this file before executing tests"""

# pylint: disable=unused-import
from tests.plugins import (
    data_folder_location,
    setup_chromedriver_for_browser_tests,
    setup_proxy_for_browser_tests,
    get_dashboard_utils,
    chromedriver,
    cleanup_dash_duo_driver,
)

# pylint: enable=unused-import
