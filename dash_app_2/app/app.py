from dash_app_2.app.callbacks import main, patient, samples, clinical
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
from django_plotly_dash import DjangoDash

app = DjangoDash(name="Dashboard",
                 external_stylesheets=[dbc.themes.BOOTSTRAP],
                 add_bootstrap_links=True,
                 suppress_callback_exceptions=True                 
                 )

main.register_callbacks()
clinical.register_callbacks()
patient.register_callbacks()
samples.register_callbacks()

app.layout = dbc.Container(
    [
        dcc.Store(id="app-state", storage_type="local"),
        dcc.Tabs(
            [
                dcc.Tab(label="Samples", value="sample-tracker-tab"),
                dcc.Tab(label="Clinical", value="clinical-tab"),
                dcc.Tab(label="Patient", value="patients-tab"),
            ],
            id="main-tabs",
            className="flex-fill"
        ),
        html.Div(
            id="main-content-div",
            className="mt-3 flex-fill"
        )
    ],   
    id="main-container",
    fluid=True,
    class_name="vh-100 p-0 d-flex flex-column"
)