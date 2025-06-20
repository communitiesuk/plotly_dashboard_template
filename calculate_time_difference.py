"""calculate_time_difference function"""

from datetime import datetime


def calculate_time_difference(start: str, end: str) -> str:
    """Calculates the difference between two time strings in HH:MM:SS format.

    Args:
        start (str): Calculates the difference between two time strings in HH:MM:SS format.
        end (str):he end time in "HH:MM:SS" format.

    Returns:
        str:The time difference as a string in "HH:MM:SS" format.
    """
    if not start or not end:  # covers None or empty string
        return None
    try:
        start = datetime.strptime(start.strip(), "%H:%M:%S")
        end = datetime.strptime(end.strip(), "%H:%M:%S")
        return str(end - start)
    except ValueError:
        return None


if __name__ == "__main__":
    import sys

    start_time = sys.argv[1]  # Get the argument passed from the .bat file
    end_time = sys.argv[2]  # Get the argument passed from the .bat file
    print(
        calculate_time_difference(start_time, end_time)
    )  # print passes the output back to .bat file (cds_to_all_blobs_azure.bat)
