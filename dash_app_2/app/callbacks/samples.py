from dash_app_2.app.components.general import make_filterable_pie, make_card
from dash import Input, Output, State, callback_context, callback
from dash_app_2.app.utils.state_management import AppState
from dash_app_2.app.components.samples import (
    make_patient_timepoint_histogram,
    make_samples_entity_histogram,
)


def register_callbacks():
    @callback(
        Output("pie-tissue-types", "figure"),
        Output("dropdown-tissue-types", "options"),
        Output("dropdown-tissue-types", "value"),
        Input("app-state", "data"),
        prevent_initial_call=True
    )
    def on_app_state_changed_tissue_types(app_state: dict):
        state = AppState(app_state)
        df_timepoint = state.get_dataset("patient-timepoint")
        filter_ = state.get_filter("tissue-types")
        figure = make_filterable_pie(
            df_timepoint, "tissue_type", "Tissue Types", filter_
        )

        return (
            figure,
            filter_.options,
            filter_.selected
        )

    @callback(
        Output("pie-entities", "figure"),
        Output("dropdown-entities", "options"),
        Output("dropdown-entities", "value"),
        Input("app-state", "data"),
        prevent_initial_call=True
    )
    def on_app_state_changed_entities(app_state: dict):
        state = AppState(app_state)
        df_timepoint = state.get_dataset("patient-timepoint")
        filter_ = state.get_filter("entities")
        figure = make_filterable_pie(
            df_timepoint, "entity", "Entities", filter_
        )

        return (
            figure, 
            filter_.options,
            filter_.selected
        )
    
    @callback(
        Output("histogram-samples-entity", "figure"),
        Output("dropdown-columns", "options"),
        Output("dropdown-columns", "value"),
        Input("app-state", "data"),
        prevent_initial_call=True
    )
    def on_app_state_changed_sample_entities(app_state: dict):
        state = AppState(app_state)
        df_timepoint = state.get_dataset("patient-timepoint")
        filter_tissue_types = state.get_filter("tissue-types")
        filter_entities = state.get_filter("entities")
        filter_columns = state.get_filter("entities-columns")
        figure = make_samples_entity_histogram(
            df_timepoint, filter_tissue_types, filter_entities, filter_columns
        )
        
        return (
            figure , 
            filter_columns.options, 
            filter_columns.selected[0]
        )

    
    @callback(
        Output("histogram-patient-timepoints", "figure"),
        Input("app-state", "data"),
        prevent_initial_call=True
    )
    def on_app_state_changed_patient_timepoints(app_state: dict):
        state = AppState(app_state)
        df_timepoint = state.get_dataset("patient-timepoint")
        filter_tissue_types = state.get_filter("tissue-types")
        filter_entities = state.get_filter("entities")
        figure = make_patient_timepoint_histogram(
            df_timepoint, filter_tissue_types, filter_entities
        )

        return figure
    
    @callback(
        Output("stack-cards-sample-tracker", "children"),
        Input("app-state", "data"),
        prevent_initial_call=True
    )
    def on_app_state_changed_cards(app_state: dict):
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

    @callback(
        Output("app-state", "data",  allow_duplicate=True),
        State("app-state", "data"),
        Input("dropdown-tissue-types", "value"),
        Input("pie-tissue-types", "relayoutData"),
        prevent_initial_call=True,
    )
    def on_tissue_types_selection_changed(app_state: dict, dtt_values: list[str], pie_state: dict): 
        trigger_component_id = callback_context.triggered_id
        filter_name = "tissue-types"
        state = AppState(app_state)

        if trigger_component_id == "dropdown-tissue-types" and dtt_values is not None:
            state.update_filter_selection(filter_name, dtt_values)

        elif trigger_component_id == "pie-tissue-types" and isinstance(pie_state, dict):
            hiddenlabels: list[str] | None =  pie_state.get("hiddenlabels")

            if hiddenlabels is not None:
                state.update_filter_selection(filter_name, hiddenlabels, select_delta=True)

        return state.state

    @callback(
        Output("app-state", "data",  allow_duplicate=True),
        State("app-state", "data"),
        Input("dropdown-entities", "value"),
        Input("pie-entities", "relayoutData"),
        prevent_initial_call=True,
    )
    def on_entity_selection_changed(app_state: dict, de_values: list[str], pie_state: dict): 
        trigger_component_id = callback_context.triggered_id
        filter_name = "entities"
        state = AppState(app_state)

        if trigger_component_id == "dropdown-entities" and de_values is not None:
            state.update_filter_selection(filter_name, de_values)

        elif trigger_component_id == "pie-entities" and isinstance(pie_state, dict):
            hiddenlabels: list[str] | None =  pie_state.get("hiddenlabels")

            if hiddenlabels is not None:
                state.update_filter_selection(filter_name, hiddenlabels, select_delta=True)

        return state.state

    @callback(
        Output("app-state", "data",  allow_duplicate=True),
        State("app-state", "data"),
        Input("dropdown-columns", "value"),
        prevent_initial_call=True,
    )
    def on_column_selection_changed(app_state: dict, dc_value: list[str]):
        state = AppState(app_state)
        if dc_value is not None:
            state.update_filter_selection("entities-columns", dc_value)

        return state.state