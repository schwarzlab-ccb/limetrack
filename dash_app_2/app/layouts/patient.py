import dash_bootstrap_components as dbc
from dash import dcc, html


layout = dbc.Row(
    [
        dbc.Col(
            dbc.Stack(
                [
                    html.H4("Select patient"),
                    dcc.Dropdown(id="dropdown-patients")
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
                            id="stack-cards-patient",
                            direction="horizontal",
                            gap=3,
                            class_name="d-flex p-0 mb-3"
                        )
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(id="patient-journey")
                            ),
                            html.H6("Display samples'"),
                            dcc.Dropdown(
                                id="dropdown-patient-journey-y-axis",
                                value="Localisation",
                            )
                        ],
                        class_name="mt-3 border rounded p-2 pb-4 shadow",
                    ),
                    dbc.Row(
                        dbc.Col(
                            dcc.Graph(id="bar-patient-samples")
                        ),
                        class_name="border rounded p-2 shadow"
                    ),
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