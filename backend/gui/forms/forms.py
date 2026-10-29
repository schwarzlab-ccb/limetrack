from ..models import (HistopathologicalSample,
                      SAMPLE_CODE_NAME, PATIENT_IDENTIFIER_NAME)
from ..utils import model_to_form
from ..config.sections import verbose_section_names, section_dict
from ..config.sample_table_interface import (column_filters_verbose_names,
                                             exclude_from_ui)
from ..config.widgets import custom_widgets
from ..config.general import PROJECT_NAME
from tempus_dominus.widgets import DatePicker  # type: ignore
from django.forms import ModelForm
from django import forms

# documentation on DatePickers
# https://github.com/FlipperPA/django-tempus-dominus


# all displayed fields' names and verbose_names
all_field_verbose_names = []
all_field_names = []

# date_picker widgets for the form
date_pickers = {}

# exclude primary key "ID" & "created" field by slicing
# for we dont want them displayed or edited
all_fields = [field for field in HistopathologicalSample._meta.get_fields()
              if field.name.lower() not in exclude_from_ui]

for field in all_fields:
    all_field_verbose_names.append(field.verbose_name)
    all_field_names.append(field.name)
    # creation of DatePicker widgets for each DateField
    if field.get_internal_type() == "DateField":
        date_pickers.update(
            {
                field.name: DatePicker(
                    options={"allowInputToggle": True},
                    attrs={"input_group": False})
            })


# create dictionary for quickly finding a field by its name
field_dict = {field.name: field for field in all_fields}


class FlexibleSampleForm(ModelForm):
    """
    This form disables fields depending on the permissions a user has.

    """
    required_css_class = "required"
    # error_css_class = "error-field"

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        model_to_form.adapt_form(self, user, section_dict, field_dict)

    class Meta:
        model = HistopathologicalSample
        # exclude = ["id"]
        fields = all_field_names

        widgets = custom_widgets | date_pickers


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.xlsx', '.csv', '.xls']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class UploadForm(forms.Form):
    file = forms.FileField(help_text="Upload '.csv' or '.xlsx' files.",
                           allow_empty_file=False,
                           validators=[validate_file_extension])


class GroupFilterForm(forms.Form):
    """
    Enables filtering of the sample tables's columns by section and/or
    customly defined sets of data fields.
    The actual filtering is handled in samples_view.py
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, label in {**verbose_section_names,
                            **column_filters_verbose_names}.items():
            self.fields[name] = forms.BooleanField(
                initial=True, required=False, label=label)


class LoginForm(forms.Form):
    user_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class SearchForm(forms.Form):

    sample_code_verbose_name = \
        HistopathologicalSample._meta.get_field(SAMPLE_CODE_NAME).verbose_name
    patient_identifier_verbose_name = \
        HistopathologicalSample._meta.get_field(
            PATIENT_IDENTIFIER_NAME).verbose_name

    radio_select = forms.ChoiceField(
        choices=[
            (patient_identifier_verbose_name,
             f"{PROJECT_NAME} {patient_identifier_verbose_name}"),
            (sample_code_verbose_name, sample_code_verbose_name)],
        label="Search for",
        widget=forms.RadioSelect())

    search_field = forms.CharField(label="Search")
