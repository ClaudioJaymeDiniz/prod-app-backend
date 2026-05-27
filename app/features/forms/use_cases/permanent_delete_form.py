from app.features.forms.exceptions import (
    FormAccessDeniedException,
    FormMustBeArchivedException,
)


class PermanentDeleteFormUseCase:

    def __init__(self, form_repository):
        self.form_repository = form_repository

    async def execute(self, form_id: str, user_id: str):
        form = await self.form_repository.find_by_id_with_project(form_id)

        if not form:
            return {
                "ok": True,
                "alreadyDeleted": True
            }

        if form.project.ownerId != user_id:
            raise FormAccessDeniedException()

        if form.deletedAt is None:
            raise FormMustBeArchivedException()

        await self.form_repository.delete_submissions_by_form(form_id)

        await self.form_repository.delete_permanent(form_id)

        return {
            "detail": "Formulário excluído com sucesso"
        }