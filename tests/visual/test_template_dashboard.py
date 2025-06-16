"""Visual regression test for test dashboard"""


def test_home_page_matches_snapshot(
    assert_valid_snapshot,
):
    """A visual regression test to ensure the current page matches the snapshot"""
    assert_valid_snapshot("/", "#title")
