"""query_parameters"""

from urllib.parse import urlencode, parse_qs, urlsplit


def dict_to_query_string(**kwargs):
    """
    Create a string of query parameters from keyword arguments.

    What are query strings and parameters? -> https://en.wikipedia.org/wiki/Query_string

    Used to synchronise the selected filters between dashboards.
    """
    return "?" + urlencode(
        {key: value for key, value in dict(kwargs).items() if value is not None}
    )


def query_string_to_dict(url):
    """
    Create a dictionary of query parameters from a query string.

    What are query strings and parameters? -> https://en.wikipedia.org/wiki/Query_string

    Used to synchronise the selected filters between dashboards.
    Will discard additional values for the same parameter.
    """
    return parse_qs(urlsplit(url).query)


def selected_filters(url):
    """
    Create a dictionary of user selections from a URL
    """
    return first_values(query_string_to_dict(url))


def first_values(query_parameters):
    """
    Select the first values from a dictionary of query parameters

    Query strings support multiple values for one key.  This function takes a dictionary of lists
    and returns a dictionary of strings, where the string is the first value in each list.
    """
    return {key: value[0] for (key, value) in query_parameters.items()}
