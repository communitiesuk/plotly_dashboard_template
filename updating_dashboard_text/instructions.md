# Instructions for updating dashboard text

Instructions for running the script to convert word docs that contain dashboard text to html and then 
upload to dev blob storage. The instructions also cover how to copy all files (data and text) from dev blob storage to tst blob storage, and from tst blob storage to prd blob storage.

## Prerequisites
This script uses Mammoth to convert Word documents (.docx) to HTML. 
Mammoth needs to be installed for this script to run properly. Mammoth should be installed in 
the conda environment, through the requirements.txt file, but you can also install directly using pip.


1. ### Environment Setup
Create a .env file in the root directory of your project with the following variables:

`PATH_TO_WORD_DOCUMENT: "<The local path to the folder containing your Word documents>" `
`CONNECTION_STRING_DEV: "<Your dev Azure Blob Storage connection string>"`
`CONNECTION_STRING_TST: "<Your tst Azure Blob Storage connection string>"`
`CONNECTION_STRING_PRD: "<Your prd Azure Blob Storage connection string>"`


## Running the Script

### Updating Text from Word Documents

There are two options for running the script:

1. **To Convert All Files in the Folder containing the word documents**:

```bash
python generate_html_from_word_and_upload_to_dev_blob.py --all
```

2. **To Convert Specific Files**:
If you only want to convert and upload specific files, list them after the script name. Make sure each filename ends with .docx and is separated by a space.

```bash
python generate_html_from_word_and_upload_to_dev_blob.py accessibility_page.docx test_page_1.docx
```

### Refreshing Local Text Files

If you want to refresh local text files without pushing them to Blob Storage, run the `refresh_local.py` script with 
the `--force_text_refresh` argument set to True. For example:

```bash
# Set force_text_refresh to True for refreshing local text files
python refresh_local.py --force_text_refresh True
```

The `refresh_local.py` script also refreshes local csv files from the cds. If you only wish to update text files 
run the script with the ``--force_refresh` argument set to false and the `--force_text_refresh` argument set to True.
For example:

```bash
python refresh_local.py --force_data_refresh False --force_text_refresh True
```


### Copying Files from dev to tst blob storage

Use `dev_to_tst_blob.py`script to copy all files (data and text) from the dev blob storage account to the tst blob storage account. 
Make sure both connection strings are provided in the .env file.

Run the script directly (this script does not need additional command-line arguments as it will copy all files specified in the mapping.json):

```bash
python dev_to_tst_blob.py
```

### Copying Files from tst to prd blob storage

Use `tst_to_prd_blob.py`script to copy all files (data and text) from the tst blob storage account to the prd blob storage account. 
Make sure both connection strings are provided in the .env file.

Run the script directly (this script does not need additional command-line arguments as it will copy all files specified in the mapping.json):

```bash
python tst_to_prd_blob.py
```


## Notes on File Handling:
If a file is renamed, a new entry will be created in the mapping, and a new file will be uploaded to Blob Storage.
Currently, the script does not automatically delete entries from the mapping or Blob Storage if they are removed from the source directory. It might be safer to manage deletions manually, as applications might still be using the old files.

## Displaying text on dashboard
1. Load the required html file from the blob.
2. Call the `get_section_component()` function passing in the html content and the required section.
3. In `extract_and_clean_section.py` ensure:
   - ALLOWED_TAGS contains all required HTML tags
   - CLASS_TAG_MAPPING contains mappings of HTML tags to className
4. Ensure text is displayed as expected on dashboard


```python
def accessibility_statement() -> list[Component]:
    "Function to create page to assist accessibility info for user"
    html_content = get_accessibility_text()

    section1_content = get_section_component(html_content, "accessibility_statement")
    section2_content = get_section_component(
        html_content,
        "section_2",
    )

    return main_content([section1_content, section2_content])
```

## Instructions for Product Owners

Instructions for product owners to modify dashboard text in word documents can be found in the following document:
`Q:\AnalyticalDashboards\housing_dashboard_text\instructions.docx`


