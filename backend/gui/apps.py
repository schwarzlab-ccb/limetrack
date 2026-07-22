from django.apps import AppConfig
from dash_app_2.app.callbacks import main, patient, samples, clinical


class GuiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.gui"

    def ready(self) -> None:
        from .signals import user
        # Register the DjangoDash application and its callbacks when Django
        # starts. Do not rely on a view module importing it as a side effect.
        from dash_app_2.app import app as dashboard_app
        main.register_callbacks(dashboard_app.app)
        clinical.register_callbacks(dashboard_app.app)
        patient.register_callbacks(dashboard_app.app)
        samples.register_callbacks(dashboard_app.app)
