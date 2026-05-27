from app.features.forms.exceptions import FormAccessDeniedException
from app.features.forms.utils import normalize_form_structure


class UpdateFormUseCase:

    def __init__(self, form_repository):
        self.form_repository = form_repository

    async def execute(self, form_id: str, data, user_id: str):
        form = await self.form_repository.find_by_id_with_project(form_id)

        if not form or form.project.ownerId != user_id:
            raise FormAccessDeniedException()

        update_data = {}

        if data.title is not None:
            update_data["title"] = data.title

        if data.description is not None:
            update_data["description"] = data.description

        if data.isPublic is not None:
            update_data["isPublic"] = data.isPublic

        if data.structure is not None:
            update_data["structure"] = normalize_form_structure(
                [
                    field.model_dump()
                    for field in data.structure
                ]
            )

        return await self.form_repository.update(
            form_id,
            update_data
        )