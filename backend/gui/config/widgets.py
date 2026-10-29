from django import forms

# widgets with additional features
# include tooltips into widgets
custom_widgets = {

            "patient_identifier": forms.TextInput(
                attrs={"data-toggle": "tooltip",
                       "data-placement": "top",
                       "title": "5-digit SATURN3 pseudonym \
                        (by Treuhandstelle Freiburg)",
                       "onchange": "autoFillPatient(this.value)"}
                       ),

            "corresponding_organoid": forms.Select(
                attrs={"data-toggle": "tooltip",
                       "data-placement": "top",
                       "title": "Generated from the same biopsy/tissue piece"}
                       ),

            "dv_200": forms.TextInput(
                attrs={"data-toggle": "tooltip",
                       "data-placement": "top",
                       "title": "Quality measure: RNA \
                        molecules larger than 200 bp [%]"}
                        ),


            "tissue_quality": forms.NumberInput(
                attrs={
                    "data-toggle": "tooltip",
                    "data-placement": "top",
                    "title": "Value  between 1 and 5",
                    'min': 1, 'max': 5, 'type': 'number'}
            )
            }
