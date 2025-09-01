"""Integration test for landing page"""

from dash.testing.composite import DashComposite

from tests.integration.dashboard_test_utils import (
    DashboardTestUtils,
    run_smoke_test_for_page,
)


def test_landing_page_loads_without_error(
    dash_duo: DashComposite, dashboard_utils: DashboardTestUtils
):
    """A smoke test to make sure the dashboard loads and has no error messages (exceptions)"""

    run_smoke_test_for_page(dash_duo, dashboard_utils, "/")
