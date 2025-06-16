"""Get data from a data source e.g. locally or blob storage"""

import logging
import os
import json
from io import StringIO
import polars as pl
from azure.storage.blob import BlobServiceClient
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from data.config import SERVER


from constants import BLOB_FILE_PATH, FILE_MAPPING_JSON_PATH


def get_data_from_blob_storage_without_mapping(file_to_get: str, data_type: str):
    """Get data from Azure Blob storage. Where data_type is the filetype, either "json" or "csv"
    or "html"."""

    file_to_get_split = file_to_get.split("/")
    data_folder_name = file_to_get_split[-2]

    if data_type in ["html", "csv", "json"]:
        blob_name = file_to_get_split[-1]
    else:
        raise ValueError(f"Unsupported data type: {data_type}")

    # Import data from Azure Blob storage
    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Create container clients to access the containers with the data
    container_client = blob_service_client.get_container_client(
        container=data_folder_name
    )

    # Download blob from Azure
    downloaded_blob = container_client.download_blob(blob_name)

    # Convert downloaded blob to a string
    downloaded_data = StringIO(str(downloaded_blob.readall(), encoding="utf-8"))
    if data_type == "csv":
        return pl.read_csv(downloaded_data, low_memory=False, infer_schema_length=None)
    if data_type == "html":
        return downloaded_data.read()
    if data_type == "json":
        return json.load(downloaded_data)
    raise ValueError(f"Unsupported data type: {data_type}")


def get_data_from_blob_storage_with_mapping(file_to_get: str, data_type: str):
    """Get data from Azure Blob storage. Where data_type is the filetype, either "json" or "csv"
    or "html"."""

    with open(FILE_MAPPING_JSON_PATH, mode="r", encoding="utf-8") as json_file:
        file_mappings = json.load(json_file)

    file_to_get_split = file_to_get.split("/")
    data_folder_name = file_to_get_split[-2]
    file_name = file_to_get_split[-1]

    if data_type in ["html", "csv", "json"]:  # Getting blob file from file mapping
        blob_name = file_mappings[file_name][BLOB_FILE_PATH].split("/")[-1]
    else:
        raise ValueError(f"Unsupported data type: {data_type}")

    # Import data from Azure Blob storage
    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Create container clients to access the containers with the data
    container_client = blob_service_client.get_container_client(
        container=data_folder_name
    )

    # Download blob from Azure
    downloaded_blob = container_client.download_blob(blob_name)

    # Convert downloaded blob to a string
    downloaded_data = StringIO(str(downloaded_blob.readall(), encoding="utf-8"))

    if data_type == "csv":
        return pl.read_csv(downloaded_data, low_memory=False)
    if data_type == "html":
        return downloaded_data.read()
    if data_type == "json":
        return json.load(downloaded_data)
    raise ValueError(f"Unsupported data type: {data_type}")


def load_data(file_to_get: str, data_type: str):
    """Get data from data source e.g. locally or blob. Where data_type can be "json" or "csv"
    or "html"."""
    # Due to files being accessed within global scopes, tests begin
    # to fail due to files irrelevant to the tests being loaded.
    # Only covering code for development so that we aren't covering up real
    # issues within blob storage and production code.

    # Get data from blob storage if platform is Azure
    if os.environ.get("DFI_TEST_PLATFORM") == "azure":
        if data_type == "html":
            return get_data_from_blob_storage_without_mapping(file_to_get, data_type)
        return get_data_from_blob_storage_with_mapping(file_to_get, data_type)

    # Get data from local file based on data type
    try:
        if data_type == "csv":
            return pl.read_csv(file_to_get, infer_schema_length=1000)
        if data_type == "html":
            with open(
                file_to_get, "r", encoding="utf-8"
            ) as file:  # r to open file in READ mode
                return file.read()
        if data_type == "json":
            with open(file_to_get, "r", encoding="utf-8") as json_file:
                return json.load(json_file)
        raise ValueError(f"Unsupported data type: {data_type}")

    except FileNotFoundError as file_not_found_error:
        logging.warning(
            """get_data.load_data failed to load %s from csv and blob.
            If running on Azure, please ensure that the correct environment
            variables are set. If running locally, please ensure that you have
            the correct files in the data folder.""",
            file_to_get,
        )
        raise file_not_found_error


class GenericDataQuery:
    """Static class for the generic data query."""

    filename: str
    dir: str
    query: str

    # @staticmethod
    def get_data_from_cds(self):
        """Static method to pull data from CDS for dashboard development."""
        # print for debugging
        print(self.filename)

        conn = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={SERVER};"
            "DATABASE=Dashboards;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )

        sql_query = pl.read_database(self.query(), conn)

        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        sql_query.write_csv(self.get_file_location())

    # @staticmethod
    def get_file_location(self):
        """Get the location of the file."""
        return os.path.join(self.dir, self.filename)


class GeojsonDataQuery:
    """Static class for the generic geojson data query."""

    filename: str
    dir: str
    query: str

    # @staticmethod
    def get_data_from_cds(self):
        """Static method to pull data from CDS for dashboard development."""
        # print for debugging
        print(self.filename)

        conn = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={SERVER};"
            "DATABASE=Dashboards;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
        connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": conn})

        geo_json_string = pl.read_database(
            self.query(),
            # NOTE: You MUST use SQLAlchemy, over arrowdbc, due to the buffer size arrowdbc allows
            # not being large enough to hold JSON strings
            connection=create_engine(connection_url),
        )

        parsed_json = json.loads(geo_json_string.item())

        features = parsed_json["features"]
        for feature in features:
            # Data read from DB is a string and Python is unaware coordinates is actually an array
            # from the first json.loads so this forces the cast as array
            feature["geometry"]["coordinates"] = json.loads(
                feature["geometry"]["coordinates"]
            )

        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        with open(self.get_file_location(), "w", encoding="utf-8") as file:
            json.dump(parsed_json, file, indent=4)

    # @staticmethod
    def get_file_location(self):
        """Get the location of the file."""
        return os.path.join(self.dir, self.filename)
