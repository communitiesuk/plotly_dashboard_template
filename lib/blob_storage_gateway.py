"""BlobStorageGateway class"""

import datetime
import json
import os
from azure.storage.blob import BlobServiceClient

from dotenv import load_dotenv

from constants import FILE_MAPPING_JSON_PATH
from lib.absolute_path import absolute_path

load_dotenv(override=True)


class BlobStorageGateway:  # pylint: disable=too-few-public-methods
    """A class for getting information about a storage container."""

    def __init__(self, container: str):
        self.blob_service_client = BlobServiceClient.from_connection_string(
            os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        )
        self.container_client = self.blob_service_client.get_container_client(container)

    def get_last_updated(self):
        """Determines when each blob in a container was last modified.

        Returns:
            dict: Dictionary with keys the name of a blob, and values the last modified date and
            time.
        """
        with open(absolute_path(FILE_MAPPING_JSON_PATH), "rb") as json_file:
            file_mapping = json.load(json_file)
            current_filepaths = [
                list(subdict.values())[0] for subdict in file_mapping.values()
            ]
            current_filenames = [
                filepath.split("/")[1] for filepath in current_filepaths
            ]
            last_modified_dict = {}
            blobs = self.container_client.list_blobs()
            for blob in blobs:
                if blob["name"] in current_filenames:  # returns bool
                    if isinstance(blob["last_modified"], datetime.datetime):
                        last_modified_dict[blob["name"]] = blob[
                            "last_modified"
                        ].isoformat()
                    elif isinstance(blob["last_modified"], str):
                        last_modified_dict[blob["name"]] = blob["last_modified"]
        return last_modified_dict
