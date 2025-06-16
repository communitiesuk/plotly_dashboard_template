"""Test map downloads"""

import os
from time import sleep

from dash.testing.composite import DashComposite
import pytest

from tests.integration.dashboard_test_utils import DashboardTestUtils


# UPDATE enable by removing x when ready
@pytest.mark.parametrize(
    "pathname, map_id",
    [
        ("/pathname", "id"),
    ],
)
def xtest_map_downloads(
    dash_duo: DashComposite, dashboard_utils: DashboardTestUtils, pathname, map_id
):
    """Test clicking download map button downloads png with expected filename"""

    dashboard_utils.start_app_and_visit_page(pathname)

    button = dash_duo.find_element(f"//button[contains(@id, '{map_id}')]", "XPATH")

    button.click()
    sleep(5)

    download_directory = dash_duo.download_path
    downloaded_png_filepath = os.path.join(download_directory, f"{map_id}.png")
    assert os.path.exists(downloaded_png_filepath)
