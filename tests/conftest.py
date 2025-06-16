"""Pytest automatically loads this file before executing tests"""

import os
from typing import Any

os.environ["STAGE"] = "testing"


def pytest_addoption(parser: Any) -> None:
    """Add the playwright command arguments to pytest"""
    group = parser.getgroup("playwright-snapshot", "Playwright Snapshot")
    group.addoption(
        "--update-snapshots",
        action="store_true",
        default=False,
        help="Update existing snapshots.",
    )
    group.addoption(
        "--fail-fast",
        action="store_true",
        default=False,
        help="Fail test as soon as an invalid pixel is found",
    )
