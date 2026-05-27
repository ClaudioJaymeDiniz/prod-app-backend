import traceback

from app.features.submissions.exceptions import (
    InvalidSubmissionPayloadException,
    SubmissionAlreadyExistsException,
    SubmissionCreateException,
    SubmissionNotFoundException,
    FormNotAvailableForSubmissionException,
)
from app.infrastructure.mail.mail_service import send_submission_notification


class CreateSubmissionUseCase:

    def __init__(self, submission_repository, invitation_repository):
        self.submission_repository = submission_repository
        self.invitation_repository = invitation_repository

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

            if not form.isPublic:
                await self._check_project_access(
                    project_id=form.projectId,
                    user_id=user_id,
                    user_email=user_email
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

    async def _check_project_access(
        self,
        project_id: str,
        user_id: str,
        user_email: str
    ):
        project = await self.invitation_repository.find_project_by_id(
            project_id
        )

        if not project:
            raise SubmissionNotFoundException("Formulário não encontrado.")

        if project.ownerId == user_id:
            return

        accepted_invitation = (
            await self.invitation_repository
            .find_accepted_by_project_and_email(
                project_id,
                user_email
            )
        )

        if accepted_invitation:
            return

        raise SubmissionNotFoundException("Formulário não encontrado.")

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