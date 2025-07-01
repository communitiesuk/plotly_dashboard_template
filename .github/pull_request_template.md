## Pull request checklist

- [ ] Above 'Pull request checklist' add the Trello card URL
- [ ] Add a descriptive message for this change to the PR
- [ ] Run `python pr_actions.py` locally to update data, update devops/Deployment_Run.txt and update app_release_version in configuration/Sentry.py
- [ ] Run `black ./` locally
- [ ] Run `pylint <dashboard name> #UPDATE` locally and obtain a score of 10.00/10.00 
- [ ] Run `python -u -m pytest --headless tests --ignore=tests/visual/` locally and there are no failures
- [ ] Check that you're using polars and not pandas
- [ ] If adding a new page, check that you've added an integration test
- [ ] If adding a new data query, check that you've added a data test in tests/data_tests
- [ ] If visual changes are detected, check the snapshots by following the [process in the README](../README.md#process-for-updating-snapshots)         
- [ ] Include screenshot for any visual changes
- [ ] Consider accessibility if making changes that impact the UI (eg changes to HTML code or React components)
- [ ] Run Narrator in the DAP (using Microsoft Edge browser) to verify your changes are accessible to a screen reader if making changes that impact the UI.

### PR Description:
