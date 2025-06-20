"""update_data_and_mapping_for_deployment.py"""

import json
import os
from dotenv import load_dotenv

from auto_cds_to_blob import run_tests
from constants import FILE_MAPPING_JSON_PATH
from data.bulk_data_download import bulk_data_download
from data.data_query_classes import data_query_classes
from blob_helper_functions.test_files_exist_in_blob import test_files_exist_in_blob
from update_mapping_and_upload_to_all_blobs import (
    update_mapping_and_upload_to_all_blobs_if_file_updated,
)


load_dotenv(override=True)


def update_data_and_mapping_for_deployment():
    """Upload data files from cds to all blobs (dev, tst, prd) and update file mapping"""
    bulk_data_download()  # refreshes data
    os.environ["USE_REAL_DATA"] = "true"  # tests need to run against real data
    _, test_result = run_tests()
    if test_result == 0:  # all integration tests have passed
        for data_query in data_query_classes:
            local_file_path = data_query.dir + "/" + data_query.filename
            print(f"Reading in {data_query.filename}")
            file_mapping = update_mapping_and_upload_to_all_blobs_if_file_updated(
                local_file_path,
                data_query.filename,
            )
            with open(FILE_MAPPING_JSON_PATH, "w", encoding="utf-8") as outfile:
                json.dump(file_mapping, outfile, indent="\t")
    del os.environ["USE_REAL_DATA"]
    test_files_exist_in_blob(os.getenv("CONNECTION_STRING_DEV"), FILE_MAPPING_JSON_PATH)
    test_files_exist_in_blob(os.getenv("CONNECTION_STRING_TST"), FILE_MAPPING_JSON_PATH)
    test_files_exist_in_blob(os.getenv("CONNECTION_STRING_PRD"), FILE_MAPPING_JSON_PATH)
    return test_result == 0
