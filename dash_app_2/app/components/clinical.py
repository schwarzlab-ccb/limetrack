from dash_app_2.app.utils.schemas import Filter
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def make_age_histogram(df: pd.DataFrame, filter_: Filter) -> go.Figure:
    df = df.loc[
        df.pid.isin(filter_.selected)
    ]

    fig = px.histogram(
        df,
        x="age_at_diagnosis",
        title="Age at Diagnosis",
    )
    fig.update_layout(
        yaxis_title="Patients [N]",
        xaxis = dict(
            title="Age",
            tickmode = 'array',
            tickvals = list(range(0, int(df.age_at_diagnosis.max()), 10)),
            range=[0, int(df.age_at_diagnosis.max())]
        )
    )

    return fig