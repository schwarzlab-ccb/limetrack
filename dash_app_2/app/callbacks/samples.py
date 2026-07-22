from dash_app_2.app.components.general import make_filterable_pie, make_card
from dash import Input, Output, State, no_update
from dash_app_2.app.utils.state_management import AppState
from dash_app_2.app.components.samples import (
    make_patient_timepoint_histogram,
    make_samples_entity_histogram,
)


def _get_triggered_component_id(callback_context) -> str | None:
    """
    This had to be added because django_plotly_dash does not have access to the callback_context
    global variable.
    Instead there is a callback_context given to the callbacks as an argument.
    (https://django-plotly-dash.readthedocs.io/en/latest/extended_callbacks.html)
    """
    if not callback_context.triggered:
        return None

    return callback_context.triggered[0]["prop_id"].rsplit(".", 1)[0]


def register_callbacks(app):
    @app.callback(
        Output("pie-tissue-types", "figure"),
        Input("app-state", "data"),
        Input("render-trigger", "data"),
        prevent_initial_call=True
    )
    def on_app_state_changed_tissue_types(app_state: dict, _render_trigger: int):
        state = AppState(app_state)
        df_timepoint = state.get_dataset("patient-timepoint")
        filter_ = state.get_filter("tissue-types")
        figure = make_filterable_pie(
            df_timepoint, "tissue_type", "Tissue Types", filter_
        )

        return figure

    @app.callback(
        Output("pie-entities", "figure"),
        Input("app-state", "data"),
        Input("render-trigger", "data"),
        prevent_initial_call=True
    )
    def on_app_state_changed_entities(app_state: dict, _render_trigger: int):
        state = AppState(app_state)
        df_timepoint = state.get_dataset("patient-timepoint")
        filter_ = state.get_filter("entities")
        figure = make_filterable_pie(
            df_timepoint, "entity", "Entities", filter_
        )

        return figure
    
    @app.callback(
        Output("histogram-samples-entity", "figure"),
        Input("app-state", "data"),
        Input("render-trigger", "data"),
        prevent_initial_call=True
    )
    def on_app_state_changed_sample_entities(app_state: dict, _render_trigger: int):
        state = AppState(app_state)
        df_timepoint = state.get_dataset("patient-timepoint")
        filter_tissue_types = state.get_filter("tissue-types")
        filter_entities = state.get_filter("entities")
        filter_columns = state.get_filter("entities-columns")
        figure = make_samples_entity_histogram(
            df_timepoint, filter_tissue_types, filter_entities, filter_columns
        )
        
        return figure

    @app.callback(
        Output("dropdown-tissue-types", "options"),
        Output("dropdown-tissue-types", "value"),
        Output("dropdown-entities", "options"),
        Output("dropdown-entities", "value"),
        Output("dropdown-columns", "options"),
        Output("dropdown-columns", "value"),
        Input("render-trigger", "data"),
        State("app-state", "data"),
        prevent_initial_call=True,
    )
    def initialise_filter_controls(_render_trigger: int, app_state: dict):
        state = AppState(app_state)
        tissue_types = state.get_filter("tissue-types")
        entities = state.get_filter("entities")
        columns = state.get_filter("entities-columns")

        return (
            tissue_types.options,
            tissue_types.selected,
            entities.options,
            entities.selected,
            columns.options,
            columns.selected[0] if columns.selected else None,
        )

    
    @app.callback(
        Output("histogram-patient-timepoints", "figure"),
        Input("app-state", "data"),
        Input("render-trigger", "data"),
        prevent_initial_call=True
    )
    def on_app_state_changed_patient_timepoints(
        app_state: dict, _render_trigger: int
    ):
        state = AppState(app_state)
        df_timepoint = state.get_dataset("patient-timepoint")
        filter_tissue_types = state.get_filter("tissue-types")
        filter_entities = state.get_filter("entities")
        figure = make_patient_timepoint_histogram(
            df_timepoint, filter_tissue_types, filter_entities
        )

        return figure
    
    @app.callback(
        Output("stack-cards-sample-tracker", "children"),
        Input("app-state", "data"),
        Input("render-trigger", "data"),
        prevent_initial_call=True
    )
    def on_app_state_changed_cards(app_state: dict, _render_trigger: int):
        state = AppState(app_state)
        df = state.get_dataset("patient-timepoint")
        df_filtered = df.loc[
            (df.entity.isin(state.get_filter("entities").selected))
            & (df.tissue_type.isin(state.get_filter("tissue-types").selected))
        ]

        cards =  [
            make_card(
                "Patients", df_filtered.patient_identifier.nunique()
            ),
            make_card(
                "Samples", df_filtered.shape[0]
            ),
            make_card(
                "Entities", df_filtered.entity.nunique()
            ),
            make_card(
               "Tissue Types", df_filtered.tissue_type.nunique()
            )
        ]

        return cards

    @app.callback(
        Output("filter-event-tissue-types", "data"),
        Input("dropdown-tissue-types", "value"),
        Input("pie-tissue-types", "relayoutData"),
        State("app-state", "data"),
        prevent_initial_call=True,
    )
    def on_tissue_types_selection_changed(
        dtt_values: list[str],
        pie_state: dict,
        app_state: dict,
        callback_context,
    ):
        trigger_component_id = _get_triggered_component_id(callback_context)
        filter_name = "tissue-types"
        selected = None

        if trigger_component_id == "dropdown-tissue-types" and dtt_values is not None:
            selected = dtt_values

        elif trigger_component_id == "pie-tissue-types" and isinstance(pie_state, dict):
            hiddenlabels: list[str] | None =  pie_state.get("hiddenlabels")

            if hiddenlabels is not None:
                filter_ = AppState(app_state).get_filter(filter_name)
                selected = [
                    option for option in filter_.options
                    if option not in hiddenlabels
                ]

        if selected is None:
            return no_update

        return {"name": filter_name, "selected": selected}

    @app.callback(
        Output("filter-event-entities", "data"),
        Input("dropdown-entities", "value"),
        Input("pie-entities", "relayoutData"),
        State("app-state", "data"),
        prevent_initial_call=True,
    )
    def on_entity_selection_changed(
        de_values: list[str],
        pie_state: dict,
        app_state: dict,
        callback_context,
    ):
        trigger_component_id = _get_triggered_component_id(callback_context)
        filter_name = "entities"
        selected = None

        if trigger_component_id == "dropdown-entities" and de_values is not None:
            selected = de_values

        elif trigger_component_id == "pie-entities" and isinstance(pie_state, dict):
            hiddenlabels: list[str] | None =  pie_state.get("hiddenlabels")

            if hiddenlabels is not None:
                filter_ = AppState(app_state).get_filter(filter_name)
                selected = [
                    option for option in filter_.options
                    if option not in hiddenlabels
                ]

        if selected is None:
            return no_update

        return {"name": filter_name, "selected": selected}

    @app.callback(
        Output("filter-event-entities-columns", "data"),
        Input("dropdown-columns", "value"),
        prevent_initial_call=True,
    )
    def on_column_selection_changed(dc_value: str):
        if dc_value is None:
            return no_update

        return {"name": "entities-columns", "selected": [dc_value]}
