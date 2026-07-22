from dash_app_2.app.components.clinical import make_age_histogram
from dash_app_2.app.utils.state_management import AppState
from dash import Output, Input, State, no_update
from dash_app_2.app.components.general import make_card



def register_callbacks(app):
    @app.callback(
        Output("stack-cards-clinical", "children"),
        Input("app-state", "data"),
        Input("render-trigger", "data"),
        prevent_initial_call=True
    )
    def on_app_state_changed_cards_redcap(app_state: dict, _render_trigger: int):
        state = AppState(app_state)
        df_therapies = state.get_dataset("redcap-therapy")
        df_samples = state.get_dataset("redcap-samples")
        df_patients = state.get_dataset("redcap-base")
        filter_ = state.get_filter("clinical-patients")

        df_th_filtered = df_therapies.loc[
            df_therapies.pid.isin(filter_.selected)
        ]
        df_sam_filtered = df_samples.loc[
            df_samples.pid.isin(filter_.selected)
        ]
        df_pat_filtered = df_patients.loc[
            df_patients.pid.isin(filter_.selected)
        ]

        cards = [
            make_card("Patients", len(filter_.selected)),
            make_card("Therapies", df_th_filtered.shape[0]),
            make_card("Samples", df_sam_filtered.shape[0]),
            make_card(
                "Patients Fully Documented",
                df_pat_filtered.loc[
                    df_pat_filtered.documentation_complete == "Complete"
                ].shape[0],
            ),
        ]
        return cards
    

    @app.callback(
        Output("grid-clinical-patients", "rowData"),
        Output("grid-clinical-patients", "selectedRows"),
        Output("grid-clinical-patients", "columnDefs"),
        Input("app-state", "data"),
        Input("render-trigger", "data"),
        prevent_initial_call=True
    )
    def on_app_state_changed_clinical_patients_grid(
        app_state: dict, _render_trigger: int
    ):
        state = AppState(app_state)
        filter_ = state.get_filter("clinical-patients")
        df = state.get_dataset("redcap-base")
        columns_defs = [
            {
                "field": column, 
                "filter": "agNumberColumnFilter", 
                "filterParams": {
                    "buttons": ["reset", "apply"],
                },
                "maxWidth": 100
            }
            if column == "age_at_diagnosis"
            else {
                "field": column,
                "filterParams": {
                    "buttons": ["reset", "apply"],
                },
            }
            for column in df.columns
        ]
        selected_rows = df.loc[
            df.pid.isin(filter_.selected)
        ].to_dict("records")

        return (
            df.to_dict("records"),
            selected_rows,
            columns_defs,
        )
    
    @app.callback(
        Output("grid-clinical-therapies", "rowData"),
        Output("grid-clinical-therapies", "columnDefs"),
        Input("app-state", "data"),
        Input("render-trigger", "data"),
        prevent_initial_call=True
    )
    def on_app_state_changed_clinical_therapy_grid(
        app_state: dict, _render_trigger: int
    ):
        state = AppState(app_state)
        df = state.get_dataset("redcap-therapy")
        filter_ = state.get_filter("clinical-patients")
        columns_defs = [ 
            {"field": column} for column in df.columns
        ]
        df = df.loc[
            df.pid.isin(filter_.selected)
        ]

        return (
            df.to_dict("records"),
            columns_defs,
        )
    
    @app.callback(
        Output("grid-clinical-samples", "rowData"),
        Output("grid-clinical-samples", "columnDefs"),
        Input("app-state", "data"),
        Input("render-trigger", "data"),
        prevent_initial_call=True
    )
    def on_app_state_changed_clinical_samples_grid(
        app_state: dict, _render_trigger: int
    ):
        state = AppState(app_state)
        df = state.get_dataset("redcap-samples")
        filter_ = state.get_filter("clinical-patients")

        columns_defs = [ 
            {"field": column} for column in df.columns
        ]
        df = df.loc[
            df.pid.isin(filter_.selected)
        ]

        return (
            df.to_dict("records"),
            columns_defs,
        )
    
    @app.callback(
        Output("dropdown-clinical-download", "options"),
        Output("dropdown-clinical-download", "value"),
        Input("render-trigger", "data"),
        State("app-state", "data"),
        prevent_initial_call=True,
    )
    def initialise_filter_controls(
        _render_trigger: int, app_state: dict
    ):
        state = AppState(app_state)
        filter_ = state.get_filter("clinical-download-selection")

        return filter_.options, filter_.selected
    
    @app.callback(
        Output("histogram-clinical-age-at-diagnosis", "figure"),
        Input("app-state", "data"),
        Input("render-trigger", "data"),
        prevent_initial_call=True
    )
    def on_app_state_changed_age_at_diagnosis(
        app_state: dict, _render_trigger: int
    ):
        state = AppState(app_state)
        df = state.get_dataset("redcap-base")
        filter_ = state.get_filter("clinical-patients")

        figure = make_age_histogram(df, filter_)

        return figure
        
    @app.callback(
        Output("filter-event-clinical-download", "data"),
        Input("dropdown-clinical-download", "value"),
        prevent_initial_call=True
    )
    def on_dropdown_clinical_download_selection_changed(value: list[str]):
        if value is None:
            return no_update

        return {"name": "clinical-download-selection", "selected": value}

    @app.callback(
        Output("filter-event-clinical-patients", "data"),
        Input("grid-clinical-patients", "virtualRowData"),
        State("grid-clinical-patients", "filterModel"),
        prevent_initial_call=True
    )
    def on_grid_clinical_patients_rows_changed(
        data: list[dict] | None, filter_model: dict | None
    ):
        if data is None or (not data and not filter_model):
            return no_update

        pids = [row["pid"] for row in data]

        return {"name": "clinical-patients", "selected": pids}
    
    @app.callback(
        Output("grid-clinical-patients", "exportDataAsCsv"),
        Output("grid-clinical-therapies", "exportDataAsCsv"),
        Output("grid-clinical-samples", "exportDataAsCsv"),
        Input("button-clinical-download", "n_clicks"),
        State("app-state", "data"),
        prevent_initial_call=True
    )
    def on_download_button_clicked(n_clicks: int, app_state: dict):
        state = AppState(app_state)
        filter_ = state.get_filter("clinical-download-selection")
        selected = filter_.selected
        response = [False, False, False]

        if n_clicks:
            if "Patients" in selected:
                response[0] = True

            if "Therapies" in selected:
                response[1] = True
            
            if "Samples" in selected:
                response[2] = True

        return tuple(response)
