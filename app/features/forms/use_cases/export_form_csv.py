import csv
import io

from app.features.forms.exceptions import FormAccessDeniedException
from app.features.forms.utils import (
    normalize_form_structure,
    field_value_from_submission,
)


class ExportFormCsvUseCase:

    def __init__(self, form_repository):
        self.form_repository = form_repository

    async def execute(self, form_id: str, user_id: str):
        form = await self.form_repository.find_by_id_with_project_and_submissions(
            form_id
        )

        if not form or form.project.ownerId != user_id:
            raise FormAccessDeniedException()

        output = io.StringIO()
        writer = csv.writer(output)

        header = [
            "Data de Envio",
            "E-mail"
        ]

        normalized_structure = normalize_form_structure(
            form.structure or []
        )

        field_labels = [
            field.get("label", field.get("fieldId", "Campo"))
            for field in normalized_structure
        ]

        header.extend(field_labels)
        writer.writerow(header)

        for submission in form.submissions:
            row = [
                submission.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
                submission.user.email if submission.user else "Anônimo"
            ]

            for field in normalized_structure:
                value = field_value_from_submission(
                    submission.formData or {},
                    field
                )

                row.append("" if value is None else value)

            writer.writerow(row)

        output.seek(0)

        return output.getvalue()