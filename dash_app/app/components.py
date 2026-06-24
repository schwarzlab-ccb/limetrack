from plotly.graph_objects import Figure
import dash_bootstrap_components as dbc
from dash import html, dcc


def Number(description: str, number: int) -> dbc.Card:
    card = dbc.Card([
        dbc.CardBody([
            html.H1(str(number)),
            html.P(description)
        ])
    ])   

    return card

def Plot(figure: Figure) -> dbc.Card:
    component = dbc.Card([
        dbc.CardBody([
            dcc.Graph(
                figure=figure
            )
        ])
    ])

    return component