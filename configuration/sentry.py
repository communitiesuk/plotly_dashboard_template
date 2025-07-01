"""Module for configuring sentry"""

# UPDATE uncomment when setting up sentry
# import os

# import sentry_sdk
# from sentry_sdk.integrations.flask import FlaskIntegration


# def configure_sentry():
#     """Configure sentry for the application."""
#     sentry_dsn = os.environ.get("SENTRY_DSN")
#     environment_name = os.environ["ENVIRONMENT_NAME"]
#     slot_name = os.environ["SLOT_NAME"]

#     app_release_version = "0.30.0"  # Change for each release

#     sentry_sdk.init(
#         dsn=sentry_dsn,
#         integrations=[FlaskIntegration()],
#         release=app_release_version,
#         environment=environment_name,
#     )

#     sentry_sdk.set_tag("slot_name", slot_name)
