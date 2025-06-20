"""Command that will regenerate all local CSV files from CDS and
all local text files from Q drive"""

# pylint: disable=wrong-import-position
import argparse
from data.bulk_data_download import bulk_data_download
from updating_dashboard_text.bulk_text_download import bulk_text_download


def string_to_bool(text_string):
    """Convert a string to a bool"""
    if text_string.lower() in ("true"):
        return True
    if text_string.lower() in ("false"):
        return False
    raise argparse.ArgumentTypeError("True or False expected.")


parser = argparse.ArgumentParser(description="Download DATA and TEXT files.")
parser.add_argument(
    "--force_data_refresh",
    type=string_to_bool,
    nargs="?",
    const=True,
    default=True,
    help="Force refresh of DATA files (default: True). Use --force_data_refresh=false to disable.",
)
parser.add_argument(
    "--force_text_refresh",
    type=string_to_bool,
    nargs="?",
    const=True,
    default=False,
    help="Force refresh of TEXT files (default: False). Use --force_text_refresh=true to enable.",
)

args = parser.parse_args()
print("Downloading DATA Files:")
bulk_data_download(force_data_refresh=args.force_data_refresh)

print("Downloading TEXT Files:")
bulk_text_download(force_text_refresh=args.force_text_refresh)
