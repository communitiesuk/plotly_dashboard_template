"""bulk_data_download"""

from data.data_query_classes import data_query_classes


def bulk_data_download(force_data_refresh=True):
    """Download all data files needed for the dashboard."""
    if force_data_refresh:
        for data_query in data_query_classes:
            print(f"Running {data_query.__name__}...")
            data_query().get_data_from_cds()
    else:
        print("No data files downloaded as force_text_refresh set to False")
