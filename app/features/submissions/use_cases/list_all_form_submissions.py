from app.features.submissions.exceptions import (
    SubmissionNotFoundException,
    SubmissionAccessDeniedException,
)


class ListAllFormSubmissionsUseCase:

    def __init__(self, submission_repository):
        self.submission_repository = submission_repository

    async def execute(self, form_id: str, user_id: str):
        form = await self.submission_repository.find_form_by_id(form_id)

        if not form:
            raise SubmissionNotFoundException("Formulário não encontrado.")

        if form.project.ownerId != user_id:
            raise SubmissionAccessDeniedException()

        return await self.submission_repository.list_by_form(form_id)