from app.features.submissions.exceptions import SubmissionNotFoundException


class ListFormSubmissionsUseCase:

    def __init__(self, submission_repository):
        self.submission_repository = submission_repository

    async def execute(self, form_id: str, user_id: str):
        form = await self.submission_repository.find_form_by_id(form_id)

        if not form:
            raise SubmissionNotFoundException("Formulário não encontrado.")

        if form.project.ownerId == user_id:
            return await self.submission_repository.list_by_form(form_id)

        return await self.submission_repository.list_by_form_and_user(
            form_id,
            user_id
        )