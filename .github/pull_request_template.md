## Pull request checklist

- [ ] Above 'Pull request checklist' add the Trello card URL
- [ ] Add a descriptive message for this change to the PR
- [ ] Run `black ./` locally
- [ ] Run `pylint <dashboard name>` locally and obtain a score of 10.00/10.00
- [ ] Run `python -u -m pytest --headless tests --ignore=tests/visual/` locally and there are no failures
- [ ] If visual changes are detected, check the snapshots *ADD LINK TO README HERE IF USING VISUAL TESTS*
- [ ] Include screenshot for any visual changes
- [ ] Consider accessibility if making changes that impact the UI (eg changes to HTML code or React components)
- [ ] Run Narrator in the DAP (using Microsoft Edge browser) to verify your changes are accessible to a screen reader if making changes that impact the UI.

### PR Description:
