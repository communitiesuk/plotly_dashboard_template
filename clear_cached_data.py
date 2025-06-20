"""ClearCachedData class"""

import json
import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from data.cache_functions import clear_cache
from data.data_query_classes import data_query_classes
from data.get_data import get_data_from_blob_storage_without_mapping
from lib.blob_storage_gateway import BlobStorageGateway

load_dotenv(override=True)

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
BLOB_NAME = "last_updated.json"
CONTAINER_NAME = "blobdates"


class ClearCachedData:  # pylint: disable=too-few-public-methods
    """Determines if data has been modified in the blob since it was last accessed, and if so
    clears the cache so new data is displayed on the front end."""

    def __init__(self):
        self.containers = self._get_containers()
        self.source_last_updated = {}

    def __call__(self):
        """If new data exists, all current caches are removed and 'last_updated.json' is updated."""
        if self._new_data_in_blob():
            clear_cache()
            self._update_local_last_updated()

    def _update_local_last_updated(self):

        _update_last_updated_json(json.dumps(self.source_last_updated))

    def _get_source_last_updated(self):
        """Retrieves the last updated timestamps for each blob in each container defined in the
        `self.containers` attribute and stores in the `self.source_last_updated` dictionary.
        """
        for container_name in self.containers:
            storage_gateway = BlobStorageGateway(container_name)
            self.source_last_updated.update(storage_gateway.get_last_updated())
            for key, value in self.source_last_updated.items():
                self.source_last_updated[key] = value

    def _get_containers(self):
        return list(
            set(data_query_class.dir[5:] for data_query_class in data_query_classes)
        )

    def _new_data_in_blob(self):
        """Determines if new data exists in the storage account by comparing:
        - self.get_source_last_updated()
        - with app_last_updated
        which are both dictionaries with keys the name of a blob, and values the last modified date
        and time."""

        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        blob_client = container_client.get_blob_client(BLOB_NAME)

        if not blob_client.exists():
            # Create the blob with an empty dictionary if it doesn't exist
            empty_dict = json.dumps({})
            try:
                blob_client.upload_blob(empty_dict, overwrite=True)
                return True
            except Exception as e:  # pylint: disable=broad-exception-caught
                print(f"Failed to upload blob: {str(e)}")

        json_data = get_data_from_blob_storage_without_mapping(
            "blobdates/last_updated.json", "json"
        )

        self._get_source_last_updated()
        if self.source_last_updated != json_data:
            return True
        return False


def _update_last_updated_json(data):
    """Updates the last_updated.json in blobdates container in blob storage."""

    json_content = data

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

    try:
        container_client.upload_blob(BLOB_NAME, json_content, overwrite=True)
        print(f"Successfully uploaded '{BLOB_NAME}' to container '{CONTAINER_NAME}'.")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Failed to upload blob: {str(e)}")
