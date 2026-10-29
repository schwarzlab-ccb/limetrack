from ..models import HistopathologicalSample

verbose_to_field = {
            field.verbose_name: field.name
            for field in HistopathologicalSample._meta.get_fields()
            if hasattr(field, "verbose_name")
        }

field_to_verbose = {v: k for k, v in verbose_to_field.items()}
