"""
The entry point for the application to be run from the command line.
"""
import argparse
import os

from werkzeug.middleware.profiler import ProfilerMiddleware
from index import app

# Required for use in staging and production
from app import server  # pylint: disable=unused-import

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile",
        action=argparse.BooleanOptionalAction,
        help="Profile requests to the perf directory",
    )

    args = parser.parse_args()

    HOST_REQUIRED_BY_DAP = "0.0.0.0"
    PORT_REQUIRED_BY_DAP = 8080

    if args.profile:
        print("**** Starting server with profiling enabled ****")
        PROF_DIR = os.path.join(os.getcwd(), "perf")

        if not os.path.exists(PROF_DIR):
            os.mkdir(PROF_DIR)
        for file in os.scandir(PROF_DIR):
            os.remove(file.path)

        app.server.config["START_PROFILER"] = True
        app.server.wsgi_app = ProfilerMiddleware(
            app.server.wsgi_app,
            sort_by=["cumtime"],
            restrictions=[50],
            stream=None,
            profile_dir=PROF_DIR,
        )

    app.run_server(host=HOST_REQUIRED_BY_DAP, port=PORT_REQUIRED_BY_DAP, debug=True)
