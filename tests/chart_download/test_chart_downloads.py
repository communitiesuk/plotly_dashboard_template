"""Tests for chart downloads"""

import os

from time import sleep

import pytest

from dash.testing.composite import DashComposite

from tests.integration.dashboard_test_utils import DashboardTestUtils


# UPDATE enable by removing x when ready
@pytest.mark.parametrize(
    "pathname, button_id, sensitivity",
    [
        (
            "/pathname",
            "id",
            "OFFICIAL-",
        ),
    ],
)
def xtest_chart_downloads(
    pathname,
    button_id,
    sensitivity,
    dash_duo: DashComposite,
    dashboard_utils: DashboardTestUtils,
):
    """Test clicking download chart button downloads png with expected filename"""
    dashboard_utils.start_app_and_visit_page(pathname)
    sleep(1)
    button = dash_duo.find_element(f"//button[contains(@id, '{button_id}')]", "XPATH")
    button.click()
    sleep(5)

    download_directory = dash_duo.download_path
    file_name = sensitivity + button_id + "-chart"
    downloaded_png_filepath = os.path.join(download_directory, f"{file_name}.png")

    assert os.path.exists(downloaded_png_filepath)
