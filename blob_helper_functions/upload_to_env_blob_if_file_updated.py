""" "upload_to_env_blob_if_file_updated"""

import os
import hashlib

from dotenv import load_dotenv

from azure.storage.blob import BlobServiceClient

from constants import FOLDER_CONTAINING_HTML_FILES

load_dotenv(override=True)

env_to_blob_string_map = {
    "dev": os.getenv("CONNECTION_STRING_DEV"),
    "tst": os.getenv("CONNECTION_STRING_TST"),
    "prd": os.getenv("CONNECTION_STRING_PRD"),
}


def upload_to_env_blob_if_file_updated(
    env: str,
    file_path: str,
    filename: str,
    include_html_files: bool = False,
) -> int:
    """
    Uploads the file to env Azure blob storage if the file has changed or the file doesn't exist in
    Azure blob storage.
    Args:
        env (str): The blob storage environment to upload to. Either "dev", "tst" or "prd"
        file_path (str): The file path of file.
        filename (str): The file name of the file.
        include_html_files (bool): Whether the files are html_files or not

    Returns:
        int: 1 if file updated/uploaded and 0 if not.
    """
    connection_string = env_to_blob_string_map[env]

    with open(file_path, "rb") as data:
        file_content = data.read()
        hash_key_of_file = hashlib.sha256(file_content).hexdigest()

        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )

        if include_html_files is False:
            container_name = file_path.split("/")[-2]
        else:
            container_name = FOLDER_CONTAINING_HTML_FILES.rsplit("\\", maxsplit=1)[-1]

        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=filename
        )

        if blob_client.exists():
            downloader = blob_client.download_blob(max_concurrency=1, encoding="UTF-8")
            blob_text = downloader.readall()
            hash_key_of_blob_file = hashlib.sha256(
                blob_text.encode("utf-8")
            ).hexdigest()

            if hash_key_of_file != hash_key_of_blob_file:
                print(f"Uploading {filename}")

                # Upload the file
                data.seek(
                    0
                )  # Rewind the file pointer to the beginning of the file, so the next operation
                # which uploads the file content (file_content), uploads the entire file content
                blob_client.upload_blob(file_content, overwrite=True)
                print(f"Uploaded {filename} with new content")
                return 1
            print(
                f"No upload necessary. The file {filename} in the blob storage matches the "
                "local file."
            )
            return 0

        # If the blob does not exist, upload the file
        print(f"Blob '{filename}' does not exist. Uploading now...")

        data.seek(
            0
        )  # Rewind the file pointer to the beginning of the file, so the next operation which
        # uploads the file content (file_content), uploads the entire file content

        blob_client.upload_blob(file_content, overwrite=True)
        print(f"Uploaded {filename} as it did not exist.")
        if env == "prd":
            return 1
        return 0
