# pylint: disable=too-many-locals
"""update_mapping_and_upload_to_all_blobs_if_file_updated"""

import json
import os
import hashlib

from datetime import date

from dotenv import load_dotenv

from azure.storage.blob import BlobServiceClient

from lib.absolute_path import absolute_path

from constants import (
    BLOB_FILE_PATH,
    FILE_MAPPING_JSON_PATH,
)

load_dotenv(override=True)

dev_connection_string = os.getenv("CONNECTION_STRING_DEV")
tst_connection_string = os.getenv("CONNECTION_STRING_TST")
prd_connection_string = os.getenv("CONNECTION_STRING_PRD")


def update_mapping_and_upload_to_all_blobs_if_file_updated(
    file_path: str,
    filename: str,
) -> dict[str, dict[str, str]]:
    """
    Updates the file mapping json dictionary and uploads the file to dev Azure blob storage if
    the file has changed.
    Args:
        file_path (str): The file path of file.
        filename (str): The file name of the file.
    Returns:
        dict: The updated file mapping dictionary.
    """

    container_name = file_path.split("/")[
        -2
    ]  # currenly not using this method for html files (for text)

    dev_blob_service_client = BlobServiceClient.from_connection_string(
        dev_connection_string
    )

    with open(absolute_path(FILE_MAPPING_JSON_PATH), "rb") as json_file:
        file_mapping = json.load(json_file)
        with open(file_path, "rb") as data:
            file_content = data.read()
            hash_key_of_local_file = hashlib.sha256(file_content).hexdigest()

            if filename in file_mapping:  # file exists in blob storage

                blob_info = file_mapping[filename]
                version = int(blob_info[BLOB_FILE_PATH].split("_")[1])

                blob_name = blob_info[BLOB_FILE_PATH].split("/")[-1]

                dev_blob_client = dev_blob_service_client.get_blob_client(
                    container_name, blob_name
                )

                # Download blob from Azure
                downloader = dev_blob_client.download_blob(
                    max_concurrency=1, encoding="UTF-8"
                )
                blob_content = downloader.readall()
                hash_key_of_blob_file = hashlib.sha256(
                    blob_content.encode("utf-8")
                ).hexdigest()
                if hash_key_of_local_file != hash_key_of_blob_file:
                    new_version = version + 1
                else:
                    print(f"No changes to file {filename}")
                    return file_mapping
            else:
                new_version = 1

            # Construct new blob file name with the new version
            new_blob_file_name = f"v_{new_version}_{date.today()}_{filename}"
            print(f"Uploading {new_blob_file_name}")

            dev_blob_client = dev_blob_service_client.get_blob_client(
                container_name, blob=new_blob_file_name
            )

            tst_blob_service_client = BlobServiceClient.from_connection_string(
                tst_connection_string
            )
            tst_blob_client = tst_blob_service_client.get_blob_client(
                container=container_name, blob=new_blob_file_name
            )
            prd_blob_service_client = BlobServiceClient.from_connection_string(
                prd_connection_string
            )
            prd_blob_client = prd_blob_service_client.get_blob_client(
                container=container_name, blob=new_blob_file_name
            )
            # Upload the file
            for blob_client in [dev_blob_client, tst_blob_client, prd_blob_client]:
                data.seek(
                    0
                )  # Rewind the file pointer to the beginning of the file, so the next operation
                # which uploads the file content (file_content), uploads the entire file content
                blob_client.upload_blob(file_content, overwrite=True)
            print(f"Uploaded {new_blob_file_name}")

            # Update the file mapping
            file_mapping[filename] = {
                BLOB_FILE_PATH: f"{container_name}/{new_blob_file_name}",
            }

    return file_mapping
