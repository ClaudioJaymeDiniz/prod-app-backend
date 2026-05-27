from app.features.forms.utils import normalize_form_structure
from app.features.forms.services.form_validation_service import FormValidationService

from app.features.submissions.exceptions import (
    SubmissionNotFoundException,
    SubmissionAccessDeniedException,
    SubmissionUpdatePayloadException,
    InvalidSubmissionDataException,
)


class UpdateSubmissionUseCase:

    def __init__(self, submission_repository):
        self.submission_repository = submission_repository

    async def execute(self, submission_id: str, data, user_id: str):
        submission = await self.submission_repository.find_by_id_with_form(
            submission_id
        )

        if not submission:
            raise SubmissionNotFoundException()

        if submission.userId != user_id:
            raise SubmissionAccessDeniedException()

        if data.formData is None:
            raise SubmissionUpdatePayloadException()

        structure = normalize_form_structure(
            submission.form.structure or []
        )

        try:
            FormValidationService.validate(
                structure=structure,
                form_data=data.formData
            )
        except ValueError as error:
            raise InvalidSubmissionDataException(error.args[0])

        return await self.submission_repository.update(
            submission_id,
            {
                "formData": data.formData
            }
        )