"""Utils for running the visual regression tests"""

from pathlib import Path
from typing import Any
import shutil
import pytest
from pixelmatch.contrib.PIL import pixelmatch


def get_expected_snapshot_file(request: Any, test_name: str, test_file_name: str):
    """Returns original snapshot file to compare new snapshot to"""
    snapshots_folder = (
        Path(request.node.fspath).parent.resolve()
        / "snapshots"
        / test_file_name
        / test_name
    )
    snapshots_folder.mkdir(parents=True, exist_ok=True)

    return snapshots_folder / "expected.png"


def save_failed_snapshot_comparison_images(
    actual_img, expected_img, diff_img, snapshots_failure_folder
):
    """Save the images into the failed snapshot images folder"""

    snapshots_failure_folder.mkdir(parents=True, exist_ok=True)

    diff_img.save(f"{snapshots_failure_folder}/diff.png")
    actual_img.save(f"{snapshots_failure_folder}/actual.png")
    expected_filename = f"{snapshots_failure_folder}/expected.png"
    expected_img.save(expected_filename)


def save_actual_snapshot_to_failure_folder_and_fail_test(
    snapshots_failure_folder, actual_img
):
    """Save actual image to the failure folder in case where there is no
    expected image to compare to"""

    snapshots_failure_folder.mkdir(parents=True, exist_ok=True)

    actual_img.save(f"{snapshots_failure_folder}/actual.png")

    pytest.fail(
        "--> No snapshot available to compare with, review the "
        "actual image and add to snapshots folder"
    )


def images_are_same(actual_img, expected_img, diff_img, fail_fast):
    """Returns true if the actual and expected images are the same"""
    try:
        mismatch_pixel_count = pixelmatch(
            actual_img, expected_img, diff_img, fail_fast=fail_fast
        )

        return mismatch_pixel_count == 0
    except ValueError:
        return False


def get_snapshots_failure_folder(request: Any, test_name: str, test_file_name: str):
    """Returns an empty folder with path snapshots_failure/<test_file_name>/<test_name>"""
    snapshots_failure_folder = (
        Path(request.node.fspath).parent.resolve()
        / "snapshots_failure_folder"
        / test_file_name
        / test_name
    )
    _delete_old_failure_snapshots_if_they_exist(snapshots_failure_folder)

    return snapshots_failure_folder


def _delete_old_failure_snapshots_if_they_exist(snapshots_failure_folder):
    if snapshots_failure_folder.exists():
        shutil.rmtree(snapshots_failure_folder)
