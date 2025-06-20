"""test_files_exist_in_blob"""

import json
from azure.storage.blob import BlobServiceClient

from constants import BLOB_FILE_PATH


def test_files_exist_in_blob(
    connection_string: str, file_mapping_json_path: str
) -> None:
    """
    Checks if the files listed in the mapping JSON exist in the Azure Blob Storage.
    If there are any missing blobs, the function raises an exception
    containing details of the missing blobs.
    Args:
        connection_string (str): The Azure Blob Storage connection string.
        file_mapping_json_path (str): Path to the JSON file containing the mapping of file names
                                      to blob storage paths and hashes.
    Raises:
        Exception: If there are any missing blobs, an exception is raised containing a list
                   of the missing blobs and their respective container names.
    """
    error_messages = []

    storage_account_name = connection_string.split(";")[1].split("=")[1]

    missing_blobs = []

    with open(file_mapping_json_path, "r", encoding="utf-8") as infile:
        file_mapping = json.load(infile)
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )
        _check_for_missing_blobs(file_mapping, blob_service_client, missing_blobs)

        if missing_blobs:
            formatted_missing_blobs = "\n".join(missing_blobs)
            error_message = (
                f"MISSING BLOBS in storage account {storage_account_name}:\n"
                f"{formatted_missing_blobs}"
            )
            error_messages.append(error_message)
        else:
            print(f"No missing blobs in storage account {storage_account_name}")

    if error_messages:
        full_error_message = "\n\n".join(error_messages)
        raise Exception(full_error_message)  # pylint: disable=broad-exception-raised


def _check_for_missing_blobs(file_mapping, blob_service_client, missing_blobs):
    for blob_info in file_mapping.values():
        container_name, blob_name = blob_info[BLOB_FILE_PATH].split("/", 1)
        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=blob_name
        )
        try:
            # if the blob doesn't exist, this will raise a ResourceNotFoundError
            blob_client.get_blob_properties()

            # read first line of blob to confirm content exists
            # Download the blob content
            blob_data = blob_client.download_blob().readall().decode("utf-8")
            # Split the blob content into lines
            lines = blob_data.splitlines()
            # Check if there is at least one line and it is not empty
            if lines and lines[0].strip():
                # Print the first line of the blob
                print(
                    f"First line of the blob '{blob_name}' in container '{container_name}':"
                )
                print(lines[0] + "\n")
            else:
                print(
                    f"The blob '{blob_name}' in container '{container_name}' is empty or has "
                    "no valid content." + "\n"
                )

        except Exception:  # pylint: disable=broad-exception-caught
            missing_blobs.append(f"{container_name}/{blob_name}")
