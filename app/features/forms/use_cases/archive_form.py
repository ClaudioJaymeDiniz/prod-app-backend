from datetime import datetime

from app.features.forms.exceptions import FormAccessDeniedException


class ArchiveFormUseCase:

    def __init__(self, form_repository):
        self.form_repository = form_repository

    async def execute(self, form_id: str, user_id: str):
        form = await self.form_repository.find_by_id_with_project(form_id)

        if not form or form.project.ownerId != user_id:
            raise FormAccessDeniedException()

        return await self.form_repository.update(
            form_id,
            {
                "deletedAt": datetime.now()
            }
        )