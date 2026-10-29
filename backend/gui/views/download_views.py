import logging
import json
import csv

import pandas as pd

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpRequest,
    HttpResponseRedirect,
    StreamingHttpResponse,
    HttpResponse,
)
from django.views.generic import TemplateView
from typing import Any, Generator, Iterable
from base64 import b64encode
from io import BytesIO
from ..forms.forms import all_field_verbose_names
from ..config.example_sample import example_sample

app_log = logging.getLogger("s3sample")

class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    @staticmethod
    def write(value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def csv_template_download_csv(request: HttpRequest):
    pseudo_buffer = Echo()
    filename = "sample_tracker_template.csv"
    data: list[Iterable[Any]] = [all_field_verbose_names, example_sample]
    writer = csv.writer(pseudo_buffer)

    return StreamingHttpResponse(
        (writer.writerow(row) for row in data),
        content_type="text/csv",
        headers={
            "Content-Disposition":
            f"attachment; filename={filename}"},
    )


def csv_template_download_excel(request: HttpRequest):
    data = [example_sample]
    columns = all_field_verbose_names
    filename = "sample_tracker_template.xlsx"
    generator: Generator | None = None
    buffer = BytesIO()

    with BytesIO() as buffer:
        pd.DataFrame(data, columns=columns).to_excel(
            buffer, index=False
        )
        buffer.seek(0)
        generator = (line for line in buffer.readlines())

    return StreamingHttpResponse(
        generator,
        content_type="application/vnd.ms-excel",
        headers={
            "Content-Disposition":
            f"attachment; filename={filename}"},
    )


class FilteredDownloadView(LoginRequiredMixin, TemplateView):
    def post(self,
             request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
        data = request.POST.get("data")
        file_type = request.GET.get("type", "CSV")

        if data:
            records: list[dict] = json.loads(data)
            df = pd.DataFrame.from_records(records)
            content_type = "text/csv;base64"

            with BytesIO() as buffer:
                file_name = "sample_tracker_samples"

                if file_type == "Excel":
                    file_name += ".xlsx"
                    content_type = "text/plain;base64"
                    df.to_excel(buffer, index=False)

                else:
                    file_name += ".csv"
                    df.to_csv(buffer, index=False)

                buffer.seek(0)
                response = HttpResponse(
                    b64encode(buffer.read()),
                    content_type=content_type,
                    headers={
                        "Content-Disposition":
                        f'attachment; filename="{file_name}"',
                        "filename": file_name
                    },
                )

            return response

        return HttpResponseRedirect("/samples/")
