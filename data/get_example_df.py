"""get_example_df function"""

import polars as pl

from data.get_data import load_data
from data.cache_functions import track_cache

from lib.absolute_path import absolute_path


@track_cache
def get_example_df() -> pl.DataFrame:
    """Load the CDS data or CSV containing example data into a DataFrame"""
    csv_location = absolute_path("data/folder/example.csv")
    dataframe = load_data(file_to_get=csv_location, data_type="csv")

    if dataframe is None:
        raise ValueError(
            f"Housing supply summary data '{csv_location}' failed to load."
        )
    return dataframe
