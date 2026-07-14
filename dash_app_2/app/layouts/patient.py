import dash_bootstrap_components as dbc
from dash import dcc, html


layout = dbc.Row(
    [
        dbc.Col(
            dbc.Stack(
                [
                    html.H4("Filter"),
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
                        dbc.Col(
                            dcc.Graph(id="bar-patient-samples")
                        ),
                        class_name="border rounded p-2 shadow"
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(id="patient-journey")
                            ),
                            dcc.Dropdown(id="dropdown-patient-journey-y-axis")
                        ],
                        class_name="mt-3 border rounded p-2 pb-4 shadow",
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