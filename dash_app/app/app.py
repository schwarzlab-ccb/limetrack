import dash_bootstrap_components as dbc
from dash_app.app.dashboard import Dashboard
from dash import Dash
from django_plotly_dash import DjangoDash

app = DjangoDash(name="Dashboard",
                 external_stylesheets=[dbc.themes.BOOTSTRAP],
                 add_bootstrap_links=True)

dashboard = Dashboard()

app.layout = dashboard.layout()