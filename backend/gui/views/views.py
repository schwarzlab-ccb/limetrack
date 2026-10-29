from ..forms.forms import (
    UploadForm, LoginForm,
    SearchForm,
    FlexibleSampleForm
)
from ..models import (HistopathologicalSample, SAMPLE_CODE_NAME,
                      PATIENT_IDENTIFIER_NAME)
from ..config.sections import patient_data_fields, section_dict
from ..config.general import SAMPLE_CODE_CUSTOM_FIELD
from ..utils.permission_manager import get_all_permitted_fields
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpRequest, HttpResponse, HttpResponseRedirect,
    QueryDict
)
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.forms.models import model_to_dict
from django.contrib import messages
from django.shortcuts import render
from django.forms import ModelForm
from django.urls import reverse
from django.contrib.auth.models import User
from typing import Any


import logging

app_log = logging.getLogger("s3sample")

# Create your views here.

visual_separation = [section_dict[section][0]
                     for section in section_dict]

constant_context = {"visual_separation": visual_separation,
                    "upload_form": UploadForm(),
                    "search_form": SearchForm(),
                    "custom_sample_field": SAMPLE_CODE_CUSTOM_FIELD,
                    "sample_code_name": SAMPLE_CODE_NAME
                    }


def get_form(
        user: User,
        data: QueryDict = None):

    return FlexibleSampleForm(data=data, user=user)


def check_existing_input_for_group(group_name: str,
                                   sample_code: str,
                                   update_dict: dict) -> bool:
    """
    Checks whether a group's specific fields already havey entries.
    """

    record = HistopathologicalSample.objects. \
        filter(**{SAMPLE_CODE_NAME: sample_code}).first()

    existing_fields = record._meta.get_fields()
    already_filled = False
    # TODO: think about iterating update_dict
    for field in existing_fields:
        if (field.name in update_dict):
            existing_field_value = getattr(record, field.name)
            new_field_value = update_dict[field.name]
            if (existing_field_value is not None
                and existing_field_value != ""  # for TextArea fields
                and str(existing_field_value) != str(new_field_value)
                and new_field_value is not None
                    and new_field_value != ""):  # for TextArea fields
                already_filled = True
                break

    return already_filled


def check_existing_entries(user: User,
                           sample_code: str, update_dict: dict) -> bool:
    """
    Checks whether a group's specific fields already has entries.
    Returns:
    - True if fields are already filled with different data
    - False if fields are not filled with different data
    """
    record = HistopathologicalSample.objects. \
        filter(**{SAMPLE_CODE_NAME: sample_code}).first()

    existing_fields = record._meta.get_fields()
    already_filled = False
    # TODO: think about iterating update_dict
    for field in existing_fields:
        if (field.name in update_dict):
            existing_field_value = getattr(record, field.name)
            new_field_value = update_dict[field.name]
            if (existing_field_value is not None
                and existing_field_value != ""  # for TextArea fields
                and str(existing_field_value) != str(new_field_value)
                and new_field_value is not None
                    and new_field_value != ""):  # for TextArea fields
                already_filled = True
                break

    return already_filled


def update_record(request: HttpRequest,
                  form, user: User,
                  data: dict, sample_code: str, tag: str):
    """
    Updates existing records in the db or returns error.

    If record with given sat3_code exists:
    Allows users to fill in data in the empty fields
    of their respective permissions.
    Edits a record's fields if the user has the permission to edit
    """
    if user.groups.first():
        group_name = user.groups.first().name.lower()
    else:
        group_name = ""

    update_dict = {}
    for field in get_all_permitted_fields(user):
        update_dict.update({field: data[field]})

    if (HistopathologicalSample.
            objects.filter(**{SAMPLE_CODE_NAME: sample_code}).exists()):

        has_entries = check_existing_entries(user, sample_code, update_dict)

        if (not request.user.has_perm("gui.change_histopathologicalsample") and
                has_entries):

            return record_already_exists(request,
                                         sample_code, tag, form, group_name)

        HistopathologicalSample.objects.filter(
            **{SAMPLE_CODE_NAME: sample_code}).update(
            **update_dict)

        if tag == "general":
            messages.success(request, "Submission successful!", extra_tags=tag)
            return HttpResponseRedirect(request.path_info)

    else:
        return no_sample_code_found(request, sample_code, tag, form)


