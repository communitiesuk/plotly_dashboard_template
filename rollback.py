"""rollback.py"""

import json
import os
import polars as pl

from dotenv import load_dotenv

from azure.storage.blob import BlobServiceClient
from azure.storage.blob import ContainerClient

from constants import BLOB_FILE_PATH, FILE_MAPPING_JSON_PATH
from lib.absolute_path import absolute_path
from data.data_query_classes import data_query_classes

load_dotenv(override=True)

dev_connection_string = os.getenv("CONNECTION_STRING_DEV")


def get_data_rollback_info():
    """Takes an input of a datetime to rollback to. Loops through all data queries and prints in the
    terminal which files require an azure rollback and which files require mapping json to be
    updated."""
    datetime_to_rollback_to = input(
        "Please enter the datetime in format YYYY-MM-DDTHH:SS eg. 2020-12-25T00:00: "
    )
    blob_service_client = BlobServiceClient.from_connection_string(
        dev_connection_string
    )
    mapping_json_rollback_dict = {
        "filename": [],
        "blobname to rollback": [],
        "version to rollback to": [],
    }
    azure_rollback_dict = {"blobname to rollback": [], "version to rollback to": []}
    with open(absolute_path(FILE_MAPPING_JSON_PATH), "rb") as json_file:
        file_mapping = json.load(json_file)
        for data_query in data_query_classes:
            local_file_path = data_query.dir + "/" + data_query.filename
            print(f"Reading in {data_query.filename}")
            container_name = local_file_path.split("/")[
                -2
            ]  # currenly not using this method for html files (for text)

            if data_query.filename in file_mapping:  # file exists in blob storage

                blob_info = file_mapping[data_query.filename]

                blob_name = blob_info[BLOB_FILE_PATH].split("/")[-1]

                current_version = int(blob_info[BLOB_FILE_PATH].split("_")[1])

                container_client = blob_service_client.get_container_client(
                    container_name
                )

                version, new_blob_name = get_version(
                    data_query.filename,
                    blob_name,
                    current_version,
                    container_client,
                    datetime_to_rollback_to,
                )

                if blob_name != new_blob_name:
                    mapping_json_rollback_dict["filename"].append(data_query.filename)
                    mapping_json_rollback_dict["blobname to rollback"].append(
                        new_blob_name
                    )
                    mapping_json_rollback_dict["version to rollback to"].append(version)
                else:
                    azure_rollback_dict["blobname to rollback"].append(new_blob_name)
                    azure_rollback_dict["version to rollback to"].append(version)

        pl.Config.set_tbl_rows(50)
        print(
            "Mapping json update required:"
            "\n1. download the specified version of the specified blob"
            "\n2. construct new file name by incrementing version by 1 from what is currently in "
            "mapping json and updating date to todays date"
            "\n3. upload file with new filename to all blob storage accounts"
            "\n4. manually update mapping json to new blobname",
            "\n5. deploy new mapping json to prd\n",
            pl.DataFrame(mapping_json_rollback_dict),
            "\nAzure rollback required:\n",
            "1. in Azure portal, rollback to the specified version of the blobname \n",
            pl.DataFrame(azure_rollback_dict),
        )


def get_version(
    local_filename: str,
    blob_name: str,
    current_version: int,
    container_client: ContainerClient,
    datetime_to_rollback_to: str,
) -> tuple[str, str]:
    """Gets the version of data for the specificed datetime_to_rollback_to for a given
    local_filename.

    Args:
        local_filename (str): The local filename.
        blob_name (str): The blob filename.
        current_version (int): Current version of the blob filename.
        container_client (ContainerClient): An instance of Azure's ContainerClient, used to interact
            with a specific container in Blob Storage.
        datetime_to_rollback_to (str): The datetime you want to roll the data back to in format
            YYYY-MM-DDTHH:SS eg. 2020-12-25T00:00

    Raises:
        ValueError: If `filtered_blobs` does not have exactly one element.

    Returns:
        tuple[str, str]: Tuple containing version to rollback to and blobname to rollback to.
    """
    blob_versions = list(
        container_client.list_blobs(name_starts_with=blob_name, include=["versions"])
    )

    version_to_rollback_to = ""
    for x in blob_versions:
        if (
            x["version_id"] > version_to_rollback_to
            and x["version_id"] < datetime_to_rollback_to
        ):
            version_to_rollback_to = x["version_id"]

    if version_to_rollback_to == "":
        previous_version = current_version - 1
        blob_versions = list(
            container_client.list_blobs(
                name_starts_with=f"v_{previous_version}_", include=["versions"]
            )
        )
        filtered_blobs = [
            blob.name
            for blob in blob_versions
            if blob.name.endswith(f"_{local_filename}") and blob["is_current_version"]
        ]
        if len(filtered_blobs) != 1:
            raise ValueError("filtered_blobs must have length 1.")
        previous_filename = filtered_blobs[0]
        return get_version(
            local_filename,
            previous_filename,
            previous_version,
            container_client,
            datetime_to_rollback_to,
        )
    return version_to_rollback_to, blob_name


if __name__ == "__main__":
    get_data_rollback_info()
