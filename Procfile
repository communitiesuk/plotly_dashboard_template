# The entry point for the application in non-development environments
# This command is run to start the web server
web: gunicorn run:server -b 0.0.0.0:$PORT --env STAGE=production