def no_sample_code_found(request: HttpRequest,
                         sample_code: str,
                         tag: str,
                         form: ModelForm) -> HttpResponse:
    """
    Returns HttpResponse with error message stating that a
    input with given sat3_code is not possible.
    """

    if tag == "file":
        msg = f"File upload failed!" \
            f" No record with {SAMPLE_CODE_NAME} Sample Code " \
            f"{str(sample_code)} found."

    else:
        msg = f"Submission failed!" \
            f" No record with {SAMPLE_CODE_NAME} Sample Code " \
            f"{str(sample_code)} found."

    messages.error(request,
                   msg,
                   extra_tags=tag)

    return render(request, "gui/sample_tracking.html",
                  context={"form": (form if tag == "general"
                                    else get_form(request.user)),
                           "jump_to": ("form" if tag == "general" else None),
                           } | constant_context)


def record_already_exists(request: HttpRequest, sample_code: str,
                          tag: str, form, group_name: str) -> HttpResponse:
    """
    Returns HttpResponse with error message stating that a
    input with given sat3_code is not possible.
    TODO: change group name display into fields
    or section that is already filled / exist
    """
    if tag == "file":
        fail = "File upload failed!"
    else:
        fail = "Submission failed!"

    msg = f"{fail} {group_name} data for " \
        f"record with {SAMPLE_CODE_NAME} Sample Code " \
        f"{str(sample_code)} already exists and you \
            are not permitted to edit it."

    messages.error(request,
                   msg,
                   extra_tags=tag)

    return render(request, "gui/sample_tracking.html",
                  context={"form": (form if tag == "general"
                                    else get_form(request.user)),
                           "jump_to": ("form" if tag == "general" else None),
                           } | constant_context)


class SampleTrackingView(LoginRequiredMixin, TemplateView):
    def get(
            self,
            request: HttpRequest,
            *args: Any,
            **kwargs: Any
    ) -> HttpResponse:
        form = get_form(request.user)
        template_name = "gui/sample_tracking.html"
        context = {
            "form": form,
            "user": request.user.get_username(),
            "user_group": str(request.user.groups.first()).lower(),
        } | constant_context

        return render(request, template_name, context=context)

    @method_decorator(requires_csrf_token)
    def post(
            self,
            request: HttpRequest,
            *args: Any,
            **kwargs: Any
    ) -> HttpResponse:
        form = get_form(request.user, request.POST)

        if form.is_valid():
            data = form.cleaned_data
            sample_code = data[SAMPLE_CODE_NAME]
            app_log.info(
                f"{request.user} added / "
                f"edited data for patient "
                f"{sample_code}")

            return handle_form(
                form,
                sample_code,
                data,
                request,
                "general"
            )

        # if form is not valid:
        # return the form with input and highlight errors red
        else:
            messages.error(
                request,
                "Submission failed!",
                extra_tags="general"
            )

            for field in form.base_fields:
                if field in form.errors:
                    messages.error(
                        request,
                        form.errors[field],
                        extra_tags=field
                    )
                else:
                    messages.success(
                        request,
                        "Success!",
                        extra_tags=field
                    )
            return render(
                request,
                "gui/sample_tracking.html",
                context={
                    "jump_to": "form",
                    "form": form} | constant_context 
            )


