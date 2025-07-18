"""Pytest automatically loads this file before executing tests"""

import os
from io import BytesIO
from pathlib import Path
from typing import Callable, Any, Optional
from time import sleep
import chromedriver_autoinstaller as chromedriver
from playwright.sync_api import Page
from selenium.common.exceptions import WebDriverException
from PIL import Image, ImageDraw, ImageFont
import pytest

from tests.integration.dashboard_test_utils import DashboardTestUtils
from tests.visual.visual_test_utils import (
    save_failed_snapshot_comparison_images,
    images_are_same,
    get_expected_snapshot_file,
    get_snapshots_failure_folder,
    save_actual_snapshot_to_failure_folder_and_fail_test,
)


@pytest.fixture(autouse=True)
def data_folder_location():
    """
    If set the DATA_FOLDER_LOCATION is used by absolute_path to specify where
    data files are located.

    See PyTest docs on the yield
    https://docs.pytest.org/en/7.1.x/how-to/fixtures.html#yield-fixtures-recommended
    """
    if os.environ.get("USE_REAL_DATA") != "true":
        os.environ["STAGE"] = "testing"
        tests_dashboards_folder = os.path.dirname(__file__)
        os.environ["DATA_FOLDER_LOCATION"] = tests_dashboards_folder

    try:
        yield
    finally:
        if "DATA_FOLDER_LOCATION" in os.environ:
            del os.environ["DATA_FOLDER_LOCATION"]


@pytest.fixture(
    autouse=True,
    params=["real"] if os.getenv("USE_REAL_DATA") == "true" else ["test", "real"],
)
def data_tests_folder_location(request):
    """
    If env variable USE_REAL_DATA=="true" fixture uses real data directory only.

    Otherwise:
    - fixture will toggle between the test and real data directories depending on
        the `request.param`.
    - Sets the DATA_FOLDER_LOCATION env variable for test data.
    - If DATA_FOLDER_LOCATION is set the DATA_FOLDER_LOCATION is used by absolute_path to specify
        where data files are located.
    - Yields the test data folder for data_tests when the real data folder does not exist
        (as in github), but yields real and test data folders when both exist.

    Note: to see which tests are being skipped and the reason, run:
    python -u -m pytest <test_location> -ra -v

    See PyTest docs on the yield
    https://docs.pytest.org/en/7.1.x/how-to/fixtures.html#yield-fixtures-recommended
    """

    if request.param == "real":
        if os.path.exists("data/housing"):
            pass
        else:
            pytest.skip(
                "Real data directory 'data/housing' not found. Skipping test for real data."
            )

    else:  # request.param == "test"
        os.environ["STAGE"] = "testing"
        tests_dashboards_folder = os.path.dirname(__file__)
        os.environ["DATA_FOLDER_LOCATION"] = tests_dashboards_folder
        if os.path.exists(f"{tests_dashboards_folder}/data/housing"):
            pass
        else:
            pytest.skip(
                f"Test data directory '{tests_dashboards_folder}/data/housing' not found."
                "Skipping test for test data."
            )

    try:
        yield
    finally:
        if "DATA_FOLDER_LOCATION" in os.environ:
            del os.environ["DATA_FOLDER_LOCATION"]


@pytest.fixture(scope="session", autouse=True)
def setup_chromedriver_for_browser_tests():
    """
    Chrome within the DAP is updated automatically, and so our test suite needs to work across
    both the latest and previous latest versions of chrome.

    You need a matching version of Chrome Driver for your version of Chrome.
    This code should install the matching version of Chrome Driver depending on the version of
    Chrome you have installed in your DAP Workspace.
    """
    chromedriver.install()


@pytest.fixture(scope="session", autouse=True)
def setup_proxy_for_browser_tests():
    """
    Bypassing localhost from accessing the proxy prevents the following error when running
    browser tests, i.e. those within the tests/dashboards folder.
        dash.testing.errors.ServerCloseError: Cannot stop server within 3s timeout

    Taken from: https://community.plotly.com/t/dash-testing-server-not-closing/49222
    """
    os.environ["no_proxy"] = "localhost"


@pytest.fixture(autouse=True, name="dashboard_utils")
def get_dashboard_utils(dash_duo):
    """
    Register the test utils as a pytest fixture
    """
    return DashboardTestUtils(dash_duo)


@pytest.fixture(autouse=True)
def cleanup_dash_duo_driver(dash_duo):
    """Quit dash duo after use in test"""
    yield
    if dash_duo.driver and dash_duo.driver.service.is_connectable():
        try:
            dash_duo.driver.quit()
        except WebDriverException:
            pass


