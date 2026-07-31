from dash_app_2.app.layouts import clinical, patient, samples
from dash_app_2.app.utils import database, redcap_connector
from dash import Output, Input, State, no_update
from dash_app_2.app.utils.state_management import AppState
import dash_bootstrap_components as dbc


def register_callbacks(app):
    @app.callback(
        Output("initial-app-state", "data"),
    )
    def initialise_app_state():
        state = AppState.initialize()
        df_therapies = redcap_connector.get_therapies_start_to_end()
        df_base_redcap = redcap_connector.get_redcap_base_data()
        df_therapy_redcap = redcap_connector.get_therapy_data()
        df_timepoints = database.get_patient_timepoint_data() 
        df_samples_redcap = redcap_connector.get_samples()

        state.add_filter(
            "entities",
            df_timepoints.entity.unique().tolist(),
            df_timepoints.entity.unique().tolist(),
        )
        state.add_filter(
            "tissue-types",
            df_timepoints.tissue_type.unique().tolist(),
            df_timepoints.tissue_type.unique().tolist(),
        )
        state.add_filter(
            "entities-columns",
            [
                "Recruiting Site",
                "Sex",
                "Spl Status",
                "Sclab Status"
            ],
            ["Recruiting Site",],
            {
                "Recruiting Site": "recruiting_site",
                "Sex": "sex",
                "Spl Status": "spl_status",
                "Sclab Status": "sclab_status"
            }  
        )
        patient_list = list(set(df_timepoints.patient_identifier.unique().tolist() + df_base_redcap.pid.unique().tolist()))
        patient_list.sort()
        state.add_filter(
            "patients", 
            patient_list,
            [df_timepoints.patient_identifier.unique().tolist()[0]]
        )
        state.add_filter(
            "patient-journey-y-axis",
            [
                "Localisation",
                "Type of Intervention",
                "Tissue Type"
            ],
            ["Localisation"],
            {
                "Localisation": "localisation",
                "Type of Intervention": "type_of_intervention",
                "Tissue Type": "tissue_type"
            }
        )
        state.add_filter(
            "clinical-patients",
            df_base_redcap.pid.unique().tolist(),
            df_base_redcap.pid.unique().tolist(),
        )
        state.add_filter(
            "clinical-download-selection",
            ["Patients", "Therapies", "Samples"],
            ["Patients", "Therapies", "Samples"]
        )
        state.add_dataset("therapies-start-end", df_therapies)
        state.add_dataset("redcap-therapy", df_therapy_redcap)
        state.add_dataset("redcap-samples", df_samples_redcap)
        state.add_dataset("patient-timepoint", df_timepoints)
        state.add_dataset("redcap-base", df_base_redcap)

        return state.state
    
    """
    This callback is necessary because django-plotly-dash cannot handle multiple
    callbacks having the same Output. In our case that has been "app-state".
    So instead we have a callback now that receives all control fields (filter dropdowns)
    as Inputs and forwards them to the app-state.

    """
    @app.callback(
        Output("app-state", "data"),
        Output("app-state-ready", "data"),
        Input("initial-app-state", "data"),
        Input("filter-event-tissue-types", "data"),
        Input("filter-event-entities", "data"),
        Input("filter-event-entities-columns", "data"),
        Input("filter-event-patients", "data"),
        Input("filter-event-patient-journey-y-axis", "data"),
        Input("filter-event-clinical-download", "data"),
        Input("filter-event-clinical-patients", "data"),
        State("app-state", "data"),
        prevent_initial_call=True,
    )
    def update_app_state(
        initial_app_state: dict,
        tissue_types_event: dict,
        entities_event: dict,
        entities_columns_event: dict,
        patients_event: dict,
        patient_journey_y_axis_event: dict,
        clinical_download_event: dict,
        clinical_patients_event: dict,
        app_state: dict,
        callback_context,
    ):
        if not callback_context.triggered:
            return no_update, no_update

        trigger_id = callback_context.triggered[0]["prop_id"].rsplit(".", 1)[0]
        if trigger_id == "initial-app-state":
            return initial_app_state, 1

        events = {
            "filter-event-tissue-types": tissue_types_event,
            "filter-event-entities": entities_event,
            "filter-event-entities-columns": entities_columns_event,
            "filter-event-patients": patients_event,
            "filter-event-patient-journey-y-axis": patient_journey_y_axis_event,
            "filter-event-clinical-download": clinical_download_event,
            "filter-event-clinical-patients": clinical_patients_event,
        }
        event = events.get(trigger_id)
        if event is None or app_state is None:
            return no_update, no_update

        state = AppState(app_state)
        state.update_filter_selection(event["name"], event["selected"])

        return state.state, no_update

    @app.callback(
        Output("main-content-div", "children"),
        Output("render-trigger", "data"),
        Input("main-tabs", "value"),
        Input("app-state-ready", "data"),
        State("render-trigger", "data"),
        prevent_initial_call=True,
    )
    def on_tabs_value_changed(
        value: str, _app_state_ready: int, render_trigger: int
    ):
        layout: dbc.Row = dbc.Row()

        match value:
            case "clinical-tab":
                layout = clinical.layout

            case "patients-tab":
                layout = patient.layout

            case _:
                layout = samples.layout

        return layout, (render_trigger or 0) + 1
