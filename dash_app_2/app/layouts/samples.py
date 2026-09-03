import dash_bootstrap_components as dbc
from dash import dcc, html


layout = dbc.Row(
    [
        dbc.Col(
            dbc.Stack(
                [
                    html.H4("Filter"),
                    dcc.Dropdown(id="dropdown-tissue-types", multi=True),
                    dcc.Dropdown(id="dropdown-entities", multi=True),
                    dcc.Graph(id="pie-entities", className="border rounded"),
                    dcc.Graph(id="pie-tissue-types", className="border rounded"),
                    
                ], 
                class_name="gap-1 p-2 border rounded shadow h-100"
            ), 
            id="col-sidebar",
            width=3,
        ),
        dbc.Col(
            dbc.Container(
                [
                    dbc.Row(
                        dbc.Stack(
                            id="stack-cards-sample-tracker",
                            direction="horizontal",
                            gap=3,
                            class_name="d-flex p-0"
                        )
                    ),
                    dbc.Row(
                        dbc.Col([dcc.Graph(id="histogram-patient-timepoints")]),
                        class_name="mt-3 border rounded p-2 shadow"
                    ),
                    dbc.Row(
                        dbc.Col([
                            dcc.Graph(id="histogram-samples-entity"),
                            html.H6("Color-code bars by"),
                            dcc.Dropdown(id="dropdown-columns"),
                        ]),
                        class_name="mt-3 border rounded p-2 pb-4 shadow"
                    )
                ],
                fluid=True,
                id="container-dashboard",
                class_name="h-100 m-auto"
            ),
            width=9, 
            id="col-dashboard"
        )
    ],
    id="main-row",
    class_name="h-100"
)