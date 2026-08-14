from dash_app_2.app.utils.schemas import Filter
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def make_patient_timepoint_histogram(
    df_orig: pd.DataFrame,
    filter_tissue_types: Filter,
    filter_entities: Filter
) -> go.Figure:
    df = df_orig.loc[
        (df_orig.tissue_type.isin(filter_tissue_types.selected)) & \
        (df_orig.entity.isin(filter_entities.selected))
    ]
    df_grouped = (
        df.loc[:, ["patient_identifier", "timepoint", "entity"]]
        .groupby(by=["patient_identifier", "timepoint"])
        .count()
        .reset_index()
    )
    df_grouped.columns = ["patient_identifier", "timepoint", "n_samples"]
    df_grouped["n_samples_legend"] = df_grouped.n_samples.apply(
        lambda n: str(n) if n <= 10 else "> 10"
    )

    fig = px.histogram(
        df_grouped,
        x="timepoint",
        color="n_samples_legend",
        title = "Patients per Timepoint",
        category_orders={
            "n_samples_legend": list(
                sorted(
                    df_grouped.n_samples_legend.unique(), 
                    key=lambda v: int(v) if not v.startswith(">") else 11
                )
            )
        },
        labels={
            "n_samples_legend": "Samples [N]" 
        }
    )
    fig.update_layout(
        xaxis_title="Timepoint",
        yaxis_title="Patients [N]",
        bargap=0.1,
        xaxis = dict(
            tickmode = 'array',
            tickvals = list(range(df_orig.timepoint.max() + 1)),
            autorange=False,
            range=[df_orig.timepoint.min() - 1, df_orig.timepoint.max() + 1]
        )
    )

    return fig

def make_samples_entity_histogram(
    df_orig: pd.DataFrame,
    filter_tissue_types: Filter,
    filter_entities: Filter,
    filter_columns: Filter,
) -> go.Figure:
    df = df_orig.loc[
        df_orig.tissue_type.isin(filter_tissue_types.selected)
        & (df_orig.entity.isin(filter_entities.selected))
    ]
    selected_column = filter_columns.selected[0]
    color_mapping = filter_columns.mappings
    df = df.sort_values(by="entity")

    if color_mapping is None:
        color_mapping = {}

    mapped_name = color_mapping.get(selected_column)

    fig = px.histogram(
        df,
        x="entity",
        color=mapped_name,
        labels={
            mapped_name: selected_column
        },
        category_orders={
            "entity": list(sorted(df["entity"].unique())),
            mapped_name: list(sorted(df[mapped_name].unique()))
        },
        title = "Samples per Entity"
    )
    fig.update_layout(
        yaxis_title="Samples [N]",
        xaxis = dict(
            title = "Entity",
            # tickmode = 'array',
            # tickvals = [0,1,2],
            # ticktext = list(sorted(df.entity.unique())),
        )
    )

    return fig
