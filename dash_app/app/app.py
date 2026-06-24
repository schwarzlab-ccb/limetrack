import dash_bootstrap_components as dbc
from dash_app.app.dashboard import Dashboard
from dash import Dash
from django_plotly_dash import DjangoDash

app = DjangoDash(name="Dashboard",
                 external_stylesheets=[dbc.themes.BOOTSTRAP]
)

dashboard = Dashboard()

app.layout = dashboard.layout()