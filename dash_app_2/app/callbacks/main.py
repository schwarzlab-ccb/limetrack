from dash_app_2.app.layouts import clinical, patient, samples
from dash_app_2.app.utils import database, redcap_connector
from dash import Output, Input, callback, State
from dash_app_2.app.utils.state_management import AppState
import dash_bootstrap_components as dbc


def register_callbacks():
    @callback(
        Output("app-state", "data"),
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
        state.add_filter(
            "patients", 
            df_timepoints.patient_identifier.unique().tolist(),
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

    @callback(
        Output("main-content-div", "children"),
        Input("main-tabs", "value"),
    )
    def on_tabs_value_changed(value: str):
        layout: dbc.Row = dbc.Row()

        match value:
            case "clinical-tab":
                layout = clinical.layout

            case "patients-tab":
                layout = patient.layout

            case _:
                layout = samples.layout

        return layout
    
    @callback(
        Output("app-state", "data", allow_duplicate=True),
        State("app-state", "data"),
        Input("main-tabs", "value"),
        prevent_initial_call=True
    )
    def on_tab_value_changed_refresh_state(app_state: dict, value: str):
        state = AppState(app_state)
        
        return state.state
