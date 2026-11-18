"""
This view handles the sample tracking table site.
For rendering the template gui/all_samples.html is utilized.

The view's post function handles deletion of entries.
The 'get' as well as the 'post' function can accept
group filters within the HttpRequest as input
and return only the fields that belong to given groups.
"""
import ast
import logging

from ..utils.field_name_translator import verbose_to_field, field_to_verbose
from ..forms.forms import GroupFilterForm
from ..config.sections import section_dict
from ..models import (HistopathologicalSample,
                      PATIENT_IDENTIFIER_NAME,
                      SAMPLE_CODE_NAME)

from django.db.models.functions import Substr
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpRequest, HttpResponse
)
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.shortcuts import render
from typing import Any
from ..config.sample_table_interface import (column_filters_no_group,
                                             group_filter_extra_fields,
                                             exclude_from_ui)
from ..config.general import SAMPLE_CODE_CUSTOM_FIELD

app_log = logging.getLogger("s3sample")
exclude_from_ui_verbose = [field_to_verbose[name] for name in exclude_from_ui]
sample_code_name_verbose = field_to_verbose[SAMPLE_CODE_NAME]
patient_identifier_name_verbose = field_to_verbose[PATIENT_IDENTIFIER_NAME]

context_config_varibales = {
    "sample_code_name": sample_code_name_verbose,
    "patient_identifier_name": patient_identifier_name_verbose,
    "custom_sample_code": SAMPLE_CODE_CUSTOM_FIELD,
    "exclude_from_ui": exclude_from_ui_verbose,
    }


def adapt_list_for_group_filter_display(section_name, field_list: list):
    """
    Custom group filters
    If groups want to have fields displayed in the table,
    that don't belong to this group these fields can be added here.
    This only works if all other groups are filtered out.
    """
    if section_name in group_filter_extra_fields:
        field_list = group_filter_extra_fields[section_name] + field_list
    return field_list


field_dict_for_group_filters = {
    section: adapt_list_for_group_filter_display(
        section, section_dict[section]) for section in section_dict
        } | column_filters_no_group


class SomeSamplesView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        column_names = ast.literal_eval(
            request.GET.get("column_names")
        )

        limit = 100
        offset = int(request.GET.get("offset", 0))
        subset = slice(offset, offset + limit)

        column_names.remove(field_to_verbose[SAMPLE_CODE_NAME])
        column_names.insert(1, field_to_verbose[SAMPLE_CODE_NAME])

        print(column_names)

        field_names = [
            verbose_to_field[cn] for cn in column_names
        ]

        samples = list(
            HistopathologicalSample.objects.values(*field_names)[subset]
        )

        sample_codes = [sample[SAMPLE_CODE_NAME] for sample in samples]

        samples = [{field_to_verbose[key]:
                    value for key, value in
                    item.items()} for item in samples]

        has_more = len(samples) == limit

        sample_rows = zip(sample_codes, samples)

        context = {
            "sample_rows": sample_rows,
            "next_offset": offset + limit if has_more else None,
            "column_names": column_names,
        } | context_config_varibales

        return render(request, "gui/partials/table_row.html", context)


class AllSamplesView(LoginRequiredMixin, TemplateView):
    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        template_name = "gui/all_samples.html"
        column_names = []
        num_samples = HistopathologicalSample.objects.count()
        num_patients = HistopathologicalSample.objects.annotate(
            patient_code=Substr(PATIENT_IDENTIFIER_NAME, 1, 5)
        ).values("patient_code").distinct().count()

        if len(request.GET) == 0:
            if num_samples > 0:
                first_sample = HistopathologicalSample.objects.first()
                column_names = [
                    field.verbose_name
                    for field in first_sample._meta.fields
                ]
            filters = GroupFilterForm()
        else:
            filtered_form = GroupFilterForm(request.GET)
            if filtered_form.is_valid():
                column_names = get_filtered_column_names(
                    filtered_form.cleaned_data
                )
            filters = filtered_form

        column_names.remove(field_to_verbose[SAMPLE_CODE_NAME])
        column_names.insert(1, field_to_verbose[SAMPLE_CODE_NAME])

        context = {
            "num_samples": num_samples,
            "num_patients": num_patients,
            "column_names": column_names,
            "filters": filters,
            "user": request.user,
        } | context_config_varibales
        return render(request, template_name, context=context)

    @method_decorator(requires_csrf_token)
    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        template_name = "gui/all_samples.html"
        post_data = request.POST
        delete_id = int(post_data["id"])

        if HistopathologicalSample.objects.filter(id=delete_id).exists():

            delete_instance = HistopathologicalSample.objects.get(id=delete_id)
            sample_code = getattr(delete_instance, SAMPLE_CODE_NAME)
            delete_instance.delete()
            app_log.info(
                f"{request.user} deleted "
                f"{sample_code}")

        filtered_form = GroupFilterForm(post_data)
        num_samples = HistopathologicalSample.objects.count()
        num_patients = HistopathologicalSample.objects.annotate(
            patient_code=Substr(SAMPLE_CODE_NAME, 4, 5)
        ).values("patient_code").distinct().count()

        column_names = []
        if filtered_form.is_valid():
            column_names = get_filtered_column_names(
                filtered_form.cleaned_data
            )
        filters = filtered_form

        context = {
            "column_names": column_names,
            "num_samples": num_samples,
            "num_patients": num_patients,
            "filters": filters,
            "user": request.user,
        } | context_config_varibales
        return render(request, template_name, context=context)


def get_filtered_column_names(group_filter: dict[str, Any]):
    if HistopathologicalSample.objects.count() == 0:
        return []

    all_filters = ["id", SAMPLE_CODE_NAME]
    first_sample = HistopathologicalSample.objects.first()

    for group in group_filter:
        if group_filter[group]:
            all_filters += [field for field in
                            field_dict_for_group_filters[group]
                            if field not in all_filters]

    # column names need to have the verbose names
    column_names = []
    for field_name in all_filters:
        column_name = first_sample._meta.get_field(field_name).verbose_name
        if column_name not in column_names:
            column_names.append(
                column_name
                )

    return column_names
