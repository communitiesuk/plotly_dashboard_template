"""Tests for chart downloads"""

import os

from time import sleep

import pytest

from dash.testing.composite import DashComposite

from constants import (
    HISTORIC_FORECAST_CHART_ID_SENSITIVE,
    HOUSING_FORECAST_PATHNAME_SENSITIVE,
    LATEST_FORECAST_CHART_ID_SENSITIVE,
    NET_ADDITIONAL_DWELLINGS_PATHNAME,
    NET_ADDITIONS_ANNUAL_COMPARISON_CHART_ID,
    NET_ADDITIONS_TRENDS_CHART_ID,
    PROGRESS_CHART_ID,
    PROGRESS_PATHNAME,
    TIME_TAKEN_TO_DEVELOP_PATHNAME,
    APPLICATION_PROGRESS_PATHNAME,
    PLANNING_APPLICATIONS_CHART_ID,
    # UNITS_IN_PROGRESS_CHART_ID_SENSITIVE,
    # UNITS_IN_PROGRESS_PATHNAME,
)
from tests.integration.dashboard_test_utils import DashboardTestUtils


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
def test_chart_downloads(
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
