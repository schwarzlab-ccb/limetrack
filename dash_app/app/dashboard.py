import dash_bootstrap_components as dbc
from dash_app.app.components import Number, Plot
from dash_app.app import redcap, database
import plotly.express as px


class Dashboard:
    def _amount_patients_card(self) -> dbc.Card:
        n_patients = database.get_amount_patients()
        component = Number(
            "Patients Sample Tracker", 
            n_patients
        )

        return component
    
    def _amount_samples_card(self) -> dbc.Card:
        n_samples = database.get_amount_samples()
        component = Number(
            "Amount Samples",
            n_samples
        )

        return component
    
    def _amount_sites_card(self) -> dbc.Card:
        n_sites = database.get_amount_recruiting_sites()
        component = Number(
            "Amount Recruiting Sites",
            n_sites
        )
        
        return component
    
    def _sample_localisations(self) -> dbc.Card:
        df = database.get_sample_localisations()
        df.sort_values(
            by="n_samples", 
            ascending=False,
            inplace=True
        )
        figure = px.bar(
            df,
            x="localisation",
            y="n_samples",
            title=f"Sample Localisation (N<sub>Localisations</sub> = {df.shape[0]})",
            labels={
                "localisation": "Localisation",
                "n_samples": "Samples [N]"
            }
        )
        component = Plot(figure)

        return component
    
    def _sample_entities(self) -> dbc.Card:
        df = database.get_sample_entites()
        df.sort_values(
            by="n_samples",
            ascending=False,
            inplace=True
        )
        figure = px.bar(
            df,
            x="entity",
            y="n_samples",
            title=f"Sample Entities (N<sub>Entities</sub> = {df.shape[0]})",
            labels={
                "entity": "Entity",
                "n_samples": "Samples [N]"
            }
        )
        component = Plot(figure)

        return component
    
    def _redcap_amount_patients(self) -> dbc.Card:
        n_patients = redcap.get_amount_patients()
        component = Number(
            "Patients RedCap",
            n_patients
        )

        return component

    def _redcap_amount_samples(self) -> dbc.Card:
        n_patients = redcap.get_amount_samples()
        component = Number(
            "Samples RedCap",
            n_patients
        )

        return component
    
    def _redcap_amount_therapies(self) -> dbc.Card:
        n_therapies = redcap.get_amount_therapies()
        component = Number(
            "Documented Therapies",
            n_therapies
        )

        return component
    
    def _redcap_kind_of_therapy(self) -> dbc.Card:
        df = redcap.get_therapy_kinds()
        df.sort_values(
            by="n_therapies", 
            ascending=False, 
            inplace=True
        )
        figure = px.bar(
            df,
            x="therapy_kind",
            y="n_therapies",
            title=f"Therapies Kinds (N<sub>Therapy Kinds</sub> = {df.shape[0]})",
            labels={
                "therapy_kind": "Kind Of Therapy",
                "n_therapies": "Therapies [N]"
            }
        )
        component = Plot(figure)

        return component
    
    def _redcap_goal_of_therapy(self) -> dbc.Card:
        df = redcap.get_therapy_goals()
        df.sort_values(
            by="n_therapies", 
            ascending=False, 
            inplace=True
        )
        figure = px.bar(
            df,
            x="therapy_goal",
            y="n_therapies",
            title=f"Therapies Goals (N<sub>Therapy Goals</sub> = {df.shape[0]})",
            labels={
                "therapy_goal": "Goal Of Therapy",
                "n_therapies": "Therapies [N]"
            }
        )
        component = Plot(figure)

        return component

    def layout(self) -> dbc.Stack:
        dashboard = dbc.Stack(
            [
                dbc.Row([
                    dbc.Col(
                        dbc.Stack(
                            [
                                self._amount_samples_card(),
                                self._amount_patients_card(),
                                self._amount_sites_card()
                            ],
                            gap=5
                            
                        ),
                        width=2
                    ),
                    dbc.Col(
                        [
                            self._sample_entities()
                        ],
                        width=5
                    ),
                    dbc.Col(
                        [
                            self._sample_localisations()
                        ],
                        width=5
                    )
                ]),
                dbc.Row([
                    dbc.Col(
                        [
                            self._redcap_kind_of_therapy()
                        ],
                        width=5
                    ),
                    dbc.Col(
                        [
                            self._redcap_goal_of_therapy()
                        ],
                        width=5
                    ),
                    dbc.Col(
                        dbc.Stack(
                            [
                                self._redcap_amount_patients(),
                                self._redcap_amount_samples(),
                                self._redcap_amount_therapies(),
                            ],
                            gap=5
                        ),
                        width=2
                    )
                ]),
            ], 
            gap=3
        )

        return dashboard