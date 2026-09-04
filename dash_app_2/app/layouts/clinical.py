import dash_bootstrap_components as dbc
import dash_ag_grid as dag
from dash import dcc, html


layout = dbc.Row(
    [
        dbc.Col(
            html.Div(
                dbc.Stack(
                    [
                        dbc.Stack(
                            [
                                dcc.Graph(id="histogram-clinical-age-at-diagnosis"),
                            ],
                            gap=1,
                        ),
                        dbc.Stack(
                            [
                                html.Hr(),
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="dropdown-clinical-download",
                                            value=["Patients", "Therapies", "Samples"],
                                            multi=True,
                                        )
                                    ]
                                ),
                                dcc.Button("Download", id="button-clinical-download"),
                            ],
                            gap=1,
                        ),
                    ],
                    gap=3,
                ),
                className="border rounded shadow h-100 p-2",
            ),
            id="col-sidebar",
            class_name="p-2",
            width=3,
        ),
        dbc.Col(
            dbc.Container(
                [
                    dbc.Row(
                        dbc.Stack(
                            id="stack-cards-clinical",
                            direction="horizontal",
                            gap=3,
                            class_name="d-flex p-0"
                        ),
                        class_name="p-2"
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dag.AgGrid(
                                    defaultColDef={"filter": True},
                                    id="grid-clinical-patients",
                                    csvExportParams={
                                        "fileName": "patients.csv",
                                        "allColumns": True,
                                    },
                                    columnSize="autoSize",
                                    className="h-100 shadow",
                                    dashGridOptions={
                                        "theme": {
                                            "function": """themeQuartz.withParams({
                                                headerBackgroundColor: '#636EFADA',
                                            })"""
                                        }}
                                ),
                                width=5,
                                class_name="p-2",
                            ),
                            dbc.Col(
                                [
                                    dbc.Row(
                                        dbc.Col(
                                            dag.AgGrid(
                                                defaultColDef={"filter": False},
                                                id="grid-clinical-therapies",
                                                csvExportParams={
                                                    "fileName": "therapies.csv",
                                                    "allColumns": True,
                                                },
                                                columnSize="autoSize",
                                                className="h-100 shadow",
                                                dashGridOptions={
                                                    "theme": {
                                                        "function": """themeQuartz.withParams({
                                                            headerBackgroundColor: '#EF553BDA',
                                                        })"""
                                                    }}
                                            ),
                                            class_name="p-2",
                                        ),
                                        class_name="h-50",
                                    ),
                                    dbc.Row(
                                        dbc.Col(
                                            dag.AgGrid(
                                                defaultColDef={"filter": False},
                                                id="grid-clinical-samples",
                                                csvExportParams={
                                                    "fileName": "samples.csv",
                                                    "allColumns": True,
                                                },
                                                columnSize="autoSize",
                                                className="h-100 shadow",
                                                dashGridOptions={
                                                    "theme": {
                                                        "function": """themeQuartz.withParams({
                                                            headerBackgroundColor: '#00CC96DA',
                                                        })"""
                                                    }}
                                            ),
                                            class_name="p-2",
                                        ),
                                        class_name="h-50",
                                    ),
                                ],
                                width=7,
                            ),
                        ],
                        class_name="flex-fill"
                    )
                ],
                fluid=True,
                class_name="h-100 m-auto d-flex flex-column"
            ),
            id="col-dashboard",
            width=9,
        ),
    ],
    id="main-row",
    class_name="h-100",
)