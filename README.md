# dashboard-template
A template repository for creating data dashboards with Plotly

## Getting started

### Sign up for GitHub

1.  Sign up for a GitHub account
1.  Ask the existing team members within the Analytical Dashboards Microsoft Teams to give access to the repository. Make sure to accept the invitation.

**This project will be run in the DAP environment.**

### Setup your local development environment

1.  Set your default browser to Google Chrome - [instructions][Make Chrome your default browser].
1.  Open Anaconda Navigator via Start menu. **Note:** Anaconda asks if you want to update it, but it won't work.
1.  Install and launch VS Code (Visual Studio Code) from within the Anaconda Navigator. **Note** after installing VS Code, a Getting Started walkthrough is shown. Click the back button to escape.

[Make Chrome your default browser]: https://support.google.com/chrome/answer/95417?hl=en-GB&co=GENIE.Platform%3DDesktop

### Downloading the code from GitHub

1.  Create a folder on your desktop, for storing source code within if you don't have one already.
1.  From VS Code open the [Explorer window][explorer_window], the overlapping pages icon on left hand menu. Select the option to "Clone Repository". Click "Clone from GitHub"
1.  If prompted, authorize with GitHub.
1.  You should be prompted to enter a repository name. Type "communitiesuk/&lt;Your repository name&gt;". Then click on communitiesuk/&lt;Your repository name&gt;.
1.  As a destination, select your folder for storing the source code. Select "Sign in with browser" if the GitHub authorisation popup is shown.
1.  This pulls the code from GitHub to your local folder.
    Click "Open folder" option, and navigate to your newly created folder containing the repository code.
1.  Select "Yes, I trust the authors".
1.  While that is downloading, navigate to the `Git CMD` from the start menu and execute the below commands. Once you have executed the commands close `Git CMD`.

    **Note: You need to change the name/email to match your own and you need to include the quotation marks. You may like to copy the commands into a word document to edit them.**

```shell
git config --global user.name "Your Name"
git config --global user.email "Your.Name@communities.gov.uk"
``` 

[explorer_window]: https://code.visualstudio.com/docs/getstarted/userinterface#_explorer

### Installing packages

1.  [Open a command prompt terminal within VS Code][open-terminal], in which you'll start executing some commands. By default, the initial terminal will be a powershell terminal, and you will need to [switch to a command prompt shell][terminal-switch]. 
1.  Update the name field in environment.workspace.yml to the dashboard name
1.  Create a new conda environment by typing `conda env create -f environment.workspace.yml` into the terminal and executing the command by pressing the Enter key.
1.  Activate your conda environment with `conda activate <dashboard name> `
1. Close VS Code. Open Anaconda Navigator, select "&lt; Dashboard name &gt;" for the 'Application on' drop down menu, then select "Launch" VS Code. Click the bin icon on the terminal toolbar to close the terminal. Click the plus icon on the terminal toolbar to launch a new terminal.
1.  Install the [Microsoft Python][python_extension] extension for VS Code.
1.  Follow the [instructions for configuring the Python interpreter][configure_python_interpreter].

 **Note: If error when creating conda environment check conda version. Type 'conda --version' in VS Code terminal. conda 4.5.12 needs to be upgraded to 4.10.3. Contact DAP-support@communities.gov.uk**

[open-terminal]: https://code.visualstudio.com/docs/editor/integrated-terminal
[terminal-switch]: https://code.visualstudio.com/docs/editor/integrated-terminal#_terminal-shells
[python_extension]: https://marketplace.visualstudio.com/items?itemName=ms-python.python
[configure_python_interpreter]: https://code.visualstudio.com/docs/python/python-tutorial#_select-a-python-interpreter

### Running the application

1.  From your VS Code terminal, execute `python run.py`
1.  Wait for the message "Dash is running on ..." message to appear
1.  Navigate to http://localhost:8080/ in your browser within the AWS workspace. Note that http://localhost:8080/ is the address that dash will run on in your local machine.
1. Use Ctrl-C in the terminal to quit the python server. 

    **Note:** Terminal can only handle one command at a time, if the python server is running the terminal will not handle any further commands. To restart the server use `python run.py`

## Development

### Running tests

Writing and running automated tests ensures software is correct, reduces risk that users will experience bugs, and allows developers to move much faster as they can make changes with confidence that any breaks will be caught be the test suite. Once you have set up unit tests:

```bash
python -u -m pytest tests
```

### Running the code formatter

