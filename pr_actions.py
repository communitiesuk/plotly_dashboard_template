"""Script to run before putting a PR out"""

from datetime import date
import re

from update_data_and_mapping_for_deployment import (
    update_data_and_mapping_for_deployment,
)


def pr_actions():
    """Refreshes local data and runs integration and data tests.
    - If tests pass, local data hash is compared to hash of file in blob via mapping.json, and new
        data uploaded to dev, tst and prd blobs and mapping.josn updated accordingly. Then prompted
        for sentry version number and devops message, to update configuration/sentry.py and
        devops/Deployment_Run.txt
    - If tests fail, prompted to investigate before trying again."""

    data_is_current = update_data_and_mapping_for_deployment()
    if data_is_current:
        with open("configuration/sentry.py", "r", encoding="utf-8") as sentry_file:
            content = sentry_file.read()
        current_sentry_version = re.findall(r"\d+\.\d+\.\d+", content)[0]
        response_1 = input(
            "Please enter the new sentry version number, current version "
            f"is {current_sentry_version} : "
        )
        response_2 = f"{input('Please enter the devops message: ')} {date.today()}"
        updated_content = re.sub(r"\d+\.\d+\.\d+", response_1, content)
        with open("configuration/sentry.py", "w", encoding="utf-8") as sentry_file:
            sentry_file.write(updated_content)
        with open("devops/Deployment_Run.txt", "a", encoding="utf-8") as devops_file:
            devops_file.write(f"\n{response_2}")
        print("Data updated, PR is ready for review.")
    else:

        print("Data update process failed, please review test failures.")


if __name__ == "__main__":
    pr_actions()
