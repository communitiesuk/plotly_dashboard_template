"""bulk_text_download"""

import os
import subprocess
import sys
from dotenv import load_dotenv

# pylint: disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants import FOLDER_CONTAINING_HTML_FILES


load_dotenv(override=True)

FOLDER_CONTAINING_WORD_DOCUMENTS = os.getenv("PATH_TO_WORD_DOCUMENT")


def get_all_docx_files(folder: str) -> list[str]:
    """
    Return a list of all .docx filenames within the given folder, excluding temporary Word files.
    Args:
        folder (str): The directory path where Word documents are stored.
    Returns:
        list[str]: A list of .docx filenames found in the specified folder.
    """
    return [
        f for f in os.listdir(folder) if f.endswith(".docx") and not f.startswith("~$")
    ]


def get_html_file_name_and_path(word_doc_filename: str) -> tuple[str, str]:
    """
    Constructs the HTML file name and its path from a Word document filename.
    Args:
        word_doc_filename (str): The filename of the Word document.
    Returns:
        tuple[str, str]: A tuple containing the output HTML filename and its full path.
    """
    output_html_filename = word_doc_filename.split(".")[0] + ".html"
    output_html_path = os.path.join(FOLDER_CONTAINING_HTML_FILES, output_html_filename)
    return output_html_filename, output_html_path


def generate_html_from_word_using_mammoth(
    word_doc_full_path: str, output_html_path: str
) -> None:
    """
    Converts a Word document to HTML format using the Mammoth command-line tool.
    Args:
        word_doc_full_path (str): The full path to the Word document.
        output_html_path (str): The path where the generated HTML should be saved.
    """
    subprocess.run(["mammoth", word_doc_full_path, output_html_path], check=True)


def ensure_directory_exists(path: str) -> None:
    """
    Ensures that the directory for the provided path exists. Creates the directory if it does not
    exist.
    Args:
        path (str): The file system path whose directory needs to exist
    """
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_word_doc_full_path(word_doc_filename: str) -> str:
    """Constructs the full file path for a given Word document filename."""
    return os.path.join(FOLDER_CONTAINING_WORD_DOCUMENTS, word_doc_filename)


def bulk_text_download(force_text_refresh: bool = True) -> None:
    """
    Download all html files, for text, needed for the dashboard.
    Args:
        force_text_refresh (bool): If True, forces the refresh of text files from Word to HTML.
                                    Defaults to True.
    """
    if force_text_refresh:
        word_doc_filenames = get_all_docx_files(FOLDER_CONTAINING_WORD_DOCUMENTS)
        for word_doc_filename in word_doc_filenames:
            output_html_filename, output_html_path = get_html_file_name_and_path(
                word_doc_filename
            )
            word_doc_full_path = get_word_doc_full_path(word_doc_filename)
            ensure_directory_exists(output_html_path)

            print(f"Generating html file from {word_doc_filename}")
            generate_html_from_word_using_mammoth(word_doc_full_path, output_html_path)
            print(f"{output_html_filename}")
    else:
        print("No text files downloaded as force_text_refresh set to False")


if __name__ == "__main__":
    bulk_text_download(force_text_refresh=True)
