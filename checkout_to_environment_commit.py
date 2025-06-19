"""Function to get the most recent commit id for an azure environment"""

import base64
import os
import sys
import subprocess
import logging
import requests
from dotenv import load_dotenv

load_dotenv(override=True)
logger = logging.getLogger(__name__)
logger.propagate = True

azure_organisation = os.getenv("AZURE_ORGANISATION")
azure_project = os.getenv("AZURE_PROJECT")
env_id_map = {
    "dev": os.getenv("ENVIRONMENT_ID_DEV"),
    "tst": os.getenv("ENVIRONMENT_ID_TST"),
    "prd": os.getenv("ENVIRONMENT_ID_PRD"),
}
pipeline_id = os.getenv("PIPELINE_ID")
API_VERSION = "7.1"

logging.basicConfig(filename="master_log.log", level=logging.INFO)


pat = os.getenv("PAT_TOKEN")
auth_header = base64.b64encode(f":{pat}".encode()).decode()
headers = {"Authorization": f"Basic {auth_header}"}


# pylint: disable=redefined-outer-name
def get_most_recent_successful_run_id(env):
    """Sends a request to azure to get all deplyments to an environment then gets the run id for the
    most recent successful deployment"""
    env_deployments = (
        f"https://dev.azure.com/{azure_organisation}/{azure_project}/_apis/"
        f"distributedtask/environments/{env_id_map[env]}/environmentdeploymentrecords?api-version="
        f"{API_VERSION}"
    )

    logger.info("Fetching deployments from %s", env_deployments)

    deployments = requests.get(env_deployments, headers=headers, timeout=5000).json()[
        "value"
    ]
    run_id = ""
    for deployment in deployments:
        if deployment["result"] == "succeeded":
            run_id = deployment["owner"]["id"]
            break
    return run_id


def get_commit_id_for_environment(env):
    """Sends a request to azure to get the details for the most recent successful deployment and
    gets the commit id for the code deployed"""
    run_id = get_most_recent_successful_run_id(env)
    run_url = (
        f"https://dev.azure.com/{azure_organisation}/{azure_project}/_apis/pipelines/{pipeline_id}"
        f"/runs/{run_id}?api-version={API_VERSION}"
    )
    logger.info("Searching for commit_id at %s", run_url)
    run_details = requests.get(run_url, headers=headers, timeout=5000).json()
    commit_id = run_details["resources"]["repositories"]["self"]["version"]
    return commit_id


def checkout_to_environment_commit(env):
    """Checks out the repo to the commit deployed to the environment"""
    subprocess.run("git checkout main", check=True)
    subprocess.run("git reset --hard", check=True)
    subprocess.run("git pull origin main", check=True)
    commit_id = get_commit_id_for_environment(env)
    subprocess.run(f"git checkout {commit_id}", check=True)
    subprocess.run("conda env update -f environment.yml", check=True)


if __name__ == "__main__":

    if len(sys.argv) > 1:
        env = sys.argv[1]  # Get the argument passed from the .bat file
        checkout_to_environment_commit(env)
    else:
        print("No environment provided. Please pass an argument.")