@pytest.fixture
def assert_valid_snapshot(
    dashboard_utils: DashboardTestUtils, page: Page, assert_snapshot: Callable
) -> Callable:
    """Check the page matches the saved snapshot"""

    def handle_tabs(tab_to_select):
        # wait for tabs that are not selected and select all tabs that match tab_to_select
        unselected_tab_class = ".tab-button"
        target_tab_selector = f'{unselected_tab_class}:has-text("{tab_to_select}")'
        page.wait_for_selector(target_tab_selector)
        target_tabs = page.query_selector_all(target_tab_selector)
        for tab in target_tabs:
            tab.click()

    def handle_accordions():
        # wait for accordions and then open all accordions that are closed
        closed_accordion_class = ".govuk-accordion-nav__chevron--down"
        accordion_button_selector = ".accordion-button"
        page.wait_for_selector(accordion_button_selector)
        closed_accordions = page.query_selector_all(closed_accordion_class)
        for accordion in closed_accordions:
            accordion.click()

    def handle_details():
        # Wait for all detail components to be visible on the page
        detail_component_selector = ".govuk-details"
        page.wait_for_selector(detail_component_selector)

        # Get all detail components
        detail_components = page.query_selector_all(detail_component_selector)

        # Iterate over each detail component and perform the desired action
        for detail_component in detail_components:
            detail_component.click()

        # go back to top
        # page.focus(".govuk-header__content")
        page.hover(".govuk-header__content")
        sleep(1)

    def handle_navbar_sections():
        navbar = page.locator("#navigation-items")  # Target the desktop navbar by ID
        page.wait_for_selector("#navigation-items")
        navbar_groups = navbar.locator(
            ".moj-side-navigation__item--collapsed"
        ).all_inner_texts()  # identify navbar groups through class

        for group in navbar_groups:
            item = navbar.get_by_text(
                group, exact=True
            )  # Search for the item by its text inside that navbar
            item.click()

    def visit_page_and_assert_snapshot(
        url: str,
        selector: str,
        page_with_accordions: bool = False,
        page_with_tabs: bool = False,
        tab_to_select: Optional[str] = None,
        page_with_details: bool = False,
        expand_all_navbar_sections: bool = False,
    ):
        dashboard_utils.start_app()
        page.set_viewport_size({"width": 1920, "height": 1200})
        page.goto(dashboard_utils.dash_duo.server.url + url)
        page.evaluate(
            "window.scrollTo(0, 0)"
        )  # add 09/01/25 to try fix sticky banner visual test bug

        if page_with_tabs:
            handle_tabs(tab_to_select)

        if page_with_accordions:
            handle_accordions()

        if page_with_details:
            handle_details()

        if expand_all_navbar_sections:
            handle_navbar_sections()

        page.wait_for_selector(selector)
        sleep(6)
        assert_snapshot(page.screenshot(full_page=True, scale="css"))

    return visit_page_and_assert_snapshot


@pytest.fixture(autouse=True, name="assert_snapshot")
def assert_snapshot_matches_baseline(pytestconfig: Any, request: Any) -> Callable:
    """Check the current snapshot matches the saved one"""
    test_name = str(Path(request.node.name.replace("/", "")))
    test_file_name = Path(os.path.basename(Path(request.node.fspath))).stem

    update_snapshot = pytestconfig.getoption("--update-snapshots")
    fail_fast = pytestconfig.getoption("--fail-fast")

    def assert_new_snapshot_matches_previous_version(new_snapshot: bytes) -> None:
        snapshots_failure_folder = get_snapshots_failure_folder(
            request, test_name, test_file_name
        )

        expected_snapshot_file = get_expected_snapshot_file(
            request, test_name, test_file_name
        )
        actual_img = Image.open(BytesIO(new_snapshot))

        if not expected_snapshot_file.exists():
            if update_snapshot:
                create_new_snapshot(expected_snapshot_file, new_snapshot)
                return
            save_actual_snapshot_to_failure_folder_and_fail_test(
                snapshots_failure_folder, actual_img
            )

        expected_img = Image.open(expected_snapshot_file)
        if expected_img.size == actual_img.size:
            diff_img = Image.new("RGBA", actual_img.size)
        else:
            diff_img = create_difference_image_for_different_sizes(
                actual_img, expected_img
            )

        if images_are_same(actual_img, expected_img, diff_img, fail_fast):
            return

        save_failed_snapshot_comparison_images(
            actual_img, expected_img, diff_img, snapshots_failure_folder
        )

        if update_snapshot:
            create_new_snapshot(expected_snapshot_file, new_snapshot)
            return

        pytest.fail(
            "--> Snapshots DO NOT match! Please look at the "
            f"differences look in {snapshots_failure_folder}"
        )

    return assert_new_snapshot_matches_previous_version


def create_new_snapshot(expected_snapshot_file: str, new_snapshot: bytes) -> None:
    """Create a new snapshot in the snapshots folder"""
    expected_snapshot_file.write_bytes(new_snapshot)
    print("--> New snapshot(s) created. Please review images")


def create_difference_image_for_different_sizes(actual_img, expected_img):
    """Create a difference image with the two images side by side which allows differences in
    sizes of the images to be seen more clearly when this causes snapshot differences.

    Args:
        actual_img : The actual snapshot of the page
        expected_img : What the expectation was for the snapshot of the page

    Returns:
        The side by side diff image with images labelled and blank space filled in red.
    """
    title_space = 40
    width = actual_img.width + expected_img.width
    max_height = max(actual_img.height, expected_img.height) + title_space

    diff_img = Image.new("RGB", (width, max_height), color=(255, 255, 255))
    title_font = ImageFont.load_default()
    text_color = (0, 0, 0)

    # Position and draw the "actual" and expected titles
    draw = ImageDraw.Draw(diff_img)
    draw.text((10, 10), "Actual", fill=text_color, font=title_font)
    draw.text((actual_img.width + 10, 10), "Expected", fill=text_color, font=title_font)

    # Paste the actual and expected images below the titles
    diff_img.paste(actual_img, (0, title_space))
    diff_img.paste(expected_img, (actual_img.width, title_space))

    # Fill the extra space below the shorter image (if any) with red
    if actual_img.height < max_height:
        draw.rectangle(
            [(0, title_space + actual_img.height), (actual_img.width, max_height)],
            fill="red",
        )
    if expected_img.height < max_height:
        draw.rectangle(
            [
                (actual_img.width, title_space + expected_img.height),
                (width, max_height),
            ],
            fill="red",
        )

    return diff_img