def handle_form(form: ModelForm,
                sample_code: str,
                data: dict[str: Any],
                request: HttpRequest,
                tag: str):
    """
    Updates existing patient records
    or creates new patient records
    depending on group and user permissions.

    variables:
    tag = "general" or "file"
    indicating if it's submission by uploading
    a file or filling in the form

    """
    user = request.user

    if user.has_perm("gui.add_histopathologicalsample"):

        # TODO: here we maybe could check if it not exists and then
        # do the else part below
        # if it does exist we might only need the update_record function
        if (HistopathologicalSample.
            objects.filter(
                **{SAMPLE_CODE_NAME: sample_code}).exists()):

            if request.user.has_perm("gui.change_histopathologicalsample"):
                return update_record(request, form,
                                     request.user, data, sample_code, tag)

            else:
                update_dict = {}
                for field in get_all_permitted_fields(user):
                    update_dict.update({field: data[field]})
                if not check_existing_entries(user, sample_code, update_dict):
                    return update_record(request, form,
                                         request.user, data, sample_code, tag)
                else:
                    messages.error(request,
                                   "Submission failed!"
                                   f" Record with {SAMPLE_CODE_NAME} Sample Code "
                                   f"{str(sample_code)} already exists and \
                                      you are not permitted to edit it.",
                                   extra_tags=tag)

                    return render(
                        request, "gui/sample_tracking.html",
                        context={
                            "form": form,
                            "jump_to": (
                                "form" if tag == "general" else None)
                                } | constant_context)

        else:
            creation_dict = {}
            for field in get_all_permitted_fields(user):
                creation_dict.update({field: data[field]})

            # TODO: check if we could just give the creation dict
            # to a new instance of the form and do a form.save()
            # instead of the solution below
            # ATTENTION: CSV UPLOADS STILL NEED TO BE ADDED IN THIS WAY
            HistopathologicalSample.objects.filter(
               **{SAMPLE_CODE_NAME: sample_code}).create(
                **creation_dict)

    elif len(user.get_all_permissions()) > 0:
        # TODO: here we need a check if the user has any permissions at all.
        return update_record(request, form,
                             request.user,
                             data, sample_code, tag)

    # unauthorized users -> error message
    else:
        messages.error(request,
                       "Submission failed!"
                       " Not permitted!",
                       extra_tags=tag)

        return render(request, "gui/sample_tracking.html",
                      context={"form": form,
                               "jump_to": ("form" if tag == "general"
                                           else None)} | constant_context)

    if tag.lower() == "general":
        # if form's been input by using the webpages form
        messages.success(request, "Submission successful!", extra_tags=tag)
        return render(
                request,
                "gui/sample_tracking.html",
                context={
                    "jump_to": "form",
                    "form": get_form(request.user),
                } | constant_context
            )
    else:
        # if a CSV file's been submitted
        # we return None because we iterate multiple forms
        # returning a response would cancel the iteration prematurely
        return


def log_out(request: HttpRequest):
    logout(request)
    return HttpResponseRedirect(reverse("home"))


class LoginView(TemplateView):
    def get(self, request: HttpRequest,
            *args: Any, **kwargs: Any) -> HttpResponse:
        template_name = "gui/login.html"
        context = {
            "form": LoginForm(),
            "user": request.user.get_username()
        }
        return render(request, template_name, context=context)

    @method_decorator(requires_csrf_token)
    def post(self, request: HttpRequest,
             *args: Any, **kwargs: Any) -> HttpResponse:
        user_name = request.POST["user_name"]
        pw = request.POST["password"]
        user = authenticate(request, username=user_name, password=pw)
        if user is None:
            messages.error(
                        request, "Wrong password or user name.")
            return HttpResponseRedirect(request.path_info)
        else:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))


class SearchView(LoginRequiredMixin, TemplateView):
    def get(self, request: HttpRequest,
            *args: Any, **kwargs: Any) -> HttpResponse:
        form = get_form(request.user)
        template_name = "gui/sample_tracking.html"
        context = {
            "form": form,
            } | constant_context
        return render(request, template_name, context=context)

    @method_decorator(requires_csrf_token)
    def post(self, request: HttpRequest,
             *args: Any, **kwargs: Any) -> HttpResponse:
        search_form = SearchForm(request.POST)

        if search_form.is_valid():
            search = search_form.cleaned_data["search_field"]
            radio_select = search_form.cleaned_data["radio_select"]
            if (HistopathologicalSample.
                    objects.filter(**{SAMPLE_CODE_NAME: search}).exists()):

                found_record = HistopathologicalSample. \
                    objects.get(**{SAMPLE_CODE_NAME: search})
                model_dict = model_to_dict(found_record)
                model_dict.pop("id")
                form = get_form(request.user, model_dict)

            elif (HistopathologicalSample.
                    objects.filter(
                        **{PATIENT_IDENTIFIER_NAME: search}).exists()):

                found_records = HistopathologicalSample. \
                    objects.filter(**{PATIENT_IDENTIFIER_NAME: search})
                found_record = found_records[0]

                model_dict = model_to_dict(found_record)
                model_dict.pop("id")

                # only include patient data, not sample data
                for key in model_dict:
                    if key not in patient_data_fields:
                        model_dict[key] = ""

                form = get_form(request.user,
                                model_dict)

            else:
                messages.error(request,
                               f"DID NOT FIND {radio_select} {search}",
                               extra_tags="general")
                return HttpResponseRedirect(reverse("sample_tracking"))

            messages.success(
                request,
                f"FOUND {radio_select} {search}", extra_tags="general")
            template_name = "gui/sample_tracking.html"
            context = {
                "jump_to": "form",
                "form": form,
            } | constant_context

            return render(request, template_name, context=context)

        else:
            messages.error(request, "Invalid input",
                           extra_tags="general")
            return HttpResponseRedirect(reverse("sample_tracking"))
