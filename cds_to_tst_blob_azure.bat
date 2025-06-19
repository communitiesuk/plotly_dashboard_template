set ARG="tst"
python checkout_to_environment_commit.py %ARG%
python updating_dashboard_text\bulk_text_download.py
python auto_cds_to_blob.py %ARG% || echo "auto cds to blob failed in tst file, continuing"
echo "completed tst"
