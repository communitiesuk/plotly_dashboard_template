"""example_data_query"""

from data.get_data import GenericDataQuery


class ExampleDataQuery(GenericDataQuery):
    """Static class for example data query."""

    filename = "example.csv"
    dir = "data/example"

    def query(self):
        """function to return query string."""
        return f"""
            SELECT *
            FROM '[Example].[table]'
            """


if __name__ == "__main__":
    ExampleDataQuery().get_data_from_cds()
