"""Data test assertions for use in testing data"""

import csv
from typing import Type
import polars as pl
from pydantic import BaseModel, ValidationError

from data.get_data import load_data
from lib.absolute_path import absolute_path
from tests.data_tests.data_test_helper_functions import extract_main_type

PYDANTIC_TO_POLARS = {
    str: pl.Utf8,
    int: pl.Int64,
    float: pl.Float64,
    bool: pl.Boolean,
}


def csv_columns_are_valid(csv_filename: str, desired_column_names: list[str]):
    """Checks csv columns are equal to desired_column_names.

    Args:
        csv_filename (str): local csv filename to test
        desired_column_names (list[str]): list of desired column names
    """
    with open(
        absolute_path(f"data/housing/{csv_filename}"),
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)
        actual_column_names = reader.fieldnames
        assert sorted(actual_column_names) == sorted(
            desired_column_names
        ), f"csv_columns_are_valid test failed for {csv_filename}"


def cvs_contains_no_duplicate_rows(csv_filename: str):
    """
    Test to check that the csv has no duplicate rows.

    Parameters:
    csv_filename (str): local csv filename to test for duplicate rows

    Returns: bool: True if there were no duplicates in the df, False otherwise.
    """

    df = pl.read_csv(absolute_path(f"data/housing/{csv_filename}"))
    num_duplicate_rows = df.is_duplicated().sum()
    assert (
        num_duplicate_rows == 0
    ), f"cvs_contains_no_duplicate_rows test failed for {csv_filename}"


def inferred_df_has_correct_column_types(csv_filename: str, schema: Type[BaseModel]):
    """
    Test to check that a df infers the correct column types as defined in schema.

    Parameters:
    csv_filename (str): local csv filename to test for duplicate rows
    schema (Type[BaseModel]): Pydantic model class to extract the expected column types

    Returns: bool: True if the inferred column types are correct, False otherwise.
    """
    expected_schema = {
        field: PYDANTIC_TO_POLARS[extract_main_type(typ)]
        for field, typ in schema.__annotations__.items()
    }

    df = load_data(absolute_path(f"data/housing/{csv_filename}"), "csv")
    assert df.schema == expected_schema


def df_has_valid_schema(csv_filename: str, schema: Type[BaseModel]):
    """Validates each row in a Polars DataFrame against a Pydantic model schema.

    Args:
        csv_filename (str): local csv filename to test
        schema (Type[BaseModel]): Pydantic model class to extract the expected column types
    """

    df = load_data(absolute_path(f"data/housing/{csv_filename}"), "csv")
    valid_rows = True
    for row in df.to_dicts():
        try:
            schema(**row)  # Pydantic validation
        except ValidationError as e:
            valid_rows = False
            print(e)
            break
    assert valid_rows


def value_is_greater_than_or_equal_to(value, value_to_be_greater_than_or_equal_to):
    """Validates that the `value` is greater than or equal to
        `value_to_be_greater_than_or_equal_to`.

    Args:
        value (float or int): The value to be validated.
        value_to_be_greater_than_or_equal_to (float or int): The value that `value` should be
            greater than or equal to.

    Raises:
        ValueError: If `value` is less than `value_to_be_greater_than_or_equal_to`.
    """
    if value < value_to_be_greater_than_or_equal_to:
        raise ValueError(
            f"{value} must be greater than or equal to {value_to_be_greater_than_or_equal_to}"
        )
