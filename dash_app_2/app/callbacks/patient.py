from dash_app_2.app.components.general import make_card
from dash_app_2.app.utils.state_management import AppState
from dash import Input, Output, State, callback
from dash_app_2.app.components.patient import (
    patient_samples_tumor_cell_content,
    patient_journey_samples_and_therapies,
)


def register_callbacks():
    @callback(
        Output('dropdown-patients', 'options'),
        Output('dropdown-patients', 'value'),
        Input("app-state", "data"),
        prevent_initial_call=True
    )
    def on_app_state_changed_patients_dropdown(app_state: dict):
        state = AppState(app_state)
        filter_ = state.get_filter("patients")

        return filter_.options, filter_.selected
    
    @callback(
        Output("dropdown-patient-journey-y-axis", "options"),
        Output("dropdown-patient-journey-y-axis", "value"),
        Input("app-state", "data"),
        prevent_initial_call=True
    )
    def on_app_state_changed_y_axis_dropdown(app_state: dict):
        state = AppState(app_state)
        filter_ = state.get_filter("patient-journey-y-axis")

        return filter_.options, filter_.selected
    
    @callback(
        Output("stack-cards-patient", "children"),
        Input("app-state", "data"),
        prevent_initial_call=True
    )
    def on_app_state_changed_cards(app_state: dict):
        state = AppState(app_state)
        df = state.get_dataset("redcap-base")
        df_filtered = df.loc[
            (df.pid.isin(state.get_filter("patients").selected))
        ]
        cards = []

        if not df_filtered.empty:
            cards =  [
                make_card(
                    "Patient Identifier", df_filtered.pid.iloc[0]
                ),
                make_card(
                    "Sex", df_filtered.sex.iloc[0]
                ),
                make_card(
                    "Age at Diagnosis", df_filtered.age_at_diagnosis.iloc[0]
                ),
                make_card(
                    "Diagnosis", df_filtered.icd10.iloc[0]
                ),
                make_card(
                    "Documentation Status", df_filtered.documentation_complete.iloc[0]
                )
            ]

        return cards
    
    @callback(
        Output("app-state", "data", allow_duplicate=True),
        State("app-state", "data"),
        Input("dropdown-patients", "value"),
        prevent_initial_call=True
    )
    def on_patients_dropdown_value_changed(app_state: dict, value: str):
        state = AppState(app_state)

        if value is not None:
            state.update_filter_selection("patients", value)

        return state.state
    
    @callback(
        Output("app-state", "data", allow_duplicate=True),
        State("app-state", "data"),
        Input("dropdown-patient-journey-y-axis", "value"),
        prevent_initial_call=True
    )
    def on_y_axis_dropdown_value_changed(app_state: dict, value: str):
        state = AppState(app_state)
        
        if value is not None:
            state.update_filter_selection("patient-journey-y-axis", value)

        return state.state


    @callback(
        Output('bar-patient-samples', 'figure'),
        Input("app-state", "data"),
        prevent_initial_call=True
    )
    def update_sample_plot(app_state: dict):
        state = AppState(app_state)
        filter_ = state.get_filter("patients")
        df_patient = state.get_dataset("patient-timepoint")

        return patient_samples_tumor_cell_content(filter_.selected[0], df_patient)

    @callback(
        Output('patient-journey', 'figure'),
        Input("app-state", "data"),
        prevent_initial_call=True
    )
    def update_therapies_plot(app_state: dict):
        state = AppState(app_state)
        selected_patient = state.get_filter("patients").selected[0]
        filter_selected_y_axis = state.get_filter("patient-journey-y-axis")
        selected_y_axis = filter_selected_y_axis.map_filter_value(
            filter_selected_y_axis.selected[0]
        )
        df_redcap = state.get_dataset("therapies-start-end")
        df_patient = state.get_dataset("patient-timepoint")

        figure = patient_journey_samples_and_therapies(
            selected_patient, selected_y_axis, df_redcap, df_patient
        )

        return figure