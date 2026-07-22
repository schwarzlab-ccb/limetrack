import dash_bootstrap_components as dbc
from dash import dcc, html
from django_plotly_dash import DjangoDash

app = DjangoDash(name="Dashboard",
                 external_stylesheets=[dbc.themes.BOOTSTRAP],
                 add_bootstrap_links=True,
                 suppress_callback_exceptions=True                 
                 )

app.layout = dbc.Container(
    [
        dcc.Store(id="initial-app-state"),
        dcc.Store(id="app-state", storage_type="local"),
        dcc.Store(id="app-state-ready", data=0),
        dcc.Store(id="render-trigger", data=0),
        dcc.Store(id="filter-event-tissue-types"),
        dcc.Store(id="filter-event-entities"),
        dcc.Store(id="filter-event-entities-columns"),
        dcc.Store(id="filter-event-patients"),
        dcc.Store(id="filter-event-patient-journey-y-axis"),
        dcc.Store(id="filter-event-clinical-download"),
        dcc.Store(id="filter-event-clinical-patients"),
        dcc.Tabs(
            [
                dcc.Tab(label="Samples", value="sample-tracker-tab"),
                dcc.Tab(label="Clinical", value="clinical-tab"),
                dcc.Tab(label="Patient", value="patients-tab"),
            ],
            id="main-tabs",
            value="sample-tracker-tab",
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
