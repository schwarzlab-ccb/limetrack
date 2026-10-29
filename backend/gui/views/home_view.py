from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render
from django.core.files import File
from django.http import (
    HttpRequest,
    HttpResponse
)
from typing import Any
from ..config.project_resources import (PROJECT_RESOURCES, DEFAULT_INFOTEXT,
                                        MEETINGS)


class HomeView(LoginRequiredMixin, TemplateView):
    def get(self,
            request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        template_name = "gui/home.html"
        context = {"project_resources": PROJECT_RESOURCES,
                   "default_infotext": DEFAULT_INFOTEXT,
                   "meetings": MEETINGS}

        with open("CHANGELOG.md", "r") as fh:
            myfile = File(fh)
            context["changelog"] = myfile.read()

        return render(request, template_name, context=context)
