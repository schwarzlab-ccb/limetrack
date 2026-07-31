import dash_bootstrap_components as dbc
from dash_app_2.app.utils.schemas import Filter
import plotly.graph_objects as go
import plotly.express as px
from typing import Literal
from dash import html, dcc
import pandas as pd


def make_filterable_pie(
    df: pd.DataFrame,
    names_column: str,
    title: str,
    filter_: Filter,
    hole: float = 0.4,
    textinfo: Literal["text", "value"] = "value",
) -> go.Figure:
    figure = px.pie(
        df,
        names=names_column,
        title=title,
        hole=hole
    )
    figure.update_layout(
        hiddenlabels=list(set(filter_.options) - set(filter_.selected)),
    )
    figure.update_traces(
        textinfo=textinfo
    )

    return figure

def make_card(text: str, value: int | str) -> dbc.Card:
    card = dbc.Card(
        dbc.CardBody(
            [
                html.H1(str(value)),
                html.P(text)
            ],
        ),
        class_name="flex-fill shadow"
    )

    return card

def make_dropdown_with_header(header: str, dropdown: dcc.Dropdown) -> html.Div:
    component = html.Div([
        html.H6(header),
        dropdown,
        html.Br()])
    
    return component

def make_plot_with_dropdown(figure: go.Figure, id, dropdowns: list[html.Div | dcc.Dropdown]) -> dbc.Card:
    component = dbc.Card([
        dbc.CardBody([
            dcc.Graph(
                id=id,
                figure=figure
            ),
            *dropdowns])
    ])

    return component
