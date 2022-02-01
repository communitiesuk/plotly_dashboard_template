"""
Data visualizations for the Department of Levelling Up, Housing and Communities
"""

import dash


from lib.absolute_path import absolute_path

app = dash.Dash(__name__, suppress_callback_exceptions=True)

with open(absolute_path("template.html"), encoding="utf-8") as f:
    app.index_string = f.read()

server = app.server