The [code formatter](https://black.readthedocs.io/en/stable/) ensures source code is formatted consistently. Running the code formatter makes changes automatically that then need to be committed.

```bash
black ./
```

### Running the linter

The linter checks for basic logic errors and bugs. Linting reports rule violations that must be corrected manually.  

```bash
pylint <Dashboard name>
```

###  Add reminder message to run formatter and linter before pushing to GitHub


Copy the following text to a new file called .git/hooks/pre-commit (You may need to create this file using File Explorer with [hidden files and folders turned on](https://support.microsoft.com/en-us/windows/view-hidden-files-and-folders-in-windows-97fbc472-c603-9d90-91d0-1166d1d9f4b5#WindowsVersion=Windows_11), as VS Code hides the .git directory by default):

```bash
#!/usr/bin/env bash
echo "Remember to run Black and Pylint before pushing to GitHub" 
```

### Retrieving data from CDS

1. From within the DAP AWS Workspace, open "Microsoft SQL Server Management Studio 18".
1. Enable [Export headers option][export-headers] and then restart the SQL Server Management Studio.
1. Enter the Server name as "DAP-SQLTEST\CDS", and under Options specify the Database name as "Dashboards".
1. Open the "New Query" from the Toolbar, paste in the query that corresponds to your table and execute.
1. Right click on the results set and select "Save Results as" to an appropriate place in the `data/` directory.

INSERT HERE SQL CHEAT SHEET 

For more information on accessing CDS you can find some more [detailed instructions][cds-documentation] from Mark Foster.

[export-headers]: https://solutioncenter.apexsql.com/sql-server-management-studio-ssms-how-to-save-results-with-headers/
[cds-documentation]: https://mhclg.sharepoint.com/:w:/r/sites/AnalyticalDashboards/_layouts/15/Doc.aspx?action=edit&sourcedoc=%7BC32BC170-2D98-4128-AD31-63FEFEFF0E0D%7D

## Deployment

### Staging

Code pushed to GitHub on the `main` branch is automatically deployed to a staging environment hosted in [Gov PaaS](https://www.cloud.service.gov.uk/), accessible at the link below:

> [https://data_dashboards.london.cloudapps.digital/](https://data_dashboards.london.cloudapps.digital/)

Post a message in the General channel on the Data Dashboard Microsoft Teams team to get the username and password.

### Production

1.  From VS Code navigate to File -> Open Folder and select `Q:\AnalyticalDashboards\data_dashboards`
1.  Pull the latest code from GitHub into that directory.
1.  Switch back to your local development environment.
1.  Send an email to DAP-Support@communities.gov.uk from your Communities email address, asking for the dashboard to be updated.  Sample message:
```
Dear DAP support,

Please could you update the Analytical Data Dashboard at
https://housing.pydash.infra.communities.gov.uk/

With the code in Q:\AnalyticalDashboards\data_dashboards

Many thanks,
Adrian
```
1. Notify the Development teams channel that a request has been made.
    The request should take less than 1 working day to be completed.

## Troubleshooting

### My DAP environment seems to be broken.  How can I get it working again?

Refresh the environment by running this command:

```bash
conda env update -f environment.workspace.yml
```

If this doesn't resolve the problem, deactivate and remove the `Dashboard name` Conda environment before running the environment setup steps in [Installing packages](###Installing packages) again.

## Customisation 

### Adding figure to dashboard
1.  Create figure function for specific chart type and save in figure folder on dashboard file
1.  Set a variable equal to the figure function and pass in the necessary parameters
1.  In order to return a graph, set a new variable and pass in dcc.Graph(with the id of your new figure)
```
barchart = bar_chart(df, "Category", "Value", color="Category")
barchart_dash = dcc.Graph(id="example bar chart", responsive=True, figure=barchart)
dashboard_content = [card(barchart_dash)]
```

## Deploying to Gov Paas
1.  Update required fields in deploy-staging.yml indicated by &lt;&gt; and a comment.
1.  Set up dedicated accounts - do not use your normal credentials whilst deploying with GitHub actions. Find out more about [configuring your CI tool accounts](https://docs.cloud.service.gov.uk/using_ci.html#configure-your-ci-tool-accounts) in GOV.UK PaaS.
1.  Store credentials in GitHub Actions - You should store your sensitive credentials in GitHub Actions. Store the username as GOV_PAAS_USER and the password as GOV_PAAS_PASS.

More information on secrets can be found [here](https://docs.github.com/en/actions/security-guides/encrypted-secrets)