import traceback
from app.features.forms.utils import normalize_form_structure
from app.features.forms.services.form_validation_service import FormValidationService

from app.features.submissions.exceptions import (
    InvalidSubmissionPayloadException,
    InvalidSubmissionDataException,
    SubmissionAlreadyExistsException,
    SubmissionCreateException,
    SubmissionNotFoundException,
    FormNotAvailableForSubmissionException,
)
from app.infrastructure.mail.mail_service import send_submission_notification


class CreateSubmissionUseCase:

    def __init__(self, submission_repository, project_access_service):
        self.submission_repository = submission_repository
        self.project_access_service = project_access_service

    async def execute(self, data: dict, user_id: str, user_email: str):
        submission_id = data.get("id")
        form_id = data.get("formId")
        form_data = data.get("formData")

        if not submission_id or not form_id or form_data is None:
            raise InvalidSubmissionPayloadException()

        try:
            form = await self.submission_repository.find_form_by_id(form_id)

            if not form:
                raise SubmissionNotFoundException("Formulário não encontrado.")

            if form.project and form.project.deletedAt is not None:
                raise FormNotAvailableForSubmissionException()

            structure = normalize_form_structure(form.structure or [])

            try:
                FormValidationService.validate(
                    structure=structure,
                    form_data=form_data
                )
            except ValueError as error:
                raise InvalidSubmissionDataException(error.args[0])

            if not form.isPublic:
                await self.project_access_service.ensure_can_submit_to_project(
                    form.projectId,
                    user_id,
                    user_email
                )

            submission = await self.submission_repository.create(
                {
                    "id": submission_id,
                    "formData": form_data,
                    "user": {
                        "connect": {
                            "id": user_id
                        }
                    },
                    "form": {
                        "connect": {
                            "id": form_id
                        }
                    }
                }
            )

            await self._notify_owner(form_id)

            return submission

        except (
            InvalidSubmissionPayloadException,
            InvalidSubmissionDataException,
            SubmissionAlreadyExistsException,
            SubmissionNotFoundException,
            FormNotAvailableForSubmissionException,
        ):
            raise

        except Exception as error:
            error_message = str(error)

            print(f"Erro crítico ao criar submissão no Prisma: {error_message}")
            print(traceback.format_exc())

            if "Unique constraint failed" in error_message and "id" in error_message:
                raise SubmissionAlreadyExistsException()

            raise SubmissionCreateException()

    async def _notify_owner(self, form_id: str):
        form_info = await self.submission_repository.find_form_with_project_owner(
            form_id
        )

        if not form_info:
            return

        if not form_info.project or not form_info.project.owner:
            return

        owner_email = form_info.project.owner.email

        if not owner_email:
            return

        try:
            await send_submission_notification(
                owner_email=owner_email,
                project_name=form_info.project.name,
                form_title=form_info.title
            )
        except Exception as error:
            print(f"⚠️ Erro ao enviar notificação: {error}")