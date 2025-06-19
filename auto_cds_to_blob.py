"""auto_cds_to_dev_blob.py"""

from datetime import datetime
import json
import os
import sys
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
import pytest
import polars as pl
from blob_helper_functions.upload_to_env_blob_if_file_updated import (
    upload_to_env_blob_if_file_updated,
)

from calculate_time_difference import calculate_time_difference
from constants import (
    BLOB_FILE_PATH,
    FILE_MAPPING_JSON_PATH,
)
from data.data_query_classes import data_query_classes
from data.bulk_data_download import bulk_data_download

from lib.absolute_path import absolute_path

load_dotenv(override=True)


class TestResultPlugin:
    """
    Plugin to capture names of failed tests.
    """

    # pylint: disable=too-few-public-methods
    def __init__(self):
        self.failed_tests = []

    def pytest_runtest_logreport(self, report):
        "Collect the name of the test if it failed during the 'call' phase (test execution)"
        if report.failed and report.when == "call":
            self.failed_tests.append(report.nodeid)


# pylint: disable=redefined-outer-name
def auto_cds_to_blob_in_all_envs(bat_env):
    """Upload valid data files from cds to specified env blob"""
    bulk_data_download()
    plugin, test_result = run_tests()
    count = 0
    if test_result == 0:  # all integration tests have passed
        with open(absolute_path(FILE_MAPPING_JSON_PATH), "rb") as json_file:
            file_mapping = json.load(json_file)
            for data_query in data_query_classes:
                local_file_path = data_query.dir + "/" + data_query.filename
                current_blob_file_path = file_mapping[data_query.filename][
                    BLOB_FILE_PATH
                ]
                current_blob_filename = current_blob_file_path.split("/")[1]
                print(f"Reading in {data_query.filename}")
                for env in ["dev", "tst", "prd"]:
                    count_for_env = 0
                    count_for_env += upload_to_env_blob_if_file_updated(
                        env,
                        local_file_path,
                        current_blob_filename,
                    )
                    if env == "prd":
                        count = count_for_env
            if bat_env == "prd":
                file_path = os.getenv("PATH_TO_DATA_DEPLOYMENT_TIME_CSV")
                dashboard = "Housing"
                # Read the CSV file
                write_to_time_taken_kpi_csv(count, file_path, dashboard)

    failed = plugin.failed_tests  # future - notify which tests have failed
    print(failed)
    print(count)


def write_to_time_taken_kpi_csv(count, file_path, dashboard):
    """Function to write the time of prd data updates completing"""
    df = pl.read_csv(file_path)

    # Get today's date string
    today_str = datetime.today().strftime(
        "%d/%m/%Y"
    )  # Adjust if your CSV uses a different format

    # Find rows where the first column matches today's date
    first_col = df.columns[0]
    matching = df.filter(pl.col(first_col) == today_str)

    if matching.height > 0:
        indices = df.select(pl.col(first_col) == today_str).to_series().arg_true()
        row_to_update = indices[-1] if indices.len() > 0 else None
        current_time = datetime.now(ZoneInfo("Europe/London")).strftime("%H:%M:%S")
        df = df.with_columns(
            pl.when(pl.arange(0, df.height) == row_to_update)
            .then(pl.lit(current_time))
            .otherwise(pl.col(f"{dashboard} finish time"))
            .alias(f"{dashboard} finish time")
        )
        df = df.with_columns(
            pl.when(pl.arange(0, df.height) == row_to_update)
            .then(pl.lit(count))
            .otherwise(pl.col(f"{dashboard} files changed"))
            .alias(f"{dashboard} files changed")
        )
        df = df.with_columns(
            [
                pl.col("Start time").str.strip_chars().alias("Start time"),
                pl.col(f"{dashboard} finish time")
                .str.strip_chars()
                .alias(f"{dashboard} finish time"),
            ]
        )
        df = df.with_columns(
            pl.when(
                (pl.arange(0, df.height) == row_to_update)
                & pl.col("Start time").is_not_null()
                & pl.col(f"{dashboard} finish time").is_not_null()
            )
            .then(
                pl.struct(["Start time", f"{dashboard} finish time"]).map_elements(
                    lambda row: calculate_time_difference(
                        row["Start time"], row[f"{dashboard} finish time"]
                    )
                )
            )
            .otherwise(None)
            .alias(f"{dashboard} time taken")
        )

        # Write the updated DataFrame back to CSV
        df.write_csv(file_path)
        print(f"Updated row {row_to_update} with time {current_time}.")
    else:
        print(
            "No matching rows for today's date found."
        )  # print needed to pass count to .bat file (cds_to_prd_blob_azure.bat)


def run_tests():
    """runs integration tests and returns 0 for success"""
    plugin = TestResultPlugin()
    test_result = pytest.main(
        ["tests/integration", "tests/data_tests"],
        plugins=[plugin],
    )
    return plugin, test_result


if __name__ == "__main__":
    assert (
        len(sys.argv) == 2
    ), f"No argument passed. Length of sys args was {len(sys.argv)}"
    bat_env = sys.argv[1]  # Get the argument passed from the .bat file
    auto_cds_to_blob_in_all_envs(bat_env)
