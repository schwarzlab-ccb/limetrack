from django.contrib.auth.mixins import LoginRequiredMixin
from backend.gui.utils.colors import Saturn3Colors
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView
from ..models import HistopathologicalSample
from django.db.models import QuerySet
from django.shortcuts import render
import plotly.graph_objects as go                               # type: ignore
from django.conf import settings
import plotly.express as px                                     # type: ignore
from typing import Any
import pandas as pd

coordinates = {
    "Göttingen": (51.542674085238346, 9.913804090413405),
    "Heidelberg": (49.39899667646808, 8.672968635087408),
    "Essen": (51.45191841759816, 7.011888831333727),
    "Köln": (50.936388829448646, 6.958386355628797),
    "Frankfurt": (50.1153717270215, 8.687365774626162),
    "München": (48.13357641953071, 11.579255350658212),
    "Augsburg": (48.36831813866189, 10.900568819747098),
}

entity_dict = {"S3M": "BC", "S3P": "PDAC", "S3C": "CRC"}

token = settings.SETTINGS.MAPPLOT_TOKEN

class DashboardView(LoginRequiredMixin, TemplateView):

    def get(self,
            request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        template_name = "gui/dashboard.html"

        context = {
            "user": request.user,  # user, not username because we
            # need to check the user's attributes
            }

        return render(request, template_name, context=context)